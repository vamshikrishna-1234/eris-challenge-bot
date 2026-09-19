# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

Solvers must read a carbon-13 NMR spectrum and decide which of several constitutional isomers — molecules with an identical molecular formula but different connectivity — actually produced it, then express calibrated uncertainty over the candidates. The candidates are matched on carbon peak-count, so naive "count the peaks" heuristics do not isolate the answer; distinguishing the true structure requires reasoning about chemical-shift windows, molecular symmetry, and how connectivity maps to the observed peak pattern. No off-the-shelf vision backbone solves this, and there is no public spectrum-to-structure foundation model to fine-tune; the task rewards genuine spectral reasoning rather than pattern matching.

---

## 2) Challenge Title

```
Constitutional Isomer Identification From Carbon NMR Spectra
```

---

## 3) Problem Description

### Overview

# Constitutional Isomer Identification From Carbon NMR Spectra

You are given a **carbon-13 NMR spectrum** of a single small organic molecule, its **molecular formula**, and a short list of **K = 5 candidate structures** (as SMILES strings) that *all share that exact molecular formula*. Exactly one candidate is the molecule that produced the spectrum; the other four are **constitutional isomers** — same atoms, different connectivity. Your job is to output a **probability distribution over the five candidates**, expressing both which structure you believe is correct and how confident you are.

This is a **chemistry × computer-vision** task that breaks the standard "image → label" setup. The spectrum is presented as a rendered 1-D stick plot (peaks along a chemical-shift axis), so the solver must first read the peak pattern from the image and then connect it to molecular structure. The two abilities the score rewards are:

1. **Identification** — pick the candidate whose structure is consistent with the observed ¹³C peaks. Because the distractors share the molecular formula *and* are matched to have a similar number of carbon peaks, neither the formula nor a raw peak count resolves the answer. A solver must reason about where peaks fall (carbonyl carbons appear far downfield, aromatic carbons in a characteristic mid-range, aliphatic carbons upfield), how molecular symmetry reduces the number of distinct carbon environments, and how each candidate's connectivity would distribute its carbons across the spectrum.
2. **Calibration** — assign honest probabilities. When two candidates are hard to separate, a well-calibrated distribution that hedges between them scores better than an over-confident wrong guess.

A vanilla image model that ignores the candidate structures cannot place the spectrum among the isomers; a model that ignores the spectrum and guesses from the candidate list alone has no signal (the candidates are deliberately equalised). The intended solution combines reading the spectrum with chemical reasoning about each candidate.

The displayed spectra are **not raw recorded measurements**. Each spectrum is synthesised at preparation time from the structure of the true candidate via a deterministic structure → ¹³C-shift relation (a HOSE-style atom-environment average shift, fit once on the training portion of the corpus), with per-peak position jitter, peak dropout, inserted spurious peaks, height jitter, and baseline noise applied on top. As a result, the image's peaks systematically disagree with any specific molecule's recorded shifts that may exist in any external NMR archive — looking up candidate SMILES against external recorded spectra is therefore both unreliable and explicitly disallowed (see *What Not To Do* below). A small, unadvertised fraction of difficult rows may be effectively ambiguous from the carbon spectrum alone — this is an irreducible error floor, and the test labels themselves are exact.

### Evaluation

For the full test set the grader computes:

```
top1   = mean over rows of [1 if argmax(pred_prob) == true_isomer_idx else 0]

calib  = mean over rows of max(0, 1 - Brier / Brier_uniform)
         where Brier = sum_k (pred_prob_k - onehot_k)^2  over the K candidates,
         and Brier_uniform is the Brier score of the flat 1/K guess.

Final  = 0.65 * top1^2 + 0.35 * calib^2,  clipped to [0, 1]
```

