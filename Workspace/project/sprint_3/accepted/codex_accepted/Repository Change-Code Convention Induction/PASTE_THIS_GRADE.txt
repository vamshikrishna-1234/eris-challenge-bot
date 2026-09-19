from __future__ import annotations

import numpy as np
import pandas as pd


SUBMISSION_COLUMNS = [
    "row_id",
    "change_code",
    "behavior_changing",
    "rollback_safe",
    "required_followup",
    "confidence",
]
ANSWER_LABEL_COLUMNS = ["change_code", "behavior_changing", "rollback_safe", "required_followup"]
VALID_CODES = {f"T_{i:02d}" for i in range(1, 12)}
VALID_TRI = {"yes", "no", "abstain"}
VALID_FOLLOWUP = {
    "none",
    "add_test",
    "add_migration_note",
    "security_review",
    "perf_review",
    "config_review",
    "owner_review",
}

W_CODE = 0.40
W_BEHAVIOR = 0.08
W_ROLLBACK = 0.08
W_FOLLOWUP = 0.08
W_BUNDLE = 0.36
W_CORRECT = 0.92
W_CALIB = 0.08
W_MEAN = 0.70
W_WORST_DIFFICULTY = 0.10
W_WORST_POLICY = 0.10
W_WORST_SEMANTIC = 0.10


def _norm(v) -> str:
    return str(v).strip()


def _norm_lower(v) -> str:
    return str(v).strip().lower()


def _confidence(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(x) or x < 0.0 or x > 1.0:
        return None
    return float(x)


def _valid_submission_values(sub: pd.DataFrame) -> bool:
    return (
        sub["change_code"].map(lambda v: _norm(v) in VALID_CODES).all()
        and sub["behavior_changing"].map(lambda v: _norm_lower(v) in VALID_TRI).all()
        and sub["rollback_safe"].map(lambda v: _norm_lower(v) in VALID_TRI).all()
        and sub["required_followup"].map(lambda v: _norm_lower(v) in VALID_FOLLOWUP).all()
    )


def _worst_group(row_scores, group_vals):
    buckets: dict[str, list[float]] = {}
    for score, group in zip(row_scores, group_vals):
        buckets.setdefault(str(group), []).append(float(score))
    if not buckets:
        return None
    return min(float(np.mean(vals)) for vals in buckets.values())


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        clean_columns = [str(c).strip().lstrip("\ufeff") for c in submission.columns]
        if clean_columns != SUBMISSION_COLUMNS:
            return 0.0
        if not {"row_id", *ANSWER_LABEL_COLUMNS}.issubset(set(answers.columns)):
            return 0.0
        sub = submission.copy()
        sub.columns = clean_columns
        ans = answers.copy()
        try:
            sub["row_id"] = sub["row_id"].astype(int)
            ans["row_id"] = ans["row_id"].astype(int)
        except (TypeError, ValueError):
            return 0.0
        if sub["row_id"].duplicated().any() or ans["row_id"].duplicated().any():
            return 0.0
        if set(sub["row_id"].tolist()) != set(ans["row_id"].tolist()):
            return 0.0
        if not _valid_submission_values(sub):
            return 0.0
        confs = []
        for v in sub["confidence"].tolist():
            c = _confidence(v)
            if c is None:
                return 0.0
            confs.append(c)
        sub["_confidence"] = confs
        sub = sub.set_index("row_id").reindex(ans["row_id"].to_numpy()).reset_index()

        row_scores: list[float] = []
        for _, pair in pd.concat([ans.reset_index(drop=True), sub.reset_index(drop=True).add_prefix("sub_")], axis=1).iterrows():
            s_code = 1.0 if _norm(pair["sub_change_code"]) == _norm(pair["change_code"]) else 0.0
            s_behavior = 1.0 if _norm_lower(pair["sub_behavior_changing"]) == _norm_lower(pair["behavior_changing"]) else 0.0
            s_rollback = 1.0 if _norm_lower(pair["sub_rollback_safe"]) == _norm_lower(pair["rollback_safe"]) else 0.0
            s_follow = 1.0 if _norm_lower(pair["sub_required_followup"]) == _norm_lower(pair["required_followup"]) else 0.0
            bundle = 1.0 if (s_code and s_behavior and s_rollback and s_follow) else 0.0
            correctness = W_CODE * s_code + W_BEHAVIOR * s_behavior + W_ROLLBACK * s_rollback + W_FOLLOWUP * s_follow + W_BUNDLE * bundle
            calibration = 1.0 - abs(float(pair["sub__confidence"]) - bundle)
            row_scores.append(float(np.clip(W_CORRECT * correctness + W_CALIB * calibration, 0.0, 1.0)))
        if not row_scores:
            return 0.0
        acc = W_MEAN * float(np.mean(row_scores))
        total_w = W_MEAN
        if "difficulty_bucket" in ans.columns:
            acc += W_WORST_DIFFICULTY * _worst_group(row_scores, ans["difficulty_bucket"].tolist())
            total_w += W_WORST_DIFFICULTY
        if "split_group" in ans.columns:
            acc += W_WORST_POLICY * _worst_group(row_scores, ans["split_group"].tolist())
            total_w += W_WORST_POLICY
        if "semantic_group" in ans.columns:
            acc += W_WORST_SEMANTIC * _worst_group(row_scores, ans["semantic_group"].tolist())
            total_w += W_WORST_SEMANTIC
        final = float(np.clip(acc / total_w, 0.0, 1.0))
        return 1.0 if abs(final - 1.0) < 1e-12 else final
    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", type=Path, required=True)
    ap.add_argument("--answers", type=Path, required=True)
    args = ap.parse_args()
    print(f"score={grade(pd.read_csv(args.submission), pd.read_csv(args.answers)):.6f}")
