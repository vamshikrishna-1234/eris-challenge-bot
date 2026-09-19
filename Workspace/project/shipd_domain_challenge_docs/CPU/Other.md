# CPU Other Challenge Examples

Scrape timestamp: 2026-07-19T00:00:00+05:30

Confirmed CPU examples in this document: 8

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Collapsed Branch Side Set Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78de7hze5fmamn558q0advph8ahk1m
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: â†‘ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Note: the full description for this earlier CPU entry was not preserved in the current local file state during a prior append.

Inspiration note: Useful because it frames CPU reasoning around recovering hidden branch structure from partial execution evidence rather than a plain label prediction.

## Receipt OCR Ledger Slot Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dctsgh2xmdv33gdcxmwp2b18amtn9
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: â†‘ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Note: the full description for this earlier CPU entry was not preserved in the current local file state during a prior append.

Inspiration note: Useful because it turns OCR cleanup into structured ledger repair: recover missing slots from noisy document evidence with a CPU-friendly tabular/text output shape.

## Art-Auction Sale Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b8thyxa8tehf2pcq7767bj58anv2j
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: â†‘ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Note: the full description for this earlier CPU entry was not preserved in the current local file state during a prior append.

Inspiration note: Useful because it frames a CPU challenge as structured event reconstruction from noisy real-world records, with outputs that resemble a sale ledger rather than a simple prediction.

