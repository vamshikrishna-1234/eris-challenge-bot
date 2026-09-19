# Aikyatan Checklist Audit — Lightning Flash Hierarchy Induction

Audit date: 2026-07-17

Challenge folder: `D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Lightning Flash Hierarchy Induction`

Checklist audited against: `D:\create_challenge_synthetic_output_folder\sprint_3\checklist_aikyatan.txt`

Verdict: SHIP under the current live challenge-builder/platform rules, with notes. I found no data leakage, grader, source-license, shortcut, determinism, or platform-survivability blocker. The only checklist warnings are version/format mismatches where the Aikyatan checklist asks for legacy artifacts or forbids Markdown tables while the current live rules require the platform form files and require Markdown tables in the problem description.

## Fingerprints

- `raw_data/`: SHA-256 tree hash `224ab6f91d94fdad87a955af9bbd54ba8a177b710942411457df455b5ac905ea`; 5 files; 2,901,827 bytes.
- `public/`: SHA-256 tree hash `415f09aea13664b83ff66a3538c8ea83ba318adc1c2e72aec8a4ffd2e3768c05`; 3 files; 1,263,818 bytes.
- `private/`: SHA-256 tree hash `41ed40cb7eaa56f29356c48b6387ae3867ad8a53175358fba9b6cd3cc6c39355`; 1 file; 118,982 bytes.
- Raw upload zip: `glm_official_raw_untouched_with_attribution_20260716_210000.zip`; 1,107,424 bytes; 6 entries; no `raw_data/`, `public/`, `private/`, `__pycache__`, `__MACOSX`, or `.DS_Store` entries.

## Score ladder

- Perfect labels: `1.0`.
- Small CPU pairwise model: `0.340643`; closes about 20.0% of the sample-to-perfect gap and about 15.0% of the best-shortcut-to-perfect gap. This is intentionally a compact feasibility baseline, not an elite reference.
- Train-tuned DBSCAN shortcut: `0.224933`; strongest measured non-learning shortcut.
- Fixed operational-threshold surrogate: `0.206663`.
- Sample submission: `0.17546042080012897`; valid, non-degenerate, above the platform floor, below 0.3.
- Opaque ID hash attack: `0.157251`.
- Metadata/schema-only baseline: `0.146721`.
- Lexical/schema-only baseline: `0.146721`.
- JSON length / point-count attack: `0.141396`.
- Opaque ID order attack: `0.140743`.
- Singleton one-flash degenerate output: `0.139911`.
- ID-pairs density exploit: `0.128787`.
- All-one empty uncertainty output: `0.096605`.
- Singleton many-flashes output: `0.05`.
- Native hierarchy oracle sanity check: `1.0`; used only to verify metric correctness and not a valid public strategy.

## Checklist headline results

- [p] Data leakage: public files contain no native filenames, exact timestamps, coordinates, scan identifiers, event/group/flash ids, source-window labels, or raw object keys. `_analyze.py` reports `forbidden_public_hits` all false, duplicate public feature vectors `0`, and train/test lexical ID boundary false.
- [p] Baseline score not too high: sample score is `0.17546042080012897`; best measured shortcut is `0.224933`; headroom to perfect is `0.775067`.
- [p] Class distribution is fine: private subgroup minimums are `source_window` min `70`, `density_bucket` min `65`, and `ambiguity_bucket` min `66`, all above `MIN_GROUP_TEST = 30`.
- [p] No missing data anywhere: `train.csv`, `test.csv`, `sample_submission.csv`, and `answers.csv` all have `0` NaN cells in the fresh schema check.
- [p] What Not To Use section present: present both inside the platform-visible problem description and in section 9 of `CHALLENGE_FORM_FILL.md`.
- [p] Source reversibility checked: `_analyze.py` reports top-1 exact raw-case recovery `0.0`, source-window top-1 `0.35`, median true-case rank `160.5/350`, p90 true-case rank `316/350`, and leakage gate pass.
- [p] Novelty checked before build: `SOURCE_VERIFICATION.md` names nearest neighbors and estimates novelty `6.5/10`; `BUILD_NOTES.md` says no duplicate GLM/lightning hierarchy challenge was found in the inspected sprint outputs/docs.

## Caspian checklist mapping

