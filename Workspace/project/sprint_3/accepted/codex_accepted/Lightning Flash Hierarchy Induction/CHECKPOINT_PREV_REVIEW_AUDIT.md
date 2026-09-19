# Checkpoints and previous-review compliance audit

Checked on 2026-07-16 against:

- `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints`
- `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt` (2,641 lines)
- `C:\Users\vamsh\Downloads\create_challenge_synthetic\.cursor\rules\challenge-creation.mdc`
- `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\LATEST.md`

The previous-review file was read as a line-by-line historical log. Date lines, reviewer-name lines, approval-only lines, and domain-specific lessons for unrelated media types are treated as historical or N/A; every actionable issue, fix, preventive check, and repeated lesson is collapsed into the compliance families below.

## Caspian checklist exact statuses

1. Dataset and audio/text quality

- [p] source and licensing: NOAA/NCEI and NODD official policy says NOAA environmental data are open/public-domain in the United States and NODD GOES data may be used as desired. The stale internal NetCDF `license` string is documented in `SOURCE_VERIFICATION.md`; it is a publication note, not a blocker under the official access policy.
- [p] raw assets only: the source upload is five untouched official NetCDF4 objects, or direct URL import of those objects. No pre-baked public/private split, derived label table, preprocessed raw archive, or synthetic raw corpus is uploaded.
- [n/a] speech/text domain fit: this is not an ASR, TTS, code-switching, or text challenge.
- [n/a] synthetic sanity check: the data are real official satellite files, so no synthetic generator is required or appropriate.

2. Challenge design and evaluation

- [p] real-world ML value: the task reconstructs a real event-to-group-to-flash lightning hierarchy from redacted local satellite measurements with uncertainty and calibrated structured output, not a decorative wrapper around a toy label.
- [p] fair split and OOD testing: whole source windows stay entirely in train or test, hidden robustness axes meet `MIN_GROUP_TEST = 30`, and the public train signal supports the same hierarchy reasoning needed on test.
- [p] metric and headroom: the metric matches the nested-partition task with count-consistent group pair F1, count-consistent flash pair F1, uncertainty F1, exact hierarchy consistency, and calibration. `sample_submission.csv` scores 0.17546042080012897; the best non-learning shortcut is 0.224933, leaving 0.775067 headroom to perfect.

3. Robust grader and exception handling

- [p] input validation: `grade.py` rejects wrong/reordered/extra columns, empty submissions, missing/extra/duplicate ids, private answer id defects, nonfinite confidence, confidence outside `[0,1]`, oversized JSON, malformed row JSON, duplicate detection/group structure, and row-set mismatches.
- [p] no internal leaks: submission-level errors are generic schema errors; row-local malformed JSON scores that row as zero without printing labels, split logic, answer keys, or private scoring internals.
- [p] agent-code safeguards: there is no solver submission pipeline, no `models = []` fallback, no hidden fallback solver, no inner-join scoring loophole, and no broad exception path that converts failed modeling into a shortcut prediction. The only broad exception found is optional memory reporting in `_sanity_smoke.py`, outside grader behavior.

4. Leakage and shortcuts

- [p] feature isolation: public inputs contain only opaque case/detection ids and normalized local point features. Public CSVs expose no native source filenames, exact timestamps, coordinates, native ids, source windows, file order, or file-size cues; rows and detections are sorted by opaque id.
- [p] no rule leaks: the participant-visible prompt defines the output contract but does not expose source object keys, split dates, native operational thresholds, exact construction transforms, alias salt, or hidden scoring tricks.
- [p] anti-regex/anti-lookup: `_analyze.py` measures lexical/schema-only, metadata-only, opaque-id order, opaque-id hash, JSON-length/count, fixed-threshold, and train-tuned DBSCAN attacks. These remain below the difficulty ceiling and leave more than 30 percent headroom, so the task requires learned point-set hierarchy inference.

## Checkpoints file

