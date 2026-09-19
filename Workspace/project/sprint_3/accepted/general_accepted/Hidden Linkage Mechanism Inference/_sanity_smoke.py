"""Self-contained smoke test for the COGCHAIN challenge pipeline.

Builds a tiny real raw corpus with generate.py, runs prepare(), then checks
grade() on perfect / baseline / malformed / structural-edge submissions plus a
determinism check. Run:  python _sanity_smoke.py
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pandas as pd

import generate as gen
import prepare as prep
from grade import grade


def _build_raw(raw: Path, n_base: int, seed: int, w: int, h: int) -> None:
    vid_dir = raw / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for base_idx in range(n_base):
        rng = gen._rng(seed, base_idx)
        scene = gen._sample_scene(rng, base_idx)
        for row in gen._variant_rows(scene, seed, True):
            frames = gen._render_clip(row["_scene"], row["_style_key"],
                                      row["_mirror"], w, h)
            gen._encode_mp4(str(vid_dir / f"{row['scene_hash']}.mp4"), frames, gen.FPS)
            clean = {k: v for k, v in row.items() if not k.startswith("_")}
            clean["video"] = f"videos/{row['scene_hash']}.mp4"
            rows.append(clean)
    cols = ["scene_hash", "video", "base_scenario_id", "variant", "num_rotors",
            "rotors", "topology_family", "board_style", "edges_json",
            "moving_at_end_json", "first_mover"]
    pd.DataFrame(rows)[cols].to_csv(raw / "scenes.csv", index=False)


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="cogchain_smoke_"))
    try:
        raw = tmp / "raw"; pub = tmp / "pub"; priv = tmp / "priv"
        _build_raw(raw, n_base=12, seed=23, w=256, h=160)
        prep.prepare(raw, pub, priv)

        ans = pd.read_csv(priv / "answers.csv")
        sample = pd.read_csv(pub / "sample_submission.csv")
        sub_cols = ["id", "edges_json", "moving_at_end_json", "first_mover", "confidence"]

        # perfect submission (confidence == correctness == 1.0)
        perfect = ans[["id", "edges_json", "moving_at_end_json", "first_mover"]].copy()
        perfect["confidence"] = 1.0
        s_perfect = grade(perfect[sub_cols], ans)

        # shipped baseline placeholders (empty edges, nothing moving)
        s_base = grade(sample.copy(), ans)

        # malformed edges cells (valid confidence): must degrade, not crash
        bad = perfect.copy()
        bad["edges_json"] = bad["edges_json"].astype(object)
        bad.loc[bad.index[:3], "edges_json"] = "not-json"
        s_bad = grade(bad[sub_cols], ans)

        # invalid confidence -> hard 0.0 (intended)
        badconf = perfect.copy()
        badconf["confidence"] = badconf["confidence"].astype(object)
        badconf.loc[badconf.index[:1], "confidence"] = "abc"
        s_badconf = grade(badconf[sub_cols], ans)

        # structural failures -> 0.0
        dup = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
        s_dup = grade(dup[sub_cols], ans)
        miss = perfect.drop(columns=["edges_json"])
        s_miss = grade(miss, ans)
        mismatch = perfect.iloc[:-1].copy()
        s_mismatch = grade(mismatch[sub_cols], ans)

        # "onset-order" trap baseline: guesses no edges but gets first_mover and
        # moving_at_end from the truth -> shows edges carry the headroom.
        trap = perfect.copy()
        trap["edges_json"] = "[]"
        s_trap = grade(trap[sub_cols], ans)

        # determinism
        priv2 = tmp / "priv2"
        prep.prepare(raw, tmp / "pub2", priv2)
        ans2 = pd.read_csv(priv2 / "answers.csv")
        deterministic = ans.equals(ans2)

        n_tot = len(ans)
        print(f"perfect score        = {s_perfect:.4f}  (expect ~1.00)")
        print(f"baseline score       = {s_base:.4f}  (expect < 0.50)")
        print(f"no-edges trap score  = {s_trap:.4f}  (edges headroom -> < perfect)")
        print(f"malformed-edge score = {s_bad:.4f}  (0 < s < 1, no crash)")
        print(f"bad-confidence score = {s_badconf:.4f}  (expect 0.0)")
        print(f"duplicate-id score   = {s_dup:.4f}  (expect 0.0)")
        print(f"missing-col score    = {s_miss:.4f}  (expect 0.0)")
        print(f"row-mismatch score   = {s_mismatch:.4f}  (expect 0.0)")
        print(f"prepare deterministic= {deterministic}")
        print(f"answers: {n_tot} test clips")
        print(f"split: train={len(pd.read_csv(pub/'train.csv'))} test={len(pd.read_csv(pub/'test.csv'))}")

        assert s_perfect > 0.98, "perfect should score ~1.0"
        assert s_base < 0.55, "baseline should leave headroom"
        assert s_trap < s_perfect - 0.1, "edges must carry meaningful headroom"
        assert 0.0 < s_bad < 1.0, "malformed edges should degrade, not crash/zero"
        assert s_badconf == 0.0, "invalid confidence must hard-fail"
        assert s_dup == 0.0 and s_miss == 0.0 and s_mismatch == 0.0, "structural -> 0.0"
        assert deterministic, "prepare must be deterministic"
        print("\nOK: smoke test passed.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
