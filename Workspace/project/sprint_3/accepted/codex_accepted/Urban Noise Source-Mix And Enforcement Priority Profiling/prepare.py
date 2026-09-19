from __future__ import annotations

import hashlib
import io
import json
import math
import shutil
import tarfile
import tempfile
import wave
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


SELECTED_AUDIO_ARCHIVE = "audio-0.tar.gz"
OFFICIAL_SOURCE_ZIP = "sonyc_ust_official_selected_source_files.zip"
EXPECTED_ARCHIVE_MD5 = "bbb4dbae7d2e58e18d24878b9ee1eb51"
EXPECTED_ARCHIVE_WAVS = 1000
REQUIRED_OFFICIAL_FILES = {"annotations.csv", "dcase-ust-taxonomy.yaml", "README.md", SELECTED_AUDIO_ARCHIVE}

ID_SALT = "urban-noise-source-mix-priority-v1-20260706"
SPLIT_SALT = "urban-noise-source-mix-priority-split-v1"
TARGET_TEST_FRAC = 0.30
MIN_GROUP_TEST = 8
MIN_GROUP_TRAIN = 12
OUTPUT_SR = 16000
OUTPUT_SECONDS = 9.0

SOURCE_FAMILIES = [
    "engine",
    "machinery_impact",
    "powered_saw",
    "alert_signal",
    "music",
    "human_voice",
    "dog",
    "other_impact",
]

FAMILY_TO_COARSE = {
    "engine": "1_engine_presence",
    "machinery_impact": "2_machinery-impact_presence",
    "other_impact": "3_non-machinery-impact_presence",
    "powered_saw": "4_powered-saw_presence",
    "alert_signal": "5_alert-signal_presence",
    "music": "6_music_presence",
    "human_voice": "7_human-voice_presence",
    "dog": "8_dog_presence",
}

FAMILY_TO_FINE_PREFIX = {
    "engine": "1-",
    "machinery_impact": "2-",
    "other_impact": "3-",
    "powered_saw": "4-",
    "alert_signal": "5-",
    "music": "6-",
    "human_voice": "7-",
    "dog": "8-",
}

FINE_SEVERITY_WEIGHTS = {
    "2-1_rock-drill_presence": 0.85,
    "2-2_jackhammer_presence": 1.00,
    "2-3_hoe-ram_presence": 1.00,
    "2-4_pile-driver_presence": 1.00,
    "2-X_other-unknown-impact-machinery_presence": 0.75,
    "4-1_chainsaw_presence": 0.75,
    "4-2_small-medium-rotating-saw_presence": 0.85,
    "4-3_large-rotating-saw_presence": 1.00,
    "4-X_other-unknown-powered-saw_presence": 0.80,
    "5-2_car-alarm_presence": 0.85,
    "5-3_siren_presence": 1.00,
    "5-4_reverse-beeper_presence": 0.75,
    "6-1_stationary-music_presence": 0.55,
    "6-2_mobile-music_presence": 0.55,
    "6-3_ice-cream-truck_presence": 0.45,
    "7-2_person-or-small-group-shouting_presence": 0.65,
    "7-3_large-crowd_presence": 0.55,
    "7-4_amplified-speech_presence": 0.70,
}

DOMINANT_ALLOWED = [
    "engine",
    "machinery_impact",
    "powered_saw",
    "alert_signal",
    "music",
    "human_voice",
    "dog",
    "other_impact",
    "mixed_uncertain",
]

PRIORITY_ALLOWED = ["low", "moderate", "high", "urgent"]
NUISANCE_ALLOWED = [
    "traffic_dominant",
    "construction_dominant",
    "alert_dominant",
    "social_music_voice",
    "animal_or_other",
    "mixed_uncertain",
]

HIDDEN_GROUP_AXES = [
    "priority_group_hidden",
    "nuisance_group_hidden",
    "source_family_hidden",
    "pressure_band_hidden",
    "mix_complexity_hidden",
]

PUBLIC_INPUT_COLUMNS = ["id", "audio_path", "clip_duration_s", "monitoring_context"]
TARGET_COLUMNS = [
    "source_mix_json",
    "dominant_source",
    "enforcement_priority",
    "nuisance_pattern",
    "confidence",
]


