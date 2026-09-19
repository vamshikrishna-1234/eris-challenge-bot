"""
grade.py - Volumetric Identity And Mismatch Inference From Orthogonal Slices

Composite score (one scalar per submission, computed over the test set):

    S_corpus    = macro-F1 across the 6 corpus_id classes {0..5}
    S_class     = mean over CLEAN rows (true_mismatched_triplet == 0) of
                  [1 if pred_class_label == true_class_label else 0]
    S_radius    = mean over rows of
                    max(0, 1 - 40 * (pred_vol_radius - true_vol_radius)^2)
    S_mismatch  = mean over rows of
                    [1 if pred_mismatched_triplet == true_mismatched_triplet else 0]
    S_axis      = macro-F1 across {NONE, AXIAL, SAGITTAL, CORONAL}, computed
                  over the entire test set

    S_partial = 0.05 * S_corpus + 0.25 * S_class + 0.20 * S_radius
              + 0.20 * S_mismatch + 0.30 * S_axis

    S_joint   = fraction of test rows for which EVERY head is correct on that
                same row (corpus + radius-within-tol + coherence + axis, plus
                class on clean rows; class is excluded on intruder rows where
                the underlying class is undefined)

    Final     = 0.5 * S_partial + 0.5 * S_joint   (clipped to [0, 1])

Why the joint term (revision 3):
  A weighted average of per-head partial credit rewards a solution for being
  "pretty good on each head", so a broadly-competent agent saturates near the
  top even when it rarely gets a whole sample right. S_joint is a per-sample
  all-heads-correct rate; since it is bounded above by the weakest head, it
  sharply lowers a broadly-mediocre solution and widens the gap between good
  and great submissions (a rule-endorsed "combined metric for a better score
  distribution"). The 0.5/0.5 blend keeps the score smooth and solvable
  (partial credit) while removing the ceiling saturation (joint term).

Partial-composite weighting rationale:
  * S_corpus is a token 0.05 (six visually-distinct corpora -> nearly free).
  * S_axis carries the most weight (0.30): naming WHICH view is the intruder
    is the single hardest head.
  * S_class 0.25, S_radius 0.20, S_mismatch 0.20.
  * S_radius Brier scale is 40 (within ~0.05 of the true extent to score ~0.9).
  * RADIUS_TOL (0.10) sets when radius counts as correct in the joint term.

Submission validation (revision):
  Predictions must be well-formed and in-domain. The grader does NOT silently
  coerce malformed values to defaults; instead the whole submission scores 0.0
  if ANY cell is invalid. A correct solution always emits valid values, so this
  only penalises broken/sloppy output (and removes the previous behaviour that
  masked solution bugs by coercing them). Specifically the grader returns 0.0
  when:
    * any required column is missing, ids are duplicated, or the id-set does
      not match the answers exactly;
    * pred_corpus_id is not an integer in {0,1,2,3,4,5};
    * pred_class_label is not a non-negative integer;
    * pred_vol_radius is not a finite float in [0, 1] (a tiny float-rounding
      epsilon is tolerated and then clamped);
    * pred_mismatched_triplet is not exactly 0 or 1;
    * pred_mismatched_axis is not one of NONE/AXIAL/SAGITTAL/CORONAL
      (case-insensitive);
    * any unhandled exception occurs during grading.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

GLOBAL_NCORPORA = 6
AXIS_VALID = {"NONE", "AXIAL", "SAGITTAL", "CORONAL"}

# --- partial-credit composite head weights (sum to 1.0) ---
W_CORPUS = 0.05
W_CLASS = 0.25
W_RADIUS = 0.20
W_MISMATCH = 0.20
W_AXIS = 0.30

# --- blend between partial-credit composite and per-sample joint exact-match ---
W_PARTIAL = 0.5
W_JOINT = 0.5

RADIUS_BRIER_SCALE = 40.0
RADIUS_EPS = 1e-6
# Tolerance for counting the radius "correct" inside the joint exact-match term.
RADIUS_TOL = 0.10


def _val_int_in_range(v, lo: int, hi: int):
    """Return int in [lo, hi] or None if not an integer-valued, in-range value."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(f):
        return None
    if abs(f - round(f)) > 1e-9:
        return None
    iv = int(round(f))
    if iv < lo or iv > hi:
        return None
    return iv


def _val_nonneg_int(v):
    """Return non-negative int or None."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(f):
        return None
    if abs(f - round(f)) > 1e-9:
        return None
    iv = int(round(f))
    return iv if iv >= 0 else None


def _val_radius(v):
    """Return float clamped to [0,1], or None if non-finite / outside [0,1]."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(f):
        return None
    if f < -RADIUS_EPS or f > 1.0 + RADIUS_EPS:
        return None
    return float(min(1.0, max(0.0, f)))


def _val_binary(v):
    """Return 0 or 1, or None."""
    iv = _val_int_in_range(v, 0, 1)
    return iv


