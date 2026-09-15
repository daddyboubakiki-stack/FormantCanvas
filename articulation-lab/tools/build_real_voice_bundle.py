#!/usr/bin/env python3
"""Build redistribution-safe short vowel samples for Articulation Lab v0.4.

Inputs are downloaded by CI from sources listed in data/real-voice-sources.json.
The script intentionally uses only Python stdlib + ffmpeg/ffprobe.
"""
from __future__ import annotations

import argparse
import audioop
import json
import math
import subprocess
import wave
from pathlib import Path

IPA_SEQUENCE = ["a","æ","ɛ","e̞","e","ɪ","i","y","ʏ","ø","ø̞","œ","ɶ","ä","ɐ","ɜ","ə","ɘ","ɪ̈","ɨ","ʉ","ʊ̈","ɵ̞","ɞ","ɞ̞","ɒ̈","ɑ","ʌ","ɤ̞","ɤ","ʊ","ɯ","u","o","o̞","ɔ","ɒ"]
IPA_EXPORTS = {
    6: "i.wav", 5: "I.wav", 2: "epsilon.wav", 1: "ae.wav", 27: "turned_v.wav",
    16: "schwa.wav", 26: "alpha.wav", 35: "open_o.wav", 30: "U.wav", 32: "u.wav",
}
JP_EXPORTS = {
    "a": "jp_a.ogg",
    "i": "jp_i.ogg",
    "u": "jp_u.ogg",
    "e": "jp_e.ogg",
    "o": "jp_o.ogg",
}


def run(*args: str) -> str:
    p = subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.strip()


def duration(path: Path) -> float:
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)))


def render_clip(src: Path, dst: Path, start: float, dur: float = 0.55) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    start = max(0.0, start)
    total = duration(src)
    dur = min(dur, max(0.20, total - start))
    fade_out_start = max(0.02, dur - 0.045)
    af = (
        "loudnorm=I=-20:TP=-2:LRA=7,"
        "afade=t=in:st=0:d=0.02,"
        f"afade=t=out:st={fade_out_start:.4f}:d=0.04"
    )
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{start:.4f}", "-i", str(src), "-t", f"{dur:.4f}",
        "-ac", "1", "-ar", "24000", "-af", af, "-c:a", "pcm_s16le", str(dst)
    ], check=True)


def central_clip(src: Path, dst: Path, target_dur: float = 0.55) -> dict:
    total = duration(src)
    dur = min(target_dur, max(0.30, total * 0.55))
    # Stay away from onset/offset and use the stable central portion of sustained-vowel recordings.
    start = max(0.0, (total - dur) / 2.0)
    render_clip(src, dst, start, dur)
    return {"sourceDuration": total, "clipStart": start, "clipDuration": dur}


def pcm_frames(wav_path: Path, frame_ms: int = 10):
    with wave.open(str(wav_path), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise RuntimeError("analysis WAV must be mono 16-bit PCM")
        rate = wf.getframerate()
        raw = wf.readframes(wf.getnframes())
    frame_bytes = max(2, int(rate * frame_ms / 1000) * 2)
    dbs = []
    for pos in range(0, len(raw), frame_bytes):
        chunk = raw[pos:pos + frame_bytes]
        if len(chunk) < 2:
            continue
        rms = audioop.rms(chunk, 2)
        db = -120.0 if rms <= 0 else 20.0 * math.log10(rms / 32768.0)
        dbs.append(db)
    return rate, dbs


def close_short_gaps(active: list[bool], gap_frames: int) -> list[bool]:
    out = active[:]
    i = 0
    while i < len(out):
        if out[i]:
            i += 1
            continue
        j = i
        while j < len(out) and not out[j]:
            j += 1
        if i > 0 and j < len(out) and (j - i) <= gap_frames:
            for k in range(i, j):
                out[k] = True
        i = j
    return out


def segments_from(active: list[bool], min_frames: int) -> list[tuple[int, int]]:
    segs = []
    i = 0
    while i < len(active):
        if not active[i]:
            i += 1
            continue
        j = i + 1
        while j < len(active) and active[j]:
            j += 1
        if j - i >= min_frames:
            segs.append((i, j))
        i = j
    return segs


def detect_ipa_segments(src: Path, work: Path) -> tuple[list[tuple[float, float]], dict]:
    analysis_wav = work / "all_ipa_analysis.wav"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(analysis_wav)
    ], check=True)
    _rate, dbs = pcm_frames(analysis_wav, 10)
    candidates = []
    # Search sensible thresholds/gap closures rather than hardcoding timestamps.
    for threshold in (-45, -42, -40, -38, -36, -34, -32, -30, -28, -26, -24):
        for gap_frames in (4, 6, 8, 10, 12, 15, 18, 22):
            active = [db > threshold for db in dbs]
            active = close_short_gaps(active, gap_frames)
            segs = segments_from(active, min_frames=14)  # >= 140 ms
            plausible = [s for s in segs if (s[1] - s[0]) <= 160]  # <= 1.6 s
            score = abs(len(plausible) - len(IPA_SEQUENCE))
            candidates.append((score, threshold, gap_frames, plausible))
    candidates.sort(key=lambda x: (x[0], abs(x[1] + 34), x[2]))
    score, threshold, gap_frames, segs = candidates[0]
    report = {
        "frameMs": 10,
        "thresholdDbfs": threshold,
        "closedGapMs": gap_frames * 10,
        "detectedCount": len(segs),
        "expectedCount": len(IPA_SEQUENCE),
        "candidateScore": score,
    }
    if len(segs) != len(IPA_SEQUENCE):
        report["error"] = "Could not robustly resolve exactly 37 isolated vowels; do not map by sequence until reviewed."
        raise RuntimeError(json.dumps(report, ensure_ascii=False))
    seconds = [(a * 0.01, b * 0.01) for a, b in segs]
    report["segments"] = [
        {"index": i, "ipa": IPA_SEQUENCE[i], "start": a, "end": b, "duration": b-a}
        for i, (a, b) in enumerate(seconds)
    ]
    return seconds, report


def build(args) -> dict:
    src = Path(args.source_dir)
    out = Path(args.output_dir)
    work = Path(args.work_dir)
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    report = {"japanese": {}, "ipaReference": {}}

    jp_out = out / "jp_reference"
    for key, filename in JP_EXPORTS.items():
        info = central_clip(src / filename, jp_out / f"{key}.wav")
        info.update({"sourceFile": filename, "output": f"jp_reference/{key}.wav"})
        report["japanese"][key] = info

    ipa_src = src / "all_ipa.ogg"
    segments, detect_report = detect_ipa_segments(ipa_src, work)
    ipa_out = out / "ipa_reference"
    report["ipaReference"]["detection"] = detect_report
    report["ipaReference"]["exports"] = {}
    total = duration(ipa_src)
    for idx, filename in IPA_EXPORTS.items():
        a, b = segments[idx]
        center = (a + b) / 2.0
        clip_dur = min(0.60, max(0.38, (b - a) + 0.05))
        start = max(0.0, min(total - clip_dur, center - clip_dur / 2.0))
        render_clip(ipa_src, ipa_out / filename, start, clip_dur)
        report["ipaReference"]["exports"][IPA_SEQUENCE[idx]] = {
            "sequenceIndex": idx, "segmentStart": a, "segmentEnd": b,
            "clipStart": start, "clipDuration": clip_dur,
            "output": f"ipa_reference/{filename}",
        }

    with (out / "build-report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--work-dir", required=True)
    args = p.parse_args()
    report = build(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
