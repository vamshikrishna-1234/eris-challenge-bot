from __future__ import annotations

import argparse
import hashlib
import math
import shutil
import tarfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly


TARGET_SR = 16000
MAX_CLIP_SECONDS = 6.0
DEFAULT_MAX_EXAMPLES = 560
ID_SALT = "blind-room-scale-echo-zone-v1"
MIN_GROUP_TEST = 12

REQUIRED_OFFICIAL_FILES = {
    "ACE_Corpus_RIRN_Single.tbz2": (
        "https://zenodo.org/record/6257551/files/ACE_Corpus_RIRN_Single.tbz2?download=1",
        "~417.2 MB",
    ),
    "ACE_Corpus_Speech.tbz2": (
        "https://zenodo.org/record/6257551/files/ACE_Corpus_Speech.tbz2?download=1",
        "~148.2 MB",
    ),
    "ACE_Corpus_Data.tbz2": (
        "https://zenodo.org/record/6257551/files/ACE_Corpus_Data.tbz2?download=1",
        "~1.2 MB",
    ),
}

ROOM_TABLE = {
    "502": {
        "room_name": "Office_1",
        "length_m": 3.32,
        "width_m": 4.83,
        "height_m": 2.95,
        "volume_m3": 47.30,
    },
    "803": {
        "room_name": "Office_2",
        "length_m": 3.22,
        "width_m": 5.10,
        "height_m": 2.94,
        "volume_m3": 48.30,
    },
    "503": {
        "room_name": "Meeting_Room_1",
        "length_m": 6.61,
        "width_m": 5.11,
        "height_m": 2.95,
        "volume_m3": 99.60,
    },
    "611": {
        "room_name": "Meeting_Room_2",
        "length_m": 10.30,
        "width_m": 9.07,
        "height_m": 2.63,
        "volume_m3": 246.00,
    },
    "508": {
        "room_name": "Lecture_Room_1",
        "length_m": 6.93,
        "width_m": 9.73,
        "height_m": 3.00,
        "volume_m3": 202.00,
    },
    "403a": {
        "room_name": "Lecture_Room_2",
        "length_m": 13.60,
        "width_m": 9.29,
        "height_m": 2.94,
        "volume_m3": 370.00,
    },
    "EE_lobby": {
        "room_name": "Building_Lobby",
        "length_m": 4.47,
        "width_m": 5.13,
        "height_m": 3.18,
        "volume_m3": 72.90,
    },
}

ROOM_CONDITIONS = {
    41: {"room_id": "502", "distance_label": "Short", "room_config": "1", "dataset": "Dev"},
    47: {"room_id": "502", "distance_label": "Long", "room_config": "2", "dataset": "Dev"},
    115: {"room_id": "EE_lobby", "distance_label": "Short", "room_config": "1", "dataset": "Dev"},
    125: {"room_id": "EE_lobby", "distance_label": "Long", "room_config": "2", "dataset": "Dev"},
    9: {"room_id": "803", "distance_label": "Short", "room_config": "1", "dataset": "Eval"},
    17: {"room_id": "803", "distance_label": "Long", "room_config": "2", "dataset": "Eval"},
    25: {"room_id": "611", "distance_label": "Short", "room_config": "1", "dataset": "Eval"},
    33: {"room_id": "611", "distance_label": "Long", "room_config": "2", "dataset": "Eval"},
    62: {"room_id": "503", "distance_label": "Short", "room_config": "1", "dataset": "Eval"},
    67: {"room_id": "503", "distance_label": "Long", "room_config": "2", "dataset": "Eval"},
    79: {"room_id": "403a", "distance_label": "Short", "room_config": "1", "dataset": "Eval"},
    84: {"room_id": "403a", "distance_label": "Long", "room_config": "2", "dataset": "Eval"},
    97: {"room_id": "508", "distance_label": "Short", "room_config": "1", "dataset": "Eval"},
    101: {"room_id": "508", "distance_label": "Long", "room_config": "2", "dataset": "Eval"},
}

