import numpy as np
import pandas as pd

GRID = 12
N_CELLS = GRID * GRID

# correctness heads (sum to 1.0). Reconstructing the occupancy map is the core
# cross-frame inverse task and carries most of the weight; counting distinct
# obstacles and forecasting the query column are secondary heads.
W_MAP = 0.65
W_COUNT = 0.15
W_QUERY = 0.20

W_CALIB = 0.10        # calibration share of the row score (correctness gets 0.90)
COUNT_WIN = 4.0       # obstacle-count error at which credit -> 0
QUERY_WIN = 1.5       # query-row error scale (exponential decay)

# the occupancy field is exactly 144 chars; cap length before any work so a
# pathological multi-megabyte cell cannot stall the grader. Other answer fields
# are tiny ints.
MAX_OCC_LEN = 400

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


def _occ_bool(v):
    """Parse a 144-char 0/1 occupancy string into a bool array. Any malformed /
    wrong-length / over-long value degrades to all-empty (never crashes).

    CSV readers commonly load an all-digit field as an integer and drop leading
    zeros (the top rows are usually empty), so an all-digit value shorter than
    144 is left-padded back to 144 before parsing."""
    s = str(v).strip()
    if len(s) > MAX_OCC_LEN:
        return np.zeros(N_CELLS, dtype=bool)
    if s.isdigit() and len(s) < N_CELLS:
        s = s.zfill(N_CELLS)
    if len(s) != N_CELLS:
        return np.zeros(N_CELLS, dtype=bool)
    arr = np.zeros(N_CELLS, dtype=bool)
    for i, c in enumerate(s):
        if c == "1":
            arr[i] = True
        elif c != "0":
            return np.zeros(N_CELLS, dtype=bool)
    return arr


def _int_or(v, default):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return default
    if not np.isfinite(x):
        return default
    return int(round(x))


def _occ_f1(pred, true):
    """F1 (Dice) on the OCCUPIED class only. Predicting an all-empty map scores 0,
    so the head measures how well the hidden cells are actually recovered rather
    than rewarding the dominant empty background."""
    tp = int(np.sum(pred & true)); fp = int(np.sum(pred & ~true)); fn = int(np.sum(~pred & true))
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    if tp == 0:
        return 0.0
    prec = tp / (tp + fp); rec = tp / (tp + fn)
    return float(2 * prec * rec / (prec + rec))


def _s_query(pred, true):
    if pred is None:
        return 0.0
    if true == -1 and pred == -1:
        return 1.0
    if (true == -1) != (pred == -1):
        return 0.0
    return float(np.exp(-abs(pred - true) / QUERY_WIN))


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
        req_sub = {"id", "occupancy", "n_obstacles", "query_hit_row", "confidence"}
        req_ans = {"id", "occupancy", "n_obstacles", "query_hit_row"}
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
        have_style = "floor_style" in ans.columns

        for _, arow in ans.iterrows():
            srow = sub_by_id[int(arow["id"])]

            conf = _coerce_conf(srow["confidence"])
            if conf is None:
                return 0.0

            true_map = _occ_bool(arow["occupancy"])
            pred_map = _occ_bool(srow["occupancy"])
            s_map = _occ_f1(pred_map, true_map)

            true_n = _int_or(arow["n_obstacles"], 0)
            pred_n = _int_or(srow["n_obstacles"], None)
            if pred_n is None:
                s_count = 0.0
            else:
                s_count = max(0.0, 1.0 - abs(pred_n - true_n) / COUNT_WIN)

            true_q = _int_or(arow["query_hit_row"], -1)
            pred_q = _int_or(srow["query_hit_row"], None)
            s_query = _s_query(pred_q, true_q)

            correctness = W_MAP * s_map + W_COUNT * s_count + W_QUERY * s_query
            calib = 1.0 - abs(conf - correctness)
            row = (1.0 - W_CALIB) * correctness + W_CALIB * calib
            row_scores.append(row)

            if have_split:
                split_g.append(arow["split_group"])
            if have_ood:
                ood_g.append(arow["ood_axis"])
            if have_style:
                style_g.append(arow["floor_style"])

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
