# Checkpoints and Previous Reviews Audit

Checked on 2026-07-17 against:

* `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints`
* `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt` (2,667 lines scanned)
* `C:\Users\vamsh\Downloads\create_challenge_synthetic\.cursor\rules\challenge-creation.mdc`
* `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\LATEST.md`

## Checkpoints

| Item | Result | Evidence |
|---|---|---|
| Data leakage | PASS | Salted opaque IDs, source stems absent, train/test sequence groups disjoint, whole-image source-thumbnail probe rank1 `0.005780`, and stronger multicrop source probe rank1 `0.052023` / rank5 `0.080925`. |
| Baseline not too high | PASS | Sample template now scores `0.269134`; metadata-only `0.233829`; CPU image kNN `0.297441`; perfect `1.0`. |
| Class distribution | PASS | Test buckets meet `MIN_GROUP_TEST=15`: mission min `18`, terrain min `39`, route min `27`. |
| No missing data | PASS | `prepare.py`, `_analyze.py`, and audit verify no NaN in train/test/sample/answers. |
| What Not To Use | PASS | Platform-visible overview and section 9 forbid source lookup, metadata-only shortcuts, APIs, rule templates, and grader exploits. |
| Source reversibility | PASS with residual risk | Source IDs, filenames, order cues, raw paths, and timestamps are stripped; public images are transformed. Stronger prohibited retrieval is still the main residual public-source risk. |
| Novelty before build | PASS with reviewer risk | `SOURCE_VERIFICATION.md` identifies AI4MARS segmentation and Mars traversability work as nearest neighbors and documents a cautious `6/10` recombined novelty claim. |

## Caspian Checklist

Legend: `[p]` pass, `[w]` warn, `[f]` fail, `[n/a]` not applicable.

### 1. Dataset And Audio/Text Quality

| Status | Item | Evidence |
|---|---|---|
| [p] | source & licensing | The NASA data page is public but says license not specified, so the challenge relies on the official Zenodo record linked from NASA. Zenodo lists CC BY 4.0, which permits redistribution/reuse with attribution, including commercial reuse. `DATASET_FORM_FILL.md` and `SOURCE_VERIFICATION.md` state CC BY 4.0 and attribution requirements. |
| [p] | raw assets only | `ai4mars_official_expert_subset.zip` contains only byte-identical official AI4MARS image, mask, and documentation/mapping files. Audit confirms it excludes `public/`, `private/`, source/cache files, and prepared split artifacts. |
| [n/a] | speech/text domain fit | This is a real computer-vision rover-terrain challenge, not ASR/TTS, code-switching, or professional text data. |
| [n/a] | synthetic sanity check | The dataset is real official Mars rover imagery and masks. `generate.py` is only a source-manifest/downloader helper and does not synthesize labels or scenes. |

### 2. Challenge Design And Evaluation

| Status | Item | Evidence |
|---|---|---|
| [p] | real-world ML value | The task is operational rover traversability evidence from Mars terrain imagery: terrain regions, hazards, route class, clearance, blockage, safe width, and uncertainty. It tests learned image-to-structured-output behavior, not an arbitrary table/regression puzzle. |
| [p] | fair split & OOD testing | Split is grouped by rover/time/product sequence family so related frames do not cross train/test. Private robustness axes are real mission, terrain, and route groups; all meet `MIN_GROUP_TEST=15` with minima `18`, `39`, and `27`. |
| [p] | metric & headroom | The metric matches the mixed output contract: mask mIoU, hazard-box IoU-F1, route class, numeric corridor measures, joint consistency, and real worst-group aggregation. Sample template scores `0.269134`, leaving about `73.1%` absolute headroom to perfect `1.0`; metadata-only is `0.233829` and CPU image kNN is `0.297441`. |

### 3. Robust Grader And Exception Handling

| Status | Item | Evidence |
|---|---|---|
| [p] | input validation | `grade.py` raises `InvalidSubmissionError` for wrong or reordered columns, missing/extra rows, duplicate IDs, mismatched IDs, empty IDs, nonfinite numbers, and numeric values outside `[0,1]`. Row-local malformed mask/box JSON is capped and scores that row as zero rather than crashing. |
| [p] | no internal leaks | Invalid structures raise clean `InvalidSubmissionError`; the CLI read-path failure also emits `InvalidSubmissionError` without a traceback. Grader errors do not print private labels, answer keys, split salts, hidden source groups, or private test rows. Public metric weights are intentionally documented in the challenge description. |
| [p] | agent-code safeguards | There is no solver/submission pipeline bundled with the challenge and no sketchy fallback such as `models = []`. The broad `try/except` catches unexpected row-local grader issues as zero credit, while explicit structural submission problems are raised as `InvalidSubmissionError`. `_analyze.py` reports sample, metadata-only, image-kNN, and source-retrieval probes. |

### 4. Leakage And Shortcuts

| Status | Item | Evidence |
|---|---|---|
| [p] | feature isolation | Public features expose opaque salted IDs, transformed image paths, coarse mission/camera/dimensions, route query, and prompt only. Source stems, product IDs, timestamps, raw paths, private source groups, masks, and answer columns are absent from `test.csv`. CSVs are sorted by opaque ID. |
| [p] | no rule leaks | Public text defines the target/output contract and visible metric, but not private split salts, source stems, selected hidden rows, raw archive order, or private group labels. The deterministic route formulas are label definitions derived from the predicted mask, not hidden generator shortcuts. |
| [p] | anti-regex/anti-lookup | Regex, row-order, filename, metadata, and template inversion shortcuts are blocked and explicitly prohibited. `_analyze.py` verifies raw-stem absence, metadata-only weakness, sequence-group disjointness, media path existence, a whole-image source-thumbnail probe of rank1 `0.005780` / rank5 `0.017341`, and a stronger multicrop source probe of rank1 `0.052023` / rank5 `0.080925` / median rank `111`. Residual stronger public-source image retrieval remains a stated enforcement risk, but the task is not solvable by simple lookup or metadata matching and requires visual modeling. |

