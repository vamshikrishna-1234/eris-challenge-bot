"""Leakage + difficulty analysis (no video decode; uses the exact sim). Confirms:
  - data is balanced and num_probes does NOT leak n_obstacles / the map,
  - a SINGLE-FRAME view cannot reconstruct the map (no trajectory),
  - a naive "obstacles = where the flashes are" baseline scores poorly (flashes
    are sparse near-side contact points, not extents),
  - a CROSS-FRAME inverse oracle (free-space carving + contact circle-fit) over
    the observable trajectories reconstructs the map well BUT is capped below 1.0
    because regions no probe visits are under-determined -> solvable, with a
    ceiling that widens the human/agent gap.
"""
import numpy as np
import generate as gen

N = 200
G = gen.GRID


def cell_of(x, y):
    """visited cell as (col, ry), ry from bottom = floor(y)."""
    col = min(G - 1, max(0, int(np.floor(x))))
    ry = min(G - 1, max(0, int(np.floor(y))))
    return col, ry


def occ_str_from_set(occ_set):
    """occ_set holds (col, ry); emit row-major string with row 0 = top."""
    out = []
    for row in range(G):
        ry = G - 1 - row
        for col in range(G):
            out.append("1" if (col, ry) in occ_set else "0")
    return "".join(out)


def macro_f1(pred_str, true_str):
    """Occupied-class F1 (Dice), matching grade.py's _occ_f1."""
    pred = np.array([c == "1" for c in pred_str]); true = np.array([c == "1" for c in true_str])
    tp = int(np.sum(pred & true)); fp = int(np.sum(pred & ~true)); fn = int(np.sum(~pred & true))
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    if tp == 0:
        return 0.0
    prec = tp / (tp + fp); rec = tp / (tp + fn)
    return float(2 * prec * rec / (prec + rec))


def _components(cells):
    """count 4-connected components of a set of (col, ry) cells."""
    cells = set(cells); seen = set(); n = 0
    for s in cells:
        if s in seen:
            continue
        n += 1; stack = [s]
        while stack:
            c, r = stack.pop()
            if (c, r) in seen or (c, r) not in cells:
                continue
            seen.add((c, r))
            stack += [(c + 1, r), (c - 1, r), (c, r + 1), (c, r - 1)]
    return n


def _candidates(contact):
    """given a contact (frame, x, y, axis), the two cells sharing the hit face."""
    _, x, y, ax = contact
    if ax == "v":
        k = int(round(x)); ry = int(np.floor(y))
        return [(k - 1, ry), (k, ry)]
    k = int(round(y)); c = int(np.floor(x))
    return [(c, k - 1), (c, k)]


def oracle(sim, single_frame=False, flash_only=False):
    """Cross-frame inverse oracle: carve free cells from visited path, then for
    each bounce mark the solid cell on the far side of the hit face."""
    probes = sim["probes"]
    visited = set()
    contacts = []
    for pr in probes:
        if single_frame:
            mid = pr["pos"][len(pr["pos"]) // 2: len(pr["pos"]) // 2 + 1]
            for (_, x, y) in mid:
                visited.add(cell_of(x, y))
            continue
        for (_, x, y) in pr["pos"]:
            visited.add(cell_of(x, y))
        contacts.extend(pr["contacts"])

    if single_frame:
        return occ_str_from_set(set()), 0, None

    if flash_only:
        # naive: mark the cell containing each flash point (no face reasoning)
        occ = set()
        for (_, x, y, _ax) in contacts:
            occ.add((min(G - 1, int(x)), min(G - 1, int(y))))
        occ -= visited
        return occ_str_from_set(occ), _components(occ), None

    occ = set()
    for ct in contacts:
        for cell in _candidates(ct):
            c, r = cell
            if 0 <= c < G and 0 <= r < G and cell not in visited:
                occ.add(cell)
    return occ_str_from_set(occ), _components(occ), occ


def main():
    def s_query(pred, true):
        if true == -1 and pred == -1:
            return 1.0
        if (true == -1) != (pred == -1):
            return 0.0
        return float(np.exp(-abs(pred - true) / 1.5))

    n_obs, num_probes, fam_count = [], [], {}
    map_oracle, map_flash, map_empty, map_single = [], [], [], []
    count_err_oracle = []
    q_oracle, q_base = [], []
    n_blocked = 0
    empty_str = "0" * (G * G)
    for b in range(N):
        scene = gen._sample_scene(gen._rng(41, b), b)
        sim = gen._simulate_scene(scene)
        true = sim["occupancy"]
        n_obs.append(sim["n_obstacles"]); num_probes.append(scene["num_probes"])
        fam_count[scene["family"]] = fam_count.get(scene["family"], 0) + 1

        o_str, o_n, o_occ = oracle(sim)
        f_str, _, _ = oracle(sim, flash_only=True)
        s_str, _, _ = oracle(sim, single_frame=True)
        map_oracle.append(macro_f1(o_str, true))
        map_flash.append(macro_f1(f_str, true))
        map_single.append(macro_f1(s_str, true))
        map_empty.append(macro_f1(empty_str, true))
        count_err_oracle.append(min(1.0, abs(o_n - sim["n_obstacles"]) / 4.0))
        true_hit = sim["query_hit_row"]
        n_blocked += int(true_hit != -1)
        q_oracle.append(s_query(gen._query_hit_row(o_occ, scene["query_col"]), true_hit))
        q_base.append(s_query(-1, true_hit))

    n_obs = np.array(n_obs, float); num_probes = np.array(num_probes, float)
    print(f"base scenarios analysed : {N}")
    print(f"family counts           : {fam_count}")
    print(f"n_obstacles mean={n_obs.mean():.2f} range=[{int(n_obs.min())},{int(n_obs.max())}]")
    print(f"num_probes  mean={num_probes.mean():.2f} range=[{int(num_probes.min())},{int(num_probes.max())}]")
    print(f"corr(num_probes, n_obstacles) = {np.corrcoef(num_probes, n_obs)[0,1]:+.3f}  (want ~0)")
    print("--- occupancy occupied-class F1 / Dice (per clip) ---")
    print(f"all-empty baseline      : {np.mean(map_empty):.3f}")
    print(f"flash-only baseline     : {np.mean(map_flash):.3f}  (flashes are sparse contacts)")
    print(f"single-frame oracle     : {np.mean(map_single):.3f}  (no trajectory -> poor)")
    print(f"cross-frame oracle      : {np.mean(map_oracle):.3f}  (solvable; <1.0 = under-determined)")
    print("--- other heads ---")
    print(f"count score (1-|dn|/4)   oracle mean : {1 - np.mean(count_err_oracle):.3f}")
    print(f"query-hit blocked share  : {n_blocked/N:.2f}  (rest pass straight through)")
    print(f"query-hit score  always-(-1) base    : {np.mean(q_base):.3f}")
    print(f"query-hit score  cross-frame oracle  : {np.mean(q_oracle):.3f}")


if __name__ == "__main__":
    main()
