# Checkpoints Line Audit

Source file: `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints`

Checked on 2026-07-19 after regenerating the real prepared split.

| Line | Status | Source line | Evidence |
|---:|---|---|---|
| 1 | N/A | `check for :` | Section heading. |
| 2 | PASS | `Data Leakage` | Public CSVs contain opaque IDs only; train/test IDs do not overlap; `_analyze.py` source scan passes. |
| 3 | PASS | `Baseline score is not too high` | Train-prior sample score is `0.12263223766283594`; spam-everything no-track score is `0.12899201312837794`; simple trajectory baseline is `0.13055405559277142`; perfect is `1.0`. |
| 4 | PASS | `Class distribution is fine` | Test subgroup counts all exceed `MIN_GROUP_TEST=12`: crowding, tracking quality, duration, waggle count, comb side, and session bucket. |
| 5 | PASS | `No missing data anywhere` | `prepare.py` fails on NaN in public train/test/answers; focused audit also checked all public NPZ numeric arrays are finite. |
| 6 | PASS | `What not to use section present` | `CHALLENGE_FORM_FILL.md` includes visible What Not To Use and invalid-approach enforcement. |
| 7 | PASS | `Source reversibility checked...` | `_analyze.py` checks raw-token leakage, NPZ object/string fields, exact/rounded/coarse feature lookup, file-size shortcut baselines, and sampled raw-coordinate overlap; `TRAJECTORY_SOURCE_LOOKUP_AUDIT.md` documents candidate-level trajectory fingerprint reduction from `40/40` rank-1 to `1/40` rank-1. |
| 8 | PASS | `Novelty checked before build...` | `SOURCE_VERIFICATION.md` documents nearest neighbor and estimates novelty `6.5/10`; task differs from source per-frame behavior classification. |
| 9 | N/A | blank | Blank line. |
| 10 | N/A | `checkpoints from Caspian:` | Section heading. |
| 11 | N/A | `[p] pass, [w] warn, [f] fail, [n/a] not applicable.` | Legend. |
| 12 | N/A | `1. dataset & audio/text quality` | Section heading. |
| 13 | PASS | `source & licensing...` | Zenodo API license id `cc-by-4.0`; CC BY 4.0 redistribution/commercial terms documented. |
| 14 | PASS | `raw assets only...` | Raw upload is clean official CSV/source subset with manifests; no `public/`, `private/`, or prepared splits in ZIP. |
| 15 | N/A | `speech/text domain fit...` | Challenge is trajectory/graph recovery, not speech, ASR/TTS, code-switching, or text. |
| 16 | N/A | `synthetic sanity check...` | Challenge is real-data. `generate.py` is only a provenance/download helper and does not synthesize labels. |
| 17 | N/A | `2. challenge design & evaluation` | Section heading. |
| 18 | PASS | `novelty...` | Source nearest neighbor documented; actual target is episode-level communication graph recovery, not source canonical per-frame label task. |
| 19 | PASS | `real-world ml value...` | Real honey-bee dance communication graph recovery from many-agent trajectories is a meaningful animal-behavior modeling task. |
| 20 | PASS | `fair split & ood testing...` | Split is by recording date, and raw dancer identities crossing test are dropped from train; target remains learnable from trajectory evidence. |
| 21 | PASS | `metric & headroom...` | Sample `0.123`, metadata-only `0.082`, file-size nearest copy `0.132`, spam-everything `0.129`, simple trajectory `0.131`, perfect `1.0`; large headroom remains. |
| 22 | N/A | `3. robust grader & exception handling` | Section heading. |
| 23 | PASS | `input validation...` | `grade.py` enforces exact ordered columns, unique IDs, full ID set, finite `[0,1]` confidence; row JSON malformedness scores row/head zero. |
| 24 | PASS | `no internal leaks...` | Grader raises `InvalidSubmissionError` on structural failure with generic messages; no private labels are exposed. |
| 25 | PASS | `agent-code safeguards...` | Challenge contains no solver pipeline or hidden fallback code; sample is deterministic train-prior baseline only. |
| 26 | N/A | `4. leakage & shortcuts` | Section heading. |
| 27 | PASS | `feature isolation...` | Public IDs, NPZ names, row order, and arrays strip dates/timestamps/raw IDs; exact/rounded/coarse train-test feature lookup scan passes; file-size label-copy baseline remains weak at `0.132319`. |
| 28 | PASS | `no rule leaks...` | Visible prompt avoids source name, selected dates, split construction, preprocessing details, and hidden grouping internals. |
| 29 | PASS | `anti-regex/anti-lookup...` | Required output needs temporal segmentation, participant roles, directed edges, and confidence from trajectory arrays; lookup/network/source methods are banned. |

No checkpoint line requires further code or form changes after this pass.
