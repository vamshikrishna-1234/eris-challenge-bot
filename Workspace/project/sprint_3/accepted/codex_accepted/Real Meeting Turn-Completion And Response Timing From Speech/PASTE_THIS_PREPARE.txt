from __future__ import annotations

import hashlib
import html
import json
import math
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import istft, resample, resample_poly, stft


TURN_STATES = ["COMPLETE", "CONTINUE", "BACKCHANNEL", "OVERLAP", "UNCERTAIN"]
RELATIONS = ["SAME", "OTHER", "MULTI", "NONE_OR_UNCLEAR"]
DEFAULT_MEETINGS = [
    "ES2002a",
    "ES2003a",
    "ES2004a",
    "IS1000a",
    "TS3003a",
    "EN2001a",
    "IB4001",
    "IN1001",
]
BACKCHANNEL_FORMS = {
    "yeah",
    "yep",
    "yes",
    "right",
    "okay",
    "ok",
    "mm",
    "mhm",
    "mmhm",
    "uhhuh",
    "uh",
    "huh",
    "hm",
    "hmm",
    "sure",
    "exactly",
    "cool",
    "alright",
    "aye",
    "fine",
}

NITE_NS = "{http://nite.sourceforge.net/}"
TARGET_SR = 16000
MAX_RESPONSE_MS = 3000
MAX_SAMPLES = 900
CONTEXT_SEC = 8.0

ID_SALT = "real-meeting-turn-completion-v2-prepare-only-source-data"
SPLIT_SEED = 0xC0DEC0DE
SAMPLE_SEED = 0xA11CE
TEST_FRACTION = 0.25
MIN_GROUP_TEST = 5

PUBLIC_INPUT_COLUMNS = [
    "id",
    "audio_path",
    "transcript_window",
    "token_timing_json",
    "speaker_context_json",
]
LABEL_COLUMNS = ["turn_state", "next_response_ms", "next_speaker_relation", "confidence"]
SUBMISSION_COLUMNS = ["id", "turn_state", "next_response_ms", "next_speaker_relation", "confidence"]


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _stable_digest(*parts: object) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def _normalise_token(text: str) -> str:
    text = html.unescape(text or "").lower().strip()
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _redacted_token(token: str) -> str:
    token = _normalise_token(token)
    if not token:
        return "tok_empty"
    if token in BACKCHANNEL_FORMS:
        return "tok_ack"
    if token.isdigit():
        return "tok_num"
    n = len(token)
    if n <= 2:
        return "tok_short"
    if n <= 5:
        return "tok_med"
    if n <= 8:
        return "tok_long"
    return "tok_xlong"


def _redacted_transcript(tokens: list[dict]) -> str:
    return " ".join(_redacted_token(tok["text"]) for tok in tokens[-32:]) or "tok_empty"


def _find_raw_root(raw: Path) -> Path:
    for candidate in [raw, raw / "raw_upload", raw / "raw_data"]:
        if (
            (candidate / "ami_public_manual_1.6.2.zip").exists()
            or ((candidate / "words").exists() and (candidate / "segments").exists())
            or ((candidate / "ami_public_manual_1.6.2" / "words").exists()
                and (candidate / "ami_public_manual_1.6.2" / "segments").exists())
        ):
            return candidate
        if any(p.name == "words" and (p.parent / "segments").exists() for p in candidate.rglob("words")):
            return candidate
    for path in sorted(raw.rglob("ami_public_manual_1.6.2.zip")):
        if "public" not in path.parts and "private" not in path.parts:
            return path.parent
    for path in sorted(raw.rglob("words")):
        if (path.parent / "segments").exists() and "public" not in path.parts and "private" not in path.parts:
            return raw
    raise FileNotFoundError(f"No AMI annotation zip or extracted AMI annotation directory found under {raw}")


