#!/usr/bin/env python3
"""Package raw_data/ into a FLAT raw_upload.zip for the dataset Source Files area.

The archive members are the raw corpus files themselves (features.csv, points.csv, README.txt,
LICENSE.txt) with no wrapping directory, so the platform extracts them as raw_upload/<file>.
generate.py is uploaded alongside the zip as the second source file.
"""
import hashlib
import os
import zipfile

MEMBERS = ["features.csv", "points.csv", "README.txt", "LICENSE.txt"]


def main(src="raw_data", out="raw_upload.zip"):
    missing = [m for m in MEMBERS if not os.path.exists(os.path.join(src, m))]
    if missing:
        raise SystemExit("missing raw files: %s" % missing)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for m in MEMBERS:
            z.write(os.path.join(src, m), arcname=m)
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    assert names == MEMBERS, "archive is not flat: %s" % names
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("wrote %s  %.2f MB  members=%s" % (out, os.path.getsize(out) / 1e6, names))
    print("sha256 %s" % h)


if __name__ == "__main__":
    main()
