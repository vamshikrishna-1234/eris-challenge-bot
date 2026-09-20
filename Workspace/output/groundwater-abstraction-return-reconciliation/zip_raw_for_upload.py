"""Build the flat raw_upload.zip for the dataset Source Files area.

Archive members are the raw corpus files directly: scenes.csv, series/, the
background provenance record and LICENSE.txt. No raw_data/ wrapper, no repo
folder, no public/, no private/, no source code, no caches.
"""
import argparse, hashlib, os, zipfile
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="raw_data")
    ap.add_argument("--out", default="raw_upload.zip")
    a = ap.parse_args()
    raw, out = Path(a.raw), Path(a.out)
    members = []
    for name in ("scenes.csv", "BACKGROUND_PROVENANCE.json", "LICENSE.txt"):
        p = raw / name
        if p.exists():
            members.append((p, name))
    for p in sorted((raw / "series").glob("*.csv")):
        members.append((p, "series/%s" % p.name))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for src, arc in members:
            z.write(src, arc)
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    print("%s: %d members, %.1f MB, sha256 %s" % (out, len(members), out.stat().st_size / 1e6, h))
    with zipfile.ZipFile(out) as z:
        bad = [n for n in z.namelist()
               if n.startswith(("raw_data/", "public/", "private/", "/")) or ".." in n]
        print("flat-archive audit:", "FAIL " + str(bad[:5]) if bad else "pass")
        print("top-level entries:", sorted({n.split("/")[0] for n in z.namelist()}))

if __name__ == "__main__":
    main()
