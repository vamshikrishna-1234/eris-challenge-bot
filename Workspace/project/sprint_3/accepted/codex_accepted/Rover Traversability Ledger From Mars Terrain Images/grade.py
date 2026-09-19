"""Strict grader for Rover Traversability Ledger From Mars Terrain Images."""

from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd


class InvalidSubmissionError(Exception):
    """Raised for structural submission errors that prevent safe row alignment."""


MASK_SIZE = 32
MASK_VALUES = {0, 1, 2, 3, 255}
BOX_KINDS = {"big_rock", "unknown"}
ROUTE_CLASSES = {"safe_to_drive", "drive_slowly", "avoid_area", "uncertain"}
MAX_MASK_JSON_LEN = 20_000
MAX_BOX_JSON_LEN = 10_000
MAX_BOXES = 8
SUBMISSION_COLUMNS = [
    "id",
    "terrain_mask_rle",
    "hazard_boxes_json",
    "route_safety_class",
    "clearance_score",
    "obstacle_coverage",
    "safe_corridor_width",
    "uncertainty_score",
]

W_MASK = 0.34
W_BOXES = 0.14
W_ROUTE = 0.15
W_CLEARANCE = 0.10
W_OBSTACLE = 0.10
W_WIDTH = 0.09
W_UNCERTAINTY = 0.08

W_MEAN = 0.76
W_MISSION = 0.10
W_TERRAIN = 0.08
W_ROUTE_GROUP = 0.06


def _text(cell, max_len: int) -> str | None:
    if cell is None:
        return None
    if isinstance(cell, float) and not np.isfinite(cell):
        return None
    value = str(cell).strip()
    if not value or len(value) > max_len or value.lower() in {"nan", "none"}:
        return None
    return value


def _parse_mask(cell) -> np.ndarray | None:
    value = _text(cell, MAX_MASK_JSON_LEN)
    if value is None:
        return None
    try:
        data = json.loads(value)
    except (json.JSONDecodeError, TypeError, ValueError, OverflowError):
        return None
    if not isinstance(data, dict) or set(data) != {"shape", "counts"}:
        return None
    if data["shape"] != [MASK_SIZE, MASK_SIZE] or not isinstance(data["counts"], list):
        return None
    if not (1 <= len(data["counts"]) <= MASK_SIZE * MASK_SIZE):
        return None
    out: list[int] = []
    for pair in data["counts"]:
        if not isinstance(pair, list) or len(pair) != 2:
            return None
        raw_value, raw_length = pair
        if isinstance(raw_value, bool) or isinstance(raw_length, bool):
            return None
        try:
            label = int(raw_value)
            length = int(raw_length)
        except (TypeError, ValueError, OverflowError):
            return None
        if label not in MASK_VALUES or length <= 0 or length > MASK_SIZE * MASK_SIZE:
            return None
        if float(raw_value) != label or float(raw_length) != length:
            return None
        if len(out) + length > MASK_SIZE * MASK_SIZE:
            return None
        out.extend([label] * length)
    if len(out) != MASK_SIZE * MASK_SIZE:
        return None
    return np.asarray(out, dtype=np.uint8).reshape(MASK_SIZE, MASK_SIZE)


def _finite_01(value) -> float | None:
    # No confidence column is scored; every numeric route field is still guarded by np.isfinite.
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if not np.isfinite(number) or number < 0.0 or number > 1.0:
        return None
    return number


def _parse_boxes(cell) -> list[dict[str, float | str]] | None:
    value = _text(cell, MAX_BOX_JSON_LEN)
    if value is None:
        return None
    try:
        data = json.loads(value)
    except (json.JSONDecodeError, TypeError, ValueError, OverflowError):
        return None
    if not isinstance(data, list) or len(data) > MAX_BOXES:
        return None
    result: list[dict[str, float | str]] = []
    for item in data:
        if not isinstance(item, dict) or set(item) != {"kind", "x", "y", "w", "h"}:
            return None
        kind = str(item["kind"]).strip().lower()
        x = _finite_01(item["x"])
        y = _finite_01(item["y"])
        width = _finite_01(item["w"])
        height = _finite_01(item["h"])
        if kind not in BOX_KINDS or None in {x, y, width, height}:
            return None
        assert x is not None and y is not None and width is not None and height is not None
        if width <= 0.0 or height <= 0.0 or x + width > 1.000001 or y + height > 1.000001:
            return None
        result.append({"kind": kind, "x": x, "y": y, "w": width, "h": height})
    return result


