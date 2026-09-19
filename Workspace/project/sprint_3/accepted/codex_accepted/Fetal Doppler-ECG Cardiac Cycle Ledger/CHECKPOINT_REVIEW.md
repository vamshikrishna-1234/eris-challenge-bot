# Checkpoint And Previous-Review Audit

This audit was run against `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints` and `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt` on 2026-07-17.

## Requested Caspian Checklist

| Status | Checklist item | Notes |
|---|---|---|
| [p] | source & licensing | PhysioNet source is open access; ODC-By v1.0 explicitly includes commercial use, reuse, and redistribution with attribution. |
| [p] | raw assets only | Official raw source import is used; no pre-baked train/test split or processed raw package is the upload artifact. |
| [n/a] | speech/text domain fit | This is medical Doppler image plus physiological signal data, not ASR/TTS/code-switching/text. |
| [n/a] | synthetic sanity check | The official challenge data are real NInFEA files; `_sanity_smoke.py` is only a local mechanical fixture. |
| [p] | real-world ML value | The task is a real antenatal sensor-fusion ledger, requiring alignment of Doppler image, ECG channels, and respiration. |
| [p] | fair split & OOD testing | Split is whole-record; hidden robustness axes use cycle-count, respiration-motion, and envelope-visibility regimes. |
| [p] | metric & headroom | Structured metric matches the ledger task; envelope/quality/count heads are event-gated and confidence only modulates earned credit. Smoke sample is `0.424`, prior/metadata baselines are below `0.50`, empty-valid is `0.0`, and perfect is `1.0`. |
| [p] | input validation | Grader rejects wrong columns, reordered columns, missing rows, duplicate ids, answer duplicate ids, non-integer ids, invalid confidence, and impossible exact times. |
| [p] | no internal leaks | Grader returns numeric scores only and failure paths return `0.0`; no private labels or scoring internals are printed. |
| [p] | agent-code safeguards | No submitted solution pipeline is shipped; helper baselines contain no model-drop fallback or hidden-test bypass mechanism. |
| [p] | feature isolation | Public features omit source ids/times/order/metadata, use salted ids, fixed-dimension BMP strips, and fixed-shape NPY signal arrays. |
| [p] | no rule leaks | Participant prompt describes the clinical ledger task and allowed outputs without salts, source timing, split logic, or threshold recipes. |
| [p] | anti-regex/anti-lookup | Public task cannot be solved by regex or metadata lookup; What Not To Do bans source-row lookup and the target uses cross-modal evidence. |

## Checkpoints

| Checkpoint line | Status | Evidence or change |
|---|---|---|
| Data Leakage | Pass | `prepare.py` uses record-group split, salted opaque ids, sorted outputs, and strips source record ids, source filenames, exact start times, subject/session ids, `scene_hash`, split groups, and OOD axes from public CSVs. |
| Baseline score is not too high | Pass on smoke fixture | After hardening event matching to `0.08` seconds, smoke sample is about `0.290`, train-prior is about `0.338`, metadata-only is about `0.334`, and best fixed-periodic no-tech sweep is about `0.386`; full-corpus rerun is still required. |
| Class distribution is fine | Pass on smoke fixture | `MIN_GROUP_TEST` is enforced for `split_group`, `ood_axis`, and `render_style` with sparse Other-bucket merging. |
| No missing data anywhere | Pass on smoke fixture | Smoke preparation completed and grader/audit loaded all generated CSVs; `prepare.py` checks manifest NaN/blank fields before casting. |
| What not to use section present | Pass | Present inside the platform-visible problem description and in section 9. |
| Source reversibility checked | Pass with residual public-source risk | Public rows use transformed row-local assets and omit source ids/times. `_analyze.py` includes a source-column/source-value leak scan. Full media-fingerprint testing requires official NInFEA materialization. |
| Novelty checked before build | Pass | `SOURCE_VERIFICATION.md` names nearest NInFEA/fetal ECG/PWD neighbors and explains why the structured multimodal ledger differs from QRS detection, heart-rate regression, or envelope extraction. |
| Source/license allows challenge use | Pass | PhysioNet lists open access and ODC-By v1.0; ODC-By explicitly includes commercial use, and official source/import procedure plus attribution are documented. |
| Raw assets only | Pass | Preferred raw path is official PhysioNet import. No prepared raw ZIP or train/test package is used. |
| Speech/text domain fit | N/A | This is medical image/signal data, not speech/text. |
| Synthetic sanity check | N/A for official data | `_sanity_smoke.py` creates only a local official-shaped fixture for mechanical testing. |
| Real-world ML value | Pass | Clinical-style sensor-fusion ledger with image, ECG, respiration, events, envelope, quality, and uncertainty. |
| Fair split and OOD testing | Pass pending full source run | Splits are whole-record; private subgroups are real prepared quality/acquisition axes, not hash parity. |
| Metric and headroom | Pass on smoke fixture | Structured metric rewards event, timing, boundary, envelope, quality, count, calibration, and worst-subgroup robustness; a no-tech periodic sweep stays below `0.40` after the stricter event tolerance. |
| Robust grader input validation | Pass | Exact column order, id set, duplicate ids, duplicate answer ids, finite confidence, JSON length limits, non-negative row-local times, and impossible boundaries are handled. |
| No internal leaks | Pass | Grader returns numeric `0.0` for structural failures and does not print labels or private metadata. |
| Agent-code safeguards | Pass by design | No solution code is shipped; no fallback model list or hidden solver is present. |
| Feature isolation | Pass | Public columns avoid source identifiers, source paths, raw order, split groups, exact source times, and compressed file-size encodings; prepared strips are fixed-dimension de-identified BMP and signals are fixed-shape de-identified NPY arrays. Smoke scan found zero source-looking public values, zero train/test id overlap, no id-boundary split leak, and one unique file size per asset type. |
| No rule leaks | Pass | Participant docs describe the task contract and metric, not exact split salt, threshold values used in preparation, or record selection internals. |
| Anti-regex / anti-lookup | Pass with residual public-source risk | Public challenge bans source lookup and now constructs quality/events from cross-modal evidence, not a simple source metadata table. |

