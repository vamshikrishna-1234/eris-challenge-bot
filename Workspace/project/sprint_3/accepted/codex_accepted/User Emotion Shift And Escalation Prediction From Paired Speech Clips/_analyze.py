from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import wave
from pathlib import Path

import numpy as np
import pandas as pd

import grade as grade_mod
import prepare as prep


CODE_LEAK_RE = re.compile(r"\d{4}_[A-Z]{3}_(ANG|DIS|FEA|HAP|NEU|SAD)_(LO|MD|HI|XX)", re.IGNORECASE)


def _mode(series: pd.Series, default: str) -> str:
    counts = series.astype(str).value_counts()
    if counts.empty:
        return default
    return str(counts.sort_values(ascending=False).index[0])


def _score(name: str, sub: pd.DataFrame, answers: pd.DataFrame) -> float:
    score = grade_mod.grade(sub[prep.SUBMISSION_COLUMNS], answers)
    print(f"baseline.{name}: {score:.6f}")
    return score


def _prior_submission(train: pd.DataFrame, test: pd.DataFrame, confidence: float = 0.38) -> pd.DataFrame:
    values = {
        "affect_label": _mode(train["affect_label"], "neutral_or_unclear"),
        "valence_shift": _mode(train["valence_shift"], "no_clear_shift"),
        "arousal_shift": _mode(train["arousal_shift"], "no_clear_shift"),
        "escalation_tier": _mode(train["escalation_tier"], "none"),
    }
    out = pd.DataFrame({"id": test["id"].astype(int), "sample_id": test["sample_id"].astype(int)})
    for col, value in values.items():
        out[col] = value
    out["confidence"] = confidence
    return out[prep.SUBMISSION_COLUMNS]


def _group_mode_submission(train: pd.DataFrame, test: pd.DataFrame, group_cols: list[str], confidence: float = 0.40) -> pd.DataFrame:
    global_modes = {
        "affect_label": _mode(train["affect_label"], "neutral_or_unclear"),
        "valence_shift": _mode(train["valence_shift"], "no_clear_shift"),
        "arousal_shift": _mode(train["arousal_shift"], "no_clear_shift"),
        "escalation_tier": _mode(train["escalation_tier"], "none"),
    }
    train = train.copy()
    test = test.copy()
    train["_key"] = train[group_cols].astype(str).agg("|".join, axis=1)
    test["_key"] = test[group_cols].astype(str).agg("|".join, axis=1)
    maps: dict[str, dict[str, str]] = {}
    for label_col in global_modes:
        maps[label_col] = train.groupby("_key")[label_col].agg(lambda s: _mode(s, global_modes[label_col])).to_dict()
    out = pd.DataFrame({"id": test["id"].astype(int), "sample_id": test["sample_id"].astype(int)})
    for label_col, default in global_modes.items():
        out[label_col] = test["_key"].map(maps[label_col]).fillna(default).astype(str)
    out["confidence"] = confidence
    return out[prep.SUBMISSION_COLUMNS]


