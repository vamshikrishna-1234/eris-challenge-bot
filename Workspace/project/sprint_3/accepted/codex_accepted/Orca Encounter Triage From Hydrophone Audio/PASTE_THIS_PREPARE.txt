from __future__ import annotations

import argparse
import hashlib
import math
import shutil
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import resample_poly


TARGET_SR = 16000
CLIP_SECONDS = 8.0
DEFAULT_MAX_CLIPS_PER_FILE = 4
ID_SALT = "orca-encounter-triage-dclde-v1"
PROMPT = "Triage this short underwater hydrophone clip for encounter activity and confounders."
MIN_GROUP_TEST = 5
MIN_ROWS = 120

TRAIN_COLUMNS = [
    "id",
    "audio_path",
    "clip_duration_bucket",
    "prompt",
    "orca_presence",
    "encounter_activity",
    "ecotype_context",
    "confounder_type",
    "call_band_bucket",
    "confidence",
]
TEST_COLUMNS = ["id", "audio_path", "clip_duration_bucket", "prompt"]
SUBMISSION_COLUMNS = [
    "id",
    "orca_presence",
    "encounter_activity",
    "ecotype_context",
    "confounder_type",
    "call_band_bucket",
    "confidence",
]
ANSWER_COLUMNS = SUBMISSION_COLUMNS + [
    "provider_family",
    "ecotype_group",
    "activity_group",
    "confounder_group",
    "band_group",
    "quality_group",
    "split_group",
]


@dataclass(frozen=True)
class Candidate:
    soundfile: str
    audio_path: Path
    provider: str
    dataset: str
    split_group: str
    start_sec: float
    end_sec: float
    source_kind: str


def _hash_text(*parts: object) -> str:
    return hashlib.sha256(":".join(str(p) for p in parts).encode("utf-8")).hexdigest()


def _raw_roots(raw: Path) -> list[Path]:
    roots = [raw, raw / "raw_upload", raw / "raw_data"]
    return [r for r in roots if r.exists()]


def _find_annotations(raw: Path) -> Path:
    for root in _raw_roots(raw):
        direct = root / "Annotations.csv"
        if direct.exists():
            return direct
        matches = list(root.rglob("Annotations.csv"))
        if matches:
            return matches[0]
    raise SystemExit(
        "Annotations.csv was not found. URL-import the official NOAA Annotations.csv alongside the selected official audio files."
    )


