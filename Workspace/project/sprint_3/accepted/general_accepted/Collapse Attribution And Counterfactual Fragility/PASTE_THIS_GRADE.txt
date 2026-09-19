"""
grade.py - Collapse Attribution And Counterfactual Fragility

Composite score (one scalar per submission), each sub-score squared before
weighting:

    S_collapse  = Brier Skill Score of the predicted collapse probability
                  against the dataset collapse base-rate.
                      p   = predicted P(collapse) in [0, 1]
                      y   = true collapse outcome in {0, 1}
                      MSE_model = mean (p - y)^2
                      ref       = 0.5  (static climatology; MSE_ref = 0.25)
                      MSE_ref   = mean (ref - y)^2
                      S_collapse = clip(1 - MSE_model/MSE_ref, 0, 1)
                  A constant 0.5 predictor scores 0; only true skill scores > 0.

    S_initiator = macro-F1 over the initiator classes (the block id that first
                  loses support, or "NONE" if the stack is stable). "NONE" is
                  ALWAYS an equally-weighted scored class; numeric block-id
                  classes are scored when they occur in the ground truth. A
                  trivial "always NONE" submission therefore cannot coast.

    S_keystone  = mean keystone accuracy. Per scene: 1.0 if the predicted
                  counterfactual keystone equals the true top-1 keystone,
                  0.5 if it equals the (non-NONE) second-most-impactful block,
                  else 0.0.

    Final = 0.30 * S_collapse^2
          + 0.35 * S_initiator^2
          + 0.35 * S_keystone^2          clipped to [0, 1]

The two causal heads (initiator + keystone) carry the dominant 0.70 weight:
they are simulator-verified and cannot be read off appearance, so a stability-
only model stalls well below the ceiling. Squaring compresses the high end so
a strong-but-naive model cannot coast to a high composite, while a true oracle
(all sub-scores 1.0) still reaches 1.0.

Submission columns (header required):
    id                   int    unique per scene, matches test.csv
    will_collapse        float  predicted P(collapse) in [0, 1]
    initiator_block_id   str    a block id ("0","1",...) or "NONE"
    keystone_block_id    str    a block id ("0","1",...) or "NONE"

Robustness (documented coercion):
  * Missing rows / missing columns          -> grade returns 0.0.
  * Duplicate ids in submission             -> grade returns 0.0.
  * Submission row-set != answers row-set   -> grade returns 0.0.
  * will_collapse out of range is clipped to [0, 1]; non-numeric -> 0.5.
  * initiator/keystone values that are not a non-negative integer or "NONE"
    are coerced to "NONE".
  * Any unhandled exception during grading returns 0.0 (never raises).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

W_COLLAPSE = 0.30
W_INITIATOR = 0.35
W_KEYSTONE = 0.35
SCORE_POWER = 2.0


def _coerce_prob(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.5
    if not np.isfinite(x):
        return 0.5
    return float(np.clip(x, 0.0, 1.0))


def _coerce_label(v) -> str:
    """A block id ("0","1",...) or the sentinel "NONE"."""
    if v is None:
        return "NONE"
    s = str(v).strip()
    if s == "" or s.upper() == "NONE":
        return "NONE"
    try:
        f = float(s)
        if np.isfinite(f):
            n = int(round(f))
            if n >= 0:
                return str(n)
    except (TypeError, ValueError):
        pass
    return "NONE"


def _macro_f1(y_true: list[str], y_pred: list[str]) -> float:
    """Macro-F1 with EQUAL class weight. "NONE" is always a scored class;
    numeric block-id classes are scored only when they occur in y_true (an
    absent class's degenerate case would otherwise inflate the average)."""
    present = sorted({c for c in y_true if c != "NONE"}, key=lambda s: int(s))
    present.append("NONE")
    f1s: list[float] = []
    for cls in present:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        # A class that is absent from BOTH truth and predictions (TP+FP+FN == 0)
        # is undefined under F1; exclude it from the macro average rather than
        # scoring it 0 (standard behaviour). "NONE" has support in practice, so
        # it is still scored as an equally-weighted class and cannot be coasted.
        if tp + fp + fn == 0:
            continue
        if tp == 0:
            f1s.append(0.0)
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s)) if f1s else 0.0


def _brier_skill(p: np.ndarray, y: np.ndarray) -> float:
    # Reference is a STATIC climatology of 0.5 (max-entropy prior), not the
    # empirical test-set mean. With y in {0, 1} this fixes mse_ref = 0.25, so
    # the reference can never collapse to a zero-variance floor regardless of
    # the test label balance, and the skill score is comparable across splits.
    mse_model = float(np.mean((p - y) ** 2))
    ref = 0.5
    mse_ref = float(np.mean((ref - y) ** 2))
    if mse_ref <= 1e-12:
        return 1.0 if mse_model <= 1e-12 else 0.0
    return float(np.clip(1.0 - mse_model / mse_ref, 0.0, 1.0))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Composite: 0.30*collapse_BSS^2 + 0.35*initiator_F1^2 + 0.35*keystone^2."""
    try:
        required_sub = {"id", "will_collapse", "initiator_block_id", "keystone_block_id"}
        required_ans = {"id", "will_collapse", "initiator_block_id",
                        "keystone_block_id", "keystone_alt_block_id"}
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

        sub = sub.set_index("id").reindex(ans["id"].to_numpy()).reset_index()

        # ---- collapse head ----
        p = np.array([_coerce_prob(v) for v in sub["will_collapse"]], dtype=float)
        y = ans["will_collapse"].astype(float).to_numpy()
        s_collapse = _brier_skill(p, y)

        # ---- initiator head ----
        init_pred = [_coerce_label(v) for v in sub["initiator_block_id"]]
        init_true = [_coerce_label(v) for v in ans["initiator_block_id"]]
        s_initiator = _macro_f1(init_true, init_pred)

        # ---- keystone head ----
        key_pred = [_coerce_label(v) for v in sub["keystone_block_id"]]
        key_true = [_coerce_label(v) for v in ans["keystone_block_id"]]
        key_alt = [_coerce_label(v) for v in ans["keystone_alt_block_id"]]
        kscores = []
        for pr, kt, ka in zip(key_pred, key_true, key_alt):
            if pr == kt:
                kscores.append(1.0)
            elif ka != "NONE" and pr == ka:
                kscores.append(0.5)
            else:
                kscores.append(0.0)
        s_keystone = float(np.mean(kscores)) if kscores else 0.0

        final = (
            W_COLLAPSE * (s_collapse ** SCORE_POWER)
            + W_INITIATOR * (s_initiator ** SCORE_POWER)
            + W_KEYSTONE * (s_keystone ** SCORE_POWER)
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
    print(f"score={grade(sub, ans):.6f}")
