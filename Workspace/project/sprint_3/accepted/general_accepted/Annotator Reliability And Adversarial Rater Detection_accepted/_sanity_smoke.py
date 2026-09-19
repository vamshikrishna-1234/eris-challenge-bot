"""Smoke test: synthesise a tiny PCam-like Parquet shard, run prepare(),
verify grade() against perfect / random / various baselines.

Not shipped to the platform; for organiser-side validation only.
"""

from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import grade as G  # noqa: E402
import prepare as P  # noqa: E402


def _make_fake_parquet(out_dir: Path, n: int, name: str, seed: int) -> None:
    """Synthesise a Parquet shard with the upstream PCam schema."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        # generate a 96x96 noise patch, encode as PNG inside the dict cell
        arr = rng.integers(20, 240, size=(96, 96, 3), dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(arr, mode="RGB").save(buf, format="PNG")
        rows.append({
            "image": {"bytes": buf.getvalue(), "path": None},
            "label": bool(i % 2 == 0),
        })
    pd.DataFrame(rows).to_parquet(out_dir / name, index=False)


def _build_perfect_submission(answers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in answers.iterrows():
        sub = {"id": int(r["id"]), "pred_consensus": int(r["true_consensus"])}
        for k in range(G.N_RATERS):
            sub[f"pred_rel_{k+1}"] = float(r[f"true_rel_{k+1}"])
        sub["pred_adversarial_idx"] = str(r["true_adversarial_idx"])
        rows.append(sub)
    return pd.DataFrame(rows)


def _build_random_submission(answers: pd.DataFrame, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    adv_choices = ["1", "2", "3", "4", "5", "NONE"]
    for _, r in answers.iterrows():
        sub = {"id": int(r["id"]), "pred_consensus": int(rng.integers(0, 2))}
        for k in range(G.N_RATERS):
            sub[f"pred_rel_{k+1}"] = float(rng.random())
        sub["pred_adversarial_idx"] = str(rng.choice(adv_choices))
        rows.append(sub)
    return pd.DataFrame(rows)


def _build_constant_submission(
    answers: pd.DataFrame, c: int, rel: float, adv: str
) -> pd.DataFrame:
    rows = []
    for _, r in answers.iterrows():
        sub = {"id": int(r["id"]), "pred_consensus": int(c)}
        for k in range(G.N_RATERS):
            sub[f"pred_rel_{k+1}"] = float(rel)
        sub["pred_adversarial_idx"] = str(adv)
        rows.append(sub)
    return pd.DataFrame(rows)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        raw = td / "raw"
        pub = td / "public"
        priv = td / "private"

        _make_fake_parquet(raw, n=2400, name="train-00000-of-00001-fake.parquet", seed=11)
        _make_fake_parquet(raw, n=600, name="test-00000-of-00001-fake.parquet", seed=22)

        # shrink prepare's targets so the smoke test fits the fake corpus
        P.N_TRAIN = 200
        P.N_TEST = 100

        P.prepare(raw, pub, priv)

        ans = pd.read_csv(priv / "answers.csv")
        n_test = len(ans)
        print(f"prepared: {n_test} test rows")

        perfect = _build_perfect_submission(ans)
        s_perfect = G.grade(perfect, ans)
        print(f"perfect score        = {s_perfect:.4f}  (expect ~1.00)")
        assert s_perfect > 0.99, f"perfect should score ~1.0, got {s_perfect}"

        rnd = _build_random_submission(ans, seed=7)
        s_rnd = G.grade(rnd, ans)
        print(f"random score         = {s_rnd:.4f}  (expect <0.15 after squaring)")

        all05 = _build_constant_submission(ans, c=0, rel=0.5, adv="NONE")
        s_all05 = G.grade(all05, ans)
        print(f"all-0+0.5+NONE score = {s_all05:.4f}  (expect <0.15 after squaring)")

        all_ones = _build_constant_submission(ans, c=1, rel=1.0, adv="NONE")
        s_all1 = G.grade(all_ones, ans)
        print(f"all-1+1.0+NONE score = {s_all1:.4f}  (expect <0.15 after squaring)")

        dup = pd.concat([perfect, perfect.head(1)], ignore_index=True)
        s_dup = G.grade(dup, ans)
        print(f"duplicate-id score   = {s_dup:.4f}  (expect 0.00)")
        assert s_dup == 0.0, f"duplicate should score 0.0, got {s_dup}"

        bad = perfect.drop(columns=["pred_rel_1"])
        s_bad = G.grade(bad, ans)
        print(f"missing-col score    = {s_bad:.4f}  (expect 0.00)")
        assert s_bad == 0.0, f"missing-col should score 0.0, got {s_bad}"

        short = perfect.iloc[:-3].copy()
        s_short = G.grade(short, ans)
        print(f"short-set score      = {s_short:.4f}  (expect 0.00)")
        assert s_short == 0.0, f"row-set mismatch should score 0.0, got {s_short}"

        ans_check = pd.read_csv(priv / "answers.csv")
        train_check = pd.read_csv(pub / "train.csv")
        train_ids = set(train_check["id"].tolist())
        test_ids = set(ans_check["id"].tolist())
        assert train_ids.isdisjoint(test_ids), "DATA LEAKAGE: train/test id overlap"

        for csv in [pub / "train.csv", pub / "test.csv"]:
            df = pd.read_csv(csv)
            assert df.isnull().sum().sum() == 0, f"NULL in {csv.name}"

        adv_dist = ans_check["true_adversarial_idx"].value_counts(normalize=True)
        print(f"adversarial distribution: {adv_dist.to_dict()}")
        adv_present_frac = 1.0 - float(adv_dist.get("NONE", 0.0))
        assert 0.20 < adv_present_frac < 0.40, f"adv frac off: {adv_present_frac}"

        cons_dist = ans_check["true_consensus"].value_counts(normalize=True)
        print(f"consensus distribution: {cons_dist.to_dict()}")
        assert 0.40 < cons_dist.get(0, 0) < 0.60, "consensus not balanced"

        assert s_rnd < 0.35, f"random unexpected: {s_rnd}"
        assert s_all05 < 0.30, f"all-0.5 floor too high: {s_all05}"
        assert s_all1 < 0.30, f"all-1.0 floor too high: {s_all1}"

        print("\nOK: smoke test passed.")


if __name__ == "__main__":
    main()
