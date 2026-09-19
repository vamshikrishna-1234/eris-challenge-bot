"""
prepare.py - Annotator Reliability And Adversarial Rater Detection

Pipeline (deterministic; ALL processing happens here):
  1. Discover the upstream PatchCamelyon Parquet shards in `raw/`.
     Auto-extract any *.zip at raw root if not yet expanded.
  2. Subsample 12,000 patches (8,000 train + 4,000 test) at the
     PCam-recommended 50/50 positive/negative balance per split.
  3. Downscale-then-upscale each patch and re-encode as a moderate-quality
     JPEG (q=75) so byte-hashing against the upstream archive does not
     recover the gold label.
  4. Generate 5 synthetic-rater predictions per row from FIVE FIXED,
     PRIVATE rater profiles (specialist / novice-recall / novice-prec /
     random / adversarial-confident). Per row, 5 raters are drawn from
     the non-adversarial pool, and in ~30% of rows one uniformly-chosen
     slot is overwritten with the adversarial profile.
  5. true_consensus = the upstream PCam binary label.
     true_rel_i      = the INTRINSIC reliability of rater i's profile (its
                       long-run probability of voting correctly), a value
                       in [0, 1]. This is a property of the rater profile,
                       NOT a function of this row's gold consensus, so the
                       reliability head cannot be derived from a consensus
                       guess plus the observable rater labels.
     true_adversarial_idx = which slot 1..5 (or "NONE") holds the
                           adversarial rater for this row.
  6. 5% of TRAIN rows have the consensus label flipped (irreducible
     error floor); test labels stay clean.

OUTPUT LAYOUT
-------------
    public/train/images/<id>.jpg          (96x96 RGB JPEG q75)
    public/test/images/<id>.jpg
    public/train.csv     id, image_path, rater_{1..5}_label,
                         rater_{1..5}_conf, true_consensus,
                         true_rel_{1..5} (float in [0,1]),
                         true_adversarial_idx
    public/test.csv      id, image_path, rater_{1..5}_label,
                         rater_{1..5}_conf
    public/sample_submission.csv  id, pred_consensus,
                                  pred_rel_{1..5}, pred_adversarial_idx
    private/answers.csv           id, true_consensus,
                                  true_rel_{1..5}, true_adversarial_idx

The `prepare(raw, public, private)` signature is the platform standard.
"""

from __future__ import annotations

import hashlib
import io
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

# -------- constants --------

N_TRAIN = 8000
N_TEST = 4000
PATCH_HW = 96
# Images are downscaled to DOWNSCALE_HW and re-upsampled to PATCH_HW before a
# moderate-quality JPEG re-encode. This irreversibly removes fine texture so the
# image-only consensus task cannot be solved at near-ceiling accuracy, keeping a
# meaningful human-agent gap on the consensus head.
DOWNSCALE_HW = 72
JPEG_Q = 75

N_RATERS = 5
ADVERSARIAL_FRACTION = 0.30
LABEL_NOISE_FRACTION = 0.05

SPLIT_SEED = 0xA7C3D4E5
TEST_SPLIT_SEED = 0xF2E1D0C9  # independent RNG for the test sub-sample
RATER_SEED = 0xB1C2D3E4
ADVERSARY_SEED = 0xC2D3E4F5
NOISE_SEED = 0xD3E4F506
SAMPLE_SEED = 0xE4F50617

# rater profile bias parameters — kept INTENTIONALLY private to this file.
# The non-adversarial pool is intentionally tuned so that majority-vote
# over 5 raters is only ~0.50 accurate; this forces solvers to use
# the image evidence to recover the gold consensus, breaking the
# closed-form "submit majority vote" shortcut.
PROFILE_BIASES = {
    "specialist":     {"acc": 0.62, "conf_mean": 0.78, "conf_jit": 0.05},
    "novice_recall":  {"acc_pos": 0.50, "acc_neg": 0.45, "conf_mean": 0.55, "conf_jit": 0.06},
    "novice_prec":    {"acc_pos": 0.45, "acc_neg": 0.50, "conf_mean": 0.55, "conf_jit": 0.06},
    "random":         {"acc": 0.50, "conf_mean": 0.50, "conf_jit": 0.06},
    # The adversarial rater is deliberately HARD to spot: its confidence band
    # overlaps the specialist's (mean 0.86 vs 0.78) and its accuracy (0.22) is
    # closer to chance than before, so the naive "flag the loud disagreer"
    # heuristic no longer isolates it cleanly. Telling it apart from an
    # honest-but-wrong specialist needs joint reasoning over the image and the
    # full rater pattern, yet remains learnable (well above random).
    "adversarial":    {"acc": 0.22, "conf_mean": 0.86, "conf_jit": 0.04},
}

