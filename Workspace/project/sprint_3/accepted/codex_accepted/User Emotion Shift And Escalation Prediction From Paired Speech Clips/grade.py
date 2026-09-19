from __future__ import annotations

import math

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["id", "sample_id", "affect_label", "valence_shift", "arousal_shift", "escalation_tier", "confidence"]

AFFECT_LABELS = ["angry", "sad", "happy", "neutral_or_unclear", "other_negative"]
VALENCE_LABELS = ["positive", "negative", "no_clear_shift"]
AROUSAL_LABELS = ["higher", "lower", "no_clear_shift"]
ESCALATION_LABELS = ["none", "monitor", "urgent"]
MAX_CATEGORY_LEN = 128

W_AFFECT = 0.18
W_VALENCE = 0.17
W_AROUSAL = 0.16
W_ESCALATION = 0.14
W_BUNDLE = 0.10
W_STRICT_ROW = 0.75
W_CALIBRATION = 0.15
STRICT_ROW_POWER = 5.0


class InvalidSubmissionError(ValueError):
    """Raised when a submission is malformed rather than merely wrong."""


def _validate_prediction_labels(series: pd.Series, valid: set[str], column: str) -> pd.Series:
    text = series.astype("string")
    if text.isna().any():
        raise InvalidSubmissionError(f"Invalid submission: missing values in {column}.")
    text = text.astype(str)
    if text.str.len().gt(MAX_CATEGORY_LEN).any():
        raise InvalidSubmissionError(f"Invalid submission: overlong values in {column}.")
    if (~text.isin(valid)).any():
        raise InvalidSubmissionError(f"Invalid submission: values outside the allowed set in {column}.")
    return text


def _validate_submission(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if list(submission.columns) != REQUIRED_COLUMNS:
        raise InvalidSubmissionError("Invalid submission: columns must exactly match the required schema and order.")
    required_answers = {
        "id",
        "sample_id",
        "affect_label",
        "valence_shift",
        "arousal_shift",
        "escalation_tier",
        "confidence",
    }
    if not required_answers.issubset(set(answers.columns)):
        raise InvalidSubmissionError("Invalid answer file: missing required columns.")
    sub = submission.copy()
    ans = answers.copy()
    try:
        sub["id"] = sub["id"].astype(int)
        sub["sample_id"] = sub["sample_id"].astype(int)
        ans["id"] = ans["id"].astype(int)
        ans["sample_id"] = ans["sample_id"].astype(int)
    except (TypeError, ValueError):
        raise InvalidSubmissionError("Invalid submission: id and sample_id must be integers.") from None
    if (sub["id"] != sub["sample_id"]).any() or (ans["id"] != ans["sample_id"]).any():
        raise InvalidSubmissionError("Invalid submission: id and sample_id must match on every row.")
    if sub["id"].duplicated().any() or sub["sample_id"].duplicated().any() or ans["id"].duplicated().any() or ans["sample_id"].duplicated().any():
        raise InvalidSubmissionError("Invalid submission: duplicate ids are not allowed.")
    if set(sub["id"].tolist()) != set(ans["id"].tolist()):
        raise InvalidSubmissionError("Invalid submission: submitted ids must exactly match the test ids.")

    checks = [
        ("affect_label", set(AFFECT_LABELS)),
        ("valence_shift", set(VALENCE_LABELS)),
        ("arousal_shift", set(AROUSAL_LABELS)),
        ("escalation_tier", set(ESCALATION_LABELS)),
    ]
    for col, valid in checks:
        if (~ans[col].astype(str).isin(valid)).any():
            raise InvalidSubmissionError("Invalid answer file: label values are outside the configured schema.")
        sub[col] = _validate_prediction_labels(sub[col], valid, col)

    confidence = pd.to_numeric(sub["confidence"], errors="coerce")
    if confidence.isna().any():
        raise InvalidSubmissionError("Invalid submission: confidence must be numeric for every row.")
    conf_values = confidence.to_numpy(dtype=float)
    if not np.isfinite(conf_values).all():
        raise InvalidSubmissionError("Invalid submission: confidence must be finite.")
    if (confidence < 0.0).any() or (confidence > 1.0).any():
        raise InvalidSubmissionError("Invalid submission: confidence must be in [0, 1].")
    sub["confidence"] = confidence.astype(float)

    sub = sub.set_index("id").sort_index()
    ans = ans.set_index("id").sort_index()
    return sub, ans


def _macro_f1(y_true: pd.Series, y_pred: pd.Series, labels: list[str]) -> float:
    true_values = y_true.astype(str).to_numpy()
    pred_values = y_pred.astype(str).to_numpy()
    scored_labels = [label for label in labels if np.any(true_values == label) or np.any(pred_values == label)]
    if not scored_labels:
        return 1.0
    scores: list[float] = []
    for label in scored_labels:
        tp = int(np.sum((true_values == label) & (pred_values == label)))
        fp = int(np.sum((true_values != label) & (pred_values == label)))
        fn = int(np.sum((true_values == label) & (pred_values != label)))
        if tp == 0:
            scores.append(0.0)
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        scores.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(scores))