- [p] Source and licensing: NOAA/NCEI/NODD source supports open public use. Fresh web verification found the NOAA GOES registry states NODD data are open to the public and can be used as desired, with attribution/non-endorsement conditions; NCEI archive policy says NOAA/Federal environmental data are fully/openly available and public domain in the U.S., with CC0 intended where applicable. Caveat remains documented: the internal NetCDF global `license` string appears stale/conflicting, but official NODD/NCEI policy controls the selected source route.
- [p] Raw assets only: upload zip contains five untouched official `.nc` files plus `NOAA_ATTRIBUTION.txt`; no pre-baked splits, public/private files, generated labels, or processed raw data.
- [n/a] Speech/text domain fit: this is not ASR/TTS/code-switching/text data.
- [n/a] Synthetic sanity check: this is real official NOAA data, not synthetic data; no generator is needed.
- [p] Novelty: nearest-neighbor task documented; this is hierarchical point-set induction with nested partitions, uncertainty, and confidence, not ordinary lightning detection, storm tracking, weather forecasting, image classification, generic clustering, or the canonical GLM product task.
- [p] Real-world ML value: uses real GLM satellite hierarchy; asks for structured point-set hierarchy reconstruction under redaction.
- [p] Fair split and OOD testing: source windows are kept whole; private robustness buckets meet minimum counts; train signal supports the same point-set hierarchy reasoning needed on test.
- [p] Metric and headroom: metric matches nested group/flash partitions plus uncertainty and calibration; best shortcut leaves more than 30% headroom.
- [p] Input validation: strict checker rejects wrong/reordered/extra columns, missing/duplicate/foreign ids, NaN/inf confidence, out-of-range confidence, row-set mismatch, and malformed global structure.
- [p] No internal leaks: grader error messages are generic; platform-facing `grade()` returns `0.0` on submission-level structural failures; row-local malformed JSON is zeroed without printing labels.
- [p] Agent-code safeguards: no official solver notebook is shipped; local challenge scripts do not include a fallback solver that bypasses modeling.
- [p] Feature isolation: public rows use opaque case/detection ids and normalized point-set features; ID/order/hash/length attacks remain weak.
- [p] No rule leaks: visible prompt defines the task contract but does not expose raw object keys, split source windows, exact source times/coordinates, salt, native thresholds, or hidden construction transforms.
- [p] Anti-regex/anti-lookup: lexical/schema, metadata-only, ID order/hash, JSON length/count, fixed-threshold, DBSCAN, and raw reverse-lookup probes all remain below the difficulty gate.

## Gate summary

- Gate A — Static review: PASS-WITH-NOTES. Required current-platform artifacts exist: `prepare.py`, `grade.py`, `CHALLENGE_FORM_FILL.md`, `DATASET_FORM_FILL.md`, paste files, smoke/analyze/exploit scripts, source verification, raw zip. Aikyatan's legacy required inputs mention `config.yaml`, `solution.ipynb`, `rubrics.md`, `problem_description.md`, and `dataset_description.md`; those are not part of the current live challenge-builder form, where rubrics are explicitly removed and forms are consolidated into `CHALLENGE_FORM_FILL.md` and `DATASET_FORM_FILL.md`.
- Gate B — Determinism proofs: PASS. Two fresh subprocess `prepare.prepare(raw_str, public_str, private_str)` runs from the uploaded zip layout produced identical public/private tree hashes and matched the checked-in files.
- Gate C — Leakage audit: PASS. Public-test target absent; forbidden token scan clean; source lookup probes pass; public IDs are opaque; duplicate public feature vectors are zero.
- Gate D — Hardcoding and exploit red team: PASS. Best non-learning shortcut is `0.224933`; ID/hash/order/metadata/length attacks are weak; degenerate valid JSON outputs remain weak; perfect is still `1.0`.
- Gate E — Grader strictness battery: PASS. Perfect and shuffled-perfect both score `1.0`. Missing rows, duplicate rows, duplicate ids, foreign ids, renamed columns, extra columns, NaN confidence, and infinite confidence return platform grade `0.0` and strict `InvalidSubmissionError`. One bad row JSON and an oversized JSON cell zero only the affected row.
- Gate F — Reference solution verification: PASS-WITH-NOTES. No `solution.ipynb` is bundled in this challenge format. Instead, `_analyze.py` includes a small CPU pairwise model baseline scoring `0.340643` in `62.4` fit/tune/test seconds and process peak memory about `188 MiB`; this demonstrates CPU feasibility but is not a polished public notebook.
- Gate G — Documentation to reality diff: PASS. Documented public columns match real columns. Counts in docs match the real data: train `210`, test `140`, sample `140`, answers `140`. Dataset form avoids `grade.py`, `prepare.py`, score, submission, and split language.
- Gate H — Rubric audit: N/A. Current live rules explicitly remove rubrics; absence of `rubrics.md` is expected for this platform flow.
- Gate P — Platform survivability: PASS. `prepare()` works with string paths. Exact uploaded zip layout was extracted and prepared twice in fresh subprocesses. Raw zip is clean and flat. Sample submission scores above floor. Public/private/sample ids match.
- Gate N — Novelty and domain classification: PASS. Title and description frame a structured point-set/hierarchy task, not tabular classification/regression. Closest-neighbor novelty is documented in `SOURCE_VERIFICATION.md`; estimated novelty is `6.5/10`.
- Gate R — Render safety and formatting: PASS-WITH-NOTES / CHECKLIST CONFLICT. Aikyatan says "no markdown tables anywhere", but current live project rules require Markdown tables for file overview, train columns, test columns, and submission format. The platform also recently complained when tables were lost during rich-text paste. The current description keeps required tables and adds prose fallback definitions so it survives table-stripping. Do not remove the tables unless the live rules change.

