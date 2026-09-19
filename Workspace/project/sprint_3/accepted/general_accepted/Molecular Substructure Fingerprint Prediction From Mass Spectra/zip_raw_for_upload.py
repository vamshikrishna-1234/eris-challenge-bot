"""
Build FragmentFold_RAW_upload.zip for the platform "Data Files" uploader.

The zip root must contain ONLY `spectra.csv` at the archive root — no nested
raw_data/ folder, no .py, no .msp.

Usage
-----
1) Generate the raw CSV first:
       pip install requests rdkit numpy
       python generate.py --out raw_data

2) Create the zip next to this script:
       python zip_raw_for_upload.py
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

REQUIRED = ("spectra.csv",)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path(__file__).parent / "raw_data")
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "FragmentFold_RAW_upload.zip")
    args = ap.parse_args()
    raw = args.raw.resolve()

    missing = [f for f in REQUIRED if not (raw / f).is_file()]
    if missing:
        print(f"ERROR: missing {missing} in {raw}. Run generate.py first.", file=sys.stderr)
        sys.exit(1)

    out_zip = args.out.resolve()
    if out_zip.is_file():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for fname in REQUIRED:
            src = raw / fname
            print(f"[zip] adding {fname}  ({src.stat().st_size/1e6:.1f} MB)")
            zf.write(str(src), arcname=fname)

    with zipfile.ZipFile(out_zip, "r") as zf:
        members = [m for m in zf.namelist() if not m.endswith("/")]
    if sorted(members) != sorted(REQUIRED):
        out_zip.unlink(missing_ok=True)
        print(f"ERROR: archive layout wrong: {members}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {out_zip}  ({out_zip.stat().st_size/1e6:.1f} MB, flat root)")


if __name__ == "__main__":
    main()
