"""End-to-end smoke test for PANEL (generate -> prepare -> grade).

Asserts: perfect ~1.0, baseline < 0.5, malformed / bad-confidence / duplicate-id
/ missing-col / row-mismatch all -> 0.0, and prepare is deterministic.
Run:  python _sanity_smoke.py
"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pandas as pd

import generate as gen
import prepare as prep
from grade import grade


def _build_raw(raw: Path, n: int, seed: int, w: int, h: int) -> None:
    import imageio.v3 as iio
    vdir = raw / "videos"
    vdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for idx in range(n):
        sc, clip = gen._gen_scene(idx, seed, w, h)
        sh = gen._scene_hash(seed, idx)
        iio.imwrite(vdir / f"{sh}.mp4", clip, fps=gen.FPS, codec="libx264", quality=7,
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
    pd.DataFrame(rows).to_csv(raw / "scenes.csv", index=False)


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="panel_smoke_"))
    try:
        raw, pub, priv = tmp / "raw", tmp / "pub", tmp / "priv"
        _build_raw(raw, n=44, seed=59, w=160, h=110)
        prep.prepare(raw, pub, priv)

        ans = pd.read_csv(priv / "answers.csv")
        sample = pd.read_csv(pub / "sample_submission.csv")

        perfect = ans[["id", "wiring_json", "query_pattern"]].copy()
        perfect["confidence"] = 1.0
        s_perfect = grade(perfect, ans)
        s_base = grade(sample.copy(), ans)

        badc = perfect.copy(); badc["confidence"] = 2.0
        s_badc = grade(badc, ans)
        badjson = perfect.copy()
        badjson.loc[badjson.index[0], "wiring_json"] = "{" * 5000
        s_badjson = grade(badjson, ans)
        dup = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
        s_dup = grade(dup, ans)
        miss = perfect.drop(columns=["query_pattern"])
        s_miss = grade(miss, ans)
        mismatch = perfect.iloc[:-1].copy()
        s_mismatch = grade(mismatch, ans)

        prep.prepare(raw, tmp / "pub2", tmp / "priv2")
        ans2 = pd.read_csv(tmp / "priv2" / "answers.csv")
        deterministic = ans.equals(ans2)

        print(f"perfect           = {s_perfect:.4f}  (expect ~1.00)")
        print(f"baseline          = {s_base:.4f}  (expect < 0.50)")
        print(f"bad-confidence    = {s_badc:.4f}  (expect 0.0)")
        print(f"oversized-json    = {s_badjson:.4f}  (expect 0.0)")
        print(f"duplicate-id      = {s_dup:.4f}  (expect 0.0)")
        print(f"missing-col       = {s_miss:.4f}  (expect 0.0)")
        print(f"row-mismatch      = {s_mismatch:.4f}  (expect 0.0)")
        print(f"deterministic     = {deterministic}")

        assert s_perfect > 0.98, "perfect should be ~1.0"
        assert s_base < 0.50, "baseline should be < 0.5"
        assert s_badc == 0.0 and s_badjson == 0.0, "strict checks -> 0.0"
        assert s_dup == 0.0 and s_miss == 0.0 and s_mismatch == 0.0, "structural -> 0.0"
        assert deterministic, "prepare must be deterministic"
        print("\nOK: smoke test passed.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