# One source-microphone condition per room is held out, while the companion
# condition for the same room remains in training. Speech files are also held
# out independently, so neither original utterances nor RIRs cross the split.
TEST_SESSION_IDS = {47, 115, 17, 33, 62, 84, 97}
DEV_SESSION_IDS = {41, 47, 115, 125}
NOISE_TYPES = ["Ambient", "Fan", "Babble"]
SNR_LEVELS = [-1, 12, 18]

TRAIN_COLUMNS = [
    "sample_id",
    "audio_path",
    "prompt",
    "room_volume_bucket",
    "rt60_bucket",
    "source_mic_distance_bucket",
    "echo_zone",
    "confidence",
]
TEST_COLUMNS = ["sample_id", "audio_path", "prompt"]
SUBMISSION_COLUMNS = [
    "sample_id",
    "room_volume_bucket",
    "rt60_bucket",
    "source_mic_distance_bucket",
    "echo_zone",
    "confidence",
]
ANSWER_COLUMNS = SUBMISSION_COLUMNS + [
    "room_size_family",
    "rt60_regime",
    "distance_bucket_hidden",
    "noise_condition",
    "speech_split",
    "mic_source_config",
]
PROMPT = "Infer the acoustic environment profile from this reverberant speech clip."


@dataclass(frozen=True)
class AcousticCondition:
    session_id: int
    room_id: str
    room_name: str
    room_config: str
    distance_label: str
    gt_config: str
    rir_label: str
    rir_path: Path
    noise_paths: dict[str, Path]
    rt60: float
    drr: float
    volume_m3: float


@dataclass(frozen=True)
class Candidate:
    split: str
    speech_id: str
    speech_path: Path
    condition: AcousticCondition
    noise_type: str
    snr_db: int


def _hash_text(*parts: object) -> str:
    return hashlib.sha256(":".join(str(p) for p in parts).encode("utf-8")).hexdigest()


def _normalize_columns(columns: list[str]) -> list[str]:
    out = []
    for col in columns:
        c = str(col).strip().strip(":").lower()
        for old, new in [(" ", "_"), ("(", ""), (")", ""), ("+", "plus"), ("-", "minus")]:
            c = c.replace(old, new)
        out.append(c.strip("_"))
    return out