def _head_scores(rows: pd.DataFrame) -> dict[str, float]:
    return {
        "affect": _macro_f1(rows["affect_label"], rows["pred_affect_label"], AFFECT_LABELS),
        "valence": _macro_f1(rows["valence_shift"], rows["pred_valence_shift"], VALENCE_LABELS),
        "arousal": _macro_f1(rows["arousal_shift"], rows["pred_arousal_shift"], AROUSAL_LABELS),
        "escalation": _macro_f1(rows["escalation_tier"], rows["pred_escalation_tier"], ESCALATION_LABELS),
    }


def _bundle_score(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    scores = _head_scores(rows)
    return float(
        W_AFFECT * scores["affect"]
        + W_VALENCE * scores["valence"]
        + W_AROUSAL * scores["arousal"]
        + W_ESCALATION * scores["escalation"]
    ) / (W_AFFECT + W_VALENCE + W_AROUSAL + W_ESCALATION)


def _row_exact_indicators(rows: pd.DataFrame) -> pd.Series:
    return (
        (rows["pred_affect_label"] == rows["affect_label"])
        & (rows["pred_valence_shift"] == rows["valence_shift"])
        & (rows["pred_arousal_shift"] == rows["arousal_shift"])
        & (rows["pred_escalation_tier"] == rows["escalation_tier"])
    ).astype(float)


def _strict_row_score(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    exact_rate = float(_row_exact_indicators(rows).mean())
    return float(exact_rate**STRICT_ROW_POWER)


def _calibration_score(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    cat_total = W_AFFECT + W_VALENCE + W_AROUSAL + W_ESCALATION
    correctness = (
        W_AFFECT * (rows["pred_affect_label"] == rows["affect_label"]).astype(float)
        + W_VALENCE * (rows["pred_valence_shift"] == rows["valence_shift"]).astype(float)
        + W_AROUSAL * (rows["pred_arousal_shift"] == rows["arousal_shift"]).astype(float)
        + W_ESCALATION * (rows["pred_escalation_tier"] == rows["escalation_tier"]).astype(float)
    ) / cat_total
    return float(np.maximum(0.0, 1.0 - np.abs(rows["confidence"].astype(float) - correctness)).mean())


def _aligned_rows(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame:
    rows = ans.copy()
    rows["pred_affect_label"] = sub["affect_label"].astype(str)
    rows["pred_valence_shift"] = sub["valence_shift"].astype(str)
    rows["pred_arousal_shift"] = sub["arousal_shift"].astype(str)
    rows["pred_escalation_tier"] = sub["escalation_tier"].astype(str)
    rows["confidence"] = sub["confidence"].astype(float)
    return rows


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    sub, ans = _validate_submission(submission, answers)
    rows = _aligned_rows(sub, ans)
    if rows.empty:
        raise InvalidSubmissionError("Invalid submission: no rows to score.")
    bundle = _bundle_score(rows)
    strict_row = _strict_row_score(rows)
    calibration = _calibration_score(rows)
    final = W_BUNDLE * bundle + W_STRICT_ROW * strict_row + W_CALIBRATION * calibration
    if not math.isfinite(final):
        raise InvalidSubmissionError("Invalid score: non-finite result.")
    return float(np.clip(final, 0.0, 1.0))


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--answers", type=Path, required=True)
    args = parser.parse_args()
    print(grade(pd.read_csv(args.submission), pd.read_csv(args.answers)))
