from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "id",
    "dancer_id",
    "waggle_intervals_json",
    "roles_json",
    "edges_json",
    "confidence",
]
MAX_JSON_LEN = 20000
MAX_SUBMISSION_BYTES = 30_000_000
MAX_INTERVALS = 30
MAX_ROLES = 48
MAX_EDGES = 48
SCORE_POWER = 0.80
INTERVAL_MIN_PAIR = 0.18
COUNT_PENALTY_FLOOR = 0.35
COUNT_PENALTY_WEIGHT = 0.65
BEE_RE = re.compile(r"^B[0-9]{2}$")
GROUP_COLUMNS = [
    "crowding_level",
    "tracking_confidence_level",
    "duration_bucket",
    "waggle_count_bucket",
    "comb_side",
    "date_group",
]


class InvalidSubmissionError(ValueError):
    pass


InvalidSubmission = InvalidSubmissionError


def _load_csv(path: Path) -> pd.DataFrame:
    try:
        path = Path(path)
        if path.exists() and path.stat().st_size > MAX_SUBMISSION_BYTES:
            raise InvalidSubmission("csv file is too large")
        raw = path.read_bytes()
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


def _coerce_input(obj) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj.copy()
    return _load_csv(Path(obj))


def _validate_submission(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame:
    if list(sub.columns) != REQUIRED_COLUMNS:
        raise InvalidSubmission(f"submission columns must be exactly {REQUIRED_COLUMNS}")
    if "id" not in ans.columns:
        raise InvalidSubmission("answers are missing id column")
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
    out["dancer_id"] = out["dancer_id"].astype(str)
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


def _finite_number(x) -> bool:
    return not isinstance(x, bool) and isinstance(x, (int, float)) and math.isfinite(float(x))


def _valid_bee(value: str, bee_count: int | None = None) -> bool:
    if not isinstance(value, str) or not BEE_RE.match(value):
        return False
    if bee_count is None:
        return True
    return int(value[1:]) < int(bee_count)


def _valid_interval(item, duration: float) -> bool:
    if not isinstance(item, dict) or set(item) != {"start", "end"}:
        return False
    if not _finite_number(item["start"]) or not _finite_number(item["end"]):
        return False
    start = float(item["start"])
    end = float(item["end"])
    return 0.0 <= start <= end <= duration + 1e-6


def _valid_roles(items, bee_count: int | None = None) -> bool:
    seen = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != {"bee_id", "role"}:
            return False
        bee = item.get("bee_id")
        role = item.get("role")
        if not _valid_bee(bee, bee_count) or role not in {"follower", "attendee"}:
            return False
        if bee in seen:
            return False
        seen.add(bee)
    return True


def _valid_edges(items, bee_count: int | None = None) -> bool:
    seen = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != {"source", "target"}:
            return False
        source = item.get("source")
        target = item.get("target")
        if not _valid_bee(source, bee_count) or not _valid_bee(target, bee_count) or source == target:
            return False
        edge = (source, target)
        if edge in seen:
            return False
        seen.add(edge)
    return True


def _interval_iou(a, b) -> float:
    a0, a1 = float(a["start"]), float(a["end"])
    b0, b1 = float(b["start"]), float(b["end"])
    inter = max(0.0, min(a1, b1) - max(a0, b0))
    union = max(a1, b1) - min(a0, b0)
    return inter / union if union > 0 else 0.0


def _interval_pair_score(pred, gold) -> float:
    iou = _interval_iou(pred, gold)
    if iou < INTERVAL_MIN_PAIR:
        return 0.0
    center_err = abs((float(pred["start"]) + float(pred["end"])) / 2.0 - (float(gold["start"]) + float(gold["end"])) / 2.0)
    length_err = abs((float(pred["end"]) - float(pred["start"])) - (float(gold["end"]) - float(gold["start"])))
    timing = max(0.0, 1.0 - (center_err + 0.5 * length_err) / 1.25)
    return 0.72 * iou + 0.28 * timing


def _match_f1(pred, gold, item_score) -> float:
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    pairs = []
    for i, p in enumerate(pred):
        for j, g in enumerate(gold):
            s = item_score(p, g)
            if s > 0:
                pairs.append((s, i, j))
    pairs.sort(reverse=True)
    used_p, used_g, total = set(), set(), 0.0
    for s, i, j in pairs:
        if i in used_p or j in used_g:
            continue
        used_p.add(i)
        used_g.add(j)
        total += s
    precision = total / max(1, len(pred))
    recall = total / max(1, len(gold))
    return 0.0 if precision + recall == 0 else 2.0 * precision * recall / (precision + recall)


def _set_f1(pred_set: set, gold_set: set) -> float:
    if not pred_set and not gold_set:
        return 1.0
    if not pred_set or not gold_set:
        return 0.0
    tp = len(pred_set & gold_set)
    precision = tp / len(pred_set)
    recall = tp / len(gold_set)
    return 0.0 if precision + recall == 0 else 2.0 * precision * recall / (precision + recall)


def _role_score(pred_roles, gold_roles) -> float:
    pred_exact = {(r["bee_id"], r["role"]) for r in pred_roles}
    gold_exact = {(r["bee_id"], r["role"]) for r in gold_roles}
    exact = _set_f1(pred_exact, gold_exact)
    pred_bees = {r["bee_id"] for r in pred_roles}
    gold_bees = {r["bee_id"] for r in gold_roles}
    participant = _set_f1(pred_bees, gold_bees)
    pred_follow = {r["bee_id"] for r in pred_roles if r["role"] == "follower"}
    gold_follow = {r["bee_id"] for r in gold_roles if r["role"] == "follower"}
    follower = _set_f1(pred_follow, gold_follow)
    return 0.58 * exact + 0.22 * participant + 0.20 * follower


def _edge_score(pred_edges, gold_edges) -> float:
    pred = {(e["source"], e["target"]) for e in pred_edges}
    gold = {(e["source"], e["target"]) for e in gold_edges}
    target_pred = {e["target"] for e in pred_edges}
    target_gold = {e["target"] for e in gold_edges}
    return 0.74 * _set_f1(pred, gold) + 0.26 * _set_f1(target_pred, target_gold)


def _internal_consistency(dancer_id: str, roles, edges, bee_count: int | None = None) -> float:
    if not _valid_bee(dancer_id, bee_count):
        return 0.0
    role_map = {r["bee_id"]: r["role"] for r in roles}
    if dancer_id in role_map:
        return 0.0
    if not edges:
        return 0.0
    ok = 0
    for e in edges:
        if e["source"] == dancer_id and role_map.get(e["target"]) == "follower":
            ok += 1
    return ok / max(1, len(edges))


def _overprediction_penalty(pred_intervals, gold_intervals, pred_roles, gold_roles, pred_edges, gold_edges) -> float:
    ratios = []
    for pred_count, gold_count, slack in [
        (len(pred_intervals), len(gold_intervals), 2),
        (len(pred_roles), len(gold_roles), 2),
        (len(pred_edges), len(gold_edges), 1),
    ]:
        ratios.append(min(1.0, (gold_count + slack) / max(gold_count + slack, pred_count + slack)))
    count_score = (ratios[0] * ratios[1] * ratios[2]) ** (1.0 / 3.0)
    return COUNT_PENALTY_FLOOR + COUNT_PENALTY_WEIGHT * count_score


def _row_score(pred_row, gold_row) -> float:
    try:
        duration = float(gold_row.get("duration_sec", 60.0))
        bee_count = int(gold_row.get("bee_count", 100))
        pred_dancer = str(pred_row["dancer_id"])
        gold_dancer = str(gold_row["dancer_id"])
        pred_intervals = _parse_json_cell(pred_row["waggle_intervals_json"], list)
        pred_roles = _parse_json_cell(pred_row["roles_json"], list)
        pred_edges = _parse_json_cell(pred_row["edges_json"], list)
        gold_intervals = _parse_json_cell(gold_row["waggle_intervals_json"], list) or []
        gold_roles = _parse_json_cell(gold_row["roles_json"], list) or []
        gold_edges = _parse_json_cell(gold_row["edges_json"], list) or []
    except Exception:
        return 0.0

    if pred_intervals is None or pred_roles is None or pred_edges is None:
        return 0.0
    if len(pred_intervals) > MAX_INTERVALS or len(pred_roles) > MAX_ROLES or len(pred_edges) > MAX_EDGES:
        return 0.0
    if not _valid_bee(pred_dancer, bee_count):
        return 0.0
    dancer_score = 1.0 if pred_dancer == gold_dancer else 0.0
    if not all(_valid_interval(x, duration) for x in pred_intervals):
        return 0.0
    if not _valid_roles(pred_roles, bee_count) or not _valid_edges(pred_edges, bee_count):
        return 0.0

    interval_score = _match_f1(pred_intervals, gold_intervals, _interval_pair_score)
    role_score = _role_score(pred_roles, gold_roles)
    edge_score = _edge_score(pred_edges, gold_edges)
    consistency = _internal_consistency(pred_dancer, pred_roles, pred_edges, bee_count)
    joint = math.sqrt(max(0.0, dancer_score) * max(0.0, 0.40 * interval_score + 0.35 * edge_score + 0.25 * role_score))

    core = (
        0.18 * dancer_score
        + 0.30 * interval_score
        + 0.22 * role_score
        + 0.20 * edge_score
        + 0.10 * (0.55 * joint + 0.45 * consistency * edge_score)
    )
    powered = core ** SCORE_POWER
    confidence = float(pred_row["confidence"])
    calibration = max(0.0, 1.0 - abs(confidence - powered))
    count_penalty = _overprediction_penalty(pred_intervals, gold_intervals, pred_roles, gold_roles, pred_edges, gold_edges)
    return float(powered * (0.86 + 0.14 * calibration) * count_penalty)


def score_frames(submission_df: pd.DataFrame, answers_df: pd.DataFrame) -> float:
    answers = answers_df.copy()
    answers["id"] = answers["id"].astype(str)
    answers = answers.sort_values("id").reset_index(drop=True)
    submission = _validate_submission(submission_df.copy(), answers)
    row_scores = np.array([_row_score(s, a) for (_, s), (_, a) in zip(submission.iterrows(), answers.iterrows())], dtype=float)
    mean_score = float(np.mean(row_scores)) if len(row_scores) else 0.0

    worst_scores = []
    for col in GROUP_COLUMNS:
        if col not in answers.columns:
            continue
        vals = []
        for _, idx in answers.groupby(col, sort=False).groups.items():
            ids = list(idx)
            if ids:
                vals.append(float(np.mean(row_scores[ids])))
        if vals:
            worst_scores.append(min(vals))
    if worst_scores:
        worst = float(np.mean(worst_scores))
        final = 0.78 * mean_score + 0.22 * worst
    else:
        final = mean_score
    return float(np.clip(final, 0.0, 1.0))


def score_submission(submission_path: Path, answers_path: Path) -> float:
    return score_frames(_load_csv(Path(submission_path)), _load_csv(Path(answers_path)))


def grade(submission, answers) -> float:
    return score_frames(_coerce_input(submission), _coerce_input(answers))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python grade.py submission.csv answers.csv", file=sys.stderr)
        raise SystemExit(0)
    print(f"{grade(sys.argv[1], sys.argv[2]):.12f}")
