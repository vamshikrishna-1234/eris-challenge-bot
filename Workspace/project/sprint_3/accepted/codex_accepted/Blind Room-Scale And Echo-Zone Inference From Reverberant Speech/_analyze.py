from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import resample_poly

from grade import REQUIRED_COLUMNS, grade


LABEL_COLUMNS = ["room_volume_bucket", "rt60_bucket", "source_mic_distance_bucket", "echo_zone"]
LEAK_TERMS = [
    "502",
    "803",
    "611",
    "503",
    "403a",
    "508",
    "ee_lobby",
    "office",
    "meeting",
    "lecture",
    "lobby",
    "rir",
    "noise",
    "lin8ch",
    "crucif",
    "chromebook",
    "m1",
    "m2",
    "m3",
    "m4",
    "m5",
    "f1",
    "f2",
    "f3",
]


def _read_audio(path: Path) -> tuple[np.ndarray, int]:
    data, sr = sf.read(path, always_2d=False)
    if data.ndim == 2:
        data = data[:, 0]
    data = np.asarray(data, dtype=np.float32)
    if sr != 16000:
        gcd = math.gcd(int(sr), 16000)
        data = resample_poly(data, 16000 // gcd, sr // gcd).astype(np.float32)
        sr = 16000
    return data, sr


def _audio_features(path: Path) -> dict[str, float]:
    y, sr = _read_audio(path)
    if y.size == 0:
        y = np.zeros(1, dtype=np.float32)
    duration = y.size / sr
    rms = float(np.sqrt(np.mean(y.astype(np.float64) ** 2) + 1e-12))
    peak = float(np.max(np.abs(y)))
    zcr = float(np.mean(np.abs(np.diff(np.signbit(y).astype(np.int8)))))
    spec = np.abs(np.fft.rfft(y[: min(len(y), sr * 6)] * np.hanning(min(len(y), sr * 6))))
    freqs = np.fft.rfftfreq((len(spec) - 1) * 2, d=1 / sr)
    total = float(np.sum(spec) + 1e-12)
    centroid = float(np.sum(freqs * spec) / total)
    cumsum = np.cumsum(spec) / total
    rolloff = float(freqs[min(len(freqs) - 1, int(np.searchsorted(cumsum, 0.85)))])
    low = float(np.sum(spec[(freqs >= 80) & (freqs < 600)]) / total)
    mid = float(np.sum(spec[(freqs >= 600) & (freqs < 2400)]) / total)
    high = float(np.sum(spec[(freqs >= 2400) & (freqs < 7200)]) / total)
    frame = max(1, int(0.05 * sr))
    env = np.array([_rms(y[i : i + frame]) for i in range(0, len(y), frame)], dtype=np.float64)
    if len(env) > 6 and np.max(env) > 0:
        start = int(np.argmax(env))
        tail = np.maximum(env[start:], 1e-8)
        x = np.arange(len(tail), dtype=np.float64)
        decay = float(np.polyfit(x, np.log(tail), 1)[0]) if len(tail) > 2 else 0.0
    else:
        decay = 0.0
    return {
        "duration": duration,
        "rms": rms,
        "peak": peak,
        "zcr": zcr,
        "centroid": centroid,
        "rolloff": rolloff,
        "low_ratio": low,
        "mid_ratio": mid,
        "high_ratio": high,
        "decay_slope": decay,
    }


def _rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x.astype(np.float64) ** 2) + 1e-12))


def _score_submission(name: str, sub: pd.DataFrame, answers: pd.DataFrame) -> None:
    print(f"{name}: {grade(sub[REQUIRED_COLUMNS], answers):.6f}")


def _mode_submission(test_ids: pd.Series, train: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"sample_id": test_ids.astype(str)})
    for col in LABEL_COLUMNS:
        out[col] = str(train[col].mode().iloc[0])
    out["confidence"] = float(train["confidence"].median())
    return out[REQUIRED_COLUMNS]


def _feature_matrix(df: pd.DataFrame, public: Path) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        feats = _audio_features(public / str(row["audio_path"]))
        feats["sample_id"] = row["sample_id"]
        rows.append(feats)
    return pd.DataFrame(rows).set_index("sample_id")


def _duration_baseline(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, public: Path) -> pd.DataFrame:
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

    train_f = _feature_matrix(train, public)[["duration"]]
    test_f = _feature_matrix(test, public)[["duration"]]
    out = pd.DataFrame({"sample_id": test["sample_id"].astype(str)})
    for col in LABEL_COLUMNS:
        clf = DecisionTreeClassifier(max_depth=3, random_state=17)
        clf.fit(train_f, train[col].astype(str))
        out[col] = clf.predict(test_f)
    reg = DecisionTreeRegressor(max_depth=2, random_state=17)
    reg.fit(train_f, train["confidence"].astype(float))
    out["confidence"] = np.clip(reg.predict(test_f), 0, 1)
    return out[REQUIRED_COLUMNS]