def _safe_extract_tar(archive: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:*") as tf:
        tf.extractall(dest, filter="data")


def _raw_roots(raw: Path) -> list[Path]:
    roots = [raw, raw / "raw_upload", raw / "raw_data"]
    return [r for r in roots if r.exists()]


def _find_named_file(raw: Path, name: str) -> Path | None:
    for root in _raw_roots(raw):
        direct = root / name
        if direct.exists():
            return direct
        matches = list(root.rglob(name))
        if matches:
            return matches[0]
    return None


def _official_missing_message(raw: Path) -> str:
    lines = [
        "Official ACE source files were not found.",
        f"Looked under: {raw}",
        "Place or URL-import these unmodified files at raw/ or raw/raw_upload/:",
    ]
    for name, (url, size) in REQUIRED_OFFICIAL_FILES.items():
        lines.append(f"- {name} ({size}) from {url}")
    lines.append(
        "This challenge intentionally has no raw_upload.zip; the official ACE archives are the raw source."
    )
    lines.append("For smoke tests only, run prepare.py with --allow-fixture on a fixture raw folder.")
    return "\n".join(lines)


def _ensure_official_sources(raw: Path) -> list[Path]:
    roots = _raw_roots(raw)
    data_csv = _find_data_csv(roots)
    speech_wavs = _find_speech_wavs(roots)
    acoustic_wavs = _find_acoustic_wavs(roots)
    if data_csv and speech_wavs and acoustic_wavs:
        return roots

    missing = [name for name in REQUIRED_OFFICIAL_FILES if _find_named_file(raw, name) is None]
    if missing:
        raise SystemExit(_official_missing_message(raw))

    cache = raw / "_ace_extract_cache"
    cache.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED_OFFICIAL_FILES:
        archive = _find_named_file(raw, name)
        assert archive is not None
        marker = cache / f".extracted_{name}.ok"
        if not marker.exists():
            print(f"extracting {archive.name} to {cache}")
            _safe_extract_tar(archive, cache)
            marker.write_text("ok\n", encoding="utf-8")

    roots = [cache] + _raw_roots(raw)
    data_csv = _find_data_csv(roots)
    speech_wavs = _find_speech_wavs(roots)
    acoustic_wavs = _find_acoustic_wavs(roots)
    if not data_csv or not speech_wavs or not acoustic_wavs:
        raise SystemExit(
            "ACE archives were present but expected Data CSV, Speech WAVs, and RIR/noise WAVs were not discoverable after extraction."
        )
    return roots


def _find_data_csv(roots: list[Path]) -> Path | None:
    for root in roots:
        matches = list(root.rglob("20150225T195903_test_t60_DRR_measurement_results.csv"))
        if matches:
            return matches[0]
    return None


def _find_speech_wavs(roots: list[Path]) -> list[Path]:
    wavs: list[Path] = []
    for root in roots:
        for path in root.rglob("*.wav"):
            low = path.as_posix().lower()
            name = path.name.lower()
            if "speech" in low and "noise" not in name and "rir" not in name:
                wavs.append(path)
    return sorted(set(wavs), key=lambda p: p.as_posix().lower())


def _find_acoustic_wavs(roots: list[Path]) -> list[Path]:
    wavs: list[Path] = []
    for root in roots:
        for path in root.rglob("*.wav"):
            name = path.name.lower()
            if "rir" in name or "noise" in name:
                wavs.append(path)
    return sorted(set(wavs), key=lambda p: p.as_posix().lower())


def _volume_bucket(volume_m3: float) -> str:
    if volume_m3 < 60:
        return "small"
    if volume_m3 < 130:
        return "medium"
    if volume_m3 < 260:
        return "large"
    return "very_large"


def _rt60_bucket(rt60: float) -> str:
    if rt60 <= 0.36:
        return "dry"
    if rt60 <= 0.55:
        return "moderate"
    if rt60 <= 0.85:
        return "reverberant"
    return "very_reverberant"


def _distance_bucket(distance_label: str, volume_m3: float, drr: float) -> str:
    if distance_label == "Short":
        return "near"
    if distance_label == "Long":
        if volume_m3 >= 180.0 or drr < 1.0:
            return "far"
        return "mid"
    return "unknown_or_uncertain"


def _noise_condition(snr_db: int, noise_type: str) -> str:
    if snr_db <= 0:
        return "heavy_noise"
    if snr_db <= 12 or noise_type in {"Babble", "Fan"}:
        return "moderate_noise"
    return "light_noise"


def _echo_zone(rt60: float, drr: float, distance_bucket: str, snr_db: int, noise_type: str) -> str:
    if snr_db <= 0 and (noise_type in {"Babble", "Fan"} or drr < 4.0):
        return "noisy_uncertain"
    if drr >= 6.0 and rt60 <= 0.70 and distance_bucket != "far":
        return "direct_dominant"
    if rt60 >= 0.90 or drr < 1.0 or (distance_bucket == "far" and rt60 >= 0.55):
        return "reverberant_dominant"
    return "balanced"


def _label_confidence(rt60: float, drr: float, volume_m3: float, distance_bucket: str, echo_zone: str, snr_db: int, noise_type: str) -> float:
    conf = 0.93
    for threshold in (60.0, 130.0, 260.0):
        if abs(volume_m3 - threshold) < 12.0:
            conf -= 0.04
    for threshold in (0.36, 0.55, 0.85):
        if abs(rt60 - threshold) < 0.04:
            conf -= 0.06
    for threshold in (1.0, 4.0, 6.0):
        if abs(drr - threshold) < 0.8:
            conf -= 0.05
    if snr_db <= 0:
        conf -= 0.14
    elif snr_db <= 12:
        conf -= 0.05
    if noise_type == "Babble":
        conf -= 0.04
    if echo_zone in {"balanced", "noisy_uncertain"}:
        conf -= 0.03
    if distance_bucket == "unknown_or_uncertain":
        conf -= 0.10
    return float(np.clip(round(conf, 3), 0.55, 0.97))


def _read_audio(path: Path, target_sr: int = TARGET_SR) -> np.ndarray:
    data, sr = sf.read(path, always_2d=False)
    if data.ndim == 2:
        data = data[:, 0]
    data = np.asarray(data, dtype=np.float32)
    if sr != target_sr:
        gcd = math.gcd(int(sr), int(target_sr))
        data = resample_poly(data, target_sr // gcd, sr // gcd).astype(np.float32)
    data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    if data.size == 0:
        raise ValueError(f"empty audio file: {path}")
    return data


def _rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x.astype(np.float64))) + 1e-12))


