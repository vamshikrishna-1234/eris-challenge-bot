"""
generate.py - author-side raw builder for
              "Hidden Control Panel Circuit Induction"  (codename PANEL)

NOT run on the platform. Self-simulates a control panel whose lamps are driven by
hidden Boolean gates over the switches, scripts a sequence of switch flips, and
self-renders the panel evolving (NumPy + Pillow + imageio H.264). Procedural only
-> CC0.

WHAT EACH SCENE IS
------------------
A panel has S switches and L lamps. Each lamp is wired to a hidden subset of
switches through a hidden logic gate (BUF/NOT/AND/OR/NAND/NOR/XOR/XNOR). A scripted
sequence of single/double switch flips is applied; after each flip the lamps
settle and the panel is filmed. The solver sees the clip (switch positions + lamp
on/off each step) and a public flip log, and must induce each lamp's wiring (gate
+ input switches) and predict the lamp pattern for a held-out query switch config.

GROUND TRUTH IS EXACT
---------------------
The wiring and every lamp state are computed from the sampled Boolean circuit -
never read back from pixels.

OUTPUT (into --out, default raw_data/)
    raw_data/videos/<scene_hash>.mp4
    raw_data/scenes.csv  scene_hash, n_switches, n_lamps, flip_log_json,
                         query_config, wiring_json, query_pattern, init_config_json,
                         circuit_family, variant, ood_axis, render_style

REQUIREMENTS: pip install numpy pillow imageio imageio-ffmpeg
Determinism: each scene seeded from (--seed, scene index).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np

IMG_W_DEFAULT = 480
IMG_H_DEFAULT = 320
FPS = 10
HOLD = 7                     # frames each settled state is held
GATES_MULTI = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]
GATES_SINGLE = ["BUF", "NOT"]
RENDER_STYLES = ["panelA", "panelB"]


def _scene_rng(seed: int, idx: int) -> np.random.Generator:
    digest = hashlib.sha256(f"panel:{seed}:{idx}".encode()).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _scene_hash(seed: int, idx: int) -> str:
    return hashlib.sha256(f"panel-scene:{seed}:{idx}".encode()).hexdigest()[:16]


def _eval_gate(gate: str, vals: list) -> int:
    s = sum(vals)
    if gate == "BUF":
        return int(vals[0])
    if gate == "NOT":
        return int(not vals[0])
    if gate == "AND":
        return int(all(vals))
    if gate == "OR":
        return int(any(vals))
    if gate == "NAND":
        return int(not all(vals))
    if gate == "NOR":
        return int(not any(vals))
    if gate == "XOR":
        return int(s % 2 == 1)
    if gate == "XNOR":
        return int(s % 2 == 0)
    raise ValueError(gate)


def _lamp_value(wiring: dict, config: list) -> int:
    vals = [config[i] for i in wiring["inputs"]]
    return _eval_gate(wiring["gate"], vals)


def _on_rate(wiring: dict, S: int) -> float:
    cnt = 0
    total = 0
    for cfg in product([0, 1], repeat=S):
        cnt += _lamp_value(wiring, list(cfg))
        total += 1
    return cnt / total


def _sample_wiring(rng: np.random.Generator, S: int, ood: str) -> dict:
    """One lamp's wiring with on-rate kept in a balanced band."""
    for _ in range(64):
        if ood == "multi_input":
            k = int(rng.integers(2, min(S, 3) + 1))
        elif ood == "xor_heavy":
            k = int(rng.integers(2, min(S, 3) + 1))
        else:
            k = int(rng.integers(1, min(S, 3) + 1))
        inputs = sorted(rng.permutation(S)[:k].tolist())
        if k == 1:
            gate = GATES_SINGLE[int(rng.integers(0, 2))]
        elif ood == "xor_heavy":
            gate = ["XOR", "XNOR"][int(rng.integers(0, 2))]
        else:
            gate = GATES_MULTI[int(rng.integers(0, len(GATES_MULTI)))]
        w = {"gate": gate, "inputs": [int(i) for i in inputs]}
        r = _on_rate(w, S)
        if 0.25 <= r <= 0.75:
            return w
    return w


def _sample_scene(rng: np.random.Generator) -> dict:
    render_style = RENDER_STYLES[int(rng.integers(0, len(RENDER_STYLES)))]
    circuit_family = ["ca", "cb", "cc"][int(rng.integers(0, 3))]
    variant = ["a", "b"][int(rng.integers(0, 2))]

    roll = rng.random()
    if roll < 0.13:
        ood = "xor_heavy"
    elif roll < 0.26:
        ood = "multi_input"
    elif roll < 0.39:
        ood = "sparse_interventions"
    else:
        ood = "none"

    S = int(rng.integers(3, 7))
    L = int(rng.integers(3, 7))

    # wiring per lamp, balanced overall on-rate
    for _ in range(40):
        wiring = {str(j): _sample_wiring(rng, S, ood) for j in range(L)}
        rates = [_on_rate(w, S) for w in wiring.values()]
        if 0.4 <= float(np.mean(rates)) <= 0.6:
            break

    # flip sequence
    n_steps = int(rng.integers(4, 7)) if ood == "sparse_interventions" else int(rng.integers(9, 15))
    init_config = [int(b) for b in rng.integers(0, 2, size=S)]
    config = list(init_config)
    seen = {tuple(config)}
    flip_log = []
    for _ in range(n_steps):
        k = 1 if rng.random() < 0.65 else 2
        flips = sorted(rng.permutation(S)[:k].tolist())
        for i in flips:
            config[i] ^= 1
        flip_log.append([int(i) for i in flips])
        seen.add(tuple(config))

    # held-out query config not among demonstrated configs (if possible)
    all_cfgs = [list(c) for c in product([0, 1], repeat=S)]
    held = [c for c in all_cfgs if tuple(c) not in seen]
    query_config = held[int(rng.integers(0, len(held)))] if held else all_cfgs[int(rng.integers(0, len(all_cfgs)))]
    query_pattern = [_lamp_value(wiring[str(j)], query_config) for j in range(L)]

    return {
        "render_style": render_style, "circuit_family": circuit_family, "variant": variant,
        "ood_axis": ood, "S": S, "L": L, "wiring": wiring, "init_config": init_config,
        "flip_log": flip_log, "query_config": query_config, "query_pattern": query_pattern,
    }


