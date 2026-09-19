"""
grade.py - Hidden Control Panel Circuit Induction

Per scene two sub-scores, squared and blended, then aggregated with worst-group
terms:

    S_wire  = mean over lamps of (gate_type_match * input_set_F1), where a wrong
              gate scores the lamp 0 even if the input set is right.
    S_query = mean per-lamp on/off agreement on the held-out query config.

    correctness = 0.55*S_wire^2 + 0.45*S_query^2
    row         = 0.90*correctness + 0.10*(1 - |confidence - correctness|)
    Final = 0.68*mean(row) + 0.14*worst(split_group) + 0.10*worst(ood_axis)
            + 0.08*worst(render_style), clipped to [0,1].

Allowed gate tokens (case-insensitive): BUF, NOT, AND, OR, NAND, NOR, XOR, XNOR.

STRICT (returns 0.0, never coerces structural problems):
  * missing required column (either side)                          -> 0.0
  * duplicate ids / submission id-set != answers id-set            -> 0.0
  * confidence not finite or not in [0,1]                          -> 0.0
  * any JSON cell over the length guard or not valid JSON          -> 0.0
  * any unhandled exception                                        -> 0.0
Content-level mistakes (wrong gate, wrong/short query_pattern, unknown lamp) are
scored as wrong for that component rather than failing the whole submission.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

W_WIRE = 0.55
W_QUERY = 0.45
MAX_JSON_LEN = 20000   # generous cap (real wiring/flip JSON is a few hundred chars)
MAX_TOKEN_LEN = 32
VALID_GATES = {"BUF", "NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR"}

SUB_COLS = ["id", "wiring_json", "query_pattern", "confidence"]
ANS_COLS = ["id", "wiring_json", "query_pattern", "n_lamps",
            "split_group", "ood_axis", "render_style"]


def _finite_float(v):
    s = str(v)
    if len(s) > MAX_TOKEN_LEN:
        raise ValueError("oversized")
    x = float(v)
    if not np.isfinite(x):
        raise ValueError("non-finite")
    return x


def _load_json(cell):
    s = str(cell)
    if len(s) > MAX_JSON_LEN:
        raise ValueError("oversized json")
    return json.loads(s)


def _f1(pred: set, gold: set) -> float:
    # a lamp with no inputs is correctly recovered only by predicting no inputs.
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    tp = len(pred & gold)
    if tp == 0:
        return 0.0
    p = tp / len(pred)
    r = tp / len(gold)
    return 2 * p * r / (p + r)


def _wire_score(pred_w, true_w) -> float:
    if not isinstance(pred_w, dict):
        return 0.0
    scores = []
    for lamp, tw in true_w.items():
        pw = pred_w.get(lamp)
        if not isinstance(pw, dict):
            scores.append(0.0)
            continue
        try:
            pgate = str(pw.get("gate", "")).strip().upper()
            pin = set(int(i) for i in pw.get("inputs", []))
        except (TypeError, ValueError):
            scores.append(0.0)
            continue
        gate_match = 1.0 if (pgate in VALID_GATES and pgate == tw["gate"]) else 0.0
        scores.append(gate_match * _f1(pin, set(tw["inputs"])))
    return float(np.mean(scores)) if scores else 0.0


def _query_score(pred_q, true_q) -> float:
    if not isinstance(pred_q, list) or len(pred_q) != len(true_q):
        return 0.0
    agree = 0
    for p, t in zip(pred_q, true_q):
        pv = 1 if (p == 1 or str(p).strip() == "1") else 0
        agree += int(pv == int(t))
    return agree / len(true_q)


def _worst_group(rows: np.ndarray, keys: list) -> float:
    by: dict = {}
    for r, k in zip(rows, keys):
        by.setdefault(k, []).append(r)
    return min(float(np.mean(v)) for v in by.values()) if by else 0.0


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        if not set(SUB_COLS).issubset(submission.columns):
            return 0.0
        if not set(ANS_COLS).issubset(answers.columns):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(str)
            ans["id"] = ans["id"].astype(str)
        except (TypeError, ValueError):
            return 0.0

        if sub["id"].duplicated().any():
            return 0.0
        if set(sub["id"]) != set(ans["id"]):
            return 0.0

        sub = sub.set_index("id")
        rows = np.empty(len(ans), dtype=float)
        split_keys, ood_keys, style_keys = [], [], []

        for i, arow in enumerate(ans.itertuples(index=False)):
            a = arow._asdict()
            srow = sub.loc[a["id"]]

            true_w = _load_json(a["wiring_json"])
            true_q = _load_json(a["query_pattern"])
            pred_w = _load_json(srow["wiring_json"])
            pred_q = _load_json(srow["query_pattern"])

            s_wire = _wire_score(pred_w, true_w)
            s_query = _query_score(pred_q, true_q)

            conf = _finite_float(srow["confidence"])
            if not (0.0 <= conf <= 1.0):
                return 0.0

            correctness = W_WIRE * s_wire ** 2 + W_QUERY * s_query ** 2
            rows[i] = 0.90 * correctness + 0.10 * (1.0 - abs(conf - correctness))
            split_keys.append(str(a["split_group"]))
            ood_keys.append(str(a["ood_axis"]))
            style_keys.append(str(a["render_style"]))

        final = (
            0.68 * float(np.mean(rows))
            + 0.14 * _worst_group(rows, split_keys)
            + 0.10 * _worst_group(rows, ood_keys)
            + 0.08 * _worst_group(rows, style_keys)
        )
        return float(np.clip(final, 0.0, 1.0))

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
