from __future__ import annotations

import math

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "id",
    "orca_presence",
    "encounter_activity",
    "ecotype_context",
    "confounder_type",
    "call_band_bucket",
    "confidence",
]

ORCA_PRESENCE = {"yes", "no", "uncertain"}
ENCOUNTER_ACTIVITY = {
    "quiet_background",
    "single_call",
    "multiple_calls",
    "dense_calling",
    "confuser_dominant",
}
ECOTYPE_CONTEXT = {"SRKW", "TKW", "NRKW", "OKW", "not_orca_or_unknown"}
CONFOUNDER_TYPE = {
    "humpback_or_other_bio",
    "ambient_background",
    "unidentified_bio",
    "mixed_or_uncertain",
    "none",
}
CALL_BAND_BUCKET = {"low_band", "mid_band", "high_band", "broad_band", "no_call"}

HEAD_WEIGHTS = {
    "orca_presence": 0.16,
    "encounter_activity": 0.22,
    "ecotype_context": 0.18,
    "confounder_type": 0.16,
    "call_band_bucket": 0.16,
    "confidence": 0.10,
}
WORST_GROUP_WEIGHT = 0.05
HIDDEN_GROUP_AXES = [
    "provider_family",
    "ecotype_group",
    "activity_group",
    "confounder_group",
    "band_group",
    "quality_group",
]


class InvalidSubmissionError(ValueError):
    """Raised when a submission has invalid structure or controlled values."""


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lstrip("\ufeff") for c in out.columns]
    return out


def _validate_submission(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    sub = _clean_columns(submission)
    ans = _clean_columns(answers)
    if list(sub.columns) != REQUIRED_COLUMNS:
        raise InvalidSubmissionError(f"submission columns must be exactly {REQUIRED_COLUMNS}")
    missing_answer_cols = [c for c in REQUIRED_COLUMNS if c not in ans.columns]
    if missing_answer_cols:
        raise ValueError("answers file is missing required grading columns")

    sub["id"] = sub["id"].astype(str)
    ans["id"] = ans["id"].astype(str)
    if sub["id"].duplicated().any():
        raise InvalidSubmissionError("submission contains duplicate id values")
    if ans["id"].duplicated().any():
        raise ValueError("answers file contains duplicate id values")
    if set(sub["id"]) != set(ans["id"]):
        raise InvalidSubmissionError("submission id set does not match the test set")

    checks = [
        ("orca_presence", ORCA_PRESENCE),
        ("encounter_activity", ENCOUNTER_ACTIVITY),
        ("ecotype_context", ECOTYPE_CONTEXT),
        ("confounder_type", CONFOUNDER_TYPE),
        ("call_band_bucket", CALL_BAND_BUCKET),
    ]
    for col, allowed in checks:
        bad_sub = sorted(set(sub.loc[~sub[col].astype(str).isin(allowed), col].astype(str)))
        if bad_sub:
            raise InvalidSubmissionError(f"submission column {col} contains invalid values")
        bad_ans = sorted(set(ans.loc[~ans[col].astype(str).isin(allowed), col].astype(str)))
        if bad_ans:
            raise ValueError(f"answers column {col} contains invalid values: {bad_ans[:5]}")

    sub_conf = pd.to_numeric(sub["confidence"], errors="coerce")
    ans_conf = pd.to_numeric(ans["confidence"], errors="coerce")
    if sub_conf.isna().any() or ans_conf.isna().any():
        raise InvalidSubmissionError("confidence values must be numeric and non-missing")
    if not np.isfinite(sub_conf.to_numpy(dtype=float)).all() or not np.isfinite(ans_conf.to_numpy(dtype=float)).all():
        raise InvalidSubmissionError("confidence values must be finite")
    if (sub_conf < 0).any() or (sub_conf > 1).any():
        raise InvalidSubmissionError("confidence values must be in [0, 1]")
    if (ans_conf < 0).any() or (ans_conf > 1).any():
        raise ValueError("answer confidence values must be in [0, 1]")
    sub["confidence"] = sub_conf.to_numpy(dtype=float)
    ans["confidence"] = ans_conf.to_numpy(dtype=float)

    return sub.set_index("id").sort_index(), ans.set_index("id").sort_index()


def _macro_f1(pred: pd.Series, true: pd.Series) -> float:
    pred_arr = pred.astype(str).to_numpy()
    true_arr = true.astype(str).to_numpy()
    labels = sorted(set(true_arr.tolist()))
    if not labels:
        return 0.0
    scores: list[float] = []
    for label in labels:
        tp = int(np.sum((pred_arr == label) & (true_arr == label)))
        fp = int(np.sum((pred_arr == label) & (true_arr != label)))
        fn = int(np.sum((pred_arr != label) & (true_arr == label)))
        if tp + fp == 0 and tp + fn == 0:
            scores.append(1.0)
        elif tp == 0:
            scores.append(0.0)
        else:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            scores.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(scores))


def _rows(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame:
    rows = ans.copy()
    for col in REQUIRED_COLUMNS[1:-1]:
        rows[f"pred_{col}"] = sub[col].astype(str)
    rows["pred_confidence"] = sub["confidence"].astype(float)
    rows["confidence_score"] = np.maximum(
        0.0,
        1.0 - np.abs(rows["pred_confidence"] - rows["confidence"].astype(float)) / 0.5,
    )
    return rows


def _profile_score(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    score = 0.0
    for col in REQUIRED_COLUMNS[1:-1]:
        score += HEAD_WEIGHTS[col] * (_macro_f1(rows[f"pred_{col}"], rows[col]) ** 2)
    score += HEAD_WEIGHTS["confidence"] * (float(rows["confidence_score"].mean()) ** 2)
    return float(score / sum(HEAD_WEIGHTS.values()))


def _worst_group_score(rows: pd.DataFrame) -> float:
    group_scores: list[float] = []
    for axis in HIDDEN_GROUP_AXES:
        if axis not in rows.columns:
            continue
        grouped = rows.reset_index(drop=True).groupby(axis, sort=True)
        for _, group in grouped:
            if not group.empty:
                group_scores.append(_profile_score(group))
    if not group_scores:
        return _profile_score(rows)
    return float(min(group_scores))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    sub, ans = _validate_submission(submission, answers)
    rows = _rows(sub, ans)
    base = _profile_score(rows)
    worst = _worst_group_score(rows)
    final = (1.0 - WORST_GROUP_WEIGHT) * base + WORST_GROUP_WEIGHT * worst
    if not math.isfinite(final):
        raise ValueError("computed score is not finite")
    return float(np.clip(final, 0.0, 1.0))


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--answers", type=Path, required=True)
    args = parser.parse_args()
    print(grade(pd.read_csv(args.submission), pd.read_csv(args.answers)))
