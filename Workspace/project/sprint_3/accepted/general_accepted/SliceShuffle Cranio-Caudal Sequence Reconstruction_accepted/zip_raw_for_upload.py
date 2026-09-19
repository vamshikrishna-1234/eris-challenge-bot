"""
Build SliceShuffle_RAW_upload.zip for the platform "Data Files" uploader.

The zip root must contain ONLY:

    volumes.npz
    manifest.csv

No nested folders, no .py, no README. prepare.py consumes these two
files on the platform side and produces public/ + private/.

Do NOT zip the whole challenge folder in Explorer / 7-Zip. That puts
.py files in the archive and platform validation will fail. Always
run this script so the archive contains the pristine pre-processed
source files only.

Usage
-----
1) Generate raw_data/ first:
       pip install nibabel numpy pillow
       python generate.py --ixi-dir D:/datasets/IXI-T1 --out raw_data

2) Create the zip next to this script:
       python zip_raw_for_upload.py
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


REQUIRED_FILES = ["volumes.npz", "manifest.csv"]
_ALLOWED = re.compile(r"^(volumes\.npz|manifest\.csv)$")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--raw",
        type=Path,
        default=Path(__file__).parent / "raw_data",
        help="Folder containing volumes.npz + manifest.csv.",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent / "SliceShuffle_RAW_upload.zip",
        help="Output zip path.",
    )
    args = ap.parse_args()
    raw: Path = args.raw.resolve()
    if not raw.is_dir():
        print(f"ERROR: missing {raw}", file=sys.stderr)
        print("Run:  python generate.py --ixi-dir <path> --out raw_data", file=sys.stderr)
        sys.exit(1)

    missing = [f for f in REQUIRED_FILES if not (raw / f).is_file()]
    if missing:
        print("ERROR: raw_data/ is missing required source files:", file=sys.stderr)
        for f in missing:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)

    extras = [
        p.name for p in raw.iterdir()
        if p.is_file() and p.name not in REQUIRED_FILES
    ]
    if extras:
        print(
            "ERROR: raw_data/ contains unexpected files -- aborting to keep "
            "the upload zip pristine:",
            file=sys.stderr,
        )
        for e in extras:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    out_zip: Path = args.out.resolve()
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    if out_zip.is_file():
        out_zip.unlink()

    # STORED: volumes.npz is already zlib-compressed internally.
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_STORED) as zf:
        for fname in REQUIRED_FILES:
            src = raw / fname
            print(f"[zip] adding {fname}  ({src.stat().st_size / 1e9:.2f} GB)")
            zf.write(str(src), arcname=fname)

    bad: list[str] = []
    seen: set[str] = set()
    with zipfile.ZipFile(out_zip, "r") as zf:
        for info in zf.infolist():
            name = info.filename.replace("\\", "/")
            if name.endswith("/"):
                continue
            if not _ALLOWED.match(name):
                bad.append(name)
            else:
                seen.add(name)
    missing_in_zip = sorted(set(REQUIRED_FILES) - seen)
    if bad or missing_in_zip:
        out_zip.unlink(missing_ok=True)
        if bad:
            print("ERROR: archive has unexpected members:", file=sys.stderr)
            for b in bad[:20]:
                print(f"  {b}", file=sys.stderr)
        if missing_in_zip:
            print("ERROR: archive is missing required members:", file=sys.stderr)
            for m in missing_in_zip:
                print(f"  {m}", file=sys.stderr)
        sys.exit(1)

    size_gb = out_zip.stat().st_size / 1e9
    print(f"OK: {out_zip}  ({len(REQUIRED_FILES)} source files, {size_gb:.2f} GB)")
    print("Upload ONLY this zip; it contains no .py, no README, no challenge-specific images.")


if __name__ == "__main__":
    main()
