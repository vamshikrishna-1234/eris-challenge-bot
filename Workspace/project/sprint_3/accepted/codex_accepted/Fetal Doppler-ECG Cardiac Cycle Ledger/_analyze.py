from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from grade import grade


SUB_COLS = ["id", "ledger_json", "envelope_json", "quality_json", "confidence"]


def _load(public: Path, private: Path):
    return (
        pd.read_csv(public / "train.csv"),
        pd.read_csv(public / "test.csv"),
        pd.read_csv(public / "sample_submission.csv"),
        pd.read_csv(private / "answers.csv"),
    )


def _perfect(answers: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "id": answers["id"].astype(int),
        "ledger_json": answers["ledger_json"],
        "envelope_json": answers["envelope_json"],
        "quality_json": answers["quality_json"],
        "confidence": 1.0,
    })[SUB_COLS]


def _train_prior(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    counts = []
    all_env = []
    for _, row in train.iterrows():
        try:
            counts.append(len(json.loads(row["ledger_json"])))
            env = json.loads(row["envelope_json"])
            if isinstance(env, list) and env:
                all_env.append(env)
        except Exception:
            pass
    med_count = int(np.clip(round(float(np.median(counts))) if counts else 9, 4, 16))
    env = [[round(i / 63, 4), 0.43, 0.57] for i in range(64)]
    rows = []
    for _, row in test.iterrows():
        dur = float(row["segment_duration_sec"])
        step = dur / (med_count + 1)
        ledger = [
            {"t": round((i + 1) * step, 4), "start": round(max(0, (i + 0.55) * step), 4), "end": round(min(dur, (i + 1.45) * step), 4)}
            for i in range(med_count)
        ]
        rows.append({
            "id": int(row["id"]),
            "ledger_json": json.dumps(ledger, separators=(",", ":")),
            "envelope_json": json.dumps(env, separators=(",", ":")),
            "quality_json": json.dumps(["uncertain"] * med_count, separators=(",", ":")),
            "confidence": 0.30,
        })
    return pd.DataFrame(rows)[SUB_COLS]


def _metadata_only(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in test.iterrows():
        dur = float(row["segment_duration_sec"])
        count = int(np.clip(round(dur / 0.48), 4, 16))
        step = dur / (count + 1)
        rows.append({
            "id": int(row["id"]),
            "ledger_json": json.dumps([
                {"t": round((i + 1) * step, 4), "start": round(max(0, (i + 0.55) * step), 4), "end": round(min(dur, (i + 1.45) * step), 4)}
                for i in range(count)
            ], separators=(",", ":")),
            "envelope_json": json.dumps([[round(i / 63, 4), 0.45, 0.55] for i in range(64)], separators=(",", ":")),
            "quality_json": json.dumps(["uncertain"] * count, separators=(",", ":")),
            "confidence": 0.28,
        })
    return pd.DataFrame(rows)[SUB_COLS]


def _empty_valid(test: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "id": test["id"].astype(int),
        "ledger_json": "[]",
        "envelope_json": "[[0,0.45,0.55],[1,0.45,0.55]]",
        "quality_json": "[]",
        "confidence": 0.0,
    })[SUB_COLS]


def _neutral_envelope_with_wrong_events(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in test.iterrows():
        dur = float(row["segment_duration_sec"])
        rows.append({
            "id": int(row["id"]),
            "ledger_json": json.dumps([{"t": round(0.05 * dur, 4), "start": 0.0, "end": round(0.1 * dur, 4)}], separators=(",", ":")),
            "envelope_json": json.dumps([[round(i / 63, 4), 0.45, 0.55] for i in range(64)], separators=(",", ":")),
            "quality_json": json.dumps(["uncertain"], separators=(",", ":")),
            "confidence": 0.0,
        })
    return pd.DataFrame(rows)[SUB_COLS]


def _fixed_periodic_template(test: pd.DataFrame, count: int, phase: float) -> pd.DataFrame:
    rows = []
    env = [[round(i / 63, 4), 0.45, 0.55] for i in range(64)]
    for _, row in test.iterrows():
        dur = float(row["segment_duration_sec"])
        step = dur / (count + 1)
        ledger = []
        for i in range(count):
            t = (i + phase) * step
            ledger.append({
                "t": round(max(0.0, min(dur, t)), 4),
                "start": round(max(0.0, t - 0.45 * step), 4),
                "end": round(min(dur, t + 0.45 * step), 4),
            })
        rows.append({
            "id": int(row["id"]),
            "ledger_json": json.dumps(ledger, separators=(",", ":")),
            "envelope_json": json.dumps(env, separators=(",", ":")),
            "quality_json": json.dumps(["uncertain"] * count, separators=(",", ":")),
            "confidence": 0.25,
        })
    return pd.DataFrame(rows)[SUB_COLS]


def _best_fixed_periodic(test: pd.DataFrame, answers: pd.DataFrame) -> dict:
    best_score = -1.0
    best_count = None
    best_phase = None
    for count in range(1, 21):
        for phase in [0.35, 0.50, 0.65, 0.80, 1.00]:
            score = grade(_fixed_periodic_template(test, count, phase), answers)
            if score > best_score:
                best_score = float(score)
                best_count = int(count)
                best_phase = float(phase)
    return {"score": best_score, "count": best_count, "phase": best_phase}


def _structural_scores(sample: pd.DataFrame, answers: pd.DataFrame) -> dict:
    wrong_cols = sample[["id", "confidence", "ledger_json", "envelope_json", "quality_json"]]
    duplicate = pd.concat([sample.iloc[[0]], sample.iloc[[0]], sample.iloc[1:]], ignore_index=True)
    malformed = _perfect(answers)
    malformed.loc[malformed.index[0], "ledger_json"] = "{bad-json"
    return {
        "wrong_columns": grade(wrong_cols, answers),
        "duplicate_ids": grade(duplicate, answers),
        "one_malformed_row": grade(malformed, answers),
    }


def _source_leak_scan(train: pd.DataFrame, test: pd.DataFrame) -> dict:
    leak_terms = ("record", "subject", "session", "source", "raw", "timestamp", "start", "filename", "scene_hash")
    source_value_markers = ("wfdb_format", "pwd_images", ".hea", ".dat", "physionet", "ninfea/")
    source_pattern = "|".join(re.escape(x) for x in source_value_markers)
    result = {}
    for name, frame in [("train", train), ("test", test)]:
        leaky_cols = [c for c in frame.columns if any(term in c.lower() for term in leak_terms)]
        value_hits = []
        for col in frame.columns:
            if pd.api.types.is_numeric_dtype(frame[col]):
                continue
            vals = frame[col].dropna().astype(str).head(2000)
            if vals.str.contains(source_pattern, case=False, regex=True).any():
                value_hits.append(col)
        result[name] = {"leaky_columns": leaky_cols, "source_value_columns": value_hits}
    return result


def _id_leak_scan(train: pd.DataFrame, test: pd.DataFrame) -> dict:
    train_ids = train["id"].astype(int).to_numpy()
    test_ids = test["id"].astype(int).to_numpy()
    return {
        "train_min": int(train_ids.min()) if len(train_ids) else None,
        "train_max": int(train_ids.max()) if len(train_ids) else None,
        "test_min": int(test_ids.min()) if len(test_ids) else None,
        "test_max": int(test_ids.max()) if len(test_ids) else None,
        "overlap_count": int(len(set(train_ids) & set(test_ids))),
        "boundary_leak": bool(len(train_ids) and len(test_ids) and (train_ids.max() < test_ids.min() or test_ids.max() < train_ids.min())),
    }


def _artifact_size_scan(public: Path, train: pd.DataFrame, test: pd.DataFrame) -> dict:
    result = {}
    for name, frame in [("train", train), ("test", test)]:
        out = {}
        for col in ["image", "signal_npy"]:
            sizes = []
            if col in frame.columns:
                for rel in frame[col].dropna().astype(str):
                    p = public / rel
                    sizes.append(p.stat().st_size if p.exists() else -1)
            out[col] = {
                "count": len(sizes),
                "missing": int(sum(1 for s in sizes if s < 0)),
                "unique_sizes": int(len(set(sizes))),
                "min_size": int(min(sizes)) if sizes else None,
                "max_size": int(max(sizes)) if sizes else None,
            }
        result[name] = out
    return result


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python _analyze.py <public_dir> <private_dir>")
    public = Path(sys.argv[1])
    private = Path(sys.argv[2])
    train, test, sample, answers = _load(public, private)
    scores = {
        "sample": grade(sample, answers),
        "train_prior": grade(_train_prior(train, test), answers),
        "metadata_only": grade(_metadata_only(test), answers),
        "empty_valid": grade(_empty_valid(test), answers),
        "neutral_envelope_wrong_events": grade(_neutral_envelope_with_wrong_events(test), answers),
        "best_fixed_periodic": _best_fixed_periodic(test, answers),
        "perfect": grade(_perfect(answers), answers),
        "structural_scores": _structural_scores(sample, answers),
        "source_leak_scan": _source_leak_scan(train, test),
        "id_leak_scan": _id_leak_scan(train, test),
        "artifact_size_scan": _artifact_size_scan(public, train, test),
    }
    print(json.dumps(scores, indent=2))
    if abs(scores["perfect"] - 1.0) > 1e-12:
        raise SystemExit("perfect submission did not score 1.0")


if __name__ == "__main__":
    main()