def _annotation_root(raw_root: Path, temp_dir: Path) -> Path:
    if (raw_root / "words").exists() and (raw_root / "segments").exists():
        return raw_root
    for candidate in [raw_root / "annotations", raw_root / "ann", raw_root / "ami_public_manual_1.6.2"]:
        if (candidate / "words").exists() and (candidate / "segments").exists():
            return candidate
    for words_dir in sorted(raw_root.rglob("words")):
        candidate = words_dir.parent
        if (candidate / "segments").exists() and "public" not in candidate.parts and "private" not in candidate.parts:
            return candidate
    zip_path = raw_root / "ami_public_manual_1.6.2.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing AMI manual annotation zip: {zip_path}")
    out_dir = temp_dir / "ami_annotations"
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)
    for candidate in [out_dir, *out_dir.iterdir()]:
        if candidate.is_dir() and (candidate / "words").exists() and (candidate / "segments").exists():
            return candidate
    raise RuntimeError("Could not locate words/segments in AMI annotation zip")


def _find_audio_files(raw_root: Path) -> dict[str, Path]:
    audio_files: dict[str, Path] = {}
    if (raw_root / "meetings.csv").exists():
        manifest = pd.read_csv(raw_root / "meetings.csv")
        for _, row in manifest.iterrows():
            meeting_id = str(row["meeting_id"])
            rel = Path(str(row["audio_path"]))
            path = raw_root / rel
            if path.exists():
                audio_files[meeting_id] = path
    for path in sorted(raw_root.rglob("*.Mix-Headset.wav")):
        meeting_id = path.name.split(".")[0]
        audio_files.setdefault(meeting_id, path)
    missing = [m for m in DEFAULT_MEETINGS if m not in audio_files]
    if missing:
        raise FileNotFoundError(f"Missing AMI headset-mix WAV files for meetings: {missing}")
    return {m: audio_files[m] for m in DEFAULT_MEETINGS}


def _speaker_from_name(path: Path) -> str:
    return path.name.split(".")[1]


def _session_group(meeting_id: str) -> str:
    match = re.match(r"([A-Z]{2}\d{4})", meeting_id)
    return match.group(1) if match else meeting_id


def _meeting_family(meeting_id: str) -> str:
    match = re.match(r"([A-Z]+)", meeting_id)
    return match.group(1) if match else "UNK"


def _parse_word_range(href: str) -> tuple[int, int] | None:
    match = re.search(r"words(\d+)\)\.\.id\([^)]*words(\d+)\)", href)
    if match:
        return int(match.group(1)), int(match.group(2))
    match = re.search(r"words(\d+)\)", href)
    if match:
        idx = int(match.group(1))
        return idx, idx
    return None


def _load_words(ann_root: Path, meeting_id: str) -> dict[str, list[dict]]:
    words_by_speaker: dict[str, list[dict]] = {}
    for path in sorted((ann_root / "words").glob(f"{meeting_id}.*.words.xml")):
        speaker = _speaker_from_name(path)
        root = ET.parse(path).getroot()
        words: list[dict] = []
        for el in root:
            if _local_name(el.tag) != "w" or el.attrib.get("punc") == "true":
                continue
            token = _normalise_token(el.text or "")
            if not token:
                continue
            try:
                start = float(el.attrib["starttime"])
                end = float(el.attrib["endtime"])
            except (KeyError, ValueError):
                continue
            if not (math.isfinite(start) and math.isfinite(end)) or end < start:
                continue
            nite_id = el.attrib.get(NITE_NS + "id") or el.attrib.get("nite:id") or el.attrib.get("id", "")
            idx_match = re.search(r"words(\d+)$", nite_id)
            if not idx_match:
                continue
            words.append(
                {
                    "idx": int(idx_match.group(1)),
                    "speaker": speaker,
                    "start": start,
                    "end": end,
                    "text": token,
                }
            )
        words_by_speaker[speaker] = words
    return words_by_speaker


