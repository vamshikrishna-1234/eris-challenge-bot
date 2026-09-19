"""
grade.py - Molecular Substructure Fingerprint Prediction From Mass Spectra

The solver outputs a probability for each of 512 substructure bits per row.
Scoring uses the **Brier Skill Score (BSS)**, a proper scoring rule:

    BS      = mean over all (row, bit) of (pred_prob - true_bit)^2
    BS_ref  = mean over bits j of  p_hat_j * (1 - p_hat_j)
              where p_hat_j = P_HAT_TRAIN[j], the per-bit marginal frequency on
              the TRAINING split (a fixed climatological standard precomputed in
              prepare.py and embedded below) -- never the hidden test marginals.
    BSS     = 1 - BS / BS_ref

Interpretation:
    - BSS = 1.0: perfect calibrated predictions (every bit predicted with p=1/0)
    - BSS = 0.0: no better than the fixed training climatology baseline
    - BSS < 0  : worse than the climatology baseline → clipped to 0.0

Using the train-derived reference (rather than the test set's own marginals)
keeps the baseline a static, leakage-free standard: it cannot shift with the
particular test rows being graded.

Higher is better; bounded [0, 1].

Defensive contract: returns 0.0 on any structural error (missing columns, duplicate
ids, id mismatch, wrong-length probability vectors, exceptions).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

N_BITS = 512
PROB_SEP = ";"
# Hard cap on the pred_probs cell length BEFORE splitting. 512 floats at full
# repr (~24 chars) plus separators stay well under this, so any longer string is
# adversarial/garbage and is rejected up front to bound split/parse cost & memory.
MAX_PROBS_CHARS = 20000

# Per-bit TRAINING marginal frequencies (climatological reference). Precomputed
# by prepare.py over the training split and embedded verbatim so the Brier
# reference is a fixed standard independent of the test rows being graded.
P_HAT_TRAIN = [0.128598, 0.338291, 0.031925, 0.040195, 0.096545, 0.030899, 0.014745, 0.058401, 0.049234, 0.039490, 0.054234, 0.046349, 0.036797, 0.186102, 0.041028, 0.090839, 0.034618, 0.031092, 0.024873, 0.035707, 0.020642, 0.035259, 0.086416, 0.044298, 0.023271, 0.043208, 0.025514, 0.023848, 0.178088, 0.032246, 0.013655, 0.045836, 0.020258, 0.727034, 0.035964, 0.050131, 0.171998, 0.064235, 0.043657, 0.039233, 0.025707, 0.057504, 0.055645, 0.030387, 0.021412, 0.048144, 0.084941, 0.023976, 0.023078, 0.123982, 0.053529, 0.050772, 0.035195, 0.068979, 0.036541, 0.015257, 0.047247, 0.022245, 0.027502, 0.035195, 0.013142, 0.081159, 0.036925, 0.056478, 0.345535, 0.047952, 0.199372, 0.074492, 0.079556, 0.098019, 0.023912, 0.153984, 0.033335, 0.081864, 0.046221, 0.050901, 0.025322, 0.055196, 0.046413, 0.179563, 0.633566, 0.036861, 0.020899, 0.091865, 0.041349, 0.030258, 0.062568, 0.025002, 0.064299, 0.026412, 0.148215, 0.023143, 0.030066, 0.016796, 0.075261, 0.026861, 0.028592, 0.041862, 0.083275, 0.016411, 0.018335, 0.023527, 0.082634, 0.017693, 0.048529, 0.023207, 0.023719, 0.017373, 0.020771, 0.030130, 0.069299, 0.053337, 0.072569, 0.020322, 0.122316, 0.032502, 0.089301, 0.068658, 0.141676, 0.184435, 0.028271, 0.106545, 0.012052, 0.027245, 0.034105, 0.100712, 0.024553, 0.023271, 0.264440, 0.044298, 0.059170, 0.032823, 0.018911, 0.038592, 0.088916, 0.029489, 0.075005, 0.031540, 0.804667, 0.071158, 0.073851, 0.022309, 0.022566, 0.024425, 0.288224, 0.054683, 0.030002, 0.384127, 0.012693, 0.025066, 0.020129, 0.018527, 0.036477, 0.027822, 0.037374, 0.077569, 0.019296, 0.063658, 0.034105, 0.009552, 0.053657, 0.049811, 0.049042, 0.062055, 0.028527, 0.104237, 0.017373, 0.077313, 0.029553, 0.013911, 0.035130, 0.109366, 0.040836, 0.057888, 0.014680, 0.250914, 0.020771, 0.023784, 0.033977, 0.038015, 0.127380, 0.031156, 0.215014, 0.445670, 0.054042, 0.033400, 0.134624, 0.054555, 0.038079, 0.023848, 0.036797, 0.052311, 0.125649, 0.061927, 0.114751, 0.030258, 0.025771, 0.073851, 0.028720, 0.027374, 0.032502, 0.104173, 0.126611, 0.118982, 0.038849, 0.030066, 0.088083, 0.023271, 0.027502, 0.073338, 0.115200, 0.051478, 0.059812, 0.050388, 0.579973, 0.019553, 0.081736, 0.071094, 0.096545, 0.130906, 0.024809, 0.035707, 0.182768, 0.012180, 0.053337, 0.044490, 0.038400, 0.164305, 0.074941, 0.030387, 0.016988, 0.071799, 0.029745, 0.249952, 0.020899, 0.043849, 0.029617, 0.060132, 0.064363, 0.059427, 0.030515, 0.055901, 0.062889, 0.101545, 0.018142, 0.055965, 0.033528, 0.051414, 0.032438, 0.087442, 0.120072, 0.023078, 0.031605, 0.017822, 0.019681, 0.086352, 0.025643, 0.020578, 0.030194, 0.039938, 0.034361, 0.019681, 0.021540, 0.130457, 0.025386, 0.021540, 0.037182, 0.057824, 0.098852, 0.053016, 0.045195, 0.044618, 0.075902, 0.028079, 0.077826, 0.053465, 0.030322, 0.014360, 0.048401, 0.020065, 0.066286, 0.020450, 0.186294, 0.153792, 0.052952, 0.069940, 0.038272, 0.035579, 0.037759, 0.097955, 0.035964, 0.022886, 0.035002, 0.023207, 0.297455, 0.778640, 0.021412, 0.036861, 0.029617, 0.138278, 0.013334, 0.138727, 0.084557, 0.022053, 0.127252, 0.033977, 0.006988, 0.033079, 0.129880, 0.028656, 0.064299, 0.055196, 0.020386, 0.054747, 0.255465, 0.041605, 0.022117, 0.041669, 0.038143, 0.169947, 0.027374, 0.029810, 0.115713, 0.055773, 0.037567, 0.072633, 0.049426, 0.030258, 0.038785, 0.171998, 0.054170, 0.050580, 0.114687, 0.118790, 0.031925, 0.027886, 0.040836, 0.774601, 0.026732, 0.024489, 0.037887, 0.051093, 0.061607, 0.045195, 0.014424, 0.055837, 0.018655, 0.018847, 0.029297, 0.028015, 0.081031, 0.035900, 0.073787, 0.030387, 0.027822, 0.028527, 0.774024, 0.037887, 0.028015, 0.024489, 0.043400, 0.098083, 0.112828, 0.325277, 0.027053, 0.017950, 0.077377, 0.066350, 0.024489, 0.134560, 0.024168, 0.035002, 0.028784, 0.040644, 0.029681, 0.208988, 0.044426, 0.024168, 0.235271, 0.029681, 0.028335, 0.552279, 0.020065, 0.040836, 0.090647, 0.115456, 0.058273, 0.057311, 0.014680, 0.306494, 0.025450, 0.020642, 0.149369, 0.036156, 0.031156, 0.010642, 0.033656, 0.031476, 0.036925, 0.016860, 0.019681, 0.145458, 0.020771, 0.056863, 0.028592, 0.020514, 0.068594, 0.048721, 0.041413, 0.027117, 0.042118, 0.023655, 0.048144, 0.017565, 0.348804, 0.063209, 0.099686, 0.089429, 0.023784, 0.036156, 0.187127, 0.026284, 0.020065, 0.238733, 0.039810, 0.035707, 0.021604, 0.055004, 0.148279, 0.064235, 0.051542, 0.025643, 0.047952, 0.091993, 0.111674, 0.037246, 0.038400, 0.022501, 0.030194, 0.027309, 0.025771, 0.099814, 0.030387, 0.037887, 0.067056, 0.021924, 0.036605, 0.018976, 0.083275, 0.046093, 0.017758, 0.061414, 0.108789, 0.062504, 0.031284, 0.102442, 0.141035, 0.028784, 0.043336, 0.024040, 0.024489, 0.047567, 0.045131, 0.121995, 0.044234, 0.019424, 0.065196, 0.016860, 0.097827, 0.072376, 0.028207, 0.025066, 0.066094, 0.049875, 0.015834, 0.028720, 0.024361, 0.023078, 0.030707, 0.088980, 0.035643, 0.025707, 0.054042, 0.019681, 0.029297, 0.041285, 0.169370, 0.040964, 0.026027, 0.076607, 0.020065, 0.018719, 0.115136, 0.044875, 0.023399, 0.011411, 0.020899, 0.062889, 0.048529, 0.037502, 0.029104, 0.050131, 0.065709, 0.021476, 0.044105, 0.112635, 0.030643, 0.319700, 0.037310, 0.017758, 0.029874, 0.050196]
_P_HAT_TRAIN_ARR = np.asarray(P_HAT_TRAIN, dtype=np.float64)
# Fixed Brier reference from the training climatology (constant across all runs).
BS_REF_TRAIN = float(np.mean(_P_HAT_TRAIN_ARR * (1.0 - _P_HAT_TRAIN_ARR)))


def _parse_probs(s) -> np.ndarray | None:
    if s is None:
        return None
    t = str(s).strip()
    # bound parse cost / memory: reject implausibly long cells before splitting.
    if len(t) > MAX_PROBS_CHARS:
        return None
    parts = t.split(PROB_SEP)
    if len(parts) != N_BITS:
        return None
    try:
        arr = np.array([float(p) for p in parts], dtype=np.float64)
    except (ValueError, TypeError):
        return None
    if not np.all(np.isfinite(arr)):
        return None
    return np.clip(arr, 0.0, 1.0)


def _parse_bits(s) -> np.ndarray | None:
    if s is None:
        return None
    t = str(s).strip()
    if t[:1] in ("b", "B"):
        t = t[1:]
    if len(t) != N_BITS:
        return None
    if any(c not in "01" for c in t):
        return None
    return np.frombuffer(t.encode("ascii"), dtype=np.uint8) - ord("0")


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        if "id" not in submission.columns or "pred_probs" not in submission.columns:
            return 0.0
        if "id" not in answers.columns or "fingerprint" not in answers.columns:
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

        sub_map = dict(zip(sub["id"].tolist(), sub["pred_probs"].tolist()))

        n_rows = len(ans)
        true_mat = np.zeros((n_rows, N_BITS), dtype=np.float64)
        pred_mat = np.zeros((n_rows, N_BITS), dtype=np.float64)

        for i, (rid, fp_str) in enumerate(zip(ans["id"].tolist(), ans["fingerprint"].tolist())):
            tb = _parse_bits(fp_str)
            if tb is None:
                return 0.0
            true_mat[i] = tb.astype(np.float64)

            pb = _parse_probs(sub_map.get(rid))
            if pb is None:
                pb = np.full(N_BITS, 0.5, dtype=np.float64)
            pred_mat[i] = pb

        # Brier Score: mean over all (row, bit) of (pred - true)^2
        bs = float(np.mean((pred_mat - true_mat) ** 2))

        # Reference Brier Score: FIXED training climatology (embedded constant),
        # not the hidden test marginals -- a static, leakage-free baseline.
        bs_ref = BS_REF_TRAIN

        if bs_ref <= 0.0:
            return 1.0 if bs == 0.0 else 0.0

        bss = 1.0 - bs / bs_ref
        return float(np.clip(bss, 0.0, 1.0))

    except Exception:
        return 0.0
