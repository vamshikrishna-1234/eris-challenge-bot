# Source Verification

Checked on 2026-07-19 IST against the official Zenodo page, Zenodo API record, associated PNAS Nexus article, local sprint challenge folders, and current challenge-builder rules.

## Gate Decision

PASS. This is a real-data, CPU-compatible challenge using official honey-bee observation-hive trajectory and dance-interaction files. The selected source package consists only of official CSV files and unchanged date-level track CSV members extracted from the official `Berlin2019_tracks.zip` archive. It does not contain prepared train/test splits or processed features.

## Official Source

Primary source page: `https://zenodo.org/records/7928121`

Official API record: `https://zenodo.org/api/records/7928121`

DOI: `10.5281/zenodo.7928121`

Record title: `Data used in Machine learning reveals the waggle drift's role in the honey bee dance communication system`

Creators listed by Zenodo: David M. Dormagen, Benjamin Wild, Fernando Wario, and Tim Landgraf.

Associated paper: `https://academic.oup.com/pnasnexus/article/2/9/pgad275/7251052`

Verified source facts:

* The Zenodo record is a `Dataset`, published 2023-05-17, version `1.0`.
* Zenodo API metadata reports license id `cc-by-4.0`.
* The Zenodo page rights section displays `Creative Commons Attribution 4.0 International`.
* The official description says `Berlin2019_waggle_phases.csv` contains automatic individual detections of waggle phases.
* The official description says `Berlin2019_dances.csv` contains automatic dance detections with `dancer_id`, `dance_id`, start/end times, camera side, median position, and feeder camera id.
* The official description says `Berlin2019_followers.csv` contains attendance and following behavior corresponding to dances, with `attendance` or `follower` labels.
* The official description says `Berlin2019_dances_with_manually_verified_times.csv` contains a sample of dances with manually verified start/end times.
* The official description says `Berlin2019_dance_classifier_labels.csv` contains manually annotated per-frame labels `nothing`, `waggle`, and `follower`.
* The official description says `Berlin2019_tracks.zip` contains detections and tracks grouped by date, with camera side, timestamp, frame id, track id, bee id, bee-id confidence, hive-plane position, and orientation.

## License And Redistribution

License: Creative Commons Attribution 4.0 International (`CC BY 4.0`).

CC BY 4.0 permits copying, redistribution, adaptation, and commercial use if attribution is provided, license information is preserved, and changes are indicated. This is compatible with a challenge dataset built from official source files and derived public episode files, as long as attribution is retained.

Recommended attribution:

```text
Dormagen, David M.; Wild, Benjamin; Wario, Fernando; Landgraf, Tim. "Data used in Machine learning reveals the waggle drift's role in the honey bee dance communication system." Zenodo, 2023. DOI: 10.5281/zenodo.7928121. License: Creative Commons Attribution 4.0 International.
```

## Official File Inventory

Zenodo API file metadata checked live:

| File | Size bytes | Official checksum |
|---|---:|---|
| `Berlin2019_dances.csv` | 211,675 | `md5:05dc2b731223acbd1e47213f9a86e1bc` |
| `Berlin2019_dances_with_manually_verified_times.csv` | 4,895 | `md5:7654b05690ee7c35e022ac0101d04f31` |
| `Berlin2019_feeder_experiment_log.csv` | 3,662 | `md5:1c7945b25bf9b2629088b34d0b398664` |
| `Berlin2019_dance_classifier_unlabeled.csv` | 16,915,574 | `md5:2eecc08822294fb8dc0c656988828c3d` |
| `Berlin2019_dance_classifier_labels.csv` | 202,752,865 | `md5:b86ad76e33556af3b91c69cb15f9ad2d` |
| `Berlin2019_followers.csv` | 9,171,824 | `md5:7913056e00a7d21fcef4f9dd7b876bc3` |
| `Berlin2019_tracks.zip` | 1,397,504,889 | `md5:bec5868c4f1bb4b630841cee762827a6` |
| `Berlin2021_waggle_phase_classifier_labels.csv` | 95,903 | `md5:046fa364cd9b1097c24a62e4c1454dd9` |
| `Berlin2021_waggle_phase_classifier_ground_truth.zip` | 3,205,685,969 | `md5:7c8868e49939c1a7d699050043eaab1d` |
| `Berlin2021_waggle_phases.csv` | 22,808,314 | `md5:00e013832aec73c16f85d0b4bd474e38` |
| `Berlin2019_waggle_phases.csv` | 15,202,608 | `md5:90a83db020c64e1a84ce46d1ca38b5af` |

