"""End-to-end smoke test: generate a tiny corpus, run prepare(), then grade
a range of submissions.

Checks: perfect ~1.0, sample baseline < 0.5, malformed -> degrades (no crash),
bad confidence -> 0.0, structural failures -> 0.0, prepare deterministic.

Run:  python _sanity_smoke.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

import grade as G
from prepare import prepare

ROOT = Path("_smoke")
RAW = ROOT / "raw"
PUB = ROOT / "pub"
PRIV = ROOT / "priv"

SUB_COLS = ["id", "pairing_json", "n_true_locks", "pull_outcome",
            "pull_taut_json", "confidence"]


def build_raw() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    RAW.mkdir(parents=True)
    subprocess.run([sys.executable, "generate.py", "--out", str(RAW),
                    "--n-base", "12", "--seed", "5"], check=True)


def main() -> None:
    build_raw()
    prepare(RAW, PUB, PRIV)

    ans = pd.read_csv(PRIV / "answers.csv")
    print(f"\ntrain: {len(pd.read_csv(PUB/'train.csv'))}  test: {len(ans)}")

    perfect = ans[["id", "pairing_json", "n_true_locks", "pull_outcome",
                   "pull_taut_json"]].copy()
    perfect["confidence"] = 1.0

    base = pd.read_csv(PUB / "sample_submission.csv")

    # malformed JSON cells (valid confidence) -> degrade, not crash
    bad = perfect.copy()
    bad["pairing_json"] = bad["pairing_json"].astype(object)
    bad["pull_taut_json"] = bad["pull_taut_json"].astype(object)
    bad.loc[bad.index[:3], "pairing_json"] = "{not-json"
    bad.loc[bad.index[:3], "pull_taut_json"] = "[oops"

    badconf = perfect.copy()
    badconf["confidence"] = badconf["confidence"].astype(float)
    badconf.loc[badconf.index[:1], "confidence"] = 5.0

    s_perfect = G.grade(perfect[SUB_COLS], ans)
    s_base = G.grade(base, ans)
    s_bad = G.grade(bad[SUB_COLS], ans)
    s_badconf = G.grade(badconf[SUB_COLS], ans)

    miss = perfect.drop(columns=["pull_outcome"])
    dup = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
    short = perfect.iloc[:-1].copy()
    extra = perfect.copy()
    extra["extra_col"] = "not allowed"
    neg_lock = perfect.copy()
    neg_lock.loc[neg_lock.index[:1], "n_true_locks"] = -1
    s_miss = G.grade(miss, ans)
    s_dup = G.grade(dup[SUB_COLS], ans)
    s_short = G.grade(short[SUB_COLS], ans)
    s_extra = G.grade(extra, ans)
    s_neg_lock = G.grade(neg_lock[SUB_COLS], ans)

    priv2 = ROOT / "priv2"
    prepare(RAW, ROOT / "pub2", priv2)
    ans2 = pd.read_csv(priv2 / "answers.csv")
    deterministic = ans.equals(ans2)

    print("\n--- scores ---")
    print(f"perfect              : {s_perfect:.4f}  (expect ~1.0)")
    print(f"sample baseline      : {s_base:.4f}  (expect < 0.5)")
    print(f"malformed cells      : {s_bad:.4f}  (no crash; degrades)")
    print(f"bad-confidence       : {s_badconf:.4f}  (expect 0.0)")
    print(f"missing-col          : {s_miss:.4f}  (expect 0.0)")
    print(f"extra-col            : {s_extra:.4f}  (expect 0.0)")
    print(f"negative-lock-count  : {s_neg_lock:.4f}  (expect 0.0)")
    print(f"duplicate-id         : {s_dup:.4f}  (expect 0.0)")
    print(f"row-mismatch         : {s_short:.4f}  (expect 0.0)")
    print(f"prepare deterministic: {deterministic}")

    assert s_perfect > 0.98, "perfect should score ~1.0"
    assert s_base < 0.50, "sample baseline should leave headroom"
    assert 0.0 <= s_bad < 1.0, "malformed cells should degrade, not crash"
    assert s_badconf == 0.0, "invalid confidence must hard-fail"
    assert s_miss == 0.0 and s_extra == 0.0 and s_dup == 0.0 and s_short == 0.0, "structural -> 0.0"
    assert s_neg_lock == 0.0, "negative lock counts must hard-fail"
    assert deterministic, "prepare must be deterministic"
    print("\nOK: smoke test passed.")
    shutil.rmtree(ROOT, ignore_errors=True)


if __name__ == "__main__":
    main()
