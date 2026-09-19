from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf

from grade import SUBMISSION_COLUMNS, grade


def _json_verdict(score: float, provenance: str, confidence: float) -> str:
    return json.dumps(
        {"known_reader_score": round(float(score), 6), "provenance": str(provenance), "confidence": round(float(confidence), 6)},
        separators=(",", ":"),
        sort_keys=True,
    )


def _parse_train(train: pd.DataFrame) -> pd.DataFrame:
    out = train.copy()
    parsed = out["verdict_json"].map(json.loads)
    out["is_known_reader"] = [int(float(v["known_reader_score"]) >= 0.5) for v in parsed]
    out["provenance"] = [str(v["provenance"]) for v in parsed]
    return out


def _submission(ids: pd.Series, scores: list[float], labels: list[str], conf: float | list[float]) -> pd.DataFrame:
    confs = conf if isinstance(conf, list) else [float(conf)] * len(ids)
    rows = [
        {"id": str(i), "verdict_json": _json_verdict(s, p, c)}
        for i, s, p, c in zip(ids.astype(str).tolist(), scores, labels, confs)
    ]
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _train_majority(public: Path, answers: pd.DataFrame) -> tuple[str, float]:
    train = _parse_train(pd.read_csv(public / "train.csv"))
    test = pd.read_csv(public / "test.csv")
    majority = str(train["provenance"].value_counts().idxmax())
    sub = _submission(test["id"], [1.0] * len(test), [majority] * len(test), 0.45)
    return "train_majority_reader", grade(sub, answers)


def _train_prior(public: Path, answers: pd.DataFrame) -> tuple[str, float]:
    train = _parse_train(pd.read_csv(public / "train.csv"))
    test = pd.read_csv(public / "test.csv")
    labels = sorted(train["provenance"].unique().tolist())
    rows_labels = []
    rows_scores = []
    for sample_id in test["id"].astype(str):
        h = int(__import__("hashlib").sha256(("reader-prior:" + sample_id).encode()).hexdigest()[:12], 16) / float(16**12 - 1)
        if h < 0.35:
            rows_labels.append("UNKNOWN")
            rows_scores.append(0.35)
        else:
            rows_labels.append(labels[int(h * len(labels)) % len(labels)])
            rows_scores.append(0.65)
    sub = _submission(test["id"], rows_scores, rows_labels, 0.45)
    return "train_prior_with_unknown", grade(sub, answers)


def _metadata_only(public: Path, answers: pd.DataFrame) -> tuple[str, float]:
    train = _parse_train(pd.read_csv(public / "train.csv"))
    test = pd.read_csv(public / "test.csv")
    labels = sorted(train["provenance"].unique().tolist())
    global_label = str(train["provenance"].value_counts().idxmax())
    stats: dict[str, str] = {}
    for key, group in train.groupby("utterance_length_bucket"):
        stats[str(key)] = str(group["provenance"].value_counts().idxmax())
    pred = []
    scores = []
    for _, row in test.iterrows():
        label = stats.get(str(row["utterance_length_bucket"]), global_label)
        pred.append(label)
        scores.append(0.65)
    sub = _submission(test["id"], scores, pred, 0.45)
    return "metadata_only_duration_textlen", grade(sub, answers)


def _audio_features(path: Path) -> np.ndarray:
    data, sr = sf.read(path, always_2d=False)
    if data.ndim == 2:
        data = data.mean(axis=1)
    audio = np.asarray(data, dtype=np.float32)
    if audio.size == 0:
        return np.zeros(8, dtype=np.float32)
    duration = len(audio) / float(sr)
    rms = float(np.sqrt(np.mean(audio.astype(np.float64) ** 2) + 1e-12))
    zcr = float(np.mean(np.abs(np.diff(np.signbit(audio).astype(np.int8)))))
    frame = audio[: min(len(audio), sr * 6)]
    win = np.hanning(len(frame)) if len(frame) > 8 else np.ones(len(frame))
    spec = np.abs(np.fft.rfft(frame * win)) + 1e-9
    freqs = np.fft.rfftfreq(len(frame), d=1.0 / sr)
    centroid = float(np.sum(freqs * spec) / np.sum(spec))
    bandwidth = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * spec) / np.sum(spec)))
    high_ratio = float(np.sum(spec[freqs > 3000]) / np.sum(spec))
    flatness = float(np.exp(np.mean(np.log(spec))) / np.mean(spec))
    peak = float(np.max(np.abs(audio)))
    return np.asarray([duration, rms, zcr, centroid / sr, bandwidth / sr, high_ratio, flatness, peak], dtype=np.float32)


def _feature_frames(public: Path) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    train = _parse_train(pd.read_csv(public / "train.csv"))
    test = pd.read_csv(public / "test.csv")
    x_train = np.vstack([_audio_features(public / p) for p in train["audio_path"].astype(str)])
    x_test = np.vstack([_audio_features(public / p) for p in test["audio_path"].astype(str)])
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0) + 1e-6
    return train, test, (x_train - mean) / std, (x_test - mean) / std


def _centroid(public: Path, answers: pd.DataFrame) -> tuple[str, float]:
    train, test, x_train, x_test = _feature_frames(public)
    classes = sorted(train["provenance"].unique().tolist())
    centroids = {c: x_train[train["provenance"].to_numpy() == c].mean(axis=0) for c in classes}
    own_dists = [float(np.linalg.norm(x - centroids[c])) for x, c in zip(x_train, train["provenance"])]
    threshold = float(np.quantile(own_dists, 0.75)) if own_dists else 1.0
    pred = []
    scores = []
    for x in x_test:
        dists = {c: float(np.linalg.norm(x - centroids[c])) for c in classes}
        best = min(dists, key=dists.get)
        best_dist = dists[best]
        if best_dist > threshold:
            pred.append("UNKNOWN")
            scores.append(0.25)
        else:
            pred.append(best)
            scores.append(0.75)
    sub = _submission(test["id"], scores, pred, 0.55)
    return "simple_acoustic_centroid", grade(sub, answers)


