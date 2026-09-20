"""Rule-2 two-stage reversibility attack, measured at the shipped bundle size.

Stage 1  de-anonymise the shipped bundle (one case = one corridor-window bundle of
         whole trains) back to its real (corridor, date, window) in the public corpus.
Stage 2  with the origin known, re-attack the hidden ledger using the public corpus:
         the real recorded arrival/departure delays and the real official delay-cause
         records for exactly those trains and stops.
"""
import collections, datetime as dt, json, os, sys, tempfile
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prepare as P
import grade as G

OUT = {}
raw = P.find_raw()
days = P.load_days(raw)
counter = P.segment_traffic(days)
corrs = P.corridors_from(counter, len(days))
n_days = len(days)
subs = []
for corr in corrs:
    runs = P.corridor_runs(days, corr)
    if len(runs) < P.MIN_RUNS_PER_CORRIDOR:
        continue
    single = [counter[tuple(sorted((corr[i], corr[i + 1])))] / n_days < 25 for i in range(len(corr) - 1)]
    subs.append({"corr": corr, "runs": runs, "single": single})
import random
split = random.Random(P.SEED_SPLIT)
order = list(range(len(subs)))
split.shuffle(order)
cut = int(round(len(order) * 0.6))
test_ids = sorted(order[cut:])
cases = P.generate_cases(subs, test_ids, P.N_TEST_CASES, P.SEED_TEST, "TE")
print("regenerated %d shipped test bundles" % len(cases), flush=True)

obs = pd.read_csv("public/test.csv", dtype={"case_id": str})
bundle_rows = obs.groupby("case_id").size()
bundle_trains = obs.groupby("case_id").train_slot.nunique()
OUT["shipped_bundle"] = dict(unit="one case = one corridor-window bundle of whole trains",
                             median_rows=float(bundle_rows.median()),
                             median_trains=float(bundle_trains.median()),
                             n_bundles=int(obs.case_id.nunique()))

# ---------------- stage 1: de-anonymise the bundle ------------------------
# The published planned times are genuinely real, so a determined attacker who is willing
# to spend enough compute can align a shipped bundle back to its real corridor, date and
# window. We do not try to under-claim that: stage 1 is GRANTED to the attacker. Stage 2
# below is therefore run with the true origin handed over for free, which is strictly
# more conservative than any measured stage-1 success rate could be.
OUT["stage1_bundle_deanonymisation_rank1"] = 1.0
OUT["stage1_basis"] = ("granted to the attacker by construction; the published planned times are "
                       "real, so bundle-level de-anonymisation is assumed to succeed and stage 2 "
                       "receives the true corridor, date, window and service numbers for free")
print("STAGE 1  bundle de-anonymisation GRANTED = 1.0000 (worst case)  bundle ~%d rows, ~%d services"
      % (bundle_rows.median(), bundle_trains.median()), flush=True)

# ---------------- stage 2: re-attack with the origin known ----------------
real = {}
for date, trains in days.items():
    for t in trains:
        for row in t["timeTableRows"]:
            if row.get("differenceInMinutes") is None:
                continue
            real[(date, t["trainNumber"], row["stationShortCode"], row["type"])] = float(row["differenceInMinutes"])
real_causes = collections.defaultdict(list)
for date, trains in days.items():
    for t in trains:
        for row in t["timeTableRows"]:
            for c in row.get("causes") or []:
                real_causes[(date, t["trainNumber"])].append(
                    (row["stationShortCode"], c.get("categoryCodeId"), c.get("detailedCategoryCodeId")))
OUT["real_rows_with_recorded_delay"] = len(real)
OUT["real_trains_with_official_cause"] = len(real_causes)

pub, rec = [], []
for c in cases:
    corr = c["origin"]["corridor"]; date = c["origin"]["date"]; ws = c["origin"]["ws"]
    for slot, num in enumerate(c["origin"]["train_numbers"]):
        for (idx, pa, pd_, _) in c["origin"]["stops"][slot]:
            key = (date, num, corr[idx], "ARRIVAL")
            if key not in real:
                continue
            o = [x for x in c["obs"] if x["train"] == slot and x["station"] == idx]
            if not o or o[0]["arr"] is None or o[0]["parr"] is None:
                continue
            pub.append(o[0]["arr"] - o[0]["parr"])
            rec.append(real[key])
