"""Download an untouched official AI4Mars expert-labelled subset.

This is an official-source acquisition helper, not a synthetic generator.  It
uses HTTP byte ranges to copy selected members out of the official Zenodo ZIP
without downloading the 16.2 GB archive as a whole.  Every materialised file is
byte-for-byte identical to the corresponding official archive member.
"""

from __future__ import annotations

import argparse
import binascii
import http.client
import os
import re
import struct
import time
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError
from urllib.request import Request, urlopen


RECORD_URL = "https://zenodo.org/records/15995036"
ARCHIVE_URL = RECORD_URL + "/files/ai4mars-dataset-merged-0.6.zip?download=1"
ARCHIVE_BYTES = 16_232_481_989
ARCHIVE_MD5 = "daf80a86021253292e6c425f97baa5c6"
ROOT = "ai4mars-dataset-merged-0.6/"
MSL_LABEL_PREFIX = ROOT + "msl/ncam/labels/test/masked-gold-min2-100agree/"
MER_LABEL_PREFIX = ROOT + "mer/labels/test/masked-gold-min2-100agree/"
MSL_IMAGE_PREFIX = ROOT + "msl/ncam/images/edr/"
MER_IMAGE_PREFIX = ROOT + "mer/images/test/"
DOC_MEMBERS = {
    ROOT + "info.md",
    ROOT + "changelog.md",
    ROOT + "label_keys.json",
    ROOT + "msl/NOTE.txt",
    ROOT + "mer/NOTE.txt",
    ROOT + "msl/ncam/labels/test/NOTE.txt",
    ROOT + "mer/labels/test/masked-gold-min3-100agree/test.csv",
}
EXPECTED_MSL_PAIRS = 322
EXPECTED_MER_PAIRS = 204
MAX_RAW_BYTES = 1_000_000_000
MERGE_GAP_BYTES = 1_000_000
MAX_RANGE_BYTES = 64_000_000
USER_AGENT = "Eris-AI4Mars-source-acquisition/1.0"


@dataclass(frozen=True)
class Member:
    name: str
    local_offset: int
    compressed_size: int
    uncompressed_size: int
    method: int
    crc32: int
    central_name_len: int
    central_extra_len: int


def _long_path(path: Path) -> Path:
    absolute = Path(path).resolve()
    text = str(absolute)
    if os.name == "nt" and not text.startswith("\\\\?\\"):
        return Path("\\\\?\\" + text)
    return absolute


def _request_range(start: int, end: int, attempts: int = 8) -> bytes:
    if start < 0 or end < start:
        raise ValueError(f"Invalid byte range {start}-{end}")
    headers = {"Range": f"bytes={start}-{end}", "User-Agent": USER_AGENT}
    for attempt in range(attempts):
        try:
            with urlopen(Request(ARCHIVE_URL, headers=headers), timeout=180) as response:
                data = response.read()
                if len(data) != end - start + 1:
                    raise IOError(
                        f"Short range response for {start}-{end}: got {len(data)} bytes"
                    )
                return data
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt + 1 == attempts:
                raise
            retry = exc.headers.get("Retry-After")
            delay = float(retry) if retry and retry.isdigit() else min(60.0, 2.0 ** attempt)
            time.sleep(delay)
        except (OSError, TimeoutError, http.client.IncompleteRead):
            if attempt + 1 == attempts:
                raise
            time.sleep(min(30.0, 2.0 ** attempt))
    raise RuntimeError("unreachable")


