#!/usr/bin/env python3
"""Build redistribution-safe short vowel samples for Articulation Lab v0.4.1.

Inputs are downloaded by CI from sources listed in data/real-voice-sources.json.
The script intentionally uses only Python stdlib + ffmpeg/ffprobe.

v0.4.1 fixes:
- Japanese samples are no longer cropped from the file midpoint. A voiced token is detected first.
- Output WAVs are level-matched using active-speech RMS, which also fixes quiet IPA samples such as /ɔ/.
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


def render_clip(src: Path, dst: Path, start: float, dur: float, atempo: float = 1.0) -> None:
    """Render a mono PCM excerpt with short fades.

    atempo < 1.0 slows the clip while preserving pitch reasonably well.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    start = max(0.0, start)
    total = duration(src)
    dur = min(dur, max(0.08, total - start))

    filters = []
    tempo = max(0.25, min(2.0, float(atempo)))
    # ffmpeg atempo accepts 0.5..100. Chain when a slower factor is needed.
    while tempo < 0.5:
        filters.append("atempo=0.5")
        tempo /= 0.5
    if abs(tempo - 1.0) > 1e-4:
        filters.append(f"atempo={tempo:.6f}")

    # Initial loudnorm is only coarse; a deterministic active-RMS pass follows.
    filters.append("loudnorm=I=-18:TP=-2:LRA=7")
    rendered_dur = dur / max(0.001, atempo)
    filters.append("afade=t=in:st=0:d=0.018")
    filters.append(f"afade=t=out:st={max(0.025, rendered_dur - 0.045):.4f}:d=0.04")

    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{start:.4f}", "-i", str(src), "-t", f"{dur:.4f}",
        "-ac", "1", "-ar", "24000", "-af", ",".join(filters),
        "-c:a", "pcm_s16le", str(dst)
    ], check=True)


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


def decode_analysis(src: Path, wav: Path) -> None:
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)
    ], check=True)


def detect_japanese_token(src: Path, work: Path, key: str) -> tuple[tuple[float, float], dict]:
    """Detect one clearly voiced kana token from recordings that may contain repeated utterances.

    The old midpoint crop could land in silence. We search several thresholds and choose
    a strong, self-contained voiced segment instead.
    """
    analysis_wav = work / f"jp_{key}_analysis.wav"
    decode_analysis(src, analysis_wav)
    _rate, dbs = pcm_frames(analysis_wav, 10)
    if not dbs:
        raise RuntimeError(f"No analyzable audio for Japanese {key}")

    peak_db = max(dbs)
    candidates = []
    for drop in (16, 18, 20, 22, 24, 26, 28):
        threshold = max(-52.0, peak_db - drop)
        for gap_frames in (2, 3, 4, 5):
            active = close_short_gaps([db > threshold for db in dbs], gap_frames)
            segs = segments_from(active, min_frames=4)  # >= 40 ms
            plausible = [s for s in segs if 4 <= (s[1] - s[0]) <= 80]  # 40..800 ms
            if not plausible:
                continue
            # Prefer longer tokens and thresholds near peak-22 dB; avoid edge fragments.
            for a, b in plausible:
                dur_frames = b - a
                edge_penalty = 0.15 if a == 0 or b >= len(dbs) else 0.0
                level = sum(dbs[a:b]) / max(1, dur_frames)
                score = dur_frames + 0.12 * (level - threshold) - edge_penalty
                candidates.append((score, threshold, gap_frames, a, b, plausible))

    if not candidates:
        raise RuntimeError(f"Could not find voiced token in Japanese {key}")

    candidates.sort(key=lambda x: x[0], reverse=True)
    score, threshold, gap_frames, a, b, plausible = candidates[0]
    start, end = a * 0.01, b * 0.01
    report = {
        "frameMs": 10,
        "peakDbfs": peak_db,
        "thresholdDbfs": threshold,
        "closedGapMs": gap_frames * 10,
        "selectedStart": start,
        "selectedEnd": end,
        "selectedDuration": end - start,
        "detectedSegments": [
            {"start": x * 0.01, "end": y * 0.01, "duration": (y - x) * 0.01}
            for x, y in plausible
        ],
        "selectionScore": score,
    }
    return (start, end), report


