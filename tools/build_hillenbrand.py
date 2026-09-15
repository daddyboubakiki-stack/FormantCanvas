#!/usr/bin/env python3
"""Build compact Hillenbrand et al. (1995) trajectory means for FormantCanvas.

Source mirror:
  https://github.com/santiagobarreda/hillenbrand_et_al_1995
  (hosted there with permission from Jim Hillenbrand)

The original bigdata.dat has 30 whitespace-separated columns:
  filename, duration_ms, f0_steady, f1_steady, f2_steady, f3_steady,
  then F1/F2/F3 at 10,20,...,80% of vowel duration.

In the source data, numeric 0 denotes a missing acoustic value. Missing values are
excluded point-by-point rather than treated as 0 Hz.
"""

from __future__ import annotations

import io
import json
import math
import statistics
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

SOURCE_REPO = "https://github.com/santiagobarreda/hillenbrand_et_al_1995"
SOURCE_ZIP = (
    "https://raw.githubusercontent.com/santiagobarreda/"
    "hillenbrand_et_al_1995/main/h95-alldata.zip"
)
OUT = Path(__file__).resolve().parents[1] / "data" / "hillenbrand_1995_trajectories.json"
PCTS = tuple(range(10, 90, 10))
FORMANTS = ("F1", "F2", "F3")
TYPE_NAMES = {"m": "male", "w": "female", "b": "boy", "g": "girl"}
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
    req = urllib.request.Request(
        SOURCE_ZIP,
        headers={"User-Agent": "FormantCanvas-Hillenbrand-builder/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def find_bigdata(zf: zipfile.ZipFile) -> str:
    candidates = [name for name in zf.namelist() if Path(name).name.lower() == "bigdata.dat"]
    if not candidates:
        raise RuntimeError("bigdata.dat not found in h95-alldata.zip")
    return candidates[0]


def parse_rows(text: str):
    # Ignore the explanatory header and begin at the first data record.
    started = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if not started:
            if parts and parts[0].lower() == "b01ae":
                started = True
            else:
                continue
        if len(parts) != 30:
            raise ValueError(f"Expected 30 columns, got {len(parts)}: {line[:100]}")

        filename = parts[0].lower()
        speaker_code = filename[0]
        vowel = filename[3:5]
        nums = [float(x) for x in parts[1:]]
        duration_ms = nums[0]
        # nums[1:5] = steady f0,f1,f2,f3. Dynamic values begin at nums[5].
        dynamic = nums[5:]
        points = {}
        for i, pct in enumerate(PCTS):
            triplet = dynamic[i * 3 : i * 3 + 3]
            points[pct] = {
                f: (None if value == 0 else value)
                for f, value in zip(FORMANTS, triplet)
            }
        yield {
            "filename": filename,
            "speaker_code": speaker_code,
            "speaker_type": TYPE_NAMES[speaker_code],
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
            subset = groups.get((speaker_type, vowel), [])
            if not subset:
                continue
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
        },
        "time_points": list(PCTS),
        "groups": aggregate(rows),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    for group in ("male", "female", "boy", "girl"):
        ey = payload["groups"][group].get("ey")
        oa = payload["groups"][group].get("oa")
        if ey and oa:
            print(
                group,
                "eɪ tokens=", ey["token_n"],
                "oʊ tokens=", oa["token_n"],
                "eɪ F2 10→80=", ey["points"][0]["F2"], "→", ey["points"][-1]["F2"],
                "oʊ F2 10→80=", oa["points"][0]["F2"], "→", oa["points"][-1]["F2"],
            )


if __name__ == "__main__":
    main()
