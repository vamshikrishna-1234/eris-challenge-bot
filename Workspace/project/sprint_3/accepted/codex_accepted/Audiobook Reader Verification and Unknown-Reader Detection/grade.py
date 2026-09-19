from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


SUBMISSION_COLUMNS = ["id", "verdict_json"]
ANSWER_COLUMNS = [
    "id",
    "verdict_json",
    "is_known_reader",
    "provenance",
    "reader_group",
    "source_split",
    "chapter_group",
    "sex_group",
    "duration_bucket",
]

MAX_JSON_LEN = 256
W_STRICT_ROW = 0.41
W_WORST_STRICT = 0.20
W_PROVENANCE = 0.10
W_KNOWNNESS = 0.10
W_READER_CONSISTENCY = 0.05
W_CALIBRATION = 0.14
GROUP_AXES = ["source_split", "sex_group", "duration_bucket"]
ERROR_COST = 14.0


class InvalidSubmissionError(ValueError):
    pass


class HardInvalid(InvalidSubmissionError):
    pass


@dataclass
class ParsedVerdict:
    known_reader_score: float
    known_score_valid: bool
    provenance: str
    provenance_valid: bool
    confidence: float
    row_valid: bool


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lstrip("\ufeff") for c in out.columns]
    return out


def _parse_float(value: Any) -> float | None:
    try:
        x = float(value)
    except Exception:
        return None
    if not math.isfinite(x):
        return None
    return x


def _valid_provenance(value: str) -> bool:
    return value == "UNKNOWN" or re.fullmatch(r"reader_\d{3}", value) is not None


def _parse_verdict(value: Any) -> ParsedVerdict:
    text = str(value)
    if len(text) > MAX_JSON_LEN:
        return ParsedVerdict(0.5, False, "__INVALID__", False, 0.0, False)
    try:
        payload = json.loads(text)
    except Exception:
        return ParsedVerdict(0.5, False, "__INVALID__", False, 0.0, False)
    if not isinstance(payload, dict) or set(payload.keys()) != {"known_reader_score", "provenance", "confidence"}:
        return ParsedVerdict(0.5, False, "__INVALID__", False, 0.0, False)
    known_score = _parse_float(payload.get("known_reader_score"))
    known_valid = known_score is not None and 0.0 <= known_score <= 1.0
    if not known_valid:
        known_score = 0.5
    provenance = str(payload.get("provenance"))
    provenance_valid = _valid_provenance(provenance)
    if not provenance_valid:
        provenance = "__INVALID__"
    confidence = _parse_float(payload.get("confidence"))
    if confidence is None or confidence < 0.0 or confidence > 1.0:
        raise HardInvalid("confidence must be finite and in [0, 1]")
    row_valid = bool(known_valid and provenance_valid)
    return ParsedVerdict(float(known_score), bool(known_valid), provenance, bool(provenance_valid), float(confidence), row_valid)


def _validate(submission: pd.DataFrame, answers: pd.DataFrame) -> pd.DataFrame:
    sub = _clean_columns(submission).reset_index(drop=True)
    ans = _clean_columns(answers).reset_index(drop=True)
    if list(sub.columns) != SUBMISSION_COLUMNS:
        raise HardInvalid("submission columns are wrong, missing, extra, or reordered")
    if any(col not in ans.columns for col in ANSWER_COLUMNS):
        raise ValueError("answers file is missing required columns")
    sub["id"] = sub["id"].astype(str)
    ans["id"] = ans["id"].astype(str)
    if sub["id"].duplicated().any() or ans["id"].duplicated().any():
        raise HardInvalid("duplicate ids")
    if set(sub["id"]) != set(ans["id"]):
        raise HardInvalid("submission id set does not match answers")
    if sub["verdict_json"].isna().any():
        raise HardInvalid("verdict_json contains missing values")
    rows = ans.merge(sub, on="id", how="left", validate="one_to_one", suffixes=("_true", "_pred"))
    if rows["verdict_json_pred"].isna().any():
        raise HardInvalid("missing predictions after alignment")
    return rows


def _rank_auc_skill(scores: np.ndarray, labels: np.ndarray, valid: np.ndarray) -> float:
    labels = labels.astype(int)
    scores = scores.astype(float)
    if scores.size == 0:
        return 0.0
    n_pos = int(labels.sum())
    n_neg = int(labels.size - n_pos)
    if n_pos == 0 or n_neg == 0:
        return 0.0
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty_like(scores, dtype=float)
    i = 0
    while i < len(scores):
        j = i + 1
        while j < len(scores) and sorted_scores[j] == sorted_scores[i]:
            j += 1
        ranks[order[i:j]] = (i + j - 1) / 2.0
        i = j
    auc = (float(ranks[labels == 1].sum()) - n_pos * (n_pos - 1) / 2.0) / float(n_pos * n_neg)
    return float(max(0.0, 2.0 * auc - 1.0) * valid.astype(float).mean())


def _macro_f1(pred: np.ndarray, true: np.ndarray, valid: np.ndarray) -> float:
    pred = pred.astype(str)
    true = true.astype(str)
    pred = np.where(valid, pred, "__INVALID__")
    labels = sorted(set(true.tolist()))
    if not labels:
        return 0.0
    f1s = []
    for label in labels:
        tp = int(np.sum((pred == label) & (true == label)))
        fp = int(np.sum((pred == label) & (true != label)))
        fn = int(np.sum((pred != label) & (true == label)))
        if tp + fp == 0 and tp + fn == 0:
            f1s.append(1.0)
        elif tp == 0:
            f1s.append(0.0)
        else:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s))


