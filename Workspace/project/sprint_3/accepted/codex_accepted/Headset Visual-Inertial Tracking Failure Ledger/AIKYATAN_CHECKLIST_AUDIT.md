# Aikyatan Checklist Audit

Target challenge:

`D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Headset Visual-Inertial Tracking Failure Ledger`

Checklist:

`D:\create_challenge_synthetic_output_folder\sprint_3\checklist_aikyatan.txt`

## Verdict

- SHIP for the applicable Aikyatan adversarial-validator gates.
- No BLOCKER findings.
- No MAJOR findings.
- Notes:
  - Some checklist items are for a different bundle format (`config.yaml`, `solution.ipynb`, `rubrics.md`, raw `dataset_description.md` / `problem_description.md`). This challenge uses the current local Eris challenge-builder format, so those items are N/A.
  - Gate R says "no markdown tables", but the live workspace rule and challenge-builder audit require compact markdown tables in `CHALLENGE_FORM_FILL.md`. Current local rules are stricter and newer for this workspace, so tables are treated as required, not a failure.

## Fingerprints

- `raw_upload.zip` SHA256: `B2A5258FEC1A7BA0F82D7EC9B03822F0FF433FF3AA423435C17326096B7E4708`
- `public/` tree SHA256: `ee75727382d9e35d4ed4e5b97bffcb320c4c5384d04c795bcb1475ebdd56d9c3`
- `private/` tree SHA256: `eaae359a32c2e4e62d9bae05c586afc6a2134071acc31d89f3be7d2de21e0919`
- `grade.py` SHA256: `061A7DCE299CE9CA23DF648FB1C297994AAD9F4797B9A1C631B9B595B5AE670D`
- `prepare.py` SHA256: `B37D66905DAFDA1CD9DFA249026B001F189340015A2907C5A42A790F2C29E36A`
- `PASTE_THIS_GRADE.txt` matches `grade.py`.
- `PASTE_THIS_PREPARE.txt` matches `prepare.py`.

## Score Ladder

- Perfect labels: `1.000000`.
- Perfect labels shuffled by row order: `1.000000`.
- Sample submission: `0.134105`.
- Metadata/train-prior baseline: `0.144499`.
- Degraded-pose-only heuristic: `0.218540`.
- Simple CPU feature nearest-neighbor: `0.261687`.
- ID-hash-only nearest-neighbor: `0.281071`.
- File-size-only nearest-neighbor: `0.194225`.
- Path-hash-only nearest-neighbor: `0.275574`.
- All malformed row-local JSON: `0.000000`.
- Duplicate structural submission: `0.000000`.

The weak and shortcut baselines are far below perfect, leaving more than 70 percentage points of absolute headroom from the strongest shortcut score to `1.0`.

## Gate Summary

- Gate A, Static Review: PASS.
  - Mandatory local artifacts are present.
  - `prepare(raw, public, private)` and `grade(submission, answers)` are importable.
  - Paste files match canonical scripts.
  - No rubric wording, no "What makes this challenging" section, and no editor artifacts.

- Gate B, Determinism Proofs: PASS.
  - Full `prepare.prepare(str(raw), str(public), str(private))` was run into a temp directory.
  - Output matched current `public/` and `private/` byte-for-byte.
  - Evidence: `public_hash_match True`, `private_hash_match True`, elapsed `121.0` seconds.

- Gate C, Leakage Audit: PASS.
  - Test target columns are absent from `public/test.csv`.
  - Train/test IDs have no overlap.
  - Public CSVs contain no raw source names, source paths, timestamps, or ZIP member paths.
  - Public panels are privacy-processed and fixed-size padded.
  - Source lookup probe: forbidden public tokens `false`, exact-frame top-1 `0.0109`, exact-frame top-5 `0.0297`, crop-aware exact-window top-1 `0.0250`, crop-aware exact-window top-5 `0.0750`.

- Gate D, Hardcoding And Exploit Red Team: PASS.
  - ID/path/file-size shortcut baselines remain weak.
  - Metadata/train-prior and degraded-pose-only baselines remain weak.
  - Public-to-original exact-window retrieval is low enough that source lookup is not a practical label recovery path.
  - What Not To Use explicitly bans source lookup, metadata-only answers, GPU/API use, runtime-downloaded model weights, hidden answers, and grader exploits.