## Fetal Doppler-ECG Cardiac Cycle Ledger

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76zgnnnnhcdgazrew4qwcb0x8am0z6
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: multimodal, medical
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Download Data
> Description
> Leaderboard
> (1)
> Your Submissions
> Overview
> Plain language objective: for each six-second antenatal recording segment, infer the fetal cardiac cycles that are supported by both the Doppler strip image and the synchronized physiological signals, then submit a compact clinical-style ledger for that row.
> Each public row contains two aligned inputs. The image file is a 512 x 192 Doppler ultrasound strip crop that shows the row-local velocity trace morphology. The signal_npy file is a 10 x 1536 float32 signal array sampled at 256 Hz over the same six seconds: six abdominal ECG channels, three thoracic maternal ECG channels, and one maternal respiration channel. A correct prediction identifies the fetal beat/evidence time for each cycle, the start and end of that cycle, the Doppler envelope bounds visible in the strip, whether each cycle is clinically usable or uncertain, and a row-level confidence value.
> The raw corpus behind the challenge contains roughly sixty antenatal recording sessions from about forty pregnant volunteers. The prepared challenge turns those sessions into hundreds of short row-local examples. The public view preserves the clinical morphology needed for multimodal modeling while removing direct source identifiers and simple byte-size/source-file matching cues. The original record number, source filename, subject/session identity, and exact source time are not public. The target ledger is derived from agreement and disagreement between Doppler-trace evidence and signal evidence, so ignoring either modality should leave accuracy and quality-flag headroom.
> For every test row, predict:
> ledger_json: a JSON list of cycle objects. Each object has row-local seconds t, start, and end, where t is the fetal beat/evidence time and start/end bound the cardiac cycle.
> envelope_json: a Doppler evidence envelope array with rows [x, lower_y, upper_y], all normalized to [0, 1].
> quality_json: one quality flag per predicted cycle, using usable, uncertain, or artifact.
> confidence: your calibrated probability in [0, 1] that the row-level ledger is correct.
> This is a CPU-only challenge. Solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. No GPU is required or allowed for the official run. A reasonable approach is a compact CPU pipeline: image filtering for Doppler envelopes, signal-processing features from abdominal/thoracic channels, respiration-aware artifact handling, and a structured decoder for cycle events and uncertainty.
> Train and validate only from the provided public challenge files. The private test rows are grouped so that solutions must generalize across unseen source recordings and across rows with different signal quality, respiration interference, and Doppler visibility. The task remains learnable from the training examples because the same physical relationship between Doppler strip morphology, fetal/maternal electrophysiology, and cycle timing is present in both splits; what changes is the row, record context, and artifact mix.
> Task
> Build a multimodal cardiac-cycle ledger for each unseen segment. The submitted ledger should identify row-local fetal cardiac-cycle evidence times, mark cycle start and end boundaries, attach a Doppler envelope trace, label whether each predicted cycle is usable, uncertain, or artifact-dominated, and calibrate row-level confidence. The output is intentionally structured because the useful clinical question is not only "what is the fetal heart rate?", but which cycles are supported by which sensor evidence and which cycles should be treated cautiously.
> Intended Approach
> Strong CPU-only solutions will likely combine image and signal evidence rather than solve a single subproblem. Useful ingredients include classical Doppler-strip preprocessing, ridge/envelope extraction, robust peak proposals, band-limited ECG features, multi-channel agreement checks, respiration/motion artifact features, compact tree/linear/gradient-boosted models, sequence decoding, and train-only calibration. Offline open-source libraries such as NumPy, SciPy, scikit-image, OpenCV, scikit-learn, WFDB readers, and small CPU-trained models are appropriate. Any auxiliary pretrained component must be usable fully offline within the public environment and may not depend on hosted inference or external source-row lookup.
> What Not To Do
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.
> Do not reduce the task to fetal heart-rate regression, fetal QRS detection, or a single Doppler envelope extraction.
> Do not use source-row lookup, raw record-id reconstruction, original source filenames, source start times, hidden source metadata, or source checksums to recover answers.
> Do not hardcode row ids, file ordering, file sizes, mtimes, or split-specific rules.
> Do not use external APIs, hosted LLMs, hosted vision models, or closed remote inference services.
> Do not train or infer from data outside the public challenge files except generally available offline open-source tools.
> Do not read private files, exploit the grader, or build a direct formula from hidden preparation details.
> Do not submit malformed JSON, negative times, impossible cycle boundaries, overlong arrays, or out-of-range confidence values as a format hack.
> Enforcement on invalid approaches: submissions that score by lookup, metadata reconstruction, private-file access, external hosted models, or rule-only shortcuts that ignore the multimodal ledger task may be rejected even if the CSV passes the grader.
> Evaluation
> The primary metric is Mean Robust Ledger Score. Each row receives a score in [0, 1], then the leaderboard blends the mean row score with three private worst-axis terms: cycle-count regime, respiration motion, and Doppler-envelope visibility.
> Events are matched greedily by absolute beat/evidence time error. A predicted cycle can match at most one reference cycle, and a reference cycle can match at most one predicted cycle. A match is allowed only when abs(pred_t - true_t) <= 0.08 seconds. Event precision or recall with a zero denominator is treated as 0.0.
> Per row:
> precision      = matched_events / predicted_events
> recall         = matched_events / reference_events
> event_score    = F1(precision, recall), or 0 if no events can be matched
> timing_score   = mean over matched events of max(0, 1 - abs(pred_t - true_t) / 0.08)
> boundary_score = mean over matched events of
> max(0, 1 - (abs(pred_start - true_start) + abs(pred_end - true_end)) / 0.16)
> raw_envelope_score = compare submitted and reference lower/upper envelopes at
> 64 evenly spaced x positions in [0, 1]:
> mae = mean(abs(pred_lower - true_lower) + abs(pred_upper - true_upper)) / 2
> raw_envelope_score = clip(1 - mae / 0.22, 0, 1)
> envelope_score     = event_score * raw_envelope_score
> quality_score  = mean matched-cycle flag agreement:
> exact flag match = 1.0,
> usable/uncertain confusion = 0.5,
> artifact mismatch = 0.0,
> and 0.0 if no events match
> count_score    = event_score * max(0, 1 - abs(predicted_count - reference_count) / max(1, reference_count))
> correctness = 0.40 event_score
> + 0.16 timing_score
> + 0.12 boundary_score
> + 0.17 envelope_score
> + 0.10 quality_score
> + 0.05 count_score
> confidence_factor = 1 - 0.08 * abs(confidence - correctness)
> row_score         = correctness * confidence_factor
> Final score:
> Final = 0.70 * mean(row_score)
> + 0.12 * lowest cycle-count subgroup mean
> + 0.10 * lowest respiration-motion subgroup mean
> + 0.08 * lowest Doppler-visibility subgroup mean
> The three subgroup terms are distinct. The 0.12 term is the lowest mean score across private cycle-count regimes, the 0.10 term is the lowest mean score across private respiration-motion regimes, and the 0.08 term is the lowest mean score across private Doppler-visibility regimes. These subgroup labels correspond to real prepared acquisition/quality axes, so a solution must work on difficult rows rather than only on clean strips.
> The envelope, quality, and count heads are gated by event recovery, so a row cannot score highly by submitting a plausible-looking envelope or fixed count without matching cardiac-cycle events. Confidence only modulates earned task credit and never adds standalone points to a wrong row.
> The grader returns 0.0 for structural submission errors: missing, extra, or reordered columns; duplicate ids; row-set mismatch; non-integer ids; non-finite or out-of-range confidence. Row-local malformed JSON, negative times, impossible boundaries, overlong arrays, and invalid quality flags set that row's score to 0.0 instead of leaking labels or crashing.
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0.
> Dataset
> The public data contains transformed row-local segments only. It does not expose original raw record ids, source filenames, subject/session identifiers, raw start times, split groups, private answer metadata, or compressed file-size encodings of source rows. Each row is one six-second segment. Typical prepared splits contain hundreds of rows; the exact counts are printed by prepare.py after it processes the official raw files.
> train.csv includes the input columns id, image, signal_npy, segment_duration_sec, n_signal_channels, signal_fs_hz, and prompt. It also includes the train-only labels ledger_json, envelope_json, and quality_json. test.csv has the same input columns and no label columns. sample_submission.csv is a valid weak placeholder template and should be overwritten.
> File overview
> Item	Description
> public/train/strips/*.bmp	Doppler strip crops
> public/test/strips/*.bmp	Test strip crops
> public/train/signals/*.npy	Train signal snippets
> public/test/signals/*.npy	Test signal snippets
> public/train.csv	Inputs plus labels
> public/test.csv	Inputs only
> public/sample_submission.csv	Submission template
> train.csv columns
> Column	Type	Description
> id	int	Opaque segment id with no source-row meaning
> image	string	512 x 192 BMP strip path
> signal_npy	string	10 x 1536 float32 NPY path
> segment_duration_sec	float	Segment duration in seconds
> n_signal_channels	int	Public channel count
> signal_fs_hz	float	Public sample rate in Hz
> prompt	string	Constant task text
> ledger_json	string	Train-only cycle list
> envelope_json	string	Train-only envelope
> quality_json	string	Train-only cycle flags
> test.csv columns
> Column	Type	Description
> id	int	Opaque segment id with no source-row meaning
> image	string	512 x 192 BMP strip path
> signal_npy	string	10 x 1536 float32 NPY path
> segment_duration_sec	float	Segment duration in seconds
> n_signal_channels	int	Public channel count
> signal_fs_hz	float	Public sample rate in Hz
> prompt	string	Constant task text
> signal_npy channel order
> Every public signal_npy array has shape (10, 1536). Rows are channels and columns are samples.
> Channel index	Channel name	Meaning
> 0	uni_abd1	Abdominal ECG/electrophysiology channel
> 1	uni_abd4	Abdominal ECG/electrophysiology channel
> 2	uni_abd8	Abdominal ECG/electrophysiology channel
> 3	uni_abd12	Abdominal ECG/electrophysiology channel
> 4	uni_abd16	Abdominal ECG/electrophysiology channel
> 5	uni_abd20	Abdominal ECG/electrophysiology channel
> 6	bi_tho1	Thoracic maternal ECG channel
> 7	bi_tho2	Thoracic maternal ECG channel
> 8	bi_tho3	Thoracic maternal ECG channel
> 9	matrsp	Maternal respiration channel
> The image and signal_npy paths are relative to public/. The prompt value is the same task instruction on every row and contains no hidden metadata or answer text.
> ledger_json is a JSON list of objects such as {"t": 1.24, "start": 1.02, "end": 1.48}. All times are row-local seconds inside [0, segment_duration_sec], and each object represents one predicted or reference cardiac cycle. envelope_json is a JSON list of normalized triples [x, lower_y, upper_y]; x is horizontal position across the strip, while lower_y and upper_y bound the visible Doppler evidence band. quality_json is aligned to the cycle list: usable means the cycle is supported clearly enough for clinical-style use, uncertain means the cycle has partial or conflicting image/signal evidence, and artifact means the proposed cycle is dominated by artifact or weak evidence.
> Submission
> Submit ./working/submission.csv with a header row and exactly one row per id in test.csv. The header must contain these five columns in this exact order: id, ledger_json, envelope_json, quality_json, confidence.
> Column	Type	Constraint
> id	int	Same set as test
> ledger_json	string	JSON cycle list
> envelope_json	string	JSON envelope array
> quality_json	string	JSON flag list
> confidence	float	In [0, 1]
> ledger_json must be a JSON list. Each item should be an object like {"t":1.24,"start":1.02,"end":1.48} with non-negative row-local seconds inside the segment duration. envelope_json should contain up to 96 normalized triples [x, lower_y, upper_y], where 0 <= x <= 1 and 0 <= lower_y <= upper_y <= 1. quality_json should be a JSON list of quality flags aligned to the predicted cycles.
> Example:
> id,ledger_json,envelope_json,quality_json,confidence
> 101,"[{""t"":0.52,""start"":0.31,""end"":0.73}]","[[0.0,0.42,0.58],[1.0,0.41,0.59]]","[""usable""]",0.63
> 102,"[]","[[0.0,0.45,0.55],[1.0,0.45,0.55]]","[]",0.25

Inspiration note: Useful because it combines image and physiological time-series evidence into a structured clinical ledger, which is a strong template for CPU-only multimodal reasoning challenges.

## Visual-Inertial Tracking Failure Detection and Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dnhqdk3fjw9djbvhf1bzv2189zhtt
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: image; Based on dataset: Real Headset Visual-Inertial Short Sequence Archives
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Plain language objective: look at a real headset camera-and-motion window, find where tracking went bad, and write the repair ledger an AR/VR runtime would need. An AR/VR headset must keep a stable estimate of where it is in a room even when rapid motion, texture loss, or temporary visual-inertial disagreement makes tracking unreliable.
> For each short real headset window, infer a compact failure and repair ledger: which keyframes are trustworthy, where the tracking trace drifted or was lost, which earlier anchor should be used to reconnect the path, the dominant failure state, and the row uncertainty.
> This is not a plain SLAM trajectory benchmark, continuous pose regression task, or single scene label. The public input includes real camera evidence, real inertial summaries, and a degraded partial pose trace. The output is a discrete structured audit record whose pieces must agree with one another.
> Only CPU solutions are allowed. Submissions must be reproducible within 1.5 hours on 10 CPU cores and 62 GB RAM. The intended solution is a learned visual-inertial audit model trained only on the released training rows, not a lookup against the upstream archive or a hand-coded reconstruction of hidden reference trajectories.
> What Not To Use / What Not To Do, violation may cause rejection regardless of score:
> Do not reverse-map rows to original recording names, timestamps, frame filenames, or source archive paths.
> Do not download, index, or search the upstream visual-inertial archive to recover hidden reference trajectories.
> Do not use source-row lookup, perceptual frame matching, raw image hashes, ZIP member order, file sizes, row order, salted IDs, or path strings as answer channels.
> Do not inspect private answers, grader internals, filesystem side channels, hidden platform state, or prepare-script outputs that are not in public/.
> Do not submit a metadata-only solution that ignores camera panels, IMU evidence, and degraded pose.
> Do not reduce the task to continuous pose regression or a single failure-type label; all ledger heads are required.
> Do not use GPU computation, hosted APIs, remote inference services, closed-source teacher APIs, external labels, runtime-downloaded model weights, or challenge-specific pretrained checkpoints.
> Do not exploit malformed JSON, duplicate IDs, extra columns, non-finite values, or other grader attacks.
> Enforcement on invalid approaches: solutions may be reviewed for actual use of visual and inertial evidence, source-lookup code, remote calls, hidden-answer access, and rule-only behavior. The goal is to reward learned operational tracking-audit models, not lookup tables or format exploits.
> Task
> For each test row, read the frame panel, the IMU trace, and the degraded pose trace. Submit:
> reliable_keyframes_json: keyframe indices that remain trustworthy.
> failure_spans_json: contiguous unreliable frame ranges with failure type and severity.
> anchor_edges_json: repair links from a current keyframe to an earlier anchor keyframe.
> failure_type: the dominant row state.
> uncertainty: calibrated uncertainty in the ledger.
> Keyframe indices are integers from 0 through 17. The four images in each panel are ordered top-left, top-right, bottom-left, bottom-right and correspond to keyframes 0, 5, 11, and 17. The IMU and degraded pose JSON arrays provide one object per keyframe.
> The test rows are not a lookup exercise. Related source recordings are kept out of the opposite split, and public IDs, panel filenames, paths, and row order are opaque, so useful models need to generalize from the labelled training windows to unseen headset motion and room appearances.
> Intended Approach
> A practical CPU solution is to build a compact multimodal model from train.csv. Decode the IMU and degraded-pose arrays into per-keyframe time-series features, extract visual evidence from the four panel tiles, and train models that estimate keyframe reliability, failure-span probabilities, anchor candidates, dominant failure state, and uncertainty. Reasonable visual features include local texture, edge density, blur/contrast cues, tile-to-tile differences, ORB/SIFT-style descriptors, optical-flow-like summaries, small CPU CNN features, or lightweight self-supervised embeddings computed locally.
> Another reasonable route is a two-stage ledger pipeline. First predict per-keyframe reliability and failure likelihood from image-panel, IMU, and degraded-pose evidence using random forests, gradient boosting, k-nearest-neighbor features, compact 1D sequence models, or shallow CPU neural networks. Then decode those probabilities into contiguous spans, backward anchor edges, a row-level failure type, and a calibrated uncertainty value. The submitted heads should be mutually consistent: reliable keyframes should not sit inside failure spans, anchor edges should repair or reconnect to earlier stable keyframes, and the dominant failure type should agree with the span evidence.
> Use only the released training labels for model selection. Make validation folds from train.csv that are robust to row-order and metadata shortcuts, for example by stratifying on device_family, motion_hint, failure type, and coarse visual clusters parsed from window_meta_json and the public panels. Check both the individual heads and the final ledger score on training-only validation folds. Calibrate numeric uncertainty and span severity on validation predictions so values stay in [0,1] and reflect actual ambiguity rather than acting as constants. Open-source local CV and time-series libraries, classical features, and generic offline pretrained vision features are allowed if they run under the CPU limit and do not use upstream source annotations, hidden test information, hosted APIs, or runtime downloads.
> Evaluation
> Each row receives six head scores. Higher is better.
> S_reliable = F1 over reliable keyframe sets
> S_spans    = greedy interval IoU-F1 for failure spans
> S_edges    = F1 over (current, anchor) repair edges
> S_type     = exact dominant failure state with small related-state credit
> S_uncert   = exp(-abs(pred - true) / 0.18)
> S_consist  = internal ledger consistency score
> raw = 0.22*S_reliable + 0.30*S_spans + 0.18*S_edges
> + 0.16*S_type + 0.10*S_uncert + 0.04*S_consist
> row_score = raw ** 1.55
> Span matching uses greedy one-to-one matches with interval IoU at least 0.25. Span severity contributes to matched-span credit. S_consist checks that reliable keyframes do not fall inside submitted failure spans, repair anchors point backward, and row failure type is compatible with the span list.
> The final score uses worst-group aggregation, blending mean row quality with the lowest private subgroup minimum mean:
> Final = 0.78 * mean(row_score)
> + 0.08 * worst_device_group
> + 0.08 * worst_motion_group
> + 0.06 * worst_failure_group
> The theoretical minimum is 0.0 and the theoretical maximum is 1.0. A perfect submission scores exactly 1.0. A structural submission failure returns 0.0. Malformed row-local content, invalid enums, or over-long JSON make the affected row score zero without crashing the grader.
> The grader requires exactly the submission columns in the listed order, one row per test ID, unique IDs, and the exact test ID set. uncertainty must be finite and in [0,1].
> Dataset
> The prepared data is under public/. Image paths are relative to the public/ root. The frame panels are redacted, low-fidelity visual evidence derived from short real headset-camera neighborhoods; they are not raw upstream frame copies.
> File overview:
> Item Description
> train.csv Inputs and labels
> test.csv Test inputs only
> sample_submission.csv Weak valid template
> train/panels/*.jpg Train frame panels
> test/panels/*.jpg Test frame panels
> train.csv has 328 rows. test.csv has 479 rows. Entire source recordings are held out, so no recording contributes windows to both train and test. Public IDs, panel filenames, and paths are opaque and salted.
> train.csv columns:
> Column Type Description
> id string Opaque row ID
> image string Panel image path
> imu_trace_json string IMU evidence array
> degraded_pose_json string Partial pose array
> window_meta_json string Coarse row context
> prompt string Task instruction
> reliable_keyframes_json string Train label set
> failure_spans_json string Train span labels
> anchor_edges_json string Train repair edges
> failure_type string Train row state
> uncertainty float Train uncertainty
> test.csv columns:
> Column Type Description
> id string Opaque row ID
> image string Panel image path
> imu_trace_json string IMU evidence array
> degraded_pose_json string Partial pose array
> window_meta_json string Coarse row context
> prompt string Task instruction
> The test input columns are id, image, imu_trace_json, degraded_pose_json, window_meta_json, and prompt. sample_submission.csv is a weak valid template for the required output schema.
> imu_trace_json is an array of 18 objects. Each object has k, gyro_mean, gyro_peak, acc_dev, and frame_delta. Values are finite real numbers derived from the headset sensor stream and neighboring camera frames.
> degraded_pose_json is an array of 18 objects. Each object has k and observed. If observed is true it also has x, y, z, and yaw, all in row-local coordinates. If observed is false the pose is unavailable for that keyframe.
> window_meta_json has device_family, motion_hint, keyframe_count, and panel_order. Device and motion hints are coarse anonymous context fields; they are not stable row identities and test recordings are held out.
> Train-only labels use these schemas:
> reliable_keyframes_json: JSON list of unique integers from 0 to 17.
> failure_spans_json: JSON list of up to five objects with start, end, type, and severity.
> anchor_edges_json: JSON list of up to five objects with current and anchor.
> failure_type: one of ok, drift, lost_tracking, relocalized, or uncertain.
> uncertainty: finite float in [0,1].
> Submission
> Write the final submission CSV to exactly ./working/submission.csv. It must contain exactly these six columns in this order and exactly one row for every test ID.
> Column Type Constraint
> id string Same set as test
> reliable_keyframes_json string JSON keyframe list
> failure_spans_json string JSON span list
> anchor_edges_json string JSON edge list
> failure_type string Allowed enum
> uncertainty float In [0,1]
> Example:
> id,reliable_keyframes_json,failure_spans_json,anchor_edges_json,failure_type,uncertainty
> hvit_0123456789abcdef01,"[0,4,9,14]","[{""start"":7,""end"":11,""type"":""drift"",""severity"":0.52}]","[{""current"":12,""anchor"":4}]",drift,0.47
> hvit_abcdef012345678901,"[1,6,12,17]","[]","[]",ok,0.18
> Requirements are strict: start from sample_submission.csv or write the same header yourself, preserve exactly one row per test id, keep the columns in the table order, and do not add extra columns. Duplicate IDs, missing IDs, extra IDs, reordered columns, non-finite uncertainty, or uncertainty outside [0,1] make the whole submission score 0.0. Malformed or over-long row-local JSON, invalid keyframe/span/edge ranges, invalid span types, or invalid failure_type values make the affected row score zero.

Inspiration note: Useful because it turns multimodal tracking failure analysis into a structured repair ledger, which is a rich CPU-only challenge pattern beyond simple classification or regression.

## Lightning Flash Hierarchy Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70p3hk3tm64wmqm40bhck2e58ameke
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: small-data; Based on dataset: NOAA GOES-16 GLM Level-2 Lightning Detection Hierarchies
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Your task is to recover the group-and-flash hierarchy of anonymized local lightning point sets. In plain language: decide which tiny satellite lightning detections happened together, which short-lived groups belong to the same larger flash, and which boundary detections are too ambiguous to assign with high certainty. Lightning flashes are not single points: a satellite records many tiny optical detections, nearby detections are combined into short-lived groups, and several groups can belong to the same larger flash.
> Each row is one compact case containing real optical lightning detections after source-neutral redaction. The public features preserve local relative geometry, timing, energy rank, and neighborhood density while withholding absolute time, absolute location, source-object metadata, and operational identifiers. In difficult local windows, neighboring lightning activity can overlap in space and time, so the task is not just applying a fixed distance threshold.
> This is a structured hierarchy problem, not one independent class prediction per detection. The output is a JSON hierarchy: detection-to-group partition, group-to-flash partition, optional boundary/ambiguous detections, and a confidence value.
> Every solution must run on CPU. The execution environment provides 10 CPU cores and 62 GB RAM, with a maximum runtime of 1.5 hours. GPU/CUDA libraries and large pretrained models are neither required nor permitted as dependencies.
> Task
> For each test case, infer the hidden two-level hierarchy from the public point-set evidence:
> assign every detection id in the case to exactly one predicted group;
> assign every predicted group to exactly one predicted flash;
> mark detections whose membership is genuinely ambiguous under the redacted local evidence;
> report a confidence value estimating your row-level structural quality.
> Your group and flash names are local aliases. They do not need to match training aliases or hidden native labels. The grader compares the implied partitions, not the literal strings.
> Generalization Contract
> Train and test cases come from disjoint source windows, so related lightning activity is not split between public training rows and private scoring rows. Public ids are opaque, rows are sorted by opaque id, and the test set does not provide source-window labels or operational sequence context.
> A successful solution should learn reusable local hierarchy cues: how relative time, local geometry, energy rank, and point density interact when groups merge into flashes or when neighboring flashes overlap. It should not rely on knowing where or when the original satellite observations occurred.
> Intended Approach And Allowed Methods
> Strong CPU solutions can train compact models directly on the provided train.csv cases. Reasonable approaches include:
> pairwise same-group and same-flash classifiers over detection pairs, followed by a consistency-aware clustering or graph-partition decoder;
> permutation-invariant point-set models such as Deep Sets, Set Transformer-style blocks small enough for CPU, or message-passing networks over k-nearest-neighbor graphs built from the public features;
> multi-head training that predicts group affinity, flash affinity, boundary ambiguity, and confidence/calibration from training labels only;
> train-only validation splits by case or source-neutral case properties to tune thresholds, clustering regularization, and confidence calibration;
> deterministic post-processing that repairs invalid partitions, as long as the learned point-set evidence remains the primary signal.
> Simple geometric clustering, DBSCAN-like rules, or operational-threshold surrogates may be useful as diagnostic baselines, but they are not sufficient as the primary intended solution. The challenge rewards learned hierarchy induction under redaction and overlap, not reconstruction of a known operational algorithm.
> Allowed tooling is ordinary offline CPU machine learning on the released public files: NumPy, pandas, scikit-learn, PyTorch/JAX/TensorFlow CPU builds, LightGBM/XGBoost, custom clustering decoders, and similar open-source local libraries. External raw-source lookup, private files, hosted closed-source APIs, and GPU-only dependencies are out of scope.
> What Not To Use
> Do not use source-object or archive lookup, reconstructed absolute time/location, native clustering identifiers, filename or scan matching, external operational neighbors, private files, answer dictionaries, hard-coded public ids, or native hierarchy traversal.
> Do not use row order, opaque-id hashes, CSV/JSON byte length, filesystem metadata, or other non-physical metadata as a substitute for point-set inference.
> Do not use published fixed clustering thresholds, DBSCAN-only or rule-only pipelines, TF-IDF, n-grams, regex-only logic, metadata-only priors, hosted closed-source APIs, GPU-only methods, or grader/platform exploitation as the primary solution.
> Enforcement on Invalid Approaches: a submission may be rejected before payout if it is built around prohibited lookup, private-data access, platform exploitation, hard-coded ids, native graph traversal, or a rule-only shortcut that bypasses the intended public point-set inference, even if it obtains a leaderboard score.
> Evaluation
> The metric is label-invariant. For a hierarchy, let P_group be the set of unordered detection pairs placed in the same group and let P_flash be the set of unordered detection pairs placed in the same flash. For a predicted count n_pred and true count n_true, define C(n_pred,n_true) = min(n_pred,n_true) / max(n_pred,n_true). Define:
> S_group: pair F1 between predicted and true P_group, multiplied by C(predicted group count,true group count);
> S_flash: pair F1 between predicted and true P_flash, multiplied by C(predicted flash count,true flash count);
> S_uncertain: set F1 for uncertain_detections;
> S_exact: 1 only when both partitions and the uncertainty set are completely correct, up to arbitrary group/flash aliases, and 0 otherwise.
> When both compared pair sets are empty, their F1 is 1. The uncalibrated structural quality used as the confidence target is
> Q = (0.55*S_group + 0.10*S_flash + 0.15*S_uncertain + 0.15*S_exact) / 0.95.
> This Q value is normalized to [0,1] only so confidence has a comparable target. Calibration is S_cal = 1 - abs(confidence - Q). The final row score then uses the raw structural credit plus the calibration term:
> 0.55*S_group + 0.10*S_flash + 0.15*S_uncertain + 0.15*S_exact + 0.05*S_cal.
> The final score is the mean row score. Higher is better; the theoretical minimum is 0.0 and maximum is 1.0. A perfect hierarchy with confidence 1.0 scores exactly 1.0.
> Submission-level schema failures receive score 0.0: missing, extra, or reordered columns; missing, extra, or duplicate ids; non-string/empty ids; row-set mismatch; and non-finite or out-of-range confidence. prediction_json is limited to 200,000 characters. Malformed or structurally invalid JSON affects that row only and scores zero rather than crashing the grader or exposing private information.
> Dataset
> The public dataset contains 210 labeled training cases and 140 unlabeled test cases. Related source windows are never split across train and test. Rows and embedded detections are sorted by opaque ids. Public data contains no native filenames, absolute timestamps, coordinates, scan identifiers, event/group/flash identifiers, or source-window labels.
> Item Description
> train.csv Labeled public cases
> test.csv Public cases without labels
> sample_submission.csv Valid weak structured submission
> In prose: train.csv contains the public input for each training case plus its hidden hierarchy label; test.csv contains the same public input columns but no label column; sample_submission.csv shows the exact required output columns and a weak valid JSON structure.
> train.csv columns
> Column Type Description
> id string Opaque case id
> case_json JSON string Case id and detection point set
> prompt string Row instruction
> target_json JSON string Training hierarchy and ambiguity labels
> The train.csv columns are: id, an opaque case identifier; case_json, a JSON string containing the local detection point set; prompt, the row-specific instruction text; and target_json, the training-only hierarchy label with groups, flashes, and uncertain detections.
> test.csv columns
> Column Type Description
> id string Opaque case id
> case_json JSON string Case id and detection point set
> prompt string Row instruction
> The test.csv columns are: id, an opaque case identifier; case_json, a JSON string containing the local detection point set; and prompt, the row-specific instruction text. There is no target_json column in test.csv.
> Each case_json has a case_id matching the CSV id and a detections list. Each detection contains:
> Field Type Meaning
> id string Opaque detection id
> x_rel float Local horizontal coordinate
> y_rel float Local vertical coordinate
> t_rel float Normalized relative timing coordinate
> energy_norm float Within-case normalized optical-energy rank
> local_density float Local neighbor fraction
> temporal_density float Temporal neighbor fraction
> The detection-level fields inside case_json are: id for the opaque detection id, x_rel and y_rel for local normalized geometry, t_rel for normalized relative timing, energy_norm for within-case optical-energy rank, local_density for nearby spatial crowding, and temporal_density for nearby temporal crowding.
> target_json and submitted prediction_json use the same exact structure:
> {
> "groups": [
> {"group_id": "g1", "detections": ["d01", "d02"]},
> {"group_id": "g2", "detections": ["d03"]}
> ],
> "flashes": [
> {"flash_id": "f1", "groups": ["g1", "g2"]}
> ],
> "uncertain_detections": ["d03"]
> }
> Every detection must occur in exactly one non-empty group. Group ids must be unique. Every group must occur in exactly one non-empty flash, and flash ids must be unique. uncertain_detections must contain unique detection ids from the case; an empty list is valid. Alias strings may differ from the training aliases.
> In test.csv, id, case_json, and prompt are the complete public input columns; no label column is present.
> Submission
> Submit one CSV at ./working/submission.csv with exactly these columns in exactly this order: id, prediction_json, confidence.
> Column Type Constraint
> id string Must exactly match the test id set
> prediction_json JSON string Complete valid hierarchy for the case
> confidence float Estimate of Q in [0,1]
> Example:
> id,prediction_json,confidence
> case_a1b2c3,"{""groups"":[{""group_id"":""g1"",""detections"":[""d01"",""d02""]},{""group_id"":""g2"",""detections"":[""d03""]}],""flashes"":[{""flash_id"":""f1"",""groups"":[""g1"",""g2""]}],""uncertain_detections"":[""d03""]}",0.64
> case_d4e5f6,"{""groups"":[{""group_id"":""g1"",""detections"":[""d01""]},{""group_id"":""g2"",""detections"":[""d02"",""d03""]}],""flashes"":[{""flash_id"":""f1"",""groups"":[""g1""]},{""flash_id"":""f2"",""groups"":[""g2""]}],""uncertain_detections"":[]}",0.41

Inspiration note: Useful because it turns real point-set hierarchy recovery into a structured JSON-output challenge, which is a strong CPU pattern for event grouping and uncertainty reasoning.

## Counting Overlapping Stamps From Their Merged Silhouette

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74321zstf4fa1s5khknqtpq18a9ayj
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Easy
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↓ Lower is better
- Tags: image
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Blind Recovery Of A Latent Stamp Dictionary From Boolean Superpositions
> Overview
> Each item is a 24 by 24 binary grid that is the Boolean OR-superposition of many translated copies of atoms
> drawn from a small, fixed dictionary of ten binary shapes. The dictionary is LATENT: it is never given to you.
> For each grid you must recover the usage census of the generative process, that is, how many times each of the
> ten latent atoms was stamped onto the canvas. Because you are not told what the atoms look like, you must
> recover the dictionary itself from supervision (the training grids paired with their usage vectors) and, at the
> same time, learn to invert a lossy Boolean mixing process in which overlapping atoms erase one another's
> evidence.
> This is a blind de-superposition problem, not a template-counting exercise. Two properties make it genuinely
> hard. First, the dictionary is unknown, so the task couples dictionary learning with amortized inference of the
> latent usage. Second, the mixing is Boolean OR and every atom has the same number of active cells, so the total
> number of active pixels carries no information about the mix, and heavily overlapped stamps become
> information-theoretically unrecoverable. Exact recovery is therefore impossible, and even an ideal method is
> capped well short of a perfect score.
> Background And Suggested Approach
> This challenge adapts several research directions to a controlled, fully synthetic setting; strong entries are
> expected to draw on them rather than fit a generic regressor to raw pixels.
> Convolutional dictionary learning / convolutional sparse coding: the forward model is a sum (under OR) of
> translated dictionary atoms, so recovering the atoms is a convolutional dictionary-learning problem
> (Bristow, Eriksson and Lucey 2013; Wohlberg 2016).
> Boolean matrix and tensor factorization: because the mixing is OR rather than addition, the inverse is a
> Boolean factorization rather than a linear one (Miettinen et al. 2008).
> Algorithm unrolling / deep unfolding: an effective decoder can be built by unrolling an iterative sparse
> recovery procedure into a trainable network (Gregor and LeCun 2010, LISTA; Monga, Li and Eldar 2021).
> Amortized and simulation-based inference: the generator is a simulator with a known structure and a hidden
> seed, so learning to map an observed grid to the posterior over latent usage is an amortized inference
> problem (Cranmer, Brehmer and Louppe 2020).
> Superimposed codes / group testing: the Boolean OR forward model is the classical superimposed-code setting,
> which motivates why multiplicity recovery under OR is hard (Kautz and Singleton 1964).
> Empirically, a naive pixel regressor barely improves on the constant-mean baseline (normalized error about
> 0.93), whereas a method that explicitly recovers the latent atoms and reasons about OR occlusion reaches
> substantially lower error. The gap between the two is the point of the challenge.
> Data
> Files provided:
> train.csv is the training table, one row per grid, with a grid column and ten target columns type_0 through
> type_9. The grid column is a run-length encoding of the 24 by 24 binary grid, flattened in row-major order, as
> a space-separated sequence of value-count pairs (for example "0 40 1 3 0 12 ..."; the run lengths sum to 576).
> Each type_j column is the integer number of times latent atom j was stamped into that grid.
> test.csv has an integer id column and the grid column, and no target columns. Predict the ten usage counts for
> each id.
> sample_submission.csv shows the exact required output with a trivial constant baseline you should replace.
> The latent dictionary is NOT included. The ten type indices refer to ten fixed latent atoms defined by the
> hidden generative process, and are consistent across all rows, so their appearance can be learned from the
> labeled training superpositions. What is public about the process: there are exactly ten latent atoms, each a 6
> by 6 binary pattern with exactly 14 active cells; each stamp is a translation of one atom placed fully inside
> the 24 by 24 canvas; and all stamps are combined by pixel-wise OR.
> An example training row (header then values, grid abbreviated):
> grid,type_0,type_1,type_2,type_3,type_4,type_5,type_6,type_7,type_8,type_9
> 0 40 1 2 0 9 1 3 0 519,3,1,0,4,2,1,0,2,3,1
> Submission Format
> Submit a CSV named submission.csv with exactly eleven columns: id (every id in test.csv, one row each, no
> duplicates) and type_0 through type_9, each a finite number (continuous predictions are allowed). Example:
> id,type_0,type_1,type_2,type_3,type_4,type_5,type_6,type_7,type_8,type_9
> 0,2.9,1.1,0.2,3.8,2.0,0.7,0.1,1.9,3.1,1.0
> A submission is rejected (it does not score) if it does not have exactly those eleven columns, is missing any
> id, has an extra or duplicate id, or has any non-finite value.
> Evaluation Metric
> Submissions are scored by the total absolute error over all ten usage counts, normalized by the per-type mean
> baseline error:
> score
> =
> sum over i,j of |y_hat_ij - y_ij|
> /
> sum over i,j of |y_ij - y_bar_j|
> where y_ij is the true usage of atom j in item i, y-hat the prediction, and y-bar_j the mean of atom j over the
> test items. The score is in [0, +infinity), lower is better (min 0, max +infinity). A score of 1.0 equals
> predicting the constant per-type mean; below 1.0 beats it; 0.0 is a perfect recovery and is not reachable in
> practice.
> Runnable reference scorer (exactly how submissions are graded):
> import numpy as np, pandas as pd
> TCOLS = ["type_%d" % j for j in range(10)]
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> if not isinstance(submission, pd.DataFrame): raise ValueError("not a dataframe")
> cols = [str(c) for c in submission.columns]
> if len(cols) != 11 or sorted(cols) != sorted(["id"] + TCOLS): raise ValueError("cols")
> s = submission.copy(); s.columns = cols; a = answers.copy()
> a["id"] = a["id"].astype(str).str.strip(); s["id"] = s["id"].astype(str).str.strip()
> if s["id"].duplicated().any(): raise ValueError("dup id")
> if len(s) != len(a) or set(s["id"]) != set(a["id"]): raise ValueError("ids")
> order = {i: k for k, i in enumerate(a["id"])}
> s = s.sort_values("id", key=lambda c: c.map(order))
> yt = a[TCOLS].to_numpy(float); yp = pd.to_numeric(s[TCOLS].stack(), errors="coerce").to_numpy(float).reshape(len(s), 10)
> if not (np.isfinite(yt).all() and np.isfinite(yp).all()): raise ValueError("non-finite")
> base = float(np.abs(yt - yt.mean(0, keepdims=True)).sum()) or 1.0
> return float(np.abs(yp - yt).sum() / base)
> Baselines
> Predicting the constant per-type mean scores about 1.0. A naive regressor on raw pixels barely beats it (about
> 0.93), because with a latent dictionary and equal-area atoms the raw pixels are weakly informative. A method
> that recovers the latent atoms and inverts the Boolean mixing reaches substantially lower normalized error but
> plateaus above zero, because overlap destroys usage information. A perfect score of 0 is not reachable.
> Allowed And Prohibited
> Allowed: any model or training strategy; learning the latent dictionary from the training data; unrolled or
> amortized inference; convolutional or set-based decoders; training only on the provided train.csv.
> Prohibited: nothing external is needed or permitted; the usage census must be produced by your method from
> the provided grid. Submissions and code are reviewed.
> Hardware And Compute
> CPU only, no GPU. Each grid is 576 bits and the latent dictionary has only ten small atoms; a compact
> convolutional or unrolled model trains in minutes on a CPU and inference is a single cheap pass. Grading is a
> CSV comparison.

Inspiration note: Useful because it frames dictionary learning and de-superposition as a CPU-only structured recovery task, with a clean count-vector output and a principled lower-is-better metric.

## Waggle-Dance Communication Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ce2ce8e1bdfw5b90a7e3d898as8nv
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Download Data
> Description
> Leaderboard
> (3)
> Your Submissions
> Overview
> Plain language objective: recover who communicated with whom during a short honey-bee waggle-dance episode.
> Each row is a short observation-hive episode containing many anonymized bees moving at once. The public input is a compressed trajectory file with relative public-clock time, local bee index, privacy-transformed x/y position, body orientation, tracking confidence, and local crowding summaries. The hidden record says which local bee was the dancer, when the waggle intervals occurred, which nearby bees were genuine followers versus attendees, and which directed dancer-to-follower communication edges were present.
> This is a real animal-behavior reconstruction problem. A waggle dance is a brief communication signal embedded in dense social traffic: the dancer changes motion rhythm and heading, potential receivers track or inspect it for only part of the episode, and many nearby bees are incidental passersby. Useful predictions must recover the communication record from trajectory evidence rather than assign a single frame label.
> This is not a single behavior label and not coordinate-value prediction. A valid answer is a structured communication record: dancer identity, ordered temporal intervals, participant roles, directed graph edges, and row confidence.
> You must submit these five prediction fields for every test episode:
> dancer_id: one local bee ID such as B17.
> waggle_intervals_json: ordered interval objects.
> roles_json: follower or attendee roles.
> edges_json: directed dancer-to-follower edges.
> confidence: numeric row confidence in [0,1].
> Only CPU solutions are allowed. The solution runtime limit is 1.5 hours on 10 CPU cores and 62 GB RAM. Runtime internet use, source-data lookup, hidden-answer access, external hosted animal-tracking APIs, and private annotation lookup are not allowed.
> Task
> For each test row, load the referenced episode NPZ and output one communication record. Identify the local dancer, segment the ordered waggle intervals on the public episode clock, separate true followers from attendees or passersby, and report the directed dancer-to-follower edges. The role and edge heads should be consistent with the dancer and intervals you predict: a row that names a follower should have trajectory evidence that this local bee attended the dancer during the waggle portion of the episode, not merely that it was nearby once.
> The held-out rows are designed to test generalization across recording conditions, crowding, tracking quality, local bee identities, and dance structure. Public row IDs, file paths, row order, local bee IDs, and public-clock values are not source keys. A strong solution should learn reusable movement and interaction patterns from the labeled training episodes.
> Intended Approach
> A practical CPU solution is to featurize the dense per-bee time series from the NPZ files, score dancer candidates from oscillatory motion, orientation changes, and repeated waggle-like bursts, then decode a compact set of temporal intervals. Follower and attendee candidates can be modeled from distance, relative orientation, motion synchrony, dwell time near the dancer, and before/during/after interval context. After those heads are predicted, construct edges from the predicted dancer to the follower candidates and postprocess the JSON so intervals, roles, and edges remain row-local and internally consistent.
> Reasonable CPU methods include gradient-boosted trees or random forests over hand-built trajectory features, dynamic programming or HMM/CRF-style interval decoding, k-nearest or metric features for bee-pair interactions, and compact temporal neural models that run fully on CPU. Use only the released training labels for model selection. Build train-only validation folds that check crowding, tracking-confidence, comb-side, duration, and waggle-count behavior; calibrate the confidence column on those folds; and validate the exact submission format before scoring.
> What Not To Use / What Not To Do:
> Do not look up original source files, dates, timestamps, raw bee IDs, frame IDs, track IDs, feeder IDs, or source annotations for hidden rows.
> Do not use runtime internet access or external copies of the raw source to identify test episodes.
> Do not use private files, hidden answers, row order, opaque-ID hashes, file sizes, filesystem metadata, or JSON length as answer channels.
> Do not submit a metadata-only, fixed-template, or rule-only solution that ignores the trajectory arrays.
> Do not reduce the task to one bee label, one interval count, or full continuous-coordinate prediction.
> Do not use closed-source teacher APIs, hosted tracking APIs, or external biological-behavior services for hidden-row interpretation.
> Do not exploit malformed JSON floods, duplicate IDs, extra columns, non-finite numbers, or grader/platform side channels.
> Enforcement on invalid approaches: submissions may be reviewed for source lookup, runtime network use, hidden-file access, metadata-only behavior, and solutions that avoid the structured graph-recovery contract. Prohibited approaches can be rejected before payout even if the CSV is structurally valid.
> Dataset
> The public prepared data contains labeled training episodes, hidden-label test episodes, and a sample submission. Episode files are compressed NumPy .npz files referenced from the CSVs. Public IDs are opaque and sorted; local bee IDs are remapped independently within each episode.
> Prepared files:
> Each episode NPZ contains these arrays with equal length:
> t_sec: relative seconds in the public episode clock.
> bee_index: local integer bee index; 17 corresponds to B17.
> x_mm, y_mm: transformed relative hive-plane coordinates.
> orientation_rad: body orientation in radians after the same episode transform.
> tracking_confidence: tracker confidence in [0,1].
> neighbor_count_20mm, neighbor_count_40mm: local crowding summaries.
> dense_features: bee-by-frame tensor with x, y, orientation, confidence, 20 mm count, and 40 mm count.
> dense_mask: 1 where the dense tensor has an observed detection.
> dense_frame_hz: dense tensor frame rate, always 6.0.
> train.csv contains the public input columns plus train-only target columns.
> Plain train column definitions: id is the opaque episode key; episode_npz points to the trajectory NPZ; duration_sec is the public-clock episode length; bee_count is the local bee count; comb_side is the anonymized side label; crowding_level is a coarse local-density bucket; tracking_confidence_level is a coarse trajectory-quality bucket; dancer_id, waggle_intervals_json, roles_json, and edges_json are train-only targets; label_quality is a train-only reliability weight.
> test.csv has the same public input columns and none of the target columns.
> Plain test column definitions: id is the opaque episode key; episode_npz points to the trajectory NPZ; duration_sec is the public-clock episode length; bee_count is the local bee count; comb_side is the anonymized side label; crowding_level is a coarse local-density bucket; tracking_confidence_level is a coarse trajectory-quality bucket.
> Target JSON schemas:
> waggle_intervals_json is a list of objects with exactly start and end, measured in relative seconds.
> roles_json is a list of objects with exactly bee_id and role. Role is follower or attendee.
> edges_json is a list of objects with exactly source and target, where the source should be the predicted dancer and the target should be a follower.
> Local bee IDs use the format B00, B01, ... up to the episode bee count minus one. Intervals must satisfy 0 <= start <= end <= duration_sec.
> Submission
> Write the final CSV to ./working/submission.csv. It must contain exactly these columns in this order and exactly one row for every test ID.
> Example:
> id,dancer_id,waggle_intervals_json,roles_json,edges_json,confidence
> wdg_0123456789abcd,B17,"[{""start"":2.15,""end"":2.82},{""start"":6.31,""end"":7.04}]","[{""bee_id"":""B04"",""role"":""follower""},{""bee_id"":""B12"",""role"":""attendee""}]","[{""source"":""B17"",""target"":""B04""}]",0.42
> wdg_fedcba98765432,B03,"[{""start"":1.4,""end"":2.1}]","[{""bee_id"":""B08"",""role"":""follower""}]","[{""source"":""B03"",""target"":""B08""}]",0.31
> Wrong columns, reordered columns, missing IDs, extra IDs, duplicate IDs, nonnumeric confidence, non-finite confidence, or confidence outside [0,1] make the submission score 0.0. Malformed row-local JSON, overlong JSON cells, invalid local bee IDs, invalid intervals, duplicate role IDs, or invalid edges give zero for the affected row rather than crashing the whole submission.
> Evaluation
> Minimum score: 0.0. Maximum score: 1.0. Higher is better. A perfect submission with confidence = 1.0 scores exactly 1.0.
> Each row receives component scores:
> D = 1 if dancer_id is exact, else 0
> I = greedy soft-F1 over waggle intervals
> R = role F1 over follower/attendee objects
> E = directed edge F1
> K = graph consistency and joint credit
> core = 0.18*D + 0.30*I + 0.22*R + 0.20*E + 0.10*K
> powered = core ** 0.80
> calibration = max(0, 1 - abs(confidence - powered))
> count_score = geometric mean over interval, role, and edge count precision
> count_penalty = 0.35 + 0.65*count_score
> row_score = powered * (0.86 + 0.14*calibration) * count_penalty
> Interval matching uses greedy one-to-one matching. A predicted and true interval can match only if interval IoU is at least 0.18; the pair score combines IoU with center and length timing error. Role scoring rewards exact role recovery, participant identification, and follower identification. Edge scoring rewards exact directed dancer-to-follower edges and follower targets. The consistency term rewards edges whose source is the predicted dancer and whose targets are predicted followers, with extra joint credit when dancer, interval, role, and edge evidence agree.
> The count precision term penalizes overbroad records that flood a row with too many intervals, roles, or edges. For each of the interval, role, and edge heads, the count ratio is min(1, (true_count + slack) / max(true_count + slack, predicted_count + slack)), with slack 2 for intervals, 2 for roles, and 1 for edges. count_score is the geometric mean of those three ratios. Underprediction is already handled by F1; this term mainly prevents valid-but-spammy submissions from receiving excessive recall credit.
> The final score combines mean row performance with hidden worst-group robustness:
> Final = 0.78 * mean(row_score)
> + 0.22 * mean(worst_group_scores)
> Hidden groups cover crowding level, tracking-confidence level, dance duration, waggle-count bucket, comb side, and recording-session bucket. The grouping terms reward methods that work across sparse/crowded scenes, lower/higher tracking confidence, short/long dances, and both comb sides.

Inspiration note: Useful because it turns multi-agent trajectory data into a structured communication graph recovery task with dancer identity, temporal segments, roles, edges, and calibrated confidence all tied together.

## Collapsed Branch Side Set Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78de7hze5fmamn558q0advph8ahk1m
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each row represents a small local neighborhood from an evolutionary tree. The original tree connected several endpoint taxa through internal branches. In the released example, one internal branch has been hidden and replaced by the placeholder node X. The endpoint names are anonymized as row-local tokens such as u03 or u11, but the row still provides partial relationship evidence between endpoints: integer hop counts and optional within-row branch-length ranks.
> Your task is to recover the exact set of endpoint tokens that lie on the same side of the hidden branch as anchor_taxon. In other words, if the hidden branch were restored, which visible endpoints would be grouped with the anchor before crossing that branch? A prediction is a variable-length set of row-local endpoint tokens, not a class label or scalar value. The token vocabulary is independently reassigned in every row, and evaluation rows come from held-out source groups, so solvers must infer the local branching pattern rather than reuse token identities.
> Dataset
> train.csv: 3,442 rows with inputs and answer_json.
> test.csv: 1,758 rows with inputs only.
> sample_submission.csv: 1,758 deterministic schema-only predictions in submission format. Each row contains the anchor and one pseudo-random incident endpoint; it is not a model or evidence-based baseline.
> train.csv has five columns; test.csv has the same first four columns:
> id (string): Globally shuffled opaque row identifier.
> collapsed_context_json (JSON object encoded as a string): Contains collapsed_node (string, always X), incident_taxa (array of 6 to 16 row-local endpoint-token strings), and observed_pair_count (integer).
> anchor_taxon (string): Endpoint token that must be included in the submitted side.
> distance_evidence_json (JSON array encoded as a string): Sparse local relationship evidence. Each object contains a and b (endpoint-token strings), hops (integer number of edges between them in the original local tree), and length_rank (integer 0 through 7 or JSON null). Ranks preserve only within-row ordering of branch lengths when that information exists; null means the clue carries hop structure only.
> answer_json (train only; JSON object encoded as a string): Ground-truth object with exactly one key, side, whose value is the anchored child-side list.
> Every endpoint token occurs in at least one observed pair. The target side always contains anchor_taxon, has at least two tokens, and has no more than half of the incident tokens.
> Submission Format
> Submit a CSV with exactly these two columns, in either column order:
> id: Every test id exactly once.
> answer_json: A JSON object with exactly the key side.
> side must be a nonempty list of unique endpoint-token strings from that row. It must contain anchor_taxon and must omit at least one incident endpoint token. No other JSON keys are allowed.
> A complete valid two-row CSV example is:
> id,answer_json
> clade_d23a9881c7b8de10b8,"{""side"":[""u06"",""u03""]}"
> clade_d4eec008e521559582,"{""side"":[""u04"",""u02""]}"
> The full submission must contain all 1,758 test ids, not only the two example rows.
> Evaluation
> For row i, let P_i be the submitted endpoint-token set and T_i the true anchored side set. The row score is exact side-set accuracy: it is 1 when P_i = T_i and 0 otherwise.
> The final score is the unweighted arithmetic mean across all N = 1,758 test rows:
> score = (1 / N) * sum_i 1[P_i = T_i].
> The score is bounded by 0 and 1 and is maximized. Partial overlap does not receive credit because the target is one exact branch-side set, not an independent per-token tagging task. Submission row order does not matter because rows are aligned by id.
> Expected Methods
> Suitable CPU methods include row-local graph feature extraction, constrained set search, path-consistency scoring, rank-aware clustering, lightweight message passing implemented with installed libraries, and compact models trained only on the supplied training rows. Models should exploit the interaction between hop clues, rank clues, the anchor token, and missing-edge geometry rather than memorizing token identities.
> What Not To Use
> GPU or accelerator computation of any kind.
> Hosted APIs, remote inference services, or network access during solution execution.
> External datasets, source archives, endpoint-name databases, or extra training data.
> Challenge-specific pretrained or fine-tuned checkpoints presented as general pretrained assets.
> Reverse lookup of rows, source-paper matching, original endpoint-name recovery, or source-record retrieval.
> Hardcoded answers, test-id rules, manual per-row answer tables, or reconstruction from leaked identifiers.
> Solutions must be reproducible on CPU using only the provided files and libraries already installed in the runtime.

Inspiration note: Useful because it turns collapsed tree/branch structure recovery into a CPU-friendly set prediction task, with engineered structural signals and a compact set-valued output shape.

## Receipt OCR Ledger Slot Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dctsgh2xmdv33gdcxmwp2b18amtn9
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Real receipt-processing systems often produce a nearly usable record, but some fields are missing, assigned to the wrong type, attached to the wrong OCR tokens, or grouped into the wrong line item. This challenge asks you to repair those records from real receipt artifacts: a receipt page image, OCR word boxes, OCR line candidates, and a noisy candidate ledger.
> In plain language: look at the receipt evidence, fix the broken ledger slots, and submit the corrected structured record.
> Each row is one receipt. You receive the page image, a row-local OCR/layout JSON file, and a candidate record with slot-level hints. For every slot, submit the corrected field type, normalized value, evidence token ids, line-item group id, missing flag, and row confidence.
> This is not ordinary OCR, receipt total extraction, or a table-only parsing task. The hard part is making the repaired value, field type, evidence tokens, and row grouping agree with one another when the candidate ledger is partly wrong.
> This is a CPU-only challenge. Solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. The intended approaches are lightweight document-understanding pipelines: OCR-token featurization, layout graphs, constrained decoding, classical sequence/row models, compact CPU text models, or small local models trained on the public examples. The task does not require GPU LayoutLM, Donut, large VLM fine-tuning, or external OCR.
> What Not To Use (any of these can cause solution rejection regardless of leaderboard score):
> Original source filename, split, image id, row id, or annotation id lookup.
> Loading upstream annotation files to answer hidden test rows.
> Source-row matching by image hashes, OCR text search, or raw file size.
> Slot-id, slot-order, row-order, or file-order shortcuts instead of document evidence.
> Hidden/private answer access, prepare-script introspection, or grader probing.
> External OCR, cloud document AI, hosted VLM, or commercial extraction APIs.
> Metadata-only submissions that ignore the receipt image and OCR/layout evidence.
> Rule-only template decoding, regex-only parsing, or direct lookup tables.
> GPU-only methods or large-model fine-tuning that violates the CPU budget.
> Enforcement on invalid approaches: solutions that do not solve the intended receipt-understanding task may be rejected before payout. The goal is to reward learned evidence repair from real page artifacts, not source lookup, metadata shortcuts, or template inversion.
> Intended Approach
> A strong CPU-only solution should treat each receipt as a small layout-and-text reasoning problem. Reasonable approaches include matching candidate slots to OCR tokens, using token text and bounding-box geometry to classify field types, learning row/group consistency from the public training examples, and applying constrained decoding so repaired values, evidence tokens, missing flags, and line-item groups agree with one another. Lightweight local models or classical ML over OCR/layout features are appropriate; expensive OCR-free vision-language fine-tuning is not required.
> Evaluation
> Submit one JSON repair object per test row. The grader compares each submitted slot against the hidden repaired evidence ledger. A malformed or over-long repair_json cell scores zero for that row without crashing the grader. Structural submission errors score 0.0 for the whole file.
> For each slot, the grader checks:
> exact field-category match;
> normalized value match;
> OCR-token evidence F1;
> exact line-item group id;
> exact missing flag.
> The row score rewards coupled consistency:
> slot_score     = weighted slot accuracy
> group_pair_f1  = F1 over same-group slot pairs
> joint_evidence = evidence credit gated by correct type/value/group/missing
> row_exact      = 1 if the full row ledger is exact, else 0
> head_score     = 0.45*slot_score
> + 0.15*group_pair_f1
> + 0.18*joint_evidence
> + 0.20*row_exact
> calibration    = 1 - abs(confidence - head_score/0.98)
> row_score      = head_score + 0.02*calibration
> The final score blends average performance with hidden robustness checks over real receipt-source and layout buckets:
> Final = 0.72 * mean(row_score)
> + 0.10 * worst source-split bucket
> + 0.10 * worst line-density bucket
> + 0.08 * worst layout-shape bucket
> Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. Perfect labels with confidence 1.0 score exactly 1.0.
> The grader returns 0.0 if the submission columns are missing, extra, or reordered; if ids are missing, duplicated, or do not match test.csv; or if confidence is non-finite or outside [0,1]. Invalid slot labels, invalid token ids, duplicate slot ids, and malformed row-local JSON make the affected row score zero.
> Dataset
> The prepared data is under public/. Image and OCR paths are relative to the public/ root.
> File overview
> Item	Description
> train.csv	Inputs + labels
> test.csv	Inputs only
> train/images/	Train images
> test/images/	Test images
> train/ocr/	Train OCR JSON
> test/ocr/	Test OCR JSON
> sample_submission.csv	Weak template
> train.csv columns
> id is an opaque public row id. image_path points to a receipt page image. ocr_path points to row-local OCR/layout JSON. candidate_json is a noisy candidate ledger. prompt is the task instruction. repair_json is the train-only target repair ledger.
> Column	Type	Description
> id	int	Public row id
> image_path	string	Image path
> ocr_path	string	OCR JSON path
> candidate_json	string	Noisy ledger
> prompt	string	Instruction
> repair_json	string	Train label
> test.csv columns
> id is an opaque public row id. image_path points to a receipt page image. ocr_path points to row-local OCR/layout JSON. candidate_json is a noisy candidate ledger. prompt is the task instruction.
> Column	Type	Description
> id	int	Public row id
> image_path	string	Image path
> ocr_path	string	OCR JSON path
> candidate_json	string	Noisy ledger
> prompt	string	Instruction
> OCR JSON schema
> Each OCR file is a JSON object with version, image_size, tokens, and lines. A token has tid, text, and normalized bbox as [x0,y0,x1,y1]. A line has line_id, text, token_ids, and normalized bbox.
> candidate_json schema
> candidate_json is a JSON object with version, allowed_categories, and slots. Each slot has slot_id, category_hint, value_hint, token_ids_hint, group_hint, and missing_hint. Hints are noisy and incomplete; they are not guaranteed to be correct. Slot ids are opaque and row-local, and slot order does not encode field type or group.
> Allowed output categories are neutral receipt field labels such as item.name, item.qty, item.price, subtotal.amount, tax.amount, total.amount, cash.amount, change.amount, plus UNKNOWN when used by a weak baseline. Use the training labels to learn the exact category set and output grammar.
> repair_json schema
> repair_json is a JSON object with a fields list. Each field object must contain:
> slot_id: opaque row-local slot id such as s8c12fa09;
> category: repaired field label;
> value: repaired text value, or empty string if missing;
> token_ids: OCR token ids supporting the value;
> group_id: repaired row group such as g00 or summary;
> missing: boolean.
> For missing fields, set missing to true, value to an empty string, and token_ids to an empty list.
> Submission
> Submit a CSV with exactly one row per id in test.csv and exactly these columns in this order: id, repair_json, confidence.
> Column	Type	Constraint
> id	int	Same ids as test
> repair_json	string	JSON repair
> confidence	float	In [0,1]
> Example submission format:
> id,repair_json,confidence
> 101,"{""fields"":[{""slot_id"":""s8c12fa09"",""category"":""item.name"",""value"":""Nasi Campur"",""token_ids"":[""t0003"",""t0004""],""group_id"":""g00"",""missing"":false}]}",0.63
> 102,"{""fields"":[{""slot_id"":""s47b5e0aa"",""category"":""item.qty"",""value"":"""",""token_ids"":[],""group_id"":""g00"",""missing"":true}]}",0.41

Inspiration note: Useful because it turns OCR cleanup into structured ledger repair: recover missing slots from noisy document evidence with a CPU-friendly tabular/text output shape.

## Art-Auction Sale Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b8thyxa8tehf2pcq7767bj58anv2j
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Art-Auction Sale Reconstruction
> Overview:
> Historical art auctions were documented as sale catalogs, each catalog listing the lots (individual artworks) offered at one sale. The lots in a single sale come from one or a few consignors' collections, so they tend to share the seller, the taste, the region, the period, and the price register behind that collection, even though they are a varied mix of artists and objects. In this task each example is a POOL: the lots of six different sale catalogs, shuffled together and presented as a sequence of lot descriptions. Your job is to read the pool and assign every lot a group label so that lots which came from the same original sale get the same label, reconstructing the six sales.
> Each pool is given as an ordered list of lot descriptions (lot_01, lot_02, and so on). Every lot description is a short text record with seven fields separated by two colons, in this order: an anonymized artist token, an anonymized seller (consignor) token, the artist's nationality or school, the object type, a materials note, the sale currency, and the natural log of the price. Fields can be empty. Tokens are anonymized: lots by the same artist share an artist token and lots sold by the same consignor share a seller token, but the tokens cannot be traced back to a name. For each pool you output a sequence of group labels, one label per lot in the given order, and lots you believe came from the same sale should receive the same label.
> This is a record-linkage / structured-grouping problem, not a per-field lookup: no single field decides membership, so you must learn from the training pools how the fields combine to indicate that two lots shared a sale. A shared consignor is the strongest cue but is recorded for only about 60 percent of lots, a shared artist is a weaker one, and object type, materials, nationality, and the price register add further evidence. Lots with no recorded seller must be placed from those weaker cues alone.
> The pools are deliberately built to defeat shortcuts: the six sales in a pool are drawn from the same market and the same period, so they share a currency and a price register and were held within about a year of each other. Sorting a pool by currency, by era, or by price band therefore reveals almost nothing about the grouping, and the same-period sales overlap heavily in artists and schools. A consignor also sometimes appears in more than one sale. Simple rules recover only part of the structure, and an off-the-shelf clustering of the raw fields recovers considerably less than a model that learns which cues actually indicate shared provenance. The task is CPU-solvable: it is small text metadata, and a pairwise same-sale model with a grouping step, or a learned record-linkage model, trains on a few CPU cores.
> Evaluation:
> The metric is the mean Adjusted Rand Index (ARI) across the pools. For one pool, ARI compares your predicted grouping of its lots to the true grouping (the six sales). ARI counts, over all pairs of lots in the pool, how often your grouping and the true grouping agree on whether the two lots are together, corrected for chance:
> ARI = (index - expected_index) / (max_index - expected_index)
> where index is the number of agreeing lot pairs. ARI is 1.0 for a perfect grouping and about 0.0 for a random grouping or a trivial one (all lots in one group, or every lot in its own group). The group LABELS themselves do not matter, only the partition (which lots you place together), so any labeling that reflects the correct grouping scores the same. The final score is the average ARI over all pools, clipped to the range 0.0 to 1.0: a grouping that is worse than chance reports 0.0 rather than a negative value. Higher is better. For reference, putting every lot in one group scores about 0.00, grouping by currency alone about 0.01, an off-the-shelf equal-weight clustering of the raw fields about 0.23, and a share-the-consignor rule about 0.43; learning which cues indicate shared provenance, and placing the lots whose consignor is missing, is what improves on those.
> Dataset:
> The following files are provided in the public data directory. There are 449 training pools and 256 test pools. Each pool holds the lots of exactly six sales, so every pool has exactly six true groups. Pools contain between 23 and 48 lots; lot columns beyond a pool's lot count are empty.
> train.csv - the training pools, 449 rows (one pool per row). Columns:
> id - string - unique pool identifier (for example trp_0031).
> n_lots - integer - the number of lots in this pool (how many lot columns are filled).
> lot_01 ... lot_48 - string - the lot descriptions, in order. Each filled cell is a record of seven fields separated by two colons: artist_token :: seller_token :: nationality :: object_type :: materials :: currency :: log_price. Any field may be empty (for example an empty seller_token; the seller is recorded for about 60 percent of lots). Columns past n_lots are empty strings.
> grouping - string - the true grouping: a space-separated sequence of integer labels, one per lot in lot_01..lot_n_lots order. Lots with the same label came from the same original sale (there are six distinct labels per pool). Labels are only meaningful within a pool.
> test.csv - the test pools, 256 rows (one pool per row). Columns:
> id - string - unique pool identifier (for example tep_0007).
> n_lots - integer - the number of lots in this pool.
> lot_01 ... lot_48 - string - the lot descriptions, as above. There is no grouping column.
> sample_submission.csv - a valid submission in the correct format, 256 rows (one per test pool). Columns:
> id - string - matches the ids in test.csv.
> prediction - string - a space-separated sequence of group labels, one per lot. In this sample file every lot is placed in group 0 (a trivial all-in-one-group baseline).
> Submission:
> Submit a CSV with exactly two columns, id and prediction, and one row per test pool (256 rows plus a header). For each pool, prediction is a space-separated sequence of integer group labels, one label per lot in lot_01..lot_n_lots order (so a pool with n_lots lots must have n_lots labels).
> Column - Type - Meaning
> id - string - a test pool identifier, exactly matching an id in test.csv.
> prediction - string - the group labels for the pool's lots, space-separated, in lot order. Use any integers you like; only the partition matters. Lots you believe came from the same sale should get the same label; lots from different sales should get different labels.
> Example submission (header plus two rows, abbreviated to 8 and 6 labels purely to keep the example short; a
> real row carries one label per lot, so 23 to 48 labels):
> id,prediction
> tep_0007,0 3 0 1 5 2 4 0
> tep_0008,2 2 0 1 3 4
> Requirements:
> The header row must be exactly: id,prediction
> Provide one row for every test pool (256 data rows, matching test.csv), with no duplicate and no missing ids.
> For each pool, give exactly n_lots labels in lot order. You are expected to use up to six distinct labels per pool, since each pool holds the lots of six sales.
> Rules:
> The only valid signal is the content of the lot descriptions (the artist token, seller token, nationality, object type, materials, currency, and log-price) within each pool. Groupings must be produced by a model that learns collection-coherence conventions from the training pools. The following approaches are not allowed:
> Hardcoding groupings for specific pool ids.
> Using the pool id strings, the lot ordering, or the row order of any file as a grouping signal instead of the lot content.
> Looking up or reconstructing the true sale groupings from any external dataset or reference obtained outside this challenge, instead of learning them from the provided training pools. The artist and seller tokens are anonymized and the records carry no names, titles, dates, or catalog identifiers, so grouping must come from the released content only.
> Calling any external inference or search API at prediction time; all models must run locally.
> Using private, role-gated, or API-key-based models, or non-reproducible external weights that are not publicly available.
> TF-IDF is not allowed.
> This task tests whether a model can learn what makes a set of art lots a coherent single-sale collection and use it to reconstruct sale groupings from anonymized attributes, which is the kind of entity-reconstruction / record-linkage problem that arises in provenance and archival research. A solution that scores well by exploiting ids or ordering, or by looking up the groupings from an external source rather than learning collection coherence, is not valid regardless of its score.

Inspiration note: Useful because it frames a CPU challenge as structured event reconstruction from noisy real-world records, with outputs that resemble a sale ledger rather than a simple prediction.
