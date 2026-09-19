# Checkpoint And Previous-Review Audit

This audit was run against:

```
C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints
C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt
```

Target challenge:

```
D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Headset Visual-Inertial Tracking Failure Ledger
```

## Caspian Checklist

| Item | Status | Evidence |
|---|---|---|
| Source and licensing: source/license matches the claim and strictly allows commercial challenge use, reuse, and redistribution. | [p] | Hugging Face lists `cc-by-4.0`; Collabora says CC-BY 4.0 allows commercial use with attribution. Exact source URLs, sizes, and hashes are in `SOURCE_VERIFICATION.md`. |
| Raw assets only: uploaded files must be raw data, generator scripts, or source assets, not pre-baked train/test splits. | [p] | `raw_upload.zip` has 4,513 official raw sequence members, includes CSV/PNG raw data, and contains no `public/`, `private/`, answers, source/cache files, or generated labels. |
| Speech/text domain fit: for speech AI or code-switching/text data, annotations and labels must be clean and meaningful. | [n/a] | This is a visual-inertial headset tracking challenge, not speech/text. |
| Synthetic sanity check: if synthetic data is used, the generation script must be provided and model a plausible process. | [n/a] | This is real data. `generate.py` is only a bounded official-source acquisition helper. |
| Real-world ML value: problem tests actual modeling/generalization, not a contrived challenge. | [p] | The task is an operational AR/VR tracking audit: use real camera panels, IMU traces, and degraded pose to repair a failure ledger. |
| Fair split and OOD testing: splits test realistic generalization without impossible guessing. | [p] | Train/test are disjoint by whole source recording; test shares headset/motion domain structure but uses held-out recordings. |
| Metric and headroom: metric fits the domain and baseline leaves at least about 30% improvement headroom. | [p] | Sample 0.134105, metadata/train-prior 0.144499, degraded-pose-only 0.218540, simple CPU NN 0.261687, perfect 1.0. |
| Input validation: grader actively rejects malformed submissions. | [p] | Wrong/missing/reordered columns, missing rows, duplicate IDs, NaN/inf/out-of-range uncertainty all return 0.0; row-local malformed/overlong JSON zeros the affected row. |
| No internal leaks: grader errors must never leak private labels, answer keys, split logic, or internal scoring weights. | [p] | `grade()` returns scalar `0.0` on invalid inputs; bogus CLI path prints `0.0` without traceback. |
| Agent-code safeguards: no sketchy fallback mechanisms such as `models=[]` designed to bypass hidden fluctuations. | [p] | No solver pipeline is included; repository grep found no `models=[]` or suspicious fallback solver code. The visible prompt bans GPU/API/source lookup/hidden-answer/metadata-only approaches. |
| Feature isolation: public features must not reveal targets through metadata, IDs, row order, file lengths, or hidden artifacts. | [p] | Public rows omit source names/timestamps/raw paths; IDs and panel names are salted opaque strings; train/test IDs do not overlap; source-token probe is clean. |
| No rule leaks: prompts/data must not expose answer logic, generator rules, or hidden scoring tricks. | [p] | Participant-facing form defines only public evidence and output schema. It does not disclose deterministic degradation constants, raw source identifiers, or split construction internals. |
| Anti-regex/anti-lookup: task cannot be solved by regex, lookup tables, metadata matching, or template inversion. | [p] | Metadata/train-prior and degraded-pose-only baselines are weak; ID/file-size/path-only baselines stay below 0.29; visual exact-frame retrieval is top-1 0.0109 and top-5 0.0297 over 640 tile queries; crop-aware exact-window retrieval is top-1 0.0250 and top-5 0.0750 over 120 rows. Source lookup is explicitly banned. |

## Shortcut And Exploit Audit

