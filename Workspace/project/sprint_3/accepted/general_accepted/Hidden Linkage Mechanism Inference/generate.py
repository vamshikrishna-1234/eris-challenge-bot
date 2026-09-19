"""
generate.py - author-side raw-data builder for
              "Hidden Linkage Mechanism Inference"  (codename COGCHAIN)

NOT run on the platform. Runs on the author's machine to synthesise the raw
corpus that prepare.py later splits. Everything is self-simulated and
self-rendered with a tiny dependency-free software 3D projector (NumPy + Pillow
+ imageio for H.264 muxing), so the output is original work shippable as CC0 1.0.
No external 3D assets, no Blender, no OpenGL.

WHAT EACH CLIP IS
-----------------
A fixed steep-oblique camera looks at a flat board carrying K colour-coded
rotors (short discs, each with a painted radial tick so its rotation is visible)
plus one or two raised opaque cross-bars. There are NO visible belts, gears, or
contacts between rotors -- the couplings are internal and hidden. At the start,
one or two "source" rotors begin turning on their own schedule. Through a hidden
directed coupling, each driven rotor's angular velocity equals its parent's,
scaled by a fixed ratio and sign and delayed by a lag, so a child's motion
tracks its parent's. Some rotors are decoys: independently driven on their own
schedule, driving nothing. Sources can stop partway, which stops their whole
subtree.

The solver must invert the mechanism from MOTION ALONE: recover the directed
drive graph (which rotor drives which), which rotors are still turning in the
final frame, and which rotor moved first. Onset order alone is a trap -- decoys
start interleaved with real children, so only velocity tracking (scaled, lagged)
separates true couplings from coincidences.

GROUND TRUTH IS EXACT (sampled, not measured off pixels)
--------------------------------------------------------
Every clip is built from a sampled coupling forest and source profiles, so the
labels are exact: the directed edge set, the per-rotor final-motion flags, and
the first mover.

Each base scenario is rendered as up to 3 deterministic variants:
    base, relight (different board lighting/style), mirror (horizontally
    flipped). Rotor identity is colour-coded (mirror-safe), so labels are
    unchanged across variants and a solver must read motion in the observed
    frame.

OUTPUT (into --out, default raw_data/)
    raw_data/videos/<scene_hash>.mp4
    raw_data/scenes.csv   one row per rendered clip (public inputs + answer
                          fields + private grouping fields)

REQUIREMENTS: pip install numpy pillow imageio imageio-ffmpeg
Determinism: each base scenario is seeded from (--seed, base index).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

# --------------------------------------------------------------------------
# constants (all private to data generation)
# --------------------------------------------------------------------------
W_DEFAULT, H_DEFAULT = 640, 384
N_FRAMES = 96
FPS = 12

# rotor identity vocabulary: colour-coded, mirror-safe.
ROTOR_IDS = ["red", "green", "blue", "amber", "violet", "cyan", "orange",
             "pink", "lime", "brown"]
ROTOR_COLOR = {
    "red": (208, 80, 76), "green": (86, 178, 104), "blue": (74, 126, 214),
    "amber": (226, 176, 70), "violet": (164, 108, 202), "cyan": (88, 188, 188),
    "orange": (224, 134, 70), "pink": (220, 120, 170), "lime": (150, 200, 70),
    "brown": (150, 110, 80),
}

TOPOLOGY_FAMILIES = ["chain", "tree", "star", "multi_root"]

BOARD_STYLES = {
    "slate_bright": {"bg": (226, 230, 238), "board": (150, 156, 170),
                     "light": (0.32, -0.5, 0.80), "ambient": 0.52},
    "warm_bright":  {"bg": (236, 230, 220), "board": (170, 160, 146),
                     "light": (-0.34, -0.48, 0.81), "ambient": 0.54},
    "slate_dim":    {"bg": (198, 204, 214), "board": (128, 134, 148),
                     "light": (0.22, -0.55, 0.80), "ambient": 0.40},
    "warm_dim":     {"bg": (210, 202, 192), "board": (146, 138, 126),
                     "light": (-0.26, -0.54, 0.80), "ambient": 0.42},
}
STYLE_LIST = list(BOARD_STYLES.keys())

BOARD_X, BOARD_Y = 1.28, 1.04
ROTOR_R = 0.135
ROTOR_H = 0.085
MIN_SEP = 0.40

# fixed steep-oblique camera (rotation of the top tick stays clearly visible)
CAM_EYE = np.array([0.0, -1.35, 2.45])
CAM_TARGET = np.array([0.0, 0.05, 0.0])
CAM_UP = np.array([0.0, 1.0, 0.0])
CAM_FOV = np.deg2rad(46.0)


# --------------------------------------------------------------------------
# rng / ids
# --------------------------------------------------------------------------
def _rng(seed: int, idx: int) -> np.random.Generator:
    digest = hashlib.sha256(f"cogchain:{seed}:{idx}".encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _scene_hash(seed: int, base_idx: int, variant: str) -> str:
    return hashlib.sha256(f"cogchain-clip:{seed}:{base_idx}:{variant}".encode()).hexdigest()[:16]


# --------------------------------------------------------------------------
# camera / projection
# --------------------------------------------------------------------------
def _look_at(eye, target, up):
    f = target - eye
    f = f / np.linalg.norm(f)
    s = np.cross(f, up); s = s / np.linalg.norm(s)
    u = np.cross(s, f)
    V = np.eye(4)
    V[0, :3] = s; V[1, :3] = u; V[2, :3] = -f
    V[0, 3] = -s.dot(eye); V[1, 3] = -u.dot(eye); V[2, 3] = f.dot(eye)
    return V


def _perspective(fovy, aspect, near, far):
    t = 1.0 / np.tan(fovy / 2.0)
    P = np.zeros((4, 4))
    P[0, 0] = t / aspect; P[1, 1] = t
    P[2, 2] = (far + near) / (near - far)
    P[2, 3] = 2 * far * near / (near - far)
    P[3, 2] = -1.0
    return P


class Cam:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.V = _look_at(CAM_EYE, CAM_TARGET, CAM_UP)
        self.P = _perspective(CAM_FOV, w / h, 0.05, 8.0)

    def view_z(self, p):
        return float((self.V @ np.array([p[0], p[1], p[2], 1.0]))[2])

    def project(self, p):
        clip = self.P @ self.V @ np.array([p[0], p[1], p[2], 1.0])
        if clip[3] <= 1e-6:
            return None
        ndc = clip[:3] / clip[3]
        x = (ndc[0] * 0.5 + 0.5) * self.w
        y = (1.0 - (ndc[1] * 0.5 + 0.5)) * self.h
        return (x, y)


def _shade(color, normal, light, ambient):
    d = max(0.0, float(np.dot(np.asarray(normal, float), np.asarray(light, float))))
    f = ambient + (1.0 - ambient) * d
    return tuple(int(np.clip(c * f, 0, 255)) for c in color)


def _box_faces(cam, cx, cy, cz, hx, hy, hz, color, light, ambient, faces, outline=(40, 40, 46)):
    c = [(cx - hx, cy - hy, cz - hz), (cx + hx, cy - hy, cz - hz),
         (cx + hx, cy + hy, cz - hz), (cx - hx, cy + hy, cz - hz),
         (cx - hx, cy - hy, cz + hz), (cx + hx, cy - hy, cz + hz),
         (cx + hx, cy + hy, cz + hz), (cx - hx, cy + hy, cz + hz)]
    defs = [([0, 1, 2, 3], (0, 0, -1)), ([4, 5, 6, 7], (0, 0, 1)),
            ([0, 1, 5, 4], (0, -1, 0)), ([1, 2, 6, 5], (1, 0, 0)),
            ([2, 3, 7, 6], (0, 1, 0)), ([3, 0, 4, 7], (-1, 0, 0))]
    for idxs, nrm in defs:
        quad = [c[j] for j in idxs]
        proj = [cam.project(p) for p in quad]
        if any(q is None for q in proj):
            continue
        vz = float(np.mean([cam.view_z(p) for p in quad]))
        faces.append((vz, proj, _shade(color, nrm, light, ambient), outline))


def _prism_faces(cam, cx, cy, z0, z1, radius, sides, color, light, ambient, faces,
                 outline=(30, 30, 34), top_color=None):
    ang = np.linspace(0, 2 * np.pi, sides, endpoint=False) + np.pi / sides
    ring = [(cx + radius * np.cos(a), cy + radius * np.sin(a)) for a in ang]
    for i in range(sides):
        j = (i + 1) % sides
        quad = [(ring[i][0], ring[i][1], z0), (ring[j][0], ring[j][1], z0),
                (ring[j][0], ring[j][1], z1), (ring[i][0], ring[i][1], z1)]
        proj = [cam.project(p) for p in quad]
        if any(q is None for q in proj):
            continue
        mx = (ring[i][0] + ring[j][0]) / 2 - cx
        my = (ring[i][1] + ring[j][1]) / 2 - cy
        vz = float(np.mean([cam.view_z(p) for p in quad]))
        faces.append((vz, proj, _shade(color, (mx, my, 0.0), light, ambient), outline))
    top = [(x, y, z1) for (x, y) in ring]
    proj = [cam.project(p) for p in top]
    if all(q is not None for q in proj):
        vz = float(np.mean([cam.view_z(p) for p in top]))
        tc = top_color if top_color is not None else color
        faces.append((vz, proj, _shade(tc, (0, 0, 1), light, ambient), outline))


# --------------------------------------------------------------------------
# scenario sampling: rotors, positions, hidden coupling forest, source profiles
# --------------------------------------------------------------------------
def _sample_positions(rng, n):
    pts = []
    tries = 0
    while len(pts) < n and tries < 600:
        tries += 1
        x = float(rng.uniform(-BOARD_X + 0.28, BOARD_X - 0.28))
        y = float(rng.uniform(-BOARD_Y + 0.24, BOARD_Y - 0.24))
        if all((x - px) ** 2 + (y - py) ** 2 >= MIN_SEP ** 2 for px, py in pts):
            pts.append((x, y))
    return pts


def _source_profile(rng):
    """A source's angular velocity is a DISTINCTIVE smoothly time-varying signature
    (base speed modulated by a per-source sinusoid), not a flat constant. A driven
    rotor reproduces this exact signature scaled and lagged, so the correct driver
    is identifiable by signature correlation -- a decoy with a different signature
    will not match. Speed modulates but keeps a constant sign (never reverses)."""
    onset = int(rng.integers(2, 18))
    # narrower, more similar signatures: independent sources (incl. decoys) look
    # much alike, so the true driver of a child can no longer be picked out by a
    # coarse "which spin looks roughly like this" match -- only precise, lagged
    # velocity tracking (which the exhaustive oracle does) separates them.
    base = float(rng.choice([0.20, 0.23, 0.26])) * (1 if rng.random() < 0.5 else -1)
    amp = float(rng.uniform(0.34, 0.52))
    period = float(rng.uniform(20.0, 34.0))
    phase = float(rng.uniform(0.0, 2 * np.pi))
    stops = rng.random() < 0.45
    stop_at = int(rng.integers(N_FRAMES // 2, N_FRAMES - 8)) if stops else N_FRAMES + 1
    return {"onset": onset, "base": base, "amp": amp, "period": period,
            "phase": phase, "stop_at": stop_at}


def _source_omega(prof):
    w = np.zeros(N_FRAMES)
    for t in range(N_FRAMES):
        if prof["onset"] <= t < prof["stop_at"]:
            w[t] = prof["base"] * (1.0 + prof["amp"] * np.sin(2 * np.pi * t / prof["period"]
                                                              + prof["phase"]))
    return w


def _sample_topology(rng, family):
    """Return (K, parent_of, edge_list, source_set) using rotor INDICES 0..K-1.
    parent_of[i] = index of parent, or -1 if i is a root/source."""
    # Total rotor count and the size of the COUPLED sub-structure are drawn
    # almost independently: the coupled component has `m` rotors (capped only so
    # at least two decoys remain), and the rest are independent decoys. This
    # keeps the edge count from tracking num_rotors -- a big board can still have
    # only a couple of real couplings, and a small board can be mostly coupled,
    # so num_rotors carries no shortcut about how many edges there are.
    K = int(rng.integers(6, 9))                 # 6-8 rotors total
    m = min(K - 2, int(rng.integers(3, 7)))     # coupled rotors (>=3, >=2 decoys)
    active = list(range(m))
    parent_of = {}
    if family == "chain":
        parent_of[active[0]] = -1
        for a, b in zip(active, active[1:]):
            parent_of[b] = a
    elif family == "star":
        parent_of[active[0]] = -1
        for lf in active[1:]:
            parent_of[lf] = active[0]
    elif family == "tree":
        parent_of[active[0]] = -1
        for nd in active[1:]:
            par = int(rng.choice(active[:active.index(nd)]))
            parent_of[nd] = par
    else:  # multi_root: split the coupled rotors into 2-3 independent chains
        n_roots = 2 if m <= 4 else int(rng.integers(2, 4))
        chains = [[] for _ in range(n_roots)]
        for i, nd in enumerate(active):
            chains[i % n_roots].append(nd)
        for ch in chains:
            parent_of[ch[0]] = -1
            for a, b in zip(ch, ch[1:]):
                parent_of[b] = a
    for d in range(m, K):                       # remaining rotors are decoys
        parent_of[d] = -1
    edges = [(p, c) for c, p in parent_of.items() if p >= 0]
    sources = [i for i in range(K) if parent_of.get(i, -1) < 0]
    return K, parent_of, edges, sources


def _topo_order(parent_of, K):
    order = []
    seen = set()

    def visit(i):
        if i in seen:
            return
        p = parent_of.get(i, -1)
        if p >= 0:
            visit(p)
        seen.add(i)
        order.append(i)

    for i in range(K):
        visit(i)
    return order


def _sample_scene(rng, base_idx):
    family = TOPOLOGY_FAMILIES[base_idx % len(TOPOLOGY_FAMILIES)]
    K, parent_of, edges, sources = _sample_topology(rng, family)

    ids = [str(x) for x in rng.choice(ROTOR_IDS, size=K, replace=False)]
    positions = _sample_positions(rng, K)
    K = min(K, len(positions))

    # per-edge coupling params
    ratio = {}
    sign = {}
    lag = {}
    for (p, c) in edges:
        ratio[c] = float(rng.choice([0.5, 0.75, 1.0, 1.0, 1.5, 2.0]))
        sign[c] = 1 if rng.random() < 0.5 else -1
        lag[c] = int(rng.integers(2, 16))

    # source profiles
    src_prof = {s: _source_profile(rng) for s in sources}

    # per-rotor independent "shaft wobble": a small smooth idiosyncratic velocity
    # signal unique to each rotor. A driven rotor transmits its DIRECT parent's
    # actual (wobble-carrying) rotation, so it inherits the parent's wobble -- this
    # uniquely fingerprints the true immediate driver and removes the star-vs-chain
    # / sibling ambiguity that pure shared signatures would otherwise create.
    wob = []
    for _ in range(K):
        wob.append((float(rng.uniform(0.018, 0.030)),
                    float(rng.uniform(5.0, 11.0)), float(rng.uniform(0, 2 * np.pi))))

    def _add_wobble(arr, i):
        a, per, ph = wob[i]
        mask = np.abs(arr) > 1e-9
        t = np.arange(N_FRAMES)
        arr[mask] += (a * np.sin(2 * np.pi * t / per + ph))[mask]

    # simulate angular velocity per rotor over time (topological order)
    omega = np.zeros((K, N_FRAMES))
    for s in sources:
        omega[s] = _source_omega(src_prof[s])
        _add_wobble(omega[s], s)
    for i in _topo_order(parent_of, K):
        p = parent_of.get(i, -1)
        if p < 0:
            continue
        L, g, sg = lag[i], ratio[i], sign[i]
        for t in range(N_FRAMES):
            omega[i, t] = sg * g * omega[p, t - L] if t - L >= 0 else 0.0
        _add_wobble(omega[i], i)

    # integrate angle with random start phase
    phase0 = rng.uniform(0, 2 * np.pi, size=K)
    theta = np.zeros((K, N_FRAMES))
    for i in range(K):
        th = phase0[i]
        for t in range(N_FRAMES):
            th += omega[i, t]
            theta[i, t] = th

    # No physical couplings are ever rendered: the drive linkage is internal and
    # invisible, so the directed graph can only be inferred from correlated motion
    # (a child's angular velocity tracks its parent's, scaled and lagged). There
    # is therefore nothing for frame-differencing or contact-detection to exploit.
    bars = []

    moving_end = [ids[i] for i in range(K) if abs(omega[i, N_FRAMES - 1]) > 1e-6]
    onsets = []
    for i in range(K):
        nz = np.nonzero(np.abs(omega[i]) > 1e-6)[0]
        onsets.append(int(nz[0]) if len(nz) else 10 ** 9)
    first_mover = ids[int(np.argmin(onsets))]
    edge_ids = [[ids[p], ids[c]] for (p, c) in edges]

    return {
        "base_idx": base_idx, "family": family, "K": K, "ids": ids,
        "positions": positions, "theta": theta, "bars": bars,
        "edges_ids": edge_ids, "moving_end": moving_end, "first_mover": first_mover,
        "style_key": STYLE_LIST[int(rng.integers(0, len(STYLE_LIST)))],
    }


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def _render_base(cam, scene, style, light, ambient, mx, w, h):
    """Render the static scene (board, rotor bodies, occluder bars) once. Only
    the rotating tick marks change per frame, so they are overlaid later."""
    img = Image.new("RGB", (w, h), tuple(style["bg"]))
    draw = ImageDraw.Draw(img)

    # ground plane drawn first: every rotor sits on z>=0, so the board is always
    # behind. (A single large board face can otherwise sort in front of a far
    # rotor under naive painter ordering.)
    board = []
    _box_faces(cam, 0.0, 0.0, -0.05, BOARD_X, BOARD_Y, 0.05,
               style["board"], light, ambient, board, outline=(70, 72, 80))
    board.sort(key=lambda f: f[0])
    for _, pts, fill, outline in board:
        draw.polygon(pts, fill=fill, outline=outline)

    objs = []
    for i in range(scene["K"]):
        x, y = scene["positions"][i][0] * mx, scene["positions"][i][1]
        col = ROTOR_COLOR[scene["ids"][i]]
        _prism_faces(cam, x, y, 0.0, ROTOR_H, ROTOR_R, 10, col, light, ambient, objs,
                     top_color=tuple(int(np.clip(c * 1.12, 0, 255)) for c in col))
    objs.sort(key=lambda f: f[0])
    for _, pts, fill, outline in objs:
        draw.polygon(pts, fill=fill, outline=outline)
    return img


def _render_clip(scene, style_key, mirror, w, h):
    cam = Cam(w, h)
    style = BOARD_STYLES[style_key]
    light = np.asarray(style["light"], float); light = light / np.linalg.norm(light)
    ambient = style["ambient"]
    mx = -1.0 if mirror else 1.0

    base = _render_base(cam, scene, style, light, ambient, mx, w, h)
    centers = [cam.project((scene["positions"][i][0] * mx, scene["positions"][i][1],
                            ROTOR_H + 0.002)) for i in range(scene["K"])]

    frames = []
    for fr in range(N_FRAMES):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        for i in range(scene["K"]):
            cxp = centers[i]
            if cxp is None:
                continue
            x, y = scene["positions"][i][0] * mx, scene["positions"][i][1]
            th = scene["theta"][i][fr] * (-1 if mx < 0 else 1)
            exp = cam.project((x + ROTOR_R * 0.9 * np.cos(th),
                               y + ROTOR_R * 0.9 * np.sin(th), ROTOR_H + 0.002))
            if exp is not None:
                draw.line([cxp, exp], fill=(26, 26, 30), width=4)
        frames.append(np.asarray(img, dtype=np.uint8))
    return frames


# --------------------------------------------------------------------------
# variants + main
# --------------------------------------------------------------------------
def _variant_rows(scene, seed, want_variants):
    rows = []
    base_id = f"m{scene['base_idx']:05d}"
    variants = ["base"]
    if want_variants:
        variants += ["relight", "mirror"]
    for variant in variants:
        mirror = (variant == "mirror")
        style_key = scene["style_key"]
        if variant == "relight":
            others = [s for s in STYLE_LIST if s != scene["style_key"]]
            style_key = others[scene["base_idx"] % len(others)]
        sh = _scene_hash(seed, scene["base_idx"], variant)
        rows.append({
            "scene_hash": sh, "base_scenario_id": base_id, "variant": variant,
            "num_rotors": scene["K"], "rotors": json.dumps(scene["ids"]),
            "topology_family": scene["family"], "board_style": style_key,
            "edges_json": json.dumps(scene["edges_ids"]),
            "moving_at_end_json": json.dumps(sorted(scene["moving_end"])),
            "first_mover": scene["first_mover"],
            "_scene": scene, "_mirror": mirror, "_style_key": style_key,
        })
    return rows


def _encode_mp4(path, frames, fps):
    import imageio.v2 as imageio
    with imageio.get_writer(path, fps=fps, codec="libx264", quality=7,
                            macro_block_size=1, ffmpeg_log_level="error",
                            output_params=["-preset", "ultrafast", "-pix_fmt", "yuv420p"]) as wri:
        for f in frames:
            wri.append_data(f)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    ap.add_argument("--n-base", type=int, default=100)
    ap.add_argument("--seed", type=int, default=31)
    ap.add_argument("--w", type=int, default=W_DEFAULT)
    ap.add_argument("--h", type=int, default=H_DEFAULT)
    ap.add_argument("--no-variants", action="store_true")
    args = ap.parse_args()

    import pandas as pd

    vid_dir = args.out / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)

    meta_rows = []
    n_clips = 0
    for base_idx in range(args.n_base):
        rng = _rng(args.seed, base_idx)
        scene = _sample_scene(rng, base_idx)
        for row in _variant_rows(scene, args.seed, not args.no_variants):
            frames = _render_clip(row["_scene"], row["_style_key"], row["_mirror"],
                                  args.w, args.h)
            _encode_mp4(str(vid_dir / f"{row['scene_hash']}.mp4"), frames, FPS)
            clean = {k: v for k, v in row.items() if not k.startswith("_")}
            clean["video"] = f"videos/{row['scene_hash']}.mp4"
            meta_rows.append(clean)
            n_clips += 1
        if (base_idx + 1) % 10 == 0:
            print(f"  [{base_idx+1}/{args.n_base}] base scenarios rendered ({n_clips} clips)")

    cols = ["scene_hash", "video", "base_scenario_id", "variant", "num_rotors",
            "rotors", "topology_family", "board_style", "edges_json",
            "moving_at_end_json", "first_mover"]
    pd.DataFrame(meta_rows)[cols].to_csv(args.out / "scenes.csv", index=False)
    print(f"OK: wrote {n_clips} clips to {args.out}")


if __name__ == "__main__":
    main()