def _nearest_neighbor(public: Path, answers: pd.DataFrame) -> tuple[str, float]:
    train, test, x_train, x_test = _feature_frames(public)
    labels = train["provenance"].astype(str).to_numpy()
    pred = []
    scores = []
    for x in x_test:
        d = np.linalg.norm(x_train - x[None, :], axis=1)
        k = min(5, len(d))
        idx = np.argsort(d)[:k]
        vals, counts = np.unique(labels[idx], return_counts=True)
        pred.append(str(vals[int(np.argmax(counts))]))
        scores.append(0.75)
    sub = _submission(test["id"], scores, pred, 0.50)
    return "nearest_neighbor_features", grade(sub, answers)


def _raw_audio_paths(raw: Path) -> list[Path]:
    candidates = [raw, raw / "raw_upload", raw / "raw_data"]
    paths: list[Path] = []
    for base in candidates:
        if not base.exists():
            continue
        paths.extend(sorted(base.rglob("*.flac")))
        paths.extend(sorted(base.rglob("*.wav")))
    return sorted(set(paths))


def _source_fingerprint_probe(public: Path, raw: Path | None) -> dict[str, object]:
    if raw is None or not raw.exists():
        return {"status": "skipped_no_raw", "nearest_feature_distance": None, "near_exact_matches": None}
    raw_paths = _raw_audio_paths(raw)
    if not raw_paths:
        return {"status": "skipped_no_raw_audio", "nearest_feature_distance": None, "near_exact_matches": None}
    public_csv = pd.concat([pd.read_csv(public / "train.csv"), pd.read_csv(public / "test.csv")], ignore_index=True)
    public_paths = [public / p for p in public_csv["audio_path"].astype(str).tolist()]
    public_feats = np.vstack([_audio_features(p) for p in public_paths])
    raw_paths = raw_paths[:3000]
    raw_feats = np.vstack([_audio_features(p) for p in raw_paths])
    mean = raw_feats.mean(axis=0)
    std = raw_feats.std(axis=0) + 1e-6
    pub_z = (public_feats - mean) / std
    raw_z = (raw_feats - mean) / std
    nearest = []
    for x in pub_z:
        nearest.append(float(np.min(np.linalg.norm(raw_z - x[None, :], axis=1))))
    nearest = np.asarray(nearest, dtype=float)
    return {
        "status": "ok",
        "raw_audio_compared": int(len(raw_paths)),
        "public_audio_compared": int(len(public_paths)),
        "nearest_feature_distance_min": float(np.min(nearest)) if nearest.size else None,
        "nearest_feature_distance_median": float(np.median(nearest)) if nearest.size else None,
        "near_exact_matches": int(np.sum(nearest < 1e-3)) if nearest.size else 0,
    }


def _leakage_scan(public: Path, raw: Path | None = None) -> dict[str, object]:
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    forbidden_cols = {"speaker", "speaker_id", "chapter", "chapter_id", "source_path", "source_split", "transcript", "reader_group"}
    forbidden_tokens = ["librispeech", "train-clean", "dev-clean", "speaker", "chapter"]
    cols = sorted((set(train.columns) | set(test.columns)) & forbidden_cols)
    paths = pd.concat([train["audio_path"], test["audio_path"]]).astype(str)
    bad_paths = [p for p in paths if any(tok in p.lower() for tok in forbidden_tokens)]
    return {
        "forbidden_public_columns": cols,
        "bad_path_count": len(bad_paths),
        "train_test_id_overlap": len(set(train["id"].astype(str)) & set(test["id"].astype(str))),
        "test_order_id_monotonic": bool(test["id"].astype(str).is_monotonic_increasing),
        "source_fingerprint_probe": _source_fingerprint_probe(public, raw),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    parser.add_argument("--raw", type=Path, default=None)
    args = parser.parse_args()
    public = args.public
    answers = pd.read_csv(args.private / "answers.csv")
    sample = pd.read_csv(public / "sample_submission.csv")
    perfect = answers[["id", "verdict_json"]].copy()
    rows = [
        ("sample_submission", grade(sample, answers)),
        ("perfect_oracle", grade(perfect, answers)),
    ]
    for fn in [_train_majority, _train_prior, _metadata_only, _centroid, _nearest_neighbor]:
        try:
            rows.append(fn(public, answers))
        except Exception as exc:
            rows.append((fn.__name__.lstrip("_") + "_ERROR", float("nan")))
            print(f"WARN: {fn.__name__} failed: {type(exc).__name__}: {exc}")
    print("Baseline scores:")
    for name, score in rows:
        print(f"- {name}: {score:.6f}" if math.isfinite(score) else f"- {name}: ERROR")
    print("- transcript_text_only: SKIPPED because transcript text is not public")
    print("Subgroup counts:")
    for axis in ["provenance", "source_split", "sex_group", "duration_bucket"]:
        print(f"- {axis}: {answers[axis].value_counts().sort_index().to_dict()}")
    print("Leakage scan:")
    print(json.dumps(_leakage_scan(public, args.raw), indent=2, sort_keys=True))
    public_bytes = sum(p.stat().st_size for p in public.rglob("*") if p.is_file())
    print(f"Prepared public size: {public_bytes} bytes ({public_bytes / (1024 * 1024):.2f} MiB)")


if __name__ == "__main__":
    main()
