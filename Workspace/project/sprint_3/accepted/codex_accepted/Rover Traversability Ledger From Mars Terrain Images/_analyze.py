from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageOps

from grade import SUBMISSION_COLUMNS, grade
from prepare import (
    MASK_SIZE,
    ROUTE_CLASSES,
    _pair_records,
    _public_id,
    _sequence_family,
    _source_root,
    decode_mask,
    derive_ledger,
)


ROOT = Path(__file__).resolve().parent


def _cell_mode(rows: pd.Series) -> np.ndarray:
    stack = np.stack([decode_mask(value) for value in rows], axis=0)
    classes = np.asarray([0, 1, 2, 3, 255], dtype=np.uint8)
    counts = np.stack([(stack == value).sum(axis=0) for value in classes], axis=0)
    return classes[np.argmax(counts, axis=0)]


def _encode(mask: np.ndarray) -> str:
    from prepare import encode_mask

    return encode_mask(mask)


def _metadata_baseline(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, test_row in test.iterrows():
        group = train[train["mission"] == test_row["mission"]]
        if len(group) < 10:
            group = train
        mask = _cell_mode(group["terrain_mask_rle"])
        route_class = str(group["route_safety_class"].mode().iloc[0])
        rows.append(
            {
                "id": test_row["id"],
                "terrain_mask_rle": _encode(mask),
                "hazard_boxes_json": "[]",
                "route_safety_class": route_class,
                "clearance_score": float(group["clearance_score"].median()),
                "obstacle_coverage": float(group["obstacle_coverage"].median()),
                "safe_corridor_width": float(group["safe_corridor_width"].median()),
                "uncertainty_score": float(group["uncertainty_score"].median()),
            }
        )
    return pd.DataFrame(rows)[SUBMISSION_COLUMNS]


def _thumb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("L").resize((16, 16), Image.Resampling.BILINEAR), dtype=np.float32)
    arr = arr.reshape(-1) / 255.0
    return (arr - arr.mean()) / (arr.std() + 1e-5)