def _audio_index(raw: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for root in _raw_roots(raw):
        for path in root.rglob("*"):
            if path.suffix.lower() in {".wav", ".flac"}:
                name = path.name
                if name in index and index[name] != path:
                    raise SystemExit(f"duplicate raw audio basename would make source lookup ambiguous: {name}")
                index[name] = path
    if not index:
        raise SystemExit("No official WAV/FLAC audio objects were found under raw/.")
    return index


def _load_annotations(raw: Path, audio_by_name: dict[str, Path]) -> pd.DataFrame:
    ann_path = _find_annotations(raw)
    df = pd.read_csv(ann_path)
    required = {
        "Soundfile",
        "Dataset",
        "LowFreqHz",
        "HighFreqHz",
        "FileEndSec",
        "FileBeginSec",
        "ClassSpecies",
        "KW",
        "KW_certain",
        "Ecotype",
        "Provider",
        "AnnotationLevel",
        "FileOk",
    }
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Annotations.csv is missing required columns: {sorted(missing)}")
    df = df[df["Soundfile"].astype(str).isin(set(audio_by_name))].copy()
    if df.empty:
        raise SystemExit("Annotations.csv did not reference any imported audio basenames.")
    for col in ["FileBeginSec", "FileEndSec", "LowFreqHz", "HighFreqHz", "KW", "KW_certain"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["ClassSpecies"] = df["ClassSpecies"].astype(str).str.strip()
    df["Provider"] = df["Provider"].astype(str).str.strip()
    df["Dataset"] = df["Dataset"].astype(str).str.strip()
    df["Soundfile"] = df["Soundfile"].astype(str).str.strip()
    df["Ecotype"] = df["Ecotype"].where(df["Ecotype"].notna(), "").astype(str).str.strip()
    ok = df["FileOk"].astype(str).str.lower().isin({"true", "1", "yes"})
    df = df[ok & df["FileBeginSec"].notna() & df["FileEndSec"].notna()].copy()
    df = df[df["FileEndSec"] > df["FileBeginSec"]].copy()
    if df.empty:
        raise SystemExit("No usable annotations remain after validation.")
    return df


def _recording_group(soundfile: str, provider: str, dataset: str) -> str:
    stem = Path(soundfile).stem
    return f"{provider}:{dataset}:{stem}"


def _overlaps(group: pd.DataFrame, start: float, end: float) -> pd.DataFrame:
    return group[(group["FileBeginSec"] < end) & (group["FileEndSec"] > start)].copy()


def _clip_bounds(center: float, duration: float, file_duration: float) -> tuple[float, float]:
    start = center - duration / 2.0
    end = center + duration / 2.0
    if start < 0:
        end -= start
        start = 0.0
    if end > file_duration:
        start = max(0.0, start - (end - file_duration))
        end = file_duration
    if end - start < 2.0:
        end = min(file_duration, start + duration)
    return round(float(start), 3), round(float(end), 3)


def _quiet_windows(group: pd.DataFrame, file_duration: float) -> list[tuple[float, float]]:
    candidates: list[tuple[float, float]] = []
    for frac in [0.18, 0.38, 0.58, 0.78]:
        center = max(CLIP_SECONDS / 2.0, min(file_duration - CLIP_SECONDS / 2.0, file_duration * frac))
        start, end = _clip_bounds(center, CLIP_SECONDS, file_duration)
        ov = _overlaps(group, start, end)
        if len(ov) <= 1 and int(ov["KW"].fillna(0).sum()) == 0:
            candidates.append((start, end))
    return candidates


def _file_duration(audio_path: Path, group: pd.DataFrame) -> float:
    try:
        info = sf.info(str(audio_path))
        if info.samplerate and info.frames:
            return max(float(info.frames) / float(info.samplerate), float(group["FileEndSec"].max()) + 0.1)
    except Exception:
        pass
    return max(float(group["FileEndSec"].max()) + 0.1, CLIP_SECONDS)


def _make_candidates(df: pd.DataFrame, audio_by_name: dict[str, Path], max_clips_per_file: int, min_rows: int) -> list[Candidate]:
    candidates: list[Candidate] = []
    for soundfile, group in df.groupby("Soundfile", sort=True):
        group = group.sort_values(["KW", "FileBeginSec", "FileEndSec"], ascending=[False, True, True]).copy()
        audio_path = audio_by_name[str(soundfile)]
        provider = str(group["Provider"].iloc[0])
        dataset = str(group["Dataset"].iloc[0])
        split_group = _recording_group(str(soundfile), provider, dataset)
        duration = _file_duration(audio_path, group)
        windows: list[tuple[str, float, float, str]] = []

        kw = group[group["KW"].fillna(0).astype(int) == 1].copy()
        if not kw.empty:
            dense = kw.assign(
                local_density=kw.apply(
                    lambda r: int(
                        ((kw["FileBeginSec"] < float(r["FileBeginSec"]) + 8.0) & (kw["FileEndSec"] > float(r["FileBeginSec"]) - 2.0)).sum()
                    ),
                    axis=1,
                )
            ).sort_values(["local_density", "FileBeginSec"], ascending=[False, True])
            for _, row in dense.head(2).iterrows():
                center = (float(row["FileBeginSec"]) + float(row["FileEndSec"])) / 2.0
                start, end = _clip_bounds(center, CLIP_SECONDS, duration)
                windows.append(("kw", start, end, f"kw_{row.name}"))
            sparse = dense.sort_values(["local_density", "FileBeginSec"], ascending=[True, True])
            for _, row in sparse.head(1).iterrows():
                center = (float(row["FileBeginSec"]) + float(row["FileEndSec"])) / 2.0
                start, end = _clip_bounds(center, CLIP_SECONDS, duration)
                windows.append(("kw_sparse", start, end, f"kw_sparse_{row.name}"))

        non_kw = group[group["KW"].fillna(0).astype(int) == 0].copy()
        if not non_kw.empty:
            conf = non_kw.assign(priority=non_kw["ClassSpecies"].map({"HW": 3, "UndBio": 2, "AB": 1}).fillna(0))
            conf = conf.sort_values(["priority", "FileBeginSec"], ascending=[False, True])
            for _, row in conf.head(1).iterrows():
                center = (float(row["FileBeginSec"]) + float(row["FileEndSec"])) / 2.0
                start, end = _clip_bounds(center, CLIP_SECONDS, duration)
                windows.append(("confounder", start, end, f"conf_{row.name}"))

        for start, end in _quiet_windows(group, duration)[:1]:
            windows.append(("quiet", start, end, "quiet"))

        seen: set[tuple[float, float]] = set()
        ordered = sorted(windows, key=lambda w: _hash_text(ID_SALT, soundfile, w[0], w[3]))
        picked = 0
        for kind, start, end, _ in ordered:
            key = (start, end)
            if key in seen:
                continue
            seen.add(key)
            candidates.append(
                Candidate(
                    soundfile=str(soundfile),
                    audio_path=audio_path,
                    provider=provider,
                    dataset=dataset,
                    split_group=split_group,
                    start_sec=start,
                    end_sec=end,
                    source_kind=kind,
                )
            )
            picked += 1
            if picked >= max_clips_per_file:
                break
    if len(candidates) < min_rows:
        raise SystemExit(f"Only {len(candidates)} candidate clips were built; expected at least {min_rows}.")
    keys = [(c.soundfile, c.start_sec, c.end_sec) for c in candidates]
    if len(set(keys)) != len(keys):
        raise SystemExit("candidate source-window uniqueness check failed")
    return candidates


def _assign_splits(candidates: list[Candidate], min_group_test: int = MIN_GROUP_TEST) -> dict[str, str]:
    by_group: dict[str, list[Candidate]] = {}
    for cand in candidates:
        by_group.setdefault(cand.split_group, []).append(cand)
    groups = sorted(by_group, key=lambda g: _hash_text(ID_SALT, "split", g))
    split: dict[str, str] = {}
    test_count = 0
    total = len(candidates)
    target = int(round(total * 0.30))
    for group in groups:
        group_size = len(by_group[group])
        if test_count < target and (test_count + group_size) <= max(target + 12, int(total * 0.36)):
            split[group] = "test"
            test_count += group_size
        else:
            split[group] = "train"
    if test_count < max(24, int(total * 0.18)):
        for group in groups:
            if split[group] == "train":
                split[group] = "test"
                test_count += len(by_group[group])
            if test_count >= target:
                break

    providers = sorted({cand.provider for cand in candidates})
    for provider in providers:
        provider_total = sum(len(items) for items in by_group.values() if items[0].provider == provider)
        if provider_total < min_group_test:
            continue
        provider_test = sum(
            len(items)
            for group, items in by_group.items()
            if split[group] == "test" and items[0].provider == provider
        )
        while provider_test < min_group_test:
            options = [
                group
                for group, items in by_group.items()
                if split[group] == "train" and items[0].provider == provider
            ]
            if not options:
                break
            options.sort(key=lambda g: (len(by_group[g]), _hash_text(ID_SALT, "provider-repair", provider, g)))
            chosen = options[0]
            split[chosen] = "test"
            provider_test += len(by_group[chosen])
    return split


def _dominant(values: pd.Series) -> str:
    values = values[values.astype(str).str.len() > 0].astype(str)
    if values.empty:
        return ""
    return str(values.value_counts().sort_values(ascending=False).index[0])


def _band_bucket(rows: pd.DataFrame, has_orca: bool) -> str:
    if not has_orca:
        return "no_call"
    freqs = rows[rows["KW"].fillna(0).astype(int) == 1][["LowFreqHz", "HighFreqHz"]].dropna()
    freqs = freqs[(freqs["HighFreqHz"] > 0) & (freqs["LowFreqHz"] >= 0)]
    if freqs.empty:
        return "mid_band"
    low = float(freqs["LowFreqHz"].median())
    high = float(freqs["HighFreqHz"].median())
    width = high - low
    if width >= 8500 or (low < 400 and high > 9000):
        return "broad_band"
    if high <= 1600:
        return "low_band"
    if low >= 3500 or high >= 3500:
        return "high_band"
    return "mid_band"


def _labels(overlap: pd.DataFrame) -> dict[str, object]:
    if overlap.empty:
        return {
            "orca_presence": "no",
            "encounter_activity": "quiet_background",
            "ecotype_context": "not_orca_or_unknown",
            "confounder_type": "ambient_background",
            "call_band_bucket": "no_call",
            "confidence": 0.74,
            "activity_group": "quiet_background",
            "confounder_group": "ambient_background",
            "ecotype_group": "not_orca_or_unknown",
            "band_group": "no_call",
            "quality_group": "clear_or_background",
        }

    kw_rows = overlap[overlap["KW"].fillna(0).astype(int) == 1].copy()
    non_kw = overlap[overlap["KW"].fillna(0).astype(int) == 0].copy()
    kw_count = int(len(kw_rows))
    non_kw_count = int(len(non_kw))
    has_orca = kw_count > 0
    certain_kw = int((kw_rows["KW_certain"].fillna(0).astype(float) == 1.0).sum())

    if has_orca and certain_kw == 0:
        presence = "uncertain"
    elif has_orca and non_kw_count > 0 and kw_count <= 2:
        presence = "uncertain"
    elif has_orca and non_kw_count > kw_count * 1.5:
        presence = "uncertain"
    elif has_orca:
        presence = "yes"
    else:
        presence = "no"

    if not has_orca and non_kw_count == 0:
        activity = "quiet_background"
    elif not has_orca:
        activity = "confuser_dominant"
    elif non_kw_count > kw_count and kw_count <= 1:
        activity = "confuser_dominant"
    elif kw_count == 1:
        activity = "single_call"
    elif kw_count <= 5:
        activity = "multiple_calls"
    else:
        activity = "dense_calling"

    eco = _dominant(kw_rows["Ecotype"]) if has_orca else ""
    ecotype_context = eco if eco in {"SRKW", "TKW", "NRKW", "OKW"} else "not_orca_or_unknown"

    species = set(non_kw["ClassSpecies"].astype(str))
    if has_orca and non_kw_count > 0:
        confounder = "mixed_or_uncertain"
    elif "HW" in species:
        confounder = "humpback_or_other_bio"
    elif "UndBio" in species:
        confounder = "unidentified_bio"
    elif "AB" in species or not has_orca:
        confounder = "ambient_background"
    else:
        confounder = "none"

    band = _band_bucket(overlap, has_orca)
    confidence = 0.90
    if presence == "uncertain":
        confidence -= 0.16
    if non_kw_count > 0 and has_orca:
        confidence -= 0.08
    if activity in {"single_call", "confuser_dominant"}:
        confidence -= 0.06
    if certain_kw < kw_count:
        confidence -= 0.04
    if band == "mid_band" and has_orca and kw_rows[["LowFreqHz", "HighFreqHz"]].dropna().empty:
        confidence -= 0.05
    confidence = float(np.clip(round(confidence, 3), 0.48, 0.96))
    if band in {"low_band", "high_band", "broad_band"}:
        band_group = "edge_or_broad_call_band"
    else:
        band_group = band
    quality = "clear_or_background" if confidence >= 0.84 or not has_orca else "ambiguous_or_confounded"
    return {
        "orca_presence": presence,
        "encounter_activity": activity,
        "ecotype_context": ecotype_context,
        "confounder_type": confounder,
        "call_band_bucket": band,
        "confidence": confidence,
        "activity_group": activity,
        "confounder_group": confounder,
        "ecotype_group": ecotype_context,
        "band_group": band_group,
        "quality_group": quality,
    }


def _read_rendered_clip(audio_path: Path, start_sec: float, end_sec: float, sample_key: str) -> np.ndarray:
    info = sf.info(str(audio_path))
    sr = int(info.samplerate)
    start_frame = max(0, int(math.floor(start_sec * sr)))
    frames = max(1, int(math.ceil((end_sec - start_sec) * sr)))
    data, read_sr = sf.read(str(audio_path), start=start_frame, frames=frames, always_2d=False)
    if read_sr != sr:
        sr = int(read_sr)
    data = np.asarray(data, dtype=np.float32)
    if data.ndim == 2:
        data = data.mean(axis=1)
    data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    if data.size == 0:
        raise ValueError(f"empty rendered clip source: {audio_path}")

    target_len_src = max(1, int(round(CLIP_SECONDS * sr)))
    if len(data) < target_len_src:
        data = np.pad(data, (0, target_len_src - len(data)))
    elif len(data) > target_len_src:
        data = data[:target_len_src]

    if sr != TARGET_SR:
        gcd = math.gcd(sr, TARGET_SR)
        data = resample_poly(data, TARGET_SR // gcd, sr // gcd).astype(np.float32)
    target_len = int(round(CLIP_SECONDS * TARGET_SR))
    if len(data) < target_len:
        data = np.pad(data, (0, target_len - len(data)))
    elif len(data) > target_len:
        data = data[:target_len]

    speed_opts = [(159, 160), (160, 160), (161, 160)]
    opt = speed_opts[int(_hash_text("speed", sample_key)[:2], 16) % len(speed_opts)]
    if opt != (160, 160):
        warped = resample_poly(data, opt[0], opt[1]).astype(np.float32)
        if len(warped) >= target_len:
            offset = int(_hash_text("crop", sample_key)[:8], 16) % max(1, len(warped) - target_len + 1)
            data = warped[offset : offset + target_len]
        else:
            data = np.pad(warped, (0, target_len - len(warped)))

    smooth_width = 7 + 2 * (int(_hash_text("smooth", sample_key)[:2], 16) % 3)
    kernel = np.ones(smooth_width, dtype=np.float32) / smooth_width
    low = np.convolve(data, kernel, mode="same").astype(np.float32)
    tilt = -0.035 + 0.070 * (int(_hash_text("tilt", sample_key)[:8], 16) / 0xFFFFFFFF)
    data = data + tilt * (data - low)
    rng = np.random.default_rng(int(_hash_text("dither", sample_key)[:16], 16) % (2**32))
    data = data + rng.normal(0.0, 10 ** (-60 / 20), size=len(data)).astype(np.float32)
    peak = float(np.max(np.abs(data)))
    if peak > 0:
        data = 0.90 * data / peak
    return data.astype(np.float32)


def _duration_bucket(seconds: float) -> str:
    if seconds < 6.5:
        return "short"
    if seconds < 9.5:
        return "standard"
    return "long"


def _train_prior_column(ids: pd.Series, train_df: pd.DataFrame, col: str) -> list[str]:
    counts = train_df[col].astype(str).value_counts(normalize=True).sort_index()
    labels = counts.index.to_list()
    probs = counts.to_numpy(dtype=float)
    probs = probs / probs.sum()
    cdf = np.cumsum(probs)
    out: list[str] = []
    for sample_id in ids.astype(str):
        u = int(_hash_text(ID_SALT, "sample-v3", col, sample_id)[:12], 16) / float(16**12 - 1)
        idx = int(np.searchsorted(cdf, u, side="right"))
        out.append(labels[min(idx, len(labels) - 1)])
    return out


def _validate_outputs(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    answers_df: pd.DataFrame,
    public: Path,
    min_group_test: int,
    min_rows: int,
) -> None:
    for name, df in [("train.csv", train_df), ("test.csv", test_df), ("answers.csv", answers_df)]:
        if df.empty:
            raise SystemExit(f"{name} is empty")
        if df.isna().any().any():
            raise SystemExit(f"{name} contains NaN values")
    if len(train_df) + len(test_df) < min_rows:
        raise SystemExit(f"prepared split has too few rows: {len(train_df) + len(test_df)}")
    if set(train_df["id"]).intersection(set(test_df["id"])):
        raise SystemExit("train/test id overlap")
    if set(test_df["id"]) != set(answers_df["id"]):
        raise SystemExit("test ids do not match private answer ids")
    train_groups = set(train_df.get("split_group", pd.Series(dtype=str)).astype(str))
    answer_groups = set(answers_df["split_group"].astype(str))
    if train_groups.intersection(answer_groups):
        raise SystemExit("recording split_group overlap between train and test")
    for col in SUBMISSION_COLUMNS[1:-1]:
        missing = sorted(set(answers_df[col].astype(str)) - set(train_df[col].astype(str)))
        if missing:
            raise SystemExit(f"hidden {col} labels lack training coverage: {missing}")
    for rel in pd.concat([train_df["audio_path"], test_df["audio_path"]]).astype(str):
        path = public / rel
        if not path.exists():
            raise SystemExit(f"missing public audio file referenced by CSV: {rel}")
        low = rel.lower()
        leak_tokens = [
            "dfo",
            "orcasound",
            "smru",
            "simres",
            "lime",
            "kiln",
            "bush",
            "townsend",
            "tekteksen",
            "northbc",
            "wvanisl",
            "utc",
            "iclisten",
            "rpi",
        ]
        if any(tok in low for tok in leak_tokens):
            raise SystemExit(f"public audio path leaks source token: {rel}")
    for axis in ["provider_family", "activity_group", "confounder_group", "band_group", "quality_group"]:
        counts = answers_df[axis].astype(str).value_counts()
        sparse = counts[counts < min_group_test]
        if not sparse.empty:
            raise SystemExit(f"test hidden subgroup {axis} has sparse groups below {min_group_test}: {sparse.to_dict()}")


def prepare(
    raw: Path,
    public: Path,
    private: Path,
    max_source_files: int | None = None,
    max_clips_per_file: int = DEFAULT_MAX_CLIPS_PER_FILE,
    min_group_test: int = MIN_GROUP_TEST,
    min_rows: int = MIN_ROWS,
) -> None:
    raw = raw.resolve()
    public = public.resolve()
    private = private.resolve()
    if public == raw or private == raw:
        raise SystemExit("public/private output directories must be separate from raw")
    if public.exists():
        shutil.rmtree(public)
    if private.exists():
        shutil.rmtree(private)
    (public / "train" / "audio").mkdir(parents=True, exist_ok=True)
    (public / "test" / "audio").mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    audio_by_name = _audio_index(raw)
    if max_source_files is not None:
        keep = sorted(audio_by_name, key=lambda n: _hash_text(ID_SALT, "smoke-file", n))[:max_source_files]
        audio_by_name = {name: audio_by_name[name] for name in keep}
    ann = _load_annotations(raw, audio_by_name)
    candidates = _make_candidates(ann, audio_by_name, max_clips_per_file=max_clips_per_file, min_rows=min_rows)
    split_map = _assign_splits(candidates, min_group_test=min_group_test)

    train_rows: list[dict[str, object]] = []
    test_rows: list[dict[str, object]] = []
    answer_rows: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for cand in sorted(candidates, key=lambda c: _hash_text(ID_SALT, "materialize", c.soundfile, c.start_sec, c.end_sec)):
        split = split_map[cand.split_group]
        source_key = _hash_text(ID_SALT, cand.soundfile, cand.start_sec, cand.end_sec)
        sample_id = "oet_" + source_key[:14]
        if sample_id in seen_ids:
            raise SystemExit(f"public id collision: {sample_id}")
        seen_ids.add(sample_id)
        rel_audio = f"{split}/audio/{sample_id}.wav"
        clip = _read_rendered_clip(cand.audio_path, cand.start_sec, cand.end_sec, source_key)
        sf.write(public / rel_audio, clip, TARGET_SR, subtype="PCM_16")

        overlap = _overlaps(ann[ann["Soundfile"] == cand.soundfile], cand.start_sec, cand.end_sec)
        labels = _labels(overlap)
        public_row = {
            "id": sample_id,
            "audio_path": rel_audio,
            "clip_duration_bucket": _duration_bucket(CLIP_SECONDS),
            "prompt": PROMPT,
            **{k: labels[k] for k in SUBMISSION_COLUMNS[1:]},
            "split_group": cand.split_group,
        }
        answer_row = {
            **{k: public_row[k] for k in SUBMISSION_COLUMNS},
            "provider_family": cand.provider,
            "ecotype_group": labels["ecotype_group"],
            "activity_group": labels["activity_group"],
            "confounder_group": labels["confounder_group"],
            "band_group": labels["band_group"],
            "quality_group": labels["quality_group"],
            "split_group": cand.split_group,
        }
        if split == "train":
            train_rows.append(public_row)
        else:
            test_rows.append({k: public_row[k] for k in TEST_COLUMNS})
            answer_rows.append(answer_row)

    train_df = pd.DataFrame(train_rows).sort_values("id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows, columns=TEST_COLUMNS).sort_values("id").reset_index(drop=True)
    answers_df = pd.DataFrame(answer_rows, columns=ANSWER_COLUMNS).sort_values("id").reset_index(drop=True)
    _validate_outputs(train_df, test_df, answers_df, public, min_group_test=min_group_test, min_rows=min_rows)

    train_public = train_df[TRAIN_COLUMNS].copy()
    train_public.to_csv(public / "train.csv", index=False)
    test_df.to_csv(public / "test.csv", index=False)

    sample = pd.DataFrame({"id": test_df["id"]})
    for col in SUBMISSION_COLUMNS[1:-1]:
        sample[col] = _train_prior_column(test_df["id"], train_public, col)
    sample["confidence"] = float(round(float(train_public["confidence"].median()), 3))
    sample = sample[SUBMISSION_COLUMNS]
    sample.to_csv(public / "sample_submission.csv", index=False)
    answers_df.to_csv(private / "answers.csv", index=False)
    print(f"prepared {len(train_public)} train rows and {len(test_df)} test rows from {len(audio_by_name)} official audio files")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    parser.add_argument("--max-source-files", type=int, default=None)
    parser.add_argument("--max-clips-per-file", type=int, default=DEFAULT_MAX_CLIPS_PER_FILE)
    parser.add_argument("--min-group-test", type=int, default=MIN_GROUP_TEST)
    parser.add_argument("--min-rows", type=int, default=MIN_ROWS)
    args = parser.parse_args()
    prepare(
        args.raw,
        args.public,
        args.private,
        max_source_files=args.max_source_files,
        max_clips_per_file=args.max_clips_per_file,
        min_group_test=args.min_group_test,
        min_rows=args.min_rows,
    )


if __name__ == "__main__":
    main()
