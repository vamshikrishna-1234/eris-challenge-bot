from __future__ import annotations


MESSAGE = """This real-data challenge does not create raw_upload.zip.

Use the official ACE Corpus source archives directly from Zenodo:
- ACE_Corpus_RIRN_Single.tbz2
- ACE_Corpus_Speech.tbz2
- ACE_Corpus_Data.tbz2

All challenge-specific filtering, convolution, split construction, label bucketing,
and prepared public/private materialization happens in prepare.py.
"""


def main() -> None:
    raise SystemExit(MESSAGE)


if __name__ == "__main__":
    main()
