#!/usr/bin/env python3
"""Create a clean raw_upload.zip containing only official raw source files.

The input files are official upstream sequence ZIPs. The output archive exposes
their unchanged Euroc-style members directly, so the platform raw tree contains
camera PNGs and sensor CSVs rather than a zip-of-zips.
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from generate import SOURCES


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="raw_sources")
    parser.add_argument("--output", default="raw_upload.zip")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_path = Path(args.output)
    expected = {s["name"]: s["size"] for s in SOURCES}
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for name, size in expected.items():
            src = raw_dir / name
            if not src.exists():
                raise SystemExit(f"missing official raw file: {src}")
            if src.stat().st_size != size:
                raise SystemExit(f"size mismatch for {src}")
            with zipfile.ZipFile(src) as inner:
                for info in inner.infolist():
                    if info.is_dir():
                        z.writestr(info.filename, b"")
                    else:
                        with inner.open(info) as f:
                            z.writestr(info.filename, f.read())
    print(f"wrote {out_path} with official raw members from {len(expected)} sequence ZIPs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
