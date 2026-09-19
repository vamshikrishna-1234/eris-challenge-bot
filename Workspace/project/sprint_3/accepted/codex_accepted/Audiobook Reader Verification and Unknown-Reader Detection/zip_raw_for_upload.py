from __future__ import annotations

MESSAGE = """No custom raw_upload.zip should be created for this real-source challenge.

Use the official Mini LibriSpeech URL imports:

https://openslr.trmal.net/resources/31/dev-clean-2.tar.gz
https://openslr.trmal.net/resources/31/train-clean-5.tar.gz

Manual fallback is to upload those same unmodified official tarballs only.
"""


def main() -> None:
    print(MESSAGE)


if __name__ == "__main__":
    main()
