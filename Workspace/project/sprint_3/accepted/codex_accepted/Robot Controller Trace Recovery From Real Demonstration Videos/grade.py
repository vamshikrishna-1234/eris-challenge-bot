import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "id",
    "controller_segments_json",
    "key_waypoints_json",
    "event_frames_json",
    "confidence",
]
MAX_JSON_LEN = 12000
MAX_SUBMISSION_BYTES = 25_000_000
MAX_FRAME_INDEX = 47
MAX_SEGMENTS = 12
MAX_WAYPOINTS = 12
MAX_EVENTS = 8
SEGMENT_MIN_IOU = 0.55
SEGMENT_BOUNDARY_DENOM = 12.0
WAYPOINT_FRAME_TOL = 6.0
WAYPOINT_BIN_TOL = 4.0
WAYPOINT_MIN_PAIR_SCORE = 0.60
EVENT_FRAME_TOL = 5.0
SCORE_POWER = 3.20


class InvalidSubmission(Exception):
    pass


def _load_csv(path: Path) -> pd.DataFrame:
    try:
        if Path(path).exists() and Path(path).stat().st_size > MAX_SUBMISSION_BYTES:
            raise InvalidSubmission("csv file is too large")
        raw = Path(path).read_bytes()
        if b"\x00" in raw:
            raise InvalidSubmission("csv contains NUL bytes")
        text = raw.decode("utf-8", errors="strict")
        if any((ord(ch) < 32 and ch not in "\r\n\t") for ch in text):
            raise InvalidSubmission("csv contains unsupported control characters")
        from io import StringIO

        return pd.read_csv(StringIO(text))
    except InvalidSubmission:
        raise
    except Exception as exc:
        raise InvalidSubmission(f"could not read csv: {exc}") from exc


def _validate_submission(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame:
    if list(sub.columns) != REQUIRED_COLUMNS:
        raise InvalidSubmission(f"submission columns must be exactly {REQUIRED_COLUMNS}")
    if sub["id"].duplicated().any():
        raise InvalidSubmission("duplicate ids in submission")
    if ans["id"].duplicated().any():
        raise InvalidSubmission("duplicate ids in answers")
    sub_ids = set(sub["id"].astype(str))
    ans_ids = set(ans["id"].astype(str))
    if sub_ids != ans_ids or len(sub) != len(ans):
        raise InvalidSubmission("submission id set does not match answers")
    conf = pd.to_numeric(sub["confidence"], errors="coerce")
    if not np.isfinite(conf).all():
        raise InvalidSubmission("confidence must be finite numeric")
    if ((conf < 0.0) | (conf > 1.0)).any():
        raise InvalidSubmission("confidence must be in [0, 1]")
    out = sub.copy()
    out["id"] = out["id"].astype(str)
    out["confidence"] = conf.astype(float)
    return out.sort_values("id").reset_index(drop=True)


def _parse_json_cell(value, expected_type):
    if not isinstance(value, str):
        return None
    if len(value) > MAX_JSON_LEN:
        return None
    try:
        obj = json.loads(value)
    except Exception:
        return None
    if not isinstance(obj, expected_type):
        return None
    return obj


def _finite_number(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))


def _valid_segment(item):
    if not isinstance(item, dict):
        return False
    if set(item) != {"mode", "arm", "start_frame", "end_frame"}:
        return False
    if item.get("mode") not in {"joint_move", "cartesian_move", "wait", "contact_like_pause"}:
        return False
    if item.get("arm") not in {"giver", "receiver", "both"}:
        return False
    if type(item.get("start_frame")) is not int or type(item.get("end_frame")) is not int:
        return False
    if item["start_frame"] < 0 or item["end_frame"] < item["start_frame"] or item["end_frame"] > MAX_FRAME_INDEX:
        return False
    return True


def _valid_waypoint(item):
    if not isinstance(item, dict):
        return False
    if set(item) != {"arm", "kind", "frame", "xyz_bins"}:
        return False
    if item.get("arm") not in {"giver", "receiver"}:
        return False
    if item.get("kind") not in {"start", "approach", "handover", "retreat", "end"}:
        return False
    if type(item.get("frame")) is not int or item["frame"] < 0 or item["frame"] > MAX_FRAME_INDEX:
        return False
    bins = item.get("xyz_bins")
    if not isinstance(bins, list) or len(bins) != 3:
        return False
    if any((type(v) is not int or v < 0 or v > 9) for v in bins):
        return False
    return True


def _valid_event(item):
    if not isinstance(item, dict):
        return False
    if set(item) != {"event", "arm", "frame"}:
        return False
    if item.get("event") not in {"motion_start", "handover_pause", "release_like", "motion_stop"}:
        return False
    if item.get("arm") not in {"giver", "receiver", "both"}:
        return False
    if type(item.get("frame")) is not int or item["frame"] < 0 or item["frame"] > MAX_FRAME_INDEX:
        return False
    return True