## Previous-Review Lessons Applied

| Lesson family | Result | Applied change/check |
|---|---|---|
| Tables and formatting | PASS | Markdown tables for files, train columns, test columns, and submission; no rubric or "What makes this challenging" section. |
| Single visible description | PASS | Overview, Evaluation, Dataset, and Submission are sibling sections; CPU limit and invalid-approach enforcement are visible. |
| Dataset form purity | PASS | Dataset form describes only the raw official archive subset, file tree, features, license, source, and notes. |
| Raw upload layout | PASS | `ai4mars_official_expert_subset.zip` is clean official-source material under 1 GB; handoff documents official-subset upload procedure. |
| Public source reversibility | PASS with residual risk | `_analyze.py` includes raw-id scans, metadata checks, source-family split checks, image path checks, whole-image thumbnail retrieval, and stronger multicrop source retrieval. |
| Strict grader | PASS | Exact column order, duplicate IDs, missing IDs, row mismatch, numeric finite/range checks, JSON length caps, malformed row-local JSON zeroing. |
| CLI failure hygiene | PASS | `grade.py` now exits with `InvalidSubmissionError` text and no traceback for unreadable CSV inputs. |
| Baseline headroom | PASS | Sample was reduced from `0.315726` to `0.269134`; metadata-only remains weak; image kNN leaves large headroom. |
| Metadata-only shortcut | PASS | Metadata-only baseline scores `0.233829`, well below perfect and below image-informed baseline. |
| Worst-group axes | PASS | Mission, terrain, and route groups are real semantic axes, not random salted parity splits. |
| Sparse subgroup repair | PASS | Rare labels are absorbed without flattening a whole axis; all evaluated buckets meet the minimum. |
| Path and ID leaks | PASS | Public media paths use split prefixes, source stems are absent, IDs are salted and opaque, and CSVs are sorted by ID. |
| Novelty scanner hygiene | PASS | Removed `segmentation` from tags and foregrounded the route-conditioned traversability ledger contract. |

## Targeted Shortcut Audit

| Check | Result | Evidence |
|---|---|---|
| ID exploit | PASS | IDs match `rvr_[0-9a-f]{14}`, train/test ID overlap is `0`, sorted IDs interleave splits, and the longest same-split run in sorted ID order is `9`. |
| Submission IDs | PASS | Grader aligns by exact ID set and raises `InvalidSubmissionError` for missing, extra, duplicate, blank, or mismatched IDs; row order does not create target credit. |
| Hashing exploit | PASS | Public image SHA-256 hashes have `0` exact hits among official raw source images; ID salt is not exposed in public CSVs or challenge prose. |
| File-size exploit | PASS | `0` public JPEG byte sizes equal any raw official image byte size, and `0` test rows are uniquely recoverable by raw file size. A file-size-only kNN baseline scores `0.267193`, weak and below `0.5`. |
| Original-source lookup | PASS with residual risk | Exact hash lookup is closed, filename/source tokens are absent, whole-image thumbnail source retrieval is rank1 `0.005780`, rank5 `0.017341`, median rank `199`, and the stronger multicrop source probe is rank1 `0.052023`, rank5 `0.080925`, median rank `111`; stronger prohibited local-feature retrieval remains the public-source residual risk. |
| Public/original 1:1 correlation | PASS with residual risk | Each prepared row is derived from one real official image/mask pair, but not as an exact byte copy or source-sized crop. The prepared artifact is a transformed aligned view, and simple source-correlation probes remain weak. |
| Metric strictness | PASS | Perfect is exactly `1.0`; malformed row-local JSON or an invalid route class string zeroes that row; wrong columns, duplicate IDs, missing IDs, nonfinite values, and out-of-range numerics raise `InvalidSubmissionError`. |
| Penalties and constraints | PASS | JSON length caps, class-value bounds, route-class vocabulary, max eight boxes, box coordinate bounds, and numeric `[0,1]` ranges are enforced. |
| Obfuscation | PASS | Public artifacts use salted opaque IDs, transformed/re-encoded images, stripped source identifiers, split-prefixed non-source paths, and sorted CSVs. No arbitrary target labels or LLM-generated labels are introduced. |
| Noise | PASS | No synthetic label noise is added. Image hardening is label-preserving; unknown/uncertainty comes from official NULL mask coverage. |
| Image/task proportionality | PASS | Targets are derived from the real mask aligned to the public image and route corridor. CPU image kNN scores `0.297441`, above the sample template `0.269134` while still leaving large headroom, so images carry task signal without shortcut saturation. |

## Verification Commands

```powershell
python _sanity_smoke.py
python _analyze.py
python "C:\Users\vamsh\.codex\skills\challenge-builder\scripts\challenge_audit.py" --challenge "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Rover Traversability Ledger From Mars Terrain Images" --root "C:\Users\vamsh\Downloads\create_challenge_synthetic"
```

Final results: smoke PASS, analysis PASS, challenge audit `0` failures and `0` warnings.