* `top1` is plain identification accuracy: the candidate receiving the highest predicted probability is compared to the true structure. Random guessing over K = 5 candidates yields `top1 = 0.20` in expectation.
* `calib` is a **proper-scoring** term built from the multi-class Brier score, normalised so that a flat `1/K` submission scores exactly `0` and a perfect confident submission scores `1`. A confidently-wrong row is floored at `0`. This rewards solvers that express honest uncertainty and spreads the score distribution away from the saturated top end.
* **Both terms are squared** before weighting so the composite compresses at the high end — an "almost there" model does not coast to a high score — while a perfect oracle (every row identified with full confidence) still reaches the maximum of `1.0`.

**Higher is better.** Minimum: 0.0, Maximum: 1.0.

Probabilities are **normalised per row** by the grader (clipped to be non-negative, then divided by their sum), so they need not sum to 1; an all-zero or invalid row is treated as a uniform guess. The grader returns `0.0` if the submission is missing any required column, contains duplicate `id`s, has an `id` set that does not exactly match `test.csv`, or raises any exception.

### Dataset

* `public/train/images/<id>.png` — one rendered ¹³C NMR stick spectrum per training row (grayscale PNG).
* `public/test/images/<id>.png` — one rendered ¹³C NMR stick spectrum per test row (grayscale PNG).
* `public/train.csv` — one row per training molecule: the image path, molecular formula, the five candidate SMILES, and the true candidate index.
* `public/test.csv` — the same fields for test molecules, **without** the label.
* `public/sample_submission.csv` — one row per test `id` in the exact submission format, pre-filled with a flat `1/K` distribution that participants must overwrite to score above the uniform floor.

Row counts are seed-dependent and printed at the end of `prepare.py` (typical: ~4,500 train rows and ~1,200 test rows; one row = 1 spectrum PNG + 1 CSV row). Train and test never share a molecular formula, so no candidate structure seen at test time appears anywhere in the training data.

#### File overview

Files shipped to participants: `public/train/images/<id>.png` (rendered ¹³C spectra, one per training row), `public/test/images/<id>.png` (rendered ¹³C spectra, one per test row), `public/train.csv` (labelled training rows), `public/test.csv` (test rows, no label), and `public/sample_submission.csv` (submission template with the full 6-column shape).

| Item                          | Description                          |
|-------------------------------|--------------------------------------|
| `public/train/images/*.png`   | Rendered ¹³C spectrum, 1 per row      |
| `public/test/images/*.png`    | Rendered ¹³C spectrum, 1 per row      |
| `public/train.csv`            | Labelled training rows                |
| `public/test.csv`             | Test rows, no label                   |
| `public/sample_submission.csv`| Submission template, full shape       |

#### Feature Details

**Training data columns (`public/train.csv`) — 9 columns:**

Columns (in order): `id` (int, unique row identifier), `image_path` (string, relative path to the spectrum PNG), `molecular_formula` (string, e.g. `C9H10O2`), `candidate_1` (string, SMILES), `candidate_2` (string, SMILES), `candidate_3` (string, SMILES), `candidate_4` (string, SMILES), `candidate_5` (string, SMILES), `true_isomer_idx` (int in 1–5, which candidate produced the spectrum).

| Column              | Type   | Description                          |
|---------------------|--------|--------------------------------------|
| `id`                | int    | Unique row identifier                |
| `image_path`        | string | Relative path to spectrum PNG        |
| `molecular_formula` | string | Shared formula, e.g. `C9H10O2`       |
| `candidate_1`       | string | Candidate 1 SMILES                   |
| `candidate_2`       | string | Candidate 2 SMILES                   |
| `candidate_3`       | string | Candidate 3 SMILES                   |
| `candidate_4`       | string | Candidate 4 SMILES                   |
| `candidate_5`       | string | Candidate 5 SMILES                   |
| `true_isomer_idx`   | int    | True candidate index, 1–5            |

**Test metadata columns (`public/test.csv`) — 8 columns:**

