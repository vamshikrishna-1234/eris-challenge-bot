"""
generate.py - author-side raw-data builder for
              "Collapse Attribution And Counterfactual Fragility"

NOT run on the platform. Runs on the author's machine to synthesise the raw
corpus that prepare.py later splits. Everything is self-simulated and
self-rendered, so the output is original work shippable as CC0 1.0.

Physics  : MuJoCo (Apache-2.0; prebuilt wheels, headless, deterministic).
Rendering: a small dependency-free projector (NumPy + Pillow) that draws the
           axis-aligned boxes at t=0 with a painter's algorithm - no OpenGL,
           so it works on any headless machine.

WHAT IT DOES (per scene)
------------------------
  1. Procedurally builds a leaning tower of N coloured boxes (random-walk
     horizontal offset per level -> near the stability boundary). Procedural
     geometry only; zero external-asset license risk.
  2. Renders the t=0 still and records each block's pixel centroid + colour.
  3. Settles the full stack and records, per block, the centre-of-mass
     displacement. will_collapse = (any block moved > MOVE_EPS); initiator =
     the block that FIRST exceeds MOVE_EPS (-1 if stable).
  4. Counterfactual pass: removes each block in turn, re-settles, and finds the
     block whose removal FLIPS the binary collapse outcome with the largest
     displacement effect (keystone); the second-best such block is keystone_alt
     (-1 if none).

OUTPUT (into --out, default raw_data/)
    raw_data/images/<scene_hash>.png
    raw_data/scenes.csv   scene_hash, n_blocks, will_collapse,
                          initiator_block_id, keystone_block_id,
                          keystone_alt_block_id
    raw_data/blocks.csv   scene_hash, block_id, cx, cy,
                          color_r, color_g, color_b

REQUIREMENTS
    pip install mujoco numpy pillow
Determinism: each scene is seeded from (--seed, scene index); re-running with
the same flags reproduces the corpus exactly.

NOTE: physics parameters (masses, friction, sim horizon, MOVE_EPS) live ONLY
here and in the private answers - they are never surfaced to participants.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np

# ---- physics / scene constants (private to data generation) ----
GRAVITY = -9.81
TIMESTEP = 0.004
SETTLE_STEPS = 500
MOVE_EPS = 0.03
BLOCK_HALF = 0.04
N_MIN, N_MAX = 4, 7
JITTER_STEP = 0.04           # per-level horizontal random-walk amplitude (~50% collapse)
IMG_DEFAULT = 256

PALETTE = [
    (220, 70, 70), (70, 150, 220), (90, 200, 110), (240, 200, 70),
    (180, 110, 220), (240, 150, 70), (90, 210, 210), (210, 210, 210),
]

# ---- fixed camera (shared across all scenes) ----
CAM_EYE = np.array([0.45, -0.55, 0.42])
CAM_TARGET = np.array([0.0, 0.0, 0.16])
CAM_UP = np.array([0.0, 0.0, 1.0])
CAM_FOV = np.deg2rad(45.0)
LIGHT_DIR = np.array([-0.4, -0.6, 0.8])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)

# box corner offsets (sx, sy, sz) and the 6 faces (corner index quads)
_CORNERS = np.array([(sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], dtype=float)
_FACES = [
    (0, 1, 3, 2, (-1, 0, 0)),
    (4, 6, 7, 5, (1, 0, 0)),
    (0, 4, 5, 1, (0, -1, 0)),
    (2, 3, 7, 6, (0, 1, 0)),
    (0, 2, 6, 4, (0, 0, -1)),
    (1, 5, 7, 3, (0, 0, 1)),
]


def _scene_rng(seed: int, idx: int) -> np.random.Generator:
    digest = hashlib.sha256(f"{seed}:{idx}".encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _scene_hash(seed: int, idx: int) -> str:
    return hashlib.sha256(f"collapse:{seed}:{idx}".encode()).hexdigest()[:16]


def _scene_spec(rng, jitter):
    """Return (n, positions[n][3], colors[n]) for a leaning tower."""
    n = int(rng.integers(N_MIN, N_MAX + 1))
    h = BLOCK_HALF
    x = y = 0.0
    positions = []
    for k in range(n):
        x += float(rng.uniform(-jitter, jitter))
        y += float(rng.uniform(-jitter, jitter)) * 0.5
        z = h + 2 * h * k + 0.0005 * k
        positions.append([x, y, z])
    colors = [PALETTE[k % len(PALETTE)] for k in range(n)]
    return n, positions, colors


def _build_xml(positions, drop_idx=None) -> str:
    h = BLOCK_HALF
    bodies = []
    for k, (px, py, pz) in enumerate(positions):
        if drop_idx is not None and k == drop_idx:
            continue
        bodies.append(
            f'<body pos="{px:.5f} {py:.5f} {pz:.5f}">'
            f'<freejoint/>'
            f'<geom type="box" size="{h} {h} {h}" mass="0.2" '
            f'friction="0.7 0.01 0.001" rgba="0.6 0.6 0.6 1"/></body>'
        )
    return (
        f'<mujoco><option timestep="{TIMESTEP}" gravity="0 0 {GRAVITY}"/>'
        f'<worldbody><geom type="plane" size="3 3 0.1" friction="0.8 0.01 0.001"/>'
        f'{"".join(bodies)}</worldbody></mujoco>'
    )


def _simulate(positions, drop_idx=None):
    """Settle the stack; return (per-kept-block displacement list, first-mover
    index into the KEPT ordering or -1)."""
    import mujoco

    m = mujoco.MjModel.from_xml_string(_build_xml(positions, drop_idx))
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)
    # body 0 is the world; blocks are bodies 1..nbody-1 in kept order
    block_bodies = list(range(1, m.nbody))
    start = d.xpos[block_bodies].copy()
    first_mover = -1
    for _ in range(SETTLE_STEPS):
        mujoco.mj_step(m, d)
        if first_mover == -1:
            disp = np.linalg.norm(d.xpos[block_bodies] - start, axis=1)
            over = np.where(disp > MOVE_EPS)[0]
            if over.size:
                first_mover = int(over[0])
    disp = np.linalg.norm(d.xpos[block_bodies] - start, axis=1)
    return disp, first_mover


def _kept_to_orig(idx_in_kept, n, drop_idx):
    """Map an index in the kept ordering back to the original block index."""
    orig = [k for k in range(n) if not (drop_idx is not None and k == drop_idx)]
    return orig[idx_in_kept]


# ---------- rendering ----------

def _look_at(eye, target, up):
    f = target - eye
    f = f / np.linalg.norm(f)
    s = np.cross(f, up)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)
    V = np.eye(4)
    V[0, :3] = s
    V[1, :3] = u
    V[2, :3] = -f
    V[0, 3] = -s.dot(eye)
    V[1, 3] = -u.dot(eye)
    V[2, 3] = f.dot(eye)
    return V


def _perspective(fovy, aspect, near, far):
    t = 1.0 / np.tan(fovy / 2.0)
    P = np.zeros((4, 4))
    P[0, 0] = t / aspect
    P[1, 1] = t
    P[2, 2] = (far + near) / (near - far)
    P[2, 3] = 2 * far * near / (near - far)
    P[3, 2] = -1.0
    return P


def _project(pt, V, P, w, h):
    clip = P @ V @ np.array([pt[0], pt[1], pt[2], 1.0])
    if clip[3] <= 1e-6:
        return None
    ndc = clip[:3] / clip[3]
    x = (ndc[0] * 0.5 + 0.5) * w
    y = (1.0 - (ndc[1] * 0.5 + 0.5)) * h
    return x, y


def _render(positions, colors, img_size):
    from PIL import Image, ImageDraw

    w = h = img_size
    V = _look_at(CAM_EYE, CAM_TARGET, CAM_UP)
    P = _perspective(CAM_FOV, 1.0, 0.05, 5.0)

    img = Image.new("RGB", (w, h), (235, 238, 242))
    draw = ImageDraw.Draw(img)
    # floor quad
    floor = [(-1.2, -1.2, 0), (1.2, -1.2, 0), (1.2, 1.2, 0), (-1.2, 1.2, 0)]
    fp = [_project(p, V, P, w, h) for p in floor]
    if all(q is not None for q in fp):
        draw.polygon(fp, fill=(205, 208, 214))

    hbe = BLOCK_HALF
    face_list = []  # (view_depth, polygon_pixels, rgb)
    centroids = []
    for k, (cx, cy, cz) in enumerate(positions):
        center = np.array([cx, cy, cz])
        cproj = _project(center, V, P, w, h)
        centroids.append(cproj if cproj else (w // 2, h // 2))
        corners = center + _CORNERS * hbe
        for (a, b, c, dd, normal) in _FACES:
            quad = [corners[a], corners[b], corners[c], corners[dd]]
            proj = [_project(p, V, P, w, h) for p in quad]
            if any(q is None for q in proj):
                continue
            fcenter = np.mean(quad, axis=0)
            view_z = (V @ np.array([fcenter[0], fcenter[1], fcenter[2], 1.0]))[2]
            shade = 0.35 + 0.65 * max(0.0, np.dot(np.array(normal, dtype=float), LIGHT_DIR))
            base = colors[k]
            rgb = tuple(int(np.clip(c0 * shade, 0, 255)) for c0 in base)
            face_list.append((view_z, proj, rgb))

    # painter's algorithm: farthest (most negative view z) first
    face_list.sort(key=lambda t: t[0])
    for _, proj, rgb in face_list:
        draw.polygon(proj, fill=rgb, outline=(30, 30, 30))

    centroids_px = [(int(np.clip(cx, 0, w - 1)), int(np.clip(cy, 0, h - 1))) for (cx, cy) in centroids]
    return img, centroids_px


def _gen_scene(idx, seed, img_size, jitter):
    rng = _scene_rng(seed, idx)
    n, positions, colors = _scene_spec(rng, jitter)

    base_disp, base_first = _simulate(positions, None)
    base_collapse = bool(np.any(base_disp > MOVE_EPS))
    base_total = float(base_disp.sum())
    initiator = base_first if base_collapse else -1

    flips = []
    for k in range(n):
        cf_disp, _ = _simulate(positions, k)
        cf_collapse = bool(np.any(cf_disp > MOVE_EPS))
        if cf_collapse != base_collapse:
            effect = abs(float(cf_disp.sum()) - base_total)
            flips.append((effect, k))
    flips.sort(reverse=True)
    keystone = flips[0][1] if flips else -1
    keystone_alt = flips[1][1] if len(flips) > 1 else -1

    img, centroids = _render(positions, colors, img_size)
    return {
        "n_blocks": n,
        "will_collapse": int(base_collapse),
        "initiator": initiator,
        "keystone": keystone,
        "keystone_alt": keystone_alt,
        "image": img,
        "centroids": centroids,
        "colors": colors,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    ap.add_argument("--n-scenes", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--img", type=int, default=IMG_DEFAULT)
    ap.add_argument("--jitter", type=float, default=JITTER_STEP)
    args = ap.parse_args()

    try:
        import mujoco  # noqa: F401
    except ImportError:
        raise SystemExit("pip install mujoco numpy pillow   (MuJoCo required)")
    import pandas as pd

    img_dir = args.out / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    scenes, blocks = [], []
    n_collapse = 0
    for idx in range(args.n_scenes):
        s = _gen_scene(idx, args.seed, args.img, args.jitter)
        sh = _scene_hash(args.seed, idx)
        s["image"].save(img_dir / f"{sh}.png")
        scenes.append({
            "scene_hash": sh, "n_blocks": s["n_blocks"],
            "will_collapse": s["will_collapse"], "initiator_block_id": s["initiator"],
            "keystone_block_id": s["keystone"], "keystone_alt_block_id": s["keystone_alt"],
        })
        for k in range(s["n_blocks"]):
            cx, cy = s["centroids"][k]
            r, g, b = s["colors"][k]
            blocks.append({"scene_hash": sh, "block_id": k, "cx": cx, "cy": cy,
                           "color_r": r, "color_g": g, "color_b": b})
        n_collapse += s["will_collapse"]
        if (idx + 1) % 200 == 0:
            print(f"  [{idx+1}/{args.n_scenes}] collapse-rate so far {n_collapse/(idx+1):.2f}")

    pd.DataFrame(scenes).to_csv(args.out / "scenes.csv", index=False)
    pd.DataFrame(blocks).to_csv(args.out / "blocks.csv", index=False)
    print(f"OK: wrote {len(scenes)} scenes (collapse rate "
          f"{n_collapse/max(1,len(scenes)):.2f}) to {args.out}")


if __name__ == "__main__":
    main()
