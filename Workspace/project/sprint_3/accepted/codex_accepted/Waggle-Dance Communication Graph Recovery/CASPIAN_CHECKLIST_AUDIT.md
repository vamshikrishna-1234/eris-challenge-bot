# Caspian Checklist Audit

Checked on 2026-07-19 against the exact checklist supplied by the user.

Legend: `[p]` pass, `[w]` warn, `[f]` fail, `[n/a]` not applicable.

## 1. Dataset & Audio/Text Quality

| Status | Point | Evidence |
|---|---|---|
| `[p]` | Source and licensing | The official Zenodo record is a dataset and shows `Creative Commons Attribution 4.0 International`; `SOURCE_VERIFICATION.md` records CC BY 4.0, source title, DOI, and checksum evidence. |
| `[p]` | Raw assets only | `waggle_dance_raw_subset.zip` has 18 source/provenance entries, required official CSVs, date-level track CSVs, `SOURCE_MANIFEST.csv`, `LICENSE.txt`, and no `public/`, `private/`, answers, caches, or source scripts. |
| `[n/a]` | Speech/text domain fit | This is a real trajectory/graph challenge, not ASR, TTS, speech AI, code-switching, or text. |
| `[n/a]` | Synthetic sanity check | The challenge is real-data. `generate.py` is a provenance/download helper only and does not generate synthetic labels or data. |

## 2. Challenge Design & Evaluation

| Status | Point | Evidence |
|---|---|---|
| `[p]` | Novelty | `SOURCE_VERIFICATION.md` identifies the nearest neighbor as the source paper/dataset's own automatic waggle/follower detection pipeline and documents a novelty judgment of `6.5/10`. The public task is episode-level communication graph recovery, not the source canonical per-frame behavior target. |
| `[p]` | Real-world ML value | The task recovers honey-bee waggle-dance communication graphs from multi-agent observation-hive trajectories. It requires temporal segmentation, participant identification, role separation, directed edge recovery, and calibration. |
| `[p]` | Fair split and OOD testing | Final split has 414 train and 339 test rows. It splits by recording date, drops raw dancer overlap, uses opaque local episode IDs, and keeps all hidden subgroup buckets at or above 43 rows. |
| `[p]` | Metric and headroom | Perfect is `1.000000000000`; train-prior sample is `0.122632237663`; metadata-only is `0.082239810063`; metadata plus file-size nearest-label copy is `0.132319095494`; spam-everything no-track is `0.128992013128`; simple trajectory heuristic is `0.130554055593`; empty/no-track is `0.001840913609`. Large headroom remains for stronger learned models. |

## 3. Robust Grader & Exception Handling

| Status | Point | Evidence |
|---|---|---|
| `[p]` | Input validation | Active tests raise `InvalidSubmissionError` for wrong column order, extra column, missing column, duplicate ID, missing row, extra row, NaN confidence, infinite confidence, and out-of-range confidence. Row-local malformed JSON and impossible local dancer IDs degrade without crashing. |
| `[p]` | No internal leaks | `grade()` raises generic structural `InvalidSubmissionError` messages without printing answer rows, hidden labels, split logic, or private scoring data. |
| `[p]` | Agent-code safeguards | No solver/submission pipeline is shipped. The sample is a deterministic train-label-prior baseline, not a fallback model stack or hidden-test adaptive pipeline. |

## 4. Leakage & Shortcuts

| Status | Point | Evidence |
|---|---|---|
| `[p]` | Feature isolation | Public CSVs have zero NaN values. All public NPZ numeric arrays are finite, with no object/string arrays. Public rows strip raw dates, timestamps, source filenames, raw bee IDs, frame IDs, track IDs, dance IDs, feeder IDs, and raw row order. |
| `[p]` | No rule leaks | The visible challenge prompt avoids source name, selected dates, split construction, exact preprocessing internals, raw identifiers, disabled-domain wording, and hidden scoring tricks. |
| `[p]` | Anti-regex / anti-lookup | `_analyze.py` checks raw-token leakage, exact public NPZ feature signatures, rounded feature signatures, coarse public-feature lookup, file-size shortcut baselines, spam-everything templates, and sampled raw-coordinate overlap. No source-reversibility findings were reported. Metadata-only, file-size nearest-copy, spam, and empty baselines remain weak. |

## Executed Checks

Active validation performed in this pass:

* Reverified the official Zenodo page for dataset title, files, and CC BY 4.0 license.
* Regenerated `public/` and `private/` after replacing unobserved dense-tensor NaN cells with finite zeros plus `dense_mask`.
* Checked all public CSVs for NaN: train `0`, test `0`, answers `0`, sample `0`.
* Checked all public NPZ files for non-finite numeric arrays: `0` findings.
* Checked all public NPZ files for object/string arrays: `0` findings.
* Tested structural invalid submissions: all raised `InvalidSubmissionError`.
* Tested row-local malformed JSON: submission remained scoreable and below perfect.
* Tested row-local impossible local dancer ID: affected row was zeroed without crashing.
* Tested file-size nearest-label-copy shortcut: score `0.132319095494`, near weak heuristic but far below perfect.
* Tested spam-everything no-track shortcut: score `0.128992013128`, below the simple trajectory heuristic.
* Tested sampled raw-coordinate overlap: `0/12000` exact rounded-coordinate hits.
* Confirmed source-reversibility scan has no findings.

No checklist item remains `[f]` or `[w]`.
