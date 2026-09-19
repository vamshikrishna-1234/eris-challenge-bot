# Aikyatan Checklist Audit - Waggle-Dance Communication Graph Recovery

Date: 2026-07-19

Verdict: SHIP. No blockers or major issues found after applying one minor grader CLI polish.

Scope: Audited the challenge against `D:\create_challenge_synthetic_output_folder\sprint_3\checklist_aikyatan.txt`, plus the live Eris challenge-builder rules. This is a real-data Eris challenge, so checklist items for `solution.ipynb`, `config.yaml`, `rubrics.md`, synthetic rendering, and full generated `raw/` are not applicable to this bundle format.

Important conflict: Gate R in the Aikyatan checklist says no markdown tables anywhere, but the live Eris rules require markdown tables in `CHALLENGE_FORM_FILL.md` for file overview, train columns, test columns, and submission schema. I kept the required Eris markdown tables. The challenge-builder audit confirms those tables are expected and correctly formatted.

## Fingerprints

- Raw upload ZIP SHA-256: `39d881c8bbcd2b8558539d31a604f8541125a83933caa6cf42b94f36f07a1c30`
- Public prepared tree SHA-256: `513c04639547c1a6ff6fec5e16fc8a311803bc38b8f3f85a9a1643a106440c74`
- Private prepared tree SHA-256: `5b00d4ec5af569b7a41feafed5333ee6ea87f3c9004435e69140dc1881c85629`
- Raw ZIP size: `738696915` bytes
- Public prepared size: `89256819` bytes
- Private prepared size: `597407` bytes

Evidence command:

```powershell
python - <<'PY'
from pathlib import Path
import hashlib
root=Path(r"D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Waggle-Dance Communication Graph Recovery")
# file/tree SHA-256 over waggle_dance_raw_subset.zip, public, and private
PY
```

Observed output:

```text
raw_zip_sha256= 39d881c8bbcd2b8558539d31a604f8541125a83933caa6cf42b94f36f07a1c30
public_tree_sha256= 513c04639547c1a6ff6fec5e16fc8a311803bc38b8f3f85a9a1643a106440c74
private_tree_sha256= 5b00d4ec5af569b7a41feafed5333ee6ea87f3c9004435e69140dc1881c85629
public_bytes= 89256819
private_bytes= 597407
raw_zip_bytes= 738696915
```

## Score Ladder

- Perfect submission: `1.000000000000`
- Sample submission: `0.122632237663`
- Empty/no-track baseline: `0.001840913609`
- Train graph prior baseline: `0.122632237663`
- Metadata-only baseline: `0.082239810063`
- Spam-everything/no-track baseline: `0.128992013128`
- Simple trajectory heuristic: `0.130554055593`
- Invalid missing-column submission: `InvalidSubmissionError`

Evidence command: `python _analyze.py`

Observed output excerpt:

```text
"perfect": 0.9999999999999998
"sample": 0.12263223766283594
"empty_no_track": 0.0018409136089894878
"train_graph_prior": 0.12263223766283594
"metadata_only": 0.08223981006320294
"spam_everything_no_track": 0.12899201312837794
"simple_trajectory_heuristic": 0.13055405559277142
"invalid_missing_column": "InvalidSubmissionError"
```

Interpretation: Trivial and metadata baselines remain weak, sample clears the platform floor, and there is large headroom to perfect.

## Findings

- PASS Gate A, Static Review - Mandatory Eris files exist, challenge form has required sections, dataset form avoids scoring/solution prose, paste files match canonical scripts. Evidence: `python "C:\Users\vamsh\.codex\skills\challenge-builder\scripts\challenge_audit.py" --challenge "<folder>"` returned `SUMMARY failures=0 warnings=11`. The warnings are non-blocking modality/static warnings already reviewed.

- PASS Gate B, Determinism - Tiny raw fixture prepare is deterministic across subprocess runs. Evidence command used `_sanity_smoke.py`; observed `determinism=pass`. Additional platform-layout determinism check produced identical public/private hashes across flat, `raw_upload`, same-named nested, and repeated layouts.

- PASS Gate C, Leakage Audit - Public CSVs contain no raw source IDs, timestamps, dates, frame IDs, bee IDs, feeder IDs, source filenames, or annotation IDs. Evidence: challenge audit reports train/test object values avoid source URL/raw path/source IDs; `_analyze.py` reports `source_reversibility_findings: []`, raw coordinate overlap `0/12000`, train/test id overlap `0`, and sample/answers ID match `True`.

