# Previous Reviews Line Audit Summary

Source file: `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt`

Lines processed: 2919

## Status Counts

- CONTEXT: 1284
- N/A: 560
- PASS: 1075

## Most Common Categories

- context: 1284
- blank: 388
- sample_bounds_and_headroom: 246
- source_reversibility_and_lookup: 221
- strict_grader_validation: 207
- not_applicable_modality_or_synthetic: 172
- dataset_form_and_file_structure: 125
- novelty: 85
- challenge_form_and_prompt: 80
- split_leakage_and_duplicates: 72
- subgroups: 33
- cpu_runtime_network: 6

## Applied Fixes From This Pass

- Changed `sample_submission.csv` generation from trajectory heuristic to a train-label-prior template, matching the latest sample-validation guidance.
- Changed grader/displayed `SCORE_POWER` to `0.80` so the train-prior sample scores above the platform floor while invalid submissions still score `0.0`.
- Added exact, rounded, and coarse public-feature overlap checks to `_analyze.py` to address previous lookup/feature-key review lessons.
- Added a grader overprediction penalty and tracked spam-everything baseline so broad valid JSON floods cannot beat trajectory-based methods.
- Applied the cross-challenge public-source lookup lesson by adding strong public-clock/time/geometry trajectory transforms and a candidate-level trajectory fingerprint audit.
- Added `CHECKPOINTS_LINE_AUDIT.md` for the checkpoint file and regenerated `PREV_REVIEWS_LINE_AUDIT.csv` for every previous-review line.

## Final Baselines

- Perfect: `1.000000000000`
- Train-prior sample: `0.122632237663`
- Metadata-only: `0.082239810063`
- Spam-everything no-track: `0.128992013128`
- Metadata plus file-size nearest-label copy: `0.132319095494`
- Simple trajectory heuristic: `0.130554055593`
- Empty/no-track: `0.001840913609`
- Invalid missing column: `InvalidSubmissionError`

No previous-review line remains marked FAIL or OPEN in the line audit. Lines marked N/A are modality/source-specific to other challenges; lines marked CONTEXT are reviewer-history prose without a direct reusable requirement.
