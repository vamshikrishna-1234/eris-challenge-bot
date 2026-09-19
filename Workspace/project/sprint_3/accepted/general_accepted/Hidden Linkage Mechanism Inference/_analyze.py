"""Leakage + difficulty analysis (no rendering). Confirms:
  - no metadata shortcut (num_rotors weakly related to answers),
  - the 'onset-order' heuristic is a TRAP (low edge-F1),
  - a velocity-tracking oracle recovers the graph (edge-F1 ~ 1) -> solvable.
"""
import numpy as np
import generate as gen

N = 240
RATIOS = [0.5, 0.75, 1.0, 1.5, 2.0]
LAGS = range(1, 17)


def edge_f1(pred, true):
    if not pred and not true:
        return 1.0
    if not pred or not true:
        return 0.0
    inter = len(pred & true)
    p = inter / len(pred); r = inter / len(true)
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)


def onsets_of(omega):
    out = []
    for i in range(omega.shape[0]):
        nz = np.nonzero(np.abs(omega[i]) > 1e-6)[0]
        out.append(int(nz[0]) if len(nz) else 10 ** 9)
    return out


def onset_pred(ids, omega):
    ons = onsets_of(omega)
    edges = set()
    order = sorted(range(len(ids)), key=lambda i: ons[i])
    for i in range(len(ids)):
        if ons[i] >= 10 ** 9:
            continue
        earlier = [j for j in range(len(ids)) if ons[j] < ons[i]]
        if earlier:
            par = max(earlier, key=lambda j: ons[j])  # most recent earlier mover
            edges.add((ids[par], ids[i]))
    return edges


TAU = 0.12  # normalised-residual gate: a driver explains most of the child's motion


def velocity_pred(ids, omega):
    K, T = omega.shape
    ons = onsets_of(omega)
    edges = set()
    for c in range(K):
        if ons[c] >= 10 ** 9:
            continue
        var_c = np.mean((omega[c] - np.mean(omega[c])) ** 2) + 1e-12
        best = None  # (err, lag, parent)
        for p in range(K):
            if p == c or ons[p] >= ons[c]:
                continue
            for L in LAGS:
                shifted = np.concatenate([np.zeros(L), omega[p, :T - L]])
                if np.sum(shifted * shifted) < 1e-9:
                    continue
                for g in RATIOS:
                    for s in (1.0, -1.0):
                        err = np.mean((omega[c] - s * g * shifted) ** 2)
                        if best is None or (err, L) < (best[0], best[1]):
                            best = (err, L, p)
        if best is not None and best[0] / var_c < TAU:
            edges.add((ids[best[2]], ids[c]))
    return edges


def main():
    n_edges, n_moving, num_rot, frac_moving = [], [], [], []
    first_decoy = 0
    f1_onset, f1_vel = [], []
    for b in range(N):
        sc = gen._sample_scene(gen._rng(31, b), b)
        ids = sc["ids"]
        theta = sc["theta"]
        omega = np.diff(theta, axis=1, prepend=theta[:, :1])
        true = set((e[0], e[1]) for e in sc["edges_ids"])
        n_edges.append(len(true))
        n_moving.append(len(sc["moving_end"]))
        num_rot.append(sc["K"])
        frac_moving.append(len(sc["moving_end"]) / sc["K"])
        children = set(e[1] for e in sc["edges_ids"])
        if sc["first_mover"] not in children:
            first_decoy += 1
        f1_onset.append(edge_f1(onset_pred(ids, omega), true))
        f1_vel.append(edge_f1(velocity_pred(ids, omega), true))

    num_rot = np.array(num_rot, float)
    print(f"base scenarios analysed : {N}")
    print(f"edges/clip  mean={np.mean(n_edges):.2f}  range=[{min(n_edges)},{max(n_edges)}]")
    print(f"moving/clip mean={np.mean(n_moving):.2f}  frac_moving mean={np.mean(frac_moving):.2f}")
    print(f"first_mover is a non-driver (decoy/leaf-less): {first_decoy}/{N}")
    print(f"corr(num_rotors, #edges)      = {np.corrcoef(num_rot, n_edges)[0,1]:+.3f}")
    print(f"corr(num_rotors, frac_moving) = {np.corrcoef(num_rot, frac_moving)[0,1]:+.3f}")
    print(f"onset-order heuristic edge-F1 = {np.mean(f1_onset):.3f}  (TRAP: should be low)")
    print(f"velocity-tracking oracle  F1  = {np.mean(f1_vel):.3f}  (should be ~1.0)")


if __name__ == "__main__":
    main()
