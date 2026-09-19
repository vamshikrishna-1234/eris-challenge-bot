"""Package raw_data/ into a FLAT zip for the platform uploader.

Produces:  tangle_raw.zip
Contents (flat at archive root):  scenes.csv  +  images/<scene_hash>.jpg

Usage:  python zip_raw_for_upload.py [--raw raw_data] [--out tangle_raw.zip]
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--out", type=Path, default=Path("tangle_raw.zip"))
    args = ap.parse_args()

    raw = args.raw.resolve()
    out = args.out.resolve()
    csv = raw / "scenes.csv"
    files = sorted((raw / "images").glob("*.jpg"))

    if not csv.exists():
        raise FileNotFoundError(f"scenes.csv not found in {raw}")
    if not files:
        raise FileNotFoundError(f"no .jpg files in {raw / 'images'}")

    print(f"Packaging {len(files)} images + scenes.csv -> {out}")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv, "scenes.csv")
        for f in files:
            zf.write(f, f"images/{f.name}")
    print(f"Done. {out.name}  ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
