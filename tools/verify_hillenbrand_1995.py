#!/usr/bin/env python3
"""Independently verify Formantasia's Hillenbrand et al. (1995) trajectory data.

Checks, without reusing build_hillenbrand.py:
1. data/hillenbrand_1995_trajectories.json against group means recomputed
   from the source bigdata.dat (all groups, vowels, 10-80% points, F1-F3, n).
2. The HILLENBRAND_1995 constants inlined in index.html against that JSON.

Usage:
  python3 tools/verify_hillenbrand_1995.py               # downloads h95-alldata.zip
  python3 tools/verify_hillenbrand_1995.py path/to/bigdata.dat
Exit status is non-zero on any mismatch.
"""

from __future__ import annotations

import io
import json
import re
import statistics
import sys
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data" / "hillenbrand_1995_trajectories.json"
HTML_PATH = ROOT / "index.html"
SOURCE_ZIP = "https://raw.githubusercontent.com/santiagobarreda/hillenbrand_et_al_1995/main/h95-alldata.zip"
GROUPS = {"m": "male", "w": "female", "b": "boy", "g": "girl"}
APP_KEYS = {"eI": "ey", "oU": "oa"}  # index.html key -> dataset vowel key
TOL = 0.051  # values are stored rounded to 0.1


def load_bigdata(argv: list[str]) -> str:
    if argv:
        return Path(argv[0]).read_text(encoding="latin-1")
    req = urllib.request.Request(SOURCE_ZIP, headers={"User-Agent": "Formantasia-Hillenbrand-verify/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, zipfile.ZipFile(io.BytesIO(resp.read())) as zf:
        name = next(n for n in zf.namelist() if Path(n).name.lower() == "bigdata.dat")
        return zf.read(name).decode("latin-1")


def source_rows(text: str):
    for line in text.splitlines():
        p = line.split()
        if len(p) == 30 and len(p[0]) == 5 and p[0][0] in GROUPS and p[0][1:3].isdigit():
            yield p


def main(argv: list[str]) -> int:
    rows = list(source_rows(load_bigdata(argv)))
    problems: list[str] = []
    if len(rows) != 1668:
        problems.append(f"expected 1668 source rows, found {len(rows)}")

    grouped = defaultdict(list)
    for r in rows:
        vowel = r[0][3:5]
        grouped[(GROUPS[r[0][0]], "ey" if vowel == "ei" else vowel)].append(r)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    checked = 0
    for (group, vowel), subset in grouped.items():
        entry = data["groups"][group][vowel]
        if entry["token_n"] != len(subset):
            problems.append(f"{group}/{vowel}: token_n {entry['token_n']} != {len(subset)}")
        dur = statistics.fmean(float(r[1]) for r in subset)
        if abs(dur - entry["mean_duration_ms"]) > TOL:
            problems.append(f"{group}/{vowel}: duration {entry['mean_duration_ms']} != {dur:.3f}")
        for i, point in enumerate(entry["points"]):
            for k, formant in enumerate(("F1", "F2", "F3")):
                vals = [float(r[6 + i * 3 + k]) for r in subset if float(r[6 + i * 3 + k]) != 0]
                mean = statistics.fmean(vals) if vals else None
                checked += 1
                stored = point[formant]
                if (mean is None) != (stored is None) or (mean is not None and abs(mean - stored) > TOL):
                    problems.append(f"{group}/{vowel} {point['pct']}% {formant}: {stored} != {mean}")
                if point["n"][formant] != len(vals):
                    problems.append(f"{group}/{vowel} {point['pct']}% {formant}: n {point['n'][formant]} != {len(vals)}")

    html = HTML_PATH.read_text(encoding="utf-8")
    block = re.search(r"const HILLENBRAND_1995 = \{(.*?)\n  \};", html, re.S)
    inline = 0
    if not block:
        problems.append("HILLENBRAND_1995 constant not found in index.html")
    else:
        for group in ("male", "female"):
            gblock = re.search(group + r":\{(.*?)\n    \}", block.group(1), re.S)
            for app_key, vowel in APP_KEYS.items():
                vblock = re.search(app_key + r":\{duration:([\d.]+),n:(\d+),points:\[(.*?)\]\}", gblock.group(1), re.S)
                entry = data["groups"][group][vowel]
                if int(vblock.group(2)) != entry["token_n"] or abs(float(vblock.group(1)) * 1000 - entry["mean_duration_ms"]) > TOL:
                    problems.append(f"index.html {group}/{app_key}: n/duration differ from JSON")
                pts = re.findall(r"\{p:([\d.]+),F1:([\d.]+),F2:([\d.]+),F3:([\d.]+)\}", vblock.group(3))
                for (p, f1, f2, f3), ref in zip(pts, entry["points"], strict=True):
                    for name, val in (("F1", f1), ("F2", f2), ("F3", f3)):
                        inline += 1
                        if abs(float(p) - ref["t"]) > 1e-9 or float(val) != ref[name]:
                            problems.append(f"index.html {group}/{app_key} {ref['pct']}% {name}: {val} != {ref[name]}")

    for line in problems:
        print("MISMATCH", line)
    print(f"source rows {len(rows)}; JSON values checked {checked}; index.html values checked {inline}; mismatches {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