def _noise_excerpt(noise: np.ndarray, n: int, key: str) -> np.ndarray:
    if len(noise) < n:
        reps = int(math.ceil(n / max(1, len(noise))))
        noise = np.tile(noise, reps)
    if len(noise) == n:
        return noise.astype(np.float32)
    seed = int(_hash_text("noise-offset", key)[:8], 16)
    start = seed % (len(noise) - n)
    return noise[start : start + n].astype(np.float32)


def _unit_interval(*parts: object) -> float:
    return int(_hash_text(*parts)[:12], 16) / float(16**12 - 1)


def _harden_public_audio(mix: np.ndarray, sample_key: str) -> np.ndarray:
    """Apply mild deterministic speech-preserving changes that reduce source matching."""
    if mix.size == 0:
        return mix.astype(np.float32)

    orig_len = len(mix)
    ratio_options = [(159, 160), (160, 160), (161, 160)]
    ratio = ratio_options[int(_unit_interval("speed", sample_key) * len(ratio_options)) % len(ratio_options)]
    if ratio != (160, 160):
        mix = resample_poly(mix, ratio[0], ratio[1]).astype(np.float32)
        if len(mix) > orig_len:
            start_max = len(mix) - orig_len
            start = int(_unit_interval("crop", sample_key) * start_max) if start_max > 0 else 0
            mix = mix[start : start + orig_len]
        elif len(mix) < orig_len:
            mix = np.pad(mix, (0, orig_len - len(mix)))

    smooth_width = 9 + 2 * int(_unit_interval("smooth-width", sample_key) * 3)
    kernel = np.ones(smooth_width, dtype=np.float32) / float(smooth_width)
    low = np.convolve(mix, kernel, mode="same").astype(np.float32)
    tilt = -0.045 + 0.09 * _unit_interval("tilt", sample_key)
    mix = mix + tilt * (mix - low)

    seed = int(_hash_text("dither", sample_key)[:16], 16) % (2**32)
    rng = np.random.default_rng(seed)
    dither = rng.normal(0.0, 10 ** (-58 / 20), size=len(mix)).astype(np.float32)
    mix = mix.astype(np.float32) + dither
    peak = float(np.max(np.abs(mix)))
    if peak > 0:
        mix = 0.92 * mix / peak
    return mix.astype(np.float32)


def _render_audio(candidate: Candidate, out_path: Path, sample_key: str) -> float:
    speech = _read_audio(candidate.speech_path)
    rir = _read_audio(candidate.condition.rir_path)
    noise = _read_audio(candidate.condition.noise_paths[candidate.noise_type])

    speech = speech / max(np.max(np.abs(speech)), 1e-6)
    speech = np.pad(speech, (0, int(0.45 * TARGET_SR)))
    rir = rir / max(np.max(np.abs(rir)), 1e-6)
    rev = fftconvolve(speech, rir, mode="full").astype(np.float32)
    max_len = int(MAX_CLIP_SECONDS * TARGET_SR)
    if len(rev) > max_len:
        rev = rev[:max_len]

    noise_seg = _noise_excerpt(noise, len(rev), sample_key)
    signal_rms = _rms(rev)
    noise_rms = _rms(noise_seg)
    target_noise_rms = signal_rms / (10.0 ** (candidate.snr_db / 20.0))
    mix = rev + noise_seg * (target_noise_rms / noise_rms)
    mix = _harden_public_audio(mix, sample_key)

    peak = float(np.max(np.abs(mix)))
    if peak > 0:
        mix = 0.92 * mix / peak
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out_path, mix.astype(np.float32), TARGET_SR, subtype="PCM_16")
    return round(len(mix) / TARGET_SR, 4)