## Evidence log

- Static artifact command observed: `prepare.py`, `grade.py`, `CHALLENGE_FORM_FILL.md`, `DATASET_FORM_FILL.md`, `PASTE_THIS_PREPARE.txt`, `PASTE_THIS_GRADE.txt`, `_sanity_smoke.py`, `_analyze.py`, `_grade_exploit_audit.py`, `SOURCE_VERIFICATION.md`, `requirements.txt`, and the raw zip all exist.
- Static artifact command observed signatures: `prepare_signature (raw: 'Path', public: 'Path', private: 'Path') -> 'None'`; `grade_signature (submission: 'pd.DataFrame', answers: 'pd.DataFrame') -> 'float'`.
- Zip command observed: `ZIP entries 6 size_bytes 1107424`; `ZIP bad_entries []`; entries are five NOAA `.nc` files plus `NOAA_ATTRIBUTION.txt`.
- CSV command observed: `public/train.csv (210, 4) ['id', 'case_json', 'prompt', 'target_json']`; `public/test.csv (140, 3) ['id', 'case_json', 'prompt']`; `public/sample_submission.csv (140, 3) ['id', 'prediction_json', 'confidence']`; `private/answers.csv (140, 8) [...]`; all duplicate-id counts `0` and all NaN counts `0`.
- Determinism command observed: run 1 and run 2 both returned `0` and printed `Prepared 210 train and 140 test hierarchy cases from 5 verified official files.`; `deterministic_public True`; `deterministic_private True`; `matches_checked_in_public True`; `matches_checked_in_private True`.
- Smoke command observed: status `PASS`; sample score `0.17546042080012897`; perfect score `1.0`; strict submission checks true; label invariant true; malformed row-local true; deterministic true; raw untouched true; prepare seconds about `1.64` and `1.38`; grade mean seconds about `0.022`; process peak about `227.7 MiB`.
- Exploit audit command observed: `passes true`; sample `0.17546`; perfect `1.0`; all-one-all-uncertain `0.156138`; singletons-one-flash `0.139911`; best random-100 `0.173597`; malformed/invalid submission checks all true.
- Challenge audit command observed: `SUMMARY failures=0 warnings=12`. Warnings are known/non-blocking for this real-data NetCDF challenge: no synthetic `generate.py`, no `zip_raw_for_upload.py`, generic CSV/media heuristics, manual split-safe/NaN/path checks, sample prose, and no image/audio path columns.
- Baseline/leakage command observed: difficulty gate passes; best shortcut `0.224933`; headroom `0.775067`; raw reverse lookup exact top-1 `0.0`; source-window top-1 `0.35`; metadata source-window CV `0.571429` vs chance `0.5`; public feature source-window CV `0.45`; duplicate public feature vectors `0`.
- Grader fuzz command observed: perfect `1.0`; shuffled perfect `1.0`; sample `0.17546042080012897`; missing rows/duplicate rows/duplicate ids/foreign ids/renamed column/extra column/NaN confidence/inf confidence strict errors and platform grade `0.0`; one bad JSON row and huge JSON cell score `0.9928571428571429` from an otherwise perfect 140-row submission; repeat sample grades identical.
- Documentation diff command observed: all documented columns and nested detection fields present in `CHALLENGE_FORM_FILL.md`; real columns match; documented counts `210`, `140`, score bounds `0.0`, `1.0`, formula constant `0.95`, and cap `200,000` present; dataset form contains no forbidden scoring/splitting/submission language.
- Public forbidden string scan observed: no `OR_GLM`, `GLM-L2`, `source_window`, native event/group/flash id markers, latitude, or longitude in public train/test/sample. A generic substring `2024` appears in `train.csv` only as random text content, not as a NOAA object/timestamp pattern; `test.csv` has no `2024` hit.
- Private subgroup command observed: `source_window {'window_d': 70, 'window_e': 70}`; `density_bucket {'compact': 75, 'dense': 65}`; `ambiguity_bucket {'higher': 66, 'lower': 74}`.

