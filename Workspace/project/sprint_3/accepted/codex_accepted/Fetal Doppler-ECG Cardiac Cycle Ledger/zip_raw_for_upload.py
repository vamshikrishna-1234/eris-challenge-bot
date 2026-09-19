"""Create an optional clean source-file ZIP from an official NInFEA download.

This is a fallback only. The preferred platform path is direct import from
https://physionet.org/content/ninfea/get-zip/1.0.0/. If direct import fails, run this
against an unchanged official download and upload the resulting archive. The
script refuses to include prepared public/private splits or challenge code.
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ALLOWED_TOP = {
    "LICENSE.txt",
    "RECORDS",
    "SHA256SUMS.txt",
    "pwd_images",
    "wfdb_format_ecg_and_respiration",
    "bin_format_ecg_and_respiration",
    "code",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("official_root", type=Path)
    parser.add_argument("--out", type=Path, default=Path("ninfea_official_raw.zip"))
    args = parser.parse_args()
    root = args.official_root.resolve()
    if not (root / "LICENSE.txt").exists() or not (root / "pwd_images").is_dir():
        raise SystemExit("official_root does not look like an unchanged NInFEA download")
    with zipfile.ZipFile(args.out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in sorted(root.rglob("*")):
            if p.is_dir():
                continue
            rel = p.relative_to(root).as_posix()
            top = rel.split("/")[0]
            if top not in ALLOWED_TOP:
                continue
            lower = rel.lower()
            if lower.startswith(("public/", "private/", "raw_data/")) or lower.endswith((".pyc",)):
                continue
            zf.write(p, rel)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