def _load_segments(ann_root: Path, meeting_id: str, words_by_speaker: dict[str, list[dict]]) -> list[dict]:
    segments: list[dict] = []
    for path in sorted((ann_root / "segments").glob(f"{meeting_id}.*.segments.xml")):
        speaker = _speaker_from_name(path)
        word_by_idx = {w["idx"]: w for w in words_by_speaker.get(speaker, [])}
        if not word_by_idx:
            continue
        root = ET.parse(path).getroot()
        for seg in root:
            if _local_name(seg.tag) != "segment":
                continue
            child = next((c for c in seg if _local_name(c.tag) == "child"), None)
            if child is None:
                continue
            word_range = _parse_word_range(child.attrib.get("href", ""))
            if word_range is None:
                continue
            idxs = [i for i in range(word_range[0], word_range[1] + 1) if i in word_by_idx]
            tokens = [word_by_idx[i] for i in idxs]
            if not tokens:
                continue
            try:
                seg_start = float(seg.attrib.get("transcriber_start", tokens[0]["start"]))
                seg_end = float(seg.attrib.get("transcriber_end", tokens[-1]["end"]))
            except ValueError:
                seg_start = tokens[0]["start"]
                seg_end = tokens[-1]["end"]
            seg_start = min(seg_start, tokens[0]["start"])
            seg_end = max(seg_end, tokens[-1]["end"])
            if not (math.isfinite(seg_start) and math.isfinite(seg_end)) or seg_end <= seg_start:
                continue
            seg_id = seg.attrib.get(NITE_NS + "id") or seg.attrib.get("nite:id") or ""
            segments.append(
                {
                    "meeting_id": meeting_id,
                    "speaker": speaker,
                    "segment_id": seg_id,
                    "start": float(seg_start),
                    "end": float(seg_end),
                    "tokens": tokens,
                    "text": " ".join(t["text"] for t in tokens),
                    "n_tokens": len(tokens),
                }
            )
    return sorted(segments, key=lambda s: (s["start"], s["end"], s["speaker"]))


def _is_backchannel_segment(seg: dict) -> bool:
    words = [w for w in seg["text"].split() if w]
    if not words or len(words) > 3 or (seg["end"] - seg["start"]) > 1.25:
        return False
    joined = "".join(words)
    return all(w in BACKCHANNEL_FORMS for w in words) or joined in BACKCHANNEL_FORMS


def _latency_band(ms: int) -> str:
    if ms <= 250:
        return "immediate"
    if ms <= 800:
        return "fast"
    if ms <= 1500:
        return "medium"
    return "slow_or_unclear"


def _label_confidence(turn_state: str, latency_ms: int, margin_ms: int) -> float:
    if turn_state == "UNCERTAIN":
        return 0.42
    base = {"COMPLETE": 0.86, "CONTINUE": 0.84, "BACKCHANNEL": 0.80, "OVERLAP": 0.78}[turn_state]
    if latency_ms > 1800:
        base -= 0.08
    if margin_ms < 250:
        base -= 0.05
    return float(np.clip(base, 0.55, 0.96))


def _classify_boundary(current: dict, all_segments: list[dict]) -> tuple[str, int, str, float]:
    end = current["end"]
    speaker = current["speaker"]
    overlapping = [
        seg
        for seg in all_segments
        if seg is not current
        and seg["speaker"] != speaker
        and seg["start"] < end + 0.15
        and seg["end"] > end - 0.90
    ]
    ack_overlap = [seg for seg in overlapping if _is_backchannel_segment(seg)]
    if ack_overlap:
        same_future = [
            seg
            for seg in all_segments
            if seg is not current and seg["speaker"] == speaker and 0.0 <= seg["start"] - end <= 2.0
        ]
        if same_future:
            margin = int(round(min((seg["start"] - end) * 1000 for seg in same_future)))
            return "BACKCHANNEL", 0, "OTHER", _label_confidence("BACKCHANNEL", 0, margin)
    for seg in overlapping:
        if seg["start"] < end - 0.05 and seg["n_tokens"] >= 3 and (seg["end"] - seg["start"]) >= 0.50:
            return "OVERLAP", 0, "OTHER", _label_confidence("OVERLAP", 0, 0)
    future = [seg for seg in all_segments if seg is not current and seg["start"] >= end - 0.05]
    future.sort(key=lambda s: (s["start"], s["end"]))
    if not future:
        return "UNCERTAIN", MAX_RESPONSE_MS, "NONE_OR_UNCLEAR", _label_confidence("UNCERTAIN", MAX_RESPONSE_MS, 0)
    next_seg = future[0]
    delta = next_seg["start"] - end
    if delta > 3.0:
        return "UNCERTAIN", MAX_RESPONSE_MS, "NONE_OR_UNCLEAR", _label_confidence("UNCERTAIN", MAX_RESPONSE_MS, 0)
    response_ms = int(round(max(0.0, min(3.0, delta)) * 1000))
    co_starters = sum(1 for seg in future if abs(seg["start"] - next_seg["start"]) <= 0.25)
    relation = "SAME" if next_seg["speaker"] == speaker else ("MULTI" if co_starters >= 2 else "OTHER")
    if next_seg["speaker"] != speaker and _is_backchannel_segment(next_seg):
        return "BACKCHANNEL", response_ms, relation, _label_confidence("BACKCHANNEL", response_ms, int(delta * 1000))
    if next_seg["speaker"] == speaker:
        return "CONTINUE", response_ms, "SAME", _label_confidence("CONTINUE", response_ms, int(delta * 1000))
    return "COMPLETE", response_ms, relation, _label_confidence("COMPLETE", response_ms, int(delta * 1000))