def _val_axis(v):
    """Return canonical axis name or None."""
    if v is None:
        return None
    s = str(v).strip().upper()
    return s if s in AXIS_VALID else None


def _macro_f1(y_true: list, y_pred: list, classes) -> float:
    f1s: list[float] = []
    for cls in classes:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        if tp + fp == 0 and tp + fn == 0:
            f1s.append(1.0)
            continue
        if tp == 0:
            f1s.append(0.0)
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Score submission vs `answers` (private/answers.csv).

    Strict: any malformed/out-of-domain prediction cell makes the whole
    submission score 0.0 (no silent coercion). See module docstring.
    """
    try:
        required_sub = {
            "id", "pred_corpus_id", "pred_class_label", "pred_vol_radius",
            "pred_mismatched_triplet", "pred_mismatched_axis",
        }
        required_ans = {
            "id", "true_corpus_id", "true_class_label", "true_vol_radius",
            "true_mismatched_triplet", "true_mismatched_axis",
        }
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

        merged = ans.merge(sub, on="id", how="left", suffixes=("", "_sub"))
        if merged["pred_corpus_id"].isna().any():
            return 0.0

        corpus_pred: list[int] = []
        corpus_true: list[int] = []
        class_clean_correct: list[int] = []
        radius_terms: list[float] = []
        mismatch_correct: list[int] = []
        axis_pred: list[str] = []
        axis_true: list[str] = []
        joint_correct: list[int] = []

        for _, row in merged.iterrows():
            # ---- strict validation of every predicted cell ----
            pc = _val_int_in_range(row["pred_corpus_id"], 0, GLOBAL_NCORPORA - 1)
            if pc is None:
                return 0.0
            pred_class = _val_nonneg_int(row["pred_class_label"])
            if pred_class is None:
                return 0.0
            pr = _val_radius(row["pred_vol_radius"])
            if pr is None:
                return 0.0
            pred_mismatched = _val_binary(row["pred_mismatched_triplet"])
            if pred_mismatched is None:
                return 0.0
            pa = _val_axis(row["pred_mismatched_axis"])
            if pa is None:
                return 0.0

            tc = int(row["true_corpus_id"])
            corpus_true.append(tc)
            corpus_pred.append(pc)

            true_class = int(row["true_class_label"])
            true_mismatched = int(row["true_mismatched_triplet"])

            if true_mismatched == 0:
                class_clean_correct.append(1 if pred_class == true_class else 0)

            tr = float(row["true_vol_radius"])
            radius_terms.append(max(0.0, 1.0 - RADIUS_BRIER_SCALE * (pr - tr) ** 2))

            mismatch_correct.append(1 if pred_mismatched == true_mismatched else 0)

            ta = str(row["true_mismatched_axis"]).strip().upper()
            if ta not in AXIS_VALID:
                ta = "NONE"
            axis_true.append(ta)
            axis_pred.append(pa)

            # ---- per-sample JOINT exact-match (all heads right on one row) ----
            ok_corpus = (pc == tc)
            ok_radius = (abs(pr - tr) <= RADIUS_TOL)
            ok_mismatch = (pred_mismatched == true_mismatched)
            ok_axis = (pa == ta)
            ok_class = (pred_class == true_class)
            if true_mismatched == 0:
                # clean row: corpus + class + radius + coherence + axis(=NONE)
                row_ok = ok_corpus and ok_class and ok_radius and ok_mismatch and ok_axis
            else:
                # intruder row: class is undefined, so it is excluded
                row_ok = ok_corpus and ok_radius and ok_mismatch and ok_axis
            joint_correct.append(1 if row_ok else 0)

        s_corpus = _macro_f1(corpus_true, corpus_pred, classes=list(range(GLOBAL_NCORPORA)))
        s_class = float(np.mean(class_clean_correct)) if class_clean_correct else 0.0
        s_radius = float(np.mean(radius_terms)) if radius_terms else 0.0
        s_mismatch = float(np.mean(mismatch_correct)) if mismatch_correct else 0.0
        s_axis = _macro_f1(axis_true, axis_pred, classes=["NONE", "AXIAL", "SAGITTAL", "CORONAL"])

        # Partial-credit composite: rewards per-head competence (smooth, solvable).
        s_partial = (
            W_CORPUS * s_corpus
            + W_CLASS * s_class
            + W_RADIUS * s_radius
            + W_MISMATCH * s_mismatch
            + W_AXIS * s_axis
        )
        # Joint exact-match: rewards getting an ENTIRE sample right. This is
        # <= the weakest head, so it sharply penalises a broadly-mediocre
        # solution and widens the gap between good and great submissions.
        s_joint = float(np.mean(joint_correct)) if joint_correct else 0.0

        final = W_PARTIAL * s_partial + W_JOINT * s_joint
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