def _score_path(path: Path, required: list[str], preferred: list[str]) -> tuple[int, int]:
    low = path.as_posix().lower()
    stem = path.stem.lower()
    parts = [p.lower() for p in path.parts]
    score = 0
    for token in required:
        token_low = token.lower()
        if token_low.startswith("cfg="):
            cfg = token_low.split("=", 1)[1]
            config_hit = (
                cfg in parts
                or f"_{cfg}_" in stem
                or stem.endswith(f"_{cfg}")
                or f"-{cfg}-" in stem
            )
            if not config_hit:
                return (-10_000, -len(low))
            score += 5
            continue
        if token_low not in low:
            return (-10_000, -len(low))
        score += 5
    for token in preferred:
        if token.lower() in low:
            score += 2
    return (score, -len(low))


def _find_best_wav(wavs: list[Path], required: list[str], preferred: list[str]) -> Path:
    scored = sorted((_score_path(path, required, preferred), path) for path in wavs)
    if not scored or scored[-1][0][0] < 0:
        raise SystemExit(f"Could not locate ACE WAV with required tokens={required} preferred={preferred}")
    return scored[-1][1]


def _load_official_conditions(roots: list[Path]) -> list[AcousticCondition]:
    data_csv = _find_data_csv(roots)
    assert data_csv is not None
    df = pd.read_csv(data_csv, skipinitialspace=True)
    df.columns = _normalize_columns(list(df.columns))
    needed = {
        "session_id",
        "room",
        "config",
        "rec_type",
        "rir",
        "channel",
        "fb_t60_ahm",
        "fb_t60_ahm_mean_ch",
        "fb_drr",
        "fb_drr_mean_ch",
    }
    missing = needed - set(df.columns)
    if missing:
        raise SystemExit(f"ACE measurement CSV is missing required columns: {sorted(missing)}")

    df["session_id"] = pd.to_numeric(df["session_id"], errors="coerce")
    df["channel"] = pd.to_numeric(df["channel"], errors="coerce")
    df = df[(df["rec_type"].astype(str).str.strip().str.upper() == "IR") & (df["channel"] == 1)].copy()
    grouped = (
        df.groupby(["session_id", "room", "config", "rir", "channel"], as_index=False)
        .agg(
            rt60=("fb_t60_ahm_mean_ch", "first"),
            rt60_ch=("fb_t60_ahm", "first"),
            drr=("fb_drr_mean_ch", "first"),
            drr_ch=("fb_drr", "first"),
        )
        .copy()
    )

    wavs = _find_acoustic_wavs(roots)
    conditions: list[AcousticCondition] = []
    for _, row in grouped.iterrows():
        session_id = int(row["session_id"])
        if session_id not in ROOM_CONDITIONS:
            continue
        expected_config = "Lin8Ch" if session_id in DEV_SESSION_IDS else "Crucif"
        if str(row["config"]).strip() != expected_config:
            continue
        room_id = ROOM_CONDITIONS[session_id]["room_id"]
        room_info = ROOM_TABLE[room_id]
        room_config = ROOM_CONDITIONS[session_id]["room_config"]
        rt60 = float(row["rt60"] if pd.notna(row["rt60"]) else row["rt60_ch"])
        drr = float(row["drr"] if pd.notna(row["drr"]) else row["drr_ch"])
        rir = _find_best_wav(
            wavs,
            required=[room_id.lower(), f"cfg={room_config}", "rir"],
            preferred=["single", room_info["room_name"].lower(), expected_config.lower()],
        )
        noise_paths = {
            noise_type: _find_best_wav(
                wavs,
                required=[room_id.lower(), f"cfg={room_config}", "noise", noise_type.lower()],
                preferred=["single", room_info["room_name"].lower()],
            )
            for noise_type in NOISE_TYPES
        }
        conditions.append(
            AcousticCondition(
                session_id=session_id,
                room_id=room_id,
                room_name=room_info["room_name"],
                room_config=room_config,
                distance_label=ROOM_CONDITIONS[session_id]["distance_label"],
                gt_config=expected_config,
                rir_label=str(row["rir"]),
                rir_path=rir,
                noise_paths=noise_paths,
                rt60=rt60,
                drr=drr,
                volume_m3=float(room_info["volume_m3"]),
            )
        )

    if len(conditions) < 10:
        raise SystemExit(f"Expected ACE single-channel conditions for most room/source positions; found {len(conditions)}")
    return sorted(conditions, key=lambda c: c.session_id)


