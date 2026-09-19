"""Leakage + difficulty analysis (no image decode; uses the exact braid sim).

Confirms:
  - label distributions are balanced; n_cables / pull_endpoint do not leak the
    pull outcome,
  - a best-constant baseline scores < 0.5,
  - a "trace-only" shortcut (pairing + locks right, counterfactual guessed) is
    capped,
  - a tracing ORACLE scores ~1.0, while a strong but partly tangle-limited solver
    sits < ~0.7 because buried cables and long cascades cannot be fully read.

Run:  python _analyze.py
"""

import json

import numpy as np
import pandas as pd

import generate as gen
from grade import grade

N_BASE = 600
SEED = 44


def build_answers(scenes):
    rows = []
    for i, s in enumerate(scenes):
        rows.append({
            "id": i,
            "pairing_json": s["pairing_json"],
            "n_true_locks": s["n_true_locks"],
            "pull_outcome": s["pull_outcome"],
            "pull_taut_json": s["pull_taut_json"],
            "tangle_family": s["tangle_family"],
            "render_style": s["render_style"],
            "split_group": f"{s['tangle_family']}__{s['variant']}",
            "ood_axis": s["ood_axis"],
            "n_cables": s["n"],
            "pull_endpoint": f"T{s['query']}",
        })
    return pd.DataFrame(rows)


def dist(series):
    return series.value_counts(normalize=True).round(3).to_dict()


def main():
    scenes = gen.sample_all_scenes(SEED, N_BASE)
    ans = build_answers(scenes)
    n = len(ans)
    print(f"scenes: {n}")
    print("\n-- label distributions --")
    print(f"  pull_outcome : {dist(ans['pull_outcome'])}")
    print(f"  n_true_locks : {dist(ans['n_true_locks'])}")
    print(f"  n_cables     : {dist(ans['n_cables'])}")
    print(f"  ood_axis     : {dist(ans['ood_axis'])}")
    casc_len = ans["pull_taut_json"].map(lambda s: len(json.loads(s)))
    print(f"  cascade len  : mean={casc_len.mean():.2f} max={casc_len.max()} "
          f"frac_empty={float((casc_len==0).mean()):.3f}")

    print("\n-- leakage: pull_outcome by n_cables --")
    for nc in sorted(ans["n_cables"].unique()):
        sub = ans[ans["n_cables"] == nc]
        print(f"  n={nc} (m={len(sub):4d}): {dist(sub['pull_outcome'])}")

    grader_ans = ans.drop(columns=["n_cables", "pull_endpoint"])

    def sub_from(fn):
        rows = []
        for i, s in enumerate(scenes):
            pj, nl, po, pt, conf = fn(s, i)
            rows.append({"id": i, "pairing_json": pj, "n_true_locks": nl,
                         "pull_outcome": po, "pull_taut_json": pt, "confidence": conf})
        return pd.DataFrame(rows)

    def all_unknown_pair(s):
        return json.dumps({f"T{k}": "unknown" for k in range(s["n"])})

    # 1) best-constant over the discrete heads
    best_const = 0.0
    for po in ["slips", "locks", "unknown"]:
        for nl in [0, 1, 2]:
            sub = sub_from(lambda s, i: (all_unknown_pair(s), nl, po, "[]", 0.4))
            best_const = max(best_const, grade(sub, grader_ans))
    print(f"\nbest-constant baseline : {best_const:.4f}  (want < 0.5)")

    sample = sub_from(lambda s, i: (all_unknown_pair(s), 1, "slips", "[]", 0.3))
    print(f"shipped sample prior   : {grade(sample, grader_ans):.4f}  (want >= ~0.12)")

    # 2) trace-only: pairing + locks right, counterfactual guessed
    trace = sub_from(lambda s, i: (s["pairing_json"], s["n_true_locks"], "slips", "[]", 0.5))
    print(f"trace-only (no pull)   : {grade(trace, grader_ans):.4f}  (capped: no cascade reasoning)")

    # 3) oracle -> ~1.0
    oracle = sub_from(lambda s, i: (s["pairing_json"], s["n_true_locks"],
                                    s["pull_outcome"], s["pull_taut_json"], 1.0))
    print(f"tracing oracle         : {grade(oracle, grader_ans):.4f}  (want ~1.0)")

    # 4) strong but limited solver
    rng = np.random.default_rng(7)

    def strong(s, i):
        true_pair = json.loads(s["pairing_json"])
        pred_pair = {}
        for k, v in true_pair.items():
            if v == "unknown":
                pred_pair[k] = "unknown"
            else:
                pred_pair[k] = v if rng.random() < 0.80 else "unknown"
        nl = s["n_true_locks"]
        nl_pred = nl if rng.random() < 0.6 else max(0, nl + rng.choice([-1, 1]))
        true_po = s["pull_outcome"]
        if true_po == "unknown":
            po = "unknown" if rng.random() < 0.6 else rng.choice(["locks", "slips"])
        else:
            po = true_po if rng.random() < 0.64 else (
                "locks" if true_po == "slips" else "slips")
        true_taut = json.loads(s["pull_taut_json"])
        if len(true_taut) == 0:
            pt = "[]"
        else:
            # tracing+ordering a multi-step cascade through a tangle is hard: a
            # strong solver typically gets only a short leading prefix right and
            # often tacks on a spurious cable (precision hit).
            keep = max(1, int(len(true_taut) * (0.25 + 0.25 * rng.random())))
            guess = true_taut[:keep]
            if rng.random() < 0.35:
                guess = guess + [f"T{int(rng.integers(0, s['n']))}"]
            pt = json.dumps(guess)
        return json.dumps(pred_pair), nl_pred, po, pt, 0.6

    strong_scores = [grade(sub_from(strong), grader_ans) for _ in range(3)]
    print(f"strong limited solver  : {np.mean(strong_scores):.4f}  (want < 0.7, room to improve)")

    print("\n-- sanity --")
    print(f"  any NaN in answers? {ans.isna().any().any()}")


if __name__ == "__main__":
    main()
