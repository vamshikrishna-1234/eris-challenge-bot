"""_sanity_smoke.py - fast structural checks on the prepared split.

  python _sanity_smoke.py --public <dir> --private <dir>
"""
import argparse, json, sys
from pathlib import Path
import numpy as np, pandas as pd
import grade as G

KB = 7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", required=True); ap.add_argument("--private", required=True)
    a = ap.parse_args()
    pub, priv = Path(a.public), Path(a.private)
    fails = []

    tr = pd.read_csv(pub / "train.csv"); te = pd.read_csv(pub / "test.csv")
    sa = pd.read_csv(pub / "sample_submission.csv"); an = pd.read_csv(priv / "answers.csv")

    def chk(name, ok, detail=""):
        print("%-42s %s %s" % (name, "pass" if ok else "FAIL", detail))
        if not ok: fails.append(name)

    chk("ids disjoint train/test", set(tr["id"]) & set(te["id"]) == set())
    chk("sample covers every test id", set(sa["id"]) == set(te["id"]))
    chk("answers cover every test id", set(an["id"]) == set(te["id"]))
    chk("answers absent for train ids", set(an["id"]) & set(tr["id"]) == set())
    chk("no answer columns in test.csv",
        not ({"actual", "log_t", "log_s"} & set(te.columns)))
    chk("score groups >= 4", an["score_group"].nunique() >= 4, str(an["score_group"].nunique()))
    chk("signal bands >= 2", an["signal_band"].nunique() >= 2, str(sorted(an["signal_band"].unique())))
    chk("train rows >= 1200", len(tr) >= 1200, str(len(tr)))
    chk("test rows >= 350", len(te) >= 350, str(len(te)))

    bad = 0
    for _, r in te.sample(min(40, len(te)), random_state=0).iterrows():
        p = pub / "test" / r["series"]
        if not p.exists(): bad += 1; continue
        s = pd.read_csv(p)
        if s.shape[0] != int(r["n_obs"]) or s.shape[1] != 225: bad += 1
        if len(json.loads(r["boreholes"])) != int(r["n_boreholes"]): bad += 1
    chk("sampled test series well-formed", bad == 0, "%d problems" % bad)

    for _, r in tr.sample(min(40, len(tr)), random_state=0).iterrows():
        m = np.array(json.loads(r["actual"]), float)
        if m.shape != (int(r["n_boreholes"]), KB) or (m < 0).any(): bad += 1
    chk("sampled train ledgers well-shaped", bad == 0)

    chk("sample submission scores in [0.12, 0.30]",
        0.12 <= G.grade(sa, an) <= 0.30, "%.4f" % G.grade(sa, an))
    chk("empty submission scores 0", G.grade(pd.DataFrame(columns=["id"]), an) == 0.0)
    orc = pd.DataFrame([{"id": int(x["id"]), "actual": x["actual"],
                         "log_t": x["log_t"], "log_s": x["log_s"]} for _, x in an.iterrows()])
    chk("oracle scores 1.0", abs(G.grade(orc, an) - 1.0) < 1e-9, "%.6f" % G.grade(orc, an))

    print("\n%s" % ("SMOKE PASS" if not fails else "SMOKE FAIL: " + ", ".join(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
