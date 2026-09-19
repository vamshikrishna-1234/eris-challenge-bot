# Fine-Tuning Challenge Examples

Scrape timestamp: 2026-07-01T06:39:43+05:30

Confirmed examples in this document: 38

These entries are included only because the challenge detail page displayed this target domain. Titles were not used for classification.

## Cross-Source Evidence Grounding Assessment
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78m63g68caqc39fqpzf7jpyx857x7v
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, multimodal
- Best/top context found: fate1997 ranked 1st (leaderboard #1, score —)

Full challenge description from page:

> Overview
> The goal of this challenge is to fine-tune a pretrained LLM that will find shortest Python lambda solutions for small algorithmic tasks.
> Each sample provides a natural-language specification in description, a set of input/output examples in examples, and a numeric difficulty score.
> The dataset mixes several task styles, including short arithmetic, comparison, boolean, indexing, list, string, grouping, parsing, recursion, dynamic-programming, and pattern-matching tasks. Reference solutions are compact one-line lambdas, and the metric rewards both correctness and brevity, so shorter correct code scores better than longer correct code.
> The intended way to solve this benchmark is to fine-tune a pretrained LLM to generate short Python lambdas from the task text and examples. Submissions that primarily exploit the dataset, grader, hidden examples or sandbox rather than solve the tasks as intended will be rejected.
> The following submission behaviors are not allowed:
> manually finding solution for each sample
> relying on blocked libraries or blocked builtins inside submitted code
> using reflection, interpreter internals or any bypass tricks instead of solving the tasks as intended
> any method intended primarily to exploit the benchmark, hidden examples, grader behavior or dataset structure rather than solve the tasks themselves
> using LLM API
> Any submission found to rely on these disallowed approaches will be rejected even if it achieves a high score.
> To sum up: you have to fine-tune a pretrained LLM, any other approach will be rejected.
> Evaluation
> Submissions are evaluated using difficulty-weighted score.
> For each test row:
> the submitted code string is parsed and evaluated inside a fresh isolated worker process
> the submitted code must parse to a single lambda expression
> that lambda is executed on every visible and hidden example for that row
> if parsing fails, execution raises an error, execution times out, the return type is unsafe, or any returned value differs from the expected example["output"], that row receives 0
> For correct rows, the grader computes:
> golf_score = len(reference_code.strip()) / len(submitted_code.strip())
> score = 100 * sum(difficulty_i * golf_score_i) / sum(difficulty_i)
> where:
> reference_code is the hidden gold solution for that test row
> submitted_code is your submitted code string
> difficulty_i is the difficulty value for that row
> This means:
> incorrect rows contribute 0
> correct but longer solutions score below the reference baseline for that row
> correct solutions matching the reference length score 1.0 for that row before weighting
> shorter correct solutions score above 1.0 for that row before weighting
> harder tasks contribute more because of the difficulty weight
> The grader applies a 5 second timeout per test row, uses a memory cap and compares outputs type-sensitively. For example, True does not count as 1.
> Scores are therefore interpreted as follows:
> 0.0 means nothing was solved correctly
> 100.0 means every test task was solved correctly at exactly the hidden reference-code length
> above 100.0 is possible if a submission beats the reference solutions on code length
> The true shortest solutions are not known, so there is no strict hard cap. The effective maximum is estimated around 120, while matching all reference solutions gives score 100.
> Dataset
> The source dataset contains 240 Python function-synthesis tasks in total.
> train.jsonl: 40 rows
> test.jsonl: 200 rows
> Each task is self-contained and includes examples that define the intended behavior of the target function.
> For every test row, exactly 4 examples are hidden for private evaluation and the remaining examples are released in test.jsonl.
> Answers are heterogeneous and may be JSON-serializable Python values such as:
> integers
> strings
> booleans
> lists
> dictionaries
> floating-point values
> Difficulty scores are floating-point values on an approximate 1.0 to 10.0 scale, where larger values indicate harder tasks.
> File descriptions
> train.jsonl - training set with fields: id, description, code, examples, difficulty
> test.jsonl - test set with fields: id, description, examples, difficulty
> sample_submission.csv - example submission file with columns: id, code
> Column descriptions
> id - integer identifier, unique within the released split
> description - natural-language specification of the target function
> code - reference solution for train rows; prediction target for test rows
> examples - list of dictionaries with input and output keys
> difficulty - floating-point difficulty score included in both train and test
> Each examples entry has the form:
> {"input": [1, 2], "output": 3}
> The released split uses dense integer ids starting at 1 within each split.
> Allowed Python subset
> The official grader evaluates submissions inside an isolated worker that accepts only a small expression-oriented subset of Python. Submissions must be single lambda expressions.
> Allowed standard-library modules
> The only standard-library modules that may be imported, via __import__, are:
> itertools
> math
> re
> functools
> statistics
> collections
> string
> Allowed builtins
> The grader exposes only this builtin surface:
> abs
> all
> any
> bool
> bytes
> chr
> dict
> divmod
> enumerate
> filter
> float
> frozenset
> hash
> hex
> int
> iter
> len
> list
> map
> max
> min
> next
> oct
> ord
> pow
> range
> repr
> reversed
> round
> set
> slice
> sorted
> str
> sum
> tuple
> type
> zip
> __import__ (only for the allowed modules above)
> Submission
> You must submit a submission.csv file with a header and one row per test task.
> id: test task id
> code: predicted single Python lambda expression
> Example:
> id,code
> 1,"lambda a,b:a+b"
> 2,"lambda x:-x"
> 3,"lambda s:s[::-1]"
> Requirements
> The test set contains 200 rows with ids 1..200, so the submission file must contain exactly 200 predictions
> Must include the header row: id,code
> Must include each id exactly once, with no missing ids and no duplicates
> Must not contain missing or empty values in the code column
> Must save predictions to submission.csv

Inspiration note: Useful because it frames adaptation behavior as a supervised objective with clear held-out scoring, good for challenges about tuning without losing a target capability.

## Fine Tune Without Forgetting
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ek7cy6rgqy8n87e421jpcqh844w5p
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: duongnguyen ranked 1st (leaderboard #3, score —); nxify ranked 2nd (leaderboard #17, score —); haidang ranked #6 (leaderboard #24, score —)

Full challenge description from page:

> Overview
> Every ML engineer knows that fine-tuning a language model on a new domain degrades its performance on everything else. This is called catastrophic forgetting — and most competitions ignore it entirely. This one doesn't.
> You are tasked with fine-tuning any decoder-only model with at most 1.5 billion parameters (e.g. Qwen2.5-1.5B, Llama-3.2-1B, Phi-1.5, OPT-1.3B) to become a strong medical knowledge reasoner across 10 specific medical subjects, while surgically preserving its performance on the remaining 47 general subjects.
> This is not a simple medical QA challenge. It's a challenge about how you fine-tune — whether you use LoRA with carefully chosen target layers, elastic weight consolidation (EWC), replay buffers, gradient projection, or something entirely novel. The leaderboard rewards both skill AND precision.
> The scoring baseline is fixed at 0.473 general accuracy, measured once before the challenge launched by running Qwen2.5-0.5B-Instruct zero-shot on the general test questions. This number does not change based on which base model you choose. If your fine-tuned model exceeds 0.473 general accuracy, your retention is simply capped at 1.0 — you are not penalised for being better than the reference.
> Evaluation
> Submissions are scored using a Retention-Weighted Medical F1 metric:
> BASELINE_GENERAL_ACC = 0.473  # Fixed constant — does not change per submission
> def evaluate(medical_acc, general_acc):
> retention = min(general_acc / BASELINE_GENERAL_ACC, 1.0)
> score = 2 * medical_acc * retention / (medical_acc + retention)
> return score
> medical_acc is the accuracy on the held-out medical questions.
> general_acc is the accuracy on the held-out general questions.
> retention is how much of the 0.473 baseline you preserved, capped at 1.0.
> The score is the harmonic mean of medical accuracy and retention rate. A model that scores 0.90 medically but destroys 30% of general capability (retention = 0.70) achieves only 0.788 — lower than a model that scores 0.80 medically with perfect retention (0.889). Choosing a stronger base model helps medical accuracy but does not relax the retention requirement.
> Dataset
> You are provided with an auxiliary training set for fine-tuning and a hidden
> test set for evaluation.
> Files provided:
> train.csv contains approximately 99k auxiliary training questions across both medical and general domains, with correct answers included.
> test.csv contains 8,509 hidden test questions for final evaluation, with the answer column omitted. All other columns are identical to train.csv.
> sample_submission.csv contains two columns — id and answer — pre-filled with placeholder predictions (all A) across all 8,509 test rows. Use it as a template for the correct file format and to verify your id values match.
> Columns in train.csv:
> id is a string containing a unique opaque hex identifier (e.g. 0a3f9c12b4e1d8a7).
> question is a string containing the multiple-choice question text.
> A, B, C, and D are strings containing the text for each answer option. answer is a string containing the correct option — always exactly one of A, B, C, or D. This column is present only in train.csv and is omitted in test.csv.
> category is a string containing an obfuscated subject code (e.g. cat_3f9a12). Subject names are intentionally hidden — use is_medical to distinguish domains.
> is_medical is a boolean that is True if the question belongs to one of the 10 targeted medical subjects, and False if it belongs to one of the 47 general subjects.
> Columns in test.csv:
> id, question, A, B, C, D, category, and is_medical — identical in format to train.csv. The answer column is absent.
> Example row from train.csv:
> id: 0a3f9c12b4e1d8a7
> question: What is the primary function of the mitochondria in a eukaryotic cell?
> A: Protein synthesis
> B: Cellular respiration and ATP production
> C: Lipid storage
> D: DNA replication
> answer: B
> category: cat_3f9a12
> is_medical: True
> Submission
> Your agent must output a CSV file with exactly two columns: id and answer.
> id must be a string containing the exact hex identifier copied from test.csv (e.g. 0a3f9c12b4e1d8a7). Do not convert these to integers or modify them in any way. answer must be a string containing your model's prediction — exactly one of A, B, C, or D.
> The file must contain exactly 8,509 rows of predictions plus a header row.
> Use sample_submission.csv as your starting template — it already contains all 8,509 correct id values for you to fill in.
> Example:
> id,answer
> 0a3f9c12b4e1d8a7,A
> 1b8e2d45c3f0a912,C
> 2c1a7b89d4e3f056,B
> Recommended Approach
> Choose any decoder-only model with at most 1.5B parameters from HuggingFace.
> Fine-tune using your chosen technique — LoRA, EWC, gradient surgery, replay buffers, or anything else — targeting is_medical == True rows in train.csv while minimising impact on general knowledge.
> Run inference on test.csv. Format each question as: "Question: {question}\nA) {A}\nB) {B}\nC) {C}\nD) {D}\nAnswer:"
> Extract the first token's argmax over the [A, B, C, D] logits.
> Use sample_submission.csv as your template — fill in the answer column and submit.

Inspiration note: Useful because it frames adaptation behavior as a supervised objective with clear held-out scoring, good for challenges about tuning without losing a target capability.

## Python Code Golf Fine-Tuning Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ce9ew0sdkvrfhpfn26jkh1h846dzg
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Hard
- GPU: H100
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: akhil989899 ranked 1st (leaderboard #49, score —); osman0 ranked #7 (leaderboard #43, score —)

Full challenge description from page:

> Overview
> The goal of this challenge is to fine-tune a pretrained LLM that will find shortest Python lambda solutions for small algorithmic tasks.
> Each sample provides a natural-language specification in description, a set of input/output examples in examples, and a numeric difficulty score.
> The dataset mixes several task styles, including short arithmetic, comparison, boolean, indexing, list, string, grouping, parsing, recursion, dynamic-programming, and pattern-matching tasks. Reference solutions are compact one-line lambdas, and the metric rewards both correctness and brevity, so shorter correct code scores better than longer correct code.
> The intended way to solve this benchmark is to fine-tune a pretrained LLM to generate short Python lambdas from the task text and examples. Submissions that primarily exploit the dataset, grader, hidden examples or sandbox rather than solve the tasks as intended will be rejected.
> The following submission behaviors are not allowed:
> manually finding solution for each sample
> relying on blocked libraries or blocked builtins inside submitted code
> using reflection, interpreter internals or any bypass tricks instead of solving the tasks as intended
> any method intended primarily to exploit the benchmark, hidden examples, grader behavior or dataset structure rather than solve the tasks themselves
> using LLM API
> Any submission found to rely on these disallowed approaches will be rejected even if it achieves a high score.
> To sum up: you have to fine-tune a pretrained LLM, any other approach will be rejected.
> Evaluation
> Submissions are evaluated using difficulty-weighted score.
> For each test row:
> the submitted code string is parsed and evaluated inside a fresh isolated worker process
> the submitted code must parse to a single lambda expression
> that lambda is executed on every visible and hidden example for that row
> if parsing fails, execution raises an error, execution times out, the return type is unsafe, or any returned value differs from the expected example["output"], that row receives 0
> For correct rows, the grader computes:
> golf_score = len(reference_code.strip()) / len(submitted_code.strip())
> score = 100 * sum(difficulty_i * golf_score_i) / sum(difficulty_i)
> where:
> reference_code is the hidden gold solution for that test row
> submitted_code is your submitted code string
> difficulty_i is the difficulty value for that row
> This means:
> incorrect rows contribute 0
> correct but longer solutions score below the reference baseline for that row
> correct solutions matching the reference length score 1.0 for that row before weighting
> shorter correct solutions score above 1.0 for that row before weighting
> harder tasks contribute more because of the difficulty weight
> The grader applies a 5 second timeout per test row, uses a memory cap and compares outputs type-sensitively. For example, True does not count as 1.
> Scores are therefore interpreted as follows:
> 0.0 means nothing was solved correctly
> 100.0 means every test task was solved correctly at exactly the hidden reference-code length
> above 100.0 is possible if a submission beats the reference solutions on code length
> The true shortest solutions are not known, so there is no strict hard cap. The effective maximum is estimated around 120, while matching all reference solutions gives score 100.
> Dataset
> The source dataset contains 240 Python function-synthesis tasks in total.
> train.jsonl: 40 rows
> test.jsonl: 200 rows
> Each task is self-contained and includes examples that define the intended behavior of the target function.
> For every test row, exactly 4 examples are hidden for private evaluation and the remaining examples are released in test.jsonl.
> Answers are heterogeneous and may be JSON-serializable Python values such as:
> integers
> strings
> booleans
> lists
> dictionaries
> floating-point values
> Difficulty scores are floating-point values on an approximate 1.0 to 10.0 scale, where larger values indicate harder tasks.
> File descriptions
> train.jsonl - training set with fields: id, description, code, examples, difficulty
> test.jsonl - test set with fields: id, description, examples, difficulty
> sample_submission.csv - example submission file with columns: id, code
> Column descriptions
> id - integer identifier, unique within the released split
> description - natural-language specification of the target function
> code - reference solution for train rows; prediction target for test rows
> examples - list of dictionaries with input and output keys
> difficulty - floating-point difficulty score included in both train and test
> Each examples entry has the form:
> {"input": [1, 2], "output": 3}
> The released split uses dense integer ids starting at 1 within each split.
> Allowed Python subset
> The official grader evaluates submissions inside an isolated worker that accepts only a small expression-oriented subset of Python. Submissions must be single lambda expressions.
> Allowed standard-library modules
> The only standard-library modules that may be imported, via __import__, are:
> itertools
> math
> re
> functools
> statistics
> collections
> string
> Allowed builtins
> The grader exposes only this builtin surface:
> abs
> all
> any
> bool
> bytes
> chr
> dict
> divmod
> enumerate
> filter
> float
> frozenset
> hash
> hex
> int
> iter
> len
> list
> map
> max
> min
> next
> oct
> ord
> pow
> range
> repr
> reversed
> round
> set
> slice
> sorted
> str
> sum
> tuple
> type
> zip
> __import__ (only for the allowed modules above)
> Submission
> You must submit a submission.csv file with a header and one row per test task.
> id: test task id
> code: predicted single Python lambda expression
> Example:
> id,code
> 1,"lambda a,b:a+b"
> 2,"lambda x:-x"
> 3,"lambda s:s[::-1]"
> Requirements
> The test set contains 200 rows with ids 1..200, so the submission file must contain exactly 200 predictions
> Must include the header row: id,code
> Must include each id exactly once, with no missing ids and no duplicates
> Must not contain missing or empty values in the code column
> Must save predictions to submission.csv

Inspiration note: Useful because it frames adaptation behavior as a supervised objective with clear held-out scoring, good for challenges about tuning without losing a target capability.

## Bitemporal Remote-Sensing Change Captioning & Grounding
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77gpb8h25bxjqsne7txs5qw988dv6k
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat cosmos's score of 0.817!

Full challenge description from page:

Task
Each sample is a bitemporal pair: two co-registered overhead images of the same location at two different times — image_t1 ("before") and image_t2 ("after"). From the two images alone, produce four things about the change between them:
predicted_caption — one natural-language sentence describing what changed, e.g. "several buildings were constructed on the bare ground in the lower-left." When nothing of substance changed, say so (e.g. "no change").
predicted_change_flag — 1 if a real change occurred, 0 if not. This is an explicit detection output: the grader uses this column directly and never infers change/no-change from your caption text.
predicted_cell — where the dominant change is, as a cell of a 3×3 grid over the image (reading order), or 0 if there is no change:
1 2 3
4 5 6      (1 = top-left, 5 = centre, 9 = bottom-right)
7 8 9
predicted_direction — what kind of change dominates: appeared (a built structure replaced natural land cover), removed (a structure was cleared back to natural cover), or modified (one land-cover type became another); none if there is no change.
This is a generative, multi-image problem with a localization+typing twist: the caption is open-ended free text, and the cell/direction require reasoning about where and what kind of land-cover change occurred — not just echoing a sentence. About 28% of pairs are no-change, so deciding whether anything changed is also part of the task.
Why this needs a fine-tuned vision-language model
The caption is an open-ended sentence grounded in the difference between two overhead images (a ~1,000-word vocabulary); a single-image classifier cannot compare the pair, and a change-mask wired to a template cannot match the human references. The cell and direction force the model to localize and semantically type the change from both frames. Overhead imagery, the no-change convention, and the description style are out-of-distribution for a general VLM, so zero-shot prompting scores poorly — the intended solution is to fine-tune a small/medium multimodal LLM (e.g. with QLoRA) that reads both images and produces all three outputs.
The core difficulty
Generalize to unseen scenes. Train and test are split by source scene / region: every overlapping crop of an area is entirely in train or test. A model that memorizes train scenes (or retrieves the nearest train caption) will not transfer — the test scenes are geographically held out.
Localize + type the change, not just describe it. The 3×3 cell and the appeared/removed/modified direction reward genuine spatial + land-cover reasoning.
Real radiometric & registration noise (viewpoint, contrast, illumination, tonal, alignment): report true semantic change, not pixel/illumination artifacts.
Five-reference human variability. Each change pair has five human captions; the caption metric credits the best match, so it is bounded below 1.0.
These are real annotated overhead images — there is no synthetic structure to exploit.
Provided files
File	Description
train/<pair_id>_t1.jpg, _t2.jpg	256×256 RGB "before"/"after" images of one location.
test/<pair_id>_t1.jpg, _t2.jpg	Same format, held-out scenes.
train.csv	One row per pair: pair_id, image_t1, image_t2, change_flag (1/0), caption_1…caption_5 (five human references), gold_cell (1–9, 0 = none), gold_direction (appeared/removed/modified/none).
test.csv	One row per test pair: pair_id, image_t1, image_t2 only.
sample_submission.csv	The exact output schema: pair_id, predicted_caption, predicted_change_flag, predicted_cell, predicted_direction (blank / 0 / 0 / none baseline).
All targets (change_flag, captions, gold_cell, gold_direction) are given on train and withheld on test — you are scored on blind generalization. The grounding targets were derived from per-timepoint semantic land-cover maps.
Submission format
A CSV with one row per pair_id in test.csv and exactly these columns:
pair_id,predicted_caption,predicted_change_flag,predicted_cell,predicted_direction
rsc_8a1f...,"a new road appeared in the lower-left and buildings were built",1,7,appeared
rsc_91c2...,no change,0,0,none
...
predicted_caption — one free-text sentence (quote fields containing commas); keep it concise — captions longer than ~2× the reference length are penalized.
predicted_change_flag — 1 (change) or 0 (no change).
predicted_cell — integer 0–9 (0 = no change).
predicted_direction — one of none / appeared / removed / modified.
Missing rows/columns or blank values are scored as no credit on the affected term (never rejected). Duplicate pair_id keeps the last occurrence.
Evaluation metric
A single score in [0, 1] (higher is better), combining four skills:
score = 0.60 * CaptionScore     (describe the change)
+ 0.15 * CellScore        (localize it on the 3x3 grid)
+ 0.10 * DirectionScore   (type it: appeared / removed / modified)
+ 0.15 * max(0, MCC_change)   (detect whether anything changed)
CaptionScore — multi-reference chrF (char n-grams 1–6, β=2; max over the five references), averaged over the change pairs. A verbosity penalty scales chrF down when a prediction runs more than ~2× the reference length, so padding cannot farm the recall-weighted score. No-change pairs are not chrF-scored (a constant "no change" earns no caption credit).
CellScore — adjacency-tolerant credit vs gold_cell (the cell holding the most changed pixels): 1.0 exact, 0.5 if 3×3-adjacent, then chance-corrected by subtracting the best single constant cell the test set admits and renormalizing. So genuine localization scores partial credit for near-misses, while any constant cell — including "always predict the centre" — nets 0.
DirectionScore — macro-F1 over {appeared, removed, modified} vs gold_direction on change pairs (macro, so a constant direction scores low).
MCC_change — Matthews correlation between gold change_flag and your explicit predicted_change_flag column (read directly, never inferred from the caption). max(0,·) ⇒ any constant output scores 0 here.
Rules
Train only on the provided train/ data. Test scenes are geographically held out; do not identify or download the original source tiles from external copies of the underlying dataset — ids and images are anonymized.
All three outputs must be generated by a learned multimodal model that reads both images. A change-detector wired to an if/elif/f-string template, a retrieval-only caption lookup, or any hand-written generator fails the challenge's intent (and scores poorly on the held-out scenes).

Inspiration note: Useful because it frames model adaptation around a concrete editing, captioning, or physical-reasoning behavior that can be scored on held-out examples.

## Eight-Ball Pool Shot Outcome Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dmy9cn3fwtxr81q4x8ybfbs89e3qd
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat hermes's score of 0.304!

Full challenge description from page:

Eight-Ball Pool Shot Outcome Prediction
Overview
This is a visual physical-reasoning challenge for vision-language and vision models. Each puzzle shows
one initial top-down image of a pool table: the balls in their starting positions, a cue stick lined up
behind the cue ball showing the shot direction, a short aim line, and a power gauge in the top-left
showing how hard the shot is struck. You are then given several candidate result images (between 6 and
10), each a plausible final table state. Exactly one of them is the true outcome of playing that shot;
the rest are near-misses (outcomes of slightly different shots). Your job is to pick the index of the
true resulting state.
The task is hard on purpose and cannot be solved perfectly. The simulated physics includes small
stochastic cloth and ball imperfections (a tiny random impulse at every collision), so the exact
outcome of a shot is not fully determined even with perfect knowledge of the table. The distractors are
deliberately close to the true result, so distinguishing them requires genuine physical reasoning about
how the balls collide, rebound off the cushions, and settle, not surface cues.
How A Puzzle Is Presented
For each puzzle you receive one initial image and a set of option images. In the initial image: the
white ball is the cue ball; solids are balls 1 to 7, the 8 ball is black, and stripes are balls 9 to 15
(a colored band on white); the cue stick points in the shot direction from behind the cue ball, a faint
white aim line extends forward, and the red power gauge in the top-left indicates shot strength. Each
option image shows the same table after the balls have come to rest (balls that fall into a pocket are
removed). The cue stick, aim line, and power gauge appear only on the initial image.
Why This Formulation Is Hard To Game
An earlier version of this task asked solvers to regress the final position of every ball after the
shot. That formulation is easy to game: in a typical shot most balls move only a little or not at all,
so a trivial predictor that just copies the initial positions (a "nothing moves" baseline) already
achieves a low coordinate error, and such a metric rewards getting the many near-stationary balls right
rather than the physics of the few that actually move. We therefore use a forced-choice formulation
instead. Every candidate is a complete, physically simulated resting state, and the distractors are the
outcomes of slightly different shots. A "nothing moves" or "copy the input" strategy is not even a valid
option here, and surface heuristics (overall image similarity, total displacement, which option looks
closest to the start) collapse to chance, so the only way to score is to resolve which fine-grained
physical outcome actually occurred.
This also separates the task from deterministic billiards-prediction benchmarks that regress a final
state or collision labels from a known shot. Here the outcome is not a fixed function of the shot: small
stochastic cloth and ball imperfections (a random impulse at every collision) make the true resting
state irreducibly uncertain, and the candidate options differ at the scale of a single slightly
different shot. The model must discriminate between sub-shot-scale physical outcomes under genuine
aleatoric noise, which is exactly why detecting the layout and replaying a deterministic simulator
cannot exceed roughly 0.30 here (see Baselines), and why the maximum score is strictly below 1.
Dataset And Files
Every file and column is described here in prose.
The training data is organized one folder per puzzle under a train directory. Each puzzle folder is
named by its puzzle id (for example case_00123) and contains initial.jpg (the initial state) and
option_0.jpg, option_1.jpg, and so on up to option_(n-1).jpg, where n is that puzzle's number of
options. Images are JPEG, roughly 1060 by 610 pixels, RGB.
train_labels.csv gives the answers for the training puzzles, one row per puzzle, with columns:
puzzle_id (string), n_options (integer, how many option images that puzzle has, between 6 and 10), and
correct_index (integer, the 0-based index of the option image that is the true outcome).
The test data is organized the same way under a test directory (one folder per puzzle with initial.jpg
and option_*.jpg), but the answers are withheld. test_manifest.csv lists the test puzzles with columns
puzzle_id (string) and n_options (integer). You predict the correct option index for each.
sample_submission.csv shows the required submission shape: columns puzzle_id and prediction, with
prediction filled by a placeholder (0) that you replace.
There are 375 puzzles in total: 300 training puzzles and 75 test puzzles. Each puzzle has between 6 and
10 options.
Task And Submission Format
For every puzzle in test_manifest.csv, predict the 0-based index of the option image that is the true
result of the shot shown in that puzzle's initial image. Submit a CSV named submission.csv with exactly
two columns: puzzle_id (matching the test puzzles, one row per puzzle) and prediction (an integer in
the range 0 to n_options-1 for that puzzle). A puzzle missing from your submission, or with an
out-of-range or non-integer prediction, is scored as incorrect.
puzzle_id,prediction
case_00007,3
Evaluation Metric
Submissions are scored by multiple-choice accuracy: the fraction of test puzzles for which your
predicted option index equals the true one. The score is in [0, 1] and higher is better. A score of
1.0 (every puzzle correct) is not achievable, because the physics is stochastic and the true outcome
of a shot cannot be computed with certainty.
accuracy
=
1
𝑁
∑
𝑖
=
1
𝑁
1
[
𝑦
^
𝑖
=
𝑦
𝑖
]
accuracy=
N
1
​
∑
i=1
N
​
1[
y
^
​
i
​
=y
i
​
]
Runnable reference scorer (exactly how submissions are graded):
import pandas as pd, numpy as np
def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
a = answers.copy(); a["puzzle_id"] = a["puzzle_id"].astype(str)
corr = dict(zip(a["puzzle_id"], pd.to_numeric(a["correct_index"], errors="coerce")))
s = submission.copy(); s["puzzle_id"] = s["puzzle_id"].astype(str)
pred = dict(zip(s["puzzle_id"], pd.to_numeric(s["prediction"], errors="coerce")))
ids = [i for i in corr if not pd.isna(corr[i])]
if not ids: return 0.0
ok = sum(1 for i in ids if pred.get(i) is not None and not pd.isna(pred.get(i)) and int(pred[i]) == int(corr[i]))
return float(max(0.0, min(1.0, ok / len(ids))))
Baselines
Measured on the held-out test puzzles with the official metric (accuracy; higher is better):
Random guessing: about 0.13 (the puzzles average about 8 options).
Always predict option 0: about 0.21.
Naive image similarity (pick the option most similar to the initial image, or the one with the least
total ball movement): near chance.
A privileged detect-and-simulate solver that reads the ball positions, cue angle and power from the
image and runs an exact physics simulator: about 0.30, even with near-perfect detection. It cannot do
better because the stochastic cloth and ball imperfections make the exact outcome unknowable.
Perfect: 1.0, not achievable for the reason above.
The gap is the point. Surface heuristics sit near chance; a solver that actually reasons about the
shot physics reaches around 0.30, and a strong fine-tuned model can push further, but no method can
reach 1.0. The difficulty is intrinsic to the task, not a matter of detection precision.
Allowed And Prohibited
Allowed: fine-tuning pretrained vision-language or vision models on the provided training puzzles;
any architecture; learned physics or learned matching; standard data augmentation.
Prohibited: external pool or billiards datasets; detect-and-simulate pipelines (although they are
capped by the stochastic physics, not prohibited); attempting to recover the organizers' private
generation seed or the withheld answers by any means other than predicting from the provided images;
using the test answers. Predictions must come only from the provided images and your trained model.
Hardware And Compute
The reference environment is a single A10G GPU with a wall-clock limit of 1 hour per
fine-tuning-plus-inference run;
License
The images are fully synthetic, generated by the organizers' renderer, and are released under the
Creative Commons CC0 1.0 public-domain dedication. There is no external source dataset.

Inspiration note: Useful because it frames model adaptation around a concrete editing, captioning, or physical-reasoning behavior that can be scored on held-out examples.

## Japanese Reference Drift Forensics
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bbwfd7f1a1x2bejbzsepbvd82we99
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat osman0's score of 0.837!

Full challenge description from page:

Japanese Reference Drift Forensics
Overview
Japanese document assistants often fail in ways that a plain pass/fail judge does not explain. A customer-facing answer may use the wrong figure from a table, refuse a question that the document answers, or sound reasonable because it matches a neighboring reference from before the source was refreshed. In insurance, manufacturing, retail, public-sector, and IT knowledge bases, that distinction matters: teams need to know whether an answer is current, stale, numerically wrong, or missing the substance of the approved reference.
This challenge asks you to fine-tune a local judge that classifies the dominant failure signature of a Japanese answer. Each row provides a question_text, a current_reference, and a candidate_answer. The target is audit_signature, one of five labels:
fresh_match -- The candidate matches the current reference closely enough to pass.
stale_match -- The candidate is plausible but aligns with a nearby superseded reference instead of the current one.
numeric_conflict -- The candidate changes an amount, date, count, percentage, or other numeric detail.
bad_refusal -- The candidate refuses or says information is unavailable even though the reference answers the question.
content_gap -- The candidate omits, invents, or distorts non-numeric content.
The stale_match rows are intentionally close to real matches: they use nearest-neighbor references from the same generic sector and evidence type, not random topic swaps. The hidden test split is question-disjoint, so memorizing repeated questions or surface templates is not enough.
This is an LLM fine-tuning challenge. Strong solutions should adapt an offline open-weight Japanese-capable encoder or decoder model to compare the question, reference, and candidate answer. Classical text features may help with obvious numbers or refusals, but the hard cases require learned comparison behavior.
Dataset
File descriptions
train.jsonl -- Labeled forensic audit rows with audit_signature.
test.jsonl -- Unlabeled forensic audit rows with the same input fields.
sample_submission.csv -- Submission template with random valid audit signatures.
Column descriptions
id (string) -- Unique 12-character identifier for the audit row.
sector (string) -- Generic source-sector tag.
evidence_type (string) -- Evidence type behind the original source reference. Valid values are paragraph, table, and image.
question_text (string) -- Japanese user question.
current_reference (string) -- Current approved reference answer.
candidate_answer (string) -- Candidate assistant answer to inspect.
audit_signature (string, train.jsonl only) -- Target label. One of fresh_match, stale_match, numeric_conflict, bad_refusal, or content_gap.
Evaluation
Submissions are scored with a weighted Macro F1 score. The main term measures five-way audit-signature classification, and the secondary term rewards balanced performance across paragraph, table, and image-backed rows.
labels = ["fresh_match", "stale_match", "numeric_conflict", "bad_refusal", "content_gap"]
overall = f1_score(y_true, y_pred, labels=labels, average="macro")
score = 0.70  *overall + 0.30*  mean(per_evidence_type_macro_f1)
Macro F1 matters because smaller classes such as bad_refusal and numeric_conflict are operationally important even when they appear less often than clean matches. The evidence-type term prevents solutions from doing well only on paragraph rows while missing table and image cases.
Submission
Submit a CSV file with one audit signature for every row in test.jsonl.
id (string) -- The 12-character identifier from test.jsonl.
audit_signature (string) -- One of fresh_match, stale_match, numeric_conflict, bad_refusal, or content_gap.
Example:
id,audit_signature
0015e4d538cb,stale_match
001e11f89d04,fresh_match
00256d83e6a7,content_gap
Requirements
The file must contain exactly one row for every row in test.jsonl.
Every id from test.jsonl must appear exactly once.
audit_signature must not contain missing values.
Every prediction must be one of the five allowed labels.
File format: .csv only, with exact column names id,audit_signature.
What Not To Use
Do not use zero-shot or few-shot prompting as the main classifier, this task is intended to test local fine-tuning or training on the released supervision.
Do not recover source documents, vendor names, original audit exports, or labels through fuzzy matching against external sources.
Do not key predictions to test ids, row order, hashed identifiers, or memorized source-question groups.
Do not hand-label test rows by manual inspection.

Inspiration note: Useful because it frames model adaptation around a concrete editing, captioning, or physical-reasoning behavior that can be scored on held-out examples.

## Reaction Protocol Silent-Edit Repair
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79w4qdp3ds19x2ctfy99z6y189gd0g
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat lock's score of 0.705!

Full challenge description from page:

Reaction Protocol Silent-Edit Repair
Overview
Chemistry lab notebooks often contain terse protocol notes that are later corrected by an audit trail. A useful model must not only read the recorded procedure, but also apply the silent-edit notice and regenerate the corrected protocol in the lab's canonical sequence format.
Your task is to generate a repaired six-slot reaction protocol sequence from a lab note and a correction notice. Each input gives a reaction-family header, a noisy protocol note, and one silent-edit correction written as local bench shorthand. Some copied notes are mixed-order, use local bench tags, or omit a background operation, so a useful model must infer the complete repaired procedure from the family, visible note evidence, and correction notice. The output is a semicolon-separated canonical sequence covering setup preparation, activation, addition order, control condition, quench, and workup.
This is a Chemistry x sequence-to-sequence fine-tuning task. The practical goal is protocol-log normalization: when a corrected audit note changes part of an experiment record, downstream robotic execution, safety review, and reproducibility checks need the complete repaired protocol sequence rather than a single local tag.
Dataset
File descriptions
train.jsonl -- 1,676 instruction/input/output examples for sequence-model training or fine-tuning.
test.jsonl -- 524 held-out instruction/input examples without repaired outputs.
train.csv -- CSV mirror of train.jsonl with prompt text and the repaired_sequence output.
test.csv -- CSV mirror of test.jsonl with prompt text but without repaired_sequence.
sample_submission.csv -- A template showing the required submission format with random valid-looking repaired sequences.
Column descriptions
id (string) -- Unique 12-character hex identifier for each protocol repair case.
prompt (string) -- Full input text containing the reaction-family header, protocol note, correction notice, and generation request.
protocol_note (string) -- The recorded lab-note text before applying the silent-edit correction.
correction_notice (string) -- The audit correction that overrides one recorded protocol slot through local bench shorthand.
instruction (string) -- JSONL instruction telling a model to generate only the repaired canonical protocol sequence.
input (string) -- JSONL input text equivalent to prompt.
output (string) -- Target field in train.jsonl only. Same content as repaired_sequence.
repaired_sequence (string) -- Target field in train.csv and submission column. The value must contain six ordered slot assignments separated by semicolons: prep, activation, order, control, quench, and workup.
Evaluation
Submissions are scored using Operation-Weighted Repair Sequence Score. Higher is better.
Each submitted repaired_sequence is parsed into six ordered slot assignments. The grader gives weighted credit for each slot that exactly matches the private repaired sequence, then averages scores within hidden reaction/edit groups before taking the final mean.
Setup preparation, control condition, and quench receive the largest weights because those silent edits most often change safety-critical handling. Activation, addition order, and workup still contribute to the score, but they carry less weight than the corrected operating-condition slots.
Numeric slot weights are prep=2.20, activation=0.85, order=0.60, control=3.00, quench=4.00, and workup=0.25. For one row, row_score = (2.20 prep_correct + 0.85 activation_correct + 0.60 order_correct + 3.00 control_correct + 4.00 quench_correct + 0.25 workup_correct) / 10.90, where each *_correct term is 1 if the predicted slot value exactly matches the private answer and 0 otherwise. The final score is the mean of row_score within each hidden reaction/edit group, averaged equally across groups.
The score ranges from 0 to 1. Random valid sequences should score near the low baseline. Stronger solutions should improve by training on the public examples, learning the local shorthand, and generating the full repaired sequence rather than only the edited slot.
Submission
Submit a CSV file with one generated repaired sequence for every row in test.jsonl or test.csv.
id (string) -- The 12-character hex identifier from the test file.
repaired_sequence (string) -- The generated canonical protocol sequence, exactly six semicolon-separated slot assignments in this order: prep, activation, order, control, quench, workup.
Example:
A valid submission file looks like this:
id,repaired_sequence
008d7291f5ca,prep=degas;activation=preactivate_oxidant;order=oxidant_portionwise;control=warm_hold;quench=no_quench;workup=organic_extract
00ac6657ce3d,prep=degas;activation=preactivate_oxidant;order=substrate_slow;control=vented_hold;quench=water_slow;workup=direct_concentrate
01870a3efc75,prep=dry_glass;activation=preactivate_oxidant;order=oxidant_portionwise;control=vented_hold;quench=no_quench;workup=solvent_swap
Requirements
The file must contain exactly 524 rows plus the header.
Every id from the test file must be present exactly once.
repaired_sequence must contain exactly six assignments separated by semicolons.
Slot names must appear exactly in this order: prep, activation, order, control, quench, workup.
Each assignment must use slot=value format with one of the valid values learned from public training examples.
Missing predictions, duplicate ids, malformed slot order, invalid values, extra columns, and wrong row counts are invalid.
File format: .csv only, with exact column names id,repaired_sequence.
What Not To Use
Do not build the main solution as a handwritten parser that only recognizes the visible note templates or bench-cue phrases. Diagnostic and post-processing rules are fine, but the submitted method should ONLY fine-tune a model on the public examples.
Do not submit a hardcoded map from test ids, full prompt strings, or memorized repaired_sequence values. The task is to learn the repair mapping from public examples.
Do not use externally shared answer tables, cached outputs, or leaked protocol-repair case maps to fill the held-out repaired sequences.
Do not ignore the correction_notice and predict only a common reaction-family sequence. The evaluated rows require applying the silent edit and regenerating all six slots.

Inspiration note: Useful because it frames model adaptation around a concrete editing, captioning, or physical-reasoning behavior that can be scored on held-out examples.
---

<!-- GOOGLE_DRIVE_APPEND_2026_07_01 -->
**Google Drive Folder Append (2026-07-01T08:30:33+05:30)**

These entries came from the two shared Google Drive folders. They may duplicate earlier examples because this append intentionally preserves all shared accepted/approved challenge specs. Drive entries use folder/domain labels when present and inference from the folder/spec text when no explicit DOMAIN field is available.

## Self-Supervised Histology Representations
- Challenge URL: https://drive.google.com/drive/folders/1RULlguw1YL68h1QZZN83vvuI8jckqLVq
- Source file: cd.txt
- DOMAIN used for this document: Fine-Tuning (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / Fine-Tuning / Self-Supervised Histology Representations

Full challenge description from Drive:

> Self-Supervised Histology Representations — A Hidden-Label Linear-Probe Benchmark
> Overview
> Plain-English summary. You receive 507 small histology images (256×256 RGB tiles cut from microscope photographs of stained tissue from 78 patients). Your job is to train a model that turns each tile into a numeric vector (an embedding). You submit those embeddings to the grader.
> The grader then probes your embeddings to see whether they linearly separate three categorical visual properties of the tissue that you do not get to see. The properties are real, image-grounded, and recoverable from pixels in principle — but the agent never knows which they are, never sees them in any public file, and cannot optimize for any single one. The score is the average failure rate of three frozen linear probes (one per hidden property): how much of each property your embedding fails to recover.
> This is the standard self-supervised representation evaluation protocol — linear evaluation on held-out categorical labels — applied to histopathology with one twist: the labels are not announced. You have to produce a general-purpose embedding rich enough that any reasonable downstream classification probe can read structure out of it.
> What the agent gets.
> All 507 tile PNGs.
> For ~340 training tiles: only the tile_id and an opaque patient_id. No categorical labels, no demographic targets — nothing else.
> For ~167 test tiles: same two columns, tile_id and patient_id.
> What the agent submits. One CSV with one row per public tile (train + test) and a fixed-dimensional embedding (between 16 and 1024 floats). The grader runs the three probes internally and returns a single composite score (lower is better).
> Evaluation
> The leaderboard score is the average failure rate of three frozen linear probes, each fit on the agent's submitted embeddings to recover a hidden categorical label.
> composite_score = mean over hidden labels of (1 − balanced_accuracy)
> Lower is better. The grader returns this single float. Range: 0.0 (every probe perfectly recovers its label) to ~1.0 (every probe scores at the chance balanced-accuracy).
> How each probe is computed
> For each hidden categorical label L:
> Standardise the agent's embeddings using statistics from the training tiles only (no test leakage).
> Fit a multinomial logistic-regression probe on training-tile embeddings → label L for that tile. L2-regularised, deterministic, frozen seed.
> Predict label L on the test-tile embeddings.
> Compute balanced_accuracy_score (the macro-averaged per-class recall) on the test predictions.
> The probe's contribution to the composite is 1 − balanced_accuracy.
> The composite averages over all three probes.
> Reference grading code
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """Composite score; lower is better."""
> # Extract the agent's embeddings from `submission`, aligned to the
> # tile_id ordering in `answers`.
> embed_cols = [c for c in submission.columns if c.startswith("embed_")]
> embed_cols.sort(key=lambda c: int(c.split("_", 1)[1]))
> answers_sorted = answers.sort_values("tile_id").reset_index(drop=True)
> embeddings = (
> submission.set_index("tile_id")
> .reindex(answers_sorted["tile_id"].astype(int))
> [embed_cols]
> .to_numpy(dtype=np.float64)
> )
> # Run one frozen linear probe per hidden label; aggregate.
> # The exact label names and count are kept private; see Evaluation prose
> # above for what the probes test conceptually.
> losses = []
> for label in _HIDDEN_LABELS:
> info = _probe_label(label, answers_sorted, embeddings)
> losses.append(1.0 - info["balanced_accuracy"])
> return float(np.mean(losses))
> Dataset
> You read everything from ./dataset/public/:
> dataset/public/tiles/tile_<NNNNNN>.png — 507 deterministic 256×256 RGB tile images. The integer <NNNNNN> is the tile ID, zero-padded to six digits.
> dataset/public/train_metadata.csv — one row per training tile (~340 rows). Two columns:
> tile_id (int) — the tile's image file is tiles/tile_<tile_id:06d>.png.
> patient_id (string) — opaque salted-hash patient identifier such as p5bc4a22a. Same hash for every tile from the same patient. Roughly 44 unique training patients.
> dataset/public/test_metadata.csv — one row per test tile (~167 rows). Same two columns.
> dataset/public/sample_submission.csv — example submission with 64-d zero embeddings; one row per public tile.
> Submission
> Write your predictions to ./working/submission.csv.
> Required schema (lists, not tables):
> One header row.
> tile_id (int) — every tile_id present in sample_submission.csv must appear exactly once. No duplicates, no extras, no missing.
> embed_0 (float) — first embedding dimension.
> embed_1 (float) — second embedding dimension.
> ...
> embed_<K-1> (float) — final embedding dimension.
> Embedding dimension K must satisfy 16 ≤ K ≤ 1024.
> Embedding column names must be embed_0, embed_1, ..., contiguous from 0.
> All embedding values must be finite (no NaN, no Inf).
> Concrete example of a correctly formatted submission (first 6 rows of a real 32-d submission):
> tile_id,embed_0,embed_1,embed_2,embed_3,embed_4,embed_5,embed_6,embed_7,embed_8,embed_9,embed_10,embed_11,embed_12,embed_13,embed_14,embed_15,embed_16,embed_17,embed_18,embed_19,embed_20,embed_21,embed_22,embed_23,embed_24,embed_25,embed_26,embed_27,embed_28,embed_29,embed_30,embed_31
> 0,0.5821,0.4112,0.3987,0.0834,0.0712,0.0613,-0.1422,0.2871,1.4113,-0.5832,2.0814,1.1427,0.1814,0.7203,0.4519,-0.2308,0.6112,0.4287,0.4081,0.0921,0.0788,0.0701,0.2841,0.1822,0.0033,0.0091,0.0044,0.0061,0.4922,0.6841,0.4117,-0.1182
> 100,0.6014,0.4209,0.4061,0.0911,0.0782,0.0681,-0.1311,0.2954,1.3982,-0.5601,2.1102,1.1683,0.1905,0.7411,0.4622,-0.2196,0.6244,0.4391,0.4172,0.0992,0.0853,0.0764,0.2932,0.1894,0.0035,0.0094,0.0046,0.0064,0.5031,0.6952,0.4198,-0.1097
> 101,0.5993,0.4188,0.4040,0.0892,0.0763,0.0664,-0.1342,0.2929,1.4022,-0.5673,2.1009,1.1605,0.1880,0.7349,0.4592,-0.2231,0.6202,0.4358,0.4144,0.0972,0.0833,0.0745,0.2904,0.1872,0.0034,0.0093,0.0045,0.0063,0.4998,0.6918,0.4173,-0.1124
> 1300,-0.4112,0.2914,0.5183,0.1241,0.0982,0.0822,0.4331,-0.1112,0.6224,-0.2812,1.5113,0.8232,0.2114,0.5114,0.3219,-0.1108,-0.4011,0.2812,0.5093,0.1192,0.0941,0.0791,-0.1192,0.0822,0.0011,0.0021,0.0019,0.0024,-0.0822,0.5114,0.3214,0.0741
> 1301,-0.4082,0.2891,0.5152,0.1224,0.0967,0.0810,0.4282,-0.1093,0.6172,-0.2784,1.5042,0.8181,0.2098,0.5081,0.3198,-0.1094,-0.3982,0.2792,0.5066,0.1175,0.0928,0.0780,-0.1175,0.0810,0.0011,0.0021,0.0018,0.0024,-0.0813,0.5082,0.3197,0.0732
> Notes:
> 33 columns total: one tile_id plus 32 embedding columns (embed_0 through embed_31).
> tile_id values are arbitrary integers (sample IDs from sample_submission.csv), not row offsets, and not necessarily contiguous.
> The two rows with tile_id 100 and 101 are training tiles from the same patient and look visually similar, so their embeddings are similar — that's expected.
> The rows with tile_id 1300 and 1301 are test tiles. There's nothing in the submission format that distinguishes train from test; you submit embeddings for all 507 tiles and the grader segments internally.
> Every value is a finite float. Negative numbers, values >1, values <0 are all valid.
> Requirements
> The submission must contain exactly the same set of tile_id values as sample_submission.csv, with the same number of rows.
> Embedding dimension K is fixed across all rows in your submission and must satisfy 16 ≤ K ≤ 1024.
> All standard Kaggle Python Docker libraries are available (pandas, numpy, scikit-learn, xgboost, lightgbm, tensorflow, pytorch, torchvision, timm, etc.). No external network access at submission time.
> What not to use
> The items below are out of bounds. Using any of them is grounds for automatic rejection of the submission, regardless of the leaderboard score.
> Prohibited data access
> Tile-level random splits on the public metadata. If you build your own validation set, group it by patient_id. A tile-level random split leaks across patients (because of staining-batch effects) and produces a CV score that bears no resemblance to the leaderboard.
> Hard-coding constant embeddings per patient_id. A submission whose embeddings are identical across all of a patient's tiles regardless of pixel content is gaming patient leakage rather than learning representations, and will be flagged.
> Prohibited model weights — train from scratch
> No pretrained weights of any kind. The encoder you submit embeddings from must be trained only on the 507 tiles in this dataset, starting from random initialisation. The whole point of the challenge is to test whether real self-supervised learning from scratch on this small cohort can produce useful representations; pretrained models sidestep that question entirely. Specifically prohibited:
> ImageNet-pretrained encoders. No torchvision.models.<arch>(weights="...") with any non-None weights argument. No timm.create_model(..., pretrained=True). No loading checkpoints from torch.hub, huggingface_hub, tensorflow_hub, or any equivalent.
> Histopathology foundation models. This includes (non-exhaustively) UNI, UNI2, CONCH, CONCHv1, Phikon, Phikon-v2, Lunit-DINO, HIPT, RetCCL, KimiaNet, Virchow, Virchow2, GPFM, PRISM, MUSK, and any other model whose weights were trained on histopathology corpora before the challenge. These are absolutely banned, even if the weights happen to be cached locally in the Kaggle environment.
> Generic vision foundation models. CLIP, DINO, DINOv2, MAE checkpoints, SAM, OpenCLIP, etc. — same rule, no pretrained weights.
> "Linear probe of a pretrained model" disguises. Loading a pretrained encoder, freezing it, and submitting its penultimate-layer activations is the exact failure mode this rule exists to forbid. It is not allowed.
> Self-distillation / teacher-student schemes that initialise either model from pretrained weights. The teacher must also be trained from scratch on the 507 tiles.
> Pretrained tokenisers / VAE encoders / diffusion model components when used to project tiles into a learned latent. Same rule.
> What is allowed: random initialisation, standard layer norms, hand-engineered feature pipelines (numpy / OpenCV / scikit-image filters), classical ML on raw or hand-engineered features, contrastive / masked / generative self-supervised objectives trained on this dataset only, simple architectures (small CNNs, small ViTs, MLPs) trained from scratch.
> Prohibited libraries and runtime behaviour
> External package installs at submission time. No pip install, conda install, apt-get, or shell-out installer scripts. Only libraries already in the Kaggle Python Docker image may be used.
> Network access at submission time. No urllib.request.urlopen, requests.get, httpx, huggingface_hub.snapshot_download, torch.hub.load_state_dict_from_url, or any equivalent call. (Pretrained weights are forbidden in any form, see above — this rule prevents downloading new ones at runtime.)
> Loading pretrained checkpoints from /kaggle/input/ or any other local path. Even if a checkpoint file is sitting on disk, your code must not load it. The encoder is trained from scratch.
> Histopathology-specific libraries that aren't in standard Kaggle Docker. Specifically histomicstk, staintools, histolab, openslide-python (the dataset has no WSI files), torchstain. If you want stain normalization, implement Macenko / Reinhard / Vahadane in pure numpy or torch instead.
> Prohibited evaluation tricks
> Inferring or guessing the hidden labels and one-hot-encoding them into the embedding. This is the central failure mode the protocol is designed to detect: an embedding that "happens to" perfectly classify all three hidden labels — when the agent never saw them — is suspicious. Reviewers will inspect submissions whose composite is implausibly low.
> Using RidgeCV / GridSearchCV against the leaderboard. There is no public leaderboard feedback loop and no public test labels to tune against.
> Reporting a single "best" run after re-rolling the seed many times. Reviewers will ask for a seed-controlled rerun; if your reported score is not reproducible from a single deterministic execution, the submission is rejected for unreliability.
> What Not To Use
> What not to use
> The items below are out of bounds. Using any of them is grounds for automatic rejection of the submission, regardless of the leaderboard score.
> Prohibited data access
> Tile-level random splits on the public metadata. If you build your own validation set, group it by patient_id. A tile-level random split leaks across patients (because of staining-batch effects) and produces a CV score that bears no resemblance to the leaderboard.
> Hard-coding constant embeddings per patient_id. A submission whose embeddings are identical across all of a patient's tiles regardless of pixel content is gaming patient leakage rather than learning representations, and will be flagged.
> Prohibited model weights — train from scratch
> No pretrained weights of any kind. The encoder you submit embeddings from must be trained only on the 507 tiles in this dataset, starting from random initialisation. The whole point of the challenge is to test whether real self-supervised learning from scratch on this small cohort can produce useful representations; pretrained models sidestep that question entirely. Specifically prohibited:
> ImageNet-pretrained encoders. No torchvision.models.<arch>(weights="...") with any non-None weights argument. No timm.create_model(..., pretrained=True). No loading checkpoints from torch.hub, huggingface_hub, tensorflow_hub, or any equivalent.
> Histopathology foundation models. This includes (non-exhaustively) UNI, UNI2, CONCH, CONCHv1, Phikon, Phikon-v2, Lunit-DINO, HIPT, RetCCL, KimiaNet, Virchow, Virchow2, GPFM, PRISM, MUSK, and any other model whose weights were trained on histopathology corpora before the challenge. These are absolutely banned, even if the weights happen to be cached locally in the Kaggle environment.
> Generic vision foundation models. CLIP, DINO, DINOv2, MAE checkpoints, SAM, OpenCLIP, etc. — same rule, no pretrained weights.
> "Linear probe of a pretrained model" disguises. Loading a pretrained encoder, freezing it, and submitting its penultimate-layer activations is the exact failure mode this rule exists to forbid. It is not allowed.
> Self-distillation / teacher-student schemes that initialise either model from pretrained weights. The teacher must also be trained from scratch on the 507 tiles.
> Pretrained tokenisers / VAE encoders / diffusion model components when used to project tiles into a learned latent. Same rule.
> What is allowed: random initialisation, standard layer norms, hand-engineered feature pipelines (numpy / OpenCV / scikit-image filters), classical ML on raw or hand-engineered features, contrastive / masked / generative self-supervised objectives trained on this dataset only, simple architectures (small CNNs, small ViTs, MLPs) trained from scratch.
> Prohibited libraries and runtime behaviour
> External package installs at submission time. No pip install, conda install, apt-get, or shell-out installer scripts. Only libraries already in the Kaggle Python Docker image may be used.
> Network access at submission time. No urllib.request.urlopen, requests.get, httpx, huggingface_hub.snapshot_download, torch.hub.load_state_dict_from_url, or any equivalent call. (Pretrained weights are forbidden in any form, see above — this rule prevents downloading new ones at runtime.)
> Loading pretrained checkpoints from /kaggle/input/ or any other local path. Even if a checkpoint file is sitting on disk, your code must not load it. The encoder is trained from scratch.
> Histopathology-specific libraries that aren't in standard Kaggle Docker. Specifically histomicstk, staintools, histolab, openslide-python (the dataset has no WSI files), torchstain. If you want stain normalization, implement Macenko / Reinhard / Vahadane in pure numpy or torch instead.
> Prohibited evaluation tricks
> Inferring or guessing the hidden labels and one-hot-encoding them into the embedding. This is the central failure mode the protocol is designed to detect: an embedding that "happens to" perfectly classify all three hidden labels — when the agent never saw them — is suspicious. Reviewers will inspect submissions whose composite is implausibly low.
> Using RidgeCV / GridSearchCV against the leaderboard. There is no public leaderboard feedback loop and no public test labels to tune against.
> Reporting a single "best" run after re-rolling the seed many times. Reviewers will ask for a seed-controlled rerun; if your reported score is not reproducible from a single deterministic execution, the submission is rejected for unreliability.

Inspiration note: Useful as a compact supervised adaptation pattern: small specialized data, constrained model behavior, and a measurable output format.

## Edge Medical Agent Multimodal Function Calling (Sub-500M)
- Challenge URL: https://drive.google.com/drive/folders/13L-gR7BDRaroxoG5-L4mGnY0HUB1xBFK
- Source file: cd.txt
- DOMAIN used for this document: Fine-Tuning (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / Fine-Tuning / Edge Medical Agent Multimodal Function Calling (Sub-500M)

Full challenge description from Drive:

> Edge Medical Agent: Multimodal Function Calling (Sub-500M)
> Overview
> Traditional Visual Question Answering (VQA) is insufficient for modern clinical workflows, which require structured data to trigger Electronic Health Record (EHR) systems. Furthermore, as point-of-care applications move toward edge computing, these AI agents must run efficiently on local hardware (like mobile or Android devices) without relying on cloud APIs.
> This challenge tasks you with fine-tuning a small Vision-Language Model (VLM) on a highly curated, data-constrained histopathology dataset. Your model must act as an autonomous agent outputting strict JSON function calls based on the visual context.
> There are two major complexities:
> The Hallucination Trap & Tool Selection: 30% of the image-question pairs in the test set have been intentionally scrambled to test anomaly detection. Your model must dynamically select the correct "tool" (JSON schema) based on the input:
> For binary questions: Emit the triage_binary tool.
> For open-ended pathology questions: Emit the log_pathology tool.
> For scrambled/illogical pairs: Emit the flag_anomaly tool.
> The Size Constraint: To ensure deployability for on-device inference, your final fine-tuned model must contain fewer than 500 million parameters.
> Evaluation
> Submissions are scored using a Strict JSON Parsing Accuracy metric.
> The evaluation script attempts to parse your predicted string as a JSON object. If the JSON is invalid, malformed, or missing quotes, you receive a score of 0 for that row. If it is valid, the parsed dictionary must exactly match the ground-truth dictionary structure, keys, and values.
> The formula is strictly calculated as:
> Score = Number of Exact JSON Matches / Total Predictions
> Dataset
> To evaluate true generalization and prevent data leakage from public benchmarks, this dataset is a custom, resampled, and data-constrained subset derived from larger medical archives. The original public dataset splits have been completely discarded and recombined.
> The provided splits consist of exactly 10,000 training instances and 2,500 testing instances.
> Image Properties:
> The images consist of heavily magnified tissue samples (histopathology). They represent a wide variety of physiological systems and are provided in RGB .jpg format.
> File Structure & Features:
> train/ — Directory containing 10,000 training .jpg images. Files are named with an obfuscated hash (e.g., a1b2c3d4e5f6.jpg).
> test/ — Directory containing 2,500 testing .jpg images.
> train.csv — Labeled training data (10,000 rows). Contains:
> image_id (string): The exact filename of the image.
> question (string): The medical query.
> answer (string): The ground truth target formatted as a strict JSON string.
> test.csv — Unlabeled test data (2,500 rows). Contains image_id (string) and question (string). (Note: 30% of these questions have been scrambled).
> sample_submission.csv — Example file demonstrating the expected format.
> What Not To Use
> To ensure solutions meet the criteria for on-device inference and genuine multimodal reasoning, the following techniques, models, and libraries are strictly prohibited:
> Closed-Source / Cloud APIs: Do not use external API calls for inference (e.g., OpenAI GPT-4o, Anthropic Claude). All model weights must be open-source and capable of running locally.
> Over-Parameterized Models: Any foundation model or ensemble where the total parameter count exceeds 500 Million.
> Legacy NLP Pipelines: Decoupled pipelines relying on basic OCR or Regex to format JSON. The solution must be an end-to-end generative Vision-Language Model capable of native structured output.
> Submission
> Submit a CSV file containing your model's predictions. The submission file must exactly match the following format and strictly adhere to these specific columns and data types:
> Column	Type	Description
> image_id	string	Row identifier corresponding to an image in test.csv
> answer	string	Your model's predicted JSON string
> Requirements:
> Must contain exactly 2,500 rows (excluding the header row).
> Must include the exact header row: image_id,answer
> The answer column must be a valid JSON string payload.
> Sample Format:
> image_id,answer
> 3f9a8b2c1d4e.jpg,"{""name"": ""triage_binary"", ""parameters"": {""finding_present"": true}}"
> 7c2b1a9f4e8d.jpg,"{""name"": ""flag_anomaly"", ""parameters"": {""reason"": ""unanswerable""}}"
> 9d8e7f6a5b4c.jpg,"{""name"": ""log_pathology"", ""parameters"": {""description"": ""endocrine""}}"
> What Not To Use

Inspiration note: Useful as a compact supervised adaptation pattern: small specialized data, constrained model behavior, and a measurable output format.

## Cross-Lingual Physics Reasoning Via LoRA Fine-Tuned LLMs
- Challenge URL: https://drive.google.com/drive/folders/1tc2u9WdSdIzO3CO7oYnlFRdObhOXpPQd
- Source file: cd.txt
- DOMAIN used for this document: Fine-Tuning (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / Fine-Tuning / Cross-Lingual Physics Reasoning Via LoRA Fine-Tuned LLMs

Full challenge description from Drive:

> Overview
> Models that solve physics problems often fail silently — they produce confident wrong answers with no signal of uncertainty. CaliPhys challenges participants to build a LoRA-tuned LLM that not only solves Chinese physics problems in English, but also knows when it doesn't know — outputting a calibrated confidence score alongside every prediction.
> This is not just a reasoning benchmark. It is a reliability benchmark: a model that scores 70% accuracy with well-calibrated confidence is more useful than one that scores 75% with overconfident errors.
> Task Definition
> Input: A physics problem written in Chinese (with LaTeX)
> Output (3 components):
> solution_pred — English step-by-step reasoning chain
> answer_pred — Final answer in \boxed{} format
> confidence — A scalar ∈ [0, 1] representing the model's self-assessed probability of being correct
> No external translation APIs, no pre-translation, no separate translation models. All three outputs must emerge from a single end-to-end LoRA-tuned model.
> Dataset
> Problems span five domains — Mechanics, Thermodynamics, Optics, Electromagnetism, and Modern Physics — across difficulty levels from high school to postgraduate. The dataset is curated from university-level physics curricula and covers both conceptual and computational problem types. Problems were filtered for clarity and solvability, LaTeX formatting was standardized, and answers were normalized into consistent \boxed{} format.
> FileDescriptionSamplestrain.csvChinese problems with English solutions and answers800test.csvChinese problems only200sample_submission.csvFormat reference200
> Train Schema
> ColumnTypeDescriptionidintUnique problem IDquestionstringChinese physics problem (LaTeX)solutionstringGround-truth English reasoninganswerstringFinal answer in \boxed{}answer_typestringNumerical, Expression, Equation, Multiple Choice
> Test Schema
> ColumnTypeDescriptionidintUnique problem IDquestionstringChinese physics problem (LaTeX)
> Submission Schema
> ColumnTypeDescriptionidintProblem IDsolution_predstringEnglish reasoning chainanswer_predstringFinal answer in \boxed{}confidencefloatSelf-assessed probability of correctness ∈ [0, 1]
> Method Constraints
> ✅ LoRA fine-tuning only (rank ≤ 16, target modules: q_proj, v_proj)
> ❌ Full fine-tuning not allowed
> ❌ External translation APIs or pre-translated datasets not allowed
> ❌ Ensemble methods to compute confidence are not allowed — confidence must be a single model's output token or decoded scalar
> The confidence value must be generated by the model itself — not computed post-hoc from logit aggregation over an ensemble.
> Scoring
> Final Score = 0.5 × Answer Score + 0.3 × Reasoning Score + 0.2 × Calibration Score
> Answer Score (50%)
> Answer TypeMethodMultiple ChoiceExact matchNumericalRelative error ≤ 2% → 1, else 0Expression / EquationSymPy symbolic equivalence
> Answer Score = mean(sample_scores)
> Reasoning Score (30%)
> Embedding model: paraphrase-multilingual-MiniLM-L12-v2 Metric: cosine similarity between solution_pred and ground-truth solution.
> Reasoning Score = mean(cosine_similarity(pred_i, true_i))
> Calibration Score (20%)
> Measured via Expected Calibration Error (ECE) with 10 equal-width bins over [0, 1], converted to a score:
> Calibration Score = 1 - ECE
> ECE is computed as:
> ECE = Σ (|B_m| / n) × |acc(B_m) − conf(B_m)|
> where:
> bins are defined by edges [0.0, 0.1, 0.2, ..., 1.0] (10 equal-width bins)
> B_m is the set of samples whose predicted confidence falls in bin m
> acc(B_m) is the mean answer score of samples in bin m
> conf(B_m) is the mean predicted confidence of samples in bin m
> n is the total number of samples
> empty bins contribute 0 to the sum
> A model that says "0.9 confident" and is right 90% of the time scores perfectly. A model that always outputs 1.0 is heavily penalized when wrong.
> Example Submission
> id,solution_pred,answer_pred,confidence
> 1,"Using Newton's second law, the net force equals mass times acceleration...","\boxed{9.8}",0.91
> 2,"From Gauss's law, the enclosed charge gives electric field...","\boxed{E=\frac{q}{4\pi\epsilon_0 r^2}}",0.74
> 3,"By conservation of energy, kinetic equals potential energy lost...","\boxed{B}",0.60

Inspiration note: Useful as a compact supervised adaptation pattern: small specialized data, constrained model behavior, and a measurable output format.

## Synthetic Corrupted Alignment Signal Recovery
- Challenge URL: https://drive.google.com/drive/folders/1YZyT7FNAOJn0Le92lrSgOOMX71aqgGpe
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: Fine-Tuning (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: From Google Drive challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 2 / inferred / Synthetic Corrupted Alignment Signal Recovery

Full challenge description from Drive:

> # Challenge creation form — fill-in
> ## Title
> ```
> Synthetic Corrupted Alignment Signal Recovery
> ```
> ## Problem Description
> # Synthetic Corrupted Alignment Signal Recovery
> ## Overview
> In reinforcement learning from human feedback (RLHF), reward model quality depends entirely on the integrity of annotator preference data. When annotation teams are heterogeneous — with inconsistent criteria, partial correlations between raters, and even adversarial contributors — the resulting training signal becomes a corrupted version of the true quality judgment.
> This challenge presents 60,000 synthetic instruction-response pairs that were independently rated by a hidden ensemble of 5 annotator personas. Three personas are legitimate but weigh quality dimensions differently. One is adversarial — it systematically inverts quality ratings for a subset of topic categories. One is a noisy blend of two other personas. Two personas share partial correlations in their rating functions, making clean disentanglement difficult.
> The task is to predict the **ground-truth quality tier** (0 through 4), defined as the consensus of the 3 legitimate personas only, for each test pair. The solver receives only the instruction text and response text — no numeric scores or annotator metadata are provided.
> Recovering the true quality signal requires analyzing the response text to assess latent quality dimensions (factual consistency, constraint adherence, format compliance, coherence), identifying which dimensions drive the legitimate consensus, and detecting patterns of adversarial contamination across topic categories.
> Approximately 15% of training tier labels are perturbed by ±1 tier (label noise), establishing an irreducible error floor. See the Evaluation section for organizer-measured reference scores that characterize difficulty (participants do not receive baseline code or baseline submissions).
> ## Evaluation
> Submissions are scored using **Macro F1** across 5 quality tiers (0-4).
> Higher is better. The following **reference Macro F1 scores** were measured by
> the organizers on the same train/test construction participants receive (they
> summarize difficulty only; no baseline code, weights, or precomputed
> submissions are distributed to participants):
> | Reference method (organizer evaluation only)              | Macro F1 |
> |----------------------------------------------------------|----------|
> | Constant prediction (single tier)                        | ≈ 0.07   |
> | Uniform-random                                           | ≈ 0.20   |
> | Stratified-random (sampled from train-label distribution) | ≈ 0.20   |
> | TF-IDF word 1-2 grams + multinomial logistic regression   | ≈ 0.37   |
> | Hand-engineered instruction×response interaction features + gradient boosting | ≈ 0.37 |
> The 15% per-example ±1-tier label-noise injection acts as a hard upper bound
> on achievable accuracy; the noise-limited ceiling is approximately 0.85 macro
> F1, but strong non-LLM bag-of-words and tabular-style pipelines plateau near
> the ≈0.37 row above. A solver that learns to read the response text (e.g.
> fine-tuned transformer or reward-model-style cross-encoder) is expected to
> substantially exceed that plateau.
> ## Dataset
> After preparation, the public directory contains:
> | File                   | Description                                                          |
> |------------------------|----------------------------------------------------------------------|
> | `train.csv`            | 45,000 labeled pairs with columns below                             |
> | `test.csv`             | 15,000 unlabeled pairs (same columns minus `quality_tier`)          |
> | `sample_submission.csv`| Example submission with all tiers set to 2                          |
> Training and test columns:
> | Column         | Type   | Description                                                   |
> |----------------|--------|---------------------------------------------------------------|
> | sample_id      | int    | Unique identifier                                             |
> | instruction    | str    | Instruction text specifying topic, format, length, constraint |
> | response       | str    | Response text with varying quality dimensions                 |
> | quality_tier   | int    | Ground-truth quality tier (0–4) — **training only**           |
> ## Submission
> Submit a CSV file with the following format:
> | Column       | Type | Description                              |
> |--------------|------|------------------------------------------|
> | sample_id    | int  | Identifier from the test set             |
> | quality_tier | int  | Predicted quality tier (0, 1, 2, 3, or 4)|
> **Requirements:**
> - Must contain exactly 15,000 rows (one per test sample)
> - Must include a header row
> - All `sample_id` values must be unique and match the test set
> - `quality_tier` values must be integers in {0, 1, 2, 3, 4}
> ## Rubrics
> ### Rubric 1
> - **Criteria:** Correctly loads the training CSV and parses the instruction and response text columns for downstream processing.
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Rationale:** The text fields are the sole source of signal for quality assessment; failing to load or parse them makes prediction impossible.
> ### Rubric 2
> - **Criteria:** Produces a valid submission CSV with columns `sample_id` and `quality_tier`, correct row count, unique IDs matching the test set, and integer tier values in {0, 1, 2, 3, 4}.
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Rationale:** Malformed submissions receive a score of 0.0 from the grader; structural correctness is a prerequisite for any evaluation.
> ### Rubric 3
> - **Criteria:** Achieves a Macro F1 strictly greater than **0.40** on the hidden test set.
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Rationale:** Organizer evaluation (see the Evaluation table) shows that a
> standard TF-IDF + multinomial logistic regression bag-of-words pipeline
> reaches macro F1 ≈ 0.37 on this split, and a stronger hand-engineered
> tabular-style pipeline reaches about the same. A `> 0.40` threshold places
> the pass bar *strictly above* that plateau (and roughly twice the random
> baseline of ~0.20), so clearing it demonstrates that the solver has exploited
> instruction-response signal beyond surface-level term statistics or random
> guessing. The 15% label-noise ceiling of ≈ 0.85 leaves substantial headroom
> above 0.40 for stronger methods (fine-tuned encoders, cross-encoder reward
> models) to differentiate themselves.
> ### Rubric 4
> - **Criteria:** Uses a language model or text feature extraction method (e.g., embeddings, TF-IDF, fine-tuned transformer) to derive features from the instruction and response text.
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Rationale:** The quality tier is determined by latent textual properties that require NLP-based feature extraction; surface-level heuristics alone cannot recover the hidden quality dimensions.
> ### Rubric 5
> - **Criteria:** Does not use test labels or test-set statistics during training or feature engineering.
> - **Type:** TRAINING
> - **Importance:** UNIVERSAL
> - **Rationale:** Using test information during training constitutes data leakage and produces unreliable performance estimates.
> ## Grading
> ```yaml
> grading:
> method: "program"
> script: "grade.py"
> metric: "macro_f1"
> direction: "maximize"
> min_score: 0.0
> max_score: 1.0
> ```
> ## Grading Script
> ```python
> """
> grade.py – Synthetic Corrupted Alignment Signal Recovery.
> Metric: Macro F1 across 5 quality tiers (0-4).
> Returns 0.0 for any structurally invalid submission.
> """
> import pandas as pd
> import numpy as np
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if "sample_id" not in submission.columns or "quality_tier" not in submission.columns:
> return 0.0
> if "sample_id" not in answers.columns or "quality_tier" not in answers.columns:
> return 0.0
> if submission["sample_id"].duplicated().any():
> return 0.0
> if answers["sample_id"].duplicated().any():
> return 0.0
> merged = answers.merge(submission, on="sample_id", how="left",
> suffixes=("_true", "_pred"))
> if len(merged) != len(answers):
> return 0.0
> if merged["quality_tier_pred"].isna().any():
> return 0.0
> y_true = merged["quality_tier_true"].astype(int).values
> y_pred = merged["quality_tier_pred"].astype(int).values
> classes = sorted(set(y_true))
> f1_scores = []
> for c in classes:
> tp = int(np.sum((y_pred == c) & (y_true == c)))
> fp = int(np.sum((y_pred == c) & (y_true != c)))
> fn = int(np.sum((y_pred != c) & (y_true == c)))
> precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
> recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
> if precision + recall > 0:
> f1_scores.append(2 * precision * recall / (precision + recall))
> else:
> f1_scores.append(0.0)
> return float(np.mean(f1_scores))
> except Exception:
> return 0.0
> ```
> ## Prepare Script
> ```python
> """
> prepare.py – Synthetic Corrupted Alignment Signal Recovery.
> Reads raw_data/data.csv.
> Produces:
> pub/  train.csv   (sample_id, instruction, response, quality_tier)
> test.csv    (sample_id, instruction, response)
> sample_submission.csv  (sample_id, quality_tier = 2)
> priv/ answers.csv (sample_id, quality_tier)
> """
> from pathlib import Path
> import pandas as pd
> def prepare(raw_dir="raw_data", public_dir="pub", private_dir="priv", seed=42):
> raw = Path(raw_dir)
> pub = Path(public_dir)
> priv = Path(private_dir)
> pub.mkdir(parents=True, exist_ok=True)
> priv.mkdir(parents=True, exist_ok=True)
> df = pd.read_csv(str(raw / "data.csv"))
> df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
> split = int(len(df) * 0.75)
> train_df = df.iloc[:split].copy()
> test_df = df.iloc[split:].copy()
> assert len(set(train_df["sample_id"]) & set(test_df["sample_id"])) == 0
> keep_train = ["sample_id", "instruction", "response", "quality_tier"]
> keep_test = ["sample_id", "instruction", "response"]
> train_df[keep_train].to_csv(str(pub / "train.csv"), index=False)
> test_df[keep_test].to_csv(str(pub / "test.csv"), index=False)
> test_df[["sample_id", "quality_tier"]].to_csv(str(priv / "answers.csv"), index=False)
> sub = test_df[["sample_id"]].copy()
> sub["quality_tier"] = 2
> sub.to_csv(str(pub / "sample_submission.csv"), index=False)
> print(f"Train: {len(train_df)}, Test: {len(test_df)}")
> print(f"pub/ and priv/ written.")
> if __name__ == "__main__":
> prepare()
> ```

Inspiration note: Useful as a compact supervised adaptation pattern: small specialized data, constrained model behavior, and a measurable output format.


## Molecular Signatures Of Bioactivity Reproducibility
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx798ej7949dtkt6g95rpq31gs89mk37
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-opened Shipd challenge page on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page / pasted challenge text:

> Domain: Fine-Tuning / cheminformatics — molecular sequence modeling. Each input is a short text: a molecule written as a SMILES string. You fine-tune a molecular sequence model (a SMILES transformer such as ChemBERTa) — or train one from scratch, or from molecular fingerprints to read the molecule and recover its reproducibility signature: how closely independent laboratories agree when they measure its bioactivity. The model learns directly from the SMILES tokens, exactly as a language model reads text, with a lightweight output head.
>
> Task
> The same compound–target affinity, measured by different laboratories, comes back different — sometimes in tight agreement, sometimes scattered across orders of magnitude. That scatter is not uniform across chemistry: particular molecular traits — aggregation, chemical reactivity, poor solubility, assay interference — make a compound systematically hard to measure, and that fragility is written into its structure. We call the resulting per-compound scatter its reproducibility signature: a quantity that says how much to trust a measured affinity, independent of what the affinity is.
>
> This benchmark asks a model to read that signature off the molecule itself. For each compound–target–endpoint, the affinity was measured at least eight times; the agreement among those repeats is the signature to recover. You are not asked for the affinity — you are asked how trustworthy it is: read the molecule (with the light context provided) and report its reproducibility signature.
>
> It is a structure-based cheminformatics task. It rewards learning the chemical hallmarks of hard-to-measure molecules and making them carry across to molecules the model has never seen. And it is intrinsically bounded: a large share of laboratory scatter is irreducible experimental noise that no molecule-level model can recover, so the achievable ceiling is hard and sits well below the top of the scale.
>
> What makes this its own problem. Public bioactivity scatter has been described before as a statistical phenomenon of heterogeneous data. Here it is instead a supervised, structure-driven benchmark that treats measurement reproducibility as an intrinsic, learnable property of a molecule — a facet of chemistry that affinity models are never asked to capture: a molecule in, its reproducibility signature out, scored on molecules it has never seen (the test compounds are absent from training — a compound-disjoint split), so it genuinely tests reproducibility read from chemistry rather than memorised per compound.
>
> Data
> All files are under ./dataset/public/.
>
> File	Contents
> train.csv	id, smiles, standard_type, n_range, mean_pact, disagreement — labeled training rows.
> test.csv	id, smiles, standard_type, n_range, mean_pact — the disagreement is withheld.
> sample_submission.csv	A correctly-formatted example (a flat constant; scores 0).
> Columns
>
> smiles (string) — the compound's canonical SMILES; the primary model input. The test compounds are absent from training (compound-disjoint split), so the model must generalize to new chemistry.
> standard_type (string) — the readout family: IC50, Ki, Kd, or EC50.
> n_range (string) — a coarse bucket of how many independent repeats the group has: 8-10, 11-20, or 21+ (light context).
> mean_pact (float) — the group's central potency on the p-scale 9 − log10(value in nM), deliberately noised and coarsely rounded (context only). The exact repeat count and exact mean are withheld so a row cannot be matched back to a specific source-database measurement group.
> disagreement (float, train only) — the reproducibility signature: the agreement among the group's repeats on the p-scale (their spread), a finite non-negative number. This is the quantity to recover.
> Submission
> Write ./working/submission.csv with exactly these two columns, in this order, one row per test id:
>
> id,disagreement  
>
> disagreement is your reported reproducibility signature (a finite, non-negative number). The grader rejects any submission with the wrong columns/order, a missing/extra/duplicate id, a non-finite entry, or a negative value.
>
> Evaluation
> The score (higher is better, Maximize, in [0, 1]) is Lin's concordance correlation coefficient (CCC) between your reported signature and the held-out truth, floored at 0:
>
> score = max( 0,  2·cov(y, ŷ) / ( var(y) + var(ŷ) + (mean(y) − mean(ŷ))² ) )  
>
> Concordance rewards both the ordering (which molecules are reproducible versus fragile to measure) and the calibration (matching the true centre and spread of the signature) — a model that merely ranks, or that is systematically off-scale, is penalised. A flat constant (including the training average) has zero variance and scores 0. Because the test compounds are unseen and much of the scatter is irreducible experimental noise, the achievable maximum is well below 1.
>
> What to use
> A standard cheminformatics setup: fine-tune a pretrained SMILES transformer (e.g. ChemBERTa) with a single output head, or train a graph neural network or a gradient-boosted model over molecular fingerprints — conditioning on the readout family and the light group context. Learning which structural motifs imply fragile measurements, and making that knowledge transfer to unfamiliar molecules, is the productive path.
>
> What not to use
> No internet at inference and no external bioactivity/uncertainty resources; train your model on the provided data (you may pip-install open-weight models and libraries at the start).
> No reverse lookup of the underlying individual measurements from external databases; work only from the provided molecule and context.
> No hardcoded per-id answers; submissions must come from your model.

Inspiration note: Useful as a fine-tuning benchmark pattern where a pretrained molecular sequence model reads SMILES plus light assay context and predicts a calibrated continuous reproducibility/uncertainty signature under a compound-disjoint split.


## MS/MS Stability Review Brief Generation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx735t3n5k48q4rhn8x00vcqan89qfvk
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is an LLM fine-tuning task over chemistry spectrum review text. Each example is an instruction-style packet describing one small-molecule MS/MS measurement: molecule string, precursor and mass hints, public quality hints, fragment-zone summaries, and a compact peak trace. The model must generate the lab's stability review brief in a fixed semicolon format.
> The brief is not a molecule name, candidate ranking, or database lookup result. It is a downstream review decision inferred from how spectra with similar evidence behave in the public training examples. A useful model should learn when the packet supports accepting the measurement, when low-mass cleanup is likely, when core or high-fragment evidence should be reviewed, and when repeat coverage is warranted.
> The intended solution is to train or fine-tune on the provided instruction/input/output examples. Feature engineering and smaller trained text models are allowed, but a fixed hand-written parser that ignores the public training outputs is not the target of the benchmark.
> Dataset
> File descriptions
> train.jsonl -- 649 instruction/input/output examples for sequence-model training or fine-tuning.
> test.jsonl -- 206 held-out instruction/input examples without outputs.
> train.csv -- CSV mirror of train.jsonl with instruction, input, prompt, and the generated review_brief output.
> test.csv -- CSV mirror of test.jsonl with instruction, input, and prompt, but without review_brief.
> sample_submission.csv -- A template showing the required id,review_brief submission format with random valid-looking generated briefs.
> Column descriptions
> id (string) -- Hashed identifier for the review case.
> instruction (string) -- Generation instruction telling a model to return only the stability review brief.
> input (string) -- Spectrum packet text containing the molecule string, measurement summary, fragment-zone intensity summary, peak trace, and generation request.
> prompt (string) -- Full prompt formed by concatenating instruction and input.
> review_brief (string) -- Train-only target and submission field. The generated brief must contain action, anchor, instability, and closure_cost assignments separated by semicolons.
> Evaluation
> Submissions are scored with intervention brief loss. Lower is better. The grader parses each generated review_brief and scores the four fields inside it. A perfect brief scores 0, and the worst valid per-row brief is bounded by 100.
> ZONES = ["low_frag", "core_frag", "mid_frag", "high_frag", "precursor_tail"]
> ACTION_GROUP = {
> "accept": "accept",
> "low_mass_cleanup": "cleanup",
> "core_fragment_review": "review",
> "high_fragment_review": "review",
> "coverage_repeat": "repeat",
> }
> def action_loss(predicted, actual):
> if predicted == actual:
> return 0.0
> if ACTION_GROUP[predicted] == ACTION_GROUP[actual]:
> return 45.0
> return 100.0
> def zone_loss(predicted, actual):
> return 100.0 * abs(ZONES.index(predicted) - ZONES.index(actual)) / (len(ZONES) - 1)
> def evaluate(predicted, actual):
> return (
> 0.35 * action_loss(predicted["action"], actual["action"])
> + 0.20 * zone_loss(predicted["anchor"], actual["anchor"])
> + 0.25 * zone_loss(predicted["instability"], actual["instability"])
> + 0.20 * abs(predicted["closure_cost"] - actual["closure_cost"])
> )
> The final score is the mean intervention brief loss across all test rows.
> Submission
> Submit a CSV file with one generated review brief for every row in test.jsonl or test.csv.
> id (string) -- The hashed identifier from the test file.
> review_brief (string) -- The generated stability brief in this exact assignment format: action=<label>;anchor=<zone>;instability=<zone>;closure_cost=<number>.
> Allowed action labels:
> accept
> low_mass_cleanup
> core_fragment_review
> high_fragment_review
> coverage_repeat
> Allowed anchor and instability zone labels:
> low_frag
> core_frag
> mid_frag
> high_frag
> precursor_tail
> Example:
> id,review_brief
> 009f4916ffe6,action=coverage_repeat;anchor=core_frag;instability=precursor_tail;closure_cost=74.25
> 03be083d9f8c,action=low_mass_cleanup;anchor=low_frag;instability=core_frag;closure_cost=48.60
> Requirements
> The file must contain exactly 206 rows plus the header.
> Every id from the test file must be present exactly once.
> review_brief must contain exactly four assignments: action, anchor, instability, and closure_cost.
> Assignments must be separated by semicolons and use key=value syntax.
> All labels must come from the allowed sets listed above.
> closure_cost must be finite and between 0 and 100 inclusive.
> File format: .csv only, with exact column names id,review_brief.
> What Not To Use
> Do not use web search, spectral-library search engines, or external copies of the spectra to recover held-out review briefs. The benchmark is meant to be solved from the supplied public instruction examples.
> Do not submit a hardcoded map from test IDs, full prompt strings, or memorized held-out outputs.
> Do not convert this into molecule lookup or candidate-retrieval against outside libraries. The target is the generated stability review brief, not molecular identity.
> Do not build the main solution as a fixed rule-only decoder that ignores the public review_brief training outputs. Diagnostic parsing and feature extraction are fine, but the submitted method should train or fine-tune on the public examples.

Inspiration note: Useful as a fine-tuning benchmark pattern where an instruction-style chemistry measurement packet is mapped to a fixed-format expert review brief, combining structured signals, text generation, and strict output formatting.

## Catalytic Candidate Selection
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76r4x2ssgntx9r2ptf086rrs89n86g
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is a cross-modal model fine-tuning challenge at the intersection of protein language modeling and biochemical reaction representation learning. The goal is to adapt an open-weight pretrained model to select the curated catalytic reaction of a protein from eight deliberately confusable reaction candidates.
> Each query contains one reviewed amino-acid sequence and eight reaction SMILES. Exactly one candidate is the Swiss-Prot-associated Rhea reaction for the focal protein. The other seven are not random reactions: all eight candidates belong to a symmetric biochemical neighborhood and share at least one moderately rare molecular component. No candidate is designated as the chemical “center” when the neighborhood is constructed, and the correct candidate position is randomized independently for every row.
> This construction removes the shortcuts available in ordinary reaction-matching tasks. There is no approved reference reaction to compare against, string equality cannot identify the target, and selecting the chemical medoid of the candidate set is not sufficient. A successful system must learn compatibility between protein sequence and reaction chemistry.
> Strong solutions should fine-tune a protein language model together with a reaction or molecular encoder, using a learned cross-modal scoring function. Parameter-efficient fine-tuning, such as LoRA or adapters, is allowed. Frozen embeddings may be used as auxiliary features, but the benchmark is designed so that independent global embeddings without a learned protein–reaction interaction are substantially weaker.
> Fine-Tuning Objective
> For each query, let the protein be P and the eight candidate reactions be R_0, ..., R_7. The model should learn a compatibility score:
> s_i = f_theta(P, R_i)
> and convert the eight scores into one probability distribution:
> p_i = softmax(s_0, ..., s_7)_i
> The released target, correct_candidate, identifies the correct option during training. Candidate positions have no global semantic meaning: candidate_3 is not a biochemical class, and its position is balanced and randomized.
> Suitable approaches include:
> joint fine-tuning of a protein encoder and a reaction encoder;
> a cross-encoder over serialized protein and reaction inputs;
> contrastive or listwise fine-tuning with in-query hard negatives;
> parameter-efficient adaptation of pretrained biological and chemical models;
> ensembles of independently fine-tuned cross-modal rankers.
> Zero-shot prompting is not the intended solution. The benchmark evaluates supervised parameter adaptation from the released examples.
> Generalization Design
> Closely related protein clusters cannot appear on both sides of the split.
> The private test set also contains two positive-reaction strata:
> seen_positive_reaction — the correct reaction was observed as a positive target in training, but only with proteins from disjoint UniRef50 clusters.
> unseen_positive_reaction — the correct reaction was never a positive target in training.
> There are 160 seen-positive and 320 unseen-positive hidden queries. The larger unseen stratum prevents exact reaction lookup from dominating the leaderboard and rewards transfer to new catalytic chemistry.
> Candidate sets are formed before focal proteins are selected. Every set contains eight distinct directed reactions sharing the same neighborhood-defining molecular component. This symmetric construction prevents a solver from identifying the answer solely because all negatives were sampled around it.
> Dataset
> The prepared dataset contains:
> public/
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> private/
> └── answers.csv
> train.csv: 3,200 labeled protein queries.
> test.csv: 480 unlabeled protein queries.
> Each of the eight target positions appears exactly 400 times in training and 60 times in test.
> ### `train.csv`
> Column	Type	Description
> id	string	Opaque 16-character query identifier.
> protein_sequence	string	Reviewed amino-acid sequence.
> candidate_reaction_0	string	Directed candidate reaction SMILES.
> candidate_reaction_1	string	Directed candidate reaction SMILES.
> candidate_reaction_2	string	Directed candidate reaction SMILES.
> candidate_reaction_3	string	Directed candidate reaction SMILES.
> candidate_reaction_4	string	Directed candidate reaction SMILES.
> candidate_reaction_5	string	Directed candidate reaction SMILES.
> candidate_reaction_6	string	Directed candidate reaction SMILES.
> candidate_reaction_7	string	Directed candidate reaction SMILES.
> correct_candidate	string	Fine-tuning target, from candidate_0 through candidate_7.
> ### `test.csv`
> `test.csv` contains the same input columns without `correct_candidate`.
> ### **Reaction representation**
> - `>>` separates the left and right sides of a reaction.
> - `.` separates disconnected molecular components on one side.
> - Component order is randomized and has no chemical meaning.
> - Reaction direction is meaningful.
> - Stereochemistry, charges, wildcard atoms, and explicit hydrogens are meaningful and should not be discarded blindly.
> - All eight reactions within a query are distinct after component-order normalization.
> Protein sequences range from 40 to 1,500 amino acids. Solvers should use an explicit long-sequence policy rather than silently dropping informative regions.
> ## **Evaluation**
> Submissions provide probabilities `p_0, ..., p_7` for the eight candidates. Four components are calculated.
> ### **1. Overall Mean Reciprocal Rank**
> For each query, let `rank_i` be the rank assigned to the correct candidate:
> MRR = mean(1 / rank_i)
> Tied candidates receive their shared average rank. For example, if all eight probabilities are equal, every candidate receives rank 4.5 rather than rank 1.
> ### **2. Tie-Aware Top-1 Accuracy**
> A unique correct maximum receives credit 1. If the correct candidate is tied with `m` candidates at the maximum probability, it receives credit `1/m`. Otherwise it receives 0.
> ### **3. Unseen-Positive MRR**
> `MRR_unseen` is Mean Reciprocal Rank on the private `unseen_positive_reaction` stratum only.
> ### **4. Normalized Multiclass Log-Loss**
> For multiclass log loss `L`:
> C = clip(1 - L / log(8), 0, 1)
> A uniform probability distribution gives `C = 0`; calibrated correct predictions approach `C = 1`.
> ### **Final score**
> Score = 0.35 × MRR
> 0.25 × Top1
> 0.30 × MRR_unseen
> 0.10 × C
> The score is bounded to `[0, 1]`, and **higher is better**. A perfect submission scores `1.0`. Uniform probabilities score approximately `0.176`.
> This metric rewards useful ranking across all eight hard candidates, gives substantial weight to exact top-choice quality, explicitly measures transfer to unseen positive reactions, and retains a calibration incentive.
> ## **Submission**
> Submit submission.csv with exactly these columns:
> Column	Type	Description
> id	string	Identifier copied from test.csv.
> p_candidate_0	float	Probability that candidate 0 is correct.
> p_candidate_1	float	Probability that candidate 1 is correct.
> p_candidate_2	float	Probability that candidate 2 is correct.
> p_candidate_3	float	Probability that candidate 3 is correct.
> p_candidate_4	float	Probability that candidate 4 is correct.
> p_candidate_5	float	Probability that candidate 5 is correct.
> p_candidate_6	float	Probability that candidate 6 is correct.
> p_candidate_7	float	Probability that candidate 7 is correct.
> Example:
> id,p_candidate_0,p_candidate_1,p_candidate_2,p_candidate_3,p_candidate_4,p_candidate_5,p_candidate_6,p_candidate_7 01a0b83d92f41c77,0.05,0.08,0.11,0.42,0.06,0.09,0.13,0.06 01ed529ca182e3d4,0.14,0.07,0.05,0.09,0.10,0.38,0.08,0.09
> ### **Requirements**
> - The file must contain exactly 480 rows.
> - Every `id` from `test.csv` must appear exactly once.
> - Column names must match the names above exactly.
> - All probabilities must be finite and lie in `[0, 1]`.
> - Each row must sum to 1 within an absolute tolerance of `0.001`.
> - CSV is the only accepted format.
> ## **Data-Use Rules**
> - Train or fine-tune the modeling pipeline on the released supervision.
> - Do not use zero-shot or few-shot prompting as the primary predictor.
> - Do not key predictions to `id`, CSV position, or candidate position priors.
> - Do not manually label hidden queries.
> &nbsp;

Inspiration note: Useful as a fine-tuning pattern where a pretrained scientific/sequence model adapts to structured chemistry or biology inputs and emits a calibrated score or decision.

## Molecular Photoluminescence Property Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bwkzwcs1dfq1916jzcy129189nrh2
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Given a molecule's SMILES structure, computed physicochemical descriptors, and measurement solvent, predict its photoluminescence quantum yield (PLQY) and spectral properties — absorption maximum, emission maximum, and Stokes shift. Photoluminescence quantum yield is the holy grail metric in fluorophore design: it tells you how efficiently a molecule converts absorbed light into emitted light. A QY near 1.0 means nearly every absorbed photon is re-emitted (ideal for OLEDs, bioimaging, single-molecule spectroscopy); a QY near 0 means the excited-state energy is lost as heat. Despite decades of photochemistry research, predicting QY from structure remains an unsolved problem — even expert chemists are routinely surprised.
> While public chromophore prediction models (e.g. Chemprop-based spectral predictors on Hugging Face, Joung et al. 2020 optical database) address similar inputs and targets, this challenge is not a repackaged version of that work. Four structural choices set it apart:
> Generalization, not interpolation. The split is by unique SMILES — no molecule appears in both train and test. Unlike standard random splits where the same chromophore in different solvents leaks across the boundary, models here must predict properties for entirely unseen molecules. Memorizing "BODIPY in toluene has QY 0.8" fails when that BODIPY only exists in the test set.
> Pretraining is mandatory. With ~9,500 training examples (~4,500 unique molecules, each measured in 1–5 solvents) across ~100 solvents and 6 scaffold families, training from scratch is impossible. The pretrained foundation model must supply chemical priors while finetuning teaches photophysical grammar (heavy atom quenching, energy gap law, solvatochromism) — a ground-state to excited-state transfer no existing benchmark tests.
> Physically-consistent evaluation. You submit three values (PLQY, absorption, emission); Stokes shift is derived automatically (stokes = emission − absorption) and contributes 10% of your score. This penalizes models that get individual wavelengths right but the spectral gap wrong. No existing chromophore benchmark enforces physical consistency in scoring.
> Raw solvent chemistry. The solvent column uses SMILES notation (~100 unique chemical structures: Cc1ccccc1, CC#N, C1CCOC1), not five categorical labels. A molecule's QY can vary 5–10× across solvents — models must learn genuine solvatochromic reasoning from molecular structure, not lookup tables.
> This is a finetuning challenge on molecular foundation models. You must start from a pretrained molecular model and adapt it to predict excited-state photophysical properties that the pretrained model has never seen.
> Why Finetuning?
> Molecular foundation models — MolFormer, ChemBERTa, MolCLR, GROVER, and others — have been pretrained on millions of molecules to learn general chemical representations. They understand functional groups, aromaticity, hydrogen bonding, and molecular geometry. But they know nothing about excited states.
> These models were pretrained almost exclusively on ground-state properties: formation energies, HOMO-LUMO gaps, equilibrium geometries from DFT, molecular fingerprints, and masked token reconstruction. The physics of excited states — multi-reference correlation, vibronic coupling, spin-orbit coupling, conical intersections, non-adiabatic dynamics — is fundamentally absent from their pretraining corpora.
> This challenge tests a critical capability: transfer learning from ground-state chemistry to excited-state photophysics. Can you take a model that understands what a BODIPY core looks like and teach it that the same core, with a bromine at position 2, will have its quantum yield drop from 0.9 to 0.1 due to the heavy atom effect? Can you finetune a model to internalize the energy gap law, solvatochromism, and the rigidity-QY correlation — physical rules it never encountered during pretraining?
> All existing chemistry ML benchmarks (QM9, QMugs, PCQM4Mv2, OC20/22) focus on ground-state properties. Excited-state property prediction, which governs all light-matter interactions, has zero representation in any major ML benchmark. This challenge fills that gap — not by providing more data, but by forcing models to learn the physics from limited examples.
> Data
> Files
> train.csv — Labeled molecules with all feature columns plus plqy, absorption_max_nm, emission_max_nm, and stokes_shift_nm (4 target columns for training). The first three must be predicted; stokes_shift_nm is provided as an auxiliary training signal but is computed automatically during grading — you do NOT submit it.
> test.csv — Feature columns only (no target columns — same schema as train.csv minus plqy, absorption_max_nm, emission_max_nm, stokes_shift_nm). Use this to generate predictions.
> sample_submission.csv — Submission template with 4 columns: mol_id + 3 prediction columns (plqy, absorption_max_nm, emission_max_nm). No stokes_shift_nm — it is derived automatically. Replace placeholder values with your predictions.
> Input Features
> Column	Type	Description
> mol_id	str	Unique molecule identifier
> smiles	str	SMILES string representing the molecular graph
> solvent	str	Measurement solvent in SMILES notation (~100 unique solvents, e.g. Cc1ccccc1 for toluene, CC#N for acetonitrile)
> num_rotatable_bonds	int	Number of rotatable bonds — structural flexibility proxy
> molecular_weight	float	Molecular weight (g/mol)
> logP	float	Octanol-water partition coefficient — lipophilicity
> num_heavy_atoms	int	Count of non-hydrogen atoms
> has_heavy_atom	int	Binary indicator for Br/I/Se/Te presence (heavy atom effect)
> Target Variables
> Column	Type	Range	Description
> plqy	float	[0, 1]	Photoluminescence quantum yield — submitted
> absorption_max_nm	float	[200, 800]	Wavelength of maximum absorption (nm) — submitted
> emission_max_nm	float	[300, 1000]	Wavelength of maximum emission (nm) — submitted
> stokes_shift_nm	float	[0, 300]	Stokes shift = emission_max − absorption_max (nm). Auxiliary only — computed internally during grading. Available in raw data for training but NOT submitted.
> Finetuning Data Strategy
> The training set contains ~9,500 labeled examples (~4,500 unique molecules, each measured in 1–5 solvents). This is deliberately small to simulate real-world experimental photophysics datasets. You cannot simply train a large model from scratch on this data — convergence would fail. The pretrained weights carry the chemical knowledge; your finetuning must teach the model photophysics.
> Consider: which layers to freeze, which to unfreeze, and at what learning rate. The pretrained model already knows SMILES tokenization, atom typing, and bond perception. Your job is to add a regression head and teach the encoder that bromine at position 2 of a BODIPY means low QY, while the same bromine on a rhodamine has a different effect entirely.
> Key Photophysical Rules
> Machine learning models that can internalize these rules should outperform those that treat the problem as black-box regression:
> Rigidity-QY correlation: Molecules with locked, planar geometries (few rotatable bonds) achieve higher QY because vibrational relaxation — the dominant non-radiative decay channel — is suppressed. BODIPY dyes owe their near-unity QY to their rigid dipyrromethene core.
> Heavy atom quenching: Br, I, Se, Te enhance spin-orbit coupling, promoting intersystem crossing (S1 → T1) at the expense of fluorescence (S1 → S0). This is the internal heavy atom effect — a bromine substitution can drop QY from 0.9 to 0.1.
> Conjugation length: Extending pi-conjugation reduces the HOMO-LUMO gap, red-shifting both absorption and emission. This is why cyanines can be tuned from visible to near-IR by adding vinylene units.
> Solvatochromism: Polar solvents stabilize the excited state dipole more than the ground state, reducing the emission energy and increasing the Stokes shift. Water shows the largest effect; toluene the smallest.
> Energy gap law: As the S1-T1 gap narrows (red-shifted emission), non-radiative decay accelerates exponentially, imposing a practical upper limit on near-IR fluorophore QY.
> Finetuning Strategy Guidance
> Effective finetuning for this challenge typically follows one of these patterns:
> Pattern A — Frozen Encoder + Trainable Head: Extract embeddings from a frozen pretrained model, concatenate with engineered descriptors (rotatable bonds, logP, heavy atom indicator, solvent), and train a lightweight prediction head (MLP, gradient boosting). Fastest to train; relies heavily on descriptor quality.
> Pattern B — Partial Unfreezing: Freeze early transformer/GNN layers (which capture generic atom/bond features) and unfreeze later layers + prediction head. The unfrozen layers learn photophysics-specific representations while preserving general chemistry knowledge from early layers.
> Pattern C — Full Finetuning with Low LR: Finetune all parameters with a learning rate 10-100x lower than pretraining. Highest risk of catastrophic forgetting but highest potential reward if regularization is sufficient.
> Pattern D — LoRA/QLoRA: Apply Low-Rank Adaptation to attention layers only. Parameter-efficient (trains <1% of parameters), preserves pretrained knowledge, and enables larger models on limited GPU memory.
> Multi-modal strategy: Combine a SMILES-based model (ChemBERTa/MolFormer) with a graph-based model (GROVER/MolCLR) — the SMILES model captures sequential chemical patterns while the GNN captures topological relationships between atoms and functional groups. If you generate 3D conformers locally with RDKit, you can add a geometry-aware model as a third modality.
> Evaluation
> Submissions are evaluated using a composite metric that balances quantum yield accuracy against spectral property precision. You submit only three columns (plqy, absorption_max_nm, emission_max_nm); the Stokes component is computed automatically from your predictions — no fourth column needed.
> Score = 0.4 × QY_Score + 0.25 × Abs_Score + 0.25 × Em_Score + 0.1 × Stokes_Score
> Component Definitions
> QY Score — R-squared-like metric clamped to [0, 1]:
> QY_Score = max(0, 1 - Σ(pred - true)² / Σ(true - mean(true))²)
> This is the standard R² (coefficient of determination), with negative values clamped to zero. It rewards models that capture the variance in quantum yield across the diverse chemical space.
> Absorption Score — MAE-based with 50 nm tolerance:
> Abs_Score = 1 / (1 + MAE_abs / 50)
> where MAE_abs = mean(|pred_abs - true_abs|). The 50 nm reference makes this metric lenient enough for the inherent uncertainty in computed excitation energies while still distinguishing good models from poor ones.
> Emission Score — Same form as absorption:
> Em_Score = 1 / (1 + MAE_em / 50)
> Stokes Score — MAE-based with 25 nm tolerance. Stokes shift is computed internally from your predicted absorption and emission (stokes_pred = emission_pred − absorption_pred). You do NOT submit it directly. This component rewards physically consistent spectral predictions where the gap between absorption and emission matches the true Stokes shift:
> Stokes_Score = 1 / (1 + MAE_stokes / 25)
> where MAE_stokes = mean(|stokes_pred − stokes_true|) and stokes_pred is derived from your submitted absorption and emission predictions.
> Score Range
> Final scores range from 0 to 1, where 1.0 represents perfect prediction of all three submitted properties (QY, absorption, emission) plus perfect spectral consistency (Stokes — derived automatically from your absorption and emission predictions).
> Note on finetuning advantage: Pretrained models are expected to substantially outperform from-scratch models on this task. A randomly initialized GNN/transformer trained on this dataset alone lacks the chemical priors needed to generalize across scaffold families. The pretrained weights provide the chemical vocabulary; finetuning teaches photophysical grammar. Models trained from scratch on this data alone typically score <0.3; well-finetuned pretrained models should exceed 0.6.
> Submission Format
> Submit a CSV file with three prediction columns (no Stokes shift — it is derived automatically):
> mol_id,plqy,absorption_max_nm,emission_max_nm
> mol_00001,0.7823,452.1,523.8
> mol_00002,0.1500,638.5,691.2
> mol_00003,0.4500,512.3,589.4
> mol_00004,0.9100,345.7,412.1
> mol_00005,0.2300,567.8,645.3
> Requirements:
> mol_id must match test.csv exactly (all rows, sorted by mol_id, no extras, no duplicates)
> All three numeric columns must be present and non-null
> plqy must be in [0, 1]
> absorption_max_nm must be in [200, 800]
> emission_max_nm must be in [300, 1000]
> Standard CSV formatting (no spaces around commas)
> Stokes shift is NOT submitted — it is computed from your predictions during grading
> Rules
> Allowed
> Pretrained Models — Starting Point:
> Any open-source pretrained molecular model with publicly downloadable weights. This includes but is not limited to: MolFormer, ChemBERTa, ChemBERTa-2, MolCLR, GROVER, Uni-Mol, SchNet, DimeNet++, Equiformer, TorchMD-Net, GraphMVP, MolR, GEM, ChemGPT, MoLFormer-XL, GIN, AttentiveFP, and any other molecular model with public pretrained weights on HuggingFace, GitHub, or Zenodo.
> You MUST disclose which pretrained model(s) you used and where the weights were downloaded from.
> You MAY use multiple pretrained models in ensemble (up to 5 models total).
> Finetuning Methods:
> Full finetuning (all parameters trainable)
> Partial finetuning (freeze some layers, unfreeze others)
> LoRA (Low-Rank Adaptation) and QLoRA (Quantized LoRA)
> Prefix tuning, prompt tuning, adapter layers
> Frozen encoder + trainable prediction head (linear probe, MLP head, gradient boosting on embeddings)
> Any combination of the above
> Training Data:
> ONLY the provided training set (train.csv). No external photophysical data.
> Cross-validation on the training set is allowed and encouraged.
> Standard data augmentation from the provided data (SMILES enumeration, conformer sampling, molecular graph augmentation).
> Feature Engineering:
> Feature extraction from SMILES using RDKit, Open Babel, or other open-source cheminformatics toolkits.
> Molecular fingerprints (ECFP, MACCS, Avalon, RDKit descriptors) may be concatenated with pretrained embeddings.
> 3D conformer generation from SMILES using RDKit (distance matrices, angle features, Coulomb matrices) — allowed but must be done locally; XYZ coordinates are not provided.
> Solvent encoding (one-hot, learned embeddings, or physicochemical solvent descriptors from SMILES strings).
> Ensembles:
> Ensemble of up to 5 independently trained/finetuned models.
> Models may differ in: pretrained base model, finetuning strategy, random seed, cross-validation fold, learning rate schedule.
> Checkpoint averaging (SWA) within a single training run counts as one model.
> Not Allowed
> Model Restrictions:
> Training from scratch without pretrained weights: This is a finetuning challenge. Randomly initialized models are not permitted. You must start from a pretrained checkpoint.
> Closed-source LLM APIs: GPT-4, Claude, Gemini, or any proprietary model accessed via API.
> Closed-source or proprietary molecular models: Models whose weights are not publicly downloadable.
> Models pretrained on photophysical data: The pretrained model must not have seen PLQY, emission spectra, or excited-state properties during its pretraining.
> External Data:
> No external photochemistry databases: Do not scrape additional PLQY, absorption, or emission data from the literature or from databases.
> No quantum chemistry software at inference time: Gaussian, ORCA, Q-Chem, Turbomole, or any DFT/TD-DFT calculation.
> No commercial chemistry databases: Reaxys, SciFinder, or any paid database.
> Internet access during inference is not allowed (downloading pretrained weights beforehand is permitted).
> Methods:
> Hand-coded rules: No manual mapping of specific scaffolds to properties. The test set is designed to defeat this.
> Human annotation: No manual correction of test predictions.
> Test-time adaptation: No using test set statistics or pseudo-labeling on test data.
> Reverse engineering: Do not attempt to reverse-engineer the data generation process.

Inspiration note: Useful as a fine-tuning pattern where a pretrained scientific/sequence model adapts to structured chemistry or biology inputs and emits a calibrated score or decision.

## Budgeted Time-Cutoff Continued Pretraining on NLP Abstracts
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74ab2ab7nvx5wcwejg5jmvmn89ph3g
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative, small-data
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Adapt a small language model under a strict pre-cutoff corpus budget, then generate research-paper titles for post-cutoff NLP abstract sketches.
> The setting simulates a research lab or search platform that wants to keep a small language model current in a fast-moving scientific domain without retraining on every available document. Solvers receive a timestamped corpus of pre-cutoff NLP and computational-linguistics abstracts. They must choose useful documents under a limited estimated-token budget, adapt a model, and then generate titles for later post-cutoff abstract sketches.
> The public data contains:
> pretrain_corpus.parquet — a timestamped pre-cutoff scientific abstract corpus
> public_dev.csv — public post-cutoff examples with target titles for format calibration
> test.csv — private-evaluation prompts without target titles
> sample_submission.csv — a submission-format example
> README.md — decoding and usage guidance
> dataset_card.json — schema, split information, and token budget
> prepare_report_public.json — public preparation summary
> The corpus window is earlier than the private evaluation window. This temporal split is intended to test whether corpus selection and language-model adaptation help on later scientific writing, rather than testing memorization of public development answers.
> This is a time-cutoff language-model adaptation task. It is not a classification task, not a scalar regression task, and not a computer-vision task.
> Real-World Motivation
> Scientific fields change quickly. New methods, datasets, acronyms, and evaluation settings appear every month. A small model that was trained on older text may not generate domain-appropriate titles for newer abstracts unless it is adapted to recent literature.
> In practical continued-pretraining workflows, teams often cannot use every available document. They must select a subset of useful domain text under a compute or token budget. This challenge evaluates that budgeted adaptation workflow using a clean, timestamped public corpus and a hidden post-cutoff generation set.
> The private prompts are deliberately lossy keyword sketches rather than verbatim abstracts. This reduces the value of direct source lookup and puts more emphasis on learning scientific title style, terminology, and topic framing from the public corpus.
> Why This Is Not Ordinary Title Generation
> The central challenge is the adaptation setup:
> solvers receive a larger pre-cutoff candidate corpus than the recommended training budget
> each corpus row includes an estimated token count for budgeted document selection
> the private prompts come from a later post-cutoff window
> private test prompts are lossy keyword sketches, not verbatim abstracts
> source identifiers, source URLs, author names, exact post-cutoff abstracts, and target titles are hidden from public test files
> Strong solutions should learn domain terminology, title style, and research phrasing from the public corpus while selecting useful pretraining data under the budget.
> Public Files
> The prepared public dataset contains:
> File	Type	Description
> pretrain_corpus.parquet	Parquet	Pre-cutoff corpus documents for continued pretraining, fine-tuning, retrieval, corpus filtering, or data-selection experiments.
> public_dev.csv	CSV	Public post-cutoff development examples with prompts and target titles.
> test.csv	CSV	Private-evaluation prompts without target titles.
> sample_submission.csv	CSV	Example submission with the required columns.
> README.md	Markdown	Short decoding and usage guidance.
> dataset_card.json	JSON	Schema, split information, task metadata, and token-budget information.
> prepare_report_public.json	JSON	Public preparation summary.
> Pretraining Corpus
> pretrain_corpus.parquet contains one row per pre-cutoff document.
> Column	Type	Description
> doc_id	string	Public anonymized corpus document ID.
> published_date	string	Publication date in YYYY-MM-DD format.
> primary_category	string	Primary subject category for the document.
> categories	string	Semicolon-separated category list.
> title	string	Paper title from the pre-cutoff corpus. This is available only for corpus documents, not private test examples.
> abstract	string	Paper abstract from the pre-cutoff corpus.
> pretrain_text	string	Canonical text block recommended for continued pretraining or adaptation. It combines title, category, date, and abstract information in a consistent format.
> token_count_estimate	int	Approximate tokenizer-free token count estimate for budget accounting.
> The corpus is pre-cutoff relative to the private evaluation pool. Solvers may use this corpus for continued pretraining, supervised adaptation, retrieval indexing, data selection, or other public-data-only adaptation strategies.
> Public Development Data
> public_dev.csv contains public post-cutoff examples for format calibration and local validation.
> Column	Type	Description
> id	string	Public development example ID.
> prompt	string	Title-generation prompt built from metadata and a lossy abstract keyword sketch.
> target_title	string	Expected title for the public development example.
> published_month	string	Publication month in YYYY-MM format.
> primary_category	string	Primary subject category.
> abstract_token_count_estimate	int	Approximate token count of the source abstract.
> The public development set is provided so solvers can verify format, tune decoding, and run local validation. It is not the main pretraining corpus.
> Test Data
> test.csv contains one row per private-evaluation example.
> Column	Type	Description
> id	string	Private test example ID.
> prompt	string	Title-generation prompt built from metadata and a lossy abstract keyword sketch.
> published_month	string	Publication month in YYYY-MM format.
> primary_category	string	Primary subject category.
> abstract_token_count_estimate	int	Approximate token count of the source abstract.
> The public test file does not include:
> target_title
> exact post-cutoff abstracts
> source document identifiers
> source URLs
> author names
> private split metadata
> Sample Submission
> sample_submission.csv demonstrates the required submission structure.
> Column	Type	Description
> id	string	Test ID from test.csv.
> generated_title	string	Generated title for the prompt.
> The sample submission is generated without using private target titles.
> Auxiliary Files
> dataset_card.json contains public metadata about the prepared challenge files.
> Field	Type	Description
> title	string	Challenge dataset title.
> prepare_version	string	Version identifier for the preparation script.
> task	string	Short description of the task.
> metric	string	Public description of the scoring metric.
> train_corpus_rows	int	Number of rows in pretrain_corpus.parquet.
> public_dev_rows	int	Number of rows in public_dev.csv.
> test_rows	int	Number of rows in test.csv.
> estimated_unique_token_budget	int	Recommended estimated-token budget for corpus selection and adaptation.
> submission_columns	list of strings	Required submission columns.
> sample_submission_policy	string	Statement that the sample submission is not tuned on private answers.
> prompt_privacy_policy	string	Statement describing the lossy-sketch prompt policy.
> private_source_identifiers_removed_from_public_test	bool	Whether source identifiers were removed from public test data.
> prepare_report_public.json contains a public preparation summary.
> Field	Type	Description
> prepare_version	string	Version identifier for the preparation script.
> train_corpus_rows	int	Number of rows in the pretraining corpus.
> public_dev_rows	int	Number of public development examples.
> test_rows	int	Number of private-evaluation prompts.
> estimated_unique_token_budget	int	Recommended estimated-token budget.
> answers_columns_exact	bool	Whether the hidden answer file uses the expected answer schema.
> public_test_uses_lossy_prompts	bool	Whether public test prompts use lossy keyword sketches instead of verbatim abstracts.
> README.md provides a short human-readable summary of the task, files, token-budget policy, and submission format.
> Target
> For every row in test.csv, predict:
> generated_title
> The generated title should be concise and should match the hidden target title as closely as possible. Return only the title text. Do not include explanations, quotation marks, bullet points, JSON, or extra commentary.
> Submission Format
> Submit a CSV or Parquet file containing exactly these columns:
> Column	Type	Description
> id	string	Test ID from test.csv.
> generated_title	string	Generated title for the prompt.
> Example:
> id,generated_title
> test_01ab23cd45ef,Efficient Retrieval-Augmented Adaptation for Scientific Language Models
> test_09fe87dc65ba,Robust Multimodal Alignment Under Distribution Shift
> The submission must contain every test ID exactly once and no additional IDs. Missing IDs, extra IDs, duplicate IDs, unexpected columns, blank IDs, and generated titles longer than 500 characters are rejected.
> Evaluation
> Submissions are evaluated using mean normalized title-generation similarity.
> For each example, the grader compares the submitted title with the hidden target title using:
> ExampleScore = 0.75 * TokenF1 + 0.25 * CharacterSimilarity
> The final score is:
> Score = mean(ExampleScore across private examples)
> Scores range from 0.0 to 1.0.
> Higher is better.
> Text Normalization
> Before computing both metric components, the submitted title and target title are normalized as follows:
> Apply Unicode NFKC normalization.
> Convert all text to lowercase.
> Replace & with the word and.
> Replace every character that is not an ASCII letter or digit with a space.
> Collapse repeated whitespace to a single space.
> Strip leading and trailing whitespace.
> For example:
> "Retrieval-Augmented Learning & Evaluation!"
> normalizes to:
> retrieval augmented learning and evaluation
> TokenF1
> After normalization, tokens are extracted with this pattern:
> [a-z0-9]+
> Stopwords are not removed. Stemming is not applied. Duplicate tokens count.
> Let:
> pred_tokens be the normalized token list from the submitted title
> true_tokens be the normalized token list from the hidden target title
> overlap be the multiset overlap count between the two token lists
> Then:
> precision = overlap / len(pred_tokens)
> recall = overlap / len(true_tokens)
> TokenF1 = 2 * precision * recall / (precision + recall)
> If one side has no tokens and the other side has tokens, TokenF1 = 0.0. If both sides have no tokens, TokenF1 = 1.0, though private target titles are expected to be non-empty.
> CharacterSimilarity
> CharacterSimilarity is computed on the normalized title strings using Python-style sequence matching, equivalent to:
> difflib.SequenceMatcher(None, normalized_prediction, normalized_target).ratio()
> This is an edit-similarity-style ratio between 0.0 and 1.0. It rewards close wording and minor formatting similarity even when token overlap is imperfect.
> If one normalized string is empty and the other is non-empty, CharacterSimilarity = 0.0. If both are empty, CharacterSimilarity = 1.0.
> Example Interpretation
> A submission that uses the correct major technical terms but not the exact wording can receive partial credit through TokenF1. A submission with close word order and similar phrasing can receive additional credit through CharacterSimilarity.
> A blank generated title receives 0.0 for that example.
> A perfect normalized title match receives 1.0.
> Budget Rule
> The intended continued-pretraining budget is listed in dataset_card.json as:
> estimated_unique_token_budget
> Solvers should select and use no more than this estimated token budget from pretrain_corpus.parquet for continued pretraining, supervised adaptation, retrieval indexing, or other corpus-based adaptation.
> The budget is computed using the provided token_count_estimate values. The point is not to train on every available document. The point is to choose useful pretraining data under a limited budget and then generalize to post-cutoff prompts.
> Split Design
> The pretraining corpus is pre-cutoff. The public development and private test examples are post-cutoff.
> Private test prompts use lossy keyword sketches rather than verbatim post-cutoff abstracts. Public files do not expose source document identifiers, source URLs, author names, exact post-cutoff abstracts, target titles, or private split metadata.
> This design reduces direct source lookup and makes the task focus on language-model adaptation and scientific title generation rather than retrieval of public paper metadata.
> Restrictions
> Use only the prepared public challenge files.
> Do not query online paper databases, search engines, APIs, source repositories, or external corpora during solving.
> Do not use source document identifiers, hidden URLs, author names, private files, or external lookup to recover private test titles.
> Do not hard-code predictions for specific IDs.
> Do not use leaderboard probing to infer private titles.
> Do not use post-cutoff external corpora outside the prepared public challenge files.
> Allowed approaches include:
> continued pretraining of a small open language model on selected public corpus documents
> supervised fine-tuning on public development examples
> instruction tuning or LoRA-style adaptation
> retrieval over the provided public pretraining corpus
> tokenizer or data-selection experiments using only public corpus text
> decoding and postprocessing based only on public data
> Participants may use any supervised or self-supervised language-model adaptation method that follows these restrictions and relies only on the prepared public challenge files.

Inspiration note: Useful as a fine-tuning pattern with specialized domain text, constrained outputs, and a metric-friendly target.

## Protein Engineering Solubility Contrast
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79vt002c3rn54hm9adz99ynh89n0ak
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Protein engineering workflows often compare candidate sequences that look similar under coarse amino-acid composition but behave differently in expression or purification. The practical question is not only whether a single protein is soluble; it is whether a model can choose the more soluble member of a near-match pair when length and global composition are deliberately controlled.
> In this challenge, each row contains two protein primary sequences, sequence_a and sequence_b. Exactly one member of the pair comes from the soluble class and the other comes from the insoluble class. Your task is to predict a_soluble_probability, the probability that sequence_a is the soluble member of the pair.
> The pairs are matched by length and amino-acid composition, so a solution based only on length, hydrophobic fraction, or class priors should perform poorly. A useful model should learn sequence-local motifs, distributed amino-acid context, or compact sequence embeddings that separate soluble proteins from compositionally similar decoys. This mirrors a real protein-screening workflow where an operator must prioritize between plausible constructs after coarse biochemical filters have already narrowed the list.
> Dataset
> File descriptions
> train.csv -- 5,000 labeled protein contrast pairs. Each row contains two protein sequences, pair metadata, and the target a_is_more_soluble.
> test.csv -- 1,200 hidden protein contrast pairs with the same input columns as train.csv, excluding a_is_more_soluble.
> sample_submission.csv -- A template showing the required submission format with random probability predictions.
> train.jsonl -- JSONL mirror of the training rows for sequence-model and fine-tuning workflows.
> test.jsonl -- JSONL mirror of the test rows without labels.
> Column descriptions
> id (string) -- Unique salted identifier for one protein pair.
> sequence_a (string) -- Protein primary sequence for the first candidate.
> sequence_b (string) -- Protein primary sequence for the second candidate.
> len_a (integer) -- Amino-acid length of sequence_a.
> len_b (integer) -- Amino-acid length of sequence_b.
> length_delta (integer) -- Absolute length difference between the two sequences.
> composition_distance (float) -- Distance between coarse amino-acid composition feature vectors used during pair matching.
> a_is_more_soluble (integer) -- Target in train.csv only. A value of 1 means sequence_a is the soluble member; 0 means sequence_b is the soluble member.
> Evaluation
> Submissions are scored using weighted root Brier loss on a 0 to 100 scale. Lower is better.
> def evaluate(y_true, y_pred, contrast_weight):
> y_pred = clip(y_pred, 0.0, 1.0)
> weighted_mse = weighted_mean((y_pred - y_true) ** 2, weights=contrast_weight)
> return 100.0 * sqrt(weighted_mse)
> The hidden contrast_weight is larger for tighter sequence pairs, so confident errors on the hardest near-matches are penalized more than errors on looser pairs. A perfect submission scores 0.0. Constant 0.5 predictions score about 50.0.
> Submission
> Submit a CSV file with one probability prediction for every row in test.csv.
> id (string) -- The protein pair identifier from test.csv.
> a_soluble_probability (float) -- Probability from 0.0 to 1.0 that sequence_a is the soluble member of the pair.
> Example:
> id,a_soluble_probability
> psc_8b2663457dfb,0.61
> psc_7ba6859fae12,0.28
> psc_9b900840f4fb,0.44
> Requirements
> The file must contain exactly 1,200 rows plus the header.
> Every id from test.csv must be present exactly once.
> a_soluble_probability must be finite, numeric, and between 0.0 and 1.0.
> File format: .csv only, with exact column names id,a_soluble_probability.
> What Not To Use
> Do not use external protein-solubility tables, sequence-search services, or cached answer tables to recover hidden pair labels. The task is to learn from the public training pairs.
> Do not reverse-search the full protein sequences to find their original solubility annotations or split membership.
> Do not hard-code predictions from row order, salted ids, sequence orientation frequency, or repeated public examples.
> Do not use cached answers or previously published train/test splits that overlap with these exact protein sequences.

Inspiration note: Useful as a fine-tuning pattern where a pretrained scientific/sequence model adapts to structured chemistry or biology inputs and emits a calibrated score or decision.

## Thermal Reaction-Channel Repertoires From Molecular Structure
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72yaqacrcd6jez4jc44wr97589rg1c
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Task
> A single molecule, when energised, can rearrange or fragment along many competing elementary-reaction channels — breaking and forming different bonds, each over its own activation-energy barrier. Only the low-barrier channels are kinetically accessible. Which ones those are is written into the molecule's structure — bond strengths, ring strain, and the stabilisation of each transition state — but the substrate does not trivially fix them: strain and electronic effects shift individual barriers, so structurally similar molecules can have different accessible repertoires.
> Your task: read the reactant SMILES and predict the set of reaction templates that are kinetically accessible for it — its thermal branching repertoire (a reactivity-repertoire prediction, not a barrier regression on a known reaction). A reaction template abstracts a channel to the bonds it breaks and forms (by element and bond order), e.g. BREAK{C-H(1),C-C(1)}FORM{C-C(2),H-H(1)}. A channel counts as accessible if its DFT activation barrier is within 10 kcal/mol of the molecule's lowest barrier.
> How this differs from prior work. Public models built on this quantum-chemistry data predict the activation barrier of a single, already-specified reactant→product pair — a regression on a transformation that is handed to the model. Automated reaction-network engines instead enumerate a molecule's channels by running expensive transition-state searches. Neither predicts, from the reactant structure alone, which elementary transformations will be thermally accessible. This task is exactly that missing step: it recasts per-pair barrier regression and per-molecule quantum-chemistry search as a single learned, multi-label read of the molecule — a structure → accessible-reaction-channel repertoire problem that no released model performs.
> This rewards learning the physical-organic logic of barrier ordering and transferring it to molecules unlike any in training. It is intrinsically bounded: the reactant alone does not determine which competing channels fall inside the energy window, so the map from structure to accessible-set is one-to-many and exact recovery is impossible — the achievable score has a hard ceiling well below 1.
> Why it is hard and not a lookup. Predicting accessibility from the globally most common templates scores only ~0.21, and a heuristic that flags every template whose bonds are merely present in the reactant reaches only ~0.20 — having a bond does not make breaking it low-barrier. The physics (which transformations are actually favourable) is the learnable signal. Test molecules come from held-out Murcko scaffolds (no training molecule shares the ring system), so the answer cannot be copied from a near-identical reactant.
> Data
> All files are under ./dataset/public/.
> File	Contents
> train.csv	id, reactant, templates — labeled training molecules.
> test.csv	id, reactant — the templates are withheld.
> template_vocabulary.csv	the set of reaction-template strings seen in training (your label space).
> sample_submission.csv	A correctly-formatted example (the most common template; scores ~0.05).
> Columns
> reactant (string) — the molecule as a SMILES (single closed-shell C/H/N/O species); the model input.
> templates (string, train only) — the target: ;-separated reaction-template strings, each of the form BREAK{...}FORM{...} where ... is a comma-separated list of Element-Element(order) bond descriptors (e.g. BREAK{C-O(1)}FORM{C-H(1),H-O(1)}). Every template is listed in template_vocabulary.csv.
> Submission
> Write ./working/submission.csv with exactly these two columns, in this order, one row per test id:
> id,templates
> templates is your predicted ;-separated set of template strings, each drawn from template_vocabulary.csv. The grader rejects a submission with the wrong columns/order, or a missing/extra/duplicate id.
> Evaluation
> The score (higher is better, Maximize, in [0, 1]) is the mean template set-F1: for each molecule, 2·|predicted ∩ true| / (|predicted| + |true|), averaged over the held-out molecules. Recovering the whole accessible repertoire matters — over-predicting is penalised (precision) and missing accessible channels is penalised (recall). A single-template constant scores ~0.05; because branching is underdetermined by the reactant and the test molecules are unfamiliar, the achievable maximum is well below 1.
> What to use
> Fine-tune a pretrained molecular language model (e.g. ChemBERTa, MolFormer) with a multi-label template head, or train a graph neural network / SMILES transformer from scratch. Learning which structural features lower a transition-state barrier — and making that transfer to unfamiliar scaffolds — is the productive path. (A frozen ECFP fingerprint already beats the frequency and bond-presence baselines, so the signal is real.)
> What not to use
> No internet at inference and no external reaction/quantum-chemistry databases or QM engines; train your model on the provided data (you may pip-install open-weight models and libraries at the start).
> No hardcoded per-id answers; predictions must come from your model.

Inspiration note: Useful as a fine-tuning benchmark pattern where molecular structure is mapped to reaction-channel labels or probabilities, stressing chemistry-aware representation learning and calibrated multi-output prediction.

## Quantum Chemistry Calibration Code Completion
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70tcw0dvy9dx8b3f60mrsrf989q5m6
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is a chemistry text-model fine-tuning challenge over reaction-route text. Each row is a compact route calibration note containing a coarse route sketch, low-cost profile indices, and perturbed profile estimates derived from an underlying atom-mapped route. The task is to complete one three-part calibration code for the route.
> The practical setting is high-throughput reaction triage. Chemists often screen many mapped routes with inexpensive quantum summaries, then reserve slower higher-fidelity calculations for cases where the cheap profile may misstate the barrier, the thermodynamics, or both. The target code summarizes that hidden correction behavior in a compact format that a trained model can learn from public examples.
> The held-out test routes use element-signature families that are absent from the training split. A frequency prior or a few hand-written cutoffs is not enough; useful submissions need to learn how route-size bins, heteroatom complexity, motif complexity, and low-cost profile estimates relate to calibration behavior.
> Dataset
> File descriptions
> train.csv -- Public labeled chemistry prompts with id, route_prompt, and the target calibration_code.
> train.jsonl -- Same public training examples in prompt/completion format for supervised fine-tuning workflows.
> test.csv -- Held-out chemistry prompts with id and route_prompt, but without the target.
> test.jsonl -- Same held-out examples in prompt-only JSON Lines format.
> sample_submission.csv -- Submission template with random valid calibration codes.
> split_metadata.json -- Public row counts, token sets, metric weights, and split summary.
> Column descriptions
> id (string) -- Unique hashed route identifier.
> route_prompt (string) -- Multi-line chemistry prompt containing coarse route sketch bins, low-cost profile indices, perturbed profile estimates, and the requested output format.
> calibration_code (string) -- Target completion in train.csv only. The required format is barrier-token|thermo-token|alert-token.
> JSONL field descriptions
> train.jsonl.id (string) -- Same hashed route identifier as train.csv.
> train.jsonl.prompt (string) -- Text prompt containing the route calibration note.
> train.jsonl.completion (string) -- Correct three-part calibration code.
> test.jsonl.id (string) -- Same hashed route identifier as test.csv.
> test.jsonl.prompt (string) -- Text prompt containing the route calibration note. No completion is included.
> Evaluation
> Submissions are scored with Safety-Balanced Quantum Calibration Code Loss. Lower is better.
> Each submitted code must contain exactly three pipe-separated tokens:
> Barrier token: barrier-lower, barrier-aligned, barrier-raised, or barrier-surged.
> Thermo token: thermo-more-favorable, thermo-aligned, thermo-less-favorable, or thermo-shifted.
> Alert token: no-alert, barrier-alert, thermo-alert, or both-alert.
> For each row:
> barrier_match is 1 when the submitted barrier token matches the hidden barrier token, otherwise 0.
> thermo_match is 1 when the submitted thermo token matches the hidden thermo token, otherwise 0.
> alert_match is 1 when the submitted alert token matches the hidden alert token, otherwise 0.
> row_score = 0.40 barrier_match + 0.35 thermo_match + 0.25 * alert_match.
> The row-level quality is mean(row_score).
> The metric also measures balanced recall for each component so that rare calibration states matter:
> barrier_balanced_recall is the mean recall over the four barrier tokens present in the hidden answers.
> thermo_balanced_recall is the mean recall over the four thermo tokens present in the hidden answers.
> alert_balanced_recall is the mean recall over the four alert tokens present in the hidden answers.
> balanced_component_score = 0.35 barrier_balanced_recall + 0.30 thermo_balanced_recall + 0.35 * alert_balanced_recall.
> The final loss is:
> row_level_quality = mean(row_score)
> final_quality = 0.70  *row_level_quality + 0.30*  balanced_component_score
> safety_balanced_quantum_calibration_code_loss = 100 * (1 - final_quality)
> Submission
> Submit a CSV file with one calibration code for every row in test.csv.
> id (string) -- The exact identifier from test.csv.
> calibration_code (string) -- Predicted code in the exact format barrier-token|thermo-token|alert-token.
> Example:
> id,calibration_code
> QCC-001456697909,barrier-aligned|thermo-more-favorable|barrier-alert
> QCC-004B5DC13EBA,barrier-lower|thermo-less-favorable|barrier-alert
> QCC-005BECB4EC39,barrier-surged|thermo-more-favorable|barrier-alert
> Requirements
> The file must contain exactly one row for every row in test.csv.
> Every id from test.csv must be present exactly once.
> File format must be .csv with exact columns id,calibration_code.
> Every calibration_code must contain exactly three valid tokens separated by |.
> Predictions must be produced by a local open-source text model fine-tuned on the public route prompts.
> Allowed Methods
> Fine-tune a local open-source text or sequence model on train.jsonl or an equivalent prompt/completion view built from train.csv.
> Use parameter-efficient fine-tuning, full fine-tuning, adapter tuning, or a trained neural text head on top of a local open-source text encoder.
> Use chemistry-aware prompt formatting, tokenization, validation splits, and error analysis to improve the fine-tuned model.
> Use grouped validation or held-out element-pattern validation to estimate behavior on unfamiliar route families.
> What Not To Use
> Do not reverse-map hashed route ids, coarse route bins, or perturbed profile estimates against outside datasets.
> Do not use outside reaction databases, cached quantum-calculation tables, or web-search lookups to recover hidden calibration codes for the held-out routes.
> Do not use cached answer maps or manual lookup tables for held-out reactions.
> Do not solve primarily with fixed code-frequency priors, exact string lookup, hand-written threshold rules, gradient-boosted trees, linear classifiers, TF-IDF-only classifiers, or other feature-table models. A fine-tuned local text model must provide the main predictive signal.

Inspiration note: Useful because it frames adaptation behavior around a concrete code/text completion target that can be scored on held-out examples.

## Real Meeting Turn-Completion And Response Timing From Speech
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c48mkdr9p98qg34v7f881ms89skf1
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio, multimodal
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given short 16 kHz mono WAV clips from real multi-party meetings. Each public clip is an opaque de-identified excerpt that ends at or near a candidate current-speaker boundary and is paired with a redacted token-shape window, token timings inside the clip, and coarse anonymized speaker context.
> For every test row, predict the turn-taking state at the boundary, the timing of the next speech event, the next-speaker relation, and an honest confidence value. The target is a practical endpointing and response-timing task for speech/NLP systems, not a transcript parser.
> What not to use: hosted commercial speech or language APIs, external labeled meeting corpora, source lookup of public meeting annotation files or test meeting identities, transcript-only rule shortcuts, filename/timestamp/meeting-id reconstruction, row-order tricks, and hardcoded answer maps are prohibited. The intended route is to train or fine-tune an open speech, audio-text, or multimodal model on the provided training examples.
> Task Specification
> The allowed turn_state values are COMPLETE, CONTINUE, BACKCHANNEL, OVERLAP, and UNCERTAIN. COMPLETE means the current speaker yields the floor and another speaker takes a substantive next turn. CONTINUE means the same speaker resumes after the boundary before another substantive turn. BACKCHANNEL means another speaker gives a short acknowledgement while the current speaker keeps or quickly regains the floor. OVERLAP means another speaker starts during or nearly on top of current speech in a competing way. UNCERTAIN is used only for rows where the annotation/timing region does not support a clear near-term event.
> next_response_ms is an integer in [0, 3000] measuring the clipped time from the candidate boundary to the next speech event or continuation. next_speaker_relation is one of SAME, OTHER, MULTI, or NONE_OR_UNCLEAR. confidence is a float in [0, 1] that should reflect how likely the row-level prediction is to be correct.
> Dataset
> The public dataset contains train.csv, test.csv, sample_submission.csv, and WAV clips under train/audio/ and test/audio/. train.csv has the input columns id, audio_path, transcript_window, token_timing_json, and speaker_context_json, plus the train-only label columns turn_state, next_response_ms, next_speaker_relation, and confidence. test.csv has only the input columns id, audio_path, transcript_window, token_timing_json, and speaker_context_json. sample_submission.csv is a dummy format file with the required columns id, turn_state, next_response_ms, next_speaker_relation, and confidence.
> Public Files
> Item	Description
> train.csv	labeled training rows
> test.csv	hidden-label test rows
> sample_submission.csv	dummy format file
> train/audio/	train WAV clips
> test/audio/	test WAV clips
> The audio paths in the CSVs are relative to the public/ directory. Training rows include labels; test rows include only public inputs.
> train.csv Columns
> Column	Type	Description
> id	int	opaque row id
> audio_path	string	relative WAV path
> transcript_window	string	token-shape window
> token_timing_json	JSON string	redacted token times
> speaker_context_json	JSON string	coarse context
> turn_state	string	target class
> next_response_ms	int	target latency
> next_speaker_relation	string	target relation
> confidence	float	gold confidence
> The transcript window is redacted to coarse token-shape values rather than verbatim words. The JSON timing field carries token indices, token-shape values, and relative timing, not raw lexical tokens. The JSON context uses anonymized local descriptors and does not expose meeting ids, original speaker ids, timestamps, annotation ids, future events, or source filenames.
> test.csv Columns
> Column	Type	Description
> id	int	opaque row id
> audio_path	string	relative WAV path
> transcript_window	string	token-shape window
> token_timing_json	JSON string	redacted token times
> speaker_context_json	JSON string	coarse context
> The test file has the same public input fields as the training file and withholds all targets.
> Submission Format
> Column	Type	Constraint
> id	int	exact test id
> turn_state	string	allowed class
> next_response_ms	int	0 to 3000
> next_speaker_relation	string	allowed relation
> confidence	float	0 to 1
> Submit exactly one row for every test id, with the columns in the exact order shown above.
> id,turn_state,next_response_ms,next_speaker_relation,confidence
> 102341,COMPLETE,420,OTHER,0.74
> 487221,CONTINUE,610,SAME,0.68
> 750812,BACKCHANNEL,120,OTHER,0.57
> Evaluation
> Invalid submissions score 0.0. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from test.csv; invalid categorical values; non-integer or out-of-range next_response_ms; and non-finite or out-of-range confidence.
> For valid submissions, the grader computes row heads for state correctness, next-speaker relation correctness, timing similarity, calibration, and joint exactness. Timing similarity is max(0, 1 - abs(pred_ms - true_ms) / tolerance), with tolerance determined by the true latency band. Calibration is max(0, 1 - abs(confidence - row_correctness)), where row correctness blends state, relation, and timing evidence.
> For any group of rows, GroupScore = 0.45 * mean(state_correct)^2 + 0.20 * mean(relation_correct)^2 + 0.20 * mean(timing_similarity)^2 + 0.10 * mean(calibration)^2 + 0.05 * mean(joint_exact)^2.
> The final score is 0.70 * GroupScore(all rows) + 0.15 * worst GroupScore by hidden meeting family + 0.15 * worst GroupScore by hidden turn type. The theoretical minimum is 0.0; the theoretical maximum is 1.0; higher is better.
> Intended Solution
> Strong solutions should train or fine-tune open-weight speech or audio-text models such as wav2vec2/HuBERT-style encoders, Whisper-family encoders, conformer encoders, or multimodal speech-text models, with optional text encoders over the transcript and token timing fields. Prompt-only or transcript-only approaches are not expected to handle pauses, energy decay, overlap, acknowledgement timing, and speaker dynamics reliably.
> Enforcement On Invalid Approaches
> Submissions based on hosted commercial APIs, external labeled meeting datasets, direct source lookup, manually recovered public-source test annotations, hardcoded id-to-answer maps, or rule-only parsing of the redacted text fields may be rejected before payout even if the CSV is structurally valid. The competition rewards learned speech/NLP modeling from the provided public training set.

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific input/output structure.

## Score-Margin Regression from Narrated Vietnamese Ô Ăn Quan Match Transcripts
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78q34baphf74b7xwqh4sqae989jh2f
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview:
> Ô ăn quan is a traditional Vietnamese two-player board game of the mancala family. In this challenge you are given a natural-language Vietnamese commentary transcript of a complete match between two players, A and B, and must predict the final score margin of that match: player A total points minus player B total points. A positive margin means A finished ahead; a negative margin means B finished ahead.
> Each transcript narrates the match move by move in Vietnamese: who played, roughly where they sowed, and crucially which captures occurred. Captures are the scoring events. Capturing a mandarin (quan) is worth 10 points and is always narrated as an an quan event; capturing one or more citizen cells (dân) is narrated as eating mot o, lien hoan may o, and similar phrases. The transcript never states any numeric score, and it never states how many stones a captured cell held, so those magnitudes are latent. The transcript also omits or summarises stretches with no captures, occasionally drops a capture event, varies the wording, and inserts flavour commentary, so the match cannot be reconstructed exactly. Your model must read the Vietnamese text, attribute capture events to the correct player, weigh mandarins against citizen cells, and estimate the net margin under uncertainty about the hidden magnitudes.
> This is a text regression task. The native use of a game move log is to replay the game; here the task is transformed into inferring a numeric outcome from imperfect natural-language commentary in a low-resource language, which requires per-actor event extraction and quantitative reasoning rather than simple keyword counting.
> Evaluation:
> Submissions are scored by the coefficient of determination (R squared) between the predicted score margins and the true score margins over the test matches. With y_true the true margin, y_pred the prediction, and mean(y_true) the mean true margin over the test set, the metric is R squared = 1 - (sum over test matches of (y_true - y_pred) squared) / (sum over test matches of (y_true - mean(y_true)) squared). Higher is better. A model that predicts every true margin exactly scores 1.0; a model that always predicts the mean scores about 0.0; worse-than-mean predictions score below 0.0. Because the stone counts behind each capture are hidden from the transcript, even a perfect reading of every narrated event cannot reach 1.0: the task has a built-in information ceiling.
> Dataset:
> The data is fully synthetic. Each match was produced by a deterministic Ô ăn quan rules engine driven by a greedy-plus-exploration policy over 6 to 12 rounds; every round re-stocks the board with a randomized, unstated number of stones per cell, so the exact capture magnitudes behind the commentary are latent. From 6000 generated matches, prepare.py renders one Vietnamese commentary transcript per match and builds a 75/25 train and test split. The prepared files live in the public directory.
> Files provided to solvers (in the public directory):
> public/train.csv - 4500 training matches with their transcripts and true score margins.
> public/test.csv - 1500 test matches with transcripts only (no margin).
> public/sample_submission.csv - a correctly formatted submission with every prediction set to the training-set mean margin (a constant baseline that scores R squared about 0).
> Hidden file (NOT distributed to solvers; listed only so the file set is complete):
> private/answers.csv - the ground-truth test margins used by the grader; never provided to solvers.
> Dataset statistics:
> score_margin is an integer, approximately symmetric around zero: mean about 0, standard deviation about 73, with the central 80 percent of matches falling roughly between -95 and +91 and extremes near -245 and +258.
> transcript is one line of Vietnamese free text per match, averaging about 2660 characters (roughly 480 words) and reflecting matches of about 49 narrated moves; individual transcripts range from a few hundred to several thousand characters.
> The transcript never states any numeric score or exact stone count, so even a perfect reading of the narrated events leaves irreducible uncertainty about the final margin (the built-in information ceiling noted under Evaluation).
> train.csv has one row per training match. Its columns are:
> id - string - match identifier, for example game_00001.
> transcript - string - the Vietnamese commentary of the whole match, as one line of free text.
> score_margin - integer - the ground-truth final margin, player A points minus player B points.
> test.csv has one row per test match. Its columns are:
> id - string - match identifier, for example game_04875.
> transcript - string - the Vietnamese commentary of the whole match.
> sample_submission.csv has one row per test match. Its columns are:
> id - string - the test match identifier, matching test.csv.
> prediction - float - placeholder predicted score margin, a finite real number, set to the training-set mean margin in every row of the sample.
> Submission:
> Submit a CSV file with exactly these two columns and a header row.
> id - string - the test match identifier taken from test.csv or sample_submission.csv.
> prediction - float - the predicted final score margin (A minus B), a finite real number; it may be positive, negative, or zero, and need not be a whole number even though the true margins are integers.
> The file public/sample_submission.csv is already in exactly this format, with the correct header and id column and every prediction set to the training-set mean margin (a constant baseline that scores R squared about 0); a valid submission keeps the id column unchanged and replaces each placeholder value with your predicted margin. Below is an excerpt of a correctly formatted submission file, showing the header row followed by three data rows (your file must contain all 1500 test rows in this same layout):
> id,prediction
> game_00007,-12.5
> game_00013,40.0
> game_00021,3.2
> Requirements:
> The file must contain exactly 1500 data rows (one per test match), plus the header row.
> The id values must match the test set exactly: the same set of ids, with no duplicates and no missing or extra rows.
> Predictions must be finite real numbers (no blanks, no inf, no NaN).
> Rules:
> The only valid input signal for predictions is the text content of each match transcript, and predictions must come from a model that represents the token sequence. The following approaches are not allowed:
> Hardcoding predictions for specific test ids.
> TF-IDF, bag-of-words, hashing-count, or plain n-gram-count feature vectors fed to a regressor. Sparse term-frequency representations are prohibited as the prediction mechanism; predictions must come from a model that reads the token sequence, for example learned token or character embeddings, a convolutional or recurrent encoder over the text, or a fine-tuned transformer.
> Predicting from how often each player is merely named (mention frequency) without distinguishing scoring events from non-scoring mentions. The transcript deliberately names players in non-scoring contexts (whiffed moves, borrows, flavour remarks), so raw mention counts are an unintended and unreliable shortcut.
> Predicting from how many turns or moves each player took (per-player move or turn counts, or the number of sentences attributed to each side) as a proxy for the outcome. The number of turns a side takes does not determine the margin: the margin depends on the hidden stone magnitudes captured, and the per-round starting stocks are randomized so that turn counts carry no reliable signal. Turn-count is an unintended structural feature, not the intended path.
> Using the id strings, the row order, the transcript length, or any ordering of the test file as a prediction signal instead of the transcript content.
> Reverse-engineering or reusing the synthetic generator random seed, move policy, or any hidden field to reconstruct the exact stone counts or the exact margin; only information present in the transcript text may be used.
> Treating the dataset as solvable by exact game replay: the transcript deliberately hides per-capture stone counts, gives only vague cell references, summarises no-capture stretches, and occasionally drops a capture, so exact reconstruction is infeasible and is not the intended path.
> Using private, role-gated, or API-key-based models, or calling any external inference API during inference.
> Using non-reproducible external weights or artifacts not publicly available.
> This challenge tests whether a model can read Vietnamese game commentary, attribute each capture event to the correct player (A versus B) by reading the capture verb and its subject rather than counting names, weight mandarin captures (worth ten times a citizen stone) appropriately, and aggregate them into a signed numeric margin under uncertainty about the hidden magnitudes. A solution that scores well by ignoring the language and exploiting ids, ordering, length, mention frequency, or generator internals is not valid regardless of its score.
> Pretrained model policy:
> Fine-tuning a publicly available pretrained language model (for example a multilingual transformer such as XLM-RoBERTa, or a Vietnamese model such as PhoBERT) is allowed and is the intended class of solution, provided the fine-tuning genuinely uses the provided training transcripts and their margins. Training a sequence model from scratch on the training transcripts (a character or token CNN, an RNN, or a small transformer that learns embeddings over the text) is equally valid. Sparse term-frequency methods (TF-IDF and bag-of-words) are not permitted, as stated in the rules above, because they reduce the commentary to surface counts instead of modelling the language. Because the score margin depends on stone counts that the transcript hides, no model can solve this challenge from text alone with near-perfect accuracy; even a perfect reading of every narrated event is bounded well below 1.0, so if a model appears to exceed that information ceiling it is exploiting an unintended artifact. Real learning here means parsing per-player capture and mandarin events from the Vietnamese commentary, separating them from non-scoring mentions, and mapping them to a calibrated score margin.

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific input/output structure.

## Covariation-Constrained RNA Alignment Repair
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bhfw5350gcnr1bw8r4a8zk589rp4g
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> RNA families preserve more than individual nucleotide frequencies. Paired positions can change together over evolution—an A-U pair may become G-C or G-U—while remaining structurally compatible. A substitution can therefore look plausible in either alignment column by itself yet violate the joint evolutionary grammar of the family.
> This challenge asks you to pretrain or adapt a local biological sequence model to detect and repair that kind of drift. Every example contains twelve aligned natural RNA homolog windows and a corrupted counterfactual pseudo-homolog. The counterfactual clean target is generated in a structure-preserving way and is not an exact sequence copied from Rfam. Its corrupted version contains one, two, or three additional substitutions. Your model must:
> assign an edit probability to every alignment position; and
> predict a calibrated A/C/G/U distribution for every position.
> The hidden clean sequence and exact edit positions are used only for grading. Corruptions include single-sided base-pair breaks, two-sided pair breaks whose individual nucleotides remain marginally plausible, conserved unpaired-motif drift, and mixed paired/unpaired drift.
> This is an LLM pretraining challenge for biological sequences. The intended solution is an RNA language model, MSA-aware transformer, axial-attention model, denoising model, or another learned sequence representation trained on the released clean/corrupted supervision. The task is not RNA-family classification and does not ask you to output a secondary structure.
> Conventional masked-language modeling marks the missing positions for the model. Here, no mask is supplied at test time: the model must localize subtle errors before reconstructing them.
> Conventional RNA-folding benchmarks predict base-pair contacts for one sequence. Here, the output is a calibrated repair distribution conditioned on an alignment of homologs, and the hidden split contains entirely unseen Rfam families and clans.
> Dataset
> Prepared files:
> dataset/public/
> |-- train.csv
> |-- test.csv
> `-- sample_submission.csv
> train.csv: 8,292 labeled repair examples from 474 Rfam families.
> test.csv: 3,852 hidden examples from 217 different Rfam families.
> sample_submission.csv: valid constant/uniform probabilities in the required 321-column format.
> Public input columns
> | Column | Type | Description |
> |---|---|---|
> | `example_id` | string | Opaque 16-character example identifier. |
> | `context_alignment` | string | Twelve aligned 64-character RNA sequences separated by `|`. |
> | `corrupted_sequence` | string | The 64-character sequence to inspect and repair. |
> Characters are:
> A, C, G, U for canonical RNA bases;
> - for an alignment gap; and
> | only as the separator between context sequences.
> The twelve context sequences are natural homologs from the Rfam family used to generate the counterfactual target. Their row order has no biological meaning.
> ### **Training-only target columns**
> Column	Type	Description
> clean_sequence	string	Pair-aware counterfactual sequence before controlled corruption.
> edit_positions_json	JSON list	Zero-based positions changed by corruption.
> edit_count	int	Number of changed positions: 1, 2, or 3.
> ### **Leakage-resistant split**
> Every Rfam family belongs wholly to one split. When Rfam assigns several related families to the same clan, the complete clan is also kept in one split.
> The prepared data therefore has:
> - zero Rfam-family overlap;
> - zero Rfam-clan leakage-group overlap;
> - 474 training families;
> - 217 hidden families; and
> - 177 independent hidden clan/family leakage groups.
> The test set measures transfer of denoising behavior to unseen RNA families, not memorization of family-specific consensus profiles.
> ## **Counterfactual Clean Targets**
> Natural held-out Rfam sequences are not used directly as clean prediction targets. Before applying the benchmark corruption, preparation constructs a counterfactual pseudo-homolog for every training and test example:
> - short unpaired fragments are copied from the twelve released homologs;
> - consensus-paired positions are changed jointly, using observed canonical pair states whenever sufficient family variation exists;
> - highly conserved windows may use another canonical pair state as a structure-preserving fallback;
> - benchmark edit positions and their paired partners are excluded from this background synthesis; and
> - the same construction is applied to training and test rows.
> Every generated clean target must differ from every natural Rfam sequence at the corresponding family and window coordinates by at least eight positions. Only after this gate passes is the controlled repair corruption applied.
> The release audit searched 24,611,452 overlapping 64-column windows from both the original and gap-filtered Rfam 15.1 seed alignments. It found:
> - zero exact matches among all 3,852 hidden clean targets;
> - zero exact matches among the 960 scored double-pair targets;
> - minimum same-family source distance of eight positions; and
> - zero rows where nearest-source differences exactly recovered the private edit positions.
> Observed context states were sufficient without fallback for 11,882 of 12,144 examples. Canonical-pair fallback was used in 262 examples overall and only 27 of the 960 scored examples.
> Rfam therefore supplies real family variation and structural constraints, but does not contain the hidden clean answers.
> ## **Controlled Corruptions**
> After counterfactual synthesis, the examples use four deterministic corruption mechanisms:
> ### **Single pair break**
> One side of a well-supported, covarying canonical pair is changed. The new base is chosen to break canonical pairing while remaining observed in that alignment column when possible.
> ### **Double pair break**
> Both sides of a covarying pair are changed. The replacement nucleotides are selected from column marginals when possible, but their joint state is noncanonical. Independent column models can therefore be misled.
> ### **Motif drift**
> Three conserved, non-paired positions are changed to lower-frequency alternatives. This tests family-profile and local sequence modeling.
> ### **Mixed drift**
> One side of a covarying pair and one conserved non-paired position are changed in the same sequence.
> These are controlled benchmark perturbations. They are not claimed to be observed sequencing errors.
> ## **Submission**
> Write `./working/submission.csv` with one row for every test `example_id`.
> The exact column order is:
> columns = ["example_id"] columns += [f"p_edit_{i}" for i in range(64)] columns += [ f"p_{base}_{i}" for i in range(64) for base in ["A", "C", "G", "U"] ]
> This produces 321 columns.
> ### **Edit-site probabilities**
> `p_edit_0` through `p_edit_63` are independent probabilities that the corresponding position was changed. Each must lie in `[0, 1]`. They do not need to sum to one.
> ### **Base probabilities**
> For every position `i`, provide:
> p_A_i, p_C_i, p_G_i, p_U_i
> These four values must lie in `[0, 1]` and sum to `1` for that position. Base probabilities are required even at visible gap positions, although gaps are not hidden repair targets.
> Requirements:
> - exactly 3,852 rows;
> - every test `example_id` appears exactly once;
> - exactly the 321 required columns and no extras;
> - all probabilities are finite and in `[0, 1]`;
> - each A/C/G/U group sums to `1` within absolute tolerance `0.001`; and
> - CSV format with a header row.
> ## **Evaluation**
> Submissions are scored with the **Hard Covariation Repair Score (HCRS)**. Higher is better.
> Only hidden `double_pair_break` examples contribute to HCRS. These are cases where both sides of a covarying pair were changed to individually plausible but jointly noncanonical bases. The scored subset contains:
> - 960 hidden examples;
> - 216 unseen Rfam families; and
> - 176 independent family/clan leakage groups.
> The hard-stratum flag is private. Predictions remain required for every test row because solvers are not told which rows belong to the scored subset. Other corruption mechanisms remain useful auxiliary pretraining supervision.
> All logarithms are natural logarithms.
> ### **1. Hard-stratum edit-site average-precision skill**
> Average precision is computed over canonical-base positions in hidden double-pair examples using the binary edit mask and `p_edit_i`.
> Let `prevalence` be the fraction of evaluated canonical positions that were edited:
> site_skill = clip((average_precision - prevalence) / (1 - prevalence), 0, 1)
> This chance-corrects the severe class imbalance. A constant edit probability scores zero, while perfect localization scores one.
> ### **2. Hard-stratum edited-base log skill**
> Only truly edited positions in hidden double-pair examples contribute. For each edited position, take the submitted probability assigned to its original clean base:
> base_ce = mean(-log(probability assigned to the clean base)) base_skill = clip(1 - base_ce / log(4), 0, 1)
> Uniform A/C/G/U probabilities score zero; perfect calibrated reconstruction scores one.
> ### **3. Hard-stratum paired repair skill**
> Use the highest-probability base at both edited members of every scored pair:
> exact = 1 if both edited paired positions are repaired correctly, else 0 chance = 0.25 ** 2 row_pair_skill = (exact - chance) / (1 - chance)
> The paired component is the mean `row_pair_skill`, clipped to `[0, 1]`.
> ### **Final score**
> HCRS = 0.65 * site_skill
> 0.05 * base_skill
> 0.30 * pair_skill
> HCRS lies in `[0, 1]`. A perfect submission scores `1.0`.
> Localization receives the largest weight because identifying two marginally plausible but jointly incompatible columns is the central difficulty. Independent base reconstruction has deliberately low weight so a frequency-profile model cannot dominate the benchmark.
> ## **Modeling Guidance**
> Strong solutions may:
> - pretrain a masked or corrupted-token RNA language model on `train.csv`;
> - encode the twelve homologs with axial, row/column, or permutation-invariant MSA attention;
> - initialize from an offline RNA model and continue pretraining on this repair objective;
> - combine sequence logits with family-profile and nearest-homolog features;
> - model paired-site dependencies rather than multiplying independent column frequencies;
> - use separate calibrated heads for edit localization and clean-base reconstruction; and
> - preserve the symmetry of context-row ordering through pooling or controlled row permutation.
> Validation must split by family or clan-like groups. A random row split leaks family-specific profiles and produces a misleading estimate.
> ## **What Not To Use**
> - Do not key predictions to `example_id`, CSV row order, or memorized source records.
> - Do not manually repair test examples.
> - Do not use zero-shot or few-shot prompting as the main predictor. The task is intended to evaluate local biological sequence pretraining or adaptation on the released supervision.
> &nbsp;

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific input/output structure.

## Ops-Log Causal-Chain Reconstruction From Raw Incident Telemetry
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79p0jmv55qq8qf3e3v9p0vzx89me2v
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> When a distributed service degrades, on-call SREs have to read raw logs from many services and reconstruct what actually happened: which event caused which downstream symptom, which observed event was the root cause, and which events merely occurred at the same time. This challenge turns that incident-review workflow into a structured NLP benchmark over synthetic but realistic server telemetry.
> Each row is one incident. You receive raw log text, a JSON list of observed events, a noisy fleet hint, and an instruction. The service names, template ids, and log phrases are private to this corpus. Timestamps are coarse and affected by asynchronous logging, so sorting events by time is not enough.
> For each test incident, submit a directed causal edge list, a root cause id or UNKNOWN, a list of genuinely concurrent event pairs, and a confidence. The intended solution is to fine-tune or train a permitted open-weight code/log language model or sequence-to-sequence model on the public training examples, such as Qwen Coder, StarCoder, CodeLlama, Phi, Gemma, Mistral, Llama, T5-style encoder-decoder models, or a domain text encoder with structured decoding.
> What Not To Use (any of these can cause solution rejection regardless of leaderboard score):
> Hosted commercial LLM APIs or closed model APIs for prediction, distillation, or pseudo-labeling.
> Source recovery, generator introspection, private-file access, or reverse-engineering hidden raw metadata.
> Filename, public id, row order, log-file order, event-count, or timestamp-only shortcuts.
> Hand-coded topology extraction from generator internals or exact lookup tables.
> Direct nearest-neighbor copying of train answers into test incidents.
> Metadata-only submissions that ignore the incident log text and event stream.
> Keyword-only, regex-only, or timestamp-sorting causal chains as a substitute for learned log reasoning.
> External labeled incident datasets, private SRE corpora, or web lookups for answers.
> Enforcement on invalid approaches: solutions that do not solve the intended log-understanding task may be rejected before payout. The goal is to reward learned incident-language reasoning and structured causal reconstruction, not score-chasing through public ids, metadata, row order, timestamps, or handcrafted shortcuts.
> Evaluation
> For each row, the grader parses the submitted JSON strings and computes four task heads plus calibration. A malformed or over-long JSON cell scores zero for that affected head on that row without crashing the grader; structural submission errors score 0.0 for the whole file.
> edge_f1        = directed F1 on exact [parent, child] event-id pairs
> root_score     = 1 if root_cause_id exactly matches, else 0
> concurrent_f1  = unordered-pair F1 on concurrent event pairs
> order_score    = F1 on transitive topological ordering implied by predicted edges
> head_score     = 0.52*edge_f1 + 0.22*root_score + 0.16*concurrent_f1 + 0.08*order_score
> calibration    = 1 - abs(confidence - head_score / 0.98)
> row_score      = head_score + 0.02*calibration
> The final score blends mean performance with hidden robustness terms:
> Final = 0.70 * mean(row_score)
> + 0.12 * lowest subgroup mean over hidden topology shapes
> + 0.10 * lowest subgroup mean over hidden ambiguity regimes
> + 0.08 * lowest subgroup mean over hidden dialect styles
> Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. Perfect labels with confidence 1.0 score exactly 1.0.
> The grader returns 0.0 if the submission columns are missing, extra, or reordered; if ids are duplicated; if the id set does not exactly match test.csv; or if confidence is missing, non-finite, or outside [0,1]. Event ids inside JSON must belong to that incident. Cyclic predicted edges receive zero topological-order credit.
> Dataset
> The prepared data is under public/. Log-file paths are relative to public/, and the same raw text is also present in the incident_text column for convenience.
> File overview
> public/train.csv contains labeled incidents with input columns and train-only labels. public/test.csv contains the same input columns without labels. public/train/logs/*.log and public/test/logs/*.log contain raw incident log streams. public/sample_submission.csv is a valid weak submission template.
> train.csv columns
> id is an opaque public integer row id. log_file is the relative path to the raw log text file. incident_text is the raw incident log stream with event ids inline. events_json is a JSON list of observed event objects. fleet_hint is a noisy public text hint and may be none. event_count is the number of observed events. prompt is the task instruction. causal_edges_json, root_cause_id, and concurrent_pairs_json are train-only labels.
> Each event object in events_json has event_id, ts_ms, service_code, template_id, raw_line, and severity. The root_cause_id label is either an observed event id or the literal UNKNOWN.
> test.csv columns
> id is an opaque public integer row id. log_file is the relative path to the raw log text file. incident_text is the raw incident log stream with event ids inline. events_json is a JSON list of observed event objects. fleet_hint is a noisy public text hint and may be none. event_count is the number of observed events. prompt is the task instruction.
> Submission
> Submit a CSV with exactly one row per id in test.csv and exactly these columns in this order: id, causal_edges_json, root_cause_id, concurrent_pairs_json, confidence.
> causal_edges_json must be a JSON list of [parent_event_id, child_event_id] integer pairs. root_cause_id must be an observed event id or UNKNOWN. concurrent_pairs_json must be a JSON list of unordered [event_id_a, event_id_b] integer pairs. confidence must be a finite float in [0,1].
> Example submission format:
> id,causal_edges_json,root_cause_id,concurrent_pairs_json,confidence
> 101,"[[117,131],[131,145]]",117,"[[160,174]]",0.74
> 102,[],UNKNOWN,"[[212,226],[240,254]]",0.43
> 103,"[[303,317]]",303,[],0.61

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific input/output structure.

## Chemical-Taxonomy Repertoires From 13C-NMR Peak Lists
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d931713sq1xc4tbwbm91rzd89r5x9
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Task
> Chemists read a ¹³C-NMR spectrum to work out what a molecule is; in this challenge, your model learns to do the same from the peak list alone. A ¹³C-NMR spectrum captures a molecule as the resonance frequencies (chemical shifts, in ppm) of its distinct carbons. Those shifts are a fingerprint of the carbon skeleton and its functional environment — a carbonyl carbon sits near 170–210 ppm, aromatic/olefinic carbons near 100–160, oxygenated aliphatics near 40–90 — but the spectrum underdetermines the molecule: symmetry collapses equivalent carbons to one peak, crowded regions overlap, and peaks are rounded or missing. Different molecules — belonging to different chemical-taxonomy nodes — routinely share near-identical shift sets.
> Your task: read the ¹³C peak list and predict the set of ChemOnt chemical-taxonomy nodes the molecule belongs to — its position in the chemical ontology (a set spanning several levels of the taxonomy, from broad to specific, not a single label). This rewards learning how whole-spectrum shift patterns map to chemical identity and transferring that to molecules unlike any in training. There is a natural ceiling here: because the spectrum underdetermines the structure, one shift set is consistent with many taxonomic assignments, so exact recovery is impossible and top scores stay well below 1.
> How this differs from prior work. Public tools that assign the ChemOnt ontology read mass spectra (CANOPUS) or the drawn structure (the ChemOnt rule engine) — not NMR. Tools that read NMR instead perform structure elucidation or emit a flat substructure/fragment presence array; the ontology node set is a connectivity-and-ring abstraction that a substructure array does not provide. The only prior NMR→ontology attempt is coarse (a handful of top-level superclasses, from 2-D correlation images, on a few hundred molecules). Predicting the fine, multi-level taxonomy node set directly from a 1-D ¹³C peak list as text, at scale, is unclaimed.
> Data
> All files are under ./dataset/public/.
> File	Contents
> train.csv	id, shifts, chemont_nodes — labeled training molecules.
> test.csv	id, shifts — the chemont_nodes are withheld.
> chemont_vocabulary.csv	the set of ChemOnt node names seen in training (your label space).
> sample_submission.csv	A correctly-formatted example (the most common nodes; scores ~0 macro-F1).
> Columns
> shifts (string) — the ¹³C spectrum as text: the token 13C followed by the sorted chemical shifts in ppm, e.g. 13C 21.0 40.1 55.2 114.9 128.3 129.7 138.1 172.4. One value per inequivalent carbon; this is the model input.
> chemont_nodes (string, train only) — the target: a ;-separated set of ChemOnt node names (e.g. Flavonoids;Phenylpropanoids and polyketides;Flavones), each drawn from chemont_vocabulary.csv.
> Submission
> Write ./working/submission.csv with exactly these two columns, in this order, one row per test id. For example:
> id,chemont_nodes
> 4679,Benzenoids;Phenols
> 4694,Prenol lipids;Monoterpenoids
> 4709,Flavonoids;Organooxygen compounds
> chemont_nodes is your predicted ;-separated set of node names, each from chemont_vocabulary.csv (the values above are format illustrations, not answers). The grader rejects a submission with the wrong columns/order, or a missing/extra/duplicate id.
> Evaluation
> The score (higher is better, Maximize, in [0, 1]) is the macro-averaged F1 over the ChemOnt node vocabulary: for each node, F1 is computed across the held-out molecules (predicted-contains vs truly-contains), and the per-node F1 scores are averaged. Macro-averaging weights every node equally, so recovering the informative, less-common nodes matters — predicting only the ubiquitous nodes, or spraying the whole vocabulary, both score near zero. Because the spectrum underdetermines the taxonomy and the test molecules are structurally unfamiliar, the achievable maximum is well below 1.
> Let the vocabulary V be the set of ChemOnt nodes that appear in the held-out answers or in your submission (so a node you predict that never occurs in the answers is still scored, not ignored). For a node n, count over all test molecules:
> TP(n)       = # molecules where n is BOTH predicted and true
> FP(n)       = # molecules where n is predicted but NOT true
> FN(n)       = # molecules where n is true but NOT predicted
> precision(n)= TP(n) / (TP(n) + FP(n))            # 0 if denominator is 0
> recall(n)   = TP(n) / (TP(n) + FN(n))            # 0 if denominator is 0
> F1(n)       = 2 * precision(n) * recall(n) / (precision(n) + recall(n))   # 0 if denominator is 0
> score       = ( sum over n in V of F1(n) ) / |V|,  clipped to [0, 1]
> Because V includes every node you predict, a node you output that never occurs in the answers has TP(n) = 0 and FP(n) > 0, so F1(n) = 0 — a full zero term that lowers the macro average. Over-predicting or spraying the vocabulary is therefore penalised, not free; predict only the nodes the spectrum supports.
> What to use
> Fine-tune a pretrained chemistry/sequence model (e.g. ChemBERTa) or train a peak-token transformer / sequence model from scratch, with a multi-label output head over the node vocabulary. Learning how the joint pattern of shifts (not just which ppm bins are populated) maps to chemical identity — and transferring it to unfamiliar scaffolds — is the productive path. (A frozen shift-histogram model already beats the frequency baseline, so the signal is real.)
> What not to use
> No internet at inference and no external chemical-ontology or spectral databases or structure-elucidation tools; train your model on the provided data (you may pip-install open-weight models and libraries at the start).
> No hardcoded per-id answers; predictions must come from your model.

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific input/output structure.

## Latent Isomeric Graph Reconstruction Under Instrument Shift
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78sd8e9ndc8ac4rc2nw2z5r189p3bb
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Molecular-networking systems usually return a single nearest neighbor or an
> unweighted match. That discards most of the structure in a local chemical
> family. In practice, a metabolomics system must determine which spectra imply
> close analogues, which imply remote isomers, and whether the entire inferred
> neighborhood remains chemically coherent when spectra were acquired on
> different instruments or at different collision energies.
> This challenge asks you to fine-tune a local spectrum representation model
> to reconstruct a complete latent chemical graph. Each row contains five
> experimental MS/MS spectra from five distinct molecules with the same neutral
> molecular formula. The molecular structures and formula are hidden. Your model
> must predict the continuous structural similarity of all ten undirected
> molecule pairs.
> The target for an edge is the Tanimoto similarity between chirality-aware,
> radius-2, 2,048-bit Morgan fingerprints of the two hidden structures. A
> solution therefore cannot succeed merely by identifying a single candidate.
> It must recover calibrated edge weights, the ordering of all ten relationships,
> and the high-similarity backbone of each five-node network.
> This is a representation fine-tuning challenge. Strong solutions should
> adapt an offline open-weight spectrum encoder, peak-set transformer, Siamese
> network, graph-aware model, or another learned spectrum representation using
> the released continuous supervision. Fixed spectral cosine is a useful
> diagnostic but is intentionally not sufficient: formula-matched isomers share
> precursor chemistry, acquisition conditions vary, and the hidden split is both
> formula-disjoint and scaffold-disjoint.
> Prediction Target
> Nodes are numbered 0 through 4. Predict one value in [0, 1] for each
> undirected edge in this fixed order:
> (0,1), (0,2), (0,3), (0,4), (1,2),
> (1,3), (1,4), (2,3), (2,4), (3,4)
> The corresponding target/submission columns are:
> similarity_0_1, similarity_0_2, similarity_0_3, similarity_0_4,
> similarity_1_2, similarity_1_3, similarity_1_4,
> similarity_2_3, similarity_2_4, similarity_3_4
> Node order is deterministic but chemically arbitrary. There is no privileged
> anchor node, and a model should not infer chemistry from a node index or the
> opaque network_id.
> Dataset
> The prepared public data contains:
> dataset/public/
> |-- train.csv
> |-- test.csv
> `-- sample_submission.csv
> train.csv has 617 complete networks and all ten continuous targets.
> test.csv has 242 complete hidden networks without targets.
> sample_submission.csv illustrates the required 242-row output format.
> The private evaluation contains 2,420 edge targets. Of these, 762 connect
> spectra acquired on different instrument families, spread across 146 complete
> hidden networks. Each network remains a single row, so public/private
> leaderboard partitioning never breaks a graph into dependent edge rows.
> Input columns
> | Column | Type | Description |
> |---|---|---|
> | `network_id` | string | Opaque 16-character network identifier. |
> | `node_{i}_mzs` | string | Comma-separated fragment m/z array for node `i`. |
> | `node_{i}_intensities` | string | Comma-separated intensities aligned with `node_{i}_mzs`. |
> | `node_{i}_precursor_mz` | float | Measured precursor m/z for node `i`. |
> | `node_{i}_adduct` | string | Precursor adduct for node `i`. |
> | `node_{i}_instrument_type` | string | Instrument family for node `i`. |
> | `node_{i}_collision_energy` | float/null | Collision energy when recorded. |
> The six node fields are repeated for i = 0, 1, 2, 3, 4. Peak arrays are
> variable length. mzs and intensities must be parsed as aligned arrays.
> Missing collision energy means unavailable metadata, not zero collision energy.
> Training-only columns
> The ten similarity_i_j columns contain continuous Morgan-fingerprint
> Tanimoto similarities in [0, 1].
> Split construction and leakage control
> One very novel quality-controlled spectrum is selected per molecular identity. Candidate
> networks contain five distinct molecules sharing a neutral formula. Networks
> are joined into connected components if they share either a formula or any
> non-empty, stereochemistry-stripped Bemis-Murcko scaffold. Components are
> assigned wholly to one split.
> After deterministic quality filtering:
> no molecular formula appears in both train and test;
> no non-empty Bemis-Murcko scaffold appears in both train and test;
> no selected spectrum appears in both train and test;
> exact duplicate peak arrays are removed;
> networks with nearly constant structural targets are excluded; and
> networks containing fingerprint-identical pairs are excluded.
> The test set therefore measures transfer to unseen chemistry rather than
> memorization of repeated molecular families.
> Evaluation
> Submissions are scored with the Edge-and-Topology Reconstruction Score
> (ETRS). Higher is better. ETRS combines calibrated edge reconstruction,
> within-network ordering, acquisition-shift robustness, and recovery of the
> network's maximum-similarity backbone.
> Notation:
> y[g,e] is the true similarity for edge e in network g.
> p[g,e] is the predicted similarity for that edge.
> G is the number of evaluated networks.
> clip(x, 0, 1) limits x to the inclusive range [0, 1].
> 1. Overall normalized-RMSE accuracy
> First calculate RMSE over every edge in every evaluated network:
> overall_rmse =
> sqrt(mean((y[g,e] - p[g,e]) ** 2 over all networks and edges))
> overall_accuracy =
> clip(1 - overall_rmse / 0.5, 0, 1)
> The constant 0.5 is fixed in advance and is one half of the full Tanimoto
> range. It does not depend on hidden-label statistics.
> 2. Mean within-network Spearman correlation
> For every complete network, compute Spearman correlation across its ten edge
> weights using average ranks for ties. A constant prediction receives
> correlation zero. The signed correlations are averaged first, then clipped:
> rho[g] =
> Spearman correlation between the 10 true and 10 predicted
> edge weights in network g
> network_rank_score =
> clip(mean(rho[g] over all evaluated networks), 0, 1)
> Negative networks therefore offset positive networks before clipping; negative
> correlations are not individually discarded.
> 3. Cross-instrument normalized-RMSE accuracy
> Let C be the hidden set of edges whose two spectra have different instrument
> families:
> cross_instrument_rmse =
> sqrt(mean((y[g,e] - p[g,e]) ** 2 for edges in C))
> cross_instrument_accuracy =
> clip(1 - cross_instrument_rmse / 0.5, 0, 1)
> This component contains 762 hidden edges; it is not estimated from a tiny
> query subset.
> 4. Maximum-spanning-tree edge F1
> For each network, construct the maximum spanning tree from the ten predicted
> weights and from the ten true weights. Each tree contains four edges. The
> per-network edge F1 is therefore:
> tree_f1[g] =
> number of shared edges between the true and predicted
> maximum spanning trees / 4
> tree_f1 =
> mean(tree_f1[g] over all evaluated networks)
> Exact ties are broken using the fixed edge order shown above.
> Final score
> ETRS =
> 0.35 * overall_accuracy
> + 0.25 * network_rank_score
> + 0.25 * cross_instrument_accuracy
> + 0.15 * tree_f1
> ETRS lies in [0, 1], and a perfect reconstruction scores 1.0.
> The components prevent one narrow strategy from dominating: a globally
> calibrated constant cannot recover ordering or topology; an uncalibrated
> spectral matcher may rank some edges but incurs RMSE; and a same-instrument-only
> model is penalized on the acquisition-shift stratum.
> Submission
> Write ./working/submission.csv with exactly one row per network_id.
> | Column | Type | Description |
> |---|---|---|
> | `network_id` | string | Identifier copied from `test.csv`. |
> | `similarity_i_j` | float | Predicted edge similarity in `[0, 1]`. |
> All ten edge columns listed in Prediction Target are required.
> Example:
> network_id,similarity_0_1,similarity_0_2,similarity_0_3,similarity_0_4,similarity_1_2,similarity_1_3,similarity_1_4,similarity_2_3,similarity_2_4,similarity_3_4
> 0a1b2c3d4e5f6789,0.31,0.56,0.24,0.42,0.38,0.61,0.29,0.47,0.35,0.52
> Requirements:
> exactly 242 rows, one for every test network_id;
> every test ID appears exactly once;
> exact column names and no additional columns;
> every prediction is finite and lies in [0, 1];
> CSV format with a header row.
> Modeling Guidance
> A competitive fine-tuning pipeline may:
> tokenize continuous m/z and intensity pairs or encode binned spectra;
> initialize from a local pretrained mass-spectrum or set encoder;
> use a shared Siamese encoder with a symmetric pair head;
> fine-tune jointly on calibration, edge-order, and graph-structure losses;
> condition on instrument, adduct, precursor m/z, and collision energy;
> model missing collision energy explicitly;
> augment peaks and acquisition metadata without changing node identity; and
> enforce graph-level consistency across the ten jointly predicted edges.
> Validation should keep each five-node network intact. Randomly splitting edge
> columns or treating the ten edges as unrelated examples gives an optimistic
> and structurally invalid estimate.
> What Not To Use
> Do not key predictions to network_id, row order, node index, or memorized
> source records.
> Do not manually annotate test networks.
> Do not use zero-shot or few-shot language-model prompting as the main
> predictor. The benchmark is intended to test local representation
> fine-tuning on the released supervision.

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific input/output structure.

## Historical Telugu Same-Sense Context Matching
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dq85m7gc8p4m5hn562kswys89mbc5
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Historical Telugu writing reuses the same lemma across mythology, devotional
> literature, grammar, poetry, and everyday usage. The difficult part is not
> recognizing the word form itself. The difficult part is deciding when two
> different passages are using that same surface form in the same sense.
> This challenge is a fine-tuning benchmark for that skill. The released benchmark
> contains 2449 prepared examples:
> 1943 training rows
> 506 test rows
> 110 total lemmas
> 37 lemmas represented in the test set, each with at least 8 test rows
> (median 16, max 16)
> The passages are historical, literary, devotional, and lexical Telugu rather
> than short modern benchmark sentences, which makes the task substantially more
> context-dependent than standard word-sense benchmarks.
> For each example you are given:
> one anchor context for a Telugu lemma
> four candidate contexts for that same lemma
> source titles for the anchor and all candidates
> Exactly one candidate uses the same sense as the anchor. The remaining three are
> near-miss uses of the same lemma drawn from other sense clusters, chosen to be
> genuinely confusable rather than simply the most different-looking option.
> The Task
> For each row, return a JSON object with exactly two keys:
> match_slot: which candidate context matches the anchor sense
> confidence: an integer from 0 to 100 — your estimated probability (in
> percent) that your match_slot is correct
> Allowed slot labels are A, B, C, and D.
> Required output format:
> {"match_slot":"C","confidence":74}
> Write only JSON. Do not include extra explanation.
> Dataset
> The prepared data is released under ./public/.
> Files
> The prepared dataset contains:
> public/train.csv
> Supervised training table with inputs and gold outputs.
> public/test.csv
> Hidden-evaluation input table without gold outputs.
> public/sample_submission.csv
> Minimal schema example showing the required submission format.
> File contents
> train.csv contains the anchor context, four candidate contexts, source titles,
> row-level prompt text, and the gold structured output fields.
> test.csv has the same input structure as train.csv except the gold output
> columns are removed.
> sample_submission.csv is a format example only. It is not a meaningful baseline.
> Input columns
> Important columns in train.csv and test.csv:
> Column	Type	Description
> id	string	Stable sample identifier
> lemma	string	Target Telugu lemma shared by the anchor and all four options
> anchor_source_title	string	Source page title for the anchor passage
> anchor_context	string	Anchor historical Telugu passage
> option_a_source_title	string	Source page title for candidate A
> option_a_context	string	Candidate A passage
> option_b_source_title	string	Source page title for candidate B
> option_b_context	string	Candidate B passage
> option_c_source_title	string	Source page title for candidate C
> option_c_context	string	Candidate C passage
> option_d_source_title	string	Source page title for candidate D
> option_d_context	string	Candidate D passage
> prompt	string	Full instruction-formatted prompt built from the row contents
> Training outputs
> train.csv additionally includes:
> Column	Type	Description
> output_text	string	Gold JSON output string
> match_slot	string	Gold same-sense slot, one of A, B, C, D
> confidence	integer	Always 100 in training rows (see below)
> Gold training confidence is always 100 because the gold match_slot is
> correct by construction. At evaluation time your confidence is scored against
> your own correctness, not a hidden target, so the right strategy is to learn
> calibrated confidence, not to copy 100.
> Split design
> The test set contains held-out anchor passages, so the model must compare
> contexts rather than rely on passage memorization. No context passage of any
> kind is shared between the released train and test splits. Every lemma that
> appears in the test set has at least 8 test rows, so per-lemma results are
> meaningful.
> Evaluation
> Submissions are scored from 0 to 100 using the
> Same-Sense Matching Score (SSMS).
> Each row receives:
> 90 points if match_slot is correct
> up to 10 points for confidence calibration against your own correctness
> Calibration uses a Brier-style quadratic rule, so the optimal confidence to
> report is your true probability of being correct:
> def row_score(match_ok, pred_conf):
> m = 1.0 if match_ok else 0.0
> c = pred_conf / 100.0
> match_points = 90.0 * m
> conf_points = 10.0 * (1.0 - (c - m) ** 2)
> return match_points + conf_points
> def evaluate(rows):
> return sum(row_score(**row) for row in rows) / len(rows)
> There is no hidden confidence target: conf_points depends only on your
> predicted confidence and whether your own match_slot was right. Reporting
> 100 on a wrong answer scores 0 calibration points; reporting your honest
> probability maximizes expected score.
> Perfect score is 100.0.
> Submission Format
> Submit a CSV with exactly these columns:
> Column	Type	Description
> id	string	Sample id from test.csv
> output_text	string	JSON object with match_slot, confidence
> Example:
> id,output_text
> sample_abc123def456,"{""match_slot"":""C"",""confidence"":74}"
> sample_7890fedcba12,"{""match_slot"":""B"",""confidence"":41}"
> sample_feedbead9021,"{""match_slot"":""A"",""confidence"":58}"
> Participants submit a CSV file. The JSON object lives inside the output_text
> string column of that CSV.
> Requirements:
> exactly one row per id in test.csv
> include a header row
> match_slot must be one of A, B, C, D
> confidence must be an integer from 0 to 100
> What Not To Use
> Do not use:
> external dictionary lookup or manual annotation at inference time
> handcrafted answer keys for specific sample ids
> outputs that ignore the required JSON format
> This is a fine-tuning challenge. The intended path is to adapt a language model
> to the training prompts and structured gold outputs.

Inspiration note: Useful because it frames adaptation around a concrete held-out task with domain-specific signals and evaluation.

## Commercial Telegraph Signal Generation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75awf8zwrb5vd136gh4r26cx89nh9h
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is a supervised language-model fine-tuning challenge built from real public-domain commercial telegraph codebook text. During preparation, all participant-facing clause text is converted into a deterministic source-neutralized pseudo-word representation, and row ids plus positional metadata are anonymized. Each row gives a masked neutralized codebook entry plus masked neighboring evidence. For every hidden test row, generate one structured pred_signal string. The scored outputs are the neutralized canonical entry text, its commercial register, and its message mood. The P field remains part of the required signal grammar for compatibility, but it is not used in the numeric score.
> Treat each row as a text-to-text training pair. The model input is the provided CSV row from train.csv or test.csv; the target in training is gold_signal. Competitive solutions should adapt or fine-tune a pretrained language model on the public training pairs so it can learn the neutralized phrase inventory, local masked-entry generation, and the compact signal grammar. Non-LLM structured classifiers or regressors are allowed only as auxiliary baselines; they still must emit the full C=... neutralized canonical text and are not the intended primary method.
> The rows are derived from a public-domain historical commercial cable-code corpus, but the competition is not a source lookup task: exact source wording, source row ids, source line positions, and first-letter bands are not exposed in the prepared files. The challenge adapts the standard pretrained-LM denoising text-to-text supervision pattern into a codebook signal-generation regime: the model must jointly generate the neutralized canonical entry and the three compact operator labels in a single parseable signal string. That joint text-plus-signal contract is the supervised fine-tuning target.
> The signal fields are:
> C  source-neutralized canonical entry text
> R  register_code: one of eight commercial function labels
> M  mood_code: one of six message-intent labels
> P  placeholder_count grammar field, integer 0 through 6, validated but unscored
> The task is hard because the public inputs expose only masked local evidence: the entry itself has content words replaced by ____, neighboring entries are also masked, and raw source wording, row order, source line numbers, source hashes, full OCR files, and private answers are not participant-facing. Strong solutions must learn the neutralized phrase inventory from supervised examples and fill the words hidden behind ____, rather than earn credit by copying visible words from the damaged clause.
> Dataset
> The prepared competition files are:
> public/
> train.csv                 7,600 labeled rows
> test.csv                  2,400 hidden-target rows
> sample_submission.csv     2,400 valid weak prediction rows
> submission_schema.md
> private/
> answers.csv               2,400 private answer rows
> prepare_summary.json
> train.csv
> column            type    description
> ---------------- ------- ------------------------------------------------------------
> case_id          string  Keyed anonymized row identifier.
> source_edition   string  Anonymized source-family label.
> lexical_band     string  Keyed anonymized lexical group.
> window_code      string  Keyed anonymized local-region group.
> left_context     string  Neutralized masked previous-clause hint.
> damaged_clause   string  Neutralized main clause with selected words replaced by ____.
> right_context    string  Neutralized masked next-clause hint.
> length_bin       string  Coarse word-count interval for the neutralized completion.
> gold_signal      string  Target signal string for supervised fine-tuning.
> test.csv
> Same input columns as train.csv, except gold_signal is removed. The hidden targets are in private/answers.csv for grading.
> sample_submission.csv
> A valid CSV template with exactly one row per test case_id. It uses varied deterministic weak predictions rather than one repeated majority label.
> Submission
> Submit one CSV file with exactly 2,400 rows and exactly these two columns in this order:
> column       type    description
> ------------ ------- ------------------------------------------------------------
> case_id     string  Must match one test case_id from public/test.csv exactly.
> pred_signal string  Generated signal string in the required four-field grammar.
> The pred_signal grammar is:
> C=<completion_text>;R=<register_code>;M=<mood_code>;P=<placeholder_count>
> Allowed R values:
> agency_instruction
> finance_credit
> freight_cargo
> general_commercial
> legal_claim
> market_quality
> time_quantity
> vessel_casualty
> Allowed M values:
> directive
> instruction
> negative
> query
> report
> statement
> P must be an integer from 0 through 6. C must be non-empty text and must not contain semicolons. Leaving blank markers such as ____ in C is syntactically valid but receives a severe content penalty. The P field is checked for valid format but is not part of the score.
> Example submission:
> case_id,pred_signal
> cid_ddvvzpvpudum,"C=witder catzor vat momcam;R=freight_cargo;M=query;P=0"
> cid_ddwrhtwpyjew,"C=pansar somken walbat;R=finance_credit;M=directive;P=0"
> cid_ddxxwsqsfjgh,"C=serzot jesvu guljar vegilkem;R=market_quality;M=negative;P=4"
> The submission contract is strict. Wrong columns, wrong column order, missing test ids, duplicate ids, extra ids, empty ids, empty pred_signal values, missing signal fields, repeated signal fields, unknown R or M values, and invalid P values are rejected by the grader. Valid but incorrect predictions receive low score.
> Evaluation
> The metric is the Telegraph Signal Score, a bounded maximize score from 0.01 to 1.0. Text similarity is computed only over the words that should replace ____ in damaged_clause. Visible words already present in the public input do not contribute to text similarity.
> row_score =
> 0.84 * token_F1(masked_words(C_pred), masked_words(C_true))
> + 0.10 * sequence_ratio(masked_words(C_pred), masked_words(C_true))
> + 0.04 * exact_match(R_pred, R_true)
> + 0.02 * exact_match(M_pred, M_true)
> token_F1 lowercases text, removes punctuation, tokenizes on alphanumeric words, and computes F1 overlap between predicted and true completion tokens. sequence_ratio is a normalized character-level similarity ratio after the same lowercasing and punctuation normalization. The masked_words operation aligns the submitted C field to the row's damaged clause template and extracts only the token spans that occupy the ____ positions. If C_pred contains ____, both text-similarity terms are multiplied by 0.25.
> score = mean(row_score over all private test rows)
> score is clipped to [0.01, 1.0]
> The metric direction is maximize. A perfect submission scores 1.0. The sample submission is valid but intentionally weak. Copying the visible damaged_clause without filling masked words receives little text credit because the visible words are not scored.
> Safety or Restrictions
> Use only the prepared public files supplied with the challenge when producing predictions. Do not use external scans, OCR dumps, library catalog pages, mirrors, web search over masked entries, raw dataset upload files, source line numbers, source hashes, private answers, or any other lookup oracle for hidden test rows.
> Allowed methods include supervised fine-tuning, LoRA or adapter tuning, instruction tuning, validation splits made from train.csv, and general pretrained language knowledge. The dataset contains public-domain historical commercial text only. It contains no private communications, medical data, biological records, synthetic source entries, or computer-vision data.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Remote Homology EC Level 3 Enzyme Function Ranking
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71190v5ntt31q92mcy9bjb6x89h40x
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, large-scale
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You receive protein amino-acid sequences with enzyme-function labels for training rows. For each hidden test protein, submit five ranked predictions for its three-level enzyme commission class, such as 2.7.7.
> The test split uses sequence families withheld during benchmark preparation. Close-family memorization will miss many hidden rows. Strong solutions should train or fine-tune sequence models that recognize motifs, residue patterns, and broader enzyme-class signals across remote homologs.
> Use only files under dataset/public/. Do not use internet retrieval, sequence search services, external sequence databases, source lookup, original source identifiers, or hidden answers. You may use pretrained sequence models only when their weights already exist in the execution environment and no one trained or fine-tuned them on this prepared benchmark.
> Evaluation
> The grader uses Hierarchy-Aware Top-5 EC Score. Higher is better.
> For each test protein, the grader compares the submitted ranked EC-level-3 predictions ec_1 through ec_5 with the hidden target:
> exact EC-level-3 match: 1.00 credit
> same first two EC fields: 0.35 credit
> same first EC field: 0.10 credit
> otherwise: 0.00 credit
> The grader applies these rank discounts:
> ec_1: 1.00
> ec_2: 0.75
> ec_3: 0.55
> ec_4: 0.40
> ec_5: 0.30
> The row score is the best discounted credit across the five predictions. The final score averages row scores within each true EC-level-3 label, then macro-averages those label means.
> Dataset
> dataset/public/ contains:
> train.csv: training protein sequences and labels.
> test.csv: hidden-test protein sequences without labels.
> sample_submission.csv: valid submission template.
> label_schema.json: label list, submission columns, split note, and metric summary.
> train.csv
> protein_id (string): anonymized protein identifier.
> amino_acid_sequence (string): protein sequence using one-letter amino-acid codes.
> sequence_length (integer): sequence length.
> taxon_domain (string): broad source domain bucket.
> ec_level1 (string): first EC field for the training label.
> ec_level2 (string): first two EC fields for the training label.
> ec_level3 (string): target class for training.
> test.csv
> protein_id (string): anonymized test protein identifier.
> amino_acid_sequence (string): protein sequence using one-letter amino-acid codes.
> sequence_length (integer): sequence length.
> taxon_domain (string): broad source domain bucket.
> Submission
> Submit submission.csv with these columns in this exact order:
> protein_id (string): must match each protein_id in test.csv exactly once.
> ec_1 (string): highest-ranked EC-level-3 prediction.
> ec_2 (string): second-ranked EC-level-3 prediction.
> ec_3 (string): third-ranked EC-level-3 prediction.
> ec_4 (string): fourth-ranked EC-level-3 prediction.
> ec_5 (string): fifth-ranked EC-level-3 prediction.
> Requirements:
> Include exactly one row for each test protein.
> Use a header row.
> Keep the column order shown above.
> Each prediction must use EC-level-3 format: one digit from 1 to 7, a period, one or more digits, a period, and one or more digits.
> Do not repeat an EC prediction within the same row.
> Example:
> protein_id,ec_1,ec_2,ec_3,ec_4,ec_5
> prot_0123456789abcdef01,2.7.7,2.1.1,3.1.1,1.1.1,6.1.1

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## DNA Barcode Family and Artifact Detection
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77g5rzp8939m63c57e4yqw0189c2ve
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is an open-set classification problem that goes well beyond standard barcode taxonomic identification, where a model simply names the taxon of a clean reference sequence. The classifier you train must add a sequence-integrity judgment: reading each DNA-barcode text, it decides whether the sequence is a known family, an unseen lineage, or a non-genuine barcode — and the genuine-versus-non-genuine call is the heart of the problem.
> For each barcode text the classifier outputs one of 22 class labels, which fall into three kinds:
> one of 20 known insect families (opaque codes F01…F20);
> a novel lineage (NOVEL) — an authentic barcode from a family outside the 20 known ones;
> an artifact (ARTIFACT) — not a genuine functional barcode: a pseudogene-like copy (for example a nuclear mitochondrial pseudogene / NUMT, or a frameshifted or otherwise degraded duplicate) that superficially resembles a real barcode but is not a valid one.
> Two properties make this harder than an ordinary sequence classifier and than an off-the-shelf barcode taxonomic identifier, so the modeling approach has to earn its result:
> Integrity, not just identity. Flagging the pseudogene-like artifacts is a functional-validity judgment about the sequence itself, not a similarity-to-reference judgment. Surface-similarity barcode identifiers do not make this call; a model has to learn the deeper sequence structure that betrays a non-functional copy.
> A divergence trap. Novel lineages, pseudogene artifacts, and members of known families from unseen lineages can all sit at similar surface divergence from anything in the training texts. So a nearest-neighbour / distance / closed-set-confidence approach — the reflex for both taxonomic identification and out-of-distribution rejection — conflates the three and collapses. The signal that separates them lives in the deeper structure each sequence model must learn to represent, not its surface letter composition.
> Data
> Everything is under ./dataset/public/.
> File	Columns	Contents
> train.csv	id, sequence, label	~27,600 training barcode texts with answers. label ∈ {F01…F20, NOVEL, ARTIFACT}. A fraction of the training answers are noisy.
> test.csv	id, sequence	~9,300 barcode texts for the model to answer. Answers withheld.
> sample_submission.csv	id, label	A correctly-formatted template (one row per test id, with placeholder answers).
> Column descriptions
> id (string) — opaque 16-character row identifier.
> sequence (string) — the barcode text: a raw nucleotide string over {A, C, G, T, N} plus a few IUPAC ambiguity letters; variable length (roughly 400–660 characters). Orientation and reading position are not normalized.
> label (string) — the case-sensitive answer. The 20 family codes are opaque (they carry no external meaning).
> Task
> Train your model on train.csv. Then, for each id in test.csv, have the model read the barcode text and assign its label, and write ./working/submission.csv with exactly the columns id,label (in that order), one row per test id.
> The known families are represented in training through a subset of their member lineages; the test set includes barcode texts from related lineages not present in training. NOVEL and ARTIFACT examples appear in both train and test, but the specific novel lineages and the specific artifacts in the test set are not the same individuals as those in training — so the model must generalize from the training sequences rather than memorize them.
> Evaluation
> Submissions are scored by macro-averaged F1 over the full set of 22 answers, combined across the whole test set and a hidden harder subset:
> overall = macro-F1 over all test rows (all 22 answers)
> hard    = macro-F1 over a hidden, harder subset (over the answers with enough hard rows)
> score   = 0.50 * overall + 0.50 * hard
> Macro-averaging means every one of the 22 answers — including the rarer families and the two reject answers (NOVEL, ARTIFACT) — counts equally in the overall term; a model that favours only the common families scores poorly. The hard subset (the majority of the test rows) emphasizes the more difficult barcode texts and is weighted equally with the overall term. Its macro-F1 is taken over the answers that have enough hard rows to be scored reliably, so a single data-limited family with very few hard rows is scored through the overall term alone and does not destabilize the result. You cannot identify which rows the hard subset contains, so aim to train a model that performs well across the entire test set. Higher is better; the score is in [0, 1].
> Submission format
> Write ./working/submission.csv with exactly these columns, in this order:
> id,label
> Example:
> id,label
> 3f9a1c2b7d4e5061,F07
> 8a1b2c3d4e5f6071,NOVEL
> 1c0d2e3f40516273,ARTIFACT
> One row per test id (no missing, extra, or duplicate ids); every value in the label column must be one of the 22 valid answers (case-sensitive); no empty/NaN values. The grader rejects (raises) any submission with the wrong columns, a wrong/missing/duplicate id set, or a label outside the valid set.
> What to use
> The work is in reading and modeling the raw nucleotide text — the input is the sequence text and nothing else. Train your model on the provided sequences using the deep-learning libraries available in the offline runtime. Either route below is appropriate:
> From scratch (self-contained): train a sequence model from scratch — e.g. a 1-D convolutional or transformer encoder over the nucleotide text, or a learned sequence-feature model — on the provided training texts. This needs no external weights and is always viable inside the runtime.
> Fine-tune (only if the weights are already in the runtime): if the offline runtime already provides a pretrained sequence encoder (a tokenizer + encoder over k-mer or single-nucleotide tokens), you may fine-tune it on the provided texts with a small output head — you cannot download one.
> Either way the result has to come from a model you trained on the provided sequences. No task-specific pretrained weights are required. An off-the-shelf barcode taxonomic identifier alone does not solve this task: it gives no NOVEL or ARTIFACT decision and offers no functional-validity signal. Check the platform's environment policy for the authoritative list of libraries (and any cached model weights) available in the sealed runtime.
> What not to use
> Use only what is already in the Eris/Kaggle runtime plus the challenge data. Not allowed: installing or downloading any package, wheel, repository, script, notebook, or module at runtime (pip/conda/apt/npm/…); any internet access, hosted LLM/VLM inference API, or remote service; external datasets or extra training data (via kaggle, datasets, urllib, requests, boto3, s3fs, or direct URLs); private or gated models/weights/datasets; trust_remote_code=True, torch.hub.load(), or similar loaders that fetch and execute external code; BLAST or external sequence databases; and passing off a challenge-specific fine-tuned checkpoint as "pretrained." Read each barcode with a model you train on the provided sequences using the runtime's libraries.
> No external answer catalogues or reverse lookups of the sequences.
> No hardcoded per-id predictions, and no use of the row id order or range as a signal.
> Submissions must be produced by your model, not pasted from a language model's output.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Product-Selectivity Classification of CO2 Electroreduction Catalysts from Redacted Paper Abstracts
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79nfrpkckhxyseg9w5q5sx4589v51v
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview:
> This is a natural-language understanding task. You are given the text of a research-paper passage (the title plus abstract) that describes an electrocatalyst for the electrochemical reduction of carbon dioxide (CO2 electroreduction, or CO2RR), and you must read that text and infer the single carbon product for which the described catalyst is reported to be selective. The intended approach is to fine-tune a language model (for example a scientific transformer such as SciBERT, MatSciBERT, or ChemBERTa) on the provided training passages so that it learns to map catalyst chemistry described in prose to the product the catalyst makes. Selectivity is the central design goal of CO2 electroreduction: turning CO2 into one target fuel or feedstock rather than a mixture.
> The task is deliberately a reading and reasoning problem, not a lookup. Every explicit mention of the product has been redacted from the text. Wherever the original abstract named the product, whether as a formula (such as CO, HCOOH, CH4, C2H4, C2H5OH) or as a word (such as carbon monoxide, formate, methane, ethylene, ethanol), that mention has been removed. A single placeholder token <prod> is left in each passage to mark that a redaction happened; every passage contains exactly one <prod> token regardless of how many times the product was originally named, so the number of placeholder tokens carries no information about the answer. You therefore cannot read the answer off the page. Instead the model must interpret the natural-language description of the chemistry: the catalyst metal and composition, its structure, facet, defect, and dopant engineering, the synthesis route, the electrolyte, and the way performance is discussed.
> The mapping from catalyst text to product is chemically meaningful but not one-to-one: copper-based catalysts can be steered toward CO, formate, methane, ethylene, ethanol, or generic multi-carbon products depending on their structure and environment, while silver and gold tend toward CO and tin, bismuth, and indium tend toward formate. A strong solution must model the scientific language, not match surface keywords. This is a low-resource, domain-specific text task, so language modeling and transfer learning matter more than raw data volume.
> Note on task origin: the source corpus was published for named-entity recognition (labeling the material, product, and method spans that appear in the text). This challenge is a different, non-native use of that text: the product span is deleted, and a language model must recover it as a latent property of the described catalyst.
> Evaluation:
> The metric is the macro-averaged F1 score over the six possible products (CO, HCOOH, C2H4, C2+, CH4, C2H5OH). For a single product label c, count true positives TP (test passages whose true product is c and that you labeled c), false positives FP (passages you labeled c whose true product is not c), and false negatives FN (passages whose true product is c but that you labeled something else). Then:
> precision(c) = TP / (TP + FP)
> recall(c) = TP / (TP + FN)
> F1(c) = 2 * precision(c) * recall(c) / (precision(c) + recall(c))
> with F1(c) defined as 0 when the denominator is 0. The final score is the unweighted mean of F1(c) over the six products:
> macro_F1 = (1/6) * sum over c of F1(c)
> The score ranges from 0.0 to 1.0 and higher is better. Because every product is weighted equally, always predicting the most frequent product scores near zero (about 0.06 here), so the metric rewards getting the minority products right too.
> Dataset:
> The following files are provided in the public data directory. The dataset is intentionally small (a low-resource scientific-text setting): 450 training passages and 242 test passages.
> train.csv - the training set, 450 rows. Columns:
> id - string - unique row identifier (for example co2rr_tr_0007).
> text - string - the redacted paper title plus abstract (lowercased, with DOIs and copyright boilerplate stripped, every product mention removed, and a single <prod> marker left per passage).
> product - string - the label: the CO2-reduction product the catalyst is selective for. One of CO, HCOOH, C2H4, C2+, CH4, C2H5OH.
> test.csv - the test set, 242 rows. Columns:
> id - string - unique row identifier (for example co2rr_te_0042).
> text - string - the redacted paper title plus abstract, in the same format as the training text. There is no product column.
> sample_submission.csv - a valid submission in the correct format, 242 rows (one per test id). Columns:
> id - string - matches the ids in test.csv.
> prediction - string - a product label. In this sample file every row is filled with the most frequent training product as a placeholder.
> The six possible products (label vocabulary):
> CO - carbon monoxide.
> HCOOH - formate / formic acid.
> C2H4 - ethylene.
> C2H5OH - ethanol.
> CH4 - methane.
> C2+ - unspecified multi-carbon (C2 and higher) products.
> Class balance of the labels: CO and HCOOH are the most common products and CH4 and C2H5OH are the least common; all six products appear in both the training and test sets.
> Submission:
> Submit a CSV with exactly two columns, id and prediction, and one row per test id (242 rows plus a header).
> Column - Type - Meaning
> id - string - a test row identifier, exactly matching an id in test.csv.
> prediction - string - your predicted product label, one of CO, HCOOH, C2H4, C2+, CH4, C2H5OH.
> Example submission (header plus three example rows):
> id,prediction
> co2rr_te_0000,CO
> co2rr_te_0001,C2H4
> co2rr_te_0002,HCOOH
> Requirements:
> The header row must be exactly: id,prediction
> Provide a prediction for every test id, with no duplicates and no missing ids (242 data rows, matching test.csv).
> Each prediction must be one of the six product strings above; any other string counts as incorrect for grading.
> Rules:
> The only valid input signal for predictions is the text content of each redacted catalyst passage, and predictions must come from a model that represents the token sequence. The following approaches are not allowed:
> Hardcoding predictions for specific test ids.
> TF-IDF, bag-of-words, hashing-count, or plain n-gram-count feature vectors fed to a linear model. Sparse term-frequency representations are prohibited as the prediction mechanism; predictions must come from a model that reads the token sequence, for example learned token or character embeddings, a convolutional or recurrent encoder over the text, or a fine-tuned transformer language model.
> Recovering the deleted product from the text. Every product mention is redacted and a single <prod> marker is left per passage; attempting to undo the redaction, using the number or position of <prod> tokens as a signal (the count is constant, one per passage), or exploiting residual formatting artifacts of the source PDFs (for example Faradaic-efficiency or current-density subscripts, glued tokens, or full-width parentheses) to reconstruct which product was named, is not allowed. Predict the product from the catalyst chemistry, not from a leaked mention.
> Matching a passage back to its original publication. Using the paper title, a distinctive phrase, or any web or database search to locate the source paper and read the product from the original article is prohibited. Digital object identifiers have been stripped, and only the provided redacted text may be used at inference time.
> Using the id strings, the row order, or the text length as a prediction signal instead of the passage content.
> Using private, role-gated, or API-key-based models, or calling any external inference API during inference.
> Using non-reproducible external weights or artifacts that are not publicly available.
> This task tests whether a language model can read the scientific description of a CO2-reduction electrocatalyst and infer its product selectivity, which requires understanding catalyst composition (the active metal and dopants), morphology and facet or defect engineering, electrolyte, and the way performance is discussed, and then mapping that chemistry to the correct carbon product. A solution that scores well by recovering a leaked product mention, by matching passages to their source papers, or by exploiting ids, ordering, or length rather than the chemistry is not valid regardless of its score.
> Pretrained model policy:
> Fine-tuning a publicly available pretrained language model (for example SciBERT, MatSciBERT, ChemBERTa, or a general transformer such as BERT or RoBERTa) is allowed and is the intended approach, provided the fine-tuning genuinely uses the provided training passages and their labels. Domain-pretrained scientific or chemistry language models are encouraged because the intended skill is reading catalyst chemistry. If a pretrained model were to solve this task with near-perfect macro-F1 and minimal training, train from scratch on the provided training passages instead. Real learning here means associating catalyst composition, structure, and synthesis language with product selectivity, not memorizing product keywords (which have been removed).

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Review Diff Atom Forecasting
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77jf72rzjf1jxw43d409mzsh89wnsk
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is a fine-tuning task for code-review automation. Each example contains a human review note and the anonymized code region that was reviewed. The goal is to predict the compact semantic edit signature of the accepted revision: which code atoms were added and which code atoms were removed.
> The target is not a candidate-choice label and not a full regenerated patch. The accepted human revision is transformed into two space-separated atom sets. Atoms represent semantic code elements such as Java keywords, literal kinds, and operators, using safe names like kw_if, kw_return, lit_null, op_eqeq, and op_lambda.
> Useful systems should learn how review language maps to structural code edits. For example, a note about null handling may imply lit_null, kw_if, or comparison operators; a note about exception behavior may imply kw_throw, kw_try, or kw_catch. The identifiers and literals in the public code are anonymized, and ordinary prose terms in review notes are deterministically masked as term_* tokens while code keywords are preserved. This keeps the real review signal but makes source lookup and memorized names poor shortcuts.
> Dataset
> File descriptions
> train.csv -- 3,200 labeled review-diff examples with a review note, marked code, prompt, and the two target atom lists.
> test.csv -- 1,200 held-out review-diff examples with the same public fields but without target atom lists.
> train.jsonl -- JSONL mirror of the training cases for fine-tuning workflows, with instruction, input, and output fields.
> test.jsonl -- JSONL mirror of the held-out cases for inference workflows, with instruction and input fields.
> sample_submission.csv -- A template showing the required id,added_atoms,removed_atoms submission format with random atom lists.
> Column descriptions
> id (string) -- Hashed identifier for the review case.
> review_note (string) -- Anonymized human review note describing the requested code change; ordinary prose terms may appear as term_* tokens.
> marked_code (string) -- Anonymized pre-review code with [[REVIEW_START]] and [[REVIEW_END]] markers around the reviewed span.
> prompt (string) -- Full instruction-style prompt containing the review note and marked code.
> added_atoms (string) -- Train-only target: space-separated semantic atoms added by the accepted revision.
> removed_atoms (string) -- Train-only target: space-separated semantic atoms removed by the accepted revision.
> Evaluation
> Submissions are scored with mean atom-set F1. Higher is better. The grader parses added_atoms and removed_atoms as unordered sets, computes F1 against the hidden accepted-revision atom sets for each side, then averages the added and removed scores for each row.
> def atom_f1(predicted, truth):
> predicted = set(predicted)
> truth = set(truth)
> if not predicted and not truth:
> return 1.0
> if not predicted or not truth:
> return 0.0
> return 2 * len(predicted & truth) / (len(predicted) + len(truth))
> row_score = 0.5  *atom_f1(predicted_added, true_added) + 0.5*  atom_f1(predicted_removed, true_removed)
> The final score is the mean row score across all held-out examples. Random atom lists are expected to score poorly; common-atom baselines do better but miss review-specific edit intent.
> Submission
> Submit a CSV file with predicted atom lists for every row in test.csv.
> id (string) -- The hashed identifier from test.csv.
> added_atoms (string) -- Space-separated predicted atoms added by the accepted revision.
> removed_atoms (string) -- Space-separated predicted atoms removed by the accepted revision.
> Example:
> id,added_atoms,removed_atoms
> 000a7508f0a5,kw_new kw_if kw_String,kw_final kw_String
> 00af1c7e4735,lit_str kw_new,lit_str kw_new
> Requirements
> The file must contain exactly 1,200 rows plus the header.
> Every id from test.csv must be present exactly once.
> The file must use exact column names id,added_atoms,removed_atoms.
> Atom lists may be separated by spaces, commas, or semicolons.
> Empty predictions are allowed but usually score poorly.
> Predicted atoms must use the challenge vocabulary, such as kw_if, kw_return, lit_str, lit_num, lit_null, op_eqeq, op_ne, op_lt, op_gt, op_and, op_or, and op_lambda.
> Method Requirements
> This benchmark requires learning-based approaches with model training or fine-tuning as a core component. Participants are expected to train models that learn review-note-to-diff-signature behavior from the public examples. The goal is to evaluate whether models can infer the structural edit implied by a review note and the marked code context.
> Purely rule-based, template-based, or hardcoded systems are not permitted. This includes approaches that rely only on fixed keyword lists, always predicting the most common atoms, or hand-written mappings from review words to atoms.
> Hybrid approaches are allowed only if a meaningful trained component remains central. Supporting heuristics for tokenization, atom formatting, thresholding, or post-processing are fine, but they must not replace the learned predictor.
> What Not To Use
> Do not use external copies of the underlying code-review corpus, public benchmark mirrors, or original split files to recover held-out revisions.
> Do not submit a hardcoded map from test IDs, prompt strings, marked code, or row order to atom lists.
> Do not exploit raw source split order or source-file lookup as a shortcut. The challenge is about predicting the accepted diff signature from the public review note and marked code.
> Do not use a fixed rule-only selector that ignores the public added_atoms and removed_atoms training labels.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Named Entity Span Detection
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71tjbarrwsz7bfwsrmj4tw0n89wrb0
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Pending Review
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given a tokenized sentence and must perform object detection over its token axis: find
> every named-entity mention in the sentence and, for each one, report (a) the token interval it
> spans and (b) its entity class. The eight classes are:
> person location organization building art product event other
> Each detected object is a span [start, end) over the token positions (start token inclusive, end
> token exclusive) with an entity class and a confidence score. This is the 1-D analogue of image
> object detection — localize objects (here, entity mentions) on a sequence and classify them — and it is
> scored with the standard detection metric, mean Average Precision (see Scoring). The intended apparatus
> is a sequence model / span detector (for example a token tagger or span-enumeration model) trained on
> the provided (sentence → spans) pairs.
> The classes follow the coarse entity types of the source corpus: person; location (countries,
> cities, geographical features, ...); organization (companies, institutions, teams, ...);
> building (named structures, airports, hotels, ...); art (creative works: books, films, music,
> paintings, ...); product (named products, vehicles, software, ...); event (named events, wars,
> sports events, ...); and other (a catch-all for the remaining named entities, e.g. laws, languages,
> scientific terms).
> The token axis
> Each sentence is a whitespace-separated sequence of tokens. Token index i is the i-th token when
> the sentence is split on whitespace, 0-indexed. A span [start, end) covers the tokens
> start, start+1, ..., end-1 (so a single-token entity at position i is the span [i, i+1)). All
> spans you submit are in these token indices.
> Data
> All files live under public/; the identifier is the sentence id id. The benchmark has 18,000
> sentences in total, split 14,400 train / 3,600 test by sentence (each sentence is one document, so
> no sentence is shared). Every sentence contains at least one entity; there are 42,697 training and
> 10,364 test ground-truth entity spans.
> Files provided:
> train.csv — the 14,400 training sentences, columns id, tokens (the whitespace-joined token
> sequence).
> train_labels.csv — the ground-truth entity spans for the training sentences (many rows per id).
> test.csv — the 3,600 sentences to solve, columns id, tokens (no labels).
> sample_submission.csv — an example submission in the exact required shape (columns below). Its rows
> are a capitalization-heuristic baseline (each run of capitalized tokens submitted as a location
> span); it is a weak, no-learning baseline you should aim to beat.
> Columns of train.csv and train_labels.csv, with their data types and meanings:
> id (in train.csv) — type str. The sentence identifier, an opaque token (e.g. doc-3f9a2c7b1).
> tokens (in train.csv) — type str. The sentence as a whitespace-joined token sequence; token i
> is the i-th whitespace token (0-indexed).
> id (in train_labels.csv) — type str. The sentence id (matches train.csv); it appears once per
> entity, so several rows can share the same id.
> label (in train_labels.csv) — type str. The entity class of the span — one of the eight classes
> listed above.
> start (in train_labels.csv) — type int. The first token index of the entity span (inclusive).
> end (in train_labels.csv) — type int. One past the last token index of the span (exclusive);
> always end > start.
> The same columns in table form:
> File	Column	Type	Description
> train.csv	id	str	Sentence id.
> train.csv	tokens	str	The sentence as a whitespace-joined token sequence; token i is the i-th whitespace token (0-indexed).
> train_labels.csv	id	str	Sentence id (matches train.csv); appears once per entity, so several rows share an id.
> train_labels.csv	label	str	Entity class of the span — one of the eight classes listed above.
> train_labels.csv	start	int	First token index of the entity span (inclusive).
> train_labels.csv	end	int	One past the last token index of the span (exclusive); end > start.
> Example rows (train.csv then train_labels.csv):
> id,tokens doc-3f9a2c7b1,Alan Turing was born in London and worked at Bletchley Park . id,label,start,end doc-3f9a2c7b1,person,0,2 doc-3f9a2c7b1,location,5,6 doc-3f9a2c7b1,building,9,11
> (Alan Turing = tokens 0–1 → [0,2); London = token 5 → [5,6); Bletchley Park = tokens 9–10 → [9,11).)
> Submission format
> Submit a CSV named submission.csv with exactly five columns. Each row is one predicted detection;
> a sentence may have any number of rows, including zero (variable-length output, as in object
> detection):
> Column	Type	Description
> id	str	A test sentence id (from test.csv). Every id you use must be a valid test id; you may emit multiple detections per id and need not cover every id.
> label	str	Predicted entity class — one of the eight classes (case-insensitive).
> start	int	First token index of the predicted span (inclusive).
> end	int	One past the last token index (exclusive); must satisfy end > start.
> score	float	Confidence of the detection (higher = more confident). Used only to rank detections; the scale is arbitrary.
> Include the header row id,label,start,end,score. Rows with an unknown class, a degenerate span
> (end <= start), or a non-numeric field are discarded. Concrete example (submission.csv, header +
> three rows):
> id,label,start,end,score doc-7c4e1a9d2,person,0,2,0.96 doc-7c4e1a9d2,location,5,6,0.90 doc-1b2c3d4e5,organization,3,7,0.61
> Scoring: mean Average Precision (COCO-style, on 1-D token spans)
> Your detections are scored with mean Average Precision (mAP), the standard object-detection metric,
> on 1-D token intervals. It is computed exactly as follows.
> 1. Localization overlap. For a predicted span P = [p0, p1) and a ground-truth span G = [g0, g1),
> the Intersection-over-Union is the overlap length divided by the union length:
> inter = max(0, min(p1, g1) - max(p0, g0)) IoU(P, G) = inter / ( (p1 - p0) + (g1 - g0) - inter )
> (So identical spans have IoU 1; a span that is one token too long/short has IoU below 1.)
> 2. Matching predictions to ground truth (per class, per IoU threshold). Fix an entity class c and
> an IoU threshold t. Take the predicted detections of class c across all test sentences and sort
> them by descending confidence score. Walk down that sorted list; for each detection, consider the
> ground-truth spans of class c in the same sentence that are not yet matched, and take the one with
> the highest IoU. If that IoU is >= t, the detection is a true positive and that ground-truth span
> is now consumed (each ground-truth span may be matched at most once); otherwise the detection is a
> false positive (this includes a detection in a sentence with no unmatched class-c span within IoU
> t). A detection only ever competes for and consumes ground-truth spans of its own class, so a
> detection of one class can never block, steal, or lower the match of a detection of another class.
> Emitting a duplicate or spurious span therefore only adds a false positive to that span's own class,
> lowering that class's precision — it cannot take another entity's match away.
> 3. Average precision of a class at threshold t. For each class c, restrict to the detections of
> class c, kept in the same descending-confidence order, each carrying the true-/false-positive flag
> assigned in step 2. Going down them, accumulate true and false positives and form, at each position k,
> recall(k) = (class-c true positives in the top k) / (total ground-truth spans of class c) precision(k) = (class-c true positives in the top k) / (class-c detections in the top k)
> Average Precision is the area under the precision–recall curve, computed by 101-point interpolation:
> for each recall level r in {0.00, 0.01, 0.02, ..., 1.00}, take the highest precision attained at any
> recall >= r (0 if none), and average these 101 values:
> AP(c, t) = ( 1 / 101 ) * sum over r in {0, .01, ..., 1} of max{ precision(k) : recall(k) >= r }
> 4. Averaging over thresholds and classes. AP for a class is averaged over the six IoU thresholds
> t in { 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 } AP(c) = mean over t of AP(c, t)
> and these are averaged over the classes that occur in the test set (all eight) to give the mean average
> precision:
> mAP = ( 1 / 8 ) * sum over the eight classes c of AP(c)
> 5. Difficulty shaping. The final score is a monotonic shaping of mAP that spreads similar-quality
> detectors apart (so scores do not clump together) and keeps the top of the range hard to reach:
> score = 0.45 * ( mAP / 0.40 ) ** 2 if mAP <= 0.40 score = 0.45 + 0.55 * ( mAP - 0.40 ) / ( 1 - 0.40 ) if mAP > 0.40
> What not to use
> The task is to DETECT the entity mentions in each given sentence — localize each as a token span and
> classify it — using only the sentence you are given. Your detections must be produced from the sentence
> itself, not looked up. The following are disqualifying:
> Exogenous retrieval of the answer. Matching a test sentence (or its tokens) against any external
> index, corpus, or annotation store — including the source corpus this dataset was derived from — to
> recover the ground-truth spans or labels instead of detecting them from the sentence. Detect the
> entities; do not fetch their gold annotations.
> Identity-keyed or trivial outputs: hard-coded detections, lookup tables, or predictions keyed on the
> sentence id, row order, file hashes, or the verbatim tokens string.
> Test-label leakage: using the test sentences in any way other than as detector input (e.g. matching
> test sentences against training sentences/labels by hash or near-duplicate to copy spans by index),
> or any use of held-out information not derivable from a single test sentence.
> Oracle distillation: invoking an external pretrained model or hosted service that already performs
> named-entity recognition on these sentences (a general-purpose hosted LLM, a commercial NER endpoint)
> to generate or label the test detections, or distilling such a model's outputs onto the test set.
> Human annotation: manually reading each test sentence and marking the entity spans by hand.
> PERMITTED — any method that maps a sentence to a set of (span, class, score) detections and generalizes
> to unseen sentences, for example:
> training your own sequence / span models of any architecture (token taggers with BIO/BILOU decoding,
> span-enumeration or boundary models, CRFs, biLSTMs, transformers/encoders, and so on) on the provided
> (sentence → spans) pairs;
> initializing from an open pretrained language model / word embeddings and fine-tuning it on this
> corpus; any feature engineering over the tokens;
> data augmentation (token dropout, entity swapping, synthesizing extra training sentences from the
> provided training spans), calibration, ensembling, span non-maximum suppression, and re-scoring of
> your own detector's outputs.
> In short: detect the entity spans in the sentence using any learned model you like.
> Do not retrieve the gold annotations from an external source, do not key on ids, and do not outsource the
> labelling.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Disfluency Reparandum-Repair Structure Recovery From Speech
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77p9m0g274esbv9aqh3g8cax89rnf5
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio, Based on dataset:, AMI Meeting Corpus Disfluency Source Subset, Download Data
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each row contains a short 16 kHz mono WAV clip from a licensed public meeting-speech corpus and a JSON token transcript with implicit 0-based token indices. The words are already transcribed; the task is not to recover missing words, choose among minimal-pair candidates, or run full ASR. For every test row, predict five outputs: the abandoned token span, the filler/edit span, the repair onset token, a 0/1 disfluency flag, and a calibrated confidence.
> In this challenge, reparandum means the words the speaker started and then abandoned. interregnum means filler or edit material between the abandoned phrase and the correction, such as uh or I mean. repair_onset is the first token of the corrected phrase. Rows can also be non-disfluent foils, such as ordinary emphasis, filler without a repair, or clean speech.
> The audio comes from real multi-speaker meeting recordings with headset-mix audio and aligned transcript/disfluency annotation sources. This setting mirrors practical caption cleanup, meeting-assistant transcription, and speech-interface post-processing, where a model must use transcript context plus acoustic cues such as timing, cutoff, hesitation, and prosody.
> What not to use: hosted or commercial speech/language APIs, external ASR or disfluency APIs, external labeled disfluency corpora, source lookup of original meeting clips or annotations, transcript-only/rule-only shortcuts, filename/timestamp/speaker-id leakage, row-order side channels, hardcoded answer maps, manual test labeling, and grader/filesystem exploitation are prohibited. The intended route is to fine-tune or train an open speech/audio-text model with span heads using the public training examples.
> This benchmark is distinct from accent-robust word recovery. Here the transcript words are already visible, and the model must decide which visible tokens belong to the abandoned phrase, filler/edit term, and repair onset.
> Task Specification
> reparandum_span is the abandoned token span as [start,end], inclusive, or NONE when there is no structured self-repair. interregnum_span is the filler or edit material between reparandum and repair, also inclusive, or NONE. repair_onset is the token index where the fluent repair starts, written as an integer string, or NONE. is_disfluency is 1 for a structured self-repair target and 0 for no structured repair target, including emphasis, filler-only, and clean-speech foils. confidence is a float in [0,1] calibrated to the row-level structural correctness of the prediction.
> The training labels are benchmark labels aligned to real meeting speech and real transcript timing. They are not a clinical stuttering diagnosis and should not be interpreted as human-gold discourse analysis beyond the stated span-recovery contract.
> Dataset
> The public dataset contains train.csv, test.csv, sample_submission.csv, and WAV clips under train/audio/ and test/audio/. Audio paths in the CSVs are relative to the public/ directory. Public test rows do not expose original meeting ids, speaker ids, raw timestamps, source word ids, annotation ids, split groups, repair types, or hidden subgroup names.
> Public Files
> Item	Description
> train.csv	labeled rows
> test.csv	hidden-label rows
> sample_submission.csv	valid template
> train/audio/	train WAV clips
> test/audio/	test WAV clips
> train.csv has 439 rows in this prepared split, and test.csv has 261 rows. The WAV clips are short context windows around real spontaneous-speech candidates.
> train.csv Columns
> Column	Type	Description
> id	int	opaque row id
> audio_path	string	relative WAV path
> token_transcript	JSON string	token list
> token_timing_json	JSON string	token times
> reparandum_span	string	[start,end] or NONE
> interregnum_span	string	[start,end] or NONE
> repair_onset	string	index or NONE
> is_disfluency	int	0 or 1
> confidence	float	gold confidence
> The token_transcript value is a compact JSON list of normalized tokens. The token_timing_json value gives token start and end offsets in milliseconds relative to the clip, but it does not expose source timestamps or annotation ids.
> The train-only label columns are reparandum_span, interregnum_span, repair_onset, is_disfluency, and confidence; these are withheld from test.csv.
> Example token_transcript: ["move","the","red","uh","move","the","blue","box","left"].
> Example token_timing_json: [{"token":"move","start_ms":180,"end_ms":430},{"token":"the","start_ms":440,"end_ms":540},{"token":"red","start_ms":550,"end_ms":820}].
> test.csv Columns
> Column	Type	Description
> id	int	opaque row id
> audio_path	string	relative WAV path
> token_transcript	JSON string	token list
> token_timing_json	JSON string	token times
> The test file has the same public input fields as the training file and withholds all target columns.
> In prose, test.csv contains id, audio_path, token_transcript, and token_timing_json. It does not contain labels, source meeting identifiers, source speaker identifiers, raw timestamps, repair-type groups, or annotation ids.
> Submission Format
> Column	Type	Constraint
> id	int	exact test id
> reparandum_span	string	[start,end] or NONE
> interregnum_span	string	[start,end] or NONE
> repair_onset	string	index or NONE
> is_disfluency	int	0 or 1
> confidence	float	0 to 1
> Submit exactly one row for every test id, with the columns in the exact order shown above.
> In prose, sample_submission.csv contains id, reparandum_span, interregnum_span, repair_onset, is_disfluency, and confidence, and the final submission must use the same columns in the same order.
> Example submission rows:
> id	reparandum_span	interregnum_span	repair_onset	is_disfluency	confidence
> 100000	NONE	NONE	NONE	0	0.6
> 100005	NONE	NONE	NONE	0	0.6
> 100014	NONE	NONE	NONE	0	0.6
> Evaluation
> Invalid submissions score 0.0. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from test.csv; invalid is_disfluency; non-finite or out-of-range confidence; impossible or out-of-range parsed spans; and impossible or out-of-range parsed repair-onset indices. A malformed row-local span string such as [oops] zeros that span head for that row without crashing the grader.
> For each row, S_reparandum is inclusive token-span IoU, with NONE vs NONE equal to 1 and one NONE equal to 0. S_interregnum uses the same IoU and NONE handling. S_onset is 1 for exact repair-onset match and 0 otherwise, with NONE vs NONE equal to 1. S_isdisf is exact is_disfluency correctness. If the gold row is a true repair but the submission predicts is_disfluency=0, then S_reparandum, S_interregnum, and S_onset are set to 0 for that row so an all-NONE prediction cannot receive accidental structure credit. S_joint is 1 only when S_reparandum, S_interregnum, S_onset, and S_isdisf are all exactly 1; otherwise it is 0. S_calib = max(0, 1 - abs(confidence - mean(S_reparandum, S_interregnum, S_onset, S_isdisf))).
> The row score is 0.70*S_joint + 0.10*S_reparandum^2 + 0.05*S_interregnum^2 + 0.03*S_onset^2 + 0.07*S_isdisf^2 + 0.05*S_calib^2.
> The final score is 0.45*mean(row_score) + 0.15*worst_mean_by_hidden_source_group + 0.25*worst_mean_by_hidden_repair_group + 0.15*mean_true_repair_row_score. Hidden source groups are coarse recording/source-family buckets such as meeting-family groups; they are used only to ensure the model works across different meeting sources. Hidden repair groups are coarse target-type buckets such as structured repairs and non-repair foils; they are used only to ensure the model does not perform well on one repair type while failing another. mean_true_repair_row_score is the mean row score over gold rows with is_disfluency=1, included so a trivial all-NONE submission is weak. These group labels are not included in public test rows because they would leak target information, but the grouping axes are described here so the robustness term is clear. The theoretical minimum is 0.0, the theoretical maximum is 1.0, and higher is better.
> Intended Solution
> Strong solutions should fine-tune or train open speech/audio-text models such as wav2vec2, HuBERT, Whisper-family encoders, conformer encoders, or multimodal speech-text models, with a token-level text encoder and span/onset heads. Useful models should learn acoustic timing, prosody, cutoff, hesitation, and repetition cues together with the transcript; prompt-only and transcript-only approaches are not the intended solution.
> Enforcement On Invalid Approaches
> Submissions based on hosted commercial APIs, external labeled disfluency corpora, direct source lookup, recovered original meeting annotations, transcript-only rules, filename or timestamp leakage, hardcoded id-to-answer maps, or grader/filesystem exploitation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned speech/NLP modeling from the provided public training data.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Blind Room-Scale And Echo-Zone Inference From Reverberant Speech
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx720a2rg1kqramk1j7v190sjx89wckf
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio, Based on dataset:, ACE Reverberant Speech Room-Scale And Echo-Zone Profiles, Download Data
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given short mono WAV clips of speech that have passed through measured room impulse responses and measured room noise. The public clips also include mild deterministic speech-preserving perturbations so exact source-audio matching is not a valid shortcut. For each test clip, predict the room-scale bucket, reverberation bucket, source-microphone distance bucket, echo-zone category, and a confidence value.
> The public inputs are deliberately minimal: an opaque sample_id, a non-source-revealing audio_path, and a generic prompt. Room ids, source/microphone positions, RIR ids, speaker ids, utterance filenames, SNR, raw room dimensions, measured T60, and measured DRR are not public. The intended approach is to train or fine-tune an open audio model, speech encoder, or acoustic-feature model on the provided training clips and labels.
> What not to use: do not solve this as a T60/DRR-only benchmark, do not attempt to recover the upstream corpus rows or room ids, do not match audio fingerprints to public source files, and do not use filename/order/id shortcuts. The scoring rewards the full acoustic profile, calibrated uncertainty, and hidden subgroup robustness.
> Task Specification
> Predict exactly these columns for every test sample_id:
> room_volume_bucket: one of small, medium, large, very_large.
> rt60_bucket: one of dry, moderate, reverberant, very_reverberant.
> source_mic_distance_bucket: one of near, mid, far, unknown_or_uncertain.
> echo_zone: one of direct_dominant, balanced, reverberant_dominant, noisy_uncertain.
> confidence: a float in [0, 1] estimating the reliability of the submitted acoustic profile for that row.
> The labels are bucketed from measured acoustic metadata and deliberately include uncertainty around physically ambiguous boundaries. The prepared split ensures that every hidden test category has labeled training coverage, including the dry RT60 class. Do not overclaim exact room geometry: the target is room scale and echo-zone behavior useful to speech systems.
> Dataset
> The public dataset contains train.csv, test.csv, sample_submission.csv, and WAV clips under train/audio/ and test/audio/. Audio paths are relative to the public/ directory.
> Public Files
> Item	Description
> train.csv	labeled training clips
> test.csv	hidden-label test clips
> sample_submission.csv	dummy submission format
> train/audio/	train WAV clips
> test/audio/	test WAV clips
> train.csv includes the public inputs and all five labels. test.csv includes only public inputs. The sample submission is a weak train-prior style file for schema validation, not a competitive solution.
> train.csv Columns
> Column	Type	Description
> sample_id	string	opaque clip id
> audio_path	string	public WAV path
> prompt	string	generic task prompt
> room_volume_bucket	string	scale label
> rt60_bucket	string	reverb label
> source_mic_distance_bucket	string	distance label
> echo_zone	string	echo-zone label
> confidence	float	label reliability
> The training labels are bucketed acoustic-environment targets. Public paths and ids are salted and do not contain room, RIR, source, microphone, speaker, utterance, SNR, or noise identifiers.
> test.csv Columns
> Column	Type	Description
> sample_id	string	opaque clip id
> audio_path	string	public WAV path
> prompt	string	generic task prompt
> The test file has the same public input fields as the training file and withholds all targets.
> Submission Format
> Column	Type	Constraint
> sample_id	string	exact test id
> room_volume_bucket	string	allowed bucket
> rt60_bucket	string	allowed bucket
> source_mic_distance_bucket	string	allowed bucket
> echo_zone	string	allowed category
> confidence	float	0 to 1
> Submit exactly one row for every test id, with the columns in the exact order shown above.
> Example submission rows:
> sample_id	room_volume_bucket	rt60_bucket	source_mic_distance_bucket	echo_zone	confidence
> brs_03a91d4c2e1b	medium	reverberant	mid	balanced	0.71
> brs_8d3f09ac61aa	large	moderate	far	reverberant_dominant	0.64
> brs_f18c725a4320	small	dry	near	direct_dominant	0.82
> Evaluation
> Invalid submissions raise an error rather than receiving a valid numeric score. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from test.csv; invalid categorical values; non-finite confidence; and confidence outside [0, 1].
> For valid submissions, the grader computes macro-F1 over the hidden test classes represented in each categorical head:
> RoomF1 = macro_f1(room_volume_bucket)^2
> Rt60F1 = macro_f1(rt60_bucket)^2
> DistanceF1 = macro_f1(source_mic_distance_bucket)^2
> EchoF1 = macro_f1(echo_zone)^2
> ConfCal = mean(max(0, 1 - abs(pred_confidence - target_confidence) / 0.5))^2
> The normalized base profile uses the five head terms with relative weights 25/95, 25/95, 20/95, 15/95, and 10/95:
> BaseProfile = (25/95) * RoomF1 + (25/95) * Rt60F1 + (20/95) * DistanceF1 + (15/95) * EchoF1 + (10/95) * ConfCal.
> WorstHidden is the minimum BaseProfile over hidden room-scale, RT60, distance, noise-condition, speech-split, and mic/source-configuration groups.
> Final = 0.95 * BaseProfile(all rows) + 0.05 * WorstHidden.
> The top-level weights are intentionally 0.95 for overall acoustic-profile quality and 0.05 for worst hidden-subgroup robustness, so they sum to 1.0.
> The theoretical minimum is 0.0; the theoretical maximum is 1.0; higher is better. A perfect submission with all hidden labels and target confidence values scores exactly 1.0.
> Intended Solution
> Strong solutions should train or fine-tune open audio/speech models such as wav2vec2/HuBERT-style encoders, Whisper-family encoders used as feature extractors, conformers, audio spectrogram CNNs, or calibrated gradient-boosted models over acoustic features. Useful evidence includes decay-envelope behavior, direct-to-reverberant balance, late-tail coloration, speech/noise masking, spectral tilt, and how those cues interact across labels.
> Prompt-only systems, transcript-only approaches, and T60-only estimators are not expected to solve the full multi-head profile. The training set teaches the bucket definitions and uncertainty conventions.
> Enforcement On Invalid Approaches
> Submissions based on public-source row lookup, recovered upstream room/RIR/speech identifiers, external labeled room-acoustics answer tables, audio fingerprint matching against the official source archives, hosted commercial speech APIs, manual labeling of hidden test rows, hardcoded id-to-answer maps, or rule-only T60/DRR estimation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned blind acoustic-environment inference from the provided public training split.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Cross-Lingual Clinical Span Anchoring
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71qwtej7kpxf9vv59f6bhxhd89r7yc
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Clinical concept extraction systems often need to keep disease, symptom, and procedure mentions aligned when a case note is carried across languages. Small boundary or alignment mistakes can change what gets counted in downstream clinical analytics, especially for low-resource languages where direct supervision is limited.
> In this challenge, each row gives a redacted Spanish clinical context with one marked concept and a comparable redacted target-language clinical context. Four redacted candidate spans are shown from the target-language context. Your task is to select the candidate span that aligns to the marked Spanish concept.
> This is a multilingual fine-tuning task rather than a generic text classification exercise. The redaction preserves morpheme shape, punctuation, numbers, and local context while hiding exact source strings. Strong solutions should learn cross-lingual clinical terminology, local context cues, entity-type constraints, and language-specific morphology across Czech, Dutch, English, Italian, Romanian, and Swedish.
> Dataset
> File descriptions
> train.csv -- 8,289 labeled examples with Spanish anchor contexts, target-language contexts, four candidate spans, and the correct selected_option.
> test.csv -- 5,574 unlabeled examples with the same input columns as train.csv, but without selected_option.
> train.jsonl -- JSONL mirror of the training examples for instruction/fine-tuning workflows.
> test.jsonl -- JSONL mirror of the test prompts for instruction/fine-tuning workflows.
> sample_submission.csv -- A template with id and randomized selected_option values.
> Column descriptions
> id (string) -- Unique 12-character hashed identifier for each example.
> target_language (string) -- Target-language code: cz, en, it, nl, ro, or sv.
> entity_type (string) -- Clinical concept type: disease, symptom, or procedure.
> source_context (string) -- Redacted Spanish clinical context. The source concept is marked with [[ANCHOR]] and [[/ANCHOR]].
> target_context (string) -- Redacted target-language clinical context containing the candidate spans.
> candidate_a (string) -- Redacted candidate target-language span for option A.
> candidate_b (string) -- Redacted candidate target-language span for option B.
> candidate_c (string) -- Redacted candidate target-language span for option C.
> candidate_d (string) -- Redacted candidate target-language span for option D.
> selected_option (string) -- Correct option letter in A, B, C, or D (train only).
> Evaluation
> Submissions are scored using balanced macro accuracy. Accuracy is computed separately for each (target_language, entity_type) group, then averaged across groups so that high-resource language/entity combinations cannot dominate the score.
> def evaluate(rows):
> group_scores = []
> for (target_language, entity_type), group in rows.groupby(["target_language", "entity_type"]):
> group_scores.append((group["prediction"] == group["selected_option"]).mean())
> return sum(group_scores) / len(group_scores)
> Higher is better. The score range is 0 to 1.
> Submission
> Submit a CSV file with one row for every row in test.csv.
> id (string) -- The 12-character identifier from test.csv.
> selected_option (string) -- One of A, B, C, or D.
> Example:
> id,selected_option
> a80a7c75ef0f,B
> 0db8b46104cb,B
> 479c797d8eb3,C
> Requirements
> The file must contain exactly 5,574 rows plus the header.
> Every id from test.csv must appear exactly once.
> selected_option must contain only A, B, C, or D.
> File format must be .csv with exact columns id,selected_option.
> What Not To Use
> Do not use outside copies of these clinical cases or their labeled span files to recover held-out answers. The challenge is meant to test alignment from the redacted public examples, not lookup.
> Do not reverse-map hashed IDs, row order, redacted text, or full note text against external mirrors of the corpus.
> Do not hard-code answer tables or template mappings from external clinical-span resources.
> Do not submit a purely rule-based decoder that ignores the target-language context and only exploits option-position priors.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Adaptive Enzyme-Mechanism Falsification
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ct1rwqmyfc7pvdpfysszc5s89x95b
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is a local LLM fine-tuning challenge for biochemical
> sequence-to-program reasoning.
> When several enzyme mechanisms explain the same overall chemistry, the useful
> question is not simply “which paragraph sounds most plausible?” A mechanistic
> model should identify an experiment whose result separates the hypotheses,
> then choose the next experiment conditionally on what was observed. That
> requires understanding elementary catalytic events, predicting
> counterfactual assay responses, and compiling those predictions into an
> efficient adaptive plan.
> Each row provides four to eight candidate mechanism programs and a catalogue
> of qualitative assays. Mechanisms are represented as ordered elementary-event
> cards grounded in M-CSA and EzMechanism annotations. Depending on the evidence
> profile, some normalized electron-flow summaries are withheld, so a solver
> must also use the curated mechanistic note. The target is an executable JSON
> decision tree that uniquely identifies every candidate mechanism while
> minimizing expected assay cost.
> The public training split supplies both the qualitative assay-outcome matrix
> and an exact minimum-cost plan. The hidden split supplies only the mechanism
> dossier and assay catalogue. Strong solutions should fine-tune a local
> open-weight encoder-decoder or decoder model to infer counterfactual outcomes
> and generate a plan, ideally combined with constrained decoding or an exact
> decision-tree search over model-predicted outcomes.
> This is not ordinary classification. There is no single correct class per
> query, and the grader does not compare your JSON to one reference string.
> Instead, it privately executes your tree once under every candidate mechanism.
> Any valid tree that reaches the correct leaf is accepted functionally.
> Existing enzyme benchmarks usually predict a function, catalytic residue,
> substrate, kinetic value, final product, or mechanism path. This challenge
> starts after multiple stepwise mechanisms already exist and asks for an
> adaptive falsification program.
> The examples are newly constructed from curated elementary chemistry:
> step order, direction, role, and transplant edits create source-new
> mechanism forks;
> assay responses are derived from the resulting hidden event programs;
> exact optimal trees are computed by dynamic programming;
> no test response matrix or target plan exists in M-CSA or EzMechanism; and
> train/test construction is disjoint by source mechanism and by a combined
> EC-sub-subclass/CATH-topology family key.
> Dataset
> Prepared public files:
> dataset/public/
> ├── train.jsonl
> ├── test.jsonl
> └── sample_submission.csv
> Private grading data:
> dataset/private/
> └── answers.csv
> Scale
> | Split | Queries | Source mechanisms | EC/CATH family groups |
> |---|---:|---:|---:|
> | train | 6,555 | 339 | 201 |
> | test | 2,549 | 132 | 85 |
> There is no source-mechanism or family-group overlap between train and test.
> The hidden set contains 1,697 coupled-edit queries. This hard subset is large
> enough to support stable solver ranking.
> Evidence Profiles
> evidence_profile has one of three values:
> full_ledger — every event includes a normalized electron-flow summary;
> mixed_evidence — some event summaries are withheld; or
> curated_note_only — all normalized event summaries are withheld.
> The public text is identifier-scrubbed. M-CSA IDs, UniProt accessions, PDB IDs,
> EC codes, CATH codes, source residue numbers, family keys, construction edits,
> and normalized private probe semantics are not released to solvers.
> ### JSONL Fields Shared by Train and Test
> Field	Type	Description
> id	string	Unique 16-character query identifier.
> evidence_profile	string	Evidence-availability stratum.
> mechanism_hypotheses	array	Four to eight candidate mechanism programs.
> mechanism_hypotheses[].hypothesis	string	Query-local identifier: H0, H1, and so on.
> mechanism_hypotheses[].mechanism_steps	array	Ordered elementary-event cards.
> mechanism_steps[].step	integer	One-based step position.
> mechanism_steps[].event_token	string	Opaque query-scoped event identifier.
> mechanism_steps[].curated_note	string	Anonymized mechanistic evidence.
> mechanism_steps[].electron_flow_summary	string	Normalized event delta or [withheld].
> available_assays	array	Assays allowed in the submitted plan.
> available_assays[].probe	string	Query-local assay ID such as P03.
> available_assays[].assay	string	Qualitative intervention description.
> available_assays[].cost	float	Relative cost paid whenever the assay is executed.
> available_assays[].possible_outcomes	array	Valid branch labels for that assay in this query.
> ### Training-Only Fields
> Field	Type	Description
> outcome_supervision	array	Complete observed outcome for every hypothesis-assay pair.
> optimal_plan	object	Canonical exact minimum-expected-cost decision tree.
> `outcome_supervision` is auxiliary fine-tuning supervision. A competitive
> pipeline can first adapt a model to predict assay outcomes from a hypothesis
> and then run constrained plan search. Direct plan generation is also allowed.
> ### Example Dossier Fragment
> { "hypothesis": "H2", "mechanism_steps": [ { "step": 1, "event_token": "E_f91c2bc8", "curated_note": "actor_A removes a proton from actor_B, activating a nucleophile-driven bond formation.", "electron_flow_summary": "forms C-S and H-N; breaks H-S; redistributes charge on N and O; electron path has 3 arrows" } ] }
> ## Required Plan Grammar
> Each submitted `plan` is one JSON object serialized inside a CSV cell.
> A leaf guesses one hypothesis:
> {"guess":"H2"}
> An internal node executes one public assay and branches on observed outcomes:
> { "probe": "P03", "branches": { "ABSENT": {"guess": "H1"}, "EARLY": {"guess": "H4"}, "LATE": { "probe": "P07", "branches": { "NO_SHIFT": {"guess": "H0"}, "DISTRIBUTED": {"guess": "H3"} } } } }
> Plan rules:
> - A leaf must have exactly one key: `guess`.
> - An internal node must have exactly two keys: `probe` and `branches`.
> - Every hypothesis ID, probe ID, and branch outcome must be valid for that row.
> - A probe may not be repeated on the same root-to-leaf path.
> - A tree may have at most 31 nodes and depth at most 8.
> - A plan cell may contain at most 20,000 UTF-8 bytes.
> - You may omit an outcome branch, but a hidden mechanism that reaches the
> missing branch is unresolved and receives no identification credit.
> - You do not need to reproduce the public canonical training plan. Functional
> alternatives are valid.
> ## Evaluation
> Submissions are scored by executing each plan against the private qualitative
> assay outcomes.
> For one query:
> - `R_q` is the fraction of candidate mechanisms that reach their own correct
> hypothesis leaf.
> - `C_q` is the mean accumulated assay cost across all candidate mechanisms.
> - `C_opt_q` is the exact minimum mean cost of a fully resolving tree.
> - If the plan executes at least one assay:
> E_q = R_q * min(1, C_opt_q / C_q)
> - If the plan executes no assay, `E_q = 0`.
> Dataset-level terms:
> overall_resolution = mean(R_q over every hidden query)
> cost_efficiency = mean(E_q over every hidden query)
> hard_resolution = mean( R_q over hidden coupled-edit queries )
> Final score:
> score = 0.55 * overall_resolution + 0.20 * cost_efficiency + 0.25 * hard_resolution
> Higher is better. The score lies between 0 and 1.
> The hard term prevents a model from scoring well only on adjacent single-step
> swaps. Cost receives less weight than correct discrimination: a cheap tree
> that cannot resolve mechanisms should not beat a more informative plan.
> Malformed plan JSON, invalid node grammar, invalid query-local identifiers,
> excessive depth, or excessive node count gives zero for that query. File-level
> errors such as missing IDs, duplicate IDs, missing plans, extra columns, or an
> incorrect row set reject the submission.
> ## Submission
> Write:
> ./working/submission.csv
> The CSV must have exactly these columns in this order:
> Column	Type	Description
> id	string	Query ID copied from test.jsonl.
> plan	string	Serialized JSON decision tree.
> Example:
> id,plan 02f0b7c93804af11,"{""guess"":""H0""}" 06b18adc42bb7da3,"{""probe"":""P01"",""branches"":{""ABSENT"":{""guess"":""H2""},""EARLY"":{""guess"":""H0""}}}"
> Requirements:
> - exactly 2,549 rows;
> - every test ID exactly once;
> - no missing `id` or `plan`;
> - exact column names and order `id,plan`;
> - UTF-8 CSV; and
> - `.csv` only.
> When writing JSON with pandas, use `json.dumps` for each plan and let
> `DataFrame.to_csv` perform CSV escaping:
> import json import pandas as pd
> submission = pd.DataFrame({ "id": test_ids, "plan": [json.dumps(plan, separators=(",", ":")) for plan in plans], }) submission.to_csv("./working/submission.csv", index=False)
> ## Modeling Guidance
> A strong solution will usually separate learning from constrained search:
> 1. serialize one hypothesis-assay pair or a full query dossier;
> 2. fine-tune a chemistry-capable local encoder-decoder or decoder model on
> `outcome_supervision`;
> 3. calibrate predicted qualitative outcomes;
> 4. build a response table for the hidden query;
> 5. solve or approximately solve the cost-sensitive decision-tree problem; and
> 6. serialize the tree with grammar-constrained decoding and validation.
> Useful improvements may include:
> - multi-task loss for outcome prediction and direct plan generation;
> - hard-negative training across same-element bond changes;
> - evidence-profile-aware masking;
> - family-balanced batches;
> - constrained beam search over query-local probe and hypothesis tokens;
> - uncertainty-aware robust tree search; and
> - self-consistency checks that execute generated trees against the model's own
> predicted response matrix.
> All solution notebooks must:
> - run end-to-end without manual intervention;
> - read only from `./dataset/public/`;
> - write outputs only under `./working/`;
> - use libraries available in the Kaggle Python Docker image;
> - complete within 30-60 minutes on 64 GB RAM and one NVIDIA A10G; and
> - use local model weights available in the execution environment.
> ## What Not To Use
> - Do not use zero-shot or few-shot prompting as the main solver. The intended
> capability is adaptation from the released supervision.
> - Do not recover source enzyme identities, M-CSA entries, UniProt accessions,
> PDB structures, EC/CATH groups, or construction edits through external
> matching.
> - Do not key plans to test IDs, row order, event-token hashes, or hidden
> release salts.
> - Do not manually label test dossiers.
> - Do not assume one public optimal tree is the only valid answer.
> &nbsp;

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## User Emotion Shift And Escalation Prediction From Paired Speech Clips
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71vbsndfm7b070e9fhf52gtn89v74c
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio, Based on dataset:, CREMA-D Official AudioWAV Speech Clips And Metadata, Download Data
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Objective: for each baseline/current speech pair, listen to both clips and predict the current expressed affect, the direction of valence change, the direction of arousal change, the escalation tier, and a confidence for that complete row-level decision.
> The audio is real English speech from multiple human actors recorded in controlled prompted-utterance sessions. Each public example is presented as a pair of short mono WAV clips with opaque paths and source-neutral channel rendering; original speaker ids, utterance ids, file names, sentence ids, source labels, and demographic fields are not public.
> Each row contains two clips from the same speaker: a baseline/reference clip and a current/later clip. Pairs are built to cover stable, escalating, recovering, and cross-affect cases, so the model must compare the baseline and current prosody rather than classify a single clip in isolation. The split is speaker-held-out: no speaker appears in both public train and hidden test.
> This setup is different from broad relative voice-impression scoring, where the goal is usually to rank which of two clips sounds more like a single attribute. It is also different from utterance-level escalation or intensity labeling, where one clip is classified in isolation or placed on a call trajectory. Here the baseline is a within-speaker reference point, and the submission must produce one complete monitoring decision: current expressed affect, valence direction, arousal direction, escalation tier, and confidence for the same row. A solution that only recognizes the current clip's affect, only estimates intensity, or only ranks "which clip sounds higher" leaves important parts of the target unresolved.
> The central modeling problem is baseline-calibrated change detection with a consistency-constrained output bundle. The grader mainly rewards rows where all four categorical decisions are correct together, so a model must connect the baseline/current comparison to the final operational action instead of solving separate single-purpose subtasks.
> For every test row, predict the current expressed affect category, whether valence shifted relative to the baseline, whether arousal shifted relative to the baseline, whether operational escalation is required, and an honest confidence. This is not a single-clip speech-emotion-recognition task: the required judgment is paired and relative, with a current-state label plus shift and escalation heads.
> What not to use: hosted commercial speech or language APIs, external labeled emotion or speech-affect datasets, source-corpus lookup, audio fingerprint matching against public corpora, original filename reconstruction, speaker-id reconstruction, row-order/id tricks, manual test labeling, and hardcoded answer maps are prohibited. The intended route is to train or fine-tune an open speech, audio-text, or multimodal model on the public training pairs.
> Task Specification
> affect_label is the perceived current-clip expressed affect category and must be one of angry, sad, happy, neutral_or_unclear, or other_negative. other_negative covers negative affect that is not cleanly anger or sadness in this schema.
> valence_shift compares the current clip against the baseline clip and must be positive, negative, or no_clear_shift. arousal_shift compares the current clip against the baseline clip and must be higher, lower, or no_clear_shift. escalation_tier must be none, monitor, or urgent, reflecting the practical voice-agent decision from the paired speech evidence. confidence is a finite float in [0, 1] calibrated to the complete row-level prediction.
> Dataset
> The public dataset contains train.csv, test.csv, sample_submission.csv, and WAV clips under train/audio/ and test/audio/. Audio paths are relative to the public directory. Training rows include labels; test rows include only public inputs. id and sample_id are both opaque row identifiers and have the same value; both are included to satisfy platform row-id conventions and the pair-oriented task schema.
> Exact train.csv columns are id, sample_id, baseline_audio, current_audio, pair_duration_bucket, affect_label, valence_shift, arousal_shift, escalation_tier, and confidence.
> Exact test.csv columns are id, sample_id, baseline_audio, current_audio, and pair_duration_bucket.
> pair_duration_bucket can be short_pair, medium_pair, or long_pair. It is based only on the combined duration of the baseline and current clips: short_pair is under 4.5 seconds, medium_pair is 4.5 to under 7.6 seconds, and long_pair is 7.6 seconds or longer.
> Public Files
> Item	Description
> train.csv	labeled pair rows
> test.csv	hidden-label pairs
> sample_submission.csv	dummy format file
> train/audio/	train WAV clips
> test/audio/	test WAV clips
> The same public clip may appear in more than one pair within a split, but no speaker or source clip crosses between train and test. Public filenames are opaque and do not contain source labels.
> train.csv Columns
> Column	Type	Description
> id	int	opaque row id
> sample_id	int	opaque pair id
> baseline_audio	string	baseline WAV path
> current_audio	string	current WAV path
> pair_duration_bucket	string	coarse duration bin
> affect_label	string	current affect
> valence_shift	string	valence change
> arousal_shift	string	arousal change
> escalation_tier	string	action tier
> confidence	float	gold confidence
> The training labels use the allowed values listed in the task specification. pair_duration_bucket is a coarse public descriptor with values short_pair, medium_pair, or long_pair; it is not sufficient to solve the task without the paired speech clips.
> test.csv Columns
> Column	Type	Description
> id	int	opaque row id
> sample_id	int	opaque pair id
> baseline_audio	string	baseline WAV path
> current_audio	string	current WAV path
> pair_duration_bucket	string	coarse duration bin
> The test file withholds all labels. The id and sample_id columns identify the row, baseline_audio points to the earlier reference clip, current_audio points to the later/current clip, and pair_duration_bucket gives only a coarse duration bin with values short_pair, medium_pair, or long_pair.
> Submission Format
> Column	Type	Constraint
> id	int	exact test id
> sample_id	int	exact test id
> affect_label	string	allowed affect
> valence_shift	string	allowed shift
> arousal_shift	string	allowed shift
> escalation_tier	string	allowed tier
> confidence	float	0 to 1
> Submit exactly one row for every test id and sample_id, with columns in the exact order shown above. In each row id and sample_id must match. Missing, extra, or reordered columns make the submission structurally invalid.
> id,sample_id,affect_label,valence_shift,arousal_shift,escalation_tier,confidence
> 102341,102341,angry,negative,higher,urgent,0.77
> 487221,487221,neutral_or_unclear,no_clear_shift,lower,none,0.61
> 750812,750812,sad,negative,no_clear_shift,monitor,0.58
> The example rows are illustrative schema examples, not answer hints. In the first example, the submission says that the current clip sounds angry relative to the baseline, with a negative valence shift, higher arousal, and urgent escalation; 0.77 is the participant's self-estimated confidence in that complete row prediction.
> Evaluation
> The official metric is PairedDecisionScore, a 0-to-1 composite score for paired speech monitoring. Its weights are fixed up front: 75% strict full-row exactness, 10% per-head macro-F1 bundle, and 15% confidence calibration. In plain terms, most of the score comes from making the whole row correct: the current affect label, both shift directions, and the escalation tier should agree with each other for the same baseline/current pair. A perfect submission scores 1.0; the theoretical minimum for a valid scored submission is 0.0; the provided dummy/sample-style weak baseline is expected to score around 0.14 on this split.
> Malformed submissions raise a validation error and are not scored. Invalidity includes missing, extra, or reordered columns; duplicate ids; mismatched id and sample_id; an id set different from test.csv; non-finite, missing, or out-of-range confidence; missing rows; and categorical values outside the allowed label sets. Valid submissions with wrong but well-formed labels are scored normally.
> For valid submissions, the grader computes three transparent terms: a normalized categorical head bundle, a strict full-row exactness term, and a calibration term. Let F1_affect, F1_valence, F1_arousal, and F1_escalation be macro-F1 scores over the allowed classes for their respective heads. Define CategoricalBundle = (0.18 * F1_affect + 0.17 * F1_valence + 0.16 * F1_arousal + 0.14 * F1_escalation) / 0.65. The 0.65 divisor is the sum of the four head weights and normalizes the bundle into [0, 1].
> For row i, define exact-match indicators A_i, V_i, R_i, and E_i, each equal to 1 when the submitted affect_label, valence_shift, arousal_shift, or escalation_tier matches the hidden answer, and 0 otherwise. The row correctness used for calibration is row_correctness_i = (0.18 * A_i + 0.17 * V_i + 0.16 * R_i + 0.14 * E_i) / 0.65. Calibration is mean_i(max(0, 1 - abs(confidence_i - row_correctness_i))).
> Define J_i = A_i * V_i * R_i * E_i, so J_i is 1 only when all four categorical heads are correct for the same row. StrictRowScore = (mean_i J_i)^5; the fifth power intentionally punishes submissions that get many individual heads right but do not recover complete paired decisions.
> Final score is PairedDecisionScore = 0.10 * CategoricalBundle + 0.75 * StrictRowScore + 0.15 * Calibration. These three final-score weights sum to 1.00. The theoretical minimum for a valid scored submission is 0.0; the theoretical maximum is 1.0; higher is better. A perfect submission with confidence 1.0 scores exactly 1.0.
> Intended Solution
> Strong solutions should train or fine-tune open-weight speech or audio-text models such as wav2vec2/HuBERT-style encoders, Whisper-family encoders, conformers, or multimodal speech encoders on the provided paired examples. A good model should compare baseline and current prosody, energy, pitch contour, tempo, and voice quality rather than treating each current clip as an isolated emotion tag.
> Enforcement On Invalid Approaches
> Submissions based on hosted commercial APIs, external labeled speech-affect corpora, direct source lookup, audio fingerprint matching, recovered source filenames, manual hidden-test labeling, hardcoded id-to-answer maps, or rule-only use of public metadata may be rejected before payout even if the CSV is structurally valid. The competition rewards learned paired speech modeling from the provided public training data.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.

## Killer Whale Conservation Bioacoustic Profiling From Hydrophone Audio
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72tjs317h2sk1fv35c7a9v5x895v2b
- DOMAIN exactly as displayed: Fine-Tuning
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Problem Description
> Marine conservation teams, field scientists, and monitoring systems often need to decide whether a short underwater recording should trigger a killer whale follow-up alert: is there likely killer whale or orca activity, is it sparse or dense, are other biological sounds dominating, and how reliable is the clip for conservation response? This is an audio and bioacoustics challenge: build a multi-head encounter profile from short hydrophone clips. It is not a plain call/no-call detector and it is not an ecotype-only recognizer.
> Overview
> You are given short mono WAV clips prepared from real underwater hydrophone recordings. The raw recordings come from an official public marine-bioacoustic archive of Northeast Pacific coastal and island hydrophone monitoring, collected by multiple field recording programs in habitats where killer whales and other biological sounds occur. The original source files vary by hydrophone site, recording date, sample rate, channel layout, ambient noise, vessel noise, and biological confounders. Prepared challenge clips are short source-redacted windows rendered as mono WAV audio; raw filenames, exact timestamps, provider names, locations, annotation ids, and frequency metadata are not public.
> For each hidden test clip, produce a killer whale/orca encounter profile: presence, activity density, broad ecotype/context, confounder type, call-band bucket, and calibrated confidence. The public inputs are intentionally minimal: an opaque id, a non-source-revealing audio_path, a coarse clip_duration_bucket, and a generic prompt.
> What not to use: do not attempt to recover upstream recording filenames, timestamps, locations, providers, annotation rows, or raw source paths; do not use audio fingerprint lookup against public archives; do not use filename/order/id side channels; do not submit a binary detector as if it solved the full triage task. Strong solutions should learn from the provided public training audio and labels, using acoustic evidence such as call density, spectral band, confounders, and uncertainty.
> Task Specification
> Submit exactly these values for every test id: orca_presence, encounter_activity, ecotype_context, confounder_type, call_band_bucket, and confidence. The allowed values are listed in the submission table below. The task rewards the whole acoustic profile, not only whether an orca is present.
> Dataset
> The public dataset contains labeled training clips, hidden-label test clips, and a sample submission. Audio paths are relative to the public/ directory. The audio comes from fixed underwater hydrophone recordings made in real coastal monitoring conditions, including quiet background periods, killer whale calls, other biological calls, and mixed or weak evidence. Clips were extracted around annotated sound windows and nearby background/confounder windows, then converted to a consistent short mono WAV format for modeling.
> Public Files
> Item	Description
> train.csv	labeled clips
> test.csv	hidden-label clips
> sample_submission.csv	schema example
> train/audio/	train WAV clips
> test/audio/	test WAV clips
> train.csv includes the public inputs and all target columns. test.csv includes only public inputs. Public ids and paths are opaque and do not encode recording names, timestamps, providers, locations, source annotation ids, raw paths, or frequency labels.
> train.csv Columns
> Column	Type	Description
> id	string	opaque clip id
> audio_path	string	WAV path
> clip_duration_bucket	string	coarse duration
> prompt	string	generic prompt
> orca_presence	string	presence label
> encounter_activity	string	activity label
> ecotype_context	string	context label
> confounder_type	string	confounder label
> call_band_bucket	string	band label
> confidence	float	label reliability
> orca_presence is one of yes, no, or uncertain. encounter_activity is one of quiet_background, single_call, multiple_calls, dense_calling, or confuser_dominant. ecotype_context is one of SRKW, TKW, NRKW, OKW, or not_orca_or_unknown. confounder_type is one of humpback_or_other_bio, ambient_background, unidentified_bio, mixed_or_uncertain, or none. call_band_bucket is one of low_band, mid_band, high_band, broad_band, or no_call. confidence is a float in [0, 1].
> test.csv Columns
> Column	Type	Description
> id	string	opaque clip id
> audio_path	string	WAV path
> clip_duration_bucket	string	coarse duration
> prompt	string	generic prompt
> The test file withholds all target columns. Use the audio clip and the public training labels to infer the hidden triage profile.
> Submission Format
> Column	Type	Constraint
> id	string	exact test id
> orca_presence	string	allowed value
> encounter_activity	string	allowed value
> ecotype_context	string	allowed value
> confounder_type	string	allowed value
> call_band_bucket	string	allowed value
> confidence	float	0 to 1
> Submit exactly one row for every test id, with columns in the exact order shown above.
> Example submission rows:
> id,orca_presence,encounter_activity,ecotype_context,confounder_type,call_band_bucket,confidence
> oet_04cce1b2a9935b,yes,multiple_calls,SRKW,none,mid_band,0.82
> oet_7a299f0b651923,no,confuser_dominant,not_orca_or_unknown,humpback_or_other_bio,no_call,0.61
> oet_f6ed99a26b7a81,uncertain,single_call,OKW,mixed_or_uncertain,high_band,0.54
> Evaluation
> Invalid submissions raise an error rather than receiving a valid numeric score. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from test.csv; invalid categorical values; non-numeric confidence; non-finite confidence; and confidence outside [0, 1].
> For valid submissions, the grader computes FinalScore from six component scores and one hidden robustness term. All formulas below use only rows in the hidden test set.
> For each discrete output head h, the grader first computes macro-F1 over the answer classes that appear in that hidden set. For each class c, Precision_c = TP_c / (TP_c + FP_c), Recall_c = TP_c / (TP_c + FN_c), and F1_c = 2*Precision_c*Recall_c / (Precision_c + Recall_c), with F1_c = 0 when there are no true positives. Then MacroF1_h is the mean of F1_c across classes, and HeadScore_h = MacroF1_h^2.
> For the confidence column, each row receives ConfRow_i = max(0, 1 - abs(pred_confidence_i - true_confidence_i) / 0.5). The confidence component is ConfidenceScore = mean(ConfRow_i)^2.
> The normalized base profile is:
> BaseProfile = (8/49)*OrcaPresenceScore + (11/49)*EncounterActivityScore + (9/49)*EcotypeContextScore + (8/49)*ConfounderTypeScore + (8/49)*CallBandBucketScore + (5/49)*ConfidenceScore
> These six normalized weights sum exactly to 1.0.
> The hidden robustness axes are provider-family, ecotype/context group, activity group, confounder group, call-band group, and clip-quality group. For every hidden bucket on those axes, the grader recomputes BaseProfile on only that bucket's rows. WorstGroup = min(bucket BaseProfile).
> The final score is:
> FinalScore = 0.95*BaseProfile + 0.05*WorstGroup
> The two top-level weights sum to 1.0, and the final score is clipped to [0, 1].
> The theoretical minimum is 0.0; the theoretical maximum is 1.0; higher is better. A perfect submission with every hidden label and target confidence value exactly correct scores 1.0.
> Intended Solution
> Strong approaches should train or fine-tune audio models, spectrogram CNNs, open audio encoders, or calibrated classical models over learned and hand-built acoustic features. Useful evidence includes repeated call structure, call spacing, band-limited energy, broad-band events, non-orca biological confounders, ambient-only clips, and uncertainty from weak or mixed evidence.
> Enforcement On Invalid Approaches
> Submissions based on upstream-source row lookup, recovered recording names or timestamps, external answer tables, exact audio fingerprinting against public archives, hosted commercial audio-recognition APIs, manual labeling of hidden test rows, hardcoded id-to-answer maps, or binary detector-only systems may be rejected before payout even if the CSV is structurally valid. The competition rewards learned multi-head hydrophone encounter triage from the provided training split.

Inspiration note: Useful because it asks solvers to adapt model behavior to a specialized data distribution with held-out scoring.
