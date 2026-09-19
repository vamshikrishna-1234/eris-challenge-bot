from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


SUBMISSION_COLUMNS = ["id", "ledger_json", "envelope_json", "quality_json", "confidence"]
ANSWER_REQUIRED = {
    "id",
    "ledger_json",
    "envelope_json",
    "quality_json",
    "segment_duration_sec",
}

MAX_JSON_LEN = 30000
MAX_EVENTS = 40
MAX_ENVELOPE_POINTS = 96
MATCH_TOL_SEC = 0.08

W_EVENTS = 0.40
W_TIMING = 0.16
W_BOUNDARY = 0.12
W_ENVELOPE = 0.17
W_QUALITY = 0.10
W_COUNT = 0.05
W_CONFIDENCE = 0.08

W_MEAN = 0.70
W_WORST_SPLIT = 0.12
W_WORST_OOD = 0.10
W_WORST_STYLE = 0.08


class InvalidSubmissionError(Exception):
    pass


def _bad_structure(message: str) -> None:
    raise InvalidSubmissionError(message)


def _safe_float(v):
    try:
        x = float(v)
    except (TypeError, ValueError, OverflowError):
        return None
    if not np.isfinite(x):
        return None
    return float(x)


def _parse_json_cell(cell, default):
    if cell is None:
        return default
    if isinstance(cell, float) and not np.isfinite(cell):
        return default
    text = str(cell)
    if len(text) > MAX_JSON_LEN:
        return default
    try:
        return json.loads(text)
    except (TypeError, ValueError, OverflowError, json.JSONDecodeError):
        return default


def _json_cell_with_status(cell):
    if cell is None:
        return None, True
    if isinstance(cell, float) and not np.isfinite(cell):
        return None, True
    text = str(cell)
    if len(text) > MAX_JSON_LEN:
        return None, True
    try:
        return json.loads(text), False
    except (TypeError, ValueError, OverflowError, json.JSONDecodeError):
        return None, True


def _parse_ledger(cell, duration: float):
    data = _parse_json_cell(cell, [])
    if not isinstance(data, list):
        return []
    out = []
    for item in data[:MAX_EVENTS]:
        if not isinstance(item, dict):
            continue
        t = _safe_float(item.get("t"))
        start = _safe_float(item.get("start"))
        end = _safe_float(item.get("end"))
        if t is None or start is None or end is None:
            continue
        # Reject negative or impossible row-local exact times.
        if t < 0 or start < 0 or end < 0 or t > duration or start > duration or end > duration:
            continue
        if end < start:
            continue
        if not (start <= t <= end):
            continue
        out.append({"t": t, "start": start, "end": end})
    out.sort(key=lambda r: (r["t"], r["start"], r["end"]))
    dedup = []
    last_t = None
    for row in out:
        if last_t is None or abs(row["t"] - last_t) > 0.025:
            dedup.append(row)
            last_t = row["t"]
    return dedup[:MAX_EVENTS]


def _parse_ledger_checked(cell, duration: float):
    data, malformed = _json_cell_with_status(cell)
    if malformed or not isinstance(data, list) or len(data) > MAX_EVENTS:
        return [], True
    out = []
    for item in data:
        if not isinstance(item, dict):
            return [], True
        t = _safe_float(item.get("t"))
        start = _safe_float(item.get("start"))
        end = _safe_float(item.get("end"))
        if t is None or start is None or end is None:
            return [], True
        if t < 0 or start < 0 or end < 0 or t > duration or start > duration or end > duration:
            return [], True
        if end < start or not (start <= t <= end):
            return [], True
        out.append({"t": t, "start": start, "end": end})
    out.sort(key=lambda r: (r["t"], r["start"], r["end"]))
    for a, b in zip(out, out[1:]):
        if abs(a["t"] - b["t"]) <= 0.025:
            return [], True
    return out, False


def _parse_quality(cell):
    data = _parse_json_cell(cell, [])
    if not isinstance(data, list):
        return []
    out = []
    for item in data[:MAX_EVENTS]:
        s = str(item).strip().lower()
        if s in {"usable", "uncertain", "artifact"}:
            out.append(s)
        else:
            out.append("artifact")
    return out


def _parse_quality_checked(cell, expected_len: int):
    data, malformed = _json_cell_with_status(cell)
    if malformed or not isinstance(data, list) or len(data) > MAX_EVENTS:
        return [], True
    out = []
    for item in data:
        s = str(item).strip().lower()
        if s not in {"usable", "uncertain", "artifact"}:
            return [], True
        out.append(s)
    if len(out) != expected_len:
        return [], True
    return out, False