| Check | Status | Evidence |
|---|---|---|
| Data leakage | Pass | Public CSVs contain opaque case/detection ids only; no native filenames, timestamps, coordinates, source windows, or hierarchy ids. `_analyze.py` source-token checks pass. |
| Baseline score not too high | Pass | `sample_submission.csv` scores 0.17546042080012897; best non-learning shortcut is 0.224933, leaving 0.775067 headroom. |
| Class distribution is fine | Pass | Test `source_window`, `density_bucket`, and `ambiguity_bucket` subgroups are guarded by `MIN_GROUP_TEST = 30`; smoke test verifies all buckets. |
| No missing data anywhere | Pass | `prepare.py` rejects missing prepared values; smoke verifies no NaN in public train/test; source arrays are checked with `np.isfinite`. |
| What Not To Use present | Pass | The platform-visible Problem Description includes inline What Not To Use bullets and enforcement wording; section 9 also mirrors the bans. |
| Source reversibility checked | Pass | `_analyze.py` probes source tokens, metadata-only prediction, feature-source prediction, opaque-id hash/order, JSON length/count, and duplicate feature vectors. |
| Novelty checked before build | Pass | `BUILD_NOTES.md` and `SOURCE_VERIFICATION.md` document nearest-neighbor novelty and rate the task 6.5/10; no local duplicate challenge was found. |
| Source and licensing | Pass with documented caveat | NOAA/NCEI/NODD official open-data policy supports use and redistribution; the stale NetCDF license-string caveat is documented in `SOURCE_VERIFICATION.md`. |
| Raw assets only | Pass | Direct URL import uses five untouched official NetCDF files; no pre-baked raw split or synthetic raw data is uploaded. |
| Speech/text domain fit | N/A | The challenge is structured satellite point-set hierarchy induction, not speech/text. |
| Synthetic sanity check | N/A | No synthetic generator is used; raw data are official NOAA files. |
| Real-world ML value | Pass | The task models event-group-flash hierarchy repair under redacted local satellite evidence, with uncertainty and calibrated structured output. |
| Fair split and OOD testing | Pass | Whole source windows stay in either train or test; related windows do not cross splits and public signal remains learnable. |
| Metric and headroom | Pass | Metric decomposes group pairs, flash pairs, uncertainty, exact hierarchy, and calibration. DBSCAN/threshold probes now score at most 0.224933 and leave 0.775067 headroom. |
| Robust grader | Pass | Wrong columns, extra columns, missing/extra/duplicate ids, NaN/inf/out-of-range confidence, malformed JSON, duplicate structure, and oversize JSON are tested. |
| No internal leaks | Pass | Invalid-submission messages are generic; row-local malformed JSON scores zero without private-label output. |
| Agent-code safeguards | Pass | No solver pipeline or fallback `models=[]` style path exists in grader or prepare code. |
| Feature isolation | Pass | Public rows are sorted by opaque id, source ids are stripped, and source lookup probes pass. |
| No rule leaks | Pass | The visible prompt describes the hierarchy contract but not exact construction transforms, native thresholds, hashes, or source object keys. |
| Anti-regex / anti-lookup | Pass | Lexical/schema-only, metadata-only, opaque-id, and length attacks remain weak, all at or below 0.157251 after metric reweighting. |

## Previous-review lessons