def _nearest_neighbor_baseline(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame:
    from sklearn.metrics import pairwise_distances
    from sklearn.preprocessing import StandardScaler

    train_f = _feature_matrix(train, public)
    test_f = _feature_matrix(test, public)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(train_f)
    x_test = scaler.transform(test_f)
    nearest = pairwise_distances(x_test, x_train).argmin(axis=1)
    out = pd.DataFrame({"sample_id": test["sample_id"].astype(str)})
    for col in LABEL_COLUMNS + ["confidence"]:
        out[col] = train.iloc[nearest][col].to_numpy()
    return out[REQUIRED_COLUMNS]


def _rf_feature_baseline(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame:
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.preprocessing import StandardScaler

    train_f = _feature_matrix(train, public)
    test_f = _feature_matrix(test, public)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(train_f)
    x_test = scaler.transform(test_f)
    out = pd.DataFrame({"sample_id": test["sample_id"].astype(str)})
    for col in LABEL_COLUMNS:
        clf = RandomForestClassifier(n_estimators=120, min_samples_leaf=2, random_state=23, class_weight="balanced")
        clf.fit(x_train, train[col].astype(str))
        out[col] = clf.predict(x_test)
    reg = RandomForestRegressor(n_estimators=80, min_samples_leaf=2, random_state=29)
    reg.fit(x_train, train["confidence"].astype(float))
    out["confidence"] = np.clip(reg.predict(x_test), 0, 1)
    return out[REQUIRED_COLUMNS]


def _path_leakage_report(public_df: pd.DataFrame) -> None:
    leaks = []
    for _, row in public_df.iterrows():
        hay = f"{row.get('sample_id', '')} {row.get('audio_path', '')}".lower()
        hit = [term for term in LEAK_TERMS if re.search(rf"(^|[^a-z0-9]){re.escape(term)}([^a-z0-9]|$)", hay)]
        if hit:
            leaks.append((row.get("sample_id"), row.get("audio_path"), hit))
    print(f"filename/path leakage hits: {len(leaks)}")
    if leaks:
        for sample_id, path, hit in leaks[:10]:
            print(f"  leak? {sample_id} {path}: {hit}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--challenge", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.challenge.resolve()
    public = root / "public"
    private = root / "private"
    train_path = public / "train.csv"
    test_path = public / "test.csv"
    answers_path = private / "answers.csv"
    if not train_path.exists() or not test_path.exists() or not answers_path.exists():
        raise SystemExit(
            f"Prepared split not found under {root}. Run prepare.py first; if official ACE archives are absent, _sanity_smoke.py builds a tiny fixture."
        )

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    answers = pd.read_csv(answers_path)
    print(f"rows: train={len(train)} test={len(test)}")
    print(f"missing values: train={int(train.isna().sum().sum())} test={int(test.isna().sum().sum())} answers={int(answers.isna().sum().sum())}")
    print(f"test ids match answers: {set(test['sample_id'].astype(str)) == set(answers['sample_id'].astype(str))}")
    print(f"train/test id overlap: {len(set(train['sample_id'].astype(str)) & set(test['sample_id'].astype(str)))}")

    for col in LABEL_COLUMNS:
        print(f"train {col}: {train[col].value_counts().to_dict()}")
        print(f"test  {col}: {answers[col].value_counts().to_dict()}")
    for axis in ["room_size_family", "rt60_regime", "distance_bucket_hidden", "noise_condition", "speech_split", "mic_source_config"]:
        if axis in answers.columns:
            print(f"hidden {axis}: {answers[axis].value_counts().to_dict()}")

    _path_leakage_report(pd.concat([train[["sample_id", "audio_path"]], test[["sample_id", "audio_path"]]], ignore_index=True))
    print("transcript/speech-id-only baseline: n/a; no transcript or source speech id is public.")

    perfect = answers[REQUIRED_COLUMNS].copy()
    sample = pd.read_csv(public / "sample_submission.csv")
    mode_sub = _mode_submission(test["sample_id"], train)
    _score_submission("perfect", perfect, answers)
    _score_submission("sample_submission", sample, answers)
    _score_submission("train-prior majority", mode_sub, answers)
    _score_submission("public-metadata-only", mode_sub, answers)

    try:
        _score_submission("duration-only tree", _duration_baseline(train, test, answers, public), answers)
    except Exception as exc:
        print(f"duration-only tree: not run ({exc})")
    try:
        _score_submission("nearest-neighbor audio features", _nearest_neighbor_baseline(train, test, public), answers)
    except Exception as exc:
        print(f"nearest-neighbor audio features: not run ({exc})")
    try:
        _score_submission("shallow RF acoustic features", _rf_feature_baseline(train, test, public), answers)
    except Exception as exc:
        print(f"shallow RF acoustic features: not run ({exc})")

    print("pretrained-audio embedding proxy: not run locally; no pinned pretrained embedding dependency is bundled with the challenge.")


if __name__ == "__main__":
    main()