| Surface | Status | Evidence |
|---|---|---|
| ID exploit / submission IDs | PASS | Public IDs are opaque salted strings and do not overlap across train/test. ID-hash-only nearest-neighbor score is 0.281071 after metric hardening, leaving large headroom. |
| Reverse-engineering public IDs | PASS | Public CSVs do not expose raw sequence names, raw start indices, source paths, or raw timestamps. The challenge-visible form is source-neutral and bans reverse mapping. |
| Hashing shortcut | PASS | Hash/path-only copy baselines are weak: ID-hash-only 0.281071 and path-hash-only 0.275574. |
| Public file sizes | PASS | All 807 public panel files are padded to exactly 18,000 bytes. File-size-only nearest-neighbor score is 0.194225. |
| Lookup with original source | PASS | `_analyze.py` probes official raw frames: exact-frame top-1 0.0109 and top-5 0.0297 over 640 tile queries; crop-aware exact-window top-1 0.0250 and top-5 0.0750 over 120 rows. |
| Public-to-original 1:1 mapping | PASS | Source text token probe is clean; visual panels are temporal-blended, cropped, mildly warped, downsampled, noised, JPEG re-encoded, and fixed-size padded. Exact upstream window recovery is low; source sequence appearance is sometimes recoverable but does not contain the private ledger labels. |
| Metric strictness | PASS | Row score power increased to 1.55. Structural invalid submissions return 0.0; row-local malformed/overlong JSON zeros the affected row; booleans, non-finite JSON constants, invalid enums, invalid ranges, and overlong JSON are rejected. Perfect remains 1.0. |
| Penalties and constraints | PASS | Exact column order, complete ID set, unique IDs, finite `[0,1]` uncertainty, JSON length caps, valid ranges/enums, and span/edge grammar are enforced. |
| Obfuscation | PASS | Opaque IDs, source-neutral challenge prose, stripped raw names/timestamps/paths, transformed panels, fixed-size media, and private-only source map. |
| Noise/degradation | PASS | Public degraded pose is deterministically derived from real pose/IMU/video signals and private targets compare against real reference trajectories, not arbitrary labels. |
| Data proportionality to task | PASS | Public data includes exactly the task evidence: frame panels, IMU sequence summaries, degraded pose trace, and coarse context. Baselines show no single auxiliary modality saturates the task. |

## Checkpoints File

| Checkpoint line | Status | Evidence |
|---|---|---|
| Data Leakage | PASS | Train/test split is by whole source recording; IDs are salted; public CSVs omit raw names, timestamps, and source paths. |
| Baseline score is not too high | PASS | Sample 0.134105, train-prior 0.144499, degraded-pose-only 0.218540, simple CPU NN 0.261687, ID/file/path shortcuts below 0.29, perfect 1.0. |
| Class distribution is fine | PASS | Private groups: device 287/192, motion 287/192, failure 242/237; all exceed `MIN_GROUP_TEST=20`. |
| No missing data anywhere | PASS | `_sanity_smoke.py` checks train/test/answers for NaN and all referenced images exist. |
| What not to use section present | PASS | Present inside Overview and section 9, with source lookup, GPU/API, metadata-only, hidden-answer, and grader-exploit bans. |
| Source reversibility checked | PASS | `_analyze.py` checks raw token leakage plus simple and crop-aware visual retrieval; exact-frame top-1 0.0109/top-5 0.0297 over 640 tile queries and crop-aware exact-window top-1 0.0250/top-5 0.0750 over 120 rows. |
| Novelty checked before build | PASS | `SOURCE_VERIFICATION.md` identifies Monado/EuRoC/TUM VI as nearest neighbors and documents a 7/10 ledger-task novelty judgment. |
| Source and licensing | PASS | Hugging Face source lists `cc-by-4.0`; exact official files, sizes, hashes, and attribution requirement are documented. |
| Raw assets only | PASS | `raw_upload.zip` contains only unchanged official sequence members, no public/private splits or generated labels. |
| Speech/text domain fit | N/A | Visual-inertial headset challenge, not speech/text. |
| Synthetic sanity check | N/A | Real-data challenge; `generate.py` is a bounded official-source acquisition helper. |
| Real-world ML value | PASS | Operational AR/VR tracking audit and repair ledger, not a contrived scalar target. |
| Fair split and OOD testing | PASS | Whole recordings are held out; train and test share domain structure but no source sequence. |
| Metric and headroom | PASS | Structured metric rewards spans, anchors, reliable keyframes, failure type, uncertainty, and consistency; weak baselines leave >65 percentage points to perfect. |
| Robust grader validation | PASS | Wrong columns/order, duplicate IDs, ID-set mismatch, non-finite or out-of-range uncertainty return 0.0. |
| No internal leaks | PASS | Grader returns scalar scores only; no exceptions expose answers or split logic. |
| Agent-code safeguards | PASS | What Not To Use bans GPU, hosted APIs, source lookup, hidden-answer access, and metadata-only solutions. |
| Feature isolation | PASS | Public IDs, paths, row order, and filenames are opaque; `_analyze.py` checks token and visual retrieval leakage. |
| No rule leaks | PASS | Participant form describes visible evidence and output schemas without source filenames, raw timestamps, or deterministic degradation constants. |
| Anti-regex/anti-lookup | PASS | Task requires visual, IMU, degraded-pose, and sequence reasoning; metadata-only and source lookup baselines are weak/banned. |

