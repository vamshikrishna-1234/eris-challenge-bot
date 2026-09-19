from __future__ import annotations

import argparse
from pathlib import Path

from build_source_subset_zip import build


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Real-data provenance helper for the Waggle-Dance Communication Graph Recovery challenge. "
            "This does not generate synthetic data; it downloads official Zenodo files and extracts "
            "unchanged date-level track CSV members into a clean raw source subset."
        )
    )
    parser.add_argument("--staging", type=Path, default=Path("official_raw_subset"))
    parser.add_argument("--output", type=Path, default=Path("waggle_dance_raw_subset.zip"))
    args = parser.parse_args()
    build(args.staging, args.output)


if __name__ == "__main__":
    main()
