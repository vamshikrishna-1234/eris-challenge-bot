"""Grader: Rail Corridor Incident And Dispatch Ledger Recovery.

Submission : CSV with columns case_id, ledger_json
Answers    : CSV with columns case_id, ledger_json
Score      : mean per-case score in [0, 1]; a perfect submission scores exactly 1.0.
"""
import json
import pandas as pd

INCIDENT_TYPES = ("SPEED_RESTRICTION", "SEGMENT_BLOCKAGE", "STATION_DWELL_FAULT",
                  "UNIT_FAULT", "CREW_LATE")
INTERV_TYPES = ("HOLD", "SHORT_TURN", "CANCEL")
PRIMARY_CLASSES = ("NONE", "SPEED_RESTRICTION", "SEGMENT_BLOCKAGE", "STATION_DWELL_FAULT",
                   "UNIT_FAULT", "CREW_LATE", "SHORT_TURNED", "CANCELLED")

MAX_INCIDENTS = 12
MAX_INTERVENTIONS = 120
MAX_TRAINS = 80
MAX_JSON_CHARS = 20000

W_INCIDENT, W_INTERVENTION, W_PRIMARY = 0.50, 0.25, 0.25


# ---------------------------------------------------------------- assignment
def _hungarian_max(matrix):
    """Maximum-weight assignment on a rectangular non-negative matrix (O(n^2 m))."""
    if not matrix or not matrix[0]:
        return 0.0
    n, m = len(matrix), len(matrix[0])
    transposed = n > m
    if transposed:
        matrix = [[matrix[i][j] for i in range(n)] for j in range(m)]
        n, m = m, n
    INF = float("inf")
    cost = [[-matrix[i][j] for j in range(m)] for i in range(n)]
    u = [0.0] * (n + 1)
    v = [0.0] * (m + 1)
    p = [0] * (m + 1)
    way = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0
            for j in range(1, m + 1):
                if used[j]:
                    continue
                cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j] = cur
                    way[j] = j0
                if minv[j] < delta:
                    delta = minv[j]
                    j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    total = 0.0
    for j in range(1, m + 1):
        if p[j] > 0:
            total += matrix[p[j] - 1][j - 1]
    return float(total)


def _bucket_credit(a, b):
    d = abs(int(a) - int(b))
    return 1.0 if d == 0 else (0.5 if d == 1 else 0.0)


def _locality(a, b):
    """An incident report is only useful where it is placed, so location gates the credit."""
    d = abs(int(a) - int(b))
    return 1.0 if d == 0 else (0.40 if d == 1 else 0.10)


def _incident_credit(t, p):
    return _locality(t["loc"], p["loc"]) * (
        0.45 * float(t["type"] == p["type"])
        + 0.35 * _bucket_credit(t["start_bucket"], p["start_bucket"])
        + 0.20 * _bucket_credit(t["dur_band"], p["dur_band"]))


def _interv_credit(t, p):
    same = 1.0 if int(t["train"]) == int(p["train"]) else 0.10
    return same * (0.60 * float(t["type"] == p["type"])
                   + 0.40 * _bucket_credit(t["stop"], p["stop"]))


def _soft_f1(truth, pred, credit):
    if not truth and not pred:
        return 1.0
    if not truth or not pred:
        return 0.0
    matrix = [[credit(t, p) for p in pred] for t in truth]
    return 2.0 * _hungarian_max(matrix) / float(len(truth) + len(pred))


def _macro_recall(true_labels, pred_labels):
    classes = sorted(set(true_labels))
    if not classes:
        return 1.0
    total = 0.0
    for c in classes:
        idx = [i for i, x in enumerate(true_labels) if x == c]
        hit = sum(1 for i in idx if i < len(pred_labels) and pred_labels[i] == c)
        total += hit / float(len(idx))
    return total / float(len(classes))


