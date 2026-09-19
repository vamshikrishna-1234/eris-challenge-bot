#!/usr/bin/env python3
"""Fast mechanical smoke tests for the challenge."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from grade import REQUIRED_COLUMNS, grade


ROOT = Path(__file__).resolve().parent


def main() -> int:
    train = pd.read_csv(ROOT / "public" / "train.csv")
    test = pd.read_csv(ROOT / "public" / "test.csv")
    sample = pd.read_csv(ROOT / "public" / "sample_submission.csv")
    answers = pd.read_csv(ROOT / "private" / "answers.csv")
    assert len(train) > 0 and len(test) > 0
    assert not train.isna().any().any()
    assert not test.isna().any().any()
    assert not answers.isna().any().any()
    assert set(test["id"]) == set(sample["id"]) == set(answers["id"])
    assert not (set(train["id"]) & set(test["id"]))
    for df in [train, test, sample, answers]:
        assert not df["id"].duplicated().any()
    for p in train["image"].tolist() + test["image"].tolist():
        assert (ROOT / "public" / p).exists(), p
    for _, r in train.head(5).iterrows():
        json.loads(r["imu_trace_json"])
        json.loads(r["degraded_pose_json"])
        json.loads(r["window_meta_json"])
        json.loads(r["reliable_keyframes_json"])
        json.loads(r["failure_spans_json"])
        json.loads(r["anchor_edges_json"])
    sample_score = grade(sample, answers)
    perfect_score = grade(answers[REQUIRED_COLUMNS], answers)
    malformed = sample.copy()
    malformed.loc[malformed.index[0], "failure_spans_json"] = "{not json"
    malformed_score = grade(malformed, answers)
    all_malformed = sample.copy()
    all_malformed["failure_spans_json"] = "{not json"
    all_malformed_score = grade(all_malformed, answers)
    duplicate = sample.iloc[[0]].copy()
    duplicate_score = grade(pd.concat([sample, duplicate], ignore_index=True), answers)
    print(f"sample_score={sample_score:.6f}")
    print(f"perfect_score={perfect_score:.6f}")
    print(f"malformed_row_score={malformed_score:.6f}")
    print(f"all_malformed_rows_score={all_malformed_score:.6f}")
    print(f"duplicate_structural_score={duplicate_score:.6f}")
    assert 0.12 <= sample_score < 0.50
    assert perfect_score == 1.0
    assert malformed_score < sample_score
    assert all_malformed_score == 0.0
    assert duplicate_score == 0.0
    print("sanity smoke PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