- Gate E, Grader Strictness Battery: PASS under current challenge-builder rules.
  - Structural malformed submissions return scalar `0.0`, as required by the current local rules.
  - Row-local malformed JSON zeros the affected row without crashing.
  - Wrong/extra/reordered columns, missing rows, duplicate IDs, foreign IDs, NaN/inf/out-of-range/bool uncertainty all return `0.0`.
  - Perfect shuffled rows score exactly the same as unshuffled perfect rows.
  - Repeated calls are bit-identical for the same sample input.
  - Overlong JSON is capped before parsing and affects only the bad row.

- Gate F, Reference Solution Verification: N/A with notes.
  - No `solution.ipynb` is part of the local Eris challenge-builder deliverable.
  - CPU feasibility is supported by the documented intended approach and local CPU baselines in `_analyze.py`.

- Gate G, Documentation Reality Diff: PASS.
  - Challenge-builder audit reports all required problem-description tables and sections present.
  - Submission columns in the description match `sample_submission.csv`.
  - Train/test/answers row counts and ID sets match.
  - Dataset form remains a raw-source data dictionary and does not describe scoring or split mechanics.

- Gate H, Rubric Audit: N/A.
  - Current `rules/LATEST.md` says evaluation rubrics are removed and must not be included.

- Gate P, Platform Survivability: PASS.
  - `prepare.prepare(...)` accepts string paths.
  - Local raw ZIP is clean: no nested `raw_data/`, source/cache files, or private answers.
  - Prepared public/private size is about `16.8 MB`; raw upload ZIP is about `920.384 MB`.
  - Sample submission clears the platform floor with score `0.134105`.
  - No missing values in train/test/sample/answers.

- Gate N, Novelty And Domain Classification: PASS.
  - `SOURCE_VERIFICATION.md` documents nearest neighbors and a novelty score of `7/10`.
  - Challenge is framed and implemented as a structured AR/VR tracking-failure repair ledger, not plain SLAM regression, tabular regression, or single-label classification.
  - CPU-only constraints are visible in the problem description.

- Gate R, Render-Safety And Formatting: PASS under current local rules.
  - Live workspace rules require markdown tables for file overview, train columns, test columns, and submission format; these tables are present and compact.
  - No rubric section, no "What makes this challenging" section, no fenced table backup, no `undefined` artifacts.

## Evidence Commands

- `python _sanity_smoke.py`
  - `sample_score=0.134105`
  - `perfect_score=1.000000`
  - `malformed_row_score=0.133918`
  - `all_malformed_rows_score=0.000000`
  - `duplicate_structural_score=0.000000`
  - `sanity smoke PASS`

- `python _grader_exploit_tests.py`
  - Wrong schema, missing rows, duplicate IDs, NaN/inf/out-of-range/bool uncertainty all scored `0.000000`.
  - Shuffled row order scored `0.134105`.
  - Bad row-local JSON/type/range attacks scored row `0.000000`.
  - `grader exploit tests PASS`

- `python _analyze.py`
  - `sample: 0.134105`
  - `metadata_train_prior: 0.144499`
  - `degraded_pose_only: 0.218540`
  - `simple_cpu_feature_nn: 0.261687`
  - `id_hash_only: 0.281071`
  - `file_size_only: 0.194225`
  - `path_hash_only: 0.275574`
  - `perfect: 1.000000`
  - Visual exact-frame top-1 `0.0109`, top-5 `0.0297`.
  - Crop-aware exact-window top-1 `0.0250`, top-5 `0.0750`.

- Full string-argument prepare determinism check:
  - `string_args_prepare=PASS`
  - `public_hash_match True`
  - `private_hash_match True`

- Challenge-builder audit:
  - `SUMMARY failures=0 warnings=0`

## Residual Risks

- The checklist's reference-solution notebook gates cannot be certified because this challenge bundle does not include a `solution.ipynb`; this is normal for the local challenge-builder deliverable.
- The checklist's `config.yaml` coherence gate is not applicable because this bundle uses `CHALLENGE_FORM_FILL.md` grading-configuration fields rather than a separate `config.yaml`.
- Novelty is documented locally as `7/10`, but the platform's automated novelty score is ultimately external.