Columns (in order): `id` (int, unique row identifier), `image_path` (string, relative path to the spectrum PNG), `molecular_formula` (string), `candidate_1` (string, SMILES), `candidate_2` (string, SMILES), `candidate_3` (string, SMILES), `candidate_4` (string, SMILES), `candidate_5` (string, SMILES). No label column is present.

| Column              | Type   | Description                          |
|---------------------|--------|--------------------------------------|
| `id`                | int    | Unique row identifier                |
| `image_path`        | string | Relative path to spectrum PNG        |
| `molecular_formula` | string | Shared formula                       |
| `candidate_1`       | string | Candidate 1 SMILES                   |
| `candidate_2`       | string | Candidate 2 SMILES                   |
| `candidate_3`       | string | Candidate 3 SMILES                   |
| `candidate_4`       | string | Candidate 4 SMILES                   |
| `candidate_5`       | string | Candidate 5 SMILES                   |

**Submission columns (`public/sample_submission.csv` and your final submission) — 6 columns:**

Columns (in order): `id` (int, same set as `public/test.csv`), `pred_prob_1` (float ≥ 0), `pred_prob_2` (float ≥ 0), `pred_prob_3` (float ≥ 0), `pred_prob_4` (float ≥ 0), `pred_prob_5` (float ≥ 0). Each `pred_prob_k` is the relative probability that candidate `k` produced the spectrum; rows are normalised by the grader.

| Column        | Type  | Constraint                          |
|---------------|-------|-------------------------------------|
| `id`          | int   | Same set as `public/test.csv`        |
| `pred_prob_1` | float | ≥ 0, prob. of candidate 1            |
| `pred_prob_2` | float | ≥ 0, prob. of candidate 2            |
| `pred_prob_3` | float | ≥ 0, prob. of candidate 3            |
| `pred_prob_4` | float | ≥ 0, prob. of candidate 4            |
| `pred_prob_5` | float | ≥ 0, prob. of candidate 5            |

### Submission

Submit a CSV file with a header row and **exactly one row per `id` in `test.csv`**. The header must contain these **6 columns in this order**: `id`, `pred_prob_1`, `pred_prob_2`, `pred_prob_3`, `pred_prob_4`, `pred_prob_5`.

| Column        | Type  | Description                          |
|---------------|-------|--------------------------------------|
| `id`          | int   | Identifier from `test.csv`           |
| `pred_prob_1` | float | Probability candidate 1 is correct   |
| `pred_prob_2` | float | Probability candidate 2 is correct   |
| `pred_prob_3` | float | Probability candidate 3 is correct   |
| `pred_prob_4` | float | Probability candidate 4 is correct   |
| `pred_prob_5` | float | Probability candidate 5 is correct   |

**Requirements:**

* Header row plus exactly one row per `id` in `test.csv` — the `id` set must match `test.csv` exactly. Duplicate `id`s cause the grader to return `0.0`.
* Each `pred_prob_k` should be a non-negative float. Values are clipped to be non-negative and normalised to sum to 1 per row; a row that is all zero, negative, or non-finite is treated as a uniform `1/K` guess.
* The candidate referenced by `pred_prob_k` is `candidate_k` in `test.csv` for that `id`; candidate order is fixed per row but shuffled across rows.
* The grader returns `0.0` if any of the six required columns are missing, if there are duplicate `id`s, or if the `id` set does not match `test.csv`.

**Example of a correctly formatted submission file (illustrative only):**

The three rows below come from three different test `id`s. The full submission has one row per test `id`. The values illustrate the layout — real submissions will have informative per-row probabilities.

```
id,pred_prob_1,pred_prob_2,pred_prob_3,pred_prob_4,pred_prob_5
1000000,0.05,0.70,0.10,0.10,0.05
1000001,0.20,0.20,0.20,0.20,0.20
1000002,0.02,0.03,0.90,0.03,0.02
```

## What Not To Do

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score:

* **Querying any external NMR archive for recorded spectra of the candidate SMILES.** The displayed spectrum is computed from structure via a deterministic structure → ¹³C-shift relation and then perturbed (position jitter, peak dropout, inserted spurious peaks); recorded experimental shifts in any external archive disagree with the image at the level of each peak and so do not identify the correct candidate. External-archive lookup is both unreliable and explicitly disallowed.
* **Ignoring the spectrum.** Any solution that selects a candidate without using the spectrum image (e.g. picking by SMILES string length, lexical order, or a property that is constant across the formula-matched candidates) is rejected — the candidates are equalised so such signals carry no information.
* **Filename / ordering side-channels.** Do not assume the candidate order encodes the answer (it is shuffled per row with a uniform true index), and do not exploit `id` ordering, file mtimes, or any signal outside the spectrum pixels and the CSV columns.
* **Format / range hacks.** Submitting malformed probability rows, extra columns, or values engineered to exploit the grader's normalisation or clipping behaviour.

---

## 4) Tags

```
chemistry, nmr, spectroscopy, computer-vision, structure-elucidation, calibration, multimodal
```

---

## 5) Grading Configuration

- **Scoring direction:** Higher is better
- **Theoretical minimum:** 0.0
- **Theoretical maximum:** 1.0

---

## 6) Grading Script

**Select:** `Custom`

```python
"""
grade.py - Constitutional Isomer Identification From Carbon NMR Spectra

top1   = mean over rows of [1 if argmax(pred_prob) == true_isomer_idx else 0]
calib  = mean over rows of max(0, 1 - Brier / Brier_uniform)
Final  = 0.65 * top1^2 + 0.35 * calib^2, clipped to [0, 1].
"""

from __future__ import annotations

import numpy as np
import pandas as pd


K = 5

W_TOP1 = 0.65
W_CALIB = 0.35

PROB_COLS = [f"pred_prob_{k+1}" for k in range(K)]
BRIER_UNIFORM = (1.0 - 1.0 / K) ** 2 + (K - 1) * (1.0 / K) ** 2


def _normalise_row(vals: np.ndarray) -> np.ndarray:
    v = np.array(vals, dtype=np.float64)
    v[~np.isfinite(v)] = 0.0
    v = np.clip(v, 0.0, None)
    s = v.sum()
    if s <= 0.0:
        return np.full(K, 1.0 / K, dtype=np.float64)
    return v / s


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        required_sub = {"id", *PROB_COLS}
        required_ans = {"id", "true_isomer_idx"}
        if not required_sub.issubset(set(submission.columns)):
            return 0.0
        if not required_ans.issubset(set(answers.columns)):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(int)
            ans["id"] = ans["id"].astype(int)
        except (TypeError, ValueError):
            return 0.0

        if sub["id"].duplicated().any():
            return 0.0
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            return 0.0

        sub = sub.set_index("id")
        ans = ans.set_index("id")

        top1_terms: list[float] = []
        calib_terms: list[float] = []

        for rid, arow in ans.iterrows():
            try:
                true_idx = int(arow["true_isomer_idx"])
            except (TypeError, ValueError):
                return 0.0
            if true_idx < 1 or true_idx > K:
                return 0.0

            probs = _normalise_row(sub.loc[rid, PROB_COLS].to_numpy())

            pred_idx = int(np.argmax(probs)) + 1
            top1_terms.append(1.0 if pred_idx == true_idx else 0.0)

            onehot = np.zeros(K, dtype=np.float64)
            onehot[true_idx - 1] = 1.0
            brier = float(np.sum((probs - onehot) ** 2))
            calib_terms.append(max(0.0, 1.0 - brier / BRIER_UNIFORM))

        if not top1_terms:
            return 0.0

        top1 = float(np.mean(top1_terms))
        calib = float(np.mean(calib_terms))
        final = W_TOP1 * (top1 ** 2) + W_CALIB * (calib ** 2)
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0
```

---

## 7) Prepare Script

**Select:** `Custom`