NON_ADV_PROFILES = ["specialist", "novice_recall", "novice_prec", "random"]

# Intrinsic per-profile reliability = the rater's long-run probability of
# voting correctly (the marginal accuracy of the profile). This is the
# `true_rel_i` target. Crucially it depends ONLY on the rater's profile, NOT
# on whether the rater happened to be right on a particular row, so it cannot
# be reconstructed from (observable rater label) XOR (predicted consensus).
# Solvers must infer each rater's competence from the image, the confidence,
# and the cross-rater agreement pattern.
def _profile_reliability(profile: str) -> float:
    p = PROFILE_BIASES[profile]
    if "acc" in p:
        acc = p["acc"]
    else:
        acc = 0.5 * (p["acc_pos"] + p["acc_neg"])
    return round(float(acc), 4)


PROFILE_RELIABILITY = {prof: _profile_reliability(prof) for prof in PROFILE_BIASES}


def _extract_zips(raw: Path) -> None:
    for zf in sorted(raw.glob("*.zip")):
        with zipfile.ZipFile(zf, "r") as z:
            members = z.namelist()
        sentinel = raw / Path(members[0]).parts[0] if members else None
        if sentinel is not None and sentinel.exists():
            continue
        print(f"  [extract] {zf.name}")
        with zipfile.ZipFile(zf, "r") as z:
            z.extractall(raw)


def _find_parquet_shards(raw: Path) -> list[Path]:
    candidates: list[Path] = []
    for p in raw.rglob("*.parquet"):
        candidates.append(p)
    if not candidates:
        raise FileNotFoundError(
            f"No *.parquet shards found under {raw}. "
            "Expected upstream PatchCamelyon Parquet shards."
        )
    return sorted(candidates)


def _stable_rng(seed: int, key: int) -> np.random.Generator:
    """Deterministic, statistically-independent per-row stream.

    A SHA-256 digest of (seed, key) gives 32 bytes of high-quality entropy;
    feeding all 256 bits to ``np.random.SeedSequence`` yields well-separated,
    decorrelated streams for each (seed, key) pair - far safer than an ad-hoc
    64-bit XOR/multiply mix, which can leave low-order correlations between the
    per-row streams.
    """
    digest = hashlib.sha256(f"{int(seed)}:{int(key)}".encode("utf-8")).digest()
    seed_seq = np.random.SeedSequence(int.from_bytes(digest, "big"))
    return np.random.default_rng(seed_seq)


def _decode_image_bytes(rec) -> np.ndarray:
    """Parquet image cell is dict-like {bytes: ..., path: ...}."""
    if isinstance(rec, dict) and "bytes" in rec:
        b = rec["bytes"]
    elif isinstance(rec, (bytes, bytearray)):
        b = bytes(rec)
    elif hasattr(rec, "tobytes"):
        b = rec.tobytes()
    else:
        b = bytes(rec)
    img = Image.open(io.BytesIO(b)).convert("RGB")
    return np.asarray(img, dtype=np.uint8)


def _save_jpeg(arr: np.ndarray, dst: Path) -> None:
    """Downscale -> upscale -> moderate-quality JPEG. The round-trip discards
    high-frequency texture irreversibly, lowering the achievable image-only
    consensus accuracy and keeping a meaningful human-agent gap, without
    making the task pure noise."""
    img = Image.fromarray(arr, mode="RGB")
    if DOWNSCALE_HW < PATCH_HW:
        img = img.resize((DOWNSCALE_HW, DOWNSCALE_HW), resample=Image.BILINEAR)
        img = img.resize((PATCH_HW, PATCH_HW), resample=Image.BILINEAR)
    img.save(dst, format="JPEG", quality=JPEG_Q)


def _sample_balanced(
    df_label: np.ndarray, n_total: int, rng: np.random.Generator
) -> np.ndarray:
    """Return indices into df_label for a 50/50 balanced sub-sample."""
    n_each = n_total // 2
    pos_idx = np.where(df_label == True)[0]
    neg_idx = np.where(df_label == False)[0]
    if pos_idx.size < n_each or neg_idx.size < n_each:
        raise RuntimeError(
            f"Need {n_each} positives and {n_each} negatives; "
            f"got {pos_idx.size} pos / {neg_idx.size} neg."
        )
    pos_pick = rng.choice(pos_idx, size=n_each, replace=False)
    neg_pick = rng.choice(neg_idx, size=n_each, replace=False)
    out = np.concatenate([pos_pick, neg_pick])
    rng.shuffle(out)
    return out