def _interval_iou(a0, a1, b0, b1):
    inter = max(0, min(a1, b1) - max(a0, b0) + 1)
    union = max(a1, b1) - min(a0, b0) + 1
    return inter / union if union else 0.0


def _match_f1(pred, gold, item_score):
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    scores = []
    for i, p in enumerate(pred):
        for j, g in enumerate(gold):
            s = item_score(p, g)
            if s > 0:
                scores.append((s, i, j))
    scores.sort(reverse=True)
    used_p, used_g, total = set(), set(), 0.0
    for s, i, j in scores:
        if i in used_p or j in used_g:
            continue
        used_p.add(i)
        used_g.add(j)
        total += s
    precision = total / max(1, len(pred))
    recall = total / max(1, len(gold))
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def _segment_item_score(p, g):
    if p.get("mode") != g.get("mode") or p.get("arm") != g.get("arm"):
        return 0.0
    iou = _interval_iou(int(p["start_frame"]), int(p["end_frame"]), int(g["start_frame"]), int(g["end_frame"]))
    if iou < SEGMENT_MIN_IOU:
        return 0.0
    boundary = max(
        0.0,
        1.0
        - (abs(p["start_frame"] - g["start_frame"]) + abs(p["end_frame"] - g["end_frame"]))
        / SEGMENT_BOUNDARY_DENOM,
    )
    return 0.75 * iou + 0.25 * boundary


def _waypoint_item_score(p, g):
    if p.get("arm") != g.get("arm") or p.get("kind") != g.get("kind"):
        return 0.0
    frame_score = max(0.0, 1.0 - abs(int(p["frame"]) - int(g["frame"])) / WAYPOINT_FRAME_TOL)
    bin_dist = sum(abs(int(a) - int(b)) for a, b in zip(p["xyz_bins"], g["xyz_bins"]))
    bin_score = max(0.0, 1.0 - bin_dist / WAYPOINT_BIN_TOL)
    s = 0.50 * frame_score + 0.50 * bin_score
    return s if s >= WAYPOINT_MIN_PAIR_SCORE else 0.0


def _event_item_score(p, g):
    if p.get("event") != g.get("event") or p.get("arm") != g.get("arm"):
        return 0.0
    return max(0.0, 1.0 - abs(int(p["frame"]) - int(g["frame"])) / EVENT_FRAME_TOL)


def _row_score(pred_row, gold_row):
    try:
        pred_segments = _parse_json_cell(pred_row["controller_segments_json"], list)
        pred_waypoints = _parse_json_cell(pred_row["key_waypoints_json"], list)
        pred_events = _parse_json_cell(pred_row["event_frames_json"], list)
        gold_segments = _parse_json_cell(gold_row["controller_segments_json"], list) or []
        gold_waypoints = _parse_json_cell(gold_row["key_waypoints_json"], list) or []
        gold_events = _parse_json_cell(gold_row["event_frames_json"], list) or []
    except Exception:
        return 0.0
    if pred_segments is None or pred_waypoints is None or pred_events is None:
        return 0.0
    if len(pred_segments) > MAX_SEGMENTS or len(pred_waypoints) > MAX_WAYPOINTS or len(pred_events) > MAX_EVENTS:
        return 0.0
    if not all(_valid_segment(x) for x in pred_segments):
        return 0.0
    if not all(_valid_waypoint(x) for x in pred_waypoints):
        return 0.0
    if not all(_valid_event(x) for x in pred_events):
        return 0.0

    seg_score = 0.0
    seg_score = _match_f1(pred_segments, gold_segments, _segment_item_score)

    waypoint_score = 0.0
    waypoint_score = _match_f1(pred_waypoints, gold_waypoints, _waypoint_item_score)

    event_score = 0.0
    event_score = _match_f1(pred_events, gold_events, _event_item_score)

    core = 0.55 * seg_score + 0.25 * waypoint_score + 0.20 * event_score
    core = core ** SCORE_POWER
    conf = float(pred_row["confidence"])
    calibration = max(0.0, 1.0 - abs(conf - core))
    return core * (0.85 + 0.15 * calibration)


def score_frames(submission_df: pd.DataFrame, answers_df: pd.DataFrame) -> float:
    answers = answers_df.copy()
    submission = _validate_submission(submission_df.copy(), answers)
    answers = answers.copy()
    answers["id"] = answers["id"].astype(str)
    answers = answers.sort_values("id").reset_index(drop=True)
    scores = [_row_score(s, a) for (_, s), (_, a) in zip(submission.iterrows(), answers.iterrows())]
    return float(np.clip(np.mean(scores), 0.0, 1.0))


def score_submission(submission_path: Path, answers_path: Path) -> float:
    return score_frames(_load_csv(Path(submission_path)), _load_csv(Path(answers_path)))


def _coerce_input(obj) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj.copy()
    return _load_csv(Path(obj))


def grade(submission, answers) -> float:
    try:
        return score_frames(_coerce_input(submission), _coerce_input(answers))
    except Exception:
        return 0.0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python grade.py submission.csv answers.csv")
    print(f"{grade(sys.argv[1], sys.argv[2]):.12f}")
