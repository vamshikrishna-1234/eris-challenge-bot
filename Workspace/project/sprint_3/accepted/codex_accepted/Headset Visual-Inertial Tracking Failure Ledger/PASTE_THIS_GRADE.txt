#!/usr/bin/env python3
"""Strict grader for the Headset Visual-Inertial Tracking Failure Ledger."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "id",
    "reliable_keyframes_json",
    "failure_spans_json",
    "anchor_edges_json",
    "failure_type",
    "uncertainty",
]
SUBMISSION_COLUMNS = REQUIRED_COLUMNS
FAILURE_TYPES = {"ok", "drift", "lost_tracking", "relocalized", "uncertain"}
SPAN_TYPES = {"drift", "lost_tracking", "relocalized", "uncertain"}
MAX_JSON_LEN = 6000
WINDOW = 18
ROW_POWER = 1.55


class InvalidSubmissionError(Exception):
    pass


def _as_df(obj) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj.copy()
    try:
        return pd.read_csv(obj)
    except Exception as exc:
        raise InvalidSubmissionError(f"could not read CSV input: {exc}") from exc


def _validate_structure(sub: pd.DataFrame, ans: pd.DataFrame) -> None:
    submission = sub
    if list(submission.columns) != SUBMISSION_COLUMNS:
        raise InvalidSubmissionError("submission must contain exactly the required columns in order")
    if sub["id"].duplicated().any():
        raise InvalidSubmissionError("duplicate submission ids")
    if ans["id"].duplicated().any():
        raise InvalidSubmissionError("duplicate answer ids")
    if set(sub["id"]) != set(ans["id"]):
        raise InvalidSubmissionError("submission id set does not match answers")
    if len(sub) != len(ans):
        raise InvalidSubmissionError("submission row count does not match answers")
    # The submitted uncertainty is the confidence-calibration field for audit checks.
    if sub["uncertainty"].map(lambda x: isinstance(x, (bool, np.bool_))).any():
        raise InvalidSubmissionError("uncertainty must be numeric, not boolean")
    conf = pd.to_numeric(sub["uncertainty"], errors="coerce")
    if not np.isfinite(conf).all():
        raise InvalidSubmissionError("uncertainty contains NaN or inf")
    if ((conf < 0.0) | (conf > 1.0)).any():
        raise InvalidSubmissionError("uncertainty must be in [0, 1]")


def _safe_json(value):
    if not isinstance(value, str) or len(value) > MAX_JSON_LEN:
        return None
    try:
        return json.loads(value, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("non-finite JSON constant")))
    except Exception:
        return None


def _parse_keyframes(value):
    obj = _safe_json(value)
    if not isinstance(obj, list):
        return None
    out = []
    seen = set()
    for x in obj:
        if type(x) is not int or not (0 <= x < WINDOW) or x in seen:
            return None
        out.append(x)
        seen.add(x)
    if len(out) > WINDOW:
        return None
    return set(out)


def _parse_spans(value):
    obj = _safe_json(value)
    if not isinstance(obj, list) or len(obj) > 5:
        return None
    spans = []
    prev_end = -1
    for sp in obj:
        if not isinstance(sp, dict) or set(sp) != {"start", "end", "type", "severity"}:
            return None
        st, en, typ, sev = sp["start"], sp["end"], sp["type"], sp["severity"]
        if type(st) is not int or type(en) is not int or not (0 <= st <= en < WINDOW):
            return None
        if st <= prev_end:
            return None
        if not isinstance(typ, str) or typ not in SPAN_TYPES:
            return None
        if type(sev) not in (int, float):
            return None
        sev = float(sev)
        if not math.isfinite(sev) or not (0.0 <= sev <= 1.0):
            return None
        spans.append({"start": st, "end": en, "type": typ, "severity": sev})
        prev_end = en
    return spans


def _parse_edges(value):
    obj = _safe_json(value)
    if not isinstance(obj, list) or len(obj) > 5:
        return None
    edges = []
    seen = set()
    for ed in obj:
        if not isinstance(ed, dict) or set(ed) != {"current", "anchor"}:
            return None
        cur, anc = ed["current"], ed["anchor"]
        if type(cur) is not int or type(anc) is not int:
            return None
        if not (0 <= cur < WINDOW and 0 <= anc < WINDOW) or cur == anc:
            return None
        pair = (cur, anc)
        if pair in seen:
            return None
        seen.add(pair)
        edges.append(pair)
    return set(edges)


def _f1(pred: set, gold: set) -> float:
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    inter = len(pred & gold)
    if inter == 0:
        return 0.0
    precision = inter / len(pred)
    recall = inter / len(gold)
    return 2 * precision * recall / (precision + recall)


def _interval_iou(a: dict, b: dict) -> float:
    lo = max(a["start"], b["start"])
    hi = min(a["end"], b["end"])
    inter = max(0, hi - lo + 1)
    union = max(a["end"], b["end"]) - min(a["start"], b["start"]) + 1
    return inter / union


def _span_score(pred: list[dict], gold: list[dict]) -> float:
    if pred is None:
        return 0.0
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    candidates = []
    for i, p in enumerate(pred):
        for j, g in enumerate(gold):
            iou = _interval_iou(p, g)
            if iou >= 0.25:
                type_credit = 1.0 if p["type"] == g["type"] else 0.35
                sev_credit = math.exp(-abs(float(p["severity"]) - float(g["severity"])) / 0.22)
                candidates.append((iou * (0.75 * type_credit + 0.25 * sev_credit), i, j))
    candidates.sort(reverse=True)
    used_p, used_g, matched = set(), set(), []
    for score, i, j in candidates:
        if i not in used_p and j not in used_g:
            used_p.add(i)
            used_g.add(j)
            matched.append(score)
    if not matched:
        return 0.0
    precision = sum(matched) / len(pred)
    recall = sum(matched) / len(gold)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def _type_score(pred: str, gold: str) -> float:
    if pred not in FAILURE_TYPES:
        return 0.0
    if pred == gold:
        return 1.0
    partial = {
        ("drift", "relocalized"): 0.35,
        ("relocalized", "drift"): 0.35,
        ("drift", "uncertain"): 0.20,
        ("uncertain", "drift"): 0.20,
        ("lost_tracking", "uncertain"): 0.15,
        ("uncertain", "lost_tracking"): 0.15,
    }
    return partial.get((pred, gold), 0.0)


def _consistency_score(rel: set, spans: list[dict], edges: set, ftype: str) -> float:
    if rel is None or spans is None or edges is None or ftype not in FAILURE_TYPES:
        return 0.0
    span_points = {k for sp in spans for k in range(sp["start"], sp["end"] + 1)}
    rel_clean = 1.0 - (len(rel & span_points) / max(1, len(rel)))
    edge_clean = 1.0
    for cur, anc in edges:
        if anc in span_points or cur == anc or cur < anc:
            edge_clean -= 0.25
    if ftype == "ok" and spans:
        edge_clean -= 0.35
    if ftype == "lost_tracking" and not any(sp["type"] == "lost_tracking" for sp in spans):
        edge_clean -= 0.35
    return float(np.clip(0.55 * rel_clean + 0.45 * edge_clean, 0.0, 1.0))


def _row_score(row: pd.Series, gold: pd.Series) -> float:
    pred_rel = _parse_keyframes(row["reliable_keyframes_json"])
    gold_rel = _parse_keyframes(gold["reliable_keyframes_json"])
    pred_spans = _parse_spans(row["failure_spans_json"])
    gold_spans = _parse_spans(gold["failure_spans_json"])
    pred_edges = _parse_edges(row["anchor_edges_json"])
    gold_edges = _parse_edges(gold["anchor_edges_json"])
    pred_type = row["failure_type"]
    gold_type = gold["failure_type"]
    if gold_rel is None or gold_spans is None or gold_edges is None:
        raise InvalidSubmissionError("malformed hidden answers")
    if not isinstance(gold_type, str) or gold_type not in FAILURE_TYPES:
        raise InvalidSubmissionError("malformed hidden answers")
    if (
        pred_rel is None
        or pred_spans is None
        or pred_edges is None
        or not isinstance(pred_type, str)
        or pred_type not in FAILURE_TYPES
    ):
        return 0.0
    s_rel = 0.0 if pred_rel is None else _f1(pred_rel, gold_rel)
    s_span = _span_score(pred_spans, gold_spans)
    s_edge = 0.0 if pred_edges is None else _f1(pred_edges, gold_edges)
    s_type = _type_score(pred_type, gold_type)
    s_unc = math.exp(-abs(float(row["uncertainty"]) - float(gold["uncertainty"])) / 0.18)
    s_cons = _consistency_score(pred_rel, pred_spans, pred_edges, pred_type)
    raw = 0.22 * s_rel + 0.30 * s_span + 0.18 * s_edge + 0.16 * s_type + 0.10 * s_unc + 0.04 * s_cons
    return float(np.clip(raw, 0.0, 1.0) ** ROW_POWER)


def grade(submission, answers) -> float:
    try:
        sub = _as_df(submission)
        ans = _as_df(answers)
        _validate_structure(sub, ans)
        sub["uncertainty"] = pd.to_numeric(sub["uncertainty"], errors="coerce").astype(float)
        ans = ans.reset_index(drop=True)
        sub = sub.set_index("id").loc[ans["id"]].reset_index()
        scores = np.asarray([_row_score(s, g) for (_, s), (_, g) in zip(sub.iterrows(), ans.iterrows())], dtype=float)
        if not np.isfinite(scores).all():
            return 0.0
        mean_score = float(np.mean(scores))
        final = 0.78 * mean_score
        for axis, weight in [("group_device", 0.08), ("group_motion", 0.08), ("group_failure_type", 0.06)]:
            vals = []
            for _, idx in ans.groupby(axis).groups.items():
                vals.append(float(np.mean(scores[list(idx)])))
            final += weight * min(vals)
        return float(np.clip(final, 0.0, 1.0))
    except InvalidSubmissionError:
        return 0.0
    except Exception:
        return 0.0


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python grade.py submission.csv answers.csv", file=sys.stderr)
        return 2
    score = grade(Path(sys.argv[1]), Path(sys.argv[2]))
    print(score)
    return 0 if score > 0.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