## Previous Reviews Coverage

The full `prev_reviews.txt` file has 2,847 lines. I mapped its repeated reviewer lessons into the checks below and patched the challenge where needed.

| Review-memory theme | Status | Evidence or change |
|---|---|---|
| Avoid disabled-domain routing from generic classification wording | PASS | Title and opening frame the task as a structured AR/VR repair ledger, not classification. |
| Keep visible title source-general and task-specific | FIXED | Challenge title is now `Visual-Inertial Tracking Failure Detection and Localization`, which names the visual-inertial domain and the failure detection/localization task clearly; upstream source name appears only in source/dataset docs. |
| Dataset title describes raw corpus, not task outputs | PASS | Dataset title is `Real Headset Visual-Inertial Short Sequence Archives`. |
| Use real data and verify license | PASS | Official Monado files, license, sizes, hashes, and URLs are in `SOURCE_VERIFICATION.md`. |
| Match dataset form to validator-visible raw tree | FIXED | `DATASET_FORM_FILL.md` now describes the validator-visible five top-level sequence directories and their `<sequence>/mav0/...` contents, matching the platform tree after raw source extraction. |
| Keep raw upload clean | PASS | Audit confirms no nested `raw_data/`, source/cache files, or private answers in `raw_upload.zip`. |
| Keep raw upload under practical budget | PASS | Clean upload zip is about 965 MB; prepared public/private data is about 16.8 MB. |
| Do not describe prepared splits or scoring in dataset form | PASS | Dataset form is a raw-source data dictionary only. |
| Include explicit Features/data dictionary | PASS | Dataset form lists archive member properties and source CSV columns. |
| Standard platform `prepare(raw, public, private)` callable | FIXED | Added importable `prepare(raw, public, private)` and tested its signature and execution. |
| Preserve CLI convenience without platform mismatch | PASS | CLI now wraps the same implementation used by the platform callable. |
| Prepare from raw input only, not adjacent hidden files | PASS | Preparation resolves all source material from the raw directory, official ZIPs, or extracted top-level sequence directories. |
| Accept platform-extracted raw layout | PASS | `prepare.py` accepts official ZIPs and extracted `<sequence>/mav0/...` directories. |
| Deterministic preparation | PASS | No parallel nondeterminism; salted hashing controls public IDs and panel transforms. |
| Split-leak-safe IDs | PASS | Salted SHA-256 ID pool over all scene keys; train/test IDs overlap is false. |
| Assert raw key uniqueness before ID mapping | PASS | `scene_hash.is_unique` assertion before ID assignment. |
| Check NaN/blank raw values before row casting | PASS | `_assert_no_missing_raw` rejects NaN and blank object cells. |
| Sort output CSVs by ID | PASS | train/test/answers/source map sorted by `id`. |
| Path sanitation for copied assets | PASS | Uses `Path(...).name` for raw frame names. |
| Public media paths must match disk layout | PASS | `_sanity_smoke.py` and challenge audit confirm train/test image paths exist. |
| No train/test duplicate IDs or source groups | PASS | Whole source sequences held out; train/test ID overlap false. |
| Public-corpus source lookup is not solved by filename stripping alone | FIXED | Added `_analyze.py` visual retrieval probes and strengthened prepared panels after the external CREMA-D-style review lesson; exact-frame top-1 0.0109/top-5 0.0297, crop-aware exact-window top-1 0.0250/top-5 0.0750. |
| Avoid direct source filenames/timestamps/paths in public CSVs | PASS | Token leakage probe reports `forbidden_public_tokens: false`. |
| Avoid metadata-only shortcut | PASS | Metadata/train-prior score 0.144499; source lookup and metadata-only solutions are banned. |
| Avoid degraded-pose-only saturation | PASS | Degraded-pose-only heuristic is 0.218540, well below competitive ceiling. |
| Add baseline/headroom evidence | PASS | `_analyze.py` reports sample/prior/degraded/CPU NN/perfect scores. |
| Increase undersized split when possible | FIXED | Window stride changed from 6 to 2; prepared split grew from 110/160 to 328/479 rows. |
| Keep sample valid and above platform floor | PASS | Sample score is 0.134105, above 0.12 and below 0.5. |
| Perfect labels score exactly 1.0 | PASS | `_sanity_smoke.py` verifies perfect score 1.0. |
| Invalid structural submission returns 0.0 | PASS | Duplicate-row smoke score is 0.0; wrong/missing columns return 0.0. |
| Grade supports DataFrame platform calls | PASS | `grade(submission_df, answers_df)` used in smoke/analyze. |
| CLI grader should not traceback on bogus paths | FIXED | Bad path prints `0.0` without traceback. |
| Reject duplicate IDs and row-set mismatch | PASS | `grade.py` checks submission and answer duplicate IDs, row count, and ID set. |
| Enforce exact columns and order | PASS | `SUBMISSION_COLUMNS` is checked with `list(submission.columns)`. |
| Validate finite/out-of-range numeric fields | PASS | `uncertainty` is finite and constrained to `[0,1]`. |
| Cap submitted JSON length | PASS | `MAX_JSON_LEN=6000` applies before JSON parsing. |
| Malformed row-local JSON should zero the affected row, not crash whole file | PASS | Parsers return `None` for invalid row-local content; `_row_score` gives that row 0.0 while other valid rows continue scoring. |
| Avoid validity-only score inflation | PASS | No automatic validity points; score is from semantic heads plus consistency. |
| Include exact metric formula in visible Evaluation | PASS | Evaluation lists head formulas, weights, row power, and worst-group aggregation. |
| Include top-level Overview/Evaluation/Dataset/Submission siblings | PASS | Challenge form uses sibling headings in section 3. |
| Open with plain-language objective | PASS | Overview begins with a plain-language objective sentence. |
| Define all public JSON schemas and enum values | PASS | Dataset and Submission define IMU, degraded pose, span, edge, failure type, and uncertainty schemas. |
| Include exact `./working/submission.csv` instruction | PASS | Present in Submission section. |
| Include parseable CSV example | PASS | Submission example is fenced CSV with escaped JSON cells. |
| Keep tables compact and real Markdown | PASS | Challenge audit reports compact real markdown tables. |
| Do not include rubrics or “What makes this challenging” | PASS | Neither appears in challenge form. |
| Put What Not To Use in visible problem description | PASS | Included in Overview and repeated in section 9. |
| Avoid preparation-transform leakage in participant form | PASS | Form says panels are public evidence but does not disclose crop/contrast/JPEG constants. |
| Use CPU-only constraints in visible block | PASS | Overview states 1.5 hours, 10 CPU cores, 62 GB RAM, CPU-only. |
| Ban hosted APIs/downloaded teachers/GPU | PASS | What Not To Use covers GPU, hosted APIs, remote inference, external labels, and challenge checkpoints. |
| Use real semantic worst-group axes | PASS | Private groups are device, motion, and failure type, not hash/random parity. |
| Sparse subgroup handling must not overwrite axes | PASS | No sparse fallback is used; all private subgroup counts exceed 20. |
| Avoid source-specific schema vocabulary when novelty scanner may anchor on source | PASS | Public challenge schema says headset tracking ledger, not Monado/EuRoC/TUM trajectory benchmark labels. |
| Novelty changes must affect schema, not only prose | PASS | The actual output schema is a failure/repair ledger with keyframes, spans, edges, state, and uncertainty. |

## Commands Rerun

```
python prepare.py --raw-dir raw_sources --output-dir .
python _sanity_smoke.py
python _grader_exploit_tests.py
python _analyze.py
python -c "from prepare import prepare; import inspect; print(inspect.signature(prepare))"
python grade.py does_not_exist.csv private\answers.csv
python "C:\Users\vamsh\.codex\skills\challenge-builder\scripts\challenge_audit.py" --challenge "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Headset Visual-Inertial Tracking Failure Ledger" --root "C:\Users\vamsh\Downloads\create_challenge_synthetic"
```
