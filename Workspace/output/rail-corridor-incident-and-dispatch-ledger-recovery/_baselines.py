"""Baseline suite on the real prepared split, scored with the canonical grader."""
import collections, json, os, sys, tempfile, time
os.environ.setdefault("OMP_NUM_THREADS", "3")
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade as G

ANS = "private/answers.csv"
train = pd.read_csv("public/train.csv", dtype={"case_id": str})
test = pd.read_csv("public/test.csv", dtype={"case_id": str})
tans = pd.read_csv("public/train_answers.csv", dtype={"case_id": str})
truth_train = {c: json.loads(x) for c, x in zip(tans.case_id, tans.ledger_json)}
RES = {}


def bundle(frame):
    out = {}
    for cid, g in frame.groupby("case_id", sort=True):
        g = g.sort_values(["train_slot", "stop_seq"])
        rows = collections.defaultdict(list)
        for r in g.itertuples(index=False):
            rows[r.train_slot].append(r)
        out[cid] = dict(rows=rows, n_stations=int(g.n_stations.iloc[0]),
                        n_trains=int(g.n_trains.iloc[0]),
                        cls=dict(zip(g.train_slot, g.service_class)),
                        dirn=dict(zip(g.train_slot, g.direction)))
    return out


TRB, TEB = bundle(train), bundle(test)


def score(predfn, label):
    rows = [(cid, json.dumps(predfn(cid, TEB[cid]))) for cid in sorted(TEB)]
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    pd.DataFrame(rows, columns=["case_id", "ledger_json"]).to_csv(fh.name, index=False)
    s = G.grade(fh.name, ANS)
    RES[label] = float(s)
    print("%-44s %.4f" % (label, s), flush=True)
    return s


# ---- floors ---------------------------------------------------------------
score(lambda cid, b: {"incidents": [], "interventions": [], "primary": ["NONE"] * b["n_trains"]},
      "F0 chance floor (empty / all-NONE)")
RES["F1 label prior (shipped sample)"] = float(G.grade("public/sample_submission.csv", ANS))
print("%-44s %.4f" % ("F1 label prior (shipped sample)", RES["F1 label prior (shipped sample)"]), flush=True)

