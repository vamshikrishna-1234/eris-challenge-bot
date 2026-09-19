# Other Challenge Examples

Scrape timestamp: 2026-07-04T03:52:23+05:30

Confirmed examples in this document: 2

These entries are included because the challenge detail page displayed this domain. Titles were not used for classification.

## Chemical Ontology Anchor Repair
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78w2x85w87c0kezqjvbgfaf189sw92
- DOMAIN exactly as displayed: Other
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Curated chemical knowledge bases need reliable hierarchy anchors: when a new chemical term is proposed, reviewers must decide which broader chemical classes are strong parent anchors, which are merely related, and which would misplace the term. This challenge asks you to rank candidate anchors for each query chemical term using lossy chemistry profiles.
> Each row gives one lossy profile for a query chemical term and six lossy profiles for candidate anchors labeled A through F. Profiles summarize fixed-width chemistry cue flags, motif flags, broader semantic-family flags, a capped semantic-count bin, and a coarse synonym-signal bin without exposing source identifiers, exact source names, exact source definitions, or definition-length bins. In training rows, each candidate has an ordinal support label from 0 to 5. Higher support means the candidate is a better hierarchy anchor for the query term. Test rows hide those support labels. Your job is to submit the six labels in best-to-worst order.
> This is a practical chemistry text-ranking task. It rewards models that learn chemical class language, specificity, broader-vs-narrower relationships, and when a candidate is merely a related sibling rather than a useful anchor. It is not a plain compound-classification task because every test case has its own candidate set and the metric scores the full ranking, not only the top option.
> Dataset
> File descriptions
> train.csv -- 976 labeled query cases. Each row contains one query profile, six candidate anchor profiles, the ideal target_ranking, and train-only support labels support_A through support_F.
> test.csv -- 1,224 unlabeled query cases with the same query and candidate profile fields, but without support labels or the target ranking.
> sample_submission.csv -- A template with the required id and ranking columns, filled with random valid candidate permutations.
> train.jsonl -- Line-oriented mirror of train.csv for solvers who prefer JSON parsing.
> test.jsonl -- Line-oriented mirror of test.csv for solvers who prefer JSON parsing.
> Column descriptions
> id (string) -- Unique 12-character hexadecimal identifier for each query case.
> query_profile (string) -- Lossy fixed-width profile for the query term. Contains chemistry cue flags, motif flags, semantic-family flags, a capped semantic-count bin, and a coarse synonym-signal bin.
> option_A_profile (string) -- Lossy text profile for candidate anchor A.
> option_B_profile (string) -- Lossy text profile for candidate anchor B.
> option_C_profile (string) -- Lossy text profile for candidate anchor C.
> option_D_profile (string) -- Lossy text profile for candidate anchor D.
> option_E_profile (string) -- Lossy text profile for candidate anchor E.
> option_F_profile (string) -- Lossy text profile for candidate anchor F.
> target_ranking (string) -- Train-only ideal ranking of candidate labels from best anchor to weakest anchor.
> support_A (integer) -- Train-only support level for candidate A, from 0 to 5.
> support_B (integer) -- Train-only support level for candidate B, from 0 to 5.
> support_C (integer) -- Train-only support level for candidate C, from 0 to 5.
> support_D (integer) -- Train-only support level for candidate D, from 0 to 5.
> support_E (integer) -- Train-only support level for candidate E, from 0 to 5.
> support_F (integer) -- Train-only support level for candidate F, from 0 to 5.
> Evaluation
> Submissions are scored with normalized anchor ranking loss. Lower is better. The score is bounded from 0 to 100.
> For each row, the hidden support labels define an ideal ranking. The grader computes discounted cumulative gain for your submitted order, then normalizes the loss between the best and worst valid permutations for that same row:
> A perfect ranking scores 0. Ranking the candidates in the worst possible support order scores 100 for that row. Because the score uses the full candidate order, moving a strong anchor from first to third is penalized more than swapping two weak distractors.
> Submission
> Submit a CSV file with one prediction for every row in test.csv.
> id (string) -- The 12-character identifier from test.csv.
> ranking (string) -- A pipe-separated permutation of all six candidate labels, from strongest anchor to weakest anchor.
> Example:
> Requirements
> The file must contain exactly 1,224 rows plus the header.
> Every id from test.csv must be present exactly once.
> Every ranking must contain each of A, B, C, D, E, and F exactly once.
> Candidate labels must be separated by the pipe character, for example A|B|C|D|E|F.
> File format: .csv only, with exact column names id,ranking.
> What Not To Use
> Do not reverse-engineer the lossy profiles against public chemical hierarchy databases or ontology mirrors to recover hidden support labels.
> Do not use source identifiers, filename maps, row-order reconstruction, or external hierarchy dumps to infer the test answers.
> Do not build lookup tables from external copies of the same chemical hierarchy. The intended task is to learn anchor-ranking behavior from the public training rows.
> Do not submit a purely hand-coded rule system that ignores the training labels and ranks candidates only by fixed string templates or fixed label order.