## Track Archive Inspection

The official `Berlin2019_tracks.zip` was inspected by HTTP range reads of the ZIP end-of-central-directory and central directory, without downloading the whole archive.

Result: PASS. The archive contains a top-level `Berlin2019_tracks/` directory and 48 date-level CSV members from `2019-08-01.csv` through `2019-09-23.csv` where available. Members are regular deflated CSV files. This satisfies the user requirement that clean raw subsetting is allowed only if the archive members are date-level CSVs.

Selected unchanged date-level track members:

| Member | Uncompressed bytes | Official compressed bytes |
|---|---:|---:|
| `Berlin2019_tracks/2019-08-25.csv` | 269,169,413 | 72,159,340 |
| `Berlin2019_tracks/2019-08-27.csv` | 245,301,592 | 65,887,764 |
| `Berlin2019_tracks/2019-08-28.csv` | 270,060,894 | 73,565,118 |
| `Berlin2019_tracks/2019-08-29.csv` | 276,351,880 | 74,798,318 |
| `Berlin2019_tracks/2019-09-02.csv` | 441,288,752 | 119,376,567 |
| `Berlin2019_tracks/2019-09-05.csv` | 588,314,312 | 159,951,684 |
| `Berlin2019_tracks/2019-09-10.csv` | 116,224,903 | 31,519,864 |
| `Berlin2019_tracks/2019-09-11.csv` | 349,566,169 | 94,614,230 |

The selected track members total about 691.9 MB in the official ZIP's compressed representation. The included official CSV files listed in `DATASET_FORM_FILL.md` total about 227.3 MB before compression. The clean package therefore has a conservative source-size budget of about 919.2 MB before recompression benefits from the standalone CSV files. `build_source_subset_zip.py` writes a deflated clean package and reports the actual ZIP size.

## Source Upload Decision

Current local platform notes say URL import supports HTTP/HTTPS source files up to 100 GB. Therefore direct URL import can technically ingest the official `Berlin2019_tracks.zip`. However, importing the full track ZIP plus the required official CSVs would exceed the user's around-1 GB source budget and would include many dates not needed for this challenge.

Recommended upload: run `build_source_subset_zip.py` and upload the resulting clean `waggle_dance_raw_subset.zip`. The ZIP contains official CSVs, unchanged extracted date-level track CSV members, attribution/license files, source manifest, checksums, and extraction notes. It does not contain train/test splits, public/private prepared files, generated features, answers, caches, or challenge scripts.

Built package in this folder:

* Filename: `waggle_dance_raw_subset.zip`
* Size: 738,696,915 bytes, about 738.7 MB decimal.
* SHA-256: `39D881C8BBCD2B8558539D31A604F8541125A83933CAA6CF42B94F36F07A1C30`

Fallback if a reviewer explicitly prefers official URL imports despite the size: import the official file URLs listed in `URL_IMPORT_LIST.txt`, including the full `Berlin2019_tracks.zip`, then run `prepare.py`. This fallback is not the recommended path because it violates the requested approximately 1 GB source budget.

## Novelty Gate

Nearest neighbor: the source paper's own automatic dance and dance-following pipeline. The associated paper describes a model that classifies trajectory windows into other, dancing, and following classes, then postprocesses dance events by querying nearby bees to assign attendee/follower state and dancer-follower mappings.

Shared elements:

* Same official honey-bee observation-hive source.
* Same real tracked bee trajectories.
* Same source-supported dance, waggle, attendance, and follower signals.
* Same biological domain of dance-following behavior.

Material differences:

* The challenge input is a short local episode with many anonymized bees, not an original raw bee/time/frame lookup table.
* The target is an episode-level communication record: dancer ID, ordered waggle intervals, follower-vs-attendee roles, directed dancer-to-follower graph edges, and confidence.
* Public rows strip dates, timestamps, raw bee IDs, track IDs, frame IDs, dance IDs, feeder IDs, source filenames, source row order, and absolute coordinates.
* Local bee IDs are remapped independently per episode, and coordinates/orientations are transformed with deterministic label-preserving privacy transforms.
* The metric rewards temporal segmentation, participant identification, edge recovery, role distinction, graph consistency, confidence calibration, and worst-group robustness.
* A same-input per-frame `waggle/follower/other` behavior detector is insufficient and is prohibited in the visible instructions.

Novelty judgment: PASS, estimated novelty score 6.5/10. The same public source caps novelty somewhat, but the actual participant contract is not the source dataset's canonical per-frame behavior labeling or the paper's exact trajectory classifier. It is a source-redacted, local-ID, episode-level communication graph recovery task with multi-part structured outputs and graph consistency.

## Local Duplicate Check

Checked local sprint neighbor:

`D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Beehive Swarm Risk And Queen-State Triage From Hive Audio`

Difference: that neighbor uses real hive audio and asks for queen-state/activity/noise triage labels. This challenge uses real visual trajectory tracks and asks for temporal event segmentation plus participant/graph recovery. It is not a hive-audio state triage challenge, does not use audio clips, and has a different source, modality, schema, and evaluation object.

## Leakage Controls

`prepare.py` removes or transforms source-reversible fields from public prepared data:

* No raw dates, timestamps, original bee IDs, frame IDs, track IDs, dance IDs, feeder IDs, source filenames, or raw row indices appear in public CSVs.
* Public IDs are salted SHA-256 derived from episode fingerprints and sorted lexicographically.
* Local bee IDs are assigned per episode after a deterministic shuffle.
* Episode times are relative seconds in a public episode clock, with deterministic label-preserving nonlinear time warping, per-bee timing offsets, jitter, and detection thinning.
* Coordinates are centered, transformed, nonrigidly distorted, perturbed with per-bee displacement and tracking noise, rounded, and stored as privacy-protected relative hive-plane coordinates.
* Public NPZ arrays contain only numeric arrays with local indices.
* Train/test split is by recording date and then drops raw dancer identities that would otherwise cross split.
* Hidden subgroup axes are semantic/physical: crowding, tracking confidence, duration, waggle count, comb side, and session bucket.

The cross-challenge CREMA-D lookup lesson was applied by running a trajectory-fingerprint probe against official raw candidate windows. Before this extra hardening, a rotation/translation-invariant temporal-geometry fingerprint recovered `40/40` checked public test episodes at rank 1. After stronger time-warp, missingness, and nonrigid geometry transforms, the same checked probe recovered `1/40` at rank 1 and `6/40` at rank 5, with median rank `65.5` among 342 raw candidates. See `TRAJECTORY_SOURCE_LOOKUP_AUDIT.md`.

Residual risk: because the upstream raw trajectory source is public, a determined external-source lookup attack can never be reduced to zero. This build uses source-redaction and label-preserving coordinate/time transforms, and the visible challenge prohibits source lookup and runtime internet use. `_analyze.py` performs public-file source-token scans, NPZ schema scans, train/test feature-overlap checks, metadata, file-size, and spam-template shortcut baselines, strict submission probes, and a sampled raw-coordinate overlap probe when the official raw subset is present.

## CPU Feasibility

The intended route is CPU trajectory modeling, not GPU training. The prepared arrays are compact compressed NPZ files, and solver-visible data are small enough for feature extraction, sequence models, and graph decoding within 1.5 hours on 10 CPU cores and 62 GB RAM.
