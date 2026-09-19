"""
generate.py — build the raw upload bundle for Volumetric Identity.

Downloads the six MedMNIST v3 (MedMNIST+) 3D archives at the canonical 28-cube
resolution from the official Zenodo record (10.5281/zenodo.10519652), into a
local `raw_data/` folder. Each archive is a NumPy zip carrying the upstream
train / val / test split as `train_images`, `train_labels`, `val_images`,
`val_labels`, `test_images`, `test_labels`.

License: CC-BY 4.0 (MedMNIST v2/v3). Total raw upload ~100 MB.

Usage
-----
    pip install requests
    python generate.py --out raw_data
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

import requests


ZENODO_RECORD = "10519652"

ARCHIVES = (
    "organmnist3d.npz",
    "nodulemnist3d.npz",
    "adrenalmnist3d.npz",
    "fracturemnist3d.npz",
    "vesselmnist3d.npz",
    "synapsemnist3d.npz",
)

ZENODO_URL_FMT = "https://zenodo.org/api/records/{rec}/files/{name}/content"
CHUNK = 1 << 20


def _download_one(url: str, dst: Path, max_retries: int = 3) -> None:
    if dst.exists() and dst.stat().st_size > 0:
        print(f"  [skip] {dst.name} already present ({dst.stat().st_size / 1e6:.1f} MB)")
        return
    last_exc: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            t0 = time.time()
            with requests.get(url, stream=True, timeout=120) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                tmp = dst.with_suffix(dst.suffix + ".part")
                got = 0
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=CHUNK):
                        if chunk:
                            f.write(chunk)
                            got += len(chunk)
                tmp.replace(dst)
            dt = time.time() - t0
            mb = dst.stat().st_size / 1e6
            print(f"  [done] {dst.name}  {mb:.1f} MB in {dt:.1f}s")
            return
        except Exception as e:
            last_exc = e
            print(f"  [retry {attempt}/{max_retries}] {dst.name}: {e}")
            time.sleep(2 * attempt)
    raise RuntimeError(f"failed to download {url}: {last_exc}")


def _verify_npz(path: Path) -> None:
    import numpy as np
    with np.load(path) as z:
        keys = set(z.files)
    need = {"train_images", "train_labels", "val_images", "val_labels",
            "test_images", "test_labels"}
    if not need.issubset(keys):
        raise ValueError(f"{path.name} missing keys; have {sorted(keys)}")


def generate(out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [plan] {len(ARCHIVES)} MedMNIST3D archives -> {out_dir}")

    for name in ARCHIVES:
        url = ZENODO_URL_FMT.format(rec=ZENODO_RECORD, name=name)
        dst = out_dir / name
        _download_one(url, dst)
        _verify_npz(dst)

    total = sum((out_dir / n).stat().st_size for n in ARCHIVES) / 1e6
    print(f"  [ok] {len(ARCHIVES)} archives, total {total:.1f} MB at {out_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    args = ap.parse_args()
    try:
        generate(args.out)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
