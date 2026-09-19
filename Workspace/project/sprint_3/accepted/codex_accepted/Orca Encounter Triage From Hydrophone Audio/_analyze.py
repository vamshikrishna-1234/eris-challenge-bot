from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import resample_poly
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

from grade import REQUIRED_COLUMNS, grade


LABEL_COLUMNS = REQUIRED_COLUMNS[1:-1]


def _train_prior(ids: pd.Series, train: pd.DataFrame, confidence: float) -> pd.DataFrame:
    out = pd.DataFrame({"id": ids.astype(str)})
    for col in LABEL_COLUMNS:
        counts = train[col].astype(str).value_counts(normalize=True).sort_index()
        labels = counts.index.to_list()
        probs = counts.to_numpy(dtype=float)
        probs = probs / probs.sum()
        cdf = np.cumsum(probs)
        vals: list[str] = []
        for sample_id in out["id"]:
            seed = int.from_bytes(f"{col}:{sample_id}".encode("utf-8"), "little", signed=False) % (2**32)
            u = np.random.default_rng(seed).random()
            vals.append(labels[min(int(np.searchsorted(cdf, u, side="right")), len(labels) - 1)])
        out[col] = vals
    out["confidence"] = confidence
    return out[REQUIRED_COLUMNS]


def _majority(ids: pd.Series, train: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"id": ids.astype(str)})
    for col in LABEL_COLUMNS:
        out[col] = train[col].astype(str).value_counts().index[0]
    out["confidence"] = float(train["confidence"].median())
    return out[REQUIRED_COLUMNS]


def _metadata_only(test: pd.DataFrame, train: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"id": test["id"].astype(str)})
    for col in LABEL_COLUMNS:
        mapping = train.groupby("clip_duration_bucket")[col].agg(lambda s: s.astype(str).value_counts().index[0]).to_dict()
        fallback = train[col].astype(str).value_counts().index[0]
        out[col] = test["clip_duration_bucket"].map(mapping).fillna(fallback).astype(str)
    out["confidence"] = float(train["confidence"].median())
    return out[REQUIRED_COLUMNS]


def _audio_features(public: Path, rows: pd.DataFrame) -> np.ndarray:
    feats: list[list[float]] = []
    for rel in rows["audio_path"].astype(str):
        data, sr = sf.read(public / rel, always_2d=False)
        data = np.asarray(data, dtype=np.float32)
        if data.ndim == 2:
            data = data.mean(axis=1)
        if data.size == 0:
            feats.append([0.0] * 8)
            continue
        data = np.nan_to_num(data)
        rms = float(np.sqrt(np.mean(data.astype(np.float64) ** 2) + 1e-12))
        peak = float(np.max(np.abs(data)))
        zcr = float(np.mean(np.abs(np.diff(np.signbit(data))).astype(float))) if len(data) > 1 else 0.0
        spec = np.abs(np.fft.rfft(data[: min(len(data), sr * 4)] * np.hanning(min(len(data), sr * 4))))
        freqs = np.fft.rfftfreq(len(spec) * 2 - 2, 1 / sr) if len(spec) > 1 else np.array([0.0])
        total = float(spec.sum() + 1e-12)
        centroid = float((freqs[: len(spec)] * spec).sum() / total)
        q25 = float(np.quantile(np.abs(data), 0.25))
        q75 = float(np.quantile(np.abs(data), 0.75))
        feats.append([rms, peak, zcr, centroid, q25, q75, float(len(data) / sr), float(np.mean(data))])
    return np.asarray(feats, dtype=float)


