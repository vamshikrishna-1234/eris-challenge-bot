# Handoff and upload instructions

## Preferred source procedure

The official merged Zenodo URL is directly downloadable, but importing it directly would pull `16,232,481,989` bytes and violate the requested approximately 1 GB raw-data budget. Zenodo does not expose the expert folder as a separate URL-import object.

Use the clean official-file upload procedure instead:

```powershell
python generate.py --output raw_data --workers 6
python generate.py --output raw_data --verify-only
python zip_raw_for_upload.py --raw raw_data --output ai4mars_official_expert_subset.zip
```

Upload `ai4mars_official_expert_subset.zip` as the dataset source file. It contains the original `ai4mars-dataset-merged-0.6/...` tree and only byte-identical official files. Do not upload `public/`, `private/`, prepared CSVs, challenge scripts, caches, or a resized/prepared corpus as raw data.

The final ZIP is `168,531,276` bytes with SHA-256 `ACDA3BD5BAE6475E0CC9EB534316C1BC0C37F29D693F715888B708D8ACC43565`.

On Windows, the requested challenge path plus the unchanged official mask hierarchy can exceed the legacy 260-character path limit. Run acquisition through a short junction/staging path or enable long-path support. `generate.py` also applies the Windows extended-path prefix internally.

## Platform fields

* Dataset description: paste `DATASET_FORM_FILL.md`.
* Challenge form: paste the sections from `CHALLENGE_FORM_FILL.md`.
* Prepare script: paste `PASTE_THIS_PREPARE.txt`.
* Grading script: paste `PASTE_THIS_GRADE.txt`.
* Grading direction: maximize.
* Theoretical minimum: `0.0`.
* Theoretical maximum: `1.0`.
* Compute: CPU only, 10 CPU cores, 62 GB RAM, 1.5 hours maximum.

## Verified local results

* Prepared rows: 262 train, 173 test; all source sequence families are split-disjoint.
* Grader: perfect `1.000000`; sample constant template `0.269134`; malformed row-local JSON or invalid route labels zero the affected row without crashing; wrong columns, duplicate/missing IDs, non-finite values, and out-of-range values raise `InvalidSubmissionError`.
* Baselines and shortcut probes: metadata-only `0.233829`; simple CPU thumbnail k-NN `0.297441`; ID-prefix-only `0.235963`; file-size-only k-NN `0.267193`.
* Source/hash probes: public/raw exact image SHA-256 hits `0`; test rows uniquely recoverable by raw file size `0`; whole-image source thumbnail rank-1 `0.005780`, rank-5 `0.017341`, median rank `199`; stronger multicrop source probe rank-1 `0.052023`, rank-5 `0.080925`, rank-10 `0.161850`, median rank `111` over 526 official candidates.
* Source verification: 1,059 files, 169,450,173 official bytes, every member CRC-verified twice.

## Attribution text

AI4Mars version 0.6, created/curated by Robert Swan, Masahiro Ono, Deegan Atha and collaborators at NASA Jet Propulsion Laboratory; official record https://doi.org/10.5281/zenodo.15995036; licensed CC BY 4.0. Cite the related AI4Mars paper as requested by the source record.
