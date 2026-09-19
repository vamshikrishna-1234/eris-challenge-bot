"""Leakage / oracle analysis for PANEL - no rendering required.

Reconstructs each scene deterministically via generate._sample_scene (no rendering)
and checks:
  * the true wiring oracle scores ~1.0,
  * the "single-switch correlation" shortcut (each lamp = the best single switch,
    BUF/NOT) scores low - it cannot represent AND/OR/XOR/multi-input lamps,
  * lamp on-rate is balanced ~0.5 and switch/lamp counts do not leak the label.
Run:  python _analyze.py --seed 59 --n 800
"""

from __future__ import annotations

import argparse
import json
from itertools import product

import numpy as np
import pandas as pd

import generate as gen
from grade import grade


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=59)
    ap.add_argument("--n", type=int, default=800)
    args = ap.parse_args()

    ans_rows, true_rows, short_rows = [], [], []
    on_rates, S_list, L_list = [], [], []

    for idx in range(args.n):
        rng = gen._scene_rng(args.seed, idx)
        sc = gen._sample_scene(rng)
        S, L = sc["S"], sc["L"]
        wiring = sc["wiring"]
        configs = gen._configs_over_time(sc)

        ans_rows.append({
            "id": idx, "wiring_json": json.dumps(wiring),
            "query_pattern": json.dumps(sc["query_pattern"]), "n_lamps": L,
            "split_group": f"{sc['circuit_family']}_{sc['variant']}",
            "ood_axis": sc["ood_axis"], "render_style": sc["render_style"],
        })
        true_rows.append({"id": idx, "wiring_json": json.dumps(wiring),
                          "query_pattern": json.dumps(sc["query_pattern"]), "confidence": 1.0})

        # single-switch shortcut: per lamp pick best-correlated switch (BUF or NOT)
        lamp_obs = {j: [gen._lamp_value(wiring[str(j)], c) for c in configs] for j in range(L)}
        sw_obs = {i: [c[i] for c in configs] for i in range(S)}
        short_wire = {}
        for j in range(L):
            best_i, best_gate, best_agree = 0, "BUF", -1.0
            for i in range(S):
                a_buf = np.mean([int(sw_obs[i][t] == lamp_obs[j][t]) for t in range(len(configs))])
                a_not = 1 - a_buf
                if a_buf >= best_agree:
                    best_i, best_gate, best_agree = i, "BUF", a_buf
                if a_not > best_agree:
                    best_i, best_gate, best_agree = i, "NOT", a_not
            short_wire[str(j)] = {"gate": best_gate, "inputs": [best_i]}
        short_q = [gen._lamp_value(short_wire[str(j)], sc["query_config"]) for j in range(L)]
        short_rows.append({"id": idx, "wiring_json": json.dumps(short_wire),
                           "query_pattern": json.dumps(short_q), "confidence": 0.5})

        on_rates.extend([np.mean(lamp_obs[j]) for j in range(L)])
        S_list.append(S); L_list.append(L)

    ans = pd.DataFrame(ans_rows)
    s_true = grade(pd.DataFrame(true_rows), ans)
    s_short = grade(pd.DataFrame(short_rows), ans)

    print("=== ORACLE / SHORTCUT ===")
    print(f"true-wiring oracle        = {s_true:.4f}  (expect ~1.0)")
    print(f"single-switch shortcut    = {s_short:.4f}  (expect low; can't do AND/OR/XOR/multi)")

    print("\n=== BALANCE / FEATURE-LABEL LEAKAGE ===")
    print(f"mean lamp on-rate (demonstrated) = {np.mean(on_rates):.3f}  (expect ~0.5)")
    print(f"n_switches range = {min(S_list)}-{max(S_list)}, n_lamps range = {min(L_list)}-{max(L_list)}")
    print("ood balance:\n" + pd.Series([r['ood_axis'] for r in ans_rows]).value_counts().to_string())


if __name__ == "__main__":
    main()