# ---- metadata-only attack (no realized times at all) ----------------------
cnt = collections.Counter(i["type"] for l in truth_train.values() for i in l["incidents"])
modal = cnt.most_common(1)[0][0]
starts = sorted(i["start_bucket"] for l in truth_train.values() for i in l["incidents"])
bands = sorted(i["dur_band"] for l in truth_train.values() for i in l["incidents"])
sb, db = starts[len(starts) // 2], bands[len(bands) // 2]
score(lambda cid, b: {"incidents": [{"type": modal, "loc": (b["n_stations"] - 1) // 2,
                                     "start_bucket": int(sb), "dur_band": int(db)}],
                      "interventions": [],
                      "primary": ["NONE"] * b["n_trains"]},
      "A1 metadata-only (plan + structure only)")


# ---- domain rule / DSP baseline ------------------------------------------
def rule(cid, b):
    inc, iv = [], []
    prim = ["NONE"] * b["n_trains"]
    exc, dwl = collections.defaultdict(list), collections.defaultdict(list)
    for i, rs in b["rows"].items():
        for a, c in zip(rs, rs[1:]):
            if np.isnan(a.observed_dep) or np.isnan(c.observed_arr) or np.isnan(c.planned_arr):
                continue
            exc[min(a.station_index, c.station_index)].append(
                ((c.observed_arr - a.observed_dep) - (c.planned_arr - a.planned_dep), a.observed_dep))
        d = [r.observed_arr - r.planned_arr for r in rs
             if not np.isnan(r.observed_arr) and not np.isnan(r.planned_arr)]
        if not d or all(np.isnan(r.observed_dep) and np.isnan(r.observed_arr) for r in rs):
            iv.append({"type": "CANCEL", "train": int(i), "stop": int(rs[0].station_index)})
            prim[i] = "CANCELLED"
            continue
        if max(d) > 25:
            prim[i] = "SHORT_TURNED"
            iv.append({"type": "SHORT_TURN", "train": int(i), "stop": int(rs[-1].station_index)})
        for r in rs:
            if not np.isnan(r.observed_dep) and r.observed_dep - r.planned_dep > 6:
                iv.append({"type": "HOLD", "train": int(i), "stop": int(r.station_index)})
            if np.isnan(r.observed_arr) or np.isnan(r.observed_dep) or np.isnan(r.planned_arr):
                continue
            dwl[r.station_index].append(
                ((r.observed_dep - r.observed_arr) - (r.planned_dep - r.planned_arr), r.observed_arr))
    if exc:
        seg = max(exc, key=lambda k: sum(max(0.0, e) for e, _ in exc[k]))
        bad = [t for e, t in exc[seg] if e > 3]
        if bad:
            span = (max(bad) - min(bad)) if len(bad) > 1 else 20
            inc.append({"type": "SPEED_RESTRICTION", "loc": int(seg), "start_bucket": int(min(bad) // 10),
                        "dur_band": int(np.searchsorted([10, 20, 35, 60], span))})
            for i, rs in b["rows"].items():
                for a, c in zip(rs, rs[1:]):
                    if min(a.station_index, c.station_index) == seg and not np.isnan(c.observed_arr) \
                       and not np.isnan(c.planned_arr) and c.observed_arr - c.planned_arr > 6 and prim[i] == "NONE":
                        prim[i] = "SPEED_RESTRICTION"
    if dwl:
        stn = max(dwl, key=lambda k: sum(max(0.0, e) for e, _ in dwl[k]))
        bad = [t for e, t in dwl[stn] if e > 4]
        if bad:
            span = (max(bad) - min(bad)) if len(bad) > 1 else 20
            inc.append({"type": "STATION_DWELL_FAULT", "loc": int(stn), "start_bucket": int(min(bad) // 10),
                        "dur_band": int(np.searchsorted([10, 20, 35, 60], span))})
    return {"incidents": inc, "interventions": iv, "primary": prim}


score(rule, "B1 domain rule / DSP baseline")


# ---- capability-matched learned baseline ---------------------------------
def stat(v):
    if not v:
        return [0, 0, 0, 0, 0, 0]
    a = np.asarray(v, float)
    return [len(a), a.mean(), a.max(), a.min(), np.percentile(a, 75), float((a > 3).sum())]


CLS = {"Long-distance": 0, "Commuter": 1, "Cargo": 2}
PRIM = {"NONE": 0, "SPEED_RESTRICTION": 1, "SEGMENT_BLOCKAGE": 2, "STATION_DWELL_FAULT": 3,
        "UNIT_FAULT": 4, "CREW_LATE": 5, "SHORT_TURNED": 6, "CANCELLED": 7}
INV = {v: k for k, v in PRIM.items()}


def feats(b):
    L = b["n_stations"]
    segE, segT = collections.defaultdict(list), collections.defaultdict(list)
    staD, staT, trD = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    for i, rs in b["rows"].items():
        for a, c in zip(rs, rs[1:]):
            if np.isnan(a.observed_dep) or np.isnan(c.observed_arr) or np.isnan(c.planned_arr):
                continue
            s = min(a.station_index, c.station_index)
            segE[s].append((c.observed_arr - a.observed_dep) - (c.planned_arr - a.planned_dep))
            segT[s].append(a.observed_dep)
        for r in rs:
            if not np.isnan(r.observed_arr) and not np.isnan(r.planned_arr):
                trD[i].append(r.observed_arr - r.planned_arr)
            if np.isnan(r.observed_arr) or np.isnan(r.observed_dep) or np.isnan(r.planned_arr):
                continue
            staD[r.station_index].append((r.observed_dep - r.observed_arr) - (r.planned_dep - r.planned_arr))
            staT[r.station_index].append(r.observed_arr)
    seg, sta, tra = [], [], []
    for s in range(L - 1):
        bad = [t for e, t in zip(segE[s], segT[s]) if e > 3]
        seg.append(stat(segE[s]) + [len(bad), min(bad) if bad else -1, max(bad) if bad else -1,
                                    (max(bad) - min(bad)) if len(bad) > 1 else 0, s, L])
    for s in range(L):
        bad = [t for e, t in zip(staD[s], staT[s]) if e > 4]
        sta.append(stat(staD[s]) + [len(bad), min(bad) if bad else -1, max(bad) if bad else -1,
                                    (max(bad) - min(bad)) if len(bad) > 1 else 0, s, L])
    for i in range(b["n_trains"]):
        rs = b["rows"].get(i, [])
        d = trD.get(i, [])
        nmiss = sum(1 for r in rs if np.isnan(r.observed_arr) and np.isnan(r.observed_dep))
        hold = sum(1 for r in rs if not np.isnan(r.observed_dep) and r.observed_dep - r.planned_dep > 6)
        tra.append(stat(d) + [len(rs), nmiss, hold, CLS.get(b["cls"].get(i), 1), b["dirn"].get(i, 0),
                              (d[-1] - d[0]) if len(d) > 1 else 0, L, b["n_trains"]])
    return np.array(seg, float), np.array(sta, float), np.array(tra, float)


def labels(b, led):
    L = b["n_stations"]
    segY, segS, segD = np.zeros(L - 1, int), -np.ones(L - 1, int), -np.ones(L - 1, int)
    staY, staS, staDd = np.zeros(L, int), -np.ones(L, int), -np.ones(L, int)
    traY, traS, traD = np.zeros(b["n_trains"], int), -np.ones(b["n_trains"], int), -np.ones(b["n_trains"], int)
    for i in led["incidents"]:
        t, loc = i["type"], i["loc"]
        if t == "SPEED_RESTRICTION":
            segY[loc], segS[loc], segD[loc] = 1, i["start_bucket"], i["dur_band"]
        elif t == "SEGMENT_BLOCKAGE":
            segY[loc], segS[loc], segD[loc] = 2, i["start_bucket"], i["dur_band"]
        elif t == "STATION_DWELL_FAULT":
            staY[loc], staS[loc], staDd[loc] = 1, i["start_bucket"], i["dur_band"]
        elif t == "UNIT_FAULT":
            traY[loc], traS[loc], traD[loc] = 1, i["start_bucket"], i["dur_band"]
        else:
            traY[loc], traS[loc], traD[loc] = 2, i["start_bucket"], i["dur_band"]
    return (segY, segS, segD), (staY, staS, staDd), (traY, traS, traD)


from sklearn.ensemble import HistGradientBoostingClassifier as HGB
X = {"seg": [], "sta": [], "tra": []}
Y = {k: {"y": [], "s": [], "d": []} for k in X}
PY = []
t0 = time.time()
for cid in sorted(TRB):
    b = TRB[cid]
    f = feats(b)
    l = labels(b, truth_train[cid])
    for k, j in zip(["seg", "sta", "tra"], range(3)):
        X[k].append(f[j])
        Y[k]["y"].append(l[j][0]); Y[k]["s"].append(l[j][1]); Y[k]["d"].append(l[j][2])
    PY.append(np.array([PRIM[p] for p in truth_train[cid]["primary"]]))
for k in X:
    X[k] = np.vstack(X[k])
    for q in Y[k]:
        Y[k][q] = np.concatenate(Y[k][q])
PY = np.concatenate(PY)
print("featurised train in %.1fs" % (time.time() - t0), flush=True)

M = {}
for k in ["seg", "sta", "tra"]:
    M[k] = {"y": HGB(max_iter=110, learning_rate=0.12, random_state=0, early_stopping=False).fit(X[k], Y[k]["y"])}
    m = Y[k]["y"] > 0
    for q in ["s", "d"]:
        M[k][q] = (HGB(max_iter=70, learning_rate=0.12, random_state=0, early_stopping=False)
                   .fit(X[k][m], Y[k][q][m])) if m.sum() > 50 else None
    print("fit %s" % k, flush=True)
Mp = HGB(max_iter=120, learning_rate=0.12, random_state=0, early_stopping=False).fit(X["tra"], PY)
print("fit primary", flush=True)


def gbm(cid, b):
    fseg, fsta, ftra = feats(b)
    out = []
    for k, F, kinds in [("seg", fseg, {1: "SPEED_RESTRICTION", 2: "SEGMENT_BLOCKAGE"}),
                        ("sta", fsta, {1: "STATION_DWELL_FAULT"}),
                        ("tra", ftra, {1: "UNIT_FAULT", 2: "CREW_LATE"})]:
        pr = M[k]["y"].predict_proba(F)
        cls = M[k]["y"].classes_
        pick = cls[np.argmax(pr, axis=1)]
        hot = np.nonzero(pick != 0)[0]
        if len(hot) == 0:
            continue
        sb_all = M[k]["s"].predict(F[hot]) if M[k]["s"] is not None else np.zeros(len(hot))
        db_all = M[k]["d"].predict(F[hot]) if M[k]["d"] is not None else np.full(len(hot), 2)
        for n, loc in enumerate(hot):
            out.append({"type": kinds[int(pick[loc])], "loc": int(loc),
                        "start_bucket": max(0, int(sb_all[n])), "dur_band": max(0, int(db_all[n]))})
    prim = [INV[int(x)] for x in Mp.predict(ftra)]
    iv = []
    for i, rs in b["rows"].items():
        if all(np.isnan(r.observed_dep) and np.isnan(r.observed_arr) for r in rs):
            iv.append({"type": "CANCEL", "train": int(i), "stop": int(rs[0].station_index)})
            continue
        if prim[i] == "SHORT_TURNED":
            iv.append({"type": "SHORT_TURN", "train": int(i), "stop": int(rs[-1].station_index)})
        for r in rs:
            if not np.isnan(r.observed_dep) and r.observed_dep - r.planned_dep > 6:
                iv.append({"type": "HOLD", "train": int(i), "stop": int(r.station_index)})
    return {"incidents": out, "interventions": iv, "primary": prim}


score(gbm, "C1 capability-matched GBM")
RES["oracle"] = float(G.grade(ANS, ANS))
print("%-44s %.4f" % ("oracle", RES["oracle"]), flush=True)
json.dump(RES, open("BASELINE_RESULTS.json", "w"), indent=1)
print("wrote BASELINE_RESULTS.json", flush=True)


# ---- achievable ceiling ---------------------------------------------------
# Same hidden incident programs, same dispatching, but a noise-free and
# dropout-free observation channel. Scoring the same trained solver there bounds
# what any solver could extract from this observation channel.
import random, importlib
import prepare as P
P.NOISE_SCALE = 0.0
P.OBS_DROPOUT = 0.0
raw = P.find_raw()
days = P.load_days(raw)
counter = P.segment_traffic(days)
subs = []
for corr in P.corridors_from(counter, len(days)):
    runs = P.corridor_runs(days, corr)
    if len(runs) < P.MIN_RUNS_PER_CORRIDOR:
        continue
    subs.append({"corr": corr, "runs": runs,
                 "single": [counter[tuple(sorted((corr[i], corr[i + 1])))] / len(days) < 25
                            for i in range(len(corr) - 1)]})
sp = random.Random(P.SEED_SPLIT)
order = list(range(len(subs)))
sp.shuffle(order)
test_ids = sorted(order[int(round(len(order) * 0.6)):])
clean = P.generate_cases(subs, test_ids, P.N_TEST_CASES, P.SEED_TEST, "TE")
clean_obs = P.observation_frame(clean)
clean_ans = P.ledger_frame(clean)
fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
clean_ans.to_csv(fh.name, index=False)
CB = bundle(clean_obs)
rows = [(cid, json.dumps(gbm(cid, CB[cid]))) for cid in sorted(CB)]
fp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
pd.DataFrame(rows, columns=["case_id", "ledger_json"]).to_csv(fp.name, index=False)
ceiling = G.grade(fp.name, fh.name)
RES["D1 achievable ceiling (clean channel)"] = float(ceiling)
print("%-44s %.4f" % ("D1 achievable ceiling (clean channel)", ceiling), flush=True)
RES["headroom_ceiling_minus_capability"] = float(ceiling - RES["C1 capability-matched GBM"])
RES["headroom_capability_minus_floor"] = float(RES["C1 capability-matched GBM"] - RES["F0 chance floor (empty / all-NONE)"])
print("ceiling - capability = %.4f   capability - floor = %.4f"
      % (RES["headroom_ceiling_minus_capability"], RES["headroom_capability_minus_floor"]), flush=True)
json.dump(RES, open("BASELINE_RESULTS.json", "w"), indent=1)
print("wrote BASELINE_RESULTS.json", flush=True)
