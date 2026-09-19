from __future__ import annotations

import json
import math
import wave
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import grade


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
PRIVATE = ROOT / "private"
RAW = ROOT / "raw_data"
SOURCE_KEYS = grade.SOURCE_FAMILIES


def _score(sub: pd.DataFrame, answers: pd.DataFrame) -> float:
    return grade.grade(sub[grade.REQUIRED_COLUMNS].copy(), answers)


def _mix_mean(train: pd.DataFrame) -> dict[str, float]:
    mixes = [json.loads(s) for s in train["source_mix_json"]]
    return {k: float(np.mean([m[k] for m in mixes])) for k in SOURCE_KEYS}


def _constant_submission(test: pd.DataFrame, mix: dict[str, float], dominant: str, priority: str, nuisance: str, confidence: float) -> pd.DataFrame:
    mix_json = json.dumps({k: round(float(mix[k]), 4) for k in SOURCE_KEYS}, sort_keys=True, separators=(",", ":"))
    return pd.DataFrame(
        {
            "id": test["id"],
            "source_mix_json": mix_json,
            "dominant_source": dominant,
            "enforcement_priority": priority,
            "nuisance_pattern": nuisance,
            "confidence": float(confidence),
        }
    )


def _mode(series: pd.Series) -> str:
    return str(series.mode(dropna=True).iloc[0])


def _bucket_prior_submission(train: pd.DataFrame, test: pd.DataFrame, bucket_fn) -> pd.DataFrame:
    global_mix = _mix_mean(train)
    global_dom = _mode(train["dominant_source"])
    global_pri = _mode(train["enforcement_priority"])
    global_nui = _mode(train["nuisance_pattern"])
    global_conf = float(train["confidence"].mean())
    bucket_stats = {}
    for bucket, g in train.groupby(train.apply(bucket_fn, axis=1)):
        bucket_stats[bucket] = (
            _mix_mean(g),
            _mode(g["dominant_source"]),
            _mode(g["enforcement_priority"]),
            _mode(g["nuisance_pattern"]),
            float(g["confidence"].mean()),
        )
    rows = []
    for _, row in test.iterrows():
        mix, dom, pri, nui, conf = bucket_stats.get(bucket_fn(row), (global_mix, global_dom, global_pri, global_nui, global_conf))
        rows.append(
            {
                "id": row["id"],
                "source_mix_json": json.dumps({k: round(float(mix[k]), 4) for k in SOURCE_KEYS}, sort_keys=True, separators=(",", ":")),
                "dominant_source": dom,
                "enforcement_priority": pri,
                "nuisance_pattern": nui,
                "confidence": round(float(conf), 4),
            }
        )
    return pd.DataFrame(rows)


