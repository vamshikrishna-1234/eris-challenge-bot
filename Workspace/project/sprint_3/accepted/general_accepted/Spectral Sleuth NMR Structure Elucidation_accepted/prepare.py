"""
prepare.py - Constitutional Isomer Identification From Carbon NMR Spectra

For each target molecule the solver is shown:

  * a rendered ¹³C NMR stick spectrum (PNG). The peak positions are NOT a
    recorded measurement — they are the output of a structure → shift
    predictor (see `_predict_shifts` below) plus per-peak position jitter,
    height jitter, baseline noise, peak dropout, and inserted spurious
    peaks. The image is therefore not directly comparable to any recorded
    spectrum that may exist in any external NMR repository.
  * the molecular formula;
  * K candidate SMILES that ALL share that formula (constitutional isomers),
    exactly one of which is the molecule that produced the displayed
    spectrum. Distractors are drawn from the same formula group and matched
    on predicted carbon peak count so that "count the peaks" does not
    isolate the answer.

The solver must output a probability distribution over the K candidates.

Anti-leakage:
  * The displayed spectrum is a function of structure (a HOSE-style atom
    environment shift predictor), not a measurement, so an attacker cannot
    look up any candidate's recorded spectrum in any external archive and
    obtain the right answer — recorded shifts and predicted shifts disagree.
  * Train and test are split at the level of whole molecular-formula groups,
    so no candidate that appears at test time is ever shown (as a target or
    a distractor) at train time.
  * Candidate order is shuffled per row; the true index is uniform over 1..K.
  * Source database IDs, InChI strings, atom assignments, exact peak tables
    and the underlying predictor's per-atom outputs are NOT exposed — only
    the rendered (perturbed) spectrum image, the formula, and the candidate
    SMILES.

Outputs (platform contract):
  public/train/images/<id>.png, public/train.csv   (with labels)
  public/test/images/<id>.png,  public/test.csv    (no labels)
  public/sample_submission.csv
  private/answers.csv                              (id + label)
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


# -------- constants --------

N_TRAIN = 4500
N_TEST = 1200
K = 5

PPM_MIN = -5.0
PPM_MAX = 225.0
IMG_W = 900
IMG_H = 150

POS_JITTER_PPM = 2.5        # std of per-peak position jitter (ppm)
HEIGHT_JITTER = 0.20        # relative height jitter
BASELINE_NOISE = 0.03       # grayscale baseline speckle
PEAK_MERGE_PPM = 1.0        # peaks closer than this (after jitter) are merged
PEAK_DROPOUT = 0.25         # fraction of peaks randomly omitted from the render
FAKE_PEAK_RATE = 0.20       # fraction of additional spurious peaks (of true count)

TEST_GROUP_FRACTION = 0.20
PEAKCOUNT_TOL = 2

ENV_RADIUS = 2
GLOBAL_C13_FALLBACK = 80.0  # used only for atoms whose env never appears

SPLIT_SEED = 0x5A1C7E11
SAMPLE_SEED = 0x5A1C7E22
DISTRACTOR_SEED = 0x5A1C7E33
RENDER_SEED = 0x5A1C7E44
SHUFFLE_SEED = 0x5A1C7E55
FAKE_PEAK_SEED = 0x5A1C7E66


def _ensure_rdkit():
    try:
        import rdkit  # noqa: F401
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rdkit"])


def _ensure_pillow():
    try:
        import PIL  # noqa: F401
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])


def _find_sdf(raw: Path) -> Path:
    """Locate the SDF in the raw upload by content (URL uploads may rename to
    `download` and strip the `.sd` extension)."""
    by_ext = sorted(raw.rglob("*.sd")) + sorted(raw.rglob("*.sdf"))
    for c in by_ext:
        if "signal" in c.name.lower():
            return c
    if by_ext:
        return by_ext[0]
    for c in sorted(raw.rglob("*")):
        if not c.is_file() or c.stat().st_size < 1024:
            continue
        try:
            with open(c, "r", encoding="utf-8", errors="replace") as f:
                head = f.read(4096)
        except OSError:
            continue
        if "V2000" in head and ("> <" in head or "$$$$" in head):
            return c
    raise FileNotFoundError(f"No SDF-format file found under {raw}")


def _stable_rng(seed: int, key: int) -> np.random.Generator:
    mixed = (int(seed) ^ ((int(key) * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    return np.random.default_rng(mixed)


def _parse_13c_atom_shifts(spec: str) -> list[tuple[int, float]]:
    """Parse 'shift;intensity_mult;atom_idx|...' into [(atom_idx, shift), ...].
    Returned only for use in fitting the HOSE-style shift predictor — never
    surfaced to the solver."""
    pairs: list[tuple[int, float]] = []
    for entry in spec.strip().strip("|").split("|"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(";")
        if len(parts) < 3:
            continue
        try:
            shift = float(parts[0])
            atom_idx = int(parts[2])
        except ValueError:
            continue
        pairs.append((atom_idx, shift))
    return pairs


def _atom_env_signature(mol, atom_idx: int, radius: int):
    """Hash-able BFS-layered descriptor of the atom's neighbourhood. Used as
    the key of the shift-prediction lookup table."""
    visited = {atom_idx}
    frontier = [atom_idx]
    layers = []
    for _ in range(radius + 1):
        layer = []
        for a in sorted(frontier):
            atom = mol.GetAtomWithIdx(a)
            layer.append((
                atom.GetSymbol(),
                int(atom.GetDegree()),
                int(atom.GetTotalNumHs()),
                bool(atom.GetIsAromatic()),
                bool(atom.IsInRing()),
                int(atom.GetFormalCharge()),
            ))
        layers.append(tuple(layer))
        new_frontier = []
        for a in frontier:
            for nbr in mol.GetAtomWithIdx(a).GetNeighbors():
                ni = nbr.GetIdx()
                if ni not in visited:
                    visited.add(ni)
                    new_frontier.append(ni)
        frontier = sorted(new_frontier)
    return tuple(layers)


def _load_molecules(sdf_path: Path):
    """Return list of dicts with the molecule object plus per-atom recorded
    13C shifts (for predictor fitting). One entry per distinct canonical
    SMILES; first record per SMILES wins."""
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    from rdkit import RDLogger
    RDLogger.DisableLog("rdApp.*")

    seen: set[str] = set()
    mols: list[dict] = []
    supplier = Chem.ForwardSDMolSupplier(str(sdf_path), sanitize=True, removeHs=True)
    n_seen = 0
    for mol in supplier:
        if mol is None or not mol.HasProp("Spectrum 13C 0"):
            continue
        n_seen += 1
        try:
            smiles = Chem.MolToSmiles(mol)
            formula = rdMolDescriptors.CalcMolFormula(mol)
        except Exception:
            continue
        if smiles in seen:
            continue
        atom_shifts = _parse_13c_atom_shifts(mol.GetProp("Spectrum 13C 0"))
        # only keep records where atom indices are within range and reference carbons
        clean: list[tuple[int, float]] = []
        for ai, sh in atom_shifts:
            if 0 <= ai < mol.GetNumAtoms() and mol.GetAtomWithIdx(ai).GetSymbol() == "C":
                clean.append((ai, sh))
        if len(clean) < 2:
            continue
        seen.add(smiles)
        mols.append({
            "smiles": smiles,
            "formula": formula,
            "mol": mol,
            "atom_shifts": clean,
        })
        if n_seen % 5000 == 0:
            print(f"  [load] scanned {n_seen} 13C records, {len(mols)} unique molecules")
    print(f"  [load] total unique molecules with 13C: {len(mols)}")
    return mols


def _build_hose_tables(mols):
    """Aggregate per-atom recorded shifts by their environment signature, at
    radius ENV_RADIUS and at radius 1 as a fallback for unseen environments."""
    table_r2: dict = defaultdict(list)
    table_r1: dict = defaultdict(list)
    for entry in mols:
        mol = entry["mol"]
        for ai, sh in entry["atom_shifts"]:
            try:
                sig2 = _atom_env_signature(mol, ai, ENV_RADIUS)
                sig1 = _atom_env_signature(mol, ai, 1)
            except Exception:
                continue
            table_r2[sig2].append(sh)
            table_r1[sig1].append(sh)
    mean_r2 = {k: float(np.mean(v)) for k, v in table_r2.items()}
    mean_r1 = {k: float(np.mean(v)) for k, v in table_r1.items()}
    print(f"  [hose] env signatures: r{ENV_RADIUS}={len(mean_r2)}  r1={len(mean_r1)}")
    return mean_r2, mean_r1


def _predict_shifts(mol, mean_r2, mean_r1) -> list[float]:
    """Return predicted ¹³C shift for every carbon atom in the molecule."""
    shifts: list[float] = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != "C":
            continue
        ai = atom.GetIdx()
        try:
            sig2 = _atom_env_signature(mol, ai, ENV_RADIUS)
        except Exception:
            sig2 = None
        if sig2 is not None and sig2 in mean_r2:
            shifts.append(mean_r2[sig2])
            continue
        try:
            sig1 = _atom_env_signature(mol, ai, 1)
        except Exception:
            sig1 = None
        if sig1 is not None and sig1 in mean_r1:
            shifts.append(mean_r1[sig1])
            continue
        shifts.append(GLOBAL_C13_FALLBACK)
    return shifts


def _merged_peak_count(shifts: list[float]) -> int:
    """Count peaks after coalescing predicted shifts within PEAK_MERGE_PPM."""
    if not shifts:
        return 0
    s = sorted(shifts)
    n = 1
    last = s[0]
    for v in s[1:]:
        if v - last >= PEAK_MERGE_PPM:
            n += 1
            last = v
    return n


def _render_spectrum(shifts: list[float], rng: np.random.Generator):
    """Render the predicted shifts as a noisy stick spectrum image. Applies
    per-peak position jitter, peak dropout, fake-peak insertion, height
    jitter, peak merging, and baseline speckle."""
    from PIL import Image
    canvas = np.zeros((IMG_H, IMG_W), dtype=np.float32)
    canvas += rng.normal(0.0, BASELINE_NOISE, size=canvas.shape).astype(np.float32)

    kept: list[float] = []
    for s in shifts:
        if rng.random() < PEAK_DROPOUT:
            continue
        kept.append(s + float(rng.normal(0.0, POS_JITTER_PPM)))
    n_fake = int(round(FAKE_PEAK_RATE * len(shifts)))
    for _ in range(n_fake):
        kept.append(float(rng.uniform(0.0, 220.0)))
    kept.sort()
    merged: list[float] = []
    for sj in kept:
        if merged and abs(sj - merged[-1]) < PEAK_MERGE_PPM:
            continue
        merged.append(sj)

    for sj in merged:
        if sj < PPM_MIN or sj > PPM_MAX:
            continue
        frac = (PPM_MAX - sj) / (PPM_MAX - PPM_MIN)
        x = int(round(frac * (IMG_W - 1)))
        h = float(np.clip(0.85 + rng.normal(0.0, HEIGHT_JITTER), 0.35, 1.0))
        top = int(round((1.0 - h) * (IMG_H - 6))) + 2
        x0, x1 = max(0, x - 1), min(IMG_W, x + 2)
        canvas[top:IMG_H - 2, x0:x1] = 1.0

    canvas = np.clip(canvas, 0.0, 1.0)
    arr = (canvas * 255.0 + 0.5).astype(np.uint8)
    return Image.fromarray(arr, mode="L")


def _choose_distractors(group: list[dict], target: dict, rng: np.random.Generator) -> list[dict]:
    pool = [m for m in group if m["smiles"] != target["smiles"]]
    tpc = target["pred_peakcount"]
    near = [m for m in pool if abs(m["pred_peakcount"] - tpc) <= PEAKCOUNT_TOL]
    far = [m for m in pool if abs(m["pred_peakcount"] - tpc) > PEAKCOUNT_TOL]
    rng.shuffle(near)
    rng.shuffle(far)
    return (near + far)[:K - 1]


def _build_split_rows(usable, formulas_set, n_target, seed):
    rng = np.random.default_rng(seed)
    pool = [m for f in sorted(formulas_set) for m in usable[f]]
    rng.shuffle(pool)
    return pool[:n_target]


def _assemble_candidates(target, group, rid):
    rng_d = _stable_rng(DISTRACTOR_SEED, rid)
    rng_s = _stable_rng(SHUFFLE_SEED, rid)
    distractors = _choose_distractors(group, target, rng_d)
    if len(distractors) < K - 1:
        return None
    candidates = [target["smiles"]] + [d["smiles"] for d in distractors]
    order = list(range(K))
    rng_s.shuffle(order)
    shuffled = [candidates[i] for i in order]
    return shuffled, order.index(0) + 1  # 1-based


def _materialise(targets, usable, out_dir, is_train):
    rows = []
    for local_i, target in enumerate(targets):
        rid = (1 if is_train else 1_000_000) + local_i
        asm = _assemble_candidates(target, usable[target["formula"]], rid)
        if asm is None:
            continue
        candidates, true_idx = asm
        rng_r = _stable_rng(RENDER_SEED, rid)
        img = _render_spectrum(target["pred_shifts"], rng_r)
        img_rel = f"images/{rid:07d}.png"
        img.save(out_dir / img_rel)
        row = {"id": rid, "image_path": img_rel, "molecular_formula": target["formula"]}
        for k in range(K):
            row[f"candidate_{k+1}"] = candidates[k]
        row["true_isomer_idx"] = true_idx
        rows.append(row)
    return rows


def _materialise_test(targets, usable, out_dir):
    rows: list[dict] = []
    answers: list[dict] = []
    for local_i, target in enumerate(targets):
        rid = 1_000_000 + local_i
        asm = _assemble_candidates(target, usable[target["formula"]], rid)
        if asm is None:
            continue
        candidates, true_idx = asm
        rng_r = _stable_rng(RENDER_SEED, rid)
        img = _render_spectrum(target["pred_shifts"], rng_r)
        img_rel = f"images/{rid:07d}.png"
        img.save(out_dir / img_rel)
        row = {"id": rid, "image_path": img_rel, "molecular_formula": target["formula"]}
        for k in range(K):
            row[f"candidate_{k+1}"] = candidates[k]
        rows.append(row)
        answers.append({"id": rid, "true_isomer_idx": true_idx})
    return rows, answers


def prepare(raw: Path, public: Path, private: Path) -> None:
    _ensure_rdkit()
    _ensure_pillow()
    raw, public, private = Path(raw), Path(public), Path(private)
    (public / "train" / "images").mkdir(parents=True, exist_ok=True)
    (public / "test" / "images").mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    sdf_path = _find_sdf(raw)
    print(f"  [discover] using {sdf_path.name}")
    raw_mols = _load_molecules(sdf_path)
    mean_r2, mean_r1 = _build_hose_tables(raw_mols)

    # attach predicted shift list + predicted (merged) peak count to each entry
    mols = []
    for entry in raw_mols:
        pred = _predict_shifts(entry["mol"], mean_r2, mean_r1)
        if len(pred) < 2:
            continue
        mols.append({
            "smiles": entry["smiles"],
            "formula": entry["formula"],
            "pred_shifts": pred,
            "pred_peakcount": _merged_peak_count(pred),
        })

    groups: dict[str, list[dict]] = {}
    for m in mols:
        groups.setdefault(m["formula"], []).append(m)
    usable = {f: g for f, g in groups.items() if len(g) >= K}
    print(f"  [group] {len(usable)} formula groups with >= {K} isomers")

    formulas = sorted(usable.keys())
    rng_split = np.random.default_rng(SPLIT_SEED)
    rng_split.shuffle(formulas)
    n_test_groups = max(1, int(round(len(formulas) * TEST_GROUP_FRACTION)))
    test_formulas = set(formulas[:n_test_groups])
    train_formulas = set(formulas[n_test_groups:])

    train_targets = _build_split_rows(usable, train_formulas, N_TRAIN, SAMPLE_SEED)
    test_targets = _build_split_rows(usable, test_formulas, N_TEST, SAMPLE_SEED ^ 0x99)
    print(f"  [split] {len(train_targets)} train targets, {len(test_targets)} test targets")

    train_rows = _materialise(train_targets, usable, public / "train", is_train=True)
    test_rows, answer_rows = _materialise_test(test_targets, usable, public / "test")

    _write_train_csv(public / "train.csv", train_rows)
    _write_test_csv(public / "test.csv", test_rows)
    _write_answers_csv(private / "answers.csv", answer_rows)
    _write_sample_submission(public / "sample_submission.csv", test_rows)
    print(f"  [done] {len(train_rows)} train rows, {len(test_rows)} test rows.")


def _cand_cols():
    return [f"candidate_{k+1}" for k in range(K)]


def _write_train_csv(path, rows):
    _write_csv(path, rows, ["id", "image_path", "molecular_formula"] + _cand_cols() + ["true_isomer_idx"])


def _write_test_csv(path, rows):
    _write_csv(path, rows, ["id", "image_path", "molecular_formula"] + _cand_cols())


def _write_answers_csv(path, rows):
    _write_csv(path, rows, ["id", "true_isomer_idx"])


def _write_sample_submission(path, test_rows):
    prob_cols = [f"pred_prob_{k+1}" for k in range(K)]
    rows = [{"id": r["id"], **{c: round(1.0 / K, 4) for c in prob_cols}} for r in test_rows]
    _write_csv(path, rows, ["id"] + prob_cols)


def _write_csv(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw"))
    ap.add_argument("--public", type=Path, default=Path("public"))
    ap.add_argument("--private", type=Path, default=Path("private"))
    args = ap.parse_args()
    prepare(args.raw, args.public, args.private)
