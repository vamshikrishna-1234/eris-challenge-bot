"""Grader for Sparse-Probe Roundness Adjudication.

Three heads on every scored feature:

  1. a predictive interval and median for the true roundness deviation RONt, in micrometres,
     scored with the interval score for the central 80% interval plus the median absolute error;
  2. the probability that the feature conforms to its drawing roundness tolerance, scored with
     the Brier score;
  3. the machine / set-up signature class, scored by accuracy.

Each head is expressed as skill against a fixed reference constant measured from a label-prior
submission on the prepared split, so a prior-only submission lands near 0.15 and a perfect
submission scores exactly 1.0. The final score adds a worst-subgroup term over the three physical
probe-density bands, so a solution cannot buy its score on the easy dense plans alone.

Range: 0.0 to 1.0. Any structurally invalid submission scores exactly 0.0.
"""
import numpy as np
import pandas as pd

# head weights
W_Q, W_CONF, W_SIG = 0.45, 0.35, 0.20
# aggregation: overall mean plus a worst-probe-density-band term
W_MEAN, W_WORST = 0.82, 0.18

# reference constants: the label-prior submission measured on the prepared split, divided by 0.85,
# so that a label-prior submission scores about 0.15 on each head.
REF_Q = 82.613308          # prior interval loss 70.221312 um
REF_B = 0.292320           # prior Brier 0.248472
REF_S = 0.030388           # prior signature accuracy 0.175830

ALPHA = 0.20               # central 80% interval
PEN = 2.0 / ALPHA          # = 10, the standard interval-score miss penalty
MED_W = 2.0                # weight on the median absolute error

SIG_CLASSES = ("three_jaw_chuck", "clamp_ovality", "spindle_bearing_order",
               "centreless_five_lobe", "fine_ground_smooth", "worn_tool_chatter")
REQUIRED = ["row_id", "ront_p10_um", "ront_p50_um", "ront_p90_um", "p_conform", "signature_class"]
MAX_UM = 1.0e6             # any quantile beyond this is treated as invalid


def _band(n):
    if n <= 5:
        return "sparse"
    if n <= 8:
        return "medium"
    return "dense"


def _heads(y, lo, md, hi, p, conf, sig_pred, sig_true):
    q_loss = float(np.mean((hi - lo)
                           + PEN * np.maximum(lo - y, 0.0)
                           + PEN * np.maximum(y - hi, 0.0)
                           + MED_W * np.abs(y - md)))
    q = float(np.clip(1.0 - q_loss / REF_Q, 0.0, 1.0))
    b = float(np.mean((p - conf) ** 2))
    c = float(np.clip(1.0 - b / REF_B, 0.0, 1.0))
    acc = float(np.mean(sig_pred == sig_true))
    s = float(np.clip((acc - REF_S) / (1.0 - REF_S), 0.0, 1.0))
    return W_Q * q + W_CONF * c + W_SIG * s


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        sub = submission.copy()
        ans = answers.copy()
        for col in REQUIRED:
            if col not in sub.columns:
                return 0.0
        for col in ("row_id", "ront_um", "conform", "signature_class"):
            if col not in ans.columns:
                return 0.0

        sub["row_id"] = sub["row_id"].astype(str)
        ans["row_id"] = ans["row_id"].astype(str)
        if sub["row_id"].duplicated().any():
            return 0.0
        if set(sub["row_id"]) != set(ans["row_id"]):
            return 0.0

        sub = sub.rename(columns={"signature_class": "pred_signature_class"})
        merged = ans.merge(sub[["row_id", "ront_p10_um", "ront_p50_um", "ront_p90_um",
                                "p_conform", "pred_signature_class"]],
                           on="row_id", how="left")
        if len(merged) != len(ans):
            return 0.0

        q = merged[["ront_p10_um", "ront_p50_um", "ront_p90_um"]].apply(
            pd.to_numeric, errors="coerce").to_numpy(dtype=float)
        p = pd.to_numeric(merged["p_conform"], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(q).all() or not np.isfinite(p).all():
            return 0.0
        if (q < 0.0).any() or (q > MAX_UM).any():
            return 0.0
        if (p < 0.0).any() or (p > 1.0).any():
            return 0.0

        sig_pred = merged["pred_signature_class"].astype(str).to_numpy()
        if not np.isin(sig_pred, SIG_CLASSES).all():
            return 0.0
        sig_true = merged["signature_class"].astype(str).to_numpy()

        y = pd.to_numeric(merged["ront_um"], errors="coerce").to_numpy(dtype=float)
        conf = pd.to_numeric(merged["conform"], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(y).all() or not np.isfinite(conf).all():
            return 0.0

        lo = q.min(axis=1)
        hi = q.max(axis=1)
        md = q[:, 1]

        overall = _heads(y, lo, md, hi, p, conf, sig_pred, sig_true)

        worst = overall
        if "n_probe" in merged.columns:
            bands = np.array([_band(int(v)) for v in
                              pd.to_numeric(merged["n_probe"], errors="coerce").fillna(8)])
            vals = []
            for name in ("sparse", "medium", "dense"):
                m = bands == name
                if m.sum() >= 50:
                    vals.append(_heads(y[m], lo[m], md[m], hi[m], p[m], conf[m],
                                       sig_pred[m], sig_true[m]))
            if vals:
                worst = float(min(vals))

        final = W_MEAN * overall + W_WORST * worst
        return float(np.clip(final, 0.0, 1.0))
    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", required=True)
    ap.add_argument("--answers", required=True)
    args = ap.parse_args()
    print("score=%.6f" % grade(pd.read_csv(args.submission), pd.read_csv(args.answers)))
