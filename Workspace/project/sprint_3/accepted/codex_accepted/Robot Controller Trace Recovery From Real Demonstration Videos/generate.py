"""Official-source manifest and optional downloader.

This challenge uses the unmodified Zenodo file PandaHandover_Real_Val.zip.
The script is not a data generator and does not synthesize or preprocess raw
challenge data. It only downloads the official archive when a local copy is
needed for validation.
"""

import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen


FILES = [
    {
        "name": "PandaHandover_Real_Val.zip",
        "url": "https://zenodo.org/records/6337847/files/PandaHandover_Real_Val.zip?download=1",
        "size": 296_205_835,
        "md5": "c3af4d02e686084c28d6dd7bc12cb059",
    }
]


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(output_dir: Path, force: bool = False) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in FILES:
        out = output_dir / item["name"]
        if out.exists() and not force:
            if out.stat().st_size == item["size"] and _md5(out) == item["md5"]:
                print(f"already verified: {out}")
                continue
            raise SystemExit(f"{out} exists but does not match official size/md5; remove it or pass --force")
        print(f"downloading official Zenodo file: {item['url']}")
        with urlopen(item["url"], timeout=120) as r, out.open("wb") as f:
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
        if out.stat().st_size != item["size"]:
            raise SystemExit(f"size mismatch for {out}: {out.stat().st_size} != {item['size']}")
        got = _md5(out)
        if got != item["md5"]:
            raise SystemExit(f"md5 mismatch for {out}: {got} != {item['md5']}")
        print(f"verified: {out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("raw"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    download(args.output_dir, args.force)


if __name__ == "__main__":
    main()
