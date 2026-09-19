"""
prepare.py - Molecular Substructure Fingerprint Prediction From Mass Spectra

The solver is shown a tandem-MS (MS2) peak list plus the precursor m/z, the
adduct type, and the ion mode. The target is calibrated per-bit probability
estimates for a 512-bit molecular substructure fingerprint (Morgan / ECFP,
radius 2, 512 bits). Training labels are binary; the solver must produce
probabilities scored via Brier Skill Score.

ALL challenge processing happens here:
  1. Read raw_data/spectra.csv (canonical SMILES + adduct + precursor + peaks).
  2. Derive, per molecule, the ground-truth 512-bit ECFP fingerprint and the
     Bemis-Murcko scaffold (RDKit). Acyclic molecules (empty scaffold) are
     grouped by canonical SMILES so each distinct structure is one group.
  3. Scaffold-DISJOINT split: whole scaffold groups go entirely to train or
     entirely to test, so no scaffold (hence no molecule) seen at test time
     appears in training. This defeats spectral-library / nearest-neighbour
     lookup as a solution.
  4. Mild, per-row-seeded peak perturbation (intensity renormalisation + jitter,
     small m/z jitter, low-intensity dropout, a few spurious peaks) so that
     byte-level matching of the public peak list against the upstream public
     records is not reliable. Applied identically in distribution to train/test.
  5. Emit public/train.csv (+ fingerprint label), public/test.csv (no label),
     public/sample_submission.csv (a per-(ion_mode, adduct, precursor-m/z bin)
     training marginal, shrunk toward the overall marginal -> weak BSS ~ 0.02),
     private/answers.csv, and private/p_hat_train.txt (the overall training
     marginal, embedded into grade.py as the fixed P_HAT_TRAIN Brier reference).

prepare(raw, public, private) is the platform-standard signature.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

# ---- config ----
N_BITS = 512
MORGAN_RADIUS = 2

# Fingerprints are written as a string of N_BITS '0'/'1' chars prefixed with the
# letter 'b' (e.g. "b0101..."). The prefix forces CSV readers to keep the column
# as a string instead of coercing a 512-digit value into an (overflowing) int.
FP_PREFIX = "b"

N_TRAIN = 16000
N_TEST = 4000
TEST_SCAFFOLD_FRACTION = 0.22

MIN_PEAKS_OUT = 4

# Sample-submission baseline: a per-(ion_mode, adduct, precursor-m/z bin)
# marginal learned from training, shrunk toward the overall training marginal so
# sparse cells stay calibrated. It uses ONLY public metadata (never the peaks or
# any test label), so it is a legitimately weak template -- yet it carries enough
# conditional signal to score just above the climatological floor (BSS ~ 0.02)
# under the static train-derived Brier reference, which the platform's sample
# validation requires (a degenerate all-marginal vector clips to exactly 0).
SAMPLE_MZ_BIN = 100.0
SAMPLE_SHRINK = 5.0

# Peak perturbation (mild - signal-preserving, lookup-breaking).
INTENSITY_JITTER = 0.06
MZ_JITTER_DA = 0.0020
PEAK_DROPOUT = 0.08
MAX_SPURIOUS = 3
BASE_PEAK_NORM = 999.0
MZ_MERGE_TOL = 0.001

# Private seeds (unguessable; none are 42/1337/2024).
SPLIT_SEED = 0x6B1F3D27
SAMPLE_SEED = 0x6B1F3D38
PERTURB_SEED = 0x6B1F3D49
SPURIOUS_SEED = 0x6B1F3D5A


def _ensure_rdkit() -> None:
    try:
        import rdkit  # noqa: F401
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rdkit"])


def _stable_rng(seed: int, key: int) -> np.random.Generator:
    mixed = (int(seed) ^ ((int(key) * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    return np.random.default_rng(mixed)


def _find_spectra_csv(raw: Path) -> Path:
    cands = sorted(raw.rglob("spectra.csv"))
    if cands:
        return cands[0]
    for c in sorted(raw.rglob("*.csv")):
        try:
            with open(c, "r", encoding="utf-8", errors="replace") as f:
                head = f.readline().lower()
        except OSError:
            continue
        if "smiles" in head and "peaks" in head:
            return c
    raise FileNotFoundError(f"No spectra.csv (smiles+peaks) found under {raw}")


def _parse_peaks(s: str) -> list[tuple[float, float]]:
    out = []
    for tok in str(s).split(";"):
        tok = tok.strip()
        if not tok:
            continue
        a, _, b = tok.partition(",")
        try:
            out.append((float(a), float(b)))
        except ValueError:
            continue
    return out


def _peaks_to_str(peaks: list[tuple[float, float]]) -> str:
    return ";".join(f"{mz:.4f},{int(round(it))}" for mz, it in peaks)


def _morgan_bits(mol, gen) -> str:
    fp = gen.GetFingerprint(mol)
    return fp.ToBitString()


def _scaffold_key(mol, canonical_smiles: str):
    from rdkit.Chem.Scaffolds import MurckoScaffold
    try:
        scaf = MurckoScaffold.MurckoScaffoldSmiles(mol=mol)
    except Exception:
        scaf = ""
    if not scaf:
        return ("M", canonical_smiles)   # acyclic -> own group
    return ("S", scaf)


def _load_and_featurise(spectra_csv: Path):
    from rdkit import Chem
    from rdkit import RDLogger
    from rdkit.Chem import rdFingerprintGenerator
    RDLogger.DisableLog("rdApp.*")
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=MORGAN_RADIUS, fpSize=N_BITS)

    fp_cache: dict[str, str] = {}
    scaf_cache: dict[str, tuple] = {}
    rows: list[dict] = []

    with open(spectra_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for rec in reader:
            smiles = (rec.get("smiles") or "").strip()
            peaks = _parse_peaks(rec.get("peaks") or "")
            if not smiles or len(peaks) < MIN_PEAKS_OUT:
                continue
            try:
                prec = float(rec.get("precursor_mz") or "nan")
            except ValueError:
                continue
            if not (prec == prec):
                continue
            if smiles not in fp_cache:
                mol = Chem.MolFromSmiles(smiles)
                if mol is None:
                    fp_cache[smiles] = ""
                    scaf_cache[smiles] = ("M", smiles)
                else:
                    fp_cache[smiles] = _morgan_bits(mol, gen)
                    scaf_cache[smiles] = _scaffold_key(mol, smiles)
            fp = fp_cache[smiles]
            if not fp:
                continue
            rows.append({
                "smiles": smiles,
                "scaffold": scaf_cache[smiles],
                "adduct": (rec.get("adduct") or "").strip(),
                "ion_mode": (rec.get("ion_mode") or "").strip(),
                "precursor_mz": prec,
                "peaks": peaks,
                "fingerprint": fp,
            })
    return rows


def _scaffold_split(rows: list[dict]):
    by_scaf: dict[tuple, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        by_scaf[r["scaffold"]].append(i)
    scaffolds = sorted(by_scaf.keys())
    rng = np.random.default_rng(SPLIT_SEED)
    order = rng.permutation(len(scaffolds))
    total = len(rows)
    target_test = int(round(total * TEST_SCAFFOLD_FRACTION))

    test_scaf: set = set()
    n_test = 0
    for oi in order:
        scaf = scaffolds[int(oi)]
        if n_test >= target_test:
            break
        test_scaf.add(scaf)
        n_test += len(by_scaf[scaf])

    train_idx, test_idx = [], []
    for i, r in enumerate(rows):
        if r["scaffold"] in test_scaf:
            test_idx.append(i)
        else:
            train_idx.append(i)
    return train_idx, test_idx


def _det_subsample(idx: list[int], n: int, seed: int) -> list[int]:
    idx = sorted(idx)
    if n >= len(idx):
        return idx
    rng = np.random.default_rng(seed)
    chosen = rng.choice(len(idx), size=n, replace=False)
    return sorted(idx[int(c)] for c in chosen)


def _perturb_peaks(peaks: list[tuple[float, float]], prec: float, rid: int):
    rng = _stable_rng(PERTURB_SEED, rid)
    rng_sp = _stable_rng(SPURIOUS_SEED, rid)
    if not peaks:
        return peaks
    max_it = max(it for _, it in peaks) or 1.0
    kept = []
    for mz, it in peaks:
        norm = it / max_it * BASE_PEAK_NORM
        if norm < BASE_PEAK_NORM * 0.02 and rng.random() < PEAK_DROPOUT:
            continue
        mz2 = mz + float(rng.normal(0.0, MZ_JITTER_DA))
        it2 = norm * (1.0 + float(rng.normal(0.0, INTENSITY_JITTER)))
        it2 = max(1.0, it2)
        if mz2 > 0:
            kept.append((mz2, it2))
    n_spurious = int(rng_sp.integers(0, MAX_SPURIOUS + 1))
    lo = 50.0
    hi = max(lo + 1.0, prec - 1.0)
    for _ in range(n_spurious):
        mz_s = float(rng_sp.uniform(lo, hi))
        it_s = float(rng_sp.uniform(1.0, BASE_PEAK_NORM * 0.05))
        kept.append((mz_s, it_s))
    kept.sort(key=lambda p: p[0])
    merged: list[tuple[float, float]] = []
    for mz, it in kept:
        if merged and abs(mz - merged[-1][0]) < MZ_MERGE_TOL:
            pm, pi = merged[-1]
            merged[-1] = (pm, max(pi, it))
        else:
            merged.append((mz, it))
    return merged


def prepare(raw: Path, public: Path, private: Path) -> None:
    _ensure_rdkit()
    raw, public, private = Path(raw), Path(public), Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    spectra_csv = _find_spectra_csv(raw)
    print(f"  [load] {spectra_csv}")
    rows = _load_and_featurise(spectra_csv)
    print(f"  [featurise] {len(rows)} spectra, "
          f"{len({r['scaffold'] for r in rows})} scaffold groups")

    train_idx, test_idx = _scaffold_split(rows)
    train_idx = _det_subsample(train_idx, N_TRAIN, SAMPLE_SEED)
    test_idx = _det_subsample(test_idx, N_TEST, SAMPLE_SEED ^ 0x99)

    # _det_subsample returns indices in their original spectra.csv order; ids are
    # then assigned by enumeration position, so without a shuffle the public id
    # order would encode the raw row order (a forbidden side-channel). Shuffle
    # both splits with a fixed seed so the id<->raw-row mapping is fully detached
    # while staying deterministic / byte-reproducible across runs.
    rng_shuffle = np.random.default_rng(SPLIT_SEED ^ 0x11)
    train_idx = np.asarray(train_idx, dtype=np.int64)
    test_idx = np.asarray(test_idx, dtype=np.int64)
    rng_shuffle.shuffle(train_idx)
    rng_shuffle.shuffle(test_idx)
    train_idx = train_idx.tolist()
    test_idx = test_idx.tolist()
    print(f"  [split] {len(train_idx)} train / {len(test_idx)} test (scaffold-disjoint)")

    train_rows, test_rows, answer_rows, sample_rows = [], [], [], []

    for local_i, gi in enumerate(train_idx):
        r = rows[gi]
        rid = 1 + local_i
        pk = _perturb_peaks(r["peaks"], r["precursor_mz"], rid)
        if len(pk) < MIN_PEAKS_OUT:
            continue
        train_rows.append({
            "id": rid,
            "adduct": r["adduct"],
            "ion_mode": r["ion_mode"],
            "precursor_mz": f"{r['precursor_mz']:.4f}",
            "n_peaks": len(pk),
            "peaks": _peaks_to_str(pk),
            "fingerprint": FP_PREFIX + r["fingerprint"],
        })

    for local_i, gi in enumerate(test_idx):
        r = rows[gi]
        rid = 1_000_000 + local_i
        pk = _perturb_peaks(r["peaks"], r["precursor_mz"], rid)
        if len(pk) < MIN_PEAKS_OUT:
            continue
        test_rows.append({
            "id": rid,
            "adduct": r["adduct"],
            "ion_mode": r["ion_mode"],
            "precursor_mz": f"{r['precursor_mz']:.4f}",
            "n_peaks": len(pk),
            "peaks": _peaks_to_str(pk),
        })
        answer_rows.append({"id": rid, "fingerprint": FP_PREFIX + r["fingerprint"]})
        sample_rows.append({"id": rid, "pred_probs": "",
                            "_ion_mode": r["ion_mode"], "_adduct": r["adduct"],
                            "_prec": r["precursor_mz"]})

    # ---- training marginals ----
    # Overall per-bit TRAINING marginal = the climatological reference embedded
    # into grade.py as P_HAT_TRAIN. It MUST be a fixed standard derived strictly
    # from the training split (never from the hidden test set). One decode pass
    # over the train fingerprints feeds both this and the conditional baseline.
    train_acc = np.zeros(N_BITS, dtype=np.float64)
    cond_acc: dict[tuple, np.ndarray] = {}
    cond_cnt: dict[tuple, int] = {}
    for tr in train_rows:
        bits = tr["fingerprint"][len(FP_PREFIX):]
        vec = (np.frombuffer(bits.encode("ascii"), dtype=np.uint8) - ord("0")).astype(np.float64)
        train_acc += vec
        key = (tr["ion_mode"], tr["adduct"], int(float(tr["precursor_mz"]) // SAMPLE_MZ_BIN))
        if key not in cond_acc:
            cond_acc[key] = np.zeros(N_BITS, dtype=np.float64)
            cond_cnt[key] = 0
        cond_acc[key] += vec
        cond_cnt[key] += 1

    n_train_used = len(train_rows)
    p_hat_train = train_acc / max(1, n_train_used)
    _write_phat(private / "p_hat_train.txt", p_hat_train)
    bs_ref_train = float(np.mean(p_hat_train * (1.0 - p_hat_train)))
    print(f"  [phat] wrote private/p_hat_train.txt over {n_train_used} train rows; "
          f"BS_ref(train)={bs_ref_train:.8f}. Embed this array as P_HAT_TRAIN in grade.py.")

    # Conditional baseline, shrunk toward the overall marginal for sparse cells.
    cond_marginal: dict[tuple, np.ndarray] = {}
    for key in cond_acc:
        cond_marginal[key] = ((cond_acc[key] + SAMPLE_SHRINK * p_hat_train)
                              / (cond_cnt[key] + SAMPLE_SHRINK))
    for s in sample_rows:
        key = (s.pop("_ion_mode"), s.pop("_adduct"),
               int(float(s.pop("_prec")) // SAMPLE_MZ_BIN))
        probs = cond_marginal.get(key, p_hat_train)
        s["pred_probs"] = ";".join(f"{p:.4f}" for p in probs)

    train_cols = ["id", "adduct", "ion_mode", "precursor_mz", "n_peaks", "peaks", "fingerprint"]
    test_cols = ["id", "adduct", "ion_mode", "precursor_mz", "n_peaks", "peaks"]
    _write_csv(public / "train.csv", train_rows, train_cols)
    _write_csv(public / "test.csv", test_rows, test_cols)
    _write_csv(public / "sample_submission.csv", sample_rows, ["id", "pred_probs"])
    _write_csv(private / "answers.csv", answer_rows, ["id", "fingerprint"])

    print(f"  [done] train={len(train_rows)} rows, test={len(test_rows)} rows, "
          f"fingerprint={N_BITS} bits (Morgan r{MORGAN_RADIUS}).")


def _write_csv(path: Path, rows: list[dict], cols: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def _write_phat(path: Path, p_hat: np.ndarray) -> None:
    """Persist the training per-bit marginal as a ready-to-paste Python literal
    (one float per bit, 6 dp) so it can be embedded verbatim into grade.py."""
    body = ", ".join(f"{v:.6f}" for v in p_hat.tolist())
    path.write_text(f"P_HAT_TRAIN = [{body}]\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("public"))
    ap.add_argument("--private", type=Path, default=Path("private"))
    args = ap.parse_args()
    prepare(args.raw, args.public, args.private)
    print("OK: prepare complete.")
