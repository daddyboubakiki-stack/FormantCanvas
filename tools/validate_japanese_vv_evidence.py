#!/usr/bin/env python3
"""Validate the Japanese VV evidence manifest.

The purpose is intentionally conservative: Formant Canvas must not label a
trajectory as empirical unless a reusable numeric time series has actually been
recovered. Literature can establish that dynamic measurements exist without
providing the numeric series needed for a numeric preset.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "japanese_vv_evidence_manifest.json"

REQUIRED_STUDY_FIELDS = {
    "id",
    "study",
    "source_url",
    "population",
    "sequences",
    "acoustic_measures",
    "measurement_structure",
    "normalization",
    "measured_time_series_exists_in_study",
    "numeric_series_publicly_recovered",
    "numeric_summary_publicly_recovered",
    "canvas_use_status",
    "current_canvas_use",
    "blocker",
    "checked_locations",
    "notes",
}

ALLOWED_STATUS = {
    "endpoint_and_timing_evidence",
    "dynamic_evidence_only",
    "empirical_trajectory",
    "not_usable",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(data.get("schema") == "formantcanvas.japanese-vv-evidence.v1", "Unexpected schema")
    studies = data.get("studies")
    require(isinstance(studies, list) and studies, "studies must be a non-empty list")

    ids: set[str] = set()
    for study in studies:
        missing = REQUIRED_STUDY_FIELDS - set(study)
        require(not missing, f"{study.get('id', '<unknown>')}: missing fields {sorted(missing)}")
        sid = study["id"]
        require(isinstance(sid, str) and sid, "study id must be a non-empty string")
        require(sid not in ids, f"duplicate study id: {sid}")
        ids.add(sid)

        status = study["canvas_use_status"]
        require(status in ALLOWED_STATUS, f"{sid}: unsupported canvas_use_status {status!r}")
        require(isinstance(study["sequences"], list) and study["sequences"], f"{sid}: sequences must be non-empty")
        require(isinstance(study["checked_locations"], list) and study["checked_locations"], f"{sid}: checked_locations must be non-empty")

        recovered = study["numeric_series_publicly_recovered"]
        require(isinstance(recovered, bool), f"{sid}: numeric_series_publicly_recovered must be boolean")
        if status == "empirical_trajectory":
            require(
                recovered,
                f"{sid}: empirical_trajectory is forbidden until a reusable numeric time series is recovered",
            )

        if study["measured_time_series_exists_in_study"] and not recovered:
            require(
                bool(study["blocker"].strip()),
                f"{sid}: dynamic study without recovered series must document the blocker",
            )

    expected = {"hara2016", "zhang2022", "sun_hayashi2025"}
    require(expected <= ids, f"Manifest is missing core studies: {sorted(expected - ids)}")
    print(f"Validated {len(studies)} Japanese VV evidence records: {', '.join(sorted(ids))}")


if __name__ == "__main__":
    main()
