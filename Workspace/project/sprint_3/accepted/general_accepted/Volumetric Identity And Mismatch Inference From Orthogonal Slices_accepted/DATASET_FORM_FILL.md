# Dataset creation form — fill-in

**Platform status:** **Draft**

## Title

```
MedMNIST 3D Six Volumetric Sub-Corpora at 28x28x28 Resolution
```

## Description

## Overview

This dataset is an **unaltered mirror** of six volumetric sub-corpora from the MedMNIST v2 release (`randall-lab/medmnist` on Hugging Face). Each sub-corpus is a `.npz` archive that ships a fixed train / validation / test split of low-resolution 3D medical volumes at 28×28×28 `uint8` resolution. The six included corpora are: OrganMNIST3D, NoduleMNIST3D, AdrenalMNIST3D, FractureMNIST3D, VesselMNIST3D, SynapseMNIST3D — covering abdominal CT, chest CT, adrenal CT, vertebra CT, brain MRA, and electron-microscopy synapse volumes respectively.

The corpus is intentionally tiny per file: each volume is a single `28 × 28 × 28` array of unsigned bytes (≈ 21.5 KB raw), wrapped in a NumPy zip archive with the corresponding integer labels.

## File Structure

```
organmnist3d.npz       # ~32 MB
nodulemnist3d.npz      # ~28 MB
adrenalmnist3d.npz     # ~270 KB
fracturemnist3d.npz    # ~3.1 MB
vesselmnist3d.npz      # ~390 KB
synapsemnist3d.npz     # ~36 MB
```

Six files, all sitting at the dataset root.

## Features

Per `.npz` archive:

| Key            | Type                | Description                              |
|----------------|---------------------|------------------------------------------|
| train_images   | uint8 (N,28,28,28)  | 3D volumes, training split               |
| train_labels   | uint8 (N,1)         | Per-volume integer labels                |
| val_images     | uint8 (N,28,28,28)  | Validation split volumes                 |
| val_labels     | uint8 (N,1)         | Validation split integer labels          |
| test_images    | uint8 (N,28,28,28)  | Test split volumes                       |
| test_labels    | uint8 (N,1)         | Test split integer labels                |

Per-corpus class cardinality:

| Corpus            | Modality                | Classes |
|-------------------|-------------------------|---------|
| OrganMNIST3D      | abdominal CT            | 11      |
| NoduleMNIST3D     | chest CT (lung nodule)  | 2       |
| AdrenalMNIST3D    | adrenal CT              | 2       |
| FractureMNIST3D   | chest CT (vertebra)     | 3       |
| VesselMNIST3D     | brain MRA               | 2       |
| SynapseMNIST3D    | electron microscopy     | 2       |

Per-volume properties:

| Property        | Value                                   |
|-----------------|-----------------------------------------|
| Volume shape    | 28 × 28 × 28                            |
| Voxel dtype     | uint8                                   |
| Modality        | varies per corpus (CT / MRA / EM)       |
| Spatial axes    | (depth, height, width) = (z, y, x)      |

## Notes

* Each `.npz` is a NumPy zip-archive carrying the train / validation / test splits as published by the upstream MedMNIST v2 maintainers; the archives are **unmodified**.
* All six corpora are at the standard 28-cube resolution. The MedMNIST v2 release also publishes 64-cube versions of each corpus; those are **not** included here.
* Class cardinality varies per corpus. Volume counts vary per corpus; see the upstream release for exact counts.
* The volumes are de-identified upstream — no patient identifiers, no acquisition timestamps, no file-system paths.

---

## License

**Creative Commons CC-BY 4.0**, inherited from the upstream MedMNIST v2 release. Each individual sub-corpus carries its own upstream attribution chain (LIDC, Camelyon-derived, etc.) — see the MedMNIST v2 paper and source-data table for full attribution. The Hugging Face mirror `randall-lab/medmnist` re-publishes the same files under the same CC-BY 4.0 license. **DermaMNIST is NOT included** in this archive (it carries a CC-BY-NC 4.0 restriction at the upstream source).

## Source

* Hugging Face mirror used: https://huggingface.co/datasets/randall-lab/medmnist
* Primary paper: Yang J., Shi R., Wei D., Liu Z., Zhao L., Ke B., Pfister H., Ni B. "MedMNIST v2 — A Large-Scale Lightweight Benchmark for 2D and 3D Biomedical Image Classification." Scientific Data, 2023. DOI: 10.1038/s41597-022-01721-8.
* Upstream project page: https://medmnist.com
* Sub-corpus upstream attributions: OrganMNIST3D / NoduleMNIST3D / AdrenalMNIST3D / FractureMNIST3D / VesselMNIST3D / SynapseMNIST3D — see the MedMNIST v2 paper Table 1.
