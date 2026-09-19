"""
zip_raw_for_upload.py - package the raw corpus into a FLAT zip for the platform
uploader.

The platform expects the raw data files at the ROOT of the archive (no
enclosing `raw_data/` folder). This script zips the contents of the raw folder
so that the archive members are:

    images/<scene_hash>.png
    scenes.csv
    blocks.csv

Usage:
    python zip_raw_for_upload.py --raw raw_data --out collapse_raw.zip
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--out", type=Path, default=Path("collapse_raw.zip"))
    args = ap.parse_args()

    raw = args.raw.resolve()
    if not raw.exists():
        raise SystemExit(f"raw folder not found: {raw}")

    members = sorted(p for p in raw.rglob("*") if p.is_file())
    if not members:
        raise SystemExit(f"no files under {raw}")

    with zipfile.ZipFile(args.out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in members:
            # arcname is the path RELATIVE to raw/, so the zip is flat at root.
            z.write(p, arcname=str(p.relative_to(raw)))
    print(f"OK: wrote {args.out} with {len(members)} files (flat at archive root).")


if __name__ == "__main__":
    main()
