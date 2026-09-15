#!/usr/bin/env python3
"""Build compact Hillenbrand et al. (1995) trajectory means for FormantCanvas."""

from __future__ import annotations

import io
import json
import math
import statistics
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

SOURCE_REPO = "https://github.com/santiagobarreda/hillenbrand_et_al_1995"
SOURCE_ZIP = "https://raw.githubusercontent.com/santiagobarreda/hillenbrand_et_al_1995/main/h95-alldata.zip"
OUT = Path(__file__).resolve().parents[1] / "data" / "hillenbrand_1995_trajectories.json"
PCTS = tuple(range(10, 90, 10))
FORMANTS = ("F1", "F2", "F3")
TYPE_NAMES = {"m": "male", "w": "female", "b": "boy", "g": "girl"}
SOURCE_TO_CANONICAL_VOWEL = {"ei": "ey"}
VOWEL_LABELS = {
    "ae": {"word": "had", "ipa": "æ"},
    "ah": {"word": "hod", "ipa": "ɑ"},
    "aw": {"word": "hawed", "ipa": "ɔ"},
    "eh": {"word": "head", "ipa": "ɛ"},
    "er": {"word": "heard", "ipa": "ɝ"},
    "ey": {"word": "hayed", "ipa": "eɪ"},
    "ih": {"word": "hid", "ipa": "ɪ"},
    "iy": {"word": "heed", "ipa": "i"},
    "oa": {"word": "hoed", "ipa": "oʊ"},
    "oo": {"word": "hood", "ipa": "ʊ"},
    "uh": {"word": "hud", "ipa": "ʌ"},
    "uw": {"word": "who'd", "ipa": "u"},
}


def fetch_zip() -> bytes:
    req = urllib.request.Request(SOURCE_ZIP, headers={"User-Agent": "FormantCanvas-Hillenbrand-builder/1.2"})
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def find_bigdata(zf: zipfile.ZipFile) -> str:
    candidates = [name for name in zf.namelist() if Path(name).name.lower() == "bigdata.dat"]
    if not candidates:
        raise RuntimeError("bigdata.dat not found in h95-alldata.zip")
    return candidates[0]


def parse_rows(text: str):
    started = False
    for raw in text.splitlines():
        parts = raw.strip().split()
        if not parts:
            continue
        if not started:
            if parts[0].lower() == "b01ae":
                started = True
            else:
                continue
        if len(parts) != 30:
            raise ValueError(f"Expected 30 columns, got {len(parts)}: {raw[:100]}")
        filename = parts[0].lower()
        speaker_code = filename[0]
        source_vowel = filename[3:5]
        vowel = SOURCE_TO_CANONICAL_VOWEL.get(source_vowel, source_vowel)
        nums = [float(x) for x in parts[1:]]
        duration_ms = nums[0]
        dynamic = nums[5:]
        points = {}
        for i, pct in enumerate(PCTS):
            triplet = dynamic[i * 3 : i * 3 + 3]
            points[pct] = {f: (None if value == 0 else value) for f, value in zip(FORMANTS, triplet)}
        yield {
            "filename": filename,
            "speaker_code": speaker_code,
            "speaker_type": TYPE_NAMES[speaker_code],
            "source_vowel": source_vowel,
            "vowel": vowel,
            "duration_ms": duration_ms,
            "points": points,
        }


def rounded_mean(values):
    valid = [v for v in values if v is not None and math.isfinite(v)]
    return (round(statistics.fmean(valid), 1), len(valid)) if valid else (None, 0)


def aggregate(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["speaker_type"], row["vowel"])].append(row)
    result = {}
    for speaker_type in TYPE_NAMES.values():
        result[speaker_type] = {}
        for vowel, labels in VOWEL_LABELS.items():
            subset = groups[(speaker_type, vowel)]
            points = []
            for pct in PCTS:
                item = {"t": pct / 100, "pct": pct}
                counts = {}
                for formant in FORMANTS:
                    mean, n = rounded_mean(r["points"][pct][formant] for r in subset)
                    item[formant] = mean
                    counts[formant] = n
                item["n"] = counts
                points.append(item)
            result[speaker_type][vowel] = {
                **labels,
                "source_code": sorted({r["source_vowel"] for r in subset}),
                "token_n": len(subset),
                "mean_duration_ms": round(statistics.fmean(r["duration_ms"] for r in subset), 1),
                "points": points,
            }
    return result


def main():
    archive = fetch_zip()
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        member = find_bigdata(zf)
        text = zf.read(member).decode("utf-8", errors="replace")
    rows = list(parse_rows(text))
    if len(rows) != 1668:
        raise RuntimeError(f"Expected 1668 Hillenbrand rows, found {len(rows)}")

    raw_vowels = Counter(r["source_vowel"] for r in rows)
    canonical_vowels = Counter(r["vowel"] for r in rows)
    print("source vowel codes:", dict(sorted(raw_vowels.items())))
    print("canonical vowel codes:", dict(sorted(canonical_vowels.items())))
    unknown = sorted(set(canonical_vowels) - set(VOWEL_LABELS))
    missing = sorted(set(VOWEL_LABELS) - set(canonical_vowels))
    if unknown or missing:
        raise RuntimeError(f"Vowel-code mismatch after normalization: unknown={unknown}, missing={missing}")

    groups = aggregate(rows)
    for speaker_type in TYPE_NAMES.values():
        missing_group = [v for v in VOWEL_LABELS if groups[speaker_type][v]["token_n"] == 0]
        if missing_group:
            raise RuntimeError(f"Missing categories for {speaker_type}: {missing_group}")

    payload = {
        "schema": "formantcanvas.hillenbrand-trajectories.v1",
        "source": {
            "study": "Hillenbrand, Getty, Clark & Wheeler (1995)",
            "doi": "10.1121/1.411872",
            "dataset_repository": SOURCE_REPO,
            "dataset_file": "h95-alldata.zip / bigdata.dat",
            "sampling": "F1/F2/F3 at 10%-80% of vowel duration in 10% steps",
            "missing_value_rule": "0 in source is treated as missing and excluded point-wise",
            "aggregation": "arithmetic mean by speaker type x intended vowel x normalized time point",
            "source_vowel_counts": dict(sorted(raw_vowels.items())),
            "code_normalization": {"ei": "ey (HAYED /eɪ/)"},
        },
        "time_points": list(PCTS),
        "groups": groups,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
