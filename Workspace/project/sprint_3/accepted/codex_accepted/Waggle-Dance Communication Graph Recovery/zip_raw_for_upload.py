from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


DEFAULT_STAGING = Path("official_raw_subset")
DEFAULT_OUTPUT = Path("waggle_dance_raw_subset.zip")


def zip_raw_for_upload(staging: Path = DEFAULT_STAGING, output: Path = DEFAULT_OUTPUT) -> None:
    staging = Path(staging)
    output = Path(output)
    if not staging.exists():
        raise SystemExit(
            f"{staging} does not exist. Run build_source_subset_zip.py first, "
            "or pass --staging to an extracted clean raw subset directory."
        )
    forbidden = {"public", "private", "__pycache__", ".git"}
    files = []
    for path in staging.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(staging).parts)
        if parts & forbidden:
            raise SystemExit(f"Refusing to package forbidden path: {path}")
        files.append(path)
    if not files:
        raise SystemExit("No raw files found to zip")
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(files):
            zf.write(path, path.relative_to(staging).as_posix())
    print(f"Wrote {output} ({output.stat().st_size / 1_000_000:.1f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Zip the clean raw source subset for upload.")
    parser.add_argument("--staging", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    zip_raw_for_upload(args.staging, args.output)


if __name__ == "__main__":
    main()
