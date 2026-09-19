from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import struct
import urllib.request
import zipfile
import zlib
from pathlib import Path


ZENODO_API = "https://zenodo.org/api/records/7928121"
TRACK_ZIP_URL = f"{ZENODO_API}/files/Berlin2019_tracks.zip/content"
OFFICIAL_CSVS = [
    "Berlin2019_dances.csv",
    "Berlin2019_dances_with_manually_verified_times.csv",
    "Berlin2019_feeder_experiment_log.csv",
    "Berlin2019_followers.csv",
    "Berlin2019_waggle_phases.csv",
    "Berlin2019_dance_classifier_labels.csv",
]
SELECTED_TRACK_DATES = [
    "2019-08-25",
    "2019-08-27",
    "2019-08-28",
    "2019-08-29",
    "2019-09-02",
    "2019-09-05",
    "2019-09-10",
    "2019-09-11",
]


def _urlopen(req, timeout=180):
    return urllib.request.urlopen(req, timeout=timeout)


def _download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with _urlopen(req) as r, path.open("wb") as f:
        shutil.copyfileobj(r, f, length=1024 * 1024)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_record_metadata() -> dict:
    with _urlopen(urllib.request.Request(ZENODO_API), timeout=90) as r:
        return json.load(r)


def _range_get(url: str, start: int, end: int) -> bytes:
    req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
    with _urlopen(req, timeout=240) as r:
        return r.read()


def _zip_central_directory(url: str, size: int) -> dict[str, dict]:
    tail_len = min(size, 262144)
    tail = _range_get(url, size - tail_len, size - 1)
    eocd_idx = tail.rfind(b"PK\x05\x06")
    if eocd_idx < 0:
        raise RuntimeError("Could not find ZIP end-of-central-directory record")
    fields = struct.unpack("<4sHHHHIIH", tail[eocd_idx : eocd_idx + 22])
    _, _, _, _, total_entries, cd_size, cd_offset, _ = fields
    cd = _range_get(url, cd_offset, cd_offset + cd_size - 1)
    entries = {}
    pos = 0
    for _ in range(total_entries):
        if cd[pos : pos + 4] != b"PK\x01\x02":
            raise RuntimeError(f"Bad central directory signature at {pos}")
        fields = struct.unpack("<4sHHHHHHIIIHHHHHII", cd[pos : pos + 46])
        (
            _,
            _ver_made,
            _ver_need,
            flag,
            method,
            _mtime,
            _mdate,
            crc,
            csize,
            usize,
            nlen,
            xlen,
            clen,
            _disk,
            _int_attr,
            _ext_attr,
            local_header_offset,
        ) = fields
        name = cd[pos + 46 : pos + 46 + nlen].decode("utf-8")
        entries[name] = {
            "flag": flag,
            "method": method,
            "crc32": crc,
            "compressed_size": csize,
            "uncompressed_size": usize,
            "local_header_offset": local_header_offset,
        }
        pos += 46 + nlen + xlen + clen
    return entries


def _extract_member_by_range(url: str, entry: dict, out_path: Path) -> None:
    off = int(entry["local_header_offset"])
    head = _range_get(url, off, off + 4095)
    if head[:4] != b"PK\x03\x04":
        raise RuntimeError("Bad local header signature")
    fields = struct.unpack("<4sHHHHHIIIHH", head[:30])
    _, _, _flag, method, _, _, _, _csize, _usize, nlen, xlen = fields
    data_start = off + 30 + nlen + xlen
    csize = int(entry["compressed_size"])
    comp = _range_get(url, data_start, data_start + csize - 1)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if method == 0:
        payload = comp
    elif method == 8:
        payload = zlib.decompress(comp, -15)
    else:
        raise RuntimeError(f"Unsupported ZIP compression method: {method}")
    if len(payload) != int(entry["uncompressed_size"]):
        raise RuntimeError(f"Unexpected extracted size for {out_path.name}")
    out_path.write_bytes(payload)


def build(staging: Path, output_zip: Path) -> None:
    record = _load_record_metadata()
    files = {item["key"]: item for item in record["files"]}
    license_id = record.get("metadata", {}).get("license", {}).get("id")
    if license_id != "cc-by-4.0":
        raise RuntimeError(f"Unexpected Zenodo license id: {license_id}")

    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    manifest_rows = []

    for name in OFFICIAL_CSVS:
        item = files[name]
        url = item["links"]["self"]
        dest = staging / name
        _download(url, dest)
        manifest_rows.append(
            {
                "path": name,
                "source_url": url,
                "source_file": name,
                "source_checksum": item["checksum"],
                "source_size_bytes": item["size"],
                "sha256": _sha256(dest),
                "note": "Official Zenodo CSV downloaded unchanged.",
            }
        )

    track_item = files["Berlin2019_tracks.zip"]
    entries = _zip_central_directory(TRACK_ZIP_URL, int(track_item["size"]))
    for date in SELECTED_TRACK_DATES:
        member = f"Berlin2019_tracks/{date}.csv"
        if member not in entries:
            raise RuntimeError(f"{member} missing from official track ZIP")
        dest = staging / member
        _extract_member_by_range(TRACK_ZIP_URL, entries[member], dest)
        manifest_rows.append(
            {
                "path": member,
                "source_url": TRACK_ZIP_URL,
                "source_file": "Berlin2019_tracks.zip",
                "source_checksum": track_item["checksum"],
                "source_size_bytes": entries[member]["uncompressed_size"],
                "sha256": _sha256(dest),
                "note": "Unchanged date-level CSV member extracted from official ZIP.",
            }
        )

    (staging / "LICENSE.txt").write_text(
        "Source: Zenodo record 7928121, Data used in Machine learning reveals the waggle drift's role in the honey bee dance communication system.\n"
        "License: Creative Commons Attribution 4.0 International (CC BY 4.0).\n"
        "Attribution: Dormagen, David M.; Wild, Benjamin; Wario, Fernando; Landgraf, Tim. Zenodo, 2023. DOI: 10.5281/zenodo.7928121.\n",
        encoding="utf-8",
    )
    (staging / "EXTRACTION_NOTES.md").write_text(
        "# Extraction Notes\n\n"
        "This package contains official Zenodo CSV files and unchanged date-level CSV members from `Berlin2019_tracks.zip`.\n"
        "The full track archive is not repacked. Only the selected date members listed in `SOURCE_MANIFEST.csv` are extracted.\n"
        "No train/test split, feature table, hidden answer file, or prepared challenge data is included in this raw source package.\n",
        encoding="utf-8",
    )
    with (staging / "SOURCE_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["path", "source_url", "source_file", "source_checksum", "source_size_bytes", "sha256", "note"],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)
    with (staging / "CHECKSUMS_SHA256.txt").open("w", encoding="utf-8") as f:
        for path in sorted(p for p in staging.rglob("*") if p.is_file()):
            f.write(f"{_sha256(path)}  {path.relative_to(staging).as_posix()}\n")

    if output_zip.exists():
        output_zip.unlink()
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(p for p in staging.rglob("*") if p.is_file()):
            zf.write(path, path.relative_to(staging).as_posix())
    print(f"Wrote {output_zip} ({output_zip.stat().st_size / 1_000_000:.1f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the clean real-data source subset ZIP for the waggle challenge.")
    parser.add_argument("--staging", type=Path, default=Path("official_raw_subset"))
    parser.add_argument("--output", type=Path, default=Path("waggle_dance_raw_subset.zip"))
    args = parser.parse_args()
    build(args.staging, args.output)


if __name__ == "__main__":
    main()