def _configs_over_time(sc: dict) -> list:
    cfg = list(sc["init_config"])
    seq = [list(cfg)]
    for flips in sc["flip_log"]:
        for i in flips:
            cfg[i] ^= 1
        seq.append(list(cfg))
    return seq


def _render_panel(sc: dict, config: list, img_w: int, img_h: int) -> np.ndarray:
    from PIL import Image, ImageDraw

    if sc["render_style"] == "panelA":
        bg, frame = (40, 42, 50), (66, 70, 82)
        sw_track, knob_on, knob_off = (90, 94, 108), (96, 210, 120), (150, 150, 160)
        lamp_on, lamp_off = (250, 214, 70), (60, 60, 70)
    else:
        bg, frame = (30, 36, 46), (54, 64, 80)
        sw_track, knob_on, knob_off = (78, 90, 110), (110, 180, 230), (140, 144, 156)
        lamp_on, lamp_off = (255, 150, 90), (58, 56, 64)

    im = Image.new("RGB", (img_w, img_h), bg)
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, img_w - 8, img_h - 8], outline=frame, width=4)

    S, L = sc["S"], sc["L"]
    lamp_states = [_lamp_value(sc["wiring"][str(j)], config) for j in range(L)]

    # switches across top
    sw_y0, sw_y1 = 40, 150
    for i in range(S):
        cx = int(img_w * (i + 1) / (S + 1))
        d.rectangle([cx - 14, sw_y0, cx + 14, sw_y1], fill=sw_track, outline=(20, 20, 24), width=2)
        on = config[i] == 1
        ky = sw_y0 + 8 if on else sw_y1 - 38
        d.rectangle([cx - 11, ky, cx + 11, ky + 30], fill=(knob_on if on else knob_off),
                    outline=(20, 20, 24), width=2)
        d.text((cx - 8, sw_y1 + 6), f"S{i}", fill=(220, 220, 228))

    # lamps across bottom
    lp_y = img_h - 70
    for j in range(L):
        cx = int(img_w * (j + 1) / (L + 1))
        on = lamp_states[j] == 1
        r = 18
        d.ellipse([cx - r, lp_y - r, cx + r, lp_y + r], fill=(lamp_on if on else lamp_off),
                  outline=(20, 20, 24), width=2)
        if on:
            d.ellipse([cx - r - 4, lp_y - r - 4, cx + r + 4, lp_y + r + 4], outline=lamp_on, width=2)
        d.text((cx - 8, lp_y + r + 4), f"L{j}", fill=(220, 220, 228))

    return np.asarray(im, dtype=np.uint8)


def _render_clip(sc: dict, img_w: int, img_h: int) -> np.ndarray:
    frames = []
    for cfg in _configs_over_time(sc):
        f = _render_panel(sc, cfg, img_w, img_h)
        for _ in range(HOLD):
            frames.append(f)
    return np.stack(frames, axis=0)


def _gen_scene(idx: int, seed: int, img_w: int, img_h: int):
    rng = _scene_rng(seed, idx)
    sc = _sample_scene(rng)
    clip = _render_clip(sc, img_w, img_h)
    return sc, clip


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    ap.add_argument("--n-scenes", type=int, default=800)
    ap.add_argument("--seed", type=int, default=59)
    ap.add_argument("--img-w", type=int, default=IMG_W_DEFAULT)
    ap.add_argument("--img-h", type=int, default=IMG_H_DEFAULT)
    args = ap.parse_args()

    import imageio.v3 as iio
    import pandas as pd

    vdir = args.out / "videos"
    vdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx in range(args.n_scenes):
        sc, clip = _gen_scene(idx, args.seed, args.img_w, args.img_h)
        sh = _scene_hash(args.seed, idx)
        iio.imwrite(vdir / f"{sh}.mp4", clip, fps=FPS, codec="libx264", quality=7,
                    macro_block_size=16)
        rows.append({
            "scene_hash": sh, "n_switches": sc["S"], "n_lamps": sc["L"],
            "flip_log_json": json.dumps(sc["flip_log"]),
            "query_config": json.dumps(sc["query_config"]),
            "wiring_json": json.dumps(sc["wiring"]),
            "query_pattern": json.dumps(sc["query_pattern"]),
            "init_config_json": json.dumps(sc["init_config"]),
            "circuit_family": sc["circuit_family"], "variant": sc["variant"],
            "ood_axis": sc["ood_axis"], "render_style": sc["render_style"],
        })
        if (idx + 1) % 100 == 0:
            print(f"  [{idx+1}/{args.n_scenes}] clips rendered")

    pd.DataFrame(rows).to_csv(args.out / "scenes.csv", index=False)
    print(f"OK: wrote {len(rows)} clips to {args.out}")


if __name__ == "__main__":
    main()
