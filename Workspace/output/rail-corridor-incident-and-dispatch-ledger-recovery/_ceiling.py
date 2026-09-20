"""Achievable ceiling: the best score any predictor could reach that never sees the
scored answer, bounded by what the published observation channel can carry.

An incident that left no trace in the published rows cannot be reported by any solver,
yet the grader still counts it as missed. Scoring the truth with those unobservable
entries removed is therefore an upper bound on the achievable score.
"""
import collections, json, sys, tempfile
import numpy as np, pandas as pd
sys.path.insert(0, ".")
import grade as G

BAND_MID = {0: 5.0, 1: 15.0, 2: 27.5, 3: 47.5, 4: 80.0}
test = pd.read_csv("public/test.csv", dtype={"case_id": str})
ans = pd.read_csv("private/answers.csv", dtype={"case_id": str})

by_case = {}
for cid, g in test.groupby("case_id", sort=True):
    g = g.sort_values(["train_slot", "stop_seq"])
    rows = collections.defaultdict(list)
    for r in g.itertuples(index=False):
        rows[r.train_slot].append(r)
    by_case[cid] = rows


def observable(inc, rows):
    a = inc["start_bucket"] * 10.0
    b = a + BAND_MID[inc["dur_band"]]
    t = inc["type"]
    if t in ("UNIT_FAULT", "CREW_LATE"):
        rs = rows.get(inc["loc"], [])
        return sum(1 for r in rs if not np.isnan(r.observed_arr) or not np.isnan(r.observed_dep)) >= 2
    if t == "STATION_DWELL_FAULT":
        for rs in rows.values():
            for r in rs:
                if r.station_index == inc["loc"] and not np.isnan(r.observed_arr) \
                   and not np.isnan(r.observed_dep) and a - 15 <= r.observed_arr <= b + 15:
                    return True
        return False
    for rs in rows.values():
        for x, y in zip(rs, rs[1:]):
            if min(x.station_index, y.station_index) != inc["loc"]:
                continue
            if np.isnan(x.observed_dep) or np.isnan(y.observed_arr):
                continue
            if a - 15 <= x.observed_dep <= b + 15:
                return True
    return False


def interv_observable(iv, rows):
    rs = rows.get(iv["train"], [])
    if not rs:
        return False
    seen = sum(1 for r in rs if not np.isnan(r.observed_arr) or not np.isnan(r.observed_dep))
    if iv["type"] == "CANCEL":
        return True
    return seen >= 2


kept_i = dropped_i = kept_v = dropped_v = 0
rows_out = []
for cid, cell in zip(ans.case_id, ans.ledger_json):
    t = json.loads(cell)
    rows = by_case[cid]
    inc = []
    for i in t["incidents"]:
        if observable(i, rows):
            inc.append(i); kept_i += 1
        else:
            dropped_i += 1
    iv = []
    for v in t["interventions"]:
        if interv_observable(v, rows):
            iv.append(v); kept_v += 1
        else:
            dropped_v += 1
    rows_out.append((cid, json.dumps({"incidents": inc, "interventions": iv, "primary": t["primary"]})))

fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
pd.DataFrame(rows_out, columns=["case_id", "ledger_json"]).to_csv(fh.name, index=False)
score = G.grade(fh.name, "private/answers.csv")
out = {"observability_ceiling": float(score),
       "incidents_kept": kept_i, "incidents_unobservable": dropped_i,
       "interventions_kept": kept_v, "interventions_unobservable": dropped_v,
       "note": ("truth with entries that left no trace in the published rows removed; an upper bound "
                "on any predictor that never sees the scored answer")}
print(json.dumps(out, indent=1))
json.dump(out, open("CEILING_RESULTS.json", "w"), indent=1)
