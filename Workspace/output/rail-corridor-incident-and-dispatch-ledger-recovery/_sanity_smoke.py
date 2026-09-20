"""Grader robustness and contract suite."""
import json, os, sys, tempfile, hashlib
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade as G

ANS = "private/answers.csv"
OUT = []

def check(name, cond, detail=""):
    OUT.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + ("  " + detail if detail else ""), flush=True)

def write(df):
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    df.to_csv(fh.name, index=False)
    return fh.name

ans = pd.read_csv(ANS, dtype={"case_id": str})

perfect = ans.copy()
s = G.grade(write(perfect), ANS)
check("perfect submission scores exactly 1.0", s == 1.0, "score=%r" % s)

sample = pd.read_csv("public/sample_submission.csv", dtype={"case_id": str})
ss = G.grade(write(sample), ANS)
check("sample submission in [0.12, 0.20]", 0.12 <= ss <= 0.20, "score=%.4f" % ss)
check("sample submission strictly above declared minimum 0.0", ss > 0.0, "score=%.4f" % ss)

empty = ans.copy()
empty["ledger_json"] = json.dumps({"incidents": [], "interventions": [], "primary": []})
se = G.grade(write(empty), ANS)
check("empty ledger scores well below sample+oracle", se < ss + 0.05 and se < 0.30, "score=%.4f" % se)

junk = ans.copy()
junk.loc[junk.index[:50], "ledger_json"] = "{not json"
sj = G.grade(write(junk), ANS)
check("malformed JSON is row-local, not fatal", 0.0 < sj < 1.0, "score=%.4f" % sj)

miss = ans.iloc[:-1].copy()
check("missing case id scores 0.0", G.grade(write(miss), ANS) == 0.0)

extra = pd.concat([ans, ans.iloc[:1].assign(case_id="ZZZZZZ")], ignore_index=True)
check("extra case id scores 0.0", G.grade(write(extra), ANS) == 0.0)

dup = pd.concat([ans, ans.iloc[:1]], ignore_index=True)
check("duplicate case id scores 0.0", G.grade(write(dup), ANS) == 0.0)

bad_cols = ans.rename(columns={"ledger_json": "prediction"})
check("wrong column name scores 0.0", G.grade(write(bad_cols), ANS) == 0.0)

nanned = ans.copy()
nanned.loc[nanned.index[:20], "ledger_json"] = float("nan")
sn = G.grade(write(nanned), ANS)
check("NaN cells are row-local", 0.0 < sn < 1.0, "score=%.4f" % sn)

huge = ans.copy()
huge.loc[huge.index[:10], "ledger_json"] = json.dumps(
    {"incidents": [{"type": "SPEED_RESTRICTION", "loc": 0, "start_bucket": 0, "dur_band": 0}] * 5000,
     "interventions": [], "primary": []})
sh = G.grade(write(huge), ANS)
check("oversized JSON is rejected row-locally", 0.0 < sh < 1.0, "score=%.4f" % sh)

deep = ans.copy()
deep.loc[deep.index[:10], "ledger_json"] = json.dumps({"incidents": [[[[[1]]]]], "interventions": {}, "primary": 7})
sd = G.grade(write(deep), ANS)
check("wrongly typed fields are tolerated row-locally", 0.0 < sd < 1.0, "score=%.4f" % sd)

oor = ans.copy()
oor["ledger_json"] = json.dumps({"incidents": [{"type": "SPEED_RESTRICTION", "loc": 10 ** 9,
                                                "start_bucket": -5, "dur_band": 99}],
                                 "interventions": [{"type": "HOLD", "train": -3, "stop": 10 ** 9}],
                                 "primary": ["NOT_A_CLASS"] * 200})
so = G.grade(write(oor), ANS)
check("out-of-range entries are filtered, never crash", 0.0 <= so < 0.30, "score=%.4f" % so)

bogus_type = ans.copy()
bogus_type["ledger_json"] = json.dumps({"incidents": [{"type": "SELF_DESTRUCT", "loc": 0,
                                                       "start_bucket": 0, "dur_band": 0}],
                                        "interventions": [], "primary": []})
check("unknown enum values are filtered", 0.0 <= G.grade(write(bogus_type), ANS) < 0.30)

check("grade of an unreadable file is 0.0", G.grade("/nonexistent.csv", ANS) == 0.0)

# monotonicity: degrading a perfect submission never increases the score
import random
rng = random.Random(5)
deg = ans.copy()
rows = []
for cell in deg["ledger_json"]:
    obj = json.loads(cell)
    if obj["incidents"] and rng.random() < 0.5:
        obj["incidents"] = obj["incidents"][:-1]
    obj["primary"] = ["NONE" if rng.random() < 0.4 else p for p in obj["primary"]]
    rows.append(json.dumps(obj))
deg["ledger_json"] = rows
sdeg = G.grade(write(deg), ANS)
check("degraded truth scores strictly below 1.0", sdeg < 1.0, "score=%.4f" % sdeg)
check("degraded truth still beats the sample", sdeg > ss, "%.4f > %.4f" % (sdeg, ss))

print("\n%d/%d checks passed" % (sum(1 for _, ok, _ in OUT if ok), len(OUT)))
sys.exit(0 if all(ok for _, ok, _ in OUT) else 1)
