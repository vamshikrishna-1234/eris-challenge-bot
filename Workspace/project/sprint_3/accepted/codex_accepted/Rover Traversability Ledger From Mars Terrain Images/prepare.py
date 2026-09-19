"""Prepare the AI4Mars route-conditioned traversability-ledger challenge."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, deque
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


SOURCE_DIR = "ai4mars-dataset-merged-0.6"
MSL_LABEL_REL = "msl/ncam/labels/test/masked-gold-min2-100agree"
MER_LABEL_REL = "mer/labels/test/masked-gold-min2-100agree"
MSL_IMAGE_REL = "msl/ncam/images/edr"
MER_IMAGE_REL = "mer/images/test"
SPLIT_SALT = "eris-rover-ledger-split-v1"
ID_SALT = "eris-rover-ledger-public-id-v1-9fc2"
ROUTE_SALT = "eris-rover-ledger-route-v1"
TEST_PER_1000 = 330
MIN_GROUP_TEST = 15
MASK_SIZE = 32
PUBLIC_IMAGE_SIZE = 384
SOURCE_CLASSES = {0, 1, 2, 3, 255}
ROUTE_CLASSES = {"safe_to_drive", "drive_slowly", "avoid_area", "uncertain"}

INPUT_COLUMNS = [
    "id",
    "image",
    "mission",
    "camera",
    "image_width",
    "image_height",
    "route_query_json",
    "prompt",
]
TARGET_COLUMNS = [
    "terrain_mask_rle",
    "hazard_boxes_json",
    "route_safety_class",
    "clearance_score",
    "obstacle_coverage",
    "safe_corridor_width",
    "uncertainty_score",
]
SUBMISSION_COLUMNS = ["id"] + TARGET_COLUMNS

ROUTES = [
    ("center", 0.50, 0.94, 0.50, 0.16, 0.085),
    ("left_merge", 0.28, 0.94, 0.46, 0.16, 0.085),
    ("right_merge", 0.72, 0.94, 0.54, 0.16, 0.085),
    ("left_lane", 0.34, 0.94, 0.34, 0.16, 0.075),
    ("right_lane", 0.66, 0.94, 0.66, 0.16, 0.075),
]

PROMPT = (
    "A real Mars Navcam image shows terrain ahead. The route_query_json field gives a "
    "normalized image-plane corridor from (start_x,start_y) to (end_x,end_y) with a "
    "half_width. Predict a 32x32 AI4Mars terrain region map using class ids 0=soil, "
    "1=bedrock, 2=sand, 3=big_rock, 255=unknown; class-aware hazard boxes for big-rock "
    "and substantial unknown components; route_safety_class in safe_to_drive, "
    "drive_slowly, avoid_area, uncertain; and the four route geometry measures in [0,1]. "
    "Use pixels and the stated route. Do not use original-source filename or annotation lookup."
)


def _source_root(raw: Path) -> Path:
    raw = Path(raw)
    candidates = [raw / SOURCE_DIR, raw / "raw_upload" / SOURCE_DIR, raw]
    for candidate in candidates:
        if (candidate / "label_keys.json").is_file() and (candidate / MSL_LABEL_REL).is_dir():
            return candidate
    hits = list(raw.glob(f"**/{SOURCE_DIR}/label_keys.json"))
    if len(hits) == 1:
        return hits[0].parent
    raise FileNotFoundError(
        f"Could not find the clean official {SOURCE_DIR} subset below {raw}"
    )


def _validate_label_key(source: Path) -> None:
    key = json.loads((source / "label_keys.json").read_text(encoding="utf-8"))
    expected = {"0": "soil", "1": "bedrock", "2": "sand", "3": "big rock", "255": None}
    if key.get("NAV") != expected:
        raise SystemExit(f"Unexpected official NAV class key: {key.get('NAV')}")


def _pair_records(source: Path) -> list[dict[str, str | Path]]:
    records: list[dict[str, str | Path]] = []
    msl_labels = sorted((source / MSL_LABEL_REL).glob("*.png"))
    mer_labels = sorted((source / MER_LABEL_REL).glob("*.png"))
    if len(msl_labels) != 322 or len(mer_labels) != 204:
        raise SystemExit(f"Expected 322 MSL and 204 MER expert masks; got {len(msl_labels)}, {len(mer_labels)}")
    for label in msl_labels:
        stem = label.stem.removesuffix("_merged")
        image = source / MSL_IMAGE_REL / f"{stem}.JPG"
        records.append({"stem": stem, "image": image, "label": label, "mission": "Curiosity"})
    for label in mer_labels:
        stem = re.sub(r"_\d+_T\d+_merged$", "", label.stem)
        image = source / MER_IMAGE_REL / f"{stem}.JPG"
        mission = "Opportunity" if stem.startswith("1") else "Spirit"
        records.append({"stem": stem, "image": image, "label": label, "mission": mission})
    for record in records:
        if not Path(record["image"]).is_file():
            raise FileNotFoundError(f"Official image is missing for {record['label']}")
    if len({str(r["stem"]) for r in records}) != len(records):
        raise SystemExit("Duplicate official source stems found")
    return records


def _sequence_family(stem: str, mission: str) -> str:
    if mission == "Curiosity":
        match = re.search(r"_(\d{9})EDR_(F\d{4})", stem)
        if not match:
            raise ValueError(f"Cannot parse MSL image family: {stem}")
        return f"MSL:{int(match.group(1)) // 100000}:{match.group(2)}"
    match = re.match(r"([12])[a-z](\d{9})", stem.lower())
    if not match:
        raise ValueError(f"Cannot parse MER image family: {stem}")
    return f"MER{match.group(1)}:{int(match.group(2)) // 100000}"


def _split_of(group: str) -> str:
    digest = hashlib.sha256(f"{SPLIT_SALT}:{group}".encode()).hexdigest()
    return "test" if int(digest[:8], 16) % 1000 < TEST_PER_1000 else "train"


def _public_id(stem: str) -> str:
    digest = hashlib.sha256(f"{ID_SALT}:{stem}".encode()).hexdigest()
    return "rvr_" + digest[:14]


def _route_for(stem: str) -> dict[str, str | float]:
    digest = hashlib.sha256(f"{ROUTE_SALT}:{stem}".encode()).digest()
    name, sx, sy, ex, ey, half = ROUTES[digest[0] % len(ROUTES)]
    return {
        "route_name": name,
        "start_x": sx,
        "start_y": sy,
        "end_x": ex,
        "end_y": ey,
        "half_width": half,
    }


def _crop_box(stem: str, width: int, height: int) -> tuple[int, int, int, int, bool]:
    # A local field of view materially weakens public-source thumbnail lookup
    # while preserving a coherent real terrain patch and aligned mask geometry.
    digest = hashlib.sha256(f"crop:{stem}".encode()).digest()
    base = min(width, height)
    side_fraction = 0.24 + 0.10 * (digest[3] / 255.0)
    side = int(round(base * side_fraction))
    side = min(base, max(240, min(side, 340)))
    max_x = max(0, width - side)
    max_y = max(0, height - side)
    x0 = int(digest[0] / 255 * max_x) if max_x else 0
    y0 = int(digest[1] / 255 * max_y) if max_y else 0
    return x0, y0, x0 + side, y0 + side, bool(digest[2] & 1)


def _harden_visual_pair(image: Image.Image, label: Image.Image, stem: str) -> tuple[Image.Image, Image.Image]:
    """Apply a deterministic, label-preserving image transform.

    The goal is not to synthesize new terrain, but to avoid publishing source-
    reversible crops of a public dataset.  The same local view, small rotation,
    crop offset, and photometric changes are applied deterministically to keep
    the image realistic and the mask geometry aligned.
    """

    digest = hashlib.sha256(f"visual-hardening:{stem}".encode()).digest()
    canvas = PUBLIC_IMAGE_SIZE + 96
    image = image.resize((canvas, canvas), Image.Resampling.LANCZOS)
    label = label.resize((canvas, canvas), Image.Resampling.NEAREST)

    angle = 15.0 * (digest[0] / 255.0 - 0.5)
    fill = int(np.median(np.asarray(image, dtype=np.uint8)))
    image = image.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=fill)
    label = label.rotate(angle, resample=Image.Resampling.NEAREST, expand=False, fillcolor=255)

    margin = canvas - PUBLIC_IMAGE_SIZE
    center = margin // 2
    max_offset = min(36, center)
    offset_x = center + int(round((digest[1] / 255.0 - 0.5) * 2 * max_offset))
    offset_y = center + int(round((digest[2] / 255.0 - 0.5) * 2 * max_offset))
    crop = (offset_x, offset_y, offset_x + PUBLIC_IMAGE_SIZE, offset_y + PUBLIC_IMAGE_SIZE)
    image = image.crop(crop)
    label = label.crop(crop)

    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageOps.equalize(image)
    contrast = 0.82 + 0.36 * (digest[4] / 255.0)
    brightness = 0.88 + 0.22 * (digest[5] / 255.0)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = ImageEnhance.Brightness(image).enhance(brightness)
    if digest[6] & 1:
        image = image.filter(ImageFilter.GaussianBlur(radius=0.25 + 0.45 * (digest[7] / 255.0)))
    else:
        image = image.filter(ImageFilter.UnsharpMask(radius=0.8, percent=80, threshold=4))

    array = np.asarray(image, dtype=np.float32)
    seed = int.from_bytes(digest[8:16], "big", signed=False)
    rng = np.random.default_rng(seed)
    damp_size = 336 + 16 * (digest[19] % 3)
    image = image.resize((damp_size, damp_size), Image.Resampling.BICUBIC).resize(
        (PUBLIC_IMAGE_SIZE, PUBLIC_IMAGE_SIZE), Image.Resampling.BICUBIC
    )
    array = np.asarray(image, dtype=np.float32)
    noise_sigma = 2.2 + 2.4 * (digest[16] / 255.0)
    array += rng.normal(0.0, noise_sigma, array.shape).astype(np.float32)
    yy, xx = np.mgrid[0:PUBLIC_IMAGE_SIZE, 0:PUBLIC_IMAGE_SIZE]
    array += (xx - (PUBLIC_IMAGE_SIZE - 1) / 2.0) * ((digest[17] / 255.0 - 0.5) / 34.0)
    array += (yy - (PUBLIC_IMAGE_SIZE - 1) / 2.0) * ((digest[18] / 255.0 - 0.5) / 34.0)
    image = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), mode="L")
    return image, label


def _block_mode(mask: np.ndarray) -> np.ndarray:
    h, w = mask.shape
    if h % MASK_SIZE or w % MASK_SIZE:
        pil = Image.fromarray(mask.astype(np.uint8), mode="L")
        mask = np.asarray(pil.resize((MASK_SIZE * 28, MASK_SIZE * 28), Image.Resampling.NEAREST))
        h, w = mask.shape
    bh, bw = h // MASK_SIZE, w // MASK_SIZE
    blocks = mask.reshape(MASK_SIZE, bh, MASK_SIZE, bw).transpose(0, 2, 1, 3)
    result = np.full((MASK_SIZE, MASK_SIZE), 255, dtype=np.uint8)
    for y in range(MASK_SIZE):
        for x in range(MASK_SIZE):
            values = blocks[y, x].reshape(-1)
            unknown_fraction = float(np.mean(values == 255))
            if unknown_fraction >= 0.50:
                continue
            known = values[values != 255]
            if len(known):
                counts = np.bincount(known.astype(np.int64), minlength=4)
                result[y, x] = int(np.argmax(counts[:4]))
    return result


def _transform_pair(image_path: Path, label_path: Path, stem: str) -> tuple[Image.Image, np.ndarray]:
    with Image.open(image_path) as source_image, Image.open(label_path) as source_label:
        image = source_image.convert("L")
        label = source_label.convert("L")
        if image.size != label.size:
            raise SystemExit(f"Image/mask size mismatch for {stem}: {image.size} vs {label.size}")
        box = _crop_box(stem, *image.size)
        crop = box[:4]
        flip = box[4]
        image = image.crop(crop)
        label = label.crop(crop)
        if flip:
            image = ImageOps.mirror(image)
            label = ImageOps.mirror(label)
        image, label = _harden_visual_pair(image, label, stem)
        pixels = np.asarray(label, dtype=np.uint8)
        unexpected = set(int(x) for x in np.unique(pixels)) - SOURCE_CLASSES
        if unexpected:
            raise SystemExit(f"Unexpected mask values for {stem}: {sorted(unexpected)}")
        low = _block_mode(pixels)
    return image, low


def encode_mask(mask: np.ndarray) -> str:
    flat = np.asarray(mask, dtype=np.uint8).reshape(-1)
    runs: list[list[int]] = []
    for value in flat:
        ivalue = int(value)
        if runs and runs[-1][0] == ivalue:
            runs[-1][1] += 1
        else:
            runs.append([ivalue, 1])
    return json.dumps({"shape": [MASK_SIZE, MASK_SIZE], "counts": runs}, separators=(",", ":"))


def decode_mask(cell: str) -> np.ndarray:
    data = json.loads(cell)
    if data.get("shape") != [MASK_SIZE, MASK_SIZE]:
        raise ValueError("bad shape")
    values: list[int] = []
    for value, length in data["counts"]:
        values.extend([int(value)] * int(length))
    if len(values) != MASK_SIZE * MASK_SIZE or set(values) - SOURCE_CLASSES:
        raise ValueError("bad RLE")
    return np.asarray(values, dtype=np.uint8).reshape(MASK_SIZE, MASK_SIZE)


def _components(binary: np.ndarray, kind: str, min_area: int) -> list[dict[str, float | str]]:
    h, w = binary.shape
    seen = np.zeros_like(binary, dtype=bool)
    items: list[tuple[int, dict[str, float | str]]] = []
    for y in range(h):
        for x in range(w):
            if not binary[y, x] or seen[y, x]:
                continue
            queue = deque([(y, x)])
            seen[y, x] = True
            points: list[tuple[int, int]] = []
            while queue:
                cy, cx = queue.popleft()
                points.append((cy, cx))
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < h and 0 <= nx < w and binary[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        queue.append((ny, nx))
            if len(points) < min_area:
                continue
            ys = [p[0] for p in points]
            xs = [p[1] for p in points]
            x0, x1 = min(xs), max(xs) + 1
            y0, y1 = min(ys), max(ys) + 1
            box = {
                "kind": kind,
                "x": round(x0 / w, 4),
                "y": round(y0 / h, 4),
                "w": round((x1 - x0) / w, 4),
                "h": round((y1 - y0) / h, 4),
            }
            items.append((len(points), box))
    return [box for _, box in sorted(items, key=lambda item: -item[0])]


def hazard_boxes(mask: np.ndarray) -> list[dict[str, float | str]]:
    boxes = _components(mask == 3, "big_rock", 2)
    boxes += _components(mask == 255, "unknown", 20)
    return boxes[:8]


def _corridor_mask(route: dict[str, str | float], size: int = MASK_SIZE) -> np.ndarray:
    sx, sy = float(route["start_x"]), float(route["start_y"])
    ex, ey = float(route["end_x"]), float(route["end_y"])
    half = float(route["half_width"])
    yy, xx = np.mgrid[0:size, 0:size]
    px = (xx + 0.5) / size
    py = (yy + 0.5) / size
    vx, vy = ex - sx, ey - sy
    denom = vx * vx + vy * vy
    t = np.clip(((px - sx) * vx + (py - sy) * vy) / max(denom, 1e-12), 0.0, 1.0)
    dx = px - (sx + t * vx)
    dy = py - (sy + t * vy)
    return np.sqrt(dx * dx + dy * dy) <= half


def derive_ledger(mask: np.ndarray, route: dict[str, str | float]) -> dict[str, str | float]:
    corridor = _corridor_mask(route)
    values = mask[corridor]
    if not len(values):
        raise ValueError("empty route corridor")
    weights = np.select(
        [values == 0, values == 1, values == 2, values == 3, values == 255],
        [1.0, 0.95, 0.55, 0.0, 0.25],
        default=0.0,
    )
    clearance = float(np.mean(weights))
    obstacle = float(np.mean(values == 3))
    route_unknown = float(np.mean(values == 255))
    global_unknown = float(np.mean(mask == 255))
    uncertainty = float(np.clip(0.75 * route_unknown + 0.25 * global_unknown, 0.0, 1.0))
    sand = float(np.mean(values == 2))

    widths: list[float] = []
    sx, sy = float(route["start_x"]), float(route["start_y"])
    ex, ey = float(route["end_x"]), float(route["end_y"])
    for t in np.linspace(0.05, 0.95, 15):
        x = sx + t * (ex - sx)
        y = sy + t * (ey - sy)
        row = int(np.clip(math.floor(y * MASK_SIZE), 0, MASK_SIZE - 1))
        col = int(np.clip(math.floor(x * MASK_SIZE), 0, MASK_SIZE - 1))
        if mask[row, col] in {3, 255}:
            widths.append(0.0)
            continue
        left = col
        right = col
        while left - 1 >= 0 and mask[row, left - 1] not in {3, 255}:
            left -= 1
        while right + 1 < MASK_SIZE and mask[row, right + 1] not in {3, 255}:
            right += 1
        widths.append((right - left + 1) / MASK_SIZE)
    safe_width = float(np.quantile(widths, 0.20)) if widths else 0.0

    if uncertainty >= 0.32:
        route_class = "uncertain"
    elif obstacle >= 0.14 or clearance < 0.44 or safe_width < 0.08:
        route_class = "avoid_area"
    elif obstacle >= 0.035 or sand >= 0.32 or clearance < 0.76 or safe_width < 0.18:
        route_class = "drive_slowly"
    else:
        route_class = "safe_to_drive"
    return {
        "hazard_boxes_json": json.dumps(hazard_boxes(mask), separators=(",", ":")),
        "route_safety_class": route_class,
        "clearance_score": round(clearance, 6),
        "obstacle_coverage": round(obstacle, 6),
        "safe_corridor_width": round(safe_width, 6),
        "uncertainty_score": round(uncertainty, 6),
    }


def _terrain_group(mask: np.ndarray) -> str:
    known = mask != 255
    known_fraction = float(np.mean(known))
    if float(np.mean(mask == 3)) >= 0.018:
        return "rock_hazard"
    if known.any() and float(np.mean(mask[known] == 2)) >= 0.28:
        return "sand_dominant"
    if known_fraction < 0.52:
        return "sparse_annotation"
    return "firm_ground"


def _mode_or(series: pd.Series, default: str) -> str:
    mode = series.mode(dropna=True)
    return str(mode.iloc[0]) if len(mode) else default


def _coarsen_sparse_axis(df: pd.DataFrame, col: str, fallback: str) -> None:
    counts = df[col].value_counts()
    rare = set(counts[counts < MIN_GROUP_TEST].index)
    if rare:
        df.loc[df[col].isin(rare), col] = fallback
        counts = df[col].value_counts()
        if fallback in counts and int(counts[fallback]) < MIN_GROUP_TEST:
            majority = str(counts.drop(index=fallback, errors="ignore").idxmax())
            df.loc[df[col] == fallback, col] = majority


def _validate_groups(df: pd.DataFrame) -> None:
    for col in ["mission_group", "terrain_group", "route_group"]:
        counts = df[col].value_counts()
        if len(counts) == 0 or int(counts.min()) < MIN_GROUP_TEST:
            raise SystemExit(f"TEST subgroup {col} too small: {counts.to_dict()}")


def _cellwise_mode(masks: list[np.ndarray]) -> np.ndarray:
    stack = np.stack(masks, axis=0)
    out = np.zeros((MASK_SIZE, MASK_SIZE), dtype=np.uint8)
    classes = [0, 1, 2, 3, 255]
    for y in range(MASK_SIZE):
        for x in range(MASK_SIZE):
            counts = Counter(int(v) for v in stack[:, y, x])
            out[y, x] = max(classes, key=lambda c: (counts[c], -classes.index(c)))
    return out


def prepare(raw: Path, public: Path, private: Path) -> None:
    source = _source_root(Path(raw))
    _validate_label_key(source)
    records = _pair_records(source)
    scene_hash_keys = pd.Series([str(record["stem"]).strip() for record in records], dtype="string")
    if scene_hash_keys.isna().any() or scene_hash_keys.eq("").any():
        raise SystemExit("Raw scene_hash-equivalent source stems contain NaN or blank values")
    if not scene_hash_keys.is_unique:
        raise SystemExit("Raw scene_hash-equivalent source stems are not unique")
    id_map = {scene_hash: _public_id(scene_hash) for scene_hash in scene_hash_keys.astype(str)}
    if len(id_map) != len(records) or len(set(id_map.values())) != len(records):
        raise SystemExit("Raw source stems or salted public ids are not unique")
    public = Path(public)
    private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    for split_name in ["train", "test"]:
        image_dir = public / split_name / "images"
        image_dir.mkdir(parents=True, exist_ok=True)
        for stale in image_dir.glob("*.jpg"):
            stale.unlink()

    rows: list[dict[str, object]] = []
    masks_by_id: dict[str, np.ndarray] = {}
    groups_seen: dict[str, str] = {}
    for index, record in enumerate(records, start=1):
        stem = str(record["stem"])
        mission = str(record["mission"])
        group = _sequence_family(stem, mission)
        split = _split_of(group)
        if group in groups_seen and groups_seen[group] != split:
            raise AssertionError("Sequence family crossed splits")
        groups_seen[group] = split
        rid = id_map[stem]
        route = _route_for(stem)
        image, mask = _transform_pair(Path(record["image"]), Path(record["label"]), stem)
        if float(np.mean(mask != 255)) < 0.03:
            continue
        image_name = f"{Path(rid).name}.jpg"
        image_path = public / split / "images" / image_name
        image.save(image_path, format="JPEG", quality=58, optimize=True)
        ledger = derive_ledger(mask, route)
        row: dict[str, object] = {
            "id": rid,
            "image": f"{split}/images/{image_name}",
            "mission": mission,
            "camera": "Navcam",
            "image_width": PUBLIC_IMAGE_SIZE,
            "image_height": PUBLIC_IMAGE_SIZE,
            "route_query_json": json.dumps(route, separators=(",", ":")),
            "prompt": PROMPT,
            "terrain_mask_rle": encode_mask(mask),
            **ledger,
            "split": split,
            "source_group": group,
            "mission_group": mission,
            "terrain_group": _terrain_group(mask),
            "route_group": str(route["route_name"]),
        }
        rows.append(row)
        masks_by_id[rid] = mask
        if index % 100 == 0:
            print(f"processed {index}/{len(records)} official pairs")

    frame = pd.DataFrame(rows)
    if len(frame) < 350:
        raise SystemExit(f"Too few usable expert-labelled rows after coverage guard: {len(frame)}")
    if frame["id"].duplicated().any():
        raise SystemExit("Salted public id collision")
    train = frame[frame["split"] == "train"].copy()
    test = frame[frame["split"] == "test"].copy()
    if len(train) < 220 or len(test) < 90:
        raise SystemExit(f"Split too small: train={len(train)}, test={len(test)}")

    template_mask = np.zeros((MASK_SIZE, MASK_SIZE), dtype=np.uint8)
    template_mask_rle = encode_mask(template_mask)
    sample_rows = []
    for _, row in test.iterrows():
        sample_rows.append(
            {
                "id": row["id"],
                "terrain_mask_rle": template_mask_rle,
                "hazard_boxes_json": "[]",
                "route_safety_class": "safe_to_drive",
                "clearance_score": 1.0,
                "obstacle_coverage": 0.0,
                "safe_corridor_width": 1.0,
                "uncertainty_score": 0.0,
            }
        )

    train_df = train[INPUT_COLUMNS + TARGET_COLUMNS].sort_values("id").reset_index(drop=True)
    test_df = test[INPUT_COLUMNS].sort_values("id").reset_index(drop=True)
    sample_df = pd.DataFrame(sample_rows)[SUBMISSION_COLUMNS].sort_values("id").reset_index(drop=True)
    answer_cols = SUBMISSION_COLUMNS + ["mission_group", "terrain_group", "route_group", "source_group"]
    answer_df = test[answer_cols].sort_values("id").reset_index(drop=True)
    for col, fallback in [
        ("mission_group", "other_mission"),
        ("terrain_group", "other_terrain"),
        ("route_group", "other_route"),
    ]:
        _coarsen_sparse_axis(answer_df, col, fallback)
    _validate_groups(answer_df)

    for name, data in [("train", train_df), ("test", test_df), ("sample", sample_df), ("answers", answer_df)]:
        if data.isna().any().any():
            raise SystemExit(f"{name}.csv contains missing values")
    if set(test_df["id"]) != set(answer_df["id"]):
        raise AssertionError("Test and answer ids differ")
    if set(train["source_group"]) & set(test["source_group"]):
        raise AssertionError("Related source sequences cross train/test")

    train_df.to_csv(public / "train.csv", index=False)
    test_df.to_csv(public / "test.csv", index=False)
    sample_df.to_csv(public / "sample_submission.csv", index=False)
    answer_df.to_csv(private / "answers.csv", index=False)
    print(f"OK: {len(train_df)} train, {len(test_df)} test; source groups are disjoint")
    for col in ["mission_group", "terrain_group", "route_group"]:
        print(f"{col}: {answer_df[col].value_counts().to_dict()}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    args = parser.parse_args()
    # Keep caller-provided paths without resolving Windows junctions: the
    # official AI4Mars label hierarchy is deep enough to exceed legacy MAX_PATH
    # when this challenge folder itself has a long name.
    prepare(args.raw, args.public, args.private)
