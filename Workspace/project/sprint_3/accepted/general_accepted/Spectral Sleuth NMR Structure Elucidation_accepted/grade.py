"""
grade.py - Constitutional Isomer Identification From Carbon NMR Spectra

The solver submits, for every test row, a probability distribution over the K
candidate structures (`pred_prob_1` .. `pred_prob_K`). The grader scores two
complementary skills and combines them:

    top1   = mean over rows of [1 if argmax(pred_prob) == true_isomer_idx else 0]
    calib  = mean over rows of max(0, 1 - Brier / Brier_uniform)
             where Brier   = sum_k (p_k - onehot_k)^2  over the K candidates,
             and   Brier_uniform is the Brier score of the flat 1/K guess
             (so a uniform submission scores calib = 0, a perfect confident
             submission scores 1, and a confidently-wrong row is floored at 0).

    Final  = 0.65 * top1^2 + 0.35 * calib^2,  clipped to [0, 1]

Both terms are squared to compress the high end so that an "almost there"
model does not coast to a high composite, while a perfect oracle still reaches
1.0. The calibration term rewards solvers that express honest uncertainty and
spreads the score distribution well below the saturated end.

Submission columns (header required):
    id            int           unique, matches test.csv
    pred_prob_1   float >= 0    relative probability of candidate 1
    ...
    pred_prob_K   float >= 0    relative probability of candidate K
(Probabilities are normalised per row by the grader; they need not sum to 1.)

Robustness:
  * Missing required column / duplicate ids / id-set mismatch -> grade 0.0.
  * Negative, non-finite, or all-zero rows are coerced to a safe uniform row.
  * Any unhandled exception returns 0.0 rather than raising.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


K = 5

W_TOP1 = 0.65
W_CALIB = 0.35

PROB_COLS = [f"pred_prob_{k+1}" for k in range(K)]
BRIER_UNIFORM = (1.0 - 1.0 / K) ** 2 + (K - 1) * (1.0 / K) ** 2


def _normalise_row(vals: np.ndarray) -> np.ndarray:
    v = np.array(vals, dtype=np.float64)
    v[~np.isfinite(v)] = 0.0
    v = np.clip(v, 0.0, None)
    s = v.sum()
    if s <= 0.0:
        return np.full(K, 1.0 / K, dtype=np.float64)
    return v / s


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        required_sub = {"id", *PROB_COLS}
        required_ans = {"id", "true_isomer_idx"}
        if not required_sub.issubset(set(submission.columns)):
            return 0.0
        if not required_ans.issubset(set(answers.columns)):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(int)
            ans["id"] = ans["id"].astype(int)
        except (TypeError, ValueError):
            return 0.0

        if sub["id"].duplicated().any():
            return 0.0
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            return 0.0

        sub = sub.set_index("id")
        ans = ans.set_index("id")

        top1_terms: list[float] = []
        calib_terms: list[float] = []

        for rid, arow in ans.iterrows():
            try:
                true_idx = int(arow["true_isomer_idx"])
            except (TypeError, ValueError):
                return 0.0
            if true_idx < 1 or true_idx > K:
                return 0.0

            probs = _normalise_row(sub.loc[rid, PROB_COLS].to_numpy())

            pred_idx = int(np.argmax(probs)) + 1  # 1-based
            top1_terms.append(1.0 if pred_idx == true_idx else 0.0)

            onehot = np.zeros(K, dtype=np.float64)
            onehot[true_idx - 1] = 1.0
            brier = float(np.sum((probs - onehot) ** 2))
            calib_terms.append(max(0.0, 1.0 - brier / BRIER_UNIFORM))

        if not top1_terms:
            return 0.0

        top1 = float(np.mean(top1_terms))
        calib = float(np.mean(calib_terms))
        final = W_TOP1 * (top1 ** 2) + W_CALIB * (calib ** 2)
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", type=Path, required=True)
    ap.add_argument("--answers", type=Path, required=True)
    args = ap.parse_args()
    sub = pd.read_csv(args.submission)
    ans = pd.read_csv(args.answers)
    print(f"score={grade(sub, ans):.6f}")
