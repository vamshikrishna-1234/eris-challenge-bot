"""
_sanity_smoke.py - local self-test for Collapse Attribution And Counterfactual
Fragility. Synthesises a tiny fake "raw" corpus (random images + scenes.csv +
blocks.csv in the exact format generate.py emits), runs prepare(), then checks
grade() on perfect / trivial baselines and strict edge cases, plus determinism
and no-leakage. Pure numpy/pandas/PIL - no PyBullet, no Blender.

Run:  python _sanity_smoke.py
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

import grade as G
from prepare import prepare

N_SCENES = 80
RNG = np.random.default_rng(20260613)


def _make_fake_raw(root: Path) -> None:
    img_dir = root / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    scenes = []
    blocks = []
    for i in range(N_SCENES):
        scene_hash = f"{i:08x}{RNG.integers(0, 1 << 28):07x}"
        n_blocks = int(RNG.integers(4, 8))
        # render a random RGB image (stand-in for the photoreal still)
        arr = RNG.integers(0, 256, size=(64, 64, 3), dtype=np.uint8)
        Image.fromarray(arr, "RGB").save(img_dir / f"{scene_hash}.png")

        will_collapse = int(RNG.integers(0, 2))
        if will_collapse:
            initiator = int(RNG.integers(0, n_blocks))
            keystone = int(RNG.integers(0, n_blocks))
            # second-best keystone, distinct, sometimes NONE
            alt = int(RNG.integers(0, n_blocks))
            if alt == keystone:
                alt = -1
        else:
            initiator = -1
            keystone = int(RNG.integers(0, n_blocks)) if RNG.random() < 0.5 else -1
            alt = -1
        scenes.append({
            "scene_hash": scene_hash,
            "n_blocks": n_blocks,
            "will_collapse": will_collapse,
            "initiator_block_id": initiator,
            "keystone_block_id": keystone,
            "keystone_alt_block_id": alt,
        })
        for b in range(n_blocks):
            blocks.append({
                "scene_hash": scene_hash,
                "block_id": b,
                "cx": int(RNG.integers(0, 256)),
                "cy": int(RNG.integers(0, 256)),
                "color_r": int(RNG.integers(0, 256)),
                "color_g": int(RNG.integers(0, 256)),
                "color_b": int(RNG.integers(0, 256)),
            })
    pd.DataFrame(scenes).to_csv(root / "scenes.csv", index=False)
    pd.DataFrame(blocks).to_csv(root / "blocks.csv", index=False)


def _perfect_submission(ans: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "id": ans["id"],
        "will_collapse": ans["will_collapse"].astype(float),
        "initiator_block_id": ans["initiator_block_id"].astype(str),
        "keystone_block_id": ans["keystone_block_id"].astype(str),
    })


def _const_submission(ans: pd.DataFrame, prob, init, key) -> pd.DataFrame:
    return pd.DataFrame({
        "id": ans["id"],
        "will_collapse": prob,
        "initiator_block_id": init,
        "keystone_block_id": key,
    })


def main() -> None:
    tmp = Path(tempfile.mkdtemp())
    try:
        raw = tmp / "raw"
        pub = tmp / "pub"
        priv = tmp / "priv"
        _make_fake_raw(raw)

        prepare(raw, pub, priv)
        ans = pd.read_csv(priv / "answers.csv")
        test_csv = pd.read_csv(pub / "test.csv")
        train_csv = pd.read_csv(pub / "train.csv")

        # ---- structure / no-leak checks ----
        assert set(["id", "image_path", "n_blocks"]) == set(test_csv.columns), test_csv.columns
        for leak in ("will_collapse", "initiator_block_id", "keystone_block_id"):
            assert leak not in test_csv.columns, f"LEAK: {leak} in test.csv"
        assert not (pub / "answers.csv").exists(), "answers leaked into public/"
        n_test = len(test_csv)
        assert len(ans) == n_test
        # every test image exists
        for r in test_csv["id"]:
            assert (pub / "test" / "images" / f"{int(r):06d}.jpg").exists()

        # ---- perfect ----
        s_perfect = G.grade(_perfect_submission(ans), ans)
        print(f"perfect score          = {s_perfect:.4f}  (expect ~1.00)")
        assert s_perfect > 0.999, s_perfect

        # ---- trivial baselines ----
        base_rate = float(ans["will_collapse"].mean())
        s_base = G.grade(_const_submission(ans, base_rate, "NONE", "NONE"), ans)
        print(f"base-rate+NONE score   = {s_base:.4f}  (expect < 0.15)")
        assert s_base < 0.20, s_base

        s_half = G.grade(_const_submission(ans, 0.5, "0", "0"), ans)
        print(f"0.5+block0 score       = {s_half:.4f}  (expect < 0.25)")
        assert s_half < 0.30, s_half

        # ---- malformed cell coercion (still scores, does not crash) ----
        bad = _perfect_submission(ans).copy()
        bad["will_collapse"] = bad["will_collapse"].astype(object)
        bad.loc[bad.index[0], "will_collapse"] = "garbage"
        bad.loc[bad.index[1], "will_collapse"] = 9.9
        bad["initiator_block_id"] = bad["initiator_block_id"].astype(object)
        bad.loc[bad.index[0], "initiator_block_id"] = "weird"
        s_bad = G.grade(bad, ans)
        print(f"coerced-cells score    = {s_bad:.4f}  (0 < s < 1, no crash)")
        assert 0.0 < s_bad < 1.0, s_bad

        # ---- strict structural failures -> 0.0 ----
        dup = _perfect_submission(ans)
        dup = pd.concat([dup, dup.iloc[[0]]], ignore_index=True)
        assert G.grade(dup, ans) == 0.0, "duplicate id must score 0"

        miss_col = _perfect_submission(ans).drop(columns=["keystone_block_id"])
        assert G.grade(miss_col, ans) == 0.0, "missing column must score 0"

        short = _perfect_submission(ans).iloc[:-1]
        assert G.grade(short, ans) == 0.0, "row-set mismatch must score 0"

        # ---- determinism ----
        pub2 = tmp / "pub2"
        priv2 = tmp / "priv2"
        prepare(raw, pub2, priv2)
        a1 = (priv / "answers.csv").read_bytes()
        a2 = (priv2 / "answers.csv").read_bytes()
        assert a1 == a2, "answers.csv not deterministic"
        t1 = (pub / "train.csv").read_bytes()
        t2 = (pub2 / "train.csv").read_bytes()
        assert t1 == t2, "train.csv not deterministic"
        im1 = (pub / "test" / "images" / f"{int(test_csv['id'].iloc[0]):06d}.jpg").read_bytes()
        im2 = (pub2 / "test" / "images" / f"{int(test_csv['id'].iloc[0]):06d}.jpg").read_bytes()
        assert im1 == im2, "image re-encode not deterministic"

        # ---- distributions ----
        print(f"collapse rate (test)   = {base_rate:.2f}")
        print(f"initiator dist (test)  = "
              f"{ans['initiator_block_id'].value_counts(normalize=True).round(2).to_dict()}")
        print(f"train scenes={len(train_csv)}  test scenes={n_test}")

        print("\nOK: smoke test passed.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
