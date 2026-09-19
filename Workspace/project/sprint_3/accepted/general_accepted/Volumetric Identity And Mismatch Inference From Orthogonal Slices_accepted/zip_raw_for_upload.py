"""
Build VolumetricIdentity_RAW_upload.zip for the platform "Data Files" uploader.

The zip root must contain ONLY the six MedMNIST3D `.npz` files at the archive
root — no nested raw_data/ folder, no .py, no README.

Usage
-----
1) Generate raw_data/ first:
       pip install requests numpy
       python generate.py --out raw_data

2) Create the zip next to this script:
       python zip_raw_for_upload.py
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


REQUIRED = (
    "organmnist3d.npz",
    "nodulemnist3d.npz",
    "adrenalmnist3d.npz",
    "fracturemnist3d.npz",
    "vesselmnist3d.npz",
    "synapsemnist3d.npz",
)
_ALLOWED = re.compile(r"^[a-z]+mnist3d\.npz$")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path(__file__).parent / "raw_data")
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "VolumetricIdentity_RAW_upload.zip")
    args = ap.parse_args()
    raw: Path = args.raw.resolve()
    if not raw.is_dir():
        print(f"ERROR: missing {raw}", file=sys.stderr)
        sys.exit(1)

    missing = [f for f in REQUIRED if not (raw / f).is_file()]
    if missing:
        print("ERROR: raw_data/ is missing required source files:", file=sys.stderr)
        for f in missing:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)

    out_zip: Path = args.out.resolve()
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    if out_zip.is_file():
        out_zip.unlink()

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_STORED) as zf:
        for fname in REQUIRED:
            src = raw / fname
            print(f"[zip] adding {fname}  ({src.stat().st_size / 1e6:.1f} MB)")
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
    if bad or set(REQUIRED) - seen:
        out_zip.unlink(missing_ok=True)
        print("ERROR: archive layout incorrect", file=sys.stderr)
        if bad:
            for b in bad[:20]:
                print(f"  unexpected: {b}", file=sys.stderr)
        for m in sorted(set(REQUIRED) - seen):
            print(f"  missing: {m}", file=sys.stderr)
        sys.exit(1)

    mb = out_zip.stat().st_size / 1e6
    print(f"OK: {out_zip}  ({len(REQUIRED)} archives, ~{mb:.1f} MB)")


if __name__ == "__main__":
    main()