def _split_speech(speech_wavs: list[Path]) -> tuple[set[str], set[str]]:
    speech_ids = sorted({p.stem for p in speech_wavs})
    if len(speech_ids) < 6:
        raise SystemExit(f"Expected at least 6 ACE speech utterances; found {len(speech_ids)}")
    ordered = sorted(speech_ids, key=lambda s: _hash_text(ID_SALT, "speech-split", s))
    n_test = max(2, int(round(0.28 * len(ordered))))
    test = set(ordered[:n_test])
    train = set(ordered[n_test:])
    return train, test


def _balanced_sample(candidates: list[Candidate], n_target: int, split: str) -> list[Candidate]:
    by_condition: dict[int, list[Candidate]] = {}
    for cand in candidates:
        by_condition.setdefault(cand.condition.session_id, []).append(cand)
    selected: list[Candidate] = []
    per_group = max(1, int(math.ceil(n_target / max(1, len(by_condition)))))
    for session_id in sorted(by_condition):
        group = sorted(
            by_condition[session_id],
            key=lambda c: _hash_text(ID_SALT, "candidate", split, c.condition.session_id, c.speech_id, c.noise_type, c.snr_db),
        )
        selected.extend(group[:per_group])
    selected = sorted(
        selected,
        key=lambda c: _hash_text(ID_SALT, "trim", split, c.condition.session_id, c.speech_id, c.noise_type, c.snr_db),
    )[:n_target]
    return selected


def _official_candidates(raw: Path, max_examples: int) -> list[Candidate]:
    roots = _ensure_official_sources(raw)
    conditions = _load_official_conditions(roots)
    speech_wavs = _find_speech_wavs(roots)
    speech_by_id = {p.stem: p for p in speech_wavs}
    train_speech, test_speech = _split_speech(speech_wavs)
    all_candidates: list[Candidate] = []
    for condition in conditions:
        split = "test" if condition.session_id in TEST_SESSION_IDS else "train"
        speech_ids = test_speech if split == "test" else train_speech
        for speech_id in sorted(speech_ids):
            for noise_type in NOISE_TYPES:
                for snr_db in SNR_LEVELS:
                    all_candidates.append(
                        Candidate(
                            split=split,
                            speech_id=speech_id,
                            speech_path=speech_by_id[speech_id],
                            condition=condition,
                            noise_type=noise_type,
                            snr_db=snr_db,
                        )
                    )
    n_test = max(112, int(round(max_examples * 0.30)))
    n_train = max_examples - n_test
    train = _balanced_sample([c for c in all_candidates if c.split == "train"], n_train, "train")
    test = _balanced_sample([c for c in all_candidates if c.split == "test"], n_test, "test")
    return train + test


def _fixture_candidates(raw: Path) -> list[Candidate]:
    manifest = raw / "fixture_manifest.csv"
    if not manifest.exists():
        raise SystemExit("Fixture mode requires fixture_manifest.csv in the raw folder.")
    df = pd.read_csv(manifest)
    required = {
        "split",
        "speech_id",
        "speech_path",
        "rir_path",
        "noise_path",
        "noise_type",
        "snr_db",
        "session_id",
        "room_id",
        "room_name",
        "room_config",
        "distance_label",
        "volume_m3",
        "rt60",
        "drr",
    }
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Fixture manifest missing columns: {sorted(missing)}")
    candidates: list[Candidate] = []
    for _, row in df.iterrows():
        noise_type = str(row["noise_type"])
        condition = AcousticCondition(
            session_id=int(row["session_id"]),
            room_id=str(row["room_id"]),
            room_name=str(row["room_name"]),
            room_config=str(row["room_config"]),
            distance_label=str(row["distance_label"]),
            gt_config="fixture",
            rir_label=f"fixture_{row['session_id']}",
            rir_path=raw / str(row["rir_path"]),
            noise_paths={noise_type: raw / str(row["noise_path"])},
            rt60=float(row["rt60"]),
            drr=float(row["drr"]),
            volume_m3=float(row["volume_m3"]),
        )
        candidates.append(
            Candidate(
                split=str(row["split"]),
                speech_id=str(row["speech_id"]),
                speech_path=raw / str(row["speech_path"]),
                condition=condition,
                noise_type=noise_type,
                snr_db=int(row["snr_db"]),
            )
        )
    return candidates