def _mask_miou(pred: np.ndarray | None, true: np.ndarray | None) -> float:
    if pred is None or true is None:
        return 0.0
    scores = []
    for label in [0, 1, 2, 3, 255]:
        p = pred == label
        t = true == label
        union = int(np.logical_or(p, t).sum())
        if union:
            scores.append(float(np.logical_and(p, t).sum()) / union)
    return float(np.mean(scores)) if scores else 1.0


def _iou(a: dict[str, float | str], b: dict[str, float | str]) -> float:
    ax0, ay0 = float(a["x"]), float(a["y"])
    ax1, ay1 = ax0 + float(a["w"]), ay0 + float(a["h"])
    bx0, by0 = float(b["x"]), float(b["y"])
    bx1, by1 = bx0 + float(b["w"]), by0 + float(b["h"])
    iw = max(0.0, min(ax1, bx1) - max(ax0, bx0))
    ih = max(0.0, min(ay1, by1) - max(ay0, by0))
    intersection = iw * ih
    union = (ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - intersection
    return intersection / union if union > 0 else 0.0


def _box_score(
    pred: list[dict[str, float | str]] | None,
    true: list[dict[str, float | str]] | None,
) -> float:
    if pred is None or true is None:
        return 0.0
    if not pred and not true:
        return 1.0
    if not pred or not true:
        return 0.0
    candidates = []
    for pi, pbox in enumerate(pred):
        for ti, tbox in enumerate(true):
            if pbox["kind"] == tbox["kind"]:
                overlap = _iou(pbox, tbox)
                if overlap >= 0.30:
                    candidates.append((overlap, pi, ti))
    used_p: set[int] = set()
    used_t: set[int] = set()
    credit = 0.0
    for overlap, pi, ti in sorted(candidates, reverse=True):
        if pi not in used_p and ti not in used_t:
            used_p.add(pi)
            used_t.add(ti)
            credit += overlap
    return float(np.clip(2.0 * credit / (len(pred) + len(true)), 0.0, 1.0))


def _numeric_score(pred: float, true: float, tau: float) -> float:
    return float(math.exp(-abs(pred - true) / tau))


def _worst_group(scores: list[float], values: list[str] | None) -> float | None:
    if values is None:
        return None
    buckets: dict[str, list[float]] = {}
    for score, value in zip(scores, values):
        buckets.setdefault(str(value), []).append(score)
    return min(float(np.mean(bucket)) for bucket in buckets.values()) if buckets else None


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        raw_columns = list(submission.columns)
        clean_columns = [str(col).strip().lstrip("\ufeff") for col in raw_columns]
        if clean_columns != SUBMISSION_COLUMNS:
            raise InvalidSubmissionError("submission columns do not match the required schema")
        required_answers = set(SUBMISSION_COLUMNS)
        if not required_answers.issubset(answers.columns):
            raise InvalidSubmissionError("answers file is missing required columns")
        sub = submission.copy()
        sub.columns = clean_columns
        ans = answers.copy()
        sub["id"] = sub["id"].astype(str).str.strip()
        ans["id"] = ans["id"].astype(str).str.strip()
        if sub["id"].eq("").any() or ans["id"].eq("").any():
            raise InvalidSubmissionError("blank id values are not allowed")
        if sub["id"].duplicated().any() or ans["id"].duplicated().any():
            raise InvalidSubmissionError("duplicate id values are not allowed")
        if len(sub) != len(ans) or set(sub["id"]) != set(ans["id"]):
            raise InvalidSubmissionError("submission ids must exactly match answer ids")

        numeric_columns = [
            "clearance_score",
            "obstacle_coverage",
            "safe_corridor_width",
            "uncertainty_score",
        ]
        parsed_numeric: dict[str, dict[str, float]] = {name: {} for name in numeric_columns}
        for _, row in sub.iterrows():
            rid = str(row["id"])
            for name in numeric_columns:
                value = _finite_01(row[name])
                if value is None:
                    raise InvalidSubmissionError(f"{name} must be finite and in [0,1]")
                parsed_numeric[name][rid] = value

        sub_by_id = {str(row["id"]): row for _, row in sub.iterrows()}
        row_scores: list[float] = []
        mission_values: list[str] = []
        terrain_values: list[str] = []
        route_values: list[str] = []
        for _, truth in ans.iterrows():
            rid = str(truth["id"])
            pred = sub_by_id[rid]
            if "mission_group" in ans.columns:
                mission_values.append(str(truth["mission_group"]))
            if "terrain_group" in ans.columns:
                terrain_values.append(str(truth["terrain_group"]))
            if "route_group" in ans.columns:
                route_values.append(str(truth["route_group"]))

            pred_mask = _parse_mask(pred["terrain_mask_rle"])
            true_mask = _parse_mask(truth["terrain_mask_rle"])
            pred_boxes = _parse_boxes(pred["hazard_boxes_json"])
            true_boxes = _parse_boxes(truth["hazard_boxes_json"])
            pred_route = str(pred["route_safety_class"]).strip().lower()
            true_route = str(truth["route_safety_class"]).strip().lower()

            # Row-local prediction fields are intentionally strict: malformed
            # JSON, invalid masks/boxes, or an invalid route label zero this
            # row rather than allowing solvers to farm numeric or easy heads
            # while sending unusable structured evidence.
            if pred_mask is None or pred_boxes is None or pred_route not in ROUTE_CLASSES:
                row_scores.append(0.0)
                continue

            s_mask = _mask_miou(pred_mask, true_mask)
            s_boxes = _box_score(pred_boxes, true_boxes)
            s_route = 1.0 if pred_route == true_route else 0.0
            s_clear = _numeric_score(parsed_numeric["clearance_score"][rid], float(truth["clearance_score"]), 0.14)
            s_obstacle = _numeric_score(parsed_numeric["obstacle_coverage"][rid], float(truth["obstacle_coverage"]), 0.07)
            s_width = _numeric_score(parsed_numeric["safe_corridor_width"][rid], float(truth["safe_corridor_width"]), 0.14)
            s_uncertainty = _numeric_score(parsed_numeric["uncertainty_score"][rid], float(truth["uncertainty_score"]), 0.14)
            independent = (
                W_MASK * s_mask
                + W_BOXES * s_boxes
                + W_ROUTE * s_route
                + W_CLEARANCE * s_clear
                + W_OBSTACLE * s_obstacle
                + W_WIDTH * s_width
                + W_UNCERTAINTY * s_uncertainty
            )
            joint = math.sqrt(max(0.0, s_mask * (0.45 * s_route + 0.55 * min(s_clear, s_obstacle, s_width, s_uncertainty))))
            row_score = independent * (0.70 + 0.30 * joint)
            row_scores.append(float(np.clip(row_score, 0.0, 1.0)))
        if not row_scores:
            raise InvalidSubmissionError("submission has no scorable rows")

        mean_score = float(np.mean(row_scores))
        mission = _worst_group(row_scores, mission_values if mission_values else None)
        terrain = _worst_group(row_scores, terrain_values if terrain_values else None)
        route = _worst_group(row_scores, route_values if route_values else None)
        total_weight = W_MEAN
        total = W_MEAN * mean_score
        if mission is not None:
            total += W_MISSION * mission
            total_weight += W_MISSION
        if terrain is not None:
            total += W_TERRAIN * terrain
            total_weight += W_TERRAIN
        if route is not None:
            total += W_ROUTE_GROUP * route
            total_weight += W_ROUTE_GROUP
        final = float(np.clip(total / total_weight, 0.0, 1.0))
        if abs(final - 1.0) <= 1e-12:
            return 1.0
        return final
    except InvalidSubmissionError:
        raise
    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", required=True)
    parser.add_argument("--answers", required=True)
    args = parser.parse_args()
    try:
        submission = pd.read_csv(args.submission, dtype={"id": str})
        answers = pd.read_csv(args.answers, dtype={"id": str})
    except Exception as exc:
        print(f"InvalidSubmissionError: could not read CSV inputs: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
    try:
        print(f"score={grade(submission, answers):.12f}")
    except InvalidSubmissionError as exc:
        print(f"InvalidSubmissionError: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
