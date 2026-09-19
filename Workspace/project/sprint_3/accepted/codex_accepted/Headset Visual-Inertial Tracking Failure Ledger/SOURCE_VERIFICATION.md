# Source Verification

## Source Gate

Source dataset: Monado SLAM Datasets by Collabora.

Dataset page:

```
https://huggingface.co/datasets/collabora/monado-slam-datasets
```

Collabora announcement:

```
https://www.collabora.com/news-and-blog/news-and-events/monado-slam-datasets-now-available.html
```

The Hugging Face dataset page lists the license as `cc-by-4.0`. The dataset card describes the corpus as challenging egocentric visual-inertial datasets recorded from VR headsets, with camera and IMU streams for devices including Valve Index and HP Reverb G2. The page also links individual sequence downloads and states that the permissive CC BY 4.0 license allows use with attribution.

License accepted for this build: CC BY 4.0, with attribution to Collabora and the Monado SLAM dataset.

## Selected Official Files

The full upstream repository is much larger than the upload budget, so this build uses five official short sequence archives. They are downloaded unchanged from Hugging Face.

| File | Bytes | SHA-256 |
|---|---:|---|
| `MIO09_short_1_updown.zip` | 99,569,080 | `14072018b9e424b06abfd1173169b24e53ad47632d3051e3164b27d322a0b898` |
| `MIO10_short_2_panorama.zip` | 214,797,238 | `9ca151d8dc5cb84dafecdb8595a22116e0f95162e8a1794eb2ca779bedfe60c4` |
| `MIO11_short_3_backandforth.zip` | 307,904,816 | `b36a2cb4019a15f25b4242743b8d025af7bbbe81deddc0222c85df535b17bb8b` |
| `MGO09_short_1_updown.zip` | 77,826,631 | `ae654052af4031ca905ec7cd390b3e618ff3377a265c247ca8b60123d725c6f2` |
| `MGO10_short_2_panorama.zip` | 292,156,870 | `acdbb7dc04b8f7047ce7de441d4e66fbea3bd21f52e0860f7400d47ac34c5d50` |

Total selected raw bytes: 992,254,635.

Direct download URLs:

```
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO09_short_1_updown.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO10_short_2_panorama.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO11_short_3_backandforth.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MG_reverb_g2/MGO_others/MGO09_short_1_updown.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MG_reverb_g2/MGO_others/MGO10_short_2_panorama.zip?download=true
```

## Import Or Upload Procedure

Preferred import procedure:

1. Import the five direct Hugging Face URLs above as official source files, if the platform supports URL import for multiple files.
2. Preserve the original filenames exactly.
3. Confirm the platform prepared dataset tree either retains those five ZIP files or extracts them to the five top-level sequence directories named `MIO09_short_1_updown`, `MIO10_short_2_panorama`, `MIO11_short_3_backandforth`, `MGO09_short_1_updown`, and `MGO10_short_2_panorama`.
4. Match `DATASET_FORM_FILL.md` to the validator-visible tree after extraction.
5. Run `prepare.py` with that raw directory.

Clean zip fallback used for this local package:

1. Place the five official ZIP files in `raw_sources/`.
2. Run `python zip_raw_for_upload.py --raw-dir raw_sources --output raw_upload.zip`.
3. Upload `raw_upload.zip` as the dataset source package.
4. The created `raw_upload.zip` contains the unchanged official raw members from the five upstream ZIPs, exposed as `<sequence>/mav0/...` folders at the archive root.
5. After platform extraction, the expected validator-visible tree is the five top-level sequence directories, not a wrapper directory.
6. It does not contain public splits, private answers, preprocessing outputs, caches, generated labels, or source code.

## Prepared Data Construction

All splitting and label construction happens in `prepare.py`.

The script reads each official archive, interpolates reference poses to camera keyframes, aggregates real IMU measurements, computes frame-change evidence from real camera frames, and renders compact transformed camera panels. The public degraded pose trace is deterministically derived from the real pose, camera, and IMU signals. The private ledger target is then derived by comparing the degraded trace against the reference trajectory and visual-inertial consistency signals.

Prepared public/private data size is about 16.8 MB in this local build, well below 500 MB.

## Split And Leakage Controls

- Train/test split is by whole recording: no source sequence appears in both splits.
- Public row IDs are salted SHA-256 identifiers and sorted by ID.
- Original sequence names, raw filenames, raw timestamps, ZIP paths, and source member paths are absent from `public/train.csv`, `public/test.csv`, and panel filenames.
- Public image panels are privacy-processed visual evidence derived from short real frame neighborhoods: temporal blending, cropping, mild geometric/photometric degradation, downsampling, noise, and JPEG re-encoding are applied so the panel remains useful for tracking audit while weakening source-file fingerprinting.
- Public panel files are padded to one fixed byte size so image file size is not a target shortcut.
- `private/source_map_audit_only.csv` is kept private and exists only to audit leakage.
- `_analyze.py` checks for raw source-name, timestamp, filename, and extension tokens in public CSV text.

Leakage probe result on the prepared split:

```
forbidden_public_tokens: false
panel_names_unique: true
train_test_ids_overlap: false
visual_exact_frame_top1: 0.0109
visual_exact_frame_top5: 0.0297
visual_queries: 640
crop_aware_window_top1: 0.0250
crop_aware_window_top5: 0.0750
crop_aware_window_rows: 120
crop_aware_sequence_top1: 0.6417
panel_file_sizes_unique: 1
panel_file_size_bytes: 18000
```

## Baseline And Headroom Checks

Scores on the prepared split:

| Baseline | Score |
|---|---:|
| Sample weak template | 0.134105 |
| Metadata/train-prior only | 0.144499 |
| Degraded-pose-only heuristic | 0.218540 |
| Simple CPU feature nearest-neighbor | 0.261687 |
| ID-hash-only nearest-neighbor | 0.281071 |
| File-size-only nearest-neighbor | 0.194225 |
| Path-hash-only nearest-neighbor | 0.275574 |
| Perfect labels | 1.000000 |

These results show the sample is non-degenerate but weak, metadata-only is weak, degraded-pose-only is not close to saturation, and a simple CPU feature baseline leaves substantial headroom.

## Novelty Gate

Nearest neighbors: Monado SLAM, EuRoC MAV, TUM VI, and other visual-inertial odometry benchmarks. Those benchmarks typically evaluate continuous trajectory estimation, localization accuracy, SLAM/odometry drift, or relocalization performance from camera and IMU streams.

This challenge uses the same general sensor domain but changes the ML object:

- Output is a discrete failure/repair ledger, not a continuous trajectory.
- The model audits a degraded partial trace instead of estimating absolute pose from scratch.
- The target combines trustworthy keyframe selection, failure span detection, repair anchor edges, dominant failure state, and uncertainty calibration.
- Scoring rewards structured consistency and weakest operational subgroups rather than pose RMSE or ATE/RPE.
- Public rows are anonymized and source-neutral; the task is operational AR/VR tracking triage.

Novelty judgment: 7/10. The source dataset is known, but the scored target, public input contract, and operational ledger metric are substantively different from canonical visual-inertial SLAM trajectory evaluation.

## CPU Feasibility

The prepared dataset has 328 training rows and 479 test rows with compact 320 x 240 JPEG panels plus small JSON traces. A solver can train and infer with CPU-only feature extractors, classical models, small neural networks, or constrained decoders inside 1.5 hours on 10 CPU cores and 62 GB RAM.
