from __future__ import annotations


MESSAGE = """No synthetic generator is used for this real-data challenge.

Use the official ACE Corpus archives listed in URL_IMPORT_LIST.txt. The raw
source files are imported unmodified, and prepare.py performs the reverberant
speech construction and public/private materialization.
"""


def main() -> None:
    raise SystemExit(MESSAGE)


if __name__ == "__main__":
    main()