def _image_knn_baseline(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame:
    train_x = np.stack([_thumb(public / value) for value in train["image"]])
    train_masks = [decode_mask(value) for value in train["terrain_mask_rle"]]
    rows = []
    for _, test_row in test.iterrows():
        feature = _thumb(public / test_row["image"])
        distances = np.mean((train_x - feature[None, :]) ** 2, axis=1)
        neighbors = np.argsort(distances)[:3]
        stack = np.stack([train_masks[int(index)] for index in neighbors])
        classes = np.asarray([0, 1, 2, 3, 255], dtype=np.uint8)
        counts = np.stack([(stack == value).sum(axis=0) for value in classes], axis=0)
        mask = classes[np.argmax(counts, axis=0)]
        route = json.loads(test_row["route_query_json"])
        ledger = derive_ledger(mask, route)
        rows.append({"id": test_row["id"], "terrain_mask_rle": _encode(mask), **ledger})
    return pd.DataFrame(rows)[SUBMISSION_COLUMNS]


def _file_size_knn_baseline(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame:
    train_sizes = np.asarray([(public / value).stat().st_size for value in train["image"]], dtype=np.float64)
    rows = []
    for _, test_row in test.iterrows():
        size = float((public / test_row["image"]).stat().st_size)
        neighbor = int(np.argmin(np.abs(train_sizes - size)))
        source = train.iloc[neighbor]
        mask = decode_mask(source["terrain_mask_rle"])
        route = json.loads(test_row["route_query_json"])
        ledger = derive_ledger(mask, route)
        rows.append({"id": test_row["id"], "terrain_mask_rle": _encode(mask), **ledger})
    return pd.DataFrame(rows)[SUBMISSION_COLUMNS]


def _id_prefix_baseline(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    global_mask = _cell_mode(train["terrain_mask_rle"])
    global_route = str(train["route_safety_class"].mode().iloc[0])
    numeric_cols = ["clearance_score", "obstacle_coverage", "safe_corridor_width", "uncertainty_score"]
    global_numbers = {col: float(train[col].median()) for col in numeric_cols}
    rows = []
    for _, test_row in test.iterrows():
        prefix = str(test_row["id"])[4]
        group = train[train["id"].str[4] == prefix]
        if len(group) >= 10:
            mask = _cell_mode(group["terrain_mask_rle"])
            route_class = str(group["route_safety_class"].mode().iloc[0])
            numbers = {col: float(group[col].median()) for col in numeric_cols}
        else:
            mask = global_mask
            route_class = global_route
            numbers = global_numbers
        rows.append(
            {
                "id": test_row["id"],
                "terrain_mask_rle": _encode(mask),
                "hazard_boxes_json": "[]",
                "route_safety_class": route_class,
                **numbers,
            }
        )
    return pd.DataFrame(rows)[SUBMISSION_COLUMNS]


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _hash_size_probe(
    train: pd.DataFrame, test: pd.DataFrame, public: Path, raw: Path
) -> dict[str, int]:
    records = _pair_records(_source_root(raw))
    raw_paths = [Path(record["image"]) for record in records]
    public_paths = [public / value for value in pd.concat([train["image"], test["image"]])]
    raw_hashes = {_sha256(path) for path in raw_paths}
    exact_hash_hits = sum(_sha256(path) in raw_hashes for path in public_paths)

    raw_sizes: dict[int, list[Path]] = {}
    for path in raw_paths:
        raw_sizes.setdefault(path.stat().st_size, []).append(path)
    public_size_hits = sum((path.stat().st_size in raw_sizes) for path in public_paths)

    id_to_raw_path = {_public_id(str(record["stem"])): Path(record["image"]) for record in records}
    test_size_unique_true = 0
    for _, row in test.iterrows():
        candidates = raw_sizes.get((public / row["image"]).stat().st_size, [])
        if len(candidates) == 1 and candidates[0] == id_to_raw_path[str(row["id"])]:
            test_size_unique_true += 1
    return {
        "exact_public_image_sha256_hits_in_raw_images": int(exact_hash_hits),
        "public_jpeg_size_values_matching_any_raw_image_size": int(public_size_hits),
        "test_rows_uniquely_true_by_raw_file_size": int(test_size_unique_true),
    }


def _id_order_probe(train: pd.DataFrame, test: pd.DataFrame) -> dict[str, int | bool]:
    ids = pd.concat([train["id"], test["id"]]).tolist()
    format_ok = all(re.fullmatch(r"rvr_[0-9a-f]{14}", value) for value in ids)
    ordered = sorted([(value, "train") for value in train["id"]] + [(value, "test") for value in test["id"]])
    labels = [label for _, label in ordered]
    longest_run = 1
    current_run = 1
    for left, right in zip(labels, labels[1:]):
        if left == right:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 1
    return {
        "format_ok": bool(format_ok),
        "train_test_overlap": int(len(set(train["id"]) & set(test["id"]))),
        "first_test_rank_in_sorted_ids": int(next(i for i, label in enumerate(labels) if label == "test")),
        "last_train_rank_in_sorted_ids": int(max(i for i, label in enumerate(labels) if label == "train")),
        "longest_same_split_run_sorted_ids": int(longest_run),
    }


def _retrieval_probe(
    train: pd.DataFrame, test: pd.DataFrame, public: Path, raw: Path
) -> tuple[float, float, float]:
    records = _pair_records(_source_root(raw))

    def feature(path: Path) -> np.ndarray:
        with Image.open(path) as image:
            image = ImageOps.equalize(image.convert("L"))
            array = np.asarray(image.resize((32, 32), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
        array = (array - array.mean()) / (array.std() + 1e-5)
        return array

    raw_ids: list[str] = []
    raw_features: list[np.ndarray] = []
    raw_flips: list[np.ndarray] = []
    id_to_group: dict[str, str] = {}
    for record in records:
        rid = _public_id(str(record["stem"]))
        array = feature(Path(record["image"]))
        raw_ids.append(rid)
        raw_features.append(array.reshape(-1))
        raw_flips.append(np.fliplr(array).reshape(-1))
        id_to_group[rid] = _sequence_family(str(record["stem"]), str(record["mission"]))
    raw_matrix = np.stack(raw_features)
    flip_matrix = np.stack(raw_flips)
    id_index = {rid: index for index, rid in enumerate(raw_ids)}
    ranks: list[int] = []
    for _, row in test.iterrows():
        query = feature(public / row["image"]).reshape(-1)
        distances = np.minimum(
            np.mean((raw_matrix - query[None, :]) ** 2, axis=1),
            np.mean((flip_matrix - query[None, :]) ** 2, axis=1),
        )
        order = np.argsort(distances)
        ranks.append(int(np.where(order == id_index[str(row["id"])])[0][0]) + 1)
    train_groups = {id_to_group[str(rid)] for rid in train["id"]}
    test_groups = {id_to_group[str(rid)] for rid in test["id"]}
    assert train_groups.isdisjoint(test_groups)
    rank_array = np.asarray(ranks)
    return (
        float(np.mean(rank_array == 1)),
        float(np.mean(rank_array <= 5)),
        float(np.median(rank_array)),
    )


def _multicrop_retrieval_probe(
    test: pd.DataFrame, public: Path, raw: Path
) -> tuple[float, float, float, float, int]:
    """Approximate a stronger public-source crop lookup attack.

    The exact source filename is hidden, so this probes whether a participant
    could still recover it by comparing each prepared test image against many
    normalized crops and mirrored crops from every official AI4MARS source
    image.  It is deliberately simple enough for local audit, but much closer
    to the actual lookup threat than a whole-image thumbnail hash.
    """

    records = _pair_records(_source_root(raw))
    feature_size = 24
    scales = [0.24, 0.30, 0.36, 0.42, 0.50, 0.60, 0.75, 1.00]
    positions = [0.0, 0.25, 0.50, 0.75, 1.0]

    def feature(image: Image.Image) -> np.ndarray:
        small = ImageOps.equalize(image.convert("L")).resize(
            (feature_size, feature_size), Image.Resampling.BILINEAR
        )
        array = np.asarray(small, dtype=np.float32) / 255.0
        array = (array - array.mean()) / (array.std() + 1e-5)
        flat = array.reshape(-1).astype(np.float32)
        flat /= np.linalg.norm(flat) + 1e-6
        return flat

    raw_ids: list[str] = []
    features: list[np.ndarray] = []
    source_indices: list[int] = []
    for source_index, record in enumerate(records):
        raw_ids.append(_public_id(str(record["stem"])))
        with Image.open(record["image"]) as raw_image:
            raw_image = raw_image.convert("L")
            width, height = raw_image.size
            base = min(width, height)
            seen: set[tuple[int, int, int]] = set()
            for scale in scales:
                side = max(64, min(base, int(round(base * scale))))
                max_x = max(0, width - side)
                max_y = max(0, height - side)
                for px in positions:
                    for py in positions:
                        x0 = int(round(max_x * px))
                        y0 = int(round(max_y * py))
                        key = (x0, y0, side)
                        if key in seen:
                            continue
                        seen.add(key)
                        crop = raw_image.crop((x0, y0, x0 + side, y0 + side))
                        crop_feature = feature(crop)
                        features.append(crop_feature)
                        source_indices.append(source_index)
                        flipped = np.fliplr(crop_feature.reshape(feature_size, feature_size))
                        features.append(flipped.reshape(-1).astype(np.float32))
                        source_indices.append(source_index)

    candidate_matrix = np.stack(features).astype(np.float32)
    source_index_array = np.asarray(source_indices, dtype=np.int32)
    id_to_source_index = {rid: index for index, rid in enumerate(raw_ids)}
    ranks: list[int] = []
    for _, row in test.iterrows():
        with Image.open(public / row["image"]) as public_image:
            query = feature(public_image)
        scores = candidate_matrix @ query
        best_by_source = np.full(len(raw_ids), -np.inf, dtype=np.float32)
        np.maximum.at(best_by_source, source_index_array, scores)
        order = np.argsort(-best_by_source)
        ranks.append(int(np.where(order == id_to_source_index[str(row["id"])])[0][0]) + 1)

    rank_array = np.asarray(ranks)
    return (
        float(np.mean(rank_array == 1)),
        float(np.mean(rank_array <= 5)),
        float(np.mean(rank_array <= 10)),
        float(np.median(rank_array)),
        int(len(features)),
    )


def main() -> None:
    public = ROOT / "public"
    private = ROOT / "private"
    train = pd.read_csv(public / "train.csv", dtype={"id": str})
    test = pd.read_csv(public / "test.csv", dtype={"id": str})
    answers = pd.read_csv(private / "answers.csv", dtype={"id": str})
    sample = pd.read_csv(public / "sample_submission.csv", dtype={"id": str})

    assert not train.isna().any().any() and not test.isna().any().any() and not answers.isna().any().any()
    assert set(train["id"]).isdisjoint(test["id"])
    assert set(test["id"]) == set(answers["id"])
    assert set(train["route_safety_class"]).issubset(ROUTE_CLASSES)
    assert all(re.fullmatch(r"rvr_[0-9a-f]{14}", value) for value in pd.concat([train["id"], test["id"]]))
    leak_pattern = re.compile(r"(?:NLA_|NLB_|NRB_|_merged|EDR_F|_T0_)", re.IGNORECASE)
    for frame in [train, test]:
        assert not frame.astype(str).apply(lambda col: col.str.contains(leak_pattern).any()).any()
        for image_rel in frame["image"]:
            path = public / image_rel
            assert path.is_file(), path
            with Image.open(path) as image:
                assert image.size == (384, 384) and image.format == "JPEG"
    sample_score = grade(sample, answers)
    metadata = _metadata_baseline(train, test)
    metadata_score = grade(metadata, answers)
    image_knn = _image_knn_baseline(train, test, public)
    image_score = grade(image_knn, answers)
    file_size_knn = _file_size_knn_baseline(train, test, public)
    file_size_score = grade(file_size_knn, answers)
    id_prefix = _id_prefix_baseline(train, test)
    id_prefix_score = grade(id_prefix, answers)
    hash_size = _hash_size_probe(train, test, public, ROOT / "raw_data")
    id_order = _id_order_probe(train, test)
    retrieval_rank1, retrieval_rank5, retrieval_median = _retrieval_probe(
        train, test, public, ROOT / "raw_data"
    )
    (
        multicrop_rank1,
        multicrop_rank5,
        multicrop_rank10,
        multicrop_median,
        multicrop_candidates,
    ) = _multicrop_retrieval_probe(test, public, ROOT / "raw_data")
    assert sample_score < 0.50
    assert metadata_score < 0.55
    assert image_score < 0.70
    assert id_prefix_score < 0.45
    assert file_size_score < 0.45
    assert max(sample_score, metadata_score) < image_score + 0.20
    assert hash_size["exact_public_image_sha256_hits_in_raw_images"] == 0
    assert hash_size["test_rows_uniquely_true_by_raw_file_size"] == 0
    assert id_order["format_ok"] and id_order["train_test_overlap"] == 0
    assert id_order["first_test_rank_in_sorted_ids"] < len(test)
    assert id_order["last_train_rank_in_sorted_ids"] >= len(train)
    assert retrieval_rank1 <= 0.02
    assert retrieval_rank5 <= 0.10
    assert multicrop_rank1 <= 0.08
    assert multicrop_rank5 <= 0.12
    assert multicrop_rank10 <= 0.20

    source_stem_tokens = ("NLA_", "NLB_", "NRB_", "_merged", "EDR_F", "masked-gold", "ai4mars-dataset")
    public_text = (public / "train.csv").read_text(encoding="utf-8") + (public / "test.csv").read_text(encoding="utf-8")
    assert not any(token in public_text for token in source_stem_tokens)
    print(
        json.dumps(
            {
                "rows": {"train": len(train), "test": len(test)},
                "sample_template": round(sample_score, 6),
                "metadata_only": round(metadata_score, 6),
                "cpu_image_knn": round(image_score, 6),
                "id_prefix_only": round(id_prefix_score, 6),
                "file_size_only_knn": round(file_size_score, 6),
                "id_order_probe": id_order,
                "hash_and_size_probe": hash_size,
                "source_thumbnail_probe": {
                    "rank1_rate": round(retrieval_rank1, 6),
                    "rank5_rate": round(retrieval_rank5, 6),
                    "median_rank": retrieval_median,
                    "source_pool": 526,
                },
                "source_multicrop_probe": {
                    "rank1_rate": round(multicrop_rank1, 6),
                    "rank5_rate": round(multicrop_rank5, 6),
                    "rank10_rate": round(multicrop_rank10, 6),
                    "median_rank": multicrop_median,
                    "crop_candidates": multicrop_candidates,
                    "source_pool": 526,
                },
                "source_lookup_guards": {
                    "opaque_salted_ids": True,
                    "raw_stems_absent": True,
                    "prepared_size_differs": True,
                    "prepared_jpeg_reencoded": True,
                    "sequence_groups_disjoint": True,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