def _read_mono_16k(path: Path) -> np.ndarray:
    data, sr = sf.read(path, always_2d=False)
    data = np.asarray(data, dtype=np.float32)
    if data.ndim == 2:
        data = data.mean(axis=1)
    data = np.nan_to_num(data)
    if sr != 16000:
        gcd = int(np.gcd(int(sr), 16000))
        data = resample_poly(data, 16000 // gcd, int(sr) // gcd).astype(np.float32)
    return data


def _norm_audio(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    x = x - float(np.mean(x))
    denom = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-9)
    return (x / denom).astype(np.float32)


def _raw_audio_fingerprint_probe(public: Path, raw: Path, test: pd.DataFrame, max_test: int = 24, max_raw: int = 80) -> list[str]:
    raw_files = sorted(
        [p for p in raw.rglob("*") if p.suffix.lower() in {".wav", ".flac"}],
        key=lambda p: p.as_posix().lower(),
    )[:max_raw]
    if not raw_files:
        return ["raw fingerprint probe requested but no WAV/FLAC files were found"]
    issues: list[str] = []
    test_rows = test.sort_values("id").head(max_test)
    prepared = []
    for _, row in test_rows.iterrows():
        path = public / str(row["audio_path"])
        if path.exists():
            prepared.append((str(row["id"]), _norm_audio(_read_mono_16k(path))))
    if not prepared:
        return ["raw fingerprint probe requested but no prepared test WAVs were readable"]

    for raw_path in raw_files:
        raw_audio = _read_mono_16k(raw_path)
        if raw_audio.size < 16000:
            continue
        raw_norm = _norm_audio(raw_audio)
        for sample_id, clip in prepared:
            n = len(clip)
            if len(raw_norm) < n:
                continue
            best = 0.0
            step = max(16000, n // 2)
            for start in range(0, len(raw_norm) - n + 1, step):
                window = raw_norm[start : start + n]
                corr = abs(float(np.mean(clip * window)))
                if corr > best:
                    best = corr
            if best >= 0.995:
                issues.append(f"prepared clip {sample_id} has near-exact waveform match to raw file {raw_path.name}")
    return issues


def _simple_audio(public: Path, train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> pd.DataFrame:
    x_train = _audio_features(public, train)
    x_test = _audio_features(public, test)
    out = pd.DataFrame({"id": test["id"].astype(str)})
    for col in LABEL_COLUMNS:
        clf = RandomForestClassifier(n_estimators=80, max_depth=6, min_samples_leaf=4, random_state=17, class_weight="balanced")
        clf.fit(x_train, train[col].astype(str))
        out[col] = clf.predict(x_test)
    out["confidence"] = float(train["confidence"].median())
    return out[REQUIRED_COLUMNS]


def _binary_orca_only(ids: pd.Series, answers: pd.DataFrame, train: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({"id": ids.astype(str)})
    ans = answers.set_index("id")
    out["orca_presence"] = [ans.loc[i, "orca_presence"] for i in out["id"]]
    for col in LABEL_COLUMNS:
        if col != "orca_presence":
            out[col] = train[col].astype(str).value_counts().index[0]
    out["confidence"] = float(train["confidence"].median())
    return out[REQUIRED_COLUMNS]


def _source_leak_checks(public: Path, train: pd.DataFrame, test: pd.DataFrame, raw: Path | None = None) -> list[str]:
    issues: list[str] = []
    text = "\n".join(
        train.astype(str).to_numpy().ravel().tolist()
        + test.astype(str).to_numpy().ravel().tolist()
    ).lower()
    banned = [
        "dclde",
        "noaa",
        "dfo",
        "orcasound",
        "smru",
        "simres",
        "bush",
        "lime",
        "kiln",
        "tekteksen",
        "northbc",
        "wvanisl",
        "iclisten",
        "rpi-",
    ]
    for token in banned:
        if token in text:
            issues.append(f"public CSV contains source token: {token}")
    timestamp_pattern = re.compile(
        r"20\d{2}[_-]\d{2}[_-]\d{2}"
        r"|20\d{6}[tT]"
        r"|20\d{6}[_-]\d{6}"
        r"|20\d{2}[tT]\d{6}"
    )
    for frame_name, frame in [("train", train), ("test", test)]:
        for col in frame.columns:
            if frame[col].astype(str).str.contains(timestamp_pattern).any():
                issues.append(f"{frame_name}.{col} contains timestamp-like strings")
    for rel in pd.concat([train["audio_path"], test["audio_path"]]).astype(str):
        if not (public / rel).exists():
            issues.append(f"missing public audio: {rel}")
    if raw is not None:
        issues.extend(_raw_audio_fingerprint_probe(public, raw, test))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    parser.add_argument("--raw", type=Path, default=None, help="optional official raw folder for simple audio fingerprint stress test")
    args = parser.parse_args()
    public = args.public
    private = args.private
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    answers = pd.read_csv(private / "answers.csv")
    sample = pd.read_csv(public / "sample_submission.csv")
    perfect = answers[REQUIRED_COLUMNS].copy()

    baselines: list[tuple[str, float]] = []
    baselines.append(("sample_submission", grade(sample, answers)))
    baselines.append(("train_prior", grade(_train_prior(test["id"], train, float(train["confidence"].median())), answers)))
    baselines.append(("train_majority", grade(_majority(test["id"], train), answers)))
    baselines.append(("metadata_only", grade(_metadata_only(test, train), answers)))
    baselines.append(("binary_orca_only_oracle", grade(_binary_orca_only(test["id"], answers, train), answers)))
    try:
        baselines.append(("simple_audio_features", grade(_simple_audio(public, train, test, answers), answers)))
    except Exception as exc:
        baselines.append((f"simple_audio_features_failed:{type(exc).__name__}", float("nan")))
    baselines.append(("perfect_oracle", grade(perfect, answers)))

    print("Baseline scores:")
    for name, score in baselines:
        print(f"- {name}: {score:.6f}" if np.isfinite(score) else f"- {name}: nan")

    print("\nLabel distributions:")
    for col in LABEL_COLUMNS:
        print(f"- {col} train={train[col].astype(str).value_counts().to_dict()} hidden={answers[col].astype(str).value_counts().to_dict()}")

    print("\nHidden robustness groups:")
    for col in ["provider_family", "ecotype_group", "activity_group", "confounder_group", "band_group", "quality_group"]:
        print(f"- {col}: {answers[col].astype(str).value_counts().to_dict()}")

    issues = _source_leak_checks(public, train, test, raw=args.raw)
    if issues:
        print("\nSource leak checks: FAIL")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)
    print("\nSource leak checks: PASS")

    assert abs(baselines[-1][1] - 1.0) < 1e-12


if __name__ == "__main__":
    main()
