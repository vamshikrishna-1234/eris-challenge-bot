"""
generate.py - build the raw upload bundle for FragmentFold.

Downloads the MassBank consensus tandem-MS records (NIST .msp export) from the
official MassBank-data GitHub release (CC-BY 4.0), streams through every record,
keeps the MS2 spectra that have a valid small-molecule structure, bounds the
corpus along diversity axes (cap per compound), and writes a single compact
`raw_data/spectra.csv` that `prepare.py` consumes.

The raw CSV is the dataset that gets uploaded to the platform. It deliberately
keeps the canonical SMILES (the structure) so that `prepare.py` can derive the
ground-truth substructure fingerprint and the Bemis-Murcko scaffold used for the
scaffold-disjoint split. Participants never see this file: they only receive the
processed `public/` split, which contains peaks but no structure.

License: CC-BY 4.0 (MassBank). Attribution lives in DATASET_FORM_FILL.md.

Usage
-----
    pip install requests rdkit numpy
    python generate.py --out raw_data
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import requests

MSP_URL = (
    "https://github.com/MassBank/MassBank-data/releases/download/"
    "2026.03/MassBank_NISTformat.msp"
)
MSP_NAME = "MassBank_NISTformat.msp"

# --- bounding / filtering knobs (defaults give a ~15-20 MB raw CSV) ---
MIN_PEAKS = 6
MAX_PEAKS = 200          # keep the MAX_PEAKS most intense peaks if more
MAX_HEAVY_ATOMS = 60     # drop large natural products / lipids
MIN_HEAVY_ATOMS = 4
MAX_SPECTRA_PER_COMPOUND = 6   # diversity: cap spectra per InChIKey block
MAX_TOTAL = 20000        # global cap on emitted spectra

# Common, well-defined adducts only (keeps neutral-mass reasoning tractable).
ALLOWED_ADDUCTS = {
    "[M+H]+", "[M-H]-", "[M+Na]+", "[M+NH4]+", "[M+K]+",
    "[M+H-H2O]+", "[M-H-H2O]-", "[M+Cl]-", "[M+HCOO]-", "[M+CH3COO]-",
    "[M+2H]2+", "[M-2H]2-", "[M+Na-2H]-", "[M+FA-H]-",
}

CHUNK = 1 << 20


def _download_msp(out_dir: Path) -> Path:
    dst = out_dir / MSP_NAME
    if dst.exists() and dst.stat().st_size > 100_000_000:
        print(f"  [skip] {dst.name} already present ({dst.stat().st_size/1e6:.1f} MB)")
        return dst
    print(f"  [download] {MSP_URL}")
    with requests.get(MSP_URL, stream=True, timeout=180) as r:
        r.raise_for_status()
        tmp = dst.with_suffix(".part")
        got = 0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=CHUNK):
                if chunk:
                    f.write(chunk)
                    got += len(chunk)
        tmp.replace(dst)
    print(f"  [done] {dst.name}  {dst.stat().st_size/1e6:.1f} MB")
    return dst


def _iter_records(msp_path: Path):
    """Yield dict records from a NIST-format .msp file."""
    rec: dict = {}
    peaks: list[tuple[float, float]] = []
    in_peaks = False
    with open(msp_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if rec or peaks:
                    rec["peaks"] = peaks
                    yield rec
                rec, peaks, in_peaks = {}, [], False
                continue
            if in_peaks:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        peaks.append((float(parts[0]), float(parts[1])))
                    except ValueError:
                        pass
                continue
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip()
                if key == "Num Peaks":
                    in_peaks = True
                    rec["num_peaks"] = val
                else:
                    rec[key] = val
    if rec or peaks:
        rec["peaks"] = peaks
        yield rec


def _peaks_to_str(peaks: list[tuple[float, float]]) -> str:
    return ";".join(f"{mz:.4f},{inten:.4g}" for mz, inten in peaks)


def generate(out_dir: Path) -> None:
    from rdkit import Chem
    from rdkit import RDLogger
    RDLogger.DisableLog("rdApp.*")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    msp_path = _download_msp(out_dir)

    per_compound: dict[str, int] = defaultdict(int)
    seen_splash: set[str] = set()
    n_in = 0
    by_compound: dict[str, list[dict]] = defaultdict(list)

    for rec in _iter_records(msp_path):
        n_in += 1
        stype = (rec.get("Spectrum_type") or "").upper()
        if "MS2" not in stype and "MS^2" not in stype:
            continue
        adduct = (rec.get("Precursor_type") or "").strip()
        if adduct not in ALLOWED_ADDUCTS:
            continue
        smiles = (rec.get("SMILES") or "").strip()
        if not smiles or smiles.upper() in {"N/A", "NA", "NONE"}:
            continue
        peaks = rec.get("peaks") or []
        if len(peaks) < MIN_PEAKS:
            continue
        try:
            prec = float(rec.get("PrecursorMZ") or "nan")
        except ValueError:
            continue
        if not (prec == prec) or prec <= 0:
            continue

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            continue
        nheavy = mol.GetNumHeavyAtoms()
        if nheavy < MIN_HEAVY_ATOMS or nheavy > MAX_HEAVY_ATOMS:
            continue
        if not any(a.GetSymbol() == "C" for a in mol.GetAtoms()):
            continue
        try:
            can = Chem.MolToSmiles(mol)
            inchikey = Chem.MolToInchiKey(mol)
        except Exception:
            continue
        block = inchikey.split("-")[0] if inchikey else can
        if per_compound[block] >= MAX_SPECTRA_PER_COMPOUND:
            continue

        splash = rec.get("Splash") or ""
        if splash and splash in seen_splash:
            continue
        if splash:
            seen_splash.add(splash)

        if len(peaks) > MAX_PEAKS:
            peaks = sorted(peaks, key=lambda p: -p[1])[:MAX_PEAKS]
            peaks = sorted(peaks, key=lambda p: p[0])

        per_compound[block] += 1
        by_compound[block].append({
            "smiles": can,
            "adduct": adduct,
            "ion_mode": (rec.get("Ion_mode") or "").upper(),
            "precursor_mz": f"{prec:.4f}",
            "collision_energy": (rec.get("Collision_energy") or "").strip(),
            "peaks": _peaks_to_str(peaks),
        })

    # Round-robin across compounds so a global cap keeps maximum structural
    # diversity (one spectrum from every compound before a second from any).
    rows: list[dict] = []
    blocks = sorted(by_compound.keys())
    depth = 0
    while len(rows) < MAX_TOTAL:
        added = False
        for b in blocks:
            if depth < len(by_compound[b]):
                rows.append(by_compound[b][depth])
                added = True
                if len(rows) >= MAX_TOTAL:
                    break
        if not added:
            break
        depth += 1

    rows.sort(key=lambda r: (r["smiles"], r["adduct"], r["precursor_mz"]))
    out_csv = out_dir / "spectra.csv"
    cols = ["smiles", "adduct", "ion_mode", "precursor_mz", "collision_energy", "peaks"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    n_compounds = len({r["smiles"] for r in rows})
    size_mb = out_csv.stat().st_size / 1e6
    print(f"  [scan] read {n_in} records")
    print(f"  [ok] kept {len(rows)} MS2 spectra over {n_compounds} compounds")
    print(f"  [ok] wrote {out_csv}  ({size_mb:.1f} MB)")
    print("  [note] you can delete the .msp now; only spectra.csv is the raw upload")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    args = ap.parse_args()
    try:
        generate(args.out)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
