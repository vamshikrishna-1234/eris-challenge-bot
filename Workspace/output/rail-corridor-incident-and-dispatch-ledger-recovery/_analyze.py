"""Analysis, leakage, reversibility and metric-null audit on the real prepared split."""
import collections, datetime as dt, json, math, os, sys
import pandas as pd, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade as G
import prepare as P

R = {}
train = pd.read_csv("public/train.csv", dtype={"case_id": str})
test = pd.read_csv("public/test.csv", dtype={"case_id": str})
tans = pd.read_csv("public/train_answers.csv", dtype={"case_id": str})
ans = pd.read_csv("private/answers.csv", dtype={"case_id": str})
sample = pd.read_csv("public/sample_submission.csv", dtype={"case_id": str})

R["scale"] = dict(train_cases=int(train.case_id.nunique()), train_rows=int(len(train)),
                  test_cases=int(test.case_id.nunique()), test_rows=int(len(test)),
                  trains_per_case=float(train.groupby("case_id").train_slot.nunique().mean()),
                  rows_per_case=float(train.groupby("case_id").size().mean()))

led = [json.loads(x) for x in ans.ledger_json]
R["labels"] = dict(
    incidents_per_case=float(np.mean([len(l["incidents"]) for l in led])),
    interventions_per_case=float(np.mean([len(l["interventions"]) for l in led])),
    incident_types=dict(collections.Counter(i["type"] for l in led for i in l["incidents"])),
    intervention_types=dict(collections.Counter(i["type"] for l in led for i in l["interventions"])),
    primary_classes=dict(collections.Counter(p for l in led for p in l["primary"])))

# ---- leakage scan of public artifacts -------------------------------------
BANNED = ("stationShortCode", "trainNumber", "departureDate", "actualTime", "causes",
          "digitraffic", "HKI", "2026-")
leak = {}
for name, frame in (("train.csv", train), ("test.csv", test), ("sample_submission.csv", sample)):
    blob = " ".join(map(str, frame.columns)) + " " + " ".join(
        str(x) for x in frame.head(2000).astype(str).values.ravel().tolist())
    leak[name] = [b for b in BANNED if b in blob]
R["leakage_scan"] = leak
R["public_columns"] = dict(train=list(train.columns), test=list(test.columns))
R["answers_never_in_public"] = bool(set(ans.case_id) & set(train.case_id) == set())

# ---- reversibility: can the public corpus supply the hidden ledger? -------
raw = P.find_raw()
days = P.load_days(raw)
counter = P.segment_traffic(days)
corrs = P.corridors_from(counter, len(days))
real_delay = {}
for date, trains in days.items():
    for t in trains:
        for row in t["timeTableRows"]:
            if row.get("differenceInMinutes") is None:
                continue
            st = dt.datetime.fromisoformat(row["scheduledTime"].replace("Z", "+00:00"))
            key = (date, t["trainNumber"], row["stationShortCode"], row["type"])
            real_delay[key] = float(row["differenceInMinutes"])
R["real_records_with_recorded_delay"] = len(real_delay)

# the published planned times are real, so the origin corridor/day IS identifiable;
# what matters is whether the published realized behaviour carries the real one.
pub = test[test.observed_arr.notna() & test.planned_arr.notna()]
pub_delay = (pub.observed_arr - pub.planned_arr).values
R["published_delay_stats"] = dict(median=float(np.median(pub_delay)),
                                  p90=float(np.percentile(pub_delay, 90)),
                                  max=float(pub_delay.max()))
rv = np.array(list(real_delay.values()))
R["real_delay_stats"] = dict(median=float(np.median(rv)), p90=float(np.percentile(rv, 90)),
                             max=float(rv.max()))
R["reversibility_note"] = (
    "Published realized times are produced by the operations model and are not the API's actualTime "
    "values; the scored incident and dispatch ledger has no counterpart in any public record, so "
    "recovering the (real) planned timetable - which is published to solvers anyway - yields nothing.")

# ---- metric-null and one-head audits --------------------------------------
import tempfile
def score_of(fn, label):
    rows = [(cid, json.dumps(fn(json.loads(cell)))) for cid, cell in zip(ans.case_id, ans.ledger_json)]
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    pd.DataFrame(rows, columns=["case_id", "ledger_json"]).to_csv(f.name, index=False)
    s = G.grade(f.name, "private/answers.csv")
    R.setdefault("null_audit", {})[label] = float(s)
    print("%-34s %.4f" % (label, s), flush=True)
    return s

score_of(lambda t: t, "oracle")
score_of(lambda t: {"incidents": [], "interventions": [], "primary": []}, "empty")
score_of(lambda t: {"incidents": [], "interventions": [], "primary": ["NONE"] * len(t["primary"])}, "all-NONE")
score_of(lambda t: {"incidents": t["incidents"], "interventions": [], "primary": []}, "incident head only")
score_of(lambda t: {"incidents": [], "interventions": t["interventions"], "primary": []}, "intervention head only")
score_of(lambda t: {"incidents": [], "interventions": [], "primary": t["primary"]}, "primary head only")
sm = G.grade("public/sample_submission.csv", "private/answers.csv")
R["null_audit"]["sample_submission"] = float(sm)
print("%-34s %.4f" % ("sample_submission", sm), flush=True)

json.dump(R, open("ANALYSIS_RESULTS.json", "w"), indent=1)
print("\nwrote ANALYSIS_RESULTS.json", flush=True)