def _draw_label_for_profile(
    profile: str, true_label: int, rng: np.random.Generator
) -> int:
    """Sample a rater label given the rater profile."""
    p = PROFILE_BIASES[profile]
    if profile in ("specialist", "random", "adversarial"):
        acc = p["acc"]
    else:
        acc = p["acc_pos"] if true_label == 1 else p["acc_neg"]
    return int(true_label if rng.random() < acc else 1 - true_label)


def _draw_conf_for_profile(profile: str, rng: np.random.Generator) -> float:
    p = PROFILE_BIASES[profile]
    c = float(p["conf_mean"] + rng.normal(0.0, p["conf_jit"]))
    return float(np.clip(c, 0.05, 0.99))


def _build_row_raters(
    true_label: int,
    rng_profile: np.random.Generator,
    rng_label: np.random.Generator,
    rng_conf: np.random.Generator,
) -> tuple[list[int], list[float], list[str], int]:
    """Sample 5 raters for one row.

    Returns:
        labels: list of 5 binary rater labels in {0, 1}
        confs:  list of 5 confidences in [0.05, 0.99]
        profiles: list of 5 profile names (private; not exposed)
        adv_idx: 1..5 if adversarial slot present, 0 if NONE
    """
    # Draw a full roster of N_RATERS non-adversarial profiles, then (in
    # ADVERSARIAL_FRACTION of rows) overwrite ONE uniformly-chosen slot with
    # the adversarial profile. This keeps the adversarial slot exactly uniform
    # over 1..N_RATERS and the surviving non-adversarial picks unbiased - no
    # insert/pop length juggling that could skew which slot is dropped.
    profiles = rng_profile.choice(NON_ADV_PROFILES, size=N_RATERS, replace=True).tolist()
    if rng_profile.random() < ADVERSARIAL_FRACTION:
        adv_slot_0idx = int(rng_profile.integers(0, N_RATERS))
        profiles[adv_slot_0idx] = "adversarial"
        adv_idx_1based = adv_slot_0idx + 1
    else:
        adv_idx_1based = 0

    labels: list[int] = []
    confs: list[float] = []
    for prof in profiles:
        labels.append(_draw_label_for_profile(prof, true_label, rng_label))
        confs.append(_draw_conf_for_profile(prof, rng_conf))
    return labels, confs, profiles, adv_idx_1based


def _materialise_split(
    df_subset: pd.DataFrame,
    out_img_dir: Path,
    id_offset: int,
    is_train: bool,
    rng_label_noise: np.random.Generator,
) -> tuple[list[dict], list[dict]]:
    """Iterate one balanced subset, save images, build CSV row dicts.

    Returns (rows_for_csv_full, rows_for_answers_or_test_only).
    """
    out_img_dir.mkdir(parents=True, exist_ok=True)
    rows_full: list[dict] = []
    answers_or_blank: list[dict] = []

    for local_i, (_, src) in enumerate(df_subset.iterrows()):
        rid = id_offset + local_i
        true_label = int(bool(src["label"]))
        arr = _decode_image_bytes(src["image"])
        if arr.shape != (PATCH_HW, PATCH_HW, 3):
            arr = np.asarray(
                Image.fromarray(arr, mode="RGB").resize((PATCH_HW, PATCH_HW), resample=Image.BILINEAR),
                dtype=np.uint8,
            )

        img_name = f"{rid:06d}.jpg"
        img_rel = f"images/{img_name}"
        _save_jpeg(arr, out_img_dir / img_name)

        rng_p = _stable_rng(RATER_SEED, rid)
        rng_l = _stable_rng(RATER_SEED ^ 0x1111, rid)
        rng_c = _stable_rng(RATER_SEED ^ 0x2222, rid)
        labels, confs, profiles, adv_1 = _build_row_raters(true_label, rng_p, rng_l, rng_c)

        # Reliability target is the rater's INTRINSIC profile reliability,
        # independent of this row's gold consensus (see PROFILE_RELIABILITY).
        true_rels = [PROFILE_RELIABILITY[p] for p in profiles]
        adv_str = "NONE" if adv_1 == 0 else str(adv_1)

        train_consensus = true_label
        if is_train and rng_label_noise.random() < LABEL_NOISE_FRACTION:
            train_consensus = 1 - train_consensus

        full = {
            "id": rid,
            "image_path": img_rel,
        }
        for k in range(N_RATERS):
            full[f"rater_{k+1}_label"] = int(labels[k])
            full[f"rater_{k+1}_conf"] = float(confs[k])
        if is_train:
            full["true_consensus"] = int(train_consensus)
            for k in range(N_RATERS):
                full[f"true_rel_{k+1}"] = float(true_rels[k])
            full["true_adversarial_idx"] = adv_str

        rows_full.append(full)

        if not is_train:
            ans_row = {
                "id": rid,
                "true_consensus": int(true_label),
                "true_adversarial_idx": adv_str,
            }
            for k in range(N_RATERS):
                ans_row[f"true_rel_{k+1}"] = float(true_rels[k])
            answers_or_blank.append(ans_row)
    return rows_full, answers_or_blank