pub = np.array(pub); rec = np.array(rec)
corr_coef = float(np.corrcoef(pub, rec)[0, 1]) if len(pub) > 30 else float("nan")
OUT["published_vs_real_delay"] = dict(n=int(len(pub)), pearson_r=corr_coef,
                                      published_median=float(np.median(pub)),
                                      real_median=float(np.median(rec)))
print("STAGE 2a matched rows=%d  pearson(published delay, real recorded delay)=%.4f"
      % (len(pub), corr_coef), flush=True)

# Attacker B: substitute the REAL recorded operations for the published ones and run the
# best domain rule available, then score against the hidden ledger.
def rule_from_rows(byt, n_stations, n_trains):
    iv = []; prim = ["NONE"] * n_trains; inc = []
    exc = collections.defaultdict(list); dwl = collections.defaultdict(list)
    for i, rows in byt.items():
        for a, b in zip(rows, rows[1:]):
            if a["dep"] is None or b["arr"] is None:
                continue
            exc[min(a["station"], b["station"])].append(((b["arr"] - a["dep"]) - (b["parr"] - a["pdep"]), a["dep"]))
        for r in rows:
            if r["dep"] is not None and r["pdep"] is not None and r["dep"] - r["pdep"] > 6:
                iv.append({"type": "HOLD", "train": i, "stop": r["station"]})
            if r["arr"] is not None and r["dep"] is not None and r["parr"] is not None:
                dwl[r["station"]].append(((r["dep"] - r["arr"]) - (r["pdep"] - r["parr"]), r["arr"]))
        d = [r["arr"] - r["parr"] for r in rows if r["arr"] is not None and r["parr"] is not None]
        if d and max(d) > 25:
            prim[i] = "SHORT_TURNED"
    if exc:
        seg = max(exc, key=lambda k: sum(max(0, e) for e, _ in exc[k]))
        bad = [t for e, t in exc[seg] if e > 3]
        if bad:
            inc.append({"type": "SPEED_RESTRICTION", "loc": seg, "start_bucket": int(min(bad) // 10),
                        "dur_band": P.dur_band((max(bad) - min(bad)) if len(bad) > 1 else 20)})
    if dwl:
        stn = max(dwl, key=lambda k: sum(max(0, e) for e, _ in dwl[k]))
        bad = [t for e, t in dwl[stn] if e > 4]
        if bad:
            inc.append({"type": "STATION_DWELL_FAULT", "loc": stn, "start_bucket": int(min(bad) // 10),
                        "dur_band": P.dur_band((max(bad) - min(bad)) if len(bad) > 1 else 20)})
    return {"incidents": inc, "interventions": iv, "primary": prim}

rows_attack, rows_selfrule = [], []
for c in cases:
    corr = c["origin"]["corridor"]; date = c["origin"]["date"]
    byt_real = collections.defaultdict(list)
    for slot, num in enumerate(c["origin"]["train_numbers"]):
        for seq, (idx, pa, pd_, _) in enumerate(c["origin"]["stops"][slot]):
            da = real.get((date, num, corr[idx], "ARRIVAL"))
            dd = real.get((date, num, corr[idx], "DEPARTURE"))
            byt_real[slot].append({"seq": seq, "station": idx,
                                   "parr": None if seq == 0 else pa, "pdep": pd_,
                                   "arr": None if (da is None or seq == 0) else pa + da,
                                   "dep": None if dd is None else pd_ + dd})
    pred = rule_from_rows(byt_real, c["n_stations"], c["n_trains"])
    rows_attack.append((c["case_id"], json.dumps(pred)))
ans_path = "private/answers.csv"
f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
pd.DataFrame(rows_attack, columns=["case_id", "ledger_json"]).to_csv(f.name, index=False)
s_attack = G.grade(f.name, ans_path)
OUT["stage2_real_corpus_attack_score"] = float(s_attack)
print("STAGE 2b score of the de-anonymised real-corpus attacker = %.4f" % s_attack, flush=True)

floor = G.grade("public/sample_submission.csv", ans_path)
OUT["sample_floor"] = float(floor)
print("reference: sample/label-prior floor = %.4f" % floor, flush=True)
json.dump(OUT, open("LOOKUP_ATTACK_RESULTS.json", "w"), indent=1)
print("wrote LOOKUP_ATTACK_RESULTS.json", flush=True)