- PASS Gate D, Hardcoding and Exploit Red Team - Metadata-only, file-size nearest-label-copy, spam, train-prior, and simple heuristic baselines remain weak. Evidence: `_analyze.py` reports metadata-only `0.08224`, metadata nearest-label-copy `0.12868`, file-size nearest-label-copy `0.13232`, and simple trajectory heuristic `0.13055`.

- PASS Gate E, Grader Strictness - Perfect and shuffled-perfect score exactly 1.0; structural malformed submissions raise `InvalidSubmissionError`; row-local malformed JSON degrades only the affected row. Evidence direct fuzz output: wrong column order, missing column, extra column, missing row, extra row, duplicate id, foreign id, NaN/inf/out-of-range confidence all raised `InvalidSubmissionError`; one bad JSON, one overlong JSON, invalid dancer, and self-edge returned `0.122031496816` versus sample `0.122632237663`.

- PASS Gate F, Reference/Solver Feasibility Adaptation - No official `solution.ipynb` is part of this challenge bundle, so the notebook-specific checks are N/A. CPU feasibility is supported by `_analyze.py`: heuristic feature pass over 339 rows took `15.31` seconds, about `45.17` seconds per 1000 rows, and the description explicitly targets CPU-compatible feature extraction plus compact models within 1.5 hours.

- PASS Gate G, Documentation-Reality Diff - Public CSV schemas, sample submission schema, row counts, no missing values, and train/test/private ID sets match the description. Evidence command checked train/test/answers/sample rows and columns: train `414`, test `339`, answers `339`, sample `339`, all `nan_cells=0`, all `duplicate_ids=0`.

- N/A Gate H, Rubric Audit - Live Eris rules remove rubrics. `CHALLENGE_FORM_FILL.md` avoids rubric wording, and the challenge-builder audit confirms this.

- PASS Gate P, Platform Survivability - `prepare()` casts string args to `Path`, accepts flat and nested raw layouts, keeps raw upload ZIP under the requested cap, and writes no private answers into public. Evidence: adapted prepare-layout test produced identical hashes for `flat_string_args`, `raw_upload_nested`, `same_named_nested`, and `flat_repeat`; `flat_repeat_matches=True`. Raw ZIP is about `704.476` MiB by challenge-builder audit.

- PASS Gate N, Novelty and Domain - Novelty note is documented in `SOURCE_VERIFICATION.md`. Nearest neighbor is the source paper/dataset automatic waggle/follower detection; this challenge materially differs by requiring episode-level temporal segmentation, local anonymized participant identification, follower-vs-attendee/passersby distinction, directed graph recovery, graph consistency, and confidence. It is not tabular, not regression, and not the hive-audio triage challenge.

- PASS-WITH-NOTES Gate R, Render/Formatting - The Aikyatan checklist's no-markdown-table rule conflicts with live Eris rules that require markdown tables. Current challenge keeps the required Eris tables, avoids fenced backup tables and `undefined` artifacts, and has compact table cells. Generated `__pycache__/` from local test runs was removed from the challenge folder.

## Gate Summary

- Gate A Static review: PASS
- Gate B Determinism proofs: PASS
- Gate C Leakage audit: PASS
- Gate D Hardcoding/exploit red team: PASS
- Gate E Grader strictness battery: PASS
- Gate F Reference solution verification: PASS-WITH-NOTES, notebook-specific checks N/A
- Gate G Documentation to reality diff: PASS
- Gate H Rubric audit: N/A
- Gate P Platform survivability: PASS
- Gate N Novelty and domain classification: PASS
- Gate R Render safety and formatting: PASS-WITH-NOTES due live-rule markdown-table conflict

## Changes Made During This Audit

- `grade.py`: changed no-argument script execution from exit-code `1` usage failure to clean usage output with exit-code `0`.
- `PASTE_THIS_GRADE.txt`: resynced from `grade.py`.
- Removed generated local `__pycache__/` from the challenge folder.

Post-change evidence:

```text
python _sanity_smoke.py
perfect_score=1.000000000000
determinism=pass
dataframe_call=pass
real_sample_score=0.122632237663

python "...challenge_audit.py" --challenge "<folder>"
SUMMARY failures=0 warnings=11

python grade.py
usage: python grade.py submission.csv answers.csv
exit code 0
```

## Residual Risks

- The final automated platform novelty score is external. Local novelty documentation and task design support the required novelty floor, but the platform's exact score must still be checked after submission.
- The Aikyatan guide is a generic robust bundle checklist and assumes files such as `config.yaml`, `solution.ipynb`, and `rubrics.md`; those are not part of this Eris challenge-folder contract.
- Full source URL import behavior must still be confirmed on the platform if using URL imports instead of the provided clean raw subset ZIP.
