from __future__ import annotations

import hashlib
import re
import shutil
import wave
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


ID_SALT = "cremad-paired-affect-shift-v1-20260703"
SPLIT_SEED = 0xAF51E7
TEST_FRACTION = 0.25
MIN_GROUP_TEST = 15
MAX_TRAIN_PAIRS = 2400
MAX_TEST_PAIRS = 800

EMOTION_CODES = {"ANG", "DIS", "FEA", "HAP", "NEU", "SAD"}
INTENSITY_CODES = {"LO", "MD", "HI", "XX"}

AFFECT_LABELS = ["angry", "sad", "happy", "neutral_or_unclear", "other_negative"]
VALENCE_LABELS = ["positive", "negative", "no_clear_shift"]
AROUSAL_LABELS = ["higher", "lower", "no_clear_shift"]
ESCALATION_LABELS = ["none", "monitor", "urgent"]

PUBLIC_INPUT_COLUMNS = ["id", "sample_id", "baseline_audio", "current_audio", "pair_duration_bucket"]
LABEL_COLUMNS = ["affect_label", "valence_shift", "arousal_shift", "escalation_tier", "confidence"]
PUBLIC_TRAIN_COLUMNS = PUBLIC_INPUT_COLUMNS + LABEL_COLUMNS
PUBLIC_TEST_COLUMNS = PUBLIC_INPUT_COLUMNS
SUBMISSION_COLUMNS = ["id", "sample_id", "affect_label", "valence_shift", "arousal_shift", "escalation_tier", "confidence"]

FILENAME_RE = re.compile(
    r"^(?P<actor>\d{4})_(?P<sentence>[A-Z]{3})_(?P<emotion>ANG|DIS|FEA|HAP|NEU|SAD)_(?P<intensity>LO|MD|HI|XX)\.wav$",
    re.IGNORECASE,
)

EMOTION_TO_AFFECT = {
    "ANG": "angry",
    "SAD": "sad",
    "HAP": "happy",
    "NEU": "neutral_or_unclear",
    "DIS": "other_negative",
    "FEA": "other_negative",
}
EMOTION_FAMILY = {
    "ANG": "anger",
    "SAD": "sadness",
    "HAP": "happiness",
    "NEU": "neutral",
    "DIS": "other_negative",
    "FEA": "other_negative",
}
VALENCE_SCORE = {"ANG": -1.0, "DIS": -1.0, "FEA": -1.0, "SAD": -0.8, "NEU": 0.0, "HAP": 1.0}
AROUSAL_BASE = {"ANG": 1.8, "DIS": 1.2, "FEA": 1.7, "SAD": 0.4, "NEU": 0.3, "HAP": 1.1}
INTENSITY_SCORE = {"LO": 0.20, "MD": 0.60, "HI": 1.00, "XX": 0.35}
INTENSITY_RANK = {"NEU": 0, "LO": 1, "XX": 2, "MD": 2, "HI": 3}


def _digest(*parts: object) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def _rng(*parts: object) -> np.random.Generator:
    digest = hashlib.sha256(("::".join(map(str, parts))).encode("utf-8")).digest()
    return np.random.default_rng(np.random.SeedSequence(list(digest)))


def _find_raw_root(raw: Path) -> Path:
    raw = Path(raw)
    candidates = [
        raw,
        raw / "raw_upload",
        raw / "raw_data",
        raw / "CREMA-D",
        raw / "crema-d-mirror",
    ]
    candidates.extend(p.parent for p in sorted(raw.rglob("AudioWAV")) if p.is_dir())
    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "AudioWAV").exists() and any((candidate / "AudioWAV").rglob("*.wav")):
            return candidate
    raise FileNotFoundError(
        "Official CREMA-D raw layout not found. Expected AudioWAV/*.wav from "
        "https://github.com/CheyneyComputerScience/CREMA-D, optionally with "
        "LICENSE.txt, SentenceFilenames.csv, VideoDemographics.csv, and processedResults/."
    )


def _parse_clip(path: Path) -> dict[str, object] | None:
    match = FILENAME_RE.match(path.name)
    if not match:
        return None
    actor = match.group("actor")
    sentence = match.group("sentence").upper()
    emotion = match.group("emotion").upper()
    intensity = match.group("intensity").upper()
    source_key = path.stem
    return {
        "source_key": source_key,
        "path": str(path),
        "actor_id": actor,
        "sentence_code": sentence,
        "emotion_code": emotion,
        "intensity_code": intensity,
        "clip_group": _digest("clip", source_key)[:24],
    }