def _row_from_candidate(candidate: Candidate, sample_id: str, audio_path: str) -> tuple[dict[str, object], dict[str, object]]:
    condition = candidate.condition
    volume_bucket = _volume_bucket(condition.volume_m3)
    rt60_bucket = _rt60_bucket(condition.rt60)
    distance_bucket = _distance_bucket(condition.distance_label, condition.volume_m3, condition.drr)
    echo_zone = _echo_zone(condition.rt60, condition.drr, distance_bucket, candidate.snr_db, candidate.noise_type)
    confidence = _label_confidence(
        condition.rt60,
        condition.drr,
        condition.volume_m3,
        distance_bucket,
        echo_zone,
        candidate.snr_db,
        candidate.noise_type,
    )
    public = {
        "sample_id": sample_id,
        "audio_path": audio_path,
        "prompt": PROMPT,
        "room_volume_bucket": volume_bucket,
        "rt60_bucket": rt60_bucket,
        "source_mic_distance_bucket": distance_bucket,
        "echo_zone": echo_zone,
        "confidence": confidence,
    }
    hidden = {
        **{k: public[k] for k in SUBMISSION_COLUMNS},
        "room_size_family": volume_bucket,
        "rt60_regime": rt60_bucket,
        "distance_bucket_hidden": distance_bucket,
        "noise_condition": _noise_condition(candidate.snr_db, candidate.noise_type),
        "speech_split": "heldout_speech" if candidate.split == "test" else "train_speech",
        "mic_source_config": f"{volume_bucket}_{condition.distance_label.lower()}",
    }
    return public, hidden


def _validate_outputs(train_df: pd.DataFrame, test_df: pd.DataFrame, answers_df: pd.DataFrame, public: Path, min_group_test: int) -> None:
    for name, df in [("train.csv", train_df), ("test.csv", test_df), ("answers.csv", answers_df)]:
        if df.isna().any().any():
            raise SystemExit(f"{name} contains NaN values")
    if set(test_df["sample_id"]) != set(answers_df["sample_id"]):
        raise SystemExit("test.csv ids do not match private answers.csv ids")
    if set(train_df["sample_id"]).intersection(set(test_df["sample_id"])):
        raise SystemExit("train/test sample_id overlap")
    for col in ["room_volume_bucket", "rt60_bucket", "source_mic_distance_bucket", "echo_zone"]:
        missing_train_labels = sorted(set(answers_df[col].astype(str)) - set(train_df[col].astype(str)))
        if missing_train_labels:
            raise SystemExit(f"test {col} labels lack train coverage: {missing_train_labels}")
    for path in pd.concat([train_df["audio_path"], test_df["audio_path"]]).tolist():
        full = public / str(path)
        if not full.exists():
            raise SystemExit(f"missing public audio file referenced by CSV: {path}")
        low = str(path).lower()
        leak_tokens = ["office", "meeting", "lecture", "lobby", "rir", "noise", "chromebook", "lin8ch", "crucif"]
        if any(tok in low for tok in leak_tokens):
            raise SystemExit(f"public audio path leaks source/acoustic token: {path}")
    axes = ["room_size_family", "rt60_regime", "distance_bucket_hidden", "noise_condition", "mic_source_config"]
    for axis in axes:
        counts = answers_df[axis].value_counts()
        sparse = counts[counts < min_group_test]
        if not sparse.empty:
            raise SystemExit(f"test hidden subgroup '{axis}' has sparse groups below {min_group_test}: {sparse.to_dict()}")


def _train_prior_column(test_ids: pd.Series, train_df: pd.DataFrame, col: str) -> list[str]:
    counts = train_df[col].astype(str).value_counts(normalize=True).sort_index()
    labels = counts.index.tolist()
    probs = counts.to_numpy(dtype=float)
    probs = probs / probs.sum()
    cdf = np.cumsum(probs)
    values: list[str] = []
    for sample_id in test_ids.astype(str):
        u = int(_hash_text(ID_SALT, "sample", col, sample_id)[:12], 16) / float(16**12 - 1)
        idx = int(np.searchsorted(cdf, u, side="right"))
        values.append(labels[min(idx, len(labels) - 1)])
    return values


