"""Strict, label-invariant scorer for Lightning Flash Hierarchy Induction."""

from __future__ import annotations

import json
import math
from itertools import combinations

import numpy as np
import pandas as pd


SUBMISSION_COLUMNS = ["id", "prediction_json", "confidence"]
REQUIRED_ANSWER_COLUMNS = {"id", "target_json"}
MAX_JSON_LEN = 200_000
MAX_DETECTIONS = 40
MAX_GROUPS = 40
MAX_FLASHES = 40

W_GROUP = 0.55
W_FLASH = 0.10
W_UNCERTAIN = 0.15
W_EXACT = 0.15
W_CALIBRATION = 0.05


class InvalidSubmissionError(ValueError):
    """Raised for submission-level contract violations."""


def _pairs(parts: list[frozenset[str]]) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for part in parts:
        for a, b in combinations(sorted(part), 2):
            out.add((a, b))
    return out


def _f1(pred: set, gold: set) -> float:
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    tp = len(pred & gold)
    return float(2.0 * tp / (len(pred) + len(gold)))


def _count_similarity(pred_count: int, gold_count: int) -> float:
    if pred_count <= 0 or gold_count <= 0:
        return 0.0
    return float(min(pred_count, gold_count) / max(pred_count, gold_count))


def _canonical(parts: list[frozenset[str]]) -> frozenset[frozenset[str]]:
    return frozenset(parts)


def _parse_hierarchy(cell: object, expected_ids: set[str] | None = None):
    if not isinstance(cell, str) or len(cell) > MAX_JSON_LEN:
        return None
    try:
        obj = json.loads(cell)
    except (TypeError, ValueError, json.JSONDecodeError, OverflowError, RecursionError):
        return None
    if not isinstance(obj, dict) or set(obj) != {"groups", "flashes", "uncertain_detections"}:
        return None
    groups = obj["groups"]
    flashes = obj["flashes"]
    uncertain = obj["uncertain_detections"]
    if not isinstance(groups, list) or not isinstance(flashes, list) or not isinstance(uncertain, list):
        return None
    if not (1 <= len(groups) <= MAX_GROUPS and 1 <= len(flashes) <= MAX_FLASHES):
        return None
    if len(uncertain) > MAX_DETECTIONS:
        return None

    group_ids: set[str] = set()
    group_parts: list[frozenset[str]] = []
    detection_to_group: dict[str, str] = {}
    for item in groups:
        if not isinstance(item, dict) or set(item) != {"group_id", "detections"}:
            return None
        gid, members = item["group_id"], item["detections"]
        if not isinstance(gid, str) or not gid or len(gid) > 80 or gid in group_ids:
            return None
        if not isinstance(members, list) or not members or len(members) > MAX_DETECTIONS:
            return None
        if any(not isinstance(d, str) or not d or len(d) > 80 for d in members):
            return None
        if len(set(members)) != len(members):
            return None
        if any(d in detection_to_group for d in members):
            return None
        group_ids.add(gid)
        for d in members:
            detection_to_group[d] = gid
        group_parts.append(frozenset(members))

    all_detections = set(detection_to_group)
    if len(all_detections) > MAX_DETECTIONS:
        return None
    if expected_ids is not None and all_detections != expected_ids:
        return None

    flash_ids: set[str] = set()
    seen_groups: set[str] = set()
    flash_group_parts: list[frozenset[str]] = []
    group_to_flash: dict[str, str] = {}
    for item in flashes:
        if not isinstance(item, dict) or set(item) != {"flash_id", "groups"}:
            return None
        fid, members = item["flash_id"], item["groups"]
        if not isinstance(fid, str) or not fid or len(fid) > 80 or fid in flash_ids:
            return None
        if not isinstance(members, list) or not members or len(members) > MAX_GROUPS:
            return None
        if any(not isinstance(g, str) or g not in group_ids for g in members):
            return None
        if len(set(members)) != len(members) or any(g in seen_groups for g in members):
            return None
        flash_ids.add(fid)
        for g in members:
            seen_groups.add(g)
            group_to_flash[g] = fid
        flash_group_parts.append(frozenset(members))
    if seen_groups != group_ids:
        return None

    if any(not isinstance(d, str) or d not in all_detections for d in uncertain):
        return None
    if len(set(uncertain)) != len(uncertain):
        return None

    flash_detection_parts: dict[str, set[str]] = {}
    for d, gid in detection_to_group.items():
        flash_detection_parts.setdefault(group_to_flash[gid], set()).add(d)

    return {
        "detections": all_detections,
        "groups": group_parts,
        "flashes": [frozenset(v) for v in flash_detection_parts.values()],
        "uncertain": set(uncertain),
        "group_flash_partition": flash_group_parts,
    }


