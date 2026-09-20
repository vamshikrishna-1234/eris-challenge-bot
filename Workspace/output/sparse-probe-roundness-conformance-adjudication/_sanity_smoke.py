#!/usr/bin/env python3
"""Grader robustness smoke test: column checks, ID-set checks, bounds, enums, malformed values,
independent head behaviour, sample score, and an exactly perfect submission."""
import sys

import numpy as np
import pandas as pd

import grade as G


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    ans = pd.read_csv(base + "/private/answers.csv")
    ids = ans.row_id.to_numpy()
    y = ans.ront_um.to_numpy()
    conf = ans.conform.to_numpy().astype(float)
    sig = ans.signature_class.to_numpy()
    maj = pd.Series(sig).value_counts().idxmax()

    def mk(p10=None, p50=None, p90=None, pc=0.5, sg=None, rid=ids):
        n = len(rid)
        f = lambda v, d: (np.full(n, d, float) if v is None else
                          (np.full(n, v, float) if np.isscalar(v) else np.asarray(v, float)))
        if sg is None:
            sg_col = np.full(n, maj)
        elif isinstance(sg, str):
            sg_col = np.full(n, sg)
        else:
            sg_col = np.asarray(sg)
        return pd.DataFrame(dict(row_id=rid, ront_p10_um=f(p10, 1.0), ront_p50_um=f(p50, 5.0),
                                 ront_p90_um=f(p90, 20.0), p_conform=f(pc, 0.5),
                                 signature_class=sg_col))

    perfect = mk(y, y, y, conf, sig)
    checks = []

    def chk(name, sub, expect=None, rule=None):
        s = G.grade(sub, ans)
        ok = (abs(s - expect) < 1e-9) if expect is not None else rule(s)
        checks.append((name, round(float(s), 6), "PASS" if ok else "FAIL"))

    chk("perfect submission == 1.0", perfect, expect=1.0)
    chk("sample submission in [0.10, 0.30]",
        pd.read_csv(base + "/public/sample_submission.csv"), rule=lambda s: 0.10 <= s <= 0.30)

    bad = perfect.drop(columns=["p_conform"])
    chk("missing required column -> 0", bad, expect=0.0)
    bad = perfect.rename(columns={"row_id": "id"})
    chk("renamed id column -> 0", bad, expect=0.0)
    chk("missing rows -> 0", perfect.iloc[:-5].copy(), expect=0.0)
    chk("extra rows -> 0", pd.concat([perfect, perfect.iloc[:3]], ignore_index=True), expect=0.0)
    d = perfect.copy(); d.loc[d.index[0], "row_id"] = d.row_id.iloc[1]
    chk("duplicate row_id -> 0", d, expect=0.0)
    d = perfect.copy(); d.loc[d.index[0], "ront_p50_um"] = np.nan
    chk("NaN quantile -> 0", d, expect=0.0)
    d = perfect.copy(); d.loc[d.index[0], "ront_p90_um"] = np.inf
    chk("Inf quantile -> 0", d, expect=0.0)
    d = perfect.copy(); d.loc[d.index[0], "ront_p10_um"] = -1.0
    chk("negative quantile -> 0", d, expect=0.0)
    d = perfect.copy(); d.loc[d.index[0], "p_conform"] = 1.5
    chk("p_conform out of range -> 0", d, expect=0.0)
    d = perfect.copy(); d.loc[d.index[0], "signature_class"] = "not_a_class"
    chk("illegal signature enum -> 0", d, expect=0.0)
    d = perfect.copy()
    d["ront_p50_um"] = d["ront_p50_um"].astype(object)
    d.loc[d.index[0], "ront_p50_um"] = "abc"
    chk("non-numeric quantile -> 0", d, expect=0.0)
    chk("empty submission -> 0", perfect.iloc[0:0].copy(), expect=0.0)

    chk("quantile head only (others at prior) < 0.55",
        mk(y, y, y, float(conf.mean()), maj), rule=lambda s: s < 0.55)
    chk("conformance head only < 0.46", mk(pc=conf, sg=maj), rule=lambda s: s < 0.46)
    chk("signature head only < 0.30", mk(sg=sig), rule=lambda s: s < 0.30)
    chk("all-zero quantiles, no other skill, small", mk(0.0, 0.0, 0.0, 0.5, maj),
        rule=lambda s: s < 0.10)
    chk("absurdly wide interval is penalised", mk(0.0, float(np.median(y)), 1e5, 0.5, maj),
        rule=lambda s: s < 0.10)
    chk("score is bounded above by 1.0", perfect, rule=lambda s: s <= 1.0)

    for name, score, verdict in checks:
        print("%-46s %10.6f  %s" % (name[:46], score, verdict))
    n_fail = sum(1 for _, _, v in checks if v == "FAIL")
    print("\n%d checks, %d failed" % (len(checks), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
