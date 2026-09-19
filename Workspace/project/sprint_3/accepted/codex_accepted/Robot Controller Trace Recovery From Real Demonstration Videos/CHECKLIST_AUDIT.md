# Reviewer Checklist Audit

## Dataset And Audio/Text Quality

[p] Source and licensing: Zenodo record `6337847` is titled `Video-Trajectory Robot Dataset`, version `v1`, with `CC BY 4.0`. CC BY 4.0 permits redistribution, reuse, and commercial sharing/adaptation with attribution. See `SOURCE_VERIFICATION.md`.

[p] Raw assets only: preferred import is the official unmodified `PandaHandover_Real_Val.zip` URL. Manual fallback uploads only the unmodified official ZIP, or a wrapper ZIP containing only that official ZIP. No prepared train/test files or derived labels are uploaded as raw data.

[n/a] Speech/text domain fit: this is a robotics video/trajectory challenge, not ASR, TTS, or code-switching text.

[n/a] Synthetic sanity check: the challenge uses real official robot demonstration data. `generate.py` is only an optional official-source downloader/manifest helper, not a data generator.

## Challenge Design And Evaluation

[p] Real-world ML value: the task reconstructs an operational robot-controller trace ledger from real RGB/depth robot footage and sparse robot state evidence. The output is structured and multimodal: segments, event frames, waypoint bins, and confidence.

[p] Fair split and OOD testing: `prepare.py` uses a deterministic salted source-sample split over complete motion samples. This is not an artificial OOD split; each motion sample's RGB/depth/state/derived labels remain in one split, and raw IDs are stripped.

[p] Metric and headroom: the metric matches the structured controller-timeline contract and jointly scores segment timing, waypoint bins, event frames, and calibrated confidence. On the full real prepared split, the sample score is about `0.207`, perfect is exactly `1.0`, and the train-optimized constant-head shortcut is about `0.505`, leaving meaningful headroom while keeping no-model templates below the agent ceiling.

## Robust Grader And Exception Handling

[p] Input validation: `grade.py` enforces exact column order, duplicate-ID rejection, row-set matching, finite confidence, confidence range, JSON length caps, and row-local JSON/schema validation.

[p] No internal leaks: invalid structural submissions score `0.0`; grader messages do not expose private labels, answer rows, split internals, or scoring keys. Row-local malformed JSON or invalid row-local objects zero that entire row.

[p] Agent-code safeguards: the challenge folder has no solver pipeline, no model list fallback, and no agent-style try/except recovery path. The only `try/except` blocks are CSV/JSON input guards and smoke-test cleanup.

## Leakage And Shortcuts

[p] Feature isolation: public CSVs expose opaque hash-token IDs, transformed fixed-size video paths, 16-bin sparse state observations, and a fixed prepared clip length. They do not expose source filenames, raw IDs, raw paths, exact high-rate trajectories, row-specific file lengths, high-precision state values, or private answers. Public rows are sorted by opaque ID.

[p] No rule leaks: the participant-facing description does not disclose source title, source IDs, exact derivation thresholds, split construction details, or hidden scoring internals. It defines only the submission contract and allowed JSON schemas.

[p] Anti-regex and anti-lookup: the task cannot be solved by regex/template inversion because labels are derived from continuous real robot motion and video/state alignment. `CHALLENGE_FORM_FILL.md` explicitly bans source lookup, metadata-only solutions, rule-only templates, external hosted robotics/video APIs, and reducing the task to continuous regression only. `_analyze.py` checks raw-ID/filename leakage and duration-only shortcut strength after preparation. `_source_lookup_probe.py` passed on the full official archive after hardening with top-1/top-5 raw recovery `0.0500`/`0.1250`.

## Remaining Risks

[w] Public-source retrieval risk is not mathematically zero because the upstream videos are public. The mitigation is source-neutral participant prose, stripped raw IDs, transformed/re-encoded/compressed public videos, opaque salted IDs, explicit no-lookup enforcement, and a passing full-archive source lookup probe.

[w] The official source has no explicit gripper channel. The task intentionally uses only derivable controller-trace heads and does not ask for true gripper-open or gripper-close labels.
