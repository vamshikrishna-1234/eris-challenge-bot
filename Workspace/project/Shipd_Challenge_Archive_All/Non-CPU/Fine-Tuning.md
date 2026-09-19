# Non-CPU Fine-Tuning Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 57

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Hive Audio Queen-State And Activity Profile Triage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79v7wtvk0fqahm9v0s08fes18a15pj
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Problem Description
> Beekeepers and hive-monitoring systems need to interpret noisy colony audio without opening the hive: is the colony in a normal active state, is there a queen-state concern, is the recording mostly hive sound or contaminated by external events, and how reliable is the acoustic evidence? This challenge uses real beehive recordings and asks for a multi-head triage profile from short redacted hive-audio clips.
> Overview
> Objective: given a short mono WAV clip recorded inside or near a real beehive, predict the hive-state class, the Bee/noBee activity profile, the external-noise fraction bucket, the acoustic risk context, and a calibrated confidence value.
> The audio was collected in real hive-monitoring settings. Some recording sessions came from varied field conditions with different recording devices, surrounding environments, and microphone placements, while other sessions came from more controlled monitoring conditions. The prepared challenge standardizes the selected recordings into 189 short public WAV clips: 108 labeled training clips and 81 hidden-label test clips.
> Prepared public clips are mono PCM_16 WAV files at 16,000 Hz. Clip durations range from about 5.75 to 6.20 seconds, with coarse duration buckets exposed only as short, standard, or long. Public train labels have these counts: hive_state has 45 active_normal, 45 queen_missing, and 18 queen_present; bee_activity_profile has 35 pure_bee, 24 mostly_bee, 23 mixed_external_noise, and 26 mostly_external; external_noise_fraction_bucket has 35 trace, 24 low, 23 medium, and 26 high; acoustic_risk_context has 11 calm, 31 active_normal, 21 disturbed_noise, and 45 queen_concern. Test labels are hidden.
> Each row contains an opaque id, a non-identifying WAV path, and coarse clip-duration metadata. Public training rows include target labels. Public test rows hide all target labels. The public clips preserve the real hive-audio signal needed for learning, while label-bearing raw identifiers, raw timestamps, hive/session identifiers, collection names, and raw row order are not public.
> What not to use: use only the provided public files. Do not recover original filenames, hive ids, recording ids, timestamps, label files, or raw row order; do not match public clips against any external copy of the raw recordings; do not use public filename, id, duration, file-size, or metadata shortcuts; do not submit a binary Bee/noBee detector as if it solved the whole triage task. Strong solutions should learn acoustic models from the provided public training clips and labels.
> Task Specification
> For every test id, submit exactly these values: hive_state, bee_activity_profile, external_noise_fraction_bucket, acoustic_risk_context, and confidence.
> hive_state is one of active_normal, queen_present, or queen_missing.
> bee_activity_profile is one of pure_bee, mostly_bee, mixed_external_noise, or mostly_external.
> external_noise_fraction_bucket is one of trace, low, medium, or high.
> acoustic_risk_context is one of calm, active_normal, disturbed_noise, queen_concern, or uncertain.
> confidence is a float in [0, 1] estimating row-level reliability.
> Dataset
> The public dataset contains labeled training clips, hidden-label test clips, and a sample submission. Audio paths are relative to the public/ directory. Train and test rows are sorted by opaque id, and the ids do not encode split, recording origin, hive state, or label values.
> Public Files
> train.csv includes public input columns and all target columns. test.csv includes the same public input columns without target labels. The sample submission is a weak schema-valid baseline, not a competitive solution.
> train.csv Columns
> The allowed values for the four categorical target columns are listed in the Task Specification. clip_duration_bucket is a coarse public duration bin and is not a recording-origin id or target label.
> Plain column definitions: id is the opaque public row id; audio_path is the relative WAV path; clip_duration_sec is the prepared clip duration; clip_duration_bucket is a coarse duration bin; hive_state, bee_activity_profile, external_noise_fraction_bucket, acoustic_risk_context, and confidence are train-only label columns.
> test.csv Columns
> The test file withholds all target columns and does not include original filenames, raw paths, label-file ids, hive ids, collection names, raw timestamps, label words, or interval fractions.
> Plain test column definitions: id is the opaque public row id; audio_path is the relative WAV path; clip_duration_sec is the prepared clip duration; clip_duration_bucket is a coarse duration bin.
> Submission Format
> Submit exactly one row for every test id, with columns in the exact order shown above. Unknown or malformed categorical strings receive no credit for the affected head. Strings longer than 64 characters are treated as malformed. Missing values, wrong columns, duplicate ids, row-set mismatch, non-numeric confidence, non-finite confidence, and confidence outside [0, 1] are invalid submissions.
> Example submission rows:
> id,hive_state,bee_activity_profile,external_noise_fraction_bucket,acoustic_risk_context,confidence
> hive_019a7d5afac4f5,active_normal,mostly_bee,medium,uncertain,0.63636
> hive_04752eeca4fe02,queen_missing,mostly_external,high,queen_concern,0.63636
> hive_04eeb74d2c4377,queen_missing,pure_bee,medium,uncertain,0.63636
> Evaluation
> Structural invalidity raises an invalid-submission error: missing, extra, or reordered columns; duplicate ids; an id set different from test.csv; missing cells; non-numeric confidence; non-finite confidence; or confidence outside [0, 1]. Malformed categorical strings are length-capped and scored as invalid predictions for the affected heads rather than crashing the grader.
> For each categorical head, the grader computes macro-F1 over answer classes present in the hidden test set and exact accuracy over rows. HeadScore = 0.72*MacroF1 + 0.28*Accuracy.
> The row exactness score is the fraction of rows where all four categorical heads are exactly correct. The hidden confidence answer is a row-level label reliability value in [0, 1] derived during preparation from label-interval coverage and label certainty. For each row, ConfidenceCredit = max(0, 1 - abs(submitted_confidence - hidden_confidence) / 0.5). If any categorical prediction in that row is malformed or outside the allowed values, that row's confidence credit is 0. ConfidenceScore is the mean ConfidenceCredit over all test rows.
> BaseProfile = 0.22*HiveStateScore + 0.19*ActivityScore + 0.14*NoiseBucketScore + 0.10*RiskContextScore + 0.25*RowExact + 0.10*ConfidenceScore.
> Hidden robustness groups are based on collection setting, hive state, activity profile, external-noise group, and duration bucket. WorstGroup is the minimum BaseProfile over those hidden buckets.
> FinalScore = 0.78*BaseProfile + 0.22*WorstGroup.
> The theoretical minimum is 0.0; the theoretical maximum is 1.0; higher is better. A perfect submission with every hidden target and confidence exactly correct scores 1.0.
> Intended Solution
> Strong approaches should train or fine-tune audio models on the provided training clips, or train a suitable audio model from scratch. Submissions should learn from the public audio and labels rather than relying on external raw-data lookup, filenames, fixed rules, or hand-written shortcuts.
> Metadata-only, duration-only, id-order, and filename approaches are intentionally weak. A binary Bee/noBee detector is incomplete because the score also rewards queen-state triage, external-noise bucketing, risk context, exact row profiles, hidden-group robustness, and calibration.
> Enforcement On Invalid Approaches
> Submissions based on raw-row lookup, recovered original filenames, hive/session ids, external label files, raw timestamps, audio fingerprint matching against external raw recordings, hosted commercial audio-recognition APIs, manual hidden-test labeling, hardcoded id-to-answer maps, row-order shortcuts, or grader/filesystem exploitation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned hive-audio triage from the provided public training split.

Inspiration note: Useful because it suggests a domain adaptation setup where compact supervised training can beat shallow heuristics.

## Infant Gut Microbe HMO Metabolite Release Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dh0a4m2t2k6jt44jwkzakz1892asb
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Human milk contains oligosaccharides that infants do not directly digest; gut microbes consume different subsets of these milk-sugar families and may release smaller metabolites that other microbes can use. This is a bioinformatics text/sequence modeling task. Each example is an instruction-style biological record made from a serialized infant gut microbe or small-community profile, a serialized HMO substrate-mixture profile, and a short diet-context token. Given the text-encoded reconstruction sketch, predict the released metabolite-family set, the HMO utilization bucket, the community cross-feeding behavior, and a calibrated confidence.
> The public microbe profiles are source-scrubbed sketches derived from real genome-scale metabolic reconstructions. They contain generic binned pathway motif tokens rather than raw model names, reaction IDs, strain identifiers, source file paths, exact enzyme names, released-metabolite names, or taxonomy. The CSV files are only the transport container; the modeling input is the serialized biological text in task_prompt, community_profile_json, and substrate_mixture_json. The intended solution is to train or fine-tune a local text/sequence model that reads those token sequences jointly and learns the mapping to metabolic outcomes from the public training examples.
> What To Use: fine-tune a compact open text or sequence encoder on the public training examples, train a small token-level model from scratch over the serialized profile strings, or use learned sequence embeddings with structured output heads. The productive path is to learn how community-profile tokens and HMO mixture tokens interact, then calibrate the multi-output prediction on the public labels.
> What Not To Use (any of these can cause solution rejection regardless of leaderboard score):
> Raw-source lookup, web search, external reconstruction databases, or model-name recovery for hidden rows.
> Reverse mapping public IDs, motif sketches, row order, or profile strings to source model filenames or strains.
> Using the raw upload files, private answers, hidden split metadata, or challenge scripts as prediction oracles.
> Hardcoded maps from test IDs or exact public profile strings to answers.
> Taxonomy-only, metadata-only, majority-label, or substrate-only submissions that ignore the combined community and substrate signals.
> Generic feature-vector-only classifiers over community_size, diet_context, substrate counts, or profile-length statistics as the main prediction mechanism.
> A fixed rule-only decoder that does not learn from the public labeled examples.
> Hosted closed-model APIs for prediction, distillation, or pseudo-labeling.
> Enforcement on invalid approaches: solutions that do not solve the intended reconstruction-informed metabolism task may be rejected before payout. The goal is to reward learned biological sequence reasoning over anonymized pathway sketches and HMO substrate-mixture strings, not source lookup, metadata shortcuts, or label-prior exploitation.
> Evaluation
> The grader computes three prediction heads, complete-row consistency, and calibration. metabolite_family_json is scored by exact-set-aware family F1: an exact family set receives full credit, while broad over-predicted common sets receive heavily limited partial credit. utilization_bucket and cross_feeding_bucket require exact labels. confidence is calibrated against the row's partial-head task score.
> Partial-head score is (0.48*metabolite_family_score + 0.22*utilization_exact + 0.20*cross_feeding_exact) / 0.90. Complete-row exactness is 1 only when all three non-confidence heads are exactly correct, otherwise 0. Row score uses: 0.15*partial_head_score + 0.75*complete_row_exact + 0.10*calibration.
> The final score blends mean row performance with hidden robustness groups: 0.72*mean + 0.10*worst_utilization_group + 0.10*worst_mixture_group + 0.08*worst_community_size_group.
> Higher is better. The theoretical minimum for structurally valid submissions is 0.0. Structural CSV failures raise InvalidSubmissionError and are rejected rather than assigned a leaderboard score. The theoretical maximum is 1.0; perfect hidden labels with confidence 1.0 score exactly 1.0.
> The grader raises InvalidSubmissionError if submission columns are missing, extra, or reordered; if IDs are missing, duplicated, or do not exactly match test.csv; or if any confidence is missing, non-finite, or outside [0,1]. Malformed or over-long JSON in metabolite_family_json scores zero for that row's family head without crashing the grader. Rows with malformed categorical content also receive zero calibration credit, so invalid labels cannot earn confidence-only points.
> Dataset
> Prepared files are under public/. Although the files use CSV for platform compatibility, each record should be treated as a text-to-structured-output training example. train.csv contains serialized biological inputs and labels. test.csv contains the same serialized inputs without labels. sample_submission.csv is a valid weak template. label_schema.json lists allowed labels.
> File overview
> Item	Description
> train.csv	Serialized inputs plus labels
> test.csv	Serialized inputs only
> sample_submission.csv	Valid template
> label_schema.json	Allowed labels
> train.csv columns
> community_profile_json is a serialized JSON object with a community size and per-member sketch fields. Each member has a slot, generic motif_bins, network_scale, and exchange_hint_bin; exact taxonomy, enzyme names, reaction IDs, and released-metabolite names are not public. substrate_mixture_json is a serialized JSON list of HMO substrate-family availability values whose weights sum to one. These JSON strings are the primary token sequences for the model. diet_context is one of milk_only, milk_mucin_trace, or milk_solids_trace. community_size is 1, 2, or 3. The three target columns are train-only labels.
> Column	Type	Description
> id	string	Opaque row id
> community_profile_json	string	Community token sketch
> substrate_mixture_json	string	HMO mixture tokens
> diet_context	string	Diet context
> community_size	int	Member count
> task_prompt	string	Task instruction
> metabolite_family_json	string	Family labels
> utilization_bucket	string	HMO use label
> cross_feeding_bucket	string	Dependency label
> Allowed metabolite families are fucose_pool, sialate_pool, lactose_galactose_pool, lacto_n_biose_triose_pool, n_acetylhexosamine_pool, and intact_lacto_n_intermediate.
> Allowed utilization buckets are none, low, moderate, and high.
> Allowed cross-feeding buckets are limited_or_uncertain, independent_utilizer, requires_partner, and releases_shared_intermediates.
> The training-only column metabolite_family_json is the released-metabolite family target as a JSON array of allowed family strings.
> The training-only column utilization_bucket is the HMO-use target with values none, low, moderate, or high.
> The training-only column cross_feeding_bucket is the community dependency target with values limited_or_uncertain, independent_utilizer, requires_partner, or releases_shared_intermediates.
> test.csv columns
> test.csv has the same serialized input fields as train.csv, without the three target labels.
> Column	Type	Description
> id	string	Opaque row id
> community_profile_json	string	Community token sketch
> substrate_mixture_json	string	HMO mixture tokens
> diet_context	string	Diet context
> community_size	int	Member count
> task_prompt	string	Task instruction
> The test input column task_prompt repeats the prediction instruction for each row and does not contain hidden labels.
> Submission
> Submit a CSV with exactly one row per id in test.csv and exactly these columns in this order: id, metabolite_family_json, utilization_bucket, cross_feeding_bucket, confidence.
> metabolite_family_json must be a JSON array of allowed family strings. JSON key order is irrelevant because this field is an array, but duplicate family labels are invalid row content and receive zero family credit. confidence must be a finite float from 0 to 1.
> Column	Type	Constraint
> id	string	Same ids as test
> metabolite_family_json	string	JSON family list
> utilization_bucket	string	Allowed bucket
> cross_feeding_bucket	string	Allowed bucket
> confidence	float	In [0,1]
> Example submission rows:
> id	metabolite_family_json	utilization_bucket	cross_feeding_bucket	confidence
> igm_0123abcd4567ef89	["fucose_pool"]	low	limited_or_uncertain	0.42
> igm_abcdef0123456789	[]	none	limited_or_uncertain	0.30

Inspiration note: Useful because it suggests a domain adaptation setup where compact supervised training can beat shallow heuristics.

## Selective Emotion Unlearning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77cr8zvdchqetpkt0z71c52s843zje
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Fine-tune a model to classify text into emotion categories, then selectively unlearn 5 designated categories while retaining performance on the remaining 23.
> The training set contains ~5,200 user comments labeled with anonymized emotion categories (emotion_01 through emotion_23 for retained, forget_01 through forget_05 for forget targets). Five categories are designated as "forget targets" (listed in forget_targets.txt). The model must:
> Accurately classify the 23 retained categories
> Successfully "forget" the 5 target categories -- when encountering text that expresses a forget category, the model should NOT predict that category
> Detect whether a given text contains a forget-target category
> Predict emotional intensity
> Three targets must be predicted for each test example:
> Primary Emotion (28 classes) -- The dominant emotion, but forget-target categories should be replaced with the nearest retain category
> Is Forgotten (binary) -- Whether the text contains a forget-target category
> Emotional Intensity (float 0-1) -- How intensely the emotion is expressed
> The test set includes adversarial probes -- synthetic examples designed to trick the model into predicting forgotten categories. These probes use language patterns associated with forget-target categories but should be classified as retained categories. This tests whether unlearning is robust to adversarial elicitation.
> The evaluation is retention-driven: it rewards macro-F1 on the 23 retained categories, gated by successful UNLEARNING and adversarial-probe ROBUSTNESS, with FORGET DETECTION and INTENSITY as smaller quality factors, stratified by ambiguity level.
> Evaluation
> Score = ProbeRobustness x HarmonicMean(C_low, C_mid, C_high)
> The final Score is retention-driven with unlearning as a gate: successful forgetting is necessary but not sufficient. Merely avoiding forget-category predictions satisfies the gates but earns little on its own; the score is dominated by how well the model retains the 23 kept categories, and it is scaled down whenever the model leaks forget categories.
> Each ambiguity-bucket composite C is a product, not a weighted sum:
> C = UnlearningScore x RetainF1^2 x (0.50 + 0.50 x Competence)
> where Competence = 0.60 x ForgetDetectF1 + 0.40 x IntensityScore is a quality modifier in [0, 1], so the factor (0.50 + 0.50 x Competence) lies in [0.50, 1.0]. RetainF1 is the primary driver, and it enters squared (RetainF1^2) so imperfect retention is penalized steeply -- a high score demands near-perfect retention, not merely good retention. UnlearningScore multiplies the entire bucket, so incomplete forgetting collapses that bucket regardless of retention. The three bucket composites are combined with a harmonic mean (a model must perform in every ambiguity bucket), and that is multiplied by the global ProbeRobustness gate. Every factor reaches 1.0 only at perfection, so the score spans the full [0, 1] range and a flawless submission scores 1.0 -- the difficulty comes from how steeply the score falls off below perfection, not from any cap.
> Retain F1 (primary driver, entered squared): Macro-averaged F1 on retained-category examples, evaluated across the entire space of 23 retained categories (emotion_01 .. emotion_23). Categories absent from a bucket count as 0, so the metric cannot be inflated by scoring only the classes that happen to appear. Because the composite uses RetainF1^2, an agent must retain almost perfectly to score highly -- e.g. retain-F1 0.85 contributes 0.72 and 0.75 contributes 0.56 before the gates and modifier.
> Unlearning Score (multiplicative gate): For in-bucket examples whose true label is a forget category, 1.0 minus the fraction of predictions that are forget categories. Because it multiplies the bucket, incomplete forgetting scales the whole bucket toward 0.
> Forget Detection F1 (competence modifier): Binary F1 for detecting whether a text contains a forget-target category.
> Intensity Score (competence modifier): IntensityScore = max(0, 1 - 2 x MAE), where both values are in [0, 1]. The factor of 2 makes intensity a genuine signal rather than free credit for predicting the population mean.
> Probe Robustness (final multiplicative gate): 1.0 minus the fraction of adversarial-probe predictions that are forget categories, computed once globally. Leaking forget categories on probes scales the entire final score down; a model that never leaks scores 1.0 here. Probe rows are not flagged in test.csv -- the grader holds a private label_group flag and selects this subset, so the probe sample size stays stable.
> HarmonicMean = 3 / (1/C_low + 1/C_mid + 1/C_high)
> Because unlearning and probe-robustness are gates rather than additive credit, and because retention enters squared, reaching a high score requires near-perfect retention (macro-F1 across all 23 retained categories in every ambiguity bucket) while fully unlearning the forget categories. Shallow solutions that only suppress forget labels score low, and strong-but-imperfect solutions fall well short of the top of the range. The full [0, 1] range is available -- a flawless solution scores 1.0 -- but 0.7 is a demanding bar that only near-perfect retention approaches.
> Higher score is better. Score range is [0, 1].
> Dataset
> 7,091 user comments labeled with anonymized emotion categories, split into 5,243 train rows and 1,848 test rows.
> File Structure
> train.csv -- 5,243 labeled training examples
> test.csv -- 1,848 unlabeled test examples
> forget_targets.txt -- List of 5 categories to unlearn
> sample_submission.csv -- Example submission format
> train.csv
> Labeled training data with columns:
> id (int): Unique sample identifier
> text (string): Comment text
> all_labels (string): Comma-separated list of all category labels (multi-label)
> primary_emotion (string): The dominant category label
> contains_forget_emotion (int, 0 or 1): Whether any forget-target category is present
> forget_emotions_present (string): Comma-separated forget categories in this text
> label_group (string): retain_only, forget_only, or mixed
> ambiguity_score (float, 0-1): How ambiguous the emotional content is
> emotional_intensity (float, 0-1): How intensely the emotion is expressed
> n_labels (int): Number of categories assigned
> Categories:
> 23 retained categories: emotion_01 through emotion_23
> 5 forget targets: forget_01 through forget_05 (listed in forget_targets.txt)
> Label Group Distribution (train):
> retain_only (~4,510 train): Text with only retained categories
> forget_only (~417 train): Text with only forget-target categories
> mixed (~316 train): Text with both retained and forget-target categories
> test.csv
> id (int): Unique sample identifier
> text (string): Comment text
> forget_targets.txt
> Plain text file listing the 5 categories to unlearn, one per line.
> sample_submission.csv
> id (int): Row identifier from test.csv
> primary_emotion (string): Predicted category (prefer retained categories)
> is_forgotten (int): 1 if forget-target detected, 0 otherwise
> emotional_intensity (float): Predicted intensity (0-1)
> Submission
> Submit a CSV file with columns: id, primary_emotion, is_forgotten, emotional_intensity
> Example:
> id,primary_emotion,is_forgotten,emotional_intensity
> 10234,emotion_01,0,0.45
> 20891,emotion_23,1,0.20
> 30456,emotion_03,0,0.82
> Requirements:
> Must contain exactly 1,848 rows (one per test sample)
> Must include a header row
> Each id must match an id from test.csv
> primary_emotion must be one of the 28 anonymized category strings -- emotion_01 through emotion_23 (retain) or forget_01 through forget_05 (forget). The grader accepts forget_01 through forget_05 as valid string values so a submission containing them is not rejected, but each such prediction is treated as an unlearning failure: it reduces UnlearningScore on forget-truth rows and ProbeRobustness on adversarial-probe rows. A well-unlearned model should never emit a forget_ label.
> is_forgotten must be 0 or 1
> emotional_intensity must be a float between 0 and 1
> Disallowed Techniques
> The following approaches are explicitly disallowed. Submissions relying on them will be rejected.
> No hosted LLM APIs for inference or label generation (OpenAI, Anthropic, Google, Cohere, Mistral hosted endpoints, or any other commercial API). Predictions must come from a model you fine-tuned locally on the provided training set.
> No pretrained emotion classifiers of any kind (GoEmotions-fine-tuned checkpoints, sentiment heads such as bertweet-base-emotion, emotion-english-distilroberta-base, or any other off-the-shelf emotion head). Emotion predictions must come from your own fine-tuned head.
> No zero-shot or few-shot prompting of a frozen base model as the submission. Genuine fine-tuning with a measurable training-loss decrease is required.
> No fake fine-tuning (lr <= 1e-9, single-step training, all-zero LoRA adapters, or any setup designed to bypass training while looking like fine-tuning).
> No simple keyword filtering of forget categories at the output (e.g., predict argmax over retained classes only). Such "shallow unlearning" is detected by the adversarial probe component, which penalises models that have not internalised the forget concept.
> No hand-labelling of the test set, no manual labels merged into the submission CSV, and no human-in-the-loop annotation of test rows.
> No retrieval from external labelled emotion corpora at inference that effectively looks up labels (any public emotion-classification dataset). Test predictions must come from the fine-tuned model, not nearest-neighbour lookup against external labelled data.
> No use of the label_group, contains_forget_emotion, forget_emotions_present, ambiguity_score, or n_labels columns as test-time features. These appear only in train.csv; they do not exist for the test rows and must not be fabricated.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Contour Recovery From Field Recordings

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78bxjtf1zzcwr573c55drhd18bkenq
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Hearing Tone in an Undocumented Language: Contour Recovery from Field Recordings
> The problem
> A linguist sits in a village with a wordlist and a cheap recorder. The language has fewer than a thousand speakers, no writing system, and no dictionary. Nobody has written it down before. Word by word, the linguist elicits a form, records it, and writes what they hear in IPA.
> Writing the consonants and vowels is the tractable part. Writing the tone is not. The language is tonal: pitch is lexical, part of the word, as much a part of ɕi meaning one thing rather than another as the consonant is. But pitch does not sit in the segments. It has to be heard, and heard again, and argued about. This is the step that stalls language documentation, and it is the step that automatic tools skip. State of the art universal phone recognizers transcribe the segments of an arbitrary language and emit no tone at all.
> You are given the recording and the segments. You produce the tone.
> For each utterance you receive a WAV file and its toneless phonetic transcription, and you must output the sequence of Chao tone contours the utterance carries, one per tone bearing syllable, in order. The tone marked reading is never shown to you. The task is to hear pitch in a field recording of a language with under an hour of documented audio in existence.
> This is a sequence labelling task grounded in audio. The input is a waveform plus a string, and the output is a contour sequence conditioned on both. Natural approaches are a neural audio encoder with a per slot contour head, a CTC or attention decoder over the contour vocabulary, or a fine tuned pretrained speech model with a small tagging head on top. What it is not is a lookup. There is no lexicon of this language to consult, because none exists.
> Tone is lexical, so the transcription cannot tell you the answer. This is the property the whole task rests on, and it is measurable rather than asserted. Conditioning on the segmental string leaves 57 percent of the tonal uncertainty intact: entropy falls from 1.384 bits to 0.784 bits and no further. Of syllables that appear five or more times in the corpus, 67 percent carry different tones in different words, and 75 percent of all syllable tokens belong to a syllable type whose tone varies. Even an oracle that knew the most common tone for every syllable, computed on the test set itself, would cap at 71.7 percent accuracy. The pitch is in the audio or it is nowhere.
> The split is type disjoint, and seeded with minimal pairs. No tone marked word form appears in both train and test, and the repeated recordings of a single word never straddle the boundary. But toneless forms are deliberately allowed to cross: a small share of test forms have the same consonants and vowels as something in training and a different tone. Those rows exist specifically to punish a model that has learned to map spelling to pitch.
> Fifty one minutes of audio is close to the entire documented corpus of this language. Not a subsample. There is no larger version to scrape and no second corpus to pretrain on, because the recordings in this dataset are close to the sum of what exists. The field recorder was chosen for price, not fidelity, so the audio sounds like real documentation work rather than a studio. Learning a pitch representation from forty one minutes of training audio is the problem, and four minutes of extra untranscribed clips are released for anyone who wants to pretrain on them.
> The rare contour counts as much as the common ones. Two contours cover 89 percent of the tone slots and the third covers 10 percent. Macro averaging weights all three equally, so a model that never emits the falling contour throws away a third of the available score. Recovering the minority contour is where the points are.
> There is nothing to look up. No lexicon, no orthography, no parallel corpus, no second transcription of this language exists anywhere. Automatic phone recognition for undocumented languages is an active area, but the systems built for it discard tone by construction, so no published method addresses this task. Every point on the leaderboard has to come from a model you train on the audio in front of you.
> Data
> Three CSV files and a directory of audio. Text fields are quoted in the standard CSV way, and all files are UTF-8. The transcriptions are IPA and contain non-ASCII characters throughout.
> train.csv gives you the recording, the toneless transcription, and the tone sequence:
> Column          Type     Meaning
> --------------------------------------------------------------------------
> id              string   Row identifier
> audio_path      string   Path to the WAV file, relative to the data root
> transcription   string   Toneless IPA transcription of the utterance (input)
> n_tones         int      Number of tone slots to predict
> tones           string   Space separated tone contour per slot (label)
> A sample train.csv row:
> id,audio_path,transcription,n_tones,tones
> tus_2975ac316be4ee0b,audio/train/tus_2975ac316be4ee0b.wav,kɕiefɯ,2,˥˧ ˥˩
> The word kɕiefɯ has two tone bearing syllables. The first carries a high falling contour and the second a high to low falling contour.
> test.csv has the same columns except tones, which is withheld:
> Column          Type     Meaning
> --------------------------------------------------------------------------
> id              string   Row identifier
> audio_path      string   Path to the WAV file, relative to the data root
> transcription   string   Toneless IPA transcription of the utterance (input)
> n_tones         int      Number of tone slots to predict
> A sample test.csv row:
> id,audio_path,transcription,n_tones
> tus_8a076e736bc42cc8,audio/test/tus_8a076e736bc42cc8.wav,ɕikəda,3
> The contour vocabulary
> Three contours occur in the language, written in Chao tone letters:
> Contour   Description          Train share   Test share
> ------------------------------------------------------
> ˥˧       high falling               48.4%        46.3%
> ˧˩       mid to low falling         41.7%        43.3%
> ˥˩       high to low falling         9.9%        10.4%
> Every tone slot carries exactly one of these three. There are no other values.
> Audio
> Property            Value
> ------------------------------------------------
> Format              16 kHz, mono, 16-bit PCM WAV
> Normalisation       peak normalised
> Training audio      41 minutes across 1,785 clips
> Test audio          10 minutes across 449 clips
> Labeled total       51 minutes across 2,234 clips
> Median clip length  1.30 s
> Range               0.22 s to 4.77 s
> Unlabeled audio     4 minutes across 158 clips
> Every recording is a single word or short phrase spoken in isolation, elicited from a comparative wordlist. audio/unlabeled/ holds clips for which no transcription exists in the source corpus. They have no labels and never will, and they are provided only in case self supervised pretraining is useful to you.
> Dataset facts
> Quantity                          Value
> ------------------------------------------------------------------
> Source                            field recordings, endangered tone language
> Training rows                     1,785
> Test rows                         449
> Training tone slots               5,126
> Test tone slots                   1,259
> Tone slots per utterance          median 3, range 1 to 9
> Transcription length              median 7 characters, max 28
> Transcription character vocab     43
> Contours                          3
> Split                             type disjoint by tone marked form
> Because the corpus records the same word several times, and because word forms are kept whole when splitting, the 1,785 training rows cover 567 distinct toneless forms and the 449 test rows cover 141. Some transcriptions contain a space, which marks a word boundary in a multi word phrase. Tone slots are counted across the whole utterance, so a two word phrase yields one flat contour sequence rather than two.
> All transcriptions are released in Unicode NFD, so combining diacritics are stored separately from their base letters: a nasalised vowel is two codepoints, not one. If you build a character level model, normalise consistently or your vocabulary will fragment. The 43 character vocabulary counts combining marks as their own symbols.
> The labels come from the corpus author's own narrow phonetic transcription. Where the transcription writes the tone marks for several syllables together after a multi syllable chunk, those marks are split back into one contour per syllable, so the target is always one contour per tone bearing syllable.
> How a submission is scored
> Each predicted contour sequence is aligned to the reference by position: the first predicted contour describes the first tone slot, the second the second, and so on. Grading compares contours at every slot and computes a macro averaged F1 across the three contours. For each contour, precision, recall and F1 are computed treating that contour as the positive class, and the three F1 scores are averaged with equal weight:
> for each contour in {˥˧, ˧˩, ˥˩}:
> precision = correct predictions of this contour / all predictions of this contour
> recall    = correct predictions of this contour / all reference slots of this contour
> f1        = 2 * precision * recall / (precision + recall)
> score = mean(f1 over the three contours)
> Macro averaging means the rare high to low falling contour matters as much as the two common ones, even though it covers under a tenth of the slots.
> Scoring conventions:
> Situation                                    Effect
> ------------------------------------------------------------------------
> Positions past the end of the reference      ignored
> Rows in any order                            joined on id, order does not matter
> Extra columns                                ignored
> Prediction shorter than the reference        missing slots scored as the
> most frequent contour
> Token that is not one of the three contours  scored as the most frequent
> contour
> An id in the test set missing from your file all its slots scored as the
> most frequent contour
> There is deliberately no way to abstain. Anything unusable resolves to the most frequent contour rather than being skipped, because skipping would remove a false positive without changing recall, letting a submission buy precision by emitting junk wherever it was unsure. Declining to answer is worth exactly what guessing the safe answer is worth, and no more.
> A submission is rejected rather than scored only if it is structurally unusable: a missing id or tones column, duplicate ids, or an id column that shares nothing with the test set.
> Higher is better, in the range 0 to 1. Overall slot accuracy is informative but is not the ranking metric.
> Submission format
> Submit a single UTF-8 CSV file with exactly two columns and a header row:
> Column   Type     Meaning
> ------------------------------------------------------------
> id       string   An id from test.csv
> tones    string   Space separated tone contour per slot, in order
> For each test utterance, emit one contour per tone slot, in order, separated by single spaces. The number of contours must match that row's n_tones. For example, for an utterance with three slots:
> id,tones
> tus_8a076e736bc42cc8,˥˧ ˥˧ ˧˩
> Your file must include the header row and hold one prediction per test id. Rows may appear in any order, since they are joined to the answers on the id column. The provided sample_submission.csv lists every test id with the majority contour repeated to the correct length, so it is a valid submission out of the box and shows the exact format the grader expects. It scores 0.211.
> Write the file as UTF-8. The contour characters are Chao tone letters at U+02E5 through U+02E9 and will be mangled by any other encoding.
> Rules and allowed methods
> These constraints exist so that scores reflect what a model learned to hear, and so that results are reproducible rather than retrieved. They are part of the task definition.
> Contours must be produced by a model that you train and run yourself. Any HuggingFace model or from scratch architecture that fits the compute budget is permitted: wav2vec2 and other self supervised speech encoders, audio spectrogram transformers, convolutional or recurrent networks over spectrogram or log-mel front ends, and encoder decoder architectures over the contour vocabulary. You may extract pitch tracks and other acoustic features, use the toneless transcription as a conditioning input, pretrain on the provided unlabeled clips, augment the audio, address contour imbalance with weighting or resampling, cross validate on the training data, and ensemble your own trained models.
> No TF-IDF or count based statistical models. TF-IDF, including any sklearn TfidfVectorizer or TfidfTransformer or a hand rolled equivalent, along with n-gram frequency models, Markov chains, and similar term frequency or count based schemes, are not permitted as the means of producing the contours. The prediction must come from a learned model that reads the audio, not from character frequency statistics over the transcription.
> No recovering the hidden transcription. The labels derive from a tone marked reading that is never released. You may not reconstruct that reading from any outside source in order to recover the tones, and you may not attempt to match the released audio or ids back to the source corpus they were derived from.
> No external data of any kind. No other speech corpora, no resources for this language or any related language, no lexicons, no comparative wordlists, no phonological databases. The only audio you may train on is the audio in this dataset. Pretrained speech model weights from HuggingFace are permitted and are not considered external data, since they are model parameters rather than a corpus of this language.
> Hosted or closed model APIs are not allowed, because a submission has to be reproducible from your own trained model. Do not call external services, network APIs, or remote models at inference time. No web search or retrieval at inference.
> No hand labelled entries. Predictions must be generated by the model, not produced by listening to the test clips and annotating them yourself.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cross-Column Elution-Order Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7esa8cj1yzj3d644yqq4mswh8a66gm
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mailliwa's score of 0.600!

Full challenge description from page:

> Overview
> In liquid chromatography (LC), a mixture of molecules is pushed through a separation column. Each molecule is retained for a different amount of time (its retention time) and therefore leaves the column in a characteristic elution order. That order is not a fixed property of the molecules: it depends jointly on the molecule's structure and on the chromatographic method — the type of column (its stationary-phase chemistry), the solvent gradient, and the mobile-phase conditions. Two molecules can elute in one order on one method and in the opposite order on another (for example, a water-loving molecule elutes late under one separation mode and early under another).
> You are given a collection of chromatographic methods. Each method reports a set of analytes (molecules) together with the retention time measured for each analyte on that method. Your task is to predict the elution order of analytes for a set of held-out methods — methods run on columns that never appear in the training data. Because the columns are new, you cannot memorise their behaviour; you must learn how molecular structure and method conditions interact to determine retention, and generalise that interaction to unseen columns.
> This is a multimodal problem. Neither modality is sufficient on its own:
> The molecular structure alone fixes only the average tendency of a molecule; it cannot say which direction a specific new column will retain it.
> The method descriptors alone say nothing about any particular molecule.
> You must fuse the two.
> Task
> For every analyte row in test.csv, output a single real-valued retention score. Within each method, analytes are ranked by your score (higher score = predicted to elute later), and that predicted order is compared to the true elution order. Only the relative order within a method is graded — absolute retention values and the overall scale are never scored.
> Files
> You are given five files.
> train.csv
> One row per (analyte, method) measurement in the training methods. Columns:
> id (string) — unique identifier for this analyte-in-method row.
> method_id (string) — identifier of the chromatographic method the measurement was made on. Join to methods.csv and gradients.csv on this key.
> compound_id (string) — identifier of the molecule. The same compound_id may appear in many methods (and in both train and test), letting you learn how one molecule behaves across methods.
> smiles (string) — the molecule's structure as a SMILES string.
> rt (float) — the measured retention time in minutes on this method. This is the training signal.
> test.csv
> One row per (analyte, method) measurement in the held-out methods. Same columns as train.csv except there is no rt column — the retention time is what your model must implicitly rank. Columns: id (string), method_id (string), compound_id (string), smiles (string).
> methods.csv
> One row per method (covering every method_id in both train.csv and test.csv). Columns:
> method_id (string) — method identifier.
> mode (string) — separation mode; one of RP (reversed-phase), HILIC (hydrophilic interaction), or other. This is the coarsest determinant of elution direction.
> usp_code (string) — a standardised stationary-phase class code (e.g. an octadecyl L1 phase, a phenyl phase, etc.). A class descriptor, not a unique column identity.
> col_length_mm (float) — column length in millimetres.
> col_diameter_mm (float) — column internal diameter in millimetres.
> particle_um (float) — packing particle size in micrometres.
> temperature_c (float) — column temperature in degrees Celsius.
> flow_ml_min (float) — mobile-phase flow rate in millilitres per minute.
> ph (float) — mobile-phase pH (may be missing for some methods).
> eluentA_water (float) — percentage of water in eluent A.
> eluentA_meoh (float) — percentage of methanol in eluent A.
> eluentA_acn (float) — percentage of acetonitrile in eluent A.
> eluentB_water (float) — percentage of water in eluent B.
> eluentB_meoh (float) — percentage of methanol in eluent B.
> eluentB_acn (float) — percentage of acetonitrile in eluent B.
> additive_formic (integer 0/1) — whether formic acid is present as a mobile-phase additive.
> additive_acetic (integer 0/1) — whether acetic acid is present.
> additive_nh4ac (integer 0/1) — whether ammonium acetate is present.
> gradients.csv
> The solvent gradient program for every method — a time series describing how the mobile-phase composition changes during the run. Multiple rows per method. Columns:
> method_id (string) — method identifier.
> t_min (float) — time point in minutes since injection.
> pct_b (float) — percentage of eluent B in the mobile phase at that time point.
> Encode this curve however you like (for example, resample it onto a fixed time grid and feed it as a 1-D signal to your model). Eluent A is the weak solvent and eluent B is the strong solvent, so the pct_b-versus-time curve is the shape of the elution program.
> sample_submission.csv
> A valid submission in the exact required format, with a placeholder score for every test id. Columns: id (string), score (float).
> Submission format
> Produce a CSV with exactly two columns, id and score, containing every id in test.csv exactly once and no others. score is your predicted retention scalar (any finite real number; higher = elutes later). Only the ordering induced within each method is used. Missing ids, extra ids, duplicate ids, or non-finite scores cause the submission to be rejected.
> Evaluation metric
> Selectivity-Weighted Within-Method Rank Concordance.
> For each method, we look at every pair of its analytes whose true retention times differ, and check whether your score orders that pair the same way as the true retention times (a concordant pair). Pairs are weighted so that the pairs that matter most are the ones that actually reorder across methods: each analyte carries a precomputed selectivity weight sel in [0, 1] (high for molecules whose elution position is strongly method-dependent, low for molecules whose position is essentially fixed), and a pair (i, j) is weighted w = sqrt(sel_i * sel_j). A model that just sorts by bulk lipophilicity scores near chance on the high-weight pairs.
> For one method:
> concordance(i, j) = 1.0  if your order of (i, j) matches the true order
> 0.5  if you assign the two analytes equal scores
> 0.0  if your order is reversed
> method_score = sum over pairs [ w(i,j) * concordance(i,j) ] / sum over pairs [ w(i,j) ]
> The final score aggregates methods as blend = 0.5 * (mean over methods) + 0.5 * (mean over the worst-quartile methods), then rescales so that chance-level ordering maps to 0 and perfect ordering maps to 1: score = clip((blend - 0.5) / 0.5, 0, 1). Higher is better. The worst-quartile term means the hardest columns (typically the non-reversed-phase and orthogonal ones) strongly influence your score.
> Method rules (required)
> This is a representation-learning / fine-tuning challenge. Your predictive model must learn a representation of molecular structure by fine-tuning a neural network, and fuse it with the method descriptors.
> Allowed:
> Fine-tuning a pretrained neural molecular encoder — for example a pretrained transformer / language model over SMILES, or a graph neural network over the molecular graph — and training a neural fusion head that conditions the molecular representation on the method descriptors and gradient curve (for example via concatenation, FiLM, or cross-attention).
> Any neural architecture, loss (pointwise, pairwise, or listwise ranking), and training schedule, as long as the molecular representation is learned by the network.
> Not allowed:
> Gradient-boosted decision trees or random forests or any tree ensemble (including XGBoost, LightGBM, CatBoost, and scikit-learn's tree/forest/boosting models) as the predictive model.
> Linear/logistic regression, SVM, k-NN, or similar classical models trained on hand-crafted molecular descriptors or fixed fingerprints (for example RDKit/Mordred descriptor tables, ECFP or MACCS fingerprints) as the predictive model. The molecular representation must be learned by the network, not hand-engineered and handed to a classical estimator.
> Using external retention-time data, or looking up the retention behaviour of these molecules or methods from any outside source. Every prediction must come from your model trained on the provided training data.
> You may use pretrained neural weights (downloading pretrained molecular encoders is expected and allowed). Your full solution — training and inference over the whole test set — must complete within the provided compute and time budget, so prefer efficient fine-tuning.
> Notes
> The train/test split holds out entire columns: no column in the test methods appears in the training methods. Build your validation split the same way (hold out whole columns/methods, not random rows) or you will badly overestimate your score.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Laryngeal Lesion Histotype Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cpwqzz778br99nqpg8gekt58bm15m
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 0.131!

Full challenge description from page:

> Overview: This challenge asks you to build a medical image retrieval system that finds visually similar laryngeal endoscopy images. The images were captured using Contact Endoscopy with Narrow-Band Imaging (CE-NBI), a technique that enhances the visualization of subepithelial blood vessel morphology in the vocal fold. Six histopathology categories are present: Reinke's edema, papillomatosis, polyp, squamous cell carcinoma (SCC), high-grade dysplasia, and carcinoma in situ.
> For each test image, submit the 10 test images (excluding the query itself) that are most visually similar to it, ranked from most to least similar. Similarity is evaluated by whether retrieved images share the same histopathology category as the query. The training set provides labeled examples of each category across many patients. The test set contains images from different patients than the training set.
> Real-world context: CE-NBI is used in clinical practice to characterize suspicious laryngeal lesions before biopsy. A retrieval system that surfaces visually similar historical cases allows endoscopists to ground their assessment in prior confirmed diagnoses, supporting case-based reasoning in resource-limited settings where experienced laryngologists may not be immediately available.
> Evaluation: Mean Average Precision at 10 (MAP@10).
> For each test image (query), you submit a ranked list of 10 retrieved images from the test set. Retrieved images that share the histopathology category with the query are relevant. AP@10 for one query is the average precision at each rank position where a relevant image appears, divided by min(10, total relevant images in the test set for that category). MAP@10 is the mean AP@10 across all query images.
> A retrieval system that consistently returns same-category images in the top 10 scores MAP@10 = 1.0. A system returning random images scores approximately 0.17 due to 6 balanced categories.
> Dataset: All images are 128x128 pixels, single-channel grayscale, JPEG format. Gaussian noise was applied during preparation; test images have a higher noise level than training images, creating a controlled distribution shift that challenges generalization. CE-NBI images show blood vessel patterns on the vocal fold surface; the six categories differ in vessel architecture, density, and arrangement at the lesion surface.
> The following files are provided in the public directory:
> train/ Directory of training images (JPEG files). Each file is a 128x128 grayscale image.
> train.csv filename - string - JPEG filename (e.g. img_00001.jpg), matches a file in train/ group - string - histopathology category: one of reinkesedema, papillomatosis, polyp, scc, highgradedysplasia, carcinomainsitu
> test/ Directory of test images (JPEG files). Same format as train images.
> test.csv filename - string - JPEG filename, matches a file in test/
> sample_submission.csv filename - string - test image filename (the query) retrieved_images - string - 10 test image filenames separated by spaces (placeholder: first 10 sorted test filenames excluding self)
> The six histopathology categories differ in how the underlying tissue pathology manifests in blood vessel morphology under NBI: benign lesions such as Reinke's edema show dilated, regularly-arranged vessels; papillomatosis shows irregular papillary loops; polyps show scattered punctate or loop-type vessels; malignant and premalignant lesions (SCC, high-grade dysplasia, carcinoma in situ) show irregular, tortuous, and densely-packed vessels associated with angiogenesis. These differences in vascular pattern are the intended retrieval signal.
> Submission: Your submission must be a CSV with exactly two columns: filename and retrieved_images.
> filename - string - must exactly match filenames in test.csv (each appears exactly once) retrieved_images - string - exactly 10 test image filenames separated by single spaces, ranked most to least similar
> Example submission: filename,retrieved_images img_00410.jpg,img_00411.jpg img_00412.jpg img_00413.jpg img_00414.jpg img_00415.jpg img_00416.jpg img_00417.jpg img_00418.jpg img_00419.jpg img_00420.jpg img_00411.jpg,img_00410.jpg img_00412.jpg img_00413.jpg img_00414.jpg img_00415.jpg img_00416.jpg img_00417.jpg img_00418.jpg img_00419.jpg img_00421.jpg
> Requirements: The submission must have exactly as many rows as test.csv. The filename column must contain each test image filename exactly once with no duplicates. Each retrieved_images value must contain exactly 10 test image filenames separated by single spaces. All retrieved image filenames must be valid test set filenames from test.csv.
> Rules: The only valid input signal is the pixel content of the JPEG images in train/ and test/. The following approaches are not allowed:
> Hardcoding retrieved lists for specific test image filenames.
> Using the filename or its numeric index to infer histopathology category or retrieval order.
> Using any external database of laryngeal pathology images, clinical reports, or CE-NBI image repositories not provided in train/.
> Reverse image searching or querying any external API to identify the source or category of test images.
> Using private, role-gated, or API-key-based models, or calling any external inference API at retrieval time.
> The intended approach is to learn a visual embedding space where images with the same histopathology category are closer together than images with different categories. The evaluation tests whether learned similarity reflects the fine-grained vessel morphology differences between the six laryngeal lesion types: benign reactive lesions (Reinke's edema, polyp), benign neoplasms (papillomatosis), and malignant or premalignant lesions (SCC, high-grade dysplasia, carcinoma in situ). Clustering approaches that treat the six categories as unknown groups from unlabeled train/ images are not prohibited, but supervised metric learning using the provided group labels in train.csv is expected to outperform them.
> Pretrained model policy: General-purpose image backbone models are allowed as feature extractors or for fine-tuning, provided they were not pretrained specifically on laryngeal endoscopy or CE-NBI data. Acceptable backbones include models trained on ImageNet (ResNet, EfficientNet, ViT, ConvNeXt), natural image self-supervised models (DINO, MoCo, SimCLR), or general medical imaging encoders trained on broad multi-organ data. Not allowed: models pretrained on laryngeal pathology datasets, vocal fold endoscopy benchmarks, or any encoder whose pretraining corpus includes labeled CE-NBI images. Because all images are grayscale, pretrained RGB weights must be adapted (e.g., averaging the three input channels). The intended learning task is to derive vessel-morphology similarity from the provided training images. If a pretrained model achieves MAP@10 above 0.85 without any fine-tuning or metric learning, train a retrieval head from scratch on the training set instead.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cross-Source Pollen Grain Taxonomic Relatedness

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx734c72fwvnyz6m14d44b2xn98bmc5j
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Cross-Source Pollen Grain Taxonomic Relatedness
> Overview
> Automated pollen monitoring photographs individual pollen grains under a microscope and must judge how
> alike two grains are. The hard part in practice is transfer across imaging sources: grains
> photographed at different laboratories differ in microscope, mounting, and staining — the same
> taxon can look completely different (colour, contrast, background) from one source to another, and
> naive systems that key on stain colour fail to compare them.
> This challenge is that problem in a controlled, graded form. You are given labelled training
> grains from three imaging sources and a set of test pairs of grains. For each pair you output
> a similarity score, and the score is judged by how well it ranks the pair's taxonomic
> relatedness:
> same genus — most related,
> same family, different genus — moderately related (e.g. two Betulaceae genera),
> different family — unrelated.
> In every test pair the two grains come from different imaging sources, one of which is a source
> that never appears in training (an unseen domain). Because the relatedness levels have identical
> source composition, colour tells you nothing about the answer — only morphology (shape, apertures,
> surface sculpture, wall structure) does, recognised across the change of imaging domain, including the
> hard distinction between the same genus and merely the same family within look-alike families.
> This is a metric-learning task, not classification: there is no fixed class list. You learn a
> stain-invariant notion of similarity from the training grains and apply it to pairs, including genera
> you may not have seen at training time.
> Task
> For each test pair of grain crops, output a score — higher when the two grains are more
> taxonomically related (same genus > same family > different family). Scores are used only by their
> ranking (see Evaluation), so they need not be calibrated; any real number is fine.
> Training grains carry a genus label (and a source label) so you can learn an embedding or
> similarity. The relatedness level of each test pair is hidden.
> Required level of training. Your solution must be trained on the provided training grains. A
> pretrained image backbone is encouraged, but it must be fine-tuned on this training data
> (end-to-end) — using a pretrained model as a frozen feature extractor, without training it on
> these grains, does not satisfy the task. Learning the similarity, including the embedding and any
> metric head, is the core of the problem.
> Evaluation
> Submissions are scored with TaxonConcordance ∈ [0, 1], higher is better: a graded, rank-based
> generalization of AUC. It is the probability that, taking two pairs at different relatedness
> levels, the more-related pair receives the higher score. Equivalently it is the number-of-comparable-
> pairs-weighted mean of the three between-level ROC-AUCs (same-family vs different-family, same-genus
> vs different-family, same-genus vs same-family).
> Ranking only. It depends solely on the ordering of your scores, so no threshold is tuned and
> scores need not be calibrated.
> Chance is 0.5. A constant or random score gets ≈ 0.5; a perfect ordering (same genus above same
> family above different family) gets 1.00; the reverse ordering gets 0.0. Because every pair
> mixes two imaging sources with identical composition across levels, a model that keys on staining or
> colour scores ≈ 0.5 — ordering relatedness requires stain-invariant morphology.
> Higher is better. See grade.py.
> Dataset
> The prepared public dataset (GPU / A10G runtime, ~1 hour) is laid out under public/:
> train.csv — labelled training grains (learn an embedding / similarity from these).
> pairs.csv — the test pairs to score.
> sample_submission.csv — a valid submission in the required format.
> train/images/ — the training grain images.
> test/images/ — the grain images referenced by the pairs.
> There are 7,598 training grains (from three imaging sources) and 8,001 test pairs. Each image
> is a single pollen grain, RGB, of variable size (roughly tens to a few hundred pixels on a side).
> Columns of train.csv:
> id (integer) — training grain identifier.
> image (string) — relative path to the crop, for example train/images/000123.png.
> source (string) — imaging source of this grain, one of source_1, source_2, source_3.
> genus (string) — ground-truth genus of the grain.
> Columns of pairs.csv:
> pair_id (integer) — pair identifier (used in your submission).
> image_a (string) — relative path to the first grain, for example test/images/104505.png.
> image_b (string) — relative path to the second grain, for example test/images/101776.png.
> The source labels let you treat training as multi-source (domain-balanced sampling, domain-invariant
> or style-augmented training). In every test pair the two grains are from two different sources, one of
> which is an imaging source held out of training entirely.
> Submission
> Submit a CSV with exactly these two columns:
> pair_id (integer) — a pair id from pairs.csv.
> score (number) — your similarity score for that pair; higher = more taxonomically related.
> Example:
> pair_id,score
> 500000,0.12
> 500001,0.87
> 500002,0.55
> Requirements
> Exactly 8,001 rows — one per pair_id in pairs.csv — plus a header row.
> Columns must be exactly pair_id,score; pair_ids unique and matching pairs.csv exactly.
> (The grader rejects submissions with wrong columns, duplicate pair_ids, or missing/extra rows.)
> Every score must be a finite number (no NaN/inf/blank).
> Write the final submission to ./working/submission.csv. UTF-8.
> Baselines
> sample_submission.csv gives every pair the same score and scores ≈ 0.50.
> A random score scores ≈ 0.50; a strong stain-invariant model scores well above it.
> A perfect ordering of relatedness scores 1.00, so there is large headroom. When the challenge is
> created, an AI agent attempts it to set the baseline that solvers must beat.
> Allowed And Prohibited
> Allowed:
> Train / fine-tune models on the training grains and their genus (and source) labels — metric
> learning, contrastive / triplet / ArcFace objectives, or a classifier whose features you compare.
> Use publicly available pretrained image backbones and standard augmentation, including colour /
> stain augmentation and normalization.
> Domain-generalization techniques that use only the training grains (domain-invariant learning,
> domain-balanced sampling, style augmentation, ensembling).
> Self-supervised pretraining on the provided training grains.
> Prohibited:
> Do not use external datasets or external pollen images / reference libraries of any kind.
> Do not train on, adapt to, or otherwise fit the test grains or pairs — no transductive learning,
> no test-time adaptation, no clustering of the test grains, no using test-set statistics. Treat the
> pair images as available for scoring only.
> Do not hardcode outputs or use per-pair_id answer tables.
> Do not use external LLM APIs or any LLM-generated labels in your submission.
> A genuinely trained model is expected — not a frozen off-the-shelf feature extractor applied
> unchanged.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Predicting Contested Comment Moderation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7btry1r04tmnwz6vechz0t918bmwar
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top Score | — | Created | Aug 1, 2026 | Start New Solution

Full challenge description from page:

> Predicting Contested Comment Moderation
> Overview
> When people are asked to judge whether a comment is toxic, they do not always agree. A slur is called toxic by everyone; a blunt criticism, a sarcastic aside, an in-group joke, splits the room. That split is where automated moderation is least reliable and a human reviewer is most needed. This challenge asks you to see it coming: from the comment text alone, predict how contested the comment was among the people who judged it.
> Each comment here was judged for toxicity by about ten annotators, and the target is the contestedness of that judgement, in three grades: consensus (the annotators nearly agreed), mixed (a moderate split), or contested (they were close to evenly divided). Only comments that at least one annotator flagged as toxic are included, so this is the borderline population where disagreement is real.
> The target is not the toxicity label. A very toxic comment and a very innocuous one are both consensus, because in both the annotators agreed; a very toxic comment is not automatically contested. What you are predicting is not whether the comment is toxic but whether people would disagree about it, which the words signal only indirectly, through sarcasm, ambiguity, context and tone rather than through obviously abusive or obviously clean language.
> Task
> For every comment in test.csv, output its contestedness label: consensus, mixed, or contested.
> Data
> All inputs are under dataset/public/.
> train.csv: columns comment_id, text, contestedness. The training comments with their grade.
> test.csv: columns comment_id, text. The comments to grade.
> sample_submission.csv: a correctly formatted submission for every test comment, scoring at chance.
> Comments are independent, so the split is a plain per-comment split; the test comments are not in training.
> Evaluation
> The score is the macro-averaged F1 over the three grades, the mean of the per-grade F1:
> per grade:  F1 = 2*TP / (2*TP + FP + FN)
> score = mean of the per-grade F1                 (higher is better, range 0 to 1)
> Macro-averaging weights every grade equally, so the middle and the contested grades count as much as the common consensus one. Measured on this exact split:
> the supplied random placeholder scores about 0.32 (chance for three classes).
> a word n-gram TF-IDF logistic-regression classifier, the reference here, scores about 0.44, picking up only the lexically obvious contestedness and missing the rest.
> grading every comment correctly scores 1.00.
> The reference shows how far surface words alone get you. The distance above it is contestedness that lives in tone and context, not in the presence of an abusive word.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> comment_id,label
> c_1a2b3c4d5e6f,consensus
> c_2b3c4d5e6f7a,contested
> ...
> One row per comment_id in test.csv, and no others. A submission that omits a comment, repeats one, or names an unknown one is rejected.
> label must be one of consensus, mixed, contested.
> Start from sample_submission.csv to get the id set, and write with index=False.
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> One A10G GPU (24 GB), plus 10 CPU cores and 62 GB of memory, and a hard limit of 1.5 hours for the whole run. The comments are short and there are tens of thousands of them, so fine-tuning a text model over them fits comfortably in that budget; the reference itself finishes in a couple of minutes.
> A pretrained model is allowed. You may download a general-purpose pretrained encoder or language model from a model hub and fine-tune it on the training comments. What you may not use is a model or lexicon already built to predict this contestedness target on this corpus.
> No package installs (no pip or conda install). Use the preinstalled libraries (numpy, scipy, pandas, scikit-learn, pytorch, transformers, and so on).
> What Not To Use
> Do not try to retrieve the source annotations for these comments from any public archive to recover the vote split. The comment identifiers were removed for this reason; decide from the text.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning approach is expected. The signal is in the tone and framing of the comment, the cues that make a judgement of it divisive rather than clear-cut, and it has to be read from the text of comments you have not seen. A model that learns what makes a comment contested, rather than what makes it toxic, is the line of attack.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## EchoTherm: Dual-Sensor Contact-Thermal Replay From Sound, Force, and Motion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7drmbgykg284z6hfsckcyc3h8aymxd
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Top Score | — | Created | Jul 21, 2026 | Start New Solution

Full challenge description from page:

> Overview
> EchoTherm: Dual-Sensor Contact-Thermal Replay From Sound, Force, and Motion
> Plain language objective: fine-tune a local model for dual-sensor contact-thermal replay. For each real household-object contact episode, use the initial thermal state plus early force, contact-sound, and distributed vibration/motion evidence to reconstruct how two thermal sensors change over the next eleven checkpoints.
> Each public row represents one synchronized grasp/contact episode. You receive a compact row-local observation of:
> two initial thermal sensor values;
> a 20-bin early force profile;
> a 20-bin contact-audio response profile plus a coarsened log-energy value; and
> a 20-bin distributed vibration/motion profile plus a coarsened log-energy value.
> For every test row, predict two future thermal-delta trajectories: one for the active heated thermal sensor and one for the passive thermal sensor. Each trajectory has exactly eleven values in degrees Celsius relative to that sensor's supplied initial value.
> This is a cross-modal physical-response reconstruction task. It is not activity classification, object classification, material recognition, participant identification, source-row matching, or ordinary one-number regression. The scored object is the future thermal replay itself: two ordered response curves that must be plausible for the same contact event.
> The closest public analogues estimate temperature or force from vibroacoustic or tactile signals, often as a scalar or domain-specific property. EchoTherm instead withholds the future thermal history after the initial instant and scores paired active/passive contact-sensor curves under held-out device and ambient-temperature robustness axes. A solution must model the contact response, not recover a source row or infer a semantic object/material label.
> Only GPU-tier solutions are allowed. Submissions must be reproducible within the selected platform GPU runtime budget. Fine-tune the best local open-source model for this dual-sensor contact-thermal replay task: map early force, contact-audio, vibration/motion, and initial thermal readings to both future thermal curves. The intended solution fine-tunes only on the released public files, not by looking up the upstream source archive or shortcutting through IDs, row order, filenames, private preparation artifacts, or source metadata.
> What Not To Use / What Not To Do, violation may cause rejection regardless of score:
> Do not download, index, fingerprint, or search the upstream source archive to recover hidden test rows or future thermal values.
> Do not use public IDs, signal_row, row order, file sizes, file modification times, array byte patterns, hidden split details, or any platform artifact as an answer channel.
> Do not inspect private answers, grader internals, prepare-script outputs outside public/, or filesystem side channels.
> Do not reduce the task to object/material/activity classification, device identification, duration lookup, or a single scalar prediction.
> Do not submit a model that ignores the supplied force, contact-audio, vibration, and initial-thermal evidence.
> Do not use hosted APIs, remote inference services, closed-source teacher APIs, runtime-downloaded model weights, challenge-specific pretrained checkpoints, or external labels. Public, general-purpose open-source model weights may be used only for local fine-tuning on the released public training data.
> Do not exploit malformed JSON, duplicate IDs, extra columns, non-finite values, overlong cells, impossible ranges, or other grader attacks.
> Enforcement on invalid approaches: solutions may be reviewed for actual use of the public sensor evidence, source-lookup code, remote calls, hidden-answer access, metadata-only behavior, and rule-only shortcuts. The goal is to reward learned contact-thermal reconstruction from real synchronized signals, not lookup tables or format exploits.
> Task
> For each test row, read the CSV row and the matching rows in test_signals/*.npy. Submit:
> active_thermal_delta_json: eleven active-sensor temperature deltas.
> passive_thermal_delta_json: eleven passive-sensor temperature deltas.
> The two lists use the same checkpoint convention. List position k corresponds to source sample index 100 + 20*k, for k = 0..10. Increasing list position means later physical time. Values are measured in degrees Celsius relative to that same sensor's public initial temperature.
> The active and passive sensors are independent measured channels. A strong submission should predict both, and the two trajectories should be physically compatible with the same contact episode.
> Intended Approach
> A practical fine-tuning solution starts from a compact local open-source temporal model, adapts it on the public training rows, and predicts the two thermal trajectories jointly. The force, contact-audio, and vibration/motion profiles are short aligned contact-prefix inputs conditioned on the two initial thermal values; the model predicts two eleven-step thermal-delta trajectories. Suitable local GPU-tier approaches include fine-tuning temporal convolutional encoders, GRU/LSTM encoders, small Transformer or state-space temporal models, neural basis-curve regressors, and hybrid feature-to-trajectory predictors with separate active/passive heads. Engineered summaries such as temporal differences, slopes, low-frequency DCT or FFT features, peak and area statistics, cross-profile interactions, and initial-temperature conditioning can be useful auxiliary inputs, but the final answer should remain two ordered trajectories rather than a class, object ID, or scalar.
> Good validation should be train-only and should test robustness across device-like and ambient-temperature regimes, because the private score includes worst-group terms. Calibration should come from public training folds. Open-source local libraries such as NumPy, SciPy, pandas, PyTorch, JAX, TensorFlow, and GPU-capable gradient-boosting packages are appropriate when run locally on the selected platform tier. Internet-dependent inference, hidden source metadata, and test-row lookup are not allowed.
> Evaluation
> Each submitted trajectory is parsed as a JSON list of exactly eleven finite numbers. Active-sensor values must be in [-80, 30]. Passive-sensor values must be in [-20, 40].
> For each checkpoint:
> active_value_score  = max(0, 1 - abs(pred - truth) / 6)
> passive_value_score = max(0, 1 - abs(pred - truth) / 2)
> For each row, scores are averaged over the eleven checkpoints, then the active and passive heads receive equal weight:
> row_score = 0.5 * mean(active_value_score)
> + 0.5 * mean(passive_value_score)
> The final score blends mean row quality with private physical robustness axes:
> Final = 0.80 * mean(row_score)
> + 0.10 * worst held-out device group
> + 0.10 * worst initial-ambient band
> The private group labels are used only by the grader. They are not random buckets and are not public columns. Higher is better. The theoretical minimum is 0.0, the theoretical maximum is 1.0, and a perfect valid submission scores exactly 1.0.
> The grader requires exactly the submission columns in the listed order, one row per test ID, unique IDs, and the exact test ID set. Wrong columns or column order, duplicate IDs, missing IDs, extra IDs, blank IDs, or an ID-set mismatch make the entire submission invalid. Row-local malformed JSON, non-finite values, wrong list length, nested JSON, oversized cells, or out-of-range values make the affected row/head score zero without crashing the grader; the other valid head remains scoreable.
> Dataset
> The prepared data is under public/. The split contains 1,159 training rows and 1,089 test rows. Each CSV row has a signal_row index that points to the same row in every array under that split's signal directory. The id.npy value at that row is the same opaque ID as the CSV row.
> File overview:
> Item	Description
> train.csv	Inputs plus labels
> test.csv	Test inputs only
> train_signals/	Train input arrays
> test_signals/	Test input arrays
> sample_submission.csv	Weak valid template
> signal_schema.json	Array/checkpoint schema
> train.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> signal_row	int	Signal array row
> active_thermal_delta_json	JSON string	Train active label
> passive_thermal_delta_json	JSON string	Train passive label
> test.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> signal_row	int	Signal array row
> Signal arrays in each split:
> Array	Shape	Type	Description
> id.npy	(n,)	bytes	Opaque row IDs
> initial_thermal_c.npy	(n, 2)	float32	Initial C values
> force_profile.npy	(n, 20)	float32	Early force panel
> contact_audio_profile.npy	(n, 20)	float32	Sound response panel
> contact_audio_log_energy.npy	(n,)	float32	Sound log energy
> vibration_profile.npy	(n, 20)	float32	Vibration panel
> vibration_log_energy.npy	(n,)	float32	Vibration log energy
> initial_thermal_c.npy column order is active sensor first, passive sensor second. All .npy files are ordinary NumPy arrays readable with numpy.load(path, allow_pickle=False). The public panels preserve local event order but are transformed compact summaries rather than raw upstream waveforms or raw device traces.
> Submission
> Submit a CSV with exactly these three columns in exactly this order:
> Column	Type	Constraint
> id	string	Same IDs as test
> active_thermal_delta_json	JSON string	11 values in range
> passive_thermal_delta_json	JSON string	11 values in range
> active_thermal_delta_json must be a JSON list of exactly eleven finite numbers, each in [-80, 30]. passive_thermal_delta_json must be a JSON list of exactly eleven finite numbers, each in [-20, 40]. Both lists are in degrees Celsius relative to the corresponding supplied initial temperature.
> Example submission rows:
> id,active_thermal_delta_json,passive_thermal_delta_json
> 0031d9ba38e1dc2b118f4019,"[0,0,0,0,0,0,0,0,0,0,0]","[0,0,0,0,0,0,0,0,0,0,0]"
> 01500203ddb05c00d7f41e55,"[-4.2,-5.1,-5.7,-6.0,-6.3,-6.5,-6.7,-6.8,-6.9,-7.0,-7.1]","[0.4,0.4,0.3,0.3,0.2,0.2,0.2,0.1,0.1,0.1,0.0]"
> Requirements are strict: start from sample_submission.csv or write the same header yourself, preserve exactly one row per test id, keep the columns in the table order, and do not add extra columns. Duplicate IDs, missing IDs, extra IDs, reordered columns, blank IDs, or an ID-set mismatch make the whole submission invalid. Malformed row-local trajectory cells score zero for the affected row/head.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## EEG-Guided Spontaneous Attention Path Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76wf7tkhrgzw4zb6da6zcxr98az9ft
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Top Score | — | Created

Full challenge description from page:

> Neuro-steered hearing aids should follow a listener when attention moves between competing speakers instead of requiring a manual control. In this challenge, each example is a complete 60-second listening episode with continuous EEG and two synchronized competing Mandarin speech streams. Reconstruct the listener's behaviorally reported attention path over the whole episode: which candidate stream is attended at each fixed time step, where directional switches occur, and where the available report does not support a precise state.
> Overview
> Objective: for each 60-second episode, predict the listener's attention state at every 0.5-second step and the corresponding confidence-weighted directional switches.
> Each EEG episode is a 3840 x 62 float16 array: 60 seconds at 64 Hz, with time on the first axis and order-preserved EEG channels on the second. The matching stereo 16 kHz WAV lasts 60 seconds. Audio channel 0 is candidate stream_A; audio channel 1 is candidate stream_B. Candidate order is source-neutral and balanced. The audio candidates are inputs for neural tracking; the output does not copy either waveform.
> This is a full-episode temporal reconstruction task, not an independent-window classifier. For every test episode, submit all three synchronized objects:
> A 120-step state path on a 0.5-second grid using stream_A, stream_B, or uncertain.
> A contiguous segment representation of exactly the same state path, with calibrated confidence per segment.
> An ordered sequence of directional switch intervals with previous, next, and confidence.
> The uncertain state is not a creator-invented soft label. It is used before the first behaviorally reported attention state and in grid cells containing a clustered response-defined boundary. Button times are behavioral reports and motor events, not exact cognitive onset times. Direction-changing reports less than 0.5 seconds apart are clustered into one bounded event; repeated same-state presses do not create switches.
> Training, validation, and hidden test use disjoint listener groups and disjoint speech families. A model therefore has to generalize to both unseen listeners and unseen speech content. Public identifiers are opaque, row order is randomized, fixed-size payloads remove size cues, and original participant, trial, block, event-code, timestamp, and source filename fields are absent.
> Prior spontaneous-attention benchmarks primarily score left/right decisions in fixed windows or switch detection near isolated events. This challenge instead scores a complete continuous path, directional event chronology, boundary intervals, uncertainty calibration, and agreement between the path and its event list on held-out listeners and held-out speech. A no-switch classifier, a timing template, or a button-transient detector leaves most of the scored object unresolved.
> Task Specification
> states_json must decode to a JSON list of exactly 120 strings. Index k represents [0.5k, 0.5(k+1)) seconds. Allowed values are stream_A, stream_B, and uncertain.
> segments_json must decode to a non-empty JSON list of objects with exactly start_step, end_step, state, and confidence. Each segment covers the half-open step range [start_step, end_step), so end_step is exclusive. Segments must be ordered, contiguous, non-overlapping, cover exactly step indices 0 through 119 inclusive, finish with end_step = 120, and reconstruct states_json. Step bounds are integers; confidence is finite and in [0, 1].
> switches_json must decode to an ordered JSON list of objects with exactly onset_start_s, onset_end_s, previous, next, and confidence. Times are finite seconds in [0, 60]; each interval is at most 3 seconds; intervals may not overlap. previous and next must be different decisive states, and each direction must agree with the nearest available decisive states in states_json. At most 40 switches are accepted per episode.
> Intended Approach
> Strong solutions should fine-tune an open-source model or build and train an architecture from scratch. These are the two intended model-learning routes for this challenge.
> For the fine-tuning route, adapt an open-source speech or multimodal encoder to the two candidate Mandarin streams, combine it with a learned EEG encoder and cross-modal fusion, and fine-tune the network on the provided training episodes. Learned output heads should produce the attention states, switch intervals, and calibrated confidence. The open-source weights should be updated locally; frozen hosted inference alone is not the intended solution.
> For the from-scratch route, initialize and train the EEG encoder, dual audio encoders, cross-modal attention or correlation blocks, and learned prediction heads entirely from the provided data. Convolutional encoders and trainable attention blocks are appropriate building components. In either route, predictions must come from trained EEG-audio representations rather than rule-only timing templates, independent-window heuristics, or metadata shortcuts.
> What Not To Use
> Do not use source-corpus lookup, media fingerprint matching, recovered source filenames or event arrays, participant identification, trial/order/timestamp reconstruction, row-size or hash tricks, manual test labeling, hardcoded id maps, hosted commercial EEG/speech APIs, private files, or grader exploitation. Do not reduce the task to tabular binary classification, independent windows, saved spectrogram images, computer vision, object detection, or waveform copying. Do not use response/motor artifacts as a substitute for cross-modal attention decoding.
> Enforcement On Invalid Approaches
> Solutions that obtain labels through public-source matching, hidden metadata reconstruction, private-file access, hardcoded answers, hosted inference, or rule-only shortcuts may be rejected even when their CSV is structurally valid. The intended evidence is learned EEG and speech temporal modeling from the public challenge data.
> Dataset
> The public dataset contains prepared train, validation, and test directories plus a metadata file and a sample submission. Train and validation include labels. Test contains only inputs. Paths inside each manifest are relative to the public root.
> Public Files
> | Item | Description |
> |---|---|
> | `metadata.json` | Signal and label contract |
> | `train/manifest.csv` | Train input index |
> | `train/labels.csv` | Train sequence labels |
> | `train/eeg/*.npy` | Train EEG episodes |
> | `train/audio/*.wav` | Train speech candidates |
> | `val/manifest.csv` | Validation input index |
> | `val/labels.csv` | Validation labels |
> | `val/eeg/*.npy` | Validation EEG episodes |
> | `val/audio/*.wav` | Validation speech candidates |
> | `test/manifest.csv` | Test input index |
> | `test/eeg/*.npy` | Hidden-test EEG episodes |
> | `test/audio/*.wav` | Hidden-test speech candidates |
> | `sample_submission.csv` | Valid weak template |
> manifest.csv Columns
> | Column | Type | Description |
> |---|---|---|
> | `episode_id` | string | Opaque episode token |
> | `eeg_file` | string | Relative NPY path |
> | `audio_id` | string | Opaque audio token |
> | `audio_file` | string | Relative WAV path |
> | `duration_s` | float | Always 60 seconds |
> | `eeg_sampling_rate_hz` | int | Always 64 |
> | `eeg_samples` | int | Always 3840 |
> | `eeg_channels` | int | Always 62 |
> | `audio_sampling_rate_hz` | int | Always 16000 |
> | `audio_channels` | int | Always 2 |
> labels.csv Columns
> | Column | Type | Description |
> |---|---|---|
> | `episode_id` | string | Opaque episode token |
> | `states_json` | JSON string | 120 state values |
> | `segments_json` | JSON string | Contiguous segments |
> | `switches_json` | JSON string | Directional events |
> Test Input Columns
> test/manifest.csv has the same ten input columns as the train and validation manifests. It has no attention state, segment, switch, confidence, participant, trial, event, or source-identity field.
> Submission Format
> Submit one CSV row for every test episode_id, using these columns in this exact order.
> | Column | Type | Constraint |
> |---|---|---|
> | `episode_id` | string | Exact hidden-test ID |
> | `states_json` | JSON string | Exactly 120 states |
> | `segments_json` | JSON string | Half-open full cover of indices 0-119 |
> | `switches_json` | JSON string | Ordered event list |
> episode_id,states_json,segments_json,switches_json
> ep_ae424016ec115e4b7791,"[""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A"",""stream_A""]","[{""start_step"":0,""end_step"":120,""state"":""stream_A"",""confidence"":0.5}]","[]"
> This is the first machine-valid row of the generated sample file; it contains all 120 state values.
> Evaluation
> The official metric is AttentionPathScore, a transparent 0-to-1 joint sequence score. Higher is better. A perfect valid prediction scores exactly 1.0; a fully malformed row scores 0.0 for that row.
> All formulas below are applied separately to each episode.
> StateScore
> For each decisive state s in {stream_A, stream_B} that occurs in the reference path, define Recall_s as the number of correctly predicted reference steps of state s divided by the number of reference steps of state s. A decisive state absent from the reference is omitted from the mean. For the uncertain state, let TP_u, FP_u, and FN_u be the usual step-level binary counts.
> BalancedRecall = mean(Recall_s for decisive states s present in the reference),
> or 0 if neither decisive state is present
> UncertainF1 = 1                                      if 2*TP_u + FP_u + FN_u = 0
> 2*TP_u / (2*TP_u + FP_u + FN_u)      otherwise
> StateScore = 0.80*BalancedRecall + 0.20*UncertainF1
> Switch matching, EventScore, and BoundaryScore
> For a submitted switch p and reference switch r, define the endpoint gap in seconds as:
> gap(p,r) = 0.5 * (abs(p.onset_start_s - r.onset_start_s)
> + abs(p.onset_end_s - r.onset_end_s))
> A pair is eligible only when previous and next agree exactly and gap(p,r) <= 1.5. Eligible pairs are sorted by (gap, submitted_index, reference_index) and accepted greedily while both events remain unmatched. This produces a deterministic one-to-one matching. Let P be the submitted event count, R the reference event count, M the matched-pair count, and gap_j the gap of matched pair j.
> EventScore = 1                         if P + R = 0
> 2*M / (P + R)             otherwise
> BoundaryScore = 1                                           if max(P,R) = 0
> sum_j max(0, 1 - gap_j/1.5) / max(P,R)      otherwise
> CalibrationScore
> At state step k, let c_k be the segment confidence and let y_k = 1 when the submitted state equals the reference state, otherwise y_k = 0. For submitted event i, let q_i be its confidence and let z_i = 1 when that event is in the one-to-one reference matching, otherwise z_i = 0.
> StateBrier = (1/120) * sum_k (c_k - y_k)^2
> EventBrier = (1/P) * sum_i (q_i - z_i)^2                 when P > 0
> CombinedBrier = StateBrier                               when P = 0
> 0.75*StateBrier + 0.25*EventBrier        when P > 0
> CalibrationScore = max(0, 1 - 2*CombinedBrier)
> ConsistencyScore
> Derive a transition list from the submitted state path as follows. A direct change between decisive states at grid index k creates a point transition at 0.5*k seconds. A contiguous uncertain run covering half-open indices [a,b) and bracketed by different decisive states creates one point transition at 0.25*(a+b) seconds. Match submitted switches to these derived transitions with the same direction, 1.5-second endpoint-gap rule, and greedy procedure above. Let T be the number of derived transitions, C the number of matches, and E the number of unmatched submitted switches satisfying onset_start_s <= 1e-9 or onset_end_s >= 60 - 1e-9; these edge events have only one observable state side.
> E is a subset of P: every accepted edge switch is already counted once among the submitted switches in P. Because the state outside the 60-second episode is unobservable, each such edge switch is treated as matching one virtual boundary reference transition. Therefore the extra + E in the denominator counts those virtual reference transitions, while C + E counts ordinary matches plus virtual-boundary matches. The submitted edge switch itself is not counted twice.
> ConsistencyScore = 1                          if P + T + E = 0
> 2*(C + E) / (P + T + E)    otherwise
> Episode and final scores
> The per-episode score is:
> EpisodeScore = clip(0.35*StateScore
> + 0.30*EventScore
> + 0.15*BoundaryScore
> + 0.10*CalibrationScore
> + 0.10*ConsistencyScore, 0, 1)
> The final score is the macro mean of episode scores within each hidden listener, followed by the mean across hidden listeners. Long steady segments therefore cannot dominate simply by contributing more rows.
> Wrong columns or column order, duplicate IDs, a missing/extra/foreign ID, or an invalid ID encoding raises InvalidSubmissionError and the submission is not scored. A row-local malformed JSON value, illegal enum, non-finite value, invalid range, inconsistent segment cover, impossible switch direction, excessive size/depth/count, or overlapping event makes only that row score 0.0. Error messages do not reveal labels, listener groups, event details, or split logic.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Genetic Epistasis Prediction from Gene Function Text

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75jc8etvfkavastazjg2tzmh88kkbw
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, generative, Dataset source is visible after the challenge closes.
- Best/top context found: Beat ismaildos4's score of 0.551!

Full challenge description from page:

> Overview
> When two genes are deleted simultaneously in a cell, the combined outcome is rarely just the sum of their individual effects. Sometimes the double knockout is far more devastating than expected — a synthetic lethal interaction that reveals hidden genetic buffering. Other times, it is surprisingly mild — one deletion suppresses the defect caused by the other. These non-additive interactions, called genetic epistasis, expose the wiring of biological pathways: which genes are redundant, which buffer each other, and which lie on the same essential route.
> This challenge asks: can a language model infer functional epistasis from natural language alone? No sequences. No expression profiles. No protein structures. Only the plain-text descriptions of what each gene does — its function, biological process, cellular location, and molecular activity — as written by human biologists.
> This is a biological natural language inference (NLI) benchmark. Prior computational work on genetic interaction prediction relies exclusively on structured numerical features (sequence embeddings, network topology, co-expression vectors). This challenge is the first to ask whether the biological knowledge encoded in free-text gene descriptions and controlled GO vocabulary is sufficient to classify functional relationships — and whether language models can extract that reasoning in a zero-shot or fine-tuned setting.
> Classify each gene pair into exactly one of three labels:
> AGGRAVATING — double mutant is much sicker than expected (synthetic sick / synthetic lethal)
> NEUTRAL — effects are roughly additive; no interaction detected
> ALLEVIATING — double mutant is healthier than expected (suppression / rescue)
> Solve it by fine-tuning a pretrained language model on the provided training pairs.
> The Task
> Given a pair of genes described entirely by natural language text, predict the epistasis class of their functional interaction. All genes come from Saccharomyces cerevisiae (baker's yeast). Inputs are free-text function descriptions and GO term annotations; the target is one of three class labels.
> Evaluation
> Submissions are scored with a combined metric that rewards both accurate class predictions and well-calibrated probability estimates. The overall score is a weighted sum of the two components: 70% macro-F1 plus 30% of (1 minus the normalised Brier score). As a formula:
> score = 0.7 × macro_F1 + 0.3 × (1 − normalised_Brier)
> Macro-F1 is the unweighted mean of per-class F1 scores over the three classes — it weights AGGRAVATING, NEUTRAL, and ALLEVIATING equally regardless of frequency, so a model that collapses to the majority class scores poorly.
> Normalised Brier score measures probability calibration. For a three-class problem the raw Brier score has a maximum of 2; dividing by 2 normalises it to [0, 1]. Lower Brier = better calibration; (1 − normalised_Brier) converts it to a reward. A model that predicts the right class with high confidence and the wrong class with low confidence scores near 1.0 on this component.
> Score range: 0.0 (worst) to 1.0 (perfect). A uniform-probability baseline (⅓ each class, majority-class label) scores ≈ 0.32.
> from sklearn.metrics import f1_score
> import numpy as np
> CLASSES = ["AGGRAVATING", "NEUTRAL", "ALLEVIATING"]
> def evaluate(y_true, y_pred, p_mat):
> macro_f1   = f1_score(y_true, y_pred, labels=CLASSES, average="macro")
> y_onehot   = np.eye(len(CLASSES))[[CLASSES.index(c) for c in y_true]]
> brier_norm = np.mean(np.sum((p_mat - y_onehot) ** 2, axis=1)) / 2.0
> return 0.7 * macro_f1 + 0.3 * (1.0 - brier_norm)
> Dataset
> The prepared data is under ./dataset/public/:
> public/
> ├── train.csv              # 32,835 gene pairs with labels
> ├── test.csv               # 17,165 gene pairs without labels
> ├── test_meta.csv          # 17,165 rows — per-row evaluation tier metadata
> └── sample_submission.csv  # 17,165 rows — uniform-probability baseline
> train.csv columns:
> id — Unique pair identifier (pair_NNNNN). Use exactly as-is when submitting.
> gene_a / gene_b — Pseudonymized gene identifiers (e.g. GENE_03471). Train and test use disjoint pseudonym namespaces (non-overlapping numeric ranges plus independent shufflings) — no pseudonym string that appears in train ever appears in test, so cross-split lookup is structurally impossible, not merely obfuscated.
> gene_a_function / gene_b_function — Free-text description of each gene's biological role, normalized to a deduplicated bag of common functional keywords (rare, gene-identifying words are dropped and word order is removed to prevent verbatim lookup against source SGD text). ~96% / ~89% filled in train; ~68% / ~64% filled in test (lower because ~30% of test pairs have descriptions deliberately blanked — see Evaluation Tiers).
> gene_a_process / gene_b_process — GO Biological Process terms, pipe-separated (~35% filled).
> gene_a_component / gene_b_component — GO Cellular Component terms, pipe-separated (~86–89% filled).
> gene_a_function_go / gene_b_function_go — GO Molecular Function terms, pipe-separated (~41–45% filled).
> epistasis_class — Target label: AGGRAVATING, NEUTRAL, or ALLEVIATING.
> test.csv has the same columns as train.csv except epistasis_class.
> test_meta.csv columns:
> id — Matches test.csv.
> split_tier — seen (both genes appear in training) or unseen_module (at least one gene's GO Slim category is entirely absent from training).
> held_out_module — The withheld GO Slim category for unseen_module rows; empty for seen rows.
> description_stripped — True for the ~30% of test pairs whose function description columns have been deliberately zeroed out. These pairs retain GO term columns only. See Evaluation Tiers below.
> Notes:
> Total pairs: 50,000. Train: 32,835 · Test: 17,165.
> Train class distribution: AGGRAVATING ~33% · NEUTRAL ~34% · ALLEVIATING ~33%.
> Epistasis is symmetric: if (A, B) appears in training, (B, A) does not appear in the test set.
> GO Slim terms are from the GO Slim yeast subset — ~60 high-level biological process terms.
> Evaluation Tiers
> The test set is annotated along two independent axes in test_meta.csv, and the leaderboard reports three named tiers built from them — plus an overall score — so you can see exactly where your model's biological understanding breaks down.
> Axis 1 — split_tier (partitions 100% of test, mutually exclusive):
> Tier	split_tier value	What it tests
> Seen	seen	Standard interpolation — both genes appear in training
> Unseen module	unseen_module	Cross-domain transfer — at least one gene's GO Slim category was never seen in training
> Axis 2 — description_stripped (an orthogonal, cross-cutting diagnostic slice, ~30% of test):
> Tier	description_stripped value	What it tests
> Description-blind	True	GO-only reasoning — function text is blanked; the model must infer from controlled GO vocabulary alone
> The description-blind tier is not a third partition member — it is drawn proportionally from both the seen and unseen-module rows, so it overlaps with the other two tiers by design. A row can therefore be, for example, seen and description-blind at the same time. Think of split_tier as answering "has the model seen genes like this?" and description_stripped as answering "does the model still work when the richest text signal is removed?" — the two questions are independent and are reported separately rather than merged into a single flat category.
> test_meta.csv discloses both fields for every test row, so you can reconstruct all three reported tiers (and any of the four underlying combinations) yourself.
> Submission Format
> Submit submission.csv with five columns — one row per test pair:
> id — Identifier from test.csv, format pair_NNNNN. Must match exactly.
> epistasis_class — Predicted class: one of AGGRAVATING, NEUTRAL, ALLEVIATING (case-sensitive).
> p_aggravating — Predicted probability for AGGRAVATING (float in [0, 1]).
> p_neutral — Predicted probability for NEUTRAL.
> p_alleviating — Predicted probability for ALLEVIATING.
> Probabilities must sum to 1.0 per row (±0.01 tolerance). Any row that violates this, any unknown class label, or any missing / duplicate id scores 0.0.
> id,epistasis_class,p_aggravating,p_neutral,p_alleviating
> pair_00000,AGGRAVATING,0.72,0.18,0.10
> pair_00001,NEUTRAL,0.05,0.91,0.04
> pair_00002,ALLEVIATING,0.08,0.13,0.79
> What Not To Use
> Classical bag-of-words models: TF-IDF, word-count features, n-gram models, or any approach that does not use a pretrained language model backbone are disqualified, regardless of score. A TF-IDF + logistic regression baseline already reaches ≈ 0.54 by exploiting surface term co-occurrence — this challenge measures biological language understanding, not surface statistics. Fine-tuning a pretrained language model is required; simpler trained models are out of scope for this benchmark because they can hit a competitive score without any biological language understanding, which defeats the challenge's purpose.
> External label lookup: Gene identifiers are pseudonymized and descriptions are deliberately transformed — do not attempt to reverse-map identifiers or descriptions to source genes or query any external biological database for labels. Predictions must come from a model trained on the provided training data.
> External LLM APIs (OpenAI, Anthropic, Google, etc.) at any point.
> Using test pairs in training (no pseudo-labeling on test rows).
> Allowed and expected: fine-tuning a pretrained language model (BERT, T5, DeBERTa) on the training pairs; data augmentation by swapping gene A and gene B (since epistasis is symmetric); contrastive or multi-task learning; temperature scaling or Platt scaling for calibration.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Pollution Prevention Opportunity-Method Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72qtnxnh4cg4hyq8a08v1tcd8b17gf
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Beat amtech's score of 0.442!

Full challenge description from page:

> Pollution Prevention Opportunity-Method Graph Recovery
> Overview
> Industrial pollution-prevention reports record both what source-reduction activities were implemented and how each opportunity was identified. A single report can contain several activities, each linked to one or more methods such as an internal audit, an employee recommendation, external assistance, or a team process. Methods may be shared across activities, and some plausible method cards in a case are decoys.
> This is an NLP relation-recovery challenge. For each report, reconstruct the bipartite graph connecting activity cards to their true opportunity-identification method cards. The public inputs preserve a leakage-controlled narrative sketch, readable standardized card descriptions, and reduction-band information. Direct source identifiers, facility names, locations, chemical names, source codes, and source URLs are not released.
> The objective is to predict edge_json for every test case.
> Task
> Each row contains two to four activity cards and eight to eleven method cards. Activity IDs are A0 through A3; method IDs are M0 through M10. IDs are row-local and have no meaning across cases.
> Predict every true directed edge in the form A#>M#.
> Important graph properties:
> Every activity has at least one true method neighbor.
> One activity may have up to three method neighbors.
> A method may be linked to multiple activities.
> Some method cards are hard decoys and have no true edge.
> Each row's visible slate size, from eight through eleven method cards, is selected only by a deterministic case-local hash.
> Hard decoys fill the slate after the native true methods are inserted.
> There is no fixed true methods + k formula or target-dependent cap.
> Candidate-card count is therefore independent of the number of true methods and edges.
> The graph is not a one-to-one matching or a fixed-size permutation.
> Dataset
> The preparation pipeline creates:
> public/train.csv - 1,576 labeled report graphs.
> public/test.csv - 414 unlabeled report graphs from facility groups absent from training.
> public/sample_submission.csv - A valid deterministic example with different graph predictions across rows.
> private/answers.csv - Hidden graph labels and row-specific schema information used only by the grader.
> The facility-group split prevents the same reporting facility from appearing in both train and test. Exact prepared input signatures shared with training are removed from test.
> Columns
> case_id string) - Opaque identifier for one prepared report.
> context_packet string) - Ordered leakage-controlled narrative sketch. Common operational words remain readable; other words use stable collision-prone lexical codes. Numbers, URLs, and direct source codes are replaced. The packet also includes a broad year band, three-digit industry sector, chemical-form class, and narrative-presence marker.
> activity_cards_json JSON list) - Activity cards with activity_id, standardized activity_text, and estimated_reduction.
> method_cards_json JSON list) - Candidate cards with method_id and standardized method_text.
> edge_json JSON list of strings) - Training target only. Each string is one directed edge such as A0>M2.
> Submission Format
> Submit a UTF-8 CSV with exactly these columns in this order:
> case_id,edge_json
> P2G_0123456789abcdef,"[""A0>M1"",""A1>M0"",""A1>M3""]"
> P2G_fedcba9876543210,"[""A0>M2"",""A1>M2""]"
> Requirements:
> Include exactly one row for every case_id in public/test.csv.
> Include no missing, duplicate, or unknown IDs.
> edge_json must be a valid JSON list with at most 48 unique strings.
> Every edge must use the exact A#>M# format and reference cards present in that row.
> Use [] when predicting no edges.
> Evaluation
> Scores range from 0 to 1, and higher is better.
> For each row:
> EdgeSetF1 is the set F1 over complete directed edges.
> ActivityNeighborhoodMacroF1 computes F1 between predicted and true method-neighbor sets for each activity, then averages across that row's activities.
> MethodCoverageF1 is the set F1 over method cards used by at least one edge.
> ExactGraphAccuracy is 1 only when the complete predicted edge set equals the true edge set; otherwise it is 0.
> The final score is:
> Score = 0.50 * mean(EdgeSetF1)
> + 0.25 * mean(ActivityNeighborhoodMacroF1)
> + 0.15 * mean(MethodCoverageF1)
> + 0.10 * mean(ExactGraphAccuracy)
> Malformed JSON, duplicate edges, unknown card IDs, missing rows, or an incorrect submission schema fail validation.
> Required Modelling Approach
> The primary relation scorer must be a trainable neural text encoder fine-tuned on relation examples constructed from public/train.csv.
> The neural scorer must contribute directly to final edge probabilities.
> Open-weight pretrained encoders are allowed if they were not trained on this EPA TRI activity-method dataset.
> Classical co-occurrence, graph constraints, calibration, and deterministic ensembles may be combined with the fine-tuned neural scorer.
> Every public field may be used, including relationships among the narrative sketch and both card views.
> Prohibited
> Internet may be used only for package installation, documentation, and downloading generic open-weight encoders. It must not be used to retrieve EPA reports, TRI records, labels, answer maps, or any task-specific data.
> No hosted inference API or closed external model service.
> Searching for or retrieving the original public reports, source workbooks, facility identities, chemicals, source codes, or answer-bearing records.
> Reverse-mapping lexical buckets to original words or matching packets against external text.
> Hardcoded predictions by case ID, row order, or hidden split artifacts.
> Reading private answers, grader files, or any path outside the provided public data and requested output path.
> Runtime Contract
> The execution environment provides one A10G GPU, up to 10 CPU cores, and 62 GB
> RAM. Solutions must finish within 1.5 hours. The entrypoint receives the public
> dataset directory and exact submission path as two positional arguments.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Open-World Attribution Of A Stripped Object Description To Its Image

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78j73z53r6vrhh4nb523zy8s8bqjte
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Background
> When a museum catalogues an object, a curator writes a short description of what the object physically looks like. That description is written by a person looking at the object, and it records things a photograph also records: what is depicted, how the elements are arranged, which way a figure faces, what the surface treatment is, how the parts relate to one another.
> In this challenge you are given such a description with every identifying string removed — no maker, no title, no place, no date. What remains is a purely visual account of an object. You are also given a pool of ten candidate photographs, all of objects from the same curatorial department, so they are broadly similar in kind.
> One of two things is true, and you are not told which:
> the described object is one of the ten photographs, or
> the described object was withheld, and none of the ten is it.
> Your job is to decide which case you are in, and — if the object is present — to say which photograph it is.
> This is deliberately an open-world task. A system that is good at matching but cannot tell when the target is absent will select a plausible-looking wrong image on every unanswerable row, and the metric is built so that this earns nothing. Half the score is attribution and half is knowing when to abstain.
> Task
> For each row in test.csv, output the set of pool indices corresponding to the described object. Output the empty set if you judge the described object is not in the pool.
> The gold answer for a row is either a single index in [0, 10) or the empty set.
> Data
> The dataset contains three CSV files and two image directories.
> train.csv
> Labelled training rows. It has exactly four columns:
> id — string. Unique row identifier, of the form sp_000000. Ids are globally unique across train.csv and test.csv; they never collide.
> query_text — string. The masked curatorial description. Removed strings are replaced by the literal token [MASK]. Typical length is 20–200 words.
> n_pool — integer. The number of candidate images for this row. This is always 10, for every row in both files.
> selected — string. The training label: either a single integer index in [0, 10), or an empty cell meaning the described object is absent from this row's pool.
> test.csv
> Unlabelled evaluation rows. It has exactly three columns, with the same meanings as above: id, query_text, n_pool. There is no selected column.
> sample_submission.csv
> A valid, correctly-formatted submission that selects index 0 on every row. It has exactly two columns: id and selected. It is a formatting example, not a baseline worth beating.
> train/ and test/ image directories
> One subdirectory per row, named by that row's id. Each subdirectory contains exactly ten JPEG files named im_00.jpg, im_01.jpg, … im_09.jpg. The integer in the filename is the pool index used in selected. So for row sp_000123, the image at pool index 4 is the file test/sp_000123/im_04.jpg.
> Every image is a 320×320 RGB JPEG, letterboxed onto a white square canvas. Image slot order is a fresh random permutation for every row and carries no information.
> Submission format
> A CSV with exactly two columns:
> id — every id in test.csv, each appearing exactly once.
> selected — a space-separated list of integer pool indices in [0, 10), or an empty cell to abstain.
> Example:
> id,selected
> sp_002001,4
> sp_002002,
> sp_002003,7
> Row sp_002002 abstains. An empty cell is a valid, meaningful prediction — it asserts that the described object is not in that pool.
> Evaluation
> score = 0.5 * ATTRIBUTION + 0.5 * ABSTENTION
> ATTRIBUTION is the mean set-F1 between your predicted set and the gold set, taken over the answerable rows only (rows whose gold set is non-empty). Abstaining on an answerable row scores 0 for that row.
> ABSTENTION is Youden's J statistic over all rows, treating "predicted the empty set" as a detector for "gold is the empty set":
> sensitivity = P(predicted empty | gold empty)
> specificity = P(predicted non-empty | gold non-empty)
> ABSTENTION  = max(0, sensitivity + specificity - 1)
> The final score is clipped to [0.01, 1.0]. Higher is better.
> Rules
> Your final predictions must come from a model you train or fine-tune within your run.
> Do not attempt to identify the source collection these objects come from, and do not retrieve any external record, image, or catalogue entry for them. Solutions that work by looking up the underlying objects rather than by modelling the image–description relationship will be rejected on review.
> The train/ and test/ pools are disjoint at the object level, and one whole curatorial department appears only at test time. Validate accordingly: a random split of train.csv will overstate your score.
> Notes on difficulty
> The masking is aggressive and deliberate. Names, titles, places and dates are gone, so lexical matching against anything has very little to work with; what remains is visual-content language.
> Distractors are drawn from the same department as the target, so the department itself is not a usable cue.
> Descriptions state orientation and left/right relationships. The images are never mirrored or rotated, so those statements are reliable.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Score-Grounded Trombone Embouchure Control Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71nfsry6kf4dwaxwx1jc9bh58a8psw
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: multimodal, audio, Based on dataset:, Trombone Performance Lip-Force, Pressure, Audio, and Note-Alignment Recordings, Download Data
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Score-Grounded Trombone Embouchure Control Reconstruction
> Overview
> Predict the hidden four-channel mouthpiece-force trajectory for each short trombone performance. For every test episode, use its mono audio, six-note symbolic score, synchronized intraoral and mouthpiece-pressure traces, and three labeled calibration clips from the same anonymous player. Submit all four force values at every 50 Hz time step, together with each note's control state, corrected control boundaries, force-rise or relaxation events, and uncertainty.
> The source sessions recorded 31 trombonists performing predefined tone sequences and melodies under realistic playing conditions. Each musician played through a freshly calibrated sensor-integrated trombone mouthpiece with four load cells beneath its movable rim, one pressure sensor connected to the mouthpiece cup, and another connected to the oral cavity by a flexible tube. The sensor channels were acquired at approximately 1.75 kHz. A Shure BETA 98H/C external clip-on microphone captured 44.1 kHz performance audio, which was aligned to the written score. Challenge preparation exports mono 16 kHz audio and resamples the synchronized physical sequences to the public 50 Hz grid. Audio amplitude is relative and must not be interpreted as calibrated absolute SPL.
> Each row therefore provides the query audio, note-level symbolic score, both pressure channels, and a small calibration set from the same anonymous player. The calibration examples include measured four-channel load-cell force sequences; those force measurements are hidden for the query.
> Your submission must recover the query's four force channels on a 50 Hz grid, identify the control state and transition for every written note, locate force-rise and relaxation events, and estimate note-level measurement ambiguity. These outputs describe measured behavior only. They are not diagnoses or judgments about healthy, correct, ideal, or high-quality playing.
> This is a GPU-based Fine-Tuning / From Scratch structured prediction task. Solvers may fine-tune an open-source audio model jointly with the other modalities or build the complete multimodal architecture from scratch. The dense force trace is the central prediction; note states, alignment-corrected control boundaries, events, and uncertainty make temporal structure and cross-output consistency testable. It is not Computer Vision, Object Detection, tabular classification, or scalar regression.
> Task Specification
> Predict these four fields for every test id:
> force_trace_json: all four synchronized force channels at every public 50 Hz step.
> state_sequence_json: one state and transition object for each score note, including the predicted start/end control boundaries that correct local score-to-control alignment.
> event_sequence_json: the force-rise and relaxation events supported by the episode.
> uncertainty_json: one value in [0,1] per note, where larger values mean more ambiguous measured control evidence.
> The four force channels retain their anonymous sensor names: LC1, LC2, LC3, and LC4. Do not reinterpret them as upper or lower lip anatomy. The legal note states are lc1_dominant, lc2_dominant, lc3_dominant, lc4_dominant, balanced, and uncertain. Legal note transitions are steady, force_rise, and relaxation.
> Generalization And Validation
> Complete anonymous players are held together so the hidden evaluation measures adaptation to players absent from the labeled training players. Each test player still has a small public calibration set, and every score/state/event vocabulary used in evaluation has training support. Repeated runs from one physical player never cross the labeled/hidden boundary.
> Use only labeled training rows for fitting model parameters, normalization, thresholds, calibration mappings, and model selection. The test inputs may be used only for inference. Validate by holding out complete player_token groups from the labeled data; row-random validation will overestimate performance.
> Dataset
> All paths are relative to ./dataset/public/. The prepared corpus contains 607 labeled query episodes, 221 hidden query episodes, and 96 distinct calibration clips. The 96 clips are three disjoint calibration windows for each of 32 recorded performance runs, grouped into 32 run-specific calibration sets. One physical player contributed two runs, so the 32 sets represent 31 base players. Audio, signal, score, and force arrays for one row share the same row-local clock.
> File Overview
> Item	Description
> train.csv	Labeled query rows
> test.csv	Hidden query rows
> sample_submission.csv	Valid weak template
> schema.json	Rates and enums
> calibration_index.csv	Calibration paths
> audio/query/	Query WAV files
> audio/calibration/	Calibration WAV files
> signals/query/	Query pressure NPZ
> signals/calibration/	Calibration NPZ
> score/query/	Query score JSON
> score/calibration/	Calibration scores
> calibration/	Player support sets
> train.csv Columns
> Column	Type	Description
> id	string	Opaque episode id
> player_token	string	Opaque player group
> audio_path	string	Query WAV path
> signal_path	string	Query NPZ path
> score_path	string	Query score path
> calibration_set_path	string	Support-set path
> n_steps	integer	Number of 50 Hz steps
> n_notes	integer	Number of score notes
> duration_s	float	Row-local seconds
> force_trace_json	JSON string	Dense train target
> state_sequence_json	JSON string	Note-state target
> event_sequence_json	JSON string	Event target
> uncertainty_json	JSON string	Ambiguity target
> test.csv Columns
> Column	Type	Description
> id	string	Opaque episode id
> player_token	string	Opaque player group
> audio_path	string	Query WAV path
> signal_path	string	Query NPZ path
> score_path	string	Query score path
> calibration_set_path	string	Support-set path
> n_steps	integer	Number of 50 Hz steps
> n_notes	integer	Number of score notes
> duration_s	float	Row-local seconds
> Score JSON
> Each score file contains grid_hz and a notes list. Every note object has exactly these fields:
> note: zero-based note index.
> onset: onset step on the 50 Hz grid.
> duration: duration in grid steps.
> midi: written MIDI pitch.
> dynamic: written dynamic marking or unknown.
> duration_class: source duration class or unknown.
> articulation: written articulation or none.
> register: written register category or unknown.
> difficulty: source task difficulty or unknown.
> Signal NPZ
> Query signal files contain time_s, pressure, pressure_channels, and grid_hz. Calibration signal files also contain force and force_channels.
> time_s has shape (n_steps,).
> pressure has shape (n_steps,2) in OralPres, MouthPiecePres order.
> force has shape (n_steps,4) in LC1, LC2, LC3, LC4 order.
> Arrays use finite calibration-normalized units. Audio amplitude is relative, not absolute SPL.
> Calibration Sets
> Each calibration_set_path JSON contains exactly three same-player, same-run support entries. Every entry links its calibration audio, pressure/force NPZ, score JSON, and visible target JSON. Query rows from the same recorded run reuse that run's three-entry set; no calibration clip is shared across different players. Calibration windows are disjoint from every scored query window and do not share query note indices.
> Submission
> Write exactly one file to ./working/submission.csv. It must contain one row for every id in test.csv, with no additional rows or columns. Row order does not matter because grading aligns by id.
> Submission Format
> Column	Type	Constraint
> id	string	Every test id once
> force_trace_json	JSON string	Exact dense payload
> state_sequence_json	JSON string	One item per note
> event_sequence_json	JSON string	Valid timed events
> uncertainty_json	JSON string	Values in [0,1]
> The columns must appear in exactly the order shown above.
> force_trace_json is an object with exactly n, channels, and values. n must equal the row's n_steps; channels must equal ["LC1","LC2","LC3","LC4"]; and values must contain exactly n_steps four-number rows. Every value must be finite and in [-6,6].
> {"n":3,"channels":["LC1","LC2","LC3","LC4"],"values":[[0.1,-0.2,0.0,0.3],[0.2,-0.1,0.1,0.4],[0.1,0.0,0.2,0.2]]}
> Each state item has exactly note, start, end, state, and transition. Notes must cover 0..n_notes-1 once each. Boundaries are integer steps satisfying 0 <= start < end <= n_steps.
> [{"note":0,"start":8,"end":42,"state":"balanced","transition":"steady"}]
> Each event item has exactly note, step, and event. event is force_rise or relaxation; references must be in range; duplicate events are invalid; and at most 3*n_notes events may be submitted. uncertainty_json is a list of exactly n_notes finite values in [0,1].
> Wrong/reordered columns, missing or extra rows, duplicate ids, or an id-set mismatch raise InvalidSubmission. A row-local malformed, oversized, non-finite, out-of-range, wrong-shape, or illegal JSON prediction gives that complete row zero credit while other valid rows are still scored.
> Evaluation
> The score is maximized and lies in [0,1]. A perfect valid submission scores exactly 1.0.
> The grader first computes this bounded raw score for each valid row:
> raw_row_score = 0.60 * force_trace_fidelity
> + 0.15 * note_state_score
> + 0.10 * event_timing_f1
> + 0.10 * uncertainty_score
> + 0.05 * cross_output_consistency
> The leaderboard uses a transparent row-level skill score relative to a fixed valid null prediction: four zero force channels, balanced / steady note objects spanning the row, no events, and uncertainty 0.35. The same raw metric evaluates both the submission row and that null row:
> row_skill = max(0, (raw_row_score - null_raw_score) / (1 - null_raw_score))
> final_score = mean(row_skill)
> This linear normalization makes the null score exactly 0, preserves all ordering above the null, and keeps a perfect valid row at exactly 1. It is applied per row, so any malformed row contributes exactly zero even when other rows are valid. The official sample is a deterministic training-force prior rather than the null and therefore remains a non-degenerate positive baseline.
> For force fidelity, the grader compares the submitted and measured traces at shifts from -2 through +2 grid steps and keeps the best valid overlap. Within an overlap:
> amplitude = max(0, 1 - mean_absolute_error / 2.35)
> force_trace_fidelity = 0.46 * amplitude
> + 0.26 * mean positive channel correlation
> + 0.18 * mean positive derivative correlation
> + 0.10 * mean spectral cosine similarity
> Correlations are clipped to [0,1]; anticorrelation receives no correlation credit. The bounded shift tolerance handles small synchronization error without allowing unconstrained alignment.
> note_state_score is 0.50 exact state agreement, 0.25 exact transition agreement, and 0.25 boundary accuracy. Boundary tolerance is max(2, 0.04*n_steps) steps. event_timing_f1 uses one-to-one matches with the same note and event type within three grid steps. uncertainty_score is max(0,1-MAE/0.45).
> Cross-output consistency derives states and events from the submitted force trace over the reference note intervals, then compares those derived objects with the submitted state/event objects. It is 0.45 state agreement, 0.25 transition agreement, and 0.30 event F1. This term cannot replace force accuracy; it only checks whether the submitted heads describe one coherent reconstruction.
> Intended Solution
> A competitive Fine-Tuning solution should use a pretrained open-source audio encoder and adapt it jointly with the pressure, score, calibration, and decoder modules. A competitive From Scratch solution can replace that encoder with a trainable convolutional or transformer waveform front end. Both are GPU-appropriate modeling routes. A practical pipeline is:
> Encode each 16 kHz WAV with a compact pretrained audio encoder or a trainable convolutional/transformer front end.
> Encode query pressure and calibration pressure/force streams with 1D convolutions or temporal transformers.
> Embed note pitch, timing, articulation, dynamic, register, and duration information.
> Fuse query and calibration representations with cross-attention or conditional normalization.
> Decode the four 50 Hz force channels, then predict note states, events, and uncertainty with constrained heads.
> Train with player-grouped validation and mixed precision. An A10G-class GPU with 16-24 GB memory is the target tier; compact encoders should support batches around 8-24 depending on audio backbone and padding. The full solution, including training, inference, and CSV writing, must fit the platform's 90-minute run.
> What Not To Do
> Using a prohibited approach can cause rejection regardless of score.
> Do not retrieve or match the upstream archive, source files, source annotations, original force traces, participant identities, filenames, paths, timestamps, or row order.
> Do not use waveform, pressure, force, file-size, hash, or embedding fingerprints to identify hidden source windows.
> Do not hardcode test ids, per-id predictions, parcours templates, or source-derived lookup dictionaries.
> Do not copy a calibration force trace into query rows without modeling query-specific audio, pressure, and score evidence.
> Do not ignore the dense sequence and submit a reduced single-value or note-only solution.
> Do not access private files, exploit grader exceptions, flood JSON parsers, or use malformed rows as a scoring strategy.
> Do not use hosted inference APIs, runtime internet retrieval, or private external labels.
> Do not attach medical, diagnostic, technique-quality, healthy, correct, or ideal-playing interpretations to the targets.
> Enforcement on invalid approaches: submissions may be rejected before payout when the trajectory shows source lookup, metadata/hash reconstruction, hardcoded test answers, malformed-input exploitation, or a rule-only pipeline that does not train and run a genuine multimodal sequence model on the provided public data.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cross-Modal Robot Dispatch

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a879z87bhcjbc17bn8qzxxx8brmt3
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, multimodal, text, Dataset source is visible after the challenge closes.
- Best/top context found: Beat ivycer's score of 58.284!

Full challenge description from page:

> Cross-Modal Robot Dispatch
> Overview
> Build a fine-tuned cross-modal system for an asynchronous electronics-sorting robot.
> A physical item is visible to an optical camera, but four recent X-ray acquisitions are waiting in the scanner queue. Exactly one X-ray depicts the current optical item; the other three are stale scans selected preferentially from visually and operationally similar items. The model must return one structured robot-dispatch record containing:
> the X-ray slot that belongs to the optical item;
> the operational action for that acquisition;
> every visible battery-hazard box in the matched X-ray.
> The three possible actions are:
> remove: one or more batteries are visible and must be removed before downstream processing;
> release: the acquisition provides clear no-battery evidence and the item may continue;
> reacquire: the acquisition is not safe to route because its internal-state evidence is missing or contradictory, so another X-ray should be requested.
> This is not ordinary object detection. A detector can help localize batteries, but it cannot by itself reconcile the optical and X-ray queues, reject stale scans, or decide when the scanner should reacquire the item. The task jointly tests cross-modal retrieval, acquisition-quality recognition, localization and robot routing.
> Training and test sets are separated by physical item. Multiple acquisitions of one item share a public item_group, allowing group-aware validation while preventing images of the same physical object from appearing in both splits.
> Your complete solution must run on one NVIDIA A10G GPU with 24 GB VRAM and finish within 1 hour, including training, validation, inference and writing the submission. Fine-tuning a CV backbone, detector or multimodal matching model is required.
> Dataset
> dataset/public/
> ├── train.csv
> ├── test.csv
> ├── sample_submission.csv
> └── panels/
> ├── train/
> │   └── <shard>/panel_<opaque_id>.jpg
> └── test/
> └── <shard>/panel_<opaque_id>.jpg
> The prepared dataset contains:
> 1,535 training episodes from 296 physical-item groups;
> 667 test episodes from 125 held-out physical-item groups.
> The item_group sets in train.csv and test.csv are disjoint.
> Panel layout
> Every panel_path points to one 832 × 448 RGB image. The left side contains the optical view of the current item. The right side contains four candidate X-rays in this fixed slot order:
> ┌──────────────────────────┬──────────────┬──────────────┐
> │                          │              │              │
> │      optical image       │    scan 0    │    scan 1    │
> │                          │              │              │
> │                          ├──────────────┼──────────────┤
> │                          │              │              │
> │                          │    scan 2    │    scan 3    │
> │                          │              │              │
> └──────────────────────────┴──────────────┴──────────────┘
> The tile rectangles use (left, top, width, height) pixel coordinates:
> | Region | Rectangle |
> |---|---|
> | Optical image | (16, 16, 416, 416) |
> | Scan slot 0 | (448, 36, 184, 184) |
> | Scan slot 1 | (640, 36, 184, 184) |
> | Scan slot 2 | (448, 228, 184, 184) |
> | Scan slot 3 | (640, 228, 184, 184) |
> Battery boxes use normalized [x1, y1, x2, y2] coordinates relative to the matched X-ray tile, not relative to the complete panel. Coordinates satisfy:
> 0 ≤ x1 < x2 ≤ 1
> 0 ≤ y1 < y2 ≤ 1
> train.csv
> episode_id,item_group,panel_path,dispatch
> Columns:
> episode_id
> Data type: string
> Opaque identifier unique within train.csv.
> item_group
> Data type: string
> Opaque physical-item group. Rows sharing this value are different X-ray acquisitions of the same optical item.
> panel_path
> Data type: string
> Relative path from dataset/public/ to the composite panel.
> dispatch
> Data type: JSON object serialized as a string
> Target record with exactly scan_slot, action, and hazards.
> Example target:
> {"scan_slot":2,"action":"remove","hazards":[[0.1842,0.2731,0.4175,0.6889]]}
> Target constraints:
> scan_slot is an integer from 0 through 3;
> action is remove, release, or reacquire;
> hazards is a list containing at most eight normalized boxes;
> remove has at least one hazard box;
> release and reacquire have an empty hazard list.
> Example rows:
> episode_id,item_group,panel_path,dispatch
> ep_6c22266bdb169455e73a8d,itm_fc08d591bd647f5a457b,panels/train/9d/panel_9d029819bfb4cbdeab1e7e8ed0.jpg,"{""scan_slot"":1,""action"":""remove"",""hazards"":[[0.19375,0.416016,0.465625,0.493359],[0.202344,0.480859,0.460156,0.548828]]}"
> ep_31b1d6c59e2e082e49b92c,itm_9e2279c29d8346846fad,panels/train/bd/panel_bd9762077bcb45c6a54000df79.jpg,"{""scan_slot"":2,""action"":""release"",""hazards"":[]}"
> ep_857519e1fde33ad7d59247,itm_52d965bcc0afd0d5da66,panels/train/a6/panel_a6a5d893ce57ee275e16edff04.jpg,"{""scan_slot"":2,""action"":""reacquire"",""hazards"":[]}"
> test.csv
> episode_id,item_group,panel_path
> The columns have the same meaning as in train.csv, but dispatch is hidden. Every test episode_id must appear exactly once in the submission.
> sample_submission.csv
> episode_id,dispatch
> The sample is a format-valid serialization example. It uses a weak fixed action and contains no target information.
> Submission format
> Write predictions to:
> working/submission.csv
> The CSV must contain exactly these columns in this order:
> episode_id,dispatch
> Each dispatch cell must be a valid JSON object with exactly these keys:
> {"scan_slot":0,"action":"release","hazards":[]}
> A multi-row example:
> episode_id,dispatch
> ep_73f8fdbeab237e66321b19,"{""scan_slot"":2,""action"":""remove"",""hazards"":[[0.181,0.264,0.426,0.701]]}"
> ep_18b6701cbd295bd21d16ba,"{""scan_slot"":0,""action"":""reacquire"",""hazards"":[]}"
> Rows may appear in any order. The grader rejects wrong columns, missing or extra IDs, duplicate IDs, missing values, non-finite numbers, invalid slots, unknown actions, extra or repeated JSON keys, malformed boxes, duplicate boxes, and action/box inconsistencies. Invalid values are not clipped or repaired.
> Evaluation
> The score measures four coupled capabilities:
> cross-modal scan pairing;
> pairing-gated action classification;
> balanced positive/empty hazard handling;
> complete robot dispatch for every action type.
> To prevent physical items with many X-ray acquisitions from dominating, episode i in item group g receives weight:
> w_i = 1 / number_of_episodes_in_group_g
> Thus, the total unnormalized weight of every item group is one.
> 1. Group-balanced pair accuracy
> For episode i:
> pair_i = 1 if predicted_scan_slot_i = true_scan_slot_i, else 0
> The pairing component is the weighted mean:
> pair_accuracy = weighted_mean(pair_i, w_i)
> This is equivalent to averaging pairing accuracy within each item group and then averaging the groups.
> 2. Pairing-gated action macro-F1
> An action receives credit only when its predicted scan slot is correct. For an incorrectly paired episode, the effective action prediction is replaced by a mismatch value distinct from all three valid actions.
> Using the item-group weights, compute F1 separately for:
> release, remove, reacquire
> and average the three values:
> action_score = mean(F1_release, F1_remove, F1_reacquire)
> This prevents a correct action word attached to the wrong scan from receiving credit and prevents the frequent action from dominating the component.
> 3. Pairing-gated hazard score
> For one episode, let T be the true hazard-box set and P the predicted set. A wrong scan slot forces the episode box score to 0.
> For a correctly paired episode:
> T empty and P empty  → box_score = 1
> exactly one is empty → box_score = 0
> When both sets are non-empty, standard intersection over union is:
> IoU(a, b) = area(a ∩ b) / area(a ∪ b)
> Find a maximum-weight one-to-one matching between T and P using IoU as the edge weight. Define:
> soft_iou = maximum_matched_IoU_sum / max(|T|, |P|)
> For each threshold τ ∈ {0.30, 0.50, 0.70}, let m_τ be the maximum number of one-to-one pairs with IoU ≥ τ:
> box_f1_τ = 2 × m_τ / (|T| + |P|)
> The episode score is:
> box_score = 0.40 × soft_iou
> + 0.60 × mean(box_f1_0.30, box_f1_0.50, box_f1_0.70)
> Extra predicted boxes reduce both terms. Compute separate item-group-weighted means for episodes with and without true hazard boxes:
> hazard_positive = weighted_mean(box_score | T non-empty, w_i)
> hazard_empty    = weighted_mean(box_score | T empty, w_i)
> Combine them with the harmonic mean:
> hazard_score = 0, if either mean is 0
> hazard_score = 2 × hazard_positive × hazard_empty
> / (hazard_positive + hazard_empty), otherwise
> The harmonic mean prevents excellent empty-scan handling from compensating for failure to localize real batteries, and vice versa.
> 4. Balanced complete-dispatch score
> An episode is complete when:
> the scan slot is correct;
> the action is correct;
> when true hazards exist, box_score ≥ 0.65;
> when no true hazard exists, no box is predicted.
> Compute a weighted complete rate separately for true release, remove, and reacquire episodes. The component is their three-way harmonic mean:
> complete_action = weighted_mean(complete_i | true action, w_i)
> balanced_complete = harmonic_mean(
> complete_release,
> complete_remove,
> complete_reacquire
> )
> If any action has zero complete rate, balanced_complete is zero. A system must therefore complete all three robot workflows rather than specializing in the majority action.
> Final score
> score = 100 × (
> 0.20 × pair_accuracy
> + 0.20 × action_score
> + 0.40 × hazard_score
> + 0.20 × balanced_complete
> )
> Not allowed
> External APIs or hosted inference services.
> External copies, labels, metadata, or annotations for the same physical items.
> Manual labeling of test panels.
> Hard-coding predictions by episode_id or item_group.
> Recovering source identities or using filenames, row order, JPEG artifacts, repeated-tile frequency, preparation details, or grader behavior instead of modeling the visual task.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cross-Sensor Cell Identity Reconciliation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx760ayp83gvbmwe5g5kss661x8bsdfy
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Beat supegirl's score of 0.325!

Full challenge description from page:

> Overview
> Match five unlabeled cells across three synchronized optical measurements. Each board has an optical-path-difference anchor row followed by amplitude and hologram rows. The latter two rows may be permuted, locally degraded, and visually confusable with nearby cells. Predict the two cross-sensor assignment matrices, the evidence-quality grade for every matched cell, and the overall packet condition.
> In label-free imaging flow cytometry, one physical cell can look radically different in optical path, amplitude, and raw interference measurements. A swapped sensor packet can corrupt downstream cell analysis even when every individual panel appears plausible. This challenge evaluates adaptation of a visual encoder to cross-sensor cellular morphology, where identity must survive acquisition physics, hard negative cells with similar morphology, and degraded local evidence.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Labeled cross-sensor packet records. |
> | `test.csv` | Packet records without target columns. |
> | `sample_submission.csv` | Schema-valid baseline predictions. |
> | `sensor_packets/` | 1074 by 624 RGB JPEG evidence boards. |
> Each board is a 3 by 5 panel array. Rows are OPD, amplitude, and hologram. Columns are numbered 1 through 5 independently within every row. The OPD row fixes the anchor identity order. The amplitude and hologram rows contain the same five physical cells but can be reordered. A blurred panel or blocked band is degraded evidence, not a new cell. Some packets deliberately contain near-neighbor cells with similar morphology, so evidence quality is not just an artifact detector.
> | Prepared item | Count |
> |---|---:|
> | Training packets | 2,115 |
> | Hidden test packets | 500 |
> | Opaque packet images | 2,615 |
> Packet states are represented in both splits:
> | Packet state | Train | Test |
> |---|---:|---:|
> | `triple_concordance` | 214 | 60 |
> | `shared_reindex` | 615 | 145 |
> | `sensor_divergence` | 767 | 178 |
> | `evidence_gap` | 519 | 117 |
> The training evidence-quality entries contain 519 zeros, 8,642 ones, and 11,989 twos. Code 1 can arise from visible degradation or from a true match whose morphology is too similar to another candidate cell in the same packet.
> Columns
> | Column | Present in | Data type | Description |
> |---|---|---|---|
> | `case_id` | Train and test | String | Opaque unique packet identifier. |
> | `cross_sensor_packet_path` | Train and test | String | Relative path under `sensor_packets/`. |
> | `sensor_order` | Train and test | String | Fixed statement of row and column ordering. |
> | `cell_assignment_tensor` | Train only | JSON integer tensor, shape 2 by 5 by 5 | Tensor plane 1 maps OPD anchors to amplitude columns; plane 2 maps OPD anchors to hologram columns. Every 5 by 5 plane is a permutation matrix. |
> | `evidence_quality_matrix` | Train only | JSON integer matrix, shape 2 by 5 | Rows are amplitude and hologram. Columns are OPD anchors 1-5. Values are `2` complete and distinctive, `1` degraded or visually ambiguous but usable, or `0` severely obstructed. |
> | `packet_state` | Train only | Categorical string | `triple_concordance`, `shared_reindex`, `sensor_divergence`, or `evidence_gap`. |
> triple_concordance means amplitude and hologram both preserve the OPD order. shared_reindex means amplitude and hologram share the same non-identity order. sensor_divergence means the two non-anchor rows disagree with each other. evidence_gap takes precedence when any amplitude or hologram match has evidence code 0. Code 1 remains usable and does not by itself change the packet state.
> Example:
> cell_assignment_tensor = [[[0,1,0,0,0],[1,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]],[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]]
> evidence_quality_matrix = [[2,2,0,2,1],[2,2,1,2,2]]
> packet_state = evidence_gap
> Evaluation
> The Cross-Sensor Identity Score combines three capabilities:
> Score = 0.72 * AssignmentScore
> + 0.18 * EvidenceQualityScore
> + 0.10 * PacketStateScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> AssignmentScore
> A submitted assignment must contain two valid permutation matrices. An invalid tensor receives zero.
> entry_agreement = mean(I(Y[s,i,j] = P[s,i,j]))
> row_match = mean(I(argmax(Y[s,i,:]) = argmax(P[s,i,:])))
> sample_assignment = 0.03 * entry_agreement
> + 0.12 * row_match
> + 0.85 * I(Y = P)
> AssignmentScore is the mean sample_assignment.
> EvidenceQualityScore
> For hidden vector Y and submitted vector P:
> proximity = mean(max(0, 1 - abs(Y[i] - P[i]) / 2))
> sample_morphology = 0.15 * proximity + 0.85 * I(Y = P)
> EvidenceQualityScore is the mean sample score.
> PacketStateScore
> Compute accuracy separately within each hidden packet state, then average the four state accuracies equally. If a state is absent from the hidden set, it is omitted. Invalid labels are incorrect.
> Submission Format
> Write ./working/submission.csv with exactly these columns in order:
> case_id,cell_assignment_tensor,evidence_quality_matrix,packet_state
> Example:
> case_id,cell_assignment_tensor,evidence_quality_matrix,packet_state
> cl54de0617f4ea11f3b531,"[[[0,1,0,0,0],[1,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]],[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]]","[[2,2,0,2,1],[2,2,1,2,2]]",evidence_gap
> JSON fields are limited to 220 characters. The grader rejects the wrong column order, extra columns, duplicate or unknown IDs, missing rows, and extra rows. Bad JSON, wrong shapes, non-integers, and values outside the documented vocabulary score zero for the affected component.
> Method Requirements
> Use a learned visual model trained on the supplied packet boards. Local open-weight pretrained encoders may be adapted. The expected workload includes twelve-panel feature extraction and two cross-row assignments, for which the provided A10G is materially useful.
> The solution time limit is 30 minutes on one A10G GPU.
> What Not To Use
> Do not map IDs, row positions, image names, hashes, compression size, or board layout seeds to targets.
> Do not match packet panels against external source images, source labels, or public mirrors.
> Do not create a fingerprint lookup table from duplicated source assets.
> Do not infer test answers from archive order or original cell-population folder names.
> Do not exploit submission parsing, duplicate rows, optional columns, or grader failure behavior.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cadencefall: Audio Timbre Retrieval and Instrument Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73c05906r8keqwm3j4b6720d8bp1br
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, large-scale, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Cadencefall: Audio Timbre Retrieval and Instrument Matching
> Overview
> Domain: Fine-Tuning
> The rhythm citadel of Cadencefall has lost the labels on its game-score relics. Each puzzle presents one anchor note and eight shuffled candidate notes. Restore three distinct routes:
> lower_slot — the candidate played by the anchor's exact hidden instrument at a lower pitch.
> upper_slot — the candidate played by that exact hidden instrument at a higher pitch.
> bridge_slot — a different instrument that shares both the anchor's hidden instrument family and its acoustic, electronic, or synthetic production source.
> The two exact-instrument echoes are 4 through 16 semitones below and above the anchor. The bridge is selected near the anchor's pitch. Five adversarial foils come from other family-source pairs and are pitch-matched around the lower echo, anchor, and upper echo. Instrument names, source metadata, MIDI pitch, velocity, family, and production source are all held out. Audio paths and ids are opaque.
> This is a structured unseen-instrument retrieval task, not instrument classification. All notes from an instrument stay on one side of the split. Test instruments never occur in training. A supplied audio encoder was pretrained only on training-side instruments; the intended solution fine-tunes it jointly across each nine-note puzzle with a global three-slot assignment. GPU execution is required and the 1.5-hour limit applies to the complete solution.
> Evaluation
> The metric is macroTimbreRelayScore, maximized on the closed interval [0, 1].
> For each row, let the predicted exact-instrument pair be the set containing lower_slot and upper_slot.
> T measures unordered exact-instrument pair overlap: it is the size of the set intersection between the predicted pair {lower_slot, upper_slot} and the true pair, divided by 2. Swapping the two predicted roles does not change T.
> O measures ordered slot accuracy: it is the mean of the exact lower_slot indicator and the exact upper_slot indicator. Swapping the two predicted roles can therefore reduce O even when T is unchanged.
> B is 1 when bridge_slot is exact and 0 otherwise.
> Row utility is U_row = 0.40*T + 0.40*O + 0.20*B.
> Rows with a non-numeric, non-integer, repeated, missing, infinite, or out-of-range slot receive utility 0. Utilities are averaged within each hidden test anchor-instrument group. The group means are then macro-averaged so large instruments cannot dominate. The published score is:
> import numpy as np
> def parse_slot(value):
> text = str(value)
> if len(text) > 128:
> return -1
> try:
> number = float(text.strip())
> except (TypeError, ValueError, OverflowError):
> return -1
> if not np.isfinite(number) or number != np.floor(number):
> return -1
> slot = int(number)
> return slot if 0 <= slot <= 7 else -1
> def evaluate(y_true, y_pred, hidden_groups):
> row_utility = []
> for truth, pred in zip(y_true, y_pred):
> lo, hi, bridge = map(parse_slot, pred)
> if min(lo, hi, bridge) < 0 or len({lo, hi, bridge}) < 3:
> row_utility.append(0.0)
> continue
> true_lo, true_hi, true_bridge = map(int, truth)
> twin = len({lo, hi} & {true_lo, true_hi}) / 2.0
> ordered = 0.5 * (lo == true_lo) + 0.5 * (hi == true_hi)
> row_utility.append(0.40 * twin + 0.40 * ordered + 0.20 * (bridge == true_bridge))
> row_utility = np.asarray(row_utility, dtype=float)
> group_means = [row_utility[np.asarray(hidden_groups) == g].mean() for g in sorted(set(hidden_groups))]
> return float(np.mean(group_means))
> The private group labels are used only for final scoring. Perfect structured recovery scores 1.0; wholly malformed content scores 0.0.
> Dataset
> The prepared public data has 4,800 training puzzles and 1,800 test puzzles. It includes 14,507 audio assets. The train and test sides share zero source instruments and zero audio notes.
> train.csv — puzzle paths plus all three slot targets.
> test.csv — puzzle paths with the three targets held out.
> sample_submission.csv — label-free format example using a fixed distinct-slot baseline.
> audio/ — 14,507 four-second 16 kHz mono WAV assets with opaque randomized filenames.
> checkpoints/base_encoder.pt — the supplied Cadencefall audio-encoder checkpoint for fine-tuning.
> Columns in train.csv:
> id (string) — opaque randomized puzzle identifier.
> anchor_path (string) — path relative to ./dataset/public/ for the anchor WAV.
> candidate_0_path through candidate_7_path (string) — eight shuffled candidate WAV paths.
> lower_slot (integer) — correct lower exact-instrument candidate slot, 0 through 7.
> upper_slot (integer) — correct upper exact-instrument candidate slot, 0 through 7.
> bridge_slot (integer) — correct different-instrument family-source bridge slot, 0 through 7.
> test.csv contains the same id and path columns but no target columns.
> Submission
> Write ./working/submission.csv with exactly 1,800 rows and exactly these columns in this order:
> id
> lower_slot
> upper_slot
> bridge_slot
> Use every test id exactly once. Row order does not matter because grading merges on id. Each slot must be an integer from 0 through 7, and the three slots in a row must be distinct.
> Example using real test ids:
> id,lower_slot,upper_slot,bridge_slot
> syu4kau5zvup6fjk3pfb,0,1,2
> u6pntkeqtkt4j94h7efm,0,1,2
> z77874k7fxsaga72t99y,0,1,2
> Requirements
> Complete preprocessing, fine-tuning, inference, and CSV writing within 1.5 hours.
> Read only from ./dataset/public/.
> Write only ./working/submission.csv.
> Submit exactly the required header and 1,800 required ids, without duplicates or foreign ids.
> Treat each slot as an integer in 0 through 7 and keep all three predicted slots distinct.
> Missing, NaN, infinite, non-integer, repeated, oversized, or out-of-range slot content receives worst row utility.
> What Not To Use
> Do not use external datasets, pretrained weights other than checkpoints/base_encoder.pt, internet access, or runtime downloads.
> Do not install packages at runtime.
> Do not access hidden instrument names.
> Do not derive signal from ids or filenames; they are randomized and intentionally inert.
> Extra Modelling Information
> Cadencefall changes the mechanism from pair verification or family classification into a nine-audio, three-role structured relay.
> A solver must jointly recover an ordered cross-pitch exact-instrument pair and a different-instrument family-source bridge under an instrument-disjoint holdout, while rejecting pitch-matched foils.
> Global slot exclusivity and hidden-group macro scoring make independent classification heads insufficient. This structured timbre-lineage assignment is the challenge's central novelty.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Subsea Transect Retention Memory

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72jwy6fsbk4sdhsdaczvbrn18brtrb
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Beat jesuisnadi's score of 0.774!

Full challenge description from page:

> Overview
> For each six-panel underwater transect board, predict three outputs: a retention-transition matrix showing whether each object class appears, persists, disappears, or stays absent between neighboring panels; a compact weak-link sequence naming the most important unstable transitions; and a mission disposition summarizing whether the short transect is stable, intermittent, degraded, or rapidly changing.
> The input is not a set of independent classification images. It is a short ordered pass from an underwater survey vehicle, where adjacent panels can show the same asset class under changing turbidity, distance, edge truncation, and lighting. The task measures whether an adapted visual encoder can retain evidence across a sequence of views and distinguish true disappearance from weak but continuing visual support.
> This is useful in subsea inspection workflows because survey teams often need to know whether a pipe, net, marker, or vehicle part remained visible across a pass, appeared only briefly, or was lost under poor imaging conditions. The ground truth is derived from object annotations and image-quality checks inside guarded acquisition blocks, with source blocks kept disjoint between training and hidden evaluation.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Labeled six-panel transect records. |
> | `test.csv` | Transect records without target columns. |
> | `sample_submission.csv` | Schema-valid baseline submission. |
> | `survey_packets/` | 974 by 548 RGB JPEG boards containing six numbered underwater panels. |
> Boards use a 3 by 2 layout. Panels 1-3 run left to right on the first row; panels 4-6 run left to right on the second row. The panel numbers define temporal order for the transition matrix. Underwater color, contrast, scale, and edge clipping vary between panels.
> Source frames are grouped into guarded acquisition blocks before splitting. A source block belongs entirely to training or hidden evaluation, and eight neighboring frames around each block boundary are excluded from packet construction. This reduces adjacent-frame retrieval across the split.
> | Prepared item | Count |
> |---|---:|
> | Training transects | 1,433 |
> | Hidden test transects | 351 |
> | Opaque survey-board images | 1,784 |
> Mission dispositions are represented in both splits:
> | Mission disposition | Train | Test |
> |---|---:|---:|
> | `stable_track` | 245 | 90 |
> | `intermittent_track` | 382 | 80 |
> | `evidence_loss` | 552 | 126 |
> | `scene_turnover` | 254 | 55 |
> The training retention-transition matrix contains 28,385 absent-stable entries, 5,907 appearance entries, 2,796 persistence entries, and 5,902 disappearance entries.
> Columns
> | Column | Present in | Data type | Description |
> |---|---|---|---|
> | `case_id` | Train and test | String | Opaque unique transect identifier. |
> | `survey_packet_path` | Train and test | String | Relative JPEG path under `survey_packets/`. |
> | `frame_contract` | Train and test | String | Fixed statement that panels 1-6 form an ordered transect and that class rows use the documented order. |
> | `retention_transition_matrix` | Train only | JSON integer matrix, shape 6 by 5 | Rows are object classes. Columns are transitions 1->2 through 5->6. Values are `0` absent in both panels, `1` appears, `2` persists, and `3` disappears. |
> | `weak_link_sequence` | Train only | Ordered token sequence string | Up to eight panel-major event tokens for appearances, disappearances, and weak persistent links. Use `none` only when there are no event tokens. Tokens are joined by `>`. |
> | `mission_disposition` | Train only | Categorical string | One of `stable_track`, `intermittent_track`, `evidence_loss`, or `scene_turnover`. |
> The matrix row order is fixed:
> row 1 = propeller
> row 2 = pipe_type2
> row 3 = red_fin
> row 4 = net
> row 5 = qr_codes
> row 6 = pipe
> Transition values:
> | Value | Meaning |
> |---:|---|
> | `0` | The class is absent in both neighboring panels. |
> | `1` | The class appears in the right panel after being absent in the left panel. |
> | `2` | The class is visible in both neighboring panels. |
> | `3` | The class disappears from the right panel after being visible in the left panel. |
> Weak-link tokens have this grammar:
> p<left>-<right>:<class_name>:<event>
> left and right must be neighboring panel numbers from 1-2 through 5-6. class_name must be one of propeller, pipe_type2, red_fin, net, qr_codes, or pipe. event must be appear, drop, or weak_keep. Tokens are ordered first by transition interval and then by the fixed class-row order.
> Example labeled values:
> retention_transition_matrix = [[0,0,0,0,0],[3,1,3,1,2],[3,0,0,1,2],[0,0,0,0,0],[1,3,1,3,0],[3,0,0,1,3]]
> weak_link_sequence = p1-2:pipe_type2:drop>p1-2:red_fin:drop>p1-2:qr_codes:appear>p1-2:pipe:drop>p2-3:pipe_type2:appear>p2-3:qr_codes:drop>p3-4:pipe_type2:drop>p3-4:qr_codes:appear
> mission_disposition = scene_turnover
> Submission Format
> Write the final file to exactly:
> ./working/submission.csv
> The CSV must contain exactly these columns in this order:
> case_id,retention_transition_matrix,weak_link_sequence,mission_disposition
> Example:
> case_id,retention_transition_matrix,weak_link_sequence,mission_disposition
> sr4e8a3d417bce5680544d,"[[0,0,0,0,0],[3,1,3,1,2],[3,0,0,1,2],[0,0,0,0,0],[1,3,1,3,0],[3,0,0,1,3]]",p1-2:pipe_type2:drop>p1-2:red_fin:drop>p1-2:qr_codes:appear>p1-2:pipe:drop>p2-3:pipe_type2:appear>p2-3:qr_codes:drop>p3-4:pipe_type2:drop>p3-4:qr_codes:appear,scene_turnover
> retention_transition_matrix must be a JSON integer matrix with shape 6 by 5 and values from 0 through 3. weak_link_sequence must be none or a >-delimited sequence of at most eight valid tokens. Each sequence field is limited to 520 characters. The grader rejects extra columns, reordered columns, duplicate IDs, unknown IDs, missing rows, and extra rows. Malformed matrices or invalid token strings receive zero for the affected component.
> Evaluation
> The Subsea Retention Memory Score is:
> Score = 0.55 * TransitionMatrixScore
> + 0.30 * WeakLinkSequenceScore
> + 0.15 * MissionDispositionScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> TransitionMatrixScore
> For hidden matrix Y and submitted matrix P, define entry weights from the hidden truth:
> w[i,j] = 1.0 when Y[i,j] = 0
> w[i,j] = 1.6 when Y[i,j] = 2
> w[i,j] = 2.4 when Y[i,j] is 1 or 3
> weighted_agreement = sum(w[i,j] * I(Y[i,j] = P[i,j])) / sum(w[i,j])
> Let active mean matrix entries greater than zero.
> active_iou = sum(active(Y) and active(P)) / sum(active(Y) or active(P))
> sample_transition = 0.18 * active_iou
> + 0.22 * weighted_agreement
> + 0.60 * I(Y = P)
> If both active sets are empty, active_iou = 1.0. TransitionMatrixScore is the mean sample_transition across hidden rows.
> WeakLinkSequenceScore
> Tokenize both sequences on >, with none treated as an empty sequence. Invalid tokens, duplicate tokens, overlong fields, or tokens out of panel-major order receive zero.
> set_f1 = 2 * |tokens_Y intersect tokens_P| / (|tokens_Y| + |tokens_P|)
> similarity = 1 - token_edit_distance(tokens_Y, tokens_P) / max(len(tokens_Y), len(tokens_P), 1)
> sample_sequence = 0.25 * set_f1
> + 0.20 * similarity
> + 0.55 * I(tokens_Y = tokens_P)
> If both token sets are empty, set_f1 = 1.0. WeakLinkSequenceScore is the mean sample_sequence.
> MissionDispositionScore
> Compute recall separately for each hidden mission disposition present in the answer file, then average those recalls equally. Invalid disposition strings are incorrect.
> Method Requirements
> Use the supplied labeled transect boards to fit the model. Open-weight visual encoders may be adapted locally. The intended workload uses GPU-batched six-panel feature extraction and temporal evidence aggregation within the A10G limit.
> The solution time limit is 30 minutes on one A10G GPU.
> What Makes This Interesting
> The central object is retention memory across a short underwater pass. A model must compare neighboring panels, detect whether evidence continues under viewpoint and water-quality changes, and emit a canonical transition certificate. This differs from single-image object detection because the answer depends on how visual evidence changes between panels, not only whether a category appears somewhere.
> What Not To Use
> This is a finetuning challenge, please do not use the following methods :
> Do not use source-image lookup, reverse image search, external copies, original video identities, or source annotations.
> Do not infer targets from opaque IDs, row order, JPEG names, hashes, byte sizes, or archive position.
> Do not memorize exact train images and search for related hidden views outside the supplied data.
> Do not create hardcoded object-channel rules from source filenames or directory names.
> Do not exploit malformed fields, duplicate IDs, extra columns, optional columns, or grader exceptions.
> Reference Validation
> Exact hidden answers score 1.0. The sample submission scores 0.095372. An independent train-mode submission scores 0.119371. The prepared split has zero duplicate public payloads and zero train-test survey-board hash overlap.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Spectromorphological Sound Description

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dysd9m8084wejnymnwn0cgs8bnqwc
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Experimental electroacoustic sounds are difficult to describe with ordinary event names. A sound can arrive sharply, accumulate into a stratified mass, vacillate, decay, pulse irregularly, and recede without being a familiar scene event.
> Objective: for each episode, listen to one anonymous query sound and four annotated calibration sounds from the same anonymous contributor, then predict the query's complete spectromorphological ontology, its onset-to-sustain-to-offset chain, one concise human-style description, nine field confidences, and an uncertainty band.
> The audio is real contributed experimental-sound material recorded under varied creative and technical conditions. The public corpus contains 587 labeled query episodes in train.csv, of which 495 have split_role=train and 92 have split_role=validation, plus 129 hidden-label query episodes in test.csv. All 872 public audio files are 16 kHz mono PCM-16 FLAC. Clip duration ranges from about 0.169 to 23.823 seconds, with a median of about 8.090 seconds.
> Each calibration record contains a different real clip, its complete source ontology, and its original human-written description. Calibration clips never serve as scored query clips. Complete contributor groups are held out: the 27 training, 6 validation, and 6 test contributors do not overlap. The model therefore has to learn audio structure and decide whether the same-contributor examples provide useful contributor-specific context. A one-clip classifier or captioner leaves the episodic adaptation question unresolved.
> Task
> For every test episode, submit:
> type_json: one or more native sound-type labels.
> mass_type: one native sound-mass label.
> complexity: one native complexity label.
> onset, sustain, and offset: the three native morphology stages.
> pulse_typology: one native pulse label.
> processes_json: zero or more native process labels.
> direction: one native direction label.
> morphology_chain: the submitted onset, sustain, and offset joined in that order.
> description: one concise audible-content description, not an explanation or a second technical/poetic target.
> confidence_json: one confidence for each of the nine structured fields.
> uncertainty: low, medium, or high, derived from mean confidence.
> The morphology chain is categorical. Do not invent timestamps, temporal boundaries, rankings, rationales, or multiple captions; no such truth is supplied.
> Intended approach
> A credible solution fine-tunes an open audio encoder or audio-language model on GPU. One practical design encodes query and calibration audio with shared weights, encodes calibration ontology and text as episodic context, fuses those representations, and trains separate single-label, multilabel, confidence, and short-text heads. The text decoder should be conditioned on the predicted ontology or checked against it so fluent unsupported details are not rewarded. Use the contributor-held-out validation rows for model selection and confidence calibration.
> Training from scratch is allowed, but the task is sized for fine-tuning an open model on an A10G-class GPU. Runtime downloads, hosted inference APIs, and closed-source model services are not allowed. Any pretrained weights must be open, locally available before the run, and fine-tuned on the released training episodes rather than used as an external answer service.
> This is a GPU Fine-Tuning challenge. The intended solution fine-tunes an open-weights audio-language model, or an audio encoder with structured and text decoders, on GPU. The CSV files are only a transport format; the modeling inputs are multiple real audio clips plus text and ontology context.
> Dataset
> The public file overview is:
> Path	Contents
> train.csv	587 labeled query episodes.
> test.csv	129 hidden-label query episodes.
> sample_submission.csv	Valid weak schema baseline.
> ontology.json	Allowed source ontology strings.
> train/audio/	Train/validation query and calibration FLAC.
> test/audio/	Test query and calibration FLAC.
> train.csv and test.csv share these four input fields:
> Column	Type	Meaning
> episode_id	string	Opaque unique episode ID.
> contributor_group	string	Opaque same-contributor group ID.
> query_audio_path	string	Public-root-relative query FLAC path.
> calibration_json	JSON string	Ordered list of four calibration records.
> In prose, episode_id identifies the row, contributor_group groups episodes from the same anonymous contributor, query_audio_path points to the sound to predict, and calibration_json contains four labeled same-contributor examples. train.csv also contains split_role plus all eleven supervised query targets from type_json through description. test.csv contains none of those query targets.
> Every calibration record has these fields:
> Field	Type	Meaning
> calibration_id	string	Opaque calibration clip ID.
> audio_path	string	Public-root-relative FLAC path.
> type	string list	Native multi-label type.
> mass_type	string	Native mass type.
> complexity	string	Native complexity.
> onset	string	Native onset.
> sustain	string	Native sustain.
> offset	string	Native offset.
> pulse_typology	string	Native pulse typology.
> processes	string list	Native multi-label processes.
> direction	string	Native direction.
> morphology_chain	string	Onset, sustain, and offset chain.
> description	string	Original human description.
> The two list-valued targets are type and processes; all other ontology fields are single strings. All allowed strings and exact capitalization are listed in ontology.json. The descriptions are original human annotations and can be multilingual or idiosyncratic; no generated paraphrases are included.
> Submission
> Write the final CSV to exactly ./working/submission.csv. It must have one row for every test episode_id and exactly these 14 columns in this order:
> Order	Column	Constraint
> 1	episode_id	Exact test ID, once.
> 2	type_json	Sorted unique nonempty label list.
> 3	mass_type	Valid ontology string.
> 4	complexity	Valid ontology string.
> 5	onset	Valid ontology string.
> 6	sustain	Valid ontology string.
> 7	offset	Valid ontology string.
> 8	pulse_typology	Valid ontology string.
> 9	processes_json	Sorted unique label list; [] allowed.
> 10	direction	Valid ontology string.
> 11	morphology_chain	<onset> -> <sustain> -> <offset>.
> 12	description	Grounded text, 3 to 600 characters.
> 13	confidence_json	Exact nine-key numeric object.
> 14	uncertainty	low, medium, or high.
> The exact confidence_json keys are type, mass_type, complexity, onset, sustain, offset, pulse_typology, processes, and direction; every value must be finite and in [0,1]. The uncertainty band is low when mean confidence is at least 0.75, medium when it is at least 0.45 but below 0.75, and high otherwise. JSON key order is not scored, but the key set must be exact.
> One parseable schema example is:
> Column	Example value
> episode_id	ep_example
> type_json	["Synthesis","Textural"]
> mass_type	Composite or Stratified sound
> complexity	Relatively simple element
> onset	Marked onset
> sustain	Iteration
> offset	Soft ending
> pulse_typology	Irregular pulse train
> processes_json	["Filtered","Granular"]
> direction	Neutral
> morphology_chain	Marked onset -> Iteration -> Soft ending
> description	A layered synthetic texture with irregular pulses.
> confidence_json	{"type":0.50,"mass_type":0.50,"complexity":0.50,"onset":0.50,"sustain":0.50,"offset":0.50,"pulse_typology":0.50,"processes":0.50,"direction":0.50}
> uncertainty	medium
> Evaluation
> The official metric is SpectromorphologyDescriptionScore, a transparent 0-to-1 composite. Higher is better. Structured ontology recovery carries 66% of the score; caption content carries 17%; morphology-chain recovery, ontology-caption consistency, calibrated confidence, and exact nine-field joint recovery carry the remainder. The theoretical minimum is 0.0 and a perfect valid submission scores exactly 1.0.
> For type and processes, FieldScore = 0.60 * macro_label_F1 + 0.40 * mean_sample_F1. Macro label F1 averages binary F1 over the source labels represented in the answer set. Sample F1 is set F1 for one row; a valid empty process set against an empty true process set scores 1. For each of the seven single-label fields, FieldScore is macro-F1 over the true ontology classes.
> Structured = 0.15*Type + 0.15*Processes + 0.10*(MassType + Complexity + Onset + Sustain + Offset + PulseTypology + Direction).
> The caption metric is semantic/content overlap rather than exact string equality. Text is Unicode-normalized and case-folded; punctuation is mapped to spaces; disclosed stopwords are removed; a small deterministic stemmer and sound-concept alias lexicon are applied. For each row:
> ContentF1 is set F1 over normalized content tokens.
> CharF1 is mean set F1 over normalized character 3-grams and 4-grams.
> ConceptF1 is set F1 over the disclosed sound-concept groups.
> CaptionBase = 0.55*ContentF1 + 0.30*CharF1 + 0.15*ConceptF1.
> CaptionRow = 0.75*CaptionBase + 0.25*ContentPrecision.
> Caption = mean(CaptionRow).
> Chain is the fraction whose submitted chain equals the hidden source onset, sustain, and offset chain. Consistency checks sound concepts explicitly mentioned in the caption against the submitted ontology; a caption that mentions no recognized ontology concept receives zero consistency credit. Joint is the fraction of rows with all nine structured fields exactly correct.
> For confidence, exact correctness is computed separately for all nine structured fields. Brier = mean((confidence - exact_field_correctness)^2) and Calibration = clip(1 - Brier/0.25, 0, 1).
> The final metric is 0.66*Structured + 0.17*Caption + 0.03*Chain + 0.04*Consistency + 0.06*Calibration + 0.04*Joint.
> The grader aligns rows by episode_id; row order does not matter. Wrong, missing, extra, or reordered columns; blank or duplicate IDs; an ID set different from test.csv; and malformed, non-finite, or out-of-range confidence raise InvalidSubmissionError. Malformed row-local ontology JSON, unknown/duplicate labels, an invalid morphology chain, unsafe/overlong description text, or inconsistent uncertainty make the complete affected row earn zero across all components while other rows continue to be scored. Invalid rows receive no calibration or consistency credit. The valid training-only prior sample scores 0.134546 on the hidden set.
> What Not To Use
> Do not search for the source corpus, match audio fingerprints against external archives, recover original filenames or contributors, or copy external annotations.
> Do not derive answers from episode_id, contributor_group, clip IDs, file names, file sizes, durations, hashes, codec artifacts, row order, split membership, or any mapping back to original media.
> Do not access private answers, organizer provenance, attribution maps, grader internals, filesystem paths outside the public data, or package caches.
> Do not use hosted or closed-source model APIs for training, inference, caption generation, pseudo-labeling, distillation, or judging. Runtime internet access is prohibited.
> Do not generate additional labels, captions, paraphrases, or explanations with an LLM. Use only the released human supervision.
> Do not submit a CPU-only rule/lookup system, a fixed label-frequency answer, a metadata-only system, a caption-only system, or a model that ignores query audio.
> Do not submit regex/template inversion, audio-fingerprint lookup, nearest-source answer copying, hardcoded ID tables, or a one-clip reduction that ignores the four calibration records.
> Enforcement on invalid approaches: solutions can be rejected before payout even when their CSV is structurally valid if they use prohibited source lookup, external answer recovery, hidden-file access, runtime services, or non-model shortcuts. The competition rewards locally trained GPU audio-language modeling from the released public episodes.
> Sample submission preview
> These are the literal header and first five rows of the generated
> sample_submission.csv. The complete file contains one row for every test
> episode and uses the same 14-column order.
> "episode_id","type_json","mass_type","complexity","onset","sustain","offset","pulse_typology","processes_json","direction","morphology_chain","description","confidence_json","uncertainty"
> "ep_02c70afabed36e67","[""Synthesis"",""Textural""]","Composite or Stratified sound","Relatively simple element","Marked onset","Iteration","Soft ending","Irregular pulse train","[""Filtered"",""Granular"",""Layering""]","Neutral","Marked onset -> Iteration -> Soft ending","A layered synthetic sound with an evolving noisy texture.","{""complexity"":0.4202020202020202,""direction"":0.45454545454545453,""mass_type"":0.3616161616161616,""offset"":0.3111111111111111,""onset"":0.3575757575757576,""processes"":0.00202020202020202,""pulse_typology"":0.26666666666666666,""sustain"":0.3333333333333333,""type"":0.03434343434343434}","high"
> "ep_0526e1a32fdb8160","[""Synthesis"",""Textural""]","Composite or Stratified sound","Relatively simple element","Marked onset","Iteration","Soft ending","Irregular pulse train","[""Filtered"",""Granular"",""Layering""]","Neutral","Marked onset -> Iteration -> Soft ending","A layered synthetic sound with an evolving noisy texture.","{""complexity"":0.4202020202020202,""direction"":0.45454545454545453,""mass_type"":0.3616161616161616,""offset"":0.3111111111111111,""onset"":0.3575757575757576,""processes"":0.00202020202020202,""pulse_typology"":0.26666666666666666,""sustain"":0.3333333333333333,""type"":0.03434343434343434}","high"
> "ep_05aa80fc7f06a25c","[""Synthesis"",""Textural""]","Composite or Stratified sound","Relatively simple element","Marked onset","Iteration","Soft ending","Irregular pulse train","[""Filtered"",""Granular"",""Layering""]","Neutral","Marked onset -> Iteration -> Soft ending","A layered synthetic sound with an evolving noisy texture.","{""complexity"":0.4202020202020202,""direction"":0.45454545454545453,""mass_type"":0.3616161616161616,""offset"":0.3111111111111111,""onset"":0.3575757575757576,""processes"":0.00202020202020202,""pulse_typology"":0.26666666666666666,""sustain"":0.3333333333333333,""type"":0.03434343434343434}","high"
> "ep_08a70bf1322d981a","[""Synthesis"",""Textural""]","Composite or Stratified sound","Relatively simple element","Marked onset","Iteration","Soft ending","Irregular pulse train","[""Filtered"",""Granular"",""Layering""]","Neutral","Marked onset -> Iteration -> Soft ending","A layered synthetic sound with an evolving noisy texture.","{""complexity"":0.4202020202020202,""direction"":0.45454545454545453,""mass_type"":0.3616161616161616,""offset"":0.3111111111111111,""onset"":0.3575757575757576,""processes"":0.00202020202020202,""pulse_typology"":0.26666666666666666,""sustain"":0.3333333333333333,""type"":0.03434343434343434}","high"
> "ep_09ead784e5cbc9f9","[""Synthesis"",""Textural""]","Composite or Stratified sound","Relatively simple element","Marked onset","Iteration","Soft ending","Irregular pulse train","[""Filtered"",""Granular"",""Layering""]","Neutral","Marked onset -> Iteration -> Soft ending","A layered synthetic sound with an evolving noisy texture.","{""complexity"":0.4202020202020202,""direction"":0.45454545454545453,""mass_type"":0.3616161616161616,""offset"":0.3111111111111111,""onset"":0.3575757575757576,""processes"":0.00202020202020202,""pulse_typology"":0.26666666666666666,""sustain"":0.3333333333333333,""type"":0.03434343434343434}","high"

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Forecasting Expert Attention in RTS Replays

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74y3feyj4t2h3efmh44rtb3s8bse7q
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Build a computer-vision fine-tuning system that predicts where an expert RTS participant will direct on-screen attention next.
> Each example is a 512 × 512 tactical board containing four chronological snapshots arranged from top-left to bottom-right. The board is generated from a professional two-side match and intentionally removes participant names, arena names, faction names, original interface elements, and identifying metadata. It preserves spatial and temporal evidence useful for forecasting a focal participant's next view change:
> cyan and amber density fields summarize recent spatial activity for the two anonymized sides;
> outlined squares represent persistent structures and base locations;
> gray density and marks summarize neutral map objects;
> rings and crosses show recent deployments, losses, and pressure events;
> short trails show recent command destinations;
> the white path and view box show the focal participant's recent screen-camera motion;
> paired bars summarize recent economy, army, and production state; a thin white frame marks which anonymized side is the focal participant;
> faint lines divide every panel into the nine output sectors.
> Your output is a structured attention-routing directive for the next major screen-camera move:
> the destination sector;
> which side will dominate the destination view;
> how soon the move will begin;
> how long the destination will remain the focus.
> This models a real replay-analysis and attention-assistance workflow. A useful system can prioritize review clips, compare expert attention patterns during coaching, cue highlight extraction, and provide one input to attention-aware spectator tools. It is not ordinary image classification: destination, subject, timing, and dwell must agree as one operational record.
> The public training set is drawn from three spaced earlier competition periods, while final evaluation uses disjoint match episodes from one later held-out period. Evaluation arena layouts may recur from training or may be new, but the normalized spatial semantics and all output values are shared. The split therefore tests transfer across a later competitive period and changing map pool rather than unseen-label guessing.
> Your complete solution must run on one NVIDIA A10G GPU with 24 GB of VRAM and finish within 1 hour, including training, validation, inference, and writing the submission. Fine-tuning a pretrained visual backbone is required. The custom tactical visual grammar, four-panel temporal layout, and coupled route labels have no direct zero-shot class vocabulary; frozen generic image features are useful as initialization but are not expected to be competitive without task-specific training.
> Dataset
> dataset/public/
> ├── images/
> │ └── <opaque_id>.jpg
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> Preparation retains 2700 training rows and 750 test rows. Each row has one image board; rows from the same match episode share an opaque group identifier.
> train.csv
> id,arena_id,episode_id,image_path,directive
> Columns:
> id
> Data type: string
> Opaque row identifier, unique within train.csv.
> arena_id
> Data type: string
> Opaque group shared by examples with the same underlying arena layout. Use it for grouped validation.
> episode_id
> Data type: string
> Opaque match-episode group. All rows from one episode share this value and must remain in the same validation fold.
> image_path
> Data type: string
> Path relative to dataset/public/ for the four-snapshot tactical board.
> directive
> Data type: JSON object serialized as a string
> The complete routing target.
> A training target has exactly this schema:
> {"mode":"route","sector":5,"subject":"mixed","horizon":1,"dwell":2}
> Target fields:
> mode: always "route" for labeled rows;
> sector: integer from 0 through 8, using this image-space layout:
> 0 1 2
> 3 4 5
> 6 7 8
> subject: one of:
> "alpha": cyan-side activity dominates the destination view;
> "beta": amber-side activity dominates the destination view;
> "mixed": both sides materially occupy or act in the view;
> "open": neither side materially dominates the view;
> horizon: time from the final input snapshot to the next major camera move:
> 0: at most 3 seconds;
> 1: more than 3 and at most 6 seconds;
> 2: more than 6 and at most 9 seconds;
> 3: more than 9 and at most 12 seconds;
> dwell: duration of the next destination view:
> 0: less than 2 seconds;
> 1: at least 2 and less than 5 seconds;
> 2: at least 5 and less than 9 seconds;
> 3: at least 9 seconds.
> test.csv
> id,arena_id,episode_id,image_path
> The columns have the same meanings as in train.csv, but directive is omitted. Training and test episode_id sets are disjoint. Every test id must appear exactly once in the submission.
> sample_submission.csv
> id,directive
> The sample uses the valid abstention record:
> {"mode":"abstain"}
> Abstention receives zero credit. The sample is therefore a format example with an exact score of 0.0.
> Submission format
> Write predictions to:
> working/submission.csv
> The CSV must contain exactly these columns in this order:
> id,directive
> Each directive must be either:
> {"mode":"abstain"}
> or a complete route object with exactly the five route keys:
> {"mode":"route","sector":5,"subject":"mixed","horizon":1,"dwell":2}
> Example:
> id,directive
> case_03571ce1c2471e06fdd8,"{""mode"":""route"",""sector"":5,""subject"":""mixed"",""horizon"":1,""dwell"":2}"
> case_3d29b06c49888d14afaf,"{""mode"":""abstain""}"
> Rows may appear in any order. Do not submit probabilities, additional keys, additional columns, missing rows, or duplicate IDs.
> Evaluation
> For a route prediction, map each sector to its row and column in the 3 × 3 sector grid. Define:
> sector_distance = max(|predicted_row - true_row|,
> |predicted_col - true_col|)
> spatial_similarity = max(0, 1 - sector_distance / 2)
> subject_exact = 1 when the subject is exact, else 0
> horizon_similarity = max(0, 1 - |predicted_horizon - true_horizon| / 3)
> dwell_similarity = max(0, 1 - |predicted_dwell - true_dwell| / 3)
> full_exact = 1 when all four route fields are exact, else 0
> The row score is:
> spatial_similarity × (
> 0.20
> + 0.20 × subject_exact
> + 0.15 × horizon_similarity
> + 0.15 × dwell_similarity
> )
> + 0.30 × full_exact
> A neighboring sector can receive partial spatial credit, but every non-exact location gates the subject and timing terms. Even a prediction with all non-spatial fields correct receives at most 0.35 when its sector is only adjacent. The 0.30 exact-record bonus makes coherent prediction of the complete operational directive materially more valuable than four independent guesses. Exceeding 50 therefore requires reliable localization together with useful subject and timing forecasts.
> To stop common arenas or commonly visited regions from dominating, row scores are aggregated in three explicit stages:
> Arena-sector mean: for each distinct pair (arena_id, true_sector), average the row scores of all test examples belonging to that arena whose true destination is that sector.
> Arena mean: for each arena_id, average its arena-sector means over the true sectors that are present for that arena. Each present sector therefore has equal weight within the arena, regardless of its row count.
> Final score: average the arena means over all test arenas, giving every arena equal weight, and multiply the result by 100.
> An abstention row has score 0. The score range is mathematically:
> direction: maximize
> minimum: 0.0
> maximum: 100.0
> A fully exact submission scores exactly 100.0. A submission that abstains on every row scores exactly 0.0.
> Not allowed
> External APIs or hosted inference services.
> External RTS replay collections, game-state logs, camera traces, annotations, or labels.
> Manual labeling of test images.
> Hard-coding predictions by id, arena_id, episode_id, filename, or row order.
> Exploiting identifiers, row order, image encoding, serialization artifacts, or grader behavior instead of modeling the tactical boards.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Reaction Saddle Curvature Adapter

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76dqvpw9psxjafnse1t15p418bscqw
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Predict a compact reaction-curvature certificate from three shuffled molecular geometries. For every case, a packet contains the lower-energy minimum, transition-state saddle, and higher-energy minimum from one elementary reaction. The structures are presented in unknown order and without energies, forces, or Hessians. Your model must order the stationary points and infer which atoms and curvature responses define the unstable saddle mode.
> This setting represents a practical model-adaptation problem in computational chemistry. Full Hessian calculations are expensive, yet reaction screening often needs to know whether a proposed saddle is localized on the intended atoms or spread across several competing directions. A useful adapted molecular encoder should transfer curvature knowledge learned from labeled reactions to unseen bond-change families, rather than merely reproduce a scalar energy.
> Each prediction has four connected parts:
> | Output | What it represents |
> |---|---|
> | `stationary_role_word` | Assignment of the lower well, saddle, and higher well to the three packet slots. |
> | `active_atom_set` | Atom indices carrying the dominant transition-mode displacement. |
> | `curvature_probe_matrix` | Quantized responses of four geometry-defined probes under the hidden transition-state Hessian. |
> | `transition_mode_status` | Whether the dominant unstable mode is localized, coupled, diffuse, or multi-axis. |
> The public geometries are sufficient for supervised adaptation, but none of the four targets is printed in a packet or recoverable from an identifier. Bond-change signatures used in the hidden set are separated from those used for training.
> What Makes This Interesting
> Most molecular-potential benchmarks reduce a structure to energy or force error. Here the model must recover a structured account of where the reaction coordinate lives and how local curvature responds to several probes. Two geometries with similar composition can require different certificates because their saddle modes involve different atom subsets or competing negative directions.
> The task rewards a shared geometric representation. A strong approach can fine-tune an equivariant molecular encoder with separate role, atom-selection, probe-response, and mode-status heads. The held-out bond-change families make formula memorization and nearest-neighbor lookup unreliable.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public training rows with packet paths and all four targets. |
> | `test.csv` | Public test rows with packet paths only. |
> | `sample_submission.csv` | A schema-valid example submission containing one row per test case. |
> | `geometry_packets/` | Compressed NumPy packets containing shuffled atomic structures and probe definitions. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier used only to align a submission row. |
> | `geometry_packet_path` | string | Relative path such as `geometry_packets/7c1f...npz`. |
> | `packet_contract` | string | Declares packet axis order, atom-index convention, and probe normalization. It is identical for cases that share a packet version and contains no target values. |
> Geometry Packet
> Each .npz file contains:
> | Array | Data type | Shape | Description |
> |---|---|---|---|
> | `atomic_numbers` | `int16` | `(n_atoms,)` | Atomic numbers in canonical atom order. |
> | `coordinates` | `float32` | `(3, n_atoms, 3)` | Three centered molecular geometries in shuffled packet order. |
> | `valid_atom_mask` | `uint8` | `(n_atoms,)` | One for a physical atom. |
> | `probe_vectors` | `float32` | `(4, n_atoms, 3)` | Four normalized geometry-defined displacement probes. |
> Coordinates are expressed in angstroms. Atom labels in the targets use zero-based packet atom indices with two digits: a00, a01, and so on.
> Target Columns
> | Column | Data type | Valid format |
> |---|---|---|
> | `stationary_role_word` | string | Exactly `L:i>S:j>H:k`, where `i`, `j`, and `k` are a permutation of packet slots 1, 2, and 3. `L` is the lower-energy well, `S` is the saddle, and `H` is the higher-energy well. Example: `L:2>S:1>H:3`. |
> | `active_atom_set` | pipe-delimited string | Between two and eight distinct atom tokens in ascending order, such as `a01|a04|a05`. |
> | `curvature_probe_matrix` | JSON integer matrix | Exactly 4 by 4. Every entry is one of `-2`, `-1`, `0`, `1`, or `2`. |
> | `transition_mode_status` | categorical string | One of `localized`, `coupled`, `diffuse`, or `multi_axis`. |
> The matrix is the symmetric projection of the hidden saddle Hessian onto the four public probe vectors. Entry [r,c] quantizes probe_r transpose * Hessian * probe_c after division by the largest absolute projected response in that case. Values at or below -0.42 and -0.12 become -2 and -1; values at or above 0.12 and 0.42 become 1 and 2; values inside the neutral interval become 0.
> Evaluation
> Minimum score: 0.0
> Maximum score: 1.0
> The metric is the Saddle Curvature Certificate Score. It combines four bounded component scores:
> Score = 0.20 * RoleAlignmentScore
> + 0.25 * ActiveAtomScore
> + 0.43 * CurvatureProbeScore
> + 0.12 * TransitionModeScore
> Higher is better. The minimum possible score is 0.0, and the maximum possible score is 1.0.
> RoleAlignmentScore
> Parse the three submitted role positions. For sample i, let e_i be 1 when the complete role word is exact, and let a_i be the fraction of the three individual role positions that are correct.
> role_i = 0.55 * e_i + 0.45 * a_i
> RoleAlignmentScore = mean_i(role_i)
> An invalid role word receives 0 for that sample.
> ActiveAtomScore
> Let T_i and P_i be the true and predicted atom sets. Set F1 uses exact token equality:
> precision_i = |T_i intersection P_i| / |P_i|
> recall_i    = |T_i intersection P_i| / |T_i|
> F1_i        = 2 * precision_i * recall_i / (precision_i + recall_i)
> atom_i      = 0.20 * 1[T_i = P_i] + 0.80 * F1_i
> ActiveAtomScore = mean_i(atom_i)
> The usual zero-set conventions apply. An invalid or overlong set receives 0 for that sample.
> CurvatureProbeScore
> For each 4 by 4 truth matrix Y, entry weight w[r,c] is 3 when Y[r,c] is nonzero and 1 otherwise. For prediction P:
> weighted_agreement = sum(w[r,c] * 1[Y[r,c] = P[r,c]]) / sum(w[r,c])
> matrix_i = 0.62 * 1[Y = P] + 0.38 * weighted_agreement
> CurvatureProbeScore = mean_i(matrix_i)
> This weighting prevents a neutral all-zero matrix from receiving disproportionate credit. A malformed, non-integer, out-of-range, or incorrectly shaped matrix receives 0 for that sample.
> TransitionModeScore
> TransitionModeScore is standard unweighted macro F1 across the four documented status classes. F1 for a class is 2TP / (2TP + FP + FN), and the class scores are averaged. Invalid status strings are counted as incorrect predictions.
> Submission Format
> Write the final CSV to exactly:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,stationary_role_word,active_atom_set,curvature_probe_matrix,transition_mode_status
> Example:
> case_id,stationary_role_word,active_atom_set,curvature_probe_matrix,transition_mode_status
> sc_7c1f9a04d18b91c2e4f,L:2>S:1>H:3,a01|a04|a05,"[[0,-1,0,1],[-1,0,1,0],[0,1,2,-1],[1,0,-1,0]]",coupled
> Submission IDs must match the test IDs exactly. Missing rows, extra rows, duplicate IDs, duplicate columns, reordered columns, or extra columns cause the submission to be rejected. The optional backend-managed visibility column is removed before this exact schema check. Matrix strings longer than 180 characters and atom-set strings longer than 96 characters are treated as malformed.
> Expected Methods
> The challenge is designed for a learned molecular representation. Appropriate methods include fine-tuning an SE(3)-equivariant graph network, adapting a pretrained molecular potential encoder, or training a compact geometric transformer with shared atom embeddings and multiple prediction heads. Joint losses and chemistry-preserving coordinate augmentation are allowed.
> What Not To Use
> Do not infer answers from case_id, packet filenames, row order, file order, hashes, or split position.
> Do not search for the public packets in external mirrors and copy hidden Hessian-derived labels.
> Do not use a hardcoded structure-to-answer lookup table or nearest-neighbor table built from an external copy of the source collection.
> Do not exploit submission parsing, malformed JSON, duplicate rows, or numeric overflow.
> Do not train, calibrate, or select thresholds using hidden test labels or grader feedback.
> Local open-weight pretrained molecular models are allowed. Hosted inference APIs are not allowed.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Few-Shot Voice Action Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78rpmfj63kvr00w39mcffs958br4v9
- DOMAIN exactly as displayed: Fine-Tuning
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
> Domain: Fine-Tuning
> Objective: For each row in test.csv, rank all five tokens in candidate_tokens by matching its query WAV against the five enrollment.csv WAVs with the same episode_id; place the best-matching token first.
> After a solar storm disables cloud service, each Hushforge field phone must learn five local voice actions from one labeled example each. One phone calibration is an episode containing five reference enrollments. Each enrollment overlaps two different speakers and commands: a louder lead starts first, then a quieter echo. Order matters, and each ordered pair is bound to a randomized token. A query uses new recordings, speakers, timing, and gain but matches one enrollment pair.
> The source clips are real recordings captured by volunteers with phone or laptop microphones in non-studio rooms; exact microphone and room metadata is unavailable. Prepared WAVs digitally mix two normalized clips from different speakers with a 41–188 ms delay and varied gains. They are not simultaneous field recordings and add no handset simulation.
> Train and test use 1,225 and 525 disjoint source-speaker groups. Commands, speaker keys, and source filenames are withheld, while all public identifiers and tokens are randomized. The supplied 138,688-parameter encoder was pretrained only on training-side speakers. Fine-tune and run it on a GPU within 90 minutes, then compare each query against its five enrollments.
> Evaluation
> The metric is difficultyWeightedMacroBraidMRR, maximized on the closed interval [0, 1].
> For a format-valid row, let r be the rank of the true action token in the submitted five-token ranking, where r=1 is best and r=5 is worst. Row utility is:
> row_utility = ((1.0 / r) - 0.2) / 0.8
> The five valid ranks therefore receive utilities 1.0, 0.375, 0.1666666667, 0.0625, and 0.0. A missing, NaN, infinite, oversized, duplicated, unknown, or otherwise malformed ranking receives row utility 0.0.
> Each query belongs to one fixed hidden acoustic-difficulty band created from its lead-to-echo dominance and onset separation:
> easy has weight 1.0;
> medium has weight 1.35;
> hard has weight 1.70.
> Row utilities are difficulty-weighted within each test handset episode. The final score is the unweighted mean of the 35 episode scores so an episode with more queries cannot dominate:
> import numpy as np
> def evaluate(ranks, episode_groups, difficulty_weights):
> ranks = np.asarray(ranks, dtype=float)
> utility = np.clip(((1.0 / ranks) - 0.2) / 0.8, 0.0, 1.0)
> groups = np.asarray(episode_groups)
> weights = np.asarray(difficulty_weights, dtype=float)
> episode_scores = [
> np.average(utility[groups == group], weights=weights[groups == group])
> for group in sorted(set(groups))
> ]
> return float(np.clip(np.mean(episode_scores), 0.0, 1.0))
> A valid perfect submission scores 1.0. A submission that places every target last, or provides wholly invalid prediction content, scores 0.0. The label-free sample ranking scores above zero because chance ordering has nonzero reciprocal-rank utility.
> Dataset
> The prepared data contains 3,204 scored query braids across 155 handset episodes and 775 enrollment braids. It contains 3,979 distinct one-second, 16 kHz, mono WAV assets. Every braid uses two different source voices, and no source recording is reused. Train and test source-speaker groups are disjoint.
> train.csv — 2,216 labeled training queries from 120 episodes.
> test.csv — 988 unlabeled test queries from 35 episodes.
> enrollment.csv — five token-labeled enrollment braids for each of all 155 episodes.
> sample_submission.csv — a label-free format example using the displayed candidate order.
> audio/ — 3,979 randomized WAV assets referenced by the CSV files.
> checkpoints/hushforge_base_encoder.pt — the supplied 96-dimensional convolutional encoder checkpoint.
> checkpoints/MODEL_CARD.md — checkpoint architecture, training scope, license, and limitations.
> Columns in train.csv:
> id (string) — opaque randomized query identifier.
> episode_id (string) — opaque handset-episode identifier used to join the five enrollments.
> audio_path (string) — path relative to ./dataset/public/ for the query braid.
> candidate_tokens (string) — the episode's five valid action tokens separated by single spaces in a randomized display order.
> target_token (string) — the correct action token for the training query.
> test.csv contains the same columns except target_token.
> Columns in enrollment.csv:
> episode_id (string) — episode identifier shared with query rows.
> action_token (string) — the action bound to this enrollment braid.
> audio_path (string) — path relative to ./dataset/public/ for the enrollment braid.
> Submission
> Write ./working/submission.csv with exactly 988 rows and exactly these columns in this order:
> id
> ranking
> ranking must contain all five candidate tokens for that row, each exactly once, separated by single spaces from most to least plausible. Use every test id exactly once. Row order does not matter because grading merges on id.
> Example using real test ids and the label-free displayed candidate order:
> id,ranking
> d2cqpqncnh9ys1i6e275fk,v6rx08lo5n6safuu2q rzigrxp8822rhknauo 073l3nnxe1px9qambk z9pw6ep50u5x5g1o61 p1g2jacpow51gk5d0u
> 6dyczxp88ursmi7cprmd7y,v6rx08lo5n6safuu2q z9pw6ep50u5x5g1o61 rzigrxp8822rhknauo p1g2jacpow51gk5d0u 073l3nnxe1px9qambk
> fwd8d7tfudsf5mq9gt7yaw,zieurlw4wzp2re76vb izjptpxz2t92ekyee0 hgksolw0f059tq7ypn 2pvkkzdxd1194n5cia zd9cptl8qwitvka2y5
> Requirements
> Use a GPU for encoder fine-tuning and inference. CUDA is the target environment; Apple MPS is suitable for development.
> Finish loading, fine-tuning, inference, and CSV writing within 90 minutes.
> Read only from ./dataset/public/.
> Write only ./working/submission.csv.
> Submit exactly the required header and 988 required ids, without missing, duplicate, or foreign ids.
> For every row, rank exactly the five tokens shown in that row's candidate_tokens, without repetition or additions.
> Structural id or schema violations raise a clean ValueError.
> Invalid ranking content, including NaN, infinite, oversized, duplicated, missing, or foreign tokens, receives worst row utility.
> What Not to Use
> Do not use external audio, external datasets, pretrained weights other than checkpoints/hushforge_base_encoder.pt, internet access, or runtime downloads.
> Do not install packages at runtime.
> Do not access source command names, source speaker keys, hidden difficulty bands.
> Do not infer from ids, tokens, row order, or filenames. They are randomized and intentionally inert.
> Do not hard-code test rankings or copy a stored submission.
> The CSV grader can enforce output validity and score integrity. The execution harness must enforce the GPU, network, external-data, and private-path restrictions.
> Extra Modelling info
> Hushforge instead defines a new action vocabulary inside every handset episode, expresses each action through one ordered overlapping two-voice enrollment braid, and asks for a full five-action ranking on new mixtures from held-out speakers.
> A solver must preserve lead-versus-echo order, separate two simultaneous commands, infer the local token binding, and adapt a supplied encoder without ever seeing source command identities.
> Global word classification, speaker memorization, and token-frequency lookup do not directly produce an action ranking. The mechanism is episodic ordered-mixture rebinding under source-group holdout.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Image-Audio-Question Bundle Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74pfexg13vwpbxhakkw9eqwd8bqzkg
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: multimodal
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Multimodal assistants often receive several images, audio clips, and questions in one request. Before answering, the system must determine which visual and acoustic evidence belongs to each question. A model that answers the text correctly but attaches evidence from another event is unsafe to use for media review, accessibility, and archive search.
> This is a multimodal fine-tuning challenge. Every row contains three questions with four answer options each, twelve shuffled images, and twelve separately shuffled audio clips. Exactly three images and three audio clips are positive evidence for the questions; the other eighteen media items are genuine modality-specific distractors. Starting from general-purpose pretrained vision, audio, and language representations, fine-tune a model that can recover the matching image, recover the matching audio, and select the correct answer option for each question.
> The three positive cases in a bundle are deliberately chosen from nearby task and media cohorts. For each positive case, three additional image distractors and three separately chosen audio distractors are included through balanced modality-specific neighbor maps. The image and audio candidate memberships therefore differ, and a source may appear in a bundle as an image-only or audio-only distractor while its partner modality is absent. File validity, silence detection, media type, option length, cross-bundle co-occurrence, or a fixed slot rule cannot identify the correct assignment. Strong solutions should adapt language, vision, and audio encoders to this evidence-reconstruction objective, learn cross-modal compatibility from the released training labels, and solve two injective assignments before answering the questions.
> Objective
> Fine-tune a pretrained multimodal model, cross-modal projection layers, or parameter-efficient adapters using train.csv and the referenced media. For each test bundle, predict one canonical sequence with three operations in question order:
> Q0:IMGx,AUDy,OPT_z;Q1:IMGx,AUDy,OPT_z;Q2:IMGx,AUDy,OPT_z
> Here, IMGx is the matching image slot from IMG0 through IMG11, AUDy is the matching audio slot from AUD0 through AUD11, and OPT_z is the selected answer OPT_A, OPT_B, OPT_C, or OPT_D). The three predicted image slots must be distinct, and the three predicted audio slots must be distinct. Nine image slots and nine audio slots remain unused.
> Fine-Tuning Formulation
> The 3,600 training bundles provide 10,800 labeled question-level decisions and repeated hard-negative contexts for every training media case. A practical formulation can combine 3-by-12 image-question compatibility, 3-by-12 audio-question compatibility, answer-option loss, and structured injective assignment losses. Participants may fine-tune an end-to-end multimodal model or train lightweight adapters and fusion layers on frozen pretrained encoders. Training a general-purpose vision-audio-language foundation model entirely from scratch is not the objective of this challenge.
> Dataset
> The released data contains 3,600 training bundles and 720 test bundles. The test size is 20% of the training size. Each underlying media case is assigned to exactly one of train, public test, or private test before bundles are constructed; every repeated exposure of that case remains on the same side. This prevents memorizing a training media case and retrieving it from test after fine-tuning.
> Images are standardized JPEG files at 448 by 448 pixels. Audio is standardized as mono 16 kHz MP3 with a maximum duration of 24 seconds. Media paths use independent opaque identifiers: an image filename does not reveal the corresponding audio filename, question, source record, label, split, or visibility.
> Training and test bundles use disjoint underlying media cases. Within each split, every case has balanced positive exposure and balanced distractor exposure. Three deterministic derangements build the image distractors, three separately seeded derangements build the audio distractors, and no distractor is one of the three positive cases in that row. Question order, the complete image order, the complete audio order, wrong-option order, and correct-option position use separate hash domains. Consequently, image order does not determine audio order, and the set of bundles containing an image does not uniquely identify its partner audio.
> Files
> train.csv contains the bundle inputs and target_sequence labels.
> test.csv contains the bundle inputs without labels.
> sample_submission.csv shows the required submission schema.
> images/ contains the referenced JPEG files.
> audio/ contains the referenced MP3 files.
> Input Columns
> id: opaque unique bundle identifier.
> question_0, question_1, question_2: questions in canonical output order.
> q0_option_A through q2_option_D: four candidate answers for each question.
> image_0 through image_11: paths to the twelve shuffled candidate images.
> audio_0 through audio_11: paths to the twelve independently shuffled candidate audio clips.
> target_sequence: training-only canonical label.
> Evaluation
> Each of the three question operations yields four binary indicators:
> image_hit = 1 when the predicted image slot equals the true image slot, otherwise 0.
> audio_hit = 1 when the predicted audio slot equals the true audio slot, otherwise 0.
> answer_hit = 1 when the predicted option equals the true option, otherwise 0.
> joint_hit = image_hit × audio_hit × answer_hit.
> Let N be the total number of question operations in the evaluated rows. Define:
> image_accuracy = sum(image_hit) / N
> audio_accuracy = sum(audio_hit) / N
> answer_accuracy = sum(answer_hit) / N
> joint_accuracy = sum(joint_hit) / N
> The final score is:
> score = 0.20 × image_accuracy + 0.20 × audio_accuracy + 0.30 × answer_accuracy + 0.30 × joint_accuracy
> The score ranges from 0.0 to 1.0, and higher is better. A perfect submission scores 1.0. A uniformly random valid prediction has expected image accuracy 1/12, audio accuracy 1/12, answer accuracy 1/4, joint accuracy 1/576, and final score approximately 0.1089.
> The grader raises a clear ValueError if the columns or identifiers do not exactly match the documented schema, or if any prediction is blank, non-string, malformed, noncanonical, contains whitespace, contains an unknown token, repeats an image/audio slot, omits a slot, or includes an extra operation. A syntactically valid but incorrect prediction is scored normally and may legitimately receive 0.0.
> Submission Format
> Submit a CSV with exactly two columns in this exact order: id,prediction. Every test id must occur exactly once. Predictions are case-sensitive and must contain no spaces.
> id,prediction
> B55YGXMYXGY5QV33MLK,"Q0:IMG10,AUD4,OPT_C;Q1:IMG2,AUD11,OPT_A;Q2:IMG7,AUD1,OPT_B"
> What Not to Use
> Solutions must be developed from the released public challenge files. To preserve blind evaluation, do not use private answers, hidden test annotations, grading-environment data, external copies of the media records, original record metadata, reverse-image or audio-fingerprint search, task-text lookup against public archives, or manually annotated test bundles. Do not treat filenames, bundle incidence, candidate frequency, or an inferred image-to-audio lookup table as semantic evidence. Pretrained general-purpose vision, audio, and language models are allowed when they do not contain or retrieve challenge-specific test labels.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Smartwatch Inhaler Protocol Completeness And Timing Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dxvcb33fk11havbbnqaacjd8a96q8
- DOMAIN exactly as displayed: Fine-Tuning
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
> Objective: for each complete smartwatch audio episode, determine whether activation and pre-inhalation exhalation occurred, measure five timing values (four event durations and the inhalation-to-post-exhalation gap), and report calibrated confidence in the complete result.
> Consumer wearables can hear the mechanical and respiratory events surrounding use of a handheld inhaler. A useful coaching or quality-assurance system must do more than classify an already-cut sound. It must audit a complete episode containing long background regions, decide which protocol steps are present, and measure the audible timing of the observed steps.
> The public corpus contains 212 labeled episodes in train.csv: 168 fitting episodes from four participants and 44 validation episodes from one unseen participant. test.csv contains 72 hidden-label episodes from two additional unseen participants. Every audio file is a fixed 48-second mono 16 kHz PCM WAV. Each episode is source-grounded in real smartwatch recordings and uses real manually annotated activation, inhalation, and exhalation events. All event components in an episode come from one participant, and complete participants remain on only one side of the fitting, validation, or hidden-test boundary.
> This is not the ordinary task of assigning one of three labels to a pre-segmented clip. The input is one full episode. The output is a coupled event-presence and continuous-timing audit.
> Coupled Whole-Episode Contract
> Each row is evaluated as one coupled reconstruction of the complete 48-second protocol episode, not as a collection of independently scored event windows. The complete-result target succeeds only when both optional-event presence decisions and all five timing quantities are simultaneously correct within the disclosed tolerances; confidence is calibrated against that same joint outcome. A strong model must therefore combine event discovery, cross-event timing, protocol completeness, participant-held-out transfer, and joint uncertainty from one full waveform rather than only classify or segment short inhaler sounds.
> Task
> For every hidden episode, predict exactly these seven targets and one confidence value:
> activation_present: whether the audible device-activation event is present, yes or no.
> pre_exhalation_present: whether an exhalation occurs before inhalation, yes or no.
> activation_duration_sec: audible activation duration in seconds; submit 0 when activation is absent.
> pre_exhalation_duration_sec: audible pre-inhalation exhalation duration in seconds; submit 0 when it is absent.
> inhalation_duration_sec: audible inhalation duration in seconds.
> post_exhalation_duration_sec: audible exhalation duration after inhalation, in seconds.
> inhalation_to_post_gap_sec: time from inhalation end to post-exhalation start, in seconds.
> confidence: probability in [0,1] that both presence flags are correct and all five timing errors satisfy the joint tolerances defined in Evaluation.
> These are acoustic protocol measurements, not a medical diagnosis, disease-severity score, medication recommendation, or assertion that a person used a real drug correctly.
> Generalization Contract
> Complete participants are held out. The fitting rows use four people, the disclosed validation rows use a fifth person, and the hidden rows use two different people. Within an episode, event evidence is kept participant-consistent. Public IDs, paths, and row order are opaque and carry no participant number, recording number, source filename, native event index, target, or chronology code.
> Use split_role=validation only for model selection and calibration. Do not merge it into fitting data while tuning. After choosing a frozen design without consulting hidden outcomes, retraining on all labeled rows is allowed.
> The benchmark deliberately balances the four activation/pre-exhalation presence combinations. Constant yes/no answers, total file duration, ID hashes, or row order therefore do not solve it. All public WAV files have the same duration.
> Intended Approach And Allowed Methods
> Strong solutions should fine-tune an open-source model or build an architecture from scratch. A practical fine-tuning route adapts an open audio encoder such as wav2vec 2.0, HuBERT, WavLM, BEATs, or AudioMAE, keeps time-resolved features, and attaches two presence heads plus five nonnegative timing heads. A practical from-scratch route uses a multi-resolution waveform or log-mel CNN/Conformer with temporal pooling that preserves event order and duration evidence.
> Train with participant-grouped folds, imbalance-safe flag losses, robust timing losses normalized by the disclosed scales, and validation-only calibration. Joint decoding should enforce zero duration for an absent optional event and positive durations for events submitted as present. The complete 48-second waveform matters: cutting the input into isolated source-labeled clips is not part of the public task.
> Open pretrained weights that are downloaded before the offline run are allowed. Runtime internet, hosted inference APIs, closed-source teacher services, external inhaler-event label collections used as answer keys, and external source-recording lookup are not allowed.
> Dataset
> The prepared public tree is:
> | Path                         | Contents |
> |------------------------------|----------|
> | train.csv                    | 212 labeled fitting/validation episodes |
> | test.csv                     | 72 hidden-label episodes |
> | sample_submission.csv        | One weak but schema-valid submission |
> | train/audio/*.wav            | 212 fixed-length labeled WAV files |
> | test/audio/*.wav             | 72 fixed-length hidden WAV files |
> | README.txt                   | Short prepared-data note |
> train.csv columns are:
> | Column                         | Type   | Meaning |
> |--------------------------------|--------|---------|
> | episode_id                     | string | Opaque unique episode key |
> | audio_path                     | string | Public-root-relative WAV path |
> | split_role                     | string | train or validation |
> | participant_group              | string | Opaque group token for grouped validation |
> | activation_present             | string | yes or no |
> | pre_exhalation_present         | string | yes or no |
> | activation_duration_sec        | float  | 0 when absent, otherwise event duration |
> | pre_exhalation_duration_sec    | float  | 0 when absent, otherwise event duration |
> | inhalation_duration_sec        | float  | Inhalation duration |
> | post_exhalation_duration_sec   | float  | Post-inhalation exhalation duration |
> | inhalation_to_post_gap_sec     | float  | Gap from inhalation end to post-exhalation start |
> test.csv contains only the two input columns:
> | Column       | Type   | Meaning |
> |--------------|--------|---------|
> | episode_id   | string | Opaque unique episode key |
> | audio_path   | string | Public-root-relative hidden WAV path |
> No participant group or target appears in test.csv.
> Submission
> Write the final CSV to exactly ./working/submission.csv. It must contain one row for every test episode_id and exactly these nine columns in this order:
> | Order | Column                         | Constraint |
> |------:|--------------------------------|------------|
> | 1     | episode_id                     | Exact hidden ID, once |
> | 2     | activation_present             | yes or no |
> | 3     | pre_exhalation_present         | yes or no |
> | 4     | activation_duration_sec        | Finite number in [0,30] |
> | 5     | pre_exhalation_duration_sec    | Finite number in [0,30] |
> | 6     | inhalation_duration_sec        | Finite number in [0,30] |
> | 7     | post_exhalation_duration_sec   | Finite number in [0,30] |
> | 8     | inhalation_to_post_gap_sec     | Finite number in [0,30] |
> | 9     | confidence                     | Finite number in [0,1] |
> One parseable example row is:
> episode_id,activation_present,pre_exhalation_present,activation_duration_sec,pre_exhalation_duration_sec,inhalation_duration_sec,post_exhalation_duration_sec,inhalation_to_post_gap_sec,confidence
> wia_example000001,yes,no,1.04,0,2.86,1.91,5.20,0.61
> If an optional event is absent, its submitted duration should be at most 0.05. If it is present, its submitted duration should exceed 0.05. The inhalation duration, post-exhalation duration, and inhalation-to-post gap should each exceed 0.05.
> The grader rejects globally invalid files with one generic invalid-submission error. This includes wrong, extra, missing, or reordered columns; duplicate, blank, missing, or extra IDs; illegal enums; nonnumeric, nonfinite, or out-of-range numbers; and submissions outside the row limits. The error does not reveal answers, participant identities, source paths, group membership, weights, or hidden event details.
> Evaluation
> The metric is InhalerProtocolAuditScore, bounded to [0,1]; higher is better. A perfect valid submission scores exactly 1.0.
> For each presence field, compute macro-F1 over the truth labels represented in the evaluated group. For label c, let TP_c, FP_c, and FN_c have their usual one-vs-rest meanings. If TP_c=0, F1_c=0; otherwise precision_c=TP_c/(TP_c+FP_c), recall_c=TP_c/(TP_c+FN_c), and F1_c=2*precision_c*recall_c/(precision_c+recall_c). MacroF1 is the arithmetic mean of F1_c over represented truth labels.
> The five disclosed timing error scales are:
> | Timing field                    | Scale s_j (seconds) |
> |---------------------------------|--------------------:|
> | activation_duration_sec         | 1.127 |
> | pre_exhalation_duration_sec     | 1.348 |
> | inhalation_duration_sec         | 1.536 |
> | post_exhalation_duration_sec    | 0.711 |
> | inhalation_to_post_gap_sec      | 1.995 |
> For row i and timing field j:
> Timing_ij = max(0, 1 - abs(pred_ij - true_ij) / s_j)
> For activation_duration_sec, set Timing_ij=0 whenever the submitted activation-presence flag is wrong. Apply the same rule to pre_exhalation_duration_sec and the submitted pre-exhalation-presence flag. Thus, a zero or median optional-event duration cannot earn timing credit when the event itself is misidentified.
> Timing_i is the arithmetic mean of the five Timing_ij values.
> Joint_i=1 exactly when both presence flags are correct and every timing error is at most s_j/2; otherwise Joint_i=0.
> Calibration_i = 1 - (confidence_i - Joint_i)^2.
> For any evaluated row group G, define:
> Core(G) = 0.10*ActivationMacroF1(G) + 0.15*PreExhalationMacroF1(G) + 0.35*mean_G(Timing_i) + 0.40*mean_G(Joint_i)
> Component(G) = Core(G) * (0.95 + 0.05*mean_G(Calibration_i))
> Calibration cannot create task credit: it only preserves or reduces the earned Core(G) by at most five percent. The largest component is joint audit correctness because the benchmark asks for one coherent protocol assessment, while the flag and timing terms still provide graded partial credit.
> Let P be the set of hidden participant groups. The final score is:
> InhalerProtocolAuditScore = 0.75*Component(all rows) + 0.25*mean_{p in P}(Component(rows from participant p))
> The hidden participant grouping is used only by the grader and is never returned. The participant-macro term prevents a larger participant group from dominating the score. All weights and formulas are shown above; there are no secret tolerance powers or hidden subgroup weights.
> What Not To Use
> Do not use external source-audio search, audio fingerprint matching, recovered source filenames or event annotations, participant re-identification, hosted audio or medical APIs, closed-source teacher services, runtime internet, private files, grader or filesystem exploitation, ID/hash/row-order lookup, manual hidden-set labeling, or hardcoded answer maps. Submissions that ignore the supplied audio and rely on such shortcuts may be rejected before payout even when their CSV parses.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Alopecia Multi-Panel Evidence Grounding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77gqs9dq3ewe6x2k976c3f2d8bjbv9
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> The objective is to match each visible figure panel to its correct evidence
> clause. For every test case, predict panel_sequence: the distinct row-local
> candidate IDs that describe panels A, B, C, and so on, listed in the visible
> panel_order.
> Clinical hair-loss papers often combine photographs, trichoscopy, histology,
> assays, and quantitative plots into one labeled multi-panel figure. During an
> archive migration, the panel-specific evidence clauses were detached from
> their figure.
> The visible image is authentic scholarly material from an alopecia or
> hair-loss article. Its candidate pool contains the true clauses plus clauses
> from two hidden, medically related figures with the same number of panels. All
> candidates are shuffled and their original panel letters are removed. If
> panel_order is A B C D, the first predicted candidate must describe panel
> A, the second panel B, the third panel C, and the fourth panel D.
> This is a joint visual-language grounding task. A valid solution must learn
> from both the figure and candidate text. It is not a diagnosis task and it
> does not ask for medical advice.
> Dataset
> Files
> train.csv - Labeled grounding cases.
> test.csv - Held-out article cases without panel_sequence.
> sample_submission.csv - Random valid sequences in the required format.
> images/ - Re-encoded JPEG figures referenced by image_path.
> The prepared build contains 257 labeled training cases and 215 held-out test
> cases. Test contains every eligible 2026 article plus a deterministic,
> panel-balanced article-level subset from 2025. Training contains the remaining
> 2023-2025 articles. A complete article is assigned to only one partition, so
> articles, figures, images, and caption clauses cannot cross from training into
> test. Perceptual and caption duplicates are removed before splitting.
> The test panel-count distribution for counts 2 through 8 is respectively
> 75, 50, 40, 13, 19, 9, 9. This deliberately reduces the two-panel share from
> 43.4% in the previous test split 50.8% in the full source pool) to 34.9%,
> preventing the highest-chance stratum from dominating the leaderboard while
> retaining every available figure as one visible target.
> Every eligible source figure is the visible target in exactly one case. Within
> the same train or test partition, a figure is also reused as a decoy in exactly
> two other cases. Decoy reuse does not reveal a target: it only contributes
> shuffled alternatives, and no figure, article, image, or caption clause crosses
> from training into test. This target-exclusive, decoy-reusable construction
> increases the evaluation set without duplicating hidden answers.
> Columns
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Opaque case identifier. |
> | image_path | string | Path relative to the public dataset directory. |
> | panel_count | integer | Number of visible panels and required output tokens, from 2 through 8. |
> | panel_order | string | Visible order such as A B C D. |
> | candidate_cards_json | JSON list | Shuffled candidate objects. Each object contains candidate_id and evidence_clause. |
> | answer_format_json | JSON object | Machine-readable output constraint containing field, type, and token_count. |
> | panel_sequence | string; train only | Correct candidate IDs in visible panel order. This column is absent from test.csv. |
> In answer_format_json, field is always panel_sequence, type is always
> space-separated candidate IDs, and token_count equals panel_count. For
> example:
> {"field":"panel_sequence","type":"space-separated candidate IDs","token_count":4}.
> Every case combines three source figures with the same panel_count.
> Therefore, the candidate pool always contains exactly
> 3 * panel_count cards. Exactly one source figure is visible, so exactly
> panel_count cards are correct.
> Panel labels and figure-number references are removed from candidate text.
> Candidate IDs are row-local and independently shuffled. Source PMC IDs,
> article titles, publication years, DOIs, filenames, and target/decoy group
> identities are not released.
> Evaluation
> For one case:
> PanelAccuracy is the fraction of panel positions containing the exact correct candidate.
> AdjacentPairAccuracy is the fraction of true consecutive directed pairs recovered in the predicted sequence.
> SelectedSetF1 is the overlap between the predicted and true candidate sets divided by panel_count. Both sets have the same size, so this is set precision, recall, and F1.
> ExactReconstruction is 1 only when every selected card and its order are correct.
> The four components are calculated for every case and then averaged across all
> cases. Every case therefore has equal weight. Equivalently, each panel-count
> group is weighted by its number of cases; a rare panel count cannot receive the
> same aggregate influence as a large group.
> The hidden answers contain an explicit deterministic visibility assignment.
> The public board contains 53 cases and the private board contains 162 cases.
> Both boards contain every panel count from 2 through 8, and the allocation is
> performed separately inside each panel-count group so their distributions are
> closely matched. A single rare-panel case contributes only 1 / board_size,
> not one-seventh of the final score.
> The final score is:
> Score = 0.55 * mean(PanelAccuracy over cases)
> + 0.20 * mean(AdjacentPairAccuracy over cases)
> + 0.15 * mean(SelectedSetF1 over cases)
> + 0.10 * mean(ExactReconstruction over cases)
> The four components are calculated independently. The score is bounded from
> 0 through 1, and higher is better.
> Submission
> Submit a UTF-8 CSV with exactly these columns in this order:
> case_id,panel_sequence
> ALOCASE_0123456789abcdef01,CARD_04 CARD_10 CARD_01
> ALOCASE_fedcba9876543210ab,CARD_07 CARD_00 CARD_12 CARD_03
> Requirements:
> Include every test case_id exactly once.
> Do not include missing, duplicate, or unknown IDs.
> Use exactly panel_count space-separated candidate IDs per row.
> Candidate IDs must come from that row's candidate_cards_json.
> Candidate IDs may not repeat within a row.
> Do not add columns.
> Compute And Modeling Requirements
> The compute tier is one NVIDIA A10G GPU, up to 10 CPU cores, and 62 GB RAM.
> The complete solution must finish within 1.5 hours.
> Predictions must come from a joint image-text model fitted or fine-tuned on the provided training cases.
> Generic open-weight pretrained vision or vision-language initialization is permitted.
> The model must use the visible image and candidate evidence text in its effective prediction path.
> Constrained or assignment-based decoding is permitted and encouraged.
> Prohibited
> Closed or hosted model APIs.
> External alopecia, trichoscopy, dermatology, or biomedical figure datasets.
> Challenge-specific pretrained checkpoints or externally pseudo-labeled training examples.
> Searching PMC, the web, article archives, DOIs, captions, or source figures to recover test mappings.
> Matching released text or images against cached copies of the source articles.
> Text-only retrieval, TF-IDF-only, OCR-only, image-only, candidate-position, candidate-length, or fixed-rule systems as the primary solution.
> Reconstructing source PMC IDs, titles, years, filenames, or article groups.
> Hardcoded test IDs, row-order rules, answer maps, private files, grader exploitation, or filesystem side channels.
> Expected Output
> Your script receives the public dataset directory and exact submission CSV
> path as two positional arguments:
> python3 [solution.py](http://solution.py) <public_dir> <submission_out>
> Submissions
> 25

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Three-Step Theorem Context Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74e64sxs9t5216c7952s8rr18bress
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: ↑ Higher is better

Full challenge description from page:

> Overview
> For each case, predict which six declarations should be loaded for three consecutive Lean proof steps. Then identify the declarations directly required at each step.
> Lean is an interactive theorem prover in which a proof state contains the current hypotheses and goal. A declaration is a previously verified theorem, definition, or lemma that may support the next proof operation. Each example is constructed from recorded formal proof traces and reviewed declaration text. It contains three chronological proof states and twelve candidate declaration cards. Names are replaced with packet-local aliases, but theorem types and references remain internally consistent.
> Every case therefore requires two outputs:
> | Output | Prediction |
> |---|---|
> | `context_pack` | Six distinct declaration slots, ordered by how urgently they are needed across the three proof stages. |
> | `proof_horizon_program` | The direct support set for stage 0, stage 1, and stage 2. |
> This models context preparation for an interactive theorem prover. Retrieving premises independently before every tactic is expensive, while loading too many declarations wastes a model's limited context window. The prediction must therefore cover the complete three-step horizon while distinguishing immediate support from declarations needed later.
> The task is not ordinary next-premise ranking. One selected support declaration is partially erased, declarations can be reused at multiple stages, and same-file or same-namespace declarations act as hard distractors. The hidden split uses the source benchmark's novel-premise regime, so declarations serving as hidden evaluation targets are not reused as training targets.
> What Makes This Interesting
> The prediction unit is a three-step retrieval plan rather than one theorem-query pair. A declaration useful at stage 2 still belongs in the limited context pack, but it should rank below a declaration required immediately. A declaration reused across stages should be retained even when another card looks more similar to one individual state.
> All identifiers are replaced with packet-local aliases. The same original identifier receives different aliases in different cases, while references remain consistent inside one packet. This preserves formal relationships without allowing a global theorem-name lookup table. Strong solutions must compare types, hypotheses, goals, and declaration structure across all three states.
> The dataset contains 4,000 training cases and 700 hidden cases. This supports fine-tuning a compact code model, theorem encoder, or cross-encoder that scores declarations jointly against the proof horizon.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 4,000 labeled three-stage context-packing cases. |
> | `test.csv` | 700 cases containing public inputs only. |
> | `sample_submission.csv` | A schema-valid baseline submission for every hidden ID. |
> | `retrieval_packets/` | JSON packets containing three anonymized proof states and twelve candidate declaration cards. |
> train.csv contains the three input columns and both targets. test.csv contains only the input columns.
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque key used to align submission rows. |
> | `retrieval_packet_path` | string | train and test | Relative path to one JSON packet. |
> | `context_budget` | string | train and test | Declares the six-card budget, three-stage horizon, and support-card erasure condition. It contains no answer. |
> | `context_pack` | ordered token string | train only | Six distinct slot tokens joined by `>`. |
> | `proof_horizon_program` | structured token string | train only | Three ordered stage clauses containing the direct support slots. |
> Retrieval Packet Fields
> | Field | Data type | Description |
> |---|---|---|
> | `horizon_states` | array of three strings | Proof states in chronological order, starting with the state before stage 0. |
> | `candidate_cards` | array of twelve objects | Candidate declarations. Each object contains a `slot` and an anonymized `declaration`. |
> | `context_limit` | integer | Number of cards permitted in `context_pack`. Always `6`. |
> | `horizon_length` | integer | Number of proof stages. Always `3`. |
> | `card_count` | integer | Number of candidate cards. Always `12`. |
> Slots are named p01 through p12. Two cards begin with <erased-declaration> and retain only their ending fragments. Exactly one is used somewhere in the three-stage horizon and the other is a distractor, so the marker does not reveal which erased card is useful or at which stage.
> Output Grammar
> context_pack contains exactly six distinct slot tokens separated by >. A valid example is p04>p09>p02>p11>p06>p01.
> proof_horizon_program contains exactly three stage clauses separated by >, in chronological order. Inside each clause, slot tokens are separated by |. A valid example is s0[p04|p09]>s1[p02]>s2[p06|p11].
> Each stage contains between one and four distinct slots. Slots inside a stage are serialized in ascending order. A declaration used at more than one stage appears in every applicable clause.
> The hidden context-pack urgency of a slot is its earliest support stage. Stage-0 support has gain 7, stage-1 support has gain 3, and stage-2 support has gain 1. Cards not used in the horizon have gain 0.
> Evaluation
> Minimum score: 0.0
> Maximum score: 1.0
> The metric is the Proof Horizon Packing Score.
> Score = 0.25 * ContextPackNDCG + 0.35 * StageSupportF1 + 0.40 * ExactHorizonRate
> Higher is better. The minimum possible score is 0.0, and the maximum possible score is 1.0.
> ContextPackNDCG
> The submitted pack must contain six distinct valid slots. Let g_k be the hidden urgency gain of the slot submitted at one-based rank k.
> DCG@6 = sum(g_k / log2(k + 1)) for k = 1, ..., 6.
> IDCG@6 is the same sum after sorting all hidden urgency gains from largest to smallest and retaining the first six.
> The case score is DCG@6 / IDCG@6.
> ContextPackNDCG is the arithmetic mean of the case scores.
> Repeated use of a declaration does not duplicate it in the pack. Its earliest stage determines its gain. Equal-gain cards may appear in any order without changing the score. An invalid pack receives zero for that case.
> StageSupportF1
> For stage t, let T_t be the true support set and P_t be the submitted support set.
> precision_t = |T_t intersection P_t| / |P_t|.
> recall_t = |T_t intersection P_t| / |T_t|.
> Equivalently, F1_t = 2 * |T_t intersection P_t| / (|T_t| + |P_t|).
> The case score is (F1_0 + F1_1 + F1_2) / 3.
> StageSupportF1 is the arithmetic mean of the case scores.
> A stage with no overlap receives zero. A malformed horizon program receives zero for the complete case.
> ExactHorizonRate
> For each case, the parsed program is exact only when all three submitted support sets equal their corresponding hidden sets. ExactHorizonRate = number of exact three-stage programs / number of test cases.
> Slot order inside a stage does not affect parsed equality, although ascending serialization is required for canonical submissions.
> Submission Format
> Write the final CSV to exactly ./working/submission.csv.
> It must contain exactly three columns in this order: case_id, context_pack, proof_horizon_program.
> Example rows:
> | case_id | context_pack | proof_horizon_program |
> |---|---|---|
> | `pm_6bd90a14f7c2e11a3b` | `p04>p09>p02>p11>p06>p01` | `s0[p04\|p09]>s1[p02]>s2[p06\|p11]` |
> | `pm_9a142e70c55831df2441` | `p03>p07>p01>p12>p05>p10` | `s0[p03]>s1[p01\|p07]>s2[p05\|p12]` |
> | `pm_c84216ba7f0e219d6a53` | `p02>p08>p10>p04>p06>p11` | `s0[p02\|p08]>s1[p10]>s2[p04\|p06]` |
> context_pack is limited to 32 characters. proof_horizon_program is limited to 96 characters. Missing rows, extra rows, duplicate IDs, unknown IDs, duplicate columns, reordered columns, and extra columns are rejected. The optional backend-managed visibility column is removed before exact schema validation.
> Expected Methods
> Suitable systems include a fine-tuned code encoder, a shared theorem-state and declaration encoder, a cross-encoder over each state-card pair, or a set transformer that reasons over the full packet. Multi-stage contrastive learning, hard-negative mining, and structured decoding are allowed. The model must train from the supplied public training cases and run locally at inference time.
> What Not To Use
> Do not infer outputs from case IDs, packet filenames, row order, hashes, or source ordering.
> Do not reverse-search anonymized proof text against external theorem repositories to recover recorded traces.
> Do not use an external theorem index containing hidden evaluation declarations or proof steps.
> Do not exploit malformed programs, duplicate rows, column reordering, or grader behavior.
> Do not train, calibrate, or select outputs using hidden labels or grader feedback.
> Local open-weight code and theorem models are allowed. Hosted inference APIs are not allowed.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Magnetic Microscopy Encoder Adaptation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b5xmafa2arm5n6ea9erngbd8bq739
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.539

Full challenge description from page:

> Overview
> Fine-tune a pretrained encoder on labeled magnetic microscopy boards, then use the adapted model to predict how four local interventions change magnetic-domain connectivity. Each board contains one low-contrast microscope field and four circular windows labeled A through D. For each window, the material inside the circle is hypothetically neutralized while the rest of the field remains unchanged.
> The model must return three connected predictions: a topology-change tensor for the four windows, four bridge-retention decisions, and the field's original texture regime. This is an encoder-adaptation problem because representations learned from ordinary photographs do not directly capture faint magnetic filaments, enclosed loops, or continuity across a proposed intervention boundary. The labeled training boards provide the evidence needed to update that representation for the scientific acquisition domain.
> In magnetic-device research, a local material defect or a deliberately neutralized region can split a connected texture, close a loop, or remove an isolated domain. Screening those effects before a costly follow-up experiment requires learning both local continuity and field-level structure. Evaluation uses microscope fields from held-out acquisition groups, so success depends on transferring the fine-tuned representation to unfamiliar textures rather than memorizing individual source fields.
> The three predictions are:
> | Output | What it represents |
> |---|---|
> | `topology_tensor` | Four topology-delta records, one for each intervention window. |
> | `bridge_indicator_vector` | Whether each window cuts through a component that continues beyond the circle. |
> | `texture_state` | The global topology regime before any intervention. |
> Adaptation Objective
> The supplied training set is the only labeled target-domain adaptation set. A suitable solution begins with a locally available open-weight pretrained encoder, updates encoder parameters on these boards, and learns structured prediction heads for the tensor, bridge vector, and texture state. All three outputs are evaluated together because a useful adapted representation must support intervention-level topology and whole-field interpretation at the same time.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Labeled microscope boards with input and target columns. |
> | `test.csv` | Hidden-evaluation microscope boards with input columns only. |
> | `sample_submission.csv` | A schema-valid baseline submission. |
> | `images/` | Opaque JPEG microscope boards referenced by the CSV files. |
> Every board is an 820 by 720 RGB JPEG. The original microscope field appears against a dark framing band. Four intervention circles are labeled A, B, C, and D. Circle colors distinguish proposal identity only; they do not encode the answer.
> Prepared Data Summary
> | Quantity | Value |
> |---|---:|
> | Training rows | 2,365 |
> | Test rows | 595 |
> | Training `filament_network` | 647 |
> | Training `isolated_domains` | 730 |
> | Training `mixed_texture` | 523 |
> | Training `sparse_texture` | 465 |
> | Test `filament_network` | 159 |
> | Test `isolated_domains` | 165 |
> | Test `mixed_texture` | 145 |
> | Test `sparse_texture` | 126 |
> The split is grouped by acquisition source. All microscope fields from one source remain on one side of the split. There are no duplicate board bytes across or within the two splits.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | String | Opaque unique case identifier. |
> | `microscopy_board_path` | String | Relative path to one JPEG board under `images/`. |
> | `intervention_contract` | String | Fixed instruction defining the counterfactual neutralization operation and tensor column order. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `topology_tensor` | JSON integer matrix, shape 4 by 4 | Rows A-D. Columns are connected-component delta, enclosed-hole delta, isolated-domain delta, and defect-contact delta. Every entry is clipped to the integer range -2 through 2. A delta is `after - before`. |
> | `bridge_indicator_vector` | JSON integer vector, length 4 | Entries for A-D. `1` means the window intersects a connected magnetic component that also continues outside the circle; `0` means it contains only background or complete isolated components. |
> | `texture_state` | Categorical string | One of `filament_network`, `isolated_domains`, `mixed_texture`, or `sparse_texture`. |
> sparse_texture has little magnetic foreground. isolated_domains contains many separated compact regions. filament_network is dominated by connected or loop-forming texture. mixed_texture contains substantial foreground without one of those regimes dominating.
> An example labeled target is:
> topology_tensor = [[1,0,0,0],[0,-1,-1,0],[0,0,0,0],[2,0,1,-1]]
> bridge_indicator_vector = [1,0,0,1]
> texture_state = filament_network
> Evaluation
> The Magnetic Intervention Topology Score has three components:
> Score = 0.55 * TopologyScore
> + 0.30 * BridgeScore
> + 0.15 * TextureStateScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> TopologyScore
> For one sample, let Y be the hidden 4 by 4 tensor and P the submitted tensor. Entry weights are determined by the hidden truth:
> w[i,j] = 2.5 if Y[i,j] != 0, otherwise 1.0
> weighted_agreement = sum(w[i,j] * I(Y[i,j] = P[i,j])) / sum(w[i,j])
> sample_topology = 0.34 * weighted_agreement + 0.66 * I(Y = P)
> TopologyScore is the mean sample_topology over hidden samples. Malformed tensors receive 0.0 for this component.
> BridgeScore
> For the length-4 bridge vector, the same formula is used with weight 2.0 on hidden entries equal to 1, weight 1.0 on hidden entries equal to 0, and exact-vector weight 0.66. BridgeScore is the mean sample score.
> TextureStateScore
> For each texture state present in the hidden answers, recall is the fraction of rows in that state predicted correctly. TextureStateScore is the unweighted mean of those recalls. An invalid state is incorrect.
> Submission Format
> Write the final CSV to exactly:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,topology_tensor,bridge_indicator_vector,texture_state
> All matrix and vector fields are JSON strings. A valid row is:
> case_id,topology_tensor,bridge_indicator_vector,texture_state
> mt2a41db46c2a76de9fd91,"[[1,0,0,0],[0,-1,-1,0],[0,0,0,0],[2,0,1,-1]]","[1,0,0,1]",filament_network
> The grader rejects reordered or extra columns, duplicate IDs, missing or unknown IDs, and row-count mismatches. The platform may add one backend-managed visibility column; the grader removes only that column. A tensor or vector longer than 220 characters, incorrectly shaped JSON, non-integer entries, or out-of-range values receives zero for its component.
> Method Requirements
> Predictions must come from a pretrained open-weight encoder whose parameters are fine-tuned on the supplied training examples. The resulting checkpoint must use the microscope pixels and proposal geometry jointly to produce all three structured outputs. Auxiliary losses, parameter-efficient adapters, multi-task heads, and image augmentations are allowed when they are fitted only on the public training split.
> Frozen zero-shot inference, handcrafted image statistics as the primary predictor, and a separately fitted lookup model do not satisfy the adaptation objective. Hosted model APIs are not allowed at inference time. The A10G runtime is provided for target-domain parameter updates and batched checkpoint inference.
> What Not To Use
> Do not map case_id, row order, file names, file sizes, hashes, or path strings directly to targets.
> Do not search for or match boards against external copies of the source imagery or annotations.
> Do not reconstruct hidden labels from source record identifiers, archive ordering, or cached public mirrors.
> Do not use manually authored lookup tables keyed by image fingerprints or proposal coordinates.
> Do not modify, probe, or exploit grader behavior, duplicate handling, malformed values, or submission ordering.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Which Mutation Breaks the Protein

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c7ebxj7z54a8cs643sxm12x8bp6jm
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.439

Full challenge description from page:

> Which Mutation Breaks the Protein
> Overview
> A protein is a chain of amino acids. Change one of them and the protein may keep working
> perfectly, work a little worse, or stop working altogether. Which of those happens depends on
> where in the chain the change falls and what it is changed to — a residue buried in the core
> tolerates almost nothing, while a residue on the surface often tolerates almost anything.
> You are given a protein and two single-residue variants of it. Exactly one of the two damages
> the protein's function more. Say which.
> The proteins in the test set are ones you have never seen. You cannot learn a particular
> protein's soft spots and reuse them; you have to learn what makes a substitution damaging in
> general, and carry that to a protein you have not met.
> What makes this hard
> The standard way to judge a mutation without any training data is to ask a pretrained protein
> language model how surprising it finds the substitution — a mutation the model considers
> unlikely is assumed to be damaging. It is a strong method, and on ordinary variant data it works
> well.
> It will not help you here. The pairs in this dataset are chosen in balanced halves: for every
> pair the zero-shot likelihood ranks correctly, another is included where it ranks the pair
> backwards. Across the released rows that method is exactly at chance and carries no
> information at all. Substitution heuristics cannot help either, and not merely by a little: the
> two variants in a row are the same substitution — the same wild-type residue replaced by the
> same amino acid — at two different positions. Hydropathy shift, substitution-matrix score, volume
> and charge change are therefore identical between the two options. Ranking by hydropathy scores
> 0.00. Ranking by position in the chain scores 0.03.
> What is left has to be learned from the training proteins by fine-tuning.
> Task
> For every row in test.csv, output 0 if the first variant is the more damaging of the two,
> or 1 if the second is.
> Files
> You are given four files.
> train.csv
> One row per variant pair from the training proteins. Columns:
> id (string) — unique identifier for this pair.
> protein_id (string) — identifier of the protein both variants belong to. Join to
> proteins.csv on this key.
> a_pos (integer) — position of the first variant's substitution, counting from 1 at the start
> of the protein sequence.
> a_wt (string) — the single-letter amino acid found at that position in the unmutated protein.
> a_mut (string) — the single-letter amino acid it is changed to.
> b_pos, b_wt, b_mut — the same three fields for the second variant. The two variants are
> always at different positions.
> label (integer) — 0 if the first variant is more damaging, 1 if the second is. This is
> the training signal.
> test.csv
> One row per variant pair from the held-out proteins. Same columns as train.csv except there is
> no label column — that is what your model must predict. Columns: id, protein_id, a_pos,
> a_wt, a_mut, b_pos, b_wt, b_mut.
> proteins.csv
> One row per protein, covering every protein_id in both train.csv and test.csv. Columns:
> protein_id (string) — protein identifier.
> sequence (string) — the unmutated amino-acid sequence, in single-letter code. Positions in
> a_pos and b_pos index into this sequence starting at 1, and the letter there always matches
> a_wt / b_wt.
> sample_submission.csv
> A valid submission in the exact required format, with a placeholder answer for every test id.
> It calls the variant nearer the start of the chain the more damaging one — a crude rule that uses
> no training data and scores about 0.03. Columns: id, prediction.
> Submission format
> Produce a CSV with exactly two columns, id and prediction, containing every id in
> test.csv exactly once and no others. prediction is 0 or 1. Missing ids, extra ids,
> duplicate ids, or values outside {0, 1} cause the submission to be rejected.
> Evaluation metric
> Accuracy, rescaled so that guessing maps to zero.
> The two variants are presented in random order and the pairs are balanced, so a coin flip scores
> 50%. The reported score is
> accuracy = fraction of test rows answered correctly
> score    = clip((accuracy - 0.5) / 0.5, 0, 1)
> Chance maps to 0 and a perfect answer maps to 1. Higher is better.
> For orientation: a zero-shot protein language model scores 0.00, ranking by hydropathy change
> scores 0.00, and ranking by position in the chain scores 0.03.
> Method rules (required)
> This is a representation-learning / fine-tuning challenge. Your predictive model must learn a
> representation of the protein by fine-tuning a neural network.
> Allowed:
> Fine-tuning a pretrained neural protein encoder — for example a protein language model over the
> amino-acid sequence — together with a neural head that turns a position and a substitution into
> a damage score.
> Any neural architecture, loss (pointwise, pairwise, or listwise), and training schedule, as long
> as the protein representation is learned by the network.
> Downloading pretrained neural weights is expected and allowed.
> Not allowed:
> Gradient-boosted decision trees, random forests, or any tree ensemble (including XGBoost,
> LightGBM, CatBoost, and scikit-learn's tree/forest/boosting models) as the predictive model.
> Linear/logistic regression, SVM, k-NN or similar classical models trained on hand-crafted
> features — substitution matrices such as BLOSUM or PAM, amino-acid property tables, conservation
> scores, or precomputed embeddings used as a fixed feature table — as the predictive model. The
> protein representation must be learned by the network, not hand-engineered and handed to a
> classical estimator.
> Using external variant-effect measurements, or looking up the effect of these variants or
> proteins from any outside source. Every prediction must come from your model trained on the
> provided training data.
> Identifying the source proteins in order to retrieve their published mutational data.
> Your full solution — training and inference over the whole test set — must complete within the
> provided compute and time budget, so prefer efficient fine-tuning.
> Notes
> The split holds out entire proteins: no protein in the test rows appears in the training rows.
> Build your validation split the same way — hold out whole proteins, not random rows — or you will
> badly overestimate your score, because many rows share a protein.
> Both variants in a row belong to the same protein, so a model that scores each variant
> independently and compares the two scores is a reasonable starting point. The two variants are
> never at the same position.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Seismic Self-Supervised: Learning from the Unlabeled Earth

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74z1nxev73tm8a5atjaj0dcn8bm6zv
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> The Earth's subsurface is the ultimate unlabeled dataset. Vast 3D seismic surveys cover thousands of square kilometers, but expert geological labels — painstakingly annotated by human geoscientists — exist for only a tiny fraction of the data. This is not a data problem; it's the fundamental asymmetry of geoscience: unlabeled data is abundant, labels are scarce and expensive.
>
> You are given a real 3D seismic survey from an offshore basin: ~495,000 seismic traces for self-supervised pre-training — of which only 1,000 come with expert labels for fine-tuning. Each raw trace is a 462-sample 1D time series of acoustic impedance contrasts; the prepared tables retain 450 informative time samples after integrity preprocessing. Your task is to design a self-supervised learning approach that extracts geologically meaningful representations from the unlabeled waveforms, then fine-tunes on the tiny labeled set to classify traces into 10 geological facies classes.
>
> This is NOT a standard classification problem. A supervised model trained on 1,000 examples will overfit catastrophically. You must design a pre-training objective — masked trace modeling, contrastive learning, next-trace prediction, jigsaw puzzling, or something entirely novel — that teaches your model the structure of seismic signals before it ever sees a label. The quality of your self-supervised representations determines everything.
>
> No pretrained models, no transfer learning from ImageNet or audio benchmarks. Your architecture must learn the "language" of seismic reflections from scratch, using only the provided unlabeled traces.
>
> Evaluation
>
> Submissions are scored using macro-averaged F1 across the 8 facies classes with sufficient test representation for stable evaluation.
>
> Classes 1 (Chalk Group) and 3 (Scruff Greensand) are excluded from the metric: Class 1 has zero samples anywhere in this survey slice; Class 3 has too few test samples (<5) for a single prediction to carry meaningful weight. The theoretical maximum score is 1.0.
>
> def macro_f1(y_true, y_pred, active_classes):  
>     f1_scores = []  
>     for cls in active_classes:  
>         tp = ((y_pred == cls) & (y_true == cls)).sum()  
>         fp = ((y_pred == cls) & (y_true != cls)).sum()  
>         fn = ((y_pred != cls) & (y_true == cls)).sum()  
>         precision = tp / max(tp + fp, 1)  
>         recall = tp / max(tp + fn, 1)  
>         f1 = 2 * precision * recall / max(precision + recall, 1e-9)  
>         f1_scores.append(f1)  
>     return mean(f1_scores)  
>
> Final score = macro F1 over 8 active classes (0, 2, 4, 5, 6, 7, 8, 9). Range: [0, 1].
>
> Dataset
>
> The dataset is a 3D seismic survey volume: 951 crossline sections × 651 inline positions, yielding 619,101 individual seismic traces. Each raw trace is a 462-sample 1D time series (~1.8 seconds two-way travel time), with 450 non-degenerate samples retained in the prepared CSVs. The data is split spatially into ~495,000 training traces (spanning the first ~80% of crosslines as a contiguous block) and ~124,000 test traces (spanning the remaining ~20% as a separate contiguous geographic region).
>
> Within the training pool, only 1,000 traces carry labels (train_labeled.csv is a subset of train.csv). The remaining ~494,000 training traces are unlabeled — you must design a self-supervised objective to learn from them.
>
> Phase 1: Self-Supervised Pre-training — public/train.csv
>
> ~495,000 traces WITHOUT labels. This is your pre-training corpus.
>
> Column	Type	Description
> trace_id	str	Opaque trace identifier (randomly assigned, does not encode position)
> amp_0012 … amp_0461	float	Seismic amplitude at each of 450 retained time samples
>
> No facies_class, no facies_name, and no spatial coordinates. These are pure waveforms stripped of location metadata — you decide what self-supervised objective to train on them.
>
> Amplitude values are conservatively winsorized per time sample using 3×IQR
> fences fitted on the training split only. The same fixed fences are applied to
> the labeled subset and test split. Twelve zero-IQR samples (amp_0000 through
> amp_0011) are omitted consistently because clipping would make them constant;
> no rows or trace IDs are removed.
>
> Design your SSL objective here. Ideas (not exhaustive):
>
> Masked trace modeling: Randomly mask segments of the waveform and learn to reconstruct them
> Contrastive learning: Learn augmentations of the same trace to have similar embeddings, different traces to be far apart
> Spatial proximity: Neighboring traces in the survey share geological context — use spatial relationships as a self-supervisory signal
> Temporal shuffling: Shuffle time windows and predict the correct ordering
> Next-trace prediction: Given a sequence of neighboring traces, predict the next one
> Jigsaw: Divide the trace into chunks, shuffle them, and predict the correct permutation
>
> Critical considerations for seismic SSL:
>
> Neighboring traces ARE genuinely similar (same geology) — naive contrastive learning that treats nearby traces as negatives creates false repulsion. How do you handle this?
> Seismic amplitudes have structured frequency content — random augmentations that destroy the frequency spectrum (e.g., aggressive noise) may be counterproductive
> The 450 retained time samples are NOT independent — they form a continuous waveform with causal structure (deeper = older rocks)
> Phase 2: Few-Shot Fine-tuning — public/train_labeled.csv
>
> 1,000 traces WITH expert geological labels. Fine-tune your pre-trained encoder here.
>
> Column	Type	Description
> trace_id	str	Opaque trace identifier (randomly assigned, does not encode position)
> amp_0012 … amp_0461	float	Seismic amplitude at each retained time sample
> facies_class	int	Ground truth facies (0-9)
> facies_name	str	Human-readable facies name
>
> The labeled set is small (0.2% of the training pool) and class-imbalanced — common facies like Rijnland Group (class 2) have hundreds of examples, while rare facies like Scruff Greensand (class 3) may have only a handful. Your fine-tuning strategy must handle this scarcity.
>
> Phase 3: Inference — public/test.csv
>
> ~124,000 traces from unseen crossline sections. Predict facies_class for every trace.
>
> Same columns as train.csv (features only, no labels).
>
> Facies Classes
> ID	Facies	Geological Description	Labeled Set (typ.)
> 0	Upper North Sea Group	Pleistocene-Holocene unconsolidated sediments	~7
> 1	Chalk Group	Upper Cretaceous carbonates	excluded (0, absent from survey)
> 2	Rijnland Group	Lower Cretaceous clastic sediments	~330
> 3	Scruff Greensand	Lower Cretaceous greensand	excluded (<5 test samples)
> 4	Lower Chalk Group	Lower Cretaceous carbonates	~16
> 5	Scruff	Jurassic-Lower Cretaceous sediments	~97
> 6	Zechstein Group	Permian evaporites and carbonates	~95
> 7	Rotliegendes	Permian aeolian/fluvial sandstones	~9
> 8	Carboniferous	Carboniferous coal-bearing sediments	~264
> 9	Basement	Pre-Carboniferous basement rocks	~176
>
> Classes 1 and 3 are excluded from macro F1 scoring. Class 1 is absent from this survey slice. Class 3 has insufficient test samples for stable per-class evaluation — a single trace cannot carry meaningful weight in a macro average. Contestants must still predict a class label (0-9) for every test trace; the grader simply omits these two classes when computing the average.
>
> Class 1 (Chalk Group) does not appear in this survey slice — the geological layer is not present at this depth range. Class 3 (Scruff Greensand) is present but extremely rare: a single test trace cannot produce a stable per-class F1, so it is also excluded. The class IDs are reserved but excluded from macro F1 scoring.
>
> Submission
>
> Submit a CSV file with exactly one row per test trace:
>
> Column	Type	Description
> trace_id	str	Trace identifier (matches test.csv)
> facies_class	int	Predicted facies class (0-9)
>
> Requirements:
>
> Must contain exactly one row per test trace (see sample_submission.csv)
> Include a header row
> facies_class must be integers 0-9 — no floats, no strings, no missing values
>
> Example of a correctly formatted submission:
>
> trace_id,facies_class  
> trace_004827,2  
> trace_591034,8  
> trace_210945,5  
> trace_376102,9  
> trace_000153,6  
>
> Each trace_id must match an entry in test.csv. facies_class must be a single integer 0-9 per row.
>
> Key Challenges
> 1. Self-Supervised Objective Design
>
> This is the core challenge. You must invent or adapt a self-supervised learning objective that works for 1D geophysical waveforms. Standard vision SSL methods (SimCLR, MoCo, BYOL, MAE) were designed for natural images with very different statistical properties. Seismic traces are:
>
> 1D time series with causal structure (not 2D images)
> Smooth and continuous (not discrete objects)
> Spatially correlated (neighboring traces share geology — a challenge for contrastive methods)
> Spectrally structured (frequency content matters more than raw amplitude)
>
> Your SSL objective must produce representations that capture geologically relevant features: reflection amplitudes, layer thicknesses, impedance contrasts, and stratigraphic boundaries.
>
> 2. Representation Quality with Minimal Supervision
>
> With only 1,000 labeled traces (~0.2% of the training data), your fine-tuning phase has very limited signal. Representations learned during pre-training must be so good that a simple classifier can separate facies classes with very few examples. The gap between "good SSL representations" and "good SSL representations for geology" is where this challenge lives.
>
> 3. Extreme Class Imbalance in Fine-tuning
>
> The labeled set reflects the natural geological distribution: common facies dominate, rare facies barely appear. With only ~5 labeled examples of Scruff Greensand (class 3), standard cross-entropy training will ignore it entirely. Your fine-tuning strategy — loss weighting, oversampling, meta-learning, prototypical networks — must actively counteract this.
>
> 4. Spatial Generalization
>
> Train and test traces come from contiguous but geographically separated regions of the survey (contiguous crossline block split, no shuffling). Geological layer thicknesses, amplitudes, and facies distributions vary across regions due to subsurface structure. Your model must learn signal features that transfer across this spatial domain shift — without ever seeing spatial coordinates.
>
> 5. Avoiding Shortcut Learning in SSL
>
> Self-supervised objectives are notorious for discovering shortcuts. In seismic data, obvious shortcuts include:
>
> Trace energy (total amplitude power) correlates with facies but is not fully discriminative
> Amplitude range varies across the survey due to acquisition effects — a model that relies on raw amplitude scale will fail on traces with different gain
> Temporal smoothness — neighboring time samples are highly correlated; an SSL objective that exploits only local smoothness learns trivial features
>
> Note: trace IDs are randomly assigned and carry no positional information — there is no spatial shortcut to exploit.
>
> Constraints
> From Scratch ONLY: No pretrained models, weights, or embeddings. Train from random initialization on the provided data only.
> No external data: Use only the provided dataset files (train.csv, train_labeled.csv, test.csv).
> Recommended Approach
> Design your SSL objective (most important decision). Consider what makes two traces "similar" geologically. Prototype on a small subset first.
> Build an efficient encoder. 1D CNNs (TCN, ResNet-1D), transformers, or hybrid architectures. The encoder must be fast enough to process 495K traces within your pre-training budget.
> Pre-train on train.csv. Use all ~495K unlabeled traces. Monitor your SSL loss — but remember that low SSL loss does not guarantee good downstream performance.
> Fine-tune on train_labeled.csv. Freeze early layers, use class weights or oversampling for imbalance, apply strong regularization.
> Validate carefully. With only 1,000 labeled traces, you cannot afford a large validation set. Consider leave-one-crossline-out or stratified k-fold within the labeled set.
> Predict on test.csv and submit.
> Submissions
> 0
> Top Score
> —
> Created
> Aug 1, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Piano Pedal Changes During Sensor Blackout

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b9gad7vsxs246cgb5najfcx8dw95c
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat crocx's score of 0.119!

Full challenge description from page:

> Background Piano sustain pedals are vital for shaping musical phrasing, resonance, and articulation. High-resolution sensors can accurately capture pedal trajectories during performances. However, sensor dropouts, transmission failures, or mechanical clipping occasionally produce blackout intervals. Accurately recovering a pianist's categorical pedalling technique (e.g., quarter, half, full pedal) during these blackouts is critical for high-fidelity performance reconstruction and analysis. Because the sustain pedal profoundly affects acoustic resonance and note releases, the simultaneous audio signal contains latent, identifiable evidence of the missing pedal movements. Overview Reconstruct the sequence of categorical sustain-pedal changes during a missing sensor interval. The architecture receives four seconds of real piano audio, the pedal trace for the first 1.5 seconds, and the last known categorical pedal state. The objective is to recover every subsequent state change over the remaining 2.5 seconds. The audio remains available through most of the blackout, providing acoustic evidence from resonance, releases, and new notes. The target is the native sequence of pedalling categories, not continuous pedal depth or note transcription. The predictor must identify when each change occurred and which category followed it. This challenge requires you to fine-tune a permitted general pretrained backbone using the training data, with actual updates to pretrained parameters. The complete offline execution has a 90-minute limit on one NVIDIA A10G, including cached-weight loading, adaptation, and inference. Dataset Information (Public Files) There are 471 training windows and 403 evaluation windows, drawn from five training passages and five held-out passages. Overlapping windows from a single recording remain strictly in the same partition, and all evaluation passages belong to one held-out work family (Chopin Op. 28). These counts represent localized windows, not independent performers or instruments. Audio files are four-second mono FLAC at 16 kHz. Sensor NPZ files contain 200 bins of 20 ms each. +-----------------------+--------------------------------------------------------------+ | File / Directory | Description | +-----------------------+--------------------------------------------------------------+ | train/ | FLAC audio and NPZ sensor arrays for training windows. | | test/ | FLAC audio and NPZ sensor arrays for evaluation windows. | | cases.json | Master list of all windows, splits, and metadata. | | train.csv | Training command sequences. | | sample_submission.csv | Evaluation IDs and format examples. | +-----------------------+--------------------------------------------------------------+ Feature Schema (cases.json) +--------------------+---------+-------------------------------------------------------+ | Field | Type | Meaning | +--------------------+---------+-------------------------------------------------------+ | id | String | Opaque window ID | | split | String | train or test | | audio | String | Relative FLAC path | | sensors | String | Relative NPZ path | | recording_group | String | Opaque passage recording key | | sample_rate_hz | Integer | 16,000 | | bin_ms | Integer | 20 | | blackout_start_bin | Integer | 75 (equivalent to 1.5 seconds) | | hidden_bins | Integer | 125 (equivalent to 2.5 seconds) | | last_known_state | Integer | State 0-4 at the final pre-blackout bin | | audio_delay_bins | Integer | 2, 3, or 4 terminal audio bins withheld | +--------------------+---------+-------------------------------------------------------+ NPZ Array Details The sensor NPZ contains three arrays: pedal_prefix: float16 [200] pedal_available: uint8 [200] audio_available: uint8 [200] Pedal measurements are native trace-bin means normalized by clipping (value-200)/300 to [0, 1]. Only the first 75 bins may be observed. The prefix has Gaussian noise with standard deviation 0.005, step-1/64 quantization, and one masked three-bin block. The blackout occupies bins 75–199. Unavailable trace values are explicitly set to zero. Audio features Gaussian noise at 2% of the window RMS, step-1/4096 amplitude quantization, a masked 60 ms block, and 40/60/80 ms of terminal observation latency. Availability arrays distinguish withheld data from observed zero values. No pedal samples from the blackout are provided. The native categories are: 0 (no pedalling), 1 (quarter), 2 (half), 3 (three-quarter), and 4 (full pedalling technique). The last_known_state is a legitimate supplied observation and can be directly copied into the required anchor field. Evaluation Metrics A wrong anchor receives a zero case score. For valid anchors, the final row score combines an event-based F1 metric and a state-based Dice coefficient: $$\text{Row Score} = 0.7 \times \text{Command Event F1} + 0.3 \times \text{Macro State Dice}$$ 1. Command Event F1 Event matching requires the same new state and a time difference of at most three bins (60 ms). The evaluator chooses a maximum-cardinality one-to-one match. Event F1 is computed as: $$F1 = \frac{2 \times \text{matches}}{P_c + T_c}$$ Where $P_c$ is the number of predicted commands and $T_c$ is the number of target commands. Both empty command lists score 1.0; if only one is empty, it scores 0.0. 2. Macro State Dice Each command sequence is expanded to its 125 categorical states. For each state $k$ that appears in either the predicted or target sequence, the Dice coefficient is computed over the bins assigned to that state: $$\text{Dice}k = \frac{2 \vert{}S{p,k} \cap S_{t,k}\vert{}}{\vert{}S_{p,k}\vert{} + \vert{}S_{t,k}\vert{}}$$ These state Dice values are averaged over the union of present states; states absent from both predictions and targets are omitted. Final Score Average case scores are computed across all evaluation rows. Scores are maximized in [0, 1], and a perfect submission scores exactly 1.0. A malformed payload scores zero for that specific case. Wrong ordered columns, duplicate IDs, missing/extra evaluation IDs, or an unreadable top-level file will score zero for the entire submission. Row order is irrelevant. Sample Submission Format Submit a CSV file with exactly id,pedal_commands in that order, containing one row per evaluation ID. The pedal_commands payload is a quoted JSON object containing: anchor: Integer 0–4, equal to the supplied last_known_state. changes: A list of [bin, new_state] integer pairs. bin is relative to blackout start, ranging from 0 to 124. new_state is 0–4. Change bins must strictly increase, and each new state must differ from the current state. There can be at most 125 changes. The anchor remains active from blackout start until the first command. A command at bin $b$ changes the state for bins $b$ onward until the next command. A change at bin 0 is allowed when the first blackout bin differs from the anchor. Empty changes denote that the anchor persists throughout the blackout. id,pedal_commands example_id,"{""anchor"":2,""changes"":[[12,0],[19,4],[78,0],[86,2]]}" (In this example, the first command occurs at 1.5 + 12 × 0.02 = 1.74 seconds within the audio window). Booleans, fractional numbers, duplicate/unsorted times, redundant same-state commands, and extra keys are invalid and will cause a row rejection. What Not To Use To ensure a fair evaluation of training efficiency and architecture design: No External Data: Do not use external labeled performances, source-audio fingerprint matching, or score lookup. No Web Services: Web access, hosted APIs, and external databases are prohibited. No Source Exploitation: Do not manually annotate evaluation data, use hard-coded answer tables, or access future source sensor samples. No Pretrained Task Checkpoints: Challenge-specific checkpoints are forbidden. Use supplied public observations, training labels, and general pretrained weights cached before execution. Keep complete recording groups together for internal validation. The known pre-blackout state is allowed; future source sensor samples are explicitly not. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Prompted Nasal Structure Propagation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73vrmbfg02dsh7zzwv84spns8dt3kt
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat 15_luz's score of 0.633!

Full challenge description from page:

> Background In medical imaging, consistently tracking the boundary of a specific anatomical structure across a 3D volume is a fundamental challenge. Structures like the nasal cavity or maxillary sinuses are complex, can split into multiple disconnected "islands," and eventually disappear entirely as one moves through a CT slab. Traditional segmentation often relies on training models to recognize specific, named anatomy from scratch. However, a more robust and clinically flexible approach is prompted propagation: given an initial expert-annotated contour (a prompt) on one slice, the model must track that exact structure through subsequent slices, regardless of its unverified anatomical name. This task evaluates the ability to track structural continuity and handle incomplete image delivery. Overview Prompted Nasal Structure Propagation challenges you to follow one annotated nasal-region structure through a CT slab. You receive a binary contour prompt on the first slice and a sequence of CT observations. Your task is to recover that same structure's cross-section at offsets of +12, +24, and +36 slices. The shape may split or disappear as the slab advances; you must include every part belonging to the prompted structure. The prompt alone determines the target identity (a numerical anatomical class name is neither supplied nor required). Furthermore, this task simulates real-world data latency: slice observations near the end of the slab may be unavailable (zeroed out), yet you must still predict the structure's location. You must fine-tune a general pretrained backbone using the provided training set, updating actual pretrained parameters. Your solution must run offline on a single NVIDIA A10G GPU within 90 minutes, which includes cached-weight loading, fine-tuning, and inference. Dataset Information (Public Files) All participant-facing data is stored in the public/ directory. CT volumes are strictly partitioned; a volume stays entirely in one split. +-----------------------+-------------------------------------------------------------+ | File / Directory | Description | +-----------------------+-------------------------------------------------------------+ | train/ | Directory containing training case inputs as .npz files. | | test/ | Directory containing evaluation case inputs as .npz files. | | cases.json | Metadata mapping case IDs to their NPZ files and structural | | | properties. | | train.csv | Training set ground-truth run-length encoded masks. | | sample_submission.csv | Template showing the required CSV submission format for the | | | evaluation set. | +-----------------------+-------------------------------------------------------------+ Deterministic sensor stress: Every case uses the same seeded corruption distribution in training and evaluation. CT observations are reduced to 40, 48, or 64 pixels per side and resized to 128, then blurred (sigma 0.7–1.4). A case-wide gain of 0.65–1.35, bias of −0.12–0.12, and gamma of 0.7–1.5 change contrast. Independent Gaussian noise has standard deviation 0.07–0.13 multiplied by 1+0.025*i for zero-based slice index i; a second Gaussian field (standard deviation 0.18) is spatially smoothed with a 9×9 kernel. Two to four sinusoidal bands drift across slices, with amplitudes 0.06–0.16, and three to six bright/dark streak distractors per slice have amplitudes 0.12–0.30. Intensities are clipped and quantized to 32 levels stored as 0,4,...,124. Three case-wide rectangular dropout regions have independently sampled heights and widths of 18–34 pixels. The availability array marks only dropout and undelivered slices, not noisy-but-observed pixels. These are explicitly synthetic acquisition corruptions; the source-derived prompt and target masks are unchanged. Longer-range sampling: Eligible base slices are considered every eight native slices, with targets at +12/+24/+36 and observations every three slices. A source volume remains wholly in one split, using the existing volume assignment and geometry/deduplication checks. The prompt must contain at least four grid cells. All-empty future cases are retained with a deterministic one-in-four sampling rule. Cases with disappearing or disconnected structures remain valid. Feature Schema cases.json +----------------------+------------------+-----------------------------------------------------+ | Feature | Type | Description | +----------------------+------------------+-----------------------------------------------------+ | id | String | Opaque case ID. | | split | String | train or test. | | input | String | Relative path to the .npz file. | | volume_group | String | Opaque volume key for internal grouping. | | slice_offsets | List of Integers | [0,3,6,9,12,15,18,21,24,27,30,33] - the sequence of | | | | CT slices provided. | | target_slice_offsets | List of Integers | [12,24,36] - the slices where you must predict the | | | | mask. | | prompt_slice_offset | Integer | 0 - the slice containing the initial prompt mask. | | late_slices | Integer | 9, 12, or 15 - specifies simulated latency. Slices | | | | beyond 36 - late_slices are unavailable. | | output_grid | Pair of Integers | [64, 64] - target grid dimension for the output | | | | mask. | +----------------------+------------------+-----------------------------------------------------+ Input NPZ Arrays (train/.npz, test/.npz) +------------+----------------+--------------------------------------------------------------+ | Array Name | Type / Shape | Description | +------------+----------------+--------------------------------------------------------------+ | slices | uint8 | CT observations. Native intensities are clipped to | | | [12, 128, 128] | [-1000, 800], mapped to [0,1], perturbed with mixed seeded | | | | noise, and quantized. Divide by 124 for normalized values. | | | | Three 18-34 pixel rectangles are masked in every slice. | | available | uint8 | Binary mask indicating valid pixels. Pixels subjected to | | | [12, 128, 128] | the three rectangles or delivery latency (delayed slices are | | | | zeroed) have an availability of 0. | | prompt | uint8 | Binary contour of the target structure on slice 0. | | | [64, 64] | (1 = structure, 0 = background). | +------------+----------------+--------------------------------------------------------------+ Note: Slices use row=y and column=x, with rows downward and columns rightward. The prompt covers the same field of view as the CT image but at half the raster dimension. Evaluation Metrics For each of the three prediction horizons (+12, +24, and +36 slices), three metrics are calculated: 1. Mask Dice: Measures volume overlap between the predicted mask ($P$) and true mask ($T$). $$\text{Dice}(P, T) = \frac{2 \times \vert{}P \cap T\vert{}}{\vert{}P\vert{} + \vert{}T\vert{}}$$ (If both masks are empty, Dice = 1.0) 2. Boundary F1: A cell is a boundary cell if at least one location in its 3×3 neighborhood is background. Precision is the fraction of predicted boundary cells within one Chebyshev grid step of a target boundary cell. Recall reverses the roles. $$\text{Boundary F1} = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$ (If both masks are empty, Boundary F1 = 1.0) 3. Presence Agreement: Scores 1.0 if both prediction and target are present, or both are absent. Scores 0.0 otherwise. Horizon Score: The score for a single horizon is the weighted sum: $$\text{Horizon Score} = 0.65 \times \text{Mask Dice} + 0.25 \times \text{Boundary F1} + 0.10 \times \text{Presence Agreement}$$ Final Score: Average the three horizon scores for a case, and then average across all evaluation cases. The maximum score is 1.0. Submission Format Submit a CSV file with exactly two columns, in this order: id,propagated_sections. Include one row for every evaluation ID found in sample_submission.csv. propagated_sections must be a JSON array containing three lists, corresponding to the target masks at +12, +24, and +36 slices. Each list contains Run-Length Encoded (RLE) pairs: [start, length]. The 64x64 binary mask is flattened in row-major order: index = row * 64 + column. Indices range from 0 to 4095. Runs must be sorted, non-overlapping, and bounded within the grid. An empty list [] means the structure is absent on that slice. Example Row: id,propagated_sections example_id,"[[[130,4],[194,5]],[[195,3]],[]]" (In this example, the +12 slice has two foreground runs, the +24 slice has one run, and the structure is absent on the +36 slice). Malformed submissions: Incorrect columns, duplicate IDs, or a mismatched evaluation ID set receive a file-level score of 0.0. Invalid JSON, the wrong number of masks, or malformed RLE receives 0.0 for that complete row. It is not treated as a valid prediction of three empty masks. Valid empty masks retain the stated empty-mask scoring rules. What Not To Use To ensure a fair evaluation of model architecture and training efficiency, the following are strictly prohibited: No External Data: Do not use external CT datasets, hosted APIs, or web access. No Source Exploitation: Do not attempt source-volume matching or reverse lookups against the original NasalSeg dataset. No Manual Interventions: Hard-coded answer maps, manual evaluation contours, or challenge-specific checkpoints are forbidden. Split Integrity: If making an internal validation split, you must keep complete volume groups together. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Two Check Slavic Speech Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c6f6vte3qanvka1tpr0fv158a90m8
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mikegoodman's score of 0.907!

Full challenge description from page:

> Two Check Slavic Speech Repair Overview Your goal is to determine which recordings in each four-file bundle express the same prompt. You may train from scratch or use the single vetted multilingual speech encoder specified under What not to use, with all task-specific learning restricted to the supplied construction data. Every bundle contains one Polish, one Russian, one Serbian, and one Ukrainian recording in shuffled positions. Between one and four different prompts may be present, so the four recordings can form any of 15 possible groupings. You receive 528 labelled construction bundles containing 2,112 recordings and 132 test bundles containing 528 recordings. For each test bundle, first predict how likely each of the 15 groupings is. Then precommit to two adaptive yes or no questions for a human reviewer. Each question asks whether a selected pair shares a prompt, and the second question may depend on the first answer. Your final output also specifies which grouping to use after each possible pair of answers. This models a localization workflow where mixed audio must be repaired with a strict human-review budget. Evaluation Submissions are scored with the Adaptive Two Check Repair Score. The metric evaluates the submitted state prior, the grouping produced after two simulated human answers, and the quality of the complete decision tree under the submitted prior. It produces a score from 0 to 1, and higher is better. The state-prior component uses a variation-of-information partition kernel and compares the submitted 15-state distribution with the empirical-prior reference. The realized-repair component follows the two true binary answers through the submitted tree, measures the variation of information between the selected repair and the true grouping, and compares it with the best content-blind tree. The policy-use component compares the expected loss of the entire submitted tree with both the optimal tree and the best action that asks no questions. Each baseline-relative component is clipped to 0,1]. The arithmetic mean of state-prior and realized-repair skill is multiplied by policy-use skill, as stated in Evaluation Details. Task Details For each bundle, submit 15 nonnegative state weights and seven integer policy decisions. The policy works as follows. first_check chooses the first pair of recording positions to ask about. The grader looks up the true answer. 0 means different prompts and 1 means the same prompt. If the first answer is 0, second_if_different chooses the second pair. If the first answer is 1, second_if_same chooses it instead. The grader looks up the second answer and selects one of repair_00, repair_01, repair_10, or repair_11. The first digit is the first answer and the second digit is the second answer. The selected repair is the final grouping for that bundle. The second check must be different from the first. It may differ between the two first answer branches. The human answers are simulated by the grader from the private grouping, so no interaction is required while a submission is running. This is not a pair prediction or retrieval output. The submitted object is a small conditional decision program. It must specify what to ask, how the next action changes after the answer, and what repair to make at every possible leaf. Regional setting The bundles represent a four country localization workflow covering Poland, Russia, Serbia, and Ukraine. Polish is West Slavic, Russian and Ukrainian are East Slavic, and Serbian is South Slavic. Related languages can share historical roots and acoustic patterns while expressing different content. The audio contains short human readings rather than meetings, debates, or broadcasts. There are no documents, timestamps, transcripts, speaker turns, or candidate sentences to align. Each recording occurs in one bundle only. Grouping state indices The 15 states are set partitions of four labelled positions. A code gives the block membership of positions 0, 1, 2, and 3. State indices used in the repair columns are: State 0 is code 0000. State 1 is code 0001. State 2 is code 0010. State 3 is code 0011. State 4 is code 0012. State 5 is code 0100. State 6 is code 0101. State 7 is code 0102. State 8 is code 0110. State 9 is code 0111. State 10 is code 0112. State 11 is code 0120. State 12 is code 0121. State 13 is code 0122. State 14 is code 0123. The five block shapes have 1 + 4 + 3 + 6 + 1 = 15 states. In particular, the six states with shape 2 + 1 + 1 are: 0012 gives pair {0,1} and singletons {2} and {3}. 0102 gives pair {0,2} and singletons {1} and {3}. 0112 gives pair {1,2} and singletons {0} and {3}. 0120 gives pair {0,3} and singletons {1} and {2}. 0121 gives pair {1,3} and singletons {0} and {2}. 0122 gives pair {2,3} and singletons {0} and {1}. Check indices The three query columns use integer pair indices. Check 0 asks about positions 01. Check 1 asks about positions 02. Check 2 asks about positions 03. Check 3 asks about positions 12. Check 4 asks about positions 13. Check 5 asks about positions 23. For example, suppose a row uses first_check = 0, second_if_different = 5, and second_if_same = 1. The human first checks positions 0 and 1. A different prompt answer leads to a check of positions 2 and 3. A same prompt answer instead leads to a check of positions 0 and 2. How the bundles were constructed Every grouping state is represented on both sides of the split. Construction contains 34 to 36 examples per state, and test contains 7 to 12 examples per state. Prompts used in construction do not appear in test. No deposited recording is reused. Every bundle contains exactly one recording from each locale. Locale positions are shuffled separately for every bundle. Identifiers do not reveal the locale, prompt, state, or construction order. Dataset The public data contains: train_audio/ with 2,112 construction WAV files. test_audio/ with 528 test WAV files. train_bundles.csv with 528 construction bundles. train_relations.csv with 528 relation label rows. test_bundles.csv with 132 test bundles. sample_submission.csv with 132 policy rows. Audio files in public/train_audio/ and public/test_audio/ There are 2,640 audio files. Waveform is a signed 16 bit integer array containing mono PCM audio samples. Sample rate is integer metadata and is always 8,000 Hz. Channels is integer metadata and is always 1, meaning every file is mono. Duration is a floating-point number of seconds derived from the sample count. Files are no longer than about 10.2 seconds. File name is a string consisting of an opaque audio identifier followed by the .wav extension. public/train_bundles.csv This file has 528 rows. bundle_id is a string containing the opaque bundle identifier. audio_0 is a string containing the recording identifier at position 0. audio_1 is a string containing the recording identifier at position 1. audio_2 is a string containing the recording identifier at position 2. audio_3 is a string containing the recording identifier at position 3. public/train_relations.csv This file has 528 rows. bundle_id is a string used to join labels to train_bundles.csv. relation_01 is a binary integer indicating whether positions 0 and 1 share a prompt. relation_02 is a binary integer indicating whether positions 0 and 2 share a prompt. relation_03 is a binary integer indicating whether positions 0 and 3 share a prompt. relation_12 is a binary integer indicating whether positions 1 and 2 share a prompt. relation_13 is a binary integer indicating whether positions 1 and 3 share a prompt. relation_23 is a binary integer indicating whether positions 2 and 3 share a prompt. The six relations form one valid state. Participants may convert them to a state index using the mapping above. public/test_bundles.csv This file has 132 rows. Its columns are bundle_id (string opaque bundle identifier), audio_0 (string recording identifier at position 0), audio_1 (string recording identifier at position 1), audio_2 (string recording identifier at position 2), and audio_3 (string recording identifier at position 3). Its audio identifiers refer to files in public/test_audio/. public/sample_submission.csv This file has 132 rows and the 23 required columns described below. Its state prior is produced by a small construction only acoustic model. Its policy is obtained by enumerating valid two question trees under that prior. Its columns are bundle_id (string); prob_0000, prob_0001, prob_0010, prob_0011, prob_0012, prob_0100, prob_0101, prob_0102, prob_0110, prob_0111, prob_0112, prob_0120, prob_0121, prob_0122, and prob_0123 (floating-point state weights); first_check, second_if_different, and second_if_same (integer pair indices); and repair_00, repair_01, repair_10, and repair_11 (integer grouping-state indices). Submission Submit one row for every test bundle. The required columns are bundle_id, the fifteen prob_* columns in the state order listed above, first_check, second_if_different, second_if_same, repair_00, repair_01, repair_10, and repair_11. A valid example row assigns equal weight to all fifteen states, uses checks 0, 5, and 1, and uses repair states 14, 13, 4, and 0 for leaves 00, 01, 10, and 11, respectively. The exact CSV header is: bundle_id,prob_0000,prob_0001,prob_0010,prob_0011,prob_0012,prob_0100,prob_0101,prob_0102,prob_0110,prob_0111,prob_0112,prob_0120,prob_0121,prob_0122,prob_0123,first_check,second_if_different,second_if_same,repair_00,repair_01,repair_10,repair_11 Example row 1: bd_0123456789abcdef0123456789abcdef,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,5,1,14,13,4,0 Example row 2: bd_fedcba9876543210fedcba9876543210,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,0,4,0,3,9,14 Column definitions: bundle_id is a string identifier copied from test_bundles.csv. prob_0000, prob_0001, prob_0010, prob_0011, prob_0012, prob_0100, prob_0101, prob_0102, prob_0110, prob_0111, prob_0112, prob_0120, prob_0121, prob_0122, and prob_0123 are floating-point state weights. They must be nonnegative after sanitization. The grader normalizes them within each row, so they do not need to sum to 1. Negative and nonfinite values become 0, and an all-zero row becomes uniform. first_check is an integer pair index from 0 through 5. second_if_different is an integer pair index from 0 through 5 and must differ from first_check. second_if_same is an integer pair index from 0 through 5 and must differ from first_check. repair_00, repair_01, repair_10, and repair_11 are integer grouping-state indices from 0 through 14. Requirements The CSV should contain one policy row for each of the 132 test bundles and one header row. Every test bundle_id must appear exactly once. All 23 required columns must be present. Query and repair columns must contain finite integers in their allowed ranges. A missing test identifier, duplicate graded identifier, or invalid policy affects only that bundle. The row receives zero improvement over the reference policy in all three score components, and the grader emits a warning containing the affected bundle_id. Other valid bundles are still scored. Unknown identifiers are ignored. A missing required column raises ValueError. Extra columns and column order do not affect scoring. Submission row order does not change the score. Multiplying all 15 state weights in one row by the same positive number does not change the score. Evaluation Details The Adaptive Two Check Repair Score has three components. State prior score Let q_i be the normalized 15 state prior and let Y_i be the one hot true state. Define normalized variation of information and a partition kernel: VI(a,b) = (H(a) + H(b) - 2*I(a,b)) / log(4) K(a,b) = exp(-3 * VI(a,b)) The state loss gives less penalty to nearby split and merge errors than to distant states. L_state_i = (q_i - Y_i)^T K (q_i - Y_i) Let q0 be the empirical state distribution in the graded answers. L_state = mean_i L_state_i L0_state = mean_i (q0 - Y_i)^T K (q0 - Y_i) r_state = 1 - L_state / L0_state Realized repair score The grader executes the submitted decision tree using two true binary answers. Let a_i be the final repair state reached by that path and t_i be the true state. L_repair = mean_i VI(a_i, t_i) The content blind reference is not a random tree. It is the best single adaptive two question tree and set of leaf repairs for the empirical state distribution of the graded answers. Let its loss be L0_repair. r_repair = 1 - L_repair / L0_repair A row dependent audio policy must beat the strongest fixed policy, not merely a random choice of questions. Policy use score The four leaf repairs and both possible second questions can also be evaluated before the true answers are known. For the submitted prior q_i, define: L_submit_i as the expected VI loss of the submitted tree. L_opt_i as the lowest expected loss among every valid adaptive two question tree under q_i. L_none_i as the lowest expected loss when no human question is allowed. The policy use skill is calculated separately for each bundle. This prevents a row with almost no available information gain from dominating the denominator for every other row. gain_i = L_none_i - L_opt_i excess_i = L_submit_i - L_opt_i When gain_i > 0, r_policy_i = 1 - excess_i / gain_i. When gain_i = 0, r_policy_i is 1 if excess_i = 0 and 0 otherwise. r_policy = mean_i clip(r_policy_i, 0, 1) This component checks the whole decision tree, including leaves that are not reached by the private truth. A model cannot receive full policy credit by filling only the realized path correctly. Baseline centering and final score Each raw component is clipped without squaring or a count-dependent deadband: s_state = clip(r_state, 0, 1) s_repair = clip(r_repair, 0, 1) s_policy = clip(r_policy, 0, 1) The final score gives equal weight to state and repair skill, multiplied by policy-use skill: score = 0.5 * (s_state + s_repair) * s_policy An optimal policy with no state or repair skill scores zero. Modest positive state or repair skill receives linear credit when policy use is optimal. A weak inference component no longer bottlenecks the other, while poor use of the submitted prior reduces the combined score. Full credit requires all three components to be perfect. Scoring constants: KERNEL_SCALE = 3.0 # K(a,b) = exp(-KERNEL_SCALE * VI(a,b)) EPS = 1e-12 # numerical zero for reference loss, gain, and regret STATE_WEIGHT = 0.5 # coefficient of s_state in the final formula REPAIR_WEIGHT = 0.5 # coefficient of s_repair in the final formula For a graded answer subset with L0_repair <= EPS, the fixed reference already solves the repair task. That component has no headroom, so use s_repair = s_state, making the score s_state * s_policy. If L0_state <= EPS, state skill is 1 only when L_state <= EPS, and otherwise 0. The comparisons with zero in the policy-use formulas also use EPS. Exact normalized priors and correct realized repairs on every graded row, with all policies valid, score 1, including a single-row subset. An exact policy submission scores 1. Content-blind priors and policies score 0 on the full test set. Useful inference with a weaker policy may receive partial credit; policy optimization alone earns none. What not to use The only permitted pretrained model is the base speech encoder facebook/wav2vec2-xls-r-300m at revision 1a640f32ac3e39899438a2931f9924c02f080a54. Its encoder weights, configuration, and matching waveform feature extractor are allowed. You may keep the encoder frozen or fine-tune it using only the supplied construction audio and labels. Initialize any added learned components from scratch. Other checkpoints, externally fine-tuned derivatives, pretrained text models, speech-recognition heads, translation decoders, and foundation models are prohibited. Do not use outside embeddings, weights, tokenizers, acoustic front ends, or learned features beyond that single encoder exception. Features you compute locally from supplied audio with the permitted encoder are allowed. Do not fit or adapt any model on test audio or test predictions. Do not use external speech, transcripts, translation tables, pronunciation resources, text corpora, or label resources. Do not use web search, source lookup, reverse search, fingerprint services, hosted inference services, or external label recovery. Downloading the exact permitted checkpoint and reading its software documentation are allowed; external task data and externally generated transcripts or translations are not. Do not manually transcribe, translate, identify, group, or annotate the test recordings. Do not derive predictions from identifiers, CSV order, file order, archive order, encoding artefacts, or reconstructed source metadata. Do not submit a fixed content blind question tree, fixed state prior, constant repair policy, or hand written audio rule as the final predictor. A deterministic policy optimizer is allowed when its state prior comes from a model whose task-specific training uses only the supplied construction data, optionally with the permitted encoder. You may build and train a model from scratch or use the permitted encoder under these conditions. You choose the architecture, representation, training procedure, and policy optimization method. The encoder expects 16,000 Hz input; resampling the supplied 8,000 Hz audio is allowed. The checkpoint is optional and is not downloaded by prepare.py or grade.py. Record the checkpoint ID and revision in your solution notes. The vetted checkpoint is released under Apache 2.0 and was pretrained on unlabelled multilingual speech. Its [official model card documents the model and input requirements. These permissions cover encoder use only. &nbsp;
> $700 Pool
> Closes in 3h 43m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## NTSB Causal Ledger: Final-Report Timeline and Finding Compilation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75vmdfaqf2r7x51t7gs2hbms8dy63x
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pardeep-singh's score of 0.540!

Full challenge description from page:

> NTSB Causal Ledger: Final-Report Timeline and Finding Compilation Assignment Fine-tune a model to transform a sanitized aviation accident record into a constrained JSON ledger. Each record provides a final factual narrative, a shuffled list of official occurrence candidates, and a shuffled list of official finding candidates. Your ledger must put every occurrence in chronological order, identify the official defining occurrence, and label every finding according to whether it was cited in the probable-cause statement as a cause or contributing factor. This is structured prediction, not report writing. Do not generate a probable-cause paragraph. Do not add events or findings. Do not infer legal blame. Do not connect individual findings to individual occurrences, because the modern downloadable source tables do not provide that relationship. Every valid output uses only opaque candidate IDs supplied for the same record. The task is categorized as fine-tuning because successful systems should learn recurring relationships among narrative evidence, standardized event descriptions, and finding taxonomies. A fixed prompt with a general model may produce plausible prose, but plausibility earns no credit unless the exact supplied candidates are organized and classified correctly. Inputs Each public input row has four fields. case_id is a stable opaque identifier. factual_text is a generalized final factual narrative. occurrence_candidates_json is a JSON list of two through eight objects. finding_candidates_json is a JSON list of two through twelve objects. Candidate objects contain exactly id and text. Occurrence text combines a phase or activity with a discrete event description. Presentation order is keyed and deliberately unrelated to chronology. Finding text comes from the source finding taxonomy. Legacy terminal cause/factor markers have been removed because they would directly reveal the target. A candidate ID is meaningful only inside its row; models should reason from the narrative and candidate text rather than memorize ID fragments. The factual narrative uses lowercased text and explicit generalization tokens. ` replaces structured identifying values such as a matched location, aircraft model, or organization. replaces tail-number forms. replaces recognizable calendar dates, replaces numbers, replaces links or email-like strings, and ` replaces alphabetic tokens that occurred fewer than four times in the training vocabulary. Punctuation and common causal language remain. Sanitization reduces lookup cues and removes fields irrelevant to the desired reasoning. It also makes some records harder. A rare component name may become ``, measurements lose exact values, and the metadata-heavy opening sentence may be removed. Treat the provided text as the full allowed evidence. External source lookup is prohibited. Output Submit exactly two CSV columns in this order: case_id,ledger_json The JSON object has exactly these keys: { "timeline": ["O_...", "O_..."], "defining_occurrence": "O_...", "finding_labels": {"F_...": true, "F_...": false} } timeline must contain every supplied occurrence ID exactly once. Its first element is the earliest coded occurrence and its last is the latest. defining_occurrence must be one member of the timeline. finding_labels must contain every supplied finding ID exactly once as an object key, with a genuine JSON boolean value. Strings such as "true", integers such as 1, and null are invalid. The submission may serialize object keys in any order, and CSV rows may be reordered. The timeline order is semantic and is scored. Unknown IDs, duplicated occurrence IDs, omitted candidate IDs, additional IDs, additional JSON keys, malformed JSON, or out-of-range list sizes give that record zero credit. Table-level failures such as wrong columns, missing cases, duplicate case identifiers, or mismatched identifiers return zero for the submission. Meaning of the targets The occurrence order comes from the official Occurrence_No field. The NTSB data dictionary says occurrences are entered chronologically starting with number one. The defining selection comes from Defining_ev. NTSB describes this flag as a way to group accidents of similar type and explicitly says it is not intended to indicate or suggest cause. Correctly predicting it is therefore an event-characterization task separate from finding inclusion. Finding labels come from the official cm_inPC field. true means the associated finding area was cited in the probable-cause statement as a cause or contributing factor. false means it was not cited that way. The benchmark does not separate “cause” from “factor.” The older Cause_Factor field stopped being populated for new cases after October 2020 and is not used as a target. The finding label is not an evidence-span annotation. Although the factual narrative provides relevant evidence, NTSB does not supply sentence offsets that justify each finding. The benchmark therefore evaluates selection among official candidates, not span extraction. Likewise, the output has no finding-to-occurrence edge. Adding either structure would create derived ground truth not present in the source. Metric The evaluator first confirms that the predicted candidate universes exactly match the answer candidate universes. This is possible because the output labels every finding and orders every occurrence. A universe mismatch scores zero rather than being silently repaired. For finding labels, the grader computes F1 for the positive causal class and F1 for the negative noncausal class, then averages them. Each selected record contains both classes. The resulting macro-F1 is converted to skill above a 0.5 reference: C = max(0, 2 * macro_f1 - 1). This makes all-positive, all-negative, and chance-like policies weak while preserving one for perfect classification. For occurrence order, the grader examines every pair in the predicted timeline and counts the fraction ordered the same way as the gold timeline. This is equivalent to one minus normalized Kendall inversion distance. Pair agreement is also converted to skill above 0.5: O = max(0, 2 * pair_agreement - 1). An exact sequence earns one; a complete reversal earns zero. Defining accuracy D is binary. The record score is: 0.45 * C + 0.20 * O + 0.15 * D + 0.20 * C * O * D The last term rewards a ledger whose three aspects work together. Scores are averaged over records. An oracle scores exactly one. Completely inverted findings, reversed chronology, and an incorrect defining selection score zero. The grader is deterministic, requires no images or models, and returns a finite value in [0,1]. Modeling suggestions A sequence-to-sequence model can concatenate the factual narrative and candidate JSON and generate the ledger. Constrained decoding or post-generation schema validation is recommended. Because IDs are opaque and instance-specific, copying mechanisms are useful. A model must retain all candidates even when source text approaches the maximum length. A multi-head alternative may be easier to control. Encode the narrative once, score each finding for binary inclusion, score occurrence pairs or positions, and score each occurrence as defining. A deterministic serializer can then produce valid JSON. Pairwise occurrence scores can be decoded with a ranking algorithm. This approach separates schema generation from task inference and guarantees complete candidate coverage. Training objectives should account for the negative finding class. Every record has both classes, but positives are often more numerous. Macro-F1 rewards balanced discrimination rather than raw accuracy. For sequence generation, candidate-order augmentation is permitted within training rows because presentation order is not a target. All augmented siblings must remain inside the same validation group. The development set is chronologically later than training and is the appropriate place to tune thresholds, decoding, and schema recovery. Do not mix development rows into training when reporting the standard reference comparison. Never use test candidate distributions to tune model thresholds. Baselines and runtime The sample submission marks all findings true, repeats shuffled occurrence order, and selects the first presented occurrence. It scores 0.138651. The reference baseline uses unigram TF-IDF classifiers plus average phase position and scores 0.482248. Both are intentionally below the 0.50 challenge threshold. The included starter uses google/flan-t5-small, a public non-gated sequence-to-sequence checkpoint. One epoch over 4,032 rows with length limits of 768 input tokens and 384 output tokens is intended to finish inside sixty minutes on one 16 GB GPU. Initial model/package download is excluded from timed inference and must occur before offline evaluation. Proprietary models, gated checkpoints without redistribution rights, paid APIs, and more than one GPU are not required. Split integrity All aircraft records sharing an NTSB source event remain together. Exact normalized narratives and confirmed near-duplicate narratives are merged into larger groups. Approval years through 2018 train the model, 2019 forms public development, 2020–2021 are excluded as a buffer, and 2022–2025 form private test. The private audit proves that no event or duplicate cluster crosses a split. The temporal design limits future-report leakage and makes the task sensitive to evolving finding practices. It does not guarantee immunity from pretrained-model memorization. Official reports are public, and common accident language persists over time. Results must acknowledge this residual risk. Interpretation and conduct NTSB investigations determine probable cause to improve transportation safety. They do not determine civil liability or legal fault. A model output is only a prediction of coded source fields for this filtered benchmark. It must not be presented as an independent accident conclusion, operational recommendation, or substitute for an official report. Do not attempt to reverse opaque IDs, search phrases in CAROL, query report URLs, or recover excluded source metadata. Do not manually label held-out cases. Local open-source modeling is permitted. Prediction and grading must remain offline. The release uses only NTSB-authored downloadable database text. Third-party docket attachments and media are excluded because NTSB warns that material submitted by other parties may remain copyrighted. Credit the source as “Courtesy: National Transportation Safety Board.” &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Statutory Protection Grounds from Fabric Descriptions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx716c3bwwkrfa2jpc3461y5218dwa5d
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Statutory Protection Grounds from Fabric Descriptions
> Statutory Protection Grounds from Fabric Descriptions Overview This is a from-scratch model-training task on written architectural field surveys. A national built-heritage survey sends trained architectural historians to visit standing structures one by one. At each visit the surveyor writes a systematic account of the physical fabric — plan form, bay and storey count, walling, roof, openings, joinery, ironwork, decorative treatment, curtilage — and then, separately, records which statutory grounds of protection that structure satisfies. The grounds are a fixed vocabulary set out in national legislation, and a structure may satisfy any number of them, including none beyond the ordinary one that every surveyed structure carries. You are given the fabric account and a small amount of coarse locational context. Train a model that produces, for each structure, the strength of evidence for each of the five statutory grounds. The fabric account describes what is physically present. The grounds record a judgement about why the structure is worth protecting, which is a different thing: a plain farm outbuilding and an elaborate villa can both be protected, on entirely different grounds, and the same decorative vocabulary supports different grounds in different structures. Roughly a quarter of the structures in this dataset satisfy none of the five grounds, so recognising when the evidence supports nothing beyond the ordinary is part of the task and is scored. All text is real surveyor prose. Nothing is generated. Calendar years, the surveyor's own summary vocabulary, and place identifiers have been replaced by the placeholder tokens [DATE], [X] and [PLACE] so that the answer cannot be read off the words; everything else is the surveyor's own wording, unaltered. Prediction targets For each structure, produce five numbers, each in the range 0 to 1, giving the strength of evidence that the structure was recorded as satisfying that ground: artistic - the ground concerned with designed visual quality: composition, proportion, decorative programme, craftsmanship of finish. social - the ground concerned with the structure's role in the life of a community. technical - the ground concerned with construction method, engineering, materials technology or machinery. historical - the ground concerned with association with events, phases or persons of record. specialist - the combined evidential ground, recorded when the structure attests to something beyond its design, use or construction: buried or fabric-embedded evidence of earlier periods, evidence bearing on a scientific or industrial process, or linguistic, literary, religious or commemorative meaning. This is the scarcest ground, recorded for 5.3% of structures in train.csv, and it carries the largest weight in the metric. A value of 0 means no evidence for that ground; 1 means the ground is certainly satisfied. Values may be any real number in [0, 1]; they are not required to sum to 1 and are not mutually exclusive. Data Three UTF-8 CSV files with a header row, plus this description. train.csv - 31,079 rows, 11 columns. record_id - string - rec followed by 12 digits - opaque per-structure key, unique across the whole dataset. Carries no information. survey_area - string - area followed by 6 digits - opaque key for the survey area the structure belongs to. 19 distinct areas in train.csv. Structures in one area were surveyed as one campaign. province - string - one of Leinster, Munster, Connacht, Ulster - coarse region. setting - string - built_up or open_country - whether the structure stands in a settlement or in open country. structure_kind - string - one of 13 values (dwelling, farm_building, religious, civic_institutional, education, commercial, industrial, transport, water_utility, memorial, estate_structure, defensive, other) - coarse functional grouping of the structure. evidence_text - string - the surveyor's fabric account, median 111 words, minimum 25 words. Contains the placeholder tokens [DATE], [X] and [PLACE] where calendar years, the surveyor's summary vocabulary, and place identifiers were removed. artistic, social, technical, historical, specialist - integer - 0 or 1 - whether that statutory ground was recorded for this structure. These are the training targets. test.csv - 13,700 rows, 6 columns: record_id, survey_area, province, setting, structure_kind, evidence_text. Identical in meaning to train.csv. The five ground columns are withheld. The 8 survey areas in test.csv do not appear in train.csv, so every scored structure comes from a survey campaign the model has never seen. sample_submission.csv - 13,700 rows, 6 columns - a correctly formatted submission carrying constant placeholder values. It is not a useful answer and scores near the floor. Base rates in train.csv: artistic 0.400, social 0.386, historical 0.212, technical 0.197, specialist 0.053. The mean number of grounds recorded per structure is 1.25 and 26.2% of structures have none. Submission format Exactly 6 columns in exactly this order: record_id, then the five ground columns. One row for every record_id in test.csv, 13,700 rows plus the header. Every value must be a finite number in [0, 1]. Duplicate record_id values, missing columns, extra columns, renamed columns, a different column order, non-numeric values, and values outside [0, 1] are all rejected. record_id,artistic,social,technical,historical,specialist rec709848541475,0.81,0.22,0.04,0.13,0.01 rec438727026391,0.35,0.66,0.09,0.41,0.03 rec949693611197,0.12,0.07,0.55,0.08,0.06 rec247922176830,0.04,0.03,0.02,0.05,0.01 Scoring Statutory Grounds Recovery Score. Direction: Maximize. Range: 0.0 to 1.0. Let p_k be your value and y_k the recorded indicator (0 or 1) for ground k, over the five grounds in the column order above. The scarcity weights are fixed constants that sum to 5: w = [0.6615, 0.6730, 0.9422, 0.9082, 1.8151] For each scored record compute three sub-scores. 1. Grounds agreement T - an asymmetric overlap between your evidence vector and the recorded grounds, weighted by scarcity: I = sum_k w_k * min(p_k, y_k) O = sum_k w_k * max(p_k - y_k, 0) U = sum_k w_k * max(y_k - p_k, 0) T = (I + 0.25) / (I + 0.70 * O + 1.30 * U + 0.25) Overstating a ground is penalised at 0.70; missing a ground that was recorded is penalised at 1.30, because a missed ground is the costlier error. The additive 0.25 makes an all-zero answer score 1 on a record that has no recorded grounds. 2. Evidence calibration C - how close your numbers are to the recorded indicators: C = 1 - ( sum_k w_k * |p_k - y_k| ) / ( sum_k w_k ) 3. Exact portfolio E - 1 if thresholding your values at 0.5 reproduces the recorded set of grounds exactly, and 0 otherwise. Each of T, C, E is clipped to [0.05, 1.0], then combined by a weighted geometric mean: r = exp( 0.50 * ln(T) + 0.25 * ln(C) + 0.25 * ln(E) ) The record score is r. Let R be the mean of r over all scored records. The reported score is R rescaled against a fixed reference R0 = 0.3842441, which is the mean record score achieved by the strongest rule that uses only structure_kind, province and setting — fitted and measured on the training split alone: if R float: ... What makes this hard The fabric account states what is there, not what it means. A strong model must learn which physical evidence a surveyor treats as supporting each ground — and the specialist ground occurs on only 5.3% of structures while carrying the largest scarcity weight, so a model that recovers only the two common grounds is heavily penalised. The honest ceiling is well below 1.0: several grounds turn on knowledge that the fabric account does not contain, so no model can recover them from the text alone. What not to use This is a machine-learning challenge. A model must be trained on the provided training data inside the submitted solution. Hand-written rules and hard-coded outputs are rejected on review even when they score well. Not allowed Hand-coded heuristics as the solution. Regular-expression or keyword rules over evidence_text, hand-written if/then logic over structure_kind, province or setting, lookup tables keyed on those columns, or any rule-based system standing in for a trained model. Note that the metric's zero point is exactly the best such rule: a structure_kind x province x setting lookup scores at the floor by construction. Exploiting artifacts. Row order, the numeric content of record_id or survey_area, file ordering, column ordering, or any incidental pattern not part of the described content. Hard-coded constants or per-id answer tables. (a) Test-time augmentation. (b) Pseudo-labelling, self-training, or any transductive use of the test set — no training on your own test predictions, no inference-on-test fed back into training. (c) Values fitted to the test labels — per-id answer tables, record_id-to-output maps, hard-coded weights, or thresholds and post-processing chosen to match the test distribution. (d) Fitting, adapting or normalising anything on test statistics, or any interaction with the test set beyond the single final prediction pass. (e) Inference-only solutions that ship pre-baked task-trained weights instead of training on the provided training data. You must train in the solution; the test set may be used solely to produce the final predictions. (f) External data of any kind. Use only the provided train.csv and test.csv. In particular, no external built-heritage registers, architectural inventories, conservation databases, gazetteers or scraped corpora. CARVE-OUT — public pre-trained model weights are NOT external data and ARE permitted and encouraged. You may download and fine-tune any public pre-trained backbone (for example from HuggingFace or timm) using the pre-installed packages. What is banned is external labelled data, external corpora, and any additional dataset beyond the one provided. (g) Basing development decisions on the test set — no train+test combined normalisation, no exploratory analysis of test inputs, no hyperparameter or threshold chosen from the test distribution. Every such choice must come from the training split or out-of-fold estimates only. (h) Reverse search against public indexes or catalogues. The fabric accounts are real surveyor prose. Do not attempt to match a released evidence_text against any external source — a built heritage register, an architectural inventory, a search engine, a cached web index, or any public archive — in order to recover the source record or its grounds of protection. Solutions that do this are rejected regardless of score. (i) Attempting to reconstruct the removed content. [DATE], [X] and [PLACE] placeholders mark text that was deliberately removed. Do not try to recover the underlying values from any external source. Allowed and encouraged Neural networks trained from scratch, fine-tuned public pre-trained text backbones, gradient-boosted trees, linear models, ensembles, cross-validation, feature engineering over the released columns, and probability calibration fitted on the training split. Because the 8 survey areas in test.csv are disjoint from the 19 in train.csv, grouped cross-validation by survey_area is the honest way to estimate held-out performance. survey_area is provided in both files for exactly that purpose. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Multimodal Generation Feedback Modeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e9s4ptbew2wfxfx38y65ks18bw5kj
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shivam_s's score of 0.184!

Full challenge description from page:

> Multimodal Generation Feedback Modeling Overview This is a fine-tuning / reward-modeling task. The machine-generated outputs being judged are images: each was synthesized by a text-to-image generative model from a short text brief (prompt). The images are general-domain scenes — everyday objects, people, animals, and places described by the prompt — spanning photorealistic and illustrative styles, and they carry the characteristic artifacts of generative image models (dropped or miscounted objects, malformed regions). From a labeled training split of human feedback, you model how a panel of human viewers judged these generated images and then predict that feedback for held-out images. There is no external label source: the human judgements must be learned from the provided training set — an off-the-shelf pretrained scorer does not reproduce this panel's behavior, so the challenge is to fine-tune a multimodal (image + brief) feedback judge on the supervised examples. Each item pairs one machine-generated image with the short text brief it was generated from, together with the feedback a panel of viewers left on it. The viewers left two very different kinds of feedback. First, they marked which spans of the brief were not faithfully realized in the image — a per-span omission signal, since a text-to-image generator routinely drops an object, a count, a relation, or an attribute that the brief asked for. Second, a separate panel rated the image on three axes that measure genuinely different things: how faithful it is to the brief, how internally consistent it is (structural coherence, absence of malformed regions), and how appealing it is irrespective of the brief. In this collection those three axes are only weakly related to one another — an image can be faithful yet low-appeal, or high-appeal yet incoherent — so a judge that models a single "quality" number cannot reproduce them. The task, from the generated image and its brief alone, reproduces both feedback layers: a submission must rank a fixed set of brief spans by how omitted they are, and emit a calibrated distribution over the human rating level for each of the three axes. In this collection the three axes are only weakly correlated with one another, and none of the human judgements is determined by surface statistics of the brief or the image file (brief length, encoded dimensions, or file size) — they require reading the image content against the brief. The score couples the span-omission ranking with per-axis ordinal calibration and applies an asymmetric penalty to confident rating mass placed far from the true level; the penalty is included so that a single central rating repeated across the axes does not score as a calibrated per-axis belief. Dataset Each item is one image generated by a text-to-image model from a short text brief, paired with the human feedback left on that image. The images are general-domain scenes (objects, people, animals, places) rendered in photorealistic and illustrative styles, stored as JPEG under public/images/ and referenced by the image_file column. Training rows carry the human labels (per-span omission votes and the three ordinal rating levels); test rows carry only the image and brief. Public files public/train.csv — one row per item, with labels. Feature columns (identical to test.csv): id, brief, span_A, span_B, span_C, span_D, span_E, image_file. Target columns (the same columns you submit): omit_A, omit_B, omit_C, omit_D, omit_E, faithful_p0…faithful_p4, consistent_p0…consistent_p4, appeal_p0…appeal_p4. public/test.csv — one row per item, without labels. Columns: id, brief, span_A, span_B, span_C, span_D, span_E, image_file. public/images/ — the generated images (text-to-image model outputs, one per item), re-encoded to JPEG and metadata-stripped, referenced by image_file. public/sample_submission.csv — a valid submission in the exact required format (same columns as answers.csv). Private file (organizer only) private/answers.csv — one row per test id, with exactly the same columns as sample_submission.csv: the true per-span omission vote weights (omit_A…omit_E) and, for each axis, a one-hot distribution over the five ordinal levels (faithful_p0…appeal_p4) marking the true level. Column descriptions Every column that appears in the public files is defined below. id (string) — unique item identifier, e.g. item_0f3a9c21. One generated image + brief per id; it is the unit of prediction. brief (string) — the text brief (prompt) the image was generated from. span_A … span_E (string) — five short spans taken verbatim from the brief (individual content words). These are the fixed candidate set whose omission you rank. The five spans are presented in a randomized order that carries no information about their omission. omit_A … omit_E (float) — the per-span omission signal. In train.csv (and, for the organizer, in answers.csv) these hold the human omission vote weight for the corresponding span — how strongly viewers judged that span to be not realized in the generated image, higher meaning more omitted. As a submission column, each is your predicted omission score for that span (higher = more omitted); only the induced ordering of the five is scored, so the absolute magnitudes and any ties are up to you. faithful_p0 … faithful_p4 (float) — probability distribution over the five ordinal brief-faithfulness levels (0 = least faithful, 4 = most). In train.csv/answers.csv this is a one-hot marking the true level (so the training level is the argmax); as a submission it is your calibrated belief and must be non-negative and sum to 1. consistent_p0 … consistent_p4 (float) — probability distribution over the five ordinal internal-consistency levels (0 = least consistent, 4 = most), same encoding as the faithful axis. appeal_p0 … appeal_p4 (float) — probability distribution over the five ordinal appeal levels (0 = least appealing, 4 = most), same encoding as the faithful axis. image_file (string) — relative path to the generated image under public/images/, e.g. images/img_9f3c1a2b7de4c018.jpg. The five ordinal levels on each axis are formed by quintile-binning the corresponding continuous human rating over the corpus. Split and anti-memorization Every training item that was generated from the same brief is kept entirely within one split — the train and test sets are brief-disjoint, so no test brief (and none of its generated images) appears in train.csv. A solver therefore cannot memorize a brief's feedback from training and read it back on test; it must judge unseen image–brief pairs from their content. Each image is re-encoded to JPEG and metadata-stripped, the five spans are presented in a randomized slot order, and the axis levels are quantized so the test targets cannot be recovered by matching structure or metadata. The brief-grouping key used to build the disjoint split is held internally and is not released as a column. Data example A truncated test.csv row (labels withheld): id,brief,span_A,span_B,span_C,span_D,span_E,image_file item_0f3a9c21,"three red umbrellas on a wet cobblestone street",umbrellas,cobblestone,red,three,street,images/img_9f3c1a2b7de4c018.jpg Submission format Submit a single CSV with exactly one row per id in test.csv and a header. Every row has the same fixed width. The submission has exactly the same columns as answers.csv. Columns, in order: id — the item id. omit_A, omit_B, omit_C, omit_D, omit_E — a numeric omission score for each of the five span slots, higher meaning more omitted. Only the ordering the five scores induce is scored (via a rank correlation against the true vote weights), so the absolute scale is free and ties are allowed. Every one must be a finite number. For each axis faithful, consistent, appeal, five columns _p0 … _p4 — a probability distribution over that axis's five ordinal rating levels 0–4. Each axis's five values must be non-negative and sum to 1 (a tolerance of 0.02 is allowed; values are renormalized before scoring). This is 1 + 5 + 15 = 21 columns. Extra or missing columns are rejected. Because the candidate span set is fixed at five and each axis has five levels, every submission row has identical width. Sample submission (uninformative baseline — equal omission scores and a uniform distribution on every axis): id,omit_A,omit_B,omit_C,omit_D,omit_E,faithful_p0,faithful_p1,faithful_p2,faithful_p3,faithful_p4,consistent_p0,...,appeal_p4 item_0f3a9c21,0.5,0.5,0.5,0.5,0.5,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2 Evaluation Metric — Omission-Ranking and Calibration Score. Higher is better. Each item receives a score in 0, 1] combining a span-omission ranking term, a three-axis ordinal calibration term, and an asymmetric overconfidence penalty. The headline score is the mean of the per-item scores over the test set. The two reward weights partition the positive score — W_RANK + W_AXIS = 0.40 + 0.60 = 1.0. OVERCONF is not part of that sum: it is a separate coefficient on a penalty term that is subtracted after the two weighted rewards are combined, so the three coefficients deliberately do not sum to 1. For one item: N_SPAN = 5 # fixed candidate spans A..E N_LEVEL = 5 # ordinal rating levels 0..4 per axis AXES = ["faithful", "consistent", "appeal"] W_RANK = 0.40 # reward weight; W_RANK + W_AXIS = 1.0 W_AXIS = 0.60 # reward weight; W_RANK + W_AXIS = 1.0 OVERCONF = 0.35 # SEPARATE penalty coefficient, subtracted (not part of the reward-weight sum) KERNEL_C = 0.4 # sharpness of the ordinal reward kernel 1) Omission ranking term: signed Kendall tau-b between the predicted per-span omission scores (omit_A..omit_E) and the ground-truth omission vote weights. tau-b uses only the sign of pairwise differences, so only the induced ordering matters (absolute scale is irrelevant) and ties on either side are handled. An item whose five true weights are all equal contributes 0 to this term. The tau-b is used directly (range [-1, 1]): an uninformed prediction scores ~0 in expectation and a wrong ordering scores negative, so no free credit is handed to a guess. The per-item score is floored at 0 afterwards, so a negative rank term only reduces that item. rank_term = kendall_tau_b(pred_omit_scores, true_omit_votes) 2) Calibration term: mean over the three axes of an ordinal reward kernel — the predicted probability mass, weighted by how close its level is to the truth with sharpness KERNEL_C = 0.4. Mass on the true level earns full credit, mass one level away earns 0.6, two levels away earns 0.2, and three or more earns nothing — a well-calibrated near-miss is rewarded, not treated the same as a far miss. The averaged reward is then chance-corrected: the expected reward of a constant one-hot on the centre level (2), computed under the true level marginals, is subtracted and the remainder rescaled by (1 - baseline). This centre-level baseline is CENTER_BASE ≈ 0.5133 for this collection, so an image-blind constant scores 0 on this term and a perfect one-hot scores 1. The corrected term may be negative for predictions worse than that constant; the per-item floor (step 4) handles it. axis_reward = mean( sum(pred_dist[a * max(0.0, 1.0 - KERNEL_C * abs(k - true_levela])) for k in range(N_LEVEL)) for a in AXES ) CENTER_BASE = mean( # expected reward of a centre-level one-hot sum(true_level_marginal[a * max(0.0, 1.0 - KERNEL_C * abs(2 - t)) for t in range(N_LEVEL)) for a in AXES ) # ≈ 0.5133 on this collection axis_term = (axis_reward - CENTER_BASE) / (1 - CENTER_BASE) 3) Overconfidence penalty: probability mass placed away from the true level, weighted by squared normalized distance, averaged over the three axes. penalty = mean( sum(p_k * ((abs(k - true_level[a]) / (N_LEVEL - 1)) ** 2) for k, p_k in enumerate(pred_dist[a])) for a in AXES ) item_score = max(0.0, W_RANK * rank_term + W_AXIS * axis_term - OVERCONF * penalty) The headline score is mean(item_score for item in test), clamped to [0.02, 1.0] so a valid submission never returns exactly 0. Score components (all documented, all scored): rank_term (span-omission ordering via signed tau-b in [-1, 1] between the predicted omission scores and the true vote weights, weight 0.40), axis_term (mean ordinal-reward-kernel calibration over the three axes with sharpness KERNEL_C = 0.4, chance-corrected by subtracting the centre-level one-hot baseline CENTER_BASE ≈ 0.5133 and rescaling by 1 - CENTER_BASE, weight 0.60), and OVERCONF (weight 0.35 on probability mass away from the true level, squared by normalized distance). The centre-level baseline is computed from the true level marginals, so it is a fixed property of the collection, not a submission input. Per-item scores are floored at 0 before averaging. Baseline (uniform) expected score: approximately 0.02 (the score floor). Because the axis term is chance-corrected, an image-blind constant — a uniform five-level distribution or a centre-level one-hot — earns no positive calibration credit, so after the confident-wrong penalty and the per-item floor the constant sample grades at the floor. Equal (uninformed) omission scores give rank_term ≈ 0 (signed tau-b is centered at 0). The constant sample submission — equal omission scores and uniform level distributions — grades at this baseline. Perfect predictions score ≈ 1.0. What Not To Use (Prohibited Methods) This challenge is scored against held-out human feedback. The following are prohibited: No external answer keys or precomputed feedback. Do not use any external, pre-trained preference, appeal, or reward scorer, or any published set of human ratings/omission labels for the same generated-output collection, to recover or approximate the test labels. Fine-tune your own judge on the provided train.csv only. No reverse lookup or brief matching to external sources. Do not attempt to match test outputs (by content hash, embedding nearest-neighbour, reverse lookup, or re-rendering) or test briefs back to any public generation archive, prompt/brief corpus, or human-feedback dataset to look up ratings, omission votes, or rankings. The outputs are re-encoded and metadata-stripped specifically to make such matching a violation rather than a strategy. No id-based hardcoding or structural shortcuts. Do not hardcode id- or span-label-to-rank mappings, and do not exploit span order, row order, file order, output file size, or any structural artifact of the release as a stand-in for the human judgement — spans are randomized and outputs are re-encoded to break such shortcuts. No manual labeling of the test set. Do not hand-rate the test outputs or crowdsource their ratings or omission votes. No train/test leakage or private-label tuning. Do not tune against private/answers.csv, and keep every item that shares a brief within a single split when building local folds. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Historical French OCR Palette Assignment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx766xkvts3kr3sp9tkgz320ps8brtbq
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.869!

Full challenge description from page:

> Historical French OCR Palette Assignment Overview This is a supervised Fine-Tuning challenge. Adapt a pretrained contextual language model on the supplied training routes, then use the adapted model to predict one coherent repair route for four noisy text fragments. Each record contains four historical French OCR fragments with the same observed error span marked by ..., plus a shared palette of eight possible replacement strings. Your route must assign one distinct palette candidate to each fragment, in fragment order, without reusing a candidate. An observed span is the exact string produced by OCR at the marked location. ` denotes a missing-character location, and the palette replacement ` means that the observed span should be removed. Although every fragment in a record shares same observed span, its surrounding language can license a different repair. The shared palette makes the four decisions interact: a candidate selected for one fragment is unavailable to the others. Fine-Tuning Regime An eligible entry must begin from publicly available pretrained model weights and update that model for this challenge using the labeled routes in train.csv. Full-parameter fine-tuning and parameter-efficient methods such as trainable adapters or low-rank updates are both eligible. At least one pretrained parameter or attached trainable adaptation module must be updated; training only a new prediction head over an entirely frozen pretrained representation does not meet the regime. The adapted local checkpoint must supply the contextual candidate scores used to construct each submitted route. Deterministic constrained decoding may enforce the four-distinct-candidate rule. Participants must retain a reproducible training configuration, training log, and checkpoint provenance for organizer audit; these are not additional submission columns. Evaluation For test record i, let g_i = [g_i0, g_i1, g_i2, g_i3] be the hidden route and p_i = [p_i0, p_i1, p_i2, p_i3] be the submitted route. Define the number of exact fragment assignments as: correct_i = sum(j = 0..3) 1[p_ij = g_ij] The row score is: row_score_i = (correct_i / 4)^2 The challenge score is the arithmetic mean of row_score_i over all test records. The score is not capped or compressed: it ranges naturally from 0 to 1, and the complete oracle route scores exactly 1. The quadratic weighting is intentional because the prediction target is a coupled four-fragment assignment, not four independent labels. A route with only one or two correct placements leaves most of the jointly constrained palette assignment unresolved, so it receives less credit than under a linear fraction. The possible valid-route scores are 0, 1/16, 1/4, 9/16, and 1 for zero through four correct placements. This emphasizes coherent, nearly complete repairs while, unlike an all-or-nothing route score, still distinguishing partial progress. A route is row-level malformed if it is not a JSON array of exactly four strings, repeats a candidate ID, or contains an ID outside that record's palette. A malformed row scores 0. File-level structural errors—including missing, duplicate, unknown, or extra episode_id values, or submission columns in the wrong order—cause grading to fail with a validation error. Dataset train.csv contains 5,321 outer records and 21,284 fragment-routing decisions. test.csv contains 1,040 outer records and 4,160 fragment-routing decisions. The underlying source pages are disjoint between train and test, and high-similarity contexts are excluded across splits. These controls address complementary leakage modes. Page-group disjointness prevents source-page memorization, while the five-word-shingle filter removes near-duplicate contexts even when they come from different pages. Recurring OCR spans and replacement strings are deliberately allowed because they form the transferable repair vocabulary, but they do not provide a stable label shortcut: candidate IDs are local to each episode and shuffled, and one shared observed span is paired with distinct repairs that must be assigned from four different contexts. A solver must therefore use held-out context rather than retrieve a page, reuse a global candidate-ID mapping, or match a near-duplicate training window. train.csv | Column | Type | Meaning | |---|---|---| | episode_id | string | Opaque unique record identifier. | | observed_span | string | Shared OCR string marked in all four fragments, or `` for an insertion location. | | fragments_json | JSON array | Four objects in order F0 through F3. Each object has fragment_id (string), source (the raw observed string, possibly empty), and context (the noisy text containing exactly one marked span). | | palette_json | JSON array | Eight objects in order C0 through C7. Each has candidate_id (string) and replacement (string). `` represents an empty replacement. | | route | JSON array | Four distinct candidate IDs. Position 0 repairs F0, position 1 repairs F1, and so on. | test.csv test.csv has the same first four columns as train.csv; route is withheld. sample_submission.csv | Column | Type | Meaning | |---|---|---| | episode_id | string | Must match every test ID exactly once. | | route | JSON array | Four distinct candidate IDs in F0, F1, F2, F3 order. | The sample uses [], an intentionally malformed route that scores 0 and shows where predictions belong. Populated schema example { "episode_id": "PQR-000042", "observed_span": "l", "fragments_json": [ {"fragment_id": "F0", "source": "l", "context": "...ma lson ancienne..."}, {"fragment_id": "F1", "source": "l", "context": "...une nalion entière..."}, {"fragment_id": "F2", "source": "l", "context": "...qu'il faut lire..."}, {"fragment_id": "F3", "source": "l", "context": "...appelée demain..."} ], "palette_json": [ {"candidate_id": "C0", "replacement": "ti"}, {"candidate_id": "C1", "replacement": "i"}, {"candidate_id": "C2", "replacement": "ll"}, {"candidate_id": "C3", "replacement": "l"}, {"candidate_id": "C4", "replacement": ""}, {"candidate_id": "C5", "replacement": "li"}, {"candidate_id": "C6", "replacement": "t"}, {"candidate_id": "C7", "replacement": "il"} ], "route": ["C1", "C0", "C3", "C2"] } The example illustrates the grammar only; it is not a test record or a promise that its fragments form polished modern French. Submission Submit a CSV with exactly these columns, in this order: episode_id,route Each route cell must be valid JSON. For example: episode_id,route PQR-005321,"[""C1"",""C0"",""C3"",""C2""]" Candidate IDs are local to a record. Do not assume that C1 represents the same replacement in another record. What Not To Use Do not submit a frozen-model, zero-shot, few-shot, prompt-only, retrieval-only, static-lookup, or rules-only system as the predictive entry. Such tools may support analysis, but an eligible final route must be driven by the challenge-adapted checkpoint described above. Do not train the contextual model entirely from random initialization. That is a From-Scratch regime rather than this challenge's Fine-Tuning regime. Do not look up fragments on the web, in external scanned-document collections, or in an external aligned OCR/ground-truth corpus; do not reverse-identify source pages or join records to a source release. Do not use hosted OCR-correction services, external APIs that return corrected text, external answer stores, or private retrieval indexes containing the challenge's source records. Local pretrained language-model weights and ordinary public general-language resources are allowed. Do not recover targets from organizer-private files, preparation caches, hidden answer files, source-group mappings, filenames, row order, candidate-ID hashes, archive metadata, or any stable mapping not present in the public CSVs. Do not reconstruct or replay the organizer's private source-selection, alignment, windowing, palette-construction, split, or answer-generation process, and do not join to leaked intermediate artifacts from that process. Do not manually label test records, probe the leaderboard to infer individual routes, share a test-specific answer table, or hard-code behavior for test IDs. &nbsp;
> $700 Pool
> Closes in 2h 51m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Match Speech Audio to Synchronized Vocal-Tract MRI

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e0x3awpsnhat5tcntqt2q1x8e5b56
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat gpt6astra's score of 0.756!

Full challenge description from page:

> Match Speech Audio to Synchronized Vocal-Tract MRI Overview Predict which of six silent vocal-tract MRI clips was recorded with a speech-audio query, and predict the audio/video timing offset for that match. This is a GPU fine-tuning challenge built from real speech-production recordings. Adult participants spoke prompted and spontaneous material while a midsagittal MRI sequence recorded the internal motion of the tongue, lips, jaw, velum, and pharyngeal airway. A synchronized microphone recorded speech inside the scanner. The source collection contains 2,371 recordings from 75 participants, covers 20.39 hours, uses 84 by 84 MRI frames at 83.28 frames per second, and stores mono audio at 22,050 Hz. The prepared benchmark converts those recordings into compact model-ready tensors. Every row contains: one 1.44-second speech-audio log-mel tensor; six 1.44-second silent MRI candidate sequences from the same source recording; nine possible relative timing offsets, from -120 ms through +120 ms in 30 ms steps. Exactly one of the 54 candidate-and-offset combinations is correct. Submit a calibrated probability grid over all 54 possibilities. The task models a practical synchronization and provenance problem in speech MRI: when acquisition boundaries or clocks are uncertain, identify the image interval that belongs to an audio interval and recover their relative offset. It does not ask for a transcript, a generated movie, a reconstructed waveform, or a variable-length output. The challenge domain is Fine-Tuning. A competitive solution is expected to train or fine-tune an audio encoder and a spatiotemporal MRI encoder, then score their cross-modal temporal agreement. The supplied tensor bank is sized for an NVIDIA A10G workflow and a 50–60 minute runtime budget. Objective For every row in test.csv, produce a 6 by 9 matrix of probabilities. Matrix row 0 corresponds to MRI candidate 0. Matrix row 5 corresponds to MRI candidate 5. Matrix column 0 corresponds to an audio start 120 ms before the matching MRI window. Matrix column 1 corresponds to -90 ms. Matrix column 2 corresponds to -60 ms. Matrix column 3 corresponds to -30 ms. Matrix column 4 corresponds to 0 ms. Matrix column 5 corresponds to +30 ms. Matrix column 6 corresponds to +60 ms. Matrix column 7 corresponds to +90 ms. Matrix column 8 corresponds to +120 ms. If the correct MRI sequence is candidate 2 and the query audio begins 60 ms after that candidate's image window, the correct cell is row 2, column 6. The probability values must be finite, must lie in [0, 1], and must sum to 1 over all 54 cells. How the benchmark was constructed The source recordings were decoded only once to create the distributed tensor bank. Each selected recording contributes exactly one benchmark row. For one row, the preparation pipeline performs these operations: It chooses a source recording assigned entirely to train or entirely to test through its participant. It selects a contiguous interior span with enough boundary margin for timing shifts. It extracts six non-overlapping 1.44-second MRI windows separated by 160 ms. It applies a fresh deterministic permutation to the six candidates. It chooses one candidate position and one of nine offset classes with balanced deterministic cycling. It extracts the audio query from the true source interval after applying that offset. It converts the audio to a 64 by 128 log-mel tensor and resamples each MRI candidate to 20 grayscale 48 by 48 frames. It robustly scales each view and quantizes it to unsigned 8-bit integers. No signal content is synthesized. The candidate identity is true because the audio and MRI come from the same measured source interval. Only the controlled temporal crop offset and the candidate ordering are imposed by the benchmark. Dataset files The prepared public directory contains exactly five solver-facing files. train.csv Contains 1,680 labeled-example references. It has the same feature columns as test.csv. id: string. A 20-character anonymized row ID. bank_row: integer. The first-axis index for this row in multimodal_tensor_bank.npz. train_targets.csv Contains the training targets. Its columns intentionally match the submission and private-answer schema. id: string. Training row ID. match_grid: string. JSON-encoded 6 by 9 one-hot matrix identifying the true candidate and lag. test.csv Contains 300 hidden-test references from participants absent from training. id: string. A 20-character anonymized row ID. bank_row: integer. The first-axis index for this row in multimodal_tensor_bank.npz. test.csv contains no target, source identifier, participant metadata, recording name, task name, timing coordinate, quality label, or split audit field. multimodal_tensor_bank.npz Contains two NumPy arrays and no labels. audio: uint8 array with shape (1980, 64, 128). video: uint8 array with shape (1980, 6, 40, 48, 48). For a row whose bank_row is k: audio[k] is the query log-mel tensor; video[k, c] is candidate c, where c is 0 through 5; the 40 MRI frames are in chronological order; the first tensor value corresponds to the lowest mel bin for audio and the upper-left image pixel for video. Convert values to floating point before model input. Dividing by 255 is a valid initial scaling; learned normalization is also allowed. sample_submission.csv Contains every test ID once and assigns uniform probability 1/54 to every cell. It is structurally valid and scores exactly 0. Split, independence, and leakage control The true leakage unit is the participant. All recordings from one participant remain on one side of the split. Participant assignment is deterministic. Participant keys are ordered by a fixed SHA-256 rule. The first 15 ordered participants form the test pool, and the remaining 60 form the training pool. The participant keys themselves are not released in prepared data. The final benchmark uses: 60 train-only participants; 15 test-only participants; 1,680 distinct train recordings, 28 per train participant; 300 distinct test recordings, 20 per test participant; 11,880 non-overlapping candidate source intervals in total. Every selected recording contributes one row only. Therefore two rows never share a recording, and a candidate window is never reused as a query or candidate elsewhere. Train and test have zero participant overlap, zero recording overlap, and zero interval overlap. Exact hashes are checked for every audio tensor and every candidate video tensor. A duplicate causes preparation to fail. Because every row comes from a different recording, near-duplicate leakage through overlapping crops is also structurally prevented. The held-out participants still perform task types represented in training, so the benchmark tests new-speaker cross-modal generalization without withholding the basic speech-production primitives required to learn the task. The correct cell cannot be recovered from id, bank_row, row order, filename, recording duration, or source metadata: IDs are anonymized hashes and contain no target fields. Rows are sorted by anonymized ID after targets are assigned. bank_row only locates tensors in the public bank. candidate positions and lag classes are balanced independently of public row order; source filenames, participant IDs, task labels, and absolute timing coordinates are not released; every candidate in a row comes from the same participant, recording, scanner setup, and speech task. Output grammar match_grid must be a JSON list containing exactly six lists. Each inner list must contain exactly nine numeric values. A valid low-information prediction begins like this and continues through all six rows: [[0.0185185185,0.0185185185,0.0185185185,0.0185185185,0.0185185185,0.0185185185,0.0185185185,0.0185185185,0.0185185185],...] A valid confident prediction for candidate 2 at +60 ms is: [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]] Invalid row-level predictions include: a non-JSON string; the wrong matrix dimensions; booleans or non-numeric values; NaN or infinity; a negative value; a value greater than 1; a matrix whose 54 values do not sum to 1 within absolute tolerance 0.000001. An invalid row is replaced by an all-zero internal prediction and receives worst-case credit for every metric component. It does not crash grading and does not gain an abstention advantage. Evaluation Let N be the number of evaluated rows. Let C = 6, L = 9, and K = C * L = 54. Let p_i(c,l) be the submitted probability for candidate c and lag l in row i. Let (c_i,l_i) be the true cell. Natural logarithms are used. clip(x,0,1) means min(1,max(0,x)). Joint log skill JointLogLoss = -(1 / N) * sum_i log(max(p_i(c_i,l_i), 1e-15)) JointLogSkill = clip(1 - JointLogLoss / log(54), 0, 1) Uniform probability has JointLogSkill = 0. A perfect one-hot oracle has JointLogSkill = 1. Joint Brier skill Let y_i(c,l) be 1 at the true cell and 0 elsewhere. JointBrier = (1 / N) * sum_i sum_c sum_l (p_i(c,l) - y_i(c,l))^2 UniformJointBrier = 1 - 1 / 54 JointBrierSkill = clip(1 - JointBrier / UniformJointBrier, 0, 1) Candidate marginal log skill CandidateProbability_i = sum_l p_i(c_i,l) CandidateLogLoss = -(1 / N) * sum_i log(max(CandidateProbability_i, 1e-15)) CandidateLogSkill = clip(1 - CandidateLogLoss / log(6), 0, 1) Lag marginal log skill LagProbability_i = sum_c p_i(c,l_i) LagLogLoss = -(1 / N) * sum_i log(max(LagProbability_i, 1e-15)) LagLogSkill = clip(1 - LagLogLoss / log(9), 0, 1) Joint accuracy skill A row is correct only when the true cell is the unique largest submitted value. A tie for largest value is incorrect. JointAccuracy = number of correct rows / N JointAccuracySkill = clip((JointAccuracy - 1/54) / (1 - 1/54), 0, 1) Ranking skill For each row, compare the true-cell probability with each of the other 53 cell probabilities. A strict win contributes 1, a tie contributes 0.5, and a loss contributes 0. RowRanking_i = (strict wins + 0.5 * ties) / 53 MeanRanking = (1 / N) * sum_i RowRanking_i RankingSkill = clip((MeanRanking - 0.5) / 0.5, 0, 1) Final score final_score = 0.33 * JointLogSkill 0.22 * JointBrierSkill 0.17 * CandidateLogSkill 0.10 * LagLogSkill 0.10 * JointAccuracySkill 0.08 * RankingSkill The score is deterministic, finite, and clipped to [0, 1]. The uniform sample scores exactly 0. The known-answer one-hot submission scores exactly 1. Submission format Submit submission.csv with exactly two columns in this order: id: string copied from test.csv. match_grid: JSON-encoded 6 by 9 probability matrix. Example: id,match_grid 0a12bc34de56f789abcd,"[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]" The CSV must contain every test ID exactly once. The grader aligns by id, not by row order. Missing IDs, duplicate IDs, unknown IDs, extra rows, missing columns, extra columns, or wrong column order are structural errors and are rejected. Recommended modeling direction A useful baseline extracts an audio activity trajectory and compares it with frame-to-frame MRI motion at several offsets. A stronger system should learn phonetic and articulatory representations rather than rely only on global energy. Viable A10G approaches include: a pretrained speech encoder plus a compact 3D CNN or video transformer; contrastive audio-to-articulation pretraining on the 1,680 labeled rows; cross-attention over audio time bins and MRI frames; hard-negative training across the six same-recording candidates; temperature calibration on participant-held-out validation speakers. Because all six candidates share speaker, scanner, recording, task, and duration, speaker recognition, transcript identification, and clip-length matching do not solve the row. What not to use Do not search for source filenames or participant identities; they are not present in prepared files. Do not infer the answer from id, bank_row, CSV order, tensor-bank order, or candidate position. Do not assume one fixed lag or candidate index; both axes are balanced. Do not use source recording duration or task labels; neither is released. Do not treat the six candidates as independent examples from different speakers. They are intentionally same-recording hard negatives. Do not submit transcripts, class labels, row-local explanations, generated audio, generated video, or more than the two required CSV columns. Benchmark boundary Acoustic-to-articulatory inversion predicts a continuous articulator trajectory from speech. MRI-to-speech systems synthesize or reconstruct audio from imaging. Visible-face synchronization benchmarks match speech to external lip motion. Generic audio-video retrieval usually distinguishes different scenes, speakers, or semantic events. This benchmark has a different prediction object: a calibrated joint posterior over an internal-articulation source interval and a fine timing offset. Its negatives are six non-overlapping intervals from the same MRI recording, and its held-out unit is the complete participant. The required capability is simultaneous cross-modal binding and temporal calibration under speaker-disjoint evaluation, not transcription, generation, lip reading, ordinary synchronization classification, or unconstrained retrieval.
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Polish-language Landmark Evidence Dossiers

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79ejm251ke3375jny9rm905d8dz83q
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat amtech's score of 76.891!

Full challenge description from page:

> Polish-language Landmark Evidence Dossiers Overview Build a GPU-fine-tuned Polish-language system that assembles a complete, source-grounded spatial dossier for a highlighted object occurrence. A travel-information editor is importing narrative descriptions into a searchable knowledge base. A sentence may locate a bridge relative to a stream, describe the stream flowing through a valley, and place another object near one part of a building. Merely finding place names or a preposition is insufficient: importing the wrong attachment can assign the stream's movement to the bridge, or discard a qualifier that changes which part of a building is meant. You receive a naturally written Polish passage and the token positions of one highlighted object occurrence. Return every spatial statement involving that occurrence, with its complete attachment structure and textual evidence. Keep statements in which the object is being located, is moving, or serves as a reference or path object for something else. Keep the other participants and qualifiers needed to interpret each selected statement. The output is an evidence dossier, not geographical ground truth. Do not invent coordinates, infer routes that the passage does not state, resolve other occurrences solely because they have the same name, or translate a relative description into a new geographic claim. The complete solution must run on single NVIDIA A10G with 24 GB VRAM within 90 minutes, including training, validation, inference and writing the submission. Dataset dataset/public/ ├── train.csv ├── test.csv └── sample_submission.csv The release contains 2,058 training queries from 825 passages across 68 narrative bundles, and 900 test queries from 433 passages across 27 additional bundles. Each row is one query. These three CSVs are the complete supplied data. The files use UTF-8. The sequence columns are JSON strings inside CSV cells. Structural limits are listed under Submission format below. train.csv id,bundle_id,passage_id,words,sentences,focus,evidence | Column | Meaning | |---|---| | id | Opaque identifier of one query. | | bundle_id | Opaque narrative-family identifier. Use it for grouped validation. | | passage_id | Opaque passage identifier. Queries can share a passage but highlight different occurrences. | | words | Ordered JSON array of Polish tokens, including punctuation. | | sentences | JSON array of [start,end] sentence intervals. Indices are zero-based and end is exclusive. The intervals partition words. | | focus | Sorted JSON array of token indices for the highlighted entity occurrence. | | evidence | A JSON object containing copied query context and the complete dossier in its paths field, as described below. | bundle_id and passage_id express grouping, not semantic categories. A bundle identifies related narrative material: all passages and highlighted occurrences from the same narrative belong to one bundle, together with detected exact duplicates and strongly overlapping narrative versions. Training and test contain disjoint bundles. Queries within a bundle can share context and are correlated, so the row count is not a count of independent narratives. Keep a whole bundle on one side of any local validation split. Evaluation averages query scores within passages and passage scores within bundles before giving each bundle equal weight. The released training and test inputs contain no identical complete passages after case normalization. Across all training–test passage pairs, the largest Jaccard similarity between sets of consecutive five-token sequences is 0.0667, rounded to four decimal places. This measurement uses the supplied words tokens, including punctuation, with each token casefolded; for two sets of five-token sequences, Jaccard similarity is the size of their intersection divided by the size of their union. These observations provide evidence against verbatim passage reuse and extensive shared wording. The intended generalization is to unseen narrative content within the same Polish-language domain. Vocabulary and grammatical constructions may recur. Predictions must recover the highlighted occurrence's evidence spans, semantic roles, and complete attachment structure in its particular context. Bundle separation and low textual overlap do not, by themselves, establish resistance to reusable linguistic templates or guarantee that surface-pattern methods will perform poorly. test.csv id,bundle_id,passage_id,words,sentences,focus The columns have the same meaning as in train.csv. Predict the dossier for each query. Every query has at least one relevant spatial statement. You may abstain by setting paths to an empty array, but abstention receives no credit. Evidence cell Each evidence cell in training data and submissions is a JSON object with exactly these five fields: { "bundle_id": "b_example", "passage_id": "p_example", "word_count": 8, "focus": [3], "paths": [] } bundle_id: copy the query's public bundle_id exactly. passage_id: copy the query's public passage_id exactly. word_count: the integer length of the query's words array. focus: copy the query's public token-index array exactly. paths: the predicted evidence paths, using the format below. The first four fields are supplied context. The sample submission includes them for every query, so a solution can replace only paths. They earn no prediction credit. A row with altered or missing context receives zero credit. Training cells use this same object format with their labeled paths. Evidence vocabulary A node anchors a semantic component to one or more tokens: {"kind":"entity","at":[3]} at is a nonempty sorted list of distinct token indices. It is a list of actual included positions, not a start/end interval. This permits multiword and discontinuous evidence. A node is identified by both its kind and its token-index list; token overlap between different kinds is permitted. | kind | Meaning | |---|---| | entity | A physical object, place, or referential expression functioning as an object in a spatial statement. A pronoun or a verb carrying an implicit subject can provide its textual anchor. | | position | An expression establishing a static spatial relation, often a preposition or a multiword expression. | | movement | An expression of motion or a change of location. | | route | An expression introducing an origin, destination, or traversed path of motion. | | part | A relative part or region of an object, such as its top, back, edge, or interior. | | bearing | An expression of absolute or relative direction. | | distance | An expression of spatial separation or extent. | Use the smallest expression that carries the annotated function, following the boundary conventions demonstrated in train.csv. Do not automatically expand an entity to its entire surrounding noun phrase. Retain function words inside multiword relation, direction, or distance expressions when they belong to that component. Do not fabricate an unexpressed word to represent an implicit participant. Directed attachments have three roles: | Role | Meaning | |---|---| | figure | The object or region being located or moving relative to the governing expression. | | reference | The object or region used to locate another participant. | | detail | A dependent spatial component, including a motion-path introducer, its object, a part's carrier, a direction, or a distance, as determined by its attachment. | A card represents one governing spatial expression together with all of its outgoing spatial attachments. Its root is normally a position or movement node. A standalone part, route, or entity can also govern a card when no enclosing relation expression is present—for example, an object with a directly attached direction phrase. Which statements belong in a dossier? Select a card when the highlighted entity occurrence appears anywhere in its outgoing attachment structure. Then return all branches of that card, including branches that do not themselves visit the highlighted entity. A shared object does not merge distinct governing statements. Do not follow a new incoming statement through another participant just because that participant is mentioned in a selected card. Conversely, when the highlighted occurrence participates in two different statements, include both cards—even when it has different roles in them. Preserve nested attachment. A relation pointing to a part which in turn points to an entity is not equivalent to a direct relation pointing to that entity. Do not flatten paths, merge repeated surface strings at different positions, omit modifiers, or add geometrically plausible but unstated links. Representing a card as evidence paths The paths field is a JSON array of maximal root-to-leaf paths. Each path alternates between node objects and role strings: [node, role, node, role, node, ...] Each path has at least one attachment. Paths with the same root node belong to the same card. Include every maximal path of the card's directed attachment graph. Shared prefixes are repeated in the serialization; they do not create duplicate evidence. A path that is only a prefix of a longer path is not separately included. The ordering of paths and the ordering of keys inside a node object do not matter. Token indices, kinds, role labels, attachment direction, and path structure do matter. Worked example This illustrative passage has these tokens: ["Mostek","leży","nad","strumieniem","płynącym","przez","dolinę","."] For focus = [3], the stream occurs in two statements. The complete paths value is: [ [ {"kind":"position","at":[2]}, "figure", {"kind":"entity","at":[0]} ], [ {"kind":"position","at":[2]}, "reference", {"kind":"entity","at":[3]} ], [ {"kind":"movement","at":[4]}, "figure", {"kind":"entity","at":[3]} ], [ {"kind":"movement","at":[4]}, "detail", {"kind":"route","at":[5]}, "detail", {"kind":"entity","at":[6]} ] ] The first two paths form a position card. The last two form a movement card. Notice that two of the returned paths do not contain token 3: they are needed to complete the selected statements. For focus = [0], return only the two position-card paths. The bridge's dossier must not acquire the stream's movement merely because the stream is its reference object. sample_submission.csv id,evidence It contains an evidence object for every query with copied public context and "paths": []: a valid abstention baseline. Replace the paths array with predictions while retaining the other four fields. A bare [] is not a valid evidence cell. The sample contains no predicted statement counts, roots, or paths. Submission format Write: working/submission.csv The CSV must include these columns with these exact names: id,evidence Include each test id exactly once. Row and column order are arbitrary. Extra columns are ignored; the sample's two columns are sufficient. Use an ordinary CSV writer so that quotes and commas inside JSON are escaped correctly. Put only the documented evidence object in each evidence cell. Each cell must follow the five-field evidence-object schema above. JSON object-key order and path order do not affect scoring. The complete cell, including context, is limited to 150,000 Unicode characters. The structural limits are: At most 384 input tokens per query. Between 1 and 24 distinct token indices per node. Between 0 and 96 paths per dossier. Between 1 and 6 attachments per path. At most 192 distinct nodes and 32 cards per dossier. Token indices must be JSON integers, not booleans, floating-point numbers, or strings, and must be in [0,len(words)). Node keys must be exactly kind and at. All kinds and roles must be from the tables above. A root cannot be a bearing or distance node. Duplicate paths, duplicate JSON object keys, cycles, invalid indices, nonstandard NaNInfinity, or inconsistent path collections are invalid. Every nonempty predicted card must include the supplied entity occurrence. The maximal-path requirement is checked against the predicted card graph, not against an expected number of statements or branches. An internally consistent prediction that misses a true branch is a prediction error, not a format error. A missing or repeated required column, missing/duplicate/unexpected ID, or malformed CSV makes the submission score zero. An invalid evidence cell receives zero credit for that query; other queries are still scored. Values are never repaired or clipped. Evaluation Let P be the set of predicted paths from evidence.paths and G the set of expected paths for a query. Only the paths are scored; the copied context must first pass validation. A path matches only when every node's kind and token list and every directed role are exact. For finite sets, define: F1(A, B) = 2 × |A ∩ B| / (|A| + |B|) The value is 1 when both sets are empty. Expected dossiers are nonempty, so a valid object with "paths": [] scores 0. Group a dossier's paths by their root node. Each resulting set of paths is a card. Two cards match only if their entire path sets match, including the root and all participants and qualifiers. The three query-level components are: path_f1 = F1(predicted paths, expected paths) card_f1 = F1(predicted complete cards, expected complete cards) dossier_exact = 1 if P == G, otherwise 0 query_score = 0.30 × path_f1 0.45 × card_f1 0.25 × dossier_exact This rewards correct individual evidence branches, gives more credit to statements that can be imported intact, and separately rewards an exhaustive, uncontaminated object dossier. Extra guesses hurt precision. Listing every nearby object or attaching each preposition to every candidate is not free recall. Average query scores within each passage_id; average those passage scores within each bundle_id; then take the unweighted mean over bundles and multiply by 100. A long narrative or a passage with several highlighted objects therefore does not dominate the score. Not allowed External APIs or remotely hosted inference. Additional annotated spatial-language data, matching passage annotations obtained elsewhere, or models specifically trained to reproduce such annotations. Searching for the passages online, matching them against an external corpus, or importing externally obtained answers. Manual annotation of test passages, hard-coded predictions by identifier, or exploiting identifiers, file order, serialization artifacts, or evaluation behavior instead of language understanding. A CPU-only, dictionary-only, or rules-only main predictor. GPU use must train and run the contextual evidence model, not serve as a nominal extra operation around an otherwise unrelated solution. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Where Pronunciation Of Reviewers Disagree

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72gcqtm3xd9k3vn7ngt0k8hh8dxczm
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shikum's score of 0.414!

Full challenge description from page:

> Overview Given an English recording and its expected words and speech sounds, predict exactly where each of five reviewers marked an error. Return one structured review map: five yes/no decisions at each reference sound and at each gap where an extra sound could have been inserted. A pronunciation tutor should not give the same feedback when reviewers disagree about whether a sound is wrong and when they agree that a word contains a problem but locate it differently. Whole-word scores lose that distinction. Here the learning task preserves the location and the individual human judgment, without treating the majority as unquestionable truth. The recordings are complete read sentences from Mandarin-first-language children and adults. Five experts independently annotated speech sounds. Parenthesized reference sounds are marked incorrect or omitted; square-bracketed sounds are insertions; accented but accepted sounds are not errors. These annotations align to the expected sound sequence. There are no manually invented error locations, synthesized voices, or forced-alignment timestamps used as hidden truth. Dataset | Public item | Contents | |---|---| | train.csv | 4,000 labeled recordings: case_id, audio_path, words, reference_phones, phoneme_review | | test.csv | 1,000 recordings: case_id, audio_path, words, reference_phones | | sample_submission.csv | One all-zero review map per test ID, using the visible reference lengths; columns case_id, phoneme_review | | train_groups.csv | case_id, group; connected training-source groups for local validation, not model features | | audio/ | 5,000 complete mono WAV recordings, 16-bit PCM at 16,000 Hz | Audio paths are relative to the public directory, for example audio/u_bb1a74d51bae36753c96857f.wav. Each file contains one read sentence, not a concatenation of isolated word clips. | Column | Data type | Meaning | |---|---|---| | case_id | string | Opaque identifier; copy it exactly for submission alignment. | | audio_path | string | Relative WAV path. | | words | JSON-encoded array of strings | One to ten expected words, in spoken order. Repeated words occupy separate positions. | | reference_phones | JSON-encoded array of string arrays | One expected ARPAbet sound sequence per word, with one to twelve sounds. Digits in vowel tokens indicate lexical stress, not quality scores. | | phoneme_review | JSON-encoded nested array of strings | Training target. One array per word, containing five-bit site masks as defined below. | | group | string | Opaque validation component supplied only in the separate train_groups.csv file. | After removing phoneme_review, the training feature schema exactly equals the test schema. Reference sounds describe what was requested, not what any reviewer heard. No reviewer markup or observed pronunciation is exposed in those inputs. Sound Sites and Review Maps For a word with m expected sounds, there are exactly 2m+1 sites. Their order is gap before sound 1, sound 1, gap before sound 2, sound 2, ..., sound m, gap after sound m. With zero-based indexing, sound j occupies site 2j+1; the gap before it is site 2j. Each site is a string matching [01]{5}. Bit positions refer to reviewers 1 through 5 in a fixed order across the collection: At a sound site, 1 means that reviewer marked the expected sound as incorrect or omitted. At a gap site, 1 means that reviewer marked one or more inserted sounds at that location. 0 means no such error was marked. Accepted accent variation remains 0. Multiple inserted sounds in the same gap produce one bit, not a count. A mask with one through four positive bits represents disagreement at that exact location. Both 00000 and 11111 represent agreement. No phonetic replacement string, free-text explanation, or timestamp must be generated. For example, with words ["BEAR"] and reference_phones [["B","EH0","R"]], the seven sites are g0, B, g1, EH0, g2, R, g3. The map [["00000","00000","00000","10010","00001","10010","00000"]] says reviewers 1 and 4 flagged EH0 and R, while reviewer 5 marked an insertion between EH0 and R. All five reviewers did not simply make the same whole-word judgment. Composition and Isolation There are 200 training speakers and 50 test speakers. Whole connected components join same-speaker recordings, repeated normalized sentence text, exact/trimmed waveform duplicates, shared non-silent excerpts, and verified high-correlation near duplicates before splitting. No component or exact decoded waveform crosses the train/test boundary. The training split contains 191 validation components. The 4,000/1,000 recording split is preserved from the preceding release. These are repeated observations from 250 speakers, not 5,000 independent speaker identities. | Annotation unit | Training | Test | |---|---:|---:| | Word positions | 25,444 | 6,372 | | Sound and gap sites | 175,984 | 44,722 | | Words with any marked error | 5,926 | 1,407 | | Sites with reviewer disagreement | 8,531 | 2,134 | Positive site counts for reviewers 1 through 5 are [3952,6289,4548,4666,3994] in training and [1082,1592,1263,1333,1228] in test. These are sparse, correlated labels, not independent recordings. Submission Format Write ./working/submission.csv with exactly case_id,phoneme_review, in that order. Include each test ID exactly once; row order is unrestricted. | Column | Required type and constraints | |---|---| | case_id | String: u_ followed by 24 lowercase hexadecimal characters. | | phoneme_review | JSON-encoded string; one to ten word arrays; each word has 3 to 25 sites, an odd count, matching its public reference length. Each site is a five-character binary string. The entire field is at most 2,200 characters. | A valid illustrative record is: | case_id | phoneme_review | |---|---| | u_bb1a74d51bae36753c96857f | [["00000","00000","00000","10010","00001","10010","00000"]] | CSV writers must quote the JSON field because it contains commas. This example explains syntax, not a test label. Wrong array lengths, non-string bits, unquoted numeric masks, booleans, malformed JSON, or overlong fields receive zero credit for that recording. A field is bounded before JSON parsing. Extra, missing, reordered, or duplicate columns; wrong row counts; and duplicate, missing, or unknown IDs reject the submission. The grader accepts 1 to 100,000 evaluated rows. When backend metadata is present, submission and answers must still have identical schemas, with visibility only in the final position. Solvers submit only the two documented columns. Evaluation The Localized Reviewer Evidence Score is S = 0.50 R + 0.30 D + 0.20 W. Minimum score: 0.0. Maximum score: 1.0. Higher is better. | Component | Weight | Purpose | |---|---|---| | Reviewer error-site F1, R | 50% | The main task: locate each reviewer's errors, not just count them or identify the affected word. | | Disagreement-location F1, D | 30% | Distinguish sites with divided judgments from sites with agreement, including unanimous errors. | | Affected-word completion, W | 20% | Reward an entirely usable local review map, including correct insertion gaps and unmarked sounds. | For reviewer r, pool their bits over every site of every test word. F1_r = 2 TP_r / (2 TP_r + FP_r + FN_r) and R = (F1_1 + ... + F1_5)/5. These are ordinary binary counts; a sound and a gap each contribute one site. Reviewers have equal weight. For D, a site is positive exactly when its mask contains between one and four 1s. Pool those binary decisions over all sites and compute D = 2 TP_D / (2 TP_D + FP_D + FN_D). A mask that flags the wrong reviewers can receive D credit if it correctly identifies a disputed location, but loses reviewer-specific credit in R. Let A be the set of true words containing any marked error. W = sum over w in A of I(predicted complete site-array equals true site-array) / |A|. Complete equality includes all sounds, gaps, and reviewer bits. If A is empty in a defensive evaluation subset, W is exact-word accuracy over all words instead. I is one when its statement is true and zero otherwise. A malformed recording supplies no true-positive or completion credit. Every true positive site is a false negative. In addition, each word contributes one false positive to each reviewer's counts and one false positive to D. Thus malformed values never receive a favorable empty-positive fallback. For any F1 whose denominator is zero, its value is 1: there are no true or predicted positives and no malformed penalties for that component. Invalid hidden labels raise an error rather than being repaired. The components are computed over the complete evaluated table, not averaged independently per recording. No inverse-frequency weights, text matching, or undocumented consistency bonus is used. Simple Modeling Approach Align the supplied words and expected sounds to the audio, then encode short sound-centered and gap-centered spans. Train five sigmoid outputs per site with the provided masks. A frozen general-purpose speech encoder with small trained heads is a straightforward starting point; use grouped validation to select thresholds. Preserve sound-site and reviewer order when writing JSON. Temporal alignment is an optional modeling aid, not part of the submission. What Makes This Interesting Whole-word detection cannot distinguish a vowel dispute from an inserted consonant in the same word. Recovering those alternatives requires localized acoustic evidence and the pattern of human judgments. Disagreement is retained as the observation to model, not removed as annotation noise. This changes the granularity of the task; it does not claim a newly collected corpus or that individual reviewers are perfectly predictable. What Not To Use Do not derive judgments from IDs, filenames, hashes, file length, row order, or other packaging artifacts. Do not retrieve original annotations by matching recordings or transcripts to an external copy, or use a checkpoint specifically trained on this evaluation collection. General-purpose speech encoders, pronunciation lexicons, and forced alignment are allowed. Use training groups for validation. Do not use hidden-label feedback, repeated leaderboard probing, or malformed submissions to infer answers. The expected transcript is legitimate input; external lookup of its source review is not. Reference Validation Two standalone preparations from the unchanged raw ZIP produced byte-identical output. The release audit checked all 5,000 detailed records against the original word judgments: pooling a reviewer's localized error bits exactly recovers their previous word-level error decision. Tests reject extra rows and columns, duplicate IDs, and schema errors; malformed values score zero. Progressively removing correct error marks decreases the score. Exact answers score 1.00000. The all-zero sample scores 0.00000. A public-training-only word/site-frequency baseline scores 0.12772. These are current-version checks, not a strong-model ceiling. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Italian Wordwise Speaker-Routed Phoneme Alignment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79qf2wcpnz6s5rs7b94khhg98c5ysy
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat spyrant's score of 0.505!

Full challenge description from page:

> Background Speech alignment becomes ambiguous when two people pronounce the same words simultaneously. A transcript identifies neither the intended voice nor its timing, and recognizing the mixture alone can combine phones from different speakers. This benchmark studies voice-conditioned phonetic alignment under lexical interference, using supplied word and phone annotations. Relationship to published tasks: Here both contributors realize the same lexical sequence, so assigning a unique word token to a speaker discards the competing realization. The query deliberately switches its requested voice at word boundaries and must preserve that voice's phones and exact timing. A valid system must retain both overlapping realizations, ground each query reference acoustically, and route phone spans by word. Composing speaker extraction and alignment is a permitted baseline, but its intermediate outputs must preserve this multiplicity and support changing enrollment within a query; a single-speaker alignment or corrected word-speaker label sequence is insufficient. The benchmark claims this combined evaluation protocol, not a new alignment algorithm or an unmeasured failure of existing systems. Overview Given a mono 16-kHz mixture, an ordered list of 2–3 words spoken by both contributors, and an ordered list of voice-reference recordings, one for each word, return the phone identities and time boundaries of the requested speaker for each word. Each reference contains different sentence content and is never a target utterance. No reference transcript is supplied. Reference position j specifies which speaker to follow for word j; the requested voice changes within every query. Every mixture has two queries with identical audio and words but complementary wordwise voice selections and different target alignments. Speakers receive independent duration changes and onset offsets before mixing. A solution must bind each word-specific reference to its acoustic stream, switch the selected voice across words, resolve the realized phones, and align them to the mixture clock. A single fixed-speaker extraction and alignment does not produce the required mixed-speaker target. Return only the phones of the selected voice for each word. Phone labels come from the native LEXI phoneme tier; word association follows the native word intervals. Timing is transformed by the exact realized duration ratio and added onset offset. These are controlled mixtures of real annotated speech, not recordings of spontaneous conversations or newly synthesized phone labels. Fine-tune a general-purpose pretrained speech or audio component on the supplied training data. The offline training and inference budget remains 90 minutes on one NVIDIA A10G GPU with 24 GB VRAM. Dataset Information (Public Files) All data available for local development and prediction resides in the public directory. The CSV files enumerate the prepared mixture queries. The recordings contain four speakers; two are reserved for evaluation. Plaintext +-----------------------+--------------------------------------------------------------+ | File / Directory | Description | +-----------------------+--------------------------------------------------------------+ | audio/ | 16-kHz mono mixtures and separate voice-reference WAVs. | | train.csv | Supervised mixture queries with reference audio and alignments.| | test.csv | Evaluation mixture queries without target alignments. | | sample_submission.csv | Template demonstrating the mandatory CSV submission format. | +-----------------------+--------------------------------------------------------------+ Generalization & Split Protocol Speakers and sentence content are both held out: two voices are assigned to training and two different voices to evaluation. A deterministic seeded partition assigns 75 of 100 sentence identities to training and 25 to evaluation. Recordings are included only when both their speaker and sentence belong to the same split; every repetition stays with that sentence. The split is fixed before mixtures are constructed. Three sentence identities per split are reserved exclusively for enrollment and excluded from mixtures. Each voice reference is a 2–5 second segment from a reserved utterance, with no transcript supplied. Evaluation references identify unseen voices and are not labeled adaptation data. Both complementary queries of every mixture remain in one split. Overlapping consecutive 2–3 word windows are considered. Only chunks with identical ordered words, sentence ID and repetition across the two speakers are mixed. Each voice is duration-resampled with rate 0.96–1.04, offset by 0–160 ms in 10-ms increments, RMS-normalized to 0.12, and independently gain-scaled by 0.95–1.05. The maximum resulting mixture duration is 5 seconds. Native phone boundaries are scaled by the actual sample-count ratio, shifted, and rounded to 10-ms frames. Low-to-medium degradation applies to mixtures and references: one echo delayed by 200–599 samples (12.5–37.44 ms) with gain 0.03–0.08; sinusoidal amplitude modulation at 4–15 Hz ranging from 0.92 to 1.0; one adjacent-sample filter with weight 0.01–0.04; Gaussian noise at 32–40 dB relative to input RMS; and zero or one dropout lasting 32–80 samples (2–5 ms). Clipping uses the larger of eight times input RMS and 99.5% of the current peak. Only peaks above 0.95 are rescaled. Quiet recordings are not amplified to full scale. Use float32 waveform processing and clamp positive quantities before logarithms. Feature Schema train.csv and test.csv +-----------------+---------+-----------------------------------------------------------+ | Column | Type | Description | +-----------------+---------+-----------------------------------------------------------+ | id | String | Opaque unique query identifier. | | audio | String | Relative path to the two-speaker mixture WAV. | | reference_audio | JSON | JSON list of voice-reference WAV paths, one per word. | | words | JSON | Ordered 2–3 words spoken by both contributors. | | duration_frames | Integer | Mixture duration in 10-ms frames. | | alignment | JSON | Train only: Word-routed timed phones on the mixture clock. | +-----------------+---------+-----------------------------------------------------------+ Alignment Target Convention For word j, use the j-th path in reference_audio to identify the requested speaker, then include only that speaker's native phones associated with word j. Each routing includes both contributors. The paired query selects the other contributor at every word position. Pairs whose routed phone starts would violate chronological word order are excluded. No averaging of speaker boundaries is used. The target alignment is an ordered JSON list of tuples formatted as: $$\left[\text{wordindex}, \text{phone}, \text{startframe}, \text{endframe}\right]$$ word_index ($\text{int}$): Zero-based index ($0, 1,$ or $2$) corresponding to the element in words. Midpoint association is strictly followed: a phone belongs to the lexical word interval that encompasses its temporal midpoint $\frac{a + b}{2}$. phone ($\text{string}$): Phonetic symbol string (1 to 16 characters) matching the native training lexicon . Silence and pause markers (sil, sp, pau, #) are excluded. start_frame, end_frame ($\text{int}$): Integer boundaries in 10-ms frame units ($100\text{ Hz}$ resolution). Boundaries satisfy $0 \le \text{startframe} < \text{endframe} \le 501$. Ordering: Tuples must be sorted chronologically by non-decreasing start_frame and non-decreasing word_index. Up to 60 phonetic entries are permitted per clip. Evaluation Metrics Submissions are evaluated using an optimal bipartite temporal matching score that balances phonetic accuracy, lexical association, and boundary precision. 1. Interval Pair Quality Let $p = (w_p, ph_p, s_p, e_p)$ denote a predicted phone interval and $t = (w_t, ph_t, s_t, e_t)$ denote a ground-truth target interval. The affinity score $q(p, t)$ is non-zero if and only if both the lexical assignment and the phonetic token match exactly: If the word indices or phone strings differ, q(p,t) = 0.0. Otherwise, q(p,t) = exp(-(abs(s_p-s_t) + abs(e_p-e_t)) / 8). Start and end values are measured in 10-ms frames. The decay parameter ($8$ frames, corresponding to $80\text{ ms}$) exponentially penalizes temporal misalignment while providing smooth partial credit for near-boundary predictions. 2. Global Bipartite Assignment For an instance with $P$ predicted intervals and $T$ reference intervals, a cost matrix $C \in \mathbb{R}^{\vert{}P\vert{} \times \vert{}T\vert{}}$ is formed where $C_{ij} = -q(p_i, t_j)$. The optimal one-to-one assignment $\pi$ is computed via the Hungarian algorithm (linear sum assignment) to maximize total temporal overlap: $$\text{Sim}{\text{total}} = \sum{(i, j) \in \pi} q(p_i, t_j)$$ 3. Row Score The instance-level score is computed as a normalized harmonic balance: $$\text{Row Score} = \frac{2 \times \text{Sim}_{\text{total}}}{\vert{}P\vert{} + \vert{}T\vert{}}$$ An empty prediction set ($\vert{}P\vert{} = 0$) receives a score of $0.0$. All predicted intervals inflate the denominator $\vert{}P\vert{} + \vert{}T\vert{}$. Consequently, predicting extraneous, duplicate, or hallucinated phones heavily penalizes precision. 4. Final Score The overall benchmark score is the unweighted arithmetic mean of the row scores across all evaluation cases listed in test.csv: $$\text{Final Score} = \frac{1}{N} \sum_{k=1}^N \text{Row Score}_k$$ The score ranges strictly from $0.0$ to $1.0$, with higher scores indicating superior temporal and phonetic recovery. Sample Submission Format Submissions must be packaged as a UTF-8 CSV file containing exactly two columns in this order: id,alignment. Every test instance from test.csv must appear exactly once. JSON arrays must be quoted using standard CSV quoting conventions (wrapping the entire field in double quotes and escaping internal quotes with ""). Code snippet id,alignment 588fce89b8668ae1c3cb2851,"[[0,""uw"",8,12],[0,""n"",12,18],[1,""p"",18,29],[1,""ao"",29,61]]" 7a10be39c4451fa89012c801,"[[0,""d"",4,9],[0,""a"",9,16],[1,""k"",16,24],[1,""a"",24,35]]" 99cb4812a00192cc7711ea02,"[]" Parsing Bounds & Rejection Rules Header & Identifier Integrity: The header must match id,alignment exactly. Missing, duplicated, or unobserved test IDs result in an immediate submission score of $0.0$. Payload Size Constraints: The serialized string in the alignment cell must not exceed 6,000 characters. Array Capacity: An alignment list may contain at most 60 intervals. Interval Integrity: Each element must be a 4-element list $[w, ph, s, e]$ where $w \in 0, 1, 2$, $ph$ is a string (length 1–16), and $s, e$ are non-negative integers with $s < e \le 501$. Monotonicity: Intervals must maintain non-decreasing start times ($s_{i} \le s_{i+1}$) and non-decreasing word indices ($w_{i} \le w_{i+1}$). Duplicate identical entries are prohibited. Row Fallback: Any parsing exception, schema mismatch, or structural syntax error assigns a score of $0.0$ to that row, while other rows are evaluated normally. What Not To Use To guarantee a fair evaluation of representation fine-tuning and sequence modeling under resource-constrained settings, the following are strictly prohibited: No External Italian Speech Corpora: Do not ingest supplementary Italian read-speech databases (e.g., Common Voice Italian, CLIPS, APBI) or external forced-alignment labels. No Pre-Aligned or Forced-Alignment Checkpoints: Checkpoints explicitly pretrained for phonetic alignment or forced alignment (e.g., Montreal Forced Aligner pre-packaged Italian acoustic models) are prohibited. Fine-tuning must start from general-purpose speech representations (such as self-supervised acoustic encoders or general ASR backbones). No External Web Services or APIs: Hosted speech recognition APIs, cloud alignment endpoints, and online pronunciation lookups are disallowed. No Hidden-Label Retrieval: Do not retrieve external copies of evaluation recordings or annotations, recover private identities, or access held-out timing labels. No Test-Time Adaptation: Pseudo-labeling, transductive clustering across test instances, or test-time adaptation strategies are strictly forbidden; evaluation instances must be processed independently during forward inference. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Firestone Mechanism Phrase Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx709ak99fsrkv2rhz61wn0ng58brxnx
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat kingednut's score of 0.965!

Full challenge description from page:

> Firestone Mechanism Phrase Ranking Overview Long before matches, people could produce hot sparks by striking flint against iron pyrite or, later, steel. Museum catalogues record these percussion systems alongside fire drills, tinder containers, fire pistons, chemical matches, and mechanical igniters. When catalogue exports are damaged, a few short phrases may detach from the sentence that explained an object's construction or operation. For every test row, rank the four phrases most likely to fill the indicated gap in a fire-making catalogue description. Each row contains a title sketch, a masked description with several numbered slots, and 12 candidate phrase cards for the indicated focus_slot. Exactly one card preserves the authentic human-authored phrase. The other 11 keep the same three-token shell and replace only its center lexical alias. Return the four most plausible card IDs in descending order. A useful model must learn ordered contextual compatibility. The candidate centers are aliases that serve as authentic targets elsewhere in the same split. Candidate construction is role-conserved: for every time an alias is authentic, it is used exactly 11 times as a decoy. Consequently, alias identity, candidate position, phrase length, shared-word overlap, row ID, and fixed card priors do not identify the answer. Content words are mapped into a stable 65,536-bucket collision vocabulary such as lex_3a9f. Function words, punctuation, gap order, and sentence structure remain visible. Raw content words and catalogue identifiers are withheld; external source matching remains prohibited, and aliasing is not a guarantee of irreversibility. Related records are joined by complete transitive components built from both source text and the released-style title-plus-masked-description representation. Every detected similarity edge is retained regardless of component size, and each complete component stays on one side of the train/test split. This is a Fine-Tuning challenge on one NVIDIA A10G. Solutions must update a local sequence model's trainable parameters using train.csv. A compact Transformer or recurrent cross-encoder is sufficient; no hosted model is needed. Dataset Read challenge inputs from the public directory passed to your solution. train.csv: labelled focal-gap ranking rows. test.csv: held-out focal-gap ranking rows from disjoint source records. sample_submission.csv: a valid zero-information ranking generated from opaque row hashes. dataset_metadata.json: shared instruction, actual generated row/source/group counts, feature and prediction column lists, card vocabulary, rank length, and training/validation conventions. It contains no test targets. The supplied corpus currently produces 5,216 training rows from 941 source records and 1,197 test rows from 192 source records. These are focal-gap views, not 6,413 independent documents. Counts are recorded dynamically in dataset_metadata.json; preparation requires more than 1,000 rows per split and a test/train ratio between 0.15 and 0.25. Every view of one source record stays on the same train/test split and the same public/private board. The metric gives each source record equal weight. Component construction uses character 3-5-gram cosine links at similarity >= 0.80, including links computed on the exact released-style context before splitting. The current release has 773 complete components. As a leakage audit, preparation independently recomputes nearest train/test similarity on the final released contexts with both char and char_wb analyzers and refuses export if any test source reaches 0.84. In this release, zero test sources reach that boundary; the observed maxima are 0.7738 and 0.7990, respectively. The threshold and audit are split controls, not labels or prediction features. Columns id string): opaque identifier of the form spark__. The first hexadecimal segment groups views of one record for scoring; it does not encode a target or a catalogue identifier. validation_group string): opaque detected related-record component. Use it only for grouped validation, not as a prediction feature. context_packet JSON string): title sketch, masked mechanism trace, and focused slot. candidate_cards_json JSON string): 12 row-local candidate objects with card_id and phrase. ranked_cards string, train only): canonical four-card answer. Only its first token labels the authentic phrase. The other three are distinct non-target placeholders in card-ID order, required to make the known-answer file a valid submission. Their identities and order are not graded relevance labels; train your relevance model using the first token only. Train and test have identical feature columns; ranked_cards is the only training-only column. The instruction is shared once in metadata rather than repeated in a constant CSV column. context_packet contains exactly: title_sketch string): privacy-filtered catalogue title. masked_mechanism_trace string): ordered catalogue description with three to eight `` markers. focus_slot string): the one slot scored for this row. Candidate IDs are always the row-local literals CARD_00 through CARD_11. An ID has no meaning across rows, and card order is independently shuffled for every row. Each ` marks a removed three-token phrase. focus_slot, such as SLOT_2, identifies . Only that gap is scored in the row. Use grouped cross-validation with validation_group`; ordinary random row splits can place nearly identical catalogue views in both fitting and validation folds. Group keys and ID segments are grouping metadata, not model inputs. The role-conservation rule is applied independently to train and test. It balances labels without moving a source record across the source-family split; test answers are never copied into public files. Evaluation For one row, let r be the rank of the authentic card in the submitted four-card list. The reciprocal-rank value is 1 / r when the authentic card is present and 0 otherwise. top1 is 1 only when the first submitted card is authentic. Rows from the same hidden source record are averaged first: source_mrr = mean(row_reciprocal_rank within the source record) source_top1 = mean(row_top1 within the source record) The final score is: score = 0.70 mean(source_mrr) + 0.30 mean(source_top1) This source-macro calculation prevents longer descriptions from receiving more influence merely because they yield more focal gaps. The score ranges from 0 to 1 and is maximized. The 70% reciprocal-rank term rewards useful shortlists, while the 30% top-one term gives additional weight to a correct first choice. They intentionally overlap: a correct first choice receives exactly 1.0. No credit depends on the order of non-target cards. For a uniform four-card ranking from 12 cards, expected score is 0.70 * (1 + 1/2 + 1/3 + 1/4) / 12 + 0.30 / 12 = 0.1465277778. This is an uncorrected metric, not a zero-chance metric. Public and private scores use the same formula on their respective source-disjoint subsets. Within each subset, average over sources actually present. ID alignment determines row matching; CSV row order has no effect. A known-answer submission scores 1.0 on either subset. Submission Submit exactly two columns in this order: id,ranked_cards spark_0123456789abcdef_0123456789abcdef01,"CARD_07 CARD_02 CARD_10 CARD_04" spark_fedcba9876543210_fedcba9876543210fe,"CARD_01 CARD_11 CARD_03 CARD_06" Requirements: Include exactly one row for every test id. Use exactly the columns id,ranked_cards in that order. ranked_cards must contain exactly four distinct candidate IDs separated by single spaces. Every submitted card must occur in that row's candidate_cards_json. Rank cards from most plausible to least plausible. Missing, duplicate, unknown, or extra IDs are rejected. Compute And Modeling Requirements Fine-tune or train a local sequence model on train.csv; trainable parameters must be updated from the released labels. Use the provided NVIDIA A10G for neural training and complete within the platform time limit. Read challenge inputs only from the supplied public directory and write the submission to the supplied output path. Locally available open pretrained text weights are allowed, but runtime downloads and hosted inference APIs are not. Prohibited Do not search the museum catalogue, source export, mirrors, or other external records to recover phrases. Do not reverse-map lex_* buckets to original words. Do not use source identifiers, row order, filenames, hashes, or card positions as prediction signals. Do not hardcode row answers or submit a fixed-card, keyword-only, TF-IDF-only, nearest-neighbour-only, or other untrained feature-vector baseline as the main mechanism. Do not use private answers, hidden files, grader behavior, malformed rankings, duplicate cards, or unknown IDs. Expected Output Your entrypoint receives the public dataset directory and exact submission CSV path as two positional arguments: python3 solution.py Write id,ranked_cards to the supplied output path. &nbsp;
> $700 Pool
> Closes in 2h 10m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Question Link Provenance

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79babajwaszmmtghs9c2g4x58c7pgb
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Easy
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat abir201's score of 0.322!

Full challenge description from page:

> Overview: On a large online community for technical questions and answers, editors and answerers connect a question to earlier questions that are genuinely related to it. Recovering these curated links from text is useful for organizing knowledge bases and surfacing prior discussion. In this challenge each case contains one origin question, called the query, and a fixed pool of 24 candidate questions from the same topic area. Between one and six of the candidates are the questions that the community actually linked to the query; the rest are same-topic questions that were never linked. Your task is to assign a relevance score to every query-candidate pair, where a high score means the candidate is a true linked question for that query. The candidate pool for each case is filled with the most lexically similar same-topic questions, so shared keywords alone do not separate the true links from the distractors. The test cases come from topic areas that do not appear in training, so a solution must transfer its matching strategy to unseen topics rather than memorizing topic-specific vocabulary. This is a text ranking and provenance task, and the intended competitive route is neural: fine-tuning a bi-encoder or a cross-encoder on the provided training pairs, which is what the A10G tier is provisioned for. There are 24,552 labelled query-candidate pairs to train on. Useful approaches include sentence-embedding similarity, supervised rerankers over embedding and lexical features, cross-encoders, and within-case score calibration. Evaluation: The metric is mean average precision, written MAP. Higher is better, and the range is 0 to 1. Every relevance_score must be a finite number between 0 and 1. For each case the 24 candidates are ranked by decreasing relevance_score, with ties broken deterministically by pair_id. Let AP be the average precision of that ranking against the true linked set: if the m true links occupy ranks r_1 through r_m, then AP = (1/m) times the sum over j of (precision at rank r_j). The score for the challenge is the plain mean of AP over every test case. Why this metric. Each case is one self-contained retrieval problem: exactly 24 candidates, of which between 1 and 6 are true links. Average precision is the standard measure for that shape, and two properties make it the right single choice here. First, it normalises by the number of true links, so a case with one link and a case with six are both scored on the same 0 to 1 range and neither dominates the mean. Second, it depends only on the ORDER the scores induce, not on their absolute values. That matters because the only thing a solver controls that reflects the intended skill is which candidates it puts above which; a metric sensitive to absolute score values would reward calibration effort that has nothing to do with recovering curated links. Why nothing is combined with it. An earlier version of this challenge added a set F1 computed at a fixed threshold of relevance_score >= 0.5, and combined three weighted aggregates on top. Both additions are dropped, for reasons that are specific to this task rather than stylistic: A fixed-threshold F1 is degenerate on the majority of these cases. 62.8 percent of test cases have exactly one true link, and for a single-link case the ranking is already fully described by AP; the threshold adds only whether the solver happened to place its scores above or below 0.5. Worse, F1 could be moved independently of the intended skill. Because AP is invariant to any monotone rescaling of the scores while a fixed threshold is not, a solver could leave its ranking completely unchanged and raise its F1 simply by shifting all scores across 0.5. That is an axis of optimisation that measures calibration against an arbitrary constant, not link recovery, so the component is removed rather than justified. The threshold 0.5 was itself arbitrary. It was not derived from the data, and no principled value exists here, which is a second reason to remove the component rather than retune it. A per-topic macro average and a bottom-quartile term were also dropped. The 67 held-out topics range from 1 to 24 cases each, and four contain a single case. Macro-averaging would give a one-case topic the same weight as a 24-case topic, and a bottom-quartile term over such small groups is dominated by the smallest ones, so both add variance without measuring anything the plain mean misses. Generalisation to unseen topics is already enforced by construction, because the split holds out whole topics; it does not need to be encoded a second time in the metric. Dataset: The public directory contains the following files. train_cases.jsonl - one JSON object per line, one per training case. Fields: case_id (string), query_text (string, the origin question text), candidates (array of 24 objects, each with candidate_id (string) and text (string)). test_cases.jsonl - same schema as train_cases.jsonl, for the held-out test topics. No labels are included. train.csv - one row per training query-candidate pair, 24,552 rows over 1,023 training cases. Columns: pair_id (string, unique pair identifier), case_id (string, joins to train_cases.jsonl), candidate_id (string, joins to a candidate within that case). It carries exactly the same columns as test.csv, in the same order. train_labels.csv - the training labels, one row per row of train.csv, joined on pair_id. Columns: pair_id (string), label (integer, 1 if the candidate is a true linked question and 0 otherwise). test.csv - one row per test query-candidate pair, with exactly the same columns as train.csv in the same order: pair_id (string), case_id (string, joins to test_cases.jsonl), candidate_id (string). Every test case has exactly 24 pair rows, and no label file is provided for them. sample_submission.csv - a correctly formatted submission with placeholder scores. Columns: pair_id (string), relevance_score (float). Submission: Submit one CSV with exactly these columns. pair_id - string - every pair_id from sample_submission.csv, each exactly once. relevance_score - float - a finite value from 0.0 through 1.0; higher means more likely to be a true linked question. Example submission with three rows: pair_id,relevance_score pair_0a1b2c3d4e5f60718293,0.907 pair_1b2c3d4e5f6071829304,0.042 pair_2c3d4e5f60718293a4b5,0.613 Requirements: one row per test pair, the columns named exactly pair_id and relevance_score, scores in the closed interval from 0 to 1. Row order does not matter. Missing pairs are scored as if they had relevance 0. Extra rows that are not in the test set are ignored. Rules: The only valid input signal is the provided question text for each query and each candidate. The following approaches are not allowed. Hardcoding relevance scores for specific pair_id or candidate_id values instead of computing them from the question text. Using the pair_id, case_id, or candidate_id strings, or the row order of any file, as a prediction signal. Attempting to recover a test link by reversing a training pair. The community link relation is symmetric, so in principle a training pair (A linked to B) could reveal a test pair (B linked to A). That route has been closed at preparation time: every training case whose positive pair matches an evaluation positive pair, in either direction, is removed from the training data before it is published. Ninety such cases were dropped, and the number of test links recoverable this way is zero. The exploit is stated here so that no effort is wasted on it. A pair_id is a compound key of the form group__case__candidate, built from opaque hashes so that grading can recover the topic grouping without shipping it as a separate column. Its three parts are identifiers only and carry no information about whether the pair is linked. Searching the web for the original questions, or reverse-matching the provided text to an upstream community website, and reading its link sidebar, related-question list, or any other metadata to recover the answer. Reconstructing removed identifiers, source URLs, or the split keys. Using private, role-gated, or API-key-based models, or calling any external inference API at scoring time. Using non-reproducible external weights or artifacts that are not publicly available. The intended task is to learn, from the training cases, what makes one question a genuine curated link of another, and to transfer that to unseen topics where the candidates are chosen to look lexically similar to the query. A solution that relies on shared keywords will not separate the true links from the distractors, because the distractors were selected to maximize that overlap. The scores must be produced by a program that reads only the provided files. Pretrained model policy: Using a publicly available pretrained text model is allowed and expected. Ranking candidates by frozen sentence-embedding cosine similarity, with no fine-tuning, is a sensible first baseline and should be measured before anything is trained; the lexical TF-IDF reference point is 0.3026 MAP. Fine-tuning a matcher, such as a bi-encoder or cross-encoder, on the provided training pairs is the intended path to score above such inference-only baselines, and a submitted system should be shown to beat the frozen baseline it starts from. The held-out-topic split means the model must generalize what a curated link looks like to genuinely unseen topics, so the provided training labels are the essential signal. &nbsp;
> $700 Pool
> Closes in 6h 16m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Retrieving the True Continuation of a Historical Passage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c629xqr3r35xvvk7cs4mk458dyw99
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat amtech's score of 0.870!

Full challenge description from page:

> Retrieving the True Continuation of a Historical Passage Overview An archivist holds a page fragment and a box of thousands of other fragments from the same periodical: which one continues the text in hand? Each test item in this challenge is a 110-word passage from an early twentieth-century periodical; your model must search a pool of 1,865 candidate passages, all from the same periodical, same era, and same subject register, and rank the five most likely true continuations, best first. Exactly one candidate is the passage that actually followed in print. The pool is intentionally larger than the query set: several hundred candidates are the true continuation of no query at all (including passages whose own predecessor was withheld), so there is no one-to-one matching structure to exploit , each query must be answered on its own evidence. Because every distractor shares the publication's voice and recurring topics, surface similarity is nowhere near enough: the true continuation is distinguished by discourse continuity: an unfinished sentence resuming, an argument advancing, a named entity's story carrying forward. Real-World Motivation Digitization pipelines routinely shatter documents into disconnected fragments: OCR breaks multi-page articles at page and column boundaries, archival collections hold detached leaves, and text extracted from scans loses its reading order. Reassembling which fragment continues which is a real and manual archival task. A retrieval model that reliably finds a passage's true continuation in a large pool turns fragment soup back into readable documents, and the same capability underpins passage linking in retrieval-augmented systems, where finding the context that continues a passage matters as much as finding topically similar text. What Makes This Different The closest published work is Riedl et al. (LaTeCH 2019), which recovers article continuity in OCR'd historical newspapers by segmenting and clustering text within scanned issues, and the broader passage-retrieval literature (MS MARCO and its descendants), which ranks passages by topical relevance to a query. This benchmark poses a problem neither of them contains, and the distinction is measured, not asserted. First, the target relation is continuation, not relevance, and in a single-publication pool the two come apart: a tuned lexical tf-idf retriever places the true continuation in its top five for about 40% of queries but at rank 1 for only about 1%. Topical retrieval saturates recall of the neighborhood and still fails to identify which passage actually follows, because every distractor shares the publication's vocabulary, era, and recurring subjects. The entire useful range of the metric therefore lies in a capability standard passage retrieval does not test: reading for discourse continuity, an unfinished sentence resuming, an argument advancing, a story carrying forward. Second, unlike segmentation-and-clustering settings, the model here receives no surrounding document: queries are isolated 110-word fragments, candidates span eight full held-out issues, and several hundred candidates continue no query at all, so there is no closed-world assignment structure to exploit; each query must be answered on its own evidence against a pool where most options are the answer to nothing. Third, the evaluation is exact ranked identification (MRR@5) over that open pool, with issue-disjoint splits so publication-specific memorization cannot substitute for continuity reading, and with external source lookup prohibited so the printed order cannot be recovered from outside. Story-ending selection (Story Cloze) chooses between two authored endings of a short fiction; cloze and metadata benchmarks on historical newspapers predict masked tokens or layout; none pose open-pool continuation identification over real OCR fragments. Data train.csv , 8,395 rows, columns: query_id (string, format CH followed by six digits, e.g. CH004217), query_text (string, one 110-word OCR passage), continuation_text (string, the passage that immediately followed it in print). test_queries.csv , 1,543 rows, columns: query_id, query_text. test_candidates.csv , 1,865 rows, columns: candidate_id (string, same CH format), candidate_text. Every test query's true continuation is in this pool, and the pool also contains candidates that continue no query. sample_submission.csv , the required format, filled with random rankings. Train and test are disjoint by issue: no test passage comes from an issue seen in training. Train pairs are given as raw text so you can mine your own negatives from other training continuations. Target and Submission Submit a CSV with exactly two columns, query_id and ranking, and nothing else. Exactly one row per test query_id: no missing ids, no duplicate ids, no ids outside the test set, no extra columns. The grader rejects malformed submissions outright. ranking is a space-separated list of exactly 5 distinct candidate_ids from test_candidates.csv, your best guess first. Example of a correctly formatted submission.csv: query_id,ranking CH000123,CH001832 CH000456 CH001204 CH000031 CH001700 CH000124,CH000900 CH001101 CH000202 CH001633 CH000047 Evaluation Mean Reciprocal Rank at 5 (MRR@5), averaged over test queries, range 0-1, higher is better. If the true continuation appears at rank r in your five, the query scores 1/r; otherwise 0. Anchors: random rankings score about 0.001; a tuned lexical tf-idf retriever scores about 0.1 (rank-1 hits are rare even when the truth reaches the top five); a perfect submission scores exactly 1.0. The wide gap between the lexical baseline and the ceiling is the challenge: it can only be crossed by models that read for continuity rather than match words. Compute This is a fine-tuning challenge, designed for GPU solving: the intended solution is to fine-tune a pretrained open-weights text encoder as a dual encoder (or cross-encoder reranker over a first-stage retrieval) on the 8.4k training continuation pairs , comfortable on the provided GPU within the time limit. Lexical and rule-based CPU approaches were measured during design and sit near the floor of the useful range. Restrictions / Prohibited Methods No source retrieval: do not attempt to identify the source periodical, and do not query, scrape, or match passages against any digital library, search engine, or other external text source to recover printed order. Rankings must come from a model trained on the provided training data. No hard-coded per-query answers. No hosted or closed-source API models at any stage (training, distillation, pseudo-labelling, or inference). Open-weights pretrained models are permitted as generic backbones; fine-tuning them on the provided train.csv is allowed and expected. No probing for private answers, no training or calibrating on the test items' hidden links, no grader or platform side channels. &nbsp;
> $700 Pool
> Closes in 6h 23m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Fruitlet Visible Contours

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bm7m64ekqyxdahaw17hq6wh8e5gmc
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ravi56's score of 0.626!

Full challenge description from page:

> Background Accurate automated monitoring in precision horticulture requires precise delineation of developing fruitlets. While coarse bounding boxes or idealized parametric shapes (such as ellipses) can detect presence, they fail to capture critical morphology, calyx orientation, irregular boundaries, and severe occlusions caused by foliage, branches, or adjacent clustered fruit. This benchmark isolates the problem of prompt-conditioned instance contour extraction: given a localized visual context and a coarse prompt bounding box, models must accurately trace only the visible, unoccluded boundary of the queried target fruitlet. Overview Given a $384 \times 384$ RGB context image crop and a coarse prompt bounding box (query_box) defined on a $128 \times 128$ normalized grid, extract the exact visible boundary polygons (polygons) of the specified target fruitlet. Key Requirements: Target Boundary Adherence: Trace the visible irregular contour of the fruitlet indicated by the query box. Occlusion Handling: Exclude overlapping foliage, stems, and neighboring fruitlets from the predicted mask. No Amodal Guessing: Only predict visible surfaces; do not hallucinate hidden contours obscured by occluders. Fine-tuning a general-purpose pretrained visual backbone on the provided training set is permitted, along with deterministic post-processing routines. Dataset Information (Public Files) All assets required for model development and evaluation are supplied in the public directory. Images are provided as $384 \times 384$ 3-channel RGB files. +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | images/ | Contextual 384x384 RGB crops centered around fruit clusters. | | train.csv | 532 supervised training rows with prompt boxes and targets. | | test.csv | 211 evaluation queries requiring contour predictions. | | sample_submission.csv | Format-example rows for test IDs with empty placeholder runs.| +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +----------------+---------+-----------------------------------------------------------+ | Column | Type | Description | +----------------+---------+-----------------------------------------------------------+ | id | String | Opaque unique identifier for the specific instance query. | | image | String | Relative path to the 384x384 RGB crop (e.g. images/). | | query_box | JSON | Coarse prompt box [xmin, ymin, xmax, ymax] on a 128-grid. | | polygons | JSON | (Train only) Visible boundary polygons on a 128x128 grid. | +----------------+---------+-----------------------------------------------------------+ Prompt Box Format (query_box) The prompt box is provided as a JSON array of four integers: [x_min, y_min, x_max, y_max] Coordinates are defined in the integer range $[0, 127]$ corresponding to a $128 \times 128$ spatial grid. The query box roughly locates the target instance within the wider $384 \times 384$ contextual image. Target JSON Schema (polygons) The polygons column expects a JSON array of up to 12 filled polygons: [[[x1, y1], [x2, y2], [x3, y3], ...], ...] Coordinate Bounds: Every vertex $[x, y]$ must consist of integers strictly within $[0, 127]$. Polygon Validity: Each polygon must contain between 3 and 200 vertices, with at least 3 distinct spatial points. Mask Interpretation: Multiple polygons are unioned together into a single binary raster mask. Internal holes are not explicitly modeled. Size Limit: The JSON string for a single row must not exceed 18,000 characters. Evaluation Metrics Submissions are evaluated by rasterizing the predicted polygon union onto a $128 \times 128$ boolean mask $P$ and comparing it against the reference mask $T$. The score combines area overlap (Mask IoU) with local contour alignment (Boundary F-Score). 1. Mask Intersection over Union ($I$) $$I = \frac{\vert{}P \cap T\vert{}}{\vert{}P \cup T\vert{}}$$ (Note: If the predicted mask $P$ contains no positive pixels, the entire row score is strictly $0.0$.) 2. Boundary Extraction and Tolerance-Weighted F-Score ($B$) Boundaries are extracted using binary erosion with a standard 4-neighbor structuring element: $$\partial P = P \oplus \text{erode}(P)$$ $$\partial T = T \oplus \text{erode}(T)$$ (where $\oplus$ denotes XOR, identifying outer boundary pixels). To permit a 1-pixel spatial tolerance margin, boundaries are matched against a 1-step 4-neighbor dilation ($\text{dilate}(\cdot)$): $$\text{Precision} = \frac{\vert{}\partial P \cap \text{dilate}(\partial T)\vert{}}{\max(1, \vert{}\partial P\vert{})}$$ $$\text{Recall} = \frac{\vert{}\partial T \cap \text{dilate}(\partial P)\vert{}}{\max(1, \vert{}\partial T\vert{})}$$ The Boundary F-score is the harmonic mean of boundary precision and recall: $$B = \begin{cases} \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} & \text{if } \text{Precision} + \text{Recall} > 0 \\ 0.0 & \text{otherwise} \end{cases}$$ 3. Row Score and Final Metric The row score weights both region accuracy and boundary sharpness: $$\text{Row Score} = 0.4 \times I + 0.6 \times B$$ The overall competition metric is the unweighted arithmetic mean across all test instances: $$\text{Final Score} = \frac{1}{N_{\text{test}}} \sum_{i=1}^{N_{\text{test}}} \text{Row Score}_i$$ Scores range between $0.0$ and $1.0$ (higher is better). Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,polygons. Include one row per test ID with no duplicate or missing IDs. Quote JSON strings according to standard CSV formatting rules. id,polygons dffb03609dd70e29b24c7ea7,"[[[69,45],[61,48],[53,58],[45,74],[56,79],[71,71],[79,64],[79,50],[74,45]]]" Parsing Bounds & Rejection: Missing, extra, or mismatched ID sets, incorrect column headers, or submission files exceeding 50 MB will cause immediate file rejection (score of 0.0). Malformed JSON payloads, coordinates outside $[0, 127]$, polygons with fewer than 3 distinct vertices, polygons with more than 200 vertices, lists with more than 12 polygons, or cells exceeding 18,000 characters evaluate to 0.0 for that specific row. Row ordering does not impact grading. What Not To Use To ensure rigorous and comparable algorithmic evaluation: No External Training Data: Models must be trained solely on the supplied training rows. No additional outside segmentation or horticultural datasets may be used. Pretrained Model Guidelines: Fine-tuning at least one general-purpose pretrained vision backbone (e.g., standard checkpoints from timm or torchvision) is permitted. Task-specific segmentation models pretrained directly on the source domain or private checkpoints are prohibited. No Online or External Services: Inference must run completely offline without internet access, external API lookups, or hosted services. No Annotation Exploitation: Manual labeling of test samples, hard-coded lookup dictionaries, reverse-image matching, or exploiting metadata splits is strictly forbidden. Deterministic geometric postprocessors are permitted. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Inflation Cost-Burden Attribution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70479y09k658scctyhvyd2p58e3607
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jesuisnadi's score of 0.267!

Full challenge description from page:

> Inflation Cost-Burden Attribution Overview When wages, materials or freight get more expensive, a business can raise its own selling prices, accept a thinner margin, or do some of both. A report that mentions rising costs and rising prices in the same breath has not established which of those happened, or to whom. Each case gives you a complete Prices section from a Federal Reserve Beige Book release, together with an exact character span marking one business or business group inside it. Predict what that section establishes about the marked group's response to higher costs. This is source-grounded reading of what a document supports, not inflation forecasting and not a claim about real economic causation. Classes passed_on — the marked group actually raised its own selling prices because of higher input costs, with no stated partial transfer or retained burden. absorbed — the marked group explicitly bore higher costs or reduced margins without an offsetting selling-price increase. shared — actual partial transfer is explicit, or the marked population explicitly includes both realized transfer and retained burden. prospective — only a cost-linked intended, future, conditional or hypothetical response is established. unresolved — none of the above responses is established for this marked group in this section. Apply the classes in this order of precedence: An actual, already-realized response outranks a stated plan. A supplier that raised its own prices to cover higher input costs and expects to raise them again is passed_on, not prospective, unless partial transfer is stated. Explicit partial transfer outranks a single realized class. "Passed along about half the increase" is shared, not passed_on. "At least some" is only a lower bound and does not alone establish incomplete transfer. A marked population that explicitly contains both behaviours is shared. "Faced with higher food costs, some restaurants passed them on through menu prices while others absorbed them" is shared when the marked span covers that restaurant population as a whole. Rules that decide the hard cases: Higher input costs plus unchanged selling prices are not by themselves absorbed. The section must establish that the marked group carries the burden, through stated margin compression, an inability to raise prices, or a deliberate decision to hold them. A statement that the marked business chose to keep selling prices fixed despite its own higher input costs can establish absorbed. Do not reject that evidence merely because it does not use the word "margin". Conversely, two separate input-price and selling-price observations do not establish a decision or burden. Limited pricing power alone is not a realized response. An explicit discussion of whether or how to pass the business's increased costs to its customers is prospective if no realized response is established. It need not be a committed plan. Expected input-cost increases alone, without any linked response, remain unresolved. A fuel surcharge or other price component alone does not prove that the business's own input costs increased. Apply the same explicit cost-link rule as for any other selling-price increase. References such as "one case" or "only one" qualify when their business antecedent is clear. A market, product, or geographical place without a business referent is not an eligible focus. A selling-price increase attributed to demand, wages elsewhere in the economy, or nothing in particular is not cost pass-through. The link to that group's own higher costs must be present in the text. A broad statement about a district or sector does not settle the behaviour of a narrower group marked inside it. Mark unresolved rather than inheriting the sector claim. Information about a different business in the same section never determines the answer for the marked one. Several marked spans in one section may legitimately share a label, and the same section text appears once per marked span. Dataset 1618 marked spans drawn from 323 distinct Prices sections, across Beige Book releases published between 2018-01-17 and 2025-11-26. train.csv: 942 labelled spans from 32 report groups, releases dated 2018-01-17 to 2023-01-18. test.csv, public board: 284 spans from 11 report groups, 2023-03-08 to 2024-09-04. test.csv, private board: 392 spans from 10 report groups, 2024-10-23 to 2025-11-26. A report group is one Beige Book release, or a small set of releases linked by known duplicate passages. Every span in a group stays in one partition, so duplicated source text cannot straddle the split. Every training release precedes every evaluation release, and the private board is the most time-shifted partition, so a solution has to generalize forward rather than interpolate. Training spans outnumber evaluation spans, 942 to 676, and all five classes occur in all three partitions. Training class counts are unresolved 639, passed_on 172, shared 60, prospective 35 and absorbed 36. About 68% of training spans are unresolved, and the metric weights every present class equally, so a majority-class predictor scores badly. Annotation status. AI-origin labels; 201 retained cases received documented source-grounded AI rereview. 25 genuinely ambiguous disputed cases were quarantined. No human confirmation is claimed. File Structure train.csv: labelled cases. test.csv: unlabelled cases, the four feature fields without the label. sample_submission.csv: a valid format example cycling through the five class names. schema.json: column order, class vocabulary, offset convention and metric name. Features train.csv has five columns: case_id (string): unique case identifier, reproduced unchanged in the submission. text (string): the complete extracted Prices section, paragraphs in source order separated by blank lines. focus_start (integer): zero-based Unicode code-point index where the marked mention begins. focus_end (integer): end-exclusive Unicode code-point index where it ends. label (string): one of the five classes, the training target. test.csv has the same four feature columns without label, and sample_submission.csv has case_id and label. No report-group column is shipped: a constant placeholder is not allowed in the prepared files, and the real group would hand out the evaluation set's release structure. Group your validation by the text column rather than splitting rows at random. Every case sharing a text value is a different marked span inside one source section, so a random row split puts the same section on both sides and reports a score well above what the leaderboard will give. Sections from one release are held together in the real split, so grouping by text is a floor on how careful your validation should be, not a perfect reconstruction of it. sample_submission.csv cycles through the five classes by row order. That is a schema placeholder derived from position alone, not a hint about the answers. Offsets count Unicode code points, not encoded bytes, so recover a span with textfocus_start:focus_end] in Python rather than slicing encoded bytes. The longest section is 1791 code points. Section text repeats across rows whenever one section carries more than one marked span; that repetition is intentional and each span is scored separately, so a model that ignores the offsets cannot tell those rows apart. Evaluation The score is macro F1 over the classes present in the scored partition, higher is better, bounded 0 to 1. Let C be the set of classes appearing in either the true labels or your predictions for that partition. For each class c in C, count true positives TP(c), false positives FP(c) and false negatives FN(c): F1(c) = 2 * TP(c) / (2 * TP(c) + FP(c) + FN(c)) score = sum(F1(c) for c in C) / len(C) A class absent from both the truth and the predictions is excluded from the average. Predicting a class the partition does not contain adds a zero-F1 term, so guessing rare classes at random is penalised. Perfect predictions score 1. An always-unresolved submission cannot earn F1 credit for other true classes. The public and private boards apply the identical formula to disjoint sets of report groups. Here private names the hidden leaderboard partition; it does not mean the underlying reports are confidential. All source text is public; the evaluation labels are not supplied to solvers. Solvers receive only the four prepared public files listed above. The current public/private cutoff was selected after score comparisons across four candidate dates. Scores and bootstrap estimates on this split are exploratory, not independent evidence of stable model rankings. Submission Write a UTF-8 CSV with exactly two columns, in this order: case_id,label. One row per test.csv case, no more and no fewer. Row order does not affect the score. case_id,label item_0011223344556677889900aa,passed_on item_00aabbccddeeff0011223344,unresolved Use the real identifiers from test.csv. The grader rejects rather than repairs: missing rows, duplicate rows, unknown case IDs, class names outside the five allowed values, empty or null labels, extra columns and reordered columns all raise an error instead of scoring partially. The platform runs your script as: python3 solution.py Read the dataset from the first argument and write the CSV to exactly the second argument. Both are required; do not hardcode paths or fall back to defaults. Compute and Rules The target environment is one A10G, with an expected end-to-end runtime under 60 minutes. Build in a guard that stops training and moves to inference in time to write the submission inside that budget. Fine-tune a general-purpose pretrained language-model backbone during the submitted run, using only the supplied training labels for challenge-specific supervision. Frozen embeddings followed only by a separate classifier do not satisfy this Fine-Tuning task's training requirement. General-purpose pretrained backbones are allowed. Weights fine-tuned elsewhere on this task, cached predictions from an earlier run and remote inference APIs are not. Do not fit anything to the test collection. Per-item or per-batch inference is fine; pseudo-labelling, test-time adaptation and calibrating against the test distribution are not. Do not attempt to recover labels by matching test text back to the original Beige Book releases or to any external annotation of them. The source text is public and no attempt is made to hide it; the labels were authored for this challenge, not published by the Federal Reserve. Do not access creator-private files, answer tables or preparation inputs. Source and Attribution The underlying text is the Federal Reserve Board's historical Beige Book, published at [federalreserve.gov and reusable under the Board's disclaimer, which asks for attribution and excludes separately protected non-Board material. No seals, logos or images are redistributed. The marked spans, the class taxonomy, the annotation guide and the held-out protocol are original to this challenge. The Federal Reserve did not create and does not endorse this benchmark.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Ambiguous Entity Relation Support

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77denz9h4papj016arqxypkd8e8b84
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview A sentence may support several overlapping relations between two entities. Predict the fraction of human annotators selecting each relation, rather than forcing a single category. Task Given sentence,entity_1,entity_2, output 17 support values in the order of relation_vocabulary.json. Each value must be finite and between 0 and 1. These are independent selection fractions and need not sum to one. The none relation is one coordinate, not an empty output. Data Both feature files use task_id,group_id,sentence,entity_1,entity_2, with 1,200 training and 300 test rows. train_labels.csv provides task_id,support, where support is a JSON numeric array. Human selection counts are divided by the worker count during preparation. Connected groups of identical sentences or identical unordered entity-name pairs are assigned wholly to one split; group IDs are opaque. Publisher model predictions and distant-supervision labels are not features. Entity names can recur across different pairs. Crowd disagreement is part of the target and is not an expert assertion of factual truth. Evaluation For each row, support overlap is sum(min(pred_i,gold_i)) / sum(max(pred_i,gold_i)); average across rows. This standard continuous Jaccard similarity rewards agreement in both selected relations and support magnitude, without allowing the many near-zero relations to dominate through true negatives. Two all-zero vectors score 1. Submission Format CSV with exactly task_id,support. Supply a JSON array of exactly 17 finite numbers in [0,1]. Malformed or out-of-range rows score zero. Every test ID must appear exactly once; wrong headers and missing/extra/duplicate IDs are rejected. Expected Approach Fine-tune a compact encoder with explicit entity markers and a 17-output sigmoid head. Validate by group_id; compare with a training-mean support vector. General-purpose pretrained models are allowed. Models trained specifically on this challenge's source annotations, held-out labels, and answer lookup services are prohibited. Learn task-specific parameters from the supplied training data. For an efficient implementation, cache tokenization, use mixed precision and a small number of epochs, and calibrate on validation only. Reserve the final ten minutes for inference and output checks. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 90 minutes, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cross-Language Terminology Link Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79yjf6e31v3s7ee8673f97j98e80jx
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Technical writing places translations, abbreviations and equivalent terms close together, often with several competing mentions. Recover which exact mentions the text explicitly connects. Task Given a JSON token array, predict undirected links. Each link is [start1,end1,type1,start2,end2,type2]. Offsets are zero-based token indices, end-exclusive. Types combine mention kind and language, such as term:sl, term:en or abbr:en; mention_types.json gives the complete vocabulary. und denotes an undetermined language. The first endpoint must precede the second lexicographically. Predict only within-row links, not unlinked mentions. Data train.csv and test.csv contain 1,200 and 300 passages, with task_id,group_id,tokens. The opaque group_id identifies a source thesis. train_labels.csv contains task_id,links. Theses are assigned wholly to one split before row caps are applied: 427 training theses and 90 test theses are represented. Exact token sequences are deduplicated first. Common terminology can recur between theses, but passages from a selected test thesis do not enter training. The collection is enriched for terminology patterns, and its links are not an exhaustive ontology of all possible equivalences. Evaluation Micro F1 over complete, typed endpoint pairs: 2TP / (2TP + FP + FN). Endpoint reversal represents the same undirected link. Both mention boundaries and types must match; otherwise the predicted link cannot identify the intended terminology connection reliably. Scoring follows the native explicit links, not inferred semantic similarity. An empty reference-and-prediction slice scores 1. Submission Format UTF-8 CSV with exactly task_id,links. A payload is a JSON list, for example [[1,3,"term:sl",5,7,"term:en"]]; use [] for no links. Duplicate links and malformed row payloads earn no credit with a false-positive penalty. The file must contain every test ID exactly once; extra IDs or incorrect columns are rejected. Expected Approach Learn mention boundaries and types, then score candidate mention pairs using their context, punctuation and relative positions. Validate on held-out group_id values. General-purpose pretrained models are allowed. Models trained specifically on this challenge's source annotations, held-out labels, and answer lookup services are prohibited. Learn task-specific parameters from the supplied training data. For an efficient implementation, reuse one compact encoder for both stages, prune pairs only using public geometry in the token sequence, cache tokenization, and cap training by elapsed time. Reserve ten minutes for full-test decoding and schema validation. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 90 minutes, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Enzyme Annotation Provenance Reconciliation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7402ac0cx0v6eafyvsgxxhn98bqmqp
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat komilpamar's score of 0.698!

Full challenge description from page:

> Enzyme Annotation Provenance Reconciliation Overview Curated protein databases often export sequences, catalytic reactions, and residue annotations into separate tables. During aggregation or migration, a batch can remain intact while the row-level links between those tables are lost. This challenge asks you to reconstruct those links. Each episode contains six reviewed enzyme sequences, six intact reaction cards, and six intact catalytic-site cards. The three card collections describe the same six source proteins, but the reaction and site collections were independently permuted and given row-local labels. Recover both one-to-one mappings: which reaction card and which catalytic-site card belong to every protein. This is a GPU fine-tuning task. Strong systems should update a pretrained protein language model using the released training episodes, learn separate compatibility functions for reaction chemistry and catalytic-site profiles, and solve each episode as two global assignments. It is not ordinary reaction classification or catalytic-residue prediction: all annotations are already present, and the required action is restoring their provenance without inventing new labels. The private split holds out complete third-level enzyme families. Source reaction identifiers shared across the initial split are removed before episodes are formed. Exact sequences and exact reaction cards do not cross the final split. Dataset Public files: train.csv: 2,301 labeled reconciliation episodes, representing 13,806 proteins. test.csv: 368 unlabeled episodes, representing 2,208 proteins. sample_submission.csv: 368 valid identity-mapping examples. Columns: id (string): opaque episode identifier. protein_cards (JSON string): six objects with label, sequence, and sequence_length. Labels are P1 through P6. reaction_cards (JSON string): six objects with label and reactions. Labels are R1 through R6. Each reactions value is a list of one to three curated objects containing equation and direction. site_cards (JSON string): six objects with label and active_sites. Labels are S1 through S6. Each active site contains a categorical position_band from B1 through B8 and a biochemical role. The eight bands divide each source sequence into equal ordered regions from N-terminus (B1) to C-terminus (B8). Exact and fractional coordinates are not released. reconciliation (JSON string): target present only in train.csv. Example public input, abbreviated for readability: protein_cards = [{"label":"P1","sequence":"MAV...","sequence_length":214}, ...] reaction_cards = [{"label":"R1","reactions":[{"equation":"A + B = C","direction":"left-to-right"}]}, ...] site_cards = [{"label":"S1","active_sites":[{"position_band":"B2","role":"proton_donor"}]}, ...] The target contains exactly one assignment for each protein: {"assignments":[{"protein":"P1","reaction_card":"R4","site_card":"S2"},{"protein":"P2","reaction_card":"R1","site_card":"S5"},{"protein":"P3","reaction_card":"R6","site_card":"S1"},{"protein":"P4","reaction_card":"R2","site_card":"S6"},{"protein":"P5","reaction_card":"R5","site_card":"S3"},{"protein":"P6","reaction_card":"R3","site_card":"S4"}]} Every reaction card and every site card must be used exactly once. Card labels are randomized independently within each episode and have no meaning across rows. Evaluation For each episode: reaction_accuracy is the fraction of six proteins assigned their correct reaction card. site_accuracy is the fraction assigned their correct catalytic-site card. joint_accuracy is the fraction assigned both correct cards for the same protein. complete_episode is 1 only when all twelve links are correct, otherwise 0. The row score is: 0.40 * reaction_accuracy 0.30 * site_accuracy 0.25 * joint_accuracy 0.05 * complete_episode The final score is the mean row score clipped to [0,1]. Higher is better. A perfect submission scores 1.0. Joint credit is awarded only when both links are correct for the same protein. The weights reflect the database-repair objective. Reaction-table provenance receives 0.40 because attaching catalytic function to the wrong sequence is the primary record-level failure. Site-table provenance receives 0.30 because it restores the residue evidence needed to audit that function. Joint accuracy receives 0.25 so a system cannot score well by solving the two tables for different proteins; this component is deliberately smaller than the two marginal components to preserve useful partial credit. Complete-episode recovery receives only 0.05 because exact recovery is operationally valuable but too brittle to dominate a six-protein assignment. Equal weighting would understate the primary reaction link, while a large exact-match weight would discard informative partial repairs. Submission Submit a CSV with exactly these columns in this order: id,reconciliation batch_abc123,"{""assignments"":[{""protein"":""P1"",""reaction_card"":""R4"",""site_card"":""S2""},{""protein"":""P2"",""reaction_card"":""R1"",""site_card"":""S5""},{""protein"":""P3"",""reaction_card"":""R6"",""site_card"":""S1""},{""protein"":""P4"",""reaction_card"":""R2"",""site_card"":""S6""},{""protein"":""P5"",""reaction_card"":""R5"",""site_card"":""S3""},{""protein"":""P6"",""reaction_card"":""R3"",""site_card"":""S4""}]}" Requirements: Include every test id exactly once with no missing, duplicate, or foreign IDs. reconciliation must be valid JSON containing exactly the key assignments. Include exactly six assignment objects with exactly protein, reaction_card, and site_card. Use every released protein, reaction, and site label exactly once in its episode. Each JSON cell may contain at most 20,000 characters. Extra CSV columns are rejected. What Not To Use Do not search exact sequences or annotations in UniProt, Rhea, BLAST, or other external databases. Do not reverse-map opaque episode IDs or row-local labels to source records. Do not use cached source tables, external annotation lookup tables, private answers, or hosted inference APIs. Do not fit representations, thresholds, card priors, or assignment rules on test episodes. General-purpose public pretrained protein models are allowed, but the submitted solution must genuinely update model parameters using train.csv. &nbsp;
> Closes in 3m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Reboiler Joint Exposure Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx793e9g8hzp687jmq18e59rjd8e96f4
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat cuongtt's score of 0.601!

Full challenge description from page:

> Objective Recover the joint thermal exposure of two unavailable reboiler-jacket temperature channels from the remaining sensor and actuator histories. Predict the fraction of 512 one-second measurements occupying each of 64 paired temperature bins. This is a time-exposure distribution, not predictive uncertainty. Fine-tune a pretrained neural architecture on the supplied examples. Training plus inference must finish offline within 90 minutes using at most 10 CPU cores and 62 GB RAM. General pretrained weights may be acquired in advance. Public files train.csv: 480 rows with columns id,telemetry,exposure. test.csv: 72 rows with columns id,telemetry. telemetry/: compressed NPZ observation arrays. feature_schema.json: channel names, normalization medians and scales. bin_schema.json: bin thresholds and flattening convention. baseline.json: the 64-bin arithmetic mean of the training exposure distributions, used in scoring. sample_submission.csv: output-format examples. Equipment-run groups are separated before windowing, with 25% of groups held out by deterministic hash ordering. All phase files, overlapping windows and training variants from a group stay in one split. Use grouped internal validation. Each evaluation interval has exactly one observation, so repeated noisy views cannot be averaged. Training retains two perturbed views per interval. Windows must contain meaningful variation along both temperature axes. Observation arrays Each NPZ contains values (float32, 128×29), observed_mask (boolean, 128×29), and times (float32, length 128). Times strictly increase from 0 to 511 seconds. A false mask entry means a missing observation stored as zero; observed zeros are valid measurements. Normalize channels using training-group medians and interquartile scales, with the scale floors specified in feature_schema.json. Neither hidden temperature channel participates in input or normalization fitting. Observations are interpolated at the published times. A monotone sinusoidal clock displacement is at most 2.5% of the interval duration. Both splits use channel gains 0.99–1.01, Gaussian noise with standard deviation 0.008, sinusoidal drift of amplitude 0.012, and one 4–8-sample channel dropout block. Values are clipped to [−20,20]. Corruptions never alter exposure labels. Target distribution The lower-hemisphere temperature thresholds in degrees Celsius are [100,150,200,250,300,400,500]. Upper-hemisphere thresholds are [30,45,60,75,95,120,180]. Each axis has eight bins with unbounded outer intervals. Equality belongs to the higher bin. Flatten the 8×8 joint histogram with index = 8 × lower_bin + upper_bin. Output 64 finite probabilities in [0,1], summing to one within 0.00001. The grader normalizes accepted arrays to sum exactly to one. Correct marginal distributions alone are insufficient: paired occupancy matters. Evaluation: Hellinger skill against the training baseline For distributions P and Q, define H(P,Q) = sqrt(0.5 × sum((sqrt(P) − sqrt(Q))²)). Let B be the published baseline.json distribution. Across all N evaluation rows, the final score is: max(0, min(1, 1 − sum H(P_i,Q_i) / sum H(B,Q_i))) The denominator is fixed independently of submissions and must be positive. This measures reduction in joint-distribution error relative to a constant training-only predictor. Repeating B scores 0, exact targets score 1, and a predictor worse than B scores 0. Lower Hellinger error always improves the score before clipping. No per-row clipping is applied. Submission contract Submit UTF-8 CSV with exactly two ordered columns id,exposure, every evaluation ID once, and each JSON array quoted as a CSV cell. Row order does not affect scoring. Missing, extra, unknown or duplicate IDs and wrong columns score zero for the whole submission. A malformed row receives maximum Hellinger error 1: this includes invalid JSON, booleans, wrong array length, nonfinite or out-of-range numbers, an invalid sum, or more than 8,192 characters. Execution rules Use public training examples for task-specific supervision and validation. No external telemetry, evaluation-label retrieval, manual evaluation annotation, hard-coded answers, identifier shortcuts, hosted APIs or fitting on evaluation observations. This is a reconstruction benchmark, not a certified operational safety system.
> Closes in 2h 30m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Examiner-Grounded Novelty Passage Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75b5weqf0hz7hj5d2shqhk1n8e080v
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.670!

Full challenge description from page:

> Overview Given a patent claim and its examiner-cited passages, rank the passages that threaten the claim's novelty above background citations. Lexical overlap alone does not establish that a passage contains the claim's technical combination. Dataset train.csv and test.csv: task_id (string), claim (string); 1,200 training queries and 300 test queries. candidates.csv: task_id, passage_id, text (all strings), with one cited passage per row. Only candidates for the selected queries are included; every selected query keeps its full examiner-judged candidate set. Join candidates to their query using task_id, not row position. Candidate text and IDs are supplied for both splits; relevance labels are supplied only for training. train_labels.csv: task_id,target_json, listing the relevant candidate IDs. sample_submission.csv: the same output schema. A fixed hash ordering selects the compact query subset within each partition. Native source partitions are preserved after excluding overlapping applications/claims, conflicting judgments and queries with fewer than ten distinct candidates or only one judgment class. Evaluation claims matching training after removing punctuation and spacing are also excluded. Repeated claim text is grouped, not treated as independent examples. Only examiner-judged passages are candidates. Some dependent claims refer to preceding claims absent from the provided context. Citation coverage is incomplete, and boilerplate or shared technical vocabulary can create shortcuts; this is a citation-ranking task, not automated patent validity adjudication. Task Return an ordered list of candidate IDs, most relevant first. Candidate order in the input carries no relevance information. Submission task_id,target_json example_1,"[""p_3"",""p_1""]" example_2,"[""p_7""]" Columns must be exactly task_id,target_json, in that order. Include every test ID once. Submit a JSON list of distinct strings. Only the first ten ranks affect the metric; up to 10,000 IDs can be parsed, allowing reference files and predictions to use the identical representation. Unknown IDs are nonrelevant. Repeated IDs or malformed JSON give that query zero. Evaluation Standard MAP@10. For each query, sum precision at each relevant rank among ranks 1–10 and divide by min(10, number of relevant candidates). Average over queries. Score 1 is perfect. The metric rewards finding multiple novelty-threatening passages early, matching a reviewer's limited reading budget. File-level schema or ID errors are rejected. Expected Approach Start with lexical ranking and train a compact claim–passage reranker on the supplied relevance labels. Generic public pretrained models are allowed; a large generative model is unnecessary for producing an ordered candidate list. For an efficient implementation: Load and tokenize candidates once, grouping them by task ID. Use lexical scores to identify challenging training negatives. Train one small cross-encoder or a frozen-embedding ranking head. Batch similar-length pairs; use passage windows when truncation would discard potentially relevant evidence. Measure full-test inference throughput before choosing how many candidates to rerank. If shortlisting, preserve the remaining candidates in lexical order. Select the checkpoint by MAP@10 on held-out training claims and return up to ten distinct candidate IDs per query. What Not To Use No source lookup, external labeled patent corpora, source-specific fine-tuned checkpoints, manual test annotation or hosted APIs. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> Closes in 4h 34m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Calibrated Adaptive Crimp Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7794j4wkqamy10f0gz8svswx8e9jxb
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat papa's score of 0.354!

Full challenge description from page:

> Objective Use force traces to design an adaptive inspection policy for a basket of twelve wire crimps. An inspection reveals one part’s expert class. Choose up to three distinct parts, conditioning each later choice on earlier feedback, to discover as many different defect types as early as possible. Inspecting an OK part or rediscovering a defect type incurs a discounted wasted-inspection cost. Fine-tune a pretrained neural model using the supplied training data. Training, inference, and policy generation share a 90-minute offline budget of 10 CPU cores and 62 GB RAM. Pretrained base weights may be acquired before execution. No external task-specific data or hosted APIs are allowed. Public files train.csv: 500 baskets, with columns id,basket,policy. The policy is one optimal reference policy; other policies can achieve the same score. test.csv: 200 baskets, with columns id,basket. baskets/.json: an items list of twelve objects with local_index (0–11) and item_id, plus inspection_budget: 3. train_items.csv: columns id,signal,expert_class. test_items.csv: columns id,signal. calibration_items.csv: columns id,signal,reference. All ten rows are known class 0 (OK) controls; five have reference_A and five have reference_B. signals/.npz: array trace, float32 shape (256,2). inspection_schema.json: class names, signal shape, and policy grammar. sample_submission.csv: valid format examples for every test ID. Basket item_id values join to the id column of the corresponding item table. The signal and basket columns are paths relative to the public directory. IDs are opaque 24-character hexadecimal strings. Signals and calibration The first trace column is a strictly increasing relative event coordinate from 0 to 1, not calibrated time. The second is a normalized force signal clipped to [-0.25,1.5]. All domains and calibration controls use the same seeded perturbation family: coordinate warp amplitude ±0.008, gain 0.98–1.02, offset ±0.005, Gaussian noise with standard deviation 0.025, sinusoid amplitude 0.008 at 2–5 cycles, and 2–5 short spikes of width 2–5 samples and amplitude ±0.15. Two smooth Gaussian-shaped offsets have amplitude ±0.04, centers in [0.2,0.85] and widths in [0.04,0.12] of the event coordinate. A final correction adds 0.02(tanh(v)−v). These label-independent disturbances alter observations only; expert classes are unchanged. Normalization is already applied during preparation. Before perturbation, each unperturbed force curve is divided by the median unperturbed peak of five OK controls from its own conductor-size domain. Solvers receive the resulting normalized traces and do not need unperturbed peaks or an additional normalization step. All training parts belong to domain A. Their five matching controls are exactly the rows of calibration_items.csv whose reference equals reference_A. All test parts belong to domain B. Their five matching controls are exactly the rows whose reference equals reference_B. Use the signal paths on those rows to load the controls for optional model calibration. These two sets are unambiguous and each has five rows. Calibration controls are supplied as known-OK examples and never appear inside a basket. Classes and split 0: OK 1: one missing strand 2: two missing strands 3: three missing strands 4: crimped insulation Training and test use different conductor-size domains with disjoint unperturbed parts and no identical unperturbed force curves across splits. Parts may recur in multiple baskets within the same split. Every basket contains nine OK parts and three defective parts, each from a different nonzero class. The three defect classes are chosen uniformly without replacement among nonzero classes represented in the relevant domain; positions are shuffled. Class support can differ between domains. This composition is identical in training and evaluation. This evaluates discovery efficiency in mixed-defect baskets under a domain shift; it does not estimate factory defect prevalence. Policy grammar Each policy is either JSON null (stop immediately), or an object with exactly two keys: ask: integer local_index from 0 through 11, identifying the next part to inspect. next: an object with exactly the five string keys "0","1","2","3","4". Each value is a child policy. The grader follows the branch matching the inspected part’s true class. Every root-to-leaf path may contain at most three ask nodes and may not repeat a local_index. All five feedback branches must be explicitly present at every node, including branches that are not reached. Early stopping is valid. A policy cell may contain at most 16,384 characters. Scoring At zero-based inspection step k, a newly discovered nonzero class earns 1 / log2(k+2). Class 0 and already discovered classes incur a cost of 0.5 / log2(k+2). Utility is the sum of discovery rewards minus wasted-inspection costs along the executed path. Stopping leaves the remaining inspection slots unused. Each unused slot incurs the same discounted cost of 0.5 / log2(k+2), so stopping cannot evade the missed audit opportunity cost. Let T be the number of distinct nonzero classes actually present in the basket. The oracle gain is the sum of the first min(3,T) discounts: oracle_gain = sum(1 / log2(k+2) for k in range(min(3,T))) row_score = max(0, min(1, achieved_utility / oracle_gain)) final_score = mean(row_score over all test baskets) Released baskets have exactly T = 3, so their denominator is positive. For completeness, an all-OK basket would give any valid policy a score of 1 and a malformed policy 0. Scores range from 0 to 1; higher is better. The metric evaluates the policy’s actual discoveries, not exact agreement with the reference tree. Submission Submit a UTF-8 CSV with exactly the columns id,policy, in that order, and exactly one row per test basket ID. Row order is arbitrary. Quote JSON cells using standard CSV escaping. id,policy 4a8b1c2d3e4f5a6b7c8d9e0f,"{""ask"":0,""next"":{""0"":null,""1"":null,""2"":null,""3"":null,""4"":null}}" This illustrative policy inspects item 0 once and then stops for all five feedback classes. It is valid but is not a competitive use of the three-inspection budget. Use sample_submission.csv for actual test IDs. Missing, extra, duplicate, or unknown IDs, or incorrect columns, invalidate the whole submission and score 0. A malformed policy receives 0 for that basket. Booleans are not valid ask indices. The parser validates every branch, including unvisited ones. Permitted information Use the public training labels, reference policies, and released known-OK calibration controls for fitting and model selection. Test signals are for inference only. Inspection feedback exists only inside the grader’s execution of a single submitted basket policy; it cannot be shared between baskets. Do not recover unperturbed identifiers, access hidden expert labels or private records, manually annotate test items, hard-code test IDs, or query external services.
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Akan Disfluent Speech Transcription

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bfcvem0fn13rbwa8vtpqpas8e4vjd
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Akan Disfluent Speech Transcription Overview This competition tasks participants with automatic speech recognition (ASR) of spontaneous, disfluent Akan speech. Transcripts must be verbatim: stuttering, repeated syllables, vocalized pauses, and partial word tokens present in the native reference must be retained rather than normalized away into clean, fluent paraphrases. Both speakers and visual elicitation stimuli in the test set are completely disjoint from the training set, requiring acoustic and language models that generalize well across unseen vocal traits and novel conversational topics. File Structure All audio file paths in the metadata resolve relative to the root directory containing the CSV files. &nbsp; ├── train.csv ├── test.csv ├── sample_submission.csv └── audio/ ├── .flac └── ... train.csv: Contains 2,200 labeled training records. id (string): Unique 24-character hexadecimal identifier. audio (string): Relative file path pointing to the mono 16 kHz PCM-16 FLAC waveform (e.g., audio/1a2b3c4d5e6f7a8b9c0d1e2f.flac). duration_seconds (float): Clip duration in seconds ($1.0 \le t \le 28.0$). prediction (string): Verbatim ground-truth Akan transcript (5 to 55 words; length $\le 700$ characters). test.csv: Contains 263 unlabelled evaluation records. Contains columns id, audio, and duration_seconds (omits prediction). sample_submission.csv: Format demonstration mapping every test id to a placeholder ellipsis (…). audio/: Folder containing all referenced mono 16 kHz FLAC audio files. Prediction Schema & Submission Format Submissions must be a single UTF-8 CSV named with the header id,prediction. &nbsp; id,prediction b6d2c6123ce522494c511fb1,ɔrehyɛ mmra wɔ dan no mu. c3e1a4781fd245a99e8210bc,me me mepɛ sɛ mekɔ fie. Constraints per Prediction: Must be plain text verbatim Akan transcription. Max 120 words and max 1,400 characters (predictions exceeding these limits automatically receive a score of 0.0 for that row). Maximum raw cell length is 65,536 bytes. Submission File Validity: File size must not exceed 256 MB. Every test ID must be present with no extras, duplicates, or missing rows. Any malformed CSV structure, mismatched IDs, or incorrect schema (['id', 'prediction']) yields an overall score of 0.0. Evaluation Metric Predictions are graded using a composite of word-level and character-level Levenshtein edit similarity: $$\text{Score}{\text{row}} = 0.7 \times E{\text{word}}(p, g) + 0.3 \times E_{\text{char}}(p, g)$$ Where: $p$ and $g$ are the prediction and ground-truth reference, both pre-processed with Unicode NFC normalization and whitespace collapse (re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()). For sequences $a$ and $b$, edit similarity is defined as: $$E(a, b) = \max\left(0.0, 1.0 - \frac{\text{Levenshtein}(a, b)}{\max(\text{len}(a), \text{len}(b))}\right)$$ Exact unit-cost Levenshtein distance applies (insertions, deletions, and substitutions cost 1). $E(\emptyset, \emptyset) = 1.0$ and $E(\emptyset, b) = 0.0$ for non-empty $b$. Word tokens are derived via standard whitespace split (.split()), while character tokens are individual Unicode code points. The competition leaderboard reflects the arithmetic mean of all row scores: $$\text{Final Score} = \frac{1}{N} \sum_{i=1}^{N} \text{Score}_{\text{row}, i}$$ Rules: What to Use and What Not to Use Permitted: Supervised fine-tuning solely on the provided 2,200 training examples and associated FLAC files. Open-access, generic pre-trained foundation models (e.g., wav2vec 2.0, MMS, Whisper) provisioned locally within the execution environment. Standard data augmentation techniques (e.g., SpecAugment, noise addition, pitch shifting). Cross-validation routines built strictly from splits of train.csv. Prohibited: No external dataset access or live internet lookups: Execution must run strictly offline; external web queries, hosted speech APIs, or external dictionary scraping during run time are prohibited. No test-set leakage or reverse engineering: No manual annotation, pseudo-labeling pipelines reading external gold sets, hardcoded IDs, or reconstruction of the raw source tar archives. No text post-processing that normalizes disfluency: Removing repeated words, truncating partial utterances, or expanding shorthand will directly penalize the verbatim similarity metric. Hardware & Runtime Budget: Execution must be self-contained on a single GPU (24 GB VRAM, 10 CPU cores, 62 GB system memory). The entire inference (or train-plus-inference) pipeline must conclude within the 90-minute execution window. Model inference must execute on CUDA. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Historic Water-Level Chart Digitization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cw3125abm9dsrtrhn8af8gx8e9vmz
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat drcs's score of 0.843!

Full challenge description from page:

> Objective Read a monthly water-level chart and compile a contiguous four-segment range program that summarizes its normalized daily shape. Fine-tune a pretrained image encoder using the supplied training examples. Training and inference must finish offline within 90 minutes, using at most 10 CPU cores and 62 GB RAM. Public files train.csv: 360 rows with columns id,image,days,program. training_curves.json: maps each training ID to its normalized daily measurements. test.csv: 60 rows with columns id,image,days. images/: 420 RGB JPEG crops, each 384×256. sample_submission.csv: valid full-height ranges illustrating the output format. IDs are opaque 24-character hexadecimal strings; image paths are relative to the public directory. Each month contains 28–31 days. Training and evaluation use disjoint complete chart-year groups. Both training variants of a month stay together. Evaluation supplies exactly one observation per month, preventing repeated views of the same evaluation chart. Group internal validation by matching monthly charts where possible. Measurements and observations Each target curve is independently scaled as (level − monthly minimum)/(monthly maximum − monthly minimum). Bounds represent dimensionless within-month shape, not absolute water level. Constant months and months with zero optimal interval cost are excluded. Charts retain ink, grids, annotations and damaged regions. Both splits use the same deterministic observation process: gain 0.98–1.02, offset ±0.004, Gaussian noise with standard deviation 0.025, a spatial sinusoid with amplitude 0.0035, 3–7 small speckle patches and gamma 0.98–1.02. Values are clipped to [0,1] before JPEG encoding. Targets are unchanged by these image perturbations. Program grammar Output a JSON array of exactly four nonempty segments. Each segment is [start,end,low,high]. Day indices are zero-based inclusive integers. The first start is 0, each subsequent start equals the previous end plus 1, and the final end is days − 1. Bounds must be finite numbers with 0 ≤ low ≤ high ≤ 1. [[0,6,0.0,1.0],[7,13,0.0,1.0],[14,20,0.0,1.0],[21,27,0.0,1.0]] Evaluation: baseline-adjusted interval efficiency For daily truth v and its assigned interval [l,h], cost is: (h − l) + 10 max(l − v,0) + 10 max(v − h,0) Let A be the sum of daily costs, O the minimum possible cost over valid four-segment programs, and n the number of days. The full-height baseline has cost n and efficiency b = O/n. The submitted efficiency is e = O/max(A,O). The row score is: max(0, min(1, (e − b)/(1 − b))) The final score is the mean over evaluation rows. This measures efficiency gained beyond full-height ranges: the baseline scores 0 and every optimal program scores 1. Widening intervals can improve coverage but pays a width cost. The oracle may be computed by dynamic programming over segment boundaries, using the segment 0.1 and 0.9 empirical quantiles as optimal bounds. O is positive and less than n for every retained row. Submission and validation Submit UTF-8 CSV with exactly two ordered columns id,program, one row for every evaluation ID. Quote each JSON cell normally for CSV. Row order is irrelevant. Missing, extra, duplicate or unknown IDs and incorrect columns score zero for the whole submission. Invalid JSON, noninteger indices, gaps, overlaps, invalid bounds or a cell longer than 2,048 characters score zero for that row. Execution rules Use only supplied training labels for task-specific fitting and model selection. General pretrained weights may be acquired before offline execution. No external task data, hosted inference, manual evaluation annotation, hard-coded answers, identifier shortcuts, hidden measurements or fitting on evaluation images. This task evaluates historical document interpretation.
> Closes in 1h 15m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Unseen-Speaker Parliamentary Sentiment under Lexical Shift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76807wc7ez96r86dppa80nz58eb0j4
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Interpret the sentiment of short parliamentary statements from unfamiliar speakers and held-out lexical clusters. The target concerns the expressed evaluation in the statement, not its political position or speaker identity. Models must transfer evaluative language beyond familiar word co-occurrences. Task Predict exactly one of Negative, Neutral or Positive for each sentence. Use the final native three-class annotation, not the individual annotators' finer-grained preliminary labels. Data There are 1,200 training rows and 300 test rows. train.csv and test.csv have the same string columns: task_id (unique opaque row identifier), group_id (opaque speaker identifier, for validation grouping only), and sentence (complete statement text). train_labels.csv contains task_id,sentiment. label_vocabulary.json lists the three allowed labels; sample_submission.csv demonstrates the output format. Names, party, gender and birth-year metadata are not features. The split has 610 training speakers and 221 test speakers, with no shared speakers or exact duplicate sentences. A fixed, label-independent lexical clustering groups statements by word usage. Entire selected clusters are excluded from training; all statements by test speakers are also excluded. Cluster selection uses a fixed ordering and sample-count constraints, never sentiment labels or model errors. This blocks direct reuse of speaker-specific patterns and held-out lexical groups. Clusters are only proxies for subject matter: broad topics and debates can still overlap, and semantic near-duplicates are not guaranteed absent. Annotation disagreement and missing broader speech context remain limitations. Evaluation Macro F1 across the reference classes present in the evaluation slice. For each class, F1 = 2TP / (2TP + FP + FN); the score is the unweighted class mean. Equal class influence prevents a frequent sentiment from dominating the result. Wrong or invalid labels count as missed classifications. Submission Format UTF-8 CSV with exactly task_id,sentiment, one row for every test ID. Labels are case-sensitive. Incorrect headers and missing, extra or duplicate IDs are rejected; row order does not affect the score. Expected Approach Fine-tune a multilingual sentence encoder with a three-class head and validate on held-out speaker groups, preferably also separating lexical clusters within training. Compare against majority and character n-gram baselines. General-purpose pretrained models are allowed. Models trained specifically on this challenge's source annotations, held-out labels, and answer lookup services are prohibited. Learn task-specific parameters from the supplied training data. For an efficient implementation, cache tokenization and use short mixed-precision runs with validation-based stopping. Avoid elaborate speaker modelling: speaker identity is not an allowed feature. Reserve ten minutes for inference and CSV validation. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 90 minutes, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline.
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Unseen-Object Cross-View Silhouette Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78x815narwdzzdep8j8cda5s8e9b7f
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Unseen-Object Cross-View Silhouette Completion Overview Fine-tune a vision model to recover only the hidden part of an object's projected silhouette in a cluttered target view. Each query supplies target RGB and depth, the object's visible target mask, and a second RGB view with a visible mask of the same object. The reference view provides shape evidence; copying the target's visible mask does not predict the hidden region. Test targets belong to object categories with no labelled training targets. The task measures transfer across objects and viewpoints while keeping complete target scenes separate between training and test. Evaluation Submissions are scored by a scene- and occlusion-severity-balanced hidden-mask score from 0 to 1; higher is better. For each 256×256 prediction, hidden-region IoU is intersection over union against the gold hidden mask. Boundary F1 matches predicted and gold boundary pixels within a two-pixel dilation tolerance. The mask score is (0.7 × IoU + 0.3 × boundary F1) × (1 − visible overlap / max(1, predicted foreground pixels)), where visible overlap counts predicted foreground pixels in the supplied target visible mask. Scores are averaged within each private scene and severity group, then across scenes within each severity, then equally across the small- and large-hidden-area severity means. Invalid rows score zero. Dataset The prepared public/ directory contains train.csv, test.csv, sample_submission.csv, and inputs/. Paths in the CSV files are relative to public/. RGB images and masks are 256×256. Depth is float32 NPY in native millimetres after source scaling; zero means unavailable. Multiple queries may share a stored input asset. CSV columns (name — type — description): completion_id — string; unique query identifier. target_image — PNG path; target RGB crop. visible_mask — PNG path; observed target-object pixels. reference_image — PNG path; second RGB view of the same object. reference_mask — PNG path; visible object mask in the second view. depth — NPY path; target depth crop. mask_rle — JSON list; hidden-region training target in train.csv only. The target crop is centered and sized using visible pixels alone with 2.2× padding; it does not disclose the hidden silhouette's bounding box. The reference crop uses independent coordinates. Preparation retains target instances with native visibility between 5% and 98% and at least 32 prepared visible and hidden pixels. Complete source scenes are held out for test, and target object categories are disjoint across training and test. Objects may still appear in image backgrounds; distinct scene IDs are not claimed to guarantee distinct physical arrangements. Training and resource rules This is GPU fine-tuning for reference-conditioned amodal completion. Use one A10G or H100, at most 62 GB host RAM, and 90 minutes for the entire solution. The reference fine-tunes a generic nine-channel vision encoder for 65 minutes; target-GPU timing is unverified. Use only supplied inputs and training labels plus generic initialization. External task data, pose- or segmentation-specific pretrained models, source lookup, APIs, test-answer access, manual test labelling, and test-time learning are prohibited. Save fine-tuned weights and a timing log. CPU I/O and deterministic mask serialization are allowed. Organizer review may disqualify rule violations independently of score. Submission Submit a CSV file with a header row and exactly these columns: completion_id — string; identifier from test.csv. mask_rle — JSON list stored as a CSV cell; predicted hidden silhouette. Requirements: Include exactly one row for every test completion_id. Each mask_rle is a row-major list of alternating background and foreground run lengths, starting with background and totaling 65,536 pixels. Foreground denotes only the hidden silhouette in the target crop. An empty mask is [65536]. sample_submission.csv supplies all test IDs with empty predictions. Do not copy foreground from the supplied visible mask.
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Moving Acoustic Aperture

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cr4qy681cq73v7qxfj92qtn8e92zb
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Moving Acoustic Aperture Overview Fine-tune a spatial listening model that behaves like a moving acoustic camera. Each query describes an angular cone sweeping through a real ten-second soundscape, plus a maximum source distance. Predict class-labelled, half-open time intervals when an annotated sound source is inside the cone. Ignore outside sounds even when loud. Multiple classes may overlap; simultaneous sources of the same class merge into their union of active time. Unlike ordinary sound-event detection over a recording, the same audio window can yield different intervals, or an empty list, for different moving apertures and distance limits. At annotation frame f in 0–99, the cone center is azimuth_start + sweep_degrees*f/99 degrees. Elevation and half-angle are constant. A source qualifies when its great-circle angle to the center is at most the half-angle and its native distance is at most the maximum. Azimuth wraps. Time resolution is 0.1 seconds. Evaluation Submissions are scored by a room- and presence-stratified harmonic mean of query scores. Query scores range from 0 to 1; higher is better. Invalid submissions or missing test IDs score zero. For a query with gold events, predictions are sorted by descending confidence, then class, start, and end. Each prediction is greedily paired with the unused gold event of the same class that has the greatest interval IoU. A pair is a true positive only when IoU is at least 0.5. Average precision (AP) is the sum of precision at each true-positive rank divided by the number of gold events. Event F1 is 2 × true positives / (predicted events + gold events). Boundary F1 is 2 × boundary credit / (predicted events + gold events); each matched start and end earns 0.5 credit when within 0.2 seconds. The query score is 0.5 × AP + 0.3 × event F1 + 0.2 × boundary F1. A query with no gold events scores 1 only when its prediction is empty. Query scores are averaged within each private room and presence stratum. Room means are averaged separately for present and absent apertures, then combined by their harmonic mean, 2pn/(p+n). Dataset The prepared public/ directory contains train.csv, test.csv, sample_submission.csv, classes.json, audio/, and features/. Audio files are 24 kHz, four-channel first-order Ambisonics recordings. Optional feature files contain four log-magnitude and three signed active-intensity channels with shape 7×64×1000; they are not calibrated range measurements. classes.json maps class IDs 0–12 to names. All paths in the CSV files are relative to public/. CSV columns (name — type — description): aperture_id — string; unique query identifier. audio — string path; four-channel audio file in audio/. features — string path; optional precomputed feature file in features/. azimuth_start — integer degrees; cone-center azimuth at frame 0. sweep_degrees — integer degrees; total azimuth sweep through frame 99. elevation — integer degrees; constant cone-center elevation. half_angle — integer degrees; cone half-angle. max_distance_cm — integer centimetres; maximum qualifying native source distance. episodes — JSON list; labelled intervals in train.csv only, absent from test.csv. Each training episode contains class, start, end, and confidence. Intervals are half-open [start,end). sample_submission.csv supplies every test aperture_id with an empty episodes list. Test rows contain no episode labels. Window sampling For platform preparation, each source recording is inspected at ten-second windows beginning at 0, 30, 60 seconds, and so on. Windows lacking native activity are omitted. The query geometry and presence-stratified retention remain unchanged. This deterministic one-in-three window sampling reduces package size; the native train/test room split is retained. Training and resource rules This is GPU fine-tuning for query-conditioned spatial sound-event retrieval. Use one A10G or H100, at most 62 GB host RAM, and 90 minutes including training and inference. The reference reserves 65 minutes for fine-tuning a generic encoder; target-GPU timing is unverified. Use supplied inputs and annotations plus permitted generic initialization only. External audio/task data, task-specific SELD weights, source lookup, test-answer access, external services, manual test labelling, and test-time learning are prohibited. Save fine-tuned weights and a complete timing log. CPU I/O and interval serialization are allowed. Organizer review may disqualify rule violations independently of score. Submission Submit a CSV file with exactly these columns and a header row: aperture_id — string; query identifier from test.csv. episodes — JSON list stored as a CSV cell; predicted class-labelled time intervals. Include exactly one row for every test aperture_id and no other rows. Each episodes cell may contain an empty list []) or events such as [{"class":2,"start":1.2,"end":2.7,"confidence":0.8}]. Use at most 300 nonduplicate events per query. Each event must have class 0–12, finite times with 0 ≤ start < end ≤ 10, and confidence in [0,1]. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Codon-Consistent Splice Chain Selection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c3ps3ft05v07q6ktd059xqn8ebcqm
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.571!

Full challenge description from page:

> Objective Recover a complete, ordered splice-junction chain from a noisy, transcript-oriented DNA sequence and candidate donor and acceptor sites. Select the true sites among plausible decoys and report the cumulative coding phase at every junction. Fine-tune a general pretrained model on the supplied training examples, then decode a globally consistent chain. Training, inference and decoding share a 90-minute offline budget of at most 10 CPU cores and 62 GB RAM. General pretrained weights may be acquired before execution; task-specific fitting and model selection must use only the supplied training labels. Public files train.csv: columns id,sequence,sites,chain. test.csv: columns id,sequence,sites. train_groups.csv: columns id,locus_group,family_group, providing opaque grouping keys for validation. sample_submission.csv: columns id,chain, with an empty chain for every test ID. Training contains three independently corrupted views per locus. All views share the same candidate coordinates and kinds, with independently shuffled local IDs. Candidate recurrence across views therefore does not identify true junctions. Evaluation contains one view per locus. Complete protein-family components are held out; identical loci connect family aliases before splitting. Group validation by family_group, keeping every view of a locus together. IDs and group labels are arbitrary identifiers, not predictive features. Inputs and observation errors sequence contains A, C, G, T and possibly N. Retained loci are 500–18,000 bases long and contain 3–16 annotated exons. Seeded, length-preserving corruption uses a position-dependent replacement-attempt probability centered at 0.08 and clipped to [0.01,0.18], short reversals of 3–5 bases, and random-base bursts of 2–6 bases. A replacement may retain the same base. Candidate coordinates and labels remain in the original coordinate system. sites is an unordered JSON list of objects with id (a local label such as s0), kind (donor or acceptor), and position (a zero-based boundary between bases). Each kind has up to 64 candidates, including every true site and additional motif-like decoys, for at most 128 sites per row. Local numbering and list order do not indicate transcript order. A donor at d ends the preceding exon at d. An acceptor at a starts the next exon at a. The intron occupies the half-open interval [d,a). Target chain and coding phase Return a JSON array of triples [donor_id,acceptor_id,phase] in transcript order. The initial coding region starts at boundary zero. Phase is the cumulative number of coding bases before that intron modulo 3, represented by integer 0, 1 or 2. Count the initial exon up to the first donor, then each intervening exon from the preceding acceptor to the next donor. This is a cumulative coding-length definition, not a file-format phase convention. Maintain positive-length introns and increasing, nonoverlapping coordinates. Do not reuse a site. The submission format permits up to 30 junctions. [["s1","s8",1],["s11","s3",0],["s4","s9",2]] Evaluation Complete-chain recovery and junction-level accuracy receive equal weight. Treat each complete triple as one symbol. Let D be unit-cost Levenshtein distance between the predicted and reference symbol sequences, and let M be the reference chain length. row_score = 0.5 × I(predicted_chain == reference_chain) 0.5 × max(0, 1 − D / max(M, 1)) The final score is the arithmetic mean of row scores. An exact chain scores 1. An incorrect phase makes a triple incorrect. Missing, extra and substituted junctions each incur unit edit cost. For a reference of four junctions, one substituted junction scores 0.375; appending an extra junction to an otherwise exact chain also scores 0.375. Extra predictions cannot enlarge the normalization denominator. The grader validates JSON structure, local-ID syntax, integer phases and site reuse. It does not load coordinates to validate site existence, kind or coordinate progression. Syntactically valid but incorrect triples are scored through edit distance. Solvers should enforce biological and coordinate constraints during decoding. Submission contract Submit UTF-8 CSV with exactly two ordered columns, id,chain, and every test ID exactly once. CSV row order is irrelevant; junction order matters. Quote JSON cells using standard CSV escaping. Missing, extra, duplicate or unknown row IDs, incorrect columns, or files larger than 50,000,000 bytes score zero for the whole submission. Each chain cell is limited to 12,000 characters and 30 triples. An empty array is valid. Local labels must use canonical syntax s0 through s999, without leading zeros; actual sites are supplied in each row. Two sites in a triple must differ and no site may recur in that chain. Booleans are invalid phases. Malformed JSON, invalid triples, invalid IDs or phases, and reused sites score zero for that row. Permitted information Use the public training sequences and chains for task-specific learning and validation. Evaluation sequences are for inference only. Do not use external task annotations, biological databases, hidden labels, hosted inference, manual evaluation annotation, hard-coded answers or identifier shortcuts. All computation during the run must remain offline.
> Closes in 7h 4m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