def _archive_length() -> int:
    request = Request(ARCHIVE_URL, method="HEAD", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        size = int(response.headers["Content-Length"])
    if size != ARCHIVE_BYTES:
        raise RuntimeError(f"Official archive size changed: expected {ARCHIVE_BYTES}, got {size}")
    return size


def _central_directory() -> bytes:
    size = _archive_length()
    tail_start = max(0, size - 131_072)
    tail = _request_range(tail_start, size - 1)
    locator_at = tail.rfind(b"PK\x06\x07")
    if locator_at < 0:
        raise RuntimeError("ZIP64 locator not found in official archive")
    _, _, zip64_eocd_offset, _ = struct.unpack_from("<4sIQI", tail, locator_at)
    zip64 = _request_range(zip64_eocd_offset, zip64_eocd_offset + 55)
    values = struct.unpack_from("<4sQHHIIQQQQ", zip64, 0)
    if values[0] != b"PK\x06\x06":
        raise RuntimeError("ZIP64 end-of-central-directory signature mismatch")
    entries = int(values[7])
    cd_size = int(values[8])
    cd_offset = int(values[9])
    if entries != 146_179:
        raise RuntimeError(f"Official member count changed: expected 146179, got {entries}")
    return _request_range(cd_offset, cd_offset + cd_size - 1)


def _parse_members(cd: bytes) -> dict[str, Member]:
    result: dict[str, Member] = {}
    pos = 0
    while pos < len(cd):
        values = struct.unpack_from("<4s6H3I5H2I", cd, pos)
        if values[0] != b"PK\x01\x02":
            raise RuntimeError(f"Bad central-directory signature at {pos}")
        flag = values[3]
        method = values[4]
        crc32 = values[7]
        compressed = values[8]
        uncompressed = values[9]
        name_len = values[10]
        extra_len = values[11]
        comment_len = values[12]
        disk_start = values[13]
        local_offset = values[16]
        start = pos + 46
        codec = "utf-8" if flag & 0x800 else "cp437"
        name = cd[start : start + name_len].decode(codec)
        extra = cd[start + name_len : start + name_len + extra_len]
        cursor = 0
        while cursor + 4 <= len(extra):
            header_id, size = struct.unpack_from("<HH", extra, cursor)
            payload = extra[cursor + 4 : cursor + 4 + size]
            if header_id == 1:
                p = 0
                if uncompressed == 0xFFFFFFFF:
                    uncompressed = struct.unpack_from("<Q", payload, p)[0]
                    p += 8
                if compressed == 0xFFFFFFFF:
                    compressed = struct.unpack_from("<Q", payload, p)[0]
                    p += 8
                if local_offset == 0xFFFFFFFF:
                    local_offset = struct.unpack_from("<Q", payload, p)[0]
                    p += 8
                if disk_start == 0xFFFF:
                    disk_start = struct.unpack_from("<I", payload, p)[0]
            cursor += 4 + size
        result[name] = Member(
            name=name,
            local_offset=int(local_offset),
            compressed_size=int(compressed),
            uncompressed_size=int(uncompressed),
            method=int(method),
            crc32=int(crc32),
            central_name_len=int(name_len),
            central_extra_len=int(extra_len),
        )
        pos = start + name_len + extra_len + comment_len
    return result


def _selected_members(all_members: dict[str, Member]) -> list[Member]:
    msl_labels = sorted(
        n for n in all_members if n.startswith(MSL_LABEL_PREFIX) and n.lower().endswith(".png")
    )
    mer_labels = sorted(
        n for n in all_members if n.startswith(MER_LABEL_PREFIX) and n.lower().endswith(".png")
    )
    if len(msl_labels) != EXPECTED_MSL_PAIRS or len(mer_labels) != EXPECTED_MER_PAIRS:
        raise RuntimeError(
            f"Official expert subset changed: MSL={len(msl_labels)}, MER={len(mer_labels)}"
        )
    names = set(msl_labels + mer_labels) | DOC_MEMBERS
    for label in msl_labels:
        stem = PurePosixPath(label).stem.removesuffix("_merged")
        names.add(MSL_IMAGE_PREFIX + stem + ".JPG")
    for label in mer_labels:
        stem = re.sub(r"_\d+_T\d+_merged$", "", PurePosixPath(label).stem)
        names.add(MER_IMAGE_PREFIX + stem + ".JPG")
    missing = sorted(names - set(all_members))
    if missing:
        raise RuntimeError(f"Selected official members missing: {missing[:5]}")
    selected = [all_members[n] for n in sorted(names)]
    total = sum(m.uncompressed_size for m in selected)
    if total >= MAX_RAW_BYTES:
        raise RuntimeError(f"Clean official subset exceeds 1 GB: {total} bytes")
    return selected


def _span_end(member: Member) -> int:
    # Central and local name/extra lengths match in this pinned archive.  The
    # local header is validated again before decompression.
    return (
        member.local_offset
        + 30
        + member.central_name_len
        + member.central_extra_len
        + member.compressed_size
    )


def _coalesced_ranges(members: list[Member]) -> list[tuple[int, int, list[Member]]]:
    ranges: list[tuple[int, int, list[Member]]] = []
    for member in sorted(members, key=lambda m: m.local_offset):
        start = member.local_offset
        end = _span_end(member)
        if ranges:
            r_start, r_end, r_members = ranges[-1]
            if start - r_end <= MERGE_GAP_BYTES and end - r_start <= MAX_RANGE_BYTES:
                ranges[-1] = (r_start, max(r_end, end), r_members + [member])
                continue
        ranges.append((start, end, [member]))
    return ranges


def _safe_destination(output: Path, member_name: str) -> Path:
    parts = PurePosixPath(member_name).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"Unsafe official member path: {member_name}")
    return output.joinpath(*parts)


