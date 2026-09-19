from __future__ import annotations

import math

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["id", "turn_state", "next_response_ms", "next_speaker_relation", "confidence"]
TURN_STATES = {"COMPLETE", "CONTINUE", "BACKCHANNEL", "OVERLAP", "UNCERTAIN"}
RELATIONS = {"SAME", "OTHER", "MULTI", "NONE_OR_UNCLEAR"}
MAX_RESPONSE_MS = 3000

W_STATE = 0.45
W_RELATION = 0.20
W_TIMING = 0.20
W_CALIBRATION = 0.10
W_JOINT = 0.05

W_MEAN = 0.70
W_MEETING_FAMILY = 0.15
W_TURN_TYPE = 0.15


def _latency_band(ms: float) -> str:
    if ms <= 250:
        return "immediate"
    if ms <= 800:
        return "fast"
    if ms <= 1500:
        return "medium"
    return "slow_or_unclear"


def _timing_tolerance(row: pd.Series) -> float:
    band = str(row.get("latency_band", "") or _latency_band(float(row["true_ms"])))
    if band == "immediate":
        return 300.0
    if band == "fast":
        return 500.0
    if band == "medium":
        return 850.0
    return 1200.0


def _validate_submission(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    if list(submission.columns) != REQUIRED_COLUMNS:
        return None
    needed_answers = {"id", "turn_state", "next_response_ms", "next_speaker_relation", "confidence"}
    if not needed_answers.issubset(set(answers.columns)):
        return None
    sub = submission.copy()
    ans = answers.copy()
    try:
        sub["id"] = sub["id"].astype(int)
        ans["id"] = ans["id"].astype(int)
    except (TypeError, ValueError):
        return None
    if sub["id"].duplicated().any() or ans["id"].duplicated().any():
        return None
    if set(sub["id"].tolist()) != set(ans["id"].tolist()):
        return None
    if (~sub["turn_state"].astype(str).isin(TURN_STATES)).any():
        return None
    if (~sub["next_speaker_relation"].astype(str).isin(RELATIONS)).any():
        return None

    pred_ms = pd.to_numeric(sub["next_response_ms"], errors="coerce")
    pred_conf = pd.to_numeric(sub["confidence"], errors="coerce")
    if pred_ms.isna().any() or pred_conf.isna().any():
        return None
    if not np.isfinite(pred_ms.to_numpy(dtype=float)).all() or not np.isfinite(pred_conf.to_numpy(dtype=float)).all():
        return None
    if (pred_ms < 0).any() or (pred_ms > MAX_RESPONSE_MS).any():
        return None
    if (np.abs(pred_ms - np.round(pred_ms)) > 1e-6).any():
        return None
    if (pred_conf < 0).any() or (pred_conf > 1).any():
        return None

    sub["next_response_ms"] = np.round(pred_ms).astype(int)
    sub["confidence"] = pred_conf.astype(float)
    return sub.set_index("id").sort_index(), ans.set_index("id").sort_index()


def _row_table(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame | None:
    rows = ans.copy()
    try:
        true_ms = pd.to_numeric(rows["next_response_ms"], errors="raise").astype(float)
        true_conf = pd.to_numeric(rows["confidence"], errors="raise").astype(float)
    except (TypeError, ValueError):
        return None
    if ((true_ms < 0) | (true_ms > MAX_RESPONSE_MS)).any():
        return None
    rows["true_ms"] = true_ms
    rows["true_conf"] = true_conf
    rows["pred_state"] = sub["turn_state"].astype(str)
    rows["pred_relation"] = sub["next_speaker_relation"].astype(str)
    rows["pred_ms"] = sub["next_response_ms"].astype(float)
    rows["pred_conf"] = sub["confidence"].astype(float)

    rows["state_correct"] = (rows["pred_state"] == rows["turn_state"].astype(str)).astype(float)
    rows["relation_correct"] = (rows["pred_relation"] == rows["next_speaker_relation"].astype(str)).astype(float)
    tolerances = rows.apply(_timing_tolerance, axis=1).astype(float)
    rows["timing_score"] = np.maximum(0.0, 1.0 - np.abs(rows["pred_ms"] - rows["true_ms"]) / tolerances)
    row_correctness = 0.50 * rows["state_correct"] + 0.25 * rows["relation_correct"] + 0.25 * rows["timing_score"]
    rows["calibration_score"] = np.maximum(0.0, 1.0 - np.abs(rows["pred_conf"] - row_correctness))
    rows["joint_correct"] = (
        (rows["state_correct"] == 1.0)
        & (rows["relation_correct"] == 1.0)
        & (np.abs(rows["pred_ms"] - rows["true_ms"]) <= 100.0)
    ).astype(float)
    return rows


def _component_score(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    state = float(rows["state_correct"].mean()) ** 2
    relation = float(rows["relation_correct"].mean()) ** 2
    timing = float(rows["timing_score"].mean()) ** 2
    calibration = float(rows["calibration_score"].mean()) ** 2
    joint = float(rows["joint_correct"].mean()) ** 2
    return float(
        W_STATE * state
        + W_RELATION * relation
        + W_TIMING * timing
        + W_CALIBRATION * calibration
        + W_JOINT * joint
    )


def _worst_group_score(rows: pd.DataFrame, axis: str) -> float:
    if axis not in rows.columns:
        return _component_score(rows)
    scores = [_component_score(group) for _, group in rows.groupby(axis)]
    if not scores:
        return 0.0
    return float(min(scores))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        checked = _validate_submission(submission, answers)
        if checked is None:
            return 0.0
        sub, ans = checked
        rows = _row_table(sub, ans)
        if rows is None or rows.empty:
            return 0.0
        mean_score = _component_score(rows)
        worst_meeting = _worst_group_score(rows, "meeting_family")
        worst_turn = _worst_group_score(rows, "turn_type_bucket")
        final = W_MEAN * mean_score + W_MEETING_FAMILY * worst_meeting + W_TURN_TYPE * worst_turn
        if not math.isfinite(final):
            return 0.0
        return float(np.clip(final, 0.0, 1.0))
    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--answers", type=Path, required=True)
    args = parser.parse_args()
    print(grade(pd.read_csv(args.submission), pd.read_csv(args.answers)))