```python
"""
prepare.py - Constitutional Isomer Identification From Carbon NMR Spectra

For each target molecule the solver is shown a rendered 13C NMR stick spectrum
whose peak positions are NOT a recorded measurement. They are the output of a
HOSE-style atom-environment shift predictor (fit on the training portion of the
corpus) plus per-peak position jitter, peak dropout, inserted spurious peaks,
height jitter, and baseline noise. The image therefore systematically disagrees
with any specific molecule's recorded shifts in any external NMR archive, so
external lookup of recorded spectra cannot recover the answer. The molecular
formula and K=5 candidate SMILES (constitutional isomers of that formula) are
also shown; one is the correct structure. Distractors are matched on predicted
carbon peak count. Train and test are split at the level of whole formula
groups so no candidate at test time appears at train time.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


N_TRAIN = 4500
N_TEST = 1200
K = 5

PPM_MIN = -5.0
PPM_MAX = 225.0
IMG_W = 900
IMG_H = 150

POS_JITTER_PPM = 2.5
HEIGHT_JITTER = 0.20
BASELINE_NOISE = 0.03
PEAK_MERGE_PPM = 1.0
PEAK_DROPOUT = 0.25
FAKE_PEAK_RATE = 0.20

TEST_GROUP_FRACTION = 0.20
PEAKCOUNT_TOL = 2

ENV_RADIUS = 2
GLOBAL_C13_FALLBACK = 80.0

SPLIT_SEED = 0x5A1C7E11
SAMPLE_SEED = 0x5A1C7E22
DISTRACTOR_SEED = 0x5A1C7E33
RENDER_SEED = 0x5A1C7E44
SHUFFLE_SEED = 0x5A1C7E55


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


def _find_sdf(raw):
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


def _stable_rng(seed, key):
    mixed = (int(seed) ^ ((int(key) * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    return np.random.default_rng(mixed)


def _parse_13c_atom_shifts(spec):
    pairs = []
    for entry in spec.strip().strip("|").split("|"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(";")
        if len(parts) < 3:
            continue
        try:
            shift = float(parts[0]); atom_idx = int(parts[2])
        except ValueError:
            continue
        pairs.append((atom_idx, shift))
    return pairs


def _atom_env_signature(mol, atom_idx, radius):
    visited = {atom_idx}
    frontier = [atom_idx]
    layers = []
    for _ in range(radius + 1):
        layer = []
        for a in sorted(frontier):
            atom = mol.GetAtomWithIdx(a)
            layer.append((atom.GetSymbol(), int(atom.GetDegree()),
                          int(atom.GetTotalNumHs()), bool(atom.GetIsAromatic()),
                          bool(atom.IsInRing()), int(atom.GetFormalCharge())))
        layers.append(tuple(layer))
        new_frontier = []
        for a in frontier:
            for nbr in mol.GetAtomWithIdx(a).GetNeighbors():
                ni = nbr.GetIdx()
                if ni not in visited:
                    visited.add(ni); new_frontier.append(ni)
        frontier = sorted(new_frontier)
    return tuple(layers)


def _load_molecules(sdf_path):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors
    from rdkit import RDLogger
    RDLogger.DisableLog("rdApp.*")
    seen, mols = set(), []
    supplier = Chem.ForwardSDMolSupplier(str(sdf_path), sanitize=True, removeHs=True)
    for mol in supplier:
        if mol is None or not mol.HasProp("Spectrum 13C 0"):
            continue
        try:
            smiles = Chem.MolToSmiles(mol)
            formula = rdMolDescriptors.CalcMolFormula(mol)
        except Exception:
            continue
        if smiles in seen:
            continue
        atom_shifts = _parse_13c_atom_shifts(mol.GetProp("Spectrum 13C 0"))
        clean = [(ai, sh) for ai, sh in atom_shifts
                 if 0 <= ai < mol.GetNumAtoms() and mol.GetAtomWithIdx(ai).GetSymbol() == "C"]
        if len(clean) < 2:
            continue
        seen.add(smiles)
        mols.append({"smiles": smiles, "formula": formula, "mol": mol, "atom_shifts": clean})
    return mols


def _build_hose_tables(mols):
    table_r2, table_r1 = defaultdict(list), defaultdict(list)
    for entry in mols:
        for ai, sh in entry["atom_shifts"]:
            try:
                sig2 = _atom_env_signature(entry["mol"], ai, ENV_RADIUS)
                sig1 = _atom_env_signature(entry["mol"], ai, 1)
            except Exception:
                continue
            table_r2[sig2].append(sh); table_r1[sig1].append(sh)
    return ({k: float(np.mean(v)) for k, v in table_r2.items()},
            {k: float(np.mean(v)) for k, v in table_r1.items()})


def _predict_shifts(mol, mean_r2, mean_r1):
    shifts = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != "C":
            continue
        ai = atom.GetIdx()
        sig2 = _atom_env_signature(mol, ai, ENV_RADIUS)
        if sig2 in mean_r2:
            shifts.append(mean_r2[sig2]); continue
        sig1 = _atom_env_signature(mol, ai, 1)
        if sig1 in mean_r1:
            shifts.append(mean_r1[sig1]); continue
        shifts.append(GLOBAL_C13_FALLBACK)
    return shifts


def _merged_peak_count(shifts):
    if not shifts:
        return 0
    s = sorted(shifts); n = 1; last = s[0]
    for v in s[1:]:
        if v - last >= PEAK_MERGE_PPM:
            n += 1; last = v
    return n


def _render_spectrum(shifts, rng):
    from PIL import Image
    canvas = np.zeros((IMG_H, IMG_W), dtype=np.float32)
    canvas += rng.normal(0.0, BASELINE_NOISE, size=canvas.shape).astype(np.float32)
    kept = []
    for s in shifts:
        if rng.random() < PEAK_DROPOUT:
            continue
        kept.append(s + float(rng.normal(0.0, POS_JITTER_PPM)))
    for _ in range(int(round(FAKE_PEAK_RATE * len(shifts)))):
        kept.append(float(rng.uniform(0.0, 220.0)))
    kept.sort()
    merged = []
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
        canvas[top:IMG_H - 2, max(0, x - 1):min(IMG_W, x + 2)] = 1.0
    arr = (np.clip(canvas, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)
    return Image.fromarray(arr, mode="L")


def _choose_distractors(group, target, rng):
    pool = [m for m in group if m["smiles"] != target["smiles"]]
    tpc = target["pred_peakcount"]
    near = [m for m in pool if abs(m["pred_peakcount"] - tpc) <= PEAKCOUNT_TOL]
    far = [m for m in pool if abs(m["pred_peakcount"] - tpc) > PEAKCOUNT_TOL]
    rng.shuffle(near); rng.shuffle(far)
    return (near + far)[:K - 1]


def _assemble_candidates(target, group, rid):
    rng_d = _stable_rng(DISTRACTOR_SEED, rid)
    rng_s = _stable_rng(SHUFFLE_SEED, rid)
    distractors = _choose_distractors(group, target, rng_d)
    if len(distractors) < K - 1:
        return None
    candidates = [target["smiles"]] + [d["smiles"] for d in distractors]
    order = list(range(K)); rng_s.shuffle(order)
    return [candidates[i] for i in order], order.index(0) + 1


def _build_split_rows(usable, formulas_set, n_target, seed):
    rng = np.random.default_rng(seed)
    pool = [m for f in sorted(formulas_set) for m in usable[f]]
    rng.shuffle(pool)
    return pool[:n_target]


def _materialise(targets, usable, out_dir, is_train):
    rows = []
    for local_i, target in enumerate(targets):
        rid = (1 if is_train else 1_000_000) + local_i
        asm = _assemble_candidates(target, usable[target["formula"]], rid)
        if asm is None:
            continue
        candidates, true_idx = asm
        img = _render_spectrum(target["pred_shifts"], _stable_rng(RENDER_SEED, rid))
        img_rel = f"images/{rid:07d}.png"
        img.save(out_dir / img_rel)
        row = {"id": rid, "image_path": img_rel, "molecular_formula": target["formula"]}
        for k in range(K):
            row[f"candidate_{k+1}"] = candidates[k]
        row["true_isomer_idx"] = true_idx
        rows.append(row)
    return rows


def _materialise_test(targets, usable, out_dir):
    rows, answers = [], []
    for local_i, target in enumerate(targets):
        rid = 1_000_000 + local_i
        asm = _assemble_candidates(target, usable[target["formula"]], rid)
        if asm is None:
            continue
        candidates, true_idx = asm
        img = _render_spectrum(target["pred_shifts"], _stable_rng(RENDER_SEED, rid))
        img_rel = f"images/{rid:07d}.png"
        img.save(out_dir / img_rel)
        row = {"id": rid, "image_path": img_rel, "molecular_formula": target["formula"]}
        for k in range(K):
            row[f"candidate_{k+1}"] = candidates[k]
        rows.append(row)
        answers.append({"id": rid, "true_isomer_idx": true_idx})
    return rows, answers


def prepare(raw, public, private):
    _ensure_rdkit(); _ensure_pillow()
    raw, public, private = Path(raw), Path(public), Path(private)
    (public / "train" / "images").mkdir(parents=True, exist_ok=True)
    (public / "test" / "images").mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    sdf_path = _find_sdf(raw)
    raw_mols = _load_molecules(sdf_path)
    mean_r2, mean_r1 = _build_hose_tables(raw_mols)

    mols = []
    for entry in raw_mols:
        pred = _predict_shifts(entry["mol"], mean_r2, mean_r1)
        if len(pred) < 2:
            continue
        mols.append({"smiles": entry["smiles"], "formula": entry["formula"],
                     "pred_shifts": pred, "pred_peakcount": _merged_peak_count(pred)})

    groups = {}
    for m in mols:
        groups.setdefault(m["formula"], []).append(m)
    usable = {f: g for f, g in groups.items() if len(g) >= K}

    formulas = sorted(usable.keys())
    rng_split = np.random.default_rng(SPLIT_SEED)
    rng_split.shuffle(formulas)
    n_test_groups = max(1, int(round(len(formulas) * TEST_GROUP_FRACTION)))
    test_formulas = set(formulas[:n_test_groups])
    train_formulas = set(formulas[n_test_groups:])

    train_targets = _build_split_rows(usable, train_formulas, N_TRAIN, SAMPLE_SEED)
    test_targets = _build_split_rows(usable, test_formulas, N_TEST, SAMPLE_SEED ^ 0x99)

    train_rows = _materialise(train_targets, usable, public / "train", True)
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
```

---

## 8) GPU Tier

**Select:** **A10G** — the workload is small: ~4,500 training rows, each a single grayscale stick-spectrum PNG plus five short SMILES strings. A solution that pairs a light image encoder (or a peak-picking front end) with cheminformatics candidate featurisation (RDKit / shift-prediction) trains in single-digit GPU-hours on a 24 GB A10G. H100-class compute is not required.

---

## 9) What Not To Use

* **External NMR-archive lookup** of recorded spectra for the candidate SMILES. The displayed spectrum is synthesised from structure via a deterministic shift relation and then perturbed (position jitter, peak dropout, inserted spurious peaks), so recorded experimental shifts in any external archive systematically disagree with the image. Lookup is both unreliable and disallowed.
* **Candidate-only heuristics** that ignore the spectrum (SMILES length, lexical order, or any property constant across the formula-matched candidates).
* **Ordering / metadata side-channels** — candidate order is shuffled with a uniform true index; `id` order and file metadata carry no signal.
* **Grader format hacks** — malformed probability rows or values engineered to exploit normalisation/clipping.
