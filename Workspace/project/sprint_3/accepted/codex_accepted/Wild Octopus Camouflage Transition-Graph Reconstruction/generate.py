"""Acquire the untouched official MEVA source subset used by this real-data challenge.

This is intentionally an acquisition/verifier, not a synthetic generator.  It never
clips, decodes, renames, recodes, annotates, or derives participant assets.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


S3_ROOT = "https://mevadata-public-01.s3.amazonaws.com/"
# Pinned repository commit keeps annotation/document URLs stable.
GIT_ROOT = "https://gitlab.kitware.com/meva/meva-data-repo/-/raw/421841a75577b697c314e952e585aecbb1b99e17/"

# base name, exact official byte count, S3 multipart ETag (or single-part MD5)
VIDEO_SOURCES = [
    ("2018-03-12.11-05-01.11-10-01.school.G423", 71953582, "4d897bec25c267acf1a4dc193072ff33-9"),
    ("2018-03-12.10-00-00.10-05-00.school.G420", 70660918, "c8179f08981d26a02f9b9e996db5b336-9"),
    ("2018-03-11.11-50-00.11-54-59.school.G423", 81534972, "09da3f8ce69aee51910fb67e292cf38b-10"),
    ("2018-03-11.17-10-01.17-15-01.school.G419", 85201548, "decdd286cdf1becf76c15bc98ac280b6-11"),
    ("2018-03-11.14-05-00.14-10-00.school.G420", 73922476, "cfdec4e835ec2c2ab5cbd1770c6f3eb7-9"),
    ("2018-03-09.10-10-00.10-15-00.school.G423", 96453698, "89f5cb5451c20d38edeff69cf4e60bd1-12"),
    ("2018-03-09.10-30-01.10-35-01.school.G420", 58329782, "9cf62f7bd455f348ed2a18d4b80663b7-7"),
    ("2018-03-07.17-20-06.17-25-06.school.G424", 108761812, "33dacc29738149212057650178f3a23f-13"),
    ("2018-03-07.11-10-00.11-15-00.school.G420", 61610642, "7df7bd2a0ff99076d95e0788b916fbe0-8"),
    ("2018-03-13.16-30-00.16-35-00.school.G423", 81810710, "eae4919ab05b44e01ba2fe2ea6dd3e65-10"),
    ("2018-03-15.15-15-00.15-20-00.school.G424", 92024426, "19b9ec7219a44bb7a8162354ba20972f-11"),
    ("2018-03-05.13-20-01.13-25-01.bus.G331", 67181226, "fdc321adb1f56aeeae90a70821a029e3-9"),
    ("2018-03-11.11-40-00.11-45-00.school.G474", 3102474, "1cb38ca8a109086c85c170a015ec94b2"),
    ("2018-03-11.11-45-00.11-50-00.school.G474", 2777382, "5b5e2b2e3a99891f2b1968d07378f091"),
    ("2018-03-11.16-15-00.16-20-00.hospital.G479", 1903990, "460bb4dca451599c12d37a2778aa51a7"),
    ("2018-03-11.16-20-00.16-25-00.hospital.G479", 2025392, "94c86bc83002f4db96386adfd1326532"),
    ("2018-03-11.16-30-00.16-35-00.bus.G475", 1819848, "598b9f142beec25e5b43e7b50142b134"),
    ("2018-03-11.16-30-00.16-35-00.hospital.G476", 2048456, "469a6c64ad4e243f04a87a750e0053e5"),
    ("2018-03-11.16-30-00.16-35-00.hospital.G479", 2049446, "dfcf97636242125d439dcc6625a48770"),
    ("2018-03-11.16-30-00.16-35-00.school.G474", 2315510, "8ee1aa00a66c95fb6f553ed739917b93"),
    ("2018-03-11.16-35-00.16-40-00.hospital.G479", 1991690, "e8752b6de4a29118635aaf79755ddc84"),
]

OFFICIAL_REPO_FILES = [
    ("LICENSE", 19055),
    ("README.md", 1206),
    ("annotation/DIVA-phase-2/MEVA/kitware/README.md", 679),
    ("annotation/DIVA-phase-2/MEVA/kitware/list-of-annotated-meva-clips.txt", 31260),
    ("documents/activity-names.txt", 848),
    ("documents/KPF-specification-v4.pdf", 293212),
    ("documents/MEVA-Annotation-Definitions.pdf", 199708),
]


def _video_rel(base: str) -> str:
    return f"drops-123-r13/{base[:10]}/{base[11:13]}/{base}.r13.avi"


def _annotation_rel(base: str, suffix: str) -> str:
    return f"annotation/DIVA-phase-2/MEVA/kitware/{base[:10]}/{base[11:13]}/{base}.{suffix}.yml"


def source_objects() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for base, size, etag in VIDEO_SOURCES:
        rel = _video_rel(base)
        rows.append({"url": S3_ROOT + rel, "path": rel, "bytes": size, "etag": etag})
        for suffix in ("activities", "types"):
            ann = _annotation_rel(base, suffix)
            rows.append({"url": GIT_ROOT + ann, "path": ann, "bytes": None, "etag": None})
    for rel, size in OFFICIAL_REPO_FILES:
        rows.append({"url": GIT_ROOT + rel, "path": rel, "bytes": size, "etag": None})
    return rows


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _download_one(obj: dict[str, object], output: Path, verify_only: bool) -> tuple[str, int, str]:
    dest = output / str(obj["path"])
    expected = obj.get("bytes")
    if dest.exists() and (expected is None or dest.stat().st_size == int(expected)):
        return str(obj["path"]), dest.stat().st_size, _sha256(dest)
    if verify_only:
        raise FileNotFoundError(f"Missing or size-mismatched official file: {obj['path']}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_name(dest.name + ".partial")
    start = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": "MEVA-raw-acquisition/1.0"}
    if start:
        headers["Range"] = f"bytes={start}-"
    request = Request(str(obj["url"]), headers=headers)
    try:
        response = urlopen(request, timeout=120)
    except HTTPError as exc:
        if start and exc.code == 416:
            response = None
        else:
            raise
    if response is not None:
        append = start > 0 and getattr(response, "status", None) == 206
        mode = "ab" if append else "wb"
        if not append:
            start = 0
        with response, partial.open(mode) as handle:
            while True:
                block = response.read(4 * 1024 * 1024)
                if not block:
                    break
                handle.write(block)
    if expected is not None and partial.stat().st_size != int(expected):
        raise IOError(f"Official byte-count mismatch for {obj['path']}")
    os.replace(partial, dest)
    return str(obj["path"]), dest.stat().st_size, _sha256(dest)


def acquire(output: Path, workers: int = 4, verify_only: bool = False) -> None:
    output.mkdir(parents=True, exist_ok=True)
    objects = source_objects()
    results = []
    with ThreadPoolExecutor(max_workers=max(1, min(workers, 8))) as pool:
        futures = {pool.submit(_download_one, obj, output, verify_only): obj for obj in objects}
        for future in as_completed(futures):
            rel, size, digest = future.result()
            results.append((rel, size, digest))
            print(f"verified {rel} ({size} bytes) sha256={digest}")
    total = sum(size for _, size, _ in results)
    if total >= 1_000_000_000:
        raise RuntimeError(f"Raw source subset exceeds the 1 GB limit: {total} bytes")
    print(f"Verified {len(results)} untouched official files; total={total} bytes")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Directory for untouched official files")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    acquire(args.output, args.workers, args.verify_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