def _valid_existing(path: Path, member: Member) -> bool:
    if not path.is_file() or path.stat().st_size != member.uncompressed_size:
        return False
    crc = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            crc = binascii.crc32(block, crc)
    return (crc & 0xFFFFFFFF) == member.crc32


def _extract_from_range(
    output: Path, start: int, end: int, members: list[Member]
) -> tuple[int, int]:
    pending = [m for m in members if not _valid_existing(_safe_destination(output, m.name), m)]
    if not pending:
        return 0, sum(m.uncompressed_size for m in members)
    blob = _request_range(start, end - 1)
    written = 0
    for member in pending:
        rel = member.local_offset - start
        header = blob[rel : rel + 30]
        values = struct.unpack_from("<4s5H3I2H", header, 0)
        if values[0] != b"PK\x03\x04":
            raise RuntimeError(f"Bad local header for {member.name}")
        local_name_len, local_extra_len = values[-2], values[-1]
        data_at = rel + 30 + local_name_len + local_extra_len
        compressed = blob[data_at : data_at + member.compressed_size]
        if len(compressed) != member.compressed_size:
            raise RuntimeError(f"Truncated compressed payload for {member.name}")
        if member.method == 0:
            data = compressed
        elif member.method == 8:
            data = zlib.decompress(compressed, -15)
        else:
            raise RuntimeError(f"Unsupported ZIP method {member.method} for {member.name}")
        if len(data) != member.uncompressed_size:
            raise RuntimeError(f"Size mismatch after extracting {member.name}")
        if (binascii.crc32(data) & 0xFFFFFFFF) != member.crc32:
            raise RuntimeError(f"CRC mismatch after extracting {member.name}")
        destination = _safe_destination(output, member.name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = destination.with_name(destination.name + ".partial")
        with partial.open("wb") as handle:
            handle.write(data)
        os.replace(partial, destination)
        written += 1
    return written, sum(m.uncompressed_size for m in members)


def acquire(output: Path, workers: int = 6, verify_only: bool = False) -> None:
    output = _long_path(Path(output))
    output.mkdir(parents=True, exist_ok=True)
    members = _selected_members(_parse_members(_central_directory()))
    if verify_only:
        bad = [m.name for m in members if not _valid_existing(_safe_destination(output, m.name), m)]
        if bad:
            raise SystemExit(f"Missing or altered official files: {bad[:10]}")
    else:
        ranges = _coalesced_ranges(members)
        print(
            f"Selected {len(members)} untouched members in {len(ranges)} byte ranges; "
            f"official payload={sum(m.uncompressed_size for m in members)} bytes"
        )
        with ThreadPoolExecutor(max_workers=max(1, min(int(workers), 8))) as pool:
            futures = {
                pool.submit(_extract_from_range, output, start, end, batch): (start, end, batch)
                for start, end, batch in ranges
            }
            completed = 0
            for future in as_completed(futures):
                count, _ = future.result()
                completed += len(futures[future][2])
                print(f"verified {completed}/{len(members)} members (+{count} written)")
    total = sum(m.uncompressed_size for m in members)
    print(
        f"OK: {len(members)} byte-identical official files, {total} bytes. "
        f"Source archive MD5 is {ARCHIVE_MD5}."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("raw_data"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    acquire(args.output, args.workers, args.verify_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