def _parse_envelope(cell):
    data = _parse_json_cell(cell, [])
    if not isinstance(data, list):
        return []
    out = []
    for item in data[:MAX_ENVELOPE_POINTS]:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            continue
        x = _safe_float(item[0])
        lo = _safe_float(item[1])
        hi = _safe_float(item[2])
        if x is None or lo is None or hi is None:
            continue
        if x < 0 or x > 1 or lo < 0 or lo > 1 or hi < 0 or hi > 1:
            continue
        if hi < lo:
            continue
        out.append((x, lo, hi))
    out.sort(key=lambda r: r[0])
    return out[:MAX_ENVELOPE_POINTS]


def _parse_envelope_checked(cell):
    data, malformed = _json_cell_with_status(cell)
    if malformed or not isinstance(data, list) or not (2 <= len(data) <= MAX_ENVELOPE_POINTS):
        return [], True
    out = []
    last_x = -1.0
    for item in data:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            return [], True
        x = _safe_float(item[0])
        lo = _safe_float(item[1])
        hi = _safe_float(item[2])
        if x is None or lo is None or hi is None:
            return [], True
        if x < 0 or x > 1 or lo < 0 or lo > 1 or hi < 0 or hi > 1:
            return [], True
        if hi < lo or x <= last_x:
            return [], True
        out.append((x, lo, hi))
        last_x = x
    return out, False


def _match_events(pred, true):
    if not pred and not true:
        return [], 1.0, 1.0
    if not pred or not true:
        return [], 0.0, 0.0
    candidates = []
    for i, p in enumerate(pred):
        for j, t in enumerate(true):
            err = abs(p["t"] - t["t"])
            if err <= MATCH_TOL_SEC:
                candidates.append((err, i, j))
    candidates.sort()
    used_p = set()
    used_t = set()
    matches = []
    for err, i, j in candidates:
        if i in used_p or j in used_t:
            continue
        used_p.add(i)
        used_t.add(j)
        matches.append((i, j, err))
    precision = len(matches) / len(pred) if pred else 0.0
    recall = len(matches) / len(true) if true else 0.0
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    count_score = max(0.0, 1.0 - abs(len(pred) - len(true)) / max(1, len(true)))
    return matches, float(f1), float(count_score)


def _timing_scores(pred, true, matches):
    if not matches:
        return 0.0, 0.0
    timing = []
    boundary = []
    for i, j, err in matches:
        p = pred[i]
        t = true[j]
        timing.append(max(0.0, 1.0 - err / MATCH_TOL_SEC))
        b_err = abs(p["start"] - t["start"]) + abs(p["end"] - t["end"])
        boundary.append(max(0.0, 1.0 - b_err / (2 * MATCH_TOL_SEC)))
    return float(np.mean(timing)), float(np.mean(boundary))


def _quality_score(pred_q, true_q, matches):
    if not matches:
        return 0.0
    vals = []
    for i, j, _ in matches:
        pq = pred_q[i] if i < len(pred_q) else "artifact"
        tq = true_q[j] if j < len(true_q) else "artifact"
        vals.append(1.0 if pq == tq else (0.5 if {pq, tq} <= {"usable", "uncertain"} else 0.0))
    return float(np.mean(vals))


def _interp_env(env, xs):
    if len(env) < 2:
        return None, None
    x = np.array([p[0] for p in env], dtype=float)
    lo = np.array([p[1] for p in env], dtype=float)
    hi = np.array([p[2] for p in env], dtype=float)
    if np.any(np.diff(x) <= 0):
        return None, None
    return np.interp(xs, x, lo), np.interp(xs, x, hi)


def _envelope_score(pred_env, true_env):
    if len(pred_env) < 2 or len(true_env) < 2:
        return 0.0
    xs = np.linspace(0.0, 1.0, 64)
    plo, phi = _interp_env(pred_env, xs)
    tlo, thi = _interp_env(true_env, xs)
    if plo is None or tlo is None:
        return 0.0
    mae = float(np.mean(np.abs(plo - tlo) + np.abs(phi - thi)) / 2.0)
    return float(np.clip(1.0 - mae / 0.22, 0.0, 1.0))


