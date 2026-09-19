"""
zip_raw_for_upload.py - package raw_data/ into a FLAT zip for the platform.

The platform raw-data uploader expects the raw source files at the ROOT of the
archive (not wrapped in a raw_data/ parent). This writes each member with an
arcname relative to raw_data/, so the archive root contains:

    videos/<scene_hash>.mp4 ...
    scenes.csv

Usage:  python zip_raw_for_upload.py --raw raw_data --out cogchain_raw.zip
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--out", type=Path, default=Path("cogchain_raw.zip"))
    args = ap.parse_args()

    raw = args.raw.resolve()
    if not raw.exists():
        raise SystemExit(f"raw dir not found: {raw}")

    files = sorted(p for p in raw.rglob("*") if p.is_file())
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, arcname=str(p.relative_to(raw)))
    size_mb = args.out.stat().st_size / (1024 * 1024)
    print(f"OK: wrote {args.out} with {len(files)} files (flat at archive root), {size_mb:.1f} MB.")


if __name__ == "__main__":
    main()
