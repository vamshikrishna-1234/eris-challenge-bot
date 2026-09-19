"""
grade.py - Annotator Reliability And Adversarial Rater Detection

Composite score (one scalar per submission):

    S_consensus     = mean over rows of [1 if pred_cons==true_cons else 0]

    S_reliability   = Brier Skill Score of the per-rater reliability
                      predictions against a climatological reference.
                      Over all (row, rater) pairs:
                          MSE_model = mean (pred_rel - true_rel)^2
                          ref       = mean(true_rel)            (climatology)
                          MSE_ref   = mean (ref - true_rel)^2
                          S_reliability = clip(1 - MSE_model/MSE_ref, 0, 1)
                      true_rel is each rater's INTRINSIC reliability (its
                      long-run probability of voting correctly), a value in
                      [0, 1] that is NOT a function of this row's gold
                      consensus. A constant predictor (e.g. 0.5 everywhere,
                      or the climatological mean) scores exactly 0, so there
                      is no free floor and the head cannot be derived from a
                      consensus guess.

    S_adversarial   = macro-F1 over the adversarial classes
                        {"1", "2", "3", "4", "5", "NONE"}, computed once over
                      the whole test set. "NONE" is always an equally-weighted
                      class; numeric slot classes are included when they occur
                      in the ground truth.

    Final = 0.25 * S_consensus^2
          + 0.25 * S_reliability^2
          + 0.50 * S_adversarial^2

Each sub-score is squared before weighting. Squaring compresses the high
end (e.g. 0.85 -> 0.72) so a strong image-only classifier cannot coast to a
high composite on the consensus/reliability heads, while a true oracle (all
sub-scores 1.0) is unaffected and still reaches 1.0. Adversarial-rater
detection - the part that is genuinely hard and not solvable from the image
alone - carries the dominant 0.50 weight.

The adversarial term uses macro-averaged F1 instead of accuracy so that
a trivial "always NONE" submission (which would score high in raw accuracy
because most rows truly are NONE) is held well below what an actual learned
model achieves. Classes absent from the ground truth are excluded from the
macro average so they cannot inflate the score with a spurious perfect 1.0.

Final = clipped to [0, 1]. Higher is better.

Submission columns (positional, header required):
    id                    int            unique per row, matches test.csv
    pred_consensus        int 0..1       binary class prediction
    pred_rel_1..5         float [0, 1]   per-rater reliability estimate
    pred_adversarial_idx  str            one of {"1","2","3","4","5","NONE"}

Robustness:
  * Missing rows / missing columns -> grade returns 0.0.
  * Duplicate ids in submission -> grade returns 0.0.
  * Submission row-set mismatch with answers -> grade returns 0.0.
  * Out-of-range pred_rel_i values are clipped to [0, 1]; non-numeric
    cells default to 0.5.
  * pred_consensus values not in {0, 1} are coerced to 0 (worst case).
  * pred_adversarial_idx values that don't match the canonical set are
    coerced to "NONE".
  * Any unhandled exception during grading returns 0.0 rather than
    raising; the platform never blocks on a malformed submission.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


N_RATERS = 5

W_CONSENSUS = 0.25
W_RELIABILITY = 0.25
W_ADVERSARIAL = 0.50

# Each component sub-score is raised to this power before weighting. Squaring
# compresses the high end (e.g. 0.85 -> 0.72) so a strong image classifier no
# longer coasts to a high composite, while a true oracle (all sub-scores 1.0)
# is unaffected and still reaches 1.0.
SCORE_POWER = 2.0

ADV_CLASSES = ["1", "2", "3", "4", "5", "NONE"]
ADV_VALID = set(ADV_CLASSES)


def _coerce_consensus(v) -> int:
    try:
        x = int(round(float(v)))
    except (TypeError, ValueError):
        return 0
    return 1 if x == 1 else 0


def _coerce_rel(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.5
    if not np.isfinite(x):
        return 0.5
    return float(np.clip(x, 0.0, 1.0))


def _coerce_adv(v) -> str:
    if v is None:
        return "NONE"
    s = str(v).strip()
    if s in ADV_VALID:
        return s
    try:
        f = float(s)
        if np.isfinite(f):
            n = int(round(f))
            if 1 <= n <= N_RATERS:
                return str(n)
    except (TypeError, ValueError):
        pass
    return "NONE"


def _macro_f1_multiclass(y_true: list[str], y_pred: list[str]) -> float:
    """Macro-F1 over the adversarial classes, averaged with EQUAL weight.

    "NONE" ("no adversary on this row") is a first-class label and is ALWAYS
    one of the averaged classes, carrying exactly the same 1/n weight as each
    numeric rater-slot class - never dropped, never up-weighted for being the
    majority. The numeric classes {1..5} are included only when they actually
    occur in `y_true`: a class that never appears carries no signal, and
    counting its degenerate tp+fp==0 / tp+fn==0 case as a perfect 1.0 would
    inflate the macro average, so absent numeric classes are dropped. For any
    included class, tp+fn > 0 holds, so an unpredicted class scores 0.0.
    """
    true_set = set(y_true)
    present = [c for c in ADV_CLASSES if c in true_set]
    # "NONE" is always a scored, equally-weighted class.
    if "NONE" not in present:
        present.append("NONE")
    if not present:
        return 0.0
    f1s: list[float] = []
    for cls in present:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        if tp == 0:
            f1s.append(0.0)
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Score `submission` against `answers` (private/answers.csv).

    Composite of: 0.25 * consensus accuracy^2 + 0.25 * reliability Brier
    Skill Score^2 + 0.50 * adversarial macro-F1^2, clipped to [0, 1].
    """
    try:
        rel_cols_pred = [f"pred_rel_{k+1}" for k in range(N_RATERS)]
        rel_cols_true = [f"true_rel_{k+1}" for k in range(N_RATERS)]
        required_sub = {"id", "pred_consensus", "pred_adversarial_idx"} | set(rel_cols_pred)
        required_ans = {"id", "true_consensus", "true_adversarial_idx"} | set(rel_cols_true)

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

        # Single indexed alignment: after this, sub row i corresponds to
        # ans row i (O(N) total, no per-row scan). The set-equality + dup
        # checks above guarantee a clean 1:1 reindex with no NaN rows.
        sub = sub.set_index("id").reindex(ans["id"].to_numpy()).reset_index()

        # ---- consensus head ----
        pred_cons = np.array([_coerce_consensus(v) for v in sub["pred_consensus"]], dtype=int)
        true_cons = ans["true_consensus"].astype(int).to_numpy()
        s_consensus = float(np.mean(pred_cons == true_cons))

        # ---- reliability head (Brier Skill Score over all rater slots) ----
        pred_rel = np.column_stack([
            [_coerce_rel(v) for v in sub[col]] for col in rel_cols_pred
        ]).astype(float)
        true_rel = ans[rel_cols_true].to_numpy(dtype=float)

        flat_pred = pred_rel.reshape(-1)
        flat_true = true_rel.reshape(-1)
        mse_model = float(np.mean((flat_pred - flat_true) ** 2))
        ref = float(np.mean(flat_true))
        mse_ref = float(np.mean((ref - flat_true) ** 2))
        if mse_ref <= 1e-12:
            s_reliability = 1.0 if mse_model <= 1e-12 else 0.0
        else:
            s_reliability = float(np.clip(1.0 - mse_model / mse_ref, 0.0, 1.0))

        # ---- adversarial head (macro-F1 over present classes) ----
        adv_pred = [_coerce_adv(v) for v in sub["pred_adversarial_idx"]]
        adv_true = [
            (str(v).strip() if str(v).strip() in ADV_VALID else "NONE")
            for v in ans["true_adversarial_idx"]
        ]
        s_adversarial = _macro_f1_multiclass(adv_true, adv_pred)

        final = (
            W_CONSENSUS * (s_consensus ** SCORE_POWER)
            + W_RELIABILITY * (s_reliability ** SCORE_POWER)
            + W_ADVERSARIAL * (s_adversarial ** SCORE_POWER)
        )
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
    score = grade(sub, ans)
    print(f"score={score:.6f}")