def _confidence_factor(conf: float, correctness: float) -> float:
    # Confidence is allowed to modulate earned task credit only. It never adds
    # standalone points to an otherwise wrong row.
    return float(np.clip(1.0 - W_CONFIDENCE * abs(conf - correctness), 0.0, 1.0))


def _worst_group(row_scores, groups):
    buckets = {}
    for s, g in zip(row_scores, groups):
        buckets.setdefault(str(g), []).append(float(s))
    if not buckets:
        return None
    return min(float(np.mean(v)) for v in buckets.values())


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        if list(submission.columns) != SUBMISSION_COLUMNS:
            _bad_structure("submission columns are missing, extra, or reordered")
        if not ANSWER_REQUIRED.issubset(set(answers.columns)):
            _bad_structure("answers are missing required columns")

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(int)
            ans["id"] = ans["id"].astype(int)
        except (TypeError, ValueError, OverflowError):
            _bad_structure("id values must be integers")
        if sub["id"].duplicated().any():
            _bad_structure("duplicate ids")
        if ans["id"].duplicated().any():
            _bad_structure("duplicate answer ids")
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            _bad_structure("submission id set does not match answers")

        confs = []
        for v in sub["confidence"]:
            c = _safe_float(v)
            if c is None or c < 0.0 or c > 1.0:
                _bad_structure("confidence must be finite and in [0, 1]")
            confs.append(c)

        sub_by_id = {int(r["id"]): r for _, r in sub.iterrows()}
        row_scores = []
        split_groups = []
        ood_groups = []
        style_groups = []

        for _, arow in ans.iterrows():
            rid = int(arow["id"])
            srow = sub_by_id[rid]
            duration = float(arow["segment_duration_sec"])

            pred_led, bad_ledger = _parse_ledger_checked(srow["ledger_json"], duration)
            pred_env, bad_env = _parse_envelope_checked(srow["envelope_json"])
            pred_q, bad_quality = _parse_quality_checked(srow["quality_json"], len(pred_led))
            if bad_ledger or bad_env or bad_quality:
                row_scores.append(0.0)
                split_groups.append(arow.get("split_group", "all"))
                ood_groups.append(arow.get("ood_axis", "all"))
                style_groups.append(arow.get("render_style", "all"))
                continue
            true_led = _parse_ledger(arow["ledger_json"], duration)
            true_q = _parse_quality(arow["quality_json"])
            true_env = _parse_envelope(arow["envelope_json"])

            matches, event_f1, count_score = _match_events(pred_led, true_led)
            timing_score, boundary_score = _timing_scores(pred_led, true_led, matches)
            matched_gate = 1.0 if matches else 0.0
            event_gate = event_f1
            quality_score = matched_gate * _quality_score(pred_q, true_q, matches)
            envelope_score = event_gate * _envelope_score(pred_env, true_env)
            count_score = event_gate * count_score
            correctness = (
                W_EVENTS * event_f1
                + W_TIMING * timing_score
                + W_BOUNDARY * boundary_score
                + W_ENVELOPE * envelope_score
                + W_QUALITY * quality_score
                + W_COUNT * count_score
            )
            correctness = float(np.clip(correctness, 0.0, 1.0))
            conf = _safe_float(srow["confidence"])
            row_score = correctness * _confidence_factor(float(conf), correctness)
            row_scores.append(float(np.clip(row_score, 0.0, 1.0)))
            split_groups.append(arow.get("split_group", "all"))
            ood_groups.append(arow.get("ood_axis", "all"))
            style_groups.append(arow.get("render_style", "all"))

        if not row_scores:
            return 0.0
        mean_score = float(np.mean(row_scores))
        acc = W_MEAN * mean_score
        total = W_MEAN
        for weight, groups in [
            (W_WORST_SPLIT, split_groups),
            (W_WORST_OOD, ood_groups),
            (W_WORST_STYLE, style_groups),
        ]:
            wg = _worst_group(row_scores, groups)
            if wg is not None:
                acc += weight * wg
                total += weight
        return float(np.clip(acc / total, 0.0, 1.0))
    except InvalidSubmissionError:
        return 0.0
    except Exception:
        return 0.0


def _main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python grade.py <submission.csv> <answers.csv>", file=sys.stderr)
        return 2
    try:
        submission = pd.read_csv(Path(argv[1]))
        answers = pd.read_csv(Path(argv[2]))
        print(grade(submission, answers))
        return 0
    except Exception as exc:
        print(f"InvalidSubmissionError: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
