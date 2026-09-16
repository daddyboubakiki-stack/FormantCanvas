#!/usr/bin/env python3
import csv
import json
import sys
import urllib.request

path = sys.argv[1]
with open(path, newline='', encoding='utf-8-sig') as f:
    r = csv.DictReader(f)
    rows = list(r)

print('ROW_COUNT', len(rows))
print('COLUMNS', repr(r.fieldnames))
print('FIRST_ROW', {k: rows[0][k] for k in r.fieldnames})

# Print low-cardinality columns so the categorical coding can be mapped exactly.
for col in r.fieldnames:
    vals = sorted({row[col] for row in rows})
    if len(vals) <= 30:
        print('UNIQUE', col, len(vals), repr(vals))

# Detect formant trajectory columns by their names.
for stem in ('F1', 'F2', 'F3'):
    cols = [c for c in r.fieldnames if c.startswith(stem)]
    print('FORMANT_COLUMNS', stem, len(cols), repr(cols))

# Record current Zenodo rights metadata as an additional provenance check.
with urllib.request.urlopen('https://zenodo.org/api/records/15227304') as response:
    meta = json.load(response)
print('ZENODO_VERSION', meta.get('metadata', {}).get('version'))
print('ZENODO_RIGHTS', repr(meta.get('metadata', {}).get('rights')))
