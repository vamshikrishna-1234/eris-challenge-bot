import json

import numpy as np
import pandas as pd

# correctness heads (sum to 1.0). Recovering the hidden directed drive graph is
# the central reasoning task and carries the headroom; final-motion and the first
# mover are lighter perceptual anchors.
W_EDGES = 0.70
W_MOVING = 0.20
W_FIRST = 0.10

W_CALIB = 0.10        # calibration share of the row score (correctness gets 0.90)

# a valid edges / moving JSON for a <=7-rotor board is at most ~250 chars; cap
# the string length before parsing so a pathological multi-megabyte cell cannot
# stall the grader.
MAX_JSON_LEN = 2000

# robustness aggregation (sum to 1.0)
W_MEAN = 0.68
W_WORST_SPLIT = 0.14
W_WORST_OOD = 0.10
W_WORST_STYLE = 0.08


def _coerce_conf(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(x):
        return None
    if x < 0.0 or x > 1.0:
        return None
    return float(x)


def _norm_id(x):
    return str(x).strip().lower()


def _parse_list(cell):
    """Parse a JSON list cell -> list of normalised string ids. Malformed -> []."""
    if cell is None:
        return []
    if isinstance(cell, float) and not np.isfinite(cell):
        return []
    s = str(cell).strip()
    if s == "" or s.lower() in ("nan", "none", "[]") or len(s) > MAX_JSON_LEN:
        return []
    try:
        data = json.loads(s)
    except (ValueError, TypeError):
        return []
    if not isinstance(data, (list, tuple)):
        return []
    return [_norm_id(x) for x in data if _norm_id(x) != ""]


def _parse_edges(cell):
    """Parse edges -> set of (driver, driven) tuples. Malformed -> empty set."""
    if cell is None:
        return set()
    if isinstance(cell, float) and not np.isfinite(cell):
        return set()
    s = str(cell).strip()
    if s == "" or s.lower() in ("nan", "none", "[]") or len(s) > MAX_JSON_LEN:
        return set()
    try:
        data = json.loads(s)
    except (ValueError, TypeError):
        return set()
    if not isinstance(data, (list, tuple)):
        return set()
    out = set()
    for e in data:
        if isinstance(e, (list, tuple)) and len(e) == 2:
            a, b = _norm_id(e[0]), _norm_id(e[1])
            if a != "" and b != "" and a != b:
                out.add((a, b))
    return out


def _edge_f1(pred, true):
    if not pred and not true:
        return 1.0
    if not pred or not true:
        return 0.0
    inter = len(pred & true)
    prec = inter / len(pred)
    rec = inter / len(true)
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)


def _moving_score(pred_list, true_list, universe):
    """Per-rotor binary agreement over the full rotor set."""
    uni = set(universe)
    if not uni:
        uni = set(pred_list) | set(true_list)
        if not uni:
            return 1.0
    pset = set(pred_list) & uni
    tset = set(true_list) & uni
    correct = sum(1 for r in uni if (r in pset) == (r in tset))
    return correct / len(uni)


def _worst_group(rows, group_vals):
    if group_vals is None:
        return None
    buckets = {}
    for s, g in zip(rows, group_vals):
        buckets.setdefault(g, []).append(s)
    if not buckets:
        return None
    return min(float(np.mean(v)) for v in buckets.values())


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        req_sub = {"id", "edges_json", "moving_at_end_json", "first_mover", "confidence"}
        req_ans = {"id", "edges_json", "moving_at_end_json", "first_mover"}
        if not req_sub.issubset(set(submission.columns)):
            return 0.0
        if not req_ans.issubset(set(answers.columns)):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(int)
            ans["id"] = ans["id"].astype(int)
        except (TypeError, ValueError):
            return 0.0

        if sub["id"].duplicated().any():
            return 0.0
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            return 0.0

        sub_by_id = {int(r["id"]): r for _, r in sub.iterrows()}

        row_scores = []
        split_g, ood_g, style_g = [], [], []
        have_split = "split_group" in ans.columns
        have_ood = "ood_axis" in ans.columns
        have_style = "board_style" in ans.columns
        have_rotors = "rotors" in ans.columns

        for _, arow in ans.iterrows():
            srow = sub_by_id[int(arow["id"])]

            true_edges = _parse_edges(arow["edges_json"])
            true_moving = _parse_list(arow["moving_at_end_json"])
            true_first = _norm_id(arow["first_mover"])
            universe = _parse_list(arow["rotors"]) if have_rotors else []

            pred_edges = _parse_edges(srow["edges_json"])
            pred_moving = _parse_list(srow["moving_at_end_json"])
            pred_first = _norm_id(srow["first_mover"])
            conf = _coerce_conf(srow["confidence"])
            if conf is None:
                return 0.0

            e_s = _edge_f1(pred_edges, true_edges)
            m_s = _moving_score(pred_moving, true_moving, universe)
            f_s = 1.0 if pred_first == true_first and true_first != "" else 0.0
            correctness = W_EDGES * e_s + W_MOVING * m_s + W_FIRST * f_s
            calib = 1.0 - abs(conf - correctness)
            row = (1.0 - W_CALIB) * correctness + W_CALIB * calib
            row_scores.append(row)

            if have_split:
                split_g.append(arow["split_group"])
            if have_ood:
                ood_g.append(arow["ood_axis"])
            if have_style:
                style_g.append(arow["board_style"])

        if not row_scores:
            return 0.0

        mean_row = float(np.mean(row_scores))
        w_split = _worst_group(row_scores, split_g if have_split else None)
        w_ood = _worst_group(row_scores, ood_g if have_ood else None)
        w_style = _worst_group(row_scores, style_g if have_style else None)

        # if a worst-group axis is unavailable, fold its weight back into the mean
        total_w = W_MEAN
        acc = W_MEAN * mean_row
        if w_split is not None:
            acc += W_WORST_SPLIT * w_split; total_w += W_WORST_SPLIT
        if w_ood is not None:
            acc += W_WORST_OOD * w_ood; total_w += W_WORST_OOD
        if w_style is not None:
            acc += W_WORST_STYLE * w_style; total_w += W_WORST_STYLE
        final = acc / total_w
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", required=True)
    ap.add_argument("--answers", required=True)
    args = ap.parse_args()
    sub = pd.read_csv(args.submission)
    ans = pd.read_csv(args.answers)
    print(f"score={grade(sub, ans):.6f}")