def _bucket_duration(seconds: float) -> str:
    if seconds < 2.0:
        return "short"
    if seconds < 6.0:
        return "medium"
    return "long"


def _token_timing_json(tokens: list[dict], clip_start: float, clip_end: float) -> str:
    public_tokens = []
    for public_idx, tok in enumerate(tokens[-32:]):
        if tok["end"] < clip_start or tok["start"] > clip_end:
            continue
        public_tokens.append(
            {
                "token_index": public_idx,
                "token_shape": _redacted_token(tok["text"]),
                "start_ms": int(round(max(0.0, tok["start"] - clip_start) * 1000)),
                "end_ms": int(round(max(0.0, tok["end"] - clip_start) * 1000)),
            }
        )
    return json.dumps(public_tokens, separators=(",", ":"))


def _speaker_context_json(current: dict, all_segments: list[dict], clip_start: float, clip_end: float) -> str:
    recent = [seg for seg in all_segments if seg["end"] >= clip_start and seg["start"] <= clip_end]
    previous_same = [
        seg for seg in all_segments if seg["speaker"] == current["speaker"] and seg["end"] < current["start"]
    ]
    prev_bucket = "none"
    if previous_same:
        prev_bucket = _bucket_duration(previous_same[-1]["end"] - previous_same[-1]["start"])
    payload = {
        "current_speaker": "speaker_0",
        "recent_active_speakers": int(len({seg["speaker"] for seg in recent})),
        "prev_turn_length_bucket": prev_bucket,
        "clip_duration_ms": int(round((clip_end - clip_start) * 1000)),
        "current_words": int(current["n_tokens"]),
    }
    return json.dumps(payload, separators=(",", ":"))


def _candidate_rows_for_meeting(ann_root: Path, meeting_id: str) -> list[dict]:
    words = _load_words(ann_root, meeting_id)
    segments = _load_segments(ann_root, meeting_id, words)
    rows: list[dict] = []
    for seg in segments:
        duration = seg["end"] - seg["start"]
        if seg["n_tokens"] < 2 or duration < 0.75 or duration > 24.0:
            continue
        clip_end = seg["end"]
        clip_start = max(0.0, clip_end - CONTEXT_SEC)
        if clip_end - clip_start < 1.75:
            continue
        state, response_ms, relation, confidence = _classify_boundary(seg, segments)
        source_key = _stable_digest(meeting_id, seg["speaker"], seg["segment_id"], f"{seg['end']:.3f}")
        speaker_ctx = _speaker_context_json(seg, segments, clip_start, clip_end)
        rows.append(
            {
                "source_key": source_key,
                "meeting_id": meeting_id,
                "session_group": _session_group(meeting_id),
                "speaker_code": seg["speaker"],
                "segment_id": seg["segment_id"],
                "boundary_time_sec": round(seg["end"], 3),
                "clip_start_sec": round(clip_start, 3),
                "clip_end_sec": round(clip_end, 3),
                "transcript_window": _redacted_transcript(seg["tokens"]),
                "token_timing_json": _token_timing_json(seg["tokens"], clip_start, clip_end),
                "speaker_context_json": speaker_ctx,
                "turn_state": state,
                "next_response_ms": int(response_ms),
                "next_speaker_relation": relation,
                "confidence": round(confidence, 4),
                "meeting_family": _meeting_family(meeting_id),
                "latency_band": _latency_band(int(response_ms)),
                "turn_type_bucket": state.lower(),
                "clip_duration_sec": round(clip_end - clip_start, 3),
                "num_tokens": int(seg["n_tokens"]),
                "current_segment_duration_sec": round(duration, 3),
                "recent_active_speakers": json.loads(speaker_ctx)["recent_active_speakers"],
            }
        )
    return rows