def _read_audio_features(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
    if len(data) == 0:
        return np.zeros(18, dtype=np.float32)
    rms = float(np.sqrt(np.mean(data * data) + 1e-12))
    peak = float(np.max(np.abs(data)))
    zcr = float(np.mean(np.abs(np.diff(np.signbit(data))).astype(float)))
    q = np.quantile(np.abs(data), [0.25, 0.50, 0.75, 0.95])
    # Downsample analysis grid for a cheap full-clip spectral sketch.
    x = data[:: max(1, len(data) // 32768)]
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) + 1e-9
    freqs = np.fft.rfftfreq(len(x), d=1.0 / sr)
    total = float(spec.sum())
    centroid = float((freqs * spec).sum() / total)
    bandwidth = float(np.sqrt((((freqs - centroid) ** 2) * spec).sum() / total))
    csum = np.cumsum(spec)
    rolloff = float(freqs[np.searchsorted(csum, 0.85 * csum[-1])])
    bands = []
    for lo, hi in [(0, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000)]:
        mask = (freqs >= lo) & (freqs < hi)
        bands.append(float(spec[mask].sum() / total) if mask.any() else 0.0)
    flatness = float(np.exp(np.mean(np.log(spec))) / np.mean(spec))
    return np.array([rms, peak, zcr, *q.tolist(), centroid / 8000.0, bandwidth / 8000.0, rolloff / 8000.0, flatness, *bands], dtype=np.float32)


def _audio_knn_submission(train: pd.DataFrame, test: pd.DataFrame, k: int = 9) -> pd.DataFrame:
    train_x = np.vstack([_read_audio_features(PUBLIC / p) for p in train["audio_path"]])
    test_x = np.vstack([_read_audio_features(PUBLIC / p) for p in test["audio_path"]])
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0) + 1e-6
    train_z = (train_x - mean) / std
    test_z = (test_x - mean) / std
    train_mixes = [json.loads(s) for s in train["source_mix_json"]]
    rows = []
    for i, row in test.iterrows():
        d = np.sum((train_z - test_z[i]) ** 2, axis=1)
        idx = np.argsort(d)[:k]
        mix = {key: float(np.mean([train_mixes[j][key] for j in idx])) for key in SOURCE_KEYS}
        dom = Counter(train.iloc[idx]["dominant_source"]).most_common(1)[0][0]
        pri = Counter(train.iloc[idx]["enforcement_priority"]).most_common(1)[0][0]
        nui = Counter(train.iloc[idx]["nuisance_pattern"]).most_common(1)[0][0]
        conf = float(train.iloc[idx]["confidence"].mean())
        rows.append(
            {
                "id": row["id"],
                "source_mix_json": json.dumps({k2: round(mix[k2], 4) for k2 in SOURCE_KEYS}, sort_keys=True, separators=(",", ":")),
                "dominant_source": dom,
                "enforcement_priority": pri,
                "nuisance_pattern": nui,
                "confidence": round(conf, 4),
            }
        )
    return pd.DataFrame(rows)


def _source_lookup_probe(train: pd.DataFrame, test: pd.DataFrame) -> dict[str, object]:
    public_text = "\n".join(
        [
            (PUBLIC / "train.csv").read_text(encoding="utf-8"),
            (PUBLIC / "test.csv").read_text(encoding="utf-8"),
            (PUBLIC / "sample_submission.csv").read_text(encoding="utf-8"),
        ]
    )
    raw_hits = 0
    if (RAW / "annotations.csv").exists():
        raw_names = pd.read_csv(RAW / "annotations.csv", usecols=["audio_filename"])["audio_filename"].astype(str).unique()
        raw_hits = sum(1 for name in raw_names if name in public_text)
    leak_terms = [term for term in ["sensor_id", "audio_filename", "annotator_id", "latitude", "longitude", "borough", "block", "year", "week", "day", "hour", "split"] if term in public_text.lower()]
    path_tokens = pd.concat([train["audio_path"], test["audio_path"]]).astype(str)
    source_like_path_count = int(path_tokens.str.contains(r"\d{2}_\d{6}\.wav", regex=True).sum())
    durations = pd.concat([train["clip_duration_s"], test["clip_duration_s"]])
    return {
        "raw_filename_hits_in_public_csvs": int(raw_hits),
        "forbidden_metadata_tokens": leak_terms,
        "source_like_audio_paths": source_like_path_count,
        "unique_public_durations": sorted(float(x) for x in durations.unique()),
    }


def main() -> None:
    train = pd.read_csv(PUBLIC / "train.csv")
    test = pd.read_csv(PUBLIC / "test.csv")
    answers = pd.read_csv(PRIVATE / "answers.csv")
    sample = pd.read_csv(PUBLIC / "sample_submission.csv")
    perfect = answers[grade.REQUIRED_COLUMNS].copy()

    prior_mix = _mix_mean(train)
    train_prior = _constant_submission(
        test,
        prior_mix,
        _mode(train["dominant_source"]),
        _mode(train["enforcement_priority"]),
        _mode(train["nuisance_pattern"]),
        float(train["confidence"].mean()),
    )
    duration_only = _bucket_prior_submission(train, test, lambda r: f"dur_{float(r['clip_duration_s']):.1f}")
    id_hash_only = _bucket_prior_submission(train, test, lambda r: str(r["id"])[3:5])
    path_len_only = _bucket_prior_submission(train, test, lambda r: f"plen_{len(str(r['audio_path']))}")
    audio_knn = _audio_knn_submission(train, test, k=9)

    scores = {
        "sample_dummy": _score(sample, answers),
        "perfect_oracle": _score(perfect, answers),
        "train_prior": _score(train_prior, answers),
        "duration_only": _score(duration_only, answers),
        "id_hash_metadata_only": _score(id_hash_only, answers),
        "filename_path_length_only": _score(path_len_only, answers),
        "simple_energy_spectral_knn": _score(audio_knn, answers),
    }

    class_counts = {
        "train_enforcement_priority": train["enforcement_priority"].value_counts().to_dict(),
        "test_enforcement_priority": answers["enforcement_priority"].value_counts().to_dict(),
        "train_nuisance_pattern": train["nuisance_pattern"].value_counts().to_dict(),
        "test_nuisance_pattern": answers["nuisance_pattern"].value_counts().to_dict(),
        "test_hidden_minima": {
            axis: int(answers[axis].value_counts().min())
            for axis in [
                "priority_group_hidden",
                "nuisance_group_hidden",
                "source_family_hidden",
                "pressure_band_hidden",
                "mix_complexity_hidden",
            ]
        },
    }
    result = {
        "rows": {"train": len(train), "test": len(test)},
        "scores": scores,
        "source_lookup_probe": _source_lookup_probe(train, test),
        "class_frequency": class_counts,
        "notes": [
            "metadata-only probes use only opaque ids, path string length, and constant duration because public source metadata is stripped",
            "simple_energy_spectral_knn uses RMS, zero-crossing, quantiles, and broad spectral bands from public WAVs",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    assert scores["perfect_oracle"] == 1.0
    assert 0.12 <= scores["sample_dummy"] < 0.5
    assert scores["train_prior"] < 0.5
    assert scores["duration_only"] < 0.5
    assert result["source_lookup_probe"]["raw_filename_hits_in_public_csvs"] == 0
    assert result["source_lookup_probe"]["source_like_audio_paths"] == 0
    assert not result["source_lookup_probe"]["forbidden_metadata_tokens"]


if __name__ == "__main__":
    main()