Inspiration note: Useful because it preserves accepted challenge designs that do not fit the current named buckets while still offering task/metric patterns for ideation.

## Guitar Tablature Recovery From Real Guitar Performances
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bm68fgps9r8eg02rq8z1hp989xz9f
- DOMAIN exactly as displayed: Other
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio, Based on dataset:, GuitarSet Mono Microphone Audio And JAMS Annotations, Download Data
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Guitar Tablature Recovery From Real Guitar Performances
> You are given a short real acoustic-guitar audio clip and a compact note skeleton for that clip. The skeleton tells you each recoverable event's event_id and MIDI pitch. Your task is to predict the actual guitar tablature realization for every event: the string number and fret number used in the performance.
> This is not a standard automatic music transcription task. The pitch skeleton is already public, and a prediction can be musically pitch-correct while still being tab-wrong. For example, MIDI pitch 64 can be played as high-E string fret 0, B string fret 5, G string fret 9, D string fret 14, A string fret 19, or low-E string fret 24. The score rewards recovering the performed string/fret positions, not merely reproducing the public pitches.
> Use the training examples to learn how audio timbre, note context, local hand position, note density, and performance style affect string/fret choices. The public audio clips are short prepared excerpts with opaque IDs and no source filenames, performer IDs, original timestamps, raw onset times, or source-track metadata. The intended solution is an audio-plus-sequence model or feature pipeline trained on public/train.csv, with the note skeleton used for event identity and candidate-position constraints.
> What Not To Do (using these approaches can cause solution rejection regardless of score):
> Do not use external source-corpus lookup, public annotation search, audio fingerprinting, or filename/timestamp matching to recover hidden test labels.
> Do not use isolated-string or hexaphonic pickup audio, if you obtain it elsewhere; only the provided mono microphone clip is in scope.
> Do not infer labels from id, audio_path, row order, file sizes, file modification times, or any platform artifact outside the public files.
> Do not submit impossible string/fret positions for the public pitch, malformed JSON, duplicate event IDs, or extra/missing submission columns.
> Evaluation
> For each row, the grader parses tab_json, validates that the submitted event IDs exactly match the public skeleton, and checks every predicted (string, fret) against the physical guitar positions that can play that event's MIDI pitch. Invalid or impossible event positions receive zero for that event. Malformed or oversized JSON zeroes the affected row heads without crashing; structural CSV errors return 0.0.
> Event partial credit is:
> event = 0.84 * exact_string_and_fret
> + 0.08 * string_match
> + 0.08 * max(0, 1 - min(abs(fret_error), 5) / 5)
> The grader then computes:
> event_score = mean row event score
> chord_score = mean event-group set score
> row_exact   = fraction of rows with all events exact
> valid_score = mean physical-validity rate
> calibration = mean max(0, 1 - abs(confidence - row_exact_indicator))
> worst_group = lowest mean row-tab score across hidden groups
> Final = 0.30 * event_score^2.25
> + 0.10 * chord_score^1.90
> + 0.30 * row_exact
> + 0.06 * calibration^1.70
> + 0.20 * worst_group^1.90
> + 0.04 * valid_score^1.30
> Hidden groups cover performer family, musical style, polyphony band, ambiguity band, fret-range band, and note-density band. Performer family groups clips by the held-out source performer. Musical style groups clips by the source excerpt/style family. Polyphony band groups clips by the maximum simultaneous note count in the excerpt. Ambiguity band groups clips by how many physically valid string/fret positions can play the public pitches. Fret-range band groups clips by the true fret region used in the performance. Note-density band groups clips by the number of target note events in the 2.4 second clip. The worst-group term is the lowest mean row-tab score over those hidden axes, so a solution that only works on easy single-note or low-fret cases will not score as well as a robust solution.
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0. A perfect label submission with confidence 1.0 scores exactly 1.0.
> Dataset
> Files shipped to participants are listed below. All paths in CSVs are relative to public/. The prepared split contains 359 training rows, 233 test rows, and 592 audio clips total.
> Item	Description
> public/train.csv	Labeled training rows
> public/test.csv	Test rows, no labels
> public/audio/*.wav	Mono WAV clips
> public/sample_submission.csv	Submission template
> The audio files are source-rate mono WAV excerpts cut from the official mono microphone recordings. Each prepared WAV is 16-bit PCM, 44,100 Hz, one channel, and 2.40 seconds long. There is one audio clip per row: 359 clips referenced by train.csv and 233 clips referenced by test.csv.
> public/train.csv has 359 rows. It contains the public input columns id, audio_path, notes_json, clip_start_s, and clip_duration_s, plus the train-only label columns tab_json and confidence_label. The tab_json label is a JSON list of event objects, each with event_id, string, and fret. The confidence_label column is a float in [0, 1]; it is 1.0 for these official annotation-derived labels and may be used as an optional training sample weight.
> Column	Type	Description
> id	string	Opaque row id
> audio_path	string	Relative WAV path
> notes_json	JSON string	Event skeleton
> clip_start_s	float seconds	Clip-local start
> clip_duration_s	float seconds	Clip length
> tab_json	JSON string	Train label
> confidence_label	float [0,1]	Label weight
> For train.csv, id is a salted opaque row identifier and is not source metadata. audio_path points to a WAV under public/audio/. notes_json is a compact JSON list whose items contain event_id as a string and pitch_midi as an integer MIDI pitch. clip_start_s is a float in seconds and is always 0.0, because it is relative to the prepared clip, not the source recording. clip_duration_s is a float in seconds and is always 2.4. tab_json is the training target: a JSON list with exactly one {event_id,string,fret} object per public note event, where string is an integer from 1 to 6 and fret is an integer from 0 to 24.
> public/test.csv has 233 rows. It has the test input columns id, audio_path, notes_json, clip_start_s, and clip_duration_s, with tab_json and confidence_label removed. The clip_start_s value is relative to the prepared clip, not the source recording.
> Column	Type	Description
> id	string	Opaque row id
> audio_path	string	Relative WAV path
> notes_json	JSON string	Event skeleton
> clip_start_s	float seconds	Clip-local start
> clip_duration_s	float seconds	Clip length
> For test.csv, id, audio_path, notes_json, clip_start_s, and clip_duration_s have the same types and meanings as in train.csv. Each notes_json cell is a compact JSON list. Every item has event_id and pitch_midi. It never includes source timing, source order, string, or fret.
> public/sample_submission.csv is a submission template with the exact columns id, tab_json, and confidence, filled with a weak physically-valid baseline.
> Column	Type	Constraint
> id	string	Same ids as test
> tab_json	JSON string	One tab per event
> confidence	float	In [0, 1]
> Submission
> Submit a CSV file with exactly these three columns in this order: id, tab_json, confidence. The id set must match public/test.csv exactly, with no duplicates.
> Each tab_json value must be a JSON list. The list must contain exactly one object for every event in that row's notes_json; event IDs must match exactly. Each object must have this form:
> [{"event_id":"e00","string":2,"fret":5},{"event_id":"e01","string":1,"fret":3}]
> Valid strings are integers 1 through 6, where string 1 is the high E string and string 6 is the low E string. Valid frets are integers 0 through 24. Predictions that cannot play the public MIDI pitch are penalized even if they are in range.
> Example submission rows:
> id,tab_json,confidence
> gt_0011223344556677,"[{""event_id"":""e00"",""string"":2,""fret"":5}]",0.62
> gt_8899aabbccddeeff,"[{""event_id"":""e00"",""string"":3,""fret"":9},{""event_id"":""e01"",""string"":2,""fret"":5}]",0.48
> Enforcement On Invalid Approaches
> Submissions based on external source lookup, annotation search, audio fingerprinting, isolated-string audio, row-order side channels, or grader-format exploitation may be rejected before payout. The task is to learn the relationship between the provided mono audio, the note skeleton, and the performed tablature positions from the public training data.

Inspiration note: Useful because it broadens the challenge design space with an unusual modality or output format that can inspire cross-domain benchmarks.