## Previous-Review Lessons Applied

| Prior-review lesson | Status | Evidence or change |
|---|---|---|
| Duplicate ids and row omissions must not score | Pass | `grade.py` rejects duplicate ids and id-set mismatch. |
| Answer duplicate ids must not enable many-to-one merge issues | Fixed | Added duplicate answer-id rejection in `grade.py`. |
| Exact submission columns and order required | Pass | `SUBMISSION_COLUMNS` and `list(submission.columns)` exact check. |
| Malformed row-local JSON should degrade rows, not crash | Pass | JSON parsing is length-capped and row-local malformed fields score as empty/invalid content. |
| Perfect labels must score exactly 1.0 | Pass | `_sanity_smoke.py` asserts perfect score is `1.0`. |
| Sample must be valid but weak | Pass | Sample is valid and scores about `0.29` on the smoke fixture after metric hardening. |
| Dataset form must be a raw data dictionary only | Fixed | Removed challenge-mechanics wording from `DATASET_FORM_FILL.md`. |
| Unstructured/non-tabular raw archives must not invent columns | Pass | Dataset Features section documents actual file properties only. |
| Tables must be real markdown with compact cells | Pass | Audit passes compact markdown table checks. |
| No rubrics or "What makes this challenging" section | Pass | Neither is present. |
| Submission must be top-level sibling under problem description | Pass | `## Submission` is a sibling of Overview/Evaluation/Dataset. |
| CPU/runtime constraints must be in visible description | Pass | CPU-only, 10 cores, 62 GB RAM, 1.5 hours are in Overview. |
| What Not To Use must be visible in main prose | Pass | It appears inside `## 3) Problem Description` and again in form section 9. |
| Do not leak exact test construction or preparation transforms | Pass | Visible docs omit salts, thresholds, exact start-time construction, and split details. |
| Source lookup warnings for public media/audio/image | Pass with caveat | Public source ids/times are stripped and `_analyze.py` scans public CSVs; full fingerprint probe awaits official corpus materialization. |
| Public-source tasks need source-neutral or novelty-safe framing | Pass | Title/opening emphasize "cardiac cycle ledger" rather than generic fetal QRS or envelope detection. |
| If novelty score is still below 6, add orthogonal target head | Already addressed | Output includes event ledger, envelope, quality flags, confidence, and subgroup robustness. |
| Avoid independent-head chance credit becoming too high | Pass on smoke fixture | Empty-valid is `0.0`, neutral-envelope wrong-events is about `0.105`, train-prior/metadata baselines are about `0.338`/`0.334`, and the best fixed periodic template is about `0.386`. |
| Prepare must expose `prepare(raw, public, private)` | Pass | Canonical callable and CLI wrapper are present. |
| Paste files must match canonical scripts | Pass | Audit confirms both paste files match. |
| Challenge audit helper should be rerun after changes | Pass | Final audit: `0 FAIL`, `3 WARN`, all non-blocking. |

## Changes Made During This Audit

* Revised `prepare.py` so event and quality labels use both Doppler-image peaks and ECG/signal evidence; matched support yields `usable`, image-only support yields `uncertain`, and strong signal-only support yields `artifact`.
* Hardened `prepare.py` against source reverse-mapping by applying deterministic row-local public-view perturbations before label extraction and by writing fixed-dimension BMP strips plus fixed-shape NPY signal arrays.
* Added answer duplicate-id rejection to `grade.py`.
* Removed participant-visible ```text code fences that the audit helper flags.
* Removed challenge-mechanics wording from `DATASET_FORM_FILL.md`.
* Added source-leak, id-boundary, and artifact-size scans to `_analyze.py`.
* Hardened `grade.py` so confidence cannot add standalone score, and envelope/quality/count credit are gated by event recovery.
* Tightened event/cycle matching from `0.14` seconds to `0.08` seconds after an exploit sweep found that a fixed periodic heartbeat template could otherwise exceed `0.50` on the smoke fixture.
* Refreshed `PASTE_THIS_PREPARE.txt` and `PASTE_THIS_GRADE.txt`.

## Remaining Warnings

* `.cursor/rules/challenge-creation.mdc exists`: audit root-shape warning from running outside the main workspace rule tree; not a challenge-content issue.
* `no upload zip found in challenge folder`: intentional because the required raw source path is direct official PhysioNet import, not a preprocessed raw ZIP.
* `pub/public directory not found`: intentional because persistent prepared splits are not shipped; temporary public/private outputs are created only during smoke tests.

## Remaining Risk

The full official NInFEA corpus was not downloaded and materialized locally in this audit. Before final platform submission, run `prepare.py` against the official PhysioNet import and rerun `_analyze.py`, `_sanity_smoke.py`-equivalent checks, and the challenge audit on the full prepared split.