def _balanced_sample(rows: list[dict]) -> list[dict]:
    if MAX_SAMPLES <= 0 or MAX_SAMPLES >= len(rows):
        return rows
    rng = np.random.default_rng(SAMPLE_SEED)
    by_label: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_label[row["turn_state"]].append(row)
    for label_rows in by_label.values():
        rng.shuffle(label_rows)
    target_fracs = {"BACKCHANNEL": 0.14, "UNCERTAIN": 0.16, "COMPLETE": 0.23, "CONTINUE": 0.23, "OVERLAP": 0.24}
    quotas = {label: min(len(by_label[label]), int(round(MAX_SAMPLES * frac))) for label, frac in target_fracs.items()}
    remaining = MAX_SAMPLES - sum(quotas.values())
    while remaining > 0:
        capacities = {label: len(by_label[label]) - quotas.get(label, 0) for label in TURN_STATES}
        label = max(capacities, key=capacities.get)
        if capacities[label] <= 0:
            break
        quotas[label] = quotas.get(label, 0) + 1
        remaining -= 1
    chosen: list[dict] = []
    for label in TURN_STATES:
        chosen.extend(by_label[label][: quotas.get(label, 0)])
    rng.shuffle(chosen)
    return chosen


def _public_id_map(source_keys: list[str]) -> dict[str, int]:
    hashed = [(hashlib.sha256(f"{ID_SALT}:{key}".encode("utf-8")).hexdigest(), key) for key in source_keys]
    if len({d for d, _ in hashed}) != len(hashed):
        raise SystemExit("Public id hash collision")
    return {key: 100000 + i for i, (_, key) in enumerate(sorted(hashed))}


def _axis_min_counts(test_df: pd.DataFrame) -> dict[str, int]:
    axes = ["turn_state", "latency_band", "turn_type_bucket"]
    return {axis: int(test_df[axis].value_counts().min()) for axis in axes if test_df[axis].nunique() > 0}


def _split_penalty(df: pd.DataFrame, test_groups: set[str], min_required: int) -> tuple[int, float]:
    test = df[df["session_group"].isin(test_groups)]
    if test.empty:
        return 10_000, float("inf")
    penalty = 0
    for label in TURN_STATES:
        count = int((test["turn_state"] == label).sum())
        if count < min_required:
            penalty += (min_required - count) * 50
    for _, min_count in _axis_min_counts(test).items():
        if min_count < min_required:
            penalty += (min_required - min_count) * 10
    target_rows = len(df) * TEST_FRACTION
    size_penalty = abs(len(test) - target_rows) / max(1.0, target_rows)
    digest = hashlib.sha256(("|".join(sorted(test_groups)) + str(SPLIT_SEED)).encode("utf-8")).hexdigest()
    jitter = int(digest[:6], 16) / 16**6 * 0.001
    return penalty, size_penalty + jitter


def _choose_group_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    groups = sorted(df["session_group"].unique().tolist())
    if len(groups) < 2:
        raise SystemExit("Need at least two session groups for a grouped split")
    target_k = max(1, int(round(len(groups) * TEST_FRACTION)))
    candidate_ks = sorted({target_k, max(1, target_k - 1), min(len(groups) - 1, target_k + 1)})
    best: tuple[int, float, set[str]] | None = None
    for k in candidate_ks:
        for combo in combinations(groups, k):
            test_groups = set(combo)
            penalty, size_penalty = _split_penalty(df, test_groups, MIN_GROUP_TEST)
            if best is None or (penalty, size_penalty) < (best[0], best[1]):
                best = (penalty, size_penalty, test_groups)
    if best is None:
        raise SystemExit("Could not choose grouped split")
    train = df[~df["session_group"].isin(best[2])].copy()
    test = df[df["session_group"].isin(best[2])].copy()
    if set(train["meeting_id"]) & set(test["meeting_id"]) or set(train["session_group"]) & set(test["session_group"]):
        raise SystemExit("Meeting/session leakage across train/test")
    missing_labels = [label for label in TURN_STATES if int((test["turn_state"] == label).sum()) < MIN_GROUP_TEST]
    if missing_labels:
        raise SystemExit(f"Test split underfilled labels: {missing_labels}")
    return train, test


