#!/usr/bin/env python3
"""Difficulty, shortcut and leakage analysis on the REAL prepared split.

Scores every rung of the baseline ladder with the shipped grade.py, runs the source-retrieval /
reversibility stress test at the shipped bundle size, and checks that public identifiers carry no
join back to raw order.
"""
import json
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier

import grade as G

SIG = list(G.SIG_CLASSES)


def load(base="."):
    tr = pd.read_csv(base + "/public/train.csv")
    te = pd.read_csv(base + "/public/test.csv")
    an = pd.read_csv(base + "/private/answers.csv")
    return tr, te, an


def lsc_residuals(xy):
    """Fit the least-squares circle and return (angles, radial residuals in um)."""
    x, y = xy[:, 0], xy[:, 1]
    A = np.column_stack([x, y, np.ones(len(x))])
    b = x ** 2 + y ** 2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = sol[0] / 2.0, sol[1] / 2.0
    r = np.hypot(x - cx, y - cy)
    th = np.arctan2(y - cy, x - cx)
    return th, (r - r.mean()) * 1000.0


def featurise(df):
    res, ang = [], []
    for s in df.points_xy_mm:
        th, rr = lsc_residuals(np.asarray(json.loads(s), dtype=float))
        res.append(rr); ang.append(th)
    df = df.copy()
    df["_ptp"] = [float(r.max() - r.min()) for r in res]
    df["_sd"] = [float(r.std()) for r in res]
    df["_absmax"] = [float(np.abs(r).max()) for r in res]
    mags = []
    for r in res:
        m = np.abs(np.fft.rfft(r)) / len(r)
        v = np.zeros(5); k = min(5, len(m) - 1); v[:k] = m[1:1 + k]
        mags.append(v)
    for i in range(5):
        df["_m%d" % i] = [m[i] for m in mags]
    g = df.groupby("part_id")
    df["_sib_mean_ptp"] = g._ptp.transform("mean")
    df["_sib_max_ptp"] = g._ptp.transform("max")
    df["_sib_min_ptp"] = g._ptp.transform("min")
    df["_sib_sd_ptp"] = g._ptp.transform("std").fillna(0.0)
    df["_sib_mean_sd"] = g._sd.transform("mean")
    df["_part_n"] = g._ptp.transform("size")
    df["_distinct_n"] = g.n_probe.transform("nunique")
    df["_mean_n"] = g.n_probe.transform("mean")
    df["_max_ratio"] = g.apply(lambda d: (d._ptp / d.roundness_tol_um).max(),
                               include_groups=False).reindex(df.part_id).to_numpy()
    df["_res"] = res
    return df


FEATS = ["n_probe", "_ptp", "_sd", "_absmax", "nominal_diameter_mm", "roundness_tol_um",
         "_m0", "_m1", "_m2", "_m3", "_m4", "_sib_mean_ptp", "_sib_max_ptp", "_sib_min_ptp",
         "_sib_sd_ptp", "_sib_mean_sd", "_part_n", "_distinct_n", "_mean_n", "_max_ratio"]
META = ["n_probe", "nominal_diameter_mm", "roundness_tol_um"]


def sub_frame(ids, p10, p50, p90, pc, sg):
    n = len(ids)
    f = lambda v: np.full(n, v, dtype=float) if np.isscalar(v) else np.asarray(v, dtype=float)
    return pd.DataFrame(dict(row_id=ids, ront_p10_um=f(p10), ront_p50_um=f(p50),
                             ront_p90_um=f(p90), p_conform=f(pc),
                             signature_class=(np.full(n, sg) if isinstance(sg, str)
                                              else np.asarray(sg))))