def _score_row(pred, gold, confidence: float) -> tuple[float, dict[str, float]]:
    group_pair_f1 = _f1(_pairs(pred["groups"]), _pairs(gold["groups"]))
    flash_pair_f1 = _f1(_pairs(pred["flashes"]), _pairs(gold["flashes"]))
    group_count = _count_similarity(len(pred["groups"]), len(gold["groups"]))
    flash_count = _count_similarity(len(pred["flashes"]), len(gold["flashes"]))
    group_f1 = group_pair_f1 * group_count
    flash_f1 = flash_pair_f1 * flash_count
    uncertain_f1 = _f1(pred["uncertain"], gold["uncertain"])
    exact = float(
        _canonical(pred["groups"]) == _canonical(gold["groups"])
        and _canonical(pred["flashes"]) == _canonical(gold["flashes"])
        and pred["uncertain"] == gold["uncertain"]
    )
    structural = (
        W_GROUP * group_f1
        + W_FLASH * flash_f1
        + W_UNCERTAIN * uncertain_f1
        + W_EXACT * exact
    ) / (W_GROUP + W_FLASH + W_UNCERTAIN + W_EXACT)
    calibration = 1.0 - abs(confidence - structural)
    score = (
        W_GROUP * group_f1
        + W_FLASH * flash_f1
        + W_UNCERTAIN * uncertain_f1
        + W_EXACT * exact
        + W_CALIBRATION * calibration
    )
    return float(score), {
        "group_pair_f1": group_f1,
        "flash_pair_f1": flash_f1,
        "group_raw_pair_f1": group_pair_f1,
        "flash_raw_pair_f1": flash_pair_f1,
        "group_count_similarity": group_count,
        "flash_count_similarity": flash_count,
        "uncertain_f1": uncertain_f1,
        "exact": exact,
        "calibration": calibration,
    }


def _validate_submission(submission: pd.DataFrame, answers: pd.DataFrame) -> pd.DataFrame:
    if list(submission.columns) != SUBMISSION_COLUMNS:
        raise InvalidSubmissionError(
            "Submission columns must be exactly id,prediction_json,confidence in that order."
        )
    if not REQUIRED_ANSWER_COLUMNS.issubset(answers.columns):
        raise InvalidSubmissionError("Private answers do not contain the required schema.")
    if submission.empty:
        raise InvalidSubmissionError("Submission must not be empty.")
    ids = submission["id"]
    if ids.isna().any() or any(not isinstance(x, str) or not x for x in ids):
        raise InvalidSubmissionError("Every id must be a non-empty string.")
    if ids.duplicated().any():
        raise InvalidSubmissionError("Submission contains duplicate ids.")
    answer_ids = answers["id"]
    if answer_ids.isna().any() or answer_ids.duplicated().any():
        raise InvalidSubmissionError("Private answer ids are invalid.")
    if set(ids) != set(answer_ids) or len(ids) != len(answer_ids):
        raise InvalidSubmissionError("Submission ids must exactly match the test id set.")

    confidence = pd.to_numeric(submission["confidence"], errors="coerce").to_numpy(dtype=float)
    if not np.isfinite(confidence).all() or np.any(confidence < 0.0) or np.any(confidence > 1.0):
        raise InvalidSubmissionError("confidence must contain finite values in [0,1].")
    aligned = answers.merge(submission, on="id", how="left", validate="one_to_one", sort=True)
    aligned["confidence"] = pd.to_numeric(aligned["confidence"], errors="raise").astype(float)
    return aligned


def score_details(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[float, pd.DataFrame]:
    """Return the official score and row/head details used by local checks."""
    aligned = _validate_submission(submission.copy(), answers.copy())
    rows = []
    for row in aligned.itertuples(index=False):
        gold = _parse_hierarchy(row.target_json)
        if gold is None:
            raise InvalidSubmissionError("Private answers contain malformed target_json.")
        pred = _parse_hierarchy(row.prediction_json, gold["detections"])
        if pred is None:
            rows.append({
                "id": row.id,
                "row_score": 0.0,
                "group_pair_f1": 0.0,
                "flash_pair_f1": 0.0,
                "uncertain_f1": 0.0,
                "exact": 0.0,
                "calibration": 0.0,
            })
            continue
        value, heads = _score_row(pred, gold, float(row.confidence))
        rows.append({"id": row.id, "row_score": value, **heads})
    details = pd.DataFrame(rows)
    if details.empty or not np.isfinite(details["row_score"]).all():
        raise InvalidSubmissionError("No finite rows were scored.")
    score = float(details["row_score"].mean())
    if not math.isfinite(score) or score < 0.0 or score > 1.0:
        raise InvalidSubmissionError("Computed score is outside [0,1].")
    return score, details


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Platform entry point."""
    try:
        score, _ = score_details(submission, answers)
        return float(np.clip(score, 0.0, 1.0))
    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", required=True, type=Path)
    ap.add_argument("--answers", required=True, type=Path)
    args = ap.parse_args()
    print(f"score={grade(pd.read_csv(args.submission), pd.read_csv(args.answers)):.6f}")