def _load_clips(raw_root: Path, smoke: bool) -> pd.DataFrame:
    audio_dir = raw_root / "AudioWAV"
    rows = [_parse_clip(path) for path in sorted(audio_dir.rglob("*.wav"))]
    rows = [row for row in rows if row is not None]
    if not rows:
        raise SystemExit(f"No CREMA-D style WAV filenames were found under {audio_dir}")
    df = pd.DataFrame(rows)
    required = {"actor_id", "sentence_code", "emotion_code", "intensity_code", "source_key", "path"}
    if df[list(required)].isna().any().any():
        raise SystemExit("Parsed CREMA-D clip table contains missing required values")
    if df["source_key"].duplicated().any():
        raise SystemExit("CREMA-D source clip names must be unique")
    bad_emotions = sorted(set(df["emotion_code"]) - EMOTION_CODES)
    bad_intensities = sorted(set(df["intensity_code"]) - INTENSITY_CODES)
    if bad_emotions or bad_intensities:
        raise SystemExit(f"Unexpected CREMA-D filename labels: emotions={bad_emotions}, intensities={bad_intensities}")
    if not smoke and (df["actor_id"].nunique() < 24 or len(df) < 300):
        raise SystemExit(
            "Too few official CREMA-D WAV files for a speaker-held challenge. "
            "Use the full AudioWAV directory or a documented official subset with at least 24 actors and 300 clips."
        )
    return df


def _read_demographics(raw_root: Path) -> pd.DataFrame:
    path = raw_root / "VideoDemographics.csv"
    if not path.exists():
        return pd.DataFrame(columns=["actor_id", "actor_sex", "actor_race"])
    df = pd.read_csv(path, dtype=str)
    cols = {c.lower().strip(): c for c in df.columns}
    actor_col = cols.get("actorid") or cols.get("actor_id") or cols.get("actor")
    sex_col = cols.get("sex") or cols.get("gender")
    race_col = cols.get("race")
    if actor_col is None:
        return pd.DataFrame(columns=["actor_id", "actor_sex", "actor_race"])
    out = pd.DataFrame()
    out["actor_id"] = df[actor_col].astype(str).str.extract(r"(\d{4})", expand=False)
    out["actor_sex"] = df[sex_col].astype(str).str.strip().replace({"": "unknown"}) if sex_col else "unknown"
    out["actor_race"] = df[race_col].astype(str).str.strip().replace({"": "unknown"}) if race_col else "unknown"
    out = out.dropna(subset=["actor_id"]).drop_duplicates("actor_id")
    return out


def _emotion_intensity_score(row: pd.Series | dict[str, object]) -> float:
    emotion = str(row["emotion_code"])
    intensity = str(row["intensity_code"])
    if emotion == "NEU":
        return 0.2
    return float(AROUSAL_BASE[emotion] + INTENSITY_SCORE[intensity])


def _intensity_rank(row: pd.Series | dict[str, object]) -> int:
    emotion = str(row["emotion_code"])
    intensity = str(row["intensity_code"])
    if emotion == "NEU":
        return INTENSITY_RANK["NEU"]
    return INTENSITY_RANK[intensity]


def _valence_shift(base: pd.Series, current: pd.Series) -> str:
    diff = VALENCE_SCORE[str(current["emotion_code"])] - VALENCE_SCORE[str(base["emotion_code"])]
    if diff >= 0.55:
        return "positive"
    if diff <= -0.55:
        return "negative"
    return "no_clear_shift"


def _arousal_shift(base: pd.Series, current: pd.Series) -> str:
    diff = _emotion_intensity_score(current) - _emotion_intensity_score(base)
    if diff >= 0.55:
        return "higher"
    if diff <= -0.55:
        return "lower"
    return "no_clear_shift"


def _escalation_tier(base: pd.Series, current: pd.Series, valence_shift: str, arousal_shift: str) -> str:
    emotion = str(current["emotion_code"])
    intensity = str(current["intensity_code"])
    rank = _intensity_rank(current)
    if emotion == "ANG" and (rank >= 2 or arousal_shift == "higher"):
        return "urgent"
    if emotion in {"DIS", "FEA"} and intensity == "HI" and arousal_shift == "higher":
        return "urgent"
    if emotion in {"ANG", "DIS", "FEA", "SAD"}:
        return "monitor"
    if valence_shift == "negative" or (arousal_shift == "higher" and emotion != "HAP"):
        return "monitor"
    return "none"


