# Dataset creation form — fill-in

**Platform status:** **Draft** — paired challenge *SliceShuffle: Cranio-Caudal Sequence Reconstruction*.

## Title

```
SliceShuffle IXI T1 Brain MRI NIfTI Corpus
```

## Description

## Overview

This dataset is an **unaltered mirror** of the IXI (Information eXtraction from Images) T1-weighted brain MRI archive from the Brain Development project at Imperial College London. It ships the upstream `*.nii.gz` NIfTI files byte-for-byte — no subsampling, no resizing, no intensity normalisation, no splitting, and no challenge-specific transforms are applied here. All of that processing happens downstream in the challenge's `prepare.py`, which reads the raw NIfTI files on the platform side and emits the challenge's `public/` + `private/` splits.

The IXI dataset contains ~580 healthy-volunteer brain MRI volumes acquired at three London hospital sites (Hammersmith Hospital on a Philips 3T, Guy's Hospital on a Philips 1.5T, and the Institute of Psychiatry on a GE 1.5T). Each file is a single T1-weighted 3D volume in compressed NIfTI format (`.nii.gz`).

## File Structure

The raw dataset is ~580 NIfTI files placed flat at the zip root:

```
SliceShuffle IXI T1 Brain MRI NIfTI Corpus/
├── IXI002-Guys-0828-T1.nii.gz
├── IXI012-HH-1211-T1.nii.gz
├── IXI013-HH-1212-T1.nii.gz
├── ...
└── IXI662-Guys-1120-T1.nii.gz
```

Each filename follows the upstream IXI naming convention: `IXI<subject_id>-<site>-<session>-T1.nii.gz`.

No `train.csv`, no `test.csv`, no labels, no per-image annotations, no scanner metadata CSVs, no patient demographics. The corpus is the pristine upstream NIfTI archive only.

## Features

Each `.nii.gz` file is a standard NIfTI-1 3D volume:

| Property   | Value                                    |
|------------|------------------------------------------|
| Modality   | T1-weighted structural MRI               |
| Format     | NIfTI-1 compressed (.nii.gz)             |
| Dimensions | 3D, varies per subject (typical ~256^3)  |
| Dtype      | float32 or int16 (per upstream scanner)  |
| Orientation| Varies; downstream reorients to RAS      |

## Notes

* The full IXI-T1 archive is ~5 GB on disk. Default settings in the downstream `prepare.py` cap processing at 600 subjects, which typically yields ~580 valid volumes after skipping subjects with insufficient axial brain coverage.
* Files are the upstream IXI T1 NIfTI archives byte-for-byte. No re-encoding, no re-compression, no metadata stripping.
* No patient-level identifiers beyond the upstream IXI subject / site / session string, no DICOM headers, and no demographics are included in this corpus; the upstream IXI authors already de-identified the source.

---

## License

**Creative Commons Attribution–ShareAlike 3.0 Unported (CC BY-SA 3.0)**, inherited from the upstream IXI dataset's licence terms ("This data is made available under the Creative Commons CC BY-SA 3.0 license"). Any derivative distribution of this corpus must credit the IXI / Brain Development project and be licensed under the same CC BY-SA 3.0 terms.

## Source

* Primary source: https://brain-development.org/ixi-dataset/
* Direct T1 archive: https://biomedic.doc.ic.ac.uk/brain-development/downloads/IXI/IXI-T1.tar
* Project: Information eXtraction from Images (IXI), Brain Development project, Imperial College London. ~580 healthy-volunteer T1 / T2 / PD / MRA / DTI brain MRI volumes, multi-site.
* Subset used: T1-weighted volumes only.
* Reproducibility: the dataset is the upstream archive byte-for-byte; no processing is applied at this stage.