def _row_core(rows: pd.DataFrame) -> np.ndarray:
    known = rows["is_known_reader"].astype(float).to_numpy()
    score = rows["pred_known_score"].astype(float).to_numpy()
    known_quality = np.maximum(0.0, 1.0 - np.abs(score - known)) * rows["known_score_valid"].astype(float).to_numpy()
    prov_quality = (rows["pred_provenance"].astype(str).to_numpy() == rows["provenance"].astype(str).to_numpy()).astype(float)
    prov_quality *= rows["provenance_valid"].astype(float).to_numpy()
    return 0.50 * known_quality + 0.50 * prov_quality


def _row_exact(rows: pd.DataFrame) -> np.ndarray:
    known = rows["is_known_reader"].astype(int).to_numpy()
    score = rows["pred_known_score"].astype(float).to_numpy()
    known_side = (score >= 0.5).astype(int) == known
    provenance_exact = rows["pred_provenance"].astype(str).to_numpy() == rows["provenance"].astype(str).to_numpy()
    valid = rows["known_score_valid"].astype(bool).to_numpy() & rows["provenance_valid"].astype(bool).to_numpy()
    return (known_side & provenance_exact & valid).astype(float)


def _penalized_accuracy(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    acc = float(np.mean(values.astype(float)))
    return float(max(0.0, 1.0 - ERROR_COST * (1.0 - acc)))


def _strict_row_score(rows: pd.DataFrame) -> float:
    return _penalized_accuracy(_row_exact(rows))


def _worst_strict_group(rows: pd.DataFrame) -> float:
    rows = rows.copy()
    rows["_exact"] = _row_exact(rows)
    vals = []
    for axis in GROUP_AXES:
        if axis not in rows.columns:
            continue
        for _, group in rows.groupby(axis):
            if not group.empty:
                vals.append(_penalized_accuracy(group["_exact"].to_numpy(dtype=float)))
    if not vals:
        return _penalized_accuracy(rows["_exact"].to_numpy(dtype=float)) if not rows.empty else 0.0
    return float(min(vals))


def _reader_consistency(rows: pd.DataFrame) -> float:
    vals = []
    for _, group in rows.groupby("reader_group"):
        if len(group) < 2:
            continue
        true = str(group["provenance"].iloc[0])
        pred = group["pred_provenance"].astype(str).to_numpy()
        valid = group["provenance_valid"].astype(bool).to_numpy()
        vals.append(float(np.mean((pred == true) & valid)))
    if not vals:
        return float(np.mean(_row_core(rows))) if not rows.empty else 0.0
    return float(np.mean(vals))


def _worst_group(rows: pd.DataFrame) -> float:
    rows = rows.copy()
    rows["_core"] = _row_core(rows)
    vals = []
    for axis in GROUP_AXES:
        if axis not in rows.columns:
            continue
        for _, group in rows.groupby(axis):
            if not group.empty:
                vals.append(float(group["_core"].mean()))
    if not vals:
        return float(rows["_core"].mean()) if not rows.empty else 0.0
    return float(min(vals))


def _calibration(rows: pd.DataFrame) -> float:
    core = _row_core(rows)
    conf = rows["pred_confidence"].astype(float).to_numpy()
    valid = rows["row_valid"].astype(float).to_numpy()
    return float(np.mean(np.maximum(0.0, 1.0 - np.abs(conf - core)) * valid)) if core.size else 0.0


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        rows = _validate(submission, answers)
        parsed = [_parse_verdict(v) for v in rows["verdict_json_pred"].tolist()]
        rows = rows.copy()
        rows["pred_known_score"] = [p.known_reader_score for p in parsed]
        rows["known_score_valid"] = [p.known_score_valid for p in parsed]
        rows["pred_provenance"] = [p.provenance for p in parsed]
        rows["provenance_valid"] = [p.provenance_valid for p in parsed]
        rows["pred_confidence"] = [p.confidence for p in parsed]
        rows["row_valid"] = [p.row_valid for p in parsed]
        knownness = _rank_auc_skill(
            rows["pred_known_score"].to_numpy(dtype=float),
            rows["is_known_reader"].astype(int).to_numpy(),
            rows["known_score_valid"].to_numpy(dtype=bool),
        )
        provenance = _macro_f1(
            rows["pred_provenance"].astype(str).to_numpy(),
            rows["provenance"].astype(str).to_numpy(),
            rows["provenance_valid"].to_numpy(dtype=bool),
        )
        consistency = _reader_consistency(rows)
        strict = _strict_row_score(rows)
        worst_strict = _worst_strict_group(rows)
        calibration = _calibration(rows)
        final = (
            W_STRICT_ROW * strict
            + W_WORST_STRICT * worst_strict
            + W_PROVENANCE * provenance
            + W_KNOWNNESS * knownness
            + W_READER_CONSISTENCY * consistency
            + W_CALIBRATION * calibration
        )
        if not math.isfinite(final):
            return 0.0
        if abs(final - 1.0) < 1e-12:
            return 1.0
        return float(np.clip(final, 0.0, 1.0))
    except InvalidSubmissionError:
        raise
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