def _repair_sparse_axis(values: pd.Series, min_count: int) -> pd.Series:
    counts = values.value_counts()
    if counts.empty:
        return values
    majority = str(counts.idxmax())
    rare = counts[counts < min_count].index.tolist()
    if not rare:
        return values.astype(str)
    repaired = values.astype(str).copy()
    rare_total = int(values.isin(rare).sum())
    repaired[values.isin(rare)] = "OTHER" if rare_total >= min_count else majority
    return repaired


def _read_audio(path: Path) -> tuple[int, np.ndarray]:
    sr, data = wavfile.read(path)
    if data.ndim == 2:
        data = data.mean(axis=1)
    if data.dtype != np.float32:
        if np.issubdtype(data.dtype, np.integer):
            data = data.astype(np.float32) / float(np.iinfo(data.dtype).max)
        else:
            data = data.astype(np.float32)
    if sr != TARGET_SR:
        gcd = math.gcd(int(sr), TARGET_SR)
        data = resample_poly(data, TARGET_SR // gcd, int(sr) // gcd).astype(np.float32)
        sr = TARGET_SR
    return sr, np.asarray(data, dtype=np.float32)


def _clip_rng(key: object) -> np.random.Generator:
    digest = hashlib.sha256(f"{ID_SALT}:audio:{key}".encode("utf-8")).digest()
    return np.random.default_rng(int.from_bytes(digest[:8], "big"))


def _fit_length(x: np.ndarray, target_len: int) -> np.ndarray:
    if x.size < target_len:
        return np.pad(x, (0, target_len - x.size)).astype(np.float32)
    return np.asarray(x[:target_len], dtype=np.float32)


def _phase_vocoder_stretch(x: np.ndarray, rate: float, n_fft: int = 1024, hop: int = 256) -> np.ndarray:
    if x.size < n_fft or abs(rate - 1.0) < 1e-3:
        return x.astype(np.float32)
    _, _, spec = stft(x, fs=TARGET_SR, nperseg=n_fft, noverlap=n_fft - hop, boundary="zeros")
    if spec.shape[1] < 2:
        return x.astype(np.float32)
    time_steps = np.arange(0, spec.shape[1] - 1, rate, dtype=np.float64)
    phase_acc = np.angle(spec[:, 0])
    phase_advance = 2.0 * np.pi * hop * np.arange(spec.shape[0]) / float(n_fft)
    stretched = np.empty((spec.shape[0], len(time_steps)), dtype=np.complex64)
    for out_idx, step in enumerate(time_steps):
        left = int(np.floor(step))
        frac = float(step - left)
        right = min(left + 1, spec.shape[1] - 1)
        mag = (1.0 - frac) * np.abs(spec[:, left]) + frac * np.abs(spec[:, right])
        stretched[:, out_idx] = mag * np.exp(1j * phase_acc)
        phase_delta = np.angle(spec[:, right]) - np.angle(spec[:, left]) - phase_advance
        phase_delta -= 2.0 * np.pi * np.round(phase_delta / (2.0 * np.pi))
        phase_acc += phase_advance + phase_delta
    _, y = istft(stretched, fs=TARGET_SR, nperseg=n_fft, noverlap=n_fft - hop, input_onesided=True)
    return _fit_length(np.asarray(y, dtype=np.float32), max(1, int(round(x.size / rate))))


def _pitch_shift_preserve_length(x: np.ndarray, semitones: float) -> np.ndarray:
    original_len = x.size
    rate = float(2.0 ** (semitones / 12.0))
    stretched = _phase_vocoder_stretch(x, rate)
    shifted = resample(stretched, original_len).astype(np.float32)
    return _fit_length(shifted, original_len)


def _formant_warp_preserve_phase(x: np.ndarray, scale: float, n_fft: int = 512, hop: int = 128) -> np.ndarray:
    original_len = x.size
    if x.size < n_fft or abs(scale - 1.0) < 1e-3:
        return x.astype(np.float32)
    _, _, spec = stft(x, fs=TARGET_SR, nperseg=n_fft, noverlap=n_fft - hop, boundary="zeros")
    if spec.size == 0:
        return x.astype(np.float32)
    mag = np.abs(spec)
    phase = np.angle(spec)
    bins = np.arange(mag.shape[0], dtype=np.float64)
    source_bins = np.clip(bins / scale, 0.0, mag.shape[0] - 1.0)
    warped = np.empty_like(mag)
    for frame_idx in range(mag.shape[1]):
        warped[:, frame_idx] = np.interp(source_bins, bins, mag[:, frame_idx])
    _, y = istft(
        warped * np.exp(1j * phase),
        fs=TARGET_SR,
        nperseg=n_fft,
        noverlap=n_fft - hop,
        input_onesided=True,
    )
    return _fit_length(np.asarray(y, dtype=np.float32), original_len)


def _deidentify_clip(clip: np.ndarray, key: object) -> np.ndarray:
    rng = _clip_rng(key)
    x = np.asarray(clip, dtype=np.float32).copy()
    if x.size == 0:
        return x
    if int(rng.integers(0, 2)):
        x = -x
    gain = float(rng.uniform(0.82, 1.08))
    x = x * gain
    x = _pitch_shift_preserve_length(x, float(rng.uniform(-1.8, 1.8)))
    x = _formant_warp_preserve_phase(x, float(rng.uniform(0.92, 1.08)))
    # Deterministic pitch/formant perturbation, dither, and spectral tilt reduce
    # source matching while keeping the clip speech-like for speech encoders.
    rms = float(np.sqrt(np.mean(x**2)))
    if rms > 1e-5:
        snr_db = float(rng.uniform(35.0, 43.0))
        noise_scale = rms / (10.0 ** (snr_db / 20.0))
        x = x + rng.normal(0.0, noise_scale, size=x.shape).astype(np.float32)
    alpha = float(rng.uniform(0.015, 0.055))
    prev = np.concatenate(([0.0], x[:-1]))
    x = (1.0 - alpha) * x + alpha * (x - prev)
    bit_depth = int(rng.integers(13, 15))
    levels = float(2 ** (bit_depth - 1) - 1)
    x = np.round(np.clip(x, -1.0, 1.0) * levels) / levels
    fade = min(x.size // 8, int(0.012 * TARGET_SR))
    if fade > 1:
        ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
        x[:fade] *= ramp
        x[-fade:] *= ramp[::-1]
    peak = float(np.max(np.abs(x)))
    if peak > 0.98:
        x = x / peak * 0.98
    return np.asarray(x, dtype=np.float32)


def _write_clip(audio: np.ndarray, sr: int, start_sec: float, end_sec: float, dest: Path, key: object) -> None:
    start = max(0, int(round(start_sec * sr)))
    end = min(len(audio), int(round(end_sec * sr)))
    if end <= start:
        raise ValueError("empty clip")
    clip = np.asarray(audio[start:end], dtype=np.float32)
    clip = _deidentify_clip(clip, key)
    peak = float(np.max(np.abs(clip))) if clip.size else 0.0
    if peak > 0.98:
        clip = clip / peak * 0.98
    pcm = np.clip(clip * 32767.0, -32768, 32767).astype(np.int16)
    dest.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(dest, sr, pcm)


def _materialise_public_audio(rows: pd.DataFrame, audio_files: dict[str, Path], split_dir: Path) -> list[str]:
    out_dir = split_dir / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)
    rel_paths: list[str] = []
    by_meeting = {m: g.copy() for m, g in rows.groupby("meeting_id")}
    for meeting_id, group in sorted(by_meeting.items()):
        sr, audio = _read_audio(audio_files[meeting_id])
        for _, row in group.iterrows():
            dest_name = f"{int(row['id'])}.wav"
            _write_clip(
                audio,
                sr,
                float(row["clip_start_sec"]),
                float(row["clip_end_sec"]),
                out_dir / dest_name,
                row["source_key"],
            )
    for _, row in rows.iterrows():
        rel_paths.append(f"{split_dir.name}/audio/{int(row['id'])}.wav")
    return rel_paths


def _context_key(row: pd.Series) -> tuple:
    ctx = json.loads(row["speaker_context_json"])
    words = int(ctx.get("current_words", 0))
    word_bucket = "short" if words < 5 else ("medium" if words < 16 else "long")
    return (int(ctx.get("recent_active_speakers", 1)), str(ctx.get("prev_turn_length_bucket", "none")), word_bucket)


def _sample_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    del train
    rows = []
    for i, (_, row) in enumerate(test.iterrows()):
        rows.append(
            {
                "id": int(row["id"]),
                "turn_state": TURN_STATES[i % len(TURN_STATES)],
                "next_response_ms": int((i % 5) * 600),
                "next_speaker_relation": RELATIONS[i % len(RELATIONS)],
                "confidence": 0.5,
            }
        )
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _write_sorted_csv(df: pd.DataFrame, path: Path, columns: list[str]) -> None:
    df[columns].copy().sort_values("id").reset_index(drop=True).to_csv(path, index=False)


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    raw_root = _find_raw_root(raw)
    audio_files = _find_audio_files(raw_root)

    with tempfile.TemporaryDirectory(prefix="ami_prepare_") as tmp:
        ann_root = _annotation_root(raw_root, Path(tmp))
        rows: list[dict] = []
        for meeting_id in DEFAULT_MEETINGS:
            rows.extend(_candidate_rows_for_meeting(ann_root, meeting_id))
    if not rows:
        raise RuntimeError("No AMI boundary candidates derived from source annotations")

    sampled = _balanced_sample(rows)
    df = pd.DataFrame(sampled).sort_values("source_key").reset_index(drop=True)
    if df["source_key"].duplicated().any():
        raise SystemExit("source_key must be unique")
    id_map = _public_id_map(df["source_key"].astype(str).tolist())
    df["id"] = df["source_key"].map(id_map).astype(int)

    train, test = _choose_group_split(df)
    train = train.copy()
    test = test.copy()
    train["audio_path"] = _materialise_public_audio(train, audio_files, public / "train")
    test["audio_path"] = _materialise_public_audio(test, audio_files, public / "test")

    _write_sorted_csv(train, public / "train.csv", PUBLIC_INPUT_COLUMNS + LABEL_COLUMNS)
    _write_sorted_csv(test, public / "test.csv", PUBLIC_INPUT_COLUMNS)
    sample = _sample_submission(train, test)
    _write_sorted_csv(sample, public / "sample_submission.csv", SUBMISSION_COLUMNS)

    answers = test[
        [
            "id",
            "source_key",
            "meeting_id",
            "session_group",
            "speaker_code",
            "turn_state",
            "next_response_ms",
            "next_speaker_relation",
            "confidence",
            "meeting_family",
            "latency_band",
            "turn_type_bucket",
        ]
    ].copy()
    answers["confidence"] = 1.0
    answers["meeting_family"] = _repair_sparse_axis(answers["meeting_family"], MIN_GROUP_TEST)
    answers["turn_type_bucket"] = _repair_sparse_axis(answers["turn_type_bucket"], MIN_GROUP_TEST)
    answers["latency_band"] = _repair_sparse_axis(answers["latency_band"], MIN_GROUP_TEST)
    _write_sorted_csv(
        answers,
        private / "answers.csv",
        [
            "id",
            "source_key",
            "meeting_id",
            "session_group",
            "speaker_code",
            "turn_state",
            "next_response_ms",
            "next_speaker_relation",
            "confidence",
            "meeting_family",
            "latency_band",
            "turn_type_bucket",
        ],
    )

    leakage_columns = {"meeting_id", "session_group", "speaker_code", "segment_id", "source_key", "boundary_time_sec"}
    if leakage_columns & set(pd.read_csv(public / "test.csv", nrows=0).columns):
        raise SystemExit("Leakage-prone columns present in public/test.csv")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)
    print("OK: prepare complete.")
