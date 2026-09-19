from __future__ import annotations

import math
import re
from typing import Any

import numpy as np
import pandas as pd


SUBMISSION_COLUMNS = ["id", "reparandum_span", "interregnum_span", "repair_onset", "is_disfluency", "confidence"]
ANSWER_REQUIRED_COLUMNS = [
    "id",
    "reparandum_span",
    "interregnum_span",
    "repair_onset",
    "is_disfluency",
    "confidence",
    "token_count",
    "source_group",
    "repair_group",
]
MAX_CELL_CHARS = 64


class MalformedSpan:
    pass


BAD_SPAN = MalformedSpan()


def _parse_span_cell(value: Any, token_count: int) -> tuple[int, int] | None | MalformedSpan:
    text = str(value).strip()
    if len(text) > MAX_CELL_CHARS:
        return BAD_SPAN
    if text == "NONE":
        return None
    match = re.fullmatch(r"\[(\d+),(\d+)\]", text)
    if not match:
        return BAD_SPAN
    start, end = int(match.group(1)), int(match.group(2))
    if start > end or start < 0 or end >= token_count:
        raise ValueError("span out of range")
    return (start, end)


def _parse_onset_cell(value: Any, token_count: int) -> int | None:
    text = str(value).strip()
    if len(text) > MAX_CELL_CHARS:
        raise ValueError("repair_onset too long")
    if text == "NONE":
        return None
    if not re.fullmatch(r"\d+", text):
        raise ValueError("repair_onset must be an integer string or NONE")
    idx = int(text)
    if idx < 0 or idx >= token_count:
        raise ValueError("repair_onset out of range")
    return idx


def _span_iou(pred: tuple[int, int] | None | MalformedSpan, gold: tuple[int, int] | None) -> float:
    if pred is BAD_SPAN:
        return 0.0
    if pred is None and gold is None:
        return 1.0
    if pred is None or gold is None:
        return 0.0
    ps, pe = pred
    gs, ge = gold
    inter = max(0, min(pe, ge) - max(ps, gs) + 1)
    union = max(pe, ge) - min(ps, gs) + 1
    if union <= 0:
        return 0.0
    return float(inter / union)


def _parse_is_disfluency(value: Any) -> int:
    text = str(value).strip()
    if text not in {"0", "1"}:
        if re.fullmatch(r"[01]\.0+", text):
            text = text[0]
        else:
            raise ValueError("is_disfluency must be 0 or 1")
    return int(text)


def _parse_confidence(value: Any) -> float:
    x = float(value)
    if not math.isfinite(x) or x < 0.0 or x > 1.0:
        raise ValueError("confidence must be finite in [0, 1]")
    return x


def _row_scores(aligned: pd.DataFrame) -> np.ndarray:
    scores = []
    for _, row in aligned.iterrows():
        token_count = int(row["token_count"])
        true_rep = _parse_span_cell(row["reparandum_span_true"], token_count)
        true_int = _parse_span_cell(row["interregnum_span_true"], token_count)
        if true_rep is BAD_SPAN or true_int is BAD_SPAN:
            raise ValueError("answers contain malformed spans")
        pred_rep = _parse_span_cell(row["reparandum_span_pred"], token_count)
        pred_int = _parse_span_cell(row["interregnum_span_pred"], token_count)
        true_onset = _parse_onset_cell(row["repair_onset_true"], token_count)
        pred_onset = _parse_onset_cell(row["repair_onset_pred"], token_count)
        true_is = _parse_is_disfluency(row["is_disfluency_true"])
        pred_is = _parse_is_disfluency(row["is_disfluency_pred"])
        conf = _parse_confidence(row["confidence_pred"])

        s_is = 1.0 if pred_is == true_is else 0.0
        if true_is == 1 and pred_is == 0:
            s_rep = 0.0
            s_int = 0.0
            s_onset = 0.0
        else:
            s_rep = _span_iou(pred_rep, true_rep)  # type: ignore[arg-type]
            s_int = _span_iou(pred_int, true_int)  # type: ignore[arg-type]
            s_onset = 1.0 if pred_onset == true_onset else 0.0
        core_mean = (s_rep + s_int + s_onset + s_is) / 4.0
        s_cal = max(0.0, 1.0 - abs(conf - core_mean))
        s_joint = 1.0 if (s_rep == 1.0 and s_int == 1.0 and s_onset == 1.0 and s_is == 1.0) else 0.0
        row_score = (
            0.70 * s_joint
            + 0.10 * (s_rep**2)
            + 0.05 * (s_int**2)
            + 0.03 * (s_onset**2)
            + 0.07 * (s_is**2)
            + 0.05 * (s_cal**2)
        )
        scores.append(row_score)
    return np.asarray(scores, dtype=np.float64)


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        if list(submission.columns) != SUBMISSION_COLUMNS:
            return 0.0
        if any(col not in answers.columns for col in ANSWER_REQUIRED_COLUMNS):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        sub["id"] = sub["id"].astype(str)
        ans["id"] = ans["id"].astype(str)
        if sub["id"].duplicated().any() or ans["id"].duplicated().any():
            return 0.0
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            return 0.0

        for col in ["confidence", "is_disfluency", "reparandum_span", "interregnum_span", "repair_onset"]:
            if sub[col].isna().any():
                return 0.0
        try:
            confs = sub["confidence"].map(_parse_confidence)
            _ = confs.to_numpy(dtype=float)
            _ = sub["is_disfluency"].map(_parse_is_disfluency)
        except Exception:
            return 0.0

        aligned = ans.merge(sub, on="id", how="left", suffixes=("_true", "_pred"), validate="one_to_one")
        row_scores = _row_scores(aligned)
        if row_scores.size == 0 or not np.isfinite(row_scores).all():
            return 0.0
        aligned = aligned.copy()
        aligned["_row_score"] = row_scores
        mean_score = float(np.mean(row_scores))
        source_worst = float(aligned.groupby("source_group")["_row_score"].mean().min())
        repair_worst = float(aligned.groupby("repair_group")["_row_score"].mean().min())
        disfluent_rows = aligned[aligned["is_disfluency_true"].astype(int) == 1]
        if disfluent_rows.empty:
            return 0.0
        disfluent_mean = float(disfluent_rows["_row_score"].mean())
        final = 0.45 * mean_score + 0.15 * source_worst + 0.25 * repair_worst + 0.15 * disfluent_mean
        return float(np.clip(final, 0.0, 1.0))
    except Exception:
        return 0.0
