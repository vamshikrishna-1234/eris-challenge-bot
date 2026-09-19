"""
generate.py - author-side raw-data builder for
              "Tangle Trace: Cable Connectivity And Counterfactual Pull"
              (codename TANGLE)

NOT run on the platform. Runs on the author's machine to synthesise the raw
corpus that prepare.py later splits into public/private. Everything is
self-simulated and self-rendered with a tiny dependency-free 2-D software
renderer (NumPy + Pillow), so the output is original work shippable as CC0 1.0.
No external assets.

WHAT EACH IMAGE IS
------------------
A flat over/under diagram of N distinctly-coloured cables running from labelled
top endpoints (T0, T1, ...) down through a central tangle to labelled bottom
endpoints (X0, X1, ...). At every crossing one cable passes OVER the other (the
under cable is drawn broken, standard knot-diagram convention). The tangle is
built as a braid (a stack of adjacent swaps), so the ground truth - which top
endpoint connects to which bottom endpoint, every over/under, and therefore the
whole pull behaviour - is exact by construction.

THE PULL RULE (stated to solvers; they apply it by tracing the diagram)
----------------------------------------------------------------------
Pulling a top endpoint tensions its cable. Wherever that cable passes UNDER
another cable, the pull drags the over-cable (it goes taut). That cable in turn
drags any cable IT passes under, and so on - a cascade. The pulled cable LOCKS
(will not pull free) if this dragging chains back to it (a mutual interlock);
otherwise it SLIPS free.

THE TASK (per image)
--------------------
  pairing_json    : which bottom endpoint each top endpoint connects to (or
                    "unknown" for cables buried too deep in the tangle to trace)
  n_true_locks    : number of genuine pairwise interlocks (clasps) vs illusory
                    crossings
  pull_outcome    : for the queried top endpoint -> "locks" / "slips"
                    ("unknown" if that cable is buried)
  pull_taut_json  : ORDERED list of the other cables that go taut when the
                    queried endpoint is pulled (the counterfactual cascade)

Cables buried in the dense core are genuinely untraceable -> "unknown" is the
correct answer there (an irreducible-information cap).

OUTPUTS (into --out, default raw_data/)
    raw_data/images/<scene_hash>.jpg
    raw_data/scenes.csv

REQUIREMENTS: pip install numpy pillow
Determinism: each base scenario is seeded from (--seed, base index).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# --------------------------------------------------------------------------
# render constants
# --------------------------------------------------------------------------
W, H = 640, 480
Y_TOP = 92            # y of the top endpoints
Y_BOT = 404          # y of the bottom endpoints
X_MARGIN = 96        # left/right margin for the outermost tracks
LINE_W = 7           # nominal cable width (px)

N_CHOICES = [4, 5, 6]
N_WEIGHTS = [0.34, 0.40, 0.26]
R_MIN, R_MAX = 11, 16   # braid rows

P_CORE = 0.58        # crossing probability inside the dense core band
P_EDGE = 0.30        # crossing probability outside it

CABLE_PALETTES = {
    "light": [
        [(176, 64, 54), (54, 96, 168), (55, 142, 78), (194, 142, 45), (130, 88, 170), (55, 150, 150)],
        [(180, 76, 92), (68, 116, 154), (74, 132, 86), (190, 158, 72), (146, 98, 136), (70, 138, 154)],
        [(150, 70, 52), (48, 108, 164), (76, 122, 58), (172, 132, 50), (126, 76, 156), (74, 140, 132)],
    ],
    "dark": [
        [(220, 102, 88), (86, 150, 214), (102, 188, 118), (222, 184, 82), (176, 128, 214), (96, 198, 198)],
        [(214, 94, 118), (96, 136, 196), (116, 178, 120), (218, 174, 96), (186, 132, 176), (108, 184, 204)],
        [(228, 120, 78), (90, 166, 206), (126, 190, 104), (230, 198, 104), (172, 142, 220), (116, 204, 184)],
    ],
}
STYLE_BG = {"light": (235, 232, 222), "dark": (36, 39, 43)}
STYLE_INK = {"light": (45, 42, 36), "dark": (218, 216, 206)}
STYLE_CORE = {"light": (218, 214, 204), "dark": (50, 53, 58)}


# --------------------------------------------------------------------------
# rng / ids
# --------------------------------------------------------------------------
def _rng(seed: int, idx: int) -> np.random.Generator:
    digest = hashlib.sha256(f"tangle:{seed}:{idx}".encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _scene_hash(seed: int, base_idx: int, variant: str) -> str:
    return hashlib.sha256(f"tangle-img:{seed}:{base_idx}:{variant}".encode()).hexdigest()[:16]


def _base_id(seed: int, base_idx: int) -> str:
    return hashlib.sha256(f"tangle-base:{seed}:{base_idx}".encode()).hexdigest()[:12]


# --------------------------------------------------------------------------
# braid construction (exact ground truth)
# --------------------------------------------------------------------------
def _build_braid(rng, n, rows):
    """Brick-wall braid. Returns states (level -> pos->strand) and crossings
    [(a, b, over_strand, row, track_k)]."""
    core_lo, core_hi = int(0.40 * rows), int(0.62 * rows)
    states = [list(range(n))]
    crossings = []
    for r in range(rows):
        cur = states[-1][:]
        pc = P_CORE if core_lo <= r < core_hi else P_EDGE
        k = r % 2
        while k + 1 < n:
            if rng.random() < pc:
                a, b = cur[k], cur[k + 1]
                over = a if rng.random() < 0.5 else b
                crossings.append((a, b, over, r, k))
                cur[k], cur[k + 1] = cur[k + 1], cur[k]
            k += 2
        states.append(cur)
    return states, crossings, (core_lo, core_hi)


def _analyze_braid(n, states, crossings, core):
    """Derive the under-graph, clasps, determinability, and final positions."""
    core_lo, core_hi = core
    # under -> over edges, with the earliest row of contact
    adj = {s: set() for s in range(n)}
    edge_row = {}
    under_in_core = [0] * n
    for (a, b, over, r, k) in crossings:
        under = b if over == a else a
        adj[under].add(over)
        key = (under, over)
        if key not in edge_row or r < edge_row[key]:
            edge_row[key] = r
        if core_lo <= r < core_hi:
            under_in_core[under] += 1
    determinable = [under_in_core[s] < 2 for s in range(n)]
    final_pos = [states[-1].index(s) for s in range(n)]   # strand s -> exit X
    # clasps: pairs with mutual under-edges, both determinable
    n_locks = 0
    for a in range(n):
        for b in range(a + 1, n):
            if b in adj[a] and a in adj[b] and determinable[a] and determinable[b]:
                n_locks += 1
    return adj, edge_row, determinable, final_pos, n_locks


def _cascade(q, adj, edge_row):
    """BFS of cables dragged taut by pulling q (q excluded), in contact order."""
    seen = {q}
    order = []
    dq = deque([q])
    while dq:
        u = dq.popleft()
        for v in sorted(adj[u], key=lambda v: edge_row.get((u, v), 999)):
            if v not in seen:
                seen.add(v)
                order.append(v)
                dq.append(v)
    return order


def _locks_back(q, adj):
    """Does pulling q chain back to q (mutual interlock -> locks)?"""
    seen = set()
    dq = deque(adj[q])
    while dq:
        u = dq.popleft()
        if u == q:
            return True
        if u in seen:
            continue
        seen.add(u)
        dq.extend(adj[u])
    return q in seen or False


def _choose_query(rng, n, adj, edge_row, determinable):
    """Pick the pulled top endpoint, balancing answerable vs buried (unknown)."""
    det = [s for s in range(n) if determinable[s]]
    bur = [s for s in range(n) if not determinable[s]]
    # answerable = determinable AND whole cascade determinable; prefer ones with a
    # NON-trivial cascade so a constant empty-cascade guess cannot coast.
    answerable, answerable_nonempty = [], []
    for s in det:
        casc = _cascade(s, adj, edge_row)
        if all(determinable[c] for c in casc):
            answerable.append(s)
            if len(casc) >= 1:
                answerable_nonempty.append(s)
    want_unknown = (rng.random() < 0.25) and bur
    if want_unknown:
        return int(rng.choice(bur)), "unknown"
    if answerable_nonempty:
        return int(rng.choice(answerable_nonempty)), "ok"
    if answerable:
        return int(rng.choice(answerable)), "ok"
    if bur:
        return int(rng.choice(bur)), "unknown"
    return int(rng.choice(det)) if det else 0, "ok"


# --------------------------------------------------------------------------
# scene assembly
# --------------------------------------------------------------------------
def _ood_axis(n, n_cross, query_state, n_locks):
    if query_state == "unknown":
        return "buried_query"
    if n >= 6:
        return "many_cables"
    return "standard"


def _make_scene(rng, n):
    rows = int(rng.integers(R_MIN, R_MAX + 1))
    states, crossings, core = _build_braid(rng, n, rows)
    adj, edge_row, determinable, final_pos, n_locks = _analyze_braid(n, states, crossings, core)

    q, qstate = _choose_query(rng, n, adj, edge_row, determinable)
    if qstate == "unknown":
        pull_outcome = "unknown"
        taut = []
    else:
        pull_outcome = "locks" if _locks_back(q, adj) else "slips"
        taut = _cascade(q, adj, edge_row)

    pairing = {f"T{s}": (f"X{final_pos[s]}" if determinable[s] else "unknown")
               for s in range(n)}
    pull_taut = [f"T{s}" for s in taut]

    return dict(
        n=n, rows=rows, states=states, crossings=crossings, core=core,
        determinable=determinable, final_pos=final_pos,
        n_true_locks=n_locks, query=q, pull_outcome=pull_outcome,
        pairing_json=json.dumps(pairing, allow_nan=False),
        pull_taut_json=json.dumps(pull_taut, allow_nan=False),
        n_cross=len(crossings),
        ood_axis=_ood_axis(n, len(crossings), qstate, n_locks),
    )


def sample_all_scenes(seed: int, n_base: int):
    scenes = []
    for i in range(n_base):
        base_id = _base_id(seed, i)
        for variant, style in (("base", "light"), ("recolor", "dark")):
            vrng = _rng(seed + (1 if variant == "base" else 2) * 6151, i)
            n = int(vrng.choice(N_CHOICES, p=N_WEIGHTS))
            sc = _make_scene(vrng, n)
            sc.update(base_scenario_id=base_id, variant=variant, render_style=style,
                      scene_hash=_scene_hash(seed, i, variant))
            sc["tangle_family"] = f"n{n}"
            scenes.append(sc)
    return scenes


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def _track_x(n):
    if n == 1:
        return [W // 2]
    step = (W - 2 * X_MARGIN) / (n - 1)
    return [int(X_MARGIN + i * step) for i in range(n)]


def _row_y(rows, r):
    return int(Y_TOP + (Y_BOT - Y_TOP) * (r / rows))


def _render_rng(scene):
    digest = hashlib.sha256(f"render:{scene['scene_hash']}".encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _jitter_color(col, rng, amount=16):
    arr = np.array(col, dtype=np.int16) + rng.integers(-amount, amount + 1, size=3)
    return tuple(int(np.clip(v, 0, 255)) for v in arr)


def _mix(a, b, t):
    return tuple(int(round((1 - t) * x + t * y)) for x, y in zip(a, b))


def _textured_background(style, rng):
    base = np.array(STYLE_BG[style], dtype=np.int16)
    noise = rng.normal(0, 8 if style == "light" else 5, size=(H, W, 1))
    grain = np.repeat(noise, 3, axis=2)
    tint = rng.integers(-5, 6, size=(1, 1, 3))
    arr = np.clip(base + grain + tint, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGB").filter(ImageFilter.GaussianBlur(0.35))
    dr = ImageDraw.Draw(img)
    for _ in range(26):
        x0 = int(rng.integers(-60, W + 20))
        y0 = int(rng.integers(40, H - 30))
        length = int(rng.integers(90, 260))
        col = _jitter_color(STYLE_CORE[style], rng, 10)
        dr.line([(x0, y0), (x0 + length, y0 + int(rng.integers(-5, 6)))],
                fill=col, width=int(rng.integers(1, 3)))
    return img


def _palette(style, n, rng):
    pal = list(CABLE_PALETTES[style][int(rng.integers(0, len(CABLE_PALETTES[style])))])
    rng.shuffle(pal)
    return [_jitter_color(pal[i % len(pal)], rng, 18) for i in range(n)]


def _row_track_positions(n, rows, rng):
    base = np.array(_track_x(n), dtype=float)
    jitter = rng.normal(0, 5.0, size=(rows + 1, n))
    jitter[0, :] *= 0.45
    jitter[-1, :] *= 0.45
    phase = rng.random(n) * 2 * math.pi
    for r in range(rows + 1):
        jitter[r, :] += np.sin((r / max(rows, 1)) * math.pi * 2 + phase) * rng.uniform(1.5, 4.0, size=n)
    return np.round(base[None, :] + jitter).astype(int)


def _draw_polyline(dr, pts, col, w, shadow=True, highlight=True):
    if shadow:
        dr.line([(x + 3, y + 4) for x, y in pts], fill=(0, 0, 0), width=w + 3)
    dr.line(pts, fill=col, width=w)
    rr = w / 2
    for (x, y) in (pts[0], pts[-1]):
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
    if highlight and w >= 6:
        hi = _mix(col, (255, 255, 255), 0.20)
        dr.line([(x - 1, y - 1) for x, y in pts], fill=hi, width=max(1, w // 4))


def _segment_points(x0, y0, x1, y1, rng, bend=12):
    mx = (x0 + x1) / 2 + float(rng.normal(0, bend))
    my = (y0 + y1) / 2 + float(rng.normal(0, bend * 0.45))
    return [(int(x0), int(y0)), (int(round(mx)), int(round(my))), (int(x1), int(y1))]


def _draw_endpoint(dr, x, y, label, col, ink, rng, top=True):
    r = int(rng.integers(7, 10))
    shape = int(rng.integers(0, 3))
    outline = _mix(ink, col, 0.15)
    if shape == 0:
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=outline, width=2)
    elif shape == 1:
        dr.rounded_rectangle([x - r, y - r, x + r, y + r], radius=3, fill=col, outline=outline, width=2)
    else:
        pts = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
        dr.polygon(pts, fill=col)
        dr.line(pts + [pts[0]], fill=outline, width=2)
    tx = x + int(rng.integers(-12, 2))
    ty = y - int(rng.integers(21, 29)) if top else y + int(rng.integers(11, 18))
    dr.text((tx, ty), label, fill=ink)


def _draw_distractors(dr, style, colors, rng):
    for _ in range(int(rng.integers(3, 7))):
        col = _jitter_color(colors[int(rng.integers(0, len(colors)))], rng, 26)
        x = int(rng.integers(35, W - 35))
        y = int(rng.integers(130, H - 95))
        length = int(rng.integers(34, 86))
        ang = float(rng.uniform(-0.9, 0.9))
        pts = [
            (x, y),
            (int(x + length * 0.55 * math.cos(ang)), int(y + length * 0.55 * math.sin(ang))),
            (int(x + length * math.cos(ang + rng.normal(0, 0.18))), int(y + length * math.sin(ang + rng.normal(0, 0.18)))),
        ]
        _draw_polyline(dr, pts, col, int(rng.integers(3, 6)), shadow=True, highlight=False)


def _render(scene, out_path: Path):
    n = scene["n"]
    rows = scene["rows"]
    states = scene["states"]
    crossings = scene["crossings"]
    core_lo, core_hi = scene["core"]
    style = scene["render_style"]
    rng = _render_rng(scene)
    colors = _palette(style, n, rng)
    ink = STYLE_INK[style]

    img = _textured_background(style, rng)
    dr = ImageDraw.Draw(img)
    xs = _row_track_positions(n, rows, rng)
    widths = [int(np.clip(LINE_W + rng.integers(-2, 3), 5, 10)) for _ in range(n)]

    # Faint board/tape region: it gives the bundle depth without creating a clean
    # parser-friendly crossing mask.
    dr.rounded_rectangle([X_MARGIN - 30, _row_y(rows, core_lo) - 6,
                          W - X_MARGIN + 30, _row_y(rows, core_hi) + 6],
                         radius=16, fill=_jitter_color(STYLE_CORE[style], rng, 9))
    for _ in range(4):
        y = int(rng.integers(_row_y(rows, core_lo) - 18, _row_y(rows, core_hi) + 18))
        dr.line([(X_MARGIN - 44, y), (W - X_MARGIN + 44, y + int(rng.integers(-8, 9)))],
                fill=_jitter_color(STYLE_CORE[style], rng, 18), width=int(rng.integers(3, 8)))

    # row-swap lookup: track_k -> over_strand at row r
    swaps = {}
    for (a, b, over, r, k) in crossings:
        swaps[(r, k)] = over

    _draw_distractors(dr, style, colors, rng)

    # stubs from top endpoints into row 0, and from last row to bottom endpoints
    for p in range(n):
        s_top = states[0][p]
        _draw_polyline(dr, [(int(xs[0, p]), Y_TOP), (int(xs[0, p]), _row_y(rows, 0))],
                       colors[s_top % len(colors)], widths[s_top], shadow=True)
        s_bot = states[rows][p]
        _draw_polyline(dr, [(int(xs[rows, p]), _row_y(rows, rows)), (int(xs[rows, p]), Y_BOT)],
                       colors[s_bot % len(colors)], widths[s_bot], shadow=True)

    for r in range(rows):
        y0, y1 = _row_y(rows, r), _row_y(rows, r + 1)
        segs = []  # (strand, x0, x1, role)
        for p in range(n):
            s = states[r][p]
            dest = states[r + 1].index(s)
            if dest == p:
                segs.append((s, int(xs[r, p]), int(xs[r + 1, p]), "plain"))
            else:
                k = min(p, dest)
                over_s = swaps.get((r, k))
                segs.append((s, int(xs[r, p]), int(xs[r + 1, dest]), "over" if s == over_s else "under"))
        # plains + unders first
        for s, x0, x1, role in segs:
            if role != "over":
                pts = _segment_points(x0, y0, x1, y1, rng, bend=7 if role == "plain" else 10)
                _draw_polyline(dr, pts, colors[s % len(colors)], widths[s], shadow=True)
        # overs last: the upper cable physically covers the lower cable instead
        # of using a uniform background-coloured gap convention.
        for s, x0, x1, role in segs:
            if role == "over":
                pts = _segment_points(x0, y0, x1, y1, rng, bend=10)
                _draw_polyline(dr, pts, _mix(colors[s % len(colors)], (255, 255, 255), 0.04),
                               widths[s] + 1, shadow=True)

    # endpoint dots + labels
    for p in range(n):
        s_top = states[0][p]
        _draw_endpoint(dr, int(xs[0, p]), Y_TOP, f"T{s_top}",
                       colors[s_top % len(colors)], ink, rng, top=True)
        _draw_endpoint(dr, int(xs[rows, p]), Y_BOT, f"X{p}",
                       colors[states[rows][p] % len(colors)], ink, rng, top=False)

    # Mild acquisition artifacts: every scene has a slightly different camera
    # angle, blur/noise, and JPEG response. This breaks brittle colour-threshold
    # and fixed-gap parsers while keeping the labels legible to vision models.
    angle = float(rng.normal(0.0, 0.65))
    fill = STYLE_BG[style]
    img = img.rotate(angle, resample=Image.Resampling.BICUBIC, fillcolor=fill)
    if rng.random() < 0.85:
        img = img.filter(ImageFilter.GaussianBlur(float(rng.uniform(0.15, 0.65))))
    arr = np.array(img).astype(np.int16)
    arr += rng.normal(0, float(rng.uniform(1.5, 4.5)), size=arr.shape).astype(np.int16)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=int(rng.integers(78, 91)))


# --------------------------------------------------------------------------
# csv row
# --------------------------------------------------------------------------
def _scene_row(sc):
    return {
        "scene_hash": sc["scene_hash"],
        "image": f"images/{sc['scene_hash']}.jpg",
        "base_scenario_id": sc["base_scenario_id"],
        "variant": sc["variant"],
        "render_style": sc["render_style"],
        "n_cables": sc["n"],
        "pull_endpoint": f"T{sc['query']}",
        "pairing_json": sc["pairing_json"],
        "n_true_locks": sc["n_true_locks"],
        "pull_outcome": sc["pull_outcome"],
        "pull_taut_json": sc["pull_taut_json"],
        "tangle_family": sc["tangle_family"],
        "ood_axis": sc["ood_axis"],
    }


def _done(sc, img_dir: Path) -> bool:
    return (img_dir / f"{sc['scene_hash']}.jpg").exists()


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Generate TANGLE raw corpus.")
    ap.add_argument("--n-base", type=int, default=1000,
                    help="Base scenarios (each yields 2 variant images).")
    ap.add_argument("--seed", type=int, default=44)
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    ap.add_argument("--skip-render", action="store_true")
    args = ap.parse_args()

    out_dir = args.out.resolve()
    img_dir = out_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    print(f"Sampling {args.n_base} base scenarios (seed={args.seed}) -> "
          f"{args.n_base * 2} images ...")
    scenes = sample_all_scenes(args.seed, args.n_base)

    if not args.skip_render:
        already = sum(1 for s in scenes if _done(s, img_dir))
        if already:
            print(f"  {already} images already rendered - skipping those.")
        for idx, sc in enumerate(scenes):
            if _done(sc, img_dir):
                continue
            _render(sc, img_dir / f"{sc['scene_hash']}.jpg")
            if (idx + 1) % 200 == 0:
                print(f"  rendered {idx + 1} / {len(scenes)} ...")

    import pandas as pd
    cols = ["scene_hash", "image", "base_scenario_id", "variant", "render_style",
            "n_cables", "pull_endpoint", "pairing_json", "n_true_locks",
            "pull_outcome", "pull_taut_json", "tangle_family", "ood_axis"]
    pd.DataFrame([_scene_row(s) for s in scenes])[cols].to_csv(
        out_dir / "scenes.csv", index=False)
    print(f"Done. {len(scenes)} images. scenes.csv -> {out_dir / 'scenes.csv'}")


if __name__ == "__main__":
    main()