def level_match_active_rms(wav_path: Path, target_dbfs: float = -17.0) -> dict:
    """Match active-frame RMS while preserving headroom.

    This is intentionally simple and deterministic for short isolated vowels.
    """
    with wave.open(str(wav_path), "rb") as wf:
        params = wf.getparams()
        if params.nchannels != 1 or params.sampwidth != 2:
            raise RuntimeError("level matching expects mono 16-bit PCM")
        raw = wf.readframes(params.nframes)

    sample_count = len(raw) // 2
    if sample_count == 0:
        return {"appliedGainDb": 0.0, "reason": "empty"}

    import array
    samples = array.array("h")
    samples.frombytes(raw)
    if samples.itemsize != 2:
        raise RuntimeError("unexpected int16 size")
    if __import__("sys").byteorder != "little":
        samples.byteswap()

    rate = params.framerate
    frame_len = max(1, int(rate * 0.01))
    frame_rms = []
    for i in range(0, len(samples), frame_len):
        chunk = samples[i:i + frame_len]
        if not chunk:
            continue
        ss = sum(float(v) * float(v) for v in chunk)
        rms = math.sqrt(ss / len(chunk))
        db = -120.0 if rms <= 0 else 20.0 * math.log10(rms / 32768.0)
        frame_rms.append((i, min(len(samples), i + frame_len), rms, db))

    max_db = max((x[3] for x in frame_rms), default=-120.0)
    threshold = max(-45.0, max_db - 24.0)
    active = [x for x in frame_rms if x[3] > threshold]
    if not active:
        return {"appliedGainDb": 0.0, "reason": "no_active_frames", "thresholdDbfs": threshold}

    sumsq = 0.0
    count = 0
    for a, b, _rms, _db in active:
        for v in samples[a:b]:
            sumsq += float(v) * float(v)
            count += 1
    active_rms = math.sqrt(sumsq / max(1, count))
    active_db = -120.0 if active_rms <= 0 else 20.0 * math.log10(active_rms / 32768.0)

    desired_gain = 10.0 ** ((target_dbfs - active_db) / 20.0)
    peak = max(abs(v) for v in samples) / 32768.0
    peak_limit = 10.0 ** (-1.5 / 20.0)
    headroom_gain = peak_limit / max(1e-9, peak)
    gain = min(desired_gain, headroom_gain, 4.0)
    gain = max(0.25, gain)

    for i, v in enumerate(samples):
        samples[i] = int(max(-32768, min(32767, round(v * gain))))

    if __import__("sys").byteorder != "little":
        samples.byteswap()
    with wave.open(str(wav_path), "wb") as wf:
        wf.setparams(params)
        wf.writeframes(samples.tobytes())

    return {
        "activeRmsBeforeDbfs": active_db,
        "targetActiveRmsDbfs": target_dbfs,
        "thresholdDbfs": threshold,
        "appliedGainDb": 20.0 * math.log10(max(1e-9, gain)),
        "peakBeforeDbfs": -120.0 if peak <= 0 else 20.0 * math.log10(peak),
    }


def build_japanese_sample(src: Path, dst: Path, work: Path, key: str) -> dict:
    total = duration(src)
    (a, b), detect = detect_japanese_token(src, work, key)
    token_dur = b - a

    # Include a little natural onset/offset context.
    margin = 0.025
    clip_start = max(0.0, a - margin)
    clip_end = min(total, b + margin)
    clip_dur = clip_end - clip_start

    # The source files contain short kana repetitions. Mildly sustain very short tokens
    # (max 2x duration) so button playback is comparable to the English reference samples.
    desired_voiced = 0.36
    stretch = min(2.0, max(1.0, desired_voiced / max(0.08, token_dur)))
    atempo = 1.0 / stretch
    render_clip(src, dst, clip_start, clip_dur, atempo=atempo)
    level = level_match_active_rms(dst, target_dbfs=-17.0)
    return {
        "sourceDuration": total,
        "clipStart": clip_start,
        "clipDurationBeforeStretch": clip_dur,
        "selectedVoicedDuration": token_dur,
        "stretchFactor": stretch,
        "outputDuration": duration(dst),
        "detection": detect,
        "levelMatch": level,
    }


def detect_ipa_segments(src: Path, work: Path) -> tuple[list[tuple[float, float]], dict]:
    analysis_wav = work / "all_ipa_analysis.wav"
    decode_analysis(src, analysis_wav)
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
    report = {"version": "v0.4.1", "japanese": {}, "ipaReference": {}}

    jp_out = out / "jp_reference"
    for key, filename in JP_EXPORTS.items():
        info = build_japanese_sample(src / filename, jp_out / f"{key}.wav", work, key)
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
        dst = ipa_out / filename
        render_clip(ipa_src, dst, start, clip_dur)
        level = level_match_active_rms(dst, target_dbfs=-17.0)
        report["ipaReference"]["exports"][IPA_SEQUENCE[idx]] = {
            "sequenceIndex": idx, "segmentStart": a, "segmentEnd": b,
            "clipStart": start, "clipDuration": clip_dur,
            "output": f"ipa_reference/{filename}",
            "outputDuration": duration(dst),
            "levelMatch": level,
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
