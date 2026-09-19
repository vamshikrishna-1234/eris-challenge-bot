from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


REQUIRED_ROOT_FILES = ["clips.csv", "LICENSE.txt", "ATTRIBUTION.txt", "SOURCE_URLS.txt", "README.txt"]


def zip_raw(raw_dir: Path, zip_path: Path) -> None:
    raw_dir = Path(raw_dir)
    zip_path = Path(zip_path)
    for name in REQUIRED_ROOT_FILES:
        if not (raw_dir / name).exists():
            raise FileNotFoundError(f"Missing required raw file: {raw_dir / name}")
    audio_dir = raw_dir / "audio"
    if not audio_dir.exists() or not any(audio_dir.glob("*.wav")):
        raise FileNotFoundError(f"Missing WAV clips under {audio_dir}")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for name in REQUIRED_ROOT_FILES:
            zf.write(raw_dir / name, arcname=name)
        for wav in sorted(audio_dir.glob("*.wav")):
            zf.write(wav, arcname=f"audio/{wav.name}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
    bad = [n for n in names if n.startswith("raw_data/") or n.startswith("public/") or n.startswith("private/")]
    if bad:
        raise RuntimeError(f"raw_upload.zip contains forbidden nested paths: {bad[:5]}")
    print(f"Wrote {zip_path} with {len(names)} members and size {zip_path.stat().st_size / (1024 * 1024):.2f} MiB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--zip", type=Path, default=Path("raw_upload.zip"))
    parser.add_argument(
        "--allow-local-debug-zip",
        action="store_true",
        help="Create a local debug archive. Do not upload it for this real-source URL-import dataset.",
    )
    args = parser.parse_args()
    if not args.allow_local_debug_zip:
        raise SystemExit(
            "This real-source challenge uses official AMI URL imports, not raw_upload.zip. "
            "See URL_IMPORT_LIST.txt. Pass --allow-local-debug-zip only for a local debug archive."
        )
    zip_raw(args.raw, args.zip)


if __name__ == "__main__":
    main()
