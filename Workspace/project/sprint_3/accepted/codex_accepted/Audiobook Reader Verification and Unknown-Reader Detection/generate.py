from __future__ import annotations

MESSAGE = """This is a real-source Mini LibriSpeech challenge.

Import the official OpenSLR SLR31 archives directly:

https://openslr.trmal.net/resources/31/dev-clean-2.tar.gz
https://openslr.trmal.net/resources/31/train-clean-5.tar.gz

prepare.py derives a bounded de-identified public split from those official real-speech archives.
"""


def main() -> None:
    print(MESSAGE)


if __name__ == "__main__":
    main()
