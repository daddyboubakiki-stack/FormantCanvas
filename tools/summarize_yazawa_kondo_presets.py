#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('input_json', type=Path)
ap.add_argument('output_csv', type=Path)
args = ap.parse_args()

data = json.loads(args.input_json.read_text(encoding='utf-8'))
rows = []
for p in data['presets']:
    first = p['trajectory'][0]
    last = p['trajectory'][-1]
    rows.append({
        'id': p['id'],
        'sex': p['sex'],
        'context': p['context_label'],
        'vowel': p['vowel'],
        'length': p['length'],
        'n_speakers': p['n_speakers'],
        'raw_tokens': p['raw_tokens'],
        'duration_mean_ms': p['duration_ms']['mean'],
        'duration_sd_speaker_means_ms': p['duration_ms']['sd_across_speaker_means'],
        'F1_midpoint_hz': p['midpoint_hz']['F1'],
        'F2_midpoint_hz': p['midpoint_hz']['F2'],
        'F3_midpoint_hz': p['midpoint_hz']['F3'],
        'F1_sd_speaker_means_hz': p['midpoint_sd_across_speaker_means_hz']['F1'],
        'F2_sd_speaker_means_hz': p['midpoint_sd_across_speaker_means_hz']['F2'],
        'F3_sd_speaker_means_hz': p['midpoint_sd_across_speaker_means_hz']['F3'],
        'F1_at_20pct_hz': first['F1_hz'],
        'F2_at_20pct_hz': first['F2_hz'],
        'F3_at_20pct_hz': first['F3_hz'],
        'F1_at_80pct_hz': last['F1_hz'],
        'F2_at_80pct_hz': last['F2_hz'],
        'F3_at_80pct_hz': last['F3_hz'],
        'delta_F1_20_to_80_hz': round(last['F1_hz'] - first['F1_hz'], 3),
        'delta_F2_20_to_80_hz': round(last['F2_hz'] - first['F2_hz'], 3),
        'delta_F3_20_to_80_hz': round(last['F3_hz'] - first['F3_hz'], 3),
    })

args.output_csv.parent.mkdir(parents=True, exist_ok=True)
with args.output_csv.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print('SUMMARY_ROWS', len(rows))
print('WROTE', args.output_csv)
