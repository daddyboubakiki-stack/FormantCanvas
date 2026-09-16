#!/usr/bin/env python3
"""Build speaker-balanced adult Japanese vowel presets from Yazawa & Kondo data.

Input: JPLongShortVowels.csv from Zenodo record 15227304 (v3).
Output: JSON containing 40 presets: sex x position x V1 (10 short/long vowels).

Aggregation is deliberately speaker-balanced:
1. Mean all tokens for each speaker within a condition.
2. Mean those speaker means equally within sex/position/V1.
3. Report sample SD across the 8 speaker means.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

SOURCE_MD5 = "56ffdcaab756399e7d9f846ccb091860"
SOURCE_DOI = "10.5281/zenodo.15227304"
SOURCE_RECORD = "https://zenodo.org/records/15227304"
SOURCE_FILE = "JPLongShortVowels.csv"
VOWELS = ("i", "e", "a", "o", "u")
LONG_TO_SHORT = {v + v: v for v in VOWELS}
NUMERIC = ["Duration", "F1_Midpoint", "F2_Midpoint", "F3_Midpoint"] + [
    f"F{formant}_{i}" for formant in (1, 2, 3) for i in range(1, 31)
]
REQUIRED = ["Speaker", "Gender", "Position", "V1", *NUMERIC]


def fmean(values):
    values = [v for v in values if v is not None and math.isfinite(v)]
    return statistics.fmean(values) if values else None


def fsd(values):
    values = [v for v in values if v is not None and math.isfinite(v)]
    return statistics.stdev(values) if len(values) >= 2 else None


def r(value, digits=3):
    return None if value is None else round(value, digits)


def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing_cols = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing_cols:
            raise SystemExit(f"Missing required columns: {missing_cols}")
        rows = []
        for raw in reader:
            row = dict(raw)
            for col in NUMERIC:
                text = row[col].strip()
                row[col] = float(text) if text else None
            rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("output_json", type=Path)
    args = ap.parse_args()

    source_md5 = md5sum(args.csv_path)
    if source_md5 != SOURCE_MD5:
        raise SystemExit(f"Source MD5 mismatch: expected {SOURCE_MD5}, got {source_md5}")

    rows = load(args.csv_path)
    if len(rows) != 3200:
        raise SystemExit(f"Expected 3200 rows, got {len(rows)}")

    genders = sorted({x["Gender"] for x in rows})
    positions = sorted({x["Position"] for x in rows})
    v1s = sorted({x["V1"] for x in rows})
    speakers = sorted({x["Speaker"] for x in rows})
    if genders != ["F", "M"]:
        raise SystemExit(f"Unexpected Gender values: {genders}")
    if positions != ["embedded", "isolated"]:
        raise SystemExit(f"Unexpected Position values: {positions}")
    expected_v1 = sorted(list(VOWELS) + [v + v for v in VOWELS])
    if v1s != expected_v1:
        raise SystemExit(f"Unexpected V1 values: {v1s}")
    if len(speakers) != 16:
        raise SystemExit(f"Expected 16 speakers, got {len(speakers)}")

    gender_speakers = {
        g: sorted({x["Speaker"] for x in rows if x["Gender"] == g}) for g in genders
    }
    if any(len(v) != 8 for v in gender_speakers.values()):
        raise SystemExit(f"Expected 8 speakers per gender, got {gender_speakers}")

    # Raw rows -> speaker-condition buckets.
    speaker_buckets = defaultdict(list)
    raw_condition_counts = defaultdict(int)
    for row in rows:
        condition = (row["Gender"], row["Position"], row["V1"])
        raw_condition_counts[condition] += 1
        speaker_buckets[condition + (row["Speaker"],)].append(row)

    if len(raw_condition_counts) != 40:
        raise SystemExit(f"Expected 40 conditions, got {len(raw_condition_counts)}")
    bad_counts = {k: v for k, v in raw_condition_counts.items() if v != 80}
    if bad_counts:
        raise SystemExit(f"Expected 80 raw tokens per condition: {bad_counts}")

    # Build a numeric mean for every speaker within every condition.
    speaker_means = {}
    token_counts = {}
    for key, bucket in speaker_buckets.items():
        token_counts[key] = len(bucket)
        speaker_means[key] = {col: fmean([x[col] for x in bucket]) for col in NUMERIC}
    bad_speaker_counts = {k: v for k, v in token_counts.items() if v != 10}
    if bad_speaker_counts:
        raise SystemExit(f"Expected 10 tokens per speaker-condition: {bad_speaker_counts}")

    positions_normalized = [0.20 + i * (0.60 / 29) for i in range(30)]
    presets = []
    for gender in ("M", "F"):
        for position in ("isolated", "embedded"):
            for v1 in ("i", "ii", "e", "ee", "a", "aa", "o", "oo", "u", "uu"):
                speakers_here = gender_speakers[gender]
                means = [speaker_means[(gender, position, v1, sp)] for sp in speakers_here]
                group_mean = {col: fmean([m[col] for m in means]) for col in NUMERIC}
                group_sd = {col: fsd([m[col] for m in means]) for col in NUMERIC}

                is_long = len(v1) == 2
                vowel = LONG_TO_SHORT.get(v1, v1)
                sex = "male" if gender == "M" else "female"
                context = position
                trajectory = []
                for i, p in enumerate(positions_normalized, start=1):
                    trajectory.append({
                        "sample_index": i,
                        "position_normalized": r(p, 6),
                        "F1_hz": r(group_mean[f"F1_{i}"]),
                        "F2_hz": r(group_mean[f"F2_{i}"]),
                        "F3_hz": r(group_mean[f"F3_{i}"]),
                        "F1_sd_across_speaker_means_hz": r(group_sd[f"F1_{i}"]),
                        "F2_sd_across_speaker_means_hz": r(group_sd[f"F2_{i}"]),
                        "F3_sd_across_speaker_means_hz": r(group_sd[f"F3_{i}"]),
                    })

                presets.append({
                    "id": f"ja_yk2019_{sex}_{context}_{'long' if is_long else 'short'}_{vowel}",
                    "language": "ja",
                    "population": "adult",
                    "sex": sex,
                    "source_position": position,
                    "context_label": "carrier_sentence" if position == "embedded" else "isolated_word",
                    "vowel": vowel,
                    "source_v1": v1,
                    "length": "long" if is_long else "short",
                    "n_speakers": len(speakers_here),
                    "raw_tokens": raw_condition_counts[(gender, position, v1)],
                    "tokens_per_speaker": 10,
                    "duration_ms": {
                        "mean": r(group_mean["Duration"]),
                        "sd_across_speaker_means": r(group_sd["Duration"]),
                    },
                    "midpoint_hz": {
                        "F1": r(group_mean["F1_Midpoint"]),
                        "F2": r(group_mean["F2_Midpoint"]),
                        "F3": r(group_mean["F3_Midpoint"]),
                    },
                    "midpoint_sd_across_speaker_means_hz": {
                        "F1": r(group_sd["F1_Midpoint"]),
                        "F2": r(group_sd["F2_Midpoint"]),
                        "F3": r(group_sd["F3_Midpoint"]),
                    },
                    "trajectory": trajectory,
                })

    missing_numeric_cells = sum(1 for row in rows for col in NUMERIC if row[col] is None)
    payload = {
        "schema_version": "1.0.0",
        "generated_for": "Formantasia / FormantCanvas",
        "source": {
            "dataset_title": "Japanese Vowel Length Acoustic Data",
            "dataset_version": "v3",
            "creator": "Kakeru Yazawa",
            "reported_study": "Yazawa & Kondo (2019), Acoustic characteristics of Japanese short and long vowels: Formant displacement effect revisited",
            "record_url": SOURCE_RECORD,
            "doi": SOURCE_DOI,
            "file": SOURCE_FILE,
            "file_md5": SOURCE_MD5,
            "license": "CC BY 4.0",
        },
        "population": {
            "description": "16 native speakers of Tokyo Japanese, ages 21-30",
            "male_speakers": 8,
            "female_speakers": 8,
        },
        "measurement": {
            "duration_unit": "ms",
            "formant_unit": "Hz",
            "midpoint": "temporal midpoint of each vowel interval",
            "trajectory_points": 30,
            "trajectory_source_window": "central 60% of vowel interval",
            "trajectory_nominal_window_normalized": [0.20, 0.80],
            "position_mapping_note": "The source stores points as Fn_1..Fn_30 and describes them as 30 equidistant points within the central 60%. Formantasia maps indices linearly from 0.20 through 0.80 for display. No measured 0-20% or 80-100% endpoint values are claimed.",
        },
        "aggregation": {
            "unit_of_equal_weight": "speaker",
            "step_1": "For each sex x position x V1 condition, average the 10 raw tokens within each speaker.",
            "step_2": "Average the 8 speaker means with equal speaker weight.",
            "uncertainty": "Sample SD across the 8 speaker means.",
            "condition_dimensions": ["sex", "position", "V1"],
            "conditions": 40,
        },
        "qc": {
            "raw_rows": len(rows),
            "speakers": len(speakers),
            "conditions": len(raw_condition_counts),
            "raw_tokens_per_condition": 80,
            "tokens_per_speaker_condition": 10,
            "missing_numeric_cells": missing_numeric_cells,
            "source_md5_verified": True,
        },
        "presets": presets,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("BUILT", args.output_json)
    print("PRESETS", len(presets))
    print("QC", json.dumps(payload["qc"], ensure_ascii=False, sort_keys=True))
    # A few anchor values make later regression checking easy.
    for pid in (
        "ja_yk2019_male_isolated_short_a",
        "ja_yk2019_male_isolated_long_a",
        "ja_yk2019_female_isolated_short_a",
        "ja_yk2019_female_isolated_long_a",
    ):
        p = next(x for x in presets if x["id"] == pid)
        print("ANCHOR", pid, "duration_ms", p["duration_ms"]["mean"], "midpoint", p["midpoint_hz"])


if __name__ == "__main__":
    main()
