# Dataset creation form — fill-in

**Platform status:** **Draft** — paired challenge *Annotator Reliability And Adversarial Rater Detection*.

## Title

```
PatchCamelyon H And E Histology Patches With Binary Metastasis Labels
```

## Description

## Overview

This dataset is an **unaltered mirror** of the upstream PatchCamelyon (PCam) histopathology corpus published as `1aurent/PatchCamelyon` on Hugging Face. PatchCamelyon is a binary classification benchmark of 96×96 RGB H&E (Hematoxylin & Eosin) tissue patches drawn from the Camelyon16 lymph node WSIs; each patch carries a binary label of `True` (positive — metastatic tissue in the central 32×32 region) or `False` (negative — no metastasis in the central 32×32 region).

The corpus is shipped as Parquet files: each row is a single patch (96×96 RGB, PNG-encoded inside the Parquet `image` column) plus its boolean label. There are three logical splits in the upstream release: `train`, `valid`, `test`. No additional annotations, no patient identifiers, no acquisition timestamps.

## File Structure

```
data/
├── train-00000-of-00013-*.parquet
├── train-00001-of-00013-*.parquet
├── ...
├── train-00012-of-00013-*.parquet     (13 train shards)
├── valid-00000-of-00002-*.parquet
├── valid-00001-of-00002-*.parquet     (2 valid shards)
├── test-00000-of-00002-*.parquet
└── test-00001-of-00002-*.parquet      (2 test shards)
```

The 13 `train-*.parquet` shards together contain ~262K patches. The 2 `valid-*.parquet` shards contain ~32K patches. The 2 `test-*.parquet` shards contain ~32K patches. The full corpus is **327,680 patches** at ~3.5 GB total when loaded as Parquet.

## Features

Per Parquet row:

| Column | Type   | Description                              |
|--------|--------|------------------------------------------|
| image  | dict   | `{"bytes": <PNG>, "path": null}` 96x96   |
| label  | bool   | True = metastasis present in centre 32   |

Per decoded image:

| Property        | Value                                   |
|-----------------|-----------------------------------------|
| Format          | PNG (RGB, 3 channels) inside Parquet    |
| Modality        | H&E histology patch                     |
| Dimensions      | 96 × 96 px                              |
| Color           | RGB, 8-bit per channel                  |

## Notes

* The full upstream release is **327,680 patches** at ~3.5 GB. Only a small, balanced subsample is ever materialised by downstream consumers; the raw upload here is the upstream Parquet shards unmodified.
* PatchCamelyon labels are derived from the Camelyon16 ground-truth pixel masks; a patch is positive iff the centre 32×32 region overlaps the metastasis annotation. Surrounding context outside the centre 32×32 may contain tumour or normal tissue regardless of the label.
* The dataset is fully de-identified upstream — no patient IDs, no slide IDs, no scanner-ID metadata, no acquisition timestamps in the Parquet rows.

---

## License

**Creative Commons CC0 1.0 Universal** (Public Domain Dedication), inherited from the upstream PatchCamelyon release at `github.com/basveeling/pcam`. The Hugging Face mirror `1aurent/PatchCamelyon` re-publishes the same files under the same CC0 1.0 license. No attribution is legally required, but academic credit to the original authors is customary.

## Source

* Primary source: https://github.com/basveeling/pcam
* Hugging Face mirror used: https://huggingface.co/datasets/1aurent/PatchCamelyon
* Upstream paper: Veeling B. S., Linmans J., Winkens J., Cohen T., Welling M. "Rotation Equivariant CNNs for Digital Pathology." MICCAI 2018. arXiv:1806.03962.
* Underlying corpus: Camelyon16 challenge (Bejnordi et al., JAMA 2017) — H&E whole-slide images from sentinel lymph node biopsies.
* Reproducibility: the dataset is the upstream Parquet shards unmodified; no processing is applied at this stage.
