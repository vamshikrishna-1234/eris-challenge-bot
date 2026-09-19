from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="This real-data challenge does not generate synthetic raw data. Use official CREMA-D AudioWAV files directly."
    )
    parser.add_argument("--raw", type=Path, default=None, help="Optional official CREMA-D root to validate.")
    args = parser.parse_args()
    if args.raw is None:
        print("No synthetic generation is used. Import official CREMA-D AudioWAV files and metadata directly.")
        return
    import prepare

    root = prepare._find_raw_root(args.raw)
    clips = prepare._load_clips(root, smoke=(root / "SMOKE_FIXTURE_ONLY.txt").exists())
    print(f"OK: found CREMA-D-style AudioWAV layout at {root} with {len(clips)} parsed WAV files.")


if __name__ == "__main__":
    main()