def prepare(raw: Path, public: Path, private: Path, allow_fixture: bool = False, max_examples: int = DEFAULT_MAX_EXAMPLES) -> None:
    raw = raw.resolve()
    public = public.resolve()
    private = private.resolve()
    if public == raw or private == raw:
        raise SystemExit("public/private output directories must be separate from raw source directory")
    if public.exists():
        shutil.rmtree(public)
    if private.exists():
        shutil.rmtree(private)
    (public / "train" / "audio").mkdir(parents=True, exist_ok=True)
    (public / "test" / "audio").mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    fixture_mode = allow_fixture and (raw / "fixture_manifest.csv").exists()
    candidates = _fixture_candidates(raw) if fixture_mode else _official_candidates(raw, max_examples=max_examples)
    if not candidates:
        raise SystemExit("No candidates were generated from the raw source.")

    seen_ids: set[str] = set()
    train_rows: list[dict[str, object]] = []
    test_rows: list[dict[str, object]] = []
    answer_rows: list[dict[str, object]] = []
    materialized_keys: list[str] = []
    for cand in sorted(
        candidates,
        key=lambda c: _hash_text(ID_SALT, "materialize", c.split, c.condition.session_id, c.speech_id, c.noise_type, c.snr_db),
    ):
        sample_key = _hash_text(ID_SALT, cand.split, cand.condition.session_id, cand.condition.rir_label, cand.speech_id, cand.noise_type, cand.snr_db)
        sample_id = "brs_" + sample_key[:12]
        if sample_id in seen_ids:
            raise SystemExit(f"sample_id collision: {sample_id}")
        seen_ids.add(sample_id)
        audio_rel = f"{cand.split}/audio/{sample_id}.wav"
        _render_audio(cand, public / audio_rel, sample_key)
        public_row, answer_row = _row_from_candidate(cand, sample_id, audio_rel)
        materialized_keys.append(sample_key)
        if cand.split == "train":
            train_rows.append(public_row)
        elif cand.split == "test":
            test_rows.append({k: public_row[k] for k in TEST_COLUMNS})
            answer_rows.append(answer_row)
        else:
            raise SystemExit(f"invalid split in candidate: {cand.split}")

    if len(set(materialized_keys)) != len(materialized_keys):
        raise SystemExit("raw hash/key uniqueness check failed")

    train_df = pd.DataFrame(train_rows, columns=TRAIN_COLUMNS).sort_values("sample_id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows, columns=TEST_COLUMNS).sort_values("sample_id").reset_index(drop=True)
    answers_df = pd.DataFrame(answer_rows, columns=ANSWER_COLUMNS).sort_values("sample_id").reset_index(drop=True)

    min_group_test = 1 if fixture_mode else MIN_GROUP_TEST
    _validate_outputs(train_df, test_df, answers_df, public, min_group_test=min_group_test)

    train_df.to_csv(public / "train.csv", index=False)
    test_df.to_csv(public / "test.csv", index=False)

    sample = pd.DataFrame({"sample_id": test_df["sample_id"]})
    for col in ["room_volume_bucket", "rt60_bucket", "source_mic_distance_bucket", "echo_zone"]:
        sample[col] = _train_prior_column(test_df["sample_id"], train_df, col)
    sample["confidence"] = float(round(float(train_df["confidence"].median()), 3))
    sample = sample[SUBMISSION_COLUMNS]
    sample.to_csv(public / "sample_submission.csv", index=False)

    answers_df.to_csv(private / "answers.csv", index=False)
    print(
        f"prepared {'fixture' if fixture_mode else 'official ACE'} split: "
        f"{len(train_df)} train rows, {len(test_df)} test rows, "
        f"{len(train_df) + len(test_df)} WAV clips"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    parser.add_argument("--allow-fixture", action="store_true", help="only for _sanity_smoke.py tiny fixtures")
    parser.add_argument("--max-examples", type=int, default=DEFAULT_MAX_EXAMPLES)
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private, allow_fixture=args.allow_fixture, max_examples=args.max_examples)


if __name__ == "__main__":
    main()
