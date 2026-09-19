import argparse
import hashlib
import zipfile
from pathlib import Path


OFFICIAL_NAME = "PandaHandover_Real_Val.zip"
OFFICIAL_SIZE = 296_205_835
OFFICIAL_MD5 = "c3af4d02e686084c28d6dd7bc12cb059"


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Package the unmodified official Zenodo ZIP only.")
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("official_raw_upload.zip"))
    args = parser.parse_args()
    src = args.raw_dir / OFFICIAL_NAME
    if not src.exists():
        raise SystemExit(f"missing official file: {src}")
    if src.stat().st_size != OFFICIAL_SIZE:
        raise SystemExit(f"size mismatch: {src.stat().st_size} != {OFFICIAL_SIZE}")
    got = _md5(src)
    if got != OFFICIAL_MD5:
        raise SystemExit(f"md5 mismatch: {got} != {OFFICIAL_MD5}")
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_STORED) as zf:
        zf.write(src, OFFICIAL_NAME)
    print(f"wrote {args.output} containing only {OFFICIAL_NAME}")


if __name__ == "__main__":
    main()
