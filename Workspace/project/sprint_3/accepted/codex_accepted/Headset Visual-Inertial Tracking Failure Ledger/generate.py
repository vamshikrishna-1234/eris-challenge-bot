#!/usr/bin/env python3
"""Download the selected official Monado SLAM source ZIP files.

This is a real-data acquisition helper, not a synthetic data generator. It
fetches only a bounded set of official raw sequence archives from the upstream
Hugging Face dataset so the raw source upload stays under about 1 GB.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path


SOURCES = [
    {
        "name": "MIO09_short_1_updown.zip",
        "url": "https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO09_short_1_updown.zip?download=true",
        "size": 99569080,
    },
    {
        "name": "MIO10_short_2_panorama.zip",
        "url": "https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO10_short_2_panorama.zip?download=true",
        "size": 214797238,
    },
    {
        "name": "MIO11_short_3_backandforth.zip",
        "url": "https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO11_short_3_backandforth.zip?download=true",
        "size": 307904816,
    },
    {
        "name": "MGO09_short_1_updown.zip",
        "url": "https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MG_reverb_g2/MGO_others/MGO09_short_1_updown.zip?download=true",
        "size": 77826631,
    },
    {
        "name": "MGO10_short_2_panorama.zip",
        "url": "https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MG_reverb_g2/MGO_others/MGO10_short_2_panorama.zip?download=true",
        "size": 292156870,
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".download")
    with urllib.request.urlopen(url, timeout=60) as src, tmp.open("wb") as out:
        while True:
            block = src.read(1024 * 1024)
            if not block:
                break
            out.write(block)
    tmp.replace(dest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="raw_data", help="Directory for official source ZIPs.")
    parser.add_argument("--skip-download", action="store_true", help="Only validate files already present.")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for src in SOURCES:
        dest = out_dir / src["name"]
        if not dest.exists() and not args.skip_download:
            print(f"Downloading {src['name']} ({src['size']} bytes)")
            download(src["url"], dest)
        if not dest.exists():
            print(f"missing: {dest}", file=sys.stderr)
            return 2
        size = dest.stat().st_size
        if size != src["size"]:
            print(f"size mismatch for {dest.name}: got {size}, expected {src['size']}", file=sys.stderr)
            return 3
        total += size
        print(f"{dest.name}\t{size}\tsha256={sha256_file(dest)}")
    print(f"total_bytes={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
