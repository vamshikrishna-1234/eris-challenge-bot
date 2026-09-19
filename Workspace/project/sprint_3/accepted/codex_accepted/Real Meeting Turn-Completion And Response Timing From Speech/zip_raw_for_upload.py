from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw_data"
ZIP_PATH = ROOT / "raw_source_upload_optional.zip"
EXPECTED_FILES = [
    "ami_public_manual_1.6.2.zip",
    "meetings.csv",
    "LICENSE.txt",
    "ATTRIBUTION.txt",
    "SOURCE_URLS.txt",
    "README.txt",
]


def main() -> None:
    if not RAW_DIR.exists():
        raise SystemExit(f"Missing raw_data directory: {RAW_DIR}")
    for name in EXPECTED_FILES:
        if not (RAW_DIR / name).exists():
            raise SystemExit(f"Missing raw_data/{name}")
    audio_files = sorted((RAW_DIR / "audio").glob("*.Mix-Headset.wav"))
    if len(audio_files) != 8:
        raise SystemExit(f"Expected 8 AMI headset-mix WAV files, found {len(audio_files)}")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for name in EXPECTED_FILES:
            zf.write(RAW_DIR / name, arcname=name)
        for path in audio_files:
            zf.write(path, arcname=f"audio/{path.name}")

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        names = zf.namelist()
    bad = [n for n in names if n.startswith(("raw_data/", "public/", "private/", "_"))]
    if bad:
        raise SystemExit(f"Zip contains forbidden nested paths: {bad[:5]}")
    size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    print(f"wrote optional source zip {ZIP_PATH} with {len(names)} members, {size_mb:.2f} MiB")


if __name__ == "__main__":
    main()
