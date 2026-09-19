"""
generate.py - author-side raw-data builder for
              "Hidden Obstacle-Field Reconstruction From Probe-Ball Deflections"
              (codename PROBEMAP)

NOT run on the platform. Runs on the author's machine to synthesise the raw
corpus that prepare.py later splits. Everything is self-simulated and
self-rendered with a tiny dependency-free top-down software renderer (NumPy +
Pillow + imageio for H.264 muxing), so the output is original work shippable as
CC0 1.0. No external assets, no Blender, no OpenGL, no physics engine.

WHAT EACH CLIP IS
-----------------
A top-down view of a square arena. Several probe balls are launched straight
down from marked ports along the top edge. The arena contains a few HIDDEN
circular obstacles rendered the same colour as the floor (invisible). Each probe
bounces off the obstacles and the side walls by exact closed-form circle/segment
reflection, so its visible path kinks wherever it strikes an unseen obstacle; a
brief FLASH marks each contact POINT (not the obstacle's extent). Four coloured
corner markers fix a 12x12 cell coordinate frame.

The solver must INVERT the hidden layout from the deflections alone: recover the
occupancy of the 12x12 grid, count the obstacles, and forecast the behaviour of a
fresh straight-down probe from an un-shown column (the row of the first hidden
cell it would strike, or -1 if the column is clear). The map is deliberately
under-determined where no probe ever travels, which caps the ceiling and widens
the human/agent gap. Trails fade, so no single frame contains the full trajectory
set -- the layout lives only in motion integrated over time.

GROUND TRUTH IS EXACT (sampled, not measured off pixels)
--------------------------------------------------------
Obstacles, ports, and trajectories are all sampled / simulated in closed form,
so occupancy, obstacle count, and the query exit are exact by construction.

Each base scenario is rendered as up to 3 deterministic variants:
    base, relight (different floor style), mirror (horizontally flipped). Mirror
    flips the layout, ports, and labels together so answers stay in the observed
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
GRID = 12                       # 12 x 12 occupancy grid over the arena
W_DEFAULT = H_DEFAULT = 480
N_FRAMES = 90
FPS = 12

SCALE = None                    # set per render from W/H
BALL_R = 0.16
SPEED = 0.16                    # board units per frame
SUBSTEPS = 5                    # collision sub-steps per frame (anti-tunnelling)
TRAIL = 16                      # frames of fading trail kept visible
FLASH_LIFE = 6                  # frames a contact flash stays visible

LAYOUT_FAMILIES = ["sparse", "spread", "cluster", "dense"]

FLOOR_STYLES = {
    "slate":  {"bg": (232, 234, 240), "floor": (206, 210, 219), "grid": (192, 196, 206)},
    "warm":   {"bg": (238, 233, 224), "floor": (216, 208, 195), "grid": (200, 192, 178)},
    "cool":   {"bg": (224, 232, 236), "floor": (198, 212, 216), "grid": (184, 200, 205)},
    "dim":    {"bg": (214, 218, 226), "floor": (188, 193, 204), "grid": (174, 180, 192)},
}
STYLE_LIST = list(FLOOR_STYLES.keys())

PROBE_COLORS = [(208, 80, 76), (74, 126, 214), (86, 178, 104), (226, 176, 70),
                (164, 108, 202), (88, 188, 188), (224, 134, 70), (200, 96, 150),
                (120, 140, 70)]


# --------------------------------------------------------------------------
# rng / ids
# --------------------------------------------------------------------------
def _rng(seed: int, idx: int) -> np.random.Generator:
    digest = hashlib.sha256(f"probemap:{seed}:{idx}".encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _scene_hash(seed: int, base_idx: int, variant: str) -> str:
    return hashlib.sha256(f"probemap-clip:{seed}:{base_idx}:{variant}".encode()).hexdigest()[:16]


# --------------------------------------------------------------------------
# scenario sampling
# --------------------------------------------------------------------------
# obstacles are hidden GRID-CELL blocks (a concealed maze). Cells use (col, ry)
# with col 0=left and ry 0=BOTTOM (ry = floor(y)). Each "obstacle" is a small
# connected polyomino; blocks are separated by >=1 empty cell (incl. diagonals)
# so they are distinct and probes can pass between them.
SHAPES = [
    [(0, 0)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]


def _sample_blocks(rng, family):
    if family == "sparse":
        target = 3; lo_c, hi_c, lo_r, hi_r = 1, GRID - 2, 1, GRID - 3
    elif family == "spread":
        target = int(rng.integers(4, 6)); lo_c, hi_c, lo_r, hi_r = 1, GRID - 2, 1, GRID - 3
    elif family == "cluster":
        target = int(rng.integers(4, 6))
        cc = int(rng.integers(4, 8)); cr = int(rng.integers(3, 8))
        lo_c, hi_c = max(1, cc - 3), min(GRID - 2, cc + 3)
        lo_r, hi_r = max(1, cr - 3), min(GRID - 3, cr + 3)
    else:  # dense
        target = int(rng.integers(6, 8)); lo_c, hi_c, lo_r, hi_r = 1, GRID - 2, 1, GRID - 3

    occ = set(); blocks = []
    tries = 0
    while len(blocks) < target and tries < 1500:
        tries += 1
        shape = SHAPES[int(rng.integers(0, len(SHAPES)))]
        ac = int(rng.integers(lo_c, hi_c)); ar = int(rng.integers(lo_r, hi_r))
        cells = [(ac + dc, ar + dr) for (dc, dr) in shape]
        if any(not (1 <= c <= GRID - 2 and 1 <= r <= GRID - 2) for c, r in cells):
            continue
        # reject if any cell or its 8-neighbourhood touches an existing block
        clash = False
        for (c, r) in cells:
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if (c + dc, r + dr) in occ:
                        clash = True
        if clash:
            continue
        for cell in cells:
            occ.add(cell)
        blocks.append(cells)
    return occ, blocks


def _sample_scene(rng, base_idx):
    family = LAYOUT_FAMILIES[base_idx % len(LAYOUT_FAMILIES)]
    occ, blocks = _sample_blocks(rng, family)

    # candidate top-edge port columns; pick shown ports + one un-shown query port.
    # Shown probes get a small launch angle (visible in the video) so the field is
    # swept more thoroughly; the query probe is always launched straight down so a
    # solver can reproduce it exactly from the reconstructed map.
    cols = [round(0.8 + 0.65 * i, 3) for i in range(17)]   # ~0.8 .. 11.2
    num_probes = int(rng.integers(9, 16))
    num_probes = min(num_probes, len(cols) - 1)
    perm = list(rng.permutation(len(cols)))
    chosen = sorted(perm[:num_probes])
    ports = [{"x": float(cols[i]),
              "angle": float(rng.uniform(-0.30, 0.30)),
              "launch": int(rng.integers(0, 9))} for i in chosen]
    # query column: an integer cell-column whose centre lies on no shown port
    # (so it is "un-shown" from the top). We forecast how a fresh straight-down
    # probe from this column behaves -- see _query_hit_row.
    used_cols = {int(p["x"]) for p in ports}
    cand_cols = [c for c in range(GRID) if c not in used_cols]
    if not cand_cols:
        cand_cols = list(range(GRID))
    query_col = int(cand_cols[int(rng.integers(0, len(cand_cols)))])
    query_port = query_col + 0.5

    return {
        "base_idx": base_idx, "family": family, "occ": occ, "n_blocks": len(blocks),
        "ports": ports, "num_probes": num_probes,
        "query_col": query_col, "query_port": query_port,
        "style_key": STYLE_LIST[int(rng.integers(0, len(STYLE_LIST)))],
    }


def _mirror_scene(scene):
    m = dict(scene)
    m["occ"] = set((GRID - 1 - c, r) for (c, r) in scene["occ"])
    m["ports"] = [{"x": GRID - p["x"], "angle": -p["angle"], "launch": p["launch"]}
                  for p in scene["ports"]]
    m["query_col"] = GRID - 1 - scene["query_col"]
    m["query_port"] = m["query_col"] + 0.5
    return m


def _query_hit_row(occ, query_col):
    """Row (0=top) of the topmost solid cell a straight-down probe from
    `query_col` would strike, or -1 if the column is clear (probe passes
    through to the bottom)."""
    for ry in range(GRID - 1, -1, -1):
        if (query_col, ry) in occ:
            return GRID - 1 - ry
    return -1


# --------------------------------------------------------------------------
# exact tile-collision roller (axis-aligned reflection off hidden blocks)
# --------------------------------------------------------------------------
def _solid(occ, px, py):
    """True if board point (px,py) is inside a hidden block cell."""
    c = int(np.floor(px)); r = int(np.floor(py))
    return (c, r) in occ


def _roll(start_x, occ, n_frames, launch_frame=0, max_extra=0, angle=0.0):
    """Launch a probe from (start_x, top) heading downward at `angle` rad off
    vertical. Reflect off hidden block faces (axis-aligned) and the L/R/top walls
    (no flash on walls); the bottom edge is open. Return per-frame positions
    [(frame, x, y)], contacts [(frame, x, y, axis)] (only at hidden blocks), and
    the bottom-exit x. If max_extra>0, simulate past n_frames to find the exit."""
    x, y = float(start_x), GRID - BALL_R - 0.01
    vx, vy = SPEED * np.sin(angle), -SPEED * np.cos(angle)
    positions, contacts = [], []
    exit_x = None

    def step(f, record):
        nonlocal x, y, vx, vy, exit_x
        for _ in range(SUBSTEPS):
            dx, dy = vx / SUBSTEPS, vy / SUBSTEPS
            nx = x + dx
            if nx < BALL_R:
                vx = abs(vx)
            elif nx > GRID - BALL_R:
                vx = -abs(vx)
            elif _solid(occ, nx + (BALL_R if dx > 0 else -BALL_R), y):
                vx = -vx
                if record:
                    contacts.append((f, round(nx + (BALL_R if dx > 0 else -BALL_R)), y, "v"))
            else:
                x = nx
            ny = y + dy
            if ny > GRID - BALL_R:
                vy = -abs(vy)
            elif _solid(occ, x, ny + (BALL_R if dy > 0 else -BALL_R)):
                vy = -vy
                if record:
                    contacts.append((f, x, round(ny + (BALL_R if dy > 0 else -BALL_R)), "h"))
            else:
                y = ny
            if y < BALL_R:
                exit_x = x
                return True
        return False

    for f in range(n_frames):
        if f < launch_frame:
            positions.append((f, x, y)); continue
        done = step(f, True)
        positions.append((f, x, y))
        if done:
            break
    if max_extra > 0 and exit_x is None:
        for _ in range(max_extra):
            if step(n_frames, False):
                break
    if exit_x is None:
        exit_x = x
    return positions, contacts, float(exit_x)


def _occupancy(occ):
    """144-char row-major mask. row 0 = TOP (high y), col 0 = LEFT (low x).
    occ uses (col, ry) with ry = floor(y) measured from the BOTTOM."""
    cells = []
    for row in range(GRID):
        ry = GRID - 1 - row
        for col in range(GRID):
            cells.append("1" if (col, ry) in occ else "0")
    return "".join(cells)


def _simulate_scene(scene):
    occ = scene["occ"]
    probes = []
    for p in scene["ports"]:
        pos, con, _ = _roll(p["x"], occ, N_FRAMES, launch_frame=p["launch"],
                            angle=p["angle"])
        probes.append({"port": p["x"], "launch": p["launch"], "pos": pos, "contacts": con})
    occ_str = _occupancy(occ)
    return {"probes": probes, "occupancy": occ_str, "n_obstacles": scene["n_blocks"],
            "query_hit_row": _query_hit_row(occ, scene["query_col"])}


# --------------------------------------------------------------------------
# rendering (top-down)
# --------------------------------------------------------------------------
def _board_to_px(bx, by, scale, marg):
    return (marg + bx * scale, marg + (GRID - by) * scale)


def _render_base(scene, sim, style, scale, marg, w, h):
    img = Image.new("RGB", (w, h), tuple(style["bg"]))
    d = ImageDraw.Draw(img)
    x0, y0 = _board_to_px(0, GRID, scale, marg)
    x1, y1 = _board_to_px(GRID, 0, scale, marg)
    d.rectangle([x0, y0, x1, y1], fill=tuple(style["floor"]), outline=(120, 124, 134), width=2)
    for i in range(1, GRID):
        gx0, gy0 = _board_to_px(i, 0, scale, marg); gx1, gy1 = _board_to_px(i, GRID, scale, marg)
        d.line([gx0, gy0, gx1, gy1], fill=tuple(style["grid"]), width=1)
        gx0, gy0 = _board_to_px(0, i, scale, marg); gx1, gy1 = _board_to_px(GRID, i, scale, marg)
        d.line([gx0, gy0, gx1, gy1], fill=tuple(style["grid"]), width=1)
    for (mx, my, c) in [(0, 0, (220, 70, 70)), (GRID, 0, (70, 160, 220)),
                        (0, GRID, (90, 180, 100)), (GRID, GRID, (230, 180, 70))]:
        px, py = _board_to_px(mx, my, scale, marg)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=c, outline=(40, 40, 46))
    for p in scene["ports"]:
        px, py = _board_to_px(p["x"], GRID, scale, marg)
        d.polygon([(px - 6, py - 13), (px + 6, py - 13), (px, py - 2)], fill=(90, 92, 100))
    return img


def _render_clip(scene, sim, style_key, scale, marg, w, h):
    style = FLOOR_STYLES[style_key]
    base = _render_base(scene, sim, style, scale, marg, w, h)
    probes = sim["probes"]
    # index positions by frame for each probe
    pos_by_probe = []
    for pr in probes:
        m = {f: (x, y) for (f, x, y) in pr["pos"]}
        pos_by_probe.append(m)

    frames = []
    for fr in range(N_FRAMES):
        img = base.copy()
        d = ImageDraw.Draw(img)
        for pi, pr in enumerate(probes):
            col = PROBE_COLORS[pi % len(PROBE_COLORS)]
            m = pos_by_probe[pi]
            seg = [m[f] for f in range(max(pr["launch"], fr - TRAIL), fr + 1) if f in m]
            if len(seg) >= 2:
                pts = [_board_to_px(x, y, scale, marg) for (x, y) in seg]
                d.line(pts, fill=col, width=3, joint="curve")
            if fr in m and fr >= pr["launch"]:
                bx, by = _board_to_px(m[fr][0], m[fr][1], scale, marg)
                d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=col, outline=(30, 30, 34))
            for (cf, cx, cy, _ax) in pr["contacts"]:
                if 0 <= fr - cf < FLASH_LIFE:
                    fx, fy = _board_to_px(cx, cy, scale, marg)
                    rad = 6 - (fr - cf)
                    if rad > 0:
                        d.ellipse([fx - rad, fy - rad, fx + rad, fy + rad],
                                  fill=(255, 238, 130), outline=(190, 160, 30))
        frames.append(np.asarray(img, dtype=np.uint8))
    return frames


# --------------------------------------------------------------------------
# variants + main
# --------------------------------------------------------------------------
def _variant_rows(scene, seed, want_variants):
    rows = []
    base_id = f"q{scene['base_idx']:05d}"
    variants = ["base"]
    if want_variants:
        variants += ["relight", "mirror"]
    for variant in variants:
        vscene = _mirror_scene(scene) if variant == "mirror" else dict(scene)
        style_key = scene["style_key"]
        if variant == "relight":
            others = [s for s in STYLE_LIST if s != scene["style_key"]]
            style_key = others[scene["base_idx"] % len(others)]
        sim = _simulate_scene(vscene)
        sh = _scene_hash(seed, scene["base_idx"], variant)
        rows.append({
            "scene_hash": sh, "base_scenario_id": base_id, "variant": variant,
            "num_probes": vscene["num_probes"], "query_port": round(vscene["query_port"], 3),
            "layout_family": scene["family"], "floor_style": style_key,
            "occupancy_json": sim["occupancy"], "n_obstacles": sim["n_obstacles"],
            "query_hit_row": sim["query_hit_row"],
            "_scene": vscene, "_sim": sim, "_style_key": style_key,
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
    ap.add_argument("--n-base", type=int, default=240)
    ap.add_argument("--seed", type=int, default=41)
    ap.add_argument("--w", type=int, default=W_DEFAULT)
    ap.add_argument("--h", type=int, default=H_DEFAULT)
    ap.add_argument("--no-variants", action="store_true")
    args = ap.parse_args()

    import pandas as pd

    marg = 26
    scale = (min(args.w, args.h) - 2 * marg) / GRID

    vid_dir = args.out / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)

    meta_rows = []
    n_clips = 0
    for base_idx in range(args.n_base):
        rng = _rng(args.seed, base_idx)
        scene = _sample_scene(rng, base_idx)
        for row in _variant_rows(scene, args.seed, not args.no_variants):
            frames = _render_clip(row["_scene"], row["_sim"], row["_style_key"],
                                  scale, marg, args.w, args.h)
            _encode_mp4(str(vid_dir / f"{row['scene_hash']}.mp4"), frames, FPS)
            clean = {k: v for k, v in row.items() if not k.startswith("_")}
            clean["video"] = f"videos/{row['scene_hash']}.mp4"
            meta_rows.append(clean)
            n_clips += 1
        if (base_idx + 1) % 10 == 0:
            print(f"  [{base_idx+1}/{args.n_base}] base scenarios rendered ({n_clips} clips)")

    cols = ["scene_hash", "video", "base_scenario_id", "variant", "num_probes",
            "query_port", "layout_family", "floor_style", "occupancy_json",
            "n_obstacles", "query_hit_row"]
    pd.DataFrame(meta_rows)[cols].to_csv(args.out / "scenes.csv", index=False)
    print(f"OK: wrote {n_clips} clips to {args.out}")


if __name__ == "__main__":
    main()
