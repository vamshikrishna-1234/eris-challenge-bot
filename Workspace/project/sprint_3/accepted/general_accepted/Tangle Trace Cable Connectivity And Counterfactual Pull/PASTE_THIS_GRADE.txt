import json

import numpy as np
import pandas as pd

# correctness heads (sum to 1.0). The counterfactual pull (outcome + the ORDERED
# taut cascade) carries 0.60 of the weight; the cascade head alone is dominant at
# 0.40 because it requires tracing the whole under/over contact graph and ordering
# the chain - something no single-frame read or local cue provides.
W_PAIR = 0.20      # endpoint-pairing permutation (with "unknown" for buried cables)
W_LOCK = 0.10      # count of genuine interlocks (clasps) vs illusory crossings
W_PULL = 0.22      # COUNTERFACTUAL: pulled endpoint locks / slips / unknown
W_CASC = 0.48      # COUNTERFACTUAL cascade: ordered list of cables dragged taut

W_CALIB = 0.10     # calibration share of the row score (correctness gets 0.90)

# robustness aggregation (sum to 1.0)
W_MEAN = 0.68
W_WORST_SPLIT = 0.14
W_WORST_OOD = 0.10
W_WORST_STYLE = 0.08

MAX_JSON_LEN = 4000
MAX_ITEMS = 32

PULL_CLASSES = {"locks", "slips", "unknown"}
SUBMISSION_COLUMNS = ["id", "pairing_json", "n_true_locks", "pull_outcome",
                      "pull_taut_json", "confidence"]


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


def _norm(v):
    return str(v).strip().lower()


def _parse_obj(v):
    s = str(v).strip()
    if len(s) > MAX_JSON_LEN:
        return None
    try:
        d = json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(d, dict) or len(d) > MAX_ITEMS:
        return None
    return {str(k).strip().lower(): str(val).strip().lower() for k, val in d.items()}


def _parse_list(v):
    s = str(v).strip()
    if len(s) > MAX_JSON_LEN:
        return None
    try:
        lst = json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(lst, list) or len(lst) > MAX_ITEMS:
        return None
    return [str(x).strip().lower() for x in lst]


def _int_or(v, default):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return default
    if not np.isfinite(x):
        return default
    return int(round(x))


def _nonneg_int_or_none(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(x):
        return None
    if abs(x - round(x)) > 1e-9:
        return None
    x = int(round(x))
    if x < 0:
        return None
    return x


def _s_pair(pred_d, true_d):
    if true_d is None or len(true_d) == 0:
        return 0.0
    if pred_d is None:
        return 0.0
    correct = sum(1 for k, tv in true_d.items() if pred_d.get(k) == tv)
    return correct / len(true_d)


def _s_lock(pred_n, true_n):
    if pred_n is None:
        return 0.0
    return max(0.0, 1.0 - abs(pred_n - true_n) / 2.0)


def _s_casc(pred_l, true_l):
    """Ordered-cascade similarity: half set-F1, half ordered-prefix agreement.
    When the true cascade is empty (buried/unknown query), only an empty
    prediction earns credit."""
    if true_l is None or pred_l is None:
        return 0.0
    if len(true_l) == 0:
        return 1.0 if len(pred_l) == 0 else 0.0
    tset, pset = set(true_l), set(pred_l)
    tp = len(tset & pset)
    prec = tp / len(pset) if pset else 0.0
    rec = tp / len(tset) if tset else 0.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    prefix = 0
    for a, b in zip(pred_l, true_l):
        if a == b:
            prefix += 1
        else:
            break
    return 0.5 * f1 + 0.5 * (prefix / len(true_l))


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
        req_ans = {"id", "pairing_json", "n_true_locks", "pull_outcome",
                   "pull_taut_json"}
        if list(submission.columns) != SUBMISSION_COLUMNS:
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
        have_style = "render_style" in ans.columns

        for _, arow in ans.iterrows():
            srow = sub_by_id[int(arow["id"])]

            conf = _coerce_conf(srow["confidence"])
            if conf is None:
                return 0.0

            s_pair = _s_pair(_parse_obj(srow["pairing_json"]), _parse_obj(arow["pairing_json"]))
            pred_locks = _nonneg_int_or_none(srow["n_true_locks"])
            if pred_locks is None:
                return 0.0
            s_lock = _s_lock(pred_locks, _int_or(arow["n_true_locks"], 0))

            true_pull = _norm(arow["pull_outcome"])
            pred_pull = _norm(srow["pull_outcome"])
            s_pull = 1.0 if (pred_pull in PULL_CLASSES and pred_pull == true_pull) else 0.0

            # When the pulled cable is buried, the cascade is unanswerable: credit
            # is given only for correctly recognising it (pull_outcome == unknown),
            # not for a blanket empty list. Otherwise score the ordered cascade.
            if true_pull == "unknown":
                s_casc = 1.0 if pred_pull == "unknown" else 0.0
            else:
                s_casc = _s_casc(_parse_list(srow["pull_taut_json"]),
                                 _parse_list(arow["pull_taut_json"]))

            correctness = (W_PAIR * s_pair + W_LOCK * s_lock
                           + W_PULL * s_pull + W_CASC * s_casc)
            calib = 1.0 - abs(conf - correctness)
            row = (1.0 - W_CALIB) * correctness + W_CALIB * calib
            row_scores.append(row)

            if have_split:
                split_g.append(arow["split_group"])
            if have_ood:
                ood_g.append(arow["ood_axis"])
            if have_style:
                style_g.append(arow["render_style"])

        if not row_scores:
            return 0.0

        mean_row = float(np.mean(row_scores))
        w_split = _worst_group(row_scores, split_g if have_split else None)
        w_ood = _worst_group(row_scores, ood_g if have_ood else None)
        w_style = _worst_group(row_scores, style_g if have_style else None)

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