def _sha(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def _find_unique(root: Path, name: str) -> Path | None:
    candidates = []
    for base in [root, root / "raw_upload"]:
        p = base / name
        if p.exists():
            candidates.append(p)
    candidates.extend([p for p in root.rglob(name) if p.is_file()])
    unique = []
    seen = set()
    for p in candidates:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(p)
    if len(unique) > 1:
        raise SystemExit(f"Found multiple {name} files; keep only the official selected source file.")
    return unique[0] if unique else None


def _find_audio_dir(root: Path) -> Path | None:
    for base in [root / "audio-0", root / "raw_upload" / "audio-0", root / "audio"]:
        if base.exists() and any(base.glob("*.wav")):
            return base
    matches = [p for p in root.rglob("audio-0") if p.is_dir() and any(p.glob("*.wav"))]
    if len(matches) > 1:
        raise SystemExit("Found multiple extracted audio-0 directories; keep one official extracted shard.")
    return matches[0] if matches else None


def _extract_official_source_zip(zip_path: Path, dest: Path) -> Path:
    with zipfile.ZipFile(zip_path, "r") as zf:
        entries = []
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            if "/" in name or name.startswith(".") or name not in REQUIRED_OFFICIAL_FILES:
                raise SystemExit(f"{zip_path.name} contains unexpected member {info.filename!r}.")
            entries.append(name)
        if set(entries) != REQUIRED_OFFICIAL_FILES:
            missing = sorted(REQUIRED_OFFICIAL_FILES - set(entries))
            extra = sorted(set(entries) - REQUIRED_OFFICIAL_FILES)
            raise SystemExit(f"{zip_path.name} must contain exactly the official selected files; missing={missing}, extra={extra}.")
        for name in sorted(REQUIRED_OFFICIAL_FILES):
            target = dest / name
            with zf.open(name) as src, target.open("wb") as out:
                shutil.copyfileobj(src, out)
    return dest


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _list_archive_wavs(archive_path: Path) -> list[str]:
    actual_md5 = _md5(archive_path)
    if actual_md5.lower() != EXPECTED_ARCHIVE_MD5:
        raise SystemExit(
            f"{archive_path.name} md5 mismatch: got {actual_md5}, expected {EXPECTED_ARCHIVE_MD5}. "
            "Download the official Zenodo file unchanged."
        )
    with tarfile.open(archive_path, "r:gz") as tf:
        names = [Path(m.name).name for m in tf.getmembers() if m.isfile() and m.name.lower().endswith(".wav")]
    if len(names) != EXPECTED_ARCHIVE_WAVS:
        raise SystemExit(f"{archive_path.name} should contain {EXPECTED_ARCHIVE_WAVS} WAV files, found {len(names)}.")
    if len(set(names)) != len(names):
        raise SystemExit("Duplicate WAV basenames found inside official archive.")
    return sorted(names)


def _list_extracted_wavs(audio_dir: Path) -> list[str]:
    names = sorted(p.name for p in audio_dir.glob("*.wav"))
    if len(names) != EXPECTED_ARCHIVE_WAVS:
        raise SystemExit(f"{audio_dir} should contain {EXPECTED_ARCHIVE_WAVS} official WAV files, found {len(names)}.")
    if len(set(names)) != len(names):
        raise SystemExit("Duplicate WAV basenames found in extracted audio directory.")
    return names


def _validate_annotations(df: pd.DataFrame) -> None:
    required = [
        "split",
        "sensor_id",
        "audio_filename",
        "annotator_id",
        "borough",
        "block",
        "latitude",
        "longitude",
        "year",
        "week",
        "day",
        "hour",
        *FAMILY_TO_COARSE.values(),
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"annotations.csv is missing required columns: {missing}")
    for col in required:
        if df[col].isna().any():
            raise SystemExit(f"annotations.csv has missing values in required column {col}")
    if (df["audio_filename"].astype(str).str.strip() == "").any():
        raise SystemExit("annotations.csv contains blank audio_filename values")


def _presence_mean(rows: pd.DataFrame, col: str) -> float | None:
    if rows.empty:
        return None
    vals = pd.to_numeric(rows[col], errors="coerce")
    vals = vals[vals.isin([0, 1])]
    if vals.empty:
        return None
    return float(vals.mean())


def _family_fine_cols(columns: list[str], family: str) -> list[str]:
    prefix = FAMILY_TO_FINE_PREFIX[family]
    return [c for c in columns if c.startswith(prefix) and c.endswith("_presence")]


def _family_proximity(rows: pd.DataFrame, fine_cols: list[str]) -> float:
    if rows.empty:
        return 0.65
    prox_values = []
    for fine_col in fine_cols:
        prox_col = fine_col.replace("_presence", "_proximity")
        if prox_col not in rows.columns:
            continue
        present = pd.to_numeric(rows[fine_col], errors="coerce").fillna(-1)
        for val in rows.loc[present == 1, prox_col].astype(str):
            if val == "near":
                prox_values.append(1.0)
            elif val == "notsure":
                prox_values.append(0.65)
            elif val == "far":
                prox_values.append(0.35)
    if not prox_values:
        return 0.65
    return float(np.mean(prox_values))


def _fine_score(rows: pd.DataFrame, col: str) -> float:
    verified = rows[rows["annotator_id"] == 0]
    volunteers = rows[rows["annotator_id"] > 0]
    team = rows[rows["annotator_id"] < 0]
    v = _presence_mean(verified, col)
    vol = _presence_mean(volunteers, col)
    tm = _presence_mean(team, col)
    if v is not None:
        return float(0.72 * v + 0.28 * (vol if vol is not None else v))
    if tm is not None and vol is not None:
        return float(0.55 * tm + 0.45 * vol)
    if tm is not None:
        return float(tm)
    if vol is not None:
        return float(vol)
    return 0.0


def _derive_record(filename: str, rows: pd.DataFrame, all_columns: list[str]) -> dict[str, object]:
    rows = rows.copy()
    first = rows.iloc[0]
    verified = rows[rows["annotator_id"] == 0]
    volunteers = rows[rows["annotator_id"] > 0]
    team = rows[rows["annotator_id"] < 0]

    source_weights: dict[str, float] = {}
    family_base: dict[str, float] = {}
    family_prox: dict[str, float] = {}
    for family, coarse_col in FAMILY_TO_COARSE.items():
        v = _presence_mean(verified, coarse_col)
        vol = _presence_mean(volunteers, coarse_col)
        tm = _presence_mean(team, coarse_col)
        if v is not None:
            base = 0.70 * v + 0.30 * (vol if vol is not None else v)
        elif tm is not None and vol is not None:
            base = 0.55 * tm + 0.45 * vol
        elif tm is not None:
            base = tm
        elif vol is not None:
            base = vol
        else:
            base = 0.0
        prox = _family_proximity(volunteers, _family_fine_cols(all_columns, family))
        weight = float(np.clip(base * (0.78 + 0.22 * prox), 0.0, 1.0))
        source_weights[family] = weight
        family_base[family] = float(base)
        family_prox[family] = float(prox)

    ordered = sorted(source_weights.items(), key=lambda kv: (-kv[1], kv[0]))
    top_family, top_weight = ordered[0]
    second_weight = ordered[1][1]
    if top_weight < 0.28 or (top_weight < 0.55 and (top_weight - second_weight) < 0.10):
        dominant = "mixed_uncertain"
    else:
        dominant = top_family

    construction = max(source_weights["machinery_impact"], source_weights["powered_saw"])
    social = max(source_weights["music"], source_weights["human_voice"])
    animal_other = max(source_weights["dog"], source_weights["other_impact"])
    alert = source_weights["alert_signal"]
    engine = source_weights["engine"]
    if construction >= 0.34 or source_weights["machinery_impact"] + source_weights["powered_saw"] >= 0.52:
        nuisance = "construction_dominant"
    elif alert >= 0.36:
        nuisance = "alert_dominant"
    elif engine >= 0.42 and engine >= social and engine >= construction:
        nuisance = "traffic_dominant"
    elif social >= 0.35 or source_weights["music"] + source_weights["human_voice"] >= 0.50:
        nuisance = "social_music_voice"
    elif animal_other >= 0.35:
        nuisance = "animal_or_other"
    else:
        nuisance = "mixed_uncertain"

    severity = 0.0
    for col, sev in FINE_SEVERITY_WEIGHTS.items():
        if col in all_columns:
            severity += sev * _fine_score(rows, col)
    severity = min(1.0, severity / 2.5)
    risk = (
        0.18 * source_weights["engine"]
        + 0.52 * source_weights["machinery_impact"]
        + 0.62 * source_weights["powered_saw"]
        + 0.50 * source_weights["alert_signal"]
        + 0.28 * source_weights["music"]
        + 0.22 * source_weights["human_voice"]
        + 0.13 * source_weights["dog"]
        + 0.20 * source_weights["other_impact"]
        + 0.22 * severity
    )
    if max(family_prox["machinery_impact"], family_prox["powered_saw"], family_prox["alert_signal"]) >= 0.80:
        risk += 0.04
    if risk >= 0.68 or (construction >= 0.58 and severity >= 0.35) or (alert >= 0.62 and severity >= 0.35):
        priority = "urgent"
    elif risk >= 0.42 or construction >= 0.38 or source_weights["powered_saw"] >= 0.34 or alert >= 0.45:
        priority = "high"
    elif risk >= 0.18 or max(source_weights.values()) >= 0.30:
        priority = "moderate"
    else:
        priority = "low"

    vol_scores = []
    for coarse_col in FAMILY_TO_COARSE.values():
        val = _presence_mean(volunteers, coarse_col)
        if val is not None:
            vol_scores.append(val)
    if vol_scores:
        agreement = 1.0 - float(np.mean([4.0 * p * (1.0 - p) for p in vol_scores]))
    else:
        agreement = 0.55
    n_vol = int(volunteers["annotator_id"].nunique())
    has_verified = 1.0 if not verified.empty else 0.0
    n_active = sum(1 for v in source_weights.values() if v >= 0.30)
    confidence = (
        0.34
        + 0.25 * has_verified
        + 0.16 * min(n_vol, 3) / 3.0
        + 0.20 * agreement
        + 0.05 * min(max(source_weights.values()), 1.0)
        - 0.03 * max(0, n_active - 1)
    )
    confidence = float(np.clip(confidence, 0.25, 0.98))

    row_id = "un_" + _sha(f"{ID_SALT}|{filename}", 14)
    group_key = (
        f"s{int(first['sensor_id'])}|b{int(first['block'])}|"
        f"{int(first['year'])}|{int(first['week'])}|{int(first['day'])}|{int(first['hour'])}"
    )
    max_pressure = max(source_weights.values())
    if max_pressure >= 0.62:
        pressure_band = "strong_source"
    elif max_pressure >= 0.38:
        pressure_band = "medium_source"
    else:
        pressure_band = "weak_or_diffuse"
    if n_active >= 3:
        complexity = "three_plus_sources"
    elif n_active == 2:
        complexity = "two_sources"
    else:
        complexity = "zero_or_one_source"
    if dominant in {"machinery_impact", "powered_saw"}:
        source_family_hidden = "construction"
    elif dominant == "engine":
        source_family_hidden = "traffic"
    elif dominant == "alert_signal":
        source_family_hidden = "alert"
    elif dominant in {"music", "human_voice"}:
        source_family_hidden = "social"
    elif dominant in {"dog", "other_impact"}:
        source_family_hidden = "animal_or_other"
    else:
        source_family_hidden = "mixed_uncertain"

    mix_json = json.dumps(
        {k: round(float(source_weights[k]), 4) for k in SOURCE_FAMILIES},
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return {
        "source_filename": filename,
        "source_key": _sha(f"{ID_SALT}|source|{filename}", 20),
        "id": row_id,
        "group_key": group_key,
        "source_mix_json": mix_json,
        "dominant_source": dominant,
        "enforcement_priority": priority,
        "nuisance_pattern": nuisance,
        "confidence": round(confidence, 4),
        "priority_group_hidden": priority,
        "nuisance_group_hidden": nuisance,
        "source_family_hidden": source_family_hidden,
        "pressure_band_hidden": pressure_band,
        "mix_complexity_hidden": complexity,
    }


def _assign_split(records: pd.DataFrame) -> pd.DataFrame:
    groups = []
    for gkey, group in records.groupby("group_key"):
        h = int(_sha(f"{SPLIT_SALT}|{gkey}", 16), 16)
        groups.append((h, gkey, group.index.tolist()))
    groups.sort()
    test_groups: set[str] = set()
    for h, gkey, _ in groups:
        if (h % 10000) / 10000.0 < TARGET_TEST_FRAC:
            test_groups.add(gkey)

    def split_df() -> tuple[pd.DataFrame, pd.DataFrame]:
        mask = records["group_key"].isin(test_groups)
        return records.loc[~mask], records.loc[mask]

    def add_groups_for_axis(axis: str) -> None:
        train, test = split_df()
        total_counts = records[axis].value_counts()
        for label, total in total_counts.items():
            if total < MIN_GROUP_TEST + MIN_GROUP_TRAIN:
                continue
            while int(test[axis].value_counts().get(label, 0)) < MIN_GROUP_TEST:
                candidates = []
                train, test = split_df()
                for _, gkey, idxs in groups:
                    if gkey in test_groups:
                        continue
                    g = records.loc[idxs]
                    gain = int((g[axis] == label).sum())
                    if gain:
                        candidates.append((-gain, len(idxs), _sha(f"{SPLIT_SALT}|repair|{axis}|{label}|{gkey}"), gkey))
                if not candidates:
                    break
                candidates.sort()
                test_groups.add(candidates[0][3])

    for axis in HIDDEN_GROUP_AXES:
        add_groups_for_axis(axis)

    out = records.copy()
    out["split_out"] = np.where(out["group_key"].isin(test_groups), "test", "train")
    train = out[out["split_out"] == "train"]
    test = out[out["split_out"] == "test"]
    if train.empty or test.empty:
        raise SystemExit("Split assignment produced an empty train or test set.")
    if set(train["group_key"]) & set(test["group_key"]):
        raise SystemExit("Group leakage: a sensor/time/block group crosses train and test.")
    for axis in HIDDEN_GROUP_AXES:
        train_counts = train[axis].value_counts()
        test_counts = test[axis].value_counts()
        for label, total in out[axis].value_counts().items():
            if total >= MIN_GROUP_TEST + MIN_GROUP_TRAIN:
                if int(test_counts.get(label, 0)) < MIN_GROUP_TEST:
                    raise SystemExit(f"Test group {axis}={label} has fewer than {MIN_GROUP_TEST} rows.")
                if int(train_counts.get(label, 0)) < MIN_GROUP_TRAIN:
                    raise SystemExit(f"Train group {axis}={label} has fewer than {MIN_GROUP_TRAIN} rows.")
    return out


def _read_wav_bytes_from_archive(tf: tarfile.TarFile, member_by_name: dict[str, tarfile.TarInfo], filename: str) -> bytes:
    member = member_by_name.get(filename)
    if member is None:
        raise SystemExit(f"Missing {filename} from official audio archive.")
    f = tf.extractfile(member)
    if f is None:
        raise SystemExit(f"Could not extract {filename} from official audio archive.")
    return f.read()


def _read_wav_bytes_from_dir(audio_dir: Path, filename: str) -> bytes:
    p = audio_dir / filename
    if not p.exists():
        raise SystemExit(f"Missing {filename} from extracted official audio directory.")
    return p.read_bytes()


def _transform_audio(wav_bytes: bytes, row_id: str) -> np.ndarray:
    with wave.open(io.BytesIO(wav_bytes), "rb") as w:
        channels = w.getnchannels()
        sr = w.getframerate()
        sampwidth = w.getsampwidth()
        frames = w.getnframes()
        raw = w.readframes(frames)
    if channels != 1 or sampwidth != 2:
        raise SystemExit(f"Expected mono 16-bit PCM WAV, got channels={channels}, sampwidth={sampwidth}")
    audio = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if len(audio) < sr * OUTPUT_SECONDS:
        raise SystemExit("Source WAV is shorter than expected.")
    seed = int(_sha(f"audio-transform|{row_id}", 16), 16) & 0xFFFFFFFF
    rng = np.random.default_rng(seed)
    max_start = max(0, len(audio) - int(sr * OUTPUT_SECONDS) - int(0.05 * sr))
    start = int(rng.integers(int(0.10 * sr), max(int(0.11 * sr), max_start + 1))) if max_start > int(0.10 * sr) else 0
    clip = audio[start : start + int(sr * OUTPUT_SECONDS)].copy()
    if sr == OUTPUT_SR:
        y = clip
    elif sr % OUTPUT_SR == 0:
        y = clip[:: sr // OUTPUT_SR]
    else:
        old_x = np.linspace(0.0, len(clip) / sr, num=len(clip), endpoint=False)
        new_len = int(round(len(clip) * OUTPUT_SR / sr))
        new_x = np.linspace(0.0, len(clip) / sr, num=new_len, endpoint=False)
        y = np.interp(new_x, old_x, clip).astype(np.float32)
    # Mild, deterministic channel coloration and dither reduce exact source fingerprinting while preserving events.
    y = y.astype(np.float32)
    y = y - 0.018 * np.concatenate([[0.0], y[:-1]])
    rms = float(np.sqrt(np.mean(y * y) + 1e-9))
    target_rms = float(rng.uniform(0.045, 0.075))
    gain = min(3.0, target_rms / max(rms, 1e-6))
    y = y * gain
    y += rng.normal(0.0, 0.00018, size=len(y)).astype(np.float32)
    fade_len = min(int(0.035 * OUTPUT_SR), len(y) // 4)
    if fade_len > 1:
        fade = np.linspace(0.0, 1.0, fade_len, dtype=np.float32)
        y[:fade_len] *= fade
        y[-fade_len:] *= fade[::-1]
    y = np.clip(y, -0.98, 0.98)
    return np.round(y * 32767.0).astype("<i2")


def _write_wav(path: Path, samples: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(OUTPUT_SR)
        w.writeframes(samples.tobytes())


def _materialize_audio(records: pd.DataFrame, public: Path, archive_path: Path | None, audio_dir: Path | None) -> None:
    if archive_path is None and audio_dir is None:
        raise SystemExit("No official audio archive or extracted audio-0 directory found.")
    if archive_path is not None:
        record_by_source = {str(row.source_filename): row for row in records.itertuples(index=False)}
        seen: set[str] = set()
        with tarfile.open(archive_path, "r|gz") as tf:
            for member in tf:
                if not member.isfile() or not member.name.lower().endswith(".wav"):
                    continue
                basename = Path(member.name).name
                row = record_by_source.get(basename)
                if row is None:
                    continue
                f = tf.extractfile(member)
                if f is None:
                    raise SystemExit(f"Could not extract {basename} from official audio archive.")
                samples = _transform_audio(f.read(), row.id)
                _write_wav(public / row.audio_path, samples)
                seen.add(basename)
        missing = sorted(set(record_by_source) - seen)
        if missing:
            raise SystemExit(f"Missing selected WAVs while streaming archive: {missing[:5]}")
    else:
        assert audio_dir is not None
        for row in records.itertuples(index=False):
            wav_bytes = _read_wav_bytes_from_dir(audio_dir, row.source_filename)
            samples = _transform_audio(wav_bytes, row.id)
            _write_wav(public / row.audio_path, samples)


def _sample_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    # A deliberately weak but valid dummy profile. Using train priors is too competitive
    # because the weighted mix head gives useful partial credit even without audio.
    mix_json = json.dumps({k: 0.5 for k in SOURCE_FAMILIES}, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return pd.DataFrame(
        {
            "id": test["id"],
            "source_mix_json": mix_json,
            "dominant_source": "alert_signal",
            "enforcement_priority": "high",
            "nuisance_pattern": "alert_dominant",
            "confidence": 0.5,
        }
    )


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    temp_source: tempfile.TemporaryDirectory[str] | None = None
    try:
        source_root = raw
        annotations_path = _find_unique(source_root, "annotations.csv")
        taxonomy_path = _find_unique(source_root, "dcase-ust-taxonomy.yaml")
        readme_path = _find_unique(source_root, "README.md")
        archive_path = _find_unique(source_root, SELECTED_AUDIO_ARCHIVE)
        audio_dir = None if archive_path else _find_audio_dir(source_root)
        missing = [
            name
            for name, path in [
                ("annotations.csv", annotations_path),
                ("dcase-ust-taxonomy.yaml", taxonomy_path),
                ("README.md", readme_path),
            ]
            if path is None
        ]
        if missing or (archive_path is None and audio_dir is None):
            zip_path = _find_unique(raw, OFFICIAL_SOURCE_ZIP)
            if zip_path is not None:
                temp_source = tempfile.TemporaryDirectory(prefix="sonyc_ust_source_")
                source_root = _extract_official_source_zip(zip_path, Path(temp_source.name))
                annotations_path = _find_unique(source_root, "annotations.csv")
                taxonomy_path = _find_unique(source_root, "dcase-ust-taxonomy.yaml")
                readme_path = _find_unique(source_root, "README.md")
                archive_path = _find_unique(source_root, SELECTED_AUDIO_ARCHIVE)
                audio_dir = None if archive_path else _find_audio_dir(source_root)

        missing = [
            name
            for name, path in [
                ("annotations.csv", annotations_path),
                ("dcase-ust-taxonomy.yaml", taxonomy_path),
                ("README.md", readme_path),
            ]
            if path is None
        ]
        if missing:
            raise SystemExit(f"Missing official source file(s): {missing}")
        if archive_path is None and audio_dir is None:
            raise SystemExit(f"Missing official {SELECTED_AUDIO_ARCHIVE} or extracted audio-0 directory.")

        assert annotations_path is not None
        df = pd.read_csv(annotations_path)
        _validate_annotations(df)
        selected_names = _list_archive_wavs(archive_path) if archive_path else _list_extracted_wavs(audio_dir)  # type: ignore[arg-type]
        selected_set = set(selected_names)
        ann = df[df["audio_filename"].astype(str).isin(selected_set)].copy()
        if ann["audio_filename"].nunique() != len(selected_set):
            missing_audio = sorted(selected_set - set(ann["audio_filename"].astype(str)))
            raise SystemExit(f"Some selected audio files are missing annotations: {missing_audio[:5]}")

        records = []
        for filename, rows in ann.groupby("audio_filename", sort=True):
            records.append(_derive_record(str(filename), rows, list(df.columns)))
        rec = pd.DataFrame(records)
        if rec["source_key"].duplicated().any() or rec["id"].duplicated().any():
            raise SystemExit("Source keys or public ids are not unique before splitting.")
        rec = _assign_split(rec)
        rec["clip_duration_s"] = OUTPUT_SECONDS
        rec["monitoring_context"] = "urban acoustic monitor clip"
        rec["audio_path"] = rec.apply(lambda r: f"{r['split_out']}/audio/{r['id']}.wav", axis=1)
        rec = rec.sort_values("id").reset_index(drop=True)

        if public.exists():
            shutil.rmtree(public)
        if private.exists():
            shutil.rmtree(private)
        public.mkdir(parents=True, exist_ok=True)
        private.mkdir(parents=True, exist_ok=True)

        _materialize_audio(rec, public, archive_path, audio_dir)

        train = rec[rec["split_out"] == "train"].copy().sort_values("id")
        test = rec[rec["split_out"] == "test"].copy().sort_values("id")
        train_out = train[PUBLIC_INPUT_COLUMNS + TARGET_COLUMNS]
        test_out = test[PUBLIC_INPUT_COLUMNS]
        answers = test[["id"] + TARGET_COLUMNS + HIDDEN_GROUP_AXES].copy()
        sample = _sample_submission(train, test)

        for name, frame in [("train", train_out), ("test", test_out), ("answers", answers), ("sample", sample)]:
            if frame.isna().any().any():
                raise SystemExit(f"{name} output contains NaN values.")
        train_out.to_csv(public / "train.csv", index=False)
        test_out.to_csv(public / "test.csv", index=False)
        sample.to_csv(public / "sample_submission.csv", index=False)
        answers.to_csv(private / "answers.csv", index=False)

        leak_terms = ["source_filename", "sensor_id", "audio_filename", "annotator_id", "split", "borough", "block", "latitude", "longitude", "year", "week", "day", "hour"]
        public_text = "\n".join((public / "train.csv").read_text(encoding="utf-8").splitlines()[:5])
        public_text += "\n" + "\n".join((public / "test.csv").read_text(encoding="utf-8").splitlines()[:5])
        lowered = public_text.lower()
        if any(term in lowered for term in leak_terms):
            raise SystemExit("Leak-prone source metadata term appeared in public CSV header/sample.")
    finally:
        if temp_source is not None:
            temp_source.cleanup()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("public", type=Path)
    parser.add_argument("private", type=Path)
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)