| Review lesson family | Status | Applied check or fix |
|---|---|---|
| Duplicate train/test rows | Pass | Train/test case ids are disjoint; no duplicate public feature vectors in the hidden split. |
| Problem/data count mismatch | Pass | Form states 210 train and 140 test, matching prepared files and smoke checks. |
| Optional columns giving advantage | Pass | Grader requires exactly `id,prediction_json,confidence`; no ignored probability/extra columns are accepted. |
| Same sample with conflicting labels | Pass | Each case id has one target hierarchy; duplicate public ids are rejected. |
| `merge(..., how="inner")` masking missing ids | Pass | Grader enforces exact id set and uses `how="left"` with `validate="one_to_one"`. |
| Broken markdown / all in one code block | Pass | Forms use normal headings, prose, tables, and fenced examples only where appropriate. |
| Low novelty / generic dataset reuse | Pass | The task is not ordinary lightning detection, storm tracking, image classification, tabular prediction, or canonical GLM use; novelty is documented at 6.5/10. |
| Unbounded or unclear score range | Pass | Declared and actual range is 0.0 to 1.0; perfect labels score exactly 1.0. |
| Missing unique-id and range checks | Pass | Grader rejects duplicate ids and invalid confidence values; smoke fuzzes these cases. |
| Public feature-name anonymization | Pass | Public columns are generic local features and opaque JSON ids; native column names are absent from public CSVs. |
| Agent scores saturated / low variance | Pass | `_analyze.py` decomposes weak, shortcut, threshold, DBSCAN, and small CPU learned baselines. |
| Dataset form should be a raw data dictionary | Fixed | Removed `prepare.py`, challenge-case, and downstream-public-input wording from `DATASET_FORM_FILL.md`. |
| Do not reveal test construction | Pass | Visible challenge text does not disclose exact source windows, object keys, split dates, construction thresholds, or proportions beyond observable row counts. |
| Do not reveal hidden generation rules/noise | N/A/Pass | Real-data build; visible text avoids exact native clustering thresholds and preparation transforms. |
| What Not To Use inside main description | Fixed | Converted the inline What Not To Use prose into visible bullets under Overview and kept enforcement wording. |
| Remove rubrics and grading YAML | Pass | No rubric section or grading YAML block exists. |
| Standard `prepare(raw, public, private)` signature | Pass | `prepare.py` exposes the required callable and local smoke invokes it directly. |
| Required markdown tables | Pass | Problem Description contains public-file, train.csv, test.csv, detection-field, and submission tables. |
| No "What makes this challenging" section | Pass | That section is absent. |
| Dataset form must not mention scoring or challenge mechanics | Fixed | Dataset form now describes only raw NetCDF files, variables, license, source, and upload notes. |
| Submission example rows | Fixed | Submission section now includes header plus two parseable example rows and the exact `./working/submission.csv` path. |
| Prose line wrapping | Pass | Narrative prose is kept as logical single lines; tables and fenced examples keep their own structure. |
| Source lookup for public corpora | Pass | `_analyze.py` includes public/raw token scans, metadata prediction, opaque-id/hash/order attacks, and feature-source prediction. |
| Parallel nondeterminism in prepare | Pass | `prepare.py` does not use parallel result collection; smoke confirms byte-for-byte deterministic output. |
| Named primary metric and aggregation | Pass | Evaluation defines the row score formula and final mean score. |
| Nested JSON schema fully defined | Pass | `case_json`, `target_json`, `prediction_json`, group/flash constraints, uncertainty, and confidence are described in the Problem Description. |
| Fixed-valid baseline too high | Pass | There are no validity-only points; sample and metadata baselines remain weak, and exact hierarchy earns the main reward. |
| Public raw media fingerprinting lessons | N/A/Pass | No public raw media is released; source reversibility is tested through structured-feature and metadata probes. |
| Sparse subgroup repair lessons | Pass | Semantic robustness axes are `source_window`, `density_bucket`, and `ambiguity_bucket`; all hidden buckets meet the minimum without random parity axes. |
| Platform import layout clarity | Pass | Direct URL import is canonical. Fallback untouched-file upload is documented without creating a custom preprocessed raw ZIP. |

## Changes made in this review pass

- Cleaned `DATASET_FORM_FILL.md` so it no longer references `prepare.py`, downstream challenge cases, scoring, or participant-facing challenge mechanics.
- Converted the visible What Not To Use guidance into bullets inside the Problem Description Overview.
- Added the exact `./working/submission.csv` path and a second parseable sample row.
- Added this audit note to make the checkpoint and previous-review pass reproducible.
- Added `EXPLOIT_AUDIT.md`, strengthened `_analyze.py` with an official-raw reverse-matching probe, and added `_grade_exploit_audit.py` for degenerate valid-JSON and schema-cheating attacks.
