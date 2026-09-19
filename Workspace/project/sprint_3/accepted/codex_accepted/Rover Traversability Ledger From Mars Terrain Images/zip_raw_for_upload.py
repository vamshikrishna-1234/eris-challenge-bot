"""Package only the byte-identical selected official AI4Mars source files."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT_NAME = "ai4mars-dataset-merged-0.6"
EXPECTED_FILES = 2 * (322 + 204) + 7
MAX_BYTES = 1_000_000_000


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--output", type=Path, default=Path("ai4mars_official_expert_subset.zip"))
    args = parser.parse_args()
    source = args.raw / ROOT_NAME
    if not source.is_dir():
        raise SystemExit(f"Missing official source directory: {source}")
    files = sorted(path for path in source.rglob("*") if path.is_file())
    if len(files) != EXPECTED_FILES:
        raise SystemExit(f"Expected {EXPECTED_FILES} official files, found {len(files)}")
    total = sum(path.stat().st_size for path in files)
    if total >= MAX_BYTES:
        raise SystemExit(f"Official subset is too large: {total} bytes")
    forbidden = {"train.csv", "sample_submission.csv", "answers.csv", "prepare.py", "grade.py"}
    if any(path.name in forbidden for path in files):
        raise SystemExit("Derived challenge file found in raw source tree")
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
        for path in files:
            archive.write(path, arcname=path.relative_to(args.raw).as_posix())
    print(f"OK: {args.output} contains {len(files)} untouched official files; raw bytes={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