## Findings

- [MINOR] [Gate A/F/H] The Aikyatan checklist names legacy artifacts (`config.yaml`, `solution.ipynb`, `rubrics.md`, `problem_description.md`, `dataset_description.md`) that are not part of the current live form. Evidence: current rules say rubrics are removed and require `CHALLENGE_FORM_FILL.md` / `DATASET_FORM_FILL.md`; challenge audit reports zero failures. Proposed fix: do not add legacy files unless the platform explicitly asks; keep current form files as source of truth.
- [MINOR] [Gate A/P] `generate.py` and `zip_raw_for_upload.py` are absent. Evidence: challenge audit warns on both. Proposed fix: no change; this is a real-data NOAA build with a clean untouched official raw zip and direct-URL import option. Adding a synthetic generator would violate the source gate.
- [MINOR] [Gate R] Markdown tables exist in `CHALLENGE_FORM_FILL.md` and `SOURCE_VERIFICATION.md`. Evidence: formatting scan found 30 table lines in `CHALLENGE_FORM_FILL.md` and 7 in `SOURCE_VERIFICATION.md`. Proposed fix: no change under current live rules; challenge problem description tables are required, and prose fallback has been added for paste/render robustness.
- [MINOR] [Source/license] Official source policy is clear, but native NetCDF global metadata contains a stale conflicting `license` string documented in `SOURCE_VERIFICATION.md`. Evidence: `SOURCE_VERIFICATION.md` records the caveat; fresh official source check confirms NODD/NCEI open use. Proposed fix: keep the documented caveat and attribution; if a reviewer insists the internal string controls, obtain clarification from NOAA/NODD before submission.
- [PASS-BORDERLINE] [Gate C/D] Source-window recovery diagnostics are nonzero but not label-recovering. Evidence: raw reverse lookup exact top-1 `0.0`, source-window top-1 `0.35`, median true rank `160.5/350`; source-window labels are not public and are not the scored hierarchy. Proposed fix: no change; rerun `_analyze.py` if public feature construction changes.
- [PASS-BORDERLINE] [Gate D] DBSCAN has high flash-pair F1 but low total score. Evidence: train-tuned DBSCAN total `0.224933`, group-pair F1 `0.109566`, exact rate `0.0`, uncertainty F1 `0.219144`, headroom `0.775067`. Proposed fix: no change; current metric emphasizes the harder group/uncertainty/exact hierarchy components.

## Residual risks

- Platform novelty score is ultimately external. Local novelty documentation supports `6.5/10`, but the platform's scorer is the final arbiter.
- The no-table instruction in Aikyatan's checklist conflicts with current live rules and the platform's recent table-related validation behavior. I did not remove required tables.
- No full independent solver-agent notebook was run as part of this audit. `_analyze.py` does run a CPU-small trainable pairwise model baseline, but it is an analysis baseline rather than a polished solution notebook.
- The official-source license caveat should remain visible: NODD/NCEI policy supports use, redistribution, and CC0/public-domain treatment, while one internal NetCDF metadata string appears stale/conflicting.