# ---------------------------------------------------------------- validation
def _clean_incidents(raw, n_stations, n_trains):
    out = []
    if not isinstance(raw, list):
        return out
    for item in raw[:MAX_INCIDENTS]:
        if not isinstance(item, dict):
            continue
        t = item.get("type")
        if t not in INCIDENT_TYPES:
            continue
        try:
            loc = int(item.get("loc"))
            sb = int(item.get("start_bucket"))
            db = int(item.get("dur_band"))
        except (TypeError, ValueError):
            continue
        limit = n_trains if t in ("UNIT_FAULT", "CREW_LATE") else n_stations
        if not (0 <= loc < max(1, limit)) or not (0 <= sb <= 200) or not (0 <= db <= 4):
            continue
        out.append({"type": t, "loc": loc, "start_bucket": sb, "dur_band": db})
    return out


def _clean_interventions(raw, n_stations, n_trains):
    out = []
    if not isinstance(raw, list):
        return out
    for item in raw[:MAX_INTERVENTIONS]:
        if not isinstance(item, dict):
            continue
        t = item.get("type")
        if t not in INTERV_TYPES:
            continue
        try:
            tr = int(item.get("train"))
            st = int(item.get("stop"))
        except (TypeError, ValueError):
            continue
        if not (0 <= tr < max(1, n_trains)) or not (0 <= st < max(1, n_stations)):
            continue
        out.append({"type": t, "train": tr, "stop": st})
    seen = set()
    uniq = []
    for item in out:
        key = (item["type"], item["train"], item["stop"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(item)
    return uniq


def _clean_primary(raw, n_trains):
    out = ["NONE"] * n_trains
    if isinstance(raw, list):
        for i, x in enumerate(raw[:n_trains]):
            if isinstance(x, str) and x in PRIMARY_CLASSES:
                out[i] = x
    return out


def _parse(cell, n_stations, n_trains):
    if not isinstance(cell, str) or len(cell) > MAX_JSON_CHARS:
        return None
    try:
        obj = json.loads(cell)
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    return {
        "incidents": _clean_incidents(obj.get("incidents"), n_stations, n_trains),
        "interventions": _clean_interventions(obj.get("interventions"), n_stations, n_trains),
        "primary": _clean_primary(obj.get("primary"), n_trains),
    }


def _case_score(truth, pred):
    if pred is None:
        return 0.0
    a = _soft_f1(truth["incidents"], pred["incidents"], _incident_credit)
    b = _soft_f1(truth["interventions"], pred["interventions"], _interv_credit)
    c = _macro_recall(truth["primary"], pred["primary"])
    return W_INCIDENT * a + W_INTERVENTION * b + W_PRIMARY * c


def grade(submission_file, answer_file):
    try:
        sub = pd.read_csv(submission_file, dtype={"case_id": str})
        ans = pd.read_csv(answer_file, dtype={"case_id": str})
    except Exception:
        return 0.0
    for frame, cols in ((sub, ("case_id", "ledger_json")), (ans, ("case_id", "ledger_json"))):
        for c in cols:
            if c not in frame.columns:
                return 0.0
    if sub["case_id"].duplicated().any():
        return 0.0
    if set(sub["case_id"]) != set(ans["case_id"]):
        return 0.0

    lookup = dict(zip(sub["case_id"], sub["ledger_json"]))
    total = 0.0
    for case_id, cell in zip(ans["case_id"], ans["ledger_json"]):
        try:
            truth = json.loads(cell)
        except Exception:
            return 0.0
        n_trains = min(MAX_TRAINS, len(truth.get("primary", [])))
        n_stations = int(truth.get("n_stations", 60))
        pred = _parse(lookup.get(case_id), n_stations, n_trains)
        try:
            total += _case_score(truth, pred)
        except Exception:
            total += 0.0
    score = total / float(len(ans)) if len(ans) else 0.0
    if score != score or score in (float("inf"), float("-inf")):
        return 0.0
    return float(min(1.0, max(0.0, score)))
