"""
grade.py - SliceShuffle: Cranio-Caudal Sequence Reconstruction

Per-volume composite score:

    rank_score(volume) = max(0, kendall_tau(pred_rank, true_rank)) ** 2
    mask_score(volume) = macro_f1(pred_mask_48, true_mask_48) ** 2

    S(volume)          = 0.60 * rank_score + 0.40 * mask_score
    Final              = mean of S(volume) over test volumes, clipped [0,1]

Both per-volume metrics are squared so that a high-but-imperfect agent
sees its score compress aggressively at the top: a Kendall tau of 0.9
contributes 0.81 to rank_score (instead of 0.9), and a macro-F1 of 0.7
contributes 0.49 to mask_score. This widens the relative gap between
saturated agents and the theoretical perfect submission, leaving more
room for genuine human-vs-agent skill differentiation.

The two ingredients:
  * pred_rank is the agent's predicted cranio-caudal rank in {0..31}
    of every visible slice; tau is computed over the 32 (presented_index,
    rank) tuples of one volume. max(0, tau) ** 2 maps the [-1, +1] tau
    range to [0, 1], with anti-correlation collapsing to 0. A uniformly
    random permutation has E[tau] = 0, so it scores rank_score = 0 in
    expectation -- no free floor.
  * pred_missing_mask is a 48-char "0"/"1" string predicting which of
    the original 48 axial positions were dropped; macro_f1 averages the
    F1 of class "0" and class "1" over the 48 cells, then is squared.

The grader takes the *first row's* pred_missing_mask per volume_id (rows
are sorted by presented_index first) -- if the agent submits varying
masks per row of the same volume, only the first is used.

Submission columns (positional, header required):
    row_id            int            unique per row
    volume_id         int            matches public/test.csv
    presented_index   int 0..31      matches public/test.csv
    pred_rank         int 0..31      predicted rank for this slice
    pred_missing_mask str length 48  "0"/"1" chars; constant per volume

Robustness:
  * Missing rows: rows are matched on (volume_id, presented_index);
    any missing pair contributes pred_rank=0 and pred_missing_mask="0"*48.
  * pred_rank values out of range are clipped to [0, 31].
  * pred_missing_mask is sanitised to a 48-char "0"/"1" string; non-binary
    chars are stripped, over-long strings are truncated, short ones are
    right-padded with "0".
  * Duplicate (volume_id, presented_index) pairs in submission cause the
    grader to return 0.0 -- a clean submission must have one row per
    (volume_id, presented_index) tuple in test.csv.
  * Any unhandled exception during grading returns 0.0 rather than
    raising; the platform never blocks on a malformed submission.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


SLICES_PER_VOLUME = 48
SLICES_PRESENTED = 32

RANK_WEIGHT = 0.60
MASK_WEIGHT = 0.40


def _kendall_tau(x: np.ndarray, y: np.ndarray) -> float:
    """Kendall's tau-b for two equal-length integer sequences. O(n^2)."""
    n = int(x.shape[0])
    if n < 2:
        return 0.0
    concord = 0
    discord = 0
    tie_x = 0
    tie_y = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = int(x[i]) - int(x[j])
            dy = int(y[i]) - int(y[j])
            # Track ties in each variable independently (scipy tau-b
            # convention): a pair tied in x counts toward tie_x, a pair tied
            # in y counts toward tie_y, and a pair tied in BOTH counts toward
            # both. Only pairs untied in both are concordant/discordant.
            if dx == 0:
                tie_x += 1
            if dy == 0:
                tie_y += 1
            if dx != 0 and dy != 0:
                if (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                    concord += 1
                else:
                    discord += 1
    n_pairs = n * (n - 1) // 2
    denom = float(np.sqrt((n_pairs - tie_x) * (n_pairs - tie_y)))
    if denom <= 0.0:
        return 0.0
    return (concord - discord) / denom


def _macro_f1_binary(pred: np.ndarray, true: np.ndarray) -> float:
    """Macro F1 over the two classes {0, 1} for one 32-cell vector."""
    pred = pred.astype(np.int32)
    true = true.astype(np.int32)
    f1s: list[float] = []
    for cls in (0, 1):
        tp = int(np.sum((pred == cls) & (true == cls)))
        fp = int(np.sum((pred == cls) & (true != cls)))
        fn = int(np.sum((pred != cls) & (true == cls)))
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


def _sanitize_mask(value) -> np.ndarray:
    """Coerce any submission cell into a length-32 0/1 vector. The
    canonical encoding is the 33-char string `"M" + 32 chars in {"0","1"}`,
    but the grader is permissive: any non-binary characters are stripped,
    and the result is right-padded or truncated to exactly 32 entries."""
    s = "" if value is None else str(value)
    s = "".join(c for c in s if c in ("0", "1"))
    if len(s) > SLICES_PER_VOLUME:
        s = s[:SLICES_PER_VOLUME]
    elif len(s) < SLICES_PER_VOLUME:
        s = s + "0" * (SLICES_PER_VOLUME - len(s))
    return np.array([int(c) for c in s], dtype=np.int32)


def _coerce_int(value, lo: int, hi: int) -> int:
    try:
        v = int(float(value))
    except (TypeError, ValueError):
        return lo
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Score submission vs `answers` (private/answers.csv). Composite of squared max(0, Kendall-tau) on cranio-caudal ranks and squared macro-F1 on the 48-cell missing-position mask, weighted 0.6 and 0.4."""
    try:
        required = {"row_id", "volume_id", "presented_index", "pred_rank", "pred_missing_mask"}
        missing_cols = required - set(submission.columns)
        if missing_cols:
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        sub["volume_id"] = sub["volume_id"].astype(int)
        sub["presented_index"] = sub["presented_index"].astype(int)
        ans["volume_id"] = ans["volume_id"].astype(int)
        ans["presented_index"] = ans["presented_index"].astype(int)

        if sub.duplicated(subset=["volume_id", "presented_index"]).any():
            return 0.0

        sub_lookup = {
            (int(r.volume_id), int(r.presented_index)): r
            for r in sub.itertuples(index=False)
        }

        per_volume_scores: list[float] = []
        for vol_id, group in ans.groupby("volume_id", sort=True):
            group = group.sort_values("presented_index")
            true_ranks = group["true_rank"].astype(int).to_numpy()
            true_mask = _sanitize_mask(group["true_missing_mask"].iloc[0])

            pred_ranks = np.zeros(len(group), dtype=np.int32)
            pred_mask_first = np.zeros(SLICES_PER_VOLUME, dtype=np.int32)
            first_seen = False
            for k, row in enumerate(group.itertuples(index=False)):
                pi = int(row.presented_index)
                sub_row = sub_lookup.get((int(vol_id), pi))
                if sub_row is None:
                    continue
                pred_ranks[k] = _coerce_int(sub_row.pred_rank, 0, SLICES_PRESENTED - 1)
                if not first_seen:
                    pred_mask_first = _sanitize_mask(sub_row.pred_missing_mask)
                    first_seen = True

            tau = _kendall_tau(pred_ranks, true_ranks)
            rank_score = max(0.0, tau) ** 2
            mask_f1 = _macro_f1_binary(pred_mask_first, true_mask)
            mask_score = mask_f1 ** 2
            per_volume_scores.append(
                RANK_WEIGHT * rank_score + MASK_WEIGHT * mask_score
            )

        if not per_volume_scores:
            return 0.0
        final = float(np.mean(per_volume_scores))
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
