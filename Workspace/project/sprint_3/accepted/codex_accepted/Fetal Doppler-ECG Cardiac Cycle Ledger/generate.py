"""NInFEA is a real PhysioNet source, so this file does not synthesize data.

Use the official source import instead:
https://physionet.org/content/ninfea/get-zip/1.0.0/

The challenge platform should import the official PhysioNet ZIP URL directly
when possible. The directory index URL may import only a small HTML file named
downloaded-file. If direct ZIP import is unavailable, download the official files or use
`wget -r -N -c -np https://physionet.org/files/ninfea/1.0.0/` and upload only
the unchanged official files. All segmentation and label construction happens
inside prepare.py.
"""

from __future__ import annotations


def main() -> None:
    print(__doc__)


if __name__ == "__main__":
    main()