def _read_wav(path: Path) -> tuple[int, np.ndarray]:
    with wave.open(str(path), "rb") as wf:
        sr = wf.getframerate()
        channels = wf.getnchannels()
        width = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())
    if width == 1:
        x = (np.frombuffer(frames, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    elif width == 2:
        x = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
    else:
        x = np.frombuffer(frames, dtype="<i4").astype(np.float32) / 2147483648.0
    if channels > 1:
        x = x.reshape(-1, channels).mean(axis=1)
    return sr, x.astype(np.float32)


def _clip_features(path: Path) -> np.ndarray:
    sr, x = _read_wav(path)
    if x.size == 0:
        return np.zeros(10, dtype=np.float32)
    x = x.astype(np.float32)
    duration = x.size / max(1, sr)
    rms = float(np.sqrt(np.mean(x**2)))
    mean_abs = float(np.mean(np.abs(x)))
    peak = float(np.max(np.abs(x)))
    zcr = float(np.mean(np.signbit(x[1:]) != np.signbit(x[:-1]))) if x.size > 1 else 0.0
    if x.size >= 64:
        window = np.hanning(x.size)
        spec = np.abs(np.fft.rfft(x * window))
        freqs = np.fft.rfftfreq(x.size, d=1.0 / sr)
        denom = float(spec.sum()) + 1e-9
        centroid = float((spec * freqs).sum() / denom)
        spread = float(np.sqrt((spec * (freqs - centroid) ** 2).sum() / denom))
        low_energy = float(spec[freqs <= 500].sum() / denom)
        high_energy = float(spec[freqs >= 2500].sum() / denom)
    else:
        centroid = spread = low_energy = high_energy = 0.0
    envelope = np.abs(x)
    attack = float(np.argmax(envelope >= max(1e-6, 0.75 * peak)) / max(1, x.size)) if peak > 0 else 0.0
    return np.array([duration, rms, mean_abs, peak, zcr, centroid / 4000.0, spread / 4000.0, low_energy, high_energy, attack], dtype=np.float32)


def _resample_linear(x: np.ndarray, n: int) -> np.ndarray:
    n = max(16, int(n))
    if len(x) == n:
        return x.astype(np.float32, copy=False)
    old = np.linspace(0.0, 1.0, num=len(x), endpoint=False)
    new = np.linspace(0.0, 1.0, num=n, endpoint=False)
    return np.interp(new, old, x).astype(np.float32)


def _clip_fingerprint(path: Path) -> np.ndarray:
    sr, x = _read_wav(path)
    if x.size < 512:
        return np.zeros(256, dtype=np.float32)
    if sr != 8000:
        x = _resample_linear(x, int(round(len(x) * 8000 / max(sr, 1))))
        sr = 8000
    x = x.astype(np.float32, copy=False)
    x = x / (float(np.sqrt(np.mean(x**2))) + 1e-6)
    frame = 512
    hop = 160
    if len(x) < frame:
        x = np.pad(x, (0, frame - len(x)))
    starts = range(0, len(x) - frame + 1, hop)
    freqs = np.fft.rfftfreq(frame, d=1.0 / sr)
    bands = np.linspace(150.0, 3800.0, 25)
    band_bins = [(freqs >= bands[i]) & (freqs < bands[i + 1]) for i in range(len(bands) - 1)]
    top_history: list[list[int]] = []
    vec = np.zeros(256, dtype=np.float32)
    win = np.hanning(frame).astype(np.float32)
    for start in starts:
        mag = np.abs(np.fft.rfft(x[start : start + frame] * win)).astype(np.float32)
        vals = np.array([float(mag[mask].sum()) if mask.any() else 0.0 for mask in band_bins], dtype=np.float32)
        vals = np.log1p(vals)
        if float(vals.max()) <= 0:
            top_history.append([])
            continue
        top = [int(i) for i in np.argsort(vals)[-4:]]
        top_history.append(top)
        for rank, band in enumerate(top):
            vec[(band * 11 + rank * 17) % len(vec)] += 1.0
        if len(top_history) >= 2:
            prev = top_history[-2]
            for a in prev:
                for b in top:
                    vec[(a * 31 + b * 7 + 3) % len(vec)] += 1.0
    norm = float(np.linalg.norm(vec))
    return vec / norm if norm > 0 else vec


def _pair_features(df: pd.DataFrame, public: Path) -> np.ndarray:
    feats = []
    cache: dict[str, np.ndarray] = {}
    for _, row in df.iterrows():
        row_feats = []
        for col in ["baseline_audio", "current_audio"]:
            rel = str(row[col])
            if rel not in cache:
                cache[rel] = _clip_features(public / rel)
            row_feats.append(cache[rel])
        base, cur = row_feats
        feats.append(np.concatenate([base, cur, cur - base, np.abs(cur - base)]))
    return np.vstack(feats).astype(np.float32)


def _nearest_neighbor_submission(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame:
    train_x = _pair_features(train, public)
    test_x = _pair_features(test, public)
    scale = train_x.std(axis=0) + 1e-6
    train_z = (train_x - train_x.mean(axis=0)) / scale
    test_z = (test_x - train_x.mean(axis=0)) / scale
    labels = train[["affect_label", "valence_shift", "arousal_shift", "escalation_tier"]].reset_index(drop=True)
    rows = []
    for i, vec in enumerate(test_z):
        dist = np.sum((train_z - vec) ** 2, axis=1)
        idx = int(np.argmin(dist))
        item = labels.iloc[idx].to_dict()
        item["id"] = int(test.iloc[i]["id"])
        item["sample_id"] = int(test.iloc[i]["sample_id"])
        item["confidence"] = 0.46
        rows.append(item)
    return pd.DataFrame(rows)[prep.SUBMISSION_COLUMNS]


def _shallow_acoustic_submission(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame | None:
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
    except Exception as exc:
        print(f"baseline.shallow_acoustic: not_run sklearn unavailable: {exc}")
        return None
    train_x = _pair_features(train, public)
    test_x = _pair_features(test, public)
    scaler = StandardScaler()
    train_z = scaler.fit_transform(train_x)
    test_z = scaler.transform(test_x)
    out = pd.DataFrame({"id": test["id"].astype(int).to_numpy(), "sample_id": test["sample_id"].astype(int).to_numpy()})
    confidences = []
    for col in ["affect_label", "valence_shift", "arousal_shift", "escalation_tier"]:
        if train[col].nunique() <= 1:
            out[col] = str(train[col].iloc[0])
            confidences.append(np.full(len(test), 0.35))
            continue
        clf = RandomForestClassifier(
            n_estimators=120,
            min_samples_leaf=3,
            random_state=prep.SPLIT_SEED,
            class_weight="balanced_subsample",
        )
        clf.fit(train_z, train[col].astype(str))
        out[col] = clf.predict(test_z)
        proba = clf.predict_proba(test_z)
        confidences.append(proba.max(axis=1))
    out["confidence"] = np.clip(np.mean(np.vstack(confidences), axis=0), 0.05, 0.95)
    return out[prep.SUBMISSION_COLUMNS]


def _validate_no_public_leaks(public: Path, train: pd.DataFrame, test: pd.DataFrame) -> None:
    leak_cols = {
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
    for name, df in [("train", train), ("test", test)]:
        exposed = leak_cols & set(df.columns)
        print(f"leakage.public_columns.{name}: {'FAIL ' + str(sorted(exposed)) if exposed else 'pass'}")
    for csv_path in [public / "train.csv", public / "test.csv", public / "sample_submission.csv"]:
        text = csv_path.read_text(encoding="utf-8")
        print(f"leakage.cremad_filename_tokens.{csv_path.name}: {'FAIL' if CODE_LEAK_RE.search(text) else 'pass'}")
    path_values = pd.concat([train["baseline_audio"], train["current_audio"], test["baseline_audio"], test["current_audio"]]).astype(str)
    path_leaks = [p for p in path_values if CODE_LEAK_RE.search(p) or re.search(r"\b\d{4}\b", p)]
    print(f"leakage.public_path_tokens: {'FAIL ' + str(path_leaks[:3]) if path_leaks else 'pass'}")
    missing = [p for p in path_values if not (public / p).exists()]
    tiny = [p for p in path_values if (public / p).exists() and (public / p).stat().st_size < 512]
    print(f"files.audio_exists: {'FAIL missing=' + str(len(missing)) + ' tiny=' + str(len(tiny)) if missing or tiny else 'pass'}")
    public_text = " ".join(path_values.tolist()) + " ".join(map(str, train.columns)) + " ".join(map(str, test.columns))
    sentence_words = ["eleven", "airplane", "appointment", "jacket", "surface", "minutes"]
    lexical_hits = [word for word in sentence_words if word in public_text.lower()]
    print(f"leakage.sentence_text_public: {'FAIL ' + str(lexical_hits) if lexical_hits else 'pass'}")


def _find_raw_audio_dir(root: Path) -> Path | None:
    candidates = [
        root / "raw_data" / "AudioWAV",
        root / "raw_data" / "CREMA-D" / "AudioWAV",
        root / "raw" / "AudioWAV",
        root / "raw" / "raw_upload" / "AudioWAV",
    ]
    for candidate in candidates:
        if candidate.exists() and any(candidate.rglob("*.wav")):
            return candidate
    for base in [root / "raw_data", root / "raw"]:
        if base.exists():
            matches = [p for p in base.rglob("AudioWAV") if p.is_dir() and any(p.rglob("*.wav"))]
            if matches:
                return sorted(matches)[0]
    return None


def _file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _source_lookup_stress(root: Path, public: Path, test: pd.DataFrame) -> None:
    diag_path = root / "private" / "split_diagnostics.csv"
    raw_audio = _find_raw_audio_dir(root)
    if raw_audio is None or not diag_path.exists():
        print("leakage.source_lookup_feature_top1: not_run raw AudioWAV or diagnostics unavailable")
        return

    diag = pd.read_csv(diag_path, dtype=str)
    diag = diag[diag["split"].astype(str).eq("test")].copy()
    if diag.empty:
        print("leakage.source_lookup_feature_top1: not_run no test diagnostics")
        return
    test_public = test.copy()
    test_public["_sid"] = test_public["sample_id"].astype(str)
    public_by_id = test_public.set_index("_sid")

    lookup_items: list[tuple[str, str]] = []
    for _, row in diag.sort_values("sample_id").iterrows():
        sid = str(row["sample_id"])
        if sid not in public_by_id.index:
            continue
        public_row = public_by_id.loc[sid]
        lookup_items.append((str(public_row["baseline_audio"]), str(row["baseline_source_key"])))
        lookup_items.append((str(public_row["current_audio"]), str(row["current_source_key"])))
    if not lookup_items:
        print("leakage.source_lookup_feature_top1: not_run no public/source alignment")
        return

    dedup: dict[str, str] = {}
    for rel, source_key in lookup_items:
        dedup.setdefault(rel, source_key)
    items = sorted(dedup.items(), key=lambda kv: _file_digest(public / kv[0]))[:320]
    raw_paths = sorted(raw_audio.rglob("*.wav"))
    raw_keys = [path.stem for path in raw_paths]

    def report_lookup(label: str, raw_matrix: np.ndarray, query_fn, standardize: bool) -> None:
        matrix = raw_matrix.astype(np.float32)
        if standardize:
            mean = matrix.mean(axis=0)
            scale = matrix.std(axis=0) + 1e-6
            matrix = (matrix - mean) / scale
        top1 = 0
        top5 = 0
        checked = 0
        for rel, true_key in items:
            path = public / rel
            if not path.exists():
                continue
            vec = query_fn(path).astype(np.float32)
            if standardize:
                vec = (vec - mean) / scale
                dist = np.sum((matrix - vec) ** 2, axis=1)
            else:
                norm = float(np.linalg.norm(vec))
                vec = vec / norm if norm > 0 else vec
                dist = 1.0 - np.clip(matrix @ vec, -1.0, 1.0)
            k = min(5, len(raw_keys))
            nearest = np.argpartition(dist, k - 1)[:k]
            nearest = nearest[np.argsort(dist[nearest])]
            guesses = [raw_keys[int(i)] for i in nearest]
            top1 += int(guesses[0] == true_key)
            top5 += int(true_key in guesses)
            checked += 1
        if checked == 0:
            print(f"leakage.{label}: not_run no public audio checked")
            return
        top1_rate = top1 / checked
        top5_rate = top5 / checked
        status = "pass" if top1_rate <= 0.05 and top5_rate <= 0.15 else "warn" if top1_rate <= 0.12 and top5_rate <= 0.30 else "FAIL"
        print(f"leakage.{label}: {status} rate={top1_rate:.3f} top5={top5_rate:.3f} n={checked}")

    raw_x = np.vstack([_clip_features(path) for path in raw_paths]).astype(np.float32)
    report_lookup("source_lookup_feature_top1", raw_x, _clip_features, standardize=True)
    raw_fp = np.vstack([_clip_fingerprint(path) for path in raw_paths]).astype(np.float32)
    report_lookup("source_lookup_fingerprint_top1", raw_fp, _clip_fingerprint, standardize=False)


def _label_report(train: pd.DataFrame, answers: pd.DataFrame) -> None:
    print(f"rows.train: {len(train)}")
    print(f"rows.test: {len(answers)}")
    for col in ["affect_label", "valence_shift", "arousal_shift", "escalation_tier"]:
        print(f"dist.train.{col}: {json.dumps(train[col].astype(str).value_counts().to_dict(), sort_keys=True)}")
        print(f"dist.test.{col}: {json.dumps(answers[col].astype(str).value_counts().to_dict(), sort_keys=True)}")
    for axis in ["current_affect_family", "baseline_affect_family", "intensity_transition", "sentence_group", "pair_construction", "actor_sex", "actor_race"]:
        if axis in answers.columns:
            counts = answers[axis].astype(str).value_counts()
            print(f"hidden_group.{axis}.min: {int(counts.min()) if not counts.empty else 0}")
            print(f"hidden_group.{axis}.counts: {json.dumps(counts.to_dict(), sort_keys=True)}")


def _split_report(root: Path) -> None:
    diag_path = root / "private" / "split_diagnostics.csv"
    if not diag_path.exists():
        print("split.actor_overlap: not_available")
        return
    diag = pd.read_csv(diag_path, dtype=str)
    train_actors = set(diag.loc[diag["split"].eq("train"), "actor_id"].astype(str))
    test_actors = set(diag.loc[diag["split"].eq("test"), "actor_id"].astype(str))
    overlap = train_actors & test_actors
    print(f"split.actor_overlap: {'FAIL ' + str(sorted(overlap)[:5]) if overlap else 'pass'}")
    for col in ["baseline_source_key", "current_source_key"]:
        train_keys = set(diag.loc[diag["split"].eq("train"), col].astype(str))
        test_keys = set(diag.loc[diag["split"].eq("test"), col].astype(str))
        key_overlap = train_keys & test_keys
        print(f"split.{col}_overlap: {'FAIL ' + str(sorted(key_overlap)[:5]) if key_overlap else 'pass'}")


def main() -> None:
    root = Path(__file__).resolve().parent
    public = root / "public"
    private = root / "private"
    train_path = public / "train.csv"
    test_path = public / "test.csv"
    answers_path = private / "answers.csv"
    if not (train_path.exists() and test_path.exists() and answers_path.exists()):
        print("analysis.status: prepared split not found")
        print(f"analysis.expected: run python prepare.py --raw <official-crema-d-root> --public {public} --private {private}")
        return

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    answers = pd.read_csv(answers_path)
    test_with_answers = test.merge(answers, on="sample_id", how="left", validate="one_to_one")
    if test_with_answers.isna().any().any():
        print("answers_alignment: FAIL")
        sys.exit(1)
    print("answers_alignment: pass")
    print(f"nan.train: {int(train.isna().sum().sum())}")
    print(f"nan.test: {int(test.isna().sum().sum())}")
    print(f"nan.answers: {int(answers.isna().sum().sum())}")
    _label_report(train, answers)
    _split_report(root)
    _validate_no_public_leaks(public, train, test)
    _source_lookup_stress(root, public, test)

    sample = pd.read_csv(public / "sample_submission.csv")
    _score("sample_dummy", sample, answers)
    prior = _prior_submission(train, test)
    _score("train_prior_majority", prior, answers)
    duration = _group_mode_submission(train, test, ["pair_duration_bucket"])
    _score("duration_only", duration, answers)
    metadata = _group_mode_submission(train, test, ["pair_duration_bucket"])
    _score("public_metadata_only", metadata, answers)
    print("baseline.transcript_sentence_only: not_run no transcript or source sentence text is public")
    nearest = _nearest_neighbor_submission(train, test, public)
    nn_score = _score("nearest_neighbor_audio_features", nearest, answers)
    shallow = _shallow_acoustic_submission(train, test, public)
    shallow_score = None
    if shallow is not None:
        shallow_score = _score("shallow_acoustic_random_forest", shallow, answers)
    perfect = answers[
        ["id", "sample_id", "affect_label", "valence_shift", "arousal_shift", "escalation_tier"]
    ].assign(confidence=1.0)[prep.SUBMISSION_COLUMNS]
    perfect_score = _score("perfect_labels", perfect, answers)
    if perfect_score != 1.0:
        print("check.perfect: FAIL")
        sys.exit(1)
    print("check.perfect: pass")
    if shallow_score is not None and shallow_score >= 0.70:
        print(f"warning.shallow_acoustic_high: {shallow_score:.6f}")
    if nn_score >= 0.70:
        print(f"warning.nearest_neighbor_high: {nn_score:.6f}")
    print("baseline.pretrained_audio_embedding_proxy: not_run no local pretrained speech embedding dependency configured")


if __name__ == "__main__":
    main()
