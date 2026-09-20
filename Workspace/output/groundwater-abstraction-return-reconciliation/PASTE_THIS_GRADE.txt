"""
grade.py - Groundwater Abstraction Return Reconciliation

Two scored heads, both referenced to a trivial predictor so that no-op,
empty, constant and random submissions sit at the floor.

  ledger  (0.62) - on every borehole whose declared return is materially wrong,
                   the fraction of the declaration's volume error that the
                   submission removes, expressed as skill over the BEST trivial
                   strategy. Copying the declaration and reporting zero
                   abstraction everywhere both score 0; recovering the actual
                   ledgers scores 1.
  aquifer (0.38) - accuracy of log10 transmissivity and log10 storage
                   coefficient, expressed as skill over the best constant
                   (mid-range) predictor.

Both heads are rectified at GROUP level, never per row, so a lucky row cannot
lift the floor. The global score is the mean of the group scores.

Range: 0.0 (empty, invalid, id-mismatched, a verbatim copy of the declared
returns, or an all-zero ledger) to 1.0 (exact recovery).
"""

import json

import numpy as np
import pandas as pd

KB = 7
W_LEDGER = 0.62
W_AQUIFER = 0.38

TAU = 100.0            # m^3/day summed over blocks: materially wrong declaration
S_LOGT = 0.12
S_LOGS = 0.18
LOGT_MID = 0.5 * (1.477 + 2.903)
LOGS_MID = 0.5 * (-3.301 + -1.523)

MAX_JSON_LEN = 200000  # cap before parsing so a pathological cell cannot stall
MAX_BOREHOLES = 40


def _ledger_matrix(value, n_rows):
    """Parse a JSON list-of-lists into an (n_rows, KB) nonnegative array.
    Anything malformed degrades to zeros and never raises."""
    out = np.zeros((n_rows, KB))
    s = str(value)
    if len(s) > MAX_JSON_LEN:
        return out
    try:
        obj = json.loads(s)
    except Exception:
        return out
    if not isinstance(obj, list):
        return out
    for i, row in enumerate(obj[:min(n_rows, MAX_BOREHOLES)]):
        if not isinstance(row, (list, tuple)):
            continue
        for k, v in enumerate(row[:KB]):
            try:
                x = float(v)
            except (TypeError, ValueError):
                continue
            if np.isfinite(x) and x >= 0.0:
                out[i, k] = x
    return out


def _scalar(value):
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def _aq_credit(lt, ls, true_lt, true_ls):
    if lt is None or ls is None:
        return 0.0
    return float(0.5 * np.exp(-abs(lt - true_lt) / S_LOGT)
                 + 0.5 * np.exp(-abs(ls - true_ls) / S_LOGS))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        if submission is None or answers is None or len(answers) == 0:
            return 0.0
        sub = submission.copy()
        if "id" not in sub.columns:
            return 0.0
        sub["id"] = pd.to_numeric(sub["id"], errors="coerce")
        sub = sub.dropna(subset=["id"]).drop_duplicates(subset=["id"], keep="first")
        sub["id"] = sub["id"].astype(np.int64)
        by_id = sub.set_index("id")

        matched_any = bool(set(by_id.index) & set(pd.to_numeric(answers["id"], errors="coerce").dropna().astype(np.int64)))
        if not matched_any:
            return 0.0

        groups = {}
        for _, a in answers.iterrows():
            rid = int(a["id"])
            g = int(a["score_group"]) if "score_group" in answers.columns else 0
            act = _ledger_matrix(a["actual"], MAX_BOREHOLES)
            dec = _ledger_matrix(a["declared"], MAX_BOREHOLES)
            n_bh = int(a["n_boreholes"]) if "n_boreholes" in answers.columns else MAX_BOREHOLES
            act, dec = act[:n_bh], dec[:n_bh]

            if rid in by_id.index:
                row = by_id.loc[rid]
                pred = _ledger_matrix(row.get("actual", ""), n_bh)
                lt = _scalar(row.get("log_t")); ls = _scalar(row.get("log_s"))
            else:
                pred = np.zeros((n_bh, KB)); lt = ls = None

            b = groups.setdefault(g, {"fix": [], "fix_ref": [], "aq": [], "ref": []})
            err_dec = np.abs(dec - act).sum(axis=1)
            for i in range(n_bh):
                if err_dec[i] > TAU:
                    b["fix"].append(max(0.0, 1.0 - float(np.abs(pred[i] - act[i]).sum()) / err_dec[i]))
                    # best trivial strategy on this borehole: keep the declared
                    # return (credit 0) or report no abstraction at all
                    b["fix_ref"].append(max(0.0, 1.0 - float(np.abs(act[i]).sum()) / err_dec[i]))
            b["aq"].append(_aq_credit(lt, ls, float(a["log_t"]), float(a["log_s"])))
            b["ref"].append(_aq_credit(LOGT_MID, LOGS_MID, float(a["log_t"]), float(a["log_s"])))

        scores = []
        for g, b in groups.items():
            fix = float(np.mean(b["fix"])) if b["fix"] else 0.0
            fix_ref = float(np.mean(b["fix_ref"])) if b["fix_ref"] else 0.0
            fix_skill = max(0.0, (fix - fix_ref) / (1.0 - fix_ref)) if fix_ref < 1.0 else 0.0
            aq = float(np.mean(b["aq"])) if b["aq"] else 0.0
            ref = float(np.mean(b["ref"])) if b["ref"] else 0.0
            aq_skill = max(0.0, (aq - ref) / (1.0 - ref)) if ref < 1.0 else 0.0
            scores.append(W_LEDGER * fix_skill + W_AQUIFER * aq_skill)
        if not scores:
            return 0.0
        return float(np.clip(np.mean(scores), 0.0, 1.0))
    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", required=True)
    ap.add_argument("--answers", required=True)
    a = ap.parse_args()
    print("score=%.6f" % grade(pd.read_csv(a.submission), pd.read_csv(a.answers)))
