"""End-to-end smoke test: build a tiny raw corpus, run prepare(), then grade a
range of submissions. Checks perfect~1, sample-baseline<0.5, malformed->0, and
that structural failures hard-zero."""
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

import grade as G
from prepare import prepare

ROOT = Path("_smoke")
RAW = ROOT / "raw"; PUB = ROOT / "pub"; PRIV = ROOT / "priv"


def build_raw():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    RAW.mkdir(parents=True)
    subprocess.run([sys.executable, "generate.py", "--out", str(RAW),
                    "--n-base", "8", "--seed", "5"], check=True)


def main():
    build_raw()
    prepare(RAW, PUB, PRIV)
    ans = pd.read_csv(PRIV / "answers.csv")
    print(f"\ntest clips: {len(ans)}")

    # perfect: copy labels, confidence matched to a perfect correctness (=1.0)
    perfect = ans[["id", "occupancy", "n_obstacles", "query_hit_row"]].copy()
    perfect["confidence"] = 1.0

    # sample baseline (what prepare ships)
    base = pd.read_csv(PUB / "sample_submission.csv")

    # all-empty but well-calibrated low confidence
    empty = base.copy(); empty["confidence"] = 0.35

    # map perfect, but count/query wrong + overconfident
    half = perfect.copy(); half["n_obstacles"] = 0; half["query_hit_row"] = -1

    # malformed confidence -> hard zero
    badconf = perfect.copy(); badconf["confidence"] = 5.0

    # over-long occupancy string -> degrades, must not crash
    longocc = perfect.copy(); longocc["occupancy"] = "1" * 5000

    print("--- scores ---")
    print(f"perfect              : {G.grade(perfect, ans):.4f}  (expect ~1.0)")
    print(f"sample baseline      : {G.grade(base, ans):.4f}  (expect < 0.5)")
    print(f"all-empty conf=.35   : {G.grade(empty, ans):.4f}")
    print(f"map-only (n/q wrong) : {G.grade(half, ans):.4f}")
    print(f"malformed confidence : {G.grade(badconf, ans):.4f}  (expect 0.0)")
    print(f"over-long occupancy  : {G.grade(longocc, ans):.4f}  (no crash; degrades)")

    # structural failures
    miss = perfect.drop(columns=["query_hit_row"])
    print(f"missing column       : {G.grade(miss, ans):.4f}  (expect 0.0)")
    dup = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
    print(f"duplicate id         : {G.grade(dup, ans):.4f}  (expect 0.0)")
    short = perfect.iloc[:-1].copy()
    print(f"missing row          : {G.grade(short, ans):.4f}  (expect 0.0)")


if __name__ == "__main__":
    main()
