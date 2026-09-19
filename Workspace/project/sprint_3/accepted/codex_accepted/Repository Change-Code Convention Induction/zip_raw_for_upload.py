from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


RAW_FILES = ["records.csv", "attributions.csv", "manifest.json", "LICENSE.txt"]


def build_zip(raw: Path, output: Path) -> None:
    missing = [name for name in RAW_FILES if not (raw / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing raw files: {missing}")
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in RAW_FILES:
            zf.write(raw / name, arcname=name)
    with zipfile.ZipFile(output) as zf:
        names = zf.namelist()
    bad = [n for n in names if n.startswith(("raw_data/", "public/", "private/")) or n.endswith(".py")]
    if bad:
        raise RuntimeError(f"raw_upload.zip contains forbidden members: {bad}")
    print(f"Wrote {output} with {len(names)} flat members.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--output", type=Path, default=Path("raw_upload.zip"))
    args = ap.parse_args()
    build_zip(args.raw, args.output)


if __name__ == "__main__":
    main()
