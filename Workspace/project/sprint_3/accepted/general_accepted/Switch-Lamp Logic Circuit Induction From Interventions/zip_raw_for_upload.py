"""Package raw_data/ FLAT at the archive root for platform upload.

Produces panel_raw_upload.zip containing:
    scenes.csv
    videos/<scene_hash>.mp4
(no wrapping raw_data/ folder). prepare.py consumes this layout directly.
Run:  python zip_raw_for_upload.py
"""

from __future__ import annotations

import zipfile
from pathlib import Path

RAW = Path("raw_data")
OUT = Path("panel_raw_upload.zip")


def main() -> None:
    if not (RAW / "scenes.csv").exists():
        raise SystemExit("raw_data/scenes.csv not found - run generate.py first.")
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(RAW / "scenes.csv", arcname="scenes.csv")
        for mp4 in sorted((RAW / "videos").glob("*.mp4")):
            zf.write(mp4, arcname=f"videos/{mp4.name}")
    print(f"OK: wrote {OUT} ({OUT.stat().st_size / (1024*1024):.1f} MB)")


if __name__ == "__main__":
    main()
