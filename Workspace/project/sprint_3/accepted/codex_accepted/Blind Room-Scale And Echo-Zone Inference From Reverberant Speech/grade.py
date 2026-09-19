from __future__ import annotations

import math

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "sample_id",
    "room_volume_bucket",
    "rt60_bucket",
    "source_mic_distance_bucket",
    "echo_zone",
    "confidence",
]

ROOM_VOLUME_BUCKETS = {"small", "medium", "large", "very_large"}
RT60_BUCKETS = {"dry", "moderate", "reverberant", "very_reverberant"}
DISTANCE_BUCKETS = {"near", "mid", "far", "unknown_or_uncertain"}
ECHO_ZONES = {"direct_dominant", "balanced", "reverberant_dominant", "noisy_uncertain"}

W_ROOM = 0.25
W_RT60 = 0.25
W_DISTANCE = 0.20
W_ECHO = 0.15
W_CONFIDENCE = 0.10
W_WORST_SUBGROUP = 0.05
W_HEADS_TOTAL = W_ROOM + W_RT60 + W_DISTANCE + W_ECHO + W_CONFIDENCE

HIDDEN_GROUP_AXES = [
    "room_size_family",
    "rt60_regime",
    "distance_bucket_hidden",
    "noise_condition",
    "speech_split",
    "mic_source_config",
]


class InvalidSubmissionError(ValueError):
    """Raised when a submitted CSV violates the required schema or value domain."""


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lstrip("\ufeff") for c in out.columns]
    return out


def _macro_f1(pred: pd.Series, true: pd.Series) -> float:
    pred_arr = pred.astype(str).to_numpy()
    true_arr = true.astype(str).to_numpy()
    labels = sorted(set(true_arr.tolist()))
    if not labels:
        return 0.0
    f1s: list[float] = []
    for label in labels:
        tp = int(np.sum((pred_arr == label) & (true_arr == label)))
        fp = int(np.sum((pred_arr == label) & (true_arr != label)))
        fn = int(np.sum((pred_arr != label) & (true_arr == label)))
        if tp + fp == 0 and tp + fn == 0:
            f1s.append(1.0)
        elif tp == 0:
            f1s.append(0.0)
        else:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s))


def _validate_submission(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    sub = _clean_columns(submission)
    ans = _clean_columns(answers)
    if list(sub.columns) != REQUIRED_COLUMNS:
        raise InvalidSubmissionError(f"submission columns must be exactly {REQUIRED_COLUMNS}")
    if not set(REQUIRED_COLUMNS).issubset(set(ans.columns)):
        raise ValueError("answers file is missing required grading columns")

    sub["sample_id"] = sub["sample_id"].astype(str)
    ans["sample_id"] = ans["sample_id"].astype(str)
    if sub["sample_id"].duplicated().any():
        raise InvalidSubmissionError("submission contains duplicate sample_id values")
    if ans["sample_id"].duplicated().any():
        raise ValueError("answers file contains duplicate sample_id values")
    if set(sub["sample_id"]) != set(ans["sample_id"]):
        raise InvalidSubmissionError("submission sample_id set does not match the test set")

    checks = [
        ("room_volume_bucket", ROOM_VOLUME_BUCKETS),
        ("rt60_bucket", RT60_BUCKETS),
        ("source_mic_distance_bucket", DISTANCE_BUCKETS),
        ("echo_zone", ECHO_ZONES),
    ]
    for col, allowed in checks:
        bad_sub = sorted(set(sub.loc[~sub[col].astype(str).isin(allowed), col].astype(str)))
        if bad_sub:
            raise InvalidSubmissionError(f"submission column {col} has invalid values: {bad_sub[:5]}")
        bad_ans = sorted(set(ans.loc[~ans[col].astype(str).isin(allowed), col].astype(str)))
        if bad_ans:
            raise ValueError(f"answers column {col} has invalid values: {bad_ans[:5]}")

    conf = pd.to_numeric(sub["confidence"], errors="coerce")
    true_conf = pd.to_numeric(ans["confidence"], errors="coerce")
    if conf.isna().any() or true_conf.isna().any():
        raise InvalidSubmissionError("confidence values must be numeric and non-missing")
    conf_arr = conf.to_numpy(dtype=float)
    true_conf_arr = true_conf.to_numpy(dtype=float)
    if not np.isfinite(conf_arr).all() or not np.isfinite(true_conf_arr).all():
        raise InvalidSubmissionError("confidence values must be finite")
    if (conf_arr < 0).any() or (conf_arr > 1).any() or (true_conf_arr < 0).any() or (true_conf_arr > 1).any():
        raise InvalidSubmissionError("confidence values must be in [0, 1]")
    sub["confidence"] = conf_arr
    ans["confidence"] = true_conf_arr

    sub = sub.set_index("sample_id").sort_index()
    ans = ans.set_index("sample_id").sort_index()
    return sub, ans


def _rows(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame:
    rows = ans.copy()
    rows["pred_room_volume_bucket"] = sub["room_volume_bucket"].astype(str)
    rows["pred_rt60_bucket"] = sub["rt60_bucket"].astype(str)
    rows["pred_source_mic_distance_bucket"] = sub["source_mic_distance_bucket"].astype(str)
    rows["pred_echo_zone"] = sub["echo_zone"].astype(str)
    rows["pred_confidence"] = sub["confidence"].astype(float)
    rows["confidence_score"] = np.maximum(0.0, 1.0 - np.abs(rows["pred_confidence"] - rows["confidence"].astype(float)) / 0.5)
    return rows


def _head_score(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    room = _macro_f1(rows["pred_room_volume_bucket"], rows["room_volume_bucket"]) ** 2
    rt60 = _macro_f1(rows["pred_rt60_bucket"], rows["rt60_bucket"]) ** 2
    distance = _macro_f1(rows["pred_source_mic_distance_bucket"], rows["source_mic_distance_bucket"]) ** 2
    echo = _macro_f1(rows["pred_echo_zone"], rows["echo_zone"]) ** 2
    confidence = float(rows["confidence_score"].mean()) ** 2
    return float(W_ROOM * room + W_RT60 * rt60 + W_DISTANCE * distance + W_ECHO * echo + W_CONFIDENCE * confidence)


def _profile_score(rows: pd.DataFrame) -> float:
    if W_HEADS_TOTAL <= 0:
        return 0.0
    return float(_head_score(rows) / W_HEADS_TOTAL)


def _worst_hidden_group(rows: pd.DataFrame) -> float:
    group_scores: list[float] = []
    for axis in HIDDEN_GROUP_AXES:
        if axis not in rows.columns:
            continue
        for _, group in rows.groupby(axis):
            if not group.empty:
                group_scores.append(_profile_score(group))
    if not group_scores:
        return _profile_score(rows)
    return float(min(group_scores))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    sub, ans = _validate_submission(submission, answers)
    rows = _rows(sub, ans)
    base = _head_score(rows)
    worst = _worst_hidden_group(rows)
    final = base + W_WORST_SUBGROUP * worst
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
