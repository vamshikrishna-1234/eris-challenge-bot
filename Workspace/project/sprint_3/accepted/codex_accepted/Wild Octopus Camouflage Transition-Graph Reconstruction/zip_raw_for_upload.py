"""Build the clean untouched-official-files-only transport archive."""

from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from pathlib import Path

from generate import source_objects


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def build(source: Path, output: Path) -> None:
    source, output = Path(source), Path(output)
    objects = source_objects()
    expected = {str(obj["path"]): obj for obj in objects}
    actual = {path.relative_to(source).as_posix(): path for path in source.rglob("*") if path.is_file()}
    partials = [name for name in actual if name.endswith(".partial") or name.endswith(".partial.mp4")]
    if partials or set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise RuntimeError(f"Raw tree is not the frozen official-only set; missing={missing[:3]} extra={extra[:3]}")
    total = 0
    for rel, obj in expected.items():
        size = actual[rel].stat().st_size
        if obj.get("bytes") is not None and size != int(obj["bytes"]):
            raise RuntimeError(f"Official byte-count mismatch: {rel}")
        total += size
    if total >= 1_000_000_000:
        raise RuntimeError(f"Official raw files exceed 1 GB: {total}")

    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_name(output.name + ".partial")
    partial.unlink(missing_ok=True)
    with zipfile.ZipFile(partial, "w", allowZip64=True) as archive:
        for rel in sorted(actual):
            method = zipfile.ZIP_STORED if rel.lower().endswith(".avi") else zipfile.ZIP_DEFLATED
            archive.write(actual[rel], arcname=rel, compress_type=method, compresslevel=None if method == zipfile.ZIP_STORED else 9)
    os.replace(partial, output)

    with zipfile.ZipFile(output, "r") as archive:
        names = archive.namelist()
        if names != sorted(expected) or any(name.startswith(("public/", "private/", "raw_data/")) for name in names):
            raise RuntimeError("Archive member audit failed")
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"Archive CRC validation failed: {bad}")
    print(f"archive={output}")
    print(f"members={len(expected)} untouched_bytes={total} archive_bytes={output.stat().st_size}")
    print(f"sha256={_sha256(output)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("OFFICIAL_RAW_FILES_ONLY.zip"))
    args = parser.parse_args()
    build(args.source, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