def prepare(raw: Path, public: Path, private: Path) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    _extract_zips(raw)
    shards = _find_parquet_shards(raw)
    print(f"  [discover] {len(shards)} parquet shards under {raw}")

    train_shards = [p for p in shards if "train" in p.name.lower()]
    test_shards = [p for p in shards if "test" in p.name.lower()]
    valid_shards = [p for p in shards if "valid" in p.name.lower()]
    if not train_shards or not test_shards:
        train_shards = shards[: max(1, len(shards) // 2)]
        test_shards = shards[max(1, len(shards) // 2):]

    print(f"  [load] reading {len(train_shards)} train shards for the train pool")
    train_df = pd.concat([pd.read_parquet(p) for p in train_shards], ignore_index=True)
    test_pool_shards = test_shards if test_shards else valid_shards
    print(f"  [load] reading {len(test_pool_shards)} test/valid shards for the test pool")
    test_df = pd.concat([pd.read_parquet(p) for p in test_pool_shards], ignore_index=True)

    # Independent RNG streams for the train and test sub-samples so the test
    # split does not inherit (and depend on) the train split's RNG state.
    rng_split_train = np.random.default_rng(SPLIT_SEED)
    rng_split_test = np.random.default_rng(TEST_SPLIT_SEED)
    train_pick = _sample_balanced(train_df["label"].to_numpy(), N_TRAIN, rng_split_train)
    test_pick = _sample_balanced(test_df["label"].to_numpy(), N_TEST, rng_split_test)

    train_subset = train_df.iloc[train_pick].reset_index(drop=True)
    test_subset = test_df.iloc[test_pick].reset_index(drop=True)

    train_dir = public / "train"
    test_dir = public / "test"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    rng_noise = np.random.default_rng(NOISE_SEED)
    print(f"  [materialise] writing {N_TRAIN} train images")
    train_rows, _ = _materialise_split(
        train_subset, train_dir / "images", id_offset=0,
        is_train=True, rng_label_noise=rng_noise,
    )
    print(f"  [materialise] writing {N_TEST} test images")
    test_rows, ans_rows = _materialise_split(
        test_subset, test_dir / "images", id_offset=N_TRAIN,
        is_train=False, rng_label_noise=rng_noise,
    )

    train_cols = ["id", "image_path"]
    for k in range(N_RATERS):
        train_cols.append(f"rater_{k+1}_label")
        train_cols.append(f"rater_{k+1}_conf")
    train_cols.append("true_consensus")
    for k in range(N_RATERS):
        train_cols.append(f"true_rel_{k+1}")
    train_cols.append("true_adversarial_idx")
    train_csv = pd.DataFrame(train_rows)[train_cols]
    train_csv.to_csv(public / "train.csv", index=False)

    test_cols = ["id", "image_path"]
    for k in range(N_RATERS):
        test_cols.append(f"rater_{k+1}_label")
        test_cols.append(f"rater_{k+1}_conf")
    test_csv = pd.DataFrame(test_rows)[test_cols]
    test_csv.to_csv(public / "test.csv", index=False)

    sample_rows = []
    for row in test_rows:
        sub = {
            "id": row["id"],
            "pred_consensus": 0,
        }
        for k in range(N_RATERS):
            sub[f"pred_rel_{k+1}"] = 0.5
        sub["pred_adversarial_idx"] = "NONE"
        sample_rows.append(sub)
    sample_cols = ["id", "pred_consensus"] + [f"pred_rel_{k+1}" for k in range(N_RATERS)] + ["pred_adversarial_idx"]
    pd.DataFrame(sample_rows)[sample_cols].to_csv(public / "sample_submission.csv", index=False)

    ans_cols = ["id", "true_consensus"] + [f"true_rel_{k+1}" for k in range(N_RATERS)] + ["true_adversarial_idx"]
    pd.DataFrame(ans_rows)[ans_cols].to_csv(private / "answers.csv", index=False)

    print(f"  [done] {N_TRAIN} train rows, {N_TEST} test rows.")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")
