"""Prepare Lightning Flash Hierarchy Induction from official NOAA GLM L2 files.

The five raw inputs are untouched official NetCDF objects imported directly from
NOAA's public GOES-16 NODD bucket.  This script verifies each object, reads the
native event -> group -> flash hierarchy, builds source-day-disjoint local
point-set cases, removes source lookup keys, and writes the platform files.

Platform entry point: prepare(raw, public, private)
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


CASE_SALT = "lfhi-public-alias-v3-20260716"
CASES_PER_SOURCE = 70
MIN_GROUP_TEST = 30
MAX_DETECTIONS = 40
MIN_DETECTIONS = 12

PROMPT = (
    "Reconstruct the anonymous detections' two-level hierarchy: partition all "
    "detections into simultaneous local groups, partition those groups into "
    "larger flashes, and identify detections whose parent assignment is "
    "genuinely ambiguous in the supplied redacted evidence."
)

MANIFEST = (
    {
        "key": "window_a",
        "split": "train",
        "name": "OR_GLM-L2-LCFA_G16_s20241532200000_e20241532200200_c20241532200219.nc",
        "url": "https://noaa-goes16.s3.amazonaws.com/GLM-L2-LCFA/2024/153/22/OR_GLM-L2-LCFA_G16_s20241532200000_e20241532200200_c20241532200219.nc",
        "bytes": 398567,
        "sha256": "10f9c79a8a3acb50f62599d1cecb930e27f01e0148d0885bdf31c33d1c590f75",
        "events": 9862,
        "groups": 4261,
        "flashes": 279,
    },
    {
        "key": "window_b",
        "split": "train",
        "name": "OR_GLM-L2-LCFA_G16_s20241832200000_e20241832200200_c20241832200214.nc",
        "url": "https://noaa-goes16.s3.amazonaws.com/GLM-L2-LCFA/2024/183/22/OR_GLM-L2-LCFA_G16_s20241832200000_e20241832200200_c20241832200214.nc",
        "bytes": 478439,
        "sha256": "3d62f783a2cc6f57de9493630dc7f26f8bd7d635fdb9c82a50524dec2fa4ba3f",
        "events": 12855,
        "groups": 5567,
        "flashes": 466,
    },
    {
        "key": "window_c",
        "split": "train",
        "name": "OR_GLM-L2-LCFA_G16_s20242142200000_e20242142200200_c20242142200221.nc",
        "url": "https://noaa-goes16.s3.amazonaws.com/GLM-L2-LCFA/2024/214/22/OR_GLM-L2-LCFA_G16_s20242142200000_e20242142200200_c20242142200221.nc",
        "bytes": 628519,
        "sha256": "6f8f150d5a423181d7e169923f063df53c00a16135583e152a8e3dfbcf4ecabf",
        "events": 17190,
        "groups": 7597,
        "flashes": 603,
    },
    {
        "key": "window_d",
        "split": "test",
        "name": "OR_GLM-L2-LCFA_G16_s20242692200000_e20242692200200_c20242692200221.nc",
        "url": "https://noaa-goes16.s3.amazonaws.com/GLM-L2-LCFA/2024/269/22/OR_GLM-L2-LCFA_G16_s20242692200000_e20242692200200_c20242692200221.nc",
        "bytes": 780071,
        "sha256": "362ea0e9a348247102340f7a02e2af3d88841e81158aa49285419280f41e3fb6",
        "events": 23685,
        "groups": 9524,
        "flashes": 701,
    },
    {
        "key": "window_e",
        "split": "test",
        "name": "OR_GLM-L2-LCFA_G16_s20242792200000_e20242792200200_c20242792200220.nc",
        "url": "https://noaa-goes16.s3.amazonaws.com/GLM-L2-LCFA/2024/279/22/OR_GLM-L2-LCFA_G16_s20242792200000_e20242792200200_c20242792200220.nc",
        "bytes": 616231,
        "sha256": "4c4b56f21be7196651d5bc1cff7548a89158d2f953ac14208f06f77c768d1113",
        "events": 17935,
        "groups": 6766,
        "flashes": 465,
    },
)


@dataclass(frozen=True)
class Event:
    eid: int
    gid: int
    fid: int
    time_s: float
    lat: float
    lon: float
    energy: float


@dataclass
class Flash:
    fid: int
    groups: dict[int, list[Event]]
    time_s: float
    lat: float
    lon: float


def _json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_seed(*parts: object) -> int:
    raw = ":".join(str(p) for p in (CASE_SALT, *parts))
    return int.from_bytes(hashlib.sha256(raw.encode("utf-8")).digest()[:8], "big")


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _locate_sources(raw: Path) -> list[tuple[dict, Path]]:
    raw = Path(raw)
    files = [p for p in raw.rglob("*.nc") if p.is_file()]
    by_hash: dict[str, Path] = {}
    for path in sorted(files):
        if path.stat().st_size in {int(m["bytes"]) for m in MANIFEST}:
            digest = _file_sha256(path)
            if digest in {str(m["sha256"]) for m in MANIFEST}:
                if digest in by_hash:
                    raise ValueError("Duplicate official source object in raw input")
                by_hash[digest] = path

    found: list[tuple[dict, Path]] = []
    for item in MANIFEST:
        path = by_hash.get(str(item["sha256"]))
        if path is None:
            raise FileNotFoundError(
                f"Missing verified NOAA object {item['name']}; import the five URLs "
                "listed in URL_IMPORT_LIST.txt without changing their bytes"
            )
        if path.stat().st_size != int(item["bytes"]):
            raise ValueError(f"Byte-length mismatch for {item['name']}")
        found.append((item, path))
    return found


def _scalar_attr(value):
    arr = np.asarray(value)
    if arr.shape == ():
        out = arr.item()
    else:
        out = arr.ravel()[0].item()
    if isinstance(out, bytes):
        return out.decode("utf-8", errors="replace")
    return out


class _Netcdf4Reader:
    def __init__(self, dataset):
        self.dataset = dataset

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.dataset.close()

    def attr(self, name: str):
        return getattr(self.dataset, name, "")

    def dimension_size(self, name: str) -> int:
        if name not in self.dataset.dimensions:
            raise KeyError(name)
        return len(self.dataset.dimensions[name])

    def variable_names(self) -> set[str]:
        return set(self.dataset.variables)

    def array(self, name: str, dtype) -> np.ndarray:
        return np.asarray(self.dataset[name][:], dtype=dtype)


class _H5pyReader:
    DIMENSION_VARIABLES = {
        "number_of_events": "event_id",
        "number_of_groups": "group_id",
        "number_of_flashes": "flash_id",
    }

    def __init__(self, h5file):
        self.h5file = h5file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.h5file.close()

    def attr(self, name: str):
        if name not in self.h5file.attrs:
            return ""
        return _scalar_attr(self.h5file.attrs[name])

    def dimension_size(self, name: str) -> int:
        var_name = self.DIMENSION_VARIABLES.get(name)
        if var_name is None or var_name not in self.h5file:
            raise KeyError(name)
        return int(self.h5file[var_name].shape[0])

    def variable_names(self) -> set[str]:
        return {name for name, value in self.h5file.items() if hasattr(value, "shape")}

    def array(self, name: str, dtype) -> np.ndarray:
        if name not in self.h5file:
            raise KeyError(name)
        dataset = self.h5file[name]
        raw = np.asarray(dataset[()])
        unsigned = str(_scalar_attr(dataset.attrs.get("_Unsigned", ""))).lower() == "true"
        if unsigned and raw.dtype.kind == "i":
            raw = raw.view(np.dtype(f"u{raw.dtype.itemsize}"))
        fill_value = dataset.attrs.get("_FillValue", None)
        scale = dataset.attrs.get("scale_factor", None)
        offset = dataset.attrs.get("add_offset", None)

        if scale is not None or offset is not None:
            attr_dtypes = [
                np.asarray(v).dtype
                for v in (scale, offset)
                if v is not None
            ]
            calc_dtype = np.float32 if any(dt == np.dtype("float32") for dt in attr_dtypes) else np.float64
            arr = raw.astype(calc_dtype)
            if fill_value is not None:
                fill = _scalar_attr(fill_value)
                arr = np.where(raw == fill, np.nan, arr)
            if scale is not None:
                arr = arr * np.asarray(scale, dtype=calc_dtype).ravel()[0]
            if offset is not None:
                arr = arr + np.asarray(offset, dtype=calc_dtype).ravel()[0]
            return np.asarray(arr, dtype=dtype)
        return np.asarray(raw, dtype=dtype)


def _open_glm_dataset(path: Path):
    try:
        from netCDF4 import Dataset  # type: ignore
    except ImportError:
        Dataset = None
    if Dataset is not None:
        return _Netcdf4Reader(Dataset(path, "r"))

    try:
        import h5py  # type: ignore
    except ImportError as exc:  # pragma: no cover - platform dependency message
        raise RuntimeError(
            "prepare.py requires either netCDF4 or h5py to read official GLM NetCDF4/HDF5 files"
        ) from exc
    return _H5pyReader(h5py.File(path, "r"))


def _load_flashes(item: dict, path: Path) -> dict[int, Flash]:
    with _open_glm_dataset(path) as ds:
        if ds.attr("title") != "GLM L2 Lightning Detections: Events, Groups, and Flashes":
            raise ValueError("Unexpected NOAA product title")
        if ds.attr("processing_level") != "National Aeronautics and Space Administration (NASA) L2":
            raise ValueError("Unexpected processing level")
        if ds.attr("platform_ID") != "G16":
            raise ValueError("Unexpected satellite platform")
        expected_dims = {
            "number_of_events": int(item["events"]),
            "number_of_groups": int(item["groups"]),
            "number_of_flashes": int(item["flashes"]),
        }
        for name, expected in expected_dims.items():
            try:
                actual = ds.dimension_size(name)
            except KeyError as exc:
                raise ValueError(f"Missing {name} dimension") from exc
            if actual != expected:
                raise ValueError(f"Unexpected {name} count")

        required = {
            "event_id", "event_parent_group_id", "event_time_offset", "event_lat",
            "event_lon", "event_energy", "group_id", "group_parent_flash_id",
            "group_time_offset", "group_lat", "group_lon", "group_quality_flag",
            "flash_id", "flash_quality_flag",
        }
        missing = sorted(required - ds.variable_names())
        if missing:
            raise ValueError(f"Missing GLM variables: {missing}")

        event_id = ds.array("event_id", np.int64)
        event_gid = ds.array("event_parent_group_id", np.int64)
        event_t = ds.array("event_time_offset", np.float64)
        event_lat = ds.array("event_lat", np.float64)
        event_lon = ds.array("event_lon", np.float64)
        event_energy = ds.array("event_energy", np.float64)

        group_id = ds.array("group_id", np.int64)
        group_fid = ds.array("group_parent_flash_id", np.int64)
        group_t = ds.array("group_time_offset", np.float64)
        group_lat = ds.array("group_lat", np.float64)
        group_lon = ds.array("group_lon", np.float64)
        group_q = ds.array("group_quality_flag", np.int64)
        flash_id = ds.array("flash_id", np.int64)
        flash_q = ds.array("flash_quality_flag", np.int64)

    arrays = [event_t, event_lat, event_lon, event_energy, group_t, group_lat, group_lon]
    if any(not np.all(np.isfinite(a)) for a in arrays):
        raise ValueError("Non-finite required values in official source")
    if len(set(event_id.tolist())) != len(event_id) or len(set(group_id.tolist())) != len(group_id):
        raise ValueError("Native event/group identifiers are not unique within product")

    gid_to_fid = {int(g): int(f) for g, f in zip(group_id, group_fid)}
    valid_flashes = {int(f) for f, q in zip(flash_id, flash_q) if int(q) == 0}
    valid_groups = {
        int(g) for g, f, q in zip(group_id, group_fid, group_q)
        if int(q) == 0 and int(f) in valid_flashes
    }
    group_meta = {
        int(g): (float(t), float(la), float(lo))
        for g, t, la, lo in zip(group_id, group_t, group_lat, group_lon)
        if int(g) in valid_groups
    }
    grouped: dict[int, list[Event]] = {g: [] for g in valid_groups}
    for eid, gid, t, la, lo, en in zip(
        event_id, event_gid, event_t, event_lat, event_lon, event_energy
    ):
        g = int(gid)
        if g not in valid_groups:
            continue
        grouped[g].append(
            Event(int(eid), g, gid_to_fid[g], float(t), float(la), float(lo), float(en))
        )

    by_flash: dict[int, dict[int, list[Event]]] = {}
    for gid, events in grouped.items():
        if not events:
            continue
        by_flash.setdefault(gid_to_fid[gid], {})[gid] = sorted(events, key=lambda e: e.eid)

    flashes: dict[int, Flash] = {}
    for fid, groups in by_flash.items():
        eligible = {g: ev for g, ev in groups.items() if 1 <= len(ev) <= 10}
        if len(eligible) < 3 or not any(len(ev) >= 2 for ev in eligible.values()):
            continue
        metas = [group_meta[g] for g in eligible]
        flashes[fid] = Flash(
            fid=fid,
            groups=eligible,
            time_s=float(np.median([m[0] for m in metas])),
            lat=float(np.mean([m[1] for m in metas])),
            lon=float(np.mean([m[2] for m in metas])),
        )
    return flashes


def _km_distance(a: Flash, b: Flash) -> float:
    lat0 = math.radians(0.5 * (a.lat + b.lat))
    dx = 111.32 * math.cos(lat0) * (a.lon - b.lon)
    dy = 110.57 * (a.lat - b.lat)
    return math.hypot(dx, dy)


def _flash_proximity(a: Flash, b: Flash) -> float:
    return math.sqrt((_km_distance(a, b) / 42.0) ** 2 + (abs(a.time_s - b.time_s) / 1.2) ** 2)


def _select_group_events(flash: Flash, source_key: str, case_no: int) -> list[list[Event]]:
    groups = sorted(
        flash.groups.values(),
        key=lambda ev: (float(np.mean([e.time_s for e in ev])), ev[0].gid),
    )
    rng = np.random.default_rng(_stable_seed(source_key, case_no, flash.fid, "groups"))
    start = int(rng.integers(0, max(1, len(groups) - 2)))
    rolled = groups[start:] + groups[:start]
    chosen: list[list[Event]] = []
    total = 0
    for events in rolled:
        if len(chosen) >= 5:
            break
        if total + len(events) > 18 and len(chosen) >= 2:
            continue
        chosen.append(events)
        total += len(events)
        if len(chosen) >= 3 and total >= 7:
            break
    if len(chosen) < 2 or total < 4:
        return []
    return chosen


def _pair_flashes(flashes: dict[int, Flash], source_key: str) -> list[tuple[Flash, Flash]]:
    ordered = sorted(
        flashes.values(),
        key=lambda f: _hash_text(f"{CASE_SALT}:{source_key}:{f.fid}"),
    )
    used: set[int] = set()
    pairs: list[tuple[Flash, Flash]] = []
    for anchor in ordered:
        if anchor.fid in used:
            continue
        candidates = [
            other for other in ordered
            if other.fid not in used and other.fid != anchor.fid
        ]
        candidates.sort(key=lambda f: (_flash_proximity(anchor, f), f.fid))
        # Distinct native flashes cannot be too close under the operational
        # metric. Keep the nearest available hard decoy, but reject unrelated
        # full-disk pairs that would make the hierarchy trivial.
        partner = next(
            (f for f in candidates if _flash_proximity(anchor, f) <= 3.6 and _km_distance(anchor, f) <= 115.0),
            None,
        )
        if partner is None:
            continue
        used.add(anchor.fid)
        used.add(partner.fid)
        pairs.append((anchor, partner))
        if len(pairs) >= CASES_PER_SOURCE * 2:
            break
    return pairs


def _alias(prefix: str, *parts: object, n: int = 12) -> str:
    digest = _hash_text(":".join(str(p) for p in (CASE_SALT, *parts)))
    return prefix + digest[:n]


def _public_features(events: list[Event], source_key: str, case_no: int) -> list[dict]:
    rng = np.random.default_rng(_stable_seed(source_key, case_no, "features"))
    lat = np.asarray([e.lat for e in events], dtype=np.float64)
    lon = np.asarray([e.lon for e in events], dtype=np.float64)
    tim = np.asarray([e.time_s for e in events], dtype=np.float64)
    energy = np.asarray([max(e.energy, 0.0) for e in events], dtype=np.float64)

    lat0 = float(np.mean(lat))
    x = 111.32 * math.cos(math.radians(lat0)) * (lon - float(np.mean(lon)))
    y = 110.57 * (lat - float(np.mean(lat)))
    angle = float(rng.uniform(-math.pi, math.pi))
    ca, sa = math.cos(angle), math.sin(angle)
    xr = ca * x - sa * y
    yr = sa * x + ca * y
    if rng.random() < 0.5:
        xr = -xr
    shear = float(rng.uniform(-0.22, 0.22))
    xr = xr + shear * yr
    scale = max(float(np.percentile(np.hypot(xr, yr), 90)), 8.0)
    xr = np.tanh(xr / (1.15 * scale))
    yr = np.tanh(yr / (1.15 * scale))

    span = max(float(np.percentile(tim, 95) - np.percentile(tim, 5)), 0.25)
    tr = (tim - float(np.percentile(tim, 5))) / span
    tr = np.clip(tr, -0.2, 1.2)

    # Redaction deliberately blurs the operational 2-ms frame and 16.5-km /
    # 330-ms thresholds while preserving learnable local ordering and shape.
    xr = xr + rng.normal(0.0, 0.075, len(events))
    yr = yr + rng.normal(0.0, 0.075, len(events))
    tr = tr + rng.normal(0.0, 0.055, len(events))

    loge = np.log1p(energy)
    order = np.argsort(np.argsort(loge, kind="stable"), kind="stable")
    erank = (order + 0.5) / len(events)
    en = np.clip(0.12 + 0.76 * erank + rng.normal(0.0, 0.035, len(events)), 0.0, 1.0)

    xyz = np.column_stack([xr, yr, 0.72 * tr])
    dist = np.linalg.norm(xyz[:, None, :] - xyz[None, :, :], axis=2)
    local_density = (np.sum(dist < 0.24, axis=1) - 1) / max(1, len(events) - 1)
    time_density = (np.sum(np.abs(tr[:, None] - tr[None, :]) < 0.10, axis=1) - 1) / max(1, len(events) - 1)

    rows = []
    for i, event in enumerate(events):
        did = _alias("d", source_key, case_no, event.fid, event.gid, event.eid, n=10)
        rows.append({
            "id": did,
            "x_rel": round(float(xr[i]), 4),
            "y_rel": round(float(yr[i]), 4),
            "t_rel": round(float(tr[i]), 4),
            "energy_norm": round(float(en[i]), 4),
            "local_density": round(float(local_density[i]), 4),
            "temporal_density": round(float(time_density[i]), 4),
        })
    return rows


def _uncertain_ids(public_rows: list[dict], events: list[Event]) -> list[str]:
    ids = [r["id"] for r in public_rows]
    z = np.asarray(
        [[r["x_rel"], r["y_rel"], 0.72 * r["t_rel"], 0.20 * r["energy_norm"]] for r in public_rows],
        dtype=np.float64,
    )
    d = np.linalg.norm(z[:, None, :] - z[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    group = np.asarray([e.gid for e in events], dtype=np.int64)
    flash = np.asarray([e.fid for e in events], dtype=np.int64)
    margins = np.full(len(events), np.inf, dtype=np.float64)
    for i in range(len(events)):
        same_g = d[i, group == group[i]]
        cross_g = d[i, group != group[i]]
        same_f = d[i, flash == flash[i]]
        cross_f = d[i, flash != flash[i]]
        candidates = []
        if np.isfinite(same_g).any() and np.isfinite(cross_g).any():
            candidates.append(float(np.min(cross_g) - np.min(same_g)))
        if np.isfinite(same_f).any() and np.isfinite(cross_f).any():
            candidates.append(float(np.min(cross_f) - np.min(same_f)))
        if candidates:
            margins[i] = min(candidates)
    finite = margins[np.isfinite(margins)]
    if not len(finite):
        return []
    threshold = min(0.10, float(np.quantile(finite, 0.22)))
    selected = [ids[i] for i, m in enumerate(margins) if np.isfinite(m) and m <= threshold]
    cap = max(1, int(math.ceil(0.35 * len(events))))
    if len(selected) > cap:
        selected = [ids[i] for i in np.argsort(margins)[:cap]]
    return sorted(selected)


def _target_json(public_rows: list[dict], events: list[Event], uncertain: list[str]) -> str:
    by_event = {e.eid: r["id"] for e, r in zip(events, public_rows)}
    group_members: dict[int, list[str]] = {}
    group_flash: dict[int, int] = {}
    for event in events:
        group_members.setdefault(event.gid, []).append(by_event[event.eid])
        group_flash[event.gid] = event.fid
    ordered_groups = sorted(group_members, key=lambda g: min(group_members[g]))
    group_alias = {g: f"g{i + 1}" for i, g in enumerate(ordered_groups)}
    groups = [
        {"group_id": group_alias[g], "detections": sorted(group_members[g])}
        for g in ordered_groups
    ]
    flash_groups: dict[int, list[str]] = {}
    for gid in ordered_groups:
        flash_groups.setdefault(group_flash[gid], []).append(group_alias[gid])
    ordered_flashes = sorted(flash_groups, key=lambda f: min(flash_groups[f]))
    flashes = [
        {"flash_id": f"f{i + 1}", "groups": sorted(flash_groups[f])}
        for i, f in enumerate(ordered_flashes)
    ]
    return _json({"groups": groups, "flashes": flashes, "uncertain_detections": sorted(uncertain)})


def _sample_prediction(case_obj: dict) -> str:
    detections = sorted(case_obj["detections"], key=lambda r: (r["t_rel"], r["x_rel"], r["id"]))
    groups = []
    for i in range(0, len(detections), 2):
        groups.append({
            "group_id": f"g{i // 2 + 1}",
            "detections": sorted(r["id"] for r in detections[i:i + 2]),
        })
    flashes = []
    for i in range(0, len(groups), 2):
        flashes.append({
            "flash_id": f"f{i // 2 + 1}",
            "groups": [g["group_id"] for g in groups[i:i + 2]],
        })
    k = max(1, int(round(0.18 * len(detections))))
    uncertain = sorted(
        (r["id"] for r in sorted(detections, key=lambda r: (-r["local_density"], r["id"]))[:k])
    )
    return _json({"groups": groups, "flashes": flashes, "uncertain_detections": uncertain})


def _build_source_cases(item: dict, flashes: dict[int, Flash]) -> list[dict]:
    source_key = str(item["key"])
    pairs = _pair_flashes(flashes, source_key)
    cases: list[dict] = []
    for pair_no, (fa, fb) in enumerate(pairs):
        selected = []
        for flash in (fa, fb):
            selected.extend(_select_group_events(flash, source_key, pair_no))
        events = [event for group in selected for event in group]
        if not (MIN_DETECTIONS <= len(events) <= MAX_DETECTIONS):
            continue
        if len({e.gid for e in events}) < 5 or len({e.fid for e in events}) != 2:
            continue
        if sum(len(v) >= 2 for v in selected) < 2:
            continue

        # Stable event order for feature generation, then publish rows sorted by
        # opaque detection id so raw time/order cannot leak through JSON order.
        events = sorted(events, key=lambda e: (e.fid, e.gid, e.eid))
        public_rows = _public_features(events, source_key, pair_no)
        uncertain = _uncertain_ids(public_rows, events)
        if len(uncertain) == 0 or len(uncertain) > int(math.ceil(0.40 * len(events))):
            continue
        target = _target_json(public_rows, events, uncertain)
        case_id = _alias("case_", source_key, pair_no, fa.fid, fb.fid, n=14)
        case_obj = {
            "case_id": case_id,
            "detections": sorted(public_rows, key=lambda r: r["id"]),
        }
        ratio = len(uncertain) / len(events)
        cases.append({
            "id": case_id,
            "case_json": _json(case_obj),
            "prompt": PROMPT,
            "target_json": target,
            "sample_json": _sample_prediction(case_obj),
            "source_window": source_key,
            "density_bucket": "compact" if len(events) <= 15 else "dense",
            "ambiguity_bucket": "lower" if ratio < 0.24 else "higher",
            "n_detections": len(events),
            "n_groups": len({e.gid for e in events}),
            "n_flashes": 2,
        })
        if len(cases) >= CASES_PER_SOURCE:
            break
    if len(cases) < CASES_PER_SOURCE:
        raise ValueError(
            f"Only {len(cases)} valid cases could be built from {source_key}; "
            f"expected {CASES_PER_SOURCE}"
        )
    return cases


def _assert_clean_frames(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> None:
    if train.isna().any().any() or test.isna().any().any() or answers.isna().any().any():
        raise ValueError("Prepared tables contain missing values")
    if train["id"].duplicated().any() or test["id"].duplicated().any():
        raise ValueError("Prepared public ids are not unique")
    if set(train["id"]) & set(test["id"]):
        raise ValueError("Train/test id overlap")
    if set(test["id"]) != set(answers["id"]):
        raise ValueError("Private answer ids do not match test ids")
    forbidden = ("source", "file", "time_coverage", "latitude", "longitude", "event_id", "group_id", "flash_id")
    for frame in (train, test):
        for col in frame.columns:
            if any(token in col.lower() for token in forbidden):
                raise ValueError(f"Leak-prone public column: {col}")

    for axis in ("source_window", "density_bucket", "ambiguity_bucket"):
        counts = answers[axis].value_counts()
        if counts.empty or int(counts.min()) < MIN_GROUP_TEST:
            raise ValueError(f"Private subgroup {axis} below MIN_GROUP_TEST: {counts.to_dict()}")


def _write_csv(path: Path, rows: Iterable[dict], columns: list[str]) -> None:
    frame = pd.DataFrame(list(rows), columns=columns).sort_values("id").reset_index(drop=True)
    frame.to_csv(path, index=False, lineterminator="\n")


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw, public, private = Path(raw), Path(public), Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    all_cases: list[dict] = []
    for item, path in _locate_sources(raw):
        flashes = _load_flashes(item, path)
        cases = _build_source_cases(item, flashes)
        for case in cases:
            case["split"] = item["split"]
        all_cases.extend(cases)

    if len({c["id"] for c in all_cases}) != len(all_cases):
        raise ValueError("Opaque case-id collision")
    all_detection_ids: list[str] = []
    for case in all_cases:
        obj = json.loads(case["case_json"])
        all_detection_ids.extend(d["id"] for d in obj["detections"])
    if len(set(all_detection_ids)) != len(all_detection_ids):
        raise ValueError("Opaque detection-id collision")

    train_cases = [c for c in all_cases if c["split"] == "train"]
    test_cases = [c for c in all_cases if c["split"] == "test"]
    train_rows = [
        {"id": c["id"], "case_json": c["case_json"], "prompt": c["prompt"], "target_json": c["target_json"]}
        for c in train_cases
    ]
    test_rows = [
        {"id": c["id"], "case_json": c["case_json"], "prompt": c["prompt"]}
        for c in test_cases
    ]
    sample_rows = [
        {"id": c["id"], "prediction_json": c["sample_json"], "confidence": 0.20}
        for c in test_cases
    ]
    answer_rows = [
        {
            "id": c["id"],
            "target_json": c["target_json"],
            "source_window": c["source_window"],
            "density_bucket": c["density_bucket"],
            "ambiguity_bucket": c["ambiguity_bucket"],
            "n_detections": c["n_detections"],
            "n_groups": c["n_groups"],
            "n_flashes": c["n_flashes"],
        }
        for c in test_cases
    ]

    train_df = pd.DataFrame(train_rows).sort_values("id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows).sort_values("id").reset_index(drop=True)
    answers_df = pd.DataFrame(answer_rows).sort_values("id").reset_index(drop=True)
    _assert_clean_frames(train_df, test_df, answers_df)

    _write_csv(public / "train.csv", train_rows, ["id", "case_json", "prompt", "target_json"])
    _write_csv(public / "test.csv", test_rows, ["id", "case_json", "prompt"])
    _write_csv(public / "sample_submission.csv", sample_rows, ["id", "prediction_json", "confidence"])
    _write_csv(
        private / "answers.csv",
        answer_rows,
        ["id", "target_json", "source_window", "density_bucket", "ambiguity_bucket", "n_detections", "n_groups", "n_flashes"],
    )

    print(
        f"Prepared {len(train_rows)} train and {len(test_rows)} test hierarchy cases "
        f"from {len(MANIFEST)} verified official files."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)
