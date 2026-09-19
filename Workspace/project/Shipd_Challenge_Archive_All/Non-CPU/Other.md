# Non-CPU Other Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 64

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Audio-Visual Melt-Pool Process-State And Defect-Risk Ledger

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx737tkabf6qv4c9jmzgxmhxms8938vs
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Manufacturing engineers often need a compact process-state report from noisy in-process sensor streams rather than a raw media label. In this challenge, each row is a short synchronized segment from a real robotic laser metal-deposition run. The public inputs pair machine audio recorded during deposition with coaxial melt-pool camera imagery captured from the same time span.
> Your task is to predict a four-field process ledger for every hidden segment. process_state describes whether deposition appears stable, transitional, defect-indicating, or in an off/restart transition. defect_risk summarizes the segment as low, medium, or high risk. anomaly_timing gives the coarse within-segment location of the strongest anomaly: none, early, middle, or late. av_agreement reports whether audio and visual evidence agree as clean, agree as anomalous, or point to an audio-only or visual-only anomaly.
> This is not a normal video-file challenge and not a single-frame classification task. Treat frame_dir as an ordered sequence of 25 prepared JPG melt-pool signal views aligned with the corresponding 1.0-second mono WAV file in audio_path.
> The intended solution should learn from both modalities. The audio clip carries acoustic energy and transient machine-state cues; the frame sequence carries melt-pool intensity, edge, motion, and shape cues. A solution that only memorizes ids, path strings, row order, or file artifacts is outside the intended task.
> Task
> For each row in test.csv, submit one ledger row with:
> process_state: the segment's manufacturing process state.
> defect_risk: the overall risk level indicated by the synchronized segment.
> anomaly_timing: the coarse within-segment timing of the strongest anomaly.
> av_agreement: whether audio and visual evidence are clean, jointly anomalous, or disagree.
> confidence: your calibrated confidence that all categorical ledger fields are correct.
> What to use:
> Learned multimodal models that combine audio and ordered still frames.
> Audio feature extractors, frame-sequence encoders, temporal pooling, and calibrated validation on the provided training labels.
> What not to use:
> Source lookup, public-corpus matching, reverse-searching media, raw filename or timestamp recovery, hard-coded row-order rules, or manual relabeling from external copies.
> Submissions based only on segment ids, path strings, file lengths, or dataset-specific metadata.
> Enforcement on invalid approaches: rule-only or lookup-based solutions that do not model the supplied audio and melt-pool frame content may be rejected before payout.
> Dataset
> The public data contains train and test input tables plus media folders. Paths in train.csv are relative to public/train/; paths in test.csv are relative to public/test/. Train labels are provided separately so solvers can join them by segment_id without exposing hidden test labels.
> Files
> Item	Description
> train.csv	Public train inputs
> train_labels.csv	Train target labels
> test.csv	Hidden test inputs
> sample_submission.csv	Valid dummy submission
> train/audio/	Train wav clips
> train/frames/	Train frame folders
> test/audio/	Test wav clips
> test/frames/	Test frame folders
> train.csv has 134 input rows, train_labels.csv has the matching training labels, and test.csv has 44 hidden-label input rows. Each segment is 1.0 second long and has one WAV clip plus 25 ordered JPG frame views. Each WAV file is mono 16-bit PCM at 44,100 Hz. Each frame view is an RGB JPG at 224 by 168 pixels. Frame files are named in temporal order inside each frame_dir.
> Train Columns
> Column	Type	Description
> segment_id	string	Opaque segment id
> frame_dir	string	25 JPG frame folder
> audio_path	string	Mono WAV path
> duration_sec	float	Always 1.0 seconds
> For train rows, frame_dir is relative to public/train/ and contains exactly 25 ordered RGB JPG files. audio_path is relative to public/train/ and points to the synchronized mono WAV clip for the same segment. duration_sec is always 1.0.
> Test Columns
> Column	Type	Description
> segment_id	string	Opaque segment id
> frame_dir	string	25 JPG frame folder
> audio_path	string	Mono WAV path
> duration_sec	float	Always 1.0 seconds
> For test rows, frame_dir is relative to public/test/ and contains exactly 25 ordered RGB JPG files. audio_path is relative to public/test/ and points to the synchronized mono WAV clip for the same segment. Test rows have the same input columns as train rows, with all labels hidden.
> Train Label Columns
> Column	Type	Description
> segment_id	string	Opaque segment id
> process_state	class	One of four states
> defect_risk	class	Low/medium/high
> anomaly_timing	class	None/early/mid/late
> av_agreement	class	Audio-visual relation
> Allowed process_state values:
> stable_deposition: no strong segment-level process disturbance is indicated.
> quality_transition: the segment shows mixed or changing quality evidence.
> sustained_defect_signature: the segment is dominated by defect-indicating deposition evidence.
> laser_off_or_restart: the segment contains an off/restart-style process transition.
> Allowed defect_risk values: low, medium, high.
> Allowed anomaly_timing values:
> none: no anomaly timing is indicated.
> early: strongest anomaly evidence is in the first third.
> middle: strongest anomaly evidence is in the middle third.
> late: strongest anomaly evidence is in the final third.
> Allowed av_agreement values:
> agree_clean: neither modality gives strong anomaly evidence.
> agree_anomalous: both modalities support anomalous behavior.
> visual_only: visual evidence is anomalous while audio is not.
> audio_only: audio evidence is anomalous while visual evidence is not.
> Evaluation
> Scores are maximized from 0.0 to 1.0. A perfect submission with confidence 1.0 scores exactly 1.0.
> Each row receives exact-match credit for four categorical heads. The label head weights are:
> process_state: 0.36
> defect_risk: 0.235
> anomaly_timing: 0.235
> av_agreement: 0.17
> For a row, let categorical_score = 0.36*I_process + 0.235*I_risk + 0.235*I_timing + 0.17*I_agreement, where each indicator is 1 if that submitted categorical value exactly matches the hidden answer and 0 otherwise. Let all_correct = 1 only when all four categorical fields are correct; otherwise all_correct = 0. The calibration term is calibration = max(0, 1 - abs(confidence - all_correct)), using the submitted confidence clipped by the required [0, 1] validity rule.
> The row score is 0.94 * categorical_score^2.4 + 0.06 * calibration. This strict row scoring means broad common-class guesses receive limited partial credit, while complete multimodal ledger recovery is rewarded.
> Structural submission failures such as wrong or reordered columns, duplicate ids, missing ids, extra ids, or non-finite/out-of-range confidence values are invalid. Row-local invalid class strings receive no credit for the affected heads and receive no calibration credit.
> Submission Format
> Column	Type	Constraint
> segment_id	string	From test.csv
> process_state	class	Allowed value
> defect_risk	class	Allowed value
> anomaly_timing	class	Allowed value
> av_agreement	class	Allowed value
> confidence	float	0 to 1
> Requirements:
> Submit exactly one row for every segment_id in test.csv.
> Use exactly the columns shown above, in the same order.
> Do not include duplicate, missing, unknown, or extra ids.
> Use only the allowed categorical values and finite confidence values in [0, 1].
> Example:
> segment_id,process_state,defect_risk,anomaly_timing,av_agreement,confidence
> sg_000000,sustained_defect_signature,high,early,agree_clean,0.35
> sg_000001,sustained_defect_signature,high,early,agree_clean,0.35
> sg_000004,sustained_defect_signature,high,early,agree_clean,0.35

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## String-Aware Guitar Note Event Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx714jz9g7dad5r6d0hn0g6n5x8a3pc9
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: audio, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Your objective is to recover a fretboard-aware note-event ledger from a two-second mono guitar performance excerpt. For every note event in the excerpt, predict its onset time bin, string id, MIDI pitch, and duration bin.
> The audio comes from real solo acoustic guitar performances captured with a close mono microphone and converted into short 16-bit PCM WAV excerpts. The recordings contain played notes, chords, overlapping note decays, string changes, and realistic timing variation from human performance. This is not ordinary audio tagging: the same pitch can be played on multiple strings, so a correct ledger must recover both pitch-time content and string assignment.
> Each excerpt is exactly two seconds long. Time is quantized into 32 onset bins, so each onset bin represents 1/16 second.
> Dataset
> train.csv: 699 labeled audio windows with answer_json.
> test.csv: 401 held-out audio windows without labels.
> sample_submission.csv: 401-row valid baseline submission.
> audio/: Mono WAV excerpts, encoded as 16-bit PCM at 44.1 kHz.
> Column definitions:
> id (string): Opaque row id.
> audio_path (string): Relative WAV path.
> prompt (string): Task instruction. It asks solvers to recover the string-aware note event ledger for the two-second excerpt.
> sample_rate (integer): Audio sample rate. In this package it is 44100.
> duration_seconds (float): Clip duration. In this package it is 2.0.
> answer_format_json (JSON object): Required event schema and valid ranges: onset_bins=32, string=0-5, midi=20-108, and duration_bin=0-15.
> answer_json (JSON object, train only): Ground-truth event ledger.
> answer_json has this structure:
> events (JSON list): Zero or more note-event objects, with at most 96 events.
> events[i].onset_bin (integer): Onset time bin. Valid values are 0 through 31.
> events[i].string (integer): Zero-indexed guitar string id. Valid values are 0 through 5.
> events[i].midi (integer): MIDI pitch. Valid values are 20 through 108.
> events[i].duration_bin (integer): Quantized note duration. Valid values are 0 through 15.
> The event list is treated as a multiset. If the same event tuple appears more than once, duplicates count separately.
> Submission Format
> Submit a CSV with exactly these columns: id, answer_json.
> Example:
> id,answer_json
> row_example,"{""events"":[{""onset_bin"":8,""string"":2,""midi"":55,""duration_bin"":3},{""onset_bin"":8,""string"":4,""midi"":67,""duration_bin"":4}]}"
> Every submitted event must contain exactly the four fields onset_bin, string, midi, and duration_bin, all as integers within the valid ranges above.
> Evaluation
> Rows are scored with three duplicate-aware multiset F1 terms:
> row_score = 0.58 * exact_event_f1 + 0.27 * onset_string_pitch_f1 + 0.15 * onset_pitch_f1
> For any F1 term, the grader converts the predicted events and hidden events into multisets of tuples. It counts matches as:
> matched = sum(min(predicted_count[token], true_count[token]) for each token)
> Then:
> precision = matched / number_of_predicted_tokens
> recall = matched / number_of_true_tokens
> F1 = 2 * precision * recall / (precision + recall)
> If the hidden multiset is empty, the F1 term is 1 only when the submitted multiset is also empty; otherwise it is 0.
> The three row-level F1 terms use different tuple projections:
> exact_event_f1: (onset_bin, string, midi, duration_bin).
> onset_string_pitch_f1: (onset_bin, string, midi), ignoring duration.
> onset_pitch_f1: (onset_bin, midi), ignoring string and duration.
> The final leaderboard score is:
> 0.82 * mean_row_score + 0.06 * worst_event_count_group + 0.06 * worst_string_mix_group + 0.06 * worst_density_group
> mean_row_score is the average row score over the hidden answers. Each worst-group term is also a 0-to-1 mean row score: it is the lowest mean row score among held-out grouping labels with at least five rows.
> The grouping axes are:
> worst_event_count_group: rows grouped by hidden event-count bucket: few for 1-4 events, medium for 5-10 events, and dense for 11 or more events.
> worst_string_mix_group: rows grouped by hidden string-coverage bucket: single_string for one distinct string, partial_chord for two or three distinct strings, and wide_chord for four or more distinct strings.
> worst_density_group: rows grouped by a second hidden event-load bucket with intentionally shifted thresholds: sparse for 1-5 events, active for 6-12 events, and busy for 13 or more events. This is separate from worst_event_count_group; it is a robustness slice for near-boundary event density, not a field participants need to submit.
> Scores range from 0 to 1; higher is better.
> What Not To Use
> Hardcoded mappings from filenames or row ids to answers.
> Any annotations, files, tablature, MIDI, source-track metadata, or note labels outside the released public files.
> Row-order shortcuts or package-internal generation artifacts.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Multimodal Robot Episode-Weave Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72ca6wzrmkqtam7ny1k0e68n8bj5cw
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: large-scale, multimodal, video, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Real robot-learning archives store vision, robot state, and actions as synchronized trajectories. During fragmented exports, anonymization, or multimodal data integration, the correspondence and chronology between these streams can be lost.
> Each case contains nine anonymized visual fragments and nine control fragments derived from three real robot trajectories. Each original trajectory contributes three temporally ordered fragments. The visual and control fragments are independently shuffled.
> Recover the hidden episode weave: determine which fragments belong to the same trajectory, pair each visual fragment with its synchronized control fragment, and restore the three-fragment temporal order within every trajectory.
> This is a joint constrained reconstruction problem. It is not ordinary video classification, action recognition, retrieval, or independent pair matching.
> Prediction Objective
> For every case_id, predict exactly three ordered chains. Each chain must contain exactly three entries.
> Across the three chains:
> every allowed visual ID must appear exactly once;
> every allowed control ID must appear exactly once;
> each entry pairs one visual fragment with one control fragment;
> chain membership represents the recovered source trajectory;
> entry order represents temporal precedence within that trajectory.
> The order of the three chains themselves is irrelevant.
> Dataset
> The prepared dataset contains:
> public/
> ├── train.csv
> ├── test.csv
> ├── sample_submission.csv
> ├── visual/
> ├── control/
> ├── ATTRIBUTION.txt
> └── source_metadata.json
> private/
> └── answers.csv
> The public split contains 350 labeled training cases and 130 held-out test cases. Complete physical-scene groups are assigned to only one split.
> public/train.csv
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Opaque case identifier. |
> | visual_fragments_json | JSON array | Nine objects containing a row-local fragment_id and relative .npz path. |
> | control_ids_json | JSON array | Nine row-local control fragment IDs. |
> | fragment_count | integer | Always 9. |
> | chain_count | integer | Always 3. |
> | fragments_per_chain | integer | Always 3. |
> | answer_json | JSON object | Ground-truth three-chain reconstruction. |
> public/test.csv
> Contains the same input columns as train.csv, without answer_json.
> Visual fragments
> Each file under public/visual/ is a compressed NumPy archive containing:
> | Array | Shape | Dtype | Description |
> |---|---:|---|---|
> | frames | (4, 96, 96, 3) | uint8 | Four temporally ordered RGB frames. |
> Control fragments
> Each file under public/control/ is a compressed NumPy archive containing:
> | Array | Shape | Dtype | Description |
> |---|---:|---|---|
> | relative_state | (4, 7) | float32 | Relative robot-state sequence. |
> | action | (4, 7) | float32 | Robot-action sequence. |
> The file for control ID ctl_x is public/control/ctl_x.npz.
> Submission Format
> Submit submission.csv with exactly these columns:
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Test identifier copied exactly from test.csv. |
> | prediction_json | JSON string | Three ordered chains satisfying all one-use constraints. |
> Each prediction_json must have this structure:
> {
> "chains": [
> [
> {"visual_id": "vis_a", "control_id": "ctl_d"},
> {"visual_id": "vis_b", "control_id": "ctl_e"},
> {"visual_id": "vis_c", "control_id": "ctl_f"}
> ],
> [
> {"visual_id": "vis_d", "control_id": "ctl_a"},
> {"visual_id": "vis_e", "control_id": "ctl_b"},
> {"visual_id": "vis_f", "control_id": "ctl_c"}
> ],
> [
> {"visual_id": "vis_g", "control_id": "ctl_g"},
> {"visual_id": "vis_h", "control_id": "ctl_h"},
> {"visual_id": "vis_i", "control_id": "ctl_i"}
> ]
> ]
> }
> A valid submission must:
> contain exactly one row for every test case_id;
> contain no duplicate case_id values;
> use exactly the nine visual IDs supplied for that case;
> use exactly the nine control IDs supplied for that case;
> use every allowed ID exactly once;
> contain exactly three chains with exactly three entries each.
> Use public/sample_submission.csv as a schema example. Its predictions are valid structurally but are not intended to be accurate.
> Evaluation
> Each test case receives three partial scores.
> 1. Cross-Modal Assignment
> The fraction of visual fragments paired with their correct control fragments.
> 2. Episode Partition
> Pairwise F1 over whether two visual fragments belong to the same hidden trajectory.
> 3. Temporal Precedence
> Among pairs that truly belong to the same trajectory, the fraction for which the prediction places both fragments in one chain and orders them correctly.
> The case score is:
> 0.40 × assignment
> + 0.30 × partition_F1
> + 0.30 × precedence
> The final score is the arithmetic mean across all test cases.
> Direction: maximize
> Minimum: 0.0
> Maximum: 1.0
> Malformed submissions or predictions violating the per-case one-use constraints are rejected rather than silently repaired.
> Expected Methods
> Competitive solutions should naturally use GPU-trained components such as:
> a compact video encoder or video transformer;
> a temporal encoder for state and action sequences;
> multimodal contrastive or Siamese training;
> row-level cross-attention;
> learned visual-control compatibility matrices;
> Hungarian or Sinkhorn assignment;
> learned trajectory-membership and precedence scores;
> dynamic programming or another constrained structured decoder.
> Pretrained weights may be used when permitted by the platform, but the supplied training set must be used for genuine learning or fine-tuning.
> Rules
> Train and validate using only the supplied public training data and explicitly permitted pretrained weights.
> Treat the public test set only as unlabeled inference data.
> Do not fit normalization statistics, thresholds, blend weights, or hyperparameters using test cases.
> Do not use external BridgeData files, original trajectory metadata, task instructions, source paths, timestamps, scene labels, or hidden trajectory identifiers.
> Do not reverse-engineer or enumerate opaque IDs.
> Do not patch individual test cases or submit fixed outputs.
> Do not use external APIs to recover labels.
> The solution must run end to end in the configured GPU environment and write ./working/submission.csv.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Open-Population Caller Turnover Program

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7by8w188jx96vf39n95tnft58b23hj
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat zzz_grs's score of 0.353!

Full challenge description from page:

> Overview
> Predict an open-population turnover program from two nightly acoustic surveys. Every case contains a reference-night montage with slots R1 through R8 and a later survey montage with slots N1 through N8. Exactly seven callers return, one reference caller is absent, and one survey caller is new. Submit the seven return links, the departure, the arrival, and a calibrated event-confidence vector as one structured answer.
> Acoustic recapture can estimate population continuity without physically marking every animal. It is difficult because temperature changes call timing and pitch, nearby individuals have similar repertoires, and field noise varies between nights. The task therefore evaluates open-population turnover reasoning rather than closed-set call classification.
> The practical setting is a field survey where the roster is not closed. A later night contains mostly returning callers, but one earlier caller has disappeared and one new caller has entered the recording area. A useful system has to recover the one-to-one links and explicitly name both population events, rather than forcing every clip into a fixed identity class.
> The novelty is the local turnover program. R1 and N1 are not persistent IDs, and the unmatched slots are part of the answer rather than nuisance cases. The solver must infer a partial bijection, leave one reference slot unmatched, leave one survey slot unmatched, and serialize all decisions in one program. This differs from speaker identification, speaker verification, closed-set animal ID, and pairwise same-different scoring because the output is a complete open-roster edit.
> The audio comes from real male field-cricket recordings collected over three nights. Each montage contains eight consecutive 0.55-second five-syllable call slots. Mild deterministic gain and passband changes suppress file-level shortcuts without changing caller evidence. Training and test cases use disjoint biological individuals and disjoint source call intervals.
> This challenge is designed for GPU-enabled inference. Solutions may use an A10G GPU within the platform runtime.
> Dataset
> The prepared dataset contains 400 labeled training cases and 350 hidden test cases.
> | Path | Contents |
> |---|---|
> | `train.csv` | Four input columns plus `roster_program` and `event_confidence_vector` for 400 cases |
> | `test.csv` | Four input columns for 350 cases |
> | `sample_submission.csv` | A schema-valid fixed-roster baseline |
> | `audio/` | Two short mono MP3 montages for every case |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier beginning with `r` followed by 22 hexadecimal characters |
> | `reference_audio_path` | string | Relative path to the reference-night montage |
> | `survey_audio_path` | string | Relative path to the later-night montage |
> | `temperature_context` | string | Mean of the available source-session temperatures for each montage and the slot-order declaration. Sessions without a temperature record are omitted from the mean. |
> The eight reference clips occur in order R1 to R8. The eight survey clips occur in order N1 to N8. Every slot is 0.55 seconds, so slot boundaries are determined directly from elapsed time.
> Example input:
> case_id,reference_audio_path,survey_audio_path,temperature_context
> r84fd727885f780e2f91ad8,audio/1e421d767665f80a17a07cd8.mp3,audio/0bb3196ae4b070ca573791a2.mp3,"reference_mean_c=28.4;survey_mean_c=25.9;reference_slots=R1..R8;survey_slots=N1..N8"
> Turnover Roster Program
> roster_program is a string of exactly ten >-separated tokens:
> Seven match:Rx=Ny tokens, sorted by Rx
> One depart:Rx token for the unmatched reference slot
> One arrive:Ny token for the unmatched survey slot
> The final token commit:open_census
> Every reference and survey slot must appear exactly once across the match and event tokens.
> Example:
> match:R1=N4>match:R2=N7>match:R3=N2>match:R4=N8>match:R5=N1>match:R6=N6>match:R8=N3>depart:R7>arrive:N5>commit:open_census
> Event Confidence Vector
> event_confidence_vector is a JSON-encoded float array with 16 entries. Entries 0 through 7 give the predicted probability distribution over departure slots R1 through R8. Entries 8 through 15 give the predicted probability distribution over arrival slots N1 through N8. The grader clips negative submitted values to zero and normalizes the two halves separately. If either half has no positive finite value, the confidence component for that case is zero.
> Example for depart:R7 and arrive:N5:
> [0.01,0.02,0.03,0.02,0.04,0.05,0.80,0.03,0.03,0.02,0.02,0.04,0.82,0.03,0.02,0.02]
> Training Distribution
> | Slot | Departure rows | Slot | Arrival rows |
> |---|---:|---|---:|
> | `R1` | 45 | `N1` | 60 |
> | `R2` | 61 | `N2` | 47 |
> | `R3` | 47 | `N3` | 43 |
> | `R4` | 41 | `N4` | 53 |
> | `R5` | 54 | `N5` | 41 |
> | `R6` | 49 | `N6` | 50 |
> | `R7` | 48 | `N7` | 55 |
> | `R8` | 55 | `N8` | 51 |
> Every row has exactly seven links, one departure, and one arrival.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,roster_program,event_confidence_vector
> All columns are strings at CSV level. roster_program is limited to 230 characters and exactly ten tokens. event_confidence_vector must be a JSON array of 16 finite numeric values and is limited to 240 characters.
> case_id,roster_program,event_confidence_vector
> r84fd727885f780e2f91ad8,match:R1=N4>match:R2=N7>match:R3=N2>match:R4=N8>match:R5=N1>match:R6=N6>match:R8=N3>depart:R7>arrive:N5>commit:open_census,"[0.01,0.02,0.03,0.02,0.04,0.05,0.80,0.03,0.03,0.02,0.02,0.04,0.82,0.03,0.02,0.02]"
> There must be one row per test case. Extra or reordered columns, duplicate column names, duplicate IDs, missing or extra rows, and unknown IDs are rejected. A malformed roster program scores 0 for that case.
> Evaluation
> The metric is the Open Roster Program Score. Higher is better.
> Minimum score: 0.0
> Maximum score: 1.0
> For the seven true link tokens Y and seven predicted link tokens P:
> LinkF1 = 2 * |Y intersect P| / (|Y| + |P|)
> The event component gives half credit for the correct departure and half for the correct arrival:
> EventScore =
> 0.5 * I(predicted departure is correct)
> + 0.5 * I(predicted arrival is correct)
> The complete-program indicator is 1 only when all ten canonical tokens are exactly correct.
> The confidence component rewards calibrated probability mass on the true departure and arrival events. Let p_depart be the normalized probability assigned to the true departure slot in the first half of event_confidence_vector, and let p_arrive be the normalized probability assigned to the true arrival slot in the second half. The row confidence is:
> EventConfidenceScore = clip(1 - (-log(sqrt(p_depart * p_arrive)) / log(8)), 0, 1)
> case_score =
> 0.50 * LinkF1
> + 0.22 * EventScore
> + 0.18 * I(complete program is exact)
> + 0.10 * EventConfidenceScore
> FinalScore = mean(case_score over all test cases)
> Hidden programs are validated against the one-to-one roster grammar. They are never canonicalized, clipped, or repaired by the grader.
> What Makes This Interesting
> The labels are not permanent class names that can be memorized. R1 and N1 are local positions that change in every case. A solver must compare two nights, normalize temperature-related acoustic shifts, construct a one-to-one partial correspondence, and explicitly account for open-population departure and arrival.
> The central reasoning object is an open turnover roster. This differs from speaker identification or call-type classification because the model must solve a local bipartite matching problem with exactly one departure and one arrival in every case. The canonical program makes both the identity links and the unmatched events scoreable.
> The held-out biological-individual split is a second novelty point. Test callers are not the same individuals as training callers, so the task measures whether acoustic comparison rules transfer to new animals. A nearest-neighbor lookup of known identities is structurally insufficient.
> What Not To Use
> Do not map opaque IDs, filenames, row order, file size, or split position to roster programs.
> Do not recover original recording names or match clips against external copies or fingerprints.
> Do not use external identity annotations, source split tables, or online lookup to identify callers.
> Do not exploit malformed CSV behavior, duplicate rows, parser limits, or grader exceptions.
> Do not tune against hidden labels or leaderboard feedback.
> Audio embeddings, bioacoustic features, metric learning, bipartite assignment, deterministic optimization, and GPU-accelerated representation models are allowed within the supplied platform environment.
> Reference Validation
> Release validation requires two byte-identical prepares, zero train-test identity overlap, zero source-call reuse, zero public audio duplicate hashes, exact score 1.0, strict schema-attack rejection, and low sample, adjacent-ID, file-size, and simple spectral-nearest-neighbor baselines. The fixed-roster sample scores 0.074167. The prepared split has 26 training identity groups and 16 hidden identity groups, with no overlap. Measurements are recorded in validation_report.json.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Visual Graph Lineages: Glyph Rules and Counterfactual Edits

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cgjcr2my157mj9qwaaedb7h8bjd5w
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 0.106!

Full challenge description from page:

> Visual Graph Lineages: Glyph Rules and Counterfactual Edits
> Overview
> Each family begins with a canonical graph of connected parts and a lineage of
> short programs written in twelve abstract glyphs. The same glyph can mean a
> graph operation or a rule-changing operation. Rule changes persist into later
> descendants.
> Every family also has a rendered image containing a visual insignia. The
> insignia determines that family's hidden initial glyph dialect. Training
> families include the corresponding 16-bit dialect code; test dialect codes are
> withheld.
> Your task is to predict the graph produced at selected test descendants after
> one glyph in an ancestor program is replaced. A replacement can change the
> graph immediately, change the meaning or order of later instructions, or do
> both. Correct solutions must infer the family dialect from the image and carry
> the revised rule state through the lineage.
> The canonical root graph is supplied for every train and test family. Test
> descendant graphs are not supplied.
> Dataset
> Property	Value
> Families	2,500
> Training families	2,000
> Test families	500
> Artifacts per family	7
> Training artifact rows	14,000
> Test artifact rows	3,500
> Counterfactual queries per family	2
> Training scored rows	13,656
> Test scored rows	3,330
> Root images	2,500 RGB PNG files
> Image resolution	640 by 640
> Dialect code length	16 bits
> Possible initial dialect codes	65,536
> The split is family-disjoint. All artifacts and queries from one family stay
> in the same split. Identifiers are opaque and CSV row order does not encode
> lineage order.
> Files
> File or folder	Description
> train_families.csv	Training family image, canonical root graph, and dialect code.
> test_families.csv	Test family image and canonical root graph. Dialect code withheld.
> train_artifacts.csv	Training lineage tree, programs, and factual part graphs.
> test_artifacts.csv	Test lineage tree and programs. Factual descendant graphs withheld.
> train_queries.csv	Training edits and target graphs. One row per query-target pair.
> test_queries.csv	Test edits and target artifact ids. Target graphs withheld.
> images/train/	Root images for training families.
> images/test/	Root images for test families.
> starter.py	Parsing, dialect-to-grammar, and counterfactual rollout helpers.
> lineage_engine.py	Public deterministic graph executor.
> sample_submission.csv	Valid submission template with constant graph predictions.
> Encodings
> Dialect Code
> A dialect is written as d followed by exactly 16 binary digits:
> d0100110010110001
> starter.grammar_from_dialect_code converts a predicted code into the
> family's initial public grammar.
> Part Graph
> A graph begins with graph. Parts follow in canonical breadth-first order:
> graph|p0,root,root,core,c2,z1,r0|p1,p0,north,spire,c4,z2,r1
> Every part token contains seven comma-separated fields:
> part_id,parent_id,slot,kind,color,scale,rotation
> Part ids are contiguous: p0, p1, and so on.
> p0 is the only root and always uses parent root, slot root, and kind
> core.
> Child slots are north, east, south, west, or top.
> Non-root kinds are spire, ring, plate, orb, fork, fin, and
> shell.
> Colors are c0 through c5.
> Scales are z0 through z2.
> Rotations are r0 through r3.
> Valid predictions contain 3 to 18 connected parts. A parent cannot contain
> two children in the same slot.
> Glyph Program
> A program begins with program. Each instruction contains a glyph and four
> integer fields:
> program|gF,a27,x28,y08,v21|gL,a06,x23,y16,v27
> Glyphs range from gA through gL. The executor resolves their meanings from
> the current grammar. Numeric arguments are interpreted by the resolved
> operation.
> Query
> Each query replaces one glyph in ancestor_id at zero-based
> instruction_index. The changed program and all later descendants must be
> executed from the supplied root. A single query can therefore produce several
> submission rows, one for each scored target_artifact_id.
> starter.rollout_query implements this deterministic propagation once a
> dialect code has been predicted.
> Evaluation
> The metric is mean graph-token F1 distance. Lower is better.
> For a predicted graph token set (P_i) and true token set (T_i):
> [
> \operatorname{precision}_i = \frac{|P_i \cap T_i|}{|P_i|},
> \qquad
> \operatorname{recall}_i = \frac{|P_i \cap T_i|}{|T_i|}
> ]
> [
> F1_i =
> \frac{2,\operatorname{precision}_i,\operatorname{recall}_i}
> {\operatorname{precision}_i+\operatorname{recall}_i},
> \qquad
> d_i = 1-F1_i
> ]
> The leaderboard score is:
> [
> \operatorname{Score} =
> \max\left(0.0001,\frac{1}{N}\sum_{i=1}^{N} d_i\right)
> ]
> The score lies from 0.0001 to 1.0. A perfect submission scores 0.0001.
> Malformed graph strings fail validation.
> Submission Format
> Submit submission.csv with exactly two columns in this order:
> id,prediction
> q123_r456,"graph|p0,root,root,core,c2,z1,r0|p1,p0,north,spire,c4,z2,r1"
> Requirements:
> Exactly 3,330 data rows.
> Every test id appears exactly once.
> No missing, duplicate, or extra ids.
> No extra columns.
> Every prediction is a valid canonical graph string.
> UTF-8 CSV encoding with header id,prediction.
> Allowed And Prohibited
> Allowed:
> Models trained on the provided training families.
> Generic pretrained vision weights that were publicly available before the
> challenge.
> Image augmentation, cross-validation, ensembling, and pseudo-labeling.
> Any use or reimplementation of the released parsing and rollout helpers.
> Hybrid learned and symbolic solutions.
> Prohibited:
> Using withheld test dialect codes, factual descendant graphs, or target
> graphs.
> Manual labeling of test images.
> Hardware And Compute
> The reference model trains from scratch in under ten minutes on an RTX 3070
> Laptop GPU with 8 GB VRAM. A single A10G-class GPU is sufficient for strong
> experiments; larger provisioned Diamond hardware can support ensembles or
> more ambitious visual encoders.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Bioacoustic Mechanism Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eey6rkqjbw5m8pde5gqyxs98bjvxx
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aryanm's score of 0.293!

Full challenge description from page:

> Overview:
> This challenge asks you to build an audio retrieval system that finds acoustically similar insect sound clips. Insect species produce sound through one of three distinct physical mechanisms: tymbal vibration (cicadas), tegminal stridulation (crickets and katydids), or femoro-alary stridulation (grasshoppers). Each mechanism produces a characteristic waveform structure. Your system must learn these acoustic signatures from labeled training clips and use them to retrieve the most similar clips from the test set.
> For each test clip, submit the 10 test clips (excluding the query itself) that are most acoustically similar to it. Similarity is evaluated by whether retrieved clips share the same sound production mechanism as the query. The challenge uses a species-disjoint protocol: the insect species in the test set do not appear in training. A system must generalize mechanism-level acoustic patterns to previously unseen species.
> Real-world context: passive acoustic monitoring generates large volumes of unlabeled insect recordings. A retrieval system that clusters recordings by sound production mechanism helps ecologists organize new recordings without species-level annotation, especially in regions with unknown species inventories.
> Evaluation:
> Mean Average Precision at 10 (MAP@10).
> For each test clip (query), you submit a ranked list of 10 retrieved clips from the test set. Retrieved clips that share the sound production mechanism with the query are relevant. AP@10 for one query is the average of the precision values at each rank position where a relevant clip appears, divided by min(10, total relevant clips in the test set). MAP@10 is the mean AP@10 across all queries.
> A retrieval system that always returns the 10 most similar clips from the same mechanism scores MAP@10 = 1.0. A system that returns random clips scores MAP@10 approximately 0.33.
> Dataset:
> All audio clips are 2 seconds long, 11025 Hz, mono WAV (16-bit PCM). Five clips are extracted from each source recording. A small amount of additive Gaussian noise has been applied; test clips have a higher noise level than training clips to create a distribution shift.
> The following files are provided in the public directory:
> train/
> Directory of training audio clips (WAV files). Each file is a 2-second mono recording at 11025 Hz.
> train.csv
> filename - string - WAV filename (e.g. clip_0000000.wav), matches a file in train/
> group - string - sound production mechanism group for the clip: one of tymbal, ensifera, or acrididae
> test/
> Directory of test audio clips (WAV files). Same format as train clips.
> test.csv
> filename - string - WAV filename, matches a file in test/
> sample_submission.csv
> filename - string - test clip filename (the query)
> retrieved_clips - string - 10 test clip filenames separated by spaces
> Training clips and test clips come from entirely different insect species. Species-level memorization cannot produce good retrieval on the test set; the system must learn mechanism-level acoustic structure.
> Submission:
> Your submission must be a CSV with exactly two columns: filename and retrieved_clips.
> filename - string - must exactly match filenames in test.csv (each appears exactly once)
> retrieved_clips - string - exactly 10 test clip filenames separated by single spaces, in order from most to least similar
> Example submission:
> filename,retrieved_clips
> clip_0000000.wav,clip_0000500.wav clip_0000501.wav clip_0000502.wav clip_0000503.wav clip_0000504.wav clip_0000505.wav clip_0000506.wav clip_0000507.wav clip_0000508.wav clip_0000509.wav
> clip_0000001.wav,clip_0000600.wav clip_0000601.wav clip_0000602.wav clip_0000603.wav clip_0000604.wav clip_0000605.wav clip_0000606.wav clip_0000607.wav clip_0000608.wav clip_0000609.wav
> Requirements:
> The submission must have exactly as many rows as test.csv. The filename column must contain each test clip filename exactly once with no duplicates. Each retrieved_clips value must contain exactly 10 test clip filenames separated by single spaces. The query clip itself must not appear in its own retrieved list. All retrieved clip filenames must be valid test set filenames from test.csv.
> Rules:
> The only valid input signal is the audio content of the WAV files in train/ and test/.
> The following approaches are not allowed:
> Hardcoding retrieved lists for specific test clip filenames.
> Using the filename itself or the sequential index of the clip as a retrieval signal instead of the audio waveform.
> Using clip index position or file creation order to infer which test clips came from the same recording.
> Reverse-engineering which insect species produced a clip and using an external species-to-mechanism lookup instead of acoustic similarity.
> Using private, role-gated, or API-key-based models, or calling any external audio inference API at retrieval time.
> Using any external insect audio data or recordings not provided in train/.
> The intended approach is to learn an acoustic embedding space where clips from the same sound production mechanism cluster together. The evaluation specifically tests whether learned similarity reflects mechanism rather than species identity or recording artifact, because test species are entirely absent from training.
> Pretrained model policy:
> General-purpose audio backbone models are allowed as feature extractors or as initialization for fine-tuning, provided they were not pretrained specifically on bioacoustic or wildlife monitoring data. Acceptable backbones include models trained on speech (Wav2Vec2, HuBERT), general environmental sounds (VGGish/AudioSet, PANNs), or broad audio (EnCodec, audio-MAE). Not allowed: models pretrained on bioacoustic monitoring, wildlife sound identification, or insect or bird call data (including BirdNET, BioLingual, AVES, or any model whose pretraining corpus includes labeled insect recordings). Using a backbone that already encodes insect acoustic structure bypasses the intended metric learning task. If uncertain whether a pretrained model qualifies, train from scratch on the provided train/ clips.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Bioacoustic Loss-Contingency Relay Planning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7393q98eypj5p84hknvzcq6x8b32s8
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat urdev's score of 0.696!

Full challenge description from page:

> Overview
> Predict a loss-contingency relay plan for a seven-slot wildlife audio packet. Each public MP3 contains seven consecutive field recordings labeled A through G. The submission must rank all slots by acoustic quality, choose four slots for transmission, state the replacement action for each possible transmitted-slot loss, give a four-entry contingency vector, and assign calibrated probability to which transmitted slot has no backup.
> This is a counterfactual scheduling task, not a duplicate-event benchmark. A correct answer must say what the station should do before transmission and what remains possible after a transmission fails. If a transmitted repeated event is lost, the plan should point to its untransmitted backup. If the transmitted singleton event is lost, the plan must acknowledge that no backup exists. The contingency vector then scores the replacement strength from the submitted quality order.
> The practical setting is low-power ecological monitoring. Remote stations often collect redundant recordings of the same biological event through different propagation paths. A bandwidth-limited station can transmit only part of the packet, and a weather or radio failure can drop one transmitted slot. The useful output is therefore a recovery-aware relay contract: transmit the best representatives, preserve one copy of each distinct event when possible, and quantify the damage caused by each single-slot loss.
> Each montage contains three repeated source performances, each appearing twice under different acoustic conditions, plus one singleton performance. Public files do not expose source song IDs, distance codes, habitat labels, or filename-derived metadata. Training and test use disjoint source performances.
> This challenge is designed for GPU-enabled inference. Solutions may use an A10G GPU within the platform runtime.
> Dataset
> The prepared dataset contains 380 labeled training cases and 350 hidden test cases.
> | Path | Contents |
> |---|---|
> | `train.csv` | Input columns `case_id`, `audio_path`, and `slot_contract`, plus targets `propagation_order`, `uplink_program`, `failover_program`, `contingency_vector`, and `drop_confidence_vector` |
> | `test.csv` | Input columns `case_id`, `audio_path`, and `slot_contract` only |
> | `sample_submission.csv` | A schema-valid fixed relay baseline |
> | `audio/` | One mono MP3 montage for every case |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier beginning with `u` followed by 22 hexadecimal characters |
> | `audio_path` | string | Relative path to the case montage |
> | `slot_contract` | string | Fixed contract value describing seven consecutive 1.40-second clips labeled `A` through `G` |
> Example input row:
> | case_id | audio_path | slot_contract |
> |---|---|---|
> | `u81dd13d38b756f8244b6fb` | `audio/3106a1c3d98bed167945ff41.mp3` | `seven consecutive 1.40-second clips labeled A..G` |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `propagation_order` | string | A permutation of `A` through `G`, joined by `>`, from best acquisition condition to worst |
> | `uplink_program` | string | Four `keep:X` tokens followed by `commit:compact`, ordered by propagation quality |
> | `failover_program` | string | Four `loss:X>Y` tokens followed by `commit:failsafe`, joined by `|` |
> | `contingency_vector` | JSON-encoded integer array | Four integers from `0` through `3`, in the same order as the four keep tokens |
> | `drop_confidence_vector` | JSON-encoded float array | Four numeric probabilities in keep-token order. The correct entry is the transmitted slot whose failover target is `drop`. |
> Propagation Order
> propagation_order ranks all seven slots from least to most propagation loss. The valid format is a seven-label permutation such as D>A>G>C>F>B>E. Distance and habitat conditions are not printed in the public data. They must be inferred from level, reverberation, spectral loss, and background evidence.
> Uplink Program
> uplink_program contains exactly four keep tokens and one commit token. It keeps one representative of each repeated performance pair and also keeps the singleton performance. The keep tokens must follow the submitted propagation order.
> Example uplink program: keep:D>keep:G>keep:C>keep:F>commit:compact.
> Failover Program
> failover_program describes the recovery action for each transmitted slot. It has four loss tokens followed by commit:failsafe.
> Each loss token has format loss:X>Y. X is one transmitted slot. If X is a repeated-event representative, Y is the backup slot that was not transmitted. If X is the singleton event, Y is drop because no replacement exists. The four loss tokens must follow the same order as the keep tokens in uplink_program.
> Example failover program: loss:D>A|loss:G>drop|loss:C>E|loss:F>B|commit:failsafe.
> Contingency Vector
> contingency_vector is a JSON array with four integers in the same order as the keep tokens and loss tokens.
> | Value | Meaning |
> |---:|---|
> | `0` | No backup exists because the lost transmitted slot was the singleton |
> | `1` | A backup exists, but it is far lower in the submitted quality order |
> | `2` | A backup exists with moderate quality loss |
> | `3` | A backup exists with close quality to the transmitted slot |
> The vector is computed from the loss target and quality order. If a loss token is loss:X>drop, the matching vector entry is 0. If a loss token is loss:X>Y, compare the rank of Y to the rank of X in propagation_order: gap 1 gives value 3, gap 2 or 3 gives value 2, and any larger gap gives value 1.
> Example contingency vector: [3,0,2,1].
> Drop Confidence Vector
> drop_confidence_vector is a JSON array with four finite numeric values in the same order as the keep tokens. It is a calibrated prediction of which transmitted slot is the singleton event and therefore has no backup. The grader clips negative submitted values to zero and normalizes the vector. If the vector has no positive finite value, the confidence component for that case is zero.
> Example when the second kept slot has no backup:
> [0.05,0.82,0.08,0.05]
> Training Distribution
> | First slot in `propagation_order` | Rows |
> |---|---:|
> | `A` | 49 |
> | `B` | 50 |
> | `C` | 56 |
> | `D` | 57 |
> | `E` | 61 |
> | `F` | 54 |
> | `G` | 53 |
> | Contingency value | Training entries |
> |---|---:|
> | `0` | 380 |
> | `1` | 387 |
> | `2` | 530 |
> | `3` | 223 |
> Every row has exactly one 0 because each packet contains one singleton event with no failover backup.
> Submission Format
> Write the final file to ./working/submission.csv.
> It must contain exactly these columns in this order: case_id,propagation_order,uplink_program,failover_program,contingency_vector,drop_confidence_vector.
> All columns are strings at CSV level. propagation_order is limited to 13 characters, uplink_program to 52 characters, failover_program to 80 characters, contingency_vector to 20 characters, and drop_confidence_vector to 80 characters.
> Example submission row:
> | case_id | propagation_order | uplink_program | failover_program | contingency_vector | drop_confidence_vector |
> |---|---|---|---|---|---|
> | `u81dd13d38b756f8244b6fb` | `D>A>G>C>F>B>E` | `keep:D>keep:G>keep:C>keep:F>commit:compact` | `loss:D>A|loss:G>drop|loss:C>E|loss:F>B|commit:failsafe` | `[3,0,2,1]` | `[0.05,0.82,0.08,0.05]` |
> Extra or reordered columns, duplicate column names, duplicate IDs, unknown IDs, and missing or extra rows are rejected. A malformed target receives zero for its component and does not crash grading.
> Evaluation
> The metric is the Loss-Contingency Relay Score. Higher is better.
> Minimum score: 0.0
> Maximum score: 1.0
> Propagation Order Score
> For every one of the 21 unordered slot pairs, test whether the predicted order agrees with the true order.
> PairAgreement is correct ordered slot pairs / 21.
> PropagationOrderScore is 0.35 * PairAgreement + 0.65 * I(the complete seven-slot order is exact).
> Uplink Program Score
> SetF1 compares the four kept labels as sets. RelativeAgreement compares the order of every pair of labels that appears in both programs. RelativeAgreement is 0 when fewer than two labels are shared.
> UplinkProgramScore is 0.25 * SetF1 + 0.20 * RelativeAgreement + 0.55 * I(the complete keep sequence is exact).
> Failover Program Score
> SourceF1 compares the four transmitted loss sources as sets. TargetAccuracy is the fraction of shared loss sources whose replacement target is exact.
> FailoverProgramScore is 0.30 * SourceF1 + 0.25 * TargetAccuracy + 0.45 * I(the complete failover program is exact).
> Contingency Vector Score
> For true vector Y and predicted vector P, both of length four, BoundedAgreement is mean(max(0, 1 - abs(Y[i] - P[i]) / 3)).
> ContingencyVectorScore is 0.45 * BoundedAgreement + 0.55 * I(the complete contingency vector is exact).
> Drop Confidence Score
> Let k be the true position whose contingency value is 0. Let p_k be the normalized submitted probability at that position in drop_confidence_vector. The row confidence score is:
> DropConfidenceScore = clip(1 - (-log(p_k) / log(4)), 0, 1)
> Coherence And Final Score
> Coherent is 1 only when all submitted outputs agree with each other. The keep labels must equal the failover loss sources. The keep labels must follow the submitted propagation order. Exactly one failover target must be drop. Any non-drop failover target must not itself be transmitted and must be lower quality than the lost transmitted slot. The contingency vector must equal the quality-gap buckets implied by the submitted propagation order and failover program.
> For each case, base score is:
> base =
> 0.24 * PropagationOrderScore
> + 0.18 * UplinkProgramScore
> + 0.28 * FailoverProgramScore
> + 0.20 * ContingencyVectorScore
> + 0.10 * DropConfidenceScore
> The case score is base * (0.82 + 0.18 * Coherent).
> The final score is mean(case score over all hidden test cases).
> Hidden answers are validated strictly. They are never clipped, filled, reordered, or repaired.
> What Makes This Interesting
> The task asks for a counterfactual recovery plan, not just a recognition label or duplicate map. A solver must infer which slots are redundant, choose a bandwidth-limited schedule, identify which transmitted slot has no recovery path, and calculate how severe each possible loss is from the acoustic quality order.
> The contingency vector makes the output more than a set-cover solution. Two schedules can preserve the same four events before failure but have different resilience after a dropped transmission. A backup that is acoustically close to the primary is a stronger recovery option than a heavily degraded backup, and the score checks that distinction.
> The central reasoning object is a failure-aware relay contract for edge monitoring. It combines acoustic grouping, propagation-quality ranking, budgeted transmission, single-loss replacement, and quality-gap bucketing in one executable certificate. This separates it from bird activity detection, acoustic event localization, ordinary duplicate detection, and species classification.
> What Not To Use
> Do not map IDs, filenames, row order, media size, or split position to outputs.
> Do not identify recordings by matching them against external copies, fingerprints, or recovered source filenames.
> Do not use external song, distance, habitat, or source-split annotations during inference.
> Do not exploit malformed CSV behavior, duplicate rows, parser limits, or grader exceptions.
> Do not adapt predictions using hidden labels or leaderboard feedback.
> Audio embeddings, signal processing, constrained clustering, ranking, GPU-accelerated representation models, and deterministic relay optimization are allowed.
> Reference Validation
> Release checks include two byte-identical prepares, disjoint train and test source performances, maximum source recording reuse of 4, zero public media duplicate hashes, exact score 1.0, strict schema attacks, and low shortcut baselines. The fixed relay sample scores 0.189336. Validation numbers are recorded in validation_report.json after each rebuild.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Multimodal Upper-Limb Motion Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c42zsh4qf5jp9ne09dvb6w189zjgv
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Each case is a synchronized recording of a human participant performing an upper-limb reaching movement. B-mode ultrasound observes deformation inside the upper arm, while three EMG channels measure muscle activation, three triaxial accelerometers measure local motion, and sparse motion-capture anchors describe external limb kinematics. This kind of multimodal recovery is useful in movement science and rehabilitation measurement when internal tissue motion must be inferred despite incomplete or obscured ultrasound observations.
> You receive a 16 x 96 x 96 partially masked ultrasound sequence, 64 samples from each anonymous EMG and accelerometer stream, five sparse motion-capture anchors, normalized row-local timestamps, and the visible-pixel mask. The channels and anchors are shuffled independently for every case. The concrete objective is to predict all 16 frames of the 11 hidden tissue-landmark trajectories, recover which anatomical site produced each anonymous sensor stream, and label the five synchronized reach/tremor event tracks.
> Task
> For every test case, submit one compressed tensor payload containing:
> Output	What it represents
> track_xy	11 tissue-landmark paths
> sensor_site	sensor-to-site assignments
> event_bits	reach/tremor event sequence
> track_xy is a float array with shape (16, 11, 2). Coordinates are normalized row-local image coordinates in [0, 1]; the landmark order is stable across rows. sensor_site is an integer array with shape (2, 3). Row 0 maps the three anonymous EMG channels to site codes and row 1 maps the three anonymous accelerometer channels. Site code 0 is triceps, 1 is biceps, and 2 is palm; each row must be a permutation of [0, 1, 2]. event_bits is a binary array with shape (16, 5). Its columns, in order, are extension, retraction, triceps tremor, biceps tremor, and palm tremor.
> This is not whole-clip classification, scalar motion regression, event counting, or source lookup. A useful solution must combine visual ultrasound evidence with the shuffled biosignals and sparse motion anchors. Copying a mean trajectory, predicting no events, or using only channel order leaves most of the score unused.
> Train, validation, and test are participant-disjoint: no person's clips cross splits. The test set therefore measures generalization to unseen movement patterns and anatomy while retaining the same learnable sensor, landmark, and event definitions shown in training.
> Intended Approach And Validation
> Train only on the provided public training rows, using the validation rows for model selection and ablations. Appropriate solutions include compact video encoders, 2D/3D CNNs, temporal transformers, multimodal fusion networks, or physics-guided sequence models. A practical GPU route is to encode the 16 x 96 x 96 ultrasound clip, fuse it with EMG, accelerometer, and anchor features, and train multi-head losses for trajectories, site assignment, and event bits. Keep training and inference within the 1.5 hour platform limit.
> Strong solutions should check modality ablations. Ultrasound alone should recover some visible motion, sensors alone should recover movement timing and site hints, and fused models should do better on held-out participants. Public validation should be used as a participant-disjoint development set, not as an additional source of hidden test labels.
> What Not To Do
> Using any of the approaches below can cause rejection regardless of leaderboard score.
> Do not use source lookup, reverse video search, media fingerprinting against public archives, raw filenames, original timestamps, participant identities, demographics, source paths, or source ordering.
> Do not use internet access, hosted APIs, closed remote inference services, or private files at inference time.
> Do not download model weights at runtime or use challenge-specific checkpoints trained on the upstream recordings. Generic offline pretrained visual backbones are allowed when bundled with the solution and used within the runtime limit.
> Do not read or infer hidden labels, hidden manifests, grader internals, file mtimes, archive offsets, or row order.
> Do not reduce the task to whole-clip labels, scalar arm-speed regression, channel-order heuristics, or always-no-event rules.
> Do not submit malformed base64, wrong NPZ keys, wrong shapes, out-of-range coordinates, duplicate IDs, missing IDs, extra IDs, NaN/Inf values, or non-one-to-one sensor assignments.
> Enforcement on invalid approaches: submissions that rely on lookup, private files, remote services, hard-coded IDs, or rule-only shortcuts that do not solve the multimodal recovery task may be rejected before payout even if the CSV parses.
> Evaluation
> Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. A perfect private-label submission with confidence 1.0 scores exactly 1.0.
> The grader first validates the CSV structure. The submission must have exactly these columns in this order:
> case_id,prediction_npz_b64,confidence
> The ID set must exactly match test.csv, with no duplicates, missing IDs, or extra IDs. confidence must be finite and in [0, 1]. Structural CSV failures raise InvalidSubmissionError. Row-local corrupt or oversized NPZ payloads receive zero for that row and do not crash the grader.
> The prediction NPZ must contain exactly:
> track_xy     float, shape (16,11,2), range [0,1]
> sensor_site  integer, shape (2,3), permutations
> event_bits   integer, shape (16,5), values 0 or 1
> All means below are arithmetic means over the stated frames, landmarks, edges, or event cells. I(condition) is 1 when the condition is true and 0 otherwise. Every component is in [0, 1].
> For track_score, let p[t,j] and g[t,j] be the predicted and true 2D coordinates for frame t and landmark j:
> d[t,j] = ||p[t,j] - g[t,j]||_2
> point_similarity = mean(exp(-(d[t,j] / 0.055)^2))
> dv[t,j] = ||(p[t+1,j] - p[t,j]) - (g[t+1,j] - g[t,j])||_2
> velocity_similarity = mean(exp(-(dv[t,j] / 0.040)^2))
> track_score = 0.76*point_similarity + 0.24*velocity_similarity
> For sensor_score, all six channel-to-site assignments are compared directly:
> sensor_score = mean(I(predicted_site == true_site))
> For each event column that contains at least one true positive frame, compute its positive-class F1 as 2*TP / (2*TP + FP + FN); a column with no true positives is omitted from this macro average. If every true event column is empty, positive_event_f1 is 1 only when the prediction is also entirely empty, otherwise 0. Specificity is computed over all event cells:
> specificity = 1 - total_false_positive_event_cells / total_true_negative_event_cells
> event_score = 0.85*positive_event_f1 + 0.15*specificity
> If there are no true-negative event cells, specificity is defined as 1.
> For consistency_score, the fixed landmark-edge set is (0,1), (1,2), (2,3), (4,5), (5,6), (6,7), (8,9), (9,10), (2,8), (6,8). Let L_pred[t,e] and L_true[t,e] be the predicted and true edge lengths:
> topology = mean(exp(-(|L_pred[t,e] - L_true[t,e]| / 0.045)^2))
> pred_motion[t] = ||mean_j(p[t+1,j]) - mean_j(p[t,j])||_2
> true_motion[t] = ||mean_j(g[t+1,j]) - mean_j(g[t,j])||_2
> motion = 0.5 + 0.5*clip(PearsonCorr(pred_motion, true_motion), -1, 1)
> event_agreement = mean(I(predicted_event_bit == true_event_bit))
> consistency_score = 0.58*topology + 0.30*motion + 0.12*event_agreement
> When either motion sequence has standard deviation below 1e-6, motion is defined as 0. The four task heads form row_core:
> row_core = 0.48*track_score
> + 0.18*sensor_score
> + 0.20*event_score
> + 0.14*consistency_score
> calibration = max(0, 1 - abs(confidence - row_core))
> row_score = row_core * (0.95 + 0.05*calibration)
> Confidence can only preserve or slightly reduce earned task credit; it cannot add credit to a wrong prediction. A row with row_core = 0 scores zero at every confidence.
> Let R_i be each row score, and let G_k be the mean row score within hidden participant group k. The final score blends overall quality with the weakest held-out participant group:
> mean_row_score = mean_i(R_i)
> worst_group_score = min_k(G_k)
> final = 0.90*mean_row_score + 0.10*worst_group_score
> Hidden groups are participant-disjoint source families. This discourages overfitting one participant's motion style while still rewarding learnable multimodal structure. The confidence column is strictly validated as finite and in [0, 1].
> Dataset
> The public split contains source-neutral prepared clips only. It does not expose raw participant IDs, raw filenames, source paths, original timestamps, demographics, checksums, split construction metadata, or private answer metadata.
> Default preparation uses participant-disjoint train, validation, and test splits. Local real-subset smoke preparation produced 2 train, 2 validation, and 2 test rows from three source records. Full platform preparation uses all eligible records unless a record is skipped for missing required streams.
> File overview
> Item	Description
> train.csv	labeled train rows
> validation.csv	labeled val rows
> test.csv	hidden test rows
> train/clips/*.npz	train inputs
> validation/clips/*.npz	val inputs
> test/clips/*.npz	test inputs
> train/targets/*.npz	train targets
> validation/targets/*.npz	val targets
> sample_submission.csv	weak template
> All paths are relative to the public dataset root.
> train.csv columns
> Column	Type	Description
> case_id	string	opaque case id
> input_npz_path	string	input NPZ path
> frame_count	int	always 16
> sensor_samples	int	always 64
> point_count	int	always 11
> event_count	int	always 5
> task_prompt	string	task reminder
> target_npz_path	string	target NPZ path
> validation.csv has the same columns and can be used for train-only validation.
> test.csv columns
> Column	Type	Description
> case_id	string	opaque case id
> input_npz_path	string	input NPZ path
> frame_count	int	always 16
> sensor_samples	int	always 64
> point_count	int	always 11
> event_count	int	always 5
> task_prompt	string	task reminder
> Test rows do not include target paths.
> Input NPZ contents
> Array	Shape	Description
> us_masked	(16,96,96)	masked video
> observed_mask	(96,96)	visible pixels
> emg_streams	(64,3)	privacy-filtered EMG
> acc_streams	(64,3,3)	privacy-filtered accel
> mocap_anchors	(16,5,3)	coarse motion anchors
> mocap_anchor_mask	(5,)	anchor validity
> clip_time	(16,)	row clock
> sensor_time	(64,)	sensor clock
> target NPZ contents
> Array	Shape	Description
> track_xy	(16,11,2)	tissue paths
> sensor_site	(2,3)	site graph
> event_bits	(16,5)	event sequence
> Submission
> Submit a CSV with exactly these columns in this order:
> case_id,prediction_npz_b64,confidence
> Column	Type	Constraint
> case_id	string	same set as test
> prediction_npz_b64	base64 NPZ	three arrays
> confidence	float	in [0,1]
> The supplied sample_submission.csv is a complete, valid, but weak submission with real base64 NPZ payloads for every test ID. Use it as the safest starting point. If the platform expects a path, write the final file to ./working/submission.csv.
> This format-only example creates a valid payload and complete CSV without abbreviated or placeholder base64. Replace the constant arrays with model predictions:
> import base64
> import io
> import numpy as np
> import pandas as pd
> def encode_prediction(track_xy, sensor_site, event_bits):
> buffer = io.BytesIO()
> np.savez_compressed(
> buffer,
> track_xy=np.asarray(track_xy, dtype=np.float32),
> sensor_site=np.asarray(sensor_site, dtype=np.uint8),
> event_bits=np.asarray(event_bits, dtype=np.uint8),
> )
> return base64.b64encode(buffer.getvalue()).decode("ascii")
> test = pd.read_csv("./dataset/public/test.csv")
> payload = encode_prediction(
> np.full((16, 11, 2), 0.5, dtype=np.float32),
> np.tile(np.arange(3, dtype=np.uint8), (2, 1)),
> np.zeros((16, 5), dtype=np.uint8),
> )
> submission = pd.DataFrame(
> {
> "case_id": test["case_id"],
> "prediction_npz_b64": [payload] * len(test),
> "confidence": np.full(len(test), 0.25),
> }
> )
> submission.to_csv("./working/submission.csv", index=False)

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Shuffled Multi-Channel Room Recording Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71h1v5zyh49btygy64thfpas8bkndw
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal, audio
- Best/top context found: Top Score | — | Created | Aug 1, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Repair a corrupted two-channel room-recording packet. Predict station_pairing, the four pairs recorded at the same receiver positions; synchronized_streams, the two recovered four-stop channel sequences; and decay_dominance_word, four comparisons of how slowly the paired responses decay.
> The real scenario is an indoor acoustic survey whose recorder export has lost channel identifiers, station identifiers, and timestamps. A moving platform sampled four nearby receiver positions through two acquisition channels, producing eight room impulse responses. The public evidence contains only a JPEG board and a WAV packet. The board displays the shuffled observations as panels A through H, and the WAV packet stores those same responses in label order.
> The goal is recording provenance repair, not coordinate estimation, room classification, or reconstruction of a single microphone path. A correct solution must compare decay curves and impulse traces, identify cross-channel twins, recover two anonymous interleaved streams up to their unavoidable channel-swap and direction symmetry, and compare decay within each recovered station pair.
> Compute Budget
> Solutions have one NVIDIA A10G GPU and at most 30 minutes of wall-clock time. Loading media, preprocessing, training, inference, search, decoding, and writing the submission all count toward this limit. The resource profile is intended for learned waveform and evidence-board encoders over all eight observations; the final pairing and stream search is small.
> Dataset
> The prepared release contains 1,100 training cases and 420 test cases. One complete recording environment is reserved for the hidden split, so no source scene contributes measurements to both training and test.
> Public identifiers and media names are opaque. They do not encode the environment, source position, channel pair, route start, or target values.
> Before the public evidence is created, every response receives a deterministic sub-percent time-scale perturbation, fractional-sample displacement, mild spectral tilt, polarity and gain variation, and low-amplitude sensor noise. The board, WAV packet, and labels are all derived after this transformation. This preserves the acoustic evidence needed for synchronization while preventing exact matching against the original measurement table.
> Files
> | Path | Contents |
> |---|---|
> | `public/train.csv` | Public inputs and all target columns for 1,100 labeled cases |
> | `public/test.csv` | Public inputs for 420 hidden-label cases |
> | `public/sample_submission.csv` | Schema-valid baseline submission |
> | `public/images/` | JPEG evidence boards referenced by the CSV files |
> | `public/audio/` | WAV packets carrying the eight impulse responses shown on each board |
> The CSV schemas are:
> | File | Columns in exact order |
> |---|---|
> | `public/train.csv` | `case_id`, `channel_board_path`, `rir_packet_path`, `station_pairing`, `synchronized_streams`, `decay_dominance_word` |
> | `public/test.csv` | `case_id`, `channel_board_path`, `rir_packet_path` |
> | `public/sample_submission.csv` | `case_id`, `station_pairing`, `synchronized_streams`, `decay_dominance_word` |
> Evidence Board
> Each evidence board is a 1200 x 760 JPEG with two rows of four rectangular station panels.
> Panels are labeled:
> A B C D
> E F G H
> The labels identify shuffled observations only. They do not reveal station pairing, acquisition channel, or stream order.
> Within every panel:
> the top plot shows normalized remaining acoustic energy over time as a teal decay curve;
> the bottom plot shows the normalized impulse response as a red waveform trace;
> the dark label block contains only the public station letter.
> The WAV packet follows label order A through H. A short marker and silence separate consecutive station responses so participants can segment the packet without relying on hidden offsets.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque row identifier matching `am[0-9a-f]{20}` |
> | `channel_board_path` | string path | Relative path to the eight-panel JPEG evidence board |
> | `rir_packet_path` | string path | Relative path to the 48 kHz mono WAV packet |
> Target Columns
> | Column | Data type | Meaning and valid form |
> |---|---|---|
> | `station_pairing` | unordered pair-set string | Four `A~B` style pairs separated by `|`; every label `A` through `H` appears exactly once |
> | `synchronized_streams` | canonical two-stream string | Two four-label streams separated by `/`, with labels inside each stream joined by `>` |
> | `decay_dominance_word` | binary word string | `b` followed by four bits, one bit per paired station in synchronized-stream order |
> Example labeled row:
> case_id,channel_board_path,rir_packet_path,station_pairing,synchronized_streams,decay_dominance_word
> am0123456789abcdefabcd,images/am0123456789abcdefabcd.jpg,audio/am0123456789abcdefabcd.wav,A~F|B~H|C~D|E~G,A>B>C>E/F>H>D>G,b1010
> Target Semantics
> Station Pairing
> station_pairing identifies the four cross-channel observation pairs that came from the same physical receiver station. The order of pairs is ignored, and the order of the two endpoints inside each pair is ignored.
> Valid example:
> A~F|B~H|C~D|E~G
> Invalid examples include repeated labels, missing labels, self-pairs, more or fewer than four pairs, and labels outside A through H. The maximum accepted length is 31 characters.
> Synchronized Streams
> synchronized_streams reconstructs the two acquisition-channel paths through the same four receiver stations. Each side of / is one channel stream. Every label A through H must appear exactly once.
> Valid example:
> A>B>C>E/F>H>D>G
> The physical channel names and route direction are not public, so the grader canonicalizes equivalent forms. Swapping the two streams or reversing both streams represents the same answer. The maximum accepted length is 31 characters.
> Decay Dominance Word
> decay_dominance_word has the form:
> b<bit1><bit2><bit3><bit4>
> The four bits follow the paired stations in canonical synchronized-stream order. At each paired station:
> 1 means the first stream label has slower average decay than the paired second stream label;
> 0 means the second stream label has equal or slower average decay.
> Example:
> b1010
> The value must match ^b[01]{4}$.
> Target Distribution
> | Statistic | Train | Test |
> |---|---:|---:|
> | Unique station-pairing strings | 105 | 103 |
> | Unique synchronized-stream strings | 1,031 | 412 |
> Decay-word counts:
> | Word | Train | Test |
> |---|---:|---:|
> | `b0000` | 350 | 151 |
> | `b0001` | 32 | 19 |
> | `b0010` | 26 | 6 |
> | `b0011` | 28 | 11 |
> | `b0100` | 24 | 4 |
> | `b0101` | 11 | 3 |
> | `b0110` | 16 | 5 |
> | `b0111` | 37 | 15 |
> | `b1000` | 43 | 14 |
> | `b1001` | 17 | 5 |
> | `b1010` | 9 | 5 |
> | `b1011` | 26 | 6 |
> | `b1100` | 34 | 8 |
> | `b1101` | 26 | 10 |
> | `b1110` | 44 | 14 |
> | `b1111` | 377 | 144 |
> Reference Construction
> Each case uses four consecutive receiver positions and two different acquisition-channel configurations. This creates two responses at every position. The eight responses are transformed, assigned random public labels, and shuffled before rendering.
> station_pairing connects the two labels originating from the same receiver position. Private receiver coordinates define the shortest path through the four positions. Reading each hardware channel along that common path gives the two chains in synchronized_streams.
> Channel identity and travel direction are treated as gauge choices. The reference compares the original chains, both reversed chains, swapped chains, and swapped-reversed chains, then stores the lexicographically smallest serialization.
> For decay_dominance_word, remaining acoustic energy is accumulated backward from the end of each response and normalized to start at one. The reference samples 96 late-time positions:
> decay_score = mean(log10(normalized_remaining_energy))
> A larger score indicates slower decay. Each bit compares the first and second streams at one position after canonicalization.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> The file must contain exactly these columns in this order:
> case_id,station_pairing,synchronized_streams,decay_dominance_word
> Example:
> case_id,station_pairing,synchronized_streams,decay_dominance_word
> am0123456789abcdefabcd,A~F|B~H|C~D|E~G,A>B>C>E/F>H>D>G,b1010
> Submission requirements:
> Include exactly one row for every hidden case_id.
> Extra, missing, or reordered columns are rejected.
> Duplicate, missing, malformed, and unknown identifiers are rejected.
> A single backend-managed visibility column is accepted and removed before schema validation.
> Malformed target values receive zero credit for the affected target component.
> Overlong strings are rejected by the target parser and receive zero for that component.
> Evaluation
> Submissions are evaluated with the Acoustic Channel Synchronization Score:
> Score =
> 0.34 * StationPairingScore
> + 0.43 * StreamSynchronizationScore
> + 0.23 * DecayDominanceScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> The grader computes all three row-level component scores and then averages over the hidden cases.
> StationPairingScore
> Pair strings are parsed into an unordered set of four unordered pairs. Let Y be the true pair set and P be the predicted pair set.
> pair_F1 =
> 2 * |Y intersection P| / (|Y| + |P|)
> exact_pairing =
> 1 if Y equals P
> 0 otherwise
> row_pairing_score =
> 0.38 * pair_F1
> + 0.62 * exact_pairing
> StreamSynchronizationScore
> Each submitted stream value is parsed into two four-label chains. The grader canonicalizes equivalent forms by allowing a swap of the two chains and simultaneous reversal of both chains. It then compares both the exact canonical streams and the local adjacency edges within those streams.
> Let E_true and E_pred be the unordered adjacent-label edge sets induced by the two true and predicted streams.
> edge_F1 =
> 2 * |E_true intersection E_pred| / (|E_true| + |E_pred|)
> exact_streams =
> 1 if the canonical two-stream values match exactly
> 0 otherwise
> row_stream_score =
> 0.28 * edge_F1
> + 0.72 * exact_streams
> DecayDominanceScore
> For the four bits after the leading b:
> bit_accuracy =
> number of matching bit positions / 4
> exact_word =
> 1 if all four bits match
> 0 otherwise
> row_word_score =
> 0.25 * bit_accuracy
> + 0.75 * exact_word
> Malformed pair strings, malformed stream strings, invalid labels, repeated labels, overlong strings, and invalid decay words receive zero for the affected component. Schema-valid malformed submissions always receive a finite score.
> Reference Validation
> | Check | Result |
> |---|---:|
> | Exact hidden-answer submission | `1.000000` |
> | Packaged sample submission | `0.137885` |
> | Frequent-target constant submission | `0.134736` |
> | Global stream-swap plus reversal of exact answers | `1.000000` |
> | Prepared image files | `1,520` |
> | Prepared audio files | `1,520` |
> | Source-scene overlap between train and test | `0` |
> | Deterministic clean rebuild | yes |
> Expected And Allowed Methods
> Suitable approaches include audio encoders, image encoders, decay-curve descriptors, waveform descriptors, learned pairwise station compatibility, graph matching, two-stream sequence search, and constrained structured decoding. Mixed precision and pretrained backbones are allowed when the complete pipeline stays within the 30-minute A10G budget.
> What Not To Use
> Do not use identifiers, media names, CSV order, file sizes, hashes, or archive offsets as predictive features.
> Do not locate packets in external archives or match them to published receiver positions.
> Do not use source coordinates, environment names, loudspeaker IDs, receiver-channel IDs, source-row indices, private feature tables, or hidden answers during inference.
> Do not exploit stream reversal, malformed pair sets, duplicate rows, extra columns, oversized strings, or grader exceptions.
> Do not train, calibrate, pseudo-label, or select thresholds using hidden test cases.
> What Makes This Interesting
> Ordinary acoustic localization starts with known channel identities or seeks physical coordinates. Here, those identities are themselves missing. The solver must restore the provenance structure of an interleaved recorder export before any channel-level comparison is meaningful.
> The three outputs constrain one another but are not interchangeable. A correct pair set can still assign observations to the wrong stream order, and a correct stream can still produce the wrong decay dominance word. The accepted gauge equivalence also prevents the task from rewarding an arbitrary choice of channel name or travel direction.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Wearable Sensor Episode Chronology Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f8pv5d87hcm29jkzxj6ma018b3mja
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio, multimodal, text
- Best/top context found: Top Score | — | Created | Jul 24, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Reconstruct the original time order of five shuffled wearable-sensor windows, recover the animal's behavior sequence in that order, and identify every behavior transition between adjacent windows. Each case supplies one audio montage and one motion-trace image containing the same five synchronized windows in the same shuffled slot order.
> The local slots are named S1 through S5. Each slot contains 4.9 seconds of collar microphone audio and the matching triaxial accelerometer trace. The five windows came from one animal over a short observation interval, but their chronology has been removed. The submission must recover the complete order rather than predict each slot independently.
> This represents a practical failure in field telemetry. Sensor payloads can reach storage with intact records but damaged sequence metadata after buffering, packet retries, or database merges. Correct ordering matters because walking followed by drinking is not equivalent to drinking followed by walking, and a long stable episode should not be split by an incorrectly inserted window.
> Chronology is recoverable from cross-window continuity. Adjacent records can share acoustic background, ongoing chewing or footfall rhythm, and acceleration trajectories that continue across a boundary. Both modalities are useful: audio captures environmental and impact continuity, while motion captures body-state continuity and repeated movement patterns.
> Ground truth comes from source timestamps before the local slot names and order are randomized. Training and test use disjoint collar or animal groups. Raw timestamps, source window numbers, and source filenames are not exposed. The challenge is designed for A10G GPU inference.
> Dataset
> The release contains 500 labeled training episodes and 400 hidden test episodes.
> | Path | Contents |
> |---|---|
> | `train.csv` | Four input columns and four target columns for 500 episodes |
> | `test.csv` | The four input columns for 400 episodes |
> | `sample_submission.csv` | A schema-valid fixed-order baseline |
> | `audio/` | 900 opaque MP3 montages, one per row |
> | `motion/` | 900 opaque five-panel JPEG images, one per row |
> Media Features
> | Feature | Data type | Description |
> |---|---|---|
> | Audio montage | mono MP3 waveform | Five consecutive 4.9-second microphone slots, for 24.5 seconds of logical signal. MP3 encoder padding can make the container duration report approximately 24.588 seconds. |
> | Audio slot timing | fixed interval | `S1` occupies seconds 0 to 4.9, followed by `S2`, `S3`, `S4`, and `S5` |
> | Motion image | 1000 x 650 RGB JPEG | Five stacked panels corresponding to audio slots `S1` through `S5` |
> | Motion panel traces | three normalized curves | The three accelerometer axes over 100 samples. Time runs from left to right. Axis order and sign are stable within a packet but may vary between packets. |
> | Observable content | multimodal sensor evidence | Chewing and drinking rhythms, steps, impacts, resting motion, environmental sound, pauses, and continuity across neighboring source windows |
> Input Columns
> | Column | Data type | Present in | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque identifier beginning with `q` followed by 22 hexadecimal characters |
> | `audio_path` | string | train, test | Relative path to the 24.5-second audio montage |
> | `motion_path` | string | train, test | Relative path to the corresponding five-panel motion image |
> | `episode_contract` | string | train, test | Fixed value `five synchronized 4.9-second slots S1..S5 presented out of time order` |
> Target Columns
> | Column | Data type | Present in | Description |
> |---|---|---|---|
> | `chronology_program` | canonical token string | train | The five local slots in original chronological order, followed by `commit:episode` |
> | `chronology_matrix` | JSON-encoded integer matrix | train | A `5 x 5` pairwise before-after certificate over local slots |
> | `behavior_sequence` | categorical token sequence | train | Five behavior labels in recovered chronological order |
> | `transition_edge_set` | canonical token set | train | Every adjacent chronological edge where the behavior changes, or `none` |
> Chronology Program
> The program contains each of S1, S2, S3, S4, and S5 exactly once, ordered from earliest to latest, followed by commit:episode.
> S4>S1>S5>S2>S3>commit:episode
> Chronology Matrix
> Rows and columns follow fixed local-slot order S1, S2, S3, S4, S5.
> | Value | Meaning for matrix entry `[row,column]` |
> |---:|---|
> | `1` | The row slot occurred before the column slot |
> | `0` | Row and column are the same slot |
> | `-1` | The row slot occurred after the column slot |
> The matrix must have zeros on its diagonal and must be antisymmetric, so M[i,j] = -M[j,i].
> Example for chronology S1>S2>S3>S4>S5:
> [[0,1,1,1,1],[-1,0,1,1,1],[-1,-1,0,1,1],[-1,-1,-1,0,1],[-1,-1,-1,-1,0]]
> Behavior Sequence
> The sequence has five >-separated labels in recovered chronological order. Valid labels are drinking, walking, eating, and lying.
> lying>lying>walking>drinking>drinking
> Transition Edge Set
> Emit one token for every adjacent chronology edge whose behavior changes. The grammar is:
> EARLIER->LATER:OLD_BEHAVIOR~NEW_BEHAVIOR
> Tokens follow chronological order and use | as the delimiter. If no behavior changes, submit none.
> Example consistent with chronology S4>S1>S5>S2>S3 and behavior sequence lying>lying>walking>drinking>drinking:
> S1->S5:lying~walking|S5->S2:walking~drinking
> Training Distribution
> | Number of behavior-changing edges | Training episodes |
> |---:|---:|
> | `0` | 370 |
> | `1` | 87 |
> | `2` | 38 |
> | `3` | 4 |
> | `4` | 1 |
> Across all 2,500 training positions, lying occurs 1,109 times, eating 1,025 times, walking 200 times, and drinking 166 times.
> Example labeled record:
> | case_id | audio_path | motion_path | episode_contract | chronology_program | chronology_matrix | behavior_sequence | transition_edge_set |
> |---|---|---|---|---|---|---|---|
> | `qb8e599d348404e072af7ea` | `audio/ca2d5cf74471bea88eb4c20b.mp3` | `motion/cfae53373e3ba9dfbfe576f4.jpg` | `five synchronized 4.9-second slots S1..S5 presented out of time order` | `S3>S1>S4>S2>S5>commit:episode` | `[[0,1,-1,1,1],[-1,0,-1,-1,1],[1,1,0,1,1],[-1,1,-1,0,1],[-1,-1,-1,-1,0]]` | `walking>lying>lying>lying>lying` | `S3->S1:walking~lying` |
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,chronology_program,chronology_matrix,behavior_sequence,transition_edge_set
> All columns are strings at CSV level. chronology_program is limited to 70 characters. chronology_matrix is limited to 130 characters and must decode to a valid 5 x 5 antisymmetric integer matrix using only -1, 0, and 1. behavior_sequence is limited to 60 characters. transition_edge_set is limited to 220 characters and at most four unique transition tokens.
> Example submission:
> case_id,chronology_program,chronology_matrix,behavior_sequence,transition_edge_set
> qb8e599d348404e072af7ea,S3>S1>S4>S2>S5>commit:episode,"[[0,1,-1,1,1],[-1,0,-1,-1,1],[1,1,0,1,1],[-1,1,-1,0,1],[-1,-1,-1,-1,0]]",walking>lying>lying>lying>lying,S3->S1:walking~lying
> Extra or reordered columns, duplicate column names, duplicate IDs, unknown IDs, and missing or extra rows are rejected. An optional platform-managed visibility column is removed before schema validation. Malformed target values score zero for their component without causing a grader failure.
> Evaluation
> The metric is the Wearable Episode Chronology Score. Higher is better.
> Minimum score: 0.0
> Maximum score: 1.0
> Let I(condition) equal 1 when the condition is true and 0 otherwise.
> Chronology Score
> The recovered order defines four directed adjacent edges. For true adjacent-edge set Y and predicted set P:
> AdjacentEdgeF1 = 2 * |Y intersect P| / (|Y| + |P|)
> PairAgreement = number of equal entries in the two 5 x 5 matrices / 25
> ChronologyExact = I(the order and complete matrix are both exact)
> ChronologyScore = 0.25 * AdjacentEdgeF1 + 0.25 * PairAgreement + 0.50 * ChronologyExact
> Behavior Score
> BehaviorEntryAgreement is the fraction of the five chronological positions with the correct activity.
> BehaviorScore = 0.35 * BehaviorEntryAgreement + 0.65 * I(the complete behavior sequence is exact)
> Transition Score
> Treat transition tokens as a set. When both true and predicted sets are empty, their set F1 is 1. When exactly one is empty, it is 0.
> TransitionScore = 0.40 * TransitionSetF1 + 0.60 * I(the complete ordered transition token sequence is exact)
> Coherence And Final Score
> Coherent is 1 only when the submitted matrix is exactly implied by the submitted order and the submitted transition tokens are exactly implied by the submitted order plus behavior sequence.
> BaseScore = 0.60 * ChronologyScore + 0.25 * BehaviorScore + 0.15 * TransitionScore
> case_score = BaseScore * (0.88 + 0.12 * Coherent)
> FinalScore = mean(case_score over all hidden episodes)
> Hidden values are validated strictly and are never clipped, repaired, or reordered.
> What Makes This Interesting
> The task asks for temporal restoration, not audio-motion matching. Audio and acceleration already belong to the same slot. The unknown is the global order of five intact multimodal records. This makes cross-window continuity more important than broad activity recognition.
> A strong solution must combine local evidence and global constraints. Pairwise continuity estimates can conflict, so the final answer must be one valid total order. The behavior and transition outputs then test whether the recovered order supports the correct episode narrative rather than merely a plausible permutation.
> What Not To Use
> Do not map opaque IDs, row order, filenames, file sizes, or media encoding details to chronology or behavior outputs.
> Do not reverse-search public media to recover source timestamps, source window identifiers, collar identifiers, or annotation rows.
> Do not use external source manifests or timestamp tables at inference time.
> Do not exploit duplicate submissions, malformed CSV behavior, parser limits, or grader exceptions.
> Do not tune against hidden answers or use leaderboard probing as per-case supervision.
> GPU-based audio encoders, image models, multimodal fusion, sequence models, signal processing, and constrained ordering algorithms are allowed.
> Reference Validation
> The release contains 500 training episodes and 400 hidden episodes from disjoint collar groups. It has 900 unique audio hashes and 900 unique motion-image hashes. Exact hidden answers score 1.0; the fixed-order sample scores 0.36526875. Giving that baseline the correct behavior sequence while leaving chronology fixed reaches 0.4647916, so activity recognition alone remains below 0.5.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Spoken Command Queue Compilation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77jb1sk01v7f36emp2jh4qad8ap9jf
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, text, audio, multimodal
- Best/top context found: Top Score | — | Created | Jul 17, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Each example contains a short audio mixture and a visual control card. Exactly three Arabic commands are spoken in the audio, with overlapping start times and natural background sound. The card contains five abstract command glyphs arranged into priority lanes. Three glyphs correspond to the spoken commands and two are decoys. Some lanes are marked HOLD.
> Predict one complete controller decision:
> Decode the three spoken command IDs in onset order.
> Match those commands to the five card glyphs.
> Apply lane priority and HOLD marks to compile the execution tape.
> Describe the temporal relation among the three utterances.
> Report the final controller state.
> The three submitted outputs are:
> | Output | Meaning |
> |---|---|
> | `execution_tape` | Ordered decode and queue program |
> | `acoustic_overlap_matrix` | `3 x 3` relation matrix for the decoded utterances |
> | `controller_state` | `clear`, `deferred`, or `locked` according to active `HOLD` decisions |
> This is not ordinary keyword classification. A correct solution must combine speech recognition, onset reasoning, visual symbol matching, decoy rejection, and priority scheduling. The same command glyph is stable across examples, but command names are not printed on the policy card.
> The challenge is intended for A10G GPU execution. Larger audio encoders, spectrogram or waveform models, image encoders for the policy cards, and constrained structured decoders are appropriate.
> Real-World Motivation
> Voice-controlled equipment may hear several operators at once while a separate control panel defines which actions are currently permitted. A speech recognizer alone cannot decide what should execute. It must connect each utterance to the panel symbol, reject irrelevant panel entries, respect priority order, and preserve a trace of suppressed actions.
> This benchmark models that arbitration problem. It uses real one-second command recordings from 30 contributors and real background recordings. The visual control cards and mixtures are prepared deterministically for the challenge. Complete speakers are held out from training, and no exact three-command combination is shared across train and test.
> Dataset
> The prepared data contains 3,000 training examples and 750 test examples. Public media filenames and row identifiers are opaque.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public inputs and all target columns for 3,000 examples |
> | `test.csv` | Public inputs for 750 hidden-label examples |
> | `sample_submission.csv` | Schema-valid constant baseline |
> | `audio/` | Mono WAV command mixtures |
> | `policy_cards/` | RGB PNG control cards |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier matching `^aq[0-9a-f]{22}$` |
> | `audio_path` | string path | Relative path to a prepared WAV mixture |
> | `policy_card_path` | string path | Relative path to the five-lane PNG card |
> | `scheduling_contract` | string | Concise statement that three commands are active, two card glyphs are decoys, and lane order precedes `HOLD` handling |
> Audio Mixtures
> | Property | Value |
> |---|---|
> | Encoding | Mono 16-bit PCM WAV |
> | Sample rate | 16,000 Hz |
> | Duration | 1.2 to 1.5 seconds |
> | Spoken sources | Three different command classes |
> | Start positions | Three distinct offsets selected from 0.0, 0.1, 0.2, 0.3, and 0.4 seconds |
> | Background | Low-level segment from a real environmental or household recording |
> Each spoken command has a stable code from c00 through c39. The codes are categorical identifiers, not numeric measurements. Training targets provide supervision for the sound-to-code mapping.
> Policy Cards
> Each 720 x 520 card has five rows. The top row has highest execution priority. Every row contains:
> a stable 5 x 5 command glyph;
> a RUN or HOLD marker;
> its lane number.
> Only glyphs associated with the three spoken command codes participate in the output. A HOLD on either decoy does not affect the controller state.
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `execution_tape` | canonical string with seven tokens | Three `hear` tokens, three lane-ordered outcome tokens, and one commit token |
> | `acoustic_overlap_matrix` | JSON `3 x 3` integer matrix | Pairwise onset and strong-overlap relations in `hear` token order |
> | `controller_state` | categorical string | `clear`, `deferred`, or `locked` |
> Execution Tape Grammar
> The tape contains exactly seven >-separated tokens:
> hear:<command>>hear:<command>>hear:<command>>
> <outcome>:<command>><outcome>:<command>><outcome>:<command>>
> commit:queue
> Line breaks above are explanatory only. A submission uses one continuous string.
> The first three tokens list the spoken command codes from earliest to latest onset:
> hear:c07
> The next three tokens list only those same commands in card-lane order:
> run:c07
> drop:c19
> Use drop when the active command glyph has HOLD; otherwise use run. The three command codes must be unique. The outcome tokens must contain exactly the same three codes as the hear tokens. At most two outcome tokens may use drop; a three-drop tape is outside the valid grammar.
> A complete tape is:
> hear:c07>hear:c19>hear:c03>drop:c19>run:c03>run:c07>commit:queue
> The maximum accepted tape length is 180 characters.
> Acoustic Overlap Matrix
> Rows and columns follow the three hear tokens. Diagonal entries are always 0.
> For commands i and j:
> If their overlap is at least 72 percent of one command duration, both entries are 2.
> Otherwise, the earlier command has value 1 toward the later command.
> The later command has value -1 toward the earlier command.
> Thus every off-diagonal pair must be either (2, 2), (1, -1), or (-1, 1). The JSON string is limited to 100 characters.
> Example:
> [[0,2,1],[2,0,1],[-1,-1,0]]
> Controller State
> The state depends only on spoken commands whose card row has HOLD:
> | Active held commands | State |
> |---:|---|
> | 0 | `clear` |
> | 1 | `deferred` |
> | 2 | `locked` |
> Split Isolation And Distribution
> Twenty-four contributors supply training utterances. Six different contributors supply all test utterances. Source command recordings are not reused. Exact unordered three-command combinations are also disjoint between train and test.
> Command-code frequencies range from 208 to 240 in training and from 44 to 60 in test.
> | Split | `clear` | `deferred` | `locked` |
> |---|---:|---:|---:|
> | Train | 1,008 | 1,324 | 668 |
> | Test | 269 | 317 | 164 |
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in exactly this order:
> case_id,execution_tape,acoustic_overlap_matrix,controller_state
> Every test case_id must appear once. Extra columns, reordered columns, duplicate IDs, unknown IDs, missing rows, and extra rows are rejected.
> Example:
> case_id,execution_tape,acoustic_overlap_matrix,controller_state
> aq05cae2be991a3c72678d42,hear:c07>hear:c19>hear:c03>drop:c19>run:c03>run:c07>commit:queue,"[[0,2,1],[2,0,1],[-1,-1,0]]",deferred
> Evaluation
> Submissions are evaluated with the Cross-Modal Queue Certificate Score:
> BaseRowScore =
> 0.50 * TapeScore
> + 0.32 * OverlapMatrixScore
> + 0.18 * ControllerStateScore
> The final score is the mean adjusted row score. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> TapeScore
> The commit token is validated and then omitted from the comparison. Let T and P be the six remaining true and predicted tokens.
> edit_similarity =
> 1 - token_Levenshtein_distance(T, P) / max(|T|, |P|, 1)
> action_F1 =
> 2 * |set(true outcome tokens) intersection set(predicted outcome tokens)|
> / (|true outcome token set| + |predicted outcome token set|)
> TapeScore =
> 0.80 * exact_tape
> + 0.08 * edit_similarity
> + 0.12 * action_F1
> exact_tape is 1 only when all six tokens match in order. Token Levenshtein insertion, deletion, and substitution each cost 1.
> OverlapMatrixScore
> entry_accuracy = matching matrix entries / 9
> exact_matrix = 1 if all nine entries match, else 0
> OverlapMatrixScore =
> 0.18 * entry_accuracy
> + 0.82 * exact_matrix
> ControllerStateScore
> ControllerStateScore is 1 for an exact state match and 0 otherwise.
> Coherence Adjustment
> The submitted state must agree with the number of drop tokens:
> zero drops requires clear;
> one drop requires deferred;
> two drops requires locked.
> An incoherent or malformed row receives:
> AdjustedRowScore = 0.86 * BaseRowScore
> A coherent row keeps its full base score. Invalid token grammar, invalid command codes, repeated commands, overlong strings, invalid matrix shapes, and out-of-vocabulary states receive zero for the affected component. Schema-valid malformed submissions still receive a finite score.
> Reference validation:
> | Submission | Score |
> |---|---:|
> | Exact hidden answers | 1.000000 |
> | Constant sample submission | 0.099240 |
> Method Requirements
> The full solution may use the provided A10G GPU within the competition time limit. Training must use only the public training split. Test-time inference may read the public WAV and PNG files associated with each test row. Open-weight pretrained audio or vision encoders are allowed when they are run locally and fine-tuned or calibrated only on the public training data.
> What Not To Use
> Do not derive targets from case_id, media filenames, row order, file size, hashes, or archive order.
> Do not identify contributors or retrieve original recordings through external source matching.
> Do not use hidden answers, private files, grader internals, or platform feedback as supervision.
> Do not update model parameters from hidden test feedback or construct lookup tables for test rows.
> Do not exploit malformed CSV behavior, duplicate identifiers, extra columns, or parser resource exhaustion.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Dual-Cipher Bag Alignment across Disjoint Alphabets

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78mz9rxbe03r8std7y9bbkzs8bj4jg
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering
- Best/top context found: Top Score | 0.964 | Created | Jul 31, 2026 | Start New Solution

Full challenge description from page:

> Dual-Cipher Bag Alignment across Disjoint Alphabets (DCBA)
> Problem Overview
> Two independent renderings of an identical corpus were produced generations apart under contrasting stylistic principles: one utilizing rich, literary phrasing, and the other restricting itself to a deliberately small, plain vocabulary. Both renderings are provided in an enciphered format where word order is completely destroyed, turning every passage into an opaque multiset (shuffled bag) of symbols.
> Because each rendering was enciphered separately using a distinct bijective map, their symbol sets are entirely disjoint—no symbol occurs in both renderings. A query entry from the first rendering and a candidate entry from the second rendering share zero surface symbols.
> Each row in the benchmark poses 10 independent questions. For every query entry from Rendering 1, a slate of 8 candidate entries from Rendering 2 is provided. Exactly one candidate in the slate renders the same underlying passage as the query. Your task is to identify the correct candidate for all ten queries per row.
> Scoring is strictly all-or-nothing at the row level: a row counts as correct only if all 10 candidate picks are correct. Answering 9 out of 10 correctly scores 0 for that row.
> What Makes This Task Unique
> Disjoint Symbol Alphabets: Direct symbol matching is impossible. Symbol correspondences between renderings can only be learned from pairs in the labeled training rows.
> Complete Word-Order Destruction: Passages are published as shuffled bags of symbols, eliminating syntax, n-gram patterns, and word-order signals.
> Adversarial Distractor Slates: The 7 wrong candidates in every slate are chosen as the candidate-side entries that share the most underlying terms with the gold answer. All 8 candidates concern the same subject matter, so candidates cannot be picked by broad topic similarity.
> Strict Division Split: Training and test sets are partitioned by corpus division (book). The passages behind test rows come from divisions that contribute nothing to training, forcing models to generalize to material of a different character.
> Dataset Structure
> Raw Underlying Corpus
> The benchmark is constructed from a verse-aligned parallel corpus covering 160,181 verses across independent English scriptural editions (bible_verses.csv):
> entries.csv (51,332 rows): Contains every entry referenced in train or test.
> train.csv (2,081 rows): Contains training rows with queries, candidate slates, and gold assignments.
> test.csv (485 rows): Contains test queries and candidate slates to answer.
> sample_submission.csv: Demonstrates the required output format.
> Schema & Field Definitions
> Entry File (entries.csv)
> entry_id (string): Opaque salted hash identifier for the entry. Unrelated to rendering, passage, or row.
> terms (string): Space-separated opaque symbols representing the surviving words of the entry in a fixed, shuffled order.
> Row Files (train.csv & test.csv)
> id (string): Opaque identifier of the row.
> queries (string): Ten space-separated entry_id values from Rendering 1.
> slates (string): Ten slates separated by ;. Each slate contains 8 space-separated entry_id values from Rendering 2 in shuffled order.
> assignment (string, train.csv only): Ten space-separated entry_id values from Rendering 2 matching the exact order of queries.
> Leakage Controls & Construction Methodology
> Division-Level Partitioning: The corpus is split across 66 named divisions (books): 16 divisions are held out for test, and 50 are used for training. Every entry a row touches—query, gold candidate, and all 7 distractors—comes exclusively from a division on that row's side of the split. No entry appears in labels on both sides.
> Side-Isolated Distractors: Distractors are selected strictly within the same division split side as the query. Training distractors are drawn only from training divisions; test distractors are drawn only from test divisions.
> Middle Document-Frequency Band Filter: Terms are retained only if their document frequency falls in a middle band (
> 60
> ≤
> DF
> ≤
> 0.05
> ×
> 𝑁
> 60≤DF≤0.05×N). Names, numerals, rare words, and ubiquitous function words are excluded, preventing single-symbol identification shortcuts.
> Independent Per-Rendering Ciphers: Each rendering uses a private bijective cipher map based on SHA-256 salted hashes, ensuring zero shared vocabulary between renderings or external texts.
> Evaluation Metric & Submission Format
> Metric
> Submissions are evaluated on exact match accuracy across all test rows:
> Score
> =
> 1
> 𝑁
> ∑
> 𝑖
> =
> 1
> 𝑁
> ∏
> 𝑗
> =
> 1
> 10
> 𝐼
> (
> 𝑎
> ^
> 𝑖
> ,
> 𝑗
> =
> 𝑎
> 𝑖
> ,
> 𝑗
> )
> Score=
> N
> 1
> ​
> ∑
> i=1
> N
> ​
> ∏
> j=1
> 10
> ​
> I(
> a
> ^
> i,j
> ​
> =a
> i,j
> ​
> )
> where
> 𝑎
> ^
> 𝑖
> ,
> 𝑗
> a
> ^
> i,j
> ​
> is your predicted candidate ID and
> 𝑎
> 𝑖
> ,
> 𝑗
> a
> i,j
> ​
> is the gold candidate ID for question
> 𝑗
> j in row
> 𝑖
> i.
> Output Requirements
> Save your predictions to ./working/submission.csv with exactly these columns:
> Code snippet
> id,assignment
> 7f0a1b2c3d4e5f,a11bb22cc33dd4 a55ee66ff77aa8 a99bb00cc11dd2 a33ee44ff55aa6 a77bb88cc99dd0 a12ab34cd56ef7 a21ba43dc65fe8 a31ca53db75gf9 a41da63ec85hg0 a51eb73fd95ih1
> Every test id must appear exactly once.
> assignment must hold exactly 10 space-separated entry IDs drawn from the corresponding query slates.
> Missing or duplicate IDs make the submission invalid. Wrong or malformed assignments score zero on that row.
> What Not To Use
> To maintain the integrity of the benchmark, the following constraints must be strictly observed:
> Do NOT use Pretrained Models or Embeddings: The symbols in this task are artificially generated ciphers specific to this dataset. They do not exist in any external pretrained vocabulary (e.g., BERT, RoBERTa, Word2Vec), making external embeddings meaningless.
> Do NOT use External Resources: Do not use external text corpora, dictionary mappings, or external translation tools. The provided entries.csv and train.csv files constitute the sole evidence for solving the task.
> Do NOT Infer Answers from Split Artifacts: Do not attempt to reverse-engineer salted hash IDs, row order, file line ordering, or data generation split artifacts.
> Do NOT Adapt Models Using Hidden Test Labels: Solutions must rely purely on supervised or unsupervised learning from the supplied train/entry files without probing hidden evaluation answers.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Isomer Stability Ranking From Infrared Spectra

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx712d6fdm66999yvf3j733rkn88ky7p
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering, multimodal
- Best/top context found: Top Score | 0.684 | Created | Jun 13, 2026 | Start New Solution

Full challenge description from page:

> Isomer Stability Ranking From Infrared Spectra
> Overview
> Constitutional isomers share a molecular formula but differ in how their atoms are connected, and those differences make some arrangements more thermodynamically stable than others. This challenge poses a question that, to our knowledge, has not been asked before: can a model recover the stability ordering of a set of isomers using nothing but their infrared (IR) spectra?
> Every molecule is described only by its harmonic IR spectrum (a list of vibrational wavenumbers and their infrared intensities). Molecules are organised into groups; all molecules in a group are constitutional isomers of one another (same formula, different connectivity), and within each group they are deliberately close in energy. This is a ranking task: for each group you must output an ordering of its molecules from most stable to least stable. The output is an ordering, not a magnitude. Stability is defined by each molecule's quantum-chemical electronic energy, which is hidden from you.
> Evaluation
> Submissions are scored on how well your ordering agrees with the true stability ordering inside each group, using the Kendall rank correlation coefficient (tau-b).
> For every group we compute tau-b between your submitted ranks and the true (hidden) electronic energies. Group results are combined with a pair-weighted average, where each group contributes in proportion to its number of comparable pairs n*(n-1)/2. Your score is this mean rank correlation, clamped to [0, 1]:
> final_score = max(0, mean_tau)
> A perfect ordering in every group scores 1.0; a random ordering scores about 0; an ordering worse than random also scores 0. Only the order implied by your ranks matters, not their absolute values. Use rank 1 for the most stable molecule in a group, rank 2 for the next, and so on. The training label 'stability_order' is exactly this ordering computed from the hidden energies, so a model trained to reproduce 'stability_order' is optimising what you are scored on.
> Dataset
> The data is drawn from a library of computed molecular-property data. Each molecule is a small organic structure whose equilibrium geometry and harmonic vibrational spectrum were obtained from first-principles density functional theory calculations in the gas phase; the IR spectrum used here is the resulting set of vibrational modes, each with a wavenumber and an infrared intensity. To build the challenge, molecules that belong to constitutional-isomer families were grouped by molecular formula, the most and least stable members of each family were removed so that the remaining molecules are close in energy, and each family was split into the training and test sets described below.
> Scale: the challenge spans several hundred isomer groups drawn from a curated subset of tens of thousands of computed spectra. A family must contain at least 8 molecules to be included. Group sizes vary and are not fixed: each test group contains between 3 and 40 molecules, and each training group contains up to 150 molecules. The total number of molecules is in the low tens of thousands, split across train and test.
> This challenge provides three files.
> 'train.csv' contains the labelled training molecules, one row per molecule, with the following columns:
> 'id' — molecule identifier (integer)
> 'group_id' — the isomer group this molecule belongs to (integer)
> 'smiles' — SMILES string of the molecule, provided for training only so that structure-based pretrained models can be used
> 'wavenumbers' — space-separated harmonic vibrational wavenumbers in cm^-1
> 'intensities' — space-separated infrared intensities in km/mol, aligned position-by-position with 'wavenumbers'
> 'stability_order' — the prediction target: the molecule's integer stability position within its group, from 1 (most stable) to n (least stable, where n is the group size). It is the ordering induced by the hidden electronic energy.
> 'test.csv' contains the unlabelled test molecules to be ordered, one row per molecule, with the columns 'id', 'group_id', 'wavenumbers' and 'intensities' as defined for 'train.csv'. It does not include 'smiles' or any label.
> 'sample_submission.csv' is a correctly formatted example submission, one row per molecule in 'test.csv', with the columns:
> 'id' — a test molecule identifier (integer), matching 'test.csv'
> 'rank' — a placeholder integer ordering. For each group it is a valid ordering (the integers 1..n assigned by id order), that is, not the true stability order. Replace it with your predicted ordering.
> Each spectrum is a harmonic stick spectrum (peak positions and intensities only); you may broaden, scale or featurise it however you like. The groups in 'test.csv' are independent and are ordered separately.
> Submission
> Submit a CSV with the same number of rows as 'test.csv' (exactly one row per 'id'), plus a header row. Each data row has two columns:
> 'id' (integer) — molecule identifier from 'test.csv'.
> 'rank' (integer) — the molecule's position within its group, where 1 is the most stable and larger numbers are less stable.
> Within each group the ranks must be distinct integers that express a strict ordering; the recommended form is the integers 1 to n with 1 = most stable. Duplicate or tied ranks within a group, and non-integer ranks, are invalid and are scored as errors. Only the within-group order is used for scoring, so the absolute values otherwise carry no meaning.
> For example, if ids 0, 1 and 2 form one group and ids 5 and 7 form another, the submission file would contain a header followed by one line per molecule, with these lines:
> 'id,rank'
> '0,2'
> '1,1'
> '2,3'
> '5,1'
> '7,2'
> In this example ids 0, 1 and 2 are ordered 2, 1, 3 (so id 1 is predicted to be the most stable molecule in its group) and ids 5 and 7 are ordered 1, 2.
> Method Requirements
> This is a learning-to-rank problem rather than a regression or classification problem: you produce an ordering of each group and are scored only on that ordering.
> Recommended and allowed approaches include:
> Featurising each stick spectrum (for example broadening it into a fixed-length vector, binning intensities onto a wavenumber grid, or encoding the peak list directly) and training a ranker or an ordinal model, then sorting each group by the model output to obtain ranks.
> Set or sequence models over the variable-length peak list (for example DeepSets or transformers).
> Learning-to-rank objectives (pairwise or listwise) trained on the provided 'stability_order' labels, or regressing 'stability_order' and sorting.
> Using pretrained molecular representation or energy models on the training SMILES to build features or teacher targets, then distilling into a spectrum-only model that runs at test time from spectra alone.
> Any library available in the standard environment and any pretrained weights that were not trained on this challenge's hidden labels.
> To form a submission, sort each test group by your predicted stability (most stable first) and assign distinct integer ranks (the integers 1 to n work well), breaking ties arbitrarily so that the ranks within each group are distinct.
> The following are out of scope for this challenge:
> Producing the ordering from a single fixed statistic or closed-form rule alone (for example sorting by peak count, by total or mean intensity, by an extreme wavenumber, or by the zero-point energy 0.5sum(hnu)). These quantities may be used only as features inside a trained model, never as the entire solution.
> Recovering or approximating the hidden electronic energies or the molecule identities by matching the released spectra to any external dataset or public spectral library, or by looking up energies or identities from external resources. The released spectra are perturbed to prevent this.
> Inferring the ordering from the group structure or from any source other than the spectra provided.
> Pretrained models are encouraged but not required; the broaden-and-gradient-boosted-ranker baseline is acceptable.
> Notes
> All molecules are neutral, closed-shell organic species containing carbon, hydrogen, nitrogen, oxygen and fluorine, with up to nine heavy atoms. Spectra are harmonic and were computed in the gas phase with density functional theory; stability is defined by the gas-phase electronic energy.
> The released spectra have been perturbed slightly from their underlying computed values; treat the values in the data files as the definitive inputs.
> Within each group the molecules are deliberately close in energy: the most and least stable extremes have been removed, so the remaining distinctions are fine-grained.
> Order each group in 'test.csv' independently.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Audio Trace Mosaic Chain-of-Custody Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72vh02sfcxy7adps1xd3hj918b172t
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, audio, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Beat mailliwa's score of 0.090!

Full challenge description from page:

> Overview
> Each example contains a short stereo recording and a visual mosaic of sixteen unlabeled trace fragments. The task is to reconstruct the packet: assign every displayed fragment to its original measurement and time cell, mark any left-right channel reversal, recover the canonical level buckets for all source cells, and choose the correct release action.
> The sixteen source fragments come from four hearing-model measurements:
> loudness;
> roughness;
> fluctuation strength;
> tonality.
> Each measurement is divided into four consecutive time cells, giving sixteen source fragments in total. Those fragments are shuffled into display positions D00 through D15. Up to three displayed fragments can have their stereo orientation reversed. Some packets also replace one fragment with a duplicate of another, leaving one canonical source fragment absent.
> Submit exactly three connected outputs:
> | Output | Prediction |
> |---|---|
> | `tile_custody_matrix` | Signed source identity for every displayed fragment |
> | `canonical_level_matrix` | Perceptual level bucket for every metric and time cell |
> | `release_action` | `reassemble`, `channel_review`, `reacquire`, or `reject` |
> This is an audio-conditioned forensic reconstruction task. It is not sound classification, metric regression, ordinary trace alignment, or an image-only jigsaw. A complete solution must use the stereo WAV and the mosaic together, because the mosaic gives local visual witnesses while the audio determines the expected metric behavior behind those witnesses.
> Operational Context
> Acoustic verification work may combine a listening signal with trace exports produced by specialist measurement software. Long reports are often assembled from separate time windows, channels, and metric panels. A packet can remain visually plausible after fragments are reordered, duplicated, or exported with exchanged channels.
> That failure is more serious than a mislabeled chart. A duplicated fragment means some expected evidence is absent, while a channel reversal can alter the interpretation of spatially asymmetric sound. Before the packet can support a compliance or engineering decision, an auditor needs a complete chain-of-custody map and a release decision tied to the importance of any missing fragment.
> The prepared cases use real audio and reference hearing-model traces from an openly licensed verification release. Natural sound recordings provide training material. Different controlled modulation signals provide the held-out test material. This creates an acoustic-family shift while preserving exact synchronization between each WAV excerpt and its reference traces.
> Distinct Reasoning Requirement
> The benchmark treats every trace fragment as an evidence object with identity, time origin, and channel orientation. Its central target is therefore a signed, potentially non-bijective provenance relation over sixteen fragments. A substituted packet contains two visually valid copies of one source and no copy of another source, so sorting fragments into a plausible sequence is insufficient.
> The release decision also cannot be predicted from corruption type alone. It depends on which source fragment is absent and on that fragment's canonical perceptual level. The custody and level matrices must therefore support the same counterfactual question: what evidence would the packet contain if the duplicated fragment were replaced by the missing one?
> Dataset
> The prepared dataset contains 3,000 training examples and 900 test examples. Public identifiers and media filenames are opaque.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Input columns and all three targets for 3,000 examples |
> | `test.csv` | Input columns for 900 hidden-label examples |
> | `sample_submission.csv` | Schema-valid constant baseline |
> | `audio/` | Stereo WAV excerpts |
> | `metric_sheets/` | RGB PNG custody mosaics paired with the WAV excerpts |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier matching `^pa[0-9a-f]{22}$` |
> | `audio_path` | string path | Relative path to a stereo WAV excerpt |
> | `metric_sheet_path` | string path | Relative path to the paired sixteen-fragment mosaic |
> | `verification_contract` | string | Fixed text contract that explains how custody IDs are decoded. It states: `source tile order=loudness cells 0-3,roughness cells 0-3,fluctuation cells 0-3,tonality cells 0-3;negative custody IDs mean L/R swap`. It is the same kind of decoding instruction for all rows and does not contain row-specific answers. |
> Audio Properties
> | Property | Value |
> |---|---|
> | Encoding | 16-bit PCM WAV |
> | Channels | stereo |
> | Sample rate | 16,000 Hz |
> | Duration | 1.5 seconds |
> | Time partition | four equal cells |
> Mosaic Layout
> Each 1100 x 800 PNG contains a four-by-four grid of trace fragments. Display labels follow row-major order:
> D00 D01 D02 D03
> D04 D05 D06 D07
> D08 D09 D10 D11
> D12 D13 D14 D15
> Blue is the displayed left channel and amber is the displayed right channel. Each tile inherits the vertical scale of its source measurement. The small gray tabs beneath tiles vary independently and carry no target information.
> The mosaic does not print metric names or source time-cell numbers. Display position is not source identity.
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `tile_custody_matrix` | JSON integer matrix, shape `4 x 4` | Signed source ID at each display position |
> | `canonical_level_matrix` | JSON integer matrix, shape `4 x 4` | Level bucket for each canonical metric and time cell |
> | `release_action` | categorical string | Required handling of the reconstructed packet |
> Tile Custody Matrix
> Rows and columns correspond to display positions D00 through D15 in the four-by-four layout. The absolute value of an entry identifies the canonical source fragment:
> | Absolute ID | Source measurement | Source time cell |
> |---:|---|---:|
> | `1` to `4` | loudness | `0` to `3` |
> | `5` to `8` | roughness | `0` to `3` |
> | `9` to `12` | fluctuation strength | `0` to `3` |
> | `13` to `16` | tonality | `0` to `3` |
> A positive value means the displayed blue and amber channels preserve the source orientation. A negative value means the channels were exchanged.
> For example:
> [
> [6,-1,14,9],
> [12,3,5,16],
> [8,11,-4,2],
> [15,7,10,13]
> ]
> This matrix says that D00 contains roughness cell 1, D01 contains loudness cell 0 with exchanged channels, and so on.
> A valid packet has one of two custody structures:
> Complete packet: absolute IDs 1 through 16 each appear exactly once.
> Substituted packet: one absolute ID appears twice, one ID is absent, and the other fourteen appear once.
> No more than three entries are negative. Values cannot be zero. The maximum accepted JSON length is 140 characters.
> Custody Distribution
> | Swapped-channel fragments | Train | Test |
> |---:|---:|---:|
> | 0 | 548 | 179 |
> | 1 | 992 | 274 |
> | 2 | 925 | 270 |
> | 3 | 535 | 177 |
> | Packet structure | Train | Test |
> |---|---:|---:|
> | Complete | 1,576 | 480 |
> | One duplicate and one missing source | 1,424 | 420 |
> Canonical Level Matrix
> Rows use this fixed metric order:
> loudness,roughness,fluctuation,tonality
> Columns are source time cells 0, 1, 2, and 3. Every entry is an integer from 0 through 4:
> | Value | Position in that metric's reference distribution |
> |---:|---|
> | `0` | At or below the 20th percentile |
> | `1` | Above the 20th and at or below the 40th percentile |
> | `2` | Above the 40th and at or below the 60th percentile |
> | `3` | Above the 60th and at or below the 80th percentile |
> | `4` | Above the 80th percentile |
> Percentile boundaries are computed separately for each metric within its complete source reference track. The matrix is ordinal and does not represent physical units.
> Example:
> [[1,3,4,2],[0,1,2,2],[4,3,1,0],[2,2,3,4]]
> The maximum accepted JSON length is 100 characters.
> Release Action
> The required action is determined by the reconstructed custody packet:
> | Value | Required condition |
> |---|---|
> | `reassemble` | All sixteen source IDs are present and no entry is negative |
> | `channel_review` | All source IDs are present and at least one entry is negative |
> | `reacquire` | One source ID is missing and its canonical level is `0`, `1`, or `2` |
> | `reject` | One source ID is missing and its canonical level is `3` or `4` |
> The missing source ID is the number from 1 through 16 absent from the absolute values of tile_custody_matrix. Its row and column in canonical_level_matrix are recovered from the source-ID table above.
> | Split | `reassemble` | `channel_review` | `reacquire` | `reject` |
> |---|---:|---:|---:|---:|
> | Train | 296 | 1,280 | 815 | 609 |
> | Test | 105 | 375 | 271 | 149 |
> Split Isolation
> Three natural source recordings contribute training windows. Two different controlled signals contribute test windows. A source recording never crosses the split.
> Starting sample positions are unique within each source. Prepared WAV payloads and mosaic payloads are checked by cryptographic hash. No exact audio or image payload appears in both splits.
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in exactly this order:
> case_id,tile_custody_matrix,canonical_level_matrix,release_action
> Every test case_id must appear exactly once. Extra columns, reordered columns, duplicate IDs, unknown IDs, missing rows, and extra rows are rejected.
> Column value requirements:
> | Column | Required format |
> |---|---|
> | `case_id` | String copied from `test.csv` |
> | `tile_custody_matrix` | JSON string containing a `4 x 4` integer matrix with values from `-16` to `16`, excluding `0` |
> | `canonical_level_matrix` | JSON string containing a `4 x 4` integer matrix with values from `0` through `4` |
> | `release_action` | One of `reassemble`, `channel_review`, `reacquire`, or `reject` |
> Example with two valid rows:
> case_id,tile_custody_matrix,canonical_level_matrix,release_action
> pa9f80b42106c93f12b5dbd2,"[[6,-1,14,9],[12,3,5,16],[8,11,-4,2],[15,7,10,13]]","[[1,3,4,2],[0,1,2,2],[4,3,1,0],[2,2,3,4]]",channel_review
> pa0c7d4a2f9b18e3605dd44,"[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,15]]","[[0,1,2,3],[1,2,3,4],[0,2,4,1],[2,3,4,4]]",reject
> Evaluation
> Submissions are evaluated with the Trace Custody Reconstruction Score:
> For each test row, the grader computes CustodyScore, LevelScore, and ReleaseScore, then combines them as:
> BaseRowScore =
> 0.57 * CustodyScore
> + 0.30 * LevelScore
> + 0.13 * ReleaseScore
> The final score is:
> FinalScore = mean(AdjustedRowScore over all hidden test rows)
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> CustodyScore
> For true custody matrix Y and predicted matrix P:
> source_accuracy =
> mean(abs(Y[i,j]) == abs(P[i,j]) for all 16 entries)
> signed_accuracy =
> mean(Y[i,j] == P[i,j] for all 16 entries)
> exact_custody =
> 1 if all 16 signed entries match, else 0
> CustodyScore =
> 0.16 * source_accuracy
> + 0.10 * signed_accuracy
> + 0.74 * exact_custody
> source_accuracy rewards correct fragment provenance even when channel orientation is wrong. signed_accuracy requires both provenance and channel orientation.
> LevelScore
> For each matrix entry:
> entry_proximity[i,j] =
> max(0, 1 - abs(Y[i,j] - P[i,j]) / 4)
> exact_level_matrix =
> 1 if all 16 entries match, else 0
> LevelScore =
> 0.14 * mean(entry_proximity)
> + 0.86 * exact_level_matrix
> ReleaseScore
> ReleaseScore is 1 when the submitted release action exactly matches the hidden action and 0 otherwise.
> Coherence Adjustment
> The coherence check applies once per full submitted row. It uses the complete submitted tile_custody_matrix and the complete submitted canonical_level_matrix together, not individual matrix rows in isolation. The grader derives one implied release action from those two predicted matrices using the release-action table above.
> AdjustedRowScore =
> BaseRowScore,          if submitted action equals implied action
> 0.80 * BaseRowScore,   otherwise
> Malformed matrices have no implied action and therefore receive the 0.80 factor in addition to receiving zero for the malformed component.
> Matrix parsing is bounded before JSON decoding. Invalid shapes, booleans, floats, zeros in the custody matrix, out-of-range values, invalid duplicate patterns, more than three negative custody entries, unknown actions, and oversized values receive zero for the affected component. Schema-valid malformed submissions always produce a finite score.
> Reference Validation
> | Check | Result |
> |---|---:|
> | Exact hidden-answer submission | `1.0000` |
> | Packaged sample submission | `0.0576` |
> | Unique WAV payloads | `3,900 / 3,900` |
> | Unique mosaic payloads | `3,900 / 3,900` |
> | Train-test source-recording overlap | `0` |
> | Train-test WAV-hash overlap | `0` |
> | Train-test image-hash overlap | `0` |
> Method Requirements
> Solutions may use the provided A10G GPU within the competition time limit. Neural audio encoders, image encoders for the mosaic, cross-modal attention models, trace-fragment descriptors, assignment solvers, and constrained structured decoders are allowed when fitted or calibrated only with public training data.
> The primary prediction logic must use the supplied audio and mosaic evidence. The fixed verification contract can be used to decode matrix semantics but does not contain row-specific answers.
> What Not To Use
> Do not use case_id, filenames, row order, file sizes, or media hashes as target predictors.
> Do not identify or match public audio against external source copies or retrieve reference result files by source identity.
> Do not use private answers, hidden split artifacts, grader internals, or submission feedback as labels.
> Do not construct lookup tables from external recordings, report exports, or source filenames.
> Do not perform test-label adaptation or per-test memorization.
> Do not exploit malformed JSON, duplicate IDs, extra columns, oversized values, or parser behavior.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Sensor Seasonal Identity Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76xtykm7c9dc7x87jxtgz01d8bm222
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat neofrazer's score of 0.629!

Full challenge description from page:

> Overview
> Earth-observation archives combine measurements made by instruments that respond to different physical properties. Optical sensors record reflected light, radar responds to structure and moisture, and environmental products describe the climate, soil, and terrain around a location. When export metadata is damaged, measurements from several nearby survey points can become mixed even though each individual sequence remains intact.
> Each challenge case contains four optical anchor sequences from geographically and ecologically confusable survey points. It also contains a shuffled bank of four radar sequences and a separate shuffled bank of four environmental context records. Every radar sequence has additionally been circularly shifted by an unknown number of months.
> The task is to reconstruct the one-to-one identity binding for all three modalities and recover the radar phase shift. A valid answer must use every radar candidate and every context candidate exactly once. Independent nearest-neighbor predictions are therefore insufficient unless they also form a complete case-level assignment.
> Training cases use one survey year. Test cases use different, previously unseen survey-point identities from a later survey year. Public identifiers are generated independently for each modality and contain no shared point code.
> Task
> For every case_id, produce one binding clause for each optical anchor in the published anchor order.
> Each clause has this exact form:
> OPT_id=RAD_id@phase,CTX_id
> The four clauses are joined with | and contain no whitespace.
> phase is an integer from 0 through 11. It is the number of positions by which the published radar sequence was rolled forward relative to calendar order. Applying a roll of -phase restores its original January-to-December order.
> Dataset
> The public dataset contains three CSV files and three compressed NumPy files.
> train.csv: 6,000 labeled four-anchor reconstruction cases.
> test.csv: 1,500 unlabeled cases built from unseen later-year survey points.
> sample_submission.csv: one structurally valid random binding for every test case.
> optical.npz: anonymous optical IDs and normalized arrays with shape N x 12 x 10 x 3 x 3.
> radar.npz: anonymous radar IDs and normalized, phase-shifted arrays with shape N x 12 x 2 x 3 x 3.
> context.npz: anonymous context IDs, monthly environmental arrays with shape N x 12 x 18, and static soil-terrain arrays with shape N x 35.
> All tensor values are finite float16 values standardized with training-pool statistics. Missing source measurements are represented by 0.0 after standardization.
> train.csv Columns
> case_id (string): anonymous case identifier.
> anchor_ids (string): four optical IDs separated by semicolons; this order defines the required output-clause order.
> anchor_photo_masks (string): four six-bit availability masks in anchor order. Bits describe east, west, north, point, close-up, and south survey views.
> radar_candidate_ids (string): the four admissible radar IDs, separated by semicolons and shuffled.
> context_candidate_ids (string): the four admissible environmental-context IDs, separated by semicolons and shuffled independently.
> binding_path (string): target four-clause reconstruction path.
> test.csv Columns
> case_id (string): anonymous case identifier.
> anchor_ids (string): ordered optical anchor IDs.
> anchor_photo_masks (string): ordered six-bit photo-availability masks.
> radar_candidate_ids (string): shuffled admissible radar IDs.
> context_candidate_ids (string): independently shuffled admissible context IDs.
> sample_submission.csv Columns
> case_id (string): copied from test.csv.
> binding_path (string): a complete, syntax-valid four-clause path.
> Evaluation
> The score is bounded in [0, 1], where higher is better:
> Score = 0.25 * RadarAssignmentSkill + 0.20 * ContextAssignmentSkill + 0.25 * PhaseSkill + 0.30 * ExactCaseAccuracy
> RadarAssignmentAccuracy is the fraction of optical anchors assigned their correct radar candidate. Four-way random accuracy is 0.25, so RadarAssignmentSkill = max(0, (RadarAssignmentAccuracy - 0.25) / 0.75).
> ContextAssignmentAccuracy is the fraction of optical anchors assigned their correct environmental candidate. ContextAssignmentSkill = max(0, (ContextAssignmentAccuracy - 0.25) / 0.75).
> PhaseMacroF1 is standard one-vs-rest macro F1 over the twelve phase labels 0 through 11. A phase with neither true nor predicted examples in the evaluated answer partition is omitted. False positives or false negatives cause that phase to be included. The uniform twelve-way chance reference is 1/12, so PhaseSkill = max(0, (PhaseMacroF1 - 1/12) / (11/12)).
> ExactCaseAccuracy is the fraction of cases for which all four radar assignments, all four context assignments, and all four phase labels are simultaneously correct.
> The three skill terms are chance-normalized to [0, 1]. The four components appear exactly once in the displayed formula and their weights sum to 1.00.
> Submission
> Submit a CSV containing exactly these columns:
> case_id
> binding_path
> Example:
> case_id,binding_path
> CASE_0123456789abcd,OPT_11111111111111=RAD_aaaaaaaaaaaaaa@3,CTX_bbbbbbbbbbbbbb|OPT_22222222222222=RAD_cccccccccccccc@0,CTX_dddddddddddddd|OPT_33333333333333=RAD_eeeeeeeeeeeeee@11,CTX_ffffffffffffff|OPT_44444444444444=RAD_55555555555555@6,CTX_66666666666666
> For each case, clauses must follow anchor_ids order. Every listed radar candidate and every listed context candidate must occur exactly once. Missing IDs, duplicate IDs, foreign candidates, malformed clauses, invalid phases, nulls, empty predictions, and extra columns are rejected before scoring.
> Allowed And Prohibited Methods
> Allowed
> Train contrastive, sequence, assignment, or multimodal neural models using the supplied public data.
> Use generic pretrained encoders that were not trained to recover identities from this source collection.
> Enforce the one-to-one assignment with Hungarian matching, optimal transport, beam search, or another learned decoding strategy.
> Prohibited
> External source matching, geolocation lookup, or recovery of original survey-point identifiers.
> Hardcoded test bindings, manually labeled test cases, or answer tables obtained outside the public challenge data.
> Row-order, file-order, hash, or identifier reversal shortcuts.
> Non-ML lookup systems whose purpose is to reconnect anonymous records to the source release.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Electric Fish Pulse Stream Deconvolution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71rj30njv8ndrnrrkyv1xbx18brrab
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch signal-learning challenge built from real electrical recordings of weakly electric fish. These fish emit brief electric organ discharge pulses while swimming. In each row, two anonymous fish streams have been mixed into one compact multi-electrode voltage panel.
> Your task is to recover the two pulse streams. You are given:
> one mixed voltage panel;
> two calibration cards, F1 and F2, that define the row-local fish streams;
> a shuffled set of detected pulse cards, P01, P02, and so on.
> Submit the ordered pulse sequence for F1 and the ordered pulse sequence for F2.
> In plain terms: untangle which electric pulse came from which fish, and preserve the within-fish pulse order.
> The source data comes from single-fish recordings of freely swimming Gymnotus weakly electric fish. Challenge rows are generated from source-derived pulse templates with source-block-disjoint train/test splits. Public rows do not expose source file names, biological fish IDs, source block IDs, or template IDs.
> This is not species classification, sound tagging, ordinary source separation, or tabular regression. The submitted artifact is a pair of ordered symbolic pulse tracks grounded in voltage waveforms.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> voltage_panel: string. Encoded 11 by 256 mixed voltage panel.
> panel_shape: string. Always 11x256.
> calibration_cards: JSON list. Two row-local stream prototypes, F1 and F2.
> pulse_cards: JSON list. Shuffled detected pulse cards.
> pulse_count: integer. Number of pulse aliases that must be used exactly once.
> condition_hint: string. Coarse public condition hint.
> max_track_length: integer. Maximum expected length of either output track.
> track_f1: string. Training-only ordered F1 pulse track.
> track_f2: string. Training-only ordered F2 pulse track.
> test.csv has the same public columns but omits track_f1 and track_f2.
> sample_submission.csv contains:
> id: string. Test row ID.
> track_f1: string. Empty dummy track.
> track_f2: string. Empty dummy track.
> There are 3,500 training rows and 1,200 hidden test rows. Hidden test rows are balanced across five private scenario families, with 240 rows per family.
> Input field schemas
> Encoding alphabet:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> voltage_panel:
> Type: string.
> Length: 2,816 characters.
> Decoding: map each character to an integer from 0 to 63 and reshape row-major to 11 channels by 256 time frames.
> Meaning: larger values indicate stronger normalized voltage magnitude after robust row-local scaling.
> Each calibration_cards item has:
> stream: string. F1 or F2.
> calibration_code: string. Encoded 11 by 48 signed prototype waveform for that stream.
> prototype_width: string. Coarse prototype width: narrow, medium, wide, or broad.
> Each pulse_cards item has:
> pulse: string. Row-local pulse alias such as P03.
> onset_bin: integer. Coarse time bin of the detected pulse in the voltage panel.
> local_code: string. Encoded 11 by 48 local voltage snippet around the detected pulse.
> peak_tier: string. Coarse peak tier: low, mid, high, or clip.
> neighborhood: string. isolated, near, or overlap, based on nearby detected pulses.
> The pulse-card order is shuffled and is not chronological.
> Output format
> Submit two space-separated pulse tracks:
> track_f1: ordered pulse aliases assigned to stream F1.
> track_f2: ordered pulse aliases assigned to stream F2.
> Every pulse alias listed in pulse_cards must appear exactly once across the two output columns.
> Example:
> id,track_f1,track_f2
> 0a12bc34de56f789,"P03 P08 P11 P12","P01 P02 P04 P05 P06"
> Invalid row examples:
> track_f1 = P03 P03
> track_f2 = P01 P02
> The row above is invalid because P03 is duplicated and other pulse aliases are missing.
> track_f1 = F1:P03 P08
> track_f2 = P01,P02
> The row above is invalid because tracks must contain only space-separated pulse aliases.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level tracks score 0 for that row. Rows are aligned by id, not row order.
> For each row, the grader parses the predicted and hidden tracks.
> Definitions:
> AssignmentF1: F1 over (pulse_alias, stream) pairs. A pulse assigned to the wrong stream is incorrect.
> AssignmentSkill: above-chance assignment credit, computed as max(0, 2 * AssignmentF1 - 1). A random balanced stream split receives approximately 0 assignment skill.
> OrderLCS: for each stream, compute longest-common-subsequence length between predicted and hidden pulse order, divided by the hidden stream length. OrderLCS is the mean over F1 and F2.
> AdjacentLinkF1: F1 over directed adjacent links (stream, previous_pulse, next_pulse) within each stream.
> CountBalance: mean count score over both streams. A stream receives 1 if its predicted count is exact, otherwise max(0, 1 - absolute_count_error / max(hidden_count, 3)).
> ExactTracks: 1 if both tracks exactly match the hidden tracks, otherwise 0.
> Ordering credit is coupled to stream assignment:
> OrderWhenAssigned = OrderLCS * AssignmentF1
> AdjacentWhenAssigned = AdjacentLinkF1 * AssignmentF1
> The row score is:
> row_score =
> 0.42 * AssignmentSkill
> + 0.28 * OrderWhenAssigned
> + 0.15 * AdjacentWhenAssigned
> + 0.05 * CountBalance
> + 0.10 * ExactTracks
> The hidden set is balanced across five private scenario families:
> clean_duet
> overlap_collision
> weak_shadow
> polarity_reversal
> chirp_gap
> Family labels are not present in public files. They are used only for robust hidden scoring.
> The final score is:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.68 * overall_mean
> + 0.22 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly three columns in this order:
> id
> track_f1
> track_f2
> Do not include scenario-family labels, source IDs, JSON, extra columns, or natural-language explanations.
> Recommended solution approach
> A basic solution can correlate each pulse snippet with the two calibration waveforms and order predicted tracks by onset_bin. Stronger solutions should learn waveform embeddings from train.csv, use the full voltage panel to handle overlapping pulses, and calibrate for weak streams, polarity reversals, and irregular pulse timing.
> GPU use is appropriate for compact Siamese or cross-attention models over pulse snippets, calibration waveforms, and the full voltage panel within the A10G/50-minute budget.
> What not to use
> Do not use row IDs, row order, source file names, source block IDs, or fixed meanings of F1, F2, or Pxx. All aliases are row-local.
> Do not assume that onset_bin alone solves the task. It helps with ordering but not reliable stream attribution.
> Do not optimize only clean rows. Worst-family and bottom-tail scoring penalize failures on overlaps, weak streams, polarity reversals, and chirp-gap timing.
> Benchmark boundary
> Nearest prior work includes electric-organ-discharge detection, weakly electric fish pulse sorting, and generic source separation. This benchmark differs by using row-local calibration cards, compact multi-electrode voltage panels, shuffled pulse aliases, symbolic two-track outputs, source-block-disjoint generated dyads, and robust hidden family scoring. It is a pulse-stream deconvolution benchmark, not species classification, acoustic event detection, or ordinary audio transcription.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Haptic Sensor Log Reassembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73h75paxzm9bs63xgc4snkcx8bratt
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch multimodal signal-learning challenge. Each row contains five short audio log cards and five tactile log cards from the same finger-texture interaction sequence. The logs have been separated and shuffled. Your task is to reassemble the synchronized contact timeline by pairing each audio card with its matching tactile card and placing the five pairs in chronological order.
> In plain terms: recover which touch signal made which sound, then put the five recovered contacts back into sequence.
> The source data comes from real human bare-finger interactions with textured surfaces. The original recordings include microphone audio, friction-induced vibration, force/torque measurements, and fingertip position. Public challenge rows are compact source-derived windows, not raw HDF5 files. Source participants are split disjointly between train and hidden test.
> This is not computer vision, sequence-to-sequence generation, ordinary audio tagging, or tabular regression. The submitted answer is a fixed five-slot reassembly table.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> audio_cards: JSON list. Five shuffled audio cards, A1 through A5.
> tactile_cards: JSON list. Five shuffled tactile cards, T1 through T5.
> sound_shape: string. Always 2x96.
> vibration_shape: string. Always 2x96.
> force_shape: string. Always 3x48.
> speed_shape: string. Always 1x48.
> condition_hint: string. Coarse public condition hint.
> slot_count: integer. Always 5.
> slot_1 through slot_5: strings. Training-only chronological answer pairs.
> test.csv has the same public columns but omits slot_1 through slot_5.
> sample_submission.csv contains:
> id: string. Test row ID.
> slot_1 through slot_5: empty dummy values. The sample scores 0.
> There are 4,000 training rows and 1,200 hidden test rows. Hidden test rows are balanced across five private scenario families, with 240 rows per family.
> Input field schemas
> Each audio_cards item has:
> audio: string. Row-local audio alias: A1, A2, A3, A4, or A5.
> sound_strip: string. A 2 by 96 audio envelope strip encoded with 64 printable symbols.
> energy_hint: string. Coarse public energy descriptor.
> scratch_hint: string. Whether an audio gap/scratch artifact is hinted.
> Each tactile_cards item has:
> tactile: string. Row-local tactile alias: T1, T2, T3, T4, or T5.
> vibration_strip: string. A 2 by 96 encoded vibration strip.
> force_strip: string. A 3 by 48 encoded force strip.
> speed_code: string. A 1 by 48 encoded fingertip-speed trace.
> contact_hint: string. Coarse anonymized contact descriptor.
> Encoding alphabet:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> To decode a strip, map each character to an integer from 0 to 63 and reshape row-major to the documented shape. Larger values indicate stronger normalized signal magnitude.
> Output format
> Submit five fixed slot columns. Each slot is one pair token:
> A#=T#
> Examples:
> A3=T2
> A1=T5
> A valid row must use every audio alias exactly once and every tactile alias exactly once across the five slots.
> Invalid examples:
> A6=T2
> A1 T2
> {"audio":"A1","tactile":"T2"}
> A1=T1 repeated in two slots
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level reassemblies score 0 for that row. Rows are aligned by id, not row order.
> For each row:
> PairF1 is F1 over the unordered set of five predicted A#=T# pairs.
> SlotAccuracy is the fraction of the five chronological slots whose exact pair is correct.
> AdjacentLinkF1 is F1 over four ordered adjacent links: (slot_1, slot_2), (slot_2, slot_3), (slot_3, slot_4), and (slot_4, slot_5).
> ExactRoute is 1 if all five slots exactly match the hidden chronological route, otherwise 0.
> The row score is:
> row_score =
> 0.55 * PairF1
> + 0.25 * SlotAccuracy
> + 0.10 * AdjacentLinkF1
> + 0.10 * ExactRoute
> The hidden test set is balanced across five private scenario families:
> clean_reassembly
> audio_gap
> tactile_gap
> tempo_warp
> near_neighbor
> Family labels are not present in public files. They are used only for robust hidden scoring.
> The final score is:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.70 * overall_mean
> + 0.20 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly six columns in this order:
> id
> slot_1
> slot_2
> slot_3
> slot_4
> slot_5
> Example:
> id,slot_1,slot_2,slot_3,slot_4,slot_5
> 0a12bc34de56f789,A3=T2,A1=T5,A4=T1,A2=T4,A5=T3
> Recommended solution approach
> A basic solution can build a 5 by 5 audio-vibration similarity matrix and solve a bipartite assignment. Stronger solutions should learn cross-modal embeddings that use audio, vibration, force, and speed, then model local chronological continuity across the recovered pairs.
> GPU use is appropriate for compact cross-attention or Siamese models over the ten cards in each row within the A10G/50-minute budget.
> What not to use
> Do not use row IDs, row order, source subject IDs, source texture folder names, or fixed aliases. Audio and tactile aliases are row-local.
> Do not assume the strongest-energy card is the answer. Hard families include gaps, tempo warps, near-neighbor windows, and lure coupling.
> Do not submit JSON, natural-language explanations, extra columns, or one single token for the whole row.
> Benchmark boundary
> Nearest prior work includes haptic texture classification, tactile material recognition, and audio-based surface recognition. This benchmark differs by requiring row-local multimodal log reassembly: five audio fragments and five tactile fragments must be matched and ordered under participant-disjoint splits. It is a sensor-log synchronization and reassembly benchmark, not ordinary material classification, audio tagging, or single-candidate binding.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Clinical Trial Arm-Intervention Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eqqskffnwbjebvm0ww60wa98bkq08
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Clinical trial registries describe each study as a set of participant arms and a set of interventions. In a well-formed registry record, each intervention is explicitly linked to the arm groups that receive it. Those links are operationally important: downstream reviewers use them to audit comparator structure, placebo control, combination therapy, and results denominators.
> In this challenge, each example is a real interventional ClinicalTrials.gov study. The public input keeps anonymized arm descriptions, anonymized intervention descriptions, conditions, and design metadata, but removes the explicit arm-to-intervention links. Arm nodes and intervention nodes are independently shuffled within each row, and local names, NCT identifiers, and dosage-like quantities are masked, so registry ordering, public trial IDs, and simple string-copy cues are not shortcuts. Your task is to reconstruct the hidden bipartite graph as a compact edge trace.
> This is not trial outcome prediction, patient-trial matching, or ordinary intervention classification. Solvers must infer a structured within-trial graph from noisy registry text, local aliases, study design cues, and many-to-many treatment structure.
> Output Format
> Submit one edge_trace per test row:
> BEGIN A01-I01 A01-I03 A02-I02 END
> Each edge token links one arm to one intervention. Tokens must be sorted first by arm number and then intervention number. Valid arms are A01 through A06; valid interventions are I01 through I08. Each row has its own arm_count and intervention_count; do not emit edges beyond that row's counts.
> Evaluation
> The score is maximized and ranges from 0 to 1. Malformed traces receive zero row credit. Structurally invalid CSV submissions are rejected.
> For each row:
> row_score =
> 0.70  *edge_f1*  edge_count_similarity^2
> + 0.30 * exact_graph
> edge_f1 is F1 over predicted versus gold graph edges. edge_count_similarity is min(predicted_edge_count / gold_edge_count, gold_edge_count / predicted_edge_count), and it is squared to strongly penalize both sparse under-prediction and dense over-prediction. exact_graph is 1 only when the full edge set is exactly correct. Edges outside a row's actual arm or intervention count receive zero row credit.
> The final score is the mean row score over all test examples.
> Dataset
> Public files:
> | File | Rows | Description |
> |---|---:|---|
> | train.csv | 4000 | Real ClinicalTrials.gov training studies with gold edge traces. |
> | test.csv | 700 | Real ClinicalTrials.gov test studies without edge traces. |
> | train_candidate_edges.csv | variable | One row per candidate train arm-intervention edge, with binary labels. |
> | test_candidate_edges.csv | variable | One row per candidate test arm-intervention edge, without labels. |
> | sample_submission.csv | 700 | Valid constant-format submission template. |
> Hidden file:
> | File | Rows | Description |
> |---|---:|---|
> | answers.csv | 700 | Hidden test edge traces. |
> train.csv columns:
> | Column | Meaning |
> |---|---|
> | id | An anonymous row ID. |
> | conditions | Semicolon-separated condition terms from the registry record. |
> | summary | Brief study summary with local treatment names masked. |
> | detailed_description | Longer registry description with local names and dosage-like quantities masked. |
> | eligibility_criteria | Inclusion/exclusion criteria text with local names and dosage-like quantities masked. |
> | primary_outcomes_json | JSON list of primary outcome measure text and time frames. |
> | secondary_outcomes_json | JSON list of secondary outcome measure text and time frames. |
> | allocation | Registry allocation field when available. |
> | intervention_model | Registry intervention model field when available. |
> | masking | Registry masking field when available. |
> | arm_count | Number of arm nodes in this row. |
> | intervention_count | Number of intervention nodes in this row. |
> | arms_json | JSON list of arm nodes with local IDs and anonymized text. |
> | interventions_json | JSON list of intervention nodes with local IDs and anonymized text. |
> | edge_trace | Gold graph edge trace. |
> test.csv has the same columns except edge_trace.
> The candidate-edge files flatten each study graph into all possible arm-intervention pairs. They are provided as a convenience for GPU pair scorers: train rows include a label column, while test rows omit it. The final submission is still one graph trace per study, so solvers must convert pair scores back into a valid edge set.
> train_candidate_edges.csv columns:
> | Column | Meaning |
> |---|---|
> | id | Anonymous study row ID, matching train.csv. Multiple candidate-edge rows share the same ID. |
> | arm | Candidate arm node token, such as A01. |
> | intervention | Candidate intervention node token, such as I03. |
> | conditions | Same registry condition terms as the parent study row. |
> | allocation | Same allocation design field as the parent study row. |
> | intervention_model | Same intervention model design field as the parent study row. |
> | masking | Same masking design field as the parent study row. |
> | arm_text | Anonymized text for this candidate arm node. |
> | intervention_text | Anonymized text for this candidate intervention node. |
> | summary | Same masked brief summary as the parent study row. |
> | detailed_description | Same masked detailed description as the parent study row. |
> | eligibility_criteria | Same masked eligibility text as the parent study row. |
> | primary_outcomes_json | Same masked primary outcome JSON as the parent study row. |
> | secondary_outcomes_json | Same masked secondary outcome JSON as the parent study row. |
> | label | Binary training target: 1 if this arm-intervention pair is a true graph edge, otherwise 0. |
> test_candidate_edges.csv has the same columns except it omits label. For every test study, it contains exactly arm_count * intervention_count rows: all possible candidate arm-intervention pairs for that study.
> The test split is restricted to larger sparse many-to-many arm-intervention graphs: each test row has at least 8 candidate edges and no more than 55 percent of candidate edges are gold edges. This is an intentional held-out complexity shift: training still contains many complex examples, but high test performance requires graph-aware decoding rather than diagonal matching, independent pair thresholding, or predicting dense edge sets.
> Submission
> Submit exactly these columns, in this order:
> id,edge_trace
> row_0123456789abcdef,BEGIN A01-I01 A02-I02 END
> row_fedcba9876543210,BEGIN A01-I01 A01-I02 A02-I03 END
> Requirements:
> Include exactly one row for every test ID.
> Use the exact column order shown above.
> Use only sorted edge tokens inside BEGIN and END.
> Do not include duplicate edges.
> Missing values, duplicate IDs, extra IDs, extra columns, or malformed traces are rejected or receive zero row credit.
> Save the file as ./working/submission.csv.
> Restrictions
> Use only the released public files and generally available methods. Do not use hidden files, source NCT identifiers, source manifests, row order, file order, hashes, external record lookup, or private registry-link fields. The challenge is designed so a local text-and-graph model can solve it from the anonymized public inputs.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cymbal Gesture Recognition and Trace Rebinding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fp87amm1zfd0embya13229n8b39c0
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Predict a percussion gesture record from two inputs: a short cymbal strike clip and a trace sheet containing three anonymous candidate signal cards. For each case, submit the five-part gesture staff, the 3 x 4 relation matrix that identifies which trace card belongs to the clip, and the archive disposition class.
> Each case contains one 0.96-second MP4 clip with synchronized video and audio from a real cymbal performance. The paired JPEG trace sheet contains three cards named X, Y, and Z. Exactly one trace card is derived from the same strike event as the clip. The other two cards are plausible decoys drawn from different recordings in the same split. Decoys may share the same stroke family, dynamic level, or damping state, so matching by a single visual or audio cue is not enough.
> The real-world scenario is multimodal archive repair for music-performance collections. A curator may have a camera clip, an audio channel, and detached trace summaries that lost their original binding. The task is to recover the gesture notation and rebind the correct trace evidence without access to source filenames or recording IDs.
> Ground truth is obtained from synchronized laboratory recordings. Preparation detects temporally separated cymbal strikes, extracts each event once, parses the performance condition from the original recording taxonomy, and builds trace sheets from local acoustic envelopes and spectral summaries. Training and test use disjoint original recordings, and hidden scoring gives each source recording equal weight.
> The outputs are:
> | Output | Prediction |
> |---|---|
> | `gesture_staff_program` | Canonical six-token description of family, zone, dynamic, damping, and direction |
> | `trace_relation_matrix` | A `3 x 4` matrix describing how trace cards `X`, `Y`, and `Z` relate to the clip |
> | `archive_disposition` | Review class describing whether the packet has clean or confusing trace evidence |
> This is an A10G challenge because strong solutions are expected to combine video, audio, rendered trace images, and structured decoding across hundreds of multimodal packets.
> Dataset
> The prepared release contains 257 labeled training events and 108 hidden test events. The training events come from 46 original recordings. The hidden events come from 22 different recordings. All 365 event clips are unique. No original recording appears in both train and test.
> | Path | Contents |
> |---|---|
> | `train.csv` | Four input columns and three target columns for 257 labeled events |
> | `test.csv` | The four input columns for 108 hidden events |
> | `sample_submission.csv` | A schema-valid baseline with the required output columns |
> | `clips/` | 365 opaque MP4 event clips |
> | `trace_sheets/` | 365 opaque JPEG trace sheets |
> Each MP4 is H.264 video at 416 by 256 pixels and 15 frames per second with mono AAC audio at 16 kHz. Each trace sheet is a 720 by 360 RGB JPEG. The three trace cards show normalized envelope and spectral-centroid curves computed from candidate strike windows. The card labels X, Y, and Z are visible and are the row order used by trace_relation_matrix.
> Input Columns
> | Column | Data type | Present in | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque identifier beginning with `q` followed by 22 hexadecimal characters |
> | `clip_path` | string | train, test | Relative path to a short MP4 clip, such as `clips/7d4b6763b0249e07bba02998.mp4` |
> | `trace_sheet_path` | string | train, test | Relative path to a JPEG trace sheet, such as `trace_sheets/67ec2a88ccd67db05196adf3.jpg` |
> | `notation_contract` | string | train, test | Fixed instruction: `match one trace card X/Y/Z to the clip and recover the five-part gesture staff` |
> Target Columns
> | Column | Data type | Present in | Description |
> |---|---|---|---|
> | `gesture_staff_program` | canonical token string | train | Six `>`-separated tokens describing the clip gesture |
> | `trace_relation_matrix` | JSON-encoded integer matrix | train | A `3 x 4` binary matrix for trace-card linkage and attribute sharing |
> | `archive_disposition` | categorical string | train | One of `clear_archive`, `crowded_decoys`, `resonant_collision`, or `low_energy_review` |
> Gesture Staff Program
> The program has exactly six >-separated tokens in this order:
> family:<family>>zone:<zone>>dynamic:<dynamic>>damping:<damping>>direction:<direction>>commit:gesture_staff
> Valid values:
> | Field | Valid values |
> |---|---|
> | `family` | `flam`, `roll`, `staccato`, `suspended_attack`, `suspended_nonattack`, `tremolo` |
> | `zone` | `center`, `middle`, `rim`, `full`, `sweep` |
> | `dynamic` | `soft`, `medium`, `strong`, `crescendo`, `diminuendo` |
> | `damping` | `open`, `damped` |
> | `direction` | `none`, `up`, `down` |
> Example:
> family:flam>zone:rim>dynamic:soft>damping:damped>direction:down>commit:gesture_staff
> Trace Relation Matrix
> Rows follow trace cards X, Y, and Z. Columns have this fixed order:
> | Column index | Meaning |
> |---:|---|
> | `0` | This trace card is linked to the clip event |
> | `1` | This trace card has the same stroke family as the clip |
> | `2` | This trace card has the same dynamic level as the clip |
> | `3` | This trace card has the same damping state as the clip |
> Every valid hidden matrix has exactly one row with column 0 equal to 1. The linked row is always [1,1,1,1]. Decoy rows can still contain 1 values in columns 1, 2, or 3 when they share those attributes with the clip.
> Example:
> [[0,1,0,1],[1,1,1,1],[0,0,1,0]]
> This example means trace Y is linked to the clip. Trace X shares family and damping, while trace Z shares dynamic only.
> Archive Disposition
> | Class | Meaning |
> |---|---|
> | `clear_archive` | The linked trace is distinct enough from the two decoys |
> | `crowded_decoys` | Multiple decoy traces share clip attributes |
> | `resonant_collision` | Long ringing behavior makes the correct trace harder to separate from a related decoy |
> | `low_energy_review` | The clip has weak impact energy and should be reviewed carefully |
> Example labeled row:
> | case_id | clip_path | trace_sheet_path | notation_contract | gesture_staff_program | trace_relation_matrix | archive_disposition |
> |---|---|---|---|---|---|---|
> | `q6e2c5f5a4f7c95764a46b0` | `clips/7d4b6763b0249e07bba02998.mp4` | `trace_sheets/67ec2a88ccd67db05196adf3.jpg` | `match one trace card X/Y/Z to the clip and recover the five-part gesture staff` | `family:staccato>zone:center>dynamic:medium>damping:open>direction:none>commit:gesture_staff` | `[[1,1,1,1],[0,0,1,0],[0,0,0,0]]` | `clear_archive` |
> Training Distribution
> Training family counts are: flam 68, tremolo 66, staccato 35, suspended_nonattack 35, suspended_attack 29, and roll 24.
> Training disposition counts are: resonant_collision 134, low_energy_review 109, crowded_decoys 11, and clear_archive 3.
> Submission Format
> Write the final CSV to exactly:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,gesture_staff_program,trace_relation_matrix,archive_disposition
> All columns are strings at CSV level. gesture_staff_program is limited to 180 characters and exactly six tokens. trace_relation_matrix is limited to 80 characters and must decode to a 3 x 4 binary integer matrix. archive_disposition must be one valid class listed above.
> Example:
> case_id,gesture_staff_program,trace_relation_matrix,archive_disposition
> q6e2c5f5a4f7c95764a46b0,family:staccato>zone:center>dynamic:medium>damping:open>direction:none>commit:gesture_staff,"[[1,1,1,1],[0,0,1,0],[0,0,0,0]]",clear_archive
> Extra or reordered columns, duplicate column names, duplicate IDs, unknown IDs, and missing or extra rows are rejected. An optional platform-managed visibility column is removed before schema validation. Malformed target values receive zero for their component without crashing the grader.
> Evaluation
> The metric is the Gesture Trace Rebinding Score. Higher is better.
> Minimum score: 0.0
> Maximum score: 1.0
> The final score is:
> Score =
> 0.40 * GestureStaffScore
> + 0.45 * TraceRelationScore
> + 0.15 * DispositionScore
> Scores are computed per hidden row, averaged within each hidden source recording, then averaged across source recordings. This recording-macro aggregation prevents one long recording from dominating the leaderboard.
> Gesture Staff Score
> The staff program is parsed into five key-value pairs plus the commit token. Let Y be the true set of five key-value pairs and P be the predicted set.
> PairF1 = 2 * |Y intersect P| / (|Y| + |P|)
> GestureStaffScore = 0.35 * PairF1 + 0.65 * I(the complete six-token program is exact)
> Malformed programs receive 0 for this component.
> Trace Relation Score
> For true matrix Y and predicted matrix P, EntryAgreement is the fraction of the 12 entries with equal values.
> TraceRelationScore = 0.25 * EntryAgreement + 0.75 * I(the complete matrix is exact)
> The predicted matrix must be 3 x 4, binary, and have exactly one linked row. Malformed matrices receive 0 for this component.
> Disposition Score
> DispositionScore = I(predicted archive_disposition equals the true class)
> Malformed classes receive 0 for this component.
> Hidden targets are validated strictly and are never clipped, filled, or repaired.
> What Makes This Interesting
> This task is not ordinary percussion classification. The trace sheet creates an evidence rebinding problem: the solver must compare a visible and audible strike with three anonymous signal cards, then say which card belongs to the clip and which decoys merely share family, dynamic, or damping attributes.
> The gesture staff also forces the model to separate related musical factors. A flam, a staccato stroke, and a suspended-cymbal attack can share loudness but differ in timing and visible stick behavior. A damped and open stroke can share onset but differ in decay. The matrix rewards this fine-grained relationship reasoning rather than a single class label.
> What Not To Use
> Do not map opaque IDs, filenames, file sizes, row order, trace-sheet hashes, or split position to targets.
> Do not fingerprint clips or trace sheets against external copies of the source recordings or reconstruct source filenames.
> Do not build lookup tables from media hashes, near-duplicate embeddings, or known recording identities.
> Do not exploit malformed CSV behavior, duplicate rows, parser limits, or grader exceptions.
> Do not adapt predictions with hidden answers or repeated leaderboard probing.
> Learned audiovisual models, spectrogram analysis, video gesture recognition, trace-image encoders, multimodal matching, and constrained decoding are allowed.
> Reference Validation
> The prepared release contains 365 unique MP4 clips and 365 unique trace sheets. Train and test source recordings are disjoint. Exact hidden answers score 1.0. The schema-valid sample scores approximately 0.15.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Latent Source Relevance Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx763e86yjqj7hmbcntcxd5h2x8bpjpf
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each item in this competition is a 10-second mono audio clip in which several unseen sound sources are active at once, their signals superimposed into a single waveform. Against a fixed pool of seven abstract candidate sources — labelled a through g, with their real-world identity intentionally withheld — your task is to rank the candidates by how prominently each one is present in the clip and express that ranking as a normalized relevance score per candidate. The output is a full relevance profile over the candidate pool (seven non-negative scores summing to 1), not a single top pick, because the sources genuinely co-occur: 65% of clips have two or more candidates active simultaneously, so a useful answer must order and weight the whole pool rather than name the single loudest.
> The task is deliberately blind: you are given the mixed waveform and, for training clips, the reference relevance profile — but never a clean, isolated example of any single candidate, and never the candidates' semantic identities. A good ranking must therefore disentangle superimposed contributions from the mixture itself. Clips come from several distinct acoustic environments captured at different times, so each clip's ranking must be read from its own audio rather than from a global popularity prior, and the train/test split is recording-disjoint — no source recording contributes clips to both splits — so neighbouring moments cannot be memorized. You must submit a full profile over all seven candidates, but the score is macro-averaged over a fixed scored subset of the pool — {b, c, e, f, g} — so that a rarely-prominent candidate counts as much as a common one; the single recurrent dominant source (a) and an ultra-sparse source (d) remain required in the profile but are excluded from the average, because agreement on them is nearly constant across submissions and would otherwise flatten the score. Under-ranking two designated critical candidates (c and e, both rare) is penalized asymmetrically, reflecting that failing to surface a faint but important source is costlier than over-ranking it.
> Dataset
> The data consists of short audio clips and, for the training split, their reference relevance profiles over the candidate pool.
> Public files
> train.csv — one row per training clip. Columns: id, audio_path, site_group, rel_a, rel_b, rel_c, rel_d, rel_e, rel_f, rel_g.
> test.csv — one row per test clip. Columns: id, audio_path.
> sample_submission.csv — a valid submission with constant placeholder scores.
> audio/ — a directory of 10-second mono WAV clips referenced by audio_path.
> Column descriptions
> The training and reference tables use the following columns. The seven rel_* columns together form the relevance profile: the score assigned to each candidate in the pool. Candidate identities are withheld; each is characterized only by its acoustic signature.
> id (string) — unique clip identifier (e.g. clip_1a2b3c4d).
> audio_path (string) — relative path to the clip's WAV file under audio/.
> site_group (string) — an anonymized identifier for the recording environment the clip was drawn from (e.g. env_0). Present in train.csv only, to support environment-aware cross-validation. Several environments are represented; each appears among both the training recordings and the (organizer-held) test recordings, but no individual recording is shared between splits.
> rel_a (float) — relevance score for candidate a: a recurrent broadband source, most often the dominant contributor. In [0, 1].
> rel_b (float) — relevance score for candidate b: a sustained low-frequency source with strong harmonic structure. In [0, 1].
> rel_c (float) — relevance score for candidate c: a narrowband high-pitched tonal source (a designated critical candidate). In [0, 1].
> rel_d (float) — relevance score for candidate d: a heavy broadband low-frequency source. In [0, 1].
> rel_e (float) — relevance score for candidate e: brief high-frequency friction transients (a designated critical candidate). In [0, 1].
> rel_f (float) — relevance score for candidate f: a steady stationary drone. In [0, 1].
> rel_g (float) — relevance score for candidate g: residual non-mechanical sound (voices, music, incidental noise). In [0, 1].
> For every clip the seven rel_* values are non-negative and sum to 1 (a normalized relevance profile over the candidate pool).
> Data example
> A truncated train.csv row:
> id,audio_path,site_group,rel_a,rel_b,rel_c,rel_d,rel_e,rel_f,rel_g
> clip_1a2b3c4d,audio/clip_1a2b3c4d.wav,env_0,0.58,0.19,0.00,0.00,0.05,0.14,0.04
> Submission format
> Submit a CSV with exactly these eight columns and one row per test clip:
> id,rel_a,rel_b,rel_c,rel_d,rel_e,rel_f,rel_g
> Exactly one row per id in test.csv — no missing and no extra ids.
> Each rel_* value must be a finite number ≥ 0 (the relevance score for that candidate).
> The seven scores in a row should sum to 1. Rows are renormalized to sum to 1 before scoring (a row summing within ±0.02 of 1 is accepted; a row summing to 0 or containing a negative or non-finite value is rejected).
> A header row is required.
> Sample submission (constant uniform relevance profile on every row):
> id,rel_a,rel_b,rel_c,rel_d,rel_e,rel_f,rel_g
> clip_1a2b3c4d,0.142857,0.142857,0.142857,0.142857,0.142857,0.142857,0.142857
> clip_5e6f7a8b,0.142857,0.142857,0.142857,0.142857,0.142857,0.142857,0.142857
> Evaluation
> The metric is Macro Profile Agreement (MPA) — a candidate-macro-averaged agreement between predicted and reference relevance profiles across the test set, with an asymmetric penalty for under-ranking the two designated critical candidates.
> Let p[i] and t[i] be the predicted and reference 7-vectors for test clip i (each renormalized to sum to 1), over i = 1..N clips. Candidates are indexed k ∈ {a, b, c, d, e, f, g}. The macro average is taken over the scored subset K_s = {b, c, e, f, g}. Candidates a and d are still required in every submitted profile and still participate in the sum-to-1 renormalization — so mis-estimating their mass distorts the scored candidates — but they are excluded from the macro average: a is the recurrent dominant source that a trivial prior already agrees with almost perfectly, and d is too sparse to recover reliably, so including either would add a near-constant term to every submission's score.
> Per-candidate agreement (normalized L1 across clips). For each scored candidate k ∈ K_s:
> num_k = sum_i | p[i,k] - t[i,k] |
> den_k = sum_i ( p[i,k] + t[i,k] )
> agreement_k = 1 - num_k / den_k          # in [0, 1]; skipped if den_k == 0
> Because each candidate is normalized by its own total relevance mass, a rarely-prominent candidate contributes on the same footing as a frequently-dominant one — the ranking cannot be won by always favouring the majority candidate.
> Macro agreement. Average the per-candidate agreements over the scored subset present in the test set:
> macro_agreement = mean_{k in K_s} agreement_k          # K_s = {b, c, e, f, g}
> Asymmetric critical-candidate penalty. For the designated critical set S = {c, e} (two rare, high-importance candidates), measure the fraction of each candidate's true relevance mass that was under-ranked (scored lower than reference), and penalize it:
> missed_k = sum_i max(0, t[i,k] - p[i,k]) / sum_i t[i,k]     # for k in S
> penalty  = LAMBDA * mean_{k in S} missed_k                  # LAMBDA = 0.25
> Over-ranking a critical candidate is not penalized here — only failing to surface it is.
> Final score.
> MPA = max(0.02, macro_agreement - penalty)
> Higher is better. The score lies in [0, 1] (clamped to a small positive floor of 0.02). A perfect ranking scores 1.0. A constant uniform profile (the sample submission) scores about 0.15, and a constant profile equal to the global training-set average scores near 0.03 — both far below the achievable range, because a fixed profile cannot track which sources are present in an individual clip. Concentrating all mass on a single candidate scores at the floor, because the macro average collapses on every scored candidate that choice ignores.
> Score direction: higher is better.
> What Not To Use (Prohibited Methods)
> This challenge must be solved from the provided audio and training relevance profiles only. The following are prohibited:
> No external answer keys or reference profiles. Do not use any external database of audio recordings, event annotations, or pre-computed source labels to recover the reference scores for the test clips.
> No id- or filename-based hardcoding. Do not map clip ids or file paths to target values, and do not encode any per-id lookup table of scores.
> No matching test clips back to any external source. Do not attempt to identify the original recording, location, timestamp, or coordinates behind any clip, and do not use any external recording that could correspond to a test clip.
> No train/test leakage. Do not use the test audio (or statistics computed over the full test set that reveal per-clip targets) to fit or calibrate the scores; predictions for a test clip must depend only on that clip and the training data.
> No manual annotation of the test set. Do not hand-label or manually estimate the relevance profile of test clips.
> No private-label tuning. The reference profiles for the test set are organizer-only; do not attempt to obtain or approximate them from any non-provided source.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Recovering Denied Echo Structure From A First-Return Point Cloud

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74aws5kjsdx37tkkdgkzn3j58bmc4h
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Home
> Recovering Denied Echo Structure From A First-Return Point Cloud
> Editor View
> Recovering Denied Echo Structure From A First-Return Point Cloud
> Flag Problem
> DOMAIN
> Other
> DIFFICULTY
> Medium
> SCORING
> ↑ Higher is better
> COMPUTE
> A10G
> STATUS
> Accepted
> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (0)
> Your Submissions
> Background
> An airborne laser scanner sweeps a forest and fires millions of short pulses at the canopy. Most pulses do not stop at the first thing they touch. A pulse that clips the edge of a leaf keeps going, strikes a branch, then understorey, then perhaps the ground, and the instrument records a separate echo for each surface. The sequence of echoes from a single pulse is a vertical transect through the canopy — a direct measurement of what is underneath the outer surface.
> You are given a point cloud from which every echo after the first has been deleted. What remains is exactly one point per emitted pulse: the outer skin of the forest, and nothing below it.
> Your task is to recover what the deleted echoes would have said.
> This is not an obfuscation. The later echoes are not present in your input in any encoded form — they were physically removed. You are inferring the interior of a canopy from its surface.
> The task
> For each designated query pulse, predict two things.
> 1. echo_class — how many further surfaces that pulse struck.
> This is a class index, not a count. The mapping is:
> echo_class	further echoes after the first	total echoes from that pulse
> 0	1	2
> 1	2	3
> 2	3 or more	4 or more
> Note that the class index is one less than the number of further echoes, because the classes are numbered from zero and no pulse in the graded set has zero further echoes. Read echo_class == 0 as "the smallest category", not as "no extra returns".
> Every graded pulse produced at least one further echo, so there is no "the pulse stopped here" class. The easy discrimination — canopy versus bare ground — has already been removed.
> 2. depth_class — how far down the standing column the pulse burned before its last echo.
> Define, for a query pulse,
> r = (z_first - z_last) / max(z_first - g, 1.0)
> where z_first is the height of the pulse's first echo (a point you are given), z_last is the height of its last echo (withheld), and g is the ground reference defined below. Then
> value	range of r
> 0	r <= 0.25
> 1	0.25 < r <= 0.55
> 2	0.55 < r <= 0.85
> 3	r > 0.85 — the pulse burned through to the ground layer
> The ground reference g is published, not withheld
> g is a deterministic function of the point cloud you are given. It is not an estimate of the true terrain and it is not a hidden quantity — it is a definition, and you can reproduce it exactly. Only the numerator of r is withheld.
> import numpy as np
> def ground_reference(x, y, z):
> # x, y, z are float64 upcasts of the first three float32 columns of the points array.
> # Returns one reference height per point: the 5th percentile of height among all points
> # falling in the same 5 m x 5 m cell.
> ix = np.floor((x - x.min()) / 5.0).astype(np.int64)
> iy = np.floor((y - y.min()) / 5.0).astype(np.int64)
> key = iy * (ix.max() + 1) + ix
> order = np.argsort(key, kind="stable")
> key_s, z_s = key[order], z[order]
> starts = np.flatnonzero(np.append(True, key_s[1:] != key_s[:-1]))
> ends = np.append(starts[1:], len(key_s))
> g = np.empty(len(z), dtype=np.float64)
> for s, e in zip(starts, ends):
> g[order[s:e]] = np.percentile(z_s[s:e], 5.0)
> return g
> Every graded pulse satisfies z_first - g >= 2.0.
> Files
> The dataset directory contains three CSV files and two folders.
> train.csv — one row per labelled query pulse.
> test.csv — one row per query pulse you must predict.
> sample_submission.csv — a correctly formatted submission with placeholder values.
> train/ — one .npz file per training item, named <item_id>.npz.
> test/ — one .npz file per test item, named <item_id>.npz.
> Columns of train.csv
> There are five columns.
> id — string. Unique identifier of one query pulse. This is the identifier your submission must use.
> item_id — string. Identifies the item this pulse belongs to; the corresponding point cloud is train/<item_id>.npz.
> query_index — integer. Row index into that item's points array identifying which pulse this is. Zero-based.
> echo_class — integer in {0, 1, 2}. The first target, defined above.
> depth_class — integer in {0, 1, 2, 3}. The second target, defined above.
> Columns of test.csv
> There are three columns: id, item_id and query_index, with the same meanings as above. The two target columns are absent.
> Columns of sample_submission.csv
> There are three columns: id, echo_class and depth_class, in that order. This is exactly the format your submission must have.
> Contents of each .npz file
> Each .npz contains two arrays.
> points — float32 array of shape [N, 4], where N is between 3,000 and 60,000. The four columns are, in order: x (metres, recentred on the item), y (metres, recentred), z (metres, on an arbitrary per-item datum), and intensity (dimensionless, rescaled per item into [0, 1]). Each row is one emitted pulse, represented by its first echo only. Row order is shuffled and carries no meaning.
> queries — int32 array of shape [Q]. Row indices into points marking the graded pulses. These are the same values as the query_index column.
> Items are square ground patches 40 m on a side. Nothing else is provided: there is no return count, no scan angle, no timestamp, no classification, no georeference and no acquisition metadata.
> Evaluation
> Both targets are scored by macro-F1, each normalised against uninformed guessing, then combined.
> S(F1, K) = clip( (F1 - 1/K) / (1 - 1/K), 0.01, 1.0 ) score = clip( 0.60 * S(macro_F1(echo_class), 3) + 0.40 * S(macro_F1(depth_class), 4), 0.01, 1.0 )
> The held-out answers are stratified so that every class of both targets is equally frequent. Consequently uniform-random guessing scores 1/K macro-F1 on each head, and any constant submission scores less than that. Both floor at 0.01. Predicting the training prior does not help.
> Higher is better. The maximum is 1.0.
> Submission format
> Produce a CSV with exactly three columns in this order: id, echo_class, depth_class.
> Exactly one row per id in test.csv, no more and no fewer.
> echo_class must be an integer in {0, 1, 2}.
> depth_class must be an integer in {0, 1, 2, 3}.
> No missing, non-integer, or out-of-range values.
> The grader rejects a submission outright — it does not partially credit it — if the column names or order differ, if the set of ids does not match test.csv exactly, if any id is duplicated, or if any value is missing, non-integer or out of range.
> Notes on the split
> Training and test items are separated structurally, not randomly. No test item is drawn from the same locality as any training item, and a buffer distance is enforced between them, so neighbouring patches never straddle the split. Validate accordingly: a random split of the training items will overstate your score, because nearby patches share stand structure.
> Query pulses have been sampled so that height above the ground reference and intensity have matched distributions across every target class. A model that reads only those two scalars will score at chance. The information that remains is in the three-dimensional arrangement of the surrounding first returns.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Hidden Fragmentation Lattice Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cenvp796dzhshe1z4n83bhd8bqbyn
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Tandem mass spectrometry can observe the same chemical source under several fragmentation mechanisms and energies. Those observations are related, but their fragment patterns can change sharply as collision energy or fragmentation physics changes. In this challenge, the original chemical provenance has been removed.
> Each case contains a shuffled set of anonymous, de-identified spectrum cards derived from exactly eight hidden source compounds. Each source compound is observed in 3 to 6 regimes (inclusive) chosen from the six physical fragmentation regimes listed below, so an individual source may be missing zero, one, two, or three regimes. At the case level, all six regimes are always represented by at least one spectrum. The solver receives only measurement-derived internal fragment-difference features; chemical names, formulas, structures, precursor masses, source filenames, database identifiers, and original source identifiers are not provided.
> For every spectrum card, predict both:
> its physical fragmentation regime; and
> its latent source group within the case.
> The latent group numbers are local and permutation-invariant. The grader evaluates which spectra are grouped together and which typed lattice edges the complete prediction induces; it does not require a hidden source to use the same numeric group label as the ground truth.
> This is a coupled hidden-structure reconstruction task. Regime recognition alone is insufficient, and source grouping alone is insufficient. High scores require jointly recovering the hidden fragmentation state and cross-regime source correspondence structure.
> Fragmentation Lattice
> The six regimes form the fixed 2 x 3 lattice:
> CID20 ---- CID40 ---- CID60
> |          |          |
> EAD12 ---- EAD16 ---- EAD24
> The seven scored adjacency types are:
> CID20 <-> CID40
> CID40 <-> CID60
> EAD12 <-> EAD16
> EAD16 <-> EAD24
> CID20 <-> EAD12
> CID40 <-> EAD16
> CID60 <-> EAD24
> A true typed lattice edge exists when two spectra from the same hidden source are both present at one of these adjacent regime pairs.
> Dataset
> The prepared public dataset contains 75 labeled training cases and 25 held-out test cases. Complete hidden source compounds are disjoint between train and test; no source compound occurs in both splits. Each case contains spectra from all six fragmentation regimes, although any one hidden source compound may appear in only 3 to 6 of them.
> train.csv
> One row per labeled training spectrum:
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Opaque case identifier. |
> | spectrum_id | string | Opaque spectrum-card identifier. |
> | regime | string | True fragmentation regime: CID20, CID40, CID60, EAD12, EAD16, or EAD24. |
> | compound_slot | int | Local hidden-source label from 0 through 7. The numeric value has no meaning across cases. |
> test.csv
> One row per held-out spectrum:
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Opaque case identifier. |
> | spectrum_id | string | Opaque spectrum-card identifier. |
> The test labels are withheld.
> Case feature files
> Training arrays are stored in train_cases/<case_id>.npz; test arrays are stored in test_cases/<case_id>.npz.
> Each NPZ contains:
> | Array | Type | Shape | Description |
> |---|---|---|---|
> | spectrum_id | string | (N,) | Spectrum IDs for the rows in that case file. |
> | gap_histogram | float32 | (N, 512) | Normalized weighted histogram of internal relative fragment-mass differences. |
> | gap_quantiles | float32 | (N, 256) | Weighted quantiles of the same internal fragment-difference distribution. |
> Rows of gap_histogram and gap_quantiles correspond exactly to spectrum_id in the same NPZ file.
> lattice.json contains the six regime names, the seven fixed adjacency pairs, the feature dimensions, and the hidden-group count.
> Prediction Objective
> For every row of test.csv, predict:
> predicted_regime: one of the six allowed fragmentation regimes;
> predicted_group: an integer from 0 through 7 identifying the predicted latent source group within that case.
> Group labels are permutation-invariant. For example, if a true hidden source is labeled 2, predicting the same complete source partition under label 6 is not penalized merely because the numeric label differs.
> The structural objective is to recover both the latent partition of spectra into sources and the typed cross-regime lattice edges induced by those source groups.
> Submission Format
> Submit submission.csv with exactly these columns:
> case_id,spectrum_id,predicted_regime,predicted_group
> case_...,sp_...,CID40,0
> case_...,sp_...,EAD16,0
> case_...,sp_...,CID20,1
> Requirements:
> include one prediction row for every test (case_id, spectrum_id) pair;
> do not duplicate a (case_id, spectrum_id) pair;
> predicted_regime must be one of CID20, CID40, CID60, EAD12, EAD16, EAD24;
> predicted_group must be an integer from 0 through 7.
> See sample_submission.csv for a structurally valid but intentionally weak example.
> Evaluation
> Each case is scored using three deterministic components. Let S_c denote the score for case c. The final challenge score is the arithmetic mean of S_c over the evaluated cases.
> 1. Typed lattice-edge F1 — 60%
> For a case, construct the true typed-edge set T_edge as follows. For each true source group and for each of the seven fixed adjacent regime pairs (a,b), if that source contains a spectrum u at regime a and a spectrum v at regime b, add the typed edge
> (a, u, b, v)
> to T_edge.
> Construct the predicted typed-edge set P_edge in exactly the same way, but using predicted_group and predicted_regime.
> A predicted edge is therefore correct only if:
> the two spectrum IDs are the correct same-source pair; and
> they are assigned to the correct two endpoint regimes of the lattice adjacency.
> For any two finite sets T and P, the set-F1 used by the grader is:
> F1_set(T,P) = 2 * |T ∩ P| / (|T| + |P|)
> with these explicit edge cases:
> F1_set(∅,∅) = 1
> F1_set(T,∅) = 0  when T is non-empty
> F1_set(∅,P) = 0  when P is non-empty
> Thus:
> typed_lattice_edge_F1 = F1_set(T_edge, P_edge)
> Equivalently, when both sets are non-empty, if TP = |T_edge ∩ P_edge|, FP = |P_edge \ T_edge|, and FN = |T_edge \ P_edge|, then:
> typed_lattice_edge_F1 = 2*TP / (2*TP + FP + FN)
> 2. Latent-source partition F1 — 25%
> For each unordered pair of distinct spectrum IDs {u,v} in the case:
> place {u,v} in the true pair set T_pair if u and v have the same true compound_slot;
> place {u,v} in the predicted pair set P_pair if u and v have the same predicted_group.
> The partition score is the same set-F1 defined above:
> partition_F1 = F1_set(T_pair, P_pair)
> So, when both pair sets are non-empty:
> TP_pair = |T_pair ∩ P_pair|
> FP_pair = |P_pair \ T_pair|
> FN_pair = |T_pair \ P_pair|
> partition_F1 = 2*TP_pair / (2*TP_pair + FP_pair + FN_pair)
> If both pair sets are empty, partition_F1 = 1. If exactly one is empty, partition_F1 = 0.
> Because the metric depends only on same-group relations, it is invariant to any permutation of predicted group numbers.
> 3. Regime macro F1 — 15%
> For each regime r among the six allowed regimes, compute:
> TP_r = number of spectra whose true regime is r and predicted regime is r
> FP_r = number of spectra whose true regime is not r but predicted regime is r
> FN_r = number of spectra whose true regime is r but predicted regime is not r
> Then:
> F1_r = 2*TP_r / (2*TP_r + FP_r + FN_r)
> Every valid case in this dataset contains at least one true spectrum from each of the six regimes. Therefore, for every regime r, TP_r + FN_r > 0, so the denominator 2*TP_r + FP_r + FN_r is always positive on the benchmark and the zero-denominator situation cannot occur for a valid case.
> For defensive robustness only, the grader defines F1_r = 0 if a zero denominator were ever encountered. This fallback is unreachable for the released ground truth and therefore does not reduce the score of a perfect prediction.
> The regime component is the unweighted mean over all six regimes:
> regime_macro_F1 = (1/6) * Σ_r F1_r
> Case and leaderboard score
> For each case:
> S_c = 0.60 * typed_lattice_edge_F1
> + 0.25 * partition_F1
> + 0.15 * regime_macro_F1
> The leaderboard score is:
> score = (1/C) * Σ_c S_c
> where C is the number of evaluated cases.
> The score range is 0.0 to 1.0, and higher is better. A perfect reconstruction scores 1.0.
> Expected Methods
> The task is designed for a GPU runtime and genuine learned representation training. Strong approaches may combine:
> neural encoders over the 512-bin and 256-quantile spectral representations;
> contrastive or metric learning across known training source groups;
> regime-conditioned pair scoring;
> cross-spectrum attention or set encoders;
> learned compatibility matrices followed by constrained assignment;
> graph neural networks or message passing over candidate correspondences;
> discrete or differentiable global decoding.
> No particular architecture is required. Strong solutions should learn from the provided training cases and reconcile local evidence into a coherent case-level reconstruction.
> Forbidden Methods
> Do not use external datasets, network APIs, chemical databases, hidden source repositories, or provenance lookup to identify the removed compounds or original spectra. Do not recover labels from upstream source identifiers or raw-dataset construction artifacts.
> Solutions must learn from the provided public training data and solver-facing feature arrays.
> Runtime
> This challenge is intended for the configured GPU runtime. The complete solution must run end-to-end within the platform time limit and write the final submission to the required working directory.
> Submissions
> 24

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Climate Observation Networks Under Station Failure

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70b8r0nhwk0hj5w4hs6706sh8dr7hx
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.298

Full challenge description from page:

> Overview
>
> Predict which three observation sites should be funded, and which backup site should replace each of them if it fails. The selected network should still distinguish competing future climate projections when any one station is unavailable. Also predict each site's information level and the redundancy between sites, which explain the planning decision.
>
> Remote monitoring networks can lose stations to equipment failure or access restrictions. Funding the three strongest individual sites may leave almost identical observations after a failure. This challenge evaluates a learned, failure-aware network design from historical temperature and precipitation patterns.
>
> Each example contains climate patches for ten candidate locations, locally labeled A-J. The scientific data are monthly gridded fields for Greenland at approximately 10 km spacing. Training targets summarize four late-century scenario projections. They are benchmark measures of scenario disagreement, not measured forecast accuracy, actual station reliability, or observations of equipment failures.
>
> The grader measures the usefulness of the selected network and its contingency plan. Alternative decisions tied with the best one receive equal decision credit.
>
> Dataset
>
> There are 3,000 training cases and 700 test cases. Cases reuse locations within their own split; they are not 3,700 independent geographic surveys.
>
> | File | Contents |
> |---|---|
> | `train.csv` | Both input columns and all four target columns, one case per row. |
> | `test.csv` | Only `case_id` and `climate_packet_path`. |
> | `sample_submission.csv` | Every test ID with varied legal baseline predictions in submission order. These are format examples, not model predictions. |
> | `climate_packets/*.npz` | One packet per case, referenced relative to the public root. |
>
> Inputs
> | Column | Data type | Meaning |
> |---|---|---|
> | `case_id` | string | Opaque identifier beginning with `case_`; preserve unchanged. |
> | `climate_packet_path` | path string | For example `climate_packets/4fc12e9a66b374fc62c9e2be.npz`. |
>
>
> Load packets with numpy.load(path, allow_pickle=False).
>
> | Array | Data type and shape | Meaning |
> |---|---|---|
> | `baseline_patches` | float16, 10 x 4 x 21 x 21 | Historical neighborhoods in A-J order. All values are finite. |
> | `candidate_labels` | one-byte string, length 10 | A-J labels in array order. |
>
>
> The four channels are annual-mean near-surface temperature, seasonal temperature standard deviation, annual-mean precipitation, and seasonal precipitation standard deviation. They summarize twelve climatological months. Normalization medians and scales use training footprints only. Each patch is rotated, optionally reflected, and receives channel gains between 0.88 and 1.12, small offsets, and approximately 3.5% missing spatial cells filled with zero. Zero is also a valid normalized value; no missing-cell mask is supplied.
>
> Geographic Separation
>
> The source grid is partitioned before sampling. A center is retained only if its complete 21 x 21 input window lies within one split's pixel allocation. This also contains the smaller 7 x 7 future-summary window. Preparation verifies that the unions of training and test source pixels do not intersect. There are 660 eligible training centers across 20 represented blocks and 235 test centers across 10 represented blocks. Each case selects one location from each of ten distinct blocks.
>
> This prevents a held-out neighborhood, including an augmented version, from appearing in training. It tests transfer to unseen spatial regions. It does not remove broad physical correlations between regions or prove a public source map cannot be reverse-matched. Rotations and calibration changes are augmentation, not a secrecy guarantee. External coordinate recovery is prohibited; generalization and difficulty still require empirical solver evaluation.
>
> Targets
> | Column | Data type | Meaning |
> |---|---|---|
> | `candidate_information_vector` | JSON integer array encoded as a string, length 10 | Levels 0-4 for A-J; higher means greater scenario separation. Reference vectors contain two entries at each level. |
> | `redundancy_matrix` | JSON integer matrix encoded as a string, 10 x 10 | Pairwise redundancy levels 0-3. Higher means more similar future-response patterns. Symmetric, zero diagonal. |
> | `observation_portfolio` | string | Three distinct A-J labels, alphabetically sorted and joined by `|`. |
> | `outage_replacement_vector` | JSON integer array encoded as a string, length 10 | Entry i is the backup if selected site i fails. A-J map to 0-9. Unselected entries must be -1. Backups must be outside the original trio. One backup may serve different failure scenarios because outages are evaluated separately. |
>
>
> The private answer table contains case_id followed by these four targets. It is not supplied to participants.
>
> Planning Rules
>
> At each site, the future fields first supply monthly means and standard deviations for temperature anomaly, precipitation ratio, and precipitation anomaly. The spatial mean and standard deviation of each of those six maps over the 7 x 7 neighborhood form a 12-value signature for each scenario. For every signature dimension, divide scenario differences by its standard deviation across the four scenarios plus 0.00001. Euclidean distances of these standardized differences define discrimination: the smallest pairwise distance plus 0.25 times the average pairwise distance. Candidates sorted by discrimination receive levels 0,0,1,1,2,2,3,3,4,4, with index order breaking ties.
>
> Positive correlations between flattened scenario signatures define redundancy. The 45 unordered candidate pairs are sorted by correlation and then indices. Rank r, starting at zero, receives level min(3, floor(4*r/45)).
>
> Let q[i] be the true information level and R[i,j] the true redundancy. For a site set T:
>
> U(T) = sum(i in T)(q[i] + 1) - 0.72 * sum({i,j} subset of T) R[i,j]
> W(S) = min(f in S) U(S without f)
>
> Choose a three-site set S maximizing W(S), the least informative surviving pair's utility after one failure. For each selected site f, let B = S without f. Choose replacement j outside S maximizing W(B union {j}). This restores a network that can again tolerate one failure. Other replacement-vector entries are -1. Alphabetical order breaks set ties; the lowest index breaks replacement ties.
>
> Evaluation
>
> The training cases contain 2,906 distinct information vectors, 2,855 distinct redundancy matrices, and 1,471 distinct backup vectors. All 120 possible selected trios occur in both training and test. These are output-diversity counts, not independent geographic sample counts.
>
> The Single-Outage Network Design Score has four components. All component scores average over hidden cases. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
>
> InformationScore
>
> For prediction p and reference q, E is the fraction of ten exactly matching entries, X is whole-vector exact match (0 or 1), and D is mean absolute entry error.
>
> information_case = 0.72*X + 0.20*E + 0.08*(1 - D/4)
> InformationScore = mean(information_case)
>
> RedundancyScore
>
> For valid symmetric matrices, E and D are exact agreement and mean absolute error over the 90 off-diagonal entries. X is whole-matrix exact match.
>
> redundancy_case = 0.76*X + 0.17*E + 0.07*(1 - D/3)
> RedundancyScore = mean(redundancy_case)
>
> NetworkScore
>
> Evaluate W for all 120 legal trios using hidden q and R. Let m be their mean and b their maximum. Define:
>
> N(u; m,b) = clip((u-m)/(b-m), 0, 1), if b-m >= 1e-9
> N(u; m,b) = 1, otherwise
> network_case = N(W(submitted S); m,b)
> NetworkScore = mean(network_case)
>
> The tie case handles equal-utility alternatives. Mean-utility or worse networks get zero; maximizing networks get one. Per-case clipping means this is not a zero-expectation random-baseline correction.
>
> RecoveryScore
>
> Recovery uses the submitted trio, not just the canonical trio. For each of its three failed-site scenarios, enumerate seven legal backups and compute each restored network's W. Apply N using the mean and maximum of those seven utilities. Average the three results for that case, then average cases for RecoveryScore.
>
> An invalid trio, replacement vector, inactive entry, or backup selection makes the entire case recovery score zero. A good conditional backup can receive credit even when the initial trio is suboptimal.
>
> Final Score
>
> Score = 0.20*InformationScore + 0.25*RedundancyScore
> + 0.30*NetworkScore + 0.25*RecoveryScore
>
> Malformed estimates score zero for their component. Planning utilities use hidden information and redundancy, never submitted estimates. Invalid hidden answers raise an error; ground truth is never clipped.
>
> Submission Format
>
> Write ./working/submission.csv with exactly these columns in order:
>
> case_id,candidate_information_vector,redundancy_matrix,observation_portfolio,outage_replacement_vector
>
> | Column | Required value | Limit |
> |---|---|---|
> | `case_id` | Unchanged test identifier string | 64 characters |
> | `candidate_information_vector` | 10 integer-valued JSON numbers, each 0-4 | 48 characters |
> | `redundancy_matrix` | Symmetric 10 x 10 JSON matrix, entries 0-3, zero diagonal | 320 characters |
> | `observation_portfolio` | Three distinct sorted A-J labels separated by `|` | 5 characters |
> | `outage_replacement_vector` | 10 integer-valued JSON numbers, -1 through 9, satisfying planning rules | 48 characters |
>
> For example, A|D|J permits vector [1,-1,-1,5,-1,-1,-1,-1,-1,8]: replace A with B, D with F, or J with I. This illustrates syntax, not optimality.
>
> | case_id | candidate_information_vector | redundancy_matrix | observation_portfolio | outage_replacement_vector |
> |---|---|---|---|---|
> | `case_0011d64b3e1a1a4c02f5b0` | `[3,1,0,2,0,2,1,4,3,4]` | `[[0,2,0,2,0,2,0,2,2,2],[2,0,0,3,0,3,0,2,3,2],[0,0,0,0,0,0,0,0,0,1],[2,3,0,0,1,3,1,2,3,3],[0,0,0,1,0,1,1,1,1,1],[2,3,0,3,1,0,1,2,3,3],[0,0,0,1,1,1,0,1,1,2],[2,2,0,2,1,2,1,0,3,3],[2,3,0,3,1,3,1,3,0,3],[2,2,1,3,1,3,2,3,3,0]]` | `A\|H\|J` | `[8,-1,-1,-1,-1,-1,-1,8,-1,8]` |
>
> Booleans, numeric strings inside JSON, nonfinite values, wrong shapes, and out-of-range entries are invalid. Length checks precede parsing. Extra/reordered columns, missing/additional rows, duplicate IDs or column names, and unknown IDs reject the submission. Row order can vary because IDs are aligned after validation.
>
> What Makes This Interesting
>
> The objective is robustness to failure followed by restoring that robustness with a backup. A modest-information site may protect the weakest surviving pair. One candidate may be a useful backup for one outage and a poor backup for another. Geographic representation learning therefore supports a worst-case intervention decision. This is the benchmark's intended distinction, not a claim that resilient experimental design itself is new.
>
> What Not To Use
>
> Use the supplied public evidence and training labels. Do not recover source coordinates or future fields through external map matching, reverse identifiers, use private artifacts, or exploit file order or names as labels. External pretrained representations are allowed only when they do not provide source-specific hidden outcomes.
>
>  
>
> Submissions
> 39
> Top Score
> 0.298
> Created
> Sep 5, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> Grace-period rankings
> Lockdown
>
> The continuing roster is selected after the one-hour grace period; pre-cutoff submissions get up to one additional hour to finish.
>
> Closing in 10h 50m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## e

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx733ebk2s9t3hm9yz2t5nhpyd8dy9xw
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 4h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## d

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx700k8cfywzhyqhp5sj8ga1k18dztgg
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 4h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## c

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75nwtqhx81axjfgxf7j23b498dys0h
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 4h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## b

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70a9nfmt5qvx2g69e3q6hxws8drrsb
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 4h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## sep 4

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7emzz0f2qsyqf7576hvzfra98dsfpk
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 7h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Counterfactual Hypercube Recurrence Operator Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70q3nthz8ng3c01tk1ayfm6s8bxxvr
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jlm99's score of 0.613!

Full challenge description from page:

> Counterfactual Hypercube Recurrence Operator Inference Overview Each object contains four calibrated detector traces: two complementary views of a current receiver window and two views of the corresponding one-cycle-earlier window. Every trace is divided into sixteen signal blocks. For each window, you also receive sixteen candidate symbol tracks arranged as a row-local hypercube. Exactly one candidate is the organizer-known latent track, but the correct candidate index changes independently from row to row. Your task is to predict a soft 16 by 16 transport matrix connecting the sixteen earlier positions to the sixteen current positions. Task For every test object, submit one doubly stochastic matrix: Row i represents current position i. Column j represents earlier position j. Every value must be finite and between 0 and 1. Every row must sum to 1 within 1e-6. Every column must sum to 1 within 1e-6. The hidden target is a strict permutation matrix. A one at row i, column j means that earlier position j is assigned to current position i. Object-specific transport uncertainty The target permutation is the minimum-cost assignment under a row-specific organizer utility. Its edge cost combines: disagreement between the two hidden symbol values; multiview signal-block shape distance; forward cyclic displacement; a bounded edge-specific preference used to distinguish near ties. The relative contributions vary independently by object under one fixed challenge-wide distribution. The private coefficient and edge-preference draws are not released. Therefore, no single global coefficient vector exactly regenerates every target. The statistically appropriate prediction may be a soft posterior mean over plausible permutation matrices. The metric accepts such calibrated uncertainty instead of requiring an unjustified hard guess. Dataset files train.csv contains 2,172 rows and these columns: id: unique opaque object identifier. alphabet_size: categorical token A2, A4, or A8. intervention_flag: categorical token I0 or I1. setting_b: categorical operating-duration token beginning with B. current_trace_a_json: JSON list of 256 finite signal values. current_trace_b_json: JSON list of 256 finite signal values. lagged_trace_a_json: JSON list of 256 finite signal values. lagged_trace_b_json: JSON list of 256 finite signal values. current_candidates_json: JSON list containing sixteen candidate tracks, each a list of sixteen integer symbols. lagged_candidates_json: JSON list containing sixteen candidate tracks, each a list of sixteen integer symbols. recurrence_transport_json: training target, represented as 256 row-major numbers. test.csv contains 496 rows with the same public input columns but without recurrence_transport_json. sample_submission.csv contains: id: every test identifier exactly once. recurrence_transport_json: a valid row-specific placeholder permutation. benchmark_protocol.md contains the technical measurement, split, target, and scoring protocol. Signal and candidate representation Each 256-value detector trace contains sixteen consecutive blocks of sixteen values. Block k corresponds to candidate-track position k. Each candidate field contains sixteen possible length-16 symbol tracks. Exactly four track coordinates vary between two alphabet-valid alternatives. All sixteen binary combinations occur exactly once. Candidate ordering has no meaning across rows or between the current and lagged windows. Partition The split holds out four complete experimental runs: Training objects: 2,172 from seventeen runs. Test objects: 496 from four runs. Test-to-train ratio: 22.84%. Every object from the same run remains on one side of the split. Neighboring windows cannot cross the boundary. Operating-duration categories B4 and B7.5 occur only in test, while alphabet and intervention categories remain represented in training. Submission format Submit a CSV with exactly two columns in this order: id recurrence_transport_json Rows may appear in any order because scoring aligns them by id. Each recurrence_transport_json value must decode to one flat JSON list of exactly 256 numbers in row-major order. Do not submit a nested matrix. Evaluation Let Y be the hidden 16 by 16 permutation matrix and P be the submitted doubly stochastic matrix. squared_error = sum((P - Y)^2) row_skill = max(0, 1 - squared_error / 15) final_score = mean(row_skill over all 496 test objects) The normalization constant 15 is exactly the squared error of the uniform 1/16 matrix against any 16 by 16 permutation matrix. Consequently: an exact target permutation scores 1; the uniform doubly stochastic matrix scores 0; a calibrated soft matrix receives partial credit according to squared error. Invalid predictions A row receives zero if its matrix is malformed, has the wrong length, contains a Boolean, nonnumeric value, NaN, infinity, a value outside [0,1], or violates a row or column sum. The complete submission is rejected if it has missing or extra columns, duplicate column labels, missing or duplicate identifiers, unknown identifiers, or an incorrect identifier set. What not to use Do not infer meaning from row order or opaque IDs. Do not assume candidate index positions are stable across objects. Do not assume one globally fixed cost formula defines every target. Do not treat the candidate hypercube alone as revealing the correct latent track. Do not flatten the four detector traces into one undifferentiated time series without preserving their current/lagged and channel roles. Do not use source filenames, external source lookup, or cross-release joins. Do not submit unconstrained matrices; predictions must be doubly stochastic. Benchmark boundary This is not ordinary sequence classification, next-symbol prediction, signal reconstruction, or a standard optimal-transport problem with a known cost matrix. It is also not object detection, trajectory reconstruction, multi-object tracking, ranked assignment, or association from a supplied geometric cost matrix. There are no spatial detections, boxes, trajectories, identities, or externally meaningful candidate ranks. The supervised object is a recurrence operator between positions inside paired measured signal windows. The benchmark jointly requires latent-codeword inference from four role-preserving signal views, uncertainty over independently permuted row-local candidate hypercubes, posterior prediction under withheld heterogeneous utilities, and complete-run generalization to unseen operating durations. What makes the evaluation structurally different The following properties are jointly enforced and can be checked directly from the released files and metric: Inputs are deterministic derivatives of 2,668 empirical paired-window measurements from 21 complete physical experimental runs; the signal arrays are measured, not simulated. Organizer-side provenance includes a public persistent source record, license, immutable source checksum, transformation script, and build audit. These are intentionally kept outside participant files so the task cannot be solved by source lookup. Each window exposes a complete four-bit counterfactual hypercube with all sixteen vertices, independently permuted per object and time role. Candidate indices therefore cannot serve as reusable class labels. The target is not an observed trajectory or a fixed known-cost assignment. It is a position-to-position recurrence operator generated under an independently varying hidden utility and bounded edge preference. Because utility draws are withheld, the Bayes action under the scored loss is a soft doubly stochastic posterior mean. Exact-permutation accuracy and hard matching are not the evaluation objective. Generalization is measured across four entirely held-out physical runs and two unseen operating-duration categories, never across a random row split. A valid ablation must lose information in predictable ways: shuffling current and lagged roles destroys temporal recurrence evidence; collapsing the two detector views removes complementary shape evidence; fixing candidate indices across rows creates no stable label; and replacing the predicted matrix with the uniform matrix scores exactly zero. These tests distinguish the benchmark from ordinary tracking, ranking, and known-cost matching tasks. Resource limit Solutions must run on CPU only, using at most 10 CPU cores, 62 GB RAM, and 90 minutes. &nbsp;
> $700 Pool
> Closes in 3h 19m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Dual-Session Muscle Fatigue Demultiplexing from UWB Radar

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ct1jwe52skgq7acc22qq19x8dwn08
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ram_krish's score of 46.507!

Full challenge description from page:

> Dual-Session Muscle Fatigue Demultiplexing from UWB Radar Overview Recover two separate muscle-fatigue progressions from one batch of mixed radar recordings. Every row contains data from two different exercise participants, called session A and session B. Four labeled calibration recordings show the low- and high-fatigue endpoints for both sessions. Twelve additional recordings have lost their session labels and are shuffled together. Exactly six belong to A and six belong to B. Your prediction must first return each recording to the correct session and then arrange the six recordings within each session from least fatigued to most fatigued. This models a real data-engineering failure in non-contact physiological monitoring: independently captured radar windows can be merged after acquisition while their stream identifiers are lost or corrupted. Endpoint calibrations remain available, but the intermediate windows must be re-associated before longitudinal muscle-state analysis is possible. The source measurements come from a human biomechanics study. Eighteen consenting adults performed about twenty minutes of intermittent isometric knee extensions using trapezoidal force targets between approximately 8% and 45% of maximum voluntary contraction. A fixed ultra-wideband radar measured the vastus lateralis at 10 Hz. Each scan contains magnitude and phase for reflection (S11) and forward transmission (S21) at 51 frequencies from 0.1 to 2.9 GHz. Synchronized force and surface electromyography produced a source fatigue index. Force, EMG, fatigue values, participant identifiers, and timestamps are never public test inputs. The task is not ordinary fatigue classification or independent ranking. Each answer is a constrained decomposition of one anonymous 12-window mixture into two calibrated, ordered six-window trajectories. A strong model must solve session binding and within-session physiological progression jointly for participants absent from training. Exact objective For every test row: assign each query alias Q01 through Q12 to session A or B; assign exactly six aliases to each session; order each six-alias chain from least fatigued to most fatigued; submit both chains using the exact grammar below. Example: A>Q07>Q02>Q12>Q04>Q09>Q01|B>Q10>Q06>Q03>Q11>Q05>Q08 Dataset train.csv Contains 540 mixed-session training rows. The nine training participants appear in all 36 unordered participant pairings, with fifteen independently constructed mixtures per pairing. id — string. Unique anonymized training-row ID. radar_mixture_code_part1 — string. First 81,920 characters of the quantized radar tensor. radar_mixture_code_part2 — string. Final 81,920 characters of the quantized radar tensor. train_targets.csv Contains one target decomposition for every training ID. id — string. Training-row ID. target_demultiplexing — string. Correct A and B chains in the required grammar. Targets are stored separately so train.csv and test.csv have exactly the same feature columns. test.csv Contains 60 rows formed from eight participants who never appear in training. Before any pair rows are constructed, those eight participants are divided into two disjoint four-participant leaderboard pools. The public-leaderboard pool contributes 30 rows and the private-leaderboard pool contributes 30 rows. Within each pool, all six unordered participant pairings appear with five mixtures per pairing. No participant, participant pair, or radar window crosses between the two pools. id — string. Unique anonymized test-row ID. radar_mixture_code_part1 — string. First half of the encoded radar mixture. radar_mixture_code_part2 — string. Second half of the encoded radar mixture. sample_submission.csv Contains every test ID and a unique malformed placeholder. The placeholders contain no missing values, are not a constant column, and score exactly 0. id — string. Test-row ID. predicted_demultiplexing — string. Prediction field to replace. Private answers.csv The private answer file contains id,predicted_demultiplexing plus the platform-reserved visibility field. visibility is either public or private and tells the platform which leaderboard partition evaluates the row. It is not a prediction column, is not present in test.csv or sample_submission.csv, and is removed by the grader before scoring. The file contains no participant identifier, pair identifier, source-window key, target proxy, or other audit field. Decoding the radar mixture Each part is exactly 81,920 printable ASCII characters. Concatenate radar_mixture_code_part1 followed immediately by radar_mixture_code_part2, with no delimiter. The resulting code is exactly 163,840 characters. The split keeps every CSV field below common parser limits and has no semantic meaning. Use this alphabet in order: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_ Map every character to its zero-based alphabet position from 0 to 63, then reshape in C/row-major order to (16 windows, 80 time samples, 128 radar features). Divide by 63 for values in [0,1] if desired. The window axis is: Index 0 — session A, low-fatigue calibration. Index 1 — session A, high-fatigue calibration. Index 2 — session B, low-fatigue calibration. Index 3 — session B, high-fatigue calibration. Index 4 — mixed query Q01. Index 5 — mixed query Q02. Index 6 — mixed query Q03. Index 7 — mixed query Q04. Index 8 — mixed query Q05. Index 9 — mixed query Q06. Index 10 — mixed query Q07. Index 11 — mixed query Q08. Index 12 — mixed query Q09. Index 13 — mixed query Q10. Index 14 — mixed query Q11. Index 15 — mixed query Q12. Each window lasts eight seconds: 80 measurements at 10 Hz. The feature axis contains 32 evenly spaced frequencies from each physical block, in this order: S11 magnitude; S11 phase; S21 magnitude; S21 phase. To suppress static participant and hardware offsets, every window and each 32-frequency physical block are normalized independently. Preparation calculates the 2nd and 98th percentiles across the block's 80 × 32 values, clips to that interval, maps it to [0,63], and rounds to the nearest integer. This retains within-window temporal and spectral structure while preventing a global absolute-level fingerprint from directly encoding session ownership. Construction and leakage controls Independent leakage unit The complete source participant is the leakage unit. Seventeen response-positive participants are retained; the study's single non-responder is excluded before splitting. A participant must also have at least 200 eligible source windows to enter a leaderboard pool, because every test window is used at most once. Participant numbers are sorted by the integer value of SHA256("uwb-fatigue-test-pool-v3" + U+001F + decimal_participant_number). The eight smallest eligible hashes form the held-out participant set. The remaining nine participants form training. No participant contributes a window to both sets. The eight held-out participants are then independently ordered by SHA256("uwb-fatigue-visibility-pool-v3" + U+001F + decimal_participant_number). The first four form the public-leaderboard pool and the remaining four form the private-leaderboard pool. This assignment happens before participant pairs or radar mixtures are constructed. Consequently, all six pairs within one leaderboard pool are absent from the other pool. Prepared data contains 540 training rows and 60 test rows, of which 30 are public-leaderboard rows and 30 are private-leaderboard rows. One session trajectory For each session in a row, preparation selects eight distinct windows around a deterministic force center. The difference between the maximum and minimum median force is at most 8.0 percentage points of MVC, while the fatigue-index range is at least 10 percentage points. One window is drawn from each of eight fatigue quantile regions in the force-matched pool. The two endpoint windows become that session's labeled calibrations; the six interior windows become anonymous queries. The wider force tolerance is required to construct held-out mixtures without recycling a window and still keeps every trajectory inside a narrow force band relative to the study's approximately 8% to 45% MVC acquisition range. Two-session mixture Two different participants supply the two session trajectories. A deterministic hash swaps which participant is named A or B, so the label has no stable participant meaning. The twelve interior windows are combined and independently hash-shuffled into Q01 through Q12. Exactly six aliases belong to each trajectory, but their public positions do not reveal ownership or order. Duplicate and proxy controls All sixteen source windows within a row are distinct. Exact eight-window session bundle sets are not reused within a participant split. Exact derived radar-window tensors are audited; the catalog contains no exact duplicates. Every one of the 960 source-window occurrences in the 60-row test set is unique: no held-out window appears in two mixtures. The 240 public-leaderboard calibration windows, 360 public-leaderboard query windows, 240 private-leaderboard calibration windows, and 360 private-leaderboard query windows are mutually role-consistent. No source window appears once as a calibration and elsewhere as a query. Public- and private-leaderboard rows use disjoint participants, disjoint participant pairs, and disjoint source windows. Adjacent source windows may overlap in acquisition time within a participant, but complete participants are separated across train, public leaderboard, and private leaderboard, so such overlap cannot cross those boundaries. Participant ID, source row, time, force, EMG, fatigue, file name, and external source key are absent from public files. IDs are hashes of private mixture specifications and rows are hash-sorted. Session labels are swapped independently and query aliases are reshuffled per row. Per-window/per-block normalization suppresses trivial absolute session fingerprints. No public field states ownership, rank, participant pair, force center, source time, or split membership. Output grammar A valid prediction has exactly this structure: A>q1>q2>q3>q4>q5>q6|B>q7>q8>q9>q10>q11>q12. Rules: The literal session labels are uppercase A and B. The separator between items in a chain is >. The separator between chains is |. Allowed aliases are Q01 through Q12. Each chain contains exactly six aliases. Every alias appears exactly once across both chains. Within each chain, order is least fatigued to most fatigued. Aliases and delimiters are case-sensitive. Leading and trailing whitespace around the whole value are ignored; whitespace inside the grammar is invalid. Valid: A>Q07>Q02>Q12>Q04>Q09>Q01|B>Q10>Q06>Q03>Q11>Q05>Q08 Invalid examples: B>Q10>Q06>Q03>Q11>Q05>Q08|A>Q07>Q02>Q12>Q04>Q09>Q01 because the B chain appears before the A chain. A>Q01>Q02>Q03|B>Q04>Q05>Q06 because each chain has fewer than six aliases. A>Q01>Q02>Q03>Q04>Q05>Q06|B>Q07>Q08>Q09>Q10>Q11>Q11 because Q11 is repeated and Q12 is missing. {"A":["Q01"],"B":["Q02"]} because JSON is not part of the output grammar. Malformed row predictions receive worst-case raw component values. They do not crash the grader and cannot obtain abstention credit. Evaluation The grader returns a value in [0,100] and aligns rows by id. Let N be the number of evaluated rows. OwnershipSkill For a valid row, ownership accuracy is the fraction of twelve query aliases assigned to their correct session. Invalid rows receive 0. OwnershipAccuracy(row) = correctly_assigned_queries / 12 MeanOwnershipAccuracy = mean of OwnershipAccuracy(row) over all evaluated rows OwnershipSkill = clip((MeanOwnershipAccuracy - 0.5) / 0.5, 0, 1) The 0.5 term is the chance expectation for a balanced six/six partition. ChainOrderSkill Each true six-item chain contains 15 unordered pairs, giving 30 true within-session pairs per row. A true pair is covered only when both aliases are assigned to their correct session. A covered pair is order-correct when its relative predicted order matches its relative true order. Across all evaluated rows, let: CoveredPairs be the number of covered true pairs; CorrectCoveredPairs be the number of covered pairs in correct order. PairCoverage = CoveredPairs / (30 × N) If CoveredPairs = 0, then ConditionalPairAccuracy = 0. Otherwise, ConditionalPairAccuracy = CorrectCoveredPairs / CoveredPairs. ConditionalPairSkill = clip((ConditionalPairAccuracy - 0.5) / 0.5, 0, 1) ChainOrderSkill = PairCoverage × ConditionalPairSkill This construction prevents free ordering credit. Correctly recovering ownership but randomly arranging each chain has expected ConditionalPairAccuracy = 0.5 and therefore zero ChainOrderSkill. Assigning only easy items cannot help because missing or wrongly assigned pairs reduce PairCoverage. EndpointSkill There are four true endpoints per row: least- and most-fatigued queries for both sessions. A true endpoint is covered when its alias is assigned to the correct session. It is correct when it also occupies the correct end of that predicted chain. Let CoveredEndpoints and CorrectCoveredEndpoints be totals across all rows. EndpointCoverage = CoveredEndpoints / (4 × N) If CoveredEndpoints = 0, then ConditionalEndpointAccuracy = 0. Otherwise, ConditionalEndpointAccuracy = CorrectCoveredEndpoints / CoveredEndpoints. ConditionalEndpointSkill = clip((ConditionalEndpointAccuracy - 1/6) / (5/6), 0, 1) EndpointSkill = EndpointCoverage × ConditionalEndpointSkill The 1/6 term is the chance probability of placing a covered alias at the correct end of a six-item chain. ExactRate Exact(row) = 1 if both parsed chains exactly match the target; otherwise Exact(row) = 0. ExactRate = mean of Exact(row) over all evaluated rows Final score final_score = 100 × (0.15 × OwnershipSkill + 0.75 × ChainOrderSkill + 0.08 × EndpointSkill + 0.02 × ExactRate) clip(x,0,1) = min(1,max(0,x)). All constants and operations are public. No hidden reference model, normalization constant, family weight, or secret baseline is used. The sample scores exactly 0; the oracle scores exactly 100. Submission format Submit submission.csv with exactly two columns in this order: id: string from test.csv; predicted_demultiplexing: string following the dual-chain grammar. Example header: id,predicted_demultiplexing Example row: 06a2fd6fc2b6b9e09c3a,A>Q07>Q02>Q12>Q04>Q09>Q01|B>Q10>Q06>Q03>Q11>Q05>Q08 Each test ID must appear once. Missing rows, duplicate IDs, unknown IDs, extra IDs, wrong row count, extra columns, missing columns, or wrong column order raise ValueError. Submission row order has no effect. Modeling directions The 540 training rows contain 8,640 eight-second radar windows and approximately 88 million quantized measurements. Suitable approaches include: shared temporal or spectro-temporal window encoders; calibration-conditioned metric learning; balanced assignment using learned session affinities; pairwise or listwise losses within each inferred session; joint bipartite assignment and differentiable sorting; cross-participant regularization and model ensembles. A single NVIDIA A10G is appropriate for batching all sixteen windows through a shared encoder and optimizing assignment plus ordering losses. Prohibited shortcuts Do not use IDs, row order, alias position, source filenames, participant identifiers, timestamps, source coordinates, or external-record lookup as target proxies. Do not submit probabilities, continuous fatigue values, force estimates, JSON, or explanations. Only the two-chain value is graded. Benchmark boundary Published work on this sensing source estimates continuous muscle force. Other radar-fatigue work predicts classes, fatigue values, or repetition reserve from one subject stream. Source-separation benchmarks usually separate waveforms or speakers. This task instead binds anonymous radar windows to two row-calibrated human sessions and reconstructs two ordered physiological trajectories under a strict balanced-partition constraint. Its prediction object, participant-pair construction, normalization, and chance-corrected coverage metric are not the contract of force regression, fatigue classification, standard source separation, or independent list ranking.
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Scene-Text Paragraph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ddkzqwkstg60dmm94642qkh8dwm4t
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Scene-Text Paragraph Recovery
> Overview Given an unordered set of word transcriptions and polygons, infer how many paragraphs are present and assign every word to one of them. Photographs, line assignments and paragraph boundaries are unavailable; the supplied text and geometry are the evidence for each decision. Nearby words can belong to separate signs or columns, while one paragraph can extend across several lines. The challenge is to turn these local spatial and linguistic cues into a consistent partition of the entire scene. Dataset train.csv / test.csv: task_id, words_json; 7,850 training scenes and 1,285 test scenes. Each word has word_id, text and an ordered polygon vertices list. Vertex count can vary. train_labels.csv and sample_submission.csv: task_id,target_json. Email-, website- and credential-like tokens, and tokens containing seven or more digits, are replaced with [redacted]. These words retain their polygons and IDs and must still be assigned to paragraphs. This rule-based masking does not identify every personal name, address or contact detail split across words. Coordinates are normalized independently by the scene's maximum annotated x and y coordinates. These are tight annotation coordinates, not image dimensions; photographs are not supplied. Native training and validation scenes form training data; native test scenes remain held out. Scenes contain 20–400 legible words, at least three paragraphs and at least two multi-line paragraphs. Duplicate geometry/text scenes and coincident duplicate words are excluded. Line/paragraph identifiers and native ordering are withheld. Ambiguous layout and transcription errors remain possible. Task Return a complete, non-overlapping partition of the supplied word IDs. Infer paragraph membership and the number of groups jointly; no paragraph count is supplied. Every word, including a masked token, must appear exactly once. Singleton paragraphs are valid. Membership must be consistent: if two words belong with a third, all three must occur in the same group. Submit the groups themselves, not independent word-pair decisions. Neither reading order nor the order of groups or words within them is scored. Submission task_id,target_json example_1,"[[""w_a"",""w_b""],[""w_c""]]" example_2,"[[""w_d"",""w_e""]]" Columns must be exactly task_id,target_json, in that order. Include every test ID once. Missing, repeated or unknown word IDs, empty groups and malformed JSON give the scene zero. Evaluation Mean per-scene pairwise F1. A positive pair consists of two distinct words placed in the same paragraph. Compare predicted positive pairs with reference positive pairs using 2 × matching_pairs / (predicted_pairs + reference_pairs), then average across scenes. This evaluates paragraph cohesion and separation without depending on arbitrary cluster names. Score 1 is perfect. File-level schema and task-ID errors are rejected. Expected Methods Learn word compatibility from text and relative geometry, then resolve those decisions into paragraph groups using clustering, graph models or direct set prediction. Generic public pretrained models are allowed. What Not To Use No source matching, original annotation lookup, external labeled layouts, source-specific fine-tunes, manual test labeling or hosted APIs. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## PAMAP2 Body-Key Privacy Amplifier

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71dm1bhacr1vp9j2ec8ajfzx8dxsn6
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat datadrift's score of 0.365!

Full challenge description from page:

> PAMAP2 Body-Key Privacy Amplifier Overview Wearable devices on one body observe the same underlying movement through very different local signals. A hand sensor swings freely, a chest sensor follows the torso, and an ankle sensor experiences foot impacts. A useful body-key feature should nevertheless produce the same bit at all legitimate devices and remain uninformative to another motion window—even when that window contains the same activity. This is a multimodal feature-engineering challenge, not activity classification, time-series forecasting, waveform generation, sensor scheduling, user identification, or cryptographic key recovery. For every case, you receive calibration margins for 512 published binary motion primitives observed independently at the hand, chest, and ankle. You must synthesize one sparse, full-rank 16 × 512 matrix over GF(2). The private grader executes that matrix as a feature transform on hidden legitimate and impostor views. There is no organizer-authored target matrix and no predicted class. The benchmark models the reliability–privacy trade-off in shared feature extraction. An output bit is useful only when six legitimate channel views agree exactly. Among those reliable bits, it receives privacy credit only when twelve hard same-activity impostor views cannot predict whether the bit matches. This is a benchmark surrogate for learning robust cross-body feature transforms; it is not a claim that the resulting 16 bits form a production cryptosystem. Input Prompt Each case supplies a 3 × 512 array named calibration_margin. Site order is: hand, chest, ankle For site s and primitive p: calibration_bits,p] = 1 if calibration_margin[s,p] >= 0 else 0 The magnitude is distance from the primitive's fitted site-specific threshold. Large absolute values are usually more stable under the hidden channel transforms, but stability also depends on the primitive, motion context, and interactions introduced by XOR rows. Equal primitive indices at different sites arise from a training-only shared latent feature construction; raw hand, chest, and ankle waveforms are never asserted to be equal. Prepared Feature Construction The deterministic prepare script turns each 2.56-second PAMAP2 window into a bank of cross-site binary primitives: Keep three-axis acceleration and gyroscope data at hand, chest, and ankle: 18 channels total. Robustly normalize channels using medians and interquartile ranges fitted only on training participants. For each site, form rotation-invariant acceleration and gyroscope magnitudes. Compute 40 non-DC cosine coefficients plus four level/dynamics summaries for each magnitude signal, giving 88 descriptors per site. Fit a regularized, sign-canonicalized 32-dimensional shared cross-site latent basis on training participants only. Apply 512 fixed sparse projections and five deterministic training quantiles to obtain site-specific margins and bits. feature_bank.npz publishes every fitted array required to reproduce this transformation. The feature bank is fixed for the challenge and is not learned by the private grader. Hidden Channel Protocol The private evaluator holds two nuisance replicates of the query motion. Each replicate produces one bit vector at each of the three sites, giving six legitimate vectors of length 512 in this exact order: replicate_0_hand, replicate_0_chest, replicate_0_ankle, replicate_1_hand, replicate_1_chest, replicate_1_ankle It also holds four independently selected same-activity motion windows. Each impostor contributes hand, chest, and ankle vectors, giving twelve impostor vectors. The candidates are chosen privately from the same participant partition by descriptor proximity, then independently perturbed. Activity, participant, source time, and impostor identities are not released. The nuisance channel applies bounded axis rotations, sensor-specific gain and offset, mild nonlinear resampling, one- or two-step displacement, and low-amplitude noise. Training cases expose their hidden outputs so solvers can learn which calibration patterns generalize. Test cases expose calibration margins only. Amplifier Matrix amplifier_matrix is a JSON list of exactly 16 hexadecimal strings. Each string encodes one 512-bit row: exactly 128 hexadecimal characters; most-significant bit first within every byte; decoded with bytes.fromhex, then numpy.unpackbits(..., bitorder="big"); Hamming weight from 1 through 5; all 16 rows together must have rank 16 over GF(2). The sparsity budget prevents an unbounded dense parity search and models a small-device XOR budget. Full row rank prevents submitting the same feature repeatedly. These are structural validity requirements, not hidden score terms. For a primitive vector b and submitted matrix H, the 16-bit output is: k = (b @ H.T) mod 2 Every submitted row is executed. No key bits, confidence value, decoded waveform, certificate, checksum, or derived target is submitted separately. Evaluation For output bit j, let L[v,j] be its value on legitimate view v, and let I[e,j] be its value on impostor view e. The first legitimate view is used only as a reference orientation: reference_j = L[0,j] agreement_j = 1 if L[0,j] = L[1,j] = ... = L[5,j], else 0 impostor_match_rate_j = mean(I[e,j] = reference_j for e = 0,...,11) privacy_j = 1 - abs(2 * impostor_match_rate_j - 1) bit_score_j = agreement_j * privacy_j row_score = mean(bit_score_0, ..., bit_score_15) final_score = mean(row_score over all test cases) The score is maximized and lies in [0,1]. privacy_j is 1 when exactly half of the impostor outputs match and 0 when all match or all disagree. A fully complemented impostor bit is as predictable as a fully matching bit, so the symmetry around one half is necessary. Privacy is counted only for a bit that all legitimate views reproduce. The 16 output positions and all cases receive equal weight. The equation above is the complete numeric metric. It contains no baseline subtraction, leaderboard floor, calibrated constant, hidden component weight, activity score, or GPU multiplier. Every structurally valid matrix receives the formula; structural rejection is never mixed into the numeric score. Public Files train_protocols.npz | Array | Shape | Type | Description | |---|---:|---|---| | case_id | (6000,) | Unicode | Opaque training case identifier | | group_id | (6000,) | Unicode | Two calibration views of one physical source window share a group | | calibration_margin | (6000,3,512) | float16 | Public site/primitive margins | | legitimate_bits_packed | (6000,6,64) | uint8 | Six training legitimate vectors, packed MSB-first | | impostor_bits_packed | (6000,12,64) | uint8 | Twelve training impostor vectors, packed MSB-first | Unpack the last axis with: bits = np.unpackbits(packed, axis=-1, bitorder="big") Training contains no target matrix. It exposes outcomes so any valid matrix can be executed and scored offline. test_calibration.npz | Array | Shape | Type | Description | |---|---:|---|---| | case_id | (1500,) | Unicode | Opaque evaluation identifier | | calibration_margin | (1500,3,512) | float16 | Only the three-site calibration margins | Test legitimate and impostor vectors remain private. feature_bank.npz | Array | Shape | Type | Description | |---|---:|---|---| | dct_basis | (128,40) | float32 | Published non-DC cosine basis | | descriptor_mean | (3,88) | float32 | Training-only site descriptor centers | | descriptor_scale | (3,88) | float32 | Training-only site descriptor scales | | site_projection | (3,88,32) | float32 | Shared latent site projections | | latent_mean | (3,32) | float32 | Latent centers | | latent_scale | (3,32) | float32 | Latent scales | | primitive_weight | (512,32) | float32 | Sparse primitive projections | | primitive_threshold | (3,512) | float32 | Site-specific training thresholds | | primitive_quantile | (512,) | float32 | Quantile used for each primitive | Other public files: protocol_config.json — exact matrix, packing, view-order, execution, and metric contract. metadata.json — source, split, privacy, feature, and runtime metadata. preparation_report.json — deterministic file and row inventory. sample_submission.csv — complete valid one-hot matrices showing exact CSV/JSON formatting. Submission Write ./working/submission.csv with exactly these columns in exactly this order: | Column | Type | Description | |---|---|---| | case_id | string | Identifier copied from test_calibration.npz | | amplifier_matrix | JSON string | Sixteen 128-character hexadecimal matrix rows | The full sample file is authoritative. A shortened illustration is: case_id,amplifier_matrix bka_example,"[""8000...0000"",""4000...0000"",...14 further rows...]" The ellipses are explanatory only and are not valid submission content. Submission requirements: Include exactly 1,500 rows, one for every test case_id, in any row order. Do not duplicate, omit, or invent identifiers. Preserve the exact two-column schema. JSON must contain exactly 16 strings and no other values. Each string must contain exactly 128 hexadecimal characters. Each decoded row must contain from one through five set bits. The complete matrix must have rank 16 over GF(2). Additional columns, missing JSON, null, numbers, booleans, nested objects, short/long rows, non-hex characters, zero/dense rows, and rank-deficient matrices are invalid. Critical schema, identifier, encoding, sparsity, or rank failures reject the submission cleanly. Lowercase hexadecimal is accepted and has the same meaning as uppercase. Split and Anti-Shortcut Design Participants 101–107 supply training cases; participants 108–109 supply evaluation cases. No participant crosses the boundary. Both training calibration views of one physical window share group_id and must remain in the same validation fold. Case IDs and public row order are independent hashes. Source activity is used only to balance source windows and select difficult same-activity impostors; it is not released or scored. Participant, recording, source offset, activity, private nuisance seeds, impostor identities, and test outcome histograms are absent from public files. A global matrix and a per-case margin ranking are useful baselines. They do not learn context-dependent cross-site stability or parity interactions. A competitive solver must estimate how a proposed sparse XOR row will behave across hidden legitimate channels and hard impostors, then assemble 16 linearly independent rows. Relation to Prior Work Gait-Key and related systems generate shared keys from accelerometers on different body locations. Accelerometer/fuzzy-vault group-key work develops fixed feature extraction, reconciliation, and distribution protocols. Biometric fuzzy extractors formalize reliable extraction from noisy measurements. This benchmark does not claim those fields are new. Its evaluated learning object is different: a model synthesizes a case-conditioned sparse full-rank privacy-amplification matrix, with no target matrix, and the leaderboard executes it on hidden multi-site replicates and matched same-activity impostors. Located prior systems evaluate a designed protocol; they do not define a supervised/offline competition where each test context requires a new executable GF(2) transform and receives functional reliability–privacy credit. Primary references: Xu et al., “Gait-Key: A Gait-Based Shared Secret Key Generation Protocol for Wearable Devices,” ACM TOSN: [https://doi.org/10.1145/3023954 Sun et al., “Accelerometer-Based Key Generation and Distribution Method for Wearable IoT Devices,” IEEE IoT Journal: https://doi.org/10.1109/JIOT.2020.3014646 Dodis et al., “Fuzzy Extractors: How to Generate Strong Keys from Biometrics and Other Noisy Data”: https://doi.org/10.1137/S0097539704446627 Reiss, PAMAP2 Physical Activity Monitoring, UCI: https://doi.org/10.24432/C5NW2H Single-A10G Runtime Contract Evaluation has two stages. First, the configured solution job must verify CUDA, exactly one visible GPU, and an NVIDIA A10G device name. Learned matrix synthesis, differentiable parity modeling, training, and all test inference must run on that GPU. A missing or mismatched device, multiple visible GPUs, or CPU prediction fallback terminates the job without a submission; grade.py is not invoked and no leaderboard score is issued. Second, an eligible CSV receives only the numeric formula above. Hardware is not a score component, multiplier, penalty, or threshold. The grader cannot infer runtime provenance from matrix text, so the platform execution record enforces eligibility before numeric grading. The intended approach is a three-site set encoder followed by a structured sparse-row decoder. Training exposes more than three million primitive contexts and supports differentiable parity surrogates, straight-through sparse selection, contrastive reliability/privacy objectives, or search-guided imitation. A full policy emits 1,500 × 16 × 512 row logits before sparse decoding; mixed precision and batched outcome simulation make a single A10G materially useful. CPU is limited to bounded NPZ/CSV I/O, bit packing, grouped split bookkeeping, diagnostics, and final serialization. CPU-only primitive ranking, CPU matrix search, or CPU inference is not an eligible primary solution. The creator's CPU attacks are diagnostics, not eligible reference solutions. Data-Use Rules Allowed: Use every file under ./dataset/public/. Train from scratch on the exposed training protocols and execute arbitrary valid matrices offline. Use grouped validation that keeps equal group_id values together. Use GPU-based discrete optimization, differentiable relaxations, contrastive learning, or ensembles within one A10G. Reproduce the public feature transform from feature_bank.npz for analysis. Not allowed: Access private legitimate/impostor bits, answer payloads, nuisance seeds, source offsets, participant IDs, activity IDs, or preparation state. Retrieve or match original PAMAP2 evaluation windows outside the challenge files. Use case_id, row order, archive order, hashes, storage bytes, or serialization details as predictive features. Hard-code test matrices, manually inspect private results, call external inference APIs, use external datasets, or use more than one GPU. Submit a CPU-only primary synthesizer or silently fall back to CPU prediction. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## EchoBudget: Counterfactual Probe Selection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bbkmg2ac37y18tcvw4y3rcx8dthfg
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat haidang's score of 0.686!

Full challenge description from page:

> EchoBudget: Counterfactual Probe Selection Overview A monitoring system cannot always acquire every missing measurement. Each EchoBudget case starts with one partially observed physical state and six possible follow-up probes. A probe reveals either a waveform interval or a region of a period–velocity image, but its outcome is unavailable when the decision is made. Every action has a case-specific footprint, acquisition cost, and noise level. The task is to predict a calibrated utility distribution over the six probes. The target is not an event class, a source identity, a reconstructed signal, or a cross-modal match. It represents which unobserved measurement would best resolve the difficult alternatives that remain consistent with the released context. The challenge tests whether a model can estimate the value of unseen evidence from incomplete multimodal observations. A useful policy must identify what remains ambiguous, compare that ambiguity with each candidate footprint, account for measurement reliability, and determine whether the expected discrimination is worth its cost. What Makes This Challenge Different The closest same-domain public work is Callahan et al., Analysis and Optimization of Seismic Monitoring Networks with Bayesian Optimal Experimental Design (Geophysical Journal International, 2025). That work chooses locations, sensor types, and fidelity for a monitoring network before a particular observation arrives, maximizing expected information gain about hypothetical events under an ensemble prior. EchoBudget operates at a different decision level: after seeing one incomplete case, a solver must value six case-specific candidate probes whose locations, modalities, costs, and noise levels are different in every row. A second neighboring family is sequential adaptive acquisition for inverse problems, including Silvestri et al. (2024). Those methods repeatedly acquire low-dimensional measurements to improve reconstruction of an underlying signal and jointly learn the reconstruction policy. EchoBudget is neither sequential acquisition nor reconstruction-quality optimization. No action is executed during scoring, no acquired outcome is returned to the model, and no hidden signal reconstruction is submitted. The supervised object is the complete utility distribution of a fixed one-step action set. A useful abstract view of one EchoBudget case is: context = retain_fine_measurements(state, visible_mask) low_resolution_scout(state, hidden_regions) given: one incomplete multimodal state six high-dimensional probe masks, costs, and noise levels recover: the six-action robust utility distribution not: a sensor-network design, an acquisition sequence, a reconstructed field, or a source label The six actions are not interchangeable scalar features. Three are temporal masks over a 1,536-sample waveform, while three are spatial masks over a 128 × 49 physical image. Their target values are computed jointly against the same eight-world counterfactual cohort. Consequently, the correct action depends on which fine-scale disagreements survive the released scout context, not on a globally useful sensor position. Five design choices form the benchmark's distinguishing contract: Case-conditioned rather than network-level design: the decision is made after observing the individual incomplete state. Cross-representation action geometry: one policy directly compares temporal waveform masks with two-dimensional dispersion masks. Counterfactual rather than posterior-average utility: every action is evaluated over a deliberately matched eight-world cohort. Robust rather than expected discrimination: utility uses the twentieth percentile of pairwise separation, then adjusts for action cost and noise. Distributional rather than selected-action evaluation: the grader measures calibration against all six relative utilities with a chance-referenced squared-error score. The fragmented evaluation probes also use a region topology absent from training. This tests transfer of the action-valuation rule itself, rather than only interpolation among familiar mask shapes. The resulting input-output contract is: | Task type | Typical output | EchoBudget output | | --- | --- | --- | | Bayesian seismic network OED | one network configuration maximizing prior-averaged expected information gain | one six-probe policy for each already-observed case | | Sequential adaptive acquisition | a measurement sequence that improves a reconstructed signal | one-shot utility estimates without executing a probe or reconstructing a target | | Cross-modal retrieval | identity or similarity between observed items | prospective value of unobserved regions from two different representations | | Physical inversion | a field, source, or model parameter estimate | calibrated lower-tail separation of an unresolved counterfactual set | The central research question is whether a model can predict a cost-aware, lower-tail counterfactual certificate for an unrevealed measurement from one incomplete multimodal state. Solving network placement, sequential reconstruction, source localization, or pair retrieval does not directly produce that six-action certificate. Construction Boundary The physical starting material is a compact bank of 21,330 aligned station-pair observations containing measured waveform and dispersion representations. EchoBudget reuses those physical signal values and their shared coordinate axes. It does not claim that the underlying observations were newly acquired. License, revision, checksums, and complete source attribution are recorded in the accompanying dataset description and platform Source field. Everything that defines the participant task is constructed after source selection: | Benchmark stage | Reused physical information | Newly designed for EchoBudget | | --- | --- | --- | | Source representation | aligned waveform and dispersion observations | validated compact tensors and creator-side dependency graph | | Ambiguity construction | processed physical similarity evidence | eight-world cohorts with unique pairs and endpoint stations | | Observation process | waveform and image values | visible masks, low-resolution scouts, and held-out probe topology | | Candidate actions | no pre-existing action labels | six masks with modality, cost, noise, and randomized order | | Prediction target | no pre-existing supervised target | robust lower-tail utility distribution at temperature 0.22 | | Evaluation protocol | no pre-existing score | chance-referenced squared-error skill with stable row normalization | Every case uses eight different source pairs with 16 distinct station endpoints. Three actions query disjoint 256-sample waveform regions, and three query disjoint 512-pixel regions of a 128 × 49 dispersion panel. Full-resolution content inside the union of candidate regions is replaced in the released context by deterministic low-resolution scout measurements. For action a, preparation calculates pairwise mean squared distances among the eight fine-resolution residuals inside the proposed region. Let D_a be the twentieth percentile of those distances. After normalization by the median inside the action's modality: raw_value_a = normalized_D_a / (cost_a × (0.08 + noise_a)²) The six raw values are mapped linearly to the interval from zero to one and converted into the training target with softmax temperature 0.22. Source selection, cohort construction, masks, targets, shuffling, split assignment, and serialization are deterministic. Task For every id in test.csv, predict six finite, nonnegative values. Columns probe_0 through probe_5 correspond to the six candidate actions in their released order. The grader converts every valid prediction row to unit mass. For numerical stability, it first divides the row by its largest entry and then divides by the resulting row sum. This prevents overflow and makes the score invariant to finite positive rescaling. Larger normalized values place more acquisition probability on the corresponding probe. Training rows expose the six oracle utility values. Test utilities, unrevealed probe outcomes, ambiguity-cohort members, station identities, source mappings, and visibility assignments remain private. Prediction Rules Submit exactly one row for every test id. Include id followed by probe_0 through probe_5 in the published order. Every prediction value must be finite and nonnegative. Every row must contain strictly positive total mass. Do not add, remove, rename, or reorder columns. Predictions do not need to arrive normalized because normalization is part of grading. Why the Task Is Difficult Each visible context is compatible with eight related physical worlds. Candidate actions expose different regions and modalities, and their value changes with the residual ambiguity of the individual case. Two cases with identical probe geometry may therefore have different targets. Waveform and image actions have different geometry, feature statistics, cost, and noise. A strong model must interpret the released state, condition its representation on each proposed region, and compare all six candidates jointly. Independent action scoring is possible, but it cannot directly model competition for probability mass. Simple global rules do not solve the task. The cheapest-action, lowest-noise, fixed-index, first-waveform, and first-image policies all score below 0.008, while a uniform six-action policy scores 0.02. Candidate order is randomized, every action index is balanced as the best action, and training rows are shuffled before local array indices are assigned. The useful signal is a learned relationship among context, candidate footprint, modality, cost, and noise. Action-conditioned one-dimensional and two-dimensional encoders, multimodal attention, uncertainty models, and set-based policy networks are natural model families. Data Files The participant release contains: train.csv: 1,200 labeled rows; test.csv: 240 held-out rows; train_context_waveforms.npy: float16 tensor with shape [1200, 1536]; test_context_waveforms.npy: float16 tensor with shape [240, 1536]; train_context_images.npy: float16 tensor with shape [1200, 128, 49]; test_context_images.npy: float16 tensor with shape [240, 128, 49]; train and test visible masks for both modalities; train and test candidate-probe masks for both modalities; train_probe_metadata.npy and test_probe_metadata.npy; waveform_time.npy, periods.npy, and velocity_axis.npy; and sample_submission.csv: a complete structurally valid submission template. Preparation and modeling require no network access. CSV Schema train.csv id: unique opaque case identifier. array_index: zero-based row index in every train_*.npy case tensor. probe_0 through probe_5: normalized target utility distribution. Training array_index values run from 0 through 1,199. test.csv id: unique opaque case identifier. array_index: globally unique row reference from 1,200 through 1,439. For a test row, subtract 1,200 from array_index to address the first axis of every test_*.npy case tensor. Global indexing keeps train and test feature rows disjoint. sample_submission.csv The template contains exactly seven columns: id followed by probe_0 through probe_5. The private answer key uses exactly the same schema and column order. Id text, CSV row order, and array indices carry no target, dependency, or visibility information. Input Channels For a split containing N cases: context_waveforms.npy: float16, shape [N, 1536]; context_images.npy: float16, shape [N, 128, 49]; waveform_visible_masks.npy: uint8, shape [N, 1536]; image_visible_masks.npy: uint8, shape [N, 128, 49]; probe_waveform_masks.npy: uint8, shape [N, 6, 1536]; probe_image_masks.npy: uint8, shape [N, 6, 128, 49]; and probe_metadata.npy: float32, shape [N, 6, 3]. The three metadata channels are: channel 0: modality, where 0 denotes waveform and 1 denotes image; channel 1: normalized acquisition cost; and channel 2: noise scale. An image action has an all-zero waveform mask, and a waveform action has an all-zero image mask. Candidate regions do not overlap within a modality. Visible masks use 1 for released fine-resolution context and 0 for regions replaced by low-resolution scout measurements. Convert float16 inputs to float32 before model computation. The shared coordinate arrays are: waveform_time.npy: float32, shape [1536], with 0.2-second spacing; periods.npy: float32, shape [49], covering periods 2 through 50; and velocity_axis.npy: float32, shape [128], spanning 2.5 through 4.3 km/s. Evaluation The grader validates the complete submission contract and normalizes every prediction row. Let P[i,a] be the normalized submitted probability for action a in scored case i, and let Q[i,a] be the private normalized utility target. ModelSSE = sum_i sum_a (P[i,a] - Q[i,a])² UniformSSE = sum_i sum_a (1/6 - Q[i,a])² NormalizedError = ModelSSE / UniformSSE The exact score is: if NormalizedError <= 1: Score = 0.02 + 0.98 × (1 - NormalizedError) else: Score = 0.001 + 0.019 / NormalizedError The score is clipped to [0.001, 1.0], and higher is better. Reproducing the complete target distribution scores 1.0. A uniform six-action policy scores exactly 0.02. Predictions worse than uniform remain distinguishable below 0.02 and approach 0.001 as error increases. UniformSSE is recomputed from the exact answer subset being scored. Public and private therefore use the same formula and their own cases without treating correct predictions from the other visibility as errors. Wrong or reordered columns, missing or unknown ids, duplicate ids, nonnumeric cells, NaN, infinity, negative values, or zero-mass rows raise actionable validation errors instead of being converted into a model score. Split and Leaderboard Design The independent unit is one complete case. Its context, six actions, eight creator-side worlds, derived utility distribution, and all dependency information remain together under one visibility value. Stations are partitioned before ambiguity cohorts, masks, costs, noise, or targets are generated. The 1,200 training cases use 9,600 unique source pairs from a 246-station graph. The 240 evaluation cases use 1,920 different source pairs from held-out station graphs. No station, source pair, opaque id, or exact context tensor crosses the train/evaluation boundary. The release contains: training: 1,200 complete cases; public test: 60 complete cases; and private test: 180 complete cases. Public evaluation contains exactly 25 percent of held-out cases. Each action index is optimal 200 times in training, 10 times in public test, and 30 times in private test. Training uses contiguous-block and paired-region mask families, while both evaluation subsets use only the held-out fragmented family. Public and private visibility is assigned at complete-case level and was selected using organizer-side reference policies to preserve ranking stability. The perfect distribution scores 1.0 on both sides. Across three representative solver tiers, public/private score drift is at most 0.00485 and the ranking is identical. Twenty equal-quality private perturbations have score standard deviation 0.00415 and range 0.01299. Successive representative solver gaps are 4.16 and 11.67 times that standard deviation. Computational Expectations GPU training has a material advantage. Every example combines a 1,536-sample waveform, a 128 × 49 physical image, context masks, and six candidate masks. Suitable models repeatedly apply one-dimensional and two-dimensional convolutions or attention while comparing all six actions. The compact neural reference processes 14,400 case-epochs in one run. Architecture, seed, and hyperparameter searches naturally expand this into hundreds of thousands of multimodal case-epochs. CPU preprocessing and classical baselines are permitted, but the intended high-capacity action-conditioned models train more efficiently on an accelerator. Submission Use sample_submission.csv as the template. Submit one CSV row per test id with exactly seven columns: id followed by probe_0 through probe_5 in the published order. Row order may change because the grader joins by id. Column order may not change. What Not To Use Do not use hidden answers, visibility assignments, creator dependency maps, station identities, source mappings, counterfactual outcomes, or unreleased metadata. Do not infer targets from id text, row order, or array_index; these fields are opaque and audited. Do not manually coordinate decisions for held-out examples or access evaluator-only files. Classical signal processing, physical reasoning, CPU models, and legitimate external modeling libraries remain valid approaches. These rules prohibit unreleased information, not valid experimental-design methods. Expected Output The expected artifact is one valid submission.csv containing a six-action utility distribution for every test case. The leaderboard maximizes the normalized squared-error skill score defined above. &nbsp;
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Selective Activation Explanation Binding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78xxq3f4y1ccry1a0dbn1nd98dtszm
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat lelouch's score of 0.601!

Full challenge description from page:

> Overview Predict which of five written explanations belongs to each of three language-model hidden states. Return one three-entry binding vector, using zero when the matching explanation is absent. A hidden state is a numerical representation produced while a language model reads text. Explanations can describe the same broad topic yet refer to different sentence endings: expecting a date is different from expecting the next item in a list. This task tests whether a learned model can connect those local distinctions to the internal representation rather than simply recognize the document's subject. The states were measured at layer index 18 of a frozen 1.7-billion-parameter transformer reading English web text. An annotation model described the corresponding prefixes, including their final-token constraints. Each case uses three positions within one document. All five candidate explanations come from distinct positions in that document, except that in about half the cases one positive explanation is omitted and replaced with a textually similar explanation from another document. The benchmark evaluates source-paired annotation binding, not whether an explanation is a proven causal account of the network. Dataset Files Paths are relative to the supplied public directory. | File | Contents | |---|---| | train.csv | 2,341 labeled cases. Columns, in order: case_id, state_path, explanation_candidates, explanation_binding. | | test.csv | 440 unlabeled cases. Columns, in order: case_id, state_path, explanation_candidates. | | sample_submission.csv | One varied training-label baseline for each test ID, with the required two-column submission schema. These are example predictions, not inferred answers. | | states/ | 2,781 NumPy .npy files, one per case. Each contains a (3, 2048) float16 array; row order is query order. | The evaluator reads case_id and explanation_binding from its private answer table. The platform may append private grading metadata; those additional columns are ignored and must not be included in participant submissions. Columns and Arrays | Column | Data type | Meaning | |---|---|---| | case_id | String | Opaque identifier such as bind_486fb839d6f6919c9a7d66ba. It has no predictive meaning. | | state_path | String | Relative path such as states/bind_486fb839d6f6919c9a7d66ba.npy. Load with NumPy and allow_pickle=False. | | explanation_candidates | JSON-encoded string containing five strings | The five explanations in candidate order. Candidate numbers are one-based: 1 through 5. Text can include line breaks, quotation marks, and non-ASCII characters. | | explanation_binding | JSON-encoded string containing three integers | Entry j selects the explanation for state-array row j, with zero meaning its paired explanation was not offered. | Each state is L2-normalized independently and stored as float16. All cases use the same 2,048-coordinate representation basis; there is no per-case rotation. Rounding can make the stored norm slightly different from one. The original text prefixes and position indices are not model inputs. The explanations themselves are intended linguistic evidence. Binding Rules A binding such as [2,0,4] means: state row 0 pairs with candidate 2; state row 1 has no offered match; state row 2 pairs with candidate 4. A positive candidate number cannot be reused. Zero can be repeated in a prediction, although reference cases contain either no missing match or one missing match. The annotation attached to a sampled state is its positive match. A nearby-position annotation remains a distractor even when it concerns the same topic. This is annotation attribution, not open-ended paraphrase grading. Generated annotation noise is a limitation of the task; explanations are not human-certified semantic equivalence classes. Construction and Separation Preparation requires five distinct annotated positions separated by at least 20 tokens. It excludes explanation pairs whose normalized word-set Jaccard similarity exceeds 0.80 and vector pairs whose cosine similarity is at least 0.995. Three positions become query rows; two other positions provide same-document distractors. Thus topic matching alone cannot distinguish the correct position from the other candidate positions. When a positive is omitted, its replacement is selected from the 32 nearest document summaries by TF-IDF cosine similarity, excluding the original document group. Among those documents' eligible annotations, preparation chooses the largest normalized word-set Jaccard similarity to the omitted annotation, subject to a maximum of 0.80. Stable source/text ordering breaks ties. Every replacement comes from the same split. Candidate and query order are shuffled; the replaced query index is chosen without inspecting the annotation content. The task preserves the original measured vectors and explanation text, rather than deleting informative coordinates or adding artificial noise to force lower scores. Source documents, shared prefixes, identical annotations, and identical vectors are grouped before splitting. Highly similar document prefixes are joined using a fixed text-similarity threshold. Training and test cases use disjoint document groups, including every distractor source. This evaluates transfer to unseen documents within the same model and layer, not transfer to an unseen model or an entirely new subject domain. Hashing identifiers does not itself create independence. | Number of omitted matches | Training cases | Test cases | |---|---|---| | 0 | 1,154 | 201 | | 1 | 1,187 | 239 | | Total | 2,341 | 440 | Example One training case is bind_7cbd0c0bdcedecef5696c32b, with state path states/bind_7cbd0c0bdcedecef5696c32b.npy and binding [3,0,4]. State row 0 matches candidate 3, row 1 has no offered match, and row 2 matches candidate 4. The complete five explanation strings are available in that training row. Candidate 1 discusses a sentence ending in “standalone” and the expectation of a following noun; its shared technical subject alone does not make it a positive match. Submission Format Write the final CSV to ./working/submission.csv. It must have exactly these columns, in this order: case_id, explanation_binding. | Column | Required format | |---|---| | case_id | String copied exactly from a test row. | | explanation_binding | JSON string encoding exactly three integers from 0 through 5, at most 32 characters. Positive numbers must be unique. Booleans, floating-point values, quoted numbers, and nested arrays are invalid. | Example of a correctly serialized CSV row: bind_7cbd0c0bdcedecef5696c32b,"[3,0,4]". This illustrates a training ID; actual submissions must use every test ID exactly once. The grader rejects extra, missing, reordered, or duplicate participant columns; duplicate, unknown, missing, or malformed IDs; incorrect row counts; and empty evaluations. Participant columns must be exactly case_id,explanation_binding in that order, even when private answers contain additional metadata. Duplicate private column names, missing required private columns and invalid hidden targets raise errors. Row order may differ because valid IDs are used for alignment. Invalid binding values receive zero credit for that entire case rather than a favorable default or an exception during scoring. Evaluation The Selective Binding Score combines positive-match correctness, complete-case correctness, and the ability to recognize missing matches: Score = 0.30 * MatchScore + 0.60 * PacketScore + 0.10 * AbstentionScore. Complete-case correctness receives 60% because a packet is ready for explanation review only when every state has the correct association or explicit absence. The 30% match term retains partial credit for learning individual associations, while 10% measures recognizing missing evidence. A wrong positive association must not be hidden by correctly identifying that most states have some match. These weights define the review objective; they do not make the input prediction problem intrinsically harder. For a scoring subset with no absent matches, truth [1,2,3] and prediction [1,2,4] score 0.30 * (2/3) + 0.60 * 0 + 0.10 * 1 = 0.30. A fully correct prediction scores 1.0. Across the full test set, the abstention term is averaged over both present and absent groups as defined below, not assigned separately per case. An incorrect packet can contribute at most 0.40 through the two partial-credit terms. Minimum score: 0.0. Maximum score: 1.0. Higher is better. The grader accepts 1 to 100,000 evaluation rows and uses canonical ID ordering for deterministic aggregation. Let Y[i,j] be the reference candidate number for case i, state j, and let P[i,j] be the submitted number. I(condition) is one when the condition is true and zero otherwise. There are three states per case and N evaluated cases. | Component | Exact definition | |---|---| | MatchScore | For each case, count correctly assigned positive matches and divide by that case's number of positive reference matches. Average these fractions over the N cases. Formula: mean_i(sum_j I(Y[i,j]>0 and P[i,j]=Y[i,j]) / sum_j I(Y[i,j]>0)). The denominator is either two or three. | | PacketScore | Fraction of cases whose entire three-entry prediction equals the reference: sum_i I(P[i,:]=Y[i,:]) / N. | | AbstentionScore | Treat every state as either match-present or match-absent. Compute recall separately for the two reference groups, then take their arithmetic mean. Absent recall is the fraction of reference-zero entries predicted zero. Present recall is the fraction of reference-positive entries predicted nonzero. The positive candidate must also be correct to earn MatchScore credit. | Abstention groups are determined from the answer rows being graded, not estimated from training frequencies. If a scoring subset contains only one group, use that group's recall. An invalid binding is incorrect for all three entries in both recall groups and contributes zero to MatchScore and PacketScore. All component aggregation occurs before the final weighted sum; there is no hidden coherence multiplier, semantic language judge, or parser-based bonus. Training and Allowed Methods Learn the relationship between numerical states and candidate language from the supplied training cases. Text encoders, learned state projections, joint candidate scoring, and structured assignment are permitted. General-purpose pretrained language encoders may be adapted to the supplied labels. A model should learn that a relevant explanation can still refer to the wrong position and should calibrate abstention rather than force every state to match. What Not To Use Do not derive predictions from identifiers, filenames, hashes, storage sizes, or CSV ordering. Do not identify records in external activation/explanation collections or use lookup tables that recover their original pairings. Models or checkpoints specifically trained on these source annotations are not permitted, since they can contain test-document supervision. General-purpose pretrained encoders remain allowed. Do not tune to recovered hidden labels, coordinate leaderboard probing, or exploit malformed submissions. Legitimate learned relationships in the supplied explanations and activation values are the intended evidence. Reference Validation | Check | Measured result | |---|---| | Exact reference submission | 1.000000 | | Supplied sample submission | 0.111192 | | Always abstain | 0.050000 | &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Ledger Extent Reconstruction — Ordering Volumes When Only Batch Totals Survive

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76yhf5yk6pj5myz9dkann3z18a1hs7
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat samluu206's score of 0.515!

Full challenge description from page:

> Ledger Extent Reconstruction — Ordering Volumes When Only Batch Totals Survive Overview An archive holds 80,000 volumes in two separately-ledgered wings: a 70,000-volume wing whose records you may study, and a 10,000-volume wing you have to put in order. Nobody ever wrote down how long any single volume is. What survives, in each wing, is two independent inventories of the same holdings: an accession lot ledger (which volumes arrived together) and a shelf ledger (which volumes were stored together). Each ledger line records only two things — how many volumes the batch contains and their combined extent in pages. Every volume is therefore counted twice, in two different batches, and its own extent appears nowhere. Extent is the bibliographic term for how physically long a book is. Your job is to put the 10,000 volumes of test.csv in order of individual extent: emit one real-valued score per volume so that longer volumes score higher. You have their titles, you have the two batch totals each volume participates in, and you have nothing else — no subject headings, no publisher, no author, no edition count, and no per-volume extent anywhere in the released data, not even in the training portion. This is a reconstruction problem in two halves that only work together. The batch totals are exact arithmetic constraints but leave the ordering inside a batch completely open. The titles hint at the ordering but are never paired with an extent you could imitate. Neither half reaches 0.30 on its own; fusing them reaches 0.42. Task For every volume in test.csv, output a real-valued value — a score that should increase with that volume's own extent. Only the ordering your scores induce is graded, never their scale, so a reconstructed page count, its logarithm, or any monotone transformation of either all score identically. You must learn what titles imply about extent from train.csv + train_records.csv, where the only extent information given is the combined total of each 14–26 volume batch. test_records.csv gives you the same two batch totals for every test volume. They are exact and they are yours to use: reconciling a proposed ordering with those 1,000 sums is the second half of the task. Why it is hard No volume is ever shown with its own extent. Every number you can read is a sum over a batch of 14 to 26 volumes. A title scorer has to be recovered from those aggregates — the ordinary path of fitting on per-item examples is not available anywhere in this challenge, in either split. The arithmetic alone is far from enough. The 10,000 test volumes are covered by 1,000 batch equations, so at least 9,001 directions of the solution space are entirely unconstrained. Scoring each volume by the average of its two batch means — the best you can do while ignoring the titles completely — reaches only 0.28; reconciling a flat guess against every total exactly reaches 0.29. The titles alone are not enough either. A shallow lexical scorer trained on the batch totals reaches 0.30. The corpus is multilingual (about 8% of titles contain non-ASCII characters — accented Latin, Cyrillic, CJK and romanised transliterations all occur) and a title is short: median 19 characters, median 3 tokens. Surface tricks fail. The title's own length correlates negatively with extent (rank correlation ≈ −0.12 in characters and in tokens), so the cheapest available feature is worse than useless. Batch membership itself is uninformative: both inventories are independent uniform random partitions, so which batch a volume sits in tells you nothing except through the total. Nothing can be memorised. Titles are globally deduplicated, the split is title-disjoint, ids are salted hashes, and train and test batches are disjoint universes: a train batch never contains a test volume. Real but bounded signal. Fusing a learned title prior with the batch constraints reaches ≈ 0.41–0.42. Even an oracle scorer that had been shown per-volume extents outright — information this challenge never releases — reconciles to only 0.49, so the ceiling is well below 1 and the headroom is a genuine inference gap. What the ledgers do and do not give away The totals are deliberately released, in both splits, and using them is the intended solution, not an exploit. What they cannot do is give the answer away: A batch of 14–26 volumes pins one linear equation, never an individual extent. No test volume is determined by the system: for every one of the 10,000 there are corrections that keep all 1,000 totals exactly satisfied while moving that volume's value. The minimum-norm solution of the totals-only system — the answer to "which values are consistent with the ledgers and nothing else" — misses individual extents by up to 1,576 pages and scores 0.29. Because each volume sits in one lot and one shelf, the two ledgers interlock: changing one volume's estimate forces compensations along an alternating chain through other batches. Propagating that coupling, rather than treating the two totals as two independent features, is where the score is won. How this differs from scoring a title on its own A public catalogue table that pairs a title with a page-count field supports one thing: fitting a title scorer on per-item examples. That is not this task, and it is not this data. The supervision is aggregate, not per-item. Nothing in the released data is an example of the form (title, extent). Recovering a scorer from 7,000 batch sums over 70,000 volumes is a different estimation problem with a different failure mode, and it costs real accuracy: on identical features, aggregate-only training reaches 0.30 against 0.40 for the same model shown per-item extents. The decision is joint, not per-item. Test volumes are coupled through 1,000 exact equations, so scoring each title independently leaves most of the available signal on the table: the same title prior goes from 0.30 standalone to 0.41 once reconciled against the ledgers. A scorer carried in from elsewhere still has to be reconciled here to compete. The evaluation rewards the reconstruction, not the fit. Only the induced order is scored and it is floored at 0, so calibrating magnitudes earns nothing and a scorer that reproduces the marginal distribution perfectly while ordering at chance earns exactly 0. The target is a cross-edition median extent, not one printing's page field, and it is never stated for any volume in any released file. Dataset Five UTF-8 CSV files are provided. Every file has a header row, is comma-separated, and uses standard CSV quoting (a title containing a comma or a quote is wrapped in double quotes). There are no missing values anywhere: no cell is empty or null in any file. Files train.csv — 70,000 rows, one row per training volume. Columns, in order: id, title, lot_id, shelf_id. There is no extent column: the training volumes' own extents are withheld exactly as the test ones are. train_records.csv — 7,000 rows, one row per training ledger line (3,500 accession lots and 3,500 shelves). Columns, in order: record_id, kind, n_items, total_pages. Together the 3,500 lots partition the 70,000 training volumes exactly once, and so do the 3,500 shelves. test.csv — 10,000 rows, one row per volume you must score. Columns, in order: id, title, lot_id, shelf_id. test_records.csv — 1,000 rows, one row per test ledger line (500 lots and 500 shelves), same four columns. The 500 lots partition the 10,000 test volumes exactly once, and so do the 500 shelves. sample_submission.csv — 10,000 rows, one per test.csv volume, in the same order as test.csv. Columns, in order: id, value. It is a valid but worthless submission (value is 0.0 on every row, which scores 0.00); use it as a formatting template. Every title in the dataset is unique, and volumes are split so that a title in test.csv never appears in train.csv. Train and test ids are disjoint, and so are train and test record_ids: no ledger line ever mixes training and test volumes. Columns There are eight column names across the five provided files, plus value in the file you submit. Each one is described below with its data type, which files contain it, and what it means. id — string, present in train.csv, test.csv and sample_submission.csv, and required in your submission. A 16-character lowercase hexadecimal token matching ^[0-9a-f]{16}$, for example 80e7b466f38e4c60. It is an opaque volume key: unique within each file and across train and test (80,000 distinct values in total), never null, and it carries no signal — it is a salted hash of an internal record number, so it is not derived from the title, from the extent, or from any ordering of the volumes. Use it to join your scores back to the rows of test.csv. title — string (free text, UTF-8), present in train.csv and test.csv. The volume's title plus its subtitle when the record has one, joined as a single field; this is the only text you are given. It is never empty: titles run from 3 to 480 characters (median 19, mean 22, 90th percentile 37) and from 1 to 78 whitespace-separated tokens (median 3). The corpus is multilingual — about 8% of titles contain at least one non-ASCII character — so do not assume English-only text. Titles may contain commas, quotes, ampersands and digits, and are quoted in the CSV where needed. Any explicit page phrase (patterns such as "320 pages", "224 pp", "180 leaves") has been stripped from the text, so the answer is never spelled out in the input. lot_id — string, present in train.csv and test.csv. A 12-character lowercase hexadecimal token matching ^[0-9a-f]{12}$, for example 02b016e055ea. It names the accession-lot ledger line this volume was counted in, and it always matches exactly one record_id in the same split's records file (with kind = lot). Never null. The lots are an independent uniform random partition of the volumes, so the identity of a lot carries no information beyond its ledger line. shelf_id — string, present in train.csv and test.csv. Same 12-hex format and the same guarantees as lot_id, but naming the shelf ledger line (kind = shelf). Never null, never equal to the row's lot_id, and drawn as a second, independent random partition — so the two ledgers cut the same volumes in two unrelated ways, and every volume belongs to exactly one lot and exactly one shelf. record_id — string, present in train_records.csv and test_records.csv. The 12-hex key of one ledger line, unique across both records files; every value appears as a lot_id or a shelf_id in the matching split's volume file. Never null and carries no signal — it is a salted hash of an internal counter, ordered arbitrarily. kind — string, present in train_records.csv and test_records.csv. Exactly one of two literal values: lot (this line came from the accession-lot inventory) or shelf (from the shelf inventory). Never null. Half the lines in each records file are of each kind, and a lot line is joined by lot_id while a shelf line is joined by shelf_id. n_items — number (integer), present in train_records.csv and test_records.csv. How many volumes this ledger line covers, always in the inclusive range [14, 26] with a median of 20 and a mean of 20.0. Never null. It is redundant by construction — it always equals the number of rows in the volume file that point at this record_id — and is given so you can check your join. total_pages — number (integer), present in train_records.csv and test_records.csv. The combined extent, in pages, of the n_items volumes covered by this ledger line: the exact sum of their individual extents, with no rounding, noise or truncation. Never null; it runs from 1,963 to 9,406 in train_records.csv (median 4,831) and from 2,178 to 8,550 in test_records.csv (median 4,895). The per-volume extents it sums are the hidden quantity of this challenge — each is an integer in the inclusive range [20, 2000] with median 234, quartiles 146 and 328, and mean 245 — and they are never released for any volume, in any file. value — number (float), present in sample_submission.csv and required in the file you submit. Your score for that volume: any finite real number, where a larger score means you believe the volume is longer. Only the ordering these scores induce is graded, never their scale or their absolute value (see Submission Format and Evaluation). Example — train.csv id,title,lot_id,shelf_id a7f7b2d44275ff6d,Tagged for murder,02b016e055ea,a97b7325926f 3e1e05b074a15203,Zerkalo trevog i somneniĭ,092daad917da,301b0a04492b 63c045a474210748,Darkness & shadows,49ed9bbdb5c4,5f02a71e4ee4 Example — train_records.csv record_id,kind,n_items,total_pages 0006c0c40deb,shelf,16,3056 002767b8e5f1,shelf,14,3957 002a9dc4d785,lot,24,5317 Example — test.csv id,title,lot_id,shelf_id 80e7b466f38e4c60,L' oiseau sous la chemise,c287371431e1,7291310c6255 ddc2ced377e2ea82,Pearce Oysters,f87292038923,46ea84d589e1 1a049c056984761f,Their forever love,af1e18d7fd90,abccbe7449aa Example — test_records.csv record_id,kind,n_items,total_pages 000d282f131e,lot,21,4621 005de4e3199d,lot,15,3821 00c298aee752,shelf,17,3829 Worked example Training lot ba96715357be covers 14 volumes and 2,032 pages between them — an average of 145 pages per volume, far below the corpus median of 234. Its members include What Mary Jo Shared, Handy Mr. Hippo, Robert the Rose Horse (Beginner Books(R)), The adventure of the stalwart companions, Unbecoming Habits and Cloud 9. No line of that ledger tells you any single one of those extents. What it does tell you is that picture-book vocabulary and short animal names have to be cheap in pages, because fourteen of them together only came to 2,032 — and the contrasting lot ccdb012b7ad9, also 14 volumes but 5,356 pages, pushes its own vocabulary the other way. Thousands of such constraints are what a title scorer has to be recovered from. The same line then works as a constraint rather than as supervision. Within ba96715357be, a Sherlock-Holmes pastiche like The adventure of the stalwart companions plausibly outruns Handy Mr. Hippo; but the total is fixed at 2,032, so raising one member must lower the others, and because each of those volumes also sits in a shelf line with its own fixed total, the correction propagates outward through the archive. Test lot 025d87bf748b — 14 volumes, 3,086 pages, containing among others The Price A Novel, All on the sea, Xanthippe's Dream and a Hebrew title — is the same puzzle with the answer withheld. Submission Format A CSV with exactly two columns, in this order: id (string) and value (real number). A header row id,value is required. Exactly one row per id in test.csv (10,000 rows), no duplicates and no extra ids. value is any real number; higher should mean longer. Non-numeric values are replaced by the median score (a neutral position in the order). A correctly formatted submission looks exactly like this (the leading header row, then one row per test id): id,value 80e7b466f38e4c60,742.0 ddc2ced377e2ea82,180.5 1a049c056984761f,-3.21 57592588e248bf6a,0.0 Here each id is an id from test.csv and value is your score for that volume — the numbers above are illustrative (any monotone score works; 742.0, 180.5, -3.21 and 0.0 simply need to rank longer volumes above shorter ones). The shipped sample_submission.csv uses a constant value of 0.0 for every row and scores 0.00. Evaluation Metric — Spearman rank correlation, floored at 0, computed over all 10,000 test volumes at once. Your scores are ranked and compared against the true per-volume extent ranking; a constant, inverted or below-chance submission scores 0. Measured reference points on this data, worst to best: a constant or random score 0.00; title length below chance; the mean of a volume's two batch means, titles ignored, 0.28; a flat guess reconciled exactly against every total 0.29; a shallow lexical scorer recovered from the batch totals 0.30; that same scorer reconciled against the test ledgers 0.41; iterating the two steps 0.42; and an upper reference that is not reachable from the released data, a scorer shown per-volume extents outright and then reconciled, 0.49. Approaches Recover a title scorer from aggregate observations: the ledger total of a batch is the sum of its members' extents, so a model whose per-volume outputs are summed over a batch can be fitted against 7,000 observed sums. Additive models make that sum trivial to form; a neural scorer can be trained the same way by summing its outputs within a batch before comparing to the total. Alternate between reconstruction and refitting: impute per-volume extents on the training archive so that every training total is satisfied, refit the title scorer on those imputed values, and repeat. Both halves improve on each pass. At scoring time, treat test_records.csv as 1,000 exact equations, not as two extra features. Correcting a prior so that it satisfies all of them — a least-change correction is the natural choice, and weighting the change by how uncertain each volume is helps — is what turns 0.30 into 0.41. Fit on the logarithm of extent if you like, but remember the ledger totals are additive in pages, so the constraint has to be applied in pages. Cues cross languages: build features that survive script changes rather than assuming English text. Validate locally by holding out whole training lots and their interlocking shelves, rebuilding a self-contained sub-archive, and computing Spearman against extents you reconstructed for that held-out part. What Not To Use Do not try to identify the specific volumes and look up their extents from any library catalogue, bookstore or search engine. Only the title is given precisely so that the task is reconstructing length from the archive's own records, not retrieving it. Do not train on an outside corpus that pairs book titles with per-item page counts. The point of this challenge is recovering a scorer from aggregate ledger totals; importing per-item supervision from elsewhere replaces the problem instead of solving it. Do not hard-code answers. The intended solution generalises to unseen titles and unseen ledgers. &nbsp;
> $700 Pool
> Closes in 3h 34m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Leaf-Litter Propagation Residual Modeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78qcdsx6km3aw85fb8d3n4z98c7970
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.219!

Full challenge description from page:

> Leaf-Litter Propagation Residual Modeling Overview This is a from-scratch scientific signal-modeling challenge. Each row contains two synchronized sensor layers from a leaf-litter monitoring window and a strong public anchor reconstruction for a third sensor layer. Your task is to improve on that anchor by predicting the residual signal it misses. In plain terms: the dataset already gives you a decent physics-style guess for the hidden vibration layer. You only score for making that guess better. Copying the anchor is valid, but it scores 0. The source setting is field monitoring under leaf litter. A small animal or environmental event can reach four sensing media differently: airborne sound above the litter; vibration at the leaf-litter surface; vibration deeper in the litter; vibration coupled into the ground. The prepared rows encode these synchronized sensor layers as compact 18 by 96 energy matrices. Solver-facing files remove original filenames, timestamps, site names, species names, and source segment identifiers. The raw dataset package contains source attribution and CC0 data-use terms. This is not species classification or regression, behavior classification, tabular regression, computer vision, ordinary audio tagging, or simple hidden-channel imputation. The central task is residual modeling: beat a public propagation anchor on source-disjoint hidden windows. Dataset files train.csv contains the public features for 4,524 training examples. test.csv contains the same feature columns in the same order for 996 hidden examples. id: string. Unique training row ID. input_sensor_a: string. First visible sensor channel. One of air, surface, bottom, or ground. input_sensor_b: string. Second visible sensor channel. target_sensor: string. Hidden channel to model. route_family: string. Public transfer route label. input_a_code: string. Encoded 18 by 96 matrix for input_sensor_a. input_b_code: string. Encoded 18 by 96 matrix for input_sensor_b. anchor_code: string. Public anchor reconstruction for target_sensor. environment_card: JSON object. Coarse environmental context. test.csv contains 996 hidden examples, balanced at 166 rows for each of the six route families. Its columns are exactly the same as train.csv. The test-to-train row ratio is 22.0%. train_targets.csv contains the public labels for the 4,524 training rows: id: string. Training row ID. target_code: string. True encoded 18 by 96 target matrix. Join train.csv to train_targets.csv by id. Row order is not a join key. Keeping labels in a separate training-label file gives train.csv and test.csv identical query schemas without exposing any test target. sample_submission.csv copies anchor_code for every test row. It is structurally valid and scores exactly 0, because the evaluation measures improvement over the anchor. sample_submission.csv and private answers.csv both contain exactly these columns in this order: id: string. Test row ID. predicted_target_code: string. The sample contains the public anchor; the private answer column contains the true target code. anchor_code and route_family remain public fields in test.csv; they are not duplicated in answers.csv. The evaluator's fixed ID-indexed copy of those public fields supports scoring after the platform partitions answer rows. Encoded signal format Every signal code has length 1,728. Decode each character through: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_ The character value is an integer from 0 to 63. Divide by 63 and reshape row-major into an 18 by 96 matrix: 18 rows are coarse frequency or vibration-energy bands, low to high. 96 columns are consecutive synchronized time frames. Larger values mean stronger normalized energy. Your submitted predicted_target_code uses the same format. Public anchor anchor_code is a deterministic public baseline reconstruction. It is fitted from public training rows and then applied to both public training rows and hidden test rows. It is included so that every solver starts from the same strong baseline and the leaderboard measures residual improvement rather than the easy smooth transfer component. For each route, concatenate the two 18-band inputs into 36 channels. At every output time frame, take the raw values from the centered ±10-frame neighborhood, pad beyond the window with zeros, append the squared values and a constant bias, and standardize non-bias features using all training frames for that route. Fit a multi-output ridge regression to the 18 target bands with diagonal penalty 20. Apply it to training and test rows, clip to [0,1], and quantize to 64 symbols. No hidden target is used. The anchor captures gross delay, damping, broad spectral shape, and the mean route residual. The challenge is to recover row-specific remaining structure: local energy bursts, route- and environment-conditioned distortion, peak placement, and errors that vary from window to window. JSON field schema environment_card is a JSON object with: site_class: string. Coarse habitat condition alias. monitoring_context: string. animal_enclosure or control_enclosure. period_bucket: string. Coarse time-of-day bucket. microclimate_bucket: string. cool_wet, mixed, or hot_dry. litter_depth_bucket: string. shallow, medium, or deep. wind_bucket: string. low, medium, or high. call_context: string. none, distant_call, near_call, or control. activity_density: string. Coarse public activity-density bucket. These fields provide context but do not contain the hidden residual. Task For each test row: Decode input_a_code, input_b_code, and anchor_code. Predict a better reconstruction of target_sensor than the public anchor. Encode your improved 18 by 96 matrix as predicted_target_code. The prediction should be the full target matrix, not just a residual matrix. The grader internally compares your prediction against the anchor. Evaluation Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order. Malformed row-level predictions score 0 for that row. A malformed prediction includes a non-string value, a code with the wrong length, or a character outside the allowed alphabet. Rows are aligned by id, not row order. For each valid row, let: P be the decoded submitted prediction. T be the decoded hidden target. A be the decoded public anchor. An exact prediction of the hidden target code receives row score 1. An all-zero prediction receives row score 0. A prediction equal to the public anchor receives row score 0 from the formulas below. Preparation verifies that no evaluated target is identical to its anchor after quantization. Weighted cell error: WeightedMAE(X, T) = mean((0.35 + 1.65 * T) * abs(X - T)) WeightedMSE(X, T) = mean((0.35 + 1.65 * T) * (X - T)^2) Profile error: TemporalMAE(X, T) = mean(abs(mean_freq(X) - mean_freq(T))) BandMAE(X, T) = mean(abs(mean_time(X) - mean_time(T))) ProfileMAE(X, T) = 0.60 * TemporalMAE(X, T) + 0.40 * BandMAE(X, T) Peak F1 compares high-energy cells. The true peak mask is: T >= max(0.32, quantile(T, 0.88)) The predicted or anchor peak mask is computed the same way for that matrix. Standard precision, recall, and F1 are computed from the two masks. If both masks are empty, F1 is 1. If only one is empty, F1 is 0. The three error components use direct relative error reduction. There are no fitted scale factors, empirical denominators, or shaping exponents. For any nonnegative error measure E: RelativeErrorGain(E) = 0, if E(A, T) <= 1e-12 clip((E(A, T) - E(P, T)) / E(A, T), 0, 1), otherwise Therefore: CellGain = RelativeErrorGain(WeightedMAE) EnergyGain = RelativeErrorGain(WeightedMSE) ProfileGain = RelativeErrorGain(ProfileMAE) For example, reducing an anchor component's error by 5% gives exactly 0.05 credit for that component. Matching or worsening the anchor gives 0; reducing the error to zero gives 1. If the anchor error is already at most 1e-12, no improvement is possible and that component is defined as 0. PeakGain measures the fraction of the remaining F1 gap that is closed: PeakGap = 1 - PeakF1(A, T) PeakGain = 0, if PeakGap <= 1e-12 clip((PeakF1(P, T) - PeakF1(A, T)) / PeakGap, 0, 1), otherwise Thus an anchor that already has perfect peak F1 has no peak gap left to close, and PeakGain is 0 for that row. These zero-denominator rules are part of the metric, not hidden implementation details. ResidualDirection checks whether the submitted correction points in the right shape: PredResidual = flatten(P - A) TrueResidual = flatten(T - A) ResidualDirection = max(0, cosine_similarity(PredResidual - mean(PredResidual), TrueResidual - mean(TrueResidual))) If the submitted prediction equals the anchor, PredResidual is all zeros and ResidualDirection is 0. The row score is: row_score = 0.34 * CellGain 0.21 * EnergyGain 0.17 * PeakGain 0.10 * ProfileGain 0.18 * ResidualDirection The hidden set is balanced across six route families, with exactly 166 rows per family: air_surface_to_bottom surface_bottom_to_ground air_bottom_to_surface surface_ground_to_bottom air_ground_to_surface bottom_ground_to_surface Final score: overall_mean = mean(row_score over all hidden rows) worst_family_mean = minimum mean(row_score) over the six route families bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows) final_score = 0.68 * overall_mean 0.22 * worst_family_mean 0.10 * bottom_20_mean Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect prediction of every hidden target scores 1. Submission format Submit a CSV file with exactly two columns in this order: id: string. Test row ID from test.csv. predicted_target_code: string. Encoded 18 by 96 target reconstruction. Example: id,predicted_target_code 0a12bc34de56f789,0000000000000000000000000000000000000000000000000000000000000000... The example is truncated. A real prediction must contain exactly 1,728 characters. What not to use Do not use original filenames, timestamps, source segment order, species names, site names, or external source lookup. These are absent from solver-facing files and are not needed. Do not infer meaning from row IDs or row order. IDs are alignment keys only. Do not submit a residual-only code. Submit the full improved target matrix. Do not optimize only one route family. Worst-family and bottom-tail scoring penalize uneven improvements. Resource limit Solutions are intended for CPU execution: 10 CPU cores; 62.5 GiB RAM; maximum runtime 1.5 hours. Benchmark boundary Most bioacoustic and vibration benchmarks ask for event detection, species labels, call labels, or direct sensor imputation. This benchmark asks solvers to beat a public cross-medium propagation anchor and is scored only on residual improvement. That makes it a residual scientific modeling benchmark rather than ordinary hidden-channel reconstruction.
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Support-Fiber Gauge Inference and Metamorphic Orbit Breakpoint Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75qn159tzrz4x23v8qrbt72h8dtb5w
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat konda's score of 93.365!

Full challenge description from page:

> Overview Support-Fiber Gauge Inference and Metamorphic Orbit Breakpoint Localization is an episodic structured-reasoning challenge over semi-structured tables. Its central object is not a fixed table program and not a conventional transform-invariance test. Every episode first creates a temporary latent language, then asks the model to infer a support-conditioned neighborhood of plausible meanings for that language, and finally to identify which behavioral equivalence class explains a transformed query. Each episode maps eight opaque symbols, Q01 through Q08, injectively into eight members of a stable sixteen-macro catalogue. The assignment is freshly randomized in every episode. A Q symbol therefore has no persistent semantics across rows. The support set is deliberately composite and incomplete. Every demonstration executes at least two Q symbols, and many intermediate checkpoints are hidden. No support example acts as a clean one-symbol diagnostic. The model must infer the temporary codebook by reconciling overlapping constraints across the whole support set. The scored queries then apply an opaque program to two aligned table views. One view is structurally transformed by transpose, reversal, or boundary crop. Rather than asking the participant to generate the resulting cell sets, the query presents eight executable cards. Each card is produced by a different support-ranked codebook hypothesis and records the full source trajectory, derived trajectory, and stepwise correspondence witness under that hypothesis. The candidate bank is therefore episode-dependent in a strong sense: changing the support evidence changes which alternative codebooks are considered plausible, which in turn changes which execution cards can appear, even when the query table and transformation are unchanged. For every episode, predict three coupled objects: the eight-symbol episode codebook; the correct behavioral card for each query; the first checkpoint at which source-to-derived correspondence fails. These are not independent labels. The codebook defines the latent execution, the execution induces a card, and the card contains the correspondence sequence from which the divergence label is derived. Problem Research This benchmark studies support-conditioned identification of a temporary transition language. Every episode independently rebinds eight opaque Q symbols to a subset of a stable macro catalogue, so symbol identity cannot be memorized across rows. Partial composite demonstrations define a local version space of plausible codebooks rather than directly identifying individual operators. Query candidates are generated from that version space. Alternative support-compatible codebooks are executed on the same transformed table query, and hypotheses producing identical observable trajectories are collapsed. The eight public cards therefore represent distinct behavioral equivalence classes induced by the episode's own unresolved semantics rather than generic corrupted answers. The task combines two forms of symmetry. The first is episode-local symbol rebinding: Q codes are temporary coordinates over latent macros. The second is structural transport between source and transformed table views. After each program step, source execution transported through the public cell correspondence is compared with direct execution in the transformed view. The divergence target records the first checkpoint where those routes disagree. Consequently, the prediction chain is partial supports → temporary codebook → query behavior class → first transport failure. Card selection and divergence localization are downstream of codebook inference rather than independent classification problems. Evaluation additionally uses a strict compositional holdout. For every query define its interaction key as (latent macro of the first Q symbol, latent macro of the second Q symbol, table transformation). Keys assigned to the evaluation bucket never occur in training. All primitive macros and transformation families remain represented; what is held out is their leading interaction. Preparation explicitly validates zero overlap between training and evaluation interaction keys before releasing the files. Research Thesis The benchmark studies a specific form of amortized epistemic system identification: Can a learned model infer a temporary operator semantics from incomplete composite demonstrations, preserve the ambiguity among observationally equivalent hypotheses, and resolve that ambiguity by predicting the correct transformed behavior and its first non-commutation witness? The table domain provides a concrete semi-structured state space, but the deeper object is the interaction between latent semantic rebinding, partial identifiability, posterior-predictive behavioral quotienting, and equivariance failure localization. That combination makes the task more than a table benchmark with hidden labels and more than breakpoint localization with a metamorphic wrapper. The scored object is an episode-conditioned reconstruction of a transition system whose semantics, behavioral equivalence classes, and failure witness are all coupled. Structural Relation Vocabulary Public table states are ordered CELL_SET values. Views expose cell text, coordinates, header flags, span footprints, local identifiers, and provenance. The stable structural relation families are: ROW COL HEAD DATA SPAN FRONTIER DIAGONAL HULL ROW_EDGE COL_EDGE VALUE INVERT These names provide inductive bias. Participants are not required to produce the result of one relation directly. Each stable macro M01 through M16 is an ordered composition of two relation families. Order matters: reversing the pair defines a different macro class even when both happen to agree on a simple table state. The macro catalogue is public in every episode. Episode Contents Every row contains thirteen public feature columns: episode_id difficulty macro_catalogue episode_tables support_set query_1 through query_8 macro_catalogue gives the sixteen stable ordered macro compositions. episode_tables contains one support view, one source query view, eight derived query views, cell metadata, and explicit provenance maps between source and derived views. Cell and view IDs are local to the episode. The support set contains fourteen compositional demonstrations. Each support demonstration includes: one starting cell set; a program of two or more Q symbols; one checkpoint per executed operator; null at deliberately hidden checkpoints. The final support checkpoint is always visible. Each scored query contains: a source view; a derived view; the declared transformation; aligned source and derived starts; a Q-symbol program of length 4 through 10; eight shuffled execution cards. Every execution card contains: source checkpoint signatures for every program step; derived checkpoint signatures for every program step; one source-to-derived correspondence bit for every program step; final source and derived signatures. A checkpoint signature contains the resulting cell-set cardinality and a deterministic digest of the ordered local cell IDs. Participants rank cards; they do not generate these signatures. Training Contract train.csv contains the thirteen public feature columns followed by twenty-four labels. The first eight labels reveal the complete local codebook: q01_macro q02_macro q03_macro q04_macro q05_macro q06_macro q07_macro q08_macro Each value is one of M01 through M16, and all eight are distinct within an episode. For every scored query, training also provides: query_i_card query_i_divergence query_i_card is one of A01 through A08 and identifies the correct execution card. Divergence Labels The divergence vocabulary is exactly: S00, S01, S02, S03, S04, S05, S06, S07, S08, S09, S10 There is no other divergence syntax. S00 means that all source-to-derived correspondence checkpoints for the public query are true. For an integer step k from 1 through 10, the label is written as S followed by the two-digit decimal representation of k. Examples: first failure after operator 1 → S01; first failure after operator 3 → S03; first failure after operator 9 → S09; first failure after operator 10 → S10. A program containing L Q operators produces exactly L correspondence checkpoints, one immediately after each executed operator. Therefore, for a query of public program length L, the valid divergence labels are exactly: S00; the labels for first failure after steps 1 through L. For example, a four-operator query permits S00,S01,S02,S03,S04. A ten-operator query permits S00 through S10. The boundary is fully visible from query_i.program. Private metadata is not needed to determine legal labels. Test Contract test.csv contains only the thirteen public feature columns. It does not expose: Q-to-macro labels; correct card labels; divergence labels; private query-symbol metadata; private query-length integrity fields. Local Q symbols, card IDs, cell IDs, and view IDs do not have stable semantic meaning across episodes. Data Split and Generalization The prepared build contains exactly: 1,000 training episodes; 200 evaluation episodes. Pages are assigned deterministically to one partition before episodes are constructed. A page cannot contribute retained tables to both partitions. Training and evaluation episodes are generated independently from those page-disjoint pools. The query sampler additionally enforces the compositional interaction holdout described above: the deterministic signature of the first two latent macros together with the transformation is disjoint between training and evaluation. Evaluation therefore tests two forms of transfer at once: structural transfer to unseen pages and tables; compositional transfer to a reserved macro-adjacency/transformation regime. The stable macro catalogue remains shared, so the challenge measures recombination of known structural primitives rather than introduction of undisclosed operator classes. Targets For every episode, predict: q01_macro through q08_macro, using eight distinct codes from M01 through M16; query_1_card through query_8_card, using A01 through A08; query_1_divergence through query_8_divergence, using the legal divergence vocabulary for that query's visible program length. There are twenty-four predictions per episode. Worked Interpretation Suppose the support set makes two mappings plausible but does not isolate either directly. Across several partial traces, the model assigns high posterior mass to Q02=M04 and Q07=M11. A scored query applies a longer program containing those Q symbols to a source view and a transformed derived view. Each candidate card corresponds to a coherent competing latent-codebook execution. Several cards may agree on final cardinality. Several may agree on the first few correspondence bits. If the correct card remains aligned through checkpoints one and two and first breaks at checkpoint three, the required divergence output is S03. The card and divergence targets are therefore tied to the same latent execution hypothesis, while the Q-to-macro labels expose whether the model reconstructed the underlying episode gauge itself. Submission Format Use sample_submission.csv exactly. The submission has twenty-five columns in this order: episode_id,q01_macro,q02_macro,q03_macro,q04_macro,q05_macro,q06_macro,q07_macro,q08_macro,query_1_card,query_1_divergence,query_2_card,query_2_divergence,query_3_card,query_3_divergence,query_4_card,query_4_divergence,query_5_card,query_5_divergence,query_6_card,query_6_divergence,query_7_card,query_7_divergence,query_8_card,query_8_divergence For every row, macro labels must use M01 through M16, card labels must use A01 through A08, and divergence labels must use S00 through S10. The intended episode codebook is injective: the eight Q symbols map to eight distinct macro codes. A submitted row that repeats a valid macro code is therefore structurally inconsistent. It is still numerically scoreable by the evaluator, but all eight macro assignments in that episode receive zero macro credit and cannot contribute exact joint or exact episode credit. This convention keeps degraded baselines and ranking-stability fixtures scoreable without weakening the target definition. Likewise, if a query program contains L operators and a submitted divergence token refers to a later step, that token is structurally inconsistent for that query. It receives zero divergence credit for that query rather than aborting evaluation. Example boundary cases: length 4: valid labels are S00,S01,S02,S03,S04; length 7: valid labels are S00 through S07; length 10: valid labels are S00 through S10. Every expected episode_id must appear exactly once. Extra IDs, missing IDs, duplicate IDs, blanks, additional columns, incorrect column order, or categorical codes outside their published domains are malformed submissions and receive the evaluator floor. Structural inconsistencies that remain inside the published code domains, such as repeated macro assignments or an out-of-range divergence step, are scoreable but receive zero credit on the affected structure as described above. Evaluation The metric rewards balanced marginal recovery and progressively stronger consistency between the inferred codebook and query decisions. Let: m be macro accuracy over the eight Q assignments; c be card accuracy over the eight scored queries; d be divergence accuracy over the eight scored queries. Define balanced recovery: R = (m × c × d)^(1/3) The geometric mean prevents one target family from compensating for complete failure on another. Soft Joint Query Accuracy For a scored query, consider the distinct Q symbols that actually appear in its public program. Let u_i be the fraction of those used Q symbols whose macro assignments are correct. If both the query card and divergence label are correct, that query receives soft-joint credit u_i. If either the card or divergence label is wrong, the soft-joint credit is zero. Let s be the mean soft-joint credit over all scored queries. This gives dense compatibility credit while preserving the connection between local card selection and the episode codebook. Exact Joint Query Accuracy Let j be the fraction of scored queries for which all of the following are correct: the selected card; the divergence label; every Q-to-macro assignment used by that query. Exact Episode Accuracy Let e be the fraction of episodes for which all twenty-four submitted targets are correct. Consistency Term Define: K = 0.55s + 0.30j + 0.15e The weighting forms a soft-to-hard hierarchy. S receives the largest weight because it preserves ranking resolution before exact query closure becomes common. J rewards fully coherent local executions. E rewards complete episode recovery but receives the smallest coefficient because it is intentionally sparse and all-or-nothing. Final Score The final score is: Score = 100 × R^0.40 × K^0.60 Scores are clipped to [0.01,100]. A perfect submission has m=c=d=s=j=e=1, giving R=1 and K=1. Therefore the score is exactly 100.0. The larger exponent on K reflects the benchmark's primary objective: not merely predicting labels independently, but reconstructing a codebook whose implied query decisions are mutually compatible. Evaluation is deterministic categorical comparison. There is no LLM judge, embedding service, external API, or manual review. Evaluator Contract Participant submissions must exactly match the twenty-five-column sample_submission.csv schema. The evaluator always returns a numeric score in [0.01,100]. Malformed submissions are mapped to the floor score rather than causing ranking fixtures to terminate without a score. The private evaluator may append grader-only metadata to the answer file after those twenty-five submission columns. Such metadata is not part of the participant contract. Evaluator-generated known-answer frames that contain those private columns are recognized only when their twenty-five submission fields exactly equal the private gold targets; arbitrary extra-column participant submissions remain malformed. Private query-symbol metadata is used only to compute soft and exact joint consistency. Stored query lengths are an integrity mirror of the already-public query_i.program length. The private evaluator does not define any hidden divergence boundary. Compute Environment The execution environment provides one NVIDIA A10G GPU with 24 GB VRAM and a 90-minute end-to-end runtime budget. Host CPU and memory are available for parsing, graph construction, caching, and batching. The GPU is part of the intended solution regime. Competitive systems should contain trainable neural parameters fitted or calibrated from the released training episodes. Useful approaches include: table-aware transformers over text, coordinates, spans, and headers; relational graph networks over row, column, span, and provenance relations; support-conditioned latent assignment models; amortized latent-variable models over the episode-local gauge; compact neural executors trained from partial checkpoints; multi-task models with macro, card, and divergence heads. A practical implementation can cache cell embeddings, encode table graphs once, use mixed precision, and batch candidate-card scoring across queries. Machine-Learning Requirement This is an ML track rather than an exact programming-puzzle track. The intended solution learns support-conditioned transition representations and candidate-ranking behavior from training episodes. Validity checks and constrained categorical decoding are allowed. A hand-written exact executor that directly encodes the benchmark's complete hidden transition semantics and deterministically solves every query is outside the intended solution class. Expected Modeling Direction A strong system should maintain a posterior over the episode-local gauge rather than predicting each Q symbol as an isolated global class. That posterior can condition a structured table encoder or neural executor that scores competing gauge-orbit hypotheses and their source/derived metamorphic trajectories. The compositional holdout makes this especially important: test queries deliberately combine familiar macros and transformations in leading interactions absent from training. The challenge therefore rewards coordinate-aware models that learn reusable structural semantics, bind those semantics to temporary episode symbols, and localize symmetry breaking under unseen structural compositions rather than memorize Q labels or macro-pair templates.
> $700 Pool
> Closes in 2h 42m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Checkpoint Relay Portfolio

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72dpads1p5v8em5hhfr9wawd8dz10q
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat singhking's score of 0.743!

Full challenge description from page:

> Overview For each case, rank eight pairs of partially trained neural architectures, select the best three compatible pairs to continue, and identify which pairs are most likely to change rank or behave inconsistently by the end of training. This models a practical experiment-allocation decision. A research team has many candidate network cells but enough compute to finish only a small, non-overlapping portfolio. Each candidate A through H contains two independently measured cell graphs. The public packet shows graph structure, operation type, parameter count, and three repeated measurements at the halfway checkpoint. Final-checkpoint measurements are hidden. The selected portfolio must respect the supplied parameter budget and cannot reuse one underlying architecture through two candidate pairs. The goal is not to predict one validation-accuracy number. It is to learn which graph and early-training patterns remain reliable late in training, then issue a connected resource-allocation certificate. Graph neural networks or transformer encoders can learn across the 12,000 training cases and process the complete candidate packet efficiently on a GPU within the 30-minute training allowance. Dataset The cases are derived from a complete public release of measured neural-architecture evaluations. The release name and license appear in the separate dataset card. Source architecture hashes and original operation strings are not exposed in the challenge data. There are 12,000 training cases and 3,000 evaluation cases. Each case contains eight candidate pairs and therefore sixteen graph appearances. The evaluation size is 25% of the training size. | File | Contents | |---|---| | train.csv | Input columns and three target columns. | | test.csv | Input columns only. | | sample_submission.csv | A schema-valid baseline with evaluation IDs. | | architecture_packets.npz | Tensor arrays for every train and evaluation case. | CSV Columns | Column | Type | Availability | Meaning | |---|---|---|---| | case_id | string | train, test | Opaque identifier relay_ followed by 26 lowercase hexadecimal characters. | | packet_row | integer | train, test | Row in every array stored in architecture_packets.npz. | | parameter_budget | integer | train, test | Maximum total trainable parameters allowed across the three selected candidates. | | continuation_portfolio | canonical label set | train only | Three compatible candidate labels chosen using final-checkpoint evidence. | | late_rank_word | ordered label sequence | train only | All eight candidates ranked from strongest to weakest final utility. | | fragility_vector | JSON integer vector | train only | One late-behavior code for each candidate A through H. | Packet Arrays Candidate axis positions 0 through 7 correspond to A through H. Endpoint axis positions 0 and 1 are the two measured architectures in that candidate. | Array | Shape | Type | Meaning | |---|---|---|---| | adjacency | (15000,8,2,7,7) | uint8 | Directed cell adjacency matrices. Internal nodes are independently relabeled at each appearance. | | operations | (15000,8,2,7) | uint8 | Node operations: 0 input, 1 one-by-one convolution, 2 three-by-three convolution, 3 max pooling, 4 output, 5 padding. | | halfway_metrics | (15000,8,2,3,4) | float32 | Three repeats. Channels 0 through 2 are rounded train, validation, and test accuracy; channel 3 is within-run normalized training time. | | parameter_count | (15000,8,2) | int32 | Trainable parameter count for each endpoint architecture. | The source measurements are not copied verbatim into public packets. Internal nodes are relabeled, accuracies are rounded to three decimals, and time is normalized within an endpoint's repeat set. These transformations preserve learning evidence while reducing direct record lookup. Targets continuation_portfolio contains exactly three alphabetically sorted labels separated by |, for example A|C|H. The three candidates use six distinct endpoint architectures and their total parameter_count does not exceed parameter_budget. Among all legal triples, the target maximizes summed final utility. Ties use alphabetical order. For candidate k, concatenate its six final repeat measurements, three from each endpoint. Its final utility is: late_rank_word lists all candidates in decreasing U(k), joined by >, such as G>A>D>C>H>B>F>E. Alphabetical order breaks exact ties. fragility_vector is a JSON array of eight integers in A through H order: | Code | Meaning | |---:|---| | 0 | Final-repeat dispersion is at or below the case median and the rank moves by fewer than three places. | | 1 | Final-repeat dispersion is above the case median, but the rank moves by fewer than three places. | | 2 | The candidate moves by at least three places between halfway and final ranking. | Target Distribution | Quantity | Training | Evaluation | |---|---:|---:| | Fragility code 0 positions | 35,939 | 8,970 | | Fragility code 1 positions | 36,186 | 9,108 | | Fragility code 2 positions | 23,875 | 5,922 | | Distinct complete rank words | 10,344 | 2,886 | | Parameter budget, minimum | 10,315,469 | 15,134,411 | | Parameter budget, median | 52,653,518 | 52,720,737 | | Parameter budget, maximum | 130,798,780 | 131,093,308 | All three fragility codes occur in both splits. No single continuation portfolio exceeds 6% of either split. Source Isolation Architecture records are assigned to training or evaluation by a salted hash before candidate pairs or cases are built. All three measured repeats of one architecture remain together. A source architecture can appear in multiple cases on its own side, but never on both sides. The case generator draws exclusively from the corresponding source pool, so no endpoint, exact graph record, or measured final trace crosses the boundary. The selected source pool contains 60,545 computationally distinct architectures. The case builder actually uses 44,131 training-side architectures and 11,002 evaluation-side architectures. Public case IDs hash the finalized transformed packets; they do not encode source hash, utility, rank, row order, or split position. packet_row follows a global opaque-ID sort across both splits. Submission Format Write ./working/submission.csv with exactly these columns in this order: All columns are CSV strings. A valid row is: | case_id | continuation_portfolio | late_rank_word | fragility_vector | |---|---|---|---| | relay_0123456789abcdef0123456789 | A|C|H | G>A>D>C>H>B>F>E | [0,1,2,0,1,0,2,1] | Submit every evaluation ID exactly once. Row order is irrelevant. Missing, extra, duplicated, malformed, numeric, or whitespace-modified IDs reject the submission. Extra, missing, duplicated, or reordered columns also reject it. The submission schema must equal the answer schema exactly. A backend-managed visibility column is accepted only when it appears in both tables in the same position; do not add it yourself. The portfolio must contain exactly three sorted unique labels. The rank must be a permutation of all eight labels. The fragility field must be JSON no longer than 32 characters and contain exactly eight integers in 0 through 2. Malformed fields receive zero for their component; they are never clipped or converted to a favorable default. Hidden answers pass the same parsers, and malformed ground truth raises an error. Evaluation The Checkpoint Relay Score is: Minimum score: 0.0. Maximum score: 1.0. Higher is better. | Component | Share | What it measures | |---|---:|---| | Portfolio score | 45% | Quality of the legal three-pair continuation decision. | | Late-rank score | 35% | Complete final ordering with bounded near-rank credit. | | Fragility macro F1 | 20% | Balanced recovery of stable, dispersed, and reversing candidates. | For each case, portfolio set F1 is |truth intersection prediction| / 3, because both sets contain three labels. The row's portfolio score is 0.75 * exact_match + 0.25 * set_F1. PortfolioScore is the mean row score. It receives 45% because the limited continuation decision is the operational outcome, and exact compatibility matters more than recovering one attractive candidate. For each rank word, pairwise agreement is the fraction of the 28 unordered candidate pairs placed in the same relative order as the truth. The row score is 0.70 * exact_permutation_match + 0.30 * pairwise_agreement. LateRankScore is the mean row score. It receives 35% because complete late ordering tests more information than the chosen triple while still giving bounded credit for near-correct ranks. FragilityMacroF1 pools all eight positions over all evaluation cases, computes standard F1 separately for codes 0, 1, and 2, and averages the three values. For code s, F1_s = 2TP_s / (2TP_s + FP_s + FN_s). It receives 20% because stable deployment also requires identifying high-dispersion and late-reversal candidates, including the less frequent reversal state. Exact answers score 1.0. The metric has no hidden frequency weights, stochastic sampling, clipping, or dependence on submission row order. What Makes This Interesting Early accuracy alone does not determine the answer. A pair can look strong at the halfway checkpoint yet become volatile, reverse rank, exceed the shared parameter budget, or conflict with another pair through a reused endpoint. The solver must combine graph representation learning, learning-curve extrapolation, repeat uncertainty, and constrained portfolio search.The complete pipeline must finish within 1.5 hours, including data loading, training, inference, validation, decoding, and submission generation. What Not To Use Use the supplied packets and training targets. Do not identify source architectures through external benchmark APIs, canonical graph lookup, or brute-force recovery of original hashes. Do not use case IDs, packet rows, file offsets, archive order, hidden answers, leaderboard probing, or parser behavior as predictive evidence. The split and transformations are designed to evaluate learned transfer to held-out architecture records, not retrieval of their published final measurements. &nbsp;
> $700 Pool
> Closes in 10h 49m
> 9 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Factory Speech Donor Span Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72hvrdttevyhv2xdmv9z32bn8dsms0
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masonjr's score of 0.453!

Full challenge description from page:

> Overview For each damaged factory-speech recording, locate the corrupted time interval, rank six possible donor recordings, and map the replacement span into every donor. Submit three structured outputs derived from the seven-channel audio packet. Industrial voice systems often record the same short instruction from several operators, headsets, and sessions. If a useful recording is clipped or contaminated, another take can supply the missing phrase, but only when its spoken content and timing agree. A low-noise recording of the wrong instruction is not a valid donor, and a correct donor can still create an audible boundary if its active span is mapped badly. Every case contains one damaged primary recording and candidates A through F. Three candidates contain the same scripted phrase as the primary, spoken by different people. The other three are nearby but different technical phrases. No transcript, script number, speaker identity, or source filename is public. Train and test use disjoint speakers and disjoint instruction scripts, and every candidate used in a packet comes from the packet's own split. You must predict: | Output | Prediction | |---|---| | damaged_interval | The corrupted interval in a 64-bin timeline. | | donor_preference | A complete best-to-worst ordering of candidates A through F. | | replacement_span_matrix | The corresponding replacement interval in each candidate's 64-bin timeline. | The three predictions specify where to repair the primary, which recording to use, and which part of each candidate corresponds to the damage. A donor order does not specify any timestamps, and donor timestamps do not establish whether the spoken phrase is correct. Acoustic boundary compatibility contributes to donor ordering but is not an additional prediction target. Dataset The prepared public collection contains 3,600 labeled training cases and 800 unlabeled test cases. | Path | Description | |---|---| | train.csv | Packet paths and three target fields for training. | | test.csv | Packet paths for held-out speakers and held-out instruction scripts. | | sample_submission.csv | Schema-valid baseline covering all test IDs. | | speech_packets/*.npz | Compressed seven-channel speech packets. | CSV Columns Both train.csv and test.csv contain: | Column | Data type | Description | |---|---|---| | case_id | string | Opaque case identifier. It does not encode speaker, phrase, date, or target values. | | speech_packet_path | string | Relative path from the public dataset root to the case's .npz packet. | Only train.csv contains: | Column | Data type | Shape or grammar | Description | |---|---|---|---| | damaged_interval | JSON integer array encoded as a string | length 2 | Half-open interval start,end) on bins 0 through 63, with start | Complete donor order. Candidates with matching spoken content precede wrong-phrase candidates; candidates within each group are ordered by measured splice risk. | | replacement_span_matrix | JSON integer matrix encoded as a string | 6 by 2 | One half-open donor interval per candidate in A through F order. Every endpoint is from 0 through 63 and each start is smaller than its end. | test.csv contains only the two input columns. sample_submission.csv and the evaluator's answers.csv contain exactly case_id, damaged_interval, donor_preference, replacement_span_matrix, in that order. Packet Arrays Load a packet with numpy.load. Candidate index 0 is A, index 1 is B, and so on. | Key | Data type | Shape | Description | |---|---|---|---| | damaged_primary | int16 array | 40000 | Corrupted primary waveform, 2.5 seconds at 16 kHz. | | donor_recordings | int16 array | 6 x 40000 | Six candidate waveforms in A through F order. | | sample_rate | int32 scalar | scalar | Sampling rate, always 16,000 Hz. | Divide a waveform into 64 equal bins when interpreting interval targets. The damaged span contains one of three localized defects: competing-phrase intrusion, intermittent attenuation, or reversed intruding speech mixed with colored noise. Each packet also applies a case-specific nonlinear time warp, smooth equalization, multi-path room response, low-level electrical hum, gain change, and compression. These transformations preserve surrounding speech and reduce exact waveform matching, but are not a guarantee against source identification. External source matching is prohibited. Target Semantics damaged_interval marks the deliberately altered primary bins. A donor span follows the monotonic spectral-time alignment between the clean primary take and that donor. Different speech rates and pauses mean that donor endpoints cannot be recovered by copying the primary bin indices or scaling one active window. Donor ordering first enforces spoken-phrase compatibility: the three matching-phrase candidates precede the three wrong-phrase candidates. Within each group, candidates are sorted by a continuous acoustic splice cost combining local alignment cost, duration strain, and spectral-envelope mismatch at both joins. Lower cost is preferred, with candidate position breaking an exact tie. This cost is a deterministic signal-processing proxy for join compatibility, not a calibrated probability of an audible defect. It is used only to define donor preference; no separate risk buckets are submitted or scored. Training Distribution The 3,600 training cases contain 713 distinct complete donor permutations. The preferred donor is balanced across candidate positions: | First donor | A | B | C | D | E | F | |---|---:|---:|---:|---:|---:|---:| | Training cases | 615 | 589 | 612 | 634 | 551 | 599 | Damage widths also cover their complete seven-value range: | Width in bins | 8 | 9 | 10 | 11 | 12 | 13 | 14 | |---|---:|---:|---:|---:|---:|---:|---:| | Training cases | 502 | 537 | 518 | 510 | 549 | 482 | 502 | Mapped donor spans range from 1 through 38 bins in the training data. Evaluation Submissions are scored by the Technical Phrase Restoration Score, which has three components. DamageIntervalScore For half-open intervals T and P, interval IoU is the intersection length divided by the union length. The per-case score is: interval_row = 0.70 * exact_interval_match + 0.30 * IoU(T, P) DamageIntervalScore = mean(interval_row) DonorOrderScore Let the hidden permutation assign relevance 6 to its first label, 5 to its second, down to 1 for its last. For submitted position k, starting at 1: DCG = sum_k (2 ^ relevance[predicted_label_k] - 1) / log2(k + 1) nDCG = DCG / DCG_of_hidden_order ranking_row = 0.72 * exact_permutation_match + 0.28 * nDCG DonorOrderScore = mean(ranking_row) ReplacementSpanScore Compute interval IoU separately for all six rows of the submitted and hidden matrices. span_row = 0.74 * exact_matrix_match + 0.26 * mean_donor_IoU ReplacementSpanScore = mean(span_row) Final Score Score = (24 * DamageIntervalScore + 29 * DonorOrderScore + 31 * ReplacementSpanScore) / 84. The normalized weights are 24/84, 29/84, and 31/84. Span mapping receives the largest share because a useful donor still fails to repair the phrase when the replacement boundaries are wrong. Donor choice receives the next largest share because spoken content must agree; localization remains necessary but does not itself identify a usable replacement. These are fixed evaluation-policy weights, not measured editing costs. A malformed value receives zero for its component. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Submission Format Write the final file to ./working/submission.csv. It must contain exactly these columns in this order: | Column | Required format | Maximum serialized length | |---|---|---:| | case_id | Unchanged test identifier. | 64 characters | | damaged_interval | JSON array of two integers from 0 through 63 with increasing endpoints. | 24 characters | | donor_preference | Each of A through F exactly once, joined by >. | 11 characters | | replacement_span_matrix | JSON 6 by 2 integer matrix with valid increasing intervals. | 96 characters | A valid row is: | case_id | damaged_interval | donor_preference | replacement_span_matrix | |---|---|---|---| | case_004636766ad552147c57ef | [26,39] | E>B>A>F>D>C | [[16,23],[22,38],[31,44],[28,40],[13,29],[36,47]] | The example is a labeled training record. In a submission, use the actual test IDs instead. The grader rejects extra or reordered columns, duplicate IDs, missing or additional rows, unknown IDs, and malformed case identifiers before scoring. What Makes This Interesting This is neither speech recognition nor waveform inpainting. The requested artifact is a donor-and-span repair certificate: the model must discover phrase equivalence across unseen speakers and instructions, localize a defect, align variable speaking rates, and judge whether an otherwise correct donor will create an audible join. The six-way ranking deliberately separates semantic repairability from signal cleanliness. Because speaker and instruction families are held out before packet construction, a model cannot solve test cases by memorizing a voice, phrase class, or source recording. Strong solutions can learn a content-sensitive audio representation and use cross-attention or differentiable alignment to connect primary and donor timelines. Relation To Existing Speech Tasks [Shan and Tsai's cross-verification method aligns a questionable recording with a trusted reference and classifies frames as matching or non-matching. That is a relevant starting point for detecting the damaged interval here. It does not by itself decide which of several different speakers supplies the preferred replacement or return intervals for all six candidates. SpeechPainter fills speech gaps using accompanying text, while EditSpeech performs text-directed waveform edits. This challenge supplies neither a transcript nor a trusted donor and does not grade a synthesized waveform. Its operational question is which existing recording to borrow from and where to cut it. Content agreement must be separated from boundary compatibility: a smooth-sounding wrong instruction remains an unsuitable repair. The evaluation keeps these failures distinct. Correct damage localization alone does not earn donor-order or replacement-span credit; correct phrase retrieval does not supply the six time mappings; accurate time mappings do not establish phrase compatibility. The novelty being proposed is this transcript-free donor-selection and alignment setup under joint speaker/script holdouts, not a new alignment algorithm or the use of CSV outputs. Existing verification, retrieval, and editing methods remain legitimate building blocks for a solution. Splice costs are reproducible acoustic proxies, not listener-validated judgments of naturalness. What Not To Use Use only the supplied public CSV files and speech packets. Do not infer labels from case IDs, packet names, row order, external source filenames, or source-archive lookup. Do not seek private answers or exploit grader behavior. These shortcuts bypass the intended cross-speaker phrase comparison and temporal restoration problem. &nbsp;
> $700 Pool
> Closes in 11h 20m
> 7 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## NeuroWeave Branch Reattachment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c8fa95d0wdvqbh4e7y1g01d8e385f
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.674!

Full challenge description from page:

> NeuroWeave Branch Reattachment Overview Recover which disconnected dendritic branch belongs to an incomplete mouse-neuron morphology. Every query contains one observed 3D morphology anchor and 12 candidate distal branches. Exactly one candidate is the authentic held-out continuation; the other 11 are hard morphometric decoys drawn from different whole-brain specimens in the same split role. Each anchor and each candidate is independently placed in an unknown rigid coordinate frame. Valid points are independently shuffled, so array order is not a tree traversal and the attachment interface is not fixed at index 0. Small deterministic measurement corruption is applied independently to every fragment: 8% point dropout, coordinate jitter with standard deviation 0.012, radius jitter with standard deviation 0.050, depth jitter with standard deviation 0.008, and an 8% child-degree perturbation rate. Absolute brain position, source neuron identity, source specimen identity, source filenames, and original node identifiers are absent. A successful model must learn noise-robust relationships among radius continuity, branching topology, spatial scale, and local morphometric style. This is a structured 3D point-cloud retrieval task, not tabular classification or regression. Train and test are disjoint by whole-brain specimen: 83 source brains contribute 12,041 training queries and a different 23 source brains contribute 3,400 test queries. The verified source-group overlap is zero. Evaluation Submit a complete ordering of the 12 candidate tokens for every test query. Let r be the one-based rank of the authentic held-out branch. The per-query Strict Branch Reattachment Utility is: w = 1 / log2(13) u(r) = ((1 / log2(r + 1)) - w) / (1 - w) The final score is the arithmetic mean of u(r) across all 3,400 test queries. Higher is better. Rank 1 scores 1.0, rank 2 approximately 0.4943, rank 3 approximately 0.3148, and rank 12 0.0. The expected score of a uniformly random rank is approximately 0.2112. A content-invalid row also scores 0.0. The scorer merges rows on id; submission row order never affects the score. Missing, duplicate, or foreign ids and missing, renamed, or extra columns raise a clean ValueError. A missing ranking, an overlong cell, an unknown candidate token, a repeated token, an incomplete ranking, or any other out-of-range ranking content receives worst utility for that row. Every valid grading path returns a finite score in [0,1]. Reference implementation of the row utility: import math def branch_reattachment_utility(rank): if rank not in range(1, 13): return 0.0 worst_valid = 1.0 / math.log2(13.0) reciprocal_log = 1.0 / math.log2(rank + 1.0) return (reciprocal_log - worst_valid) / (1.0 - worst_valid) Dataset All participant-visible files are under ./dataset/public/. train.csv — 12,041 rows with id, array_index, candidate_tokens, and target_candidate. test.csv — 3,400 rows with id, array_index, and candidate_tokens. train_morphologies.npz — fixed-shape training tensors. test_morphologies.npz — fixed-shape test tensors. sample_submission.csv — label-free candidate-order baseline with the exact submission schema. The NPZ files contain four arrays. anchors (float16) — shape (rows, 128, 6). anchor_masks (uint8) — shape (rows, 128), where one marks a real point and zero marks padding. candidates (float16) — shape (rows, 12, 64, 6); candidate axis order matches candidate_tokens. candidate_masks (uint8) — shape (rows, 12, 64). Each point has six channels. Channels 0–2 — translated, independently rotated, scaled, lightly jittered, and clipped relative 3D coordinates. Channel 3 — transformed node radius with independent measurement jitter. Channel 4 — capped child-degree feature with sparse deterministic perturbations. Channel 5 — relative tree-depth feature with independent measurement jitter. array_index selects the first NPZ axis. Masks identify retained points after deterministic 8% dropout. Valid point order is independently randomized for every anchor and candidate and must not be interpreted as DFS, BFS, path, parent, or temporal order. Query ids and candidate tokens are randomized opaque strings with no source, group, position, label, or difficulty information. Submission Write ./working/submission.csv with exactly two columns in this order: id, ranking. It must contain exactly 3,400 rows, one per test id. ranking is a single space-separated permutation of all 12 tokens listed in that query's candidate_tokens field, best candidate first. Example using a real test id and its label-free listed order: id,ranking q_c927ff6b4af17d169e67,b_a737101c0cab1e78 b_685e5ac9e7c88e7b b_14d7381e87ee2472 b_bb2a38807499be8f b_b7b1c1567f42af0a b_8659e8516ae5769a b_06d19abfdd78bb79 b_b7ecb7f01c161efc b_5b4da97df24046b0 b_b70cd93f3722f373 b_998e0c8d21dac245 b_ca0b037ab7a44270 Requirements Finish within 5,400 seconds. Train only on the supplied training tensors and labels. Treat valid points as unordered sets and build robustness to the documented measurement corruption. Produce exactly the required header and 3,400 unique test ids. Rank every allowed token exactly once for each row. Keep all output cells finite and bounded in size. Read only from ./dataset/public/ and write only ./working/submission.csv. What not to use Do not use pretrained weights, external datasets, internet downloads, source-record lookups, or manually curated neuroscience atlases. Do not reverse-engineer deterministic identifiers, source filenames, or preparation internals. Do not hard-code test rankings or copy training targets into unrelated rows. Extra Modelling Information NeuroWeave mechanism is a retrieval of an authentic removed tree branch from hard cross-specimen decoys after every fragment loses its shared rigid frame. It evaluates learned intrinsic compatibility rather than voxel segmentation, cell-type prediction, coordinate registration, or direct continuation in a common frame. The source Scientific Data paper presents these morphologies as a resource for segmentation, bouton detection, tracing, and cross-scale morphology analysis. It does not define branch-fragment reattachment, candidate ranking, specimen-held-out retrieval, or independent-frame matching.
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Prerequisite Annotation Dialect Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7124fbz2p77bsvn7vgyzqjmd8e3sj2
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shivam_s's score of 91.660!

Full challenge description from page:

> Overview Prerequisite Annotation Dialect Induction is a GPU-native graph-and-language meta-learning challenge over educational and technical concept graphs. The task is not to predict whether a prerequisite relation exists in isolation. Instead, each sample asks the model to infer a local annotation policy from a small set of demonstrations and then apply that policy to a new graph fragment. Every sample contains two parts. The first part is a support set drawn from one hidden graph domain. Each support example shows a local prerequisite fragment together with several transitively implied candidate relations and identifies which of those relations were explicitly authored as direct prerequisite edges. The second part is a target fragment from the same hidden domain. Several direct prerequisite relations have been masked. Eight candidate completion bundles, C01 through C08, are provided. Exactly one completion reproduces the original authored target fragment. All eight target completions are deliberately constructed to preserve the same relevant reachability behavior. They are therefore indistinguishable by transitive closure, weak connectivity, and the released graph-query shadow. The model must use the support demonstrations to infer how this particular domain tends to encode semantically meaningful direct prerequisites and then transfer that inferred annotation policy to the target fragment. The benchmark is therefore episodic. A sample does not merely ask: "Which edge is likely?" It asks: "Given several examples of how this hidden curriculum chooses to represent redundant prerequisite relations, which graph realization is consistent with the same annotation dialect?" The submission predicts one completion code per sample. Research Objective Concept-prerequisite prediction is usually formulated as binary or pairwise relation prediction. A model receives concept representations, graph structure, or course dependencies and estimates whether one concept is a prerequisite of another. This benchmark changes both the unit of prediction and the source of supervision. The prediction unit is a complete graph realization rather than one edge. The supervision is local and episodic rather than only global. The hidden object is an annotation policy that governs which logically redundant prerequisite relations are explicitly retained. For a directed prerequisite graph G, let TC(G) denote its transitive closure. If two graph realizations have the same transitive closure, then they agree on every pure reachability statement. However, educational and technical graphs often contain direct edges that are already implied by longer paths. Such edges can still carry representational meaning. An author may preserve a direct relation because it expresses an immediate pedagogical dependency, highlights a foundational concept, crosses an important taxonomy boundary, or reflects a domain-specific preference for dense or sparse annotation. Different domains can express these preferences differently. The benchmark treats those preferences as a prerequisite annotation dialect. A support set demonstrates that dialect through concrete local decisions. The model must infer the latent policy from those examples and use it to rank target completions that are otherwise structurally equivalent under reachability. This makes the benchmark a conditional graph-realization problem rather than a static concept-prerequisite classifier. Episodic Structure Each row is one self-contained episode. A row contains: sample_id; development_fold; support_set; target_nodes; target_visible_edges; completion_candidates; query_shadow. All structured fields are serialized as JSON inside the CSV. No original domain name is exposed. Node identifiers are reassigned independently inside each episode. The model is expected to infer the relevant domain-local graph style from the support set itself. Support Set The support set contains between four and eight calibration examples from the same hidden graph domain as the target. Each support example contains: a local node set; visible prerequisite edges; a small set of transitively implied candidate relations; a binary authored-status label for each candidate relation; taxonomy tokens where available; coarse structural features. A support candidate is only included if its endpoints are already connected by an alternate prerequisite path. Therefore, every support relation is logically compatible with the same reachability graph whether or not the direct edge is explicitly present. The support label answers a narrower question: "Did the source graph explicitly encode this relation as a direct prerequisite?" This distinction is central to the challenge. The support set is not a collection of arbitrary positive and negative edges. Both authored and omitted support relations must be transitively implied. This prevents trivial learning of prerequisite existence from reachability alone. Support examples are sampled from graph regions that do not overlap the target fragment. The target hidden edges are never included directly in the support set. Annotation Dialect The term "annotation dialect" refers to recurring local tendencies in how a graph domain chooses to materialize redundant but semantically meaningful prerequisite edges. Examples of learnable tendencies include: whether highly foundational concepts are repeatedly attached directly to advanced descendants; whether direct edges are favored within the same taxonomy or across taxonomies; whether semantically close concepts are more likely to receive explicit shortcuts; whether shortcuts are concentrated at particular alternate-path lengths; whether the graph emphasizes immediate technical dependencies even when a longer path exists; whether hubs are linked directly to many downstream concepts; whether similar semantic motifs are represented sparsely or densely. The benchmark does not expose a handcrafted dialect label. There is no target such as dense, sparse, or cross_taxonomy. The latent policy must be inferred from support demonstrations. Two episodes can contain structurally similar target fragments but different support sets from different graph domains. A strong model should be capable of changing its preference when the demonstrated annotation policy changes. This is the intended meta-learning pressure. Target Fragment The target fragment contains approximately 32 to 96 nodes. Each node card contains: opaque local node ID; concept label; taxonomy token when available; visible in-degree; visible out-degree; root or leaf indicators in the masked fragment; coarse component role; optional query-mention count derived from public source queries. The target graph contains all visible prerequisite edges after masking. Edge direction is always from prerequisite concept to dependent concept. Several direct relations are hidden simultaneously. The hidden relations are selected from authored edges that can be removed without changing the required reachability relation of the public fragment. This ensures that the missing direct edges are not recoverable merely by asking which node pairs must remain connected. Completion Candidates Every target provides exactly eight completion bundles: C01,C02,C03,C04,C05,C06,C07,C08. Each bundle contains the same number of directed edges. Exactly one bundle restores the original authored target fragment. The remaining seven are hard alternative realizations. For acyclic fragments, every candidate edge must already be transitively implied by the visible graph or by another edge in the same candidate bundle. For cyclic fragments, candidate generation preserves the intended strongly connected component structure and condensation-level reachability. Candidate codes are randomly permuted per row. The code C05, for example, has no persistent meaning across samples. Reachability Equivalence The defining construction requirement is that target candidates are equivalent under the released reachability semantics. For every candidate completion, preparation reconstructs the completed target graph and performs an explicit audit. For DAG_SHORTCUT episodes, all eight candidate completions must have: identical transitive closure over the public target nodes; identical weakly connected components; preserved acyclicity; identical answers to every public reachability probe in query_shadow; equal completion-bundle size. For SCC_REALIZATION episodes, all candidates must additionally preserve: the same strongly connected component partition; the same condensation graph; the same condensation-level reachability; the same public SCC-level query-shadow observations. A sample is rejected if any of these invariants fail. The preparation pipeline should compute these checks directly rather than infer them from heuristics. Structural Candidate Matching Reachability equivalence alone is not sufficient because one candidate might still have an obvious structural fingerprint. After the hard equivalence audit, the generator performs candidate matching. Candidate bundles are compared on public or easily reconstructed statistics including: alternate-path-length histogram; source endpoint degree bands; target endpoint degree bands; same-taxonomy and cross-taxonomy edge counts; root and leaf interaction counts; endpoint component roles; hub participation; visible two-hop neighborhood signatures. The objective is not to make every candidate identical under every graph statistic. The benchmark makes a narrower and testable promise: the candidates are exactly equivalent under the released reachability semantics and are matched closely enough on common structural shortcuts that a topology-only predictor should remain weak. Samples with one candidate that is uniquely identifiable from simple structural summaries are rejected. Support-Target Separation Support examples and target fragments come from the same hidden source domain but from disjoint local graph regions. The generator prevents direct leakage by enforcing: no shared hidden edge; no shared masked node pair; no identical local fragment; no target candidate relation appearing as a labeled support relation; no stable source identifier; no source-domain name. Concept labels may recur because semantic transfer is intentional. The model must use support examples as evidence about annotation style rather than as a direct lookup table for target edges. Query Shadow query_shadow contains a compact family of graph observations that are guaranteed to be identical under all eight target completions. It may include: selected reachability pairs; ancestor-count bands; descendant-count bands; weak-component membership checks; taxonomy-conditioned reachability checks; SCC and condensation-level checks where relevant. The query shadow makes the ambiguity auditable. A participant can verify that the candidate completions agree on the released query family. The query shadow is not an additional prediction target. Construction Regimes Preparation uses two private construction regimes. They are generation metadata, not public participant features and not prediction targets. DAG_SHORTCUT is used internally for acyclic prerequisite regions. Candidate differences consist of direct edges that are redundant under transitive reachability. SCC_REALIZATION is used internally for fragments intersecting cyclic regions. Candidate differences preserve the strongly connected component partition and condensation-level reachability while changing the direct authored realization. Both regimes use the same public completion-label space and submission format. The private answers.csv may retain the construction regime for grading audits and release diagnostics. Train and Evaluation Split The official split is domain-disjoint. All episodes derived from one graph domain remain on the same side. Evaluation domains are not used to construct training episodes. This is important because the benchmark is intended to test adaptation to a new annotation dialect rather than memorization of one domain's direct-edge patterns. Every evaluation episode still contains support demonstrations from its own held-out domain. The model is therefore allowed to adapt to the new domain through the support set while remaining unable to train globally on that domain. The public development_fold field provides a grouped local validation protocol. Recommended development uses: all rows where development_fold != F0 for fitting; rows where development_fold == F0 for validation. Episodes derived from overlapping graph regions remain in the same development fold. The default challenge targets: 3,000 training episodes; 750 evaluation episodes. Preparation fails rather than duplicating identical episodes merely to reach the requested count. Submission Contract Use sample_submission.csv exactly. The submission contains exactly two columns: sample_id,completion_id sample_submission.csv contains the exact evaluation sample_id sequence and the same two submission columns projected from the private answer table. The private answers.csv may contain additional grading-only fields such as candidate edge bundles, gold edge bundles, construction regime, and private source-domain metadata. Those extra columns are not part of the participant submission schema. completion_id must be one of: C01,C02,C03,C04,C05,C06,C07,C08. Every expected sample_id must appear exactly once. Missing rows, extra rows, duplicate IDs, blank predictions, unknown completion codes, missing columns, extra columns, or incorrect column order receive the evaluator floor. Evaluation The primary objective is exact recovery of the authored target realization. Let E denote exact completion accuracy. Candidate bundles can share individual hidden edges, so the evaluator also grants bounded structural credit. For predicted edge bundle P and gold bundle G, define directed-edge overlap F1 as: F_edge = 2 * |P intersection G| / (|P| + |G|). Let O denote mean directed-edge overlap across evaluation episodes. The final score is: Score = 100 * (0.70E + 0.30O). Scores are clipped to the interval [0.01,100]. A perfect submission receives exactly 100.0. The weight on exact completion is larger because the main target is the domain-consistent authored realization, not independent recovery of individual edges. The overlap term preserves ranking resolution when a model selects a near-miss candidate containing several correct direct relations. These coefficients are fixed benchmark-design constants and are not tuned on private evaluation data. Evaluation is fully deterministic. There is no LLM judge, embedding service, remote API, or manual scoring. Why the Support Set Matters to Evaluation A static global link predictor can still learn that some semantic prerequisite relations are common across training domains. That is an acceptable baseline, but it does not fully solve the benchmark. The intended advantage comes from conditioning on the support demonstrations. Evaluation should therefore include diagnostic analysis comparing: full support-conditioned models; the same model with support examples removed; the same model with support examples randomly replaced by demonstrations from another domain; topology-only models; global semantic link predictors. A valid challenge release should show a measurable gap between correctly conditioned and support-ablated systems. If replacing the support set has no effect, the episodic construction is not doing useful work and should be revised. Compute Environment The execution environment provides: one NVIDIA A10G GPU; 24 GB GPU memory; host CPU and system memory; a 90-minute end-to-end runtime limit. The runtime includes: CSV and JSON parsing; graph construction; text tokenization; support-set encoding; neural model fitting or adaptation; graph batching; target-candidate scoring; inference; submission writing. There are no images. Machine-Learning Requirement This is a learned graph-and-language meta-learning challenge. Final candidate ranking must materially depend on trainable neural parameters fitted or calibrated from the released training episodes. The following are not valid primary solution systems: TF-IDF; BM25; bag-of-words matching; raw lexical similarity as the decisive predictor; deterministic transitive closure as the complete solver; deterministic transitive reduction as the complete solver; degree-only ranking; taxonomy-only ranking; manually authored shortcut rules; logistic regression; SVM; nearest-neighbor classification; random forests; gradient-boosted trees; similar classical statistical models as the decisive final predictor. Graph algorithms are allowed for preprocessing, legality checking, and feature construction. Participants may compute features such as: transitive-reduction backbones; alternate path lengths; SCC condensation graphs; degree statistics; local motif counts; candidate legality masks. However, a neural model must remain materially responsible for learning how the support demonstrations modify candidate preference. Remote model APIs are not allowed. Modeling Direction A strong solution can be implemented as an episodic graph-language ranker. One practical design is: encode support and target concept labels with a compact pretrained transformer; initialize graph nodes with semantic embeddings plus taxonomy and structural features; propagate information through each support fragment and the target visible graph using a GNN or graph transformer; encode each labeled support relation as an authored or omitted directness example; aggregate support examples into a latent domain-policy representation; condition target candidate-edge representations on that policy embedding; aggregate edge scores into candidate-bundle scores; train with eight-way candidate-ranking loss plus optional support-contrastive objectives. The support-policy representation can be implemented through: attention pooling; a set transformer; a recurrent meta-encoder; prototype aggregation; cross-attention between support relations and target candidate edges. Useful model families include: graph transformers; relational GNNs; graph attention networks; text-initialized message-passing networks; candidate-conditioned cross-encoders; episodic meta-learning networks; set transformers; neural matching networks over graph relations. A practical A10G solution can cache concept-label embeddings, batch episodes by target graph size, use mixed precision, and train lightweight graph and meta-conditioning layers on top of a frozen or partially frozen text encoder. Expected Failure Modes Static CPR behavior. The model ignores the support set and applies one global prerequisite-edge classifier to every evaluation domain. It can learn transferable semantics but cannot adapt to a domain whose annotation style differs from the training average. Reachability shortcut. The solver expects a transitive-closure or path algorithm to identify the gold completion. All candidates satisfy the same released reachability semantics. Support memorization. The model searches for the exact target node pair inside the support examples. Support-target separation prevents this direct lookup. Wrong-domain conditioning. The model extracts generic statistics from the support set but does not learn how they should change candidate preferences. Support-swap diagnostics should reveal this failure. Lexical nearest pair. The model chooses the completion with the most semantically similar endpoint labels. Hard candidates contain plausible semantic alternatives and are matched structurally. Topology fingerprinting. The model exploits degree or alternate-path anomalies. Candidate matching and release-time topology-only baselines are designed to suppress this shortcut. Independent-edge scoring. The model ranks every candidate edge independently without representing the local annotation policy or bundle-level consistency. Domain memorization. The model learns graph-specific conventions from training domains. Official evaluation domains are held out. Release Validation Before publishing the evaluation set, preparation should emit a private audit summary covering: reachability-equivalence pass rate; SCC-equivalence pass rate; candidate structural-match statistics; support-target overlap checks; candidate-code balance; graph-mode balance; completion-bundle-size distribution; topology-only baseline accuracy; support-ablated neural baseline accuracy; support-swapped neural baseline accuracy. The purpose of this audit is to make the benchmark claim falsifiable. The release is only interesting if three statements are simultaneously true: graph algorithms cannot distinguish the eight target realizations under the declared public semantics; global structure or lexical shortcuts do not trivially reveal the answer; same-domain support demonstrations provide learnable information about the target realization. Research Thesis The benchmark asks: Can a graph-language model infer how an unseen domain chooses to explicitly annotate logically redundant prerequisite relations, then apply that inferred policy to a new reachability-equivalent graph completion problem? The key object is not an isolated prerequisite relation. It is a domain-conditioned representation policy. Classical graph algorithms determine what is logically implied. Global concept-prerequisite models estimate what relations are generally plausible. This benchmark requires a third capability: infer from a handful of demonstrations which plausible, already-implied relations this particular hidden domain chooses to encode directly. The final objective is: support demonstrations, hidden annotation dialect, target fragment, eight reachability-equivalent completions, one domain-consistent authored realization
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Robust Budgeted Diagnostic Policy Induction under Noisy Logical Measurements

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fs91bhqj9tb5mh6pfebg68x8e2xj0
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ravi56's score of 64.910!

Full challenge description from page:

> Overview Robust Budgeted Diagnostic Policy Induction under Noisy Logical Measurements is a GPU-native active-reasoning challenge over symbolic environments, competing logical hypotheses, adaptive diagnostic measurements, controlled observation noise, paired equivalent validator views, and board-level resource allocation. Every board contains four independent logical cases. Each case exposes eight plausible rule hypotheses, two independently anonymized validator views of the same underlying symbolic environment, a finite diagnostic probe library, eight candidate adaptive policies, and eight local regret cards. The task is not to choose one informative probe. A policy is a shallow conditional decision tree: it chooses an initial diagnostic measurement, branches on the observed response, optionally chooses second and third measurements, and terminates in a hypothesis decision. The diagnostic responses are not assumed to be perfectly reliable. Every public probe belongs to a controlled noise family and exposes a reliability profile. Examples include symmetric response flips, asymmetric false-positive/false-negative channels, abstention-like missing responses, and low-rate branch confusion. The underlying latent rule is deterministic; only the measurement channel is noisy. A policy must therefore be useful not only when every probe response is exact, but across several known observation channels. Preparation evaluates candidate trees under a fixed public family of noise scenarios and prefers policies that preserve diagnostic quality when a locally attractive probe becomes unreliable. For each case, predict four coupled targets: case_i_policy: the selected adaptive policy route; case_i_terminal: the shared terminal-hypothesis route; case_i_critical: the shared critical-probe route; case_i_regret: the local regret-profile route. The four cases on a board share one public diagnostic budget. Policy costs therefore interact across cases. A locally attractive policy can be globally suboptimal if its cost prevents stronger diagnostic plans elsewhere on the board. The latent chain is: ambiguous hypothesis set → adaptive diagnostic policy → terminal hypothesis → critical probe → regret under a greedy alternative and the board adds: four local policies → one shared budget → one globally admissible allocation. Problem Research The benchmark studies active logical diagnosis under resource-coupled experiment design. Most logical benchmarks are passive: the observation set is fixed and the model predicts an answer. Falsification-style tasks add an active component by asking which test would best challenge a hypothesis. Here, the scored object is a complete conditional acquisition policy rather than one test. Let: H = {h1,...,h8} be the eight candidate hypotheses for one case, and let: Q = {q1,...,qm} be the available diagnostic probes. Every probe partitions the current hypothesis set according to the response each candidate rule would produce. A complete policy recursively refines these partitions. A first probe can create a balanced immediate split yet leave one branch difficult to resolve. Another probe can look weaker initially but lead to shallower and cheaper downstream branches. For this reason, preparation evaluates complete decision trees rather than one-step information gain alone. Each policy is scored privately by robust diagnostic quantities including: unresolved terminal mass under supported noise scenarios; terminal error probability; worst-case diagnostic depth; expected diagnostic depth; total probe cost. The public policy card exposes the policy tree, its maximum depth, and its total probe cost. It does not expose the private semantic utility used during board construction. The board itself is a small diagnostic portfolio. If the four selected policies are pi_1,...,pi_4, then they must satisfy: cost(pi_1) + cost(pi_2) + cost(pi_3) + cost(pi_4) <= board_budget. Several complete policy tuples remain budget-feasible. The budget is intended to create genuine opportunity cost rather than uniquely reveal the answer. The generator searches for boards where the independently preferred local policies are not all jointly affordable when possible, so the final selection depends on both case-level diagnostic quality and cross-case resource allocation. The paired validator views are also part of the reasoning setup. Views A and B contain independently anonymized versions of the same canonical symbolic environment. They use different entity aliases and different public statement orderings. Their role is to suppress identifier-specific shortcuts and encourage semantic reasoning over the logical structure. The current benchmark does not score an explicit A/B robustness term; instead, both views are released as equivalent evidence channels for the learned model. The critical-probe target measures conditional necessity. For the selected policy, preparation removes each used probe in turn and re-optimizes the remaining decision tree. The probe whose removal causes the largest deterioration is the gold critical probe. It is not necessarily the first probe, the most expensive probe, or the probe with the strongest immediate split. The regret target measures myopic planning failure. Preparation identifies a strong greedy first action based on immediate partition quality, forces that action at the root, and recomputes the best continuation. The resulting regret card summarizes how that greedy tree differs from the selected policy through fields such as worst-case depth increase, expected-depth increase, unresolved leaves, extra cost, and branch imbalance. These mechanics make the task different from simple test selection. The benchmark evaluates a portfolio of conditional diagnostic policies, the hypotheses they diagnose, the measurements that are indispensable to those policies, and the cost of choosing locally tempting but globally inferior diagnostic actions. Additional Research Framing A useful way to interpret one case is as a compact experiment-design problem over a finite version space. The eight rule hypotheses are not merely eight class labels. They represent eight different explanations of the same public evidence, and the policy tree describes how additional measurements would progressively separate those explanations. This matters because an adaptive tree can only be evaluated by considering the consequences of its future branches. A probe that appears weak at the root can become valuable if it creates branches that are cheap to finish. Likewise, an apparently strong probe can be globally poor when one rare response leaves a difficult residual hypothesis set. The benchmark therefore rewards systems that represent future diagnostic consequences rather than only immediate relevance. The shared board budget adds a second kind of dependency. The utility of one case-level policy depends partly on the alternative policies available elsewhere on the board. In this sense, the board behaves like a small resource-constrained design problem: the model must trade a marginal improvement in one experiment against the opportunity to make a larger improvement in another. This is why exact budget-aware decoding is allowed after neural scoring. The combinatorial decoder enforces legality, while the learned model is responsible for estimating the semantic value of the candidate policies. The terminal, critical, and regret targets expose different projections of the same diagnostic mechanism. Terminal prediction asks what concept the policy is trying to isolate. Critical-probe prediction asks which measurement is structurally indispensable once replanning is allowed. Regret prediction asks why a tempting greedy root action can still lead to an inferior tree. A model that truly understands the experiment plan should therefore perform well across all four targets, while a shortcut that only recognizes the terminal rule should fail on the planning-specific supervision. The paired A/B validators provide a weak form of representation stress testing. Because both views encode the same canonical symbolic environment under independent anonymization and ordering, a model that relies heavily on brittle identifier morphology should lose signal. The challenge does not require explicit graph alignment, but the duplicated semantic evidence gives learned systems an opportunity to build representations that are less sensitive to one arbitrary surface encoding. The intended empirical story is therefore not that one architectural component is uniquely necessary. Instead, the benchmark creates several measurable pressure points: greedy probe scoring should underperform complete policy scoring; independent per-case policy selection should underperform budget-aware board decoding; terminal-only systems should lag models trained jointly on policy, critical, and regret supervision; systems that use both validator views should be more robust than systems that rely on one encoding alone; classical lexical or frequency baselines should remain substantially below learned neural systems. These comparisons make the challenge falsifiable. If a cheap baseline solves the policies from tree shape or cost alone, the construction has leaked. If the board budget never changes a preferred policy tuple, the resource-coupling mechanism has collapsed. If terminal prediction alone reaches the same score as a full multi-target model, the planning supervision is not contributing enough. The preparation and validation process should therefore treat shortcut analysis as part of benchmark quality control rather than as an afterthought. Robust Diagnostic Channels The additional research axis is robust adaptive experiment design under controlled measurement noise. In the deterministic version of a diagnostic tree, each probe partitions the hypothesis set into exact response classes. Under noisy measurement, the same probe induces a distribution over observed responses. For hypothesis h and probe q, preparation privately defines a latent response: z = response(h,q) and a public noise channel: C_q(y | z), which gives the probability of observing response y when the latent response is z. The challenge does not ask participants to estimate arbitrary unknown noise. Probe cards expose a compact reliability profile derived from a small stable noise vocabulary. The model must learn how reliability interacts with logical discrimination. A probe with a perfect deterministic split can be a poor root action when its strongest branch is measured through a noisy channel. Conversely, a slightly weaker split can become preferable when its responses are substantially more reliable. Candidate policy quality is therefore evaluated under several controlled channel conditions rather than one noiseless execution. Preparation computes robust quantities such as: expected unresolved hypothesis mass under the public noise scenarios; worst-case diagnostic depth over supported channel families; expected diagnostic depth after noisy branching; probability of reaching an incorrect terminal leaf under the channel model; total probe cost. The current submission schema does not add a new noise target. Noise affects which P01P08 policy is correct, which probe becomes critical, and which regret profile is induced. Noise Families Probe reliability comes from a stable categorical vocabulary. Representative channel families are: CLEAN: deterministic response; SYMMETRIC_LOW: low-probability response flip; ASYMMETRIC_POS: positive-like responses are less reliable than negative-like responses; ASYMMETRIC_NEG: negative-like responses are less reliable; ABSTAIN_LOW: the probe can emit an explicit unknown response with low probability; BRANCH_CONFUSION: neighboring ordinal response bands can be confused. Exact numeric channel parameters are public in the probe card through compact probability bands or a small confusion table. The same logical probe can therefore appear with different reliability profiles across cases. Robust Policy Objective A policy is not considered strong merely because it is optimal under the clean channel. Preparation evaluates every candidate tree across the public noise scenario set. The preferred policy minimizes unresolved hypotheses and diagnostic error before trading off depth and cost. One conceptual ordering is: minimize worst-case unresolved terminal mass; minimize worst-case terminal error probability; minimize robust worst-case depth; minimize expected depth; minimize total cost. The exact policy card remains finite and categorical. Participants select among eight supplied trees rather than generate a stochastic control program. This changes the interpretation of the shared board budget. A cheap but noisy probe can consume little budget while producing high diagnostic risk. An expensive reliable probe can be locally attractive yet crowd out reliable experiments on other cases. The board therefore couples semantic utility, measurement reliability, and resource cost. Noise-Aware Critical Probe Critical-probe supervision is also noise-aware. Preparation removes each probe used by the selected tree, then re-optimizes the remaining policy under the same noise family. The critical probe is the removal that most degrades the robust diagnostic objective. This can differ sharply from deterministic importance. A probe may be critical because it is the only reliable measurement available on one difficult branch, even if its clean information gain is modest. Noise-Aware Regret The regret target compares the selected robust policy with a greedy alternative chosen from immediate clean or expected partition quality. The strongest greedy action can fail for two distinct reasons: it creates expensive downstream branches; it relies on an unreliable measurement channel. Regret cards therefore capture consequences of both myopic planning and reliability blindness without adding another submission head. Why This Is a Different Research Object The closest diagnostic-policy and falsification benchmarks usually assume either deterministic test outcomes or optimize expected cost under a single known diagnosis model. Here, the model must choose among complete finite policy trees whose relative value changes across controlled response-noise families, while four cases compete for one shared budget and two equivalent validator views suppress representation-specific shortcuts. This creates a joint problem of: logical hypothesis discrimination + adaptive policy planning + measurement-channel robustness + cross-case resource allocation. A clean-policy baseline, a cost-only baseline, and a noise-ignorant tree scorer should therefore fail for different reasons. The benchmark is explicitly constructed to make these ablations measurable. Public Data and Candidate Structure The public feature columns are: sample_id; development_fold; predicate_lexicon; board_budget; case_1; case_2; case_3; case_4; terminal_bank; critical_probe_bank. Each case_i is JSON encoded inside the CSV cell. A case contains: validator view A; validator view B; labeled support examples; eight hypothesis cards; a diagnostic probe library; eight adaptive policy candidates; eight local regret candidates. The public validator views are bounded symbolic excerpts rather than the complete raw source environment. They contain enough facts to support the challenge while keeping the released CSV practical to load and train on. Original source identifiers are not exposed. Predicate names are rebound to a board-local opaque vocabulary such as V03, V08, and V14. The mapping changes independently from board to board. Predicate arity remains public. Rule hypotheses use R01 through R08. They are structurally related candidate rules produced by controlled mutations such as same-arity predicate substitution, argument exchange, and variable rebinding. The gold hypothesis is not submitted directly as one of these local R codes. Instead, independently rendered hypothesis cards are shuffled into the shared terminal bank. Diagnostic probes are finite measurements over candidate-rule structure and validator support. Probe families can include measurements such as: slot fact-support bands; slot entity-support bands; slot neighborhood bands; slot argument classes; slot predicate classes; example-neighborhood measurements; total fact-support summaries; minimum fact-support summaries; unique-entity support summaries. The exact probe library is public in each case. The private candidate-response partitions used to build policy trees are not directly exposed. Policy routes use P01 through P08. Each public policy card contains: the conditional decision tree; maximum_depth; probe_cost_total. The tree has depth at most three. Terminal routes use H01 through H08 and refer to entries in the shared terminal_bank. For each case, exactly one H-code is the correct terminal-hypothesis route. All eight H-codes are valid candidates for every case. The four case-level gold H-codes are guaranteed to be distinct by construction, so the four submitted terminal routes must also be distinct. Critical-probe routes use Q01 through Q08 and refer to entries in the shared critical_probe_bank. For each case, exactly one Q-code is the correct critical-probe route. All eight Q-codes are valid candidates for every case. The four case-level gold Q-codes are guaranteed to be distinct by construction, so the four submitted critical-probe routes must also be distinct. There is no separate hidden set of "active" H or Q entries that must be identified before making case predictions. The participant simply predicts one H-code and one Q-code for each case, with the cross-case distinctness constraints above. Regret routes use G01 through G08, but these codes are case-local. Each case_i contains its own eight-card regret candidate set, so G03 in case 1 and G03 in case 2 refer to different local cards. Regret codes may therefore repeat across cases. Construction, Split, and Development Protocol The challenge uses a fresh challenge-level structural split rather than exposing upstream source split semantics. Preparation first selects a bounded construction pool from the processed logical corpus. Usable rules are grouped by structural family. A family key captures the ordered predicate-role structure and variable-sharing pattern of the candidate rule. Challenge train and evaluation pools are family-disjoint. Evaluation deliberately receives a larger share of rarer structural families so that held-out cases emphasize structural recombination rather than memorization of one repeated rule template. Multiple deterministic challenge variants may be derived from one usable source task when necessary for capacity. All variants of one source task remain on the same challenge side. A board cannot contain the same source task twice, and its four cases are drawn from distinct structural families. The public development_fold field provides the recommended reproducible local validation protocol. It is computed deterministically from challenge-local structural grouping. Recommended development: train on development_fold != F0; validate on development_fold == F0. Published baselines should use this split unless another grouped protocol is explicitly stated. The default prepared challenge contains: 1,000 training boards; 250 evaluation boards. Every board contains four cases, giving: 4,000 training diagnostic cases; 1,000 evaluation diagnostic cases. The public package contains: train.csv; test.csv; sample_submission.csv. There is no public answer key. Training Targets and Submission Contract Training provides exactly 16 target columns: case_1_policy; case_1_terminal; case_1_critical; case_1_regret; the same four targets for cases 2 through 4. Valid domains are: policy: P01 through P08, interpreted against that case's local policy cards; terminal: H01 through H08, interpreted against the board-level shared terminal_bank; critical probe: Q01 through Q08, interpreted against the board-level shared critical_probe_bank; regret: G01 through G08, interpreted against that case's local regret cards. For terminal and critical-probe prediction, all eight codes are legal candidates for every case. The evaluator stores exactly one gold H-code and one gold Q-code for each case. Across the four cases on a board, the four gold H-codes are distinct and the four gold Q-codes are distinct. Participants therefore submit four distinct H-codes and four distinct Q-codes directly; no additional board-level activation label or subset prediction exists. Use sample_submission.csv exactly. The submission contains exactly 17 columns in total: 1 sample_id column plus 16 target columns. The required columns, in order, are: sample_id,case_1_policy,case_1_terminal,case_1_critical,case_1_regret,case_2_policy,case_2_terminal,case_2_critical,case_2_regret,case_3_policy,case_3_terminal,case_3_critical,case_3_regret,case_4_policy,case_4_terminal,case_4_critical,case_4_regret This is exactly 17 columns total: sample_id plus four targets for each of four cases 4 × 4 = 16 target columns). The terminal and critical-probe columns are direct case-level route predictions into shared banks. For example, if the four correct terminal routes are case 1 → H06, case 2 → H02, case 3 → H08, and case 4 → H03, then those four codes are submitted in the corresponding case columns. The remaining H-codes are simply incorrect candidates for those cases. The Q-coded critical-probe bank works the same way: each case has one correct Q-code, and the four correct Q-codes are distinct. Policy and regret codes are local to each case and therefore do not have cross-case uniqueness constraints. Every expected sample_id must appear exactly once. The four terminal routes on a board must be distinct. The four critical-probe routes on a board must be distinct. The selected policy costs must satisfy the public board_budget. Malformed submissions, including unknown categorical codes, missing rows, extra rows, duplicate IDs, missing columns, extra columns, incorrect column order, repeated shared routes, or over-budget policy selections, receive the evaluator floor. Evaluation Let: p = diagnostic-policy accuracy; h = terminal-hypothesis accuracy; q = critical-probe accuracy; g = regret-profile accuracy. Define balanced marginal recovery: M = (p × h × q × g)^(1/4). For every case, form the six unordered target pairs: policy + terminal; policy + critical; policy + regret; terminal + critical; terminal + regret; critical + regret. Let s be the mean fraction of these pairs for which both predictions are correct. Let j be complete-case accuracy, requiring all four predictions for one case to be correct. Let b be complete-board accuracy, requiring all sixteen predictions on the board to be correct. Define: K = 0.60s + 0.35j + 0.05b. The final score is: Score = 100 × M^0.40 × K^0.60. Scores are clipped to [0.01,100]. A perfect submission receives exactly 100.0. The metric uses deterministic categorical comparison only. There is no LLM judge, embedding service, external API, or manual scoring. Metric Rationale The metric is designed around two goals: every target family must matter, and the leaderboard should reward coherent reconstruction of the diagnostic process rather than four unrelated classifiers. M is the geometric mean of policy, terminal-hypothesis, critical-probe, and regret accuracy. The geometric mean strongly penalizes collapse on any one target family while still providing smooth marginal credit. A system therefore cannot compensate for near-zero policy accuracy by becoming extremely strong on terminal prediction alone. K measures increasingly strict forms of consistency. The weight 0.60 on s is the largest because pairwise correctness is the densest coherence signal. It preserves useful ranking resolution for medium-strength systems that are beginning to recover mutually compatible pieces of the diagnostic mechanism but do not yet solve entire cases exactly. The weight 0.35 on j gives substantial additional credit to complete case reconstruction. A case contributes to j only when its policy, terminal hypothesis, critical probe, and regret profile are all correct, so this term directly measures recovery of one complete diagnostic plan. The weight 0.05 on b is intentionally small because exact board recovery is sparse and all-or-nothing. It acts as a bounded global-allocation bonus for solving all four cases together under the shared-bank and budget constraints without allowing a rare complete-board event to dominate the leaderboard. The outer exponents assign 0.40 to marginal recovery and 0.60 to coherence. This reflects the intended priority of the challenge: individual target accuracy is necessary, but the main objective is a mutually compatible explanation of the adaptive policy, diagnosed hypothesis, indispensable probe, and greedy-regret profile. The larger exponent on K therefore rewards coherent experiment planning more strongly than independent head accuracy. These coefficients are fixed benchmark-design constants and are not tuned on the private evaluation set. Compute Environment and Machine-Learning Requirement The execution environment provides: one NVIDIA A10G GPU; 24 GB GPU memory; host CPU and memory; a 90-minute end-to-end runtime limit. The runtime includes data loading, JSON parsing, symbolic preprocessing, tokenization, model fitting or adaptation, inference, policy scoring, budget-aware decoding, and submission writing. This is a learned ML challenge. Final semantic predictions must materially depend on trainable neural parameters fitted or calibrated from the released training boards. The following are not valid primary solution systems: TF-IDF; BM25; bag-of-words retrieval; regex-only matching; deterministic symbolic execution as the complete solver; exhaustive policy evaluation as the complete solver; hand-authored rule induction; logistic regression; SVM; nearest-neighbor classification; random forests; gradient-boosted trees; similar classical statistical models as the decisive final predictor. These methods may be used for preprocessing, indexing, diagnostics, feature construction, candidate pruning, validity checks, or final constrained decoding after neural scoring. Remote model APIs are not allowed. A strong solution can combine a long-context transformer or graph encoder with candidate-conditioned policy scoring. One practical architecture is to encode the two validator views and the eight rule hypotheses, embed the probe library, estimate the semantic usefulness of each policy tree, predict critical-probe and regret targets from the same latent representation, and then perform exact budget-aware decoding across the four cases. Useful model families include: long-context transformers; graph transformers; neural rule encoders; candidate-conditioned cross-encoders; tree or set transformers; latent-variable models; neural experiment-design models. The expected difficult failure modes are greedy first-probe selection, static probe ranking, identifier-specific reasoning, correct terminal rules with inefficient policies, local policy choices that lose under the shared budget, incorrect critical-probe necessity, and failure to predict the regret of a tempting greedy alternative. The final objective is: four ambiguous logical cases → four adaptive diagnostic policies → four terminal hypotheses → four critical probes → four regret profiles under one shared diagnostic budget
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Orphan Timbers: Cross-Dating and Provenance of Timbers With and Without a Home Stand

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70xzz47wjnjy54zr03m0wjpx8dyrmj
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dominico's score of 55.058!

Full challenge description from page:

> Orphan Timbers: Cross-Dating and Provenance of Timbers With and Without a Home Stand Overview Wood keeps a calendar. The width of each annual ring records that year's growing season, and trees across a region share the same sequence of good and bad years. A dendrochronology laboratory dates an undated timber, a roof beam, the panel behind a painting, the top plate of a violin, by sliding its ring-width sequence along dated reference trees until the pattern locks onto one calendar position, and it says where the tree grew from which stands agree most. This challenge is an LLM-evaluation benchmark built on that job, end to end. A solver receives a library of dated reference trees from 448 European stands and 1,458 undated segments, and must build, validate and run a system that predicts, for every segment, the calendar year of its last ring, the library stand it came from, the coordinates where the tree grew, and a probability that the year is exact. Nothing is pre-built: the solver chooses the signal processing, the reference material, the validation scheme and any model. The timbers come in three regimes, and test rows do not say which. Half of the eligible stands were withheld from the library: 344 at random, so their timbers must be dated and located from same-species neighbours within 250 km, and 102 more as three whole regions, the Baltic states, eastern Finland and central Spain, so their timbers have no same-species library stand within 250 km at all. That far regime is the traded-timber case that defeats laboratories in practice: Baltic oak shipped across northern Europe for four centuries, dated today only by reference material hundreds of kilometres from where it grew. Of the 1,458 test timbers, 964 come from library stands, 378 from randomly withheld stands and 116 from the withheld regions. Segments are short, 30 to 90 rings, and every length weighs the same. One construction helps: timbers arrive in structures, groups of one to three from one stand felled within ten years, which can be cross-matched against each other before any is placed on the calendar. Research gap and benchmark position Laboratories date timbers with a classical t-value sweep against master chronologies, and the machine-learning literature on tree-ring provenance frames origin as closed-set classification: every candidate stand is in the reference set, the classifier is benchmarked against that same sweep, and dating is evaluated separately, if at all. Neither setting poses the cases that dominate practice, a timber from a stand nobody has sampled, or from a region with no reference material at all. This benchmark is built around those cases and measures them directly: Open-set and adversarially spatial. 446 of 894 stands are withheld, 102 of them as whole regions whose timbers sit 250 to 800 km from the nearest same-species library stand. Every test row is unmarked, and no test timber's stand, or region, has a labelled row in training. The classical sweep dates 38 to 78 percent of library-stand timbers exactly by band, 8 to 30 percent of randomly withheld ones and 3 percent of far ones; that gradient is the object of study. Four joint targets, one score. Exact year, library stand, continuous origin coordinates and a calibrated exact-year probability are scored together: a distance-decay stand credit normalised to the best stand the library can offer, an unnormalised coordinate credit that a withheld-stand timber can only earn in full by placing its origin away from every library stand, and Brier skill against the best constant, macro-averaged over nine cells: eight band-by-regime cells for library and randomly withheld timbers, and one pooled cell for far timbers, which are too few, and today too hard, to split by band. Structures as evidence. Timbers arrive in groups from one stand felled within ten years, so rows constrain each other; joint dating lifts the classical sweep from 26.4 to 31.6 of 100. A sealed reference. Every width is rescaled and jittered, ids derive from a secret salt, and external chronologies are prohibited, so the library shipped is the only reference and the task is the method, not the lookup. No existing dendrochronology product or published benchmark combines short fixed-length segments, withheld stands and withheld regions, continuous origin scoring and structure-level joint constraints under a single calibrated metric. Data All solver-visible files are under ./public/. sites.csv: the 448 library stands. site_id, species_code, species_group, lat and lon rounded to 0.25 degrees, elevation_m rounded to 100 m (empty when unknown), first_year, last_year, n_reference_trees (7 to 15). reference_trees.csv: 5,010 dated trees. tree_id, site_id, first_year, widths as a JSON list of integers, one per year from first_year; 0 marks a locally absent ring. reference_chronologies.csv: one master per stand. site_id, year, index (1000 × the geometric mean, over the stand's trees, of ring width divided by its Gaussian-smoothed trend, sigma 15 years), depth (trees carrying that year). train.csv: 5,787 labelled segments. id, structure_id, band, species_group, widths, and target_json holding site_id (empty when the stand is withheld), end_year, origin_lat, origin_lon and radius_km, the credit radius that row is scored with (250, or 600 and more for far rows). 3,863 training rows come from library stands, 1,562 from randomly withheld stands and 362 from a withheld region. Withheld stands are routed whole: a withheld stand, and a withheld region, contributes rows to training or to test, never to both. test.csv: 1,458 unlabelled segments with the same feature columns. sample_submission.csv: a valid, deliberately weak submission. build_summary.json: counts, band lengths, the withheld regions and the radius rules; no seed, no secret. Widths are integers in arbitrary units proportional to hundredths of a millimetre: every series was multiplied by a secret factor between 0.6 and 1.6 and every ring jittered by a few percent, so patterns survive but neither values nor ratios can be looked up anywhere. Species groups are PISY, PCAB, QUER (all oaks, which wood anatomy cannot separate), ABAL, FASY, PINI, LADE and PICE; every query's group is given. Library stands by group: PISY 113, PCAB 120, QUER 93, ABAL 37, FASY 37, PINI 25, LADE 15, PICE 8. Bands 1 to 4 are 30, 45, 65 and 90 rings, with 364, 365, 364 and 365 test rows. Test structures: 591 singletons, 279 pairs, 103 triples. Every query tree is outside the library, no tree yields more than one query, library stands supply different trees to train and test, and train and test structures are disjoint. Test end years run from 13 BC to 2021, half of them between 1927 and 1994. Targets For each test row, one JSON object: site_id: a stand from sites.csv. end_year: an integer calendar year, negative for BC. confidence: a number in [0, 1], the probability that end_year is exact. origin_lat, origin_lon: the estimated origin in decimal degrees; it need not coincide with any stand, and for a far timber it should not. {"site_id":"s3f1c9a0b2d4","end_year":1873,"confidence":0.81,"origin_lat":47.25,"origin_lon":8.5} Submission Write a CSV with exactly two columns, id and target_json, and one row per test id: 1,458 rows, a header, every id exactly once. Use sample_submission.csv as the schema authority. Structural faults raise: missing, extra, duplicate or unknown ids; missing or extra columns; invalid JSON; a missing field. Value faults are scored, never rejected: an empty or unknown site_id earns no stand credit, an end_year that is not a finite integer earns no dating credit, coordinates that are not finite numbers in range earn no coordinate credit, a confidence that is not a finite number is read as 0.5 and one outside [0, 1] is clipped. Evaluation Every test row belongs to one of nine cells. Library-stand rows and randomly withheld rows form eight cells, band crossed with regime; far rows form one pooled cell regardless of band, because they are few and, for every method measured so far, at the floor in every band. Three components are averaged within each cell, then equally across the nine, so a solver that only works on long timbers from known stands cannot carry the score, and the far cell weighs one ninth. Dating: exact-year hit rate. A year off scores 0. Provenance: mean of a stand credit and a coordinate credit, each a linear distance decay max(0, 1 - d/R) where R is the row's credit radius: 250 km for present and randomly withheld rows; for far rows, 600 km or 1.5 times the distance to the nearest same-species library stand, whichever is larger, rounded up to 50 km. The stand credit runs from the predicted stand to the true stand, is 0 if the predicted stand is another species group, and is divided by the best credit any library stand could earn (1 when the true stand is in the library; otherwise the nearest same-species neighbour's credit). The coordinate credit runs from the submitted origin to the true origin, unnormalised: the true origin earns 1 in every regime. Calibration: Brier skill of confidence against the dating hit within the cell, measured against the best constant: 1 - mean((c - hit)^2) / (rate × (1 - rate)), clipped to [0, 1]. A flat confidence scores exactly 0. score = 100 × (0.55 × Dating + 0.30 × Provenance + 0.15 × Calibration) Scores lie in [0, 100]. A perfect submission scores 100; perfect placements with a flat confidence score 85. The grader scores every row it is given and returns one float; nothing depends on row order. Anchors on the frozen test set: the sample submission scores 2.7; the strongest shortcut that never cross-dates, the top-matching stand's last reference year, 10.6; the classical sweep, which detrends and slides every segment across every same-species master and takes the highest t-value, 26.4 alone and 31.6 when structures are dated jointly; a gradient-boosted reranker over master and regional-composite sweeps, decided per structure and calibrated per band, 34.9. By regime, the classical joint sweep dates 38 to 78 percent of library-stand timbers exactly by band, 8 to 30 percent of randomly withheld ones and 3 percent of far ones, with zero calibration skill in most withheld cells. That gradient is the headroom. Modeling guidance Detrend before matching: raw widths carry the age trend, and a regressor from growth level to calendar year lands 51 years off. Restrict candidates to the query's species group. Confirm placements against the stand's individual trees, not only its master. Build regional composites of neighbouring stands for timbers with no home stand, at more than one spatial scale, because a far timber's pattern is shared only weakly and only with stands hundreds of kilometres away; place the origin between or beyond stands when the evidence is shared, since an origin snapped to the named stand can never earn more than the stand credit and for far timbers earns much less. Decide structures jointly: one stand, one ten-year window. Validate by stand, not by row, and withhold both random stands and whole regions from the library locally, otherwise the 494 withheld-stand test rows have no estimate; the 1,924 withheld-stand training rows, marked by an empty site_id and by radius_km, are labelled examples of those regimes from other withheld stands and regions, never from a test timber's own. Fit confidence out of fold, on those rows too, per band. Learned similarity over segment and reference-window pairs, sequence encoders and rerankers trained on the 5,787 labelled queries are the intended use of the GPU; the classical sweep runs on CPU in minutes and is the floor. Runtime Compute: one NVIDIA A10G GPU, within the platform's time limit. Network access: disabled. External tree-ring data of any kind is prohibited: no measurements or chronologies beyond ./public/, from any archive, database or publication, downloaded or recalled. A correlation sweep against outside material would be indistinguishable from the task itself. Pretrained components may be used only when already available in the execution environment. No external language-model APIs. No hard-coded answers, and no use of id or row order as a feature. Build notes Measurements are dated ring-width series contributed by European laboratories. Where a tree was measured on several cores, only the longest core is used, and any query whose ring widths correlate above 0.95 with a reference tree of its stand, or a test query that does so with a training query, is dropped as a second core under another id (95 rows), so no tree can sit on both sides of a split. Series on relative timescales were excluded. Files in thousandths of a millimetre were converted to hundredths before the secret scaling, so the unit cannot mark a laboratory. Segments are cut only from years where the stand had at least three reference-quality trees alive (checked on the withheld trees for withheld stands), with end years uniform over the feasible span and bands assigned after feasibility so they hold equal rows. Within every library stand, one in five query trees is a test query. Withholding was done in two steps. Every stand within 250 km of three centres (the Baltic states, eastern Finland, central Spain) was withheld as a region. Of the rest, 40 percent were withheld at random, keeping only those with a same-species library stand within 250 km. A withheld stand is scored as far when its nearest same-species library stand is 250 km or more away; 102 of the 446 withheld stands are. Withheld stands then went whole to one side: the Baltic and Spanish regions and 174 randomly withheld locations supply test rows only (378 absent and 116 far test rows, the far ones 25, 25, 35 and 31 by band, with credit radii from 600 to 1200 km); the Finnish region and 170 other locations supply training rows only. Routing is by rounded location, so co-located stands share a side, and a solver cannot rebuild a test timber's stand from labelled training rows. The far rows form one pooled cell, the smallest in the score and the one no existing method handles: the classical sweep and the shipped reranker both date FAR_34.9 of far timbers exactly, so its ninth of the score is open ground. Ids, shuffles, scale factors and jitter derive from a secret salt that is not published. Calendar-year columns (first_year, last_year, end_year) are long-tailed by nature: most rows sit in the nineteenth and twentieth centuries while a few stands reach back to 324 BC, so a 3×IQR rule flags 4 to 7 percent of them as extreme; they are genuine dated series and are kept. Shortcut audit: constant years, the most common training year, growth-level regression, id order, band and nearest-training-segment probes all sit within 0.01 of the floor. Two artefacts are documented rather than hidden: structure size correlates weakly with end year (Spearman 0.24) because larger stands were sampled later, and 6 percent of present-stand segments end at their stand's last reference year because living trees are sampled together; exploiting the latter dates 2 percent of rows against 28 percent for the sweep's own placement. Rebuilding withheld-stand chronologies from the labelled training rows and sweeping test rows against them dates far rows at 2 percent and randomly withheld rows at 9 percent, ordinary neighbour signal; before withheld stands were routed whole to one side it dated far rows at 34 percent, which is why they are. No test timber correlates above 0.95 with any reference tree of its stand; 32 of 964 correlate above 0.90, the level of unusually similar neighbours. Limits: European temperate species only; most segments fall in the last two centuries and only 5 percent before 1735; far timbers are still on the same continent as the library, and sapwood loss and the felling-date offset from the last measured ring are not modelled. The dataset is an offline research benchmark, not a dating or authentication product.
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Adduct Spectral Library Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70dwqhm1ja7gvxnm7dadgbjn8e6kn0
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Match a measured sodium-adduct spectrum, [M+Na]+, to the protonated spectrum, [M+H]+, of the same compound. Each query has a library of 4–28 alternatives with the same molecular formula. Molecular mass alone therefore cannot select the answer. Changing the attached ion can change which fragments survive and their intensities. The task is to recognize a compound across that change using measured peak patterns, without receiving molecular structures. Each library contains one representative per distinct two-dimensional molecular identity; stereoisomers are not treated as distinguishable identities. Dataset There are 1,200 training queries from 405 formula groups and 300 test queries from 145 other formula groups, using 5,152 measured spectra. A fixed hash assigns whole formula groups to train or test, so neither a formula nor any query or candidate compound crosses the split. A fixed hash ordering selects the compact query subset inside the existing formula partitions. Each query retains all its candidates and original measured peaks; spectra unreferenced by the retained queries are omitted. Related chemical families with different formulae can still occur on both sides. Up to three distinct native sodium-adduct measurements per compound are retained; these are separate measured inputs, not synthetic augmentations or independent compounds. Groups with identical candidate spectra assigned different identities were excluded. | File / field | Type | Meaning | |---|---|---| | train.csv, test.csv: task_id | string | Unique query ID. | | formula | string | Neutral molecular formula shared by the query and every candidate. | | query_spectrum | string | Query array key in spectra.npz; always a sodium adduct. | | candidates | JSON array | Objects with a row-local candidate_id and a spectrum_id array key; always protonated spectra. | | spectra.npz | NumPy archive | Each key selects a float64 array of shape (number_of_peaks, 2). | | train_labels.csv, sample_submission.csv | CSV | task_id,match, containing correct or example candidate IDs. | Load arrays with numpy.load("spectra.npz", allow_pickle=False). Column 0 is mass-to-charge ratio, in Thomson; column 1 is relative intensity, positive and normalized to a maximum of 1. Peaks are sorted by increasing mass-to-charge ratio. Every spectrum has at least six peaks. No peaks are synthesized or mixed. Protonated library representatives are selected by largest peak count, with deterministic tie-breaking. Sodium queries are selected by stable source ordering, with exact repeated peak arrays removed. Spectra can come from different instruments and acquisition energies; these conditions are not standardized by this task. Library labels may contain source errors, and some isomers may produce very similar spectra. The task measures closed-library identity matching, not clinical identification or reconstruction of a molecular graph. Submission Submit UTF-8 CSV with exactly task_id,match, in that order, once per test query. match must be one candidate ID from that query. Candidate order is shuffled and has no ranking meaning. task_id,match example_query,c003 Evaluation The score is top-1 accuracy: the fraction of queries whose selected candidate is correct. Higher is better; the range is 0–1 and exact answers score 1. The metric measures whether the library lookup returns the correct identity, not merely a similar isomer. Every query receives equal weight. Invalid, empty or out-of-pool candidate values count as incorrect. Incorrect columns, duplicate task IDs or missing/extra rows invalidate the submission. Row order does not matter. Expected Approach Train a compact query–candidate matching model on the measured spectra. Use separate adduct-aware projections or an adduct indicator so the model can learn changes between sodium and protonated observations. For an efficient implementation: Load each distinct peak array once. Cache binned intensity features or compact peak-sequence inputs, preserving the distinction between mass positions and intensities. Combine learned embeddings with inexpensive peak-overlap and mass-difference features. Molecular formula alone cannot distinguish candidates within a query. Train with other spectra in the same candidate pool as negatives. Batch all candidate scores and use one matching loss per query. Validate by formula group, keeping related measurements together. Encode each spectrum once after training and select the highest-scoring candidate's row-local ID. What Not To Use GPU training and generic pretrained models are allowed. Use only supplied data. Do not use external spectral libraries, source-corpus copies, challenge-specific spectral checkpoints, synthesized training spectra, hosted APIs, manual test identification or hard-coded answers. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Beat Montage Provenance Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70xyrja5mda6wy3mdrm8w0ed8aw7am
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Beat Montage Provenance Audit Overview A window of sixteen heartbeats is handed to you as a montage. It was assembled along two axes at once, and neither is labelled: who, the sixteen slots were cut into runs, and each run holds consecutive beats from one person. A window draws on two or three people and may return to one it used earlier. how, independently, the slots were cut into runs again, and each run was captured through one acquisition channel: one fixed configuration of the recording chain, which leaves its own mark on every beat that passes through it. A window uses two or three channels and may likewise return to one it used earlier. The two sets of cuts were drawn independently of each other. A boundary in the window may therefore belong to the who axis, to the how axis, or to both at once. Your job is to recover both partitions of the same sixteen slots, and to say where they coincide. This is not one grouping, not a label per beat, and not a score. The output is a discrete structured audit record in which two cross-cutting partitions of one set of sixteen items are asserted together, along with the relationship between them, and the record is graded head by head and on whether its own pieces agree. Two partitions that are each plausible but jointly incoherent are not a correct answer. The two axes are confounded on purpose, because both of them change what a beat looks like: a subject run deliberately spans a change of beat shape, one person's beats do not all look alike, so a run is not one waveform repeated; different people's beats can look alike; a channel change restyles every waveform while nobody has changed; and where the two axes cut in the same place, that boundary is locally unattributable, you can see that something changed, not which of the two things it was. Task constraints The window is all you get. Sixteen beats, and nothing else: no timestamps, no person identifier, no channel identifier, no other window from the same person or channel. The people are unseen. Every test montage is built from people who appear nowhere in the training data, so both partitions must be produced zero-shot. Channels are window-local. A channel has no fixed identity across the dataset and its parameters are never published; the question is only which slots within this window came through the same one, and its settings drift slightly from beat to beat. Both partitions are chance-corrected (adjusted Rand index), so putting every slot in one group scores about nothing on either axis. They are two different partitions. One grouping submitted for both axes can only be right about a window whose axes happen to cut in the same places. The five fields are one record, scored for agreeing with each other as well as against the reference, see S_consist under Evaluation. uncertainty is scored, so it has to reflect the window it describes. Data and recording conditions The beats come from real ambulatory ECG recordings, long continuous recordings from individual people, digitised at 360 samples per second, from a single chest lead, with every beat located by experts. The recordings are de-identified. Each slot is published as a normalised signal segment, built as follows: a fixed window of raw signal is cut around a beat location (±96 samples, about half a second); it is passed through that slot's acquisition channel; it is amplitude-normalised, its mean is subtracted and it is divided by its standard deviation, so overall gain and baseline offset carry no information and only the contour remains; it is resampled to 64 points and quantised to uint8 (0–255). So a slot is a 64-number curve describing a beat's contour, not its absolute voltage. Dataset You are given 2,600 training windows (each with the answer record) and must produce the record for each of the 520 test windows. Files provided: train.npz, training inputs; holds the arrays ids and beats described below, with N = 2,600 windows train.csv, training labels; one row per training window, with the six columns described below. The five label columns are exactly what you submit test.npz, test inputs; the same two arrays as train.npz, with N = 520 windows sample_submission.csv, a correctly-formatted but deliberately weak example ledger, with the same six columns as train.csv and one row for each of the 520 test ids. It is provided to show the exact expected format rather than as a useful starting point Arrays in train.npz / test.npz: ids, type str, shape (N,), the window id, e.g. win_0a1b2c3d4e5f6071 beats, type uint8, shape (N, 16, 64), the 16 slots; beats[i, k] is the 64-point normalised curve of slot k in window i, for k in 0…15 Columns in train.csv (one row per training window; the same five label columns are what you submit): id, type string, e.g. win_0a1b2c3d4e5f6071, matches an entry of ids in the matching .npz source_groups_json, type string, a JSON list of lists of int, e.g. [[0,1,2,3,10,11,12,13,14,15],[4,5,6,7,8,9]], each inner list is the slot indices contributed by one person; the lists together contain every index 0…15 exactly once. A person may recur, so a list can be non-contiguous channel_groups_json, type string, a JSON list of lists of int, e.g. [[0,1,2,3,4,5],[6,7,8,9,10,11,12,13,14,15]], the same, for the acquisition channel. **A different partition of the same 16 slots** confound_points_json, type string, a JSON list of int, e.g. [10], slot indices that are a boundary on both axes at once, where the person and the channel change together pattern, type string, one of the enum values aligned, nested, crossed (defined below), e.g. crossed, how the two partitions relate uncertainty, type float in [0,1], e.g. 0.58, how confusable the window is pattern values. Write B_who for the set of slot indices where the person changes and B_how for the set where the channel changes: aligned, B_who and B_how are the same set: the two axes cut in exactly the same places; nested, one is a proper subset of the other: one axis cuts everywhere the other does, and at least once more; crossed, neither contains the other: each axis has at least one boundary the other lacks. Evaluation Each window is scored per head, then combined: S_source : chance-corrected agreement between your PERSON partition and the true one (adjusted Rand index, clamped to [0,1]). One big group scores ~0. S_channel : the same, for your CHANNEL partition. S_confound : F1 over the coinciding-boundary slots (a prediction matches within +/-1) S_pattern : 1 if the relationship is exact, else 0 S_uncert : exp(-|pred - true| / 0.18) S_consist : the average of two structural checks on YOUR OWN record -- (a) every confound point you list is a boundary in BOTH of your partitions, (b) the pattern you report is the one your own two partitions imply raw = 0.30S_source + 0.24S_channel + 0.16S_confound + 0.14S_pattern 0.10S_uncert + 0.06S_consist row_score = raw ** 1.5 The final score is the mean row_score over all 520 test windows (range 0–1, higher is better). The provided sample_submission.csv scores ≈ 0.09. Submission format Submit submission.csv with exactly these six columns, in this order, one row per test id: id, source_groups_json, channel_groups_json, confound_points_json, pattern, uncertainty Example (two rows; note the JSON is valid, and each field is doubled-quoted because it sits inside a CSV field): id,source_groups_json,channel_groups_json,confound_points_json,pattern,uncertainty win_0a1b2c3d4e5f6071,"[[0,1,2,3,10,11,12,13,14,15],[4,5,6,7,8,9]]","[[0,1,2,3,4,5],[6,7,8,9,10,11,12,13,14,15]]","[]",crossed,0.58 win_112233445566778a,"[[0,1,2,3,4],[5,6,7,8,9,10,11,12,13,14,15]]","[[0,1,2,3,4],[5,6,7,8,9,10],[11,12,13,14,15]]","[5]",nested,0.31 A structural error (missing/extra/duplicate ids, wrong or extra columns, non-finite or out-of-range uncertainty) makes the whole submission score 0. A malformed or invalid single row scores 0 for that row without crashing the grader. Both partitions must be exact. Each of source_groups_json and channel_groups_json has to cover slots 0 to 15 exactly once: no slot left out, no slot named twice. A row that breaks this scores 0 for that row. It is checked before anything is scored, so a partition that is right about the slots it does mention earns nothing if it omits or repeats one. What not to use No external data. Train only on the released training windows, do not fetch external ECG corpora or attempt to identify the source recordings. No test labels. The test records are withheld. Reproducible inference. Fixed seeds, deterministic decoding. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cycle-Consistent Three-View Terminal Binding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70wztrzeqkxp40r9ma9dcgbs8c73m0
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aegistran's score of 0.629!

Full challenge description from page:

> Overview Electronic component libraries describe the same physical terminal in several independently drawn views. During library migration, terminal names may be replaced with anonymous local IDs while the view geometry survives. Repairing the library then requires recovering which breadboard, schematic, and circuit-board terminals represent one physical connector. Each case contains three terminal banks: breadboard IDs Bdd, schematic IDs Sdd, and circuit-board IDs Pdd. A terminal has a normalized two-dimensional location, its nearest canvas edge, and its primitive shape class. The banks contain the same 4 to 32 physical connectors, but each bank is independently renamed, reflected or rotated, and slightly perturbed. Their layouts can also be genuinely different: a schematic may arrange pins by logical role while the other views retain package geometry. A set of correct three-view bindings is supplied as case-local anchors. Recover the complete one-to-one correspondence. Every output atom must bind one B terminal, one S terminal, and one P terminal, and all atoms together must form a cycle-consistent three-way permutation. The test split is disjoint by complete source view asset: no breadboard, schematic, or circuit-board drawing used to create a test case is used to create a training case. Strong solutions must learn transferable structural compatibility, use anchor-relative geometry, and solve a global constrained assignment rather than memorize assets or match IDs. Dataset The public dataset contains three CSV files. train.csv contains 4,204 labeled cases created from 1,051 source components. test.csv contains 840 unlabeled cases created from 210 held-out source components. sample_submission.csv contains one structurally valid example ledger for every test case. train.csv Columns case_id (string): anonymous unique case identifier. terminal_count (integer): number of terminals in each of the three banks; between 4 and 32 inclusive. breadboard_terminals (JSON string): array of exactly terminal_count breadboard terminal objects. schematic_terminals (JSON string): array of exactly terminal_count schematic terminal objects. pcb_terminals (JSON string): array of exactly terminal_count circuit-board terminal objects. known_bindings (string): semicolon-separated anchor atoms already known to be correct. connector_ledger (string): complete target correspondence with exactly terminal_count atoms. test.csv Columns case_id (string): anonymous unique test-case identifier. terminal_count (integer): number of terminals in every bank. breadboard_terminals (JSON string): breadboard terminal array. schematic_terminals (JSON string): schematic terminal array. pcb_terminals (JSON string): circuit-board terminal array. known_bindings (string): supplied correct anchor atoms. test.csv omits connector_ledger. sample_submission.csv Columns case_id (string): identifier copied from test.csv. connector_ledger (string): one complete structurally valid example correspondence. Terminal Object Schema Every object in a terminal array has exactly five fields. terminal (string): case-local ID such as B03, S11, or P07; the prefix identifies only the view. x (float): normalized horizontal center coordinate in [0, 1] after the view's independent transformation. y (float): normalized vertical center coordinate in [0, 1] after the view's independent transformation. edge (string enum): nearest normalized canvas edge, one of L, R, T, or B. shape (string enum): source primitive class, one of rect, circle, line, g, path, ellipse, polygon, polyline, or other. Example terminal array: [{"edge":"L","shape":"rect","terminal":"B00","x":0.0026,"y":0.6623},{"edge":"R","shape":"rect","terminal":"B01","x":1.0,"y":0.0}] The array order follows local terminal-ID order and has no cross-view meaning. Cases with 4-6 terminals have a base allowance of one anchor, cases with 7-12 have two, cases with 13-20 have three, and larger cases have four. Some source drawings place multiple terminals at the same normalized center with the same public shape class. In those cases, preparation supplies additional correct anchors until no two unanchored terminals have an identical pre-perturbation (x, y, shape) signature in any view. At least one terminal remains hidden in every case. This prevents independent coordinate noise from manufacturing an arbitrary distinction that was absent from the source geometry. Submission Submit a CSV with exactly two columns. Header: case_id,connector_ledger Example row: PIN_0123456789abcd,B00=S03=P01;B01=S00=P03;B02=S02=P00;B03=S01=P02 An atom has the exact form Bdd=Sdd=Pdd. A ledger must contain exactly terminal_count unique atoms in lexical order, separated by semicolons with no whitespace. Every terminal ID present in each case must occur exactly once in its corresponding position. Copy the supplied known_bindings into the complete ledger and infer every remaining binding. Every required test ID must appear exactly once. Additional platform rows outside the scored answer set are ignored after required-ID and duplicate-ID validation. A non-null malformed ledger or a ledger that contradicts a supplied anchor receives the full wrong-row penalty: it contributes one false negative and one false positive for every hidden triple and every hidden pair edge, and receives no exact-case credit. Structural CSV violations, including missing IDs, duplicate IDs, null ledgers, or unexpected columns, raise an error. Evaluation The score is bounded in [0, 1], where higher is better. Supplied anchor connectors are excluded from all three components. Score = 0.55 * HiddenTripleF1 + 0.30 * HiddenPairEdgeF1 + 0.15 * HiddenExactCaseAccuracy HiddenTripleF1 Every hidden case-qualified (B, S, P) binding is one atom. Counts are pooled over all scored cases. HiddenTripleF1 = 2 * TP / (2 * TP + FP + FN) Credit requires the full three-view binding to be correct. HiddenPairEdgeF1 Each hidden triple contributes three case-qualified pair edges: (B, S), (B, P), and (S, P). These edges are pooled and scored with the same F1 formula. This component gives partial credit when two views are bound correctly but the third is not. HiddenExactCaseAccuracy This is the fraction of cases in which every hidden connector triple is correct. Supplied anchors still have to appear in a structurally valid complete ledger but do not determine exact-case credit. Allowed And Prohibited Methods Allowed CPU-compatible supervised learning, graph matching, optimal transport, assignment algorithms, and constrained reranking. Models trained exclusively from the supplied public files. Validation grouped by inferred component or shared-layout similarity. Generally available numerical and machine-learning libraries that do not contain challenge answers. Prohibited Searching external component libraries, repositories, catalogs, or web services to identify or match a case. Reconnecting anonymous rows to original component names, files, checksums, or source identifiers. Using external drawing collections, cached source records, or hardcoded test mappings. Exploiting case IDs, row order, anchor selection order, or sample values as prediction signals. &nbsp;
> $700 Pool
> Closes in 2h 1m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Pollen Trail Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bk8xhe88xy7n1tyzy3cbtqd8e186w
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat drcs's score of 0.696!

Full challenge description from page:

> Pollen Trail Reconstruction Overview A pollinator carries a mixture of pollen from several previous flowers. Given an unordered set of donor profiles and incoming pollen assays, identify the flower visited immediately before each observed flower. The most abundant donor in an assay need not be the most recent donor, because pollen can survive through many intervening visits. The task uses Mixed Pollen Assays, an original controlled simulation. Every experiment has one route that visits each of its 10 to 14 flowers exactly once. There are 1,600 independent training experiments holding 19,277 rows and 400 independent evaluation experiments holding 4,794 rows. Entire experiments are separated by a deterministic group split, so no route is divided between training and evaluation. All IDs are arbitrary identifiers and carry no chronology. Your job is to recover, for every evaluation flower, the identity of the flower visited immediately before it. Dataset Preparation writes five participant files. | File | Rows | Role | |---|---|---| | train.csv | 19,277 | Training flowers with measurements | | test.csv | 4,794 | Evaluation flowers with the identical feature schema | | train_labels.csv | 19,277 | Training predecessor labels | | train_groups.csv | 19,277 | Query-to-experiment validation group assignments | | sample_submission.csv | 4,794 | Valid-format example predictions | Both feature tables have these exact ten columns, in this order. query_id,experiment_id,flower_id,donor_profile,assay_alt_counts,assay_depths,pickup_yield,retention,entry_profile,entry_load | Column | Type | Description | |---|---|---| | query_id | string | Unique row identifier, used in the output | | experiment_id | string | Array membership; reconstruct each array separately | | flower_id | string | Opaque candidate predecessor identifier within the array | | donor_profile | JSON array of 4 floats | Donor alternate-allele proportions, each 0, 0.5 or 1 | | assay_alt_counts | JSON array of 4 integers | Incoming alternate-allele read counts | | assay_depths | JSON array of 4 integers | Total read depths, each between 20 and 60 | | pickup_yield | float | Positive nominal amount of pollen picked up at this flower | | retention | float | Array's nominal fraction of old carried pollen surviving a visit, between 0.74 and 0.90 | | entry_profile | JSON array of 4 floats | Alternate-allele proportions in the entering load | | entry_load | float | Positive initial carried-pollen load, between 1 and 3, in the same relative units as pickup | train_labels.csv and sample_submission.csv have the columns query_id,prediction. train_groups.csv has the columns query_id,group_id. Parse vector cells with a JSON parser. The same marker order is used throughout an experiment. The values of retention, entry_profile and entry_load repeat within an experiment because they are array calibration, and they vary between experiments. Hold out entire group_id values when you validate. Row order and the lexicographic ordering of IDs carry no route label. Observation model Let M be a four-element carried alternate-allele mass vector and L the total carried load. Initially M is entry_profile * entry_load and L is entry_load. On visiting flower j, its incoming assay is sampled BEFORE taking up that flower's pollen. assay_alt_counts[j,k] ~ Binomial(assay_depths[j,k], clip(M[k] / L, 0.001, 0.999)) Then draw a common survival fraction s ~ Beta(100r, 100(1-r)), where r is the provided nominal retention, and a pickup amount a = pickup_yield[j] * LogNormal(-0.25^2 / 2, 0.25). Update the carried mixture as follows. M f_C -> f_B gives the predecessor label ENTRY for f_A, the label f_A for f_C and the label f_C for f_B. The IDs in this illustration are not real dataset IDs. A flower's own ID is never its predecessor. Exactly one query per experiment has the label ENTRY`. Reference points These scores were measured on the evaluation set and are published so that you can tell early whether a pipeline is working. | Reference point | Predecessor accuracy | |---|---| | Predict ENTRY for every query | 0.0834 | | Nearest donor profile, chosen independently per row | 0.1602 | | Nearest donor profile, one-to-one assignment within each experiment | 0.2964 | Both nearest-donor rows use the squared Euclidean distance between a flower's observed alternate-allele fraction, meaning assay_alt_counts divided by assay_depths, and each candidate profile. The candidates are the donor profiles of the other flowers in the same experiment plus that experiment's entry_profile, and a flower is never its own candidate. The assignment row solves one minimum-cost one-to-one matching per experiment over the same distances. Clearing these three numbers is the beginning of the task, not the end of it. What to use Use the five supplied participant files and the CPU compute tier. No particular training algorithm, architecture or optimization method is required. Analytical likelihoods, learned compatibility scores, assignment solvers, search and structured decoding are all permitted. Deterministic calculations from a single evaluation array's own supplied measurements and candidate set, including solving that array's route, are permitted. IDs may be used for joins, grouping, output and deterministic tie-breaking. Training, fitted preprocessing, feature-statistic estimation, pseudo-labeling, hyperparameter selection and threshold selection must use training data only. If you select a method with validation, split whole training experiments using train_groups.csv. What not to use Do not use external datasets, pretrained models, external APIs, network lookup or private evaluator files. Do not install packages, vendor external code, clone repositories or download notebooks, scripts or checkpoints. Do not use the evaluation arrays to fit or select a model. They are inference-only. That covers fitting vocabularies or normalization, estimating feature statistics, selecting hyperparameters or thresholds, pseudo-labeling and choosing between models on evaluation output. Do not use IDs as predictive features, because arbitrary identifiers contain no biological chronology. Scope and limitations This benchmark measures inverse sequence inference from cumulative mixtures. It does not measure taxonomic identification or field ecology. Finite pooled counts and unknown pickup and survival realizations can leave several routes plausible, so perfect accuracy is not attainable. The task is limited to four independent biallelic markers, complete single-pass arrays and the published simulation family. There are no revisits, missing flowers or real field measurements. Results here do not establish that a model transfers to real pollinators.
> $700 Pool
> Closes in 3h 3m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Capacitor-Coded Interior Wiring Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c2tt5rjkf4h0jpv1p0gj4zn8e35ba
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aerofrazer's score of 0.350!

Full challenge description from page:

> Capacitor-Coded Interior Wiring Recovery A circuit can be probed at its terminals even when its internal connections are inaccessible. This challenge asks you to recover the labeled graph of interior resistive connections from two sets of noisy, complex boundary-impedance measurements. Each set uses a different, known capacitor configuration. Train on simulated circuits with disclosed wiring and predict the interior edges of unseen circuits. The data represent numerical passive RC networks, not measurements from manufactured devices. The intended research question is how well learned structural information and a known circuit model can recover sparse connectivity from limited terminal observations. Conductances are nuisance parameters: they affect the observations but are not prediction targets. Circuit and measurement model There are three boundary terminals, P0, P1, P2, and 18 labeled interior nodes, I0 through I17. The index order for the 21-by-21 matrices below is [P0,P1,P2,I0,...,I17]. Interior labels are meaningful: node Ii has the capacitance and harness connection specified for index i. Every circuit has the following known components: A 1-siemens harness edge from each interior node Ii to terminal P(i mod 3). A 0.05-siemens conductance from every node, including the boundary terminals, to ground. Boundary capacitance 0.5 farads at each terminal. Interior capacitance c_i = 0.35 * 8**(i/17) farads. Exact numeric values are supplied in protocol.json. The unknown interior graph is undirected, connected, has no self-loops, and contains exactly 23 of the 153 possible interior edges. Each present edge has an independently sampled, log-uniform conductance in [0.4,2.5] siemens; absent edges have conductance zero. The conductances and graph stay fixed across all measurements of one circuit. The graph prior is a random recursive spanning tree plus six additional edges. First, randomly permute the 18 node labels. For each node after the first in that permutation, select a parent uniformly from earlier nodes. Then select six distinct edges uniformly from the unused pairs. Reject previously generated labeled topologies. This is not uniform sampling over all connected graphs with 23 edges. Two capacitor states are measured: State 0: all interior capacitor multipliers are 1; boundary capacitors are unchanged. State 1: interior capacitor multipliers are 0.55 for even indices and 2.7 for odd indices; boundary capacitors are unchanged. Both states are measured at angular frequencies [0.12,0.4,1.3,4.0] radians per second, in that order. These values are not frequencies in hertz. Let e_v be the length-21 coordinate vector for a node. Let b_ij = e_(i+3) - e_(j+3) for interior pair (i,j). Define H = sum over i=0..17 of (e_(i mod 3)-e_(i+3))(e_(i mod 3)-e_(i+3))^T L = sum over interior pairs (i,j) of g_ij * b_ij b_ij^T Y(s,omega) = H + L + 0.05Identity + imaginary_unitomega*diag(C_s) Z(s,omega) = inverse(Y(s,omega))[0:3,0:3] Z_ab is the complex terminal-a voltage when a unit AC current is injected into terminal b, all other injected currents are zero, and ground is the reference. The six upper-triangular measurements are ordered (0,0),(0,1),(0,2),(1,1),(1,2),(2,2). The noiseless matrix is reciprocal; the unrecorded lower triangle is not an additional observation. For every recorded complex value z, independently draw two standard normal variables and add real and imaginary noise, each with standard deviation 0.003(abs(z)+0.03) ohms. Here z is the *noiseless** impedance and abs is complex magnitude. Round each resulting real and imaginary coordinate to nine decimal places. There are no missing measurements. Files and split The solver-facing files are under dataset/public/: train.csv: 6,144 circuits; columns id,group_id,sweeps,wiring. test.csv: 1,536 unseen circuits; columns id,group_id,sweeps. sample_submission.csv: test IDs and syntactically valid all-zero placeholders. protocol.json: all fixed physical constants, pair orders and tensor dimensions. sweeps is a JSON array of shape [2,4,6,2]: capacitor state, angular frequency, terminal pair, then [real,imaginary], in ohms. Parse the JSON string before constructing numeric features. The row ID and group ID are opaque identifiers, not physical quantities or model features. Each source circuit contributes one example. No labeled topology is repeated anywhere in the corpus, and no circuit or group appears in both partitions. A deterministic hash of the random source-circuit identifier assigns the split. Both partitions use the same graph and measurement distribution. Test conductances, wiring and source provenance are private. Use whole circuits for training/validation splits before any augmentation or expansion into edge-level examples. Fit scalers, feature selection and model parameters on the fitting partition only. All observations of a validation circuit must stay together. Do not select configurations using private test labels or leaderboard feedback. Prediction and score Write working/submission.csv with exactly the two columns id,wiring, one row for each test ID. Row and column order do not matter. Missing, extra or duplicate IDs, duplicate columns, nulls, additional columns and malformed wiring values invalidate the submission. IDs must be nonempty strings with no leading or trailing whitespace. wiring must be the ASCII prefix b: followed by exactly 153 characters, each 0 or 1. No spaces or separators are allowed. The prefix prevents CSV readers from interpreting the bit string as a number. Bit positions use lexicographic interior-pair order: edge_pairs = [(i, j) for i in range(18) for j in range(i + 1, 18)] position 0 -> (0,1); position 16 -> (0,17) position 17 -> (1,2); position 152 -> (16,17) A 1 predicts that the interior pair is connected; a 0 predicts absence. The known harness and ground shunts are excluded from the target. Predictions are not required to have exactly 23 ones or to form a connected graph. Those are known properties of the truth that a solver may choose to exploit. The all-zero sample is a format example, not a useful solution. The metric is the global Matthews correlation coefficient (MCC). Flatten all predicted and true case-edge decisions across the evaluated rows and compute MCC = (TPTN - FPFN) / sqrt((TP+FP)(TP+FN)(TN+FP)*(TN+FN)) Return 0 when the denominator is zero. Higher is better; the range is [-1,1]. Perfect predictions score 1, inverted truth scores -1, and constant predictions score 0. There is no rescaling. Counts are pooled globally, not averaged per circuit. If the platform grades a subset, the evaluator receives matching submission and answer rows and applies the same formula to that subset. When producing the actual submission, include all test IDs. Permitted modeling and reproducibility Learn from the released training circuits. Direct multilabel prediction, learned priors with numerical inversion, graph models, structured search and other reproducible approaches are permitted. A trained component must materially influence the predictions. The public physical model may be used for per-circuit test-time inference and for newly simulated training examples with independent seeds. Do not access the original private raw corpus, its generation seed, held-out labels, target-bearing files or a source lookup that reconstructs the held-out labels. No pretrained task models or external labeled circuit datasets are part of this benchmark. Record random seeds, dependencies, validation choices and compute used. The author reference was tested locally with Python, NumPy, pandas and threadpoolctl; it ran on CPU and needed no network downloads. It compares a regularized linear model, a trained nonlinear multilabel model, a validation-selected mixture and a physics refinement. The locally audited reference notebook contains the complete solver code and reads only the public directory. The selected platform CPU tier provides 10 cores and 62.5 GiB RAM; a local runtime is not a platform runtime guarantee. This is a partial-information reconstruction benchmark. Every label is an exact simulator edge, but noisy terminal measurements are not claimed to uniquely identify every graph. Useful learning must be demonstrated against uninformative and learned baselines. Low scores alone do not establish a good challenge; recoverability and improvement remain explicit review questions. Dataset provenance The numerical simulations, challenge code and documentation were developed with AI assistance. Labels are exact edges of the simulated circuits, not language-model predictions. The dataset is released under CC0 1.0.
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Dialogue Preference Stability Under Reference Removal

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7exqenfdqpg5yx0mmd4zjj8s8e850v
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Predict the smallest sets of comparison replies whose removal changes the preferred conversation in each pair. Four complete conversations stay unchanged; only unused replies in their human-review comparison pools can be withdrawn. Preference-training pipelines sometimes normalize a reply's human rank against its alternatives before combining scores across turns. Removing an alternative can then change a conversation's training label even though neither conversation was edited. This task identifies exactly which removals cause that instability, including two removals that matter only together. The evidence consists of multilingual, community-written conversation trees and human-ranked alternative replies. Each conversation contains a user prompt, an assistant reply, a follow-up prompt, and another assistant reply. Learn the withheld local preferences from the text, then determine how the specified normalization changes when comparison replies disappear. These are calculated changes to a preference-labeling rule, not observations that people changed their minds. Human ranks are held fixed throughout. The task does not measure the effect of deleting text from a live conversation. Dataset Files are UTF-8 CSVs. JSON arrays occupy individual string cells; parse the CSV first, then those cells as JSON. | File | Contents | |---|---| | train.csv | 3,060 labeled cases. Ordered columns: case_id, routes, reply_pools, withdrawal_candidates, withdrawal_witnesses. | | test.csv | 674 cases with the same four input columns, without withdrawal_witnesses. | | sample_submission.csv | One deterministic, randomly selected witness prediction per test case. Uses only public candidate IDs and the required submission schema. | Private answers.csv has exactly case_id,withdrawal_witnesses. There are no auxiliary media files. The prepared CSVs total approximately 62.5 MB. Inputs | Field | Type | Meaning | |---|---|---| | case_id | string | Opaque case identifier. | | routes | JSON-encoded string | Four objects labeled A-D, each containing id and turns. Maximum 32,000 characters. | | routes[].turns | array of objects | Four turns in order: prompter, assistant, prompter, assistant. Each has string role and text fields. | | routes[].turns[].pool, routes[].turns[].reply | strings | Assistant turns reference their comparison pool and reply, such as P0 and R2. | | reply_pools | JSON-encoded string | Array of pools. Each object has string id and an array replies; each reply has string id and text. | | withdrawal_candidates | JSON-encoded string | One to six objects with string fields id, pool, and reply. IDs are W0 through W5, consecutively assigned within the case. | Each pool contains 2-12 human-ranked alternatives for the same preceding user turn. Its context is available in the route that references it. All alternatives used in normalization are supplied, but ranks and review metadata are withheld. Pool and reply IDs are shuffled independently of quality. A withdrawal candidate always refers to an existing pool reply that is not used by any of the four routes. Routes can share prefixes or assistant replies within a case. Their combined routes and reply_pools JSON is at most 64,000 characters. Text can contain Markdown, code, or several languages. Target withdrawal_witnesses is a JSON-encoded string containing six arrays, in this fixed pair order: AB, AC, AD, BC, BD, CD. Each array lists every inclusion-minimal set of one or two allowed withdrawals that changes that pair's relation. A relation is first preferred, tied, or second preferred; entering or leaving a tie counts as a change. | Value inside a pair's array | Meaning | |---|---| | "W0" | Removing W0 alone changes the pair's relation. | | "W0+W2" | Removing both changes it, but removing either alone does not. | | [] | No allowed one- or two-removal set changes this pair. | List all minimal sets. Do not include a pair containing a successful singleton. For example, if W0 alone works, W0+W2 is not minimal. An array may contain both "W2" and "W0+W1" because neither contains the other. An empty array certifies stability only within the supplied candidates and the two-removal limit. How Reference Labels Are Calculated For each pool, sort its distinct human rank values from best to worst. A reply at zero-based position r among K distinct values has cost c = r / max(K-1, 1). Lower is better; tied ranks receive the same cost. If only one distinct rank remains, all remaining costs are zero. For a route with assistant costs c1 and c2, its comparison key is (max(c1,c2), (c1+c2)/2). Compare keys lexicographically, lowest first: avoid the worse individual reply, then use the mean to break ties. Equal keys tie. Compute each pair's original relation. For every allowed singleton and two-candidate set, remove those comparison replies, recompute distinct rank positions in the affected pools, and recompute the pair relations. Keep exactly the changing sets with no changing proper subset. All remaining human ranks retain their original order. Preparation uses rational arithmetic, not rounded floating-point costs. Deleting an unused rank can change K and a retained reply's normalized cost. The reply keeps its text and human rank, but its percentile-like position among remaining rank levels may differ. Normalized ranks are local measurements, not absolute quality scores across unrelated prompts. Separation and Coverage One case is retained per conversation tree. Whole trees linked by normalized duplicate messages of at least 160 characters share a split. Withdrawal candidates and all pool alternatives come from the same tree as their routes. The previous version's source-group assignment is preserved; training trees do not become test trees. Deleted, unapproved, synthetic-marked, or sufficiently spam/personal-information-flagged messages are excluded. This does not guarantee removal of all sensitive text, paraphrases, or upstream annotation errors. Source lookup remains a residual risk. | Number of affected route pairs | Training cases | Test cases | |---|---|---| | 0 | 841 | 190 | | 1 | 1,612 | 346 | | 2 | 562 | 131 | | 3 | 35 | 5 | | 4 | 8 | 2 | | 5 | 2 | 0 | | 6 | 0 | 0 | There are 193 training cases and 35 test cases with at least one minimal two-removal interaction. This is a subset of the cases above, not additional data. Training represents 3,057 linked source groups; test represents 674. Submission Format Write ./working/submission.csv with the exact ordered columns case_id,withdrawal_witnesses. Both columns are strings. Include every test ID once; row order may differ. Missing, extra, duplicate, null, or unknown IDs and missing, extra, duplicate, or reordered columns reject the submission. A real labeled training example is: | case_id | withdrawal_witnesses | |---|---| | case_798233ef281687693d29cc7c | [["W1"],[],["W1"],["W0+W2"],[],[]] | Here AB and AD change after W1 is withdrawn. BC changes only after both W0 and W2 are withdrawn. AC, BD, and CD remain stable within the allowed removal budget. Use test IDs in the actual submission. The JSON must have exactly six arrays, at most 15 strings per array, and at most 2,400 characters in the complete cell. Tokens are one ID W0-W5 or two distinct IDs separated by +. IDs must be available in the case. Order within a two-ID token and order of tokens within an array do not affect scoring. Duplicate sets, supersets of another listed set, extra nesting, numeric values, explanatory text, and malformed JSON are invalid. Standard JSON whitespace is allowed within the length cap. Evaluation Metric: Preference Stability Witness Score. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Score = 0.60 * WitnessScore + 0.25 * StabilityScore + 0.15 * CaseExactScore. | Component | Definition | Reason for weight | |---|---|---| | WitnessScore, 60% | Micro set F1 over exact (case, route pair, removal set) items. | Most credit requires finding the actual minimal causes, not merely predicting instability. | | StabilityScore, 25% | Balanced accuracy for stable versus affected route pairs. | Gives stable pairs equal class importance despite their prevalence. | | CaseExactScore, 15% | Fraction of cases with all six witness collections exactly correct. | Rewards a complete result without discarding partial discoveries. | Let TP count correctly predicted witness items, FP count invented items, and FN count missing true items across all evaluated cases. WitnessScore = 2TP / (2TP + FP + FN). If the denominator is zero, the component is 1: every pair is correctly stable. Matching uses exact sets of withdrawal IDs, not substring matching. Predicting unavailable IDs earns no witness credit and contributes false positives; the grader never maps them to a valid candidate. For each true pair class k, stable or affected, let N_k be its count and C_k the number with correctly predicted empty/nonempty status. StabilityScore = mean(C_k / N_k) over classes with N_k > 0 in the evaluated answers. A class absent from an evaluated subset is omitted. CaseExactScore = number of fully correct cases / number of evaluated cases. A malformed cell is not treated as an empty answer: its case receives no exact credit, all six pair statuses are wrong, every true witness is a false negative, and each pair adds one false positive. Means include every evaluated case. Malformed reference answers raise an error. No hidden labels are clipped or repaired. Local Checks | Submission | Score | |---|---| | Exact answers | 1.000000 | | Supplied sample | 0.199974 | | All pairs stable / training-mode constant | 0.167285 | | Infer local ranks by longer reply first, then enumerate removals | 0.323551 | | Infer local ranks by shorter reply first, then enumerate removals | 0.292280 | These are local diagnostics, not hosted-agent results or an upper bound on achievable performance. Modeling A practical starting point is a shared pretrained text encoder conditioned on a reply and its conversation prefix. Learn local preference estimates through the supplied witness labels, or predict pair-specific minimal sets directly. If using predicted pool rankings, the final exhaustive decoder needs at most 21 removal sets per case. Validate by conversation group and account for ties; reply length is not a quality label. What Not To Use Use public training data and locally available pretrained resources permitted by the platform. Do not retrieve evaluation annotations through source-text searches, external answer tables, source identifiers, or models specifically trained on hidden annotations. Do not predict from case IDs, row order, filenames, file sizes, or hashes. External inference services, other participants' outputs, and evaluator manipulation are prohibited. Content-based learning and legitimate local modeling are allowed; IDs and source lookup are not evidence of preference understanding. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 90 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen.
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Soil Laboratory-to-Field Horizon Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx712ypzb0aw5j98hf7zcwn79n8e4nt4
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dongfuhan's score of 0.638!

Full challenge description from page:

> Soil Laboratory-to-Field Horizon Matching Overview Soil laboratories and field-survey teams can describe the same vertical soil profile in different records, yet the sample-to-horizon links may be lost during migration or reconciliation. For each profile in this challenge, you receive an ordered set of field-horizon observations and a shuffled set of laboratory sample records. Your task is to recover the complete bipartite correspondence: assign every laboratory sample to the field horizon from which it came. This is a variable-size structured matching problem, not row-wise tabular classification or regression. Each answer is a profile-level graph represented as an ordered JSON mapping. Some field horizons have multiple distinct laboratory samples; these are native one-to-many relationships, and within-horizon sample order is undefined. The released data contain no raw sample keys, raw horizon keys, exact depths, horizon names, locations, timestamps, source paths, or source ordering. Public identifiers are opaque strings. The analytical panel is finite and complete, and every released particle-size composition is physically closed to 100 percent. Task For every test profile, use all horizons and all samples jointly. Return one matching_json object whose keys are the supplied horizon_id values in field order and whose values are lists of assigned sample_id values. Every horizon must receive at least one sample, every sample must appear exactly once, and no unknown identifier is permitted. The field view expresses relative textural evidence down the profile. The laboratory view contains particle-size, acidity, base-saturation, and cation-exchange readings. A useful model must combine cross-view compatibility with profile context, vertical trends, and the global assignment constraint; independently classifying samples and ignoring the rest of the profile is not the intended task. Generalization Contract Test profiles come from source groups not represented by the training profiles. Public IDs are independently opaque, presentation order is shuffled, and exact source-record lookup has been stress-tested against the named raw corpus. Solvers should validate on training-only group-like folds and expect unfamiliar combinations of profile length, laboratory patterns, and field transitions. Intended Approach and Validation Reasonable GPU approaches include a pair of train-from-scratch encoders for the field and laboratory views, DeepSets or set-transformer context blocks, graph neural networks over the candidate bipartite graph, listwise or contrastive compatibility learning, and differentiable assignment objectives. A practical pipeline can embed horizon tokens and continuous laboratory panels, score all sample-horizon pairs within a profile, add profile-context features, and apply a constrained decoder such as min-cost flow or linear assignment while ensuring every horizon is used. Use only released training labels for model selection. Build validation folds from whole profiles, monitor both exact assignment and cross-horizon ordering, test performance by profile length and one-to-many structure, and choose checkpoints without using test predictions or external records. Model parameters used for prediction must be initialized and trained on the provided challenge data. What Makes This Benchmark Different The novelty claim is not that bipartite matching, assignment solvers, or soil measurements are individually new. The benchmark contribution is their coupled scientific reconciliation contract: each case has unequal, variable cardinalities; the target is a native one-to-many provenance graph; the two public views use different evidence types; and the score separates exact sample membership from the vertical order induced by that graph. Field order is already supplied, so merely sorting records does not solve the task. Every laboratory sample must be used exactly once and every field horizon must be covered, but the number of samples belonging to a horizon is unknown. The closest platform tasks have materially different prediction units and outputs: | Reference task | Central output | Difference here | | --- | --- | --- | | Thermal Sensor Stack Ordering | A fixed four-item one-to-one spatial permutation of simultaneous thermal sequences | This benchmark predicts a variable-size, one-to-many sample-to-horizon graph with unequal set sizes; field order is an input, not the target. | | Ocean Core Sediment Correlation and Sensor Bridge Reconstruction | Selected core intervals, tie points, transition type, and imputed sensor windows | This benchmark has no interval selection, bridge imputation, transition classification, or confidence head; it requires exhaustive assignment of discrete laboratory samples to native field horizons. | | Conventional clean-clean entity matching | Independent pair matches, often followed by one-to-one assignment | Pair scores are only intermediate evidence here. The final output must be a legal surjective graph, may assign multiple samples to one horizon, and is evaluated jointly for membership and induced order under held-out source groups. | These distinctions are operational rather than cosmetic. A system can predict the vertical order of samples while assigning them to the wrong horizons, or recover several strong pairwise links while leaving an illegal uncovered horizon. Neither output is a usable reconciliation, and the disclosed metric measures those failures separately. What Not To Do The following approaches can cause solution rejection regardless of leaderboard score: Do not use external identity recovery, database lookup, source-row matching, hard-coded answer maps, or attempts to reconstruct removed depths, names, locations, or identifiers. Do not use public IDs, row order, JSON length, file size, hashes, archive metadata, or filesystem metadata as prediction channels. Do not replace learning with a fixed sort, regular expression, texture lookup table, hand-written depth rule, or template inversion. Diagnostics and features are allowed, but the final eligible pipeline must train a model appropriate to profile-level set matching. Do not use pretrained or fine-tuned models, external training data, teacher-model pseudo-labels, hosted inference APIs, or runtime internet access. Do not read private files, inspect grader internals, probe the filesystem for answers, exploit duplicate IDs or malformed JSON, or use any platform side channel. Enforcement on invalid approaches: a structurally valid CSV may still be rejected during solution review if the pipeline relies on source lookup, metadata-only shortcuts, hard-coded outputs, prohibited pretrained/external systems, private files, or a rule-only substitute for the required learned matching task. Evaluation The ranking metric is Profile-Macro Assignment and Order Score. Scores range from 0.0 to 1.0; higher is better, and a perfect answer file scores exactly 1.0. For one profile, assignment_accuracy is the fraction of laboratory samples assigned to their true field horizon. order_accuracy considers every pair of samples that truly belong to different horizons and measures the fraction whose predicted upper-to-lower relation matches the truth. Pairs from the same true horizon are ignored because their order is not defined. profile_score = 0.80 assignment_accuracy + 0.20 order_accuracy final_score = mean(profile_score over all test profiles) The grader aligns rows by profile_id; CSV row order has no effect. Wrong, extra, missing, or reordered columns; missing, extra, duplicate, blank, malformed, or unknown profile IDs; and row-count or ID-set mismatches raise a generic InvalidSubmissionError before scoring. A row-local malformed matching_json, wrong horizon order, duplicate or unknown sample, omitted sample, or empty horizon receives 0.0 for that profile only. Submitted JSON strings longer than 20,000 characters are treated as malformed rows before parsing. Dataset The public directory contains these files: train_profiles.jsonl: 12,000 profile objects with inputs only. train_labels.csv: 12,000 matching graphs for the training profiles. test_profiles.jsonl: 3,200 profile objects with inputs only. sample_submission.csv: all 3,200 test IDs with a valid weak cyclic assignment. metadata.json: observable row counts, allowed field tokens, and laboratory feature names. Each line of train_profiles.jsonl and test_profiles.jsonl is one JSON object with exactly these top-level fields: profile_id (string): opaque profile identifier matching ^P_[0-9a-f]{16}$. field_horizons (array): 3–12 horizon objects in upper-to-lower order. lab_samples (array): 3–16 shuffled laboratory sample objects. Each field_horizons object has exactly these fields: horizon_id (string): opaque horizon identifier. position (integer): supplied field order from 0 to the profile's horizon count minus one. observations (one-element string array): one of texture_transition:reference, texture_transition:coarser, texture_transition:similar, texture_transition:finer, texture_transition:subtle, or texture_transition:ambiguous. The first horizon uses reference; subtle means no signed transition is released, and ambiguous means the qualitative observation does not support a coarse/fine ordering. Each lab_samples object has exactly these fields: sample_id (string): opaque sample identifier. measurements (object): fourteen finite floating-point analytical readings with no blank, null, NaN, or infinite values. The measurements object has exactly these keys: sandvcmeasured, sandcomeasured, sandmedmeasured, sandfinemeasured, and sandvfmeasured: very-coarse through very-fine sand fractions, in percent by weight. sandtotmeasured, silttotmeasured, and claytotmeasured: total sand, silt, and clay percentages; these three values sum to 100.0 in every sample. siltcomeasured and siltfinemeasured: coarse and fine silt fractions, in percent by weight. ph1to1h2o and ph01mcacl2: dimensionless pH readings from water and calcium-chloride preparations. basesatsumcations: base saturation, in percent. cec7: cation-exchange capacity at pH 7, in centimoles of charge per kilogram. train_labels.csv has exactly two columns: profile_id is the opaque training profile identifier, and matching_json is the ordered target mapping described below. sample_submission.csv has the identical two-column schema for test IDs. metadata.json contains no labels or source identifiers. Submission Write ./working/submission.csv with exactly these columns in this order: profile_id (string): every test profile ID exactly once. matching_json (JSON string): an object whose keys are every supplied horizon ID in supplied field order and whose list values partition every supplied sample ID exactly once. Two valid-format rows from the weak sample are shown below. The assignments are placeholders, not labels. profile_id,matching_json P_f66c87795bf38c54,"{""H_0933513981714a75"":[""S_6303fa82a2c4b9ef""],""H_386578e582e1c1ff"":[""S_eaad78115c25ba98""],""H_da7a6b2f006d7c41"":[""S_4438207182874e4c""]}" P_c72489ca8d140729,"{""H_5b83ce57243c8b06"":[""S_0f4bbd30c0769a18""],""H_71a5f2e9f47db2df"":[""S_6a6b6bfe3af867fc""],""H_9cbcbe948629cdad"":[""S_ed218b4ea0377607""]}" Relation to Prior Work The nearest common soil-ML tasks predict a soil property, texture class, or horizon label from one record. This challenge instead removes the correspondence between two variable-size views of the same profile and scores recovery of the complete one-to-many matching graph plus its induced vertical order under held-out source groups. Unlike fixed-cardinality permutation recovery, field order is observed and allocation cardinality is hidden. Unlike generic entity resolution, every profile must produce a complete surjective graph rather than independent pair decisions. The target mechanism is scientific provenance reconciliation with global constraints, not property prediction, sequence ordering, interval correlation, or bridge-value regression.
> Closes in 21m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## PatchRoute: Counterfactual Repair Slate Selection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70c58sxqfeqvyz24sed9t4pn8e96nw
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mb_mb's score of 0.550!

Full challenge description from page:

> PatchRoute: Counterfactual Repair Slate Selection Overview A repair that removes one failure mode can create another, consume too much execution budget, or react badly when the operating regime changes. PatchRoute treats this as latent structural-equation decoding over an intervention response field. Each atomic case combines three synchronized evidence objects: an operating-context modality, a six-item intervention-design modality, and a five-condition diagnostic-response modality. The target is the unique intervention whose inferred outcome remains preferable after response dispersion, boundary behavior, nonlinear compatibility, and a context-controlled resource constraint are composed. The task is to identify that intervention. The submitted integer denotes a position inside the current case, not a reusable global action class. Candidate positions are independently shuffled, all six target positions are exactly balanced, and opaque IDs carry no decision signal. A useful solution must reconstruct a transferable context-to-intervention response law, aggregate the ordered probe conditions, and resolve the resulting six-way constrained choice. This is not ordinary vulnerability classification, behavioral-similarity scoring, direct resource-cost regression, or six independent binary decisions. A candidate can be optimal in one operating context and inferior in another, and none of the five probe conditions or released channels is individually sufficient. The evaluated object is a joint decision rule over the current six-candidate set. Objective For every row in test.csv, predict which of the six candidate positions should be recommended: 0 selects test_candidate[local_test_index, 0] and test_probe[local_test_index, 0]. 1 selects candidate slot 1. 2 selects candidate slot 2. 3 selects candidate slot 3. 4 selects candidate slot 4. 5 selects candidate slot 5. Exactly one position is correct in every slate. The hidden target is the position with maximum latent counterfactual utility for that case. Higher-quality systems should estimate a context-conditioned utility for every candidate and return the position with the highest estimate. Constraint-Reversal Decision Contract The six outputs are not reusable patch categories. They are mutually exclusive actions available only inside the current case, and their positions are freshly permuted after the winning action has been determined. Solvers must therefore infer a relative ordering for the whole slate rather than learn a global class meaning. The five probe conditions are not repeated measurements of one pass/fail test. Each condition applies a different anonymous transformation of the shared context and candidate design. Hidden utility uses complementary statistics across that intervention axis: mean beneficial response, cross-intervention dispersion, boundary-condition responses from the first and fifth probes, and nonlinear context-candidate interactions. An intervention that looks strongest under one probe can lose because disagreement across the other four indicates unstable behavior. The decision also contains a constraint reversal. Resource burden is multiplied by a monotone function of the current case budget: the same expensive candidate is penalized strongly in a constrained case and weakly in a permissive case. Because this penalty competes with efficacy and compatibility rather than being applied after prediction, changing the shared context can reverse the order of two otherwise identical candidates. The answer is therefore neither the best single-probe response nor the globally strongest candidate profile. Public tensors expose the five-condition response field but not the realized residual outcome used to choose the winner. Training labels teach how the observable probe-disagreement and budget-reversal pattern predicts the latent decision; evaluation asks whether that rule transfers to complete operating regimes excluded from training. Three-Stream Tensor Modalities The public input is a synchronized tensor bundle, not a single feature table. Its channel positions are stable so models can learn recurring cross-modal interactions, but the release contains no original program text, contract address, function name, source path, developer identity, timestamp, or global intervention label. The context modality is a 12-channel state tensor describing the operating environment, workload pressure, and constraints shared by all six candidates. The intervention modality is a six-by-ten set tensor describing anonymous candidate characteristics such as structural change, resource demand, and compatibility proxies. The response modality is a six-by-five-by-four tensor: for every candidate it preserves five diagnostic conditions, four response channels, and the ordering needed to measure boundary responses and cross-condition dispersion. Context and candidate values lie in [-2.5, 2.5]. Probe values lie in [-1, 1]. These modalities have different axes and semantics and must be aligned by case and candidate slot before fusion. Flattening them is permitted as a baseline, but independent row-wise treatment destroys the set axis, probe-condition axis, and shared-context relationship on which the target depends. Individual maxima or minima do not define the answer. Operational Grounding and Abstraction Boundary The reviewer-private build begins from a checksum-pinned collection of real program artifacts with associated structural summaries, audit findings, execution-resource profiles, and policy annotations. Those records are used only to define empirical archetypes and correlations for the simulation. They are not treated as ready-made labels, and the benchmark never claims that an upstream annotation identifies a correct repair. For every archetype, the build creates independently perturbed operating regimes and generates intervention slates around those regimes. Observable context, candidate, and probe tensors inherit distributional structure from the verified artifacts; the final decision target is then produced by the documented counterfactual utility mechanism. Raw program text, names, paths, addresses, audit prose, source identifiers, and original labels remain outside solver-facing files. This preserves operational grounding without turning source retrieval into a solution method. Dataset Files train.csv contains 20,160 labeled recommendation cases. test.csv contains 5,040 unlabeled recommendation cases. train_fold.csv provides anonymous five-fold assignments that keep nuisance regimes intact. train_context.npy and test_context.npy store one 12-value context vector per case. train_candidate.npy and test_candidate.npy store six 10-value candidate profiles per case. train_probe.npy and test_probe.npy store five four-channel diagnostic responses for every candidate. sample_submission.csv provides the exact submission schema. data_manifest.json records array dimensions, bounds, balance, split semantics, and public-file checksums. The arrays are separated into training and test files. Always use the array_index supplied in the corresponding CSV instead of assuming a CSV row position. Public Columns train.csv contains exactly three columns: id is a stable opaque case identifier. array_index selects the matching training tensor row. target is the relevant candidate position, represented by an integer from 0 through 5. test.csv contains id and array_index but omits target. Training array_index values run from 0 through 20159 and index the training tensors directly. Test values run from 20160 through 25199; compute local_test_index = array_index - 20160 before indexing a test tensor. train_fold.csv contains id and fold. Fold values run from 0 through 4. Join folds to training cases by id; do not assume that file order carries meaning. The tensor shapes are (N, 12) for context, (N, 6, 10) for candidate profiles, and (N, 6, 5, 4) for probe responses. Candidate axis position is shared between the candidate and probe tensors within a case. Construction and Split Controls One intervention case produces one scored row. Consequently, the platform's public/private assignment cannot split an independent case between leaderboard slices. Each scored row is one complete anonymous operating regime: its shared context, active constraint, six candidate designs, and all five probe responses are drawn together as one atomic slate. Training contains 20,160 such regimes and evaluation contains 5,040 different regimes. No latent nuisance realization is reused across rows. The supplied five-fold training split assigns every complete regime to exactly one fold and balances the hidden archetype and target strata. Each underlying archetype contributes 960 regimes to training and 240 to evaluation. Hidden utility is computed before candidate positions are randomized. Every target position occurs 3,360 times in training and 840 times in evaluation. Released row order is independently shuffled. Exact context-candidate-probe rows are deduplicated, and the final audit reports zero ID, nuisance-regime, or complete-feature crossings between training and evaluation. The sample template is balanced independently of the target. Across evaluation, each target-position and template-position pair occurs exactly 140 times. The sample submission therefore cannot be inverted to recover an answer. Constraint-Shift Evaluation Protocol The split is designed around atomic operating regimes. A regime jointly perturbs contextual pressure, candidate characteristics, probe responses, and the effective resource constraint, and it produces exactly one scored slate. Therefore Shipd's row-level visibility assignment also places the complete independent unit on one leaderboard side. Evaluation regimes are absent from training, and each training regime belongs to exactly one validation fold. This prevents interpolation between cases sharing a constraint realization while retaining 5,040 independent evaluation units for stable scoring. The generalization requirement is therefore crossed: a solver must transfer both across unseen nuisance conditions and across the context-dependent reversal between efficacy and cost. The six-way output and Hit@1 metric remain simple, but the item being scored is whether the model routes the complete candidate set correctly after that coupled shift. Random-row accuracy, a fixed global patch ranking, and a cost-only rule cannot satisfy this contract. Why Generalization Is Learnable Training and evaluation share the same anonymous feature system and intervention semantics while using disjoint nuisance regimes. A model can therefore learn reusable candidate utility without receiving an evaluation lookup key. For context c, candidate profile x_j, and the five-condition probe block p_j, a useful model family estimates: utility(j | c, x_j, p_j) = profile_effect(x_j) + bilinear_context_effect(c, x_j) + intervention_moments(p_j) + nonlinear_compatibility(c, x_j) - budgeted_cost(c, x_j) The recommendation is the slot with maximum estimated utility. The target is not the best response on any single probe and is not derived from similarity to a reference repair. Compact fusion networks, candidate-wise encoders with shared weights, attention across the slate, and permutation-equivariant set models can preserve all three tensor structures. Flattened linear and boosted controls are useful diagnostics but intentionally discard part of the multimodal organization. Use train_fold.csv for the preregistered, balanced validation partition. Its fold labels were assigned before source archetype information was removed from the solver-facing release. Submission Format Submit one CSV containing exactly these columns in this order: id,prediction ptr_0123456789abcdef01234567,4 ptr_fedcba9876543210fedcba98,1 For every test case: copy id unchanged from test.csv; provide one prediction from 0 through 5; include every required ID exactly once; do not add, remove, rename, or reorder user columns. CSV row order does not affect scoring. Wrong columns, missing IDs, duplicate IDs, unexpected IDs in a full submission, Boolean values, and invalid structure raise an explicit error. An isolated non-numeric, non-finite, fractional, or out-of-range prediction is counted as incorrect only for that case rather than invalidating the other rows. Evaluation The base measurement is recommendation Hit@1, implemented as candidate-position accuracy. Because all six target positions are exactly balanced, the leaderboard removes accuracy available from chance: score = max(0.001, (accuracy - 1/6) / (5/6)) A constant position, the balanced sample template, or another chance-level system reaches the platform-safe floor 0.001. A perfect recommender scores 1.0. Higher is better; the grading configuration is Maximize with minimum 0.001 and maximum 1.0. Progressively replacing increasing fractions of oracle predictions with guaranteed-wrong positions produces a strictly decreasing score ladder. The grader aligns predictions by answer-side id, so submission row order cannot change the result. The same deterministic scorer supports the platform's full, public, and private answer subsets. Anti-Shortcut Evidence The audit evaluates every constant slot, array-index cycles, minimum and maximum rules for every candidate dimension, minimum and maximum rules for every probe channel, the balanced sample template, and 64 independently salted ID rules. Constants, the template, and index cycles remain at the 0.001 floor. The strongest no-training single-feature rule scores 0.1369, below the intended learned range. Three preregistered trained controls score 0.3433, 0.4352, and 0.5038. They progress from a compact linear candidate model to an interaction-aware linear model and a boosted interaction model. Adjacent learned-control gaps are 0.0919 and 0.0686. Twenty corruptions with exactly the same number of guaranteed-wrong regimes all score 0.4000, with zero measured range; equal full-set quality is no longer confused with variable error counts. Across 100 independent-regime, class-stratified 30/70 visibility assignments, mean absolute public/private gaps range from 0.0126 to 0.0146. The largest public-score standard deviation is 0.0126; adjacent trained-control gaps are 7.30 and 5.45 times that value, and their order is stable in every simulated public and private slice. Candidate positions, IDs, array indexes, row order, target frequency, and individual tensor extrema therefore do not explain the learned scores. The actual server-generated visibility split must still be audited after preparation before agent runs begin. Research Positioning and Novelty The nearest established formulations expose a persistent candidate identity, an independently scored patch, a reference behavior, a logged action and reward, or an optimization target defined before the diagnostic interventions are observed. PatchRoute exposes none of those objects. Its primitive observation is instead a synchronized response field: one anonymous operating state, six ephemeral interventions, and five ordered transformations applied to every intervention. Correctness is not an attribute of one candidate in isolation. It is induced after three coupled operations: estimating stability from the complete five-condition trajectory, applying a context-dependent constraint that can reverse pairwise preferences, and resolving a one-of-six decision after all positions have been freshly permuted. Two candidates with identical marginal efficacy can exchange order when either the boundary probes or the shared constraint changes. Consequently, independent correctness classifiers, fixed global rankings, cost-first filters, single-probe retrieval, and propensity-based estimators do not implement the scored rule. The evaluation protocol makes this distinction testable rather than terminological. Every scored case is a complete regime; evaluation contains 5,040 unseen regimes; six output positions are exactly balanced; and the leaderboard removes the one-sixth chance component. Audited separable rules remain below 0.137, while increasingly expressive cross-stream controls form a stable 0.343, 0.435, and 0.504 ladder on the same hidden cases. Their order is preserved across all 100 simulated public/private assignments. The benchmark therefore measures recovery of a nonseparable constraint-reversal law from an intervention-indexed tensor field, not reuse of a standard candidate score or a favorable visibility split. Compute Requirement This is a CPU multimodal challenge. The public tensors are compact, and a complete pipeline using a shared candidate encoder plus cross-stream fusion trains in minutes on the 10-core CPU tier. A small permutation-aware set network is feasible, but pretrained models and large accelerators are unnecessary. A careful end-to-end run, including grouped validation, modality alignment, tensor fusion, training, and inference, should fit within approximately 10 to 15 minutes on the CPU tier. Domain PatchRoute belongs to the Multimodal domain. It requires fusion of a global context tensor, a candidate-set tensor, and an intervention-response tensor with different ranks and semantics. The output is one decision over their joint structure. It is not a conventional tabular challenge: CSV files contain only opaque IDs, array addresses, folds, and labels, while all predictive inputs reside in the three aligned NumPy tensor modalities. Rules Use only the supplied solver-facing challenge files. Do not use external datasets, pretrained models, web lookup, source-code search, or manual labeling. Do not attempt to identify, retrieve, or reconstruct upstream source materials. Do not use IDs, array indexes, row order, candidate-position frequency, file metadata, or platform metadata as prediction signals. Treat every prediction as a position inside its current shuffled slate, not as a global intervention label. Do not probe the evaluation set through repeated submissions or pseudo-label private cases. Submit only the required id,prediction CSV and keep the full solution within the CPU resource limit. &nbsp;
> Closes in 34m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Modal Vessel Re-Identification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74fgpqn8ky4518qcsejac6md8e63xn
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mb_mb's score of 0.652!

Full challenge description from page:

> Ship Track Assembly Overview A maritime imagery analyst has manually reconciled ship tracks in several acquisition collections and needs to assemble consistent inventories for new collections. You receive optical and radar crops from multiple visits. Assign a track label to every test crop so that observations of the same vessel in the same collection share a label. False merges combine different vessels; fragmented tracks count the same vessel more than once. Solve each collection jointly. Test acquisition collections and their vessels do not occur in training, so your method must transfer learned appearance relationships across acquisition conditions. There is no labeled reference gallery for a test vessel, supplied test track count, absolute vessel identifier, position, or motion model. Use appearance across all available visits, image dimensions, and modality. Track names are arbitrary and scoped to one collection; their spelling and their relationship to training label names have no meaning. Your complete solution must run on CPU, use no more than 62 GB of RAM, and finish within 90 seconds. This includes preprocessing, training, validation, inference, and submission writing. Dataset dataset/public/ ├── train.csv ├── test.csv ├── sample_submission.csv └── images/ ├── obs_.png ├── obs_.npy └── ... Each row is one distinct ship crop. Training contains 1,008 rows and 299 annotated tracks from six acquisition collections. Test contains 454 rows from seven entirely held-out acquisition collections. No test collection, annotated identity, or image occurs in training. Predict relationships between test observations rather than reusing training labels as a class vocabulary. For validation, hold out complete acquisition collections. Never split rows from one collection between fitting and validation, because that would expose its vessels and acquisition-specific appearance. The evaluation measures transfer to unseen collections, but unavailable site and global-vessel provenance prevents a stronger geographic-independence claim. Collections vary in size and modality mix, and some are radar-only. There are two to five visits per collection, observation availability is incomplete, and standalone observations with no retained counterpart occur. train.csv id,collection,visit,modality,image_path,track | Column | Type | Meaning | |---|---|---| | id | String | Unique observation ID: obs_ followed by 24 lowercase hexadecimal characters. | | collection | String | Acquisition collection. Association is evaluated within this scope. | | visit | String | Acquisition visit within its collection. Visit token spelling and order do not encode chronology, identity, or similarity. | | modality | String | RGB for optical imagery or SAR for radar imagery. | | image_path | String | Relative path from dataset/public/ to this observation's image. | | track | String | Annotated vessel correspondence: equal labels within a collection mean the same vessel. | The inputs contain only named ship observations with finite, nonnegative, nonconstant pixel arrays. A track may have missing visits or only one remaining observation. Do not force a counterpart for every observation. No track has more than one annotated observation in the same visit. Predicted groups that violate this physical property remain syntactically valid submissions and incur false-association penalties through the metric. Optical files are RGB PNG images with unsigned 8-bit pixel values. Radar files are NumPy .npy arrays with shape (height, width), dtype float32, and one intensity channel; load them with numpy.load(path, allow_pickle=False). Their numerical values are not calibrated physical ship measurements. Image dimensions vary, and crop margins affect apparent ship size. Nominal ground sampling distances are 0.75 metres per optical pixel and 1 metre per radar pixel. Crop orientation may differ by a half-turn, so top versus bottom is not a fixed bow-direction cue. Preserve aspect ratio when comparing dimensions. The files contain no missing CSV values. Every referenced image is present. All images are individual model inputs, and their filenames are opaque identifiers. There is no geographic coordinate or precise timestamp available for association. test.csv id,collection,visit,modality,image_path These input fields have the same meaning as in training. All test observations are available together, and joint inference within each collection is permitted and useful. Cross-collection label equality is ignored: the same chosen track name can be reused in different collections without asserting a shared vessel. sample_submission.csv id,track The sample assigns every test observation its own label. This is a valid format example and predicts no associations. It scores zero in any scoring collection that contains at least one true pair; a collection with no true or predicted pairs scores one. Use the sample IDs as the submission inventory. Submission format Write working/submission.csv with required columns id,track. Include exactly one row for every observation in the supplied test cohort. Rows and columns may be reordered; additional uniquely named columns are ignored. Missing or misspelled required columns, duplicate headers, missing/extra IDs, and duplicated rows are invalid. For an invented example, consider two observations in collection example_area: an RGB crop from visit early at images/example_optical.png and a SAR crop from visit later at images/example_radar.npy. Their observation IDs are the two IDs below. Suppose they show the same vessel, with corresponding hull proportions and superstructure placement despite different imaging appearance. Both predictions use ship_A, establishing one association: id,track obs_000000000000000000000001,ship_A obs_000000000000000000000002,ship_A These invented paths and IDs explain the format; they are not additional dataset files. If the observations instead showed different vessels, their labels should differ. If an observation has no counterpart, give it a unique label. A label reused in another collection refers to a separate track there. Track labels must be strings of 1–64 ASCII characters, beginning with a letter and continuing with letters, digits, underscores, or hyphens. The number of rows must still match the supplied test cohort exactly. A DataFrame interface, where available, applies the same required-field types, row/column limits, unique-header rule, and field-length limit. Invalid submissions are rejected in full rather than repaired or partially scored. Evaluation The score is a float in [0.0, 1.0], with higher values better. For each collection, consider all unordered pairs of distinct observations in that scoring cohort. Let P be the set of pairs assigned the same predicted track label and G the set assigned the same annotated track label. The collection score is pairwise F1: F1 = 2 × |P ∩ G| / (|P| + |G|) If both sets are empty, the collection score is 1. If exactly one is empty, it is 0. Pairs from the same visit are included: merging two distinct observations from one visit produces false-positive pairs. There are no confidence thresholds, ranking ties, or label-name matching steps. Renaming predicted tracks without changing their membership leaves the score unchanged. The final score is the unweighted arithmetic mean of collection scores represented in the supplied scoring cohort. Each collection contributes equally despite different row counts. If a cohort contains only part of a collection, its pair sets are formed only from the observations supplied for that call. No cross-collection or out-of-cohort pair contributes. Internal calculations are not rounded before aggregation. Perfect correspondence reaches 1. Predicting no pairs when true pairs exist reaches 0. Splitting a true track loses correct associations; merging vessels introduces incorrect associations. Singletons do not earn true-positive pair credit, but incorrectly merging them creates false positives. Copying a fraction of correct row labels need not earn that fraction of the score because each association depends on two rows and the aggregation weights collections equally. Not allowed Do not use external training data, remotely hosted models, paid or free inference APIs, source-dataset downloads, source-to-answer lookup, or manually supplied test correspondences. Do not hardcode predictions for test observation IDs or reconstruct source identities from filenames or hashes. &nbsp;
> Closes in 1h 54m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Perimeter Acoustic Drone Tracking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72a672hxbw4292p2a62t20g18e1n7k
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 88.574!

Full challenge description from page:

> Perimeter Acoustic Drone Tracking Overview Every recording in this challenge is simulated. No physical microphones, aircraft or field recordings were involved. Each scene is synthesised from a physical forward model of outdoor sound propagation, and the ground truth is the set of parameters that model was given. The scenario below describes what the simulation represents. The simulated setting is a six-microphone array around the perimeter of a protected site. Small rotor-driven aircraft pass through the surrounding airspace, their motors emitting a harmonic acoustic signature that the array picks up against a noisy outdoor background. Three things must be recovered from every recording: how many aircraft came close enough to matter, exactly when each was inside the protection radius, and where each was and how fast it was travelling. You are given 8-second, 6-channel recordings. For each one, report every aircraft that came within 80 metres of the array centroid, with the time interval it spent inside that radius, its compass bearing, and its ground speed. The simulation is physically consistent: propagation delay, Doppler shift from radial motion, spherical spreading, atmospheric absorption and ground-reflection multipath are all rendered from the same forward model. Differences between the six channels are therefore genuine spatial information rather than noise. Three properties of this task deserve emphasis before you start. Audibility is not the target. The labelled interval is defined purely by geometry: the span during which the aircraft's slant range from the array centroid is below 80 metres. An aircraft is frequently audible for the whole 8-second recording while its labelled interval covers only a fraction of it, and some audible aircraft are never labelled at all because they never come within 80 metres. Detecting that a sound is present is not sufficient; you must infer range. The array layout changes in every scene. Aperture, microphone arrangement and mast heights are redrawn per recording, and the mapping from channel index to physical position is shuffled independently each time. The layout that recorded each scene is supplied. A spatial signature memorised from training will not transfer; the coordinates have to be read and the propagation geometry inverted. The background is adversarial. Recordings may contain bird-like frequency sweeps crossing the rotor band, gusting wind, and a stationary generator with its own harmonic series. Evaluation Submissions are scored on a tIoU-weighted multi-task score in the range [0, 100], which is maximised. Matching Within each scene, predicted intervals are matched one-to-one against ground-truth intervals by maximising total temporal Intersection over Union (an optimal assignment, not greedy). For a predicted interval p and a ground-truth interval g: tIoU(p, g) = overlap(p, g) / union(p, g) A matched pair with tIoU = 0 is not counted as a detection. After matching, each scene yields TP (matched pairs with positive overlap), FP (predicted intervals left unmatched) and FN (ground-truth intervals left unmatched). Score Sums run over all matched pairs in all scenes: bearing_credit = max(0, 1 - bearing_error_deg / 60) speed_credit = max(0, 1 - speed_error_mps / 10) numerator = 0.50 * Σ tIoU 0.30 Σ tIoU bearing_credit 0.20 Σ tIoU speed_credit denominator = Σ (TP + FP + FN) score = 100 * numerator / denominator bearing_error_deg is the absolute circular difference between predicted and true bearing, wrapped to [0, 180]. speed_error_mps is the absolute difference in m/s. Bearing and speed credit are weighted by the tIoU of their match, so a prediction that barely overlaps a real aircraft earns correspondingly little credit for its bearing and speed. Aggregation is global across all scenes rather than a mean of per-scene scores. Every hallucinated detection enlarges the denominator, so predicting extra aircraft to improve recall is penalised directly. Dataset All paths are relative to the public directory supplied at runtime. audio.npy int16 array of shape (N, 6, 25600) holding every scene, training and test. Row i is one 8-second recording with 6 channels at a 3200 Hz sample rate. Channel c corresponds to row c of that scene's entry in geometry.npy. Index into it with the row_index column of train.csv or test.csv. Load with np.load(path, mmap_mode='r') to avoid reading the whole array into memory. Each scene is peak-normalised independently, so absolute amplitude carries no meaning across scenes. Relative amplitude across the six channels within a scene is physically meaningful. geometry.npy float32 array of shape (N, 6, 3), aligned with audio.npy on the first axis: geometry[i] is the microphone layout that recorded audio[i]. Each row is (x, y, z) in metres relative to the array centroid, with z the mast height above the ground plane. Layouts are drawn from several structural families (regular and irregular rings, two separated clusters, and microphones scattered within a disc) and within each family the arrangement is sampled continuously, so no two scenes share a layout. The test split additionally contains a layout family that appears nowhere in training: microphones distributed along a site boundary rather than surrounding the airspace. train.csv One row per training scene, with labels. Per-aircraft values are semicolon-separated lists ordered consistently across the three list columns: the k-th entry of each describes the same aircraft. A scene containing no aircraft has drone_count of 0 and -1 in each list | Column | Type | Description | |--------------|------|-------------------------------------------------------| | row_index | int | Index into audio.npy and geometry.npy | | scene_id | str | Scene identifier | | drone_count | int | Number of labelled aircraft in the scene | | intervals | str | start-end seconds, e.g. 1.42-3.87;5.10-6.44 | | bearings | str | Degrees in [0, 360) at each interval midpoint | | speeds | str | Ground speed in m/s | Both splits include scenes containing no aircraft. Correctly reporting nothing for those scenes is part of the task: every false positive is penalised, and scenes may additionally contain distant unlabelled aircraft that must not be reported. train_detections.csv The same training labels in one-row-per-aircraft form, joined to train.csv on scene_id, with four extra fields. Scenes containing no aircraft contribute no rows. | Column | Type | Description | |-----------------|-------|----------------------------------------------------| | scene_id | str | Scene identifier | | detection_index | int | Aircraft index within the scene, from 0 | | start_s | float | Interval start in seconds | | end_s | float | Interval end in seconds | | bearing_deg | float | Bearing in degrees, [0, 360) | | speed_mps | float | Ground speed in m/s | | f0_hz | float | Rotor fundamental frequency in Hz | | blades | float | Rotor blade count | | altitude_m | float | Altitude in metres | | impact_m | float | Horizontal closest-approach distance in metres | The last four columns are auxiliary information available for training only. They are not part of the submission and are not provided for the test set. They are included because they may be useful as additional supervision targets: both altitude and closest-approach distance constrain the range inference that the interval target depends on. test.csv | Column | Type | Description | |-----------|------|------------------------------------------| | row_index | int | Index into audio.npy and geometry.npy | | scene_id | str | Scene identifier | Predict one row per test scene. Conventions Bearing is atan2(y, x) in degrees wrapped to [0, 360), measured from the array centroid — the origin of that scene's geometry.npy coordinates — evaluated at the midpoint of the labelled interval. Times are in seconds from the start of the recording, in [0, 8]. The speed of sound is 343 m/s. Aircraft travel at 25–60 m/s. What Not To Use These restrictions apply in addition to the general Eris solver rules. A solution breaching any of them will be rejected regardless of its score. Do not reconstruct the source data or its generating process. The recordings are simulated by a deterministic physical model driven by a private master seed. Reimplementing that generator, searching for the seed, regenerating candidate scenes and matching them against the released audio, or fitting the forward model in order to read off its parameters rather than infer them from the signal, are all prohibited. This includes partial reconstruction of any single scene. The targets must be inferred from the released recordings themselves. Do not use the test set for anything beyond single-scene inference. Pseudo-labelling, test-time adaptation, reweighting training samples using test data, and calibrating predictions against the test set's overall distribution are all prohibited, even though no test labels are provided. A technique that needs visibility across the whole test set before predicting would not hold up in a real deployment. Do not bring in external data. No datasets beyond the one supplied, and no audio gathered elsewhere. Generating your own synthetic drone audio and training on it is also prohibited, including by reusing any generator inferred from this data. Do not hardcode what the model should learn. Fixed thresholds, lookup tables or constants derived offline from the training labels, substituted for a learned mapping, do not count. If a pattern in the data is worth exploiting, the model must learn it during training inside the submission script. Do not use self-trained weights from outside the submission script. General-purpose pretrained backbones loaded at runtime are fine. Weights you fine-tuned elsewhere and published are not: all fitting to this task has to happen inside the run. Design Rationale Why this metric measures the intended quality The task is only solved if a system reports the right number of aircraft, at the right times, in the right places, moving at the right speeds. A metric rewarding any one of those in isolation would admit degenerate solutions: a pure detector that never localises, or a localiser that fires constantly. The score is therefore a single quantity in which credit for bearing and speed is conditional on having detected the aircraft at all, and in which every spurious detection is charged against the total. The following strategies score near zero by construction: predicting nothing, predicting one aircraft spanning the full window in every scene, tiling every scene with intervals to maximise recall, and predicting the correct count with arbitrary intervals, bearings and speeds. None represents progress on the task, and none is rewarded. Weights The 0.50 / 0.30 / 0.20 split over detection-and-timing, bearing and speed reflects both dependency and difficulty. Detection and timing carry the largest weight because they are prerequisite: bearing and speed credit is multiplied by the tIoU of the match, so a system that cannot localise an aircraft in time cannot earn the other two components at all. Bearing is weighted above speed because it is recoverable from cross-channel structure present whenever the aircraft is audible, whereas speed depends on resolving Doppler curvature and degrades more sharply at low signal-to-noise ratio. Weighting speed equally would let the noisiest of the three estimates dominate the score. Tolerances 60 degrees and 10 m/s are calibrated so that an uninformed predictor earns approximately zero credit rather than partial credit. The mean absolute circular error of a uniformly random bearing guess is 90 degrees, beyond the 60-degree cutoff, so guessing earns nothing. The standard deviation of the speed distribution is about 10 m/s, so predicting the distribution mean for every aircraft also earns approximately nothing. Both tolerances are anchored to the point where a submission begins carrying real information rather than to an arbitrary round number. A system achieving 20-degree bearing accuracy earns two-thirds of the available bearing credit; one achieving 3 m/s speed accuracy earns seven-tenths of the speed credit. Matching and aggregation Predicted and ground-truth intervals are matched by optimal assignment rather than greedily, so the score does not depend on the order in which a submission lists its predictions. Two submissions containing the same set of predictions always receive the same score. Credit for bearing and speed is weighted by the tIoU of the match rather than gated behind a fixed IoU threshold. A threshold would introduce an arbitrary constant and a discontinuity that submissions could be tuned against; weighting degrades smoothly and needs no such constant. Aggregation is global across all scenes rather than an average of per-scene scores. Roughly one scene in six contains no aircraft, and per-scene averaging would require a convention for the resulting zero-over-zero case. Awarding full marks for a correctly empty scene would hand a submission that predicts nothing a large free score unrelated to any capability. Under global aggregation such a submission scores exactly zero, while a false positive in an empty scene still enlarges the denominator and is penalised. Split design The split is stratified on aircraft count and balanced across microphone layout families. Layout families differ substantially in how easily bearing can be resolved (a wide, well-spread array is far more informative than a narrow one) and because scoring is aggregated globally rather than per scene, an unbalanced test set would let the easiest families set the score. One layout family is withheld from training entirely and capped at a fifth of the test split, so that transfer to an unseen arrangement is measured without letting it dominate the result. Submission Write a CSV with exactly these columns, one row per test scene: | Column | Type | Description | |-------------|------|--------------------------------------------------------| | scene_id | str | Identifier from test.csv, unique within the file | | drone_count | int | Number of aircraft you predict | | intervals | str | Semicolon-separated start-end times in seconds | | bearings | str | Semicolon-separated degrees in [0, 360) | | speeds | str | Semicolon-separated ground speeds in m/s | The three list columns are ordered consistently: the k-th entry of each describes the same aircraft. Example: scene_id,drone_count,intervals,bearings,speeds sc_2qg8f3sc,1,1.42-3.87,214.6,38.20 sc_9k4mtp7w,0,-1,-1,-1 sc_bn3xq82v,2,0.00-1.70;3.51-6.71,45.2;301.8,52.10;29.44 Requirements Exactly one row per scene in test.csv, with a header row, and no columns beyond the five listed above. scene_id must be unique. drone_count must be an integer. A fractional value such as 1.9 is rejected rather than truncated. drone_count must equal the number of entries in intervals, and intervals, bearings and speeds must all have the same number of entries. end must not precede start in any interval. To predict no aircraft for a scene, set drone_count to 0 and write -1 in intervals, bearings and speeds. This is the convention used in sample_submission.csv. Empty fields are also accepted. A row violating these rules is scored as predicting nothing for that scene, which costs a false negative for every aircraft actually present. &nbsp;
> Closes in 3h 37m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## RNA Cleavage Site Prioritization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e13hq2ms1hr3ewg9khz2hc98dwgzr
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pokymono's score of 0.406!

Full challenge description from page:

> Overview For each gene, rank every supplied RNA cleavage-site candidate from highest to lowest observed usage after a cellular perturbation. The prediction is one complete ordered shortlist, not a probability or expression value. The cases come from a human-cell experiment in which several cleavage sites can compete within one terminal exon. Each candidate is represented by a long transcript-oriented DNA window and its distance from the first candidate. Experimental replicate counts define the hidden order. A useful model must compare local sequence motifs, broader nucleotide context, and the other candidates presented for the same gene. This mirrors a practical assay-prioritization decision. A laboratory may be able to validate only the most strongly used candidates first, while still needing a reliable ordering of the remaining sites. The learning problem therefore rewards the first recommendation, the complete pairwise ranking, and every exact rank position. Dataset The prepared collection contains 2,453 training genes and 491 test genes. Genomically overlapping sequence windows and detected homologous site centers are grouped before splitting. No such component occurs in both partitions. Training validation groups are supplied separately so the feature columns of train.csv and test.csv remain identical after removing the target. | File | Contents | |---|---| | train.csv | Input columns plus the observed site_order target | | test.csv | Input columns only | | sample_submission.csv | A schema-valid ordering baseline for every test ID | | train_groups.json | Opaque training IDs with a five-way grouped validation fold | | sequences/*.json | One candidate-sequence packet per gene | Input Columns | Column | Type | Description | |---|---|---| | id | string | Opaque case identifier used only to align rows | | sequence_path | string | Relative path such as sequences/rna_ab12...json | | n_sites | integer | Number of candidates in the packet, from 2 through 32 | train.csv contains id,sequence_path,n_sites,site_order. test.csv contains id,sequence_path,n_sites in the same input-column order. Each sequence packet is a JSON object with these fields: | Field | Type | Description | |---|---|---| | sequences | array of strings | One 2,049-base DNA window per candidate, in transcript 5-prime to 3-prime order | | offsets | array of integers | Genomic distance in bases from candidate s0; order matches sequences | | cleavage_index | integer | Zero-based cleavage position within every sequence window, always 1,536 | The DNA window contains 1,536 upstream bases, the cleavage nucleotide, and 512 downstream bases. Reference-masked positions may contain N. Candidate token sj refers to element j of both packet arrays. Target site_order is a string containing every candidate token exactly once, joined by >. The first token is the most-used site and the last token is the least-used site. Experimental usage is the mean relative read fraction across three quality-controlled biological replicates. Exact ties are resolved by the supplied candidate index. For four candidates, a valid target is s2>s0>s3>s1. It means candidate s2 ranks first, s0 second, s3 third, and s1 fourth. The candidate-count distributions are: | n_sites | Training rows | Test rows | |---:|---:|---:| | 2 | 1,240 | 264 | | 3 | 623 | 131 | | 4 | 337 | 50 | | 5 | 158 | 27 | | 6 | 60 | 11 | | 7 | 17 | 5 | | 8 | 6 | 3 | | 9 | 9 | 0 | | 10 | 2 | 0 | | 15 | 1 | 0 | Submission Format Write ./working/submission.csv with exactly these columns in this order: | Column | Required type | |---|---| | id | exact test identifier string | | site_order | complete >-separated candidate permutation | Example: | id | site_order | |---|---| | rna_0008523e6bc29f0590b3ca6c | s2>s0>s3>s1 | For a row with n_sites=K, valid tokens are exactly s0 through s(K-1). Every token must appear once. The field may contain at most 32 tokens and 255 characters. Missing candidates, repeated candidates, spaces, alternate separators, negative indices, and out-of-range indices make that row malformed and give it zero component credit. Submit every test ID exactly once. Row order may differ. Extra columns, reordered columns, duplicate columns, missing or unknown IDs, duplicate IDs, and wrong row counts are rejected. When the backend adds a trailing visibility column to both evaluation tables, the two schemas must still match exactly and that column is not scored. Evaluation The Cleavage Candidate Ranking Score ranges from 0.0 to 1.0, and higher is better. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Score = 0.55 P + 0.25 R + 0.20 F. | Component | Weight | Why it is included | |---|---:|---| | P, pairwise order fidelity | 55% | Measures whether every candidate pair appears in the correct relative order | | R, rank-position fidelity | 25% | Rewards placing candidates at their exact observed ranks | | F, first-choice fidelity | 20% | Preserves the operational importance of the top recommendation | Let a test row contain K candidates. Let pair_agreement be the fraction of its K(K-1)/2 unordered candidate pairs whose relative order matches the hidden order. Let position_accuracy be the fraction of candidates placed at exactly the correct rank. Let first_accuracy be 1 when the first candidate is correct and 0 otherwise. The three raw values are averaged across all test rows. Each mean is then cubed: P = mean(pair_agreement)^3 R = mean(position_accuracy)^3 F = mean(first_accuracy)^3 Cubing is a corpus-level contrast transformation, not a special correction for short permutations. For any component mean x in [0,1], x^3 preserves its ordering and endpoints while giving substantially less credit to broad but incomplete agreement. Every row contributes once to each raw mean before the transformation, so the grader does not assign a separate nonlinear reward according to candidate count. This choice keeps the score smooth and exact at 1 while emphasizing models that are consistently correct across the test collection. The effect is measured on the current hidden set rather than assumed: exact, mildly damaged, substantially damaged, and fully reversed rankings score 1.0, 0.569862, 0.028402, and 0.000261. A malformed prediction contributes zero raw agreement and accuracy for that row. Hidden targets are validated as complete permutations; malformed hidden data raises an error. What Makes This Interesting The closest sequence motif is only one part of the decision. Several plausible sites compete inside the same exon, position priors are imperfect, and rankings are derived from noisy biological replicates rather than synthetic rules. Fine-tuning a nucleotide representation with candidate-level competition can use the full 2,049-base context and the relationships among sites. What Not To Use Do not recover source gene names or measured counts through external sequence lookup. Do not predict from opaque IDs, file ordering, path hashes, row order, or candidate-count frequencies. Do not use hidden answers, leaderboard probing, malformed files, or duplicate-ID behavior. Sequence encoders, motif models, learning-to-rank methods, and grouped validation are permitted. Reference Validation Exact hidden orders score 1.0. The public sample, which preserves the supplied site order, scores 0.053825. Reversing the supplied order scores 0.163959, a training rank prior scores 0.158771, a fixed-seed random permutation scores 0.089173, and a training-only k-mer ranker scores 0.181532. These checks establish a low baseline and a useful nontrivial ranking problem; they are not an upper bound on a trained sequence model. The grader rejects structural submission attacks and gives malformed permutations zero credit. Contract tests also verify that exact, mildly damaged, substantially damaged, and reversed predictions receive strictly decreasing scores. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 90 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen.
> Closes in 1h 29m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Odia Field Record Reassembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx730cg40gq6qn1jwzps0c3x858drv17
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat krsna-dev's score of 0.162!

Full challenge description from page:

> Odia Field Record Reassembly Overview This challenge concerns recovery of broken multimodal field records. Each group contains 12 observed Odia speech records, 12 shuffled human transcript cards, 12 shuffled prompt images, and six latent target speakers. Every record is in Odia. District predictions use the fixed label set Khordha, Malkangiri, Nuapada, and Sambalpur. For every observation, recover: the exact transcript card; the exact prompt image; the recording district; and the target-speaker cluster within the group. Transcript and image assignments must each be a one-to-one permutation. Speaker cluster names are arbitrary: only the partition of clips into speakers matters. This is a GPU challenge. A submission notebook must finish within one hour on the platform hardware. Observed media and target semantics The released WAV for a row is not a single-speaker archival recording. It is a deterministic mixture of two Odia utterances from different source speakers in the same reconstruction group: the primary utterance is the source record assigned to that row; and the interfering utterance is taken from another row in the same group. All four row targets refer only to the primary source record. In particular, transcript_id is the cleaned human transcript of the primary utterance, image_id is its associated prompt-image card, district is its source district, and speaker_cluster is the primary speaker's group-local cluster. The interfering utterance and its speaker are distractors for that row. They do not become an additional correct transcript or speaker label. Every source utterance is used once as a primary and once as an interferer in another mixture within its group. Before later effects, the primary has a nominal RMS advantage of 6.0, 2.5, or 0.5 dB over the active portion of the interferer, depending on the deterministically assigned degradation tier. This designation is fixed by the construction process, not by which voice seems dominant at every instant. Audio processing may include bandwidth reduction, additive noise, short dropouts, quantization, echo, nonlinear distortion, and temporal cropping. Deterministic hash buckets give training rows nominal mild (clean in the preparation code), degraded, and severe allocations of 20%, 50%, and 30%. Test rows have nominal allocations of 10% degraded and 90% severe and contain no mild tier. The 780-row training release contains 162 mild, 391 degraded, and 227 severe rows; the 156-row test release contains 12 degraded and 144 severe rows. Per-row tier labels are not released. Prompt-image cards are transformed independently from their associated source images. Depending on the same row tier, processing may include crop, resize, JPEG compression, blur, desaturation, contrast reduction, small rotation, and rectangular occlusion. The required image_id remains the card derived from the primary record's prompt image. Candidate text cards contain cleaned human transcripts; event markup is removed, but no generated caption or translation is substituted. What not to use Hosted inference APIs or external transcription, geolocation, face, or reverse-image-search services. External dataset lookup, original filenames, file hashes, or record matching intended to recover the hidden associations. Private-answer access, grader probing, prepare-script introspection, or hardcoded test mappings. Personally identifying a contributor or attempting to reverse anonymization. Metadata shortcuts based on row order, opaque IDs, encoded file size, or CSV ordering. Submissions using source lookup or identity recovery may be rejected even when their score is high. Evaluation Higher is better. Scores are bounded to [0,1]; a perfect valid submission scores exactly 1.0. For row i, let: T_i be 1 when the transcript assignment is correct; I_i be 1 when the image assignment is correct; D_i be 1 when the district is correct; X_i = T_i I_i; and J_i = T_i I_i D_i. If its group contains k rows, the chance rates are respectively 1/k, 1/k, 1/4, 1/k^2, and 1/(4k^2) because the district label set has four values. For any binary component E with per-row chance rate c, define: Skill(E, c) = clip((mean(E) - mean(c)) / (1 - mean(c)), 0, 1) This chance correction prevents the metric from awarding a large score for random guessing in a large structured output. Speaker is the mean adjusted Rand index between true and predicted speaker partitions, clipped to [0,1]. It is invariant to cluster names. GroupExact is the fraction of groups in which every transcript, image, and district is correct and the speaker partition is exact. Score = 0.84*JointSkill^2 0.05*TranscriptAndImageSkill^2 0.015*TranscriptSkill 0.015*ImageSkill 0.01*DistrictSkill 0.05*Speaker 0.02*GroupExact Why this metric measures record reassembly The useful output is the complete association, not an isolated transcript, image, or district guess. JointSkill therefore receives most of the weight and is squared: a system must recover many complete records before receiving substantial credit, while occasional accidental conjunctions remain near the floor. TranscriptAndImageSkill measures the central cross-modal link when geographic evidence is uncertain. The three small marginal terms diagnose genuine partial recovery without allowing a single-modality system to dominate. Chance correction is necessary because every group is a forced permutation: random assignments inevitably produce some matches, and district guessing has a higher base rate than transcript-image matching. Subtracting the known chance rate makes zero represent no demonstrated skill across components with different candidate counts. Adjusted Rand index measures speaker partitions without depending on arbitrary cluster names. GroupExact rewards complete, internally consistent reconstruction. The weights sum to one, all components are bounded, and a perfect reconstruction scores exactly 1.0. Dataset All released paths are relative to public/. | Item | Description | |---|---| | train.csv | Training audio rows and all targets | | train_transcripts.csv | Shuffled transcript cards for training groups | | train_images.csv | Shuffled image cards for training groups | | train/audio/ | Processed 16 kHz two-utterance WAV training mixtures | | train/images/ | Processed JPEG training prompt-image cards | | test.csv | Test audio rows without associations | | test_transcripts.csv | Shuffled transcript cards for test groups | | test_images.csv | Shuffled image cards for test groups | | test/audio/ | Processed 16 kHz two-utterance WAV test mixtures | | test/images/ | Processed JPEG test prompt-image cards | | metadata.json | Public preparation summary | | sample_submission.csv | Structurally valid weak submission | train.csv | Column | Type | Description | |---|---|---| | group | string | Reconstruction group | | id | string | Globally unique opaque record key | | audio_path | string | Relative WAV path | | transcript_id | string | Correct transcript card | | image_id | string | Correct image card | | district | string | Correct recording district | | speaker_cluster | string | Group-local true speaker cluster | test.csv | Column | Type | Description | |---|---|---| | group | string | Reconstruction group | | id | string | Globally unique opaque record key | | audio_path | string | Relative WAV path | Candidate tables *_transcripts.csv contains group, transcript_id, and transcript. *_images.csv contains group, image_id, and image_path. A candidate ID belongs only to its stated group. Every transcript and every image must be used exactly once in that group's submission. Split isolation and leakage control Training and test are split by speaker before groups are constructed, so no test voice occurs in training. Prompt-image identities are unique and disjoint across the split as well. Public audio, transcript, and image identifiers are opaque and split-disjoint; original filenames, speaker IDs, location codes, hashes, and collection-order fields are not released. Interferers are assigned only after the speaker-disjoint split and always come from the same reconstruction group as their primary. Consequently, an audio mixture never introduces a voice, transcript, image association, or district record from the opposite split. All groups intentionally share the 12-record, six-speaker task schema and contain records from at least three of the four district labels. That common shape defines the required output but does not encode a target mapping: candidate orders are independent within each group, media and speakers do not cross splits, and speaker labels are arbitrary group-local names. District candidate sets may recur because geography is a prediction target; memorizing a group-level district prior cannot identify which district belongs to an individual test recording and is already accounted for by the district chance baseline. Submission Write submission.csv with exactly these columns in this order: | Column | Type | Constraint | |---|---|---| | id | string | Unique key; must match the complete test.csv ID set | | transcript_id | string | Candidate from the same group | | image_id | string | Candidate from the same group | | district | string | One of the four stated district labels | | speaker_cluster | string | Nonempty group-local label, at most 64 characters | Example: id,transcript_id,image_id,district,speaker_cluster r_01,t_07,i_12,Khordha,cluster_a r_02,t_03,i_09,Sambalpur,cluster_b Requirements: Include exactly one row per test id. Row order does not affect the score. Within each group, transcript_id must be a permutation of all transcript candidates and image_id must be a permutation of all image candidates. Speaker labels must be nonempty and at most 64 characters. They are evaluated as a partition against the six latent target speakers. Speaker labels need not match the labels used in training or private answers. Duplicate keys, a missing or extra test ID, missing values, incorrect column order, or speaker labels longer than 64 characters make the submission invalid. &nbsp;
> Closes in 2h 42m
> 11 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Guangdong Spoken Boundary Clocks

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7en8dcbngb0pgajgqf40j5598eahws
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Guangdong Spoken Boundary Clocks Overview You receive one continuous Cantonese speech excerpt and its complete written words, but the written excerpt has lost the places where the original human subtitles were divided. Predict a boundary chain: for every subtitle break, give both (1) the character offset in the unpunctuated text and (2) the matching time in the audio. The text and audio coordinates must agree. This is a joint speech-and-language alignment problem, not speech recognition: the words are already given, but neither their subtitle grouping nor the timing of those groups is given. For example, [14,103],[31,211],[48,324]] says that three boundaries occur after characters 14, 31, and 48 of the public transcript and at audio frames 103, 211, and 324. Frame 0 begins at the start of the supplied excerpt; there are 20 frames per second. A case contains four to eight hidden subtitle segments, so its chain has three to seven ordered pairs. You must infer the number of boundaries as well as their coordinates. This task has a practical use in subtitle repair: existing speech transcripts often contain the right words but lack reliable sentence cuts or clocks. A model that can locate both cuts together can help editors synchronize captions without re-transcribing the speech. The benchmark measures alignment to the deposited human transcription and timing, not translation, speaker identity, or literary comprehension. The realized prepared data contain 10,517 cases and 62,858 distinct source subtitle segments: 8,428 train cases and 2,089 test cases. The split holds out complete source episodes separately within each of the two books: 126 train/31 test episodes for Three Kingdoms and 74 train/18 test episodes for Water Margin. Therefore no excerpt, recording interval, or subtitle segment is shared between train and test. The opaque case IDs are join keys, not the split mechanism, and no complete transcript or exact audio/text input is duplicated across the boundary. This is generalization to unseen episodes of the same narrator and two works, not to unseen speakers or dialects. The input is genuinely multimodal. transcript contains the sequence of written Cantonese characters, without the punctuation and subtitle dividers. audio_packet contains a compressed 20-frame-per-second, 24-band acoustic map from the corresponding continuous recording. A plain table of scalar features cannot replace the temporal sound pattern or the evolving text context needed to place an ordered boundary chain. Relation to earlier work Automatic subtitling already studies segmentation and timing, including [Karakanta et al. (EAMT 2022), and Cantonese punctuation restoration has its own PunCantonese benchmark. This challenge does not claim those ingredients are new. Its particular decision object couples a character offset and a time coordinate for every boundary in one continuous excerpt, hides both kinds of subtitle boundary, uses real Guangzhou Cantonese audio, and evaluates their joint rather than separate accuracy. Unlike ASR, the transcript content is given; unlike text-only punctuation restoration, the answer must synchronize to audio; unlike ordinary forced alignment, the text has not already been segmented into target captions. Files and feature schema The public directory contains only these four CSVs: public/ train.csv train_labels.csv test.csv sample_submission.csv train.csv and test.csv have exactly the same four columns, in this order: | Column | Meaning | | --- | --- | | case_id | Unique opaque tr_ or te_ identifier; the submission join key | | transcript | Consecutive unpunctuated Cantonese characters for the whole excerpt | | audio_packet | Base64-encoded zlib-compressed unsigned-byte acoustic matrix | | frame_count | Number of acoustic frames in that matrix | Decode audio_packet by base64-decoding it, zlib-decompressing the result, and interpreting the bytes as a row-major uint8 matrix of shape (frame_count, 24). Consecutive rows are consecutive 50 ms frames. The 24 columns are increasing frequency bands. Larger bytes mean greater relative acoustic energy; the per-excerpt spectral maximum was normalized to 255 and values more than 80 dB below it were clipped to zero. This fixed, label-independent compression preserves the temporal evidence needed for alignment without distributing full-fidelity recordings. train_labels.csv has case_id,boundary_chain and joins one-to-one with train.csv. Its JSON chain is the complete target for that training excerpt. test.csv contains no target field. sample_submission.csv has case_id,boundary_chain in the same order as the private answers.csv; it covers every test ID and is generated from training-case statistics and the current audio packet only. Across the realized train and test features, transcripts contain 17–274 characters and acoustic packets contain 189–1,505 frames. Every reference chain contains three to seven pairs. The reference text offset after segment j is the cumulative number of remaining non-punctuation characters in segments 1 through j. The reference frame is the rounded midpoint between the end time of segment j and the start time of segment j+1, measured from the public audio excerpt's start at 20 frames/second. The midpoint is used because the SRT segments may have a short natural pause between them. Preparation requires strictly increasing offsets and times. Submission Submit one CSV with exactly these columns and order: case_id,boundary_chain te_0123456789abcdef12,"[[14,103],[31,211],[48,324]]" Every te_ identifier must appear once. A boundary_chain is a JSON list of up to 12 pairs; the reference chains have three to seven pairs, but the count is not supplied at test time. Every pair is [character_offset,frame_index]; both entries must be ordinary JSON integers, not booleans. Both coordinates must be positive and strictly increase along the chain. The grader accepts character offsets below 1000 and frame indices below 2000. A cell may contain at most 2048 characters. A malformed cell earns zero for that row. Missing or duplicate IDs score zero overall. Extra IDs are rejected for a full-test evaluation; one complete test submission can also be used when the platform scores an answer subset. Extra, missing, duplicated, or reordered columns raise ValueError. CSV row order does not matter. Scoring If a predicted chain has the right number of boundaries, the grader compares corresponding positions. If its length differs from the reference, it uses dynamic programming to find the maximum-credit one-to-one monotone matching. A predicted boundary can match at most one reference boundary; an inserted or omitted boundary receives no match credit. For any matched pair, let d_char and d_frame be the absolute differences between their text and acoustic coordinates. Its coupled credit is credit_i = exp(-d_char / 3 - d_frame / 10). The scales mean that a three-character error and a ten-frame (0.5 second) error each multiply credit by e^-1. Errors in both coordinates compound. Thus a text-only boundary that is timed poorly, or an acoustic pause assigned to the wrong character, receives little credit. Let W be the sum of credits under the maximum-credit monotone matching, pooled across rows. Let P and T be the total numbers of predicted and reference boundaries. The soft-F1-style match quality is M = 2W / (P + T). Extra and missing boundaries reduce this value; a malformed row is treated as an empty chain. For N graded cases, the finite-sample floor is F = max(0.025, 0.45 / sqrt(max(N-1,1))). A non-exact submission with fewer than eight graded rows scores zero. Otherwise the reported score is score = clip((max(0,M-F)/(1-F))^1.15, 0, 1). Exact reconstruction of every chain returns 1.0 directly. Empty, malformed, or blind outputs have no automatic positive credit from the floor. The floor reduces rewards for accidental near matches, especially when a platform evaluates a small answer subset. All constants are fixed before seeing submissions; the final score is invariant to row order and lies in [0,1]. The character and frame errors are both essential because the downstream subtitle needs the right words grouped and placed at the right moment. Exponential locality provides partial reward for small annotation or prediction offsets, while penalizing large errors smoothly. The floor and mild exponent do not cap the exact endpoint. Permitted methods and limitations Train from the provided public training rows only. A neural audio-text aligner, a learned boundary tagger, an empirical speech-rate model, signal-processing features, or an ensemble fitted without private answers are all eligible. Deterministic decoding of the supplied acoustic representation and ordinary monotone alignment algorithms are permitted; they do not by themselves constitute external answer lookup. Do not use other corpora, pretrained weights, a speech recognition service, source-episode lookup, or private SRT files to predict test boundaries. The archive covers one narrator, two literary works, and a historical recording style. Its SRT timestamps are human subtitle timings rather than phoneme-accurate ground truth, and the acoustic packet is deliberately lossy. The benchmark is intended for research on joint subtitle segmentation and synchronization within that domain, not for speaker identification or deployment as a universal Cantonese subtitling system. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## 2nd best

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c8z1fer5112jrm3ermjhts58bt9yx
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 22h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## c

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cjhntwfqtc8yh34dc69sfq18e6mbg
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 2d ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## b

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72v8rm8sy2ha8ef2qq79pzmh8e6r6k
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 2d ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## june 14 Synthetic Data Center Rack Thermal Snapshots

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c6v3wjbqny1qyh1hjj1hf4h8aqq3h
- DOMAIN exactly as displayed: Tabular
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> No description
> 10d ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Repairing Contradictory Sound-Search Feedback

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77s7gv7j4ayr2bjh4c2tjh4s8e3sr3
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.517!

Full challenge description from page:

> Overview Predict which editor decisions need changing to make a sound search consistent, and whether four proposed sound sequences would be accepted under the remaining interpretations. Each example supplies real sound recordings, four accept/reject decisions, and twelve possible search rules. An editor assembling sound effects can accept one sequence and reject another without expressing a fully consistent rule. A search assistant should not silently pick an arbitrary interpretation. It should identify every smallest correction of the feedback and distinguish a definite recommendation from an ambiguous one, including when one decision is withdrawn. The recordings are short, human-labeled effects covering everyday actions, objects, human sounds, and other sound-event families. Each sequence is an ordered list of three separate recordings assembled for this task, not a continuous recording of a real scene. Event identity and one-shot/multi-shot annotations come from the supplied human labels. The editor decisions are constructed challenge inputs; they are not claims about a real editor's behavior. Dataset | File | Contents | |---|---| | train.csv | 2,989 sessions. Columns are the five inputs below followed by feedback_repairs and retrieval_envelope. | | test.csv | 808 sessions with exactly the five input columns and no targets. | | training_audio_labels.csv | Direct supervision for all 4,328 distinct training recordings: audio_path (string), event (categorical string), and articulation (one of One-shot, Multi-shot). | | sample_submission.csv | All test IDs and the two target columns, populated with complete label pairs resampled from training. It is a format example, not a trained solution. | | audio/ | 5,463 mono PCM16 WAV files: 4,328 used in training and 1,135 in testing. Each is five seconds at 16 kHz and occupies 160,044 bytes. | Audio paths are relative to the public dataset directory, for example audio/a_e7ad559a33ff418068abd89a.wav. The audio retains the complete source clip after low-pass resampling, with peak normalization and silence padding. The silence position is not an event-order label: the order of the three paths defines sequence order. Contributor, original-recording, and exact-source-audio links are grouped before splitting. All 24 recording positions in a session come from that session's split. There are 1,230 source components in training and 371 in testing. References are reused within a split, so sessions are not all statistically independent. Each test session has a distinct anchor recording that is never used in the reference pool. Use recording/group-aware validation, not a random split of sound occurrences. Input Columns | Column | CSV data type | Meaning | |---|---|---| | case_id | string | Opaque identifier copied unchanged to the submission. | | support_examples | JSON-encoded string | Four objects in order S1 through S4. Each has audio_paths, an ordered list of three path strings, and accepted, a Boolean editor decision. | | retrieval_examples | JSON-encoded string | Four ordered three-path lists, T1 through T4, whose recommendation stability must be predicted. | | candidate_rules | JSON-encoded string | Twelve objects, R01 through R12. Each has string id, string op, and a list of one or two string args. | | event_vocabulary | JSON-encoded string | The complete event-name list for this session's sound family. A recording can belong to an event not mentioned by any candidate rule. | For example, one support object is {"audio_paths":["audio/a_e7ad559a33ff418068abd89a.wav","audio/a_c1100df3be3aa961f32a15ed.wav","audio/a_81d3db2b7e7c1ebb15b7a930.wav"],"accepted":false}. This describes one of the four support entries, not a complete CSV row. A rule such as {"id":"R02","op":"before","args":["Snore","Cough"]} accepts a sequence only if a Snore recording precedes a Cough recording in its path list. Complete Rule Semantics Let the three inferred event labels be E1, E2, E3. All event comparisons use the exact class strings in the public vocabulary; these are categorical labels, not free-text answers. | Operation | Arguments | Acceptance condition | |---|---|---| | has | [event] | At least one of the three recordings has this event label. | | absent | [event] | None has this event label. | | repeat | [event] | At least two recordings have this event label. This does not count repeated impulses within a single file. | | first | [event] | E1 has this label. | | last | [event] | E3 has this label. | | before | [event A, event B] | Some position i has A and a later position j has B. The events need not be adjacent. | | both | [event A, event B] | Both events occur somewhere in the sequence. | | xor | [event A, event B] | Exactly one of the two event labels occurs. | | shot_majority | [articulation] | At least two recordings have the specified One-shot or Multi-shot annotation. | Rule arguments are sampled independently of the recordings within the declared family. Rule names must not be interpreted as a shortlist of the recordings' actual event labels. Different candidate rules can behave identically on the available examples; such ambiguity is intentional. Prediction Definitions For each rule r, compare its four support acceptances with the editor's four decisions. Its disagreement mask has a 1 where the editor decision must flip and a 0 where it remains unchanged. Its repair cost is the number of 1s. Retain every rule having the smallest repair cost. feedback_repairs is the set of distinct disagreement masks of those retained rules, not their rule IDs. Prefix each four-bit mask with f:, sort lexicographically, and join with |. If the feedback is already consistent, the answer is f:0000. For example, f:0001|f:0100 says either flipping S4 alone or flipping S2 alone produces a minimum-cost repair. Do not include larger repairs. retrieval_envelope is a 4 x 5 integer matrix. Rows are T1, T2, T3, T4. Its columns are: all four support decisions; omit S1; omit S2; omit S3; omit S4. In each column, recompute the minimum-disagreement rules using only the remaining decisions. An omitted decision is ignored, not flipped. Evaluate the retrieval sequence under every retained rule: | Value | Meaning | |---|---| | 0 | Every retained rule rejects the sequence. | | 1 | At least one retained rule accepts and at least one rejects. | | 2 | Every retained rule accepts the sequence. | There is always at least one minimum-cost rule, even with contradictory feedback. The output is a set-valued recommendation under the documented finite policy list, not a probability or a claim to recover an editor's unexpressed intent. Target Distribution Counts below are matrix entries across the twenty retrieval decisions per session. | Outcome | Training | Test | |---|---|---| | 0: reject | 21,713 | 6,090 | | 1: ambiguous | 23,607 | 6,189 | | 2: accept | 14,460 | 3,881 | Submission Format Write ./working/submission.csv with exactly these columns in this order: case_id,feedback_repairs,retrieval_envelope. | Column | Required type and bound | |---|---| | case_id | String: q_ followed by 24 lowercase hexadecimal characters, copied from test. | | feedback_repairs | String, at most 83 characters. Between 1 and 12 sorted unique f:bbbb tokens separated by |; b is 0 or 1. Every mask must have the same number of 1s. | | retrieval_envelope | JSON-encoded string, at most 120 characters. Exactly four lists of five integers in 0 through 2. Booleans, floats, and quoted numbers are invalid. | This complete labeled training example demonstrates the submission serialization: | case_id | feedback_repairs | retrieval_envelope | |---|---|---| | q_c5a1f087ce7b2ca58ee62237 | f:0001\|f:0100 | [[0,0,0,0,0],[0,1,0,0,0],[1,1,0,1,2],[0,1,0,0,0]] | Use a CSV writer to quote JSON fields containing commas. Supply exactly one row per test ID. Row order can change; column order cannot. Extra/missing columns, extra/missing rows, duplicate columns, duplicate IDs, unknown IDs, and malformed IDs reject the submission. The submission schema must equal the evaluator's answer schema exactly. The ordinary files use the three columns above. Evaluation The Contradictory Feedback Recovery Score is: Score = 0.45 x RepairScore + 0.40 x EnvelopeScore + 0.15 x CompleteSessionScore. Minimum score: 0.0. Maximum score: 1.0. Higher is better. | Component | Exact definition | Weight rationale | |---|---|---| | RepairScore | For session i, compare submitted mask set P_i and true set Y_i using Jaccard agreement: J_i = size(P_i intersect Y_i) / size(P_i union Y_i). Average J_i over all sessions. | 45% emphasizes recovering the complete minimal correction set; adding unnecessary repairs reduces agreement. | | EnvelopeScore | Pool all twenty matrix entries per session. For each true class c present in the evaluated answer subset, compute F1_c = 2 TP_c / (2 TP_c + FP_c + FN_c). Average these class F1 values with equal weight. | 40% evaluates downstream recommendations without letting the most common outcome dominate. Class presence comes from the evaluated answers, not training frequencies. | | CompleteSessionScore | sum_i I[submitted mask set equals truth AND submitted matrix equals truth] / N, where N is the evaluated session count. | 15% rewards an internally useful complete session while retaining substantial partial credit in the other components. | TP, FP, and FN are true-positive, false-positive, and false-negative entry counts for class c. A malformed repair string scores zero for that session's RepairScore. A malformed matrix contributes twenty missed true labels and no predicted true-class hits. Either malformed field makes CompleteSessionScore zero for that session. Invalid hidden labels raise an error; they are never repaired or clipped by the grader. Modeling and Restrictions Learn event and articulation predictions from training_audio_labels.csv, cache recording-level predictions, then evaluate the small rule bank and its leave-one-out variants. A stronger solution should propagate uncertainty in event predictions rather than committing early to a single label. This separates a conventional audio-modeling step from a fully specified decision procedure. The competition environment provides access to a single NVIDIA A10G GPU. The entire pipeline must finish within 1.5 hours, including data loading, training or adaptation, inference, decoding, validation, and submission generation. What Not To Use Use the supplied public training data and permitted locally available models. Do not retrieve original recordings, annotations, or labels through external dataset lookup or audio fingerprint search. Do not use private files, hidden-answer access, leaderboard-query label extraction, or ID/order/hash/file-size lookup tables as predictors. Caching features of supplied recordings and reusing an inferred label for the same public recording are allowed. Reference Validation Exact answers score 1.0; the supplied sample scores 0.223537 and a train-mode baseline scores 0.207396. A vocabulary-only prior scores 0.329529.
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## ArchiveProbe: Counterfactual Clock Discrimination

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75aeyyme3z8jsbc7s72bdm4d8e5r95
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.528!

Full challenge description from page:

> ArchiveProbe: Counterfactual Clock Discrimination Overview Two instruments preserve different anonymous views of the same real archived event. The first view has 48 channels over 192 steps and the second has 32 channels over 96 steps. Their original clock metadata was damaged: each view follows a different nonuniform clock, only 5–10 of 17 clock boundaries remain trusted, and the most distorted boundaries are preferentially missing. For every row you receive eight case-specific paired probes. One paired probe reads one hidden boundary from each clock simultaneously. The two returned boundary values form a two-dimensional response. A useful probe must both separate difficult counterfactual timing histories and remain reliable under empirical cross-view calibration. Predict the index from 0 through 7 of the probe with the strongest combined certificate. This is an instance-level experimental-design problem. You are not asked to reconstruct a best warp, transcribe either view, select a global sensor layout, or request another labeled training example. Candidate positions are independently permuted for every row, and both target classes and anchor budgets are balanced. Formal Counterfactual Decision Contract The scored object is a certificate for one paired intervention, not an informative timestamp. Its first component is robust: for candidate j and hidden clock world w, the intervention returns the joint response r[j,w] from two different clocks. World-specific evidence is the distance from r[j,w] to the nearest response produced by any competing world, adjusted by empirical activity in both views and by paired acquisition cost. The 20th percentile across worlds gives the lower-tail component. The second component is empirical calibration. It captures nonlinear agreement and disagreement between the two released sequence views around the proposed boundaries, their unresolved clock spans, relative positions, and asymmetric costs. The two components are standardized within a row and combined with weights 0.40 and 0.60, respectively. The target is the candidate with the largest combined certificate. train_probe_certificates.npy exposes the eight standardized combined values for every training row; no evaluation certificate is released. This dense training-only supervision makes the intended route candidate-level utility learning rather than reconstructing an undisclosed simulator key. Three coupled ingredients define the task. First, every row has its own eight-world cohort, so there is no globally best probe. Second, the public 16-path bridge preview is deliberately misspecified relative to the private cohort and held-out evaluation clock law; reproducing the public sampler is therefore insufficient. Third, final utility couples lower-tail response geometry with nonlinear cross-view calibration rather than expected reconstruction quality or average information gain. Training labels and training certificates are the public observations from which this correction must be learned. Empirical Archive Grounding The sequential content is not synthesized. It comes from thousands of real human voice recordings paired with independently produced text records in a checksum-pinned archival corpus. Privacy-reduced acoustic tensors retain spectral dynamics from the real waveforms; the second tensors retain local structure from the paired real text. Complete source groups are separated before challenge construction. The exact repository, titles, language, paths, raw recordings, and readable text are deliberately absent from solver-facing material. Full provenance, checksums, derivation code, and license evidence remain available to reviewers in the private dataset record. Only clock loss and the counterfactual calibration audit are simulated. Real pauses, bursts, cadence changes, and cross-view structure affect probe value through the released tensors. Clock Model and Held-Out Law Every clock consists of 16 positive sector dwell times normalized to one cycle; cumulative dwell time gives 17 boundary knots. Training mixes three unlabeled timing laws: independent multiplicative jitter, persistent autoregressive drift, and alternating autoregressive drift. Evaluation uses only a fourth, held-out multiscale law that combines correlated innovation with a phase-randomized periodic beat. No timing-law label is released or encoded in an ID. The two endpoints and 3–8 interior knots survive. A mask marks these disclosed knots. Hidden entries in the public knot array contain uniform-clock placeholders, not observations. The released posterior sampler completes every interval between disclosed anchors with positive bridges. Sixteen compact Monte Carlo paths preview this continuous conditional posterior for each modality. Every path agrees at the disclosed anchors, and the generating clock is never inserted into the sample bank. The posterior preview is a reference uncertainty model, not a finite list of possible answers. Solvers may draw additional positive bridges from the documented rule. The held-out evaluation law deliberately tests whether a method can correct this reference posterior using empirical sequence evidence rather than memorize one simulator-specific calibration curve. Candidate Probe Encoding train_probe_candidates.npy and test_probe_candidates.npy have shape (N, 8, 4). Each candidate contains [acoustic_normalized_knot, orthographic_normalized_knot, acoustic_cost, orthographic_cost]. Both knot coordinates are hidden interior boundaries and are divided by 16. Costs lie in [0.70, 1.00). A candidate measures both listed boundaries simultaneously. Candidate order is independently rotated per row, so position is not predictive. Private Counterfactual Cohort Each row has eight anchor-preserving clock worlds. World 0 uses the row's generating clocks. Worlds 1–7 complete every disclosed-anchor interval with autoregressive log-dwell innovations having coefficients [-0.65, -0.35, 0.00, 0.35, 0.65, 0.48, -0.48]. A phase-randomized periodic component with periods from 4.0 through 7.0 sectors is added. Dwell factors are exponentiated, clipped to [0.22, 4.50], normalized inside each anchor interval, and cumulatively integrated. The cohort is deterministic for label generation, but its keyed random draws and exact clocks are private. This prevents evaluation labels from being reproduced from an ID while preserving a precise, auditable target. Training labels and dense candidate certificates teach how empirical sequence structure maps the public posterior preview to final probe quality. Combined Certificate and Target For one candidate and one world, normalize each measured boundary value by the span between its nearest disclosed anchors. This produces a two-dimensional cross-modal response r_w. Define margin_w = min_{v != w} EuclideanDistance(r_w, r_v). Local activity is the mean absolute first difference across all channels in the five-bin window centered at the candidate knot. Candidate activity is the geometric mean of 0.35 + activity across the two views. World utility is utility_w = margin_w * activity_factor / (acoustic_cost + orthographic_cost). The 20th percentile of the eight world utilities is standardized across the row's candidates to form the robust component. A separately standardized empirical component represents nonlinear cross-view calibration using local sequence dynamics, unresolved interval geometry, relative boundary placement, and cost asymmetry. Final certificate is 0.40 * robust_component + 0.60 * empirical_component. The target is the index of the candidate with maximum final certificate. Ties, if any, are resolved by the first maximum after the row-specific candidate permutation. The training certificate array is the direct supervision for this final utility. Its row-wise argmax equals target; its scale is standardized separately for each row. Because the evaluation certificate array is absent, a submission still requires generalizing a candidate-level model from training rows to disjoint evaluation rows. This target is not expected information gain. Its robust component protects the lower tail rather than averaging over worlds, while its calibration component requires interactions across the two views. For example, a candidate with utilities (0.01, 0.01, 0.01, 1, 1, 1, 1, 1) has mean 0.62875 but a 20th percentile of 0.01; a candidate fixed at 0.50 in all worlds wins the robust comparison. Independent per-view rankings also need not recover the best paired probe because both response separation and calibration are coupled across modalities. Why This Is Not Clock Alignment or Expected Information Gain A conventional clock-alignment benchmark asks for a dense warp, corrected timestamps, or matched keypoints and scores reconstruction error. ArchiveProbe never accepts or scores an alignment. The required output is a row-specific decision among eight jointly placed, cost-bearing probes. Two clock reconstructions with similar alignment error can induce different probe rankings because the target depends on the smallest joint response separation across an anchor-preserving counterfactual cohort. Expected information gain also optimizes a different functional: it rewards average posterior reduction and omits the learned empirical calibration required here. A candidate with excellent mean counterfactual utility can lose if it has a weak lower tail or inconsistent cross-view evidence. On all 1,024 evaluation rows, the deterministic expectation analogue reports only 0.0986, while the exact combined certificate reports 1.0. Candidate permutation, held-out clock-law transfer, balanced anchor budgets, and the stratified chance-corrected leaderboard metric together test calibrated experimental decisions rather than timestamp recovery or average uncertainty reduction. Transfer-Barrier Audit A single-timeline timepoint selector cannot consume this contract without changing its decision object: it must replace one timestamp by a paired intervention on two independently masked clocks, replace downstream predictive utility by an eight-world response-collision matrix, and replace expectation by a lower-tail quantile. A counterfactual forecasting harness also has no compatible output here. It would have to turn predicted trajectories into eight candidate-specific joint response clouds, compute all within-candidate nearest-world margins, calibrate the misspecified public bridge preview against labeled rows, and finally emit one categorical decision rather than a trajectory. The measured ablations isolate that transfer barrier. Cheapest-pair selection scores 0.0500; independent-view separation scores 0.0226; joint public-posterior separation scores 0.0803; activity-only reaches 0.1085; and replacing the lower-tail margin by its mean reaches 0.0986. Three compact certificate regressors reach 0.4601–0.4743 only after learning candidate-level nonlinear calibration from the dense training certificates. Thus neither a standard timepoint-selection objective nor a counterfactual-trajectory output can be reused as the scoring harness; the paired response set and learned cross-view certificate require substantive model and objective changes. Data Files train.csv contains id, array_index, and integer target for 7,168 rows. test.csv contains id and array_index for 1,024 rows. sample_submission.csv contains the required id,prediction schema. Acoustic feature files have shapes (7168, 48, 192) and (1024, 48, 192) with dtype float16. Orthographic feature files have shapes (7168, 32, 96) and (1024, 32, 96) with dtype float16. Clock-knot files have shape (N, 17) and dtype float32. Clock-mask files have shape (N, 17) and dtype uint8. Clock-hypothesis files have shape (N, 16, 17) and dtype float32. Probe-candidate files have shape (N, 8, 4) and dtype float32. train_probe_certificates.npy has shape (7168, 8) and dtype float32. It contains row-standardized candidate utilities for training only; there is no test counterpart. data_manifest.json records shapes, semantics, balance, and file digests. Use array_index to address the arrays. Training rows use global indices from 0 to 7167, inclusive. Test rows use global indices from 7168 to 8191, inclusive. The test-only tensors start at local index zero, so compute local_test_index = array_index - 7168; the result is always an integer from 0 to 1023. One row is one independent empirical recording–text pair. No source record is reused across rows or across train and evaluation. Evaluation Predictions are candidate classes from 0 through 7. Accuracy is computed separately for anchor budgets 5, 6, 7, 8, 9, and 10. Let raw_score be the geometric mean of those six accuracies. The leaderboard reports max(0, (raw_score - 0.125) / 0.875). All eight target classes are exactly balanced in both splits, so constant prediction and chance-level behavior map to 0.0, while oracle prediction remains 1.0. The geometric mean is intentionally strict across budgets. Internally, np.maximum(stratum_scores, 1e-12) keeps the logarithm finite. If any anchor-budget stratum is completely wrong, that epsilon term pulls the raw geometric mean below the 0.125 chance reference, so the reported score becomes 0.0 regardless of performance on the other five strata. The grader aligns by answer-side id, supports platform-created public/private answer subsets, and ignores organizer visibility metadata. Submission row order may change, but every required ID must appear exactly once. Recommended Approach Treat the eight values in train_probe_certificates.npy as candidate-level regression or ranking targets. Extract the same feature block for every candidate: paired response-cloud margins from the 16 posterior paths, local sequence-window statistics, unresolved clock spans, relative positions, and costs. Fit one shared candidate scorer, reshape its evaluation predictions to (1024, 8), and submit the row-wise argmax. Stronger methods can represent candidate interactions jointly, resample additional bridges, or learn a compact sequence encoder. Small tree ensembles, candidate-ranking models, compact 1D encoders, or ensembles are appropriate. Large pretrained speech or language models are neither required nor directly compatible with the anonymized tensors. Empirical Baselines and Runtime On the complete held-out evaluation set, constant classes report 0.0. After chance correction, activity-only reaches 0.1085; the cheapest-pair rule reaches 0.0500; one-step single-view separation reaches 0.0300; additive independent-view separation reaches 0.0226; joint posterior separation reaches 0.0803; joint separation without activity reaches 0.0818; and the expectation analogue reaches 0.0986. The exact target scores 1.0. Three independently seeded histogram-gradient certificate regressors report 0.4647, 0.4743, and 0.4601. Across 40 target-and-budget-stratified visibility simulations, their mean absolute public/private gaps are 0.0318, 0.0366, and 0.0330; the worst observed gap is below 0.088. The strongest deterministic no-training control is 0.1085, leaving a clear learned uplift without approaching saturation. Preparation takes about 15 seconds locally, and all diagnostics plus release audits finish in under two minutes. A compact learned solution can load the release, validate, train several ranking models, and predict within 10–15 minutes on the provided NVIDIA A10G. Split and Leakage Controls The archival-work split is fixed before clocks, masks, candidates, counterfactual worlds, targets, or candidate order are generated. Train and evaluation have zero archival-work, source-record, ID, complete-tensor, or clock-law-family overlap. The server-generated public/private split is audited at the independent-row level, and oracle scores must equal 1.0 on both slices. Solver-facing files contain no source repository, URL, language name, title, filename, transcript, raw recording, original row index, or source identifier. IDs are opaque and must not be used as predictive features. Submission Format Submit exactly two columns in this order: id,prediction. For example, a valid row is pfr_b05_0123456789abcdef01234567,3. Valid predictions are finite, non-boolean integers from 0 through 7. Do not add, remove, rename, or reorder columns. Missing IDs, duplicate IDs, unexpected IDs in a full submission, and wrong column structure raise explicit errors. An isolated non-numeric, non-finite, fractional, or out-of-range prediction is treated as a local corrupt cell with row credit 0.001; it does not discard the other 1,023 rows. Domain and Allowed Methods The challenge domain is multimodal feature engineering with audio-derived sequential data. The central problem is case-specific paired experimental design under missing clocks, posterior misspecification, counterfactual response separation, lower-tail certification, and held-out timing-law transfer. Signal-processing methods, linear or tree models, compact neural networks, and ensembles are allowed. External source lookup, hidden transform keys, and evaluation answers are prohibited. The benchmark must not be used for transcription, translation, speaker profiling, or source reconstruction.
> Closes in 3h 2m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Site Latent Source Attribution from Shared-Channel Transitions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c9rakxtcn3m1sxapzsvf3758dx27c
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.537!

Full challenge description from page:

> Cross-Site Latent Source Attribution from Shared-Channel Transitions Overview Each monitored site has one shared measurement channel that records total instantaneous demand on a common bus. Several independent load sources are connected to that bus. The channel is additive, so the recorded value at any instant is the sum of whatever the individual sources are drawing plus an unmetered background. When a source engages or disengages, the shared channel shows a step transition. We have extracted these transitions and turned each one into an event described by a short window of the shared channel around the transition. For a set of labelled sites we also provide, for every event, an integer identifying the latent source responsible for it. Your task is to take a set of completely unseen sites, where no labels exist, and group their events by originating source. This is hard for four reasons that compound: Group identifiers are permuted independently at every site. A model that learns "group 4 means a large fast-rising step" at training sites learns nothing usable at test sites. Only a transferable notion of similarity between two events can carry across. The number of distinct sources at a site is not given and varies between sites. You must infer it. A source's engage transition and its disengage transition have opposite signs and different local shapes, yet belong to the same group. Any similarity measure applied naively to raw windows will split them. You only ever observe the sum. Other sources may switch during the same window, unmetered background loads fluctuate constantly, and several sources at a site may draw comparable amounts. Task Inputs, per event: home_id: the site the event belongs to (string). A 121-sample window of the shared channel centred on the transition, taken from the corresponding row of a float32 array file. The transition occurs between index 59 and index 61; index 60 is the centre. day_index: integer day offset from the start of that site's recording. time_of_day: fractional position within the day, in [0, 1). step_size: post-transition level minus pre-transition level, measured on the shared channel. May be positive or negative. pre_level: level of the shared channel immediately before the transition. Output, per event in the test file: group_id: a non-negative integer. Semantics of the output: Two events at the SAME site that you assign the same group_id are asserted to come from the same latent source. Group identifiers are compared only within a site. Using the identifier 0 at two different sites does not assert any relationship between them, and is neither rewarded nor penalised. Identifiers are arbitrary. Relabelling a partition does not change its score. You choose how many groups to use at each site, and that choice affects your score. The true number lies between 3 and 9 inclusive at every site. The exact value per site is not given, and your predicted count is not scored directly, but over-segmenting or under-segmenting a site lowers the score for that site. Labelled data is provided at site level for training only. Its group identifiers are permuted per site and carry no cross-site meaning; treat them as a source of same-source / different-source supervision rather than as class labels. Evaluation The score is the mean, over test sites, of the Adjusted Mutual Information between your partition of that site's events and the true partition of that site's events. Reference definition, exactly as implemented in the grader: from sklearn.metrics import adjusted_mutual_info_score per_site = [] for site in sorted(set(answers["home_id"])): mask = answers["home_id"] == site y_true = answers.loc[mask, "group_id"] y_pred = submission["group_id"] aligned to those event_id values per_site.append( adjusted_mutual_info_score(y_true, y_pred, average_method="arithmetic") ) score = sum(per_site) / len(per_site) Higher is better. Every site contributes equally regardless of how many events it contains. Reference floor: clustering log(1 + abs(step_size)) with k-means at a fixed number of groups, using none of the window data and none of the timing data, scores approximately 0.39. Treat 0.39 as the level to beat rather than a low bar. A score near it means the transient shape, the sign structure and the timing signals are not contributing, whatever else the pipeline is doing. Per-site scores vary a lot. Across the held-out sites a single submission can span roughly 0.2 to 0.56, so the mean over sites is the score, and one site's result on its own says very little. Expect the site-to-site spread to be larger than the gap between a mediocre and a good mean. Properties you should be aware of: The metric is invariant to the numeric names you assign to groups. Relabelling a partition, or using a different set of integers at each site, does not change the score. The metric is NOT invariant to the number of groups you emit. Merging two true groups, or splitting one true group in two, changes the contingency table and therefore changes the score. Choosing how many groups exist at each site is part of the task. The metric is adjusted for chance, which means the baseline expectation for an uninformative partition is corrected for its cluster count. It does not mean the cluster count is ignored. Assigning every event at a site to a single group scores approximately 0.0. Assigning every event its own unique group also scores approximately 0.0. Random assignment scores approximately 0.0. A perfect partition scores 1.0. Values can in principle be slightly negative when a partition is worse than chance. The theoretical range is -1.0 to 1.0. Invalid submissions are rejected rather than scored: a missing required column, a missing prediction for any test event, a duplicated event_id, or a null or non-integer group_id all cause the submission to fail. Dataset The prepared public data lives in ./dataset/public/ and contains: train_events.csv — one row per labelled event, chronological within site. Columns: event_id (int, unique), home_id (string), day_index (int), time_of_day (float in [0,1)), step_size (float), pre_level (float), group_id (int, the latent source identifier, permuted per site). train_windows.npy — a float32 array of shape (number of rows in train_events.csv, 121). Row i of this array corresponds to row i of train_events.csv. test_events.csv — one row per unlabelled event, chronological within site. Same columns as train_events.csv except that group_id is absent. test_windows.npy — a float32 array of shape (number of rows in test_events.csv, 121). Row i corresponds to row i of test_events.csv. sample_submission.csv — a syntactically valid submission with a constant group assignment. It scores approximately 0.0 and exists only to show the expected format. Sites in test_events.csv do not appear in train_events.csv. The recordings behind the two files are from different sites and do not overlap in any way. Submission Write exactly one file, ./working/submission.csv, with a header row and exactly two columns, in this order: event_id (integer, must match an event_id from test_events.csv) then group_id (non-negative integer). Requirements on the file: Exactly one row for every event_id present in test_events.csv, and no rows for any other event_id. No duplicated event_id values. No missing, empty, null or NaN values in either column. group_id must be castable to a non-negative integer. Floating point values that are not whole numbers, strings that are not integers, and negative values are invalid. Row order does not matter; alignment is done on event_id. Requirements Exactly one prediction per test event, matching the schema above. No network access, no external APIs, no downloading of pretrained weights or external data at run time. The notebook must run offline. Do not attempt to read anything outside ./dataset/public/ and ./working/. The ground truth for the test sites is not present in the runtime environment. Use only libraries available in the standard environment image. The full notebook must run end to end without manual intervention and should complete in approximately one hour on the configured CPU runtime. This challenge does not use a GPU; size your models accordingly. Set random seeds. A submission that changes materially between identical runs is not reproducible and will be judged accordingly. The number of groups you emit per site is your decision; do not assume it is constant across sites.
> Closes in 4h 8m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Predicting MS3 Daughter Responses to Ion Isolation and Collision Energy

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76fm52s9fexr7we5t02rjfkn8dy4zy
- DOMAIN exactly as displayed: Other
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.641!

Full challenge description from page:

> Overview Predict which diagnostic daughter ions will be detected after isolating either of two intermediate ions and fragmenting it at low or high collision energy. Each case supplies a molecular structure, an experimentally measured MS2 spectrum, the two isolation masses, and six diagnostic mass queries for each isolation; your two outputs report the measured low- and high-energy responses to those twelve queries. In a mass spectrometer, a molecular ion can first break into several intermediate ions. An MS3 experiment selects one intermediate from that mixture and fragments it again. A peak observed in the first spectrum need not be produced by every selected intermediate, and increasing collision energy can either reveal a daughter or consume it through further fragmentation. This task asks for conditional experimental response, not a ranking of formula candidates, molecular-property regression, a chemical-impossibility verdict, or reconstruction of arbitrary missing graph edges. Dataset The public files are train.csv, test.csv, and sample_submission.csv. train.csv has the ordered columns case_id,molecule,experiment,low_response,high_response. test.csv has case_id,molecule,experiment. The sample submission has case_id,low_response,high_response. There are no external media files or sidecar context arrays. | File | Rows | Role | | --- | ---: | --- | | train.csv | 2,077 | Labeled compounds for fitting and grouped local validation. | | test.csv | 455 | Unlabeled compounds with the same experimental input schema. | | sample_submission.csv | 455 | A reproducible, varied format example borrowing complete response pairs from training cases, without consulting hidden responses. | Training and evaluation contain 1,443 and 383 source-connected groups respectively. The largest retained group contains 427 compounds and is kept intact. There are no shared standardized structures, scaffolds, source scans, feature identities, exact spectrum keys, near-spectrum keys, or complete public inputs across the split. Numeric near-replica checks also join spectra before partitioning; all exported MS stages and merging versions participate, even when they are not eligible as cases. Shared acquisition files number 827, which is why this split must not be described as batch-independent. Each retained case represents one standardized compound and one actual root experiment. Alternate annotations, repeat scans, energies, adducts, and polarities are not counted as new independent compounds. Evaluation holds out connected groups built from molecular identity, nonempty standardized Bemis-Murcko scaffolds, repeated scans, root features, and spectral replicas. Entire pooled acquisition files are not held out: independent compounds from a shared acquisition may occur in different splits. This tests unseen-compound/scaffold response on the same experimental platform, not transfer to a new instrument, acquisition batch, or chemical universe. The reference-state distribution counts diagnostic query positions, not independent molecules. Every case contributes twelve positions: | Low/High State | Meaning | Training Positions | Evaluation Positions | | --- | --- | ---: | ---: | | 00 | Not detected at either setting | 17,201 | 3,768 | | 01 | High-only | 1,439 | 359 | | 10 | Low-only | 2,605 | 591 | | 11 | Detected at both settings | 3,679 | 742 | Visible root spectra contain 8 to 246 peaks, with a median of 26 in both partitions. Molecular/root m/z spans 119.06037 to 1,229.57970 across the supplied cases. Training includes 1,660 positive-ion and 417 negative-ion examples; evaluation includes 353 and 102 respectively. These ranges describe this release, not all physically possible spectra. | Column | Type | Meaning | | --- | --- | --- | | case_id | string | Opaque identifier matching case_ followed by 24 lowercase hexadecimal characters. | | molecule | string | Canonical isomeric SMILES for the connected, neutral parent structure. Read it as a molecular graph, including bond orders, aromaticity and available stereochemistry. | | experiment | JSON object serialized as a string | Root spectral evidence and intervention/query definitions specified below. | | low_response | string | b: followed by exactly twelve binary digits, for measured MS3 at energy setting 20. | | high_response | string | The same grammar, for measured MS3 at energy setting 60. | The experiment object has precisely these keys: | Key | Type and Shape | Meaning | | --- | --- | --- | | adduct | string | [M+H]+ or [M-H]-. | | charge | integer | Respectively +1 or -1. Multiply charged ions and other adducts are excluded. | | precursor_mz | positive float | Molecular/root ion m/z, not the isolated intermediate m/z. | | root_energy | float | Actual setting, one of 15, 30, 45, 60 or 75, for the visible first fragmentation and the first stage of both isolation paths. | | root_spectrum | variable-length array of [float,float] | Ascending centroid m/z and relative intensity. Masses are rounded to five decimal places, intensities to six. The largest root intensity is 1. | | isolations | array of two objects | In ascending isolated m/z order. Each object contains mz, a positive float, and probes, six ascending positive m/z values. | The reported energy settings follow the source instrument convention, reported in eV. They are not interchangeable with an arbitrary instrument's calibrated energy scale. The root isolation window is 1.2 m/z units wide; the second-stage isolation window is 2 m/z units wide. These windows can include unresolved neighboring ions, so an isolated nominal mass is not a guarantee of a chemically pure fragment. Masses and intensities are real measurements, not assigned formula labels. There is no assumed monotonicity between low and high response. Flatten query positions in this order: isolation 0's six probes, then isolation 1's six probes. Both response fields use exactly that order. For example, low_response=b:100010001001 and high_response=b:010010001100 describe the same twelve interventions/queries at the two settings. Position 0 is low-only, position 1 is high-only, position 4 is detected at both, and position 2 is not detected at either. This example illustrates the output grammar, not a synthetic training row. Probe Selection and Measurement Labels Only visible root-spectrum peaks choose the probes. For each measured isolation, candidates are root peaks at least 40 m/z and strictly below the isolated mass minus 2.0. Select the six strongest candidates, removing overlapping tolerance windows and pairs separated by approximately one singly charged carbon-isotope spacing, then sort by mass. Select isolations by descending matching root signal among complete measured low/high pairs, requiring their centers to differ by more than 2.0 so the two isolation windows are distinct and nonoverlapping. A representative root context is chosen using visible evidence before inspecting its daughter responses. The mass-matching half-width for query q is t(q) = max(0.003, 0.000010 q) in m/z units. Thus q=100 uses 0.003, while q=800 uses 0.008. A centroid matches when its absolute mass difference is at most t(q). The same absolute-plus-10-ppm rule checks the molecular ion against the neutral parent mass plus or minus 1.007276466621 and matches the root precursor path. For one actual MS3 spectrum and isolated mass p, define eligible daughters D as all positive-intensity centroids with m/z strictly less than p-2.0. This removes the residual isolated-ion neighborhood and higher-mass signal from the normalization. Let B be the largest intensity in D. For each probe q, define R(q) = sum of intensities in D within t(q) of q, divided by B. The response bit is 1 when R(q) >= 0.06, and 0 when R(q) <= 0.04. Ratios strictly between 0.04 and 0.06 are uncertain: the entire preselected case is excluded if any of its 24 measurements is uncertain. Cases with no eligible daughter signal, missing required scans, source-flagged chimeric spectra, precursor purity below 0.90, or unresolved alternate molecular assignments are also excluded. Selection never turns a missing experiment into a negative response. A bit of 0 means not detected above the operational relative-intensity boundary in that processed measured spectrum. It does not mean chemically impossible, absent at every concentration, or below a calibrated absolute detection limit. Export noise filtering, unresolved isobars, rearrangements and instrumental variation remain sources of uncertainty. The 4%-6% interval is a conservative operational guard around a 5% reporting boundary, not a statistically estimated confidence interval. For a numerical example, suppose eligible daughter intensities have maximum 100, and two matching centroids contribute 3 each to a query. R=0.06 and its bit is 1. A matching sum of 4 gives bit 0. A sum of 5 makes the case ineligible. A residual isolated precursor with intensity 10,000 is not used in B. Submission Format Write ./working/submission.csv with exactly the ordered columns case_id,low_response,high_response. Use one row for every test ID, no duplicates and no additional rows. Row order is immaterial. Do not provide probabilities, JSON arrays, separators inside the twelve bits, or numeric response cells. | case_id | low_response | high_response | | --- | --- | --- | | case_0123456789abcdef01234567 | b:100010001001 | b:010010001100 | The example ID is syntactically valid; use the actual IDs from test.csv. Each response cell must be a string of exactly 14 characters. A schema or ID error raises ValueError. Any malformed response cell gives the whole submission score 0, preventing malformed syntax from acting as a favorable abstention. A malformed reference target is an evaluation error, not an imputable label. If the backend adds visibility, it must appear in both frames in the identical column position and its values must match after ID alignment. A one-sided or mismatched visibility column is rejected. Evaluation The Isolation Response Score combines three views of the same measured response map: Score = 0.45 StateF1 + 0.35 DetectionF1 + 0.20 SwitchF1. | Component | Percentage | Experimental Priority | | --- | --- | --- | | StateF1 | 45% | Recover the complete two-energy response: absent at both, high-only, low-only, or present at both. This is the main decision, so it has the largest share. | | DetectionF1 | 35% | Credit useful daughter-ion detection even when its energy dependence is wrong. This substantial partial credit makes an incomplete but informative spectrum model distinguishable from guessing absence. | | SwitchF1 | 20% | Emphasize the direction of a change caused by higher energy. A smaller dedicated share keeps switching behavior important without making sparse switches the entire experiment. | The shares sum to 100%. These are overlapping assessments of one response map, not independent chemical endpoints. Switches already affect StateF1 and DetectionF1; the extra 20% is a deliberate emphasis, not an additional independent observation. With StateF1=0 the other terms contribute at most 0.55; with SwitchF1=0 the ceiling is 0.80. Weights express benchmark priorities rather than measured physical costs, and are not chosen to force a particular agent score. Within DetectionF1 the two energies have equal weight; within each macro F1 every truth-active class has equal weight. The two detection terms therefore contribute 17.5% each directly to the final score. On the complete evaluation, StateF1 averages all four classes and SwitchF1 averages both directional changes; in a smaller evaluation partition their documented absent-class rules apply. These nested shares do not imply independent error probabilities because the same response bits participate in all three components. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Exact valid predictions score 1 on every nonempty evaluation, including a backend partition containing only one response class. There is no whole-row exact-match bonus or penalty for chemically legal low-only versus high-only behavior. For a class c, F1(c) = 2TP(c) / (2TP(c) + FP(c) + FN(c)), counting all twelve query positions of every evaluated case together. Every case supplies twelve observations, so no case receives extra weight for having a larger root spectrum. Counts come from the evaluated reference labels; predictions never determine which reference classes are active. StateF1 is the unweighted mean of F1 over the response states present in the evaluated truth. Encode a pair as c=2L+H: 0 is neither detected, 1 is high-only, 2 is low-only, and 3 is both detected. On the complete evaluation, all four states are represented. This is the largest term because identifying the correct intervention response is the main scientific decision, including distinguishing shared daughters from unsupported ones. DetectionF1 is the mean of positive-detection F1 at low energy and positive-detection F1 at high energy. Neither gets true-negative credit when there are positive targets. If an energy has no true positive detections in a backend partition, that energy's term is instead the fraction of predictions equal to 0. This term receives 35% because a useful experiment model must recover observed daughter links with reasonable precision and recall, even when it confuses their energy dependence. SwitchF1 is the unweighted mean of F1 for the truth-active directional switch classes 1 and 2. If there are no true switches in a partition, use the fraction of predicted pairs that are valid nonswitches, 00 or 11. This 20% term emphasizes the experimental decision about whether higher energy changes detectability, without letting rare switches dominate all ordinary daughter identification. It measures direction, so exchanging low-only and high-only is an error. These weights express operational priorities, not optimized chemical constants or a claim of unique statistical optimality. What Makes This Interesting The root spectrum reports a mixture of fragmentation channels, while isolation conditions on a particular intermediate. Models must learn which observed daughter masses remain compatible with that branch and how a second energy intervention changes their relative signal. Molecular connectivity, neutral losses, root intensities and peak relationships can all matter. Formula containment alone is insufficient: ions can rearrange, disappear below an operational threshold, or fragment again at higher energy. What Not To Use Do not retrieve matching external spectra or construct source-identity lookup tables. Do not exploit case IDs, hashes, CSV row order, serialization lengths, or accidental source formatting as labels. Do not adapt to hidden evaluation feedback or exploit malformed submission parsing. Learned molecular representations, graph models, spectrum models and classical scientific baselines are allowed; source-spectrum lookup is not a learned solution to this task. &nbsp;
> Closes in 7h 2m
> 9 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