def _confidence(base: pd.Series, current: pd.Series, escalation: str) -> float:
    emotion = str(current["emotion_code"])
    intensity = str(current["intensity_code"])
    score = 0.82
    if emotion in {"DIS", "FEA"}:
        score -= 0.05
    if intensity == "XX" and emotion != "NEU":
        score -= 0.04
    if str(base["emotion_code"]) != "NEU" and emotion != "NEU":
        score -= 0.03
    if escalation == "urgent":
        score += 0.03
    return float(np.clip(score, 0.62, 0.94))


def _duration_bucket(base_duration_ms: int, current_duration_ms: int) -> str:
    total = base_duration_ms + current_duration_ms
    if total < 4500:
        return "short_pair"
    if total < 7600:
        return "medium_pair"
    return "long_pair"


def _wav_duration_ms(path: Path) -> int:
    with wave.open(str(path), "rb") as wf:
        frames = wf.getnframes()
        sr = wf.getframerate()
    if sr <= 0:
        raise ValueError(f"Invalid WAV sample rate in {path}")
    return int(round(frames * 1000.0 / sr))


def _read_wav_mono(path: Path) -> tuple[int, np.ndarray]:
    with wave.open(str(path), "rb") as wf:
        sr = wf.getframerate()
        channels = wf.getnchannels()
        width = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())
    if width == 1:
        x = (np.frombuffer(frames, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    elif width == 2:
        x = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
    elif width == 4:
        x = np.frombuffer(frames, dtype="<i4").astype(np.float32) / 2147483648.0
    else:
        raise ValueError(f"Unsupported WAV sample width {width} in {path}")
    if channels > 1:
        x = x.reshape(-1, channels).mean(axis=1)
    return sr, x.astype(np.float32, copy=False)


def _resample_linear(x: np.ndarray, n: int) -> np.ndarray:
    n = max(16, int(n))
    if len(x) == n:
        return x.astype(np.float32, copy=False)
    old = np.linspace(0.0, 1.0, num=len(x), endpoint=False)
    new = np.linspace(0.0, 1.0, num=n, endpoint=False)
    return np.interp(new, old, x).astype(np.float32)


def _one_pole_lowpass(x: np.ndarray, alpha: float) -> np.ndarray:
    y = np.empty_like(x, dtype=np.float32)
    if len(x) == 0:
        return y
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = y[i - 1] + alpha * (x[i] - y[i - 1])
    return y


def _write_wav_mono(path: Path, sr: int, x: np.ndarray) -> None:
    x = np.nan_to_num(x.astype(np.float32, copy=False), nan=0.0, posinf=0.0, neginf=0.0)
    peak = float(np.max(np.abs(x))) if len(x) else 0.0
    if peak > 0.98:
        x = x * (0.98 / peak)
    pcm = np.clip(np.round(x * 32767.0), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def _public_audio_transform(src: Path, source_key: str, split_name: str) -> tuple[int, np.ndarray]:
    sr, x = _read_wav_mono(src)
    if sr <= 0 or len(x) < 64:
        raise ValueError(f"Invalid or too-short WAV clip: {src}")
    rng = _rng("public-audio-transform", split_name, source_key)
    target_sr = 16000
    if sr != target_sr:
        x = _resample_linear(x, int(round(len(x) * target_sr / sr)))
        sr = target_sr

    codec_factor = float(rng.choice(np.array([0.42, 0.50, 0.58, 0.66, 0.74], dtype=np.float32)))
    x = _resample_linear(_resample_linear(x, int(round(len(x) * codec_factor))), len(x))

    rate = float(rng.uniform(0.90, 1.11))
    x = _resample_linear(x, int(round(len(x) / rate)))

    base_idx = np.arange(len(x), dtype=np.float32)
    warp_depth = float(rng.uniform(0.0015, 0.0045)) * sr
    warp_freq = float(rng.uniform(0.7, 2.4))
    warp_phase = float(rng.uniform(0.0, 2.0 * np.pi))
    warped_idx = base_idx + warp_depth * np.sin(2.0 * np.pi * warp_freq * base_idx / sr + warp_phase)
    warped_idx = np.maximum.accumulate(np.clip(warped_idx, 0.0, max(0.0, len(x) - 1.0)))
    x = np.interp(base_idx, warped_idx, x).astype(np.float32)

    trim_front = int(rng.integers(int(0.020 * sr), int(0.120 * sr) + 1))
    trim_back = int(rng.integers(int(0.020 * sr), int(0.140 * sr) + 1))
    if len(x) > trim_front + trim_back + int(0.75 * sr):
        x = x[trim_front : len(x) - trim_back]
    pad_front = int(rng.integers(int(0.030 * sr), int(0.160 * sr) + 1))
    pad_back = int(rng.integers(int(0.020 * sr), int(0.170 * sr) + 1))
    x = np.pad(x, (pad_front, pad_back), mode="constant")

    alpha = float(rng.uniform(0.015, 0.130))
    low = _one_pole_lowpass(x, alpha)
    high = x - low
    x = low * float(rng.uniform(0.45, 1.45)) + high * float(rng.uniform(0.35, 1.35))

    threshold = float(rng.uniform(0.09, 0.22))
    ratio = float(rng.uniform(0.22, 0.52))
    mag = np.abs(x)
    compressed = np.where(mag > threshold, threshold + (mag - threshold) * ratio, mag)
    x = np.sign(x) * compressed

    ir_len = int(rng.integers(int(0.080 * sr), int(0.240 * sr) + 1))
    t = np.arange(ir_len, dtype=np.float32) / float(sr)
    ir = np.exp(-t * float(rng.uniform(14.0, 26.0))).astype(np.float32)
    ir *= float(rng.uniform(0.040, 0.115))
    ir[0] = 1.0
    for delay_ms in [float(rng.uniform(8, 24)), float(rng.uniform(26, 58)), float(rng.uniform(65, 135))]:
        idx = int(round(delay_ms * sr / 1000.0))
        if 0 < idx < len(ir):
            ir[idx] += float(rng.uniform(0.025, 0.095))
    x = np.convolve(x, ir, mode="full")[: len(x)].astype(np.float32)

    noise = rng.normal(0.0, float(rng.uniform(0.0025, 0.0065)), size=len(x)).astype(np.float32)
    rumble = _one_pole_lowpass(noise, float(rng.uniform(0.006, 0.018)))
    x = x + noise + 0.60 * rumble

    rms = float(np.sqrt(np.mean(np.square(x))) + 1e-8)
    target_rms = float(rng.uniform(0.055, 0.095))
    x = x * (target_rms / rms)
    x = np.tanh(x * float(rng.uniform(1.00, 1.18))) / 1.18
    quant = float(rng.choice(np.array([2048.0, 3072.0, 4096.0], dtype=np.float32)))
    x = np.round(np.clip(x, -0.98, 0.98) * quant) / quant
    return sr, x.astype(np.float32, copy=False)


def _build_pairs(clips: pd.DataFrame) -> pd.DataFrame:
    durations = {str(row.source_key): _wav_duration_ms(Path(str(row.path))) for row in clips.itertuples(index=False)}
    rows: list[dict[str, object]] = []
    grouped = clips.groupby(["actor_id", "sentence_code"], sort=True)
    for (_, _), group in grouped:
        group = group.sort_values(["emotion_code", "intensity_code", "source_key"]).reset_index(drop=True)
        neutral = group[group["emotion_code"].eq("NEU")]
        non_neutral = group[~group["emotion_code"].eq("NEU")]
        neutral_row = neutral.iloc[0] if not neutral.empty else None

        if neutral_row is not None:
            for _, current in non_neutral.iterrows():
                rows.append(_pair_row(neutral_row, current, durations, "neutral_reference"))
            for _, current in neutral.iterrows():
                rows.append(_pair_row(neutral_row, current, durations, "stable_neutral"))

        for emotion, emo_group in non_neutral.groupby("emotion_code", sort=True):
            lows = emo_group[emo_group["intensity_code"].eq("LO")]
            highs = emo_group[emo_group["intensity_code"].isin(["MD", "HI", "XX"])]
            if not lows.empty:
                base = lows.iloc[0]
                for _, current in highs.iterrows():
                    if str(base["source_key"]) != str(current["source_key"]):
                        rows.append(_pair_row(base, current, durations, "same_affect_escalation"))
            if neutral_row is not None:
                strong = emo_group[emo_group["intensity_code"].isin(["HI", "MD", "XX"])].head(1)
                for _, base in strong.iterrows():
                    rows.append(_pair_row(base, neutral_row, durations, "return_to_neutral"))

        happy = non_neutral[non_neutral["emotion_code"].eq("HAP")]
        negative = non_neutral[non_neutral["emotion_code"].isin(["ANG", "DIS", "FEA", "SAD"])]
        if not happy.empty and not negative.empty:
            hbase = happy.sort_values(["intensity_code", "source_key"]).iloc[0]
            ncur = negative.sort_values(["emotion_code", "intensity_code", "source_key"]).iloc[0]
            rows.append(_pair_row(hbase, ncur, durations, "cross_affect_negative"))
            nbase = negative.sort_values(["emotion_code", "intensity_code", "source_key"]).iloc[0]
            hcur = happy.sort_values(["intensity_code", "source_key"]).iloc[-1]
            rows.append(_pair_row(nbase, hcur, durations, "cross_affect_positive"))

    if not rows:
        raise SystemExit("No paired CREMA-D rows could be constructed")
    df = pd.DataFrame(rows).drop_duplicates("pair_key").reset_index(drop=True)
    return df


def _pair_row(base: pd.Series, current: pd.Series, durations: dict[str, int], construction: str) -> dict[str, object]:
    valence = _valence_shift(base, current)
    arousal = _arousal_shift(base, current)
    escalation = _escalation_tier(base, current, valence, arousal)
    base_key = str(base["source_key"])
    current_key = str(current["source_key"])
    pair_key = _digest("pair", base_key, current_key, construction)[:32]
    base_duration = int(durations[base_key])
    current_duration = int(durations[current_key])
    intensity_delta = _intensity_rank(current) - _intensity_rank(base)
    if intensity_delta >= 1:
        transition = "stronger_current"
    elif intensity_delta <= -1:
        transition = "calmer_current"
    else:
        transition = "similar_intensity"
    return {
        "pair_key": pair_key,
        "baseline_source_key": base_key,
        "current_source_key": current_key,
        "baseline_path": str(base["path"]),
        "current_path": str(current["path"]),
        "actor_id": str(base["actor_id"]),
        "sentence_code": str(base["sentence_code"]),
        "baseline_emotion_code": str(base["emotion_code"]),
        "baseline_intensity_code": str(base["intensity_code"]),
        "current_emotion_code": str(current["emotion_code"]),
        "current_intensity_code": str(current["intensity_code"]),
        "affect_label": EMOTION_TO_AFFECT[str(current["emotion_code"])],
        "valence_shift": valence,
        "arousal_shift": arousal,
        "escalation_tier": escalation,
        "confidence": round(_confidence(base, current, escalation), 4),
        "pair_duration_bucket": _duration_bucket(base_duration, current_duration),
        "baseline_duration_ms": base_duration,
        "current_duration_ms": current_duration,
        "current_affect_family": EMOTION_FAMILY[str(current["emotion_code"])],
        "baseline_affect_family": EMOTION_FAMILY[str(base["emotion_code"])],
        "intensity_transition": transition,
        "sentence_group": str(base["sentence_code"]),
        "pair_construction": construction,
    }


def _score_actor_split(pairs: pd.DataFrame, test_actors: set[str], min_group: int) -> tuple[float, int]:
    test = pairs[pairs["actor_id"].isin(test_actors)]
    if test.empty:
        return float("inf"), 10_000
    penalty = 0
    for col, labels in [
        ("affect_label", AFFECT_LABELS),
        ("valence_shift", VALENCE_LABELS),
        ("arousal_shift", AROUSAL_LABELS),
        ("escalation_tier", ESCALATION_LABELS),
    ]:
        counts = test[col].astype(str).value_counts()
        for label in labels:
            count = int(counts.get(label, 0))
            if count < min_group:
                penalty += (min_group - count) * 100
    for col in ["current_affect_family", "baseline_affect_family", "intensity_transition", "sentence_group", "pair_construction"]:
        counts = test[col].astype(str).value_counts()
        under = counts[counts < min_group]
        penalty += int((min_group - under).clip(lower=0).sum()) * 30
    target = len(pairs) * TEST_FRACTION
    size_penalty = abs(len(test) - target) / max(1.0, target)
    distribution_penalty = 0.0
    for col in ["affect_label", "escalation_tier"]:
        full = pairs[col].astype(str).value_counts(normalize=True)
        test_dist = test[col].astype(str).value_counts(normalize=True)
        distribution_penalty += sum(abs(float(test_dist.get(k, 0.0)) - float(v)) for k, v in full.items())
    jitter = int(_digest("split", sorted(test_actors), SPLIT_SEED)[:6], 16) / 16**6 * 0.001
    return size_penalty + distribution_penalty + jitter, penalty


def _choose_actor_split(pairs: pd.DataFrame, smoke: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    actors = sorted(pairs["actor_id"].astype(str).unique())
    if len(actors) < 2:
        raise SystemExit("Need at least two CREMA-D actors for a speaker-held split")
    min_group = 1 if smoke else MIN_GROUP_TEST
    n_test = max(1, min(len(actors) - 1, int(round(len(actors) * TEST_FRACTION))))
    rng = np.random.default_rng(SPLIT_SEED)
    best: tuple[int, float, set[str]] | None = None
    if len(actors) <= 12:
        trials = []
        for mask in range(1, 1 << len(actors)):
            if bin(mask).count("1") == n_test:
                trials.append({actors[i] for i in range(len(actors)) if mask & (1 << i)})
    else:
        trials = []
        for _ in range(6000):
            trials.append(set(rng.choice(actors, size=n_test, replace=False).tolist()))
    for candidate in trials:
        size_dist, penalty = _score_actor_split(pairs, candidate, min_group)
        if best is None or (penalty, size_dist) < (best[0], best[1]):
            best = (penalty, size_dist, candidate)
            if penalty == 0 and size_dist < 0.06:
                break
    if best is None:
        raise SystemExit("Could not choose a speaker-held split")
    train = pairs[~pairs["actor_id"].isin(best[2])].copy()
    test = pairs[pairs["actor_id"].isin(best[2])].copy()
    if set(train["actor_id"]) & set(test["actor_id"]):
        raise SystemExit("Actor leakage across train/test split")
    return train, test


def _balanced_downsample(df: pd.DataFrame, limit: int, split_name: str) -> pd.DataFrame:
    if limit <= 0 or len(df) <= limit:
        return df.copy()
    groups: dict[str, list[int]] = defaultdict(list)
    for idx, row in df.iterrows():
        key = "|".join(
            [
                str(row["affect_label"]),
                str(row["valence_shift"]),
                str(row["arousal_shift"]),
                str(row["escalation_tier"]),
            ]
        )
        groups[key].append(int(idx))
    for key, indices in groups.items():
        indices.sort(key=lambda i: _digest("downsample", split_name, key, df.loc[i, "pair_key"]))
    ordered_keys = sorted(groups, key=lambda k: _digest("downsample-key", split_name, k))
    chosen: list[int] = []
    while len(chosen) < limit and ordered_keys:
        next_keys = []
        for key in ordered_keys:
            if groups[key] and len(chosen) < limit:
                chosen.append(groups[key].pop(0))
            if groups[key]:
                next_keys.append(key)
        ordered_keys = next_keys
    return df.loc[chosen].copy()


def _public_id_map(pair_keys: list[str]) -> dict[str, int]:
    hashed = [(hashlib.sha256(f"{ID_SALT}:id:{key}".encode("utf-8")).hexdigest(), key) for key in pair_keys]
    if len({d for d, _ in hashed}) != len(hashed):
        raise SystemExit("Public id hash collision")
    return {key: 100000 + i for i, (_, key) in enumerate(sorted(hashed))}


def _public_clip_name(source_key: str, split_name: str) -> str:
    return f"a{_digest('audio-name', ID_SALT, split_name, source_key)[:18]}.wav"


def _materialize_audio(rows: pd.DataFrame, split_dir: Path, split_name: str) -> tuple[dict[str, str], dict[str, int]]:
    audio_dir = split_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    source_to_path: dict[str, str] = {}
    source_to_size: dict[str, int] = {}
    source_paths: dict[str, str] = {}
    for _, row in rows.iterrows():
        source_paths[str(row["baseline_source_key"])] = str(row["baseline_path"])
        source_paths[str(row["current_source_key"])] = str(row["current_path"])
    for source_key, src in sorted(source_paths.items()):
        name = _public_clip_name(source_key, split_name)
        dest = audio_dir / name
        sr, audio = _public_audio_transform(Path(src), source_key, split_name)
        _write_wav_mono(dest, sr, audio)
        source_to_path[source_key] = f"{split_name}/audio/{name}"
        source_to_size[source_key] = dest.stat().st_size
    return source_to_path, source_to_size


def _apply_public_paths(rows: pd.DataFrame, path_map: dict[str, str]) -> pd.DataFrame:
    out = rows.copy()
    out["baseline_audio"] = out["baseline_source_key"].map(path_map)
    out["current_audio"] = out["current_source_key"].map(path_map)
    if out[["baseline_audio", "current_audio"]].isna().any().any():
        raise SystemExit("Missing public audio path after materialization")
    return out


def _sample_submission(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i, (_, row) in enumerate(test.sort_values("sample_id").iterrows()):
        rows.append(
            {
                "id": int(row["id"]),
                "sample_id": int(row["sample_id"]),
                "affect_label": AFFECT_LABELS[i % len(AFFECT_LABELS)],
                "valence_shift": VALENCE_LABELS[(i // 2) % len(VALENCE_LABELS)],
                "arousal_shift": AROUSAL_LABELS[(i // 3) % len(AROUSAL_LABELS)],
                "escalation_tier": ESCALATION_LABELS[(i // 5) % len(ESCALATION_LABELS)],
                "confidence": 0.38,
            }
        )
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _repair_sparse_groups(series: pd.Series, min_group: int) -> pd.Series:
    counts = series.astype(str).value_counts()
    if counts.empty:
        return series.astype(str)
    rare = set(counts[counts < min_group].index.astype(str))
    if not rare:
        return series.astype(str)
    majority = str(counts.idxmax())
    rare_total = int(series.astype(str).isin(rare).sum())
    replacement = "OTHER" if rare_total >= min_group else majority
    return series.astype(str).map(lambda x: replacement if x in rare else x)


def _validate_outputs(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, public: Path, min_group: int) -> None:
    if set(train["sample_id"]) & set(test["sample_id"]):
        raise SystemExit("sample_id leakage across train/test")
    if set(train["id"]) & set(test["id"]):
        raise SystemExit("id leakage across train/test")
    if not (train["id"].astype(int).equals(train["sample_id"].astype(int)) and test["id"].astype(int).equals(test["sample_id"].astype(int))):
        raise SystemExit("id and sample_id must match exactly")
    if set(train["actor_id"]) & set(test["actor_id"]):
        raise SystemExit("actor leakage across train/test")
    for frame, name in [(train, "train"), (test, "test"), (answers, "answers")]:
        if frame.isna().any().any():
            raise SystemExit(f"{name} contains NaN values")
        if frame.astype(str).apply(lambda col: col.str.len().eq(0)).any().any():
            raise SystemExit(f"{name} contains blank values")
    for col, labels in [
        ("affect_label", AFFECT_LABELS),
        ("valence_shift", VALENCE_LABELS),
        ("arousal_shift", AROUSAL_LABELS),
        ("escalation_tier", ESCALATION_LABELS),
    ]:
        missing = set(test[col].astype(str)) - set(labels)
        if missing:
            raise SystemExit(f"Unknown {col} labels in private test: {missing}")
    for axis in ["current_affect_family", "baseline_affect_family", "intensity_transition", "sentence_group", "pair_construction"]:
        counts = answers[axis].astype(str).value_counts()
        if (counts < min_group).any():
            raise SystemExit(f"Underfilled hidden subgroup {axis}: {counts.to_dict()}")
    public_test_cols = set(pd.read_csv(public / "test.csv", nrows=0).columns)
    forbidden = {
        "actor_id",
        "sentence_code",
        "baseline_source_key",
        "current_source_key",
        "baseline_emotion_code",
        "current_emotion_code",
        "baseline_intensity_code",
        "current_intensity_code",
        "pair_key",
    }
    if forbidden & public_test_cols:
        raise SystemExit(f"Leakage-prone public columns present: {sorted(forbidden & public_test_cols)}")
    leak_re = re.compile(r"\d{4}_[A-Z]{3}_(ANG|DIS|FEA|HAP|NEU|SAD)_(LO|MD|HI|XX)", re.IGNORECASE)
    for csv_path in [public / "train.csv", public / "test.csv", public / "sample_submission.csv"]:
        text = csv_path.read_text(encoding="utf-8")
        if leak_re.search(text):
            raise SystemExit(f"Original CREMA-D filename token leaked into {csv_path}")
    for rel in pd.concat([train["baseline_audio"], train["current_audio"], test["baseline_audio"], test["current_audio"]]).astype(str):
        path = public / rel
        if not path.exists() or path.stat().st_size < 512:
            raise SystemExit(f"Missing or too-small public audio file: {rel}")


def _write_sorted(df: pd.DataFrame, path: Path, columns: list[str]) -> None:
    sort_col = "id" if "id" in columns else "sample_id"
    df[columns].copy().sort_values(sort_col).reset_index(drop=True).to_csv(path, index=False)


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    if public.exists():
        shutil.rmtree(public)
    if private.exists():
        shutil.rmtree(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    raw_root = _find_raw_root(raw)
    smoke = (raw_root / "SMOKE_FIXTURE_ONLY.txt").exists()
    min_group = 1 if smoke else MIN_GROUP_TEST
    clips = _load_clips(raw_root, smoke=smoke)
    demo = _read_demographics(raw_root)
    pairs = _build_pairs(clips)
    if not demo.empty:
        pairs = pairs.merge(demo, on="actor_id", how="left")
    else:
        pairs["actor_sex"] = "unknown"
        pairs["actor_race"] = "unknown"
    pairs["actor_sex"] = pairs["actor_sex"].fillna("unknown").astype(str)
    pairs["actor_race"] = pairs["actor_race"].fillna("unknown").astype(str)

    train, test = _choose_actor_split(pairs, smoke=smoke)
    train = _balanced_downsample(train, 200 if smoke else MAX_TRAIN_PAIRS, "train")
    test = _balanced_downsample(test, 120 if smoke else MAX_TEST_PAIRS, "test")

    all_keys = train["pair_key"].astype(str).tolist() + test["pair_key"].astype(str).tolist()
    id_map = _public_id_map(all_keys)
    train["sample_id"] = train["pair_key"].map(id_map).astype(int)
    test["sample_id"] = test["pair_key"].map(id_map).astype(int)
    train["id"] = train["sample_id"].astype(int)
    test["id"] = test["sample_id"].astype(int)

    train_paths, train_sizes = _materialize_audio(train, public / "train", "train")
    test_paths, test_sizes = _materialize_audio(test, public / "test", "test")
    train = _apply_public_paths(train, train_paths)
    test = _apply_public_paths(test, test_paths)

    _write_sorted(train, public / "train.csv", PUBLIC_TRAIN_COLUMNS)
    _write_sorted(test, public / "test.csv", PUBLIC_TEST_COLUMNS)
    sample = _sample_submission(test)
    _write_sorted(sample, public / "sample_submission.csv", SUBMISSION_COLUMNS)

    answers = test[
        [
            "id",
            "sample_id",
            "affect_label",
            "valence_shift",
            "arousal_shift",
            "escalation_tier",
            "confidence",
            "current_affect_family",
            "baseline_affect_family",
            "intensity_transition",
            "sentence_group",
            "pair_construction",
            "actor_id",
            "actor_sex",
            "actor_race",
            "baseline_source_key",
            "current_source_key",
            "pair_key",
            "baseline_duration_ms",
            "current_duration_ms",
            "pair_duration_bucket",
        ]
    ].copy()
    for axis in [
        "current_affect_family",
        "baseline_affect_family",
        "intensity_transition",
        "sentence_group",
        "pair_construction",
        "actor_sex",
        "actor_race",
    ]:
        answers[axis] = _repair_sparse_groups(answers[axis], min_group)
    answers["confidence"] = 1.0
    _write_sorted(
        answers,
        private / "answers.csv",
        [
            "id",
            "sample_id",
            "affect_label",
            "valence_shift",
            "arousal_shift",
            "escalation_tier",
            "confidence",
            "current_affect_family",
            "baseline_affect_family",
            "intensity_transition",
            "sentence_group",
            "pair_construction",
            "actor_id",
            "actor_sex",
            "actor_race",
            "baseline_source_key",
            "current_source_key",
            "pair_key",
            "baseline_duration_ms",
            "current_duration_ms",
            "pair_duration_bucket",
        ],
    )

    diagnostics = pd.concat(
        [
            train.assign(split="train"),
            test.assign(split="test"),
        ],
        ignore_index=True,
    )[
        [
            "id",
            "sample_id",
            "split",
            "actor_id",
            "sentence_code",
            "baseline_source_key",
            "current_source_key",
            "affect_label",
            "valence_shift",
            "arousal_shift",
            "escalation_tier",
            "pair_construction",
        ]
    ].sort_values("sample_id")
    diagnostics.to_csv(private / "split_diagnostics.csv", index=False)

    size_report = {
        "train_unique_audio": len(train_paths),
        "test_unique_audio": len(test_paths),
        "train_audio_bytes": int(sum(train_sizes.values())),
        "test_audio_bytes": int(sum(test_sizes.values())),
        "raw_root": str(raw_root),
        "smoke_fixture": bool(smoke),
    }
    pd.Series(size_report).to_json(private / "prepare_report.json", indent=2)
    _validate_outputs(train, test, answers, public, min_group)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prepare paired user affect shift challenge from official CREMA-D AudioWAV files.")
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)
    print("OK: prepared CREMA-D paired affect shift challenge.")