def say(*a):
    print(*a, flush=True)


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    tr, te, an = load(base)
    tr = featurise(tr); te = featurise(te)
    ids = te.row_id.to_numpy()
    y = an.set_index("row_id").loc[ids, "ront_um"].to_numpy()
    conf = an.set_index("row_id").loc[ids, "conform"].to_numpy()
    sig = an.set_index("row_id").loc[ids, "signature_class"].to_numpy()

    say("STAGE: featurised")
    q10, q50, q90 = np.quantile(tr.ront_um, [0.1, 0.5, 0.9])
    base_rate = float(tr.conform.mean())
    maj = tr.signature_class.value_counts().idxmax()
    out = {"train_rows": int(len(tr)), "test_rows": int(len(te)),
           "train_parts": int(tr.part_id.nunique()), "test_parts": int(te.part_id.nunique()),
           "conform_base_rate_test": float(conf.mean())}

    def sc(sub):
        return round(float(G.grade(sub, an)), 4)

    out["sample_submission"] = sc(pd.read_csv(base + "/public/sample_submission.csv"))
    out["prior_constant"] = sc(sub_frame(ids, q10, q50, q90, base_rate, maj))
    out["all_zero_quantiles"] = sc(sub_frame(ids, 0.0, 0.0, 0.0, 0.0, maj))
    out["copied_input_ptp"] = sc(sub_frame(ids, te._ptp, te._ptp, te._ptp,
                                           (te._ptp <= te.roundness_tol_um) * 0.96 + 0.02, maj))
    out["huge_interval_hedge"] = sc(sub_frame(ids, 0.0, q50, float(tr.ront_um.max()), 0.5, maj))
    out["perfect"] = sc(sub_frame(ids, y, y, y, conf.astype(float), sig))

    say("STAGE: null/prior rungs done")
    Xtr, Xte = tr[FEATS].to_numpy(float), te[FEATS].to_numpy(float)
    ytr, ctr, str_ = tr.ront_um.to_numpy(), tr.conform.to_numpy(), tr.signature_class.to_numpy()

    mq = [HistGradientBoostingRegressor(loss="quantile", quantile=t, max_iter=150,
                                        random_state=0).fit(tr[META], ytr).predict(te[META])
          for t in (0.1, 0.5, 0.9)]
    mc = HistGradientBoostingClassifier(max_iter=150, random_state=0).fit(tr[META], ctr)
    out["metadata_only"] = sc(sub_frame(ids, *mq, mc.predict_proba(te[META])[:, 1], maj))

    say("STAGE: metadata-only done")
    ratio = ytr / np.maximum(tr._ptp.to_numpy(), 1e-9)
    dq = [np.zeros(len(te)) for _ in range(3)]; dp = np.zeros(len(te))
    for nv in np.unique(te.n_probe):
        a = tr.n_probe.to_numpy() == nv
        b = te.n_probe.to_numpy() == nv
        rr = ratio[a] if a.sum() >= 30 else ratio
        ptp = np.maximum(te._ptp.to_numpy()[b], 1e-9)
        for i, t in enumerate((0.1, 0.5, 0.9)):
            dq[i][b] = np.quantile(rr, t) * ptp
        dp[b] = [(rr <= th).mean() for th in (te.roundness_tol_um.to_numpy()[b] / ptp)]
    out["capability_matched_domain_method"] = sc(
        sub_frame(ids, *dq, np.clip(dp, 1e-3, 1 - 1e-3), maj))

    say("STAGE: capability-matched done")
    lq = [HistGradientBoostingRegressor(loss="quantile", quantile=t, max_iter=300,
                                        learning_rate=0.07, random_state=0).fit(Xtr, ytr).predict(Xte)
          for t in (0.1, 0.5, 0.9)]
    lc = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.07, random_state=0).fit(Xtr, ctr)
    ls = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.07, random_state=0).fit(Xtr, str_)
    out["learned_route_gbm"] = sc(sub_frame(ids, *lq, lc.predict_proba(Xte)[:, 1], ls.predict(Xte)))
    nop = [c for c in FEATS if not c.startswith("_sib") and c not in ("_part_n", "_distinct_n",
                                                                      "_mean_n", "_max_ratio")]
    aq = [HistGradientBoostingRegressor(loss="quantile", quantile=t, max_iter=300,
                                        learning_rate=0.07, random_state=0).fit(tr[nop], ytr).predict(te[nop])
          for t in (0.1, 0.5, 0.9)]
    ac = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.07, random_state=0).fit(tr[nop], ctr)
    as_ = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.07, random_state=0).fit(tr[nop], str_)
    out["learned_route_no_part_pooling"] = sc(
        sub_frame(ids, *aq, ac.predict_proba(te[nop])[:, 1], as_.predict(te[nop])))

    say("STAGE: learned rungs done")
    # ---- reversibility / retrieval stress test at the shipped bundle size (one part) ----
    def bundle(df):
        g = df.groupby("part_id")
        d = g.agg(ptp_mean=("_ptp", "mean"), ptp_max=("_ptp", "max"), ptp_min=("_ptp", "min"),
                  sd_mean=("_sd", "mean"), n_mean=("n_probe", "mean"), nf=("_ptp", "size"),
                  tol_mean=("roundness_tol_um", "mean"), d_mean=("nominal_diameter_mm", "mean"),
                  m0=("_m0", "mean"), m1=("_m1", "mean"), m2=("_m2", "mean"))
        return d
    Btr, Bte = bundle(tr), bundle(te)
    mu, sd = Btr.mean(0).to_numpy(), Btr.std(0).to_numpy() + 1e-9
    Ztr = (Btr.to_numpy() - mu) / sd
    Zte = (Bte.to_numpy() - mu) / sd
    step = 400
    nn = np.concatenate([np.argmin(((Zte[i:i + step, None, :] - Ztr[None]) ** 2).sum(-1), axis=1)
                         for i in range(0, len(Zte), step)])
    te_truth = te[["row_id", "part_id"]].merge(
        an[["row_id", "signature_class", "ront_um"]], on="row_id", how="left")
    sig_by_part_tr = tr.groupby("part_id")["signature_class"].first()
    sig_by_part_te = te_truth.groupby("part_id")["signature_class"].first()
    ront_by_part_tr = tr.groupby("part_id")["ront_um"].median()
    src = Btr.index.to_numpy()[nn]
    out["retrieval_top1_signature_match"] = round(
        float((sig_by_part_tr.loc[src].to_numpy() == sig_by_part_te.loc[Bte.index].to_numpy()).mean()), 4)
    out["retrieval_signature_chance"] = round(float(sig_by_part_tr.value_counts(normalize=True).max()), 4)
    copy_map = dict(zip(Bte.index.to_numpy(), ront_by_part_tr.loc[src].to_numpy()))
    copy_sig = dict(zip(Bte.index.to_numpy(), sig_by_part_tr.loc[src].to_numpy()))
    cq = te.part_id.map(copy_map).to_numpy(float)
    cs = te.part_id.map(copy_sig).to_numpy()
    out["retrieval_target_copy_attack"] = sc(
        sub_frame(ids, cq, cq, cq, (cq <= te.roundness_tol_um) * 0.96 + 0.02, cs))

    say("STAGE: retrieval done")
    # ---- identifier / ordering attacks ----
    order_pred = np.argsort(np.argsort(ids)) / len(ids)
    out["row_id_rank_correlation_with_truth"] = round(
        float(abs(np.corrcoef(order_pred, y)[0, 1])), 4)
    out["public_columns"] = list(pd.read_csv(base + "/public/test.csv", nrows=1).columns)
    out["answers_columns"] = list(an.columns)
    out["leak_columns_in_public"] = [c for c in out["public_columns"]
                                     if c in ("ront_um", "conform", "signature_class",
                                              "machine_index", "part_index", "feature_index")]
    print(json.dumps(out, indent=1))
    json.dump(out, open(base + "/_analyze_results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
