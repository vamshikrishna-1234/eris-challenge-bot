# Handoff: Lightning Flash Hierarchy Induction

## Files created

- Core: `prepare.py`, `grade.py`, `PASTE_THIS_PREPARE.txt`, `PASTE_THIS_GRADE.txt`.
- Forms: `CHALLENGE_FORM_FILL.md`, `DATASET_FORM_FILL.md`.
- Verification: `SOURCE_VERIFICATION.md`, `URL_IMPORT_LIST.txt`, `UPLOAD_INSTRUCTIONS.md`, `AUDIT_NOTES.md`.
- Testing/analysis: `_sanity_smoke.py`, `_analyze.py`, `_grade_exploit_audit.py`, `SMOKE_RESULTS.json`, `ANALYSIS_RESULTS.json`, `GRADE_EXPLOIT_RESULTS.json`, `BUILD_NOTES.md`.
- Environment: `requirements.txt`.
- Materialized data: `public/train.csv`, `public/test.csv`, `public/sample_submission.csv`, `private/answers.csv`.
- Reproducibility inputs: five untouched official `.nc` files in `raw_data/`.

No `generate.py` was created because the task uses real official data. Direct URL import remains the preferred source route. At the user's request, a clean convenience ZIP named `glm_official_raw_untouched_with_attribution_20260716_210000.zip` is also included; it contains only the five untouched official `.nc` files plus `NOAA_ATTRIBUTION.txt`, with no prepared or preprocessed data.

## Source and license

Source/license gate: **PASS**, with one documented metadata caveat.

The five files are official NOAA GOES-16 GLM Level-2 Lightning Detections (`GLM-L2-LCFA`) objects delivered anonymously through NOAA NODD. Total raw size: 2,901,827 bytes. Their hashes, dimensions, variables, calibration-revision evidence, and exact URLs are in `SOURCE_VERIFICATION.md` and `URL_IMPORT_LIST.txt`.

NOAA/NCEI policy places NOAA-produced environmental data in the U.S. public domain, and the NODD GOES license says the data may be used as desired, with attribution requested and no implied endorsement. The embedded operational NetCDF `license` attribute says access is restricted; this conflicts with current official public dissemination and is treated as a stale template attribute. If a platform reviewer refuses that interpretation, obtain written NODD clarification before publication and do not substitute data.

## Import procedure

Direct URL import is the selected method. Add all five lines of `URL_IMPORT_LIST.txt` as URL sources, do not rename them, and run `prepare.py`. It accepts flat or nested platform raw layouts and validates exact sizes/hashes.

Fallback/direct-upload option: upload `glm_official_raw_untouched_with_attribution_20260716_210000.zip`, or download all five URLs byte-for-byte, verify the documented hashes, and upload those untouched files with an attribution note. Do not preprocess, subset, rename, or convert them. No preprocessed raw ZIP may be used.

## Prepared data

- Train: 210 cases from three whole source windows.
- Test: 140 cases from two different whole source windows.
- Prepared public size: 1,263,818 bytes (1.2053 MiB).
- Prepared total: 1,382,800 bytes (1.3187 MiB), including private answers.
- Raw and prepared combined remain far below all size gates.
- Every private source, density, and ambiguity subgroup has at least 30 cases.

## Scores and attacks

| Probe | Held-out score |
|---|---:|
| Perfect/native oracle, sanity only | 1.000000 |
| Weak sample submission | 0.175460 |
| Metadata only | 0.146721 |
| Lexical/schema only | 0.146721 |
| JSON-length/point-count | 0.141396 |
| Opaque-id order | 0.140743 |
| Opaque-id hash | 0.157251 |
| Fixed operational-threshold surrogate | 0.206663 |
| Train-tuned DBSCAN | 0.224933 |
| Small CPU pairwise model | 0.340643 |

The strongest shortcut leaves 0.775067 headroom to perfect, above the 0.30 gate. DBSCAN group-pair F1 is 0.109566 after count consistency, uncertainty F1 is 0.219144, and exact-row rate is zero. The learned model reaches group-pair F1 0.272414, uncertainty F1 0.357721, and flash-pair F1 0.993948.

Leakage checks found no filename/source/native-id/coordinate-schema tokens, no duplicate feature vectors, and low order/hash/length attack scores. Aggregate public-feature source-window classification was 0.45 versus 0.50 chance; metadata-only source-window classification was 0.571429.

## CPU runtime and memory

- Prepare: 1.1687 and 1.2163 seconds on two deterministic runs.
- Grade: 0.02074 seconds per complete 140-row submission averaged over 20 runs.
- Fixed plus train-tuned DBSCAN grid/test: 42.467 seconds.
- Small pairwise-model fit, threshold tuning, and test inference: 23.335 seconds on 25,327 training pairs.
- Full attack/model analysis: 66.081 seconds, peak process working set 187.891 MiB.
- End-to-end smoke process (two prepares plus grading/malformed tests): peak 226.922 MiB.

All paths are CPU-only and comfortably below the 1.5-hour, 10-core, 62-GB platform limit.

## Verification status

- `_sanity_smoke.py`: PASS.
- Perfect score: exactly 1.0.
- Weak sample: valid and 0.175460.
- Deterministic preparation/raw immutability: PASS.
- Missing/extra/reordered columns, id mismatch/duplicates, invalid confidence: rejected.
- Malformed/oversized/invalid structured JSON: affected row zero, no global crash.
- Label alias invariance: PASS.
- `_analyze.py` leakage/difficulty gates: PASS.
- `_grade_exploit_audit.py` degenerate-grader exploit gate: PASS.
- Challenge audit: 0 failures, 13 explained manual/intentional warnings.

## Solver-agent status

No solver-agent run was performed. The only solver-like run was the transparent compact CPU baseline in `_analyze.py`.

## Remaining risks and required procedures

1. Keep `prepare.py`, raw source objects, source manifest, and `private/answers.csv` platform-private. Publishing the exact deterministic preparation implementation alongside raw objects would allow full regeneration.
2. Review the NetCDF license-attribute conflict before publication; use the official NODD/NCEI policy evidence and seek written clarification if the platform requires it.
3. The prototype uses five short source windows and every case contains two native flashes; the coarse flash head is easier than the group/uncertainty heads. Do not claim universal scientific generalization.
4. Ensure the preparation environment has either `netCDF4` or `h5py`; `prepare.py` supports both readers for the official NetCDF4/HDF5 files. Grading itself uses only pandas/NumPy.
5. Use direct URL import first when possible. If uploading a file package directly, use only `glm_official_raw_untouched_with_attribution_20260716_210000.zip` or an equivalent flat ZIP of the same five untouched official files plus attribution note; never upload a preprocessed raw package.
6. Keep the participant-visible description free of exact raw URLs, filenames, timestamps, coordinates, native ids, and internal source procedures.
