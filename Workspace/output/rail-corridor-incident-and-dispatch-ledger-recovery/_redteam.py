"""Adversarial submissions that try to win without solving the task."""
import collections, json, random, sys, tempfile
import pandas as pd
sys.path.insert(0, ".")
import grade as G

ANS = "private/answers.csv"
ans = pd.read_csv(ANS, dtype={"case_id": str})
tans = pd.read_csv("public/train_answers.csv", dtype={"case_id": str})
truth = [json.loads(x) for x in ans.ledger_json]
rng = random.Random(7)
R = {}


def run(fn, label):
    rows = [(cid, json.dumps(fn(t))) for cid, t in zip(ans.case_id, truth)]
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    pd.DataFrame(rows, columns=["case_id", "ledger_json"]).to_csv(fh.name, index=False)
    s = G.grade(fh.name, ANS)
    R[label] = float(s)
    print("%-46s %.4f" % (label, s), flush=True)


TYPES = ["SPEED_RESTRICTION", "SEGMENT_BLOCKAGE", "STATION_DWELL_FAULT", "UNIT_FAULT", "CREW_LATE"]
IV = ["HOLD", "SHORT_TURN", "CANCEL"]

run(lambda t: {"incidents": [], "interventions": [], "primary": []}, "empty submission")
run(lambda t: {"incidents": [{"type": rng.choice(TYPES), "loc": rng.randrange(max(1, t["n_stations"])),
                              "start_bucket": rng.randrange(18), "dur_band": rng.randrange(5)}
                             for _ in range(12)],
               "interventions": [{"type": rng.choice(IV), "train": rng.randrange(len(t["primary"]) or 1),
                                  "stop": rng.randrange(max(1, t["n_stations"]))} for _ in range(120)],
               "primary": [rng.choice(TYPES + ["NONE"]) for _ in t["primary"]]},
    "max-size random spam")
run(lambda t: {"incidents": [{"type": ty, "loc": loc, "start_bucket": 8, "dur_band": 3}
                             for ty in TYPES for loc in range(min(3, t["n_stations"]))][:12],
               "interventions": [], "primary": ["NONE"] * len(t["primary"])},
    "shotgun: every type at every early loc")
run(lambda t: {"incidents": [], "interventions": [{"type": "CANCEL", "train": i, "stop": 0}
                                                  for i in range(len(t["primary"]))],
               "primary": ["CANCELLED"] * len(t["primary"])}, "all-CANCEL / all-CANCELLED")
run(lambda t: {"incidents": [], "interventions": [{"type": "HOLD", "train": i, "stop": s}
                                                  for i in range(len(t["primary"]))
                                                  for s in range(t["n_stations"])][:120],
               "primary": ["NONE"] * len(t["primary"])}, "HOLD at every train-stop pair")
pool = [json.loads(x) for x in tans.ledger_json]
cnt = collections.Counter(x for x in tans.ledger_json)
common = json.loads(cnt.most_common(1)[0][0])
run(lambda t: {"incidents": common["incidents"], "interventions": [],
               "primary": (common["primary"] * 10)[:len(t["primary"])]}, "copy the commonest train ledger")
run(lambda t: (lambda p: {"incidents": p["incidents"], "interventions": [],
                          "primary": (p["primary"] * 10)[:len(t["primary"])]})(rng.choice(pool)),
    "copy a random train ledger")
run(lambda t: {"incidents": [t["incidents"][0]] * 12 if t["incidents"] else [],
               "interventions": [], "primary": ["NONE"] * len(t["primary"])},
    "oracle first incident duplicated 12x")
json.dump(R, open("REDTEAM_RESULTS.json", "w"), indent=1)
print("wrote REDTEAM_RESULTS.json")
