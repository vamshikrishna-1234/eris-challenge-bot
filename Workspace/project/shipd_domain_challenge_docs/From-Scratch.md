# From Scratch Challenge Examples

Scrape timestamp: 2026-07-01T06:39:43+05:30

Confirmed examples in this document: 15

These entries are included only because the challenge detail page displayed this target domain. Titles were not used for classification.

## Cross-Genre Musical Pattern Language Model
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70c45dgr0e9fx0w6x8sq1kxs848abe
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: komilpamar ranked 1st (leaderboard #4, score —); ahmed_salah7 ranked 2nd (leaderboard #6, score —); masry1 ranked 3rd (leaderboard #5, score —); shivank ranked #4 (leaderboard #27, score —)

Full challenge description from page:

> Overview
> If you have ever sat in an Irish pub and heard a fiddle player launch into a reel, you know the music has a logic to it. Phrases repeat, melodies resolve, and every tune seems to know where it is going before it gets there. Musicians learn this instinctively after years of sessions -- picking up how a jig in D moves differently from a reel in G. But here is the harder test: a fiddler who has only ever played jigs, reels, and waltzes walks into a session where everyone is playing polkas and hornpipes. Can they keep up?
> That is the question behind this challenge. Your model trains on three dance forms -- reels (4/4), jigs (6/8), and waltzes (3/4) -- but is tested exclusively on three held-out forms it has never seen: polkas (2/4), hornpipes (2/2), and slip jigs (9/8). Given the first six bars of a held-out tune as context, the model must predict the seventh bar. The training and test sets share zero dance forms. The model must learn musical principles general enough to transfer across rhythmic traditions: pitch patterns that work in any meter, phrase structures that hold across dance forms, and the relationship between key signatures and melodic movement that transcends any single genre.
> About ABC Notation: ABC notation is an ASCII-based plain text musical notation system commonly used for transcribing traditional music. It provides a compact way to represent notes, rhythms, keys, and bar structure as plain ASCII characters. This challenge uses ABC notation exclusively -- there are no WAV, MP3, MIDI, or spectrogram files. The training corpus and all submissions are pure text.
> To hear what ABC notation sounds like or view it as sheet music, tools such as the Online ABC Player for playback or EasyABC for notation editing are freely available.
> What Makes This Hard
> This is not standard melody generation. The cross-genre holdout creates a genuine transfer learning problem within music:
> Zero training examples from test genres: The model never sees a polka, hornpipe, or slip jig during training. It must infer how 2/4 and 2/2 meters work from its knowledge of 4/4, 6/8, and 3/4.
> Rhythmic transfer is non-trivial: A 6/8 jig groups notes in threes. A 2/4 polka groups them in twos. The model must understand that underlying melodic logic persists across different rhythmic subdivisions.
> Key-dependent pitch selection: A tune in D major uses F# and C# as default accidentals regardless of meter. The model must learn key signatures from reels and jigs well enough to apply them correctly in polkas and hornpipes.
> Phrase structure: Irish tunes typically follow AABB form with 8-bar sections. The model predicts bar seven -- near the end of a section where melodies typically resolve toward the tonic.
> Composite evaluation: Predictions are scored across four dimensions simultaneously, preventing models from gaming any single metric.
> Dataset
> Training corpus corpus.txt: Approximately 142,000 tunes in three dance forms (reels in 4/4, jigs in 6/8, waltzes in 3/4), written in ABC notation. Each tune is separated by a blank line and begins with header fields followed by the melody. The header fields are:
> X: (integer) -- tune index number
> L: (string) -- default note length (e.g., "1/8" for eighth note)
> M: (string) -- meter / time signature (e.g., "4/4", "6/8", "3/4")
> K: (string) -- key signature (e.g., "D", "G", "Amin")
> After the headers, the melody body uses these ABC notation elements:
> Notes: C D E F G A B (low octave), c d e f g a b (high octave)
> Octave shifts: ' raises one octave (e.g., a'), , lowers one octave (e.g., C,)
> Accidentals: ^ = sharp, _ = flat, = = natural (e.g., ^F = F#)
> Durations: A2 = double length, A/ or A/2 = half length, A3/2 = 1.5x length. No modifier = default note length from L: header
> Bar lines: | separates bars, |: and :| mark repeats, || is a double bar
> Other: - = tie, () = slur, z = rest, spaces separate note groups within a bar (cosmetic, ignored by parser)
> This is your only training data.
> Test data test.jsonl: 2,000 melody completion items from three held-out dance forms (polkas in 2/4, hornpipes in 2/2, slip jigs in 9/8). None of these meters appear in the training corpus. Each line is a JSON object with:
> id (string) -- Unique item identifier (e.g., "MUS-0020ADDA1B8A")
> context (string) -- Tune header (X:, L:, M:, K: fields) plus the first six bars of the melody, separated by bar lines. This is the model's input.
> target_meter (string) -- The meter of the tune ("2/4", "2/2", or "9/8"). Provided for reference only; not used in grading.
> Sample submission sample_submission.csv: 2,000 rows with columns id (string) and next_bar (string). Contains random bars drawn from unrelated training tunes as placeholder predictions. Demonstrates the expected CSV format and column structure.
> Evaluation
> Each prediction is scored by a composite metric comparing the predicted bar to the actual seventh bar:
> item_score = max(0, 1.0 - (0.40  *kl_pitch + 0.30*  kl_duration + 0.20  *norm_edit + 0.10*  syntax))
> Pitch Class KL Divergence (40%): Compares 12-bin chromatic pitch class histograms of predicted vs actual bar. Smoothed with 1e-10 to avoid division by zero. Capped at 1.0. Measures whether the predicted notes belong to the correct key.
> Duration KL Divergence (30%): Compares duration histograms across 5 bins defined by multiples of the default note length: bin 0 = [0, 0.25], bin 1 = (0.25, 0.5], bin 2 = (0.5, 1.0], bin 3 = (1.0, 2.0], bin 4 = (2.0, infinity). Smoothed with 1e-10 and capped at 1.0. Measures whether the prediction follows the right rhythmic pattern for the meter.
> Normalized Levenshtein (20%): Edit distance between predicted and actual note-token sequences (each token = pitch class + duration), divided by the maximum of the two sequence lengths. Range [0, 1] where 0 = identical sequences. Measures structural closeness.
> ABC Syntax Validity (10%): Binary penalty. 0 if the predicted bar contains at least one parseable ABC note character (A-G or a-g with valid modifiers). 1.0 if the output contains no recognizable notes.
> Final score = mean of all 2,000 item scores, clipped to [0.0, 1.0]. Higher is better. Random baseline: approximately 0.20-0.30.
> Submission
> CSV file with two columns:
> id (string) -- Must match the IDs in test.jsonl exactly
> next_bar (string) -- Predicted ABC notation for one bar of music. No bar lines, no headers, just note content.
> Spaces within next_bar values are cosmetic grouping in ABC notation (e.g., "ABcA BAGF" groups notes visually but the space carries no musical meaning). The grading parser ignores spaces when extracting notes. Values containing commas must be quoted per CSV convention (e.g., "G,2 BG dGBG" where G, means G in the lower octave).
> Example rows using real test IDs:
> id,next_bar
> MUS-0020ADDA1B8A,ABcA BAGF
> MUS-0023C7CBF465,fef def
> MUS-0076C51618CE,"G2 BG dGBG"
> Requirements
> Exactly 2,000 rows matching test set IDs
> Both id and next_bar columns present
> Empty or unparseable predictions score 0.0 for that item
> Method Requirements
> This benchmark requires training a language model from scratch on ABC notation. The training corpus is the only permitted source of musical knowledge.
> Pre-trained language models (GPT, LLaMA, etc.) are not permitted as the primary generation method, since the goal is to evaluate learning a novel notation system from scratch. Using a pre-trained tokenizer without its weights is acceptable if the model is retrained entirely on the provided corpus.
> Rule-based ABC generators, template-matching systems, and lookup-table approaches that copy bars from the training corpus without a learned model are not permitted. The model must generate continuations based on learned patterns, not retrieve memorized sequences.
> Hybrid approaches are allowed if a trained language model remains central. Post-processing to fix ABC syntax is acceptable. Constraining generation to valid note characters is acceptable. But melodic content must come from a trained model.

Inspiration note: Useful because it asks solvers to infer a compact generative or rule structure from the provided data, without relying on retrieval or fine-tune scaffolding.

## Mermaid Diagram Cloze Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73d6wfhm3zf3jgfg3dn0jyjx84a5jv
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: haidang ranked #6 (leaderboard #24, score 0.4625)

Full challenge description from page:

> Overview
> Train a language model from random initialization on a corpus of 400,000 Mermaid diagrams, then answer 89,874 multiple-choice cloze questions about held-out diagrams. The challenge tests whether a model can learn Mermaid syntax, structural patterns, and synthetic entity-domain associations purely from the provided training corpus.
> The 8 diagram types (flowchart, sequence, class_diagram, state_diagram, er_diagram, gantt, pie, mindmap) use completely different syntax. Content is drawn from 5 synthetic domains, with 200 entity names (40 per domain) generated under a private seed.
> Three question types test different levels of understanding:
> Fill-in-Blank (42%) -- A node name, edge label, action, or relationship is replaced with [BLANK]. Predict which of 4 options is the original. Applies to all 8 diagram types.
> Error Detection (23%) -- One element has been replaced with a plausible but incorrect value drawn from the same diagram type and content domain. Identify the wrong element from 4 options. Applies to all 8 diagram types.
> Completion (35%) -- The diagram is truncated at [NEXT_LINE]. Predict which of 4 candidate next-lines is correct. Applies to flowchart, sequence, class_diagram, er_diagram, pie, and mindmap; gantt and state_diagram are excluded.
> Evaluation
> Submissions are scored by accuracy: the fraction of test questions where the predicted option matches the correct answer.
> score = correct_predictions / total_questions
> Score range: [0.0, 1.0] (higher is better). Random baseline picking uniformly among A, B, C, D scores approximately 0.25, and the supplied sample_submission.csv (a deterministic random A/B/C/D draw) lands at the same ~0.25 floor. A best-of-heuristics parser (token-overlap with input_code, length ranking, alphabetical ranking, in-code substring presence, in-code substring count) scores approximately 0.26 when applied per question type, and approximately 0.29 when allowed to specialize per (diagram_type, question_type) cell. A model trained from scratch on train.csv is expected to score in the 0.55-0.75 range; strong solutions may exceed 0.75.
> Dataset
> 500,000 Mermaid diagrams totaling about 768 MB. 400,000 for training, 89,874 questions generated from held-out diagrams.
> File Structure
> train.csv -- 400,000 labeled training diagrams with full code
> test.csv -- 89,874 multiple-choice questions
> sample_submission.csv -- Example submission format
> train.csv
> Full Mermaid diagrams for language model training:
> id (int): Unique sample identifier
> code (string): Full Mermaid diagram code
> diagram_type (string): One of 8 diagram types
> domain (string): One of 5 content domains
> n_nodes (int): Number of nodes/entities
> has_subgraph (int): Whether nested structure is present
> reachable (int): Whether node A can reach node B
> reach_query (string): The queried node pair
> complexity (string): simple, medium, or complex
> test.csv
> Multiple-choice questions:
> id (int): Unique question identifier
> input_code (string): Mermaid code with a [BLANK], an injected error, or truncated at [NEXT_LINE]
> question_type (string): fill_blank, error_detect, or completion
> option_a (string): First answer option
> option_b (string): Second answer option
> option_c (string): Third answer option
> option_d (string): Fourth answer option
> sample_submission.csv
> id (int): Question identifier from test.csv
> correct_option (string): Predicted answer (A, B, C, or D)
> Submission
> Submit a CSV file with columns: id, correct_option
> Example:
> id,correct_option
> 1234567,B
> 2345678,A
> 3456789,D
> Requirements:
> Must contain exactly 89,874 rows (one per test question)
> Must include a header row
> The set of submitted ids must equal the set of ids in test.csv exactly (no missing ids, no extra ids, no duplicates). The grader rejects submissions whose ids do not match, even if the row count is correct.
> correct_option must be one of: A, B, C, D
> Predictions are compared case-insensitively after whitespace stripping
> Allowed and Prohibited Methods
> This is an LLM pre-training challenge. The intended solution path is to train a language model from random initialization on train.csv and use it to score the 4 options for each test question.
> Allowed:
> Training any language-model architecture (transformer, RNN, state-space, n-gram, mixture of experts, etc.) from random initialization on train.csv.
> Any tokenizer choice: BPE, WordPiece, SentencePiece, byte-level, character-level, or a custom Mermaid-aware tokenizer fit on train.csv.
> Hybrid solutions that combine a from-scratch model with deterministic rule-based pre- or post-processing.
> Regex-based parsers and Mermaid grammar checks as auxiliary features alongside a trained model.
> Self-supervised objectives derived from train.csv (masked LM, next-token, span infilling, contrastive scoring of cloze candidates).
> Prohibited:
> Pretrained language models of any size. Loading any checkpoint trained on data outside train.csv is disallowed. Explicit examples (non-exhaustive): Llama, Mistral, Qwen, Phi, GPT-2 / GPT-J / GPT-Neo, BERT, RoBERTa, T5, CodeBERT, CodeT5, ByT5, StarCoder, byte-level pretrained models, and any Hugging Face checkpoint that was pretrained on public-web text. All weights must be randomly initialized at the start of training on train.csv. Loading a tokenizer fit on outside data is also disallowed; the tokenizer must be derived from train.csv or a deterministic rule.
> Parser-only systems that produce answers from input_code without a learned model. All 4 options in every question are syntactically valid for the position they go in, so a grammar-only solver scores at the 0.25 random baseline.
> Exact template decoders that match input_code against a memorized template library and return a templated answer. Distractors in error_detect and completion are drawn from the same diagram-type element pool, so template matching does not separate correct from incorrect.
> Rule-based Mermaid syntax solvers that pick an option using only Mermaid grammar without any signal learned from train.csv. All distractors are valid Mermaid for their position; grammar is not the discriminator.
> External Mermaid corpora, public Mermaid documentation, GitHub scraping for Mermaid examples, or any data source beyond train.csv.
> Hosted LLM APIs (OpenAI, Anthropic, Gemini, Cohere, and similar) at training or inference time. Solutions must run offline using only the provided corpus.
> Hand-annotation or manual labeling of test items.
> Any signal derived from the private answer file.
> Why this synthetic Mermaid cloze setup requires learned modeling under the platform's training compute budget. Submissions train within a short, single-GPU wall-clock window. Within that window, the question is which solution class can actually reach the 0.55-0.75 LM target on these specific cloze items, and the answer is: only a model that learns from train.csv during the budget. The reasoning is grounded in this challenge's data design, not in any specific hardware.
> Pure parsers, template decoders, and Mermaid grammar solvers. These do not consume the training budget at all, yet they are capped by task design well below the LM target. Every option in every question is well-formed Mermaid for its position, length-matched to the correct option within a 1.6x window, drawn from the same diagram type, drawn from the same content domain (for fill_blank and error_detect), and equally present (or equally absent) in the visible code by substring count. The empirical combined parser ceiling on test.csv is approximately 0.26 per question type and 0.29 per (diagram_type, question_type) cell -- only 1-4 percentage points above the 0.25 random floor. Grammar has no discriminator to grip on these items, so no amount of additional rule-engineering crosses the gap to 0.55+. Time spent on this path is wasted relative to the budget.
> Pretrained LMs fine-tuned on train.csv. This is the class the budget rules out most directly, which is why from-scratch training is the expected path. The corpus contains 400,000 diagrams and roughly 250 million tokens; the training window is short. A modern pretrained checkpoint that fits a single consumer-class GPU at all requires low-rank adaptation or weight quantization to load, burns a non-trivial share of the wall-clock window on checkpoint I/O before the first gradient step, and processes the corpus at a much smaller effective batch size than a model whose embedding matrix is sized to the Mermaid vocabulary. Within the budget, a pretrained-and-fine-tuned approach can therefore visit only a small fraction of train.csv and apply only low-rank updates -- far short of teaching the base model the private synthetic entity-domain associations it never saw in pretraining. The same wall-clock window is enough for a compact from-scratch model (tens of millions of parameters) to make many passes over the same corpus, so from-scratch is not just allowed; it is the more competitive choice under the budget.
> Compact model trained from scratch on train.csv. The intended path. A tokenizer fit on train.csv keeps Mermaid operators and entity names as whole tokens, which (a) shortens sequence length and increases the effective number of gradient steps per minute, (b) gives every embedding direct signal for an item the model will actually be tested on, and (c) avoids the constant cost of a generic vocabulary that has never seen the corpus. A model of this size trained for many epochs within the budget can learn the joint distribution of (diagram_type, domain, entity, syntactic position, relationship operator) that the cloze items test -- which is exactly the signal the parser ceiling cannot reach and the signal the pretrained-fine-tuning path does not have time to acquire.

Inspiration note: Useful because it asks solvers to infer a compact generative or rule structure from the provided data, without relying on retrieval or fine-tune scaffolding.

## Buddhist Canonical Text Completion
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d5y2v6tg9wwh3re1akewj19849v5j
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: gallantknight ranked 2nd (leaderboard #41, score —); decoder ranked #6 (leaderboard #45, score —); moatasemaboubakr ranked #8 (leaderboard #28, score —); decoder ranked — (leaderboard #45, score —)

Full challenge description from page:

> Overview
> Buddhist Sanskrit literature encodes philosophical arguments through a dense system of grammatical relationships. In a sutra passage like "oṃ NAM -o BUDDH -āya PRAṆAM -ya," the suffix "-āya" on BUDDH signals that the Buddha is the recipient of the action (dative case) -- changing it to "-asya" would alter the meaning from "salutation TO the Buddha" to "salutation OF the Buddha." These suffix choices are not arbitrary inflections: they encode the logical structure of Buddhist doctrinal arguments, marking which concepts are agents, patients, instruments, or goals within a philosophical framework.
> This challenge provides 93 million characters of stemmed Buddhist Sanskrit from the Mangalam corpus -- sutras, tantras, philosophical treatises, and commentaries spanning a millennium of Buddhist thought. The corpus uses a unique representation where root morphemes appear in uppercase with explicitly marked suffixes, making the grammatical structure visible in the text surface. You must train a language model from scratch on this notation system, then predict missing suffixes in sentences from held-out documents. Because the distractors are other suffixes that genuinely occur with the same root in the training corpus, the model must learn how Buddhist philosophical argument structures determine grammatical relationships -- not merely which suffix forms are possible for a given root.
> Pre-trained language models cannot handle this task: the stemmed notation format does not appear in any pretraining corpus, the grammatical suffix system has no equivalent in English, and the philosophical content requires learning domain-specific patterns of argument and reference that are unique to Buddhist canonical literature.
> Dataset
> Training corpus corpus.txt): Cleaned text from 400 Buddhist Sanskrit documents from the Mangalam corpus. Approximately 63 million characters of stemmed and normalized text. Root morphemes appear in uppercase, grammatical suffixes follow a space and hyphen (e.g., "TATHĀGAT -asya" = genitive, "BODHISATTV -āya" = dative). Compound words are joined with @ symbols. This is your only training data.
> Test data test.jsonl): 2,000 items drawn from 46 held-out documents not in the training corpus. Each line is a JSON object:
> id (string) -- Unique item identifier in SKT-XXXXXXXXXXXX format
> context (string) -- A sentence with one suffix replaced by [BLANK]
> stem (string) -- The uppercase root whose suffix was masked
> option_a through option_d (string) -- Four candidate suffixes
> One option is the original suffix. The three distractors are other suffixes that genuinely appear with the same root elsewhere in the corpus. The model must determine which grammatical relationship fits this specific sentential context.
> Sample submission sample_submission.csv): Correctly formatted submission with random labels.
> Evaluation
> score = correct_predictions / 2000
> Accuracy on predicted option labels (A/B/C/D), case-insensitive. Score range [0.0, 1.0]. Random baseline: ~0.25.
> Submission
> CSV with two columns:
> id (string) -- Must match test.jsonl IDs exactly
> correct_option (string) -- One of A, B, C, or D
> id,correct_option
> SKT-001C843782A4,D
> SKT-003F3D4D7BE6,A
> SKT-0083A0AB507D,B
> Requirements
> Exactly 2,000 rows matching the test set IDs
> Both id and correct_option columns present
> Predictions compared case-insensitively after whitespace stripping
> Empty or NaN predictions count as incorrect
> Method Requirements
> This benchmark requires learning-based approaches with model training as a core component. Participants are expected to train language models that learn the relationship between Buddhist philosophical argument structure and grammatical suffix selection from the provided corpus. The goal is to evaluate whether models can acquire enough knowledge of this notation system to predict contextually appropriate suffixes in unseen documents.
> Purely rule-based, template-based, or hardcoded systems are not permitted. This includes approaches that rely on suffix frequency tables, deterministic morphological analyzers, or hand-crafted declension rules rather than learned representations.
> Fallback mechanisms that enforce correctness without learned knowledge are disallowed if they play a central role. This includes frequency-based suffix selection, pattern matching on stems, or any post-processing that overrides model predictions with deterministic logic. The model itself must be responsible for selecting the correct option.
> Hybrid approaches are allowed only if a meaningful trained component remains central to the system. Any supporting heuristics must be minimal and must not replace or dominate the learned prediction process.
> If a model fails to produce a valid prediction for a test item, that prediction receives a score of 0. No fallback outputs or correction mechanisms are permitted.

Inspiration note: Useful because it asks solvers to infer a compact generative or rule structure from the provided data, without relying on retrieval or fine-tune scaffolding.

## curve_plot
- Challenge URL: https://drive.google.com/drive/folders/1UY1OUE609RIzJIRA57Y1b5LbEVAJ9v9x
- Source file: challenge_description.txt
- DOMAIN used for this document: From Scratch (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / From Scratch / curve_plot

Full challenge description from Drive:

> Overview
> Curve Plot LaTeX Formula Recognition is a visual mathematical-formula recognition benchmark. Each task is a rendered 1000×1000 RGB PNG of a mathematical function's plot (a curve drawn on axes), and the model must output the LaTeX formula that produced the curve. The underlying data is a synthetically-generated public corpus of function plots paired with ground-truth LaTeX.
> The benchmark covers three naturally occurring subsets of function types: elementary (named trig, root, and power functions), noisy (plots with additive noise on top of elementary functions), and static (constant / degenerate functions). These subsets are the natural axes of generalisation — a good model should handle all three, with measured drop-off under noise.
> This is a deliberately learning-centric challenge: pretrained language models, foundation models, and any kind of externally-trained weights are prohibited. The goal is to study which inductive biases (architectural, optimisation, or curriculum-based) enable a small from-scratch learner to invert a plot back into its algebraic form.
> Challenge Characteristics
> Domain: synthetic mathematical function plots paired with LaTeX formulas
> Input modality: a single 1000×1000 RGB PNG per task
> Output modality: a single LaTeX formula string per task
> Unique constraint: the model must be trained from scratch;
> pretrained weights of any kind are prohibited
> Training data: 2,000 tasks with images and LaTeX labels
> Test data: 400 held-out tasks across four diagnostic splits
> Evaluation: whitespace-normalised exact-match on the LaTeX string
> Output length: LaTeX formulas range from 3 to ~93 characters
> Dataset
> Every task is delivered as a 1000×1000 RGB PNG of a function plot, rendered with axes, tick marks, and a single smooth (or noisy) curve. The ground-truth label is the exact LaTeX formula of the plotted function, for example:
> Plotted curve type	Example LaTeX
> \sin(x) curve	\sin{\left(x \right)}
> x^2 parabola	x^{2}
> \sqrt{x} square-root branch	\sqrt{x}
> inverse trigonometric	\operatorname{atan}(x)
> sum of two elementary functions	\sin{\left(x \right)} + \cos{\left(x \right)}
> noisy variant	same LaTeX as the clean version
> The upstream corpus covers three subsets (elementary / noisy / static), which this challenge uses to construct four diagnostic test splits (see below).
> Data Files
> File	Description	Columns
> train.csv	2,000 training tasks	id, image, latex_formula
> train_images/	2,000 task PNGs (1000×1000)
> test.csv	400 held-out tasks	id, image
> test_images/	400 task PNGs
> sample_submission.csv	Submission format template (random fill)	id, latex_formula
> The image column is a relative path of the form train_images/train_0000000.png. Filenames are unique within each split. Participants are expected to carve their own validation split out of train.csv if they want one.
> Example Row (from train.csv)
> id:             train_0000000
> image:          train_images/train_0000000.png
> latex_formula:  \cos{\left(x \right)}
> The image encodes the full function plot; the model must look at the pixels to perceive the curve and produce the exact LaTeX formula that generated it.
> Test splits
> The test set is a shuffled mixture of four diagnostic splits (the split labels are hidden from participants):
> Split	Tasks	Origin	What it probes
> test_iid	100	mixture of all three upstream subsets	in-distribution generalisation
> test_elementary	100	only the graph_function_elementary subset	performance on clean, named elementary plots
> test_noisy	100	only the graph_function_noisy subset	noise robustness
> test_static	100	only the graph_function_static subset	degenerate / constant-function behaviour
> All samples drawn into the subset-specific splits are held out from the train pool, so a strong model on test_<subset> cannot have memorised those specific images during training.
> Submission Format
> Submit a CSV with exactly the columns id and latex_formula. There must be one row per test task and the id column must match test.csv exactly.
> id,latex_formula
> test_000000,"\cos{\left(x \right)}"
> test_000001,"x^{2}"
> test_000002,"\sin{\left(x \right)} + \cos{\left(x \right)}"
> Formatting requirements
> Each latex_formula is a LaTeX string reproducing the plotted function's formula
> Backslashes must be present as-is (e.g. \cos, not cos) — they count toward the exact-match comparison after whitespace normalisation
> Whitespace (spaces, tabs, newlines) is collapsed to single spaces and leading/trailing whitespace is stripped before comparison; otherwise matching is strict
> Empty answers are permitted but score 0
> Strict LaTeX Format Requirement (Important)
> The ground-truth LaTeX strings are generated by a fixed upstream pipeline and follow a canonical syntactic form. Predictions must reproduce this exact format to receive credit.
> Mathematically equivalent expressions will NOT be accepted. For example:
> \sin(x) ≠ \sin{\left(x \right)}
> atan(x) ≠ \operatorname{atan}(x)
> Participants are strongly advised to learn or model the exact formatting patterns present in the training data. Failure to match this syntax exactly will result in a score of 0 for that example.
> Evaluation: Exact Match
> Every task is scored 1 if the predicted latex_formula matches the ground truth exactly (after whitespace normalisation) and 0 otherwise. The final benchmark score is the mean per-task score across the entire test set.
> task_score = em(pred, gt)
> final_score = mean(task_score over all 400 test tasks)
> Method Requirements
> This is a train-from-scratch benchmark. Strong submissions should:
> Train an image-based model on the supplied training data, with all learned parameters initialised from scratch;
> Report held-out accuracy and explicitly discuss how their training procedure encourages robustness to the noisy and static diagnostic splits;
> Avoid pretrained weights of any kind.
> Prohibited approaches
> Foundation models, pretrained LLMs, vision foundation models, or any externally pretrained weights (including pretrained image backbones, pretrained tokenisers, or pretrained embedding tables)
> Test-time fine-tuning, retrieval over the test set, or per-test-task hyperparameter selection using the test labels
> Allowed
> Any image-based pipeline trained from scratch on the supplied training images, including:
> End-to-end learned models (CNN/ViT encoders feeding a small token decoder for the LaTeX string)
> Hand-designed feature extraction (e.g. curve sampling along pixel columns, classical computer-vision features) followed by a from-scratch decoder
> Curriculum learning, data augmentation (crop, contrast jitter, noise injection), auxiliary losses, or symbolic-regression heads — provided they only consume the supplied training data
> Ensembling multiple from-scratch models trained on the same training set
> Tokenizer Clarification
> Participants may design and train their own tokenization scheme from scratch using only the provided training LaTeX strings. This includes:
> Character-level tokenization
> Custom rule-based tokenizers
> Learning a small BPE / unigram vocabulary over the 2,000 training formulas
> However, pretrained tokenizers or vocabularies are not allowed.
> What Not To Use
> Foundation models, pretrained LLMs, vision foundation models, or any externally pretrained weights (including pretrained image backbones, pretrained tokenisers, or pretrained embedding tables)
> Test-time fine-tuning, retrieval over the test set, or per-test-task hyperparameter selection using the test labels

Inspiration note: Useful as a rule-inference benchmark pattern where solvers must learn the hidden grammar or simulator from generated examples.

## Cross-Genre Musical Pattern Language Model
- Challenge URL: https://drive.google.com/drive/folders/1Fvo5Y12-17jNrCEoXdRNZ3MLhI0tzxOj
- Source file: cd.txt
- DOMAIN used for this document: From Scratch (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / From Scratch / Cross-Genre Musical Pattern Language Model

Full challenge description from Drive:

> Cross-Genre Musical Pattern Transfer
> Overview
> If you have ever sat in an Irish pub and heard a fiddle player launch into a reel, you know the music has a logic to it. Phrases repeat, melodies resolve, and every tune seems to know where it is going before it gets there. Musicians learn this instinctively after years of sessions -- picking up how a jig in D moves differently from a reel in G. But here is the harder test: a fiddler who has only ever played jigs, reels, and waltzes walks into a session where everyone is playing polkas and hornpipes. Can they keep up?
> That is the question behind this challenge. Your model trains on three dance forms -- reels (4/4), jigs (6/8), and waltzes (3/4) -- but is tested exclusively on three held-out forms it has never seen: polkas (2/4), hornpipes (2/2), and slip jigs (9/8). Given the first six bars of a held-out tune as context, the model must predict the seventh bar. The training and test sets share zero dance forms. The model must learn musical principles general enough to transfer across rhythmic traditions: pitch patterns that work in any meter, phrase structures that hold across dance forms, and the relationship between key signatures and melodic movement that transcends any single genre.
> About ABC Notation: ABC notation is an ASCII-based plain text musical notation system commonly used for transcribing traditional music. It provides a compact way to represent notes, rhythms, keys, and bar structure as plain ASCII characters. This challenge uses ABC notation exclusively -- there are no WAV, MP3, MIDI, or spectrogram files. The training corpus and all submissions are pure text.
> To hear what ABC notation sounds like or view it as sheet music, tools such as the Online ABC Player for playback or EasyABC for notation editing are freely available.
> What Makes This Hard
> This is not standard melody generation. The cross-genre holdout creates a genuine transfer learning problem within music:
> Zero training examples from test genres: The model never sees a polka, hornpipe, or slip jig during training. It must infer how 2/4 and 2/2 meters work from its knowledge of 4/4, 6/8, and 3/4.
> Rhythmic transfer is non-trivial: A 6/8 jig groups notes in threes. A 2/4 polka groups them in twos. The model must understand that underlying melodic logic persists across different rhythmic subdivisions.
> Key-dependent pitch selection: A tune in D major uses F# and C# as default accidentals regardless of meter. The model must learn key signatures from reels and jigs well enough to apply them correctly in polkas and hornpipes.
> Phrase structure: Irish tunes typically follow AABB form with 8-bar sections. The model predicts bar seven -- near the end of a section where melodies typically resolve toward the tonic.
> Composite evaluation: Predictions are scored across four dimensions simultaneously, preventing models from gaming any single metric.
> Dataset
> Training corpus corpus.txt: Approximately 142,000 tunes in three dance forms (reels in 4/4, jigs in 6/8, waltzes in 3/4), written in ABC notation. Each tune is separated by a blank line and begins with header fields followed by the melody. The header fields are:
> X: (integer) -- tune index number
> L: (string) -- default note length (e.g., "1/8" for eighth note)
> M: (string) -- meter / time signature (e.g., "4/4", "6/8", "3/4")
> K: (string) -- key signature (e.g., "D", "G", "Amin")
> After the headers, the melody body uses these ABC notation elements:
> Notes: C D E F G A B (low octave), c d e f g a b (high octave)
> Octave shifts: ' raises one octave (e.g., a'), , lowers one octave (e.g., C,)
> Accidentals: ^ = sharp, _ = flat, = = natural (e.g., ^F = F#)
> Durations: A2 = double length, A/ or A/2 = half length, A3/2 = 1.5x length. No modifier = default note length from L: header
> Bar lines: | separates bars, |: and :| mark repeats, || is a double bar
> Other: - = tie, () = slur, z = rest, spaces separate note groups within a bar (cosmetic, ignored by parser)
> This is your only training data.
> Test data test.jsonl: 2,000 melody completion items from three held-out dance forms (polkas in 2/4, hornpipes in 2/2, slip jigs in 9/8). None of these meters appear in the training corpus. Each line is a JSON object with:
> id (string) -- Unique item identifier (e.g., "MUS-0020ADDA1B8A")
> context (string) -- Tune header (X:, L:, M:, K: fields) plus the first six bars of the melody, separated by bar lines. This is the model's input.
> target_meter (string) -- The meter of the tune ("2/4", "2/2", or "9/8"). Provided for reference only; not used in grading.
> Sample submission sample_submission.csv: 2,000 rows with columns id (string) and next_bar (string). Contains random bars drawn from unrelated training tunes as placeholder predictions. Demonstrates the expected CSV format and column structure.
> Evaluation
> Each prediction is scored by a composite metric comparing the predicted bar to the actual seventh bar:
> item_score = max(0, 1.0 - (0.40  *kl_pitch + 0.30*  kl_duration + 0.20  *norm_edit + 0.10*  syntax))
> Pitch Class KL Divergence (40%): Compares 12-bin chromatic pitch class histograms of predicted vs actual bar. Smoothed with 1e-10 to avoid division by zero. Capped at 1.0. Measures whether the predicted notes belong to the correct key.
> Duration KL Divergence (30%): Compares duration histograms across 5 bins defined by multiples of the default note length: bin 0 = [0, 0.25], bin 1 = (0.25, 0.5], bin 2 = (0.5, 1.0], bin 3 = (1.0, 2.0], bin 4 = (2.0, infinity). Smoothed with 1e-10 and capped at 1.0. Measures whether the prediction follows the right rhythmic pattern for the meter.
> Normalized Levenshtein (20%): Edit distance between predicted and actual note-token sequences (each token = pitch class + duration), divided by the maximum of the two sequence lengths. Range [0, 1] where 0 = identical sequences. Measures structural closeness.
> ABC Syntax Validity (10%): Binary penalty. 0 if the predicted bar contains at least one parseable ABC note character (A-G or a-g with valid modifiers). 1.0 if the output contains no recognizable notes.
> Final score = mean of all 2,000 item scores, clipped to [0.0, 1.0]. Higher is better. Random baseline: approximately 0.20-0.30.
> Submission
> CSV file with two columns:
> id (string) -- Must match the IDs in test.jsonl exactly
> next_bar (string) -- Predicted ABC notation for one bar of music. No bar lines, no headers, just note content.
> Spaces within next_bar values are cosmetic grouping in ABC notation (e.g., "ABcA BAGF" groups notes visually but the space carries no musical meaning). The grading parser ignores spaces when extracting notes. Values containing commas must be quoted per CSV convention (e.g., "G,2 BG dGBG" where G, means G in the lower octave).
> Example rows using real test IDs:
> id,next_bar
> MUS-0020ADDA1B8A,ABcA BAGF
> MUS-0023C7CBF465,fef def
> MUS-0076C51618CE,"G2 BG dGBG"
> Requirements
> Exactly 2,000 rows matching test set IDs
> Both id and next_bar columns present
> Empty or unparseable predictions score 0.0 for that item
> Method Requirements
> This benchmark requires training a language model from scratch on ABC notation. The training corpus is the only permitted source of musical knowledge.
> Pre-trained language models (GPT, LLaMA, etc.) are not permitted as the primary generation method, since the goal is to evaluate learning a novel notation system from scratch. Using a pre-trained tokenizer without its weights is acceptable if the model is retrained entirely on the provided corpus.
> Rule-based ABC generators, template-matching systems, and lookup-table approaches that copy bars from the training corpus without a learned model are not permitted. The model must generate continuations based on learned patterns, not retrieve memorized sequences.
> Hybrid approaches are allowed if a trained language model remains central. Post-processing to fix ABC syntax is acceptable. Constraining generation to valid note characters is acceptable. But melodic content must come from a trained model.

Inspiration note: Useful as a rule-inference benchmark pattern where solvers must learn the hidden grammar or simulator from generated examples.

## 2D Xray Inpainting Benchmark
- Challenge URL: https://drive.google.com/drive/folders/12MPsgMfAoSQdt5AK2lqaV-HkcVGBC2l8
- Source file: cd.txt
- DOMAIN used for this document: From Scratch (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / From Scratch / 2D Xray Inpainting Benchmark

Full challenge description from Drive:

> Overview
> You are part of a healthcare consulting organisation for AI in medical imaging. Your client asked you to develop a prototype approach that can inpaint (fill-in) missing pixels in a 2D X-ray image.
> The client wants to use this for data augmentation workflows later, but now wants a perfect demonstration on 64x64 downsampled X-rays before investing in more R&D or GPU resources. To facilitate faster iterations we start a company wide challenge:
> Prediction task: for each test sample, predict the masked pixel intensities (0–255) and output them in row-major masked-coordinate order.
> You are provided preprocessed X-ray images of 64x64 resolution in PNG format for training.
> For testing you are given the masks and the masked images that need to be inpainted.
> In this challenge, original high-resolution X-rays are center-cropped to 192x192, downsampled to 64x64, and transformed with a deterministic privacy-preserving intensity transform.
> The objective is to reconstruct masked pixel intensities in realistic chest X-ray anatomy. Method constraint: submissions must use a diffusion-based inpainting model trained from scratch.
> Rules and Constraints
> The client explicitly requires a diffusion-based model trained from scratch for this prototype.
> Rule-based filling methods (for example copying neighboring intensity values) are strictly prohibited.
> Non-diffusion core approaches (like GANs etc) are out of scope for this challenge deliverable.
> Only from scratch trained models are allowed, no pretrained checkpoints.
> Test data cannot be used for training, this includes any knowledge of the masked regions or shapes. So the client wants a model that can inpaint/infill any shape of mask at inference time. Ignore test data distribution in your solutions.
> It is against the logic of the prototype to look for data in the internet or other cheating techniques, so such retrieval methods are not allowed.
> Submissions may be manually reviewed for compliance.
> Dataset
> The dataset contains a public training set and a hidden private test target set.
> 20000 public training images
> 1000 hidden test images (ground truth originals are private)
> all final images are grayscale PNG, size 64x64
> Each test sample has one masked image and one binary mask. The inpainting masks are only provided for test images.
> Mask properties:
> one inpainting mask per test image
> 20 shape families (10 standard + 10 harder families)
> Mask PNGs are binary with 0 for known context and 255 for masked pixels to inpaint
> mask area per test image is between 16 and 256 pixels (inclusive). This inclusive 16–256 range is a hard cap applied to all 20 mask families, including harder families (for example fixed_16x16_block = 256).
> Standard families:
> single_horizontal_line
> single_vertical_line
> double_horizontal_line
> double_vertical_line
> plus_cross
> diagonal_cross
> box_outline
> zigzag_line
> happy_face
> sketch_curve
> Harder families:
> fixed_16x16_block
> random_rectangle_block
> double_block_cutout
> hollow_ring
> edge_stripe_band
> diagonal_ribbon
> lung_arc_band
> checkerboard_patch
> thick_plus_cross
> thick_x_cross
> File Structure
> public/
> images/
> train/
> <id>.png
> test_masked/
> <id>.png
> masks/
> <id>_mask.png
> train.csv
> test.csv
> sample_submission.csv
> CSV Schemas
> public/train.csv:
> columns: id,image_path
> id: anonymized training sample ID
> image_path: relative path under public/ to train image PNG
> public/test.csv:
> columns: id,masked_image_path,mask_path,shape_name,mask_pixel_count
> id: anonymized test sample ID
> masked_image_path: relative path under public/ to masked test image
> mask_path: relative path under public/ to binary mask PNG
> shape_name: mask family label
> mask_pixel_count: number of masked pixels for that sample
> mask_path points to public/masks and these masks are provided for test samples only. Training data should either be used with unconditional models or created on the fly synthetically.
> public/sample_submission.csv:
> columns: id,pixels
> id: test sample ID
> pixels: placeholder prediction string with exactly mask_pixel_count integers
> Evaluation
> Submissions are scored with a composite metric:
> masked-pixel normalized MAE component
> full-image PSNR-based component on reconstructed 64x64 outputs
> For each test sample, the grader reconstructs the full predicted image as:
> pred_full = masked_full
> pred_full[mask_flat == 1] = submission_pixels
> Then computes:
> mae_component = clip((MAE / 255.0) / 0.1, 0, 1)
> psnr_component = 1 - clip((PSNR - 30.0) / 10.0, 0, 1)
> score = 0.5 * mae_component + 0.5 * psnr_component
> Both sub-components are loss terms in [0,1], and better predictions push both components toward 0.
> PSNR is computed on reconstructed full 64x64 images after converting both original and reconstructed pixels to [0,1] by dividing by 255.0: MSE_full = mean((orig_full/255.0 - pred_full/255.0)^2), PSNR = 10 * log10(1 / MSE_full). PSNR values are clipped to [30, 40] dB for scoring. The MAE component is computed only on predicted/inpainted (masked) pixels.
> Official metric logic:
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> `# MAE on masked predicted values`
> `mae_norm = (total_abs / total_mask_pixels) / 255.0`
> `mae_component = clip(mae_norm / 0.1, 0, 1)`
> `# PSNR on reconstructed full image`
> `# pred_full = masked_full`
> `# pred_full[mask_flat == 1] = pred_pixels`
> `psnr_component = 1 - clip((mean_psnr - 30.0) / 10.0, 0, 1)`
> `return 0.5 * mae_component + 0.5 * psnr_component`
> Final score range is [0, 1]:
> 0.0 is perfect
> 1.0 is worst valid case
> lower is better
> ## Submission
> Submit one file named submission.csv.
> Requirements:
> exactly 1000 data rows (plus header)
> exactly these two columns in this order: id,pixels
> id values must match public/sample_submission.csv exactly
> no duplicate IDs
> no missing values
> each pixels cell must contain exactly mask_pixel_count integers in [0,255]
> pixel order must be row-major over masked coordinates:
> top to bottom (y increasing)
> left to right (x increasing) for equal y
> Valid example:
> id,pixels
> 00173b624ac5335f,120 118 117 121 122 119 ...
> 006cd30476080e3d,98 101 103 99 97 ...
> 00d820f9987fdd5b,87 89 90 92 ...
> Helper to extract pixels from a full predicted PNG:
> from PIL import Image
> import numpy as np
> def masked_png_to_cell(pred_png: str, mask_png: str) -> str:
> pred = np.asarray(Image.open(pred_png).convert("L"), dtype=np.uint8)
> mask = np.asarray(Image.open(mask_png).convert("L"), dtype=np.uint8) > 0
> coords = np.argwhere(mask)
> order = np.lexsort((coords[:, 1], coords[:, 0]))
> coords = coords[order]
> values = [str(int(pred[y, x])) for y, x in coords]
> return " ".join(values)
> What Not To Use
> Rule-based filling methods (for example copying neighboring intensity values) are strictly prohibited.
> Non-diffusion core approaches (like GANs etc) are out of scope for this challenge deliverable.
> Only from scratch trained models are allowed, no pretrained checkpoints.
> It is against the logic of the prototype to look for data in the internet or other cheating techniques, so such retrieval methods are not allowed.
> Dont use test data in any way to train models. This includes any knowledge about the inpainting masks.

Inspiration note: Useful as a rule-inference benchmark pattern where solvers must learn the hidden grammar or simulator from generated examples.

## Skaldic Honor-Court Session Tracking
- Challenge URL: https://drive.google.com/drive/folders/16g3HLq8ziLFmrKfjhG6_HooS9eXzw7nZ
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: From Scratch (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved example from shared Drive folder
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Skaldic Honor-Court Session Tracking from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Skaldic Honor-Court Session Corpus.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) GPU Tier
> **Select:** **A10G** (standard ML workloads; no LLM training required)
> ---
> ## 3) Challenge Title
> ```
> Skaldic Honor-Court Session Tracking
> ```
> ---
> ## 4) Problem Description
> # Skaldic Honor-Court Session Tracking
> ## Overview
> The **Skaldic Honor-Courts** are a fictional pre-modern legal tradition in which disputes are resolved not by written law but by chains of obligation encoded in highly stylized verse declarations called **kennslags**. In a single "court session," six to ten kennslags are uttered in a fixed order; each one may create, transfer, balance, or void an honor-debt between named parties. The final standing between any two parties at the end of the session is a function of every kennslag along the way.
> Your task is to reconstruct that final standing.
> Given a full court session (6–10 kennslags rendered as stylized English text) and a queried pair of parties `party_a` and `party_b`, predict the resulting honor-debt state in the form `STATE\|AMOUNT`:
> - `A_OWES_B\|N` — net honor-debt accumulates with party A owing party B exactly N honor-units.
> - `B_OWES_A\|N` — net honor-debt accumulates with party B owing party A exactly N honor-units.
> - `BALANCED\|0` — any prior net debt between A and B has been settled; the parties are even.
> - `KINDLED\|0` — a kindled grievance (blood-feud state) has been triggered between A and B.
> - `VOIDED\|0` — a ritual voiding has nullified all dealings between A and B.
> The session text and the queried pair are the only information provided. No rulebook, glossary, or legend accompanies the data — every mechanic of the Skaldic honor-system must be inferred from labeled training examples. The system is entirely synthetic and has no prior appearance in any real-world corpus, so pretrained models cannot transfer their knowledge of existing honor cultures.
> The following solver behaviours will cause the submission to be rejected on review, regardless of leaderboard score:
> - Hand-written rule engines, regex tables, or keyword classifiers that do not induce any parameters from the training labels. The challenge specifically tests whether an agent can learn an unseen rule system from labeled examples.
> - Zero-shot or few-shot prompting of language models without any fitting on `public/train.csv`. The Skaldic system is fully synthetic and unseen during pretraining, so pure prompting cannot learn its mechanics.
> - Hosted or closed-source API models at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), and any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
> - Solutions that ignore `(party_a, party_b)` order and only classify the session as a whole.
> - Memorizing training labels verbatim (near-zero training loss without regularization or early stopping), since ~10% of training labels are wrong and cannot be recovered from the text.
> - Grader / platform exploitation — hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel other than `public/`.
> - Ensembles mixing allowed and prohibited components. A single prohibited component contaminates the whole ensemble.
> ## Evaluation
> Submissions are scored using a **composite per-session metric** that requires correct state AND (for numeric states) a close estimate of the accumulated debt amount.
> For each test session, the grader parses the predicted `STATE\|AMOUNT` and the true `STATE\|AMOUNT`, then:
> - If the prediction is malformed, or the predicted STATE does not match the true STATE, the row scores **0.0**.
> - Else if the true STATE is `BALANCED`, `KINDLED`, or `VOIDED`, the row scores **1.0** (the amount field is ignored for these states).
> - Else the true STATE is `A_OWES_B` or `B_OWES_A`, and the row scores **max(0, 1 − \|pred_amt − true_amt\| / 5)**.
> The final leaderboard score is the mean of `row_score` across all test sessions.
> - Off-by-one on the amount earns 0.8; off-by-five or more earns 0.0.
> - A wrong STATE earns 0.0 regardless of amount, so the state must be right first.
> - Higher is better. Minimum: 0.0. Maximum: 1.0.
> **Baseline scores (for calibration):**
> - Always `BALANCED\|0` — ~0.24
> - Always `A_OWES_B\|2` — ~0.22
> - Uniform random class + random amount — ~0.18
> - Best trivial keyword-heuristic — ~0.29
> ## Dataset
> After preparation, the public directory contains:
> - `train.csv` — 3,000 labeled sessions (contains ~10% label noise).
> - `test.csv` — 1,500 unlabeled test sessions.
> - `sample_submission.csv` — 1,500 rows with placeholder `BALANCED\|0` for every row.
> Training columns:
> - `session_id` (int) — unique identifier.
> - `session_text` (str) — full session text with numbered kennslag markers `[1] ... [2] ... [3] ...`.
> - `party_a` (str) — first queried party, format "Given-Name of Village".
> - `party_b` (str) — second queried party, format "Given-Name of Village".
> - `n_kennslags` (int) — number of kennslags in the session (6–10, inclusive).
> - `label` (str) — final honor-debt state as `STATE\|AMOUNT`.
> Test columns: the same as training minus the `label` column.
> **Example session_text (truncated):**
> ```
> [1] at the stone circle, Vorn of Askhelm, shield-bearer iron-pledged to
> Brigga of Drennvik, stranger-kin. [2] in the thing-hall, Brigga of Drennvik,
> stranger-kin skarn Vorn of Askhelm, shield-bearer. [3] with the hearth cold,
> Oril of Voltsholm, salt-holder ash-named Keld of Myrrhold, ring-giver. Vorn
> of Askhelm watched but gave no pledge. ...
> ```
> For this example, the queried pair might be `party_a = "Vorn of Askhelm"`, `party_b = "Brigga of Drennvik"`.
> ## Submission
> Submit a CSV with the following columns:
> - `session_id` (int) — identifier from `test.csv`.
> - `label` (str) — predicted `STATE\|AMOUNT` string.
> **Requirements:**
> - Must contain exactly 1,500 rows — one per test session.
> - Include a header row.
> - All `session_id` values must be unique and match the test set exactly.
> - `STATE` must be one of: `A_OWES_B`, `B_OWES_A`, `BALANCED`, `KINDLED`, `VOIDED`.
> - `AMOUNT` must be a non-negative integer; non-numeric states must use `0`.
> - Malformed rows score 0.0 for that session.
> **Example submission:**
> ```csv
> session_id,label
> 4123,A_OWES_B|3
> 4124,VOIDED|0
> 4125,BALANCED|0
> 4126,B_OWES_A|1
> 4127,KINDLED|0
> ```
> ---
> ## 5) Tags
> **Select:** `text`, `small-data`
> ---
> ## 6) Grading Configuration
> - **Grade direction:** **Maximize**
> - **Theoretical minimum:** `0`
> - **Theoretical maximum:** `1`
> ---
> ## 7) Grading Script
> **Select:** `Custom`
> ```python
> import pandas as pd
> import numpy as np
> VALID_STATES = {"A_OWES_B", "B_OWES_A", "BALANCED", "KINDLED", "VOIDED"}
> NUMERIC_STATES = {"A_OWES_B", "B_OWES_A"}
> AMOUNT_TOLERANCE = 5.0
> def _parse_label(s):
> if not isinstance(s, str):
> return None, None
> parts = s.strip().split("|")
> if len(parts) != 2:
> return None, None
> state, amt_str = parts[0].strip(), parts[1].strip()
> if state not in VALID_STATES:
> return None, None
> try:
> amt = int(amt_str)
> except (ValueError, TypeError):
> return None, None
> if amt < 0:
> return None, None
> if state not in NUMERIC_STATES and amt != 0:
> return None, None
> return state, amt
> def _row_score(pred_state, pred_amt, true_state, true_amt):
> if pred_state is None:
> return 0.0
> if pred_state != true_state:
> return 0.0
> if true_state in NUMERIC_STATES:
> diff = abs(pred_amt - true_amt)
> return max(0.0, 1.0 - diff / AMOUNT_TOLERANCE)
> return 1.0
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if "session_id" not in submission.columns or "label" not in submission.columns:
> return 0.0
> if "session_id" not in answers.columns or "label" not in answers.columns:
> return 0.0
> if submission["session_id"].duplicated().any():
> return 0.0
> if answers["session_id"].duplicated().any():
> return 0.0
> if set(submission["session_id"]) != set(answers["session_id"]):
> return 0.0
> if len(submission) != len(answers):
> return 0.0
> merged = answers.merge(
> submission, on="session_id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> if merged["label_pred"].isna().any():
> return 0.0
> total = 0.0
> n = len(merged)
> for _, row in merged.iterrows():
> true_state, true_amt = _parse_label(row["label_true"])
> pred_state, pred_amt = _parse_label(row["label_pred"])
> if true_state is None:
> return 0.0
> total += _row_score(pred_state, pred_amt, true_state, true_amt)
> score = total / n
> if np.isnan(score):
> return 0.0
> return float(max(0.0, min(1.0, score)))
> except Exception:
> return 0.0
> ```
> ---
> ## 8) Prepare Script
> ```python
> from pathlib import Path
> def prepare(raw: Path, public: Path, private: Path) -> None:
> import pandas as pd
> import numpy as np
> raw = Path(raw)
> public = Path(public)
> private = Path(private)
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> df = pd.read_csv(str(raw / "data.csv"))
> assert df["session_id"].nunique() == len(df), "Duplicate session_ids"
> required = {"session_id", "session_text", "party_a", "party_b",
> "n_kennslags", "label"}
> assert required.issubset(df.columns)
> rng = np.random.RandomState(42)
> indices = np.arange(len(df))
> rng.shuffle(indices)
> split_point = int(len(df) * (2.0 / 3.0))
> train_idx = indices[:split_point]
> test_idx = indices[split_point:]
> assert len(set(train_idx) & set(test_idx)) == 0
> train_df = df.iloc[train_idx].reset_index(drop=True).copy()
> test_df = df.iloc[test_idx].reset_index(drop=True).copy()
> assert set(train_df["session_id"]) & set(test_df["session_id"]) == set()
> STATES = ["A_OWES_B", "B_OWES_A", "BALANCED", "KINDLED", "VOIDED"]
> noise_rng = np.random.RandomState(99)
> noise_mask = noise_rng.random(len(train_df)) < 0.10
> for idx in train_df.index[noise_mask]:
> true_label = str(train_df.loc[idx, "label"])
> true_state = true_label.split("|")[0]
> wrong_states = [s for s in STATES if s != true_state]
> new_state = noise_rng.choice(wrong_states)
> if new_state in ("A_OWES_B", "B_OWES_A"):
> new_amt = int(noise_rng.randint(1, 6))
> new_label = f"{new_state}|{new_amt}"
> else:
> new_label = f"{new_state}|0"
> train_df.loc[idx, "label"] = new_label
> train_out = train_df[["session_id", "session_text", "party_a", "party_b",
> "n_kennslags", "label"]].copy()
> train_out.to_csv(str(public / "train.csv"), index=False)
> test_out = test_df[["session_id", "session_text", "party_a", "party_b",
> "n_kennslags"]].copy()
> test_out.to_csv(str(public / "test.csv"), index=False)
> sample_sub = test_df[["session_id"]].copy()
> sample_sub["label"] = "BALANCED|0"
> sample_sub.to_csv(str(public / "sample_submission.csv"), index=False)
> answers = test_df[["session_id", "label"]].copy()
> answers.to_csv(str(private / "answers.csv"), index=False)
> ```
> ---
> ## 9) What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.
> - Hand-written rule engines, regex tables, or keyword classifiers that do not induce any parameters from the training labels.
> - Zero-shot or few-shot prompting of language models without any fitting on `public/train.csv`.
> - Hosted or closed-source API models at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), and any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
> - Solutions that ignore the queried `(party_a, party_b)` order and only classify the session as a whole.
> - Pure memorization of training labels without regularization, early stopping, or noise-robust training, given the ~10% training-label noise.
> - Grader / platform exploitation — hard-coded `session_id` to label dictionaries, filesystem probes for `private/answers.csv`, or any channel other than `public/`.
> - Ensembles mixing allowed and prohibited components. A single prohibited component contaminates the whole ensemble.

Inspiration note: Useful as a rule-inference benchmark pattern where solvers must learn the hidden grammar or simulator from generated examples.

## Mirror-Glyph Decryption
- Challenge URL: https://drive.google.com/drive/folders/10GhB5zGmJNdFubol3mAq2cXCKtzFPAxJ
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: From Scratch (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved example from shared Drive folder
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Mirror-Glyph Decryption from shared Google Drive folder

Full challenge description from Drive:

> # Challenge Form Fill
> ## Difficulty
> Hard
> ## Challenge Title
> Mirror-Glyph Decryption: Latent-Regime Decoding, Boundary Detection, and Lock-State Calibration
> ## Tags
> text, feature-engineering
> ## Problem Description
> ### Overview
> Mirror-Glyph Decryption is a synthetic three-output sequence-to-sequence challenge. Each input is a stream of paired glyphs `[L_t | R_t]` of variable length. The two glyph vocabularies are disjoint — `L`-glyphs come from a 16-symbol alphabet, `R`-glyphs come from a different 16-symbol alphabet. Every position `t` in the stream encodes a hidden **payload glyph** `P_t` from a 24-symbol payload vocabulary, decoded under a hidden **regime** `r_t ∈ {0, 1, …, 7}` that can shift mid-stream at unannotated positions.
> For every test stream the solver must produce three outputs.
> | Output             | Type                           | Meaning                                                                                                                                       |
> |--------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
> | `pred_payload`     | space-separated payload tokens | The decoded payload glyph at every position. Must have exactly `length` tokens, each from the 24-symbol payload vocabulary `P00..P23`.        |
> | `pred_boundaries`  | space-separated 0/1 tokens     | Per-position binary indicator: 1 if position `t` is the start of a new regime, 0 otherwise. Must have exactly `length` tokens.                |
> | `pred_lock_conf`   | float in [0, 1]                | Calibrated probability that the stream ends in the **locked** state. Lock state is a hidden cumulative function of the L-stream and is binary at the end of the stream. |
> The three outputs measure three genuinely different capabilities — per-position pattern decoding, change-point detection, and calibrated cumulative estimation. None is solvable for free given the others.
> | Hidden mechanic                  | What it does                                                                                                                                          |
> |----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
> | Regime tables                    | 8 hidden lookup tables, each mapping `(L_t, R_t) → P_t`. The active table at position `t` is determined by the current regime, which is never observed. |
> | Regime drift                     | At any position the regime can change with low probability. Boundaries are not annotated even in training — solvers must infer them from payload statistics. |
> | Lock-trigger glyphs              | A small subset of `L`-glyphs are positive lock triggers and a smaller subset are negative lock triggers. The cumulative net count, compared against a hidden threshold, defines lock state. |
> | Train and test label noise       | Training payload labels are flipped at ≈10 %, training boundary labels at ≈5 %, training lock labels at ≈5 %. Test answers are independently flipped at ≈8 %, ≈5 %, ≈5 %. This caps oracle scores below 1.0. |
> | Identifiers                      | `stream_id` is a seeded random permutation and carries no information about position in the raw upstream order.                                         |
> The 8 regime tables, the lock triggers, and the lock threshold are all **hidden** — they are never given to the solver in any file. Solvers must induce them implicitly from the supervised training pairs.
> See **What Not To Use** at the bottom for the full list of prohibited shortcuts.
> ### Evaluation
> Submissions are scored **per stream**, then averaged over all test streams. For a single stream of length `L`:
> ```
> Stream_score = 0.45 * payload_token_accuracy
> + 0.30 * boundary_macro_F1
> + 0.25 * lock_score
> lock_score = 1 - (pred_lock_conf - true_lock_state) ** 2
> ```
> The next table breaks down each term.
> | Term                       | Weight | What it measures                                                                                                                  |
> |----------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------|
> | `payload_token_accuracy`   | 0.45   | Fraction of positions where `pred_payload[t] == true_payload[t]`. Computed over the full stream length.                            |
> | `boundary_macro_F1`        | 0.30   | Unweighted mean of class-0 and class-1 F1 on the per-position binary regime-boundary prediction.                                  |
> | `lock_score`               | 0.25   | One minus the Brier loss of `pred_lock_conf` against `true_lock_state`. A perfectly calibrated probability of `0.5` against either truth scores `0.75`. |
> The leaderboard score is the arithmetic mean of `Stream_score` across every test stream, clipped to `[0, 1]`. Higher is better. Theoretical minimum is 0.0; theoretical maximum is 1.0.
> The 0.45 / 0.30 / 0.25 weighting reflects the relative difficulty of the three sub-tasks. The next table summarises why each cannot be skipped.
> | Sub-task                    | Why it cannot be skipped                                                                                                                                  |
> |-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
> | Payload decoding            | Bounded above by ≈ 0.92 token accuracy because of test-side label noise. A per-pair majority lookup ignoring regime tops out near 0.5 token accuracy.       |
> | Boundary detection          | Boundaries occur at ≈ 6 % of positions. Macro-F1 punishes both false positives and false negatives; an all-zero prediction scores ≈ 0.49.                  |
> | Lock-state calibration      | Brier-loss favours probabilities that match the true base rate, so naive constants like `0.5` cap the term at `0.75`. Reaching higher requires per-stream cumulative reasoning over the L-stream. |
> The next table gives expected scores for several common solver strategies.
> | Strategy                                                                                                  | Expected score |
> |-----------------------------------------------------------------------------------------------------------|----------------|
> | Constant-everything — `pred_payload = P00`, `pred_boundaries = 0`, `pred_lock_conf = 0.5`                  | ≈ 0.35         |
> | Per-pair majority payload + all-zero boundaries + base-rate lock                                          | ≈ 0.43         |
> | Strong seq2seq Transformer that learns regime structure but not lock-state                                | ≈ 0.55–0.65    |
> | Same plus a calibrated lock-state head that aggregates L-stream features                                  | ≈ 0.62–0.70    |
> | Same plus a regime-boundary head trained on payload-statistics features                                   | ≈ 0.70–0.80    |
> | Oracle on hidden regime + oracle lock counter, capped by test-side noise                                  | ≈ 0.95         |
> Structural failures force the final score to 0.0:
> | Failure mode                                                                                                                              |
> |-------------------------------------------------------------------------------------------------------------------------------------------|
> | Missing any required submission column — `stream_id`, `pred_payload`, `pred_boundaries`, `pred_lock_conf`.                                 |
> | Duplicate `stream_id` values in submission or answers.                                                                                    |
> | Submission length not matching the number of test streams.                                                                                |
> | Set of `stream_id` values not exactly matching the set in `test.csv`.                                                                     |
> | Any NaN or missing value in any required column.                                                                                          |
> | Any unhandled exception raised during grading.                                                                                            |
> Per-row errors — wrong-length `pred_payload`, wrong-length `pred_boundaries`, non-0/1 boundary tokens, or `pred_lock_conf` outside `[0, 1]` — zero out the affected row's score on the affected term but do not zero the leaderboard score. Other valid rows still contribute.
> ### Dataset
> The `public/` directory shipped to solvers is summarised in the next table.
> | File                            | Rows         | Columns                                                                                  |
> |---------------------------------|--------------|------------------------------------------------------------------------------------------|
> | `public/train.csv`              | 9,600        | `stream_id`, `length`, `l_tokens`, `r_tokens`, `true_payload`, `true_boundaries`, `true_lock_state`. |
> | `public/test.csv`               | 2,400        | `stream_id`, `length`, `l_tokens`, `r_tokens`. No label columns.                          |
> | `public/sample_submission.csv`  | 2,400        | `stream_id`, `pred_payload`, `pred_boundaries`, `pred_lock_conf`. Placeholder baseline.   |
> Training-data columns in `public/train.csv`:
> | Column              | Type           | Description                                                                                                  |
> |---------------------|----------------|--------------------------------------------------------------------------------------------------------------|
> | `stream_id`         | int            | Identifier of one stream. Seeded permutation; unrelated to upstream row order.                              |
> | `length`            | int            | Number of pair-positions in the stream. Range 24–64.                                                         |
> | `l_tokens`          | string         | Space-separated `L` glyphs. `length` tokens drawn from `L00..L15`.                                          |
> | `r_tokens`          | string         | Space-separated `R` glyphs. `length` tokens drawn from `R00..R15`.                                          |
> | `true_payload`      | string         | Space-separated payload glyphs. `length` tokens drawn from `P00..P23`. About 10 % of training tokens are randomly perturbed. |
> | `true_boundaries`   | string         | Space-separated 0/1 tokens. 1 marks a regime change at position `t`. About 5 % of training labels are flipped. |
> | `true_lock_state`   | int            | 0 or 1, indicating whether the stream ends in the locked state. About 5 % of training labels are flipped.    |
> Test-data columns in `public/test.csv`:
> | Column        | Type   | Description                                                       |
> |---------------|--------|-------------------------------------------------------------------|
> | `stream_id`   | int    | Stream identifier.                                                |
> | `length`      | int    | Number of pair-positions in the stream.                           |
> | `l_tokens`    | string | Space-separated `L` glyphs. `length` tokens.                       |
> | `r_tokens`    | string | Space-separated `R` glyphs. `length` tokens.                       |
> Stream-level details:
> | Aspect                     | Detail                                                                                                                  |
> |----------------------------|-------------------------------------------------------------------------------------------------------------------------|
> | Length distribution        | Uniform over 24–64 inclusive.                                                                                          |
> | `L` vocabulary             | 16 symbols, `L00` through `L15`. A small unknown subset are positive lock triggers; a smaller subset are negative.      |
> | `R` vocabulary             | 16 symbols, `R00` through `R15`. Disjoint from the `L` vocabulary.                                                      |
> | Payload vocabulary         | 24 symbols, `P00` through `P23`.                                                                                       |
> | Number of hidden regimes   | 8. Each regime is a fixed lookup table over the 256 possible `(L, R)` pairs.                                            |
> | Regime-change rate         | About 6 % of positions. Boundaries are not annotated; only their effect on payload distributions is observable.        |
> | Lock state                 | Determined by an unknown integer threshold against the cumulative `pos_triggers − neg_triggers` count over the stream.  |
> Label-noise details — the irreducible error floor:
> | Source                          | Effect                                                                                                       |
> |---------------------------------|--------------------------------------------------------------------------------------------------------------|
> | Training payload noise          | About 10 % of tokens in `true_payload` are independently flipped to a random different payload glyph.         |
> | Training boundary noise         | About 5 % of tokens in `true_boundaries` are independently flipped.                                          |
> | Training lock noise             | About 5 % of `true_lock_state` values are independently flipped.                                              |
> | Test-side payload noise         | About 8 % of payload tokens in `private/answers.csv` are independently flipped.                              |
> | Test-side boundary noise        | About 5 % of boundary tokens in `private/answers.csv` are independently flipped.                              |
> | Test-side lock noise            | About 5 % of lock-state values in `private/answers.csv` are independently flipped.                            |
> | Effect                          | Even an oracle solver on the underlying regime structure tops out near 0.92 token accuracy and ≈ 0.85 boundary macro-F1, not 1.0. |
> ### Submission
> Submit a CSV file `submission.csv` with exactly four columns.
> | Column            | Type           | Description                                                                                                |
> |-------------------|----------------|------------------------------------------------------------------------------------------------------------|
> | `stream_id`       | int            | Stream identifier taken from `public/test.csv`.                                                            |
> | `pred_payload`    | string         | Space-separated payload tokens. Must contain exactly `length` tokens, each from `P00..P23`.                 |
> | `pred_boundaries` | string         | Space-separated 0/1 tokens. Must contain exactly `length` tokens.                                          |
> | `pred_lock_conf`  | float          | Calibrated probability of locked state, in `[0, 1]`.                                                       |
> Example — first three rows of a valid submission. Lengths and tokens shown are illustrative.
> ```csv
> stream_id,pred_payload,pred_boundaries,pred_lock_conf
> 0,P03 P11 P00 P14 P02 P19 P07,0 0 0 1 0 0 0,0.78
> 1,P05 P05 P12 P12 P00 P00,0 0 1 0 0 0,0.21
> 2,P22 P10 P10 P03 P19 P19 P11 P11,0 0 0 0 1 0 0 0,0.55
> ```
> Requirements:
> | Requirement                                                                                                                            |
> |----------------------------------------------------------------------------------------------------------------------------------------|
> | Must contain exactly 2,400 rows — one per test stream — plus a header row.                                                             |
> | `stream_id` values must be unique and exactly match the set in `public/test.csv`.                                                      |
> | `pred_payload` must be a single string of space-separated tokens, with exactly `length` tokens, each from the payload vocabulary `P00..P23`. |
> | `pred_boundaries` must be a single string of space-separated 0/1 tokens, with exactly `length` tokens.                                  |
> | `pred_lock_conf` must be a finite float in `[0, 1]`. Values outside this range zero out the lock term for that row.                     |
> | Extra columns beyond the four required are ignored.                                                                                     |
> ## GPU Tier
> A10G — standard ML workload, e.g. a small Transformer encoder-decoder or a token-tagging model. Training on 9,600 streams of average length 44 fits comfortably in A10G memory. H100 is reserved for LLM training and fine-tuning challenges, which this is not.
> ## Grading Configuration
> - **Grade direction**: Maximize — higher is better
> - **Theoretical minimum**: 0.0
> - **Theoretical maximum**: 1.0
> ## Grading Script
> ```python
> import pandas as pd
> REQUIRED_SUB_COLS = {
> "stream_id",
> "pred_payload",
> "pred_boundaries",
> "pred_lock_conf",
> }
> REQUIRED_ANS_COLS = {
> "stream_id",
> "length",
> "true_payload",
> "true_boundaries",
> "true_lock_state",
> }
> W_PAYLOAD = 0.45
> W_BOUNDARY = 0.30
> W_LOCK = 0.25
> def _payload_accuracy(pred: str, true: str, length: int) -> float:
> pred_toks = str(pred).split()
> true_toks = str(true).split()
> if len(pred_toks) != length or len(true_toks) != length:
> return 0.0
> if length == 0:
> return 0.0
> correct = sum(1 for p, t in zip(pred_toks, true_toks) if p == t)
> return correct / length
> def _boundary_macro_f1(pred: str, true: str, length: int) -> float:
> pred_toks = str(pred).split()
> true_toks = str(true).split()
> if len(pred_toks) != length or len(true_toks) != length:
> return 0.0
> pred_int = []
> for tok in pred_toks:
> if tok not in ("0", "1"):
> return 0.0
> pred_int.append(int(tok))
> true_int = [int(t) for t in true_toks]
> f1s = []
> for cls in (0, 1):
> tp = sum(1 for p, t in zip(pred_int, true_int) if p == cls and t == cls)
> fp = sum(1 for p, t in zip(pred_int, true_int) if p == cls and t != cls)
> fn = sum(1 for p, t in zip(pred_int, true_int) if p != cls and t == cls)
> if tp + fp == 0 and tp + fn == 0:
> f1s.append(1.0)
> continue
> prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
> rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
> if prec + rec == 0:
> f1s.append(0.0)
> else:
> f1s.append(2 * prec * rec / (prec + rec))
> return sum(f1s) / len(f1s)
> def _lock_score(pred_conf: float, true_state: int) -> float:
> try:
> p = float(pred_conf)
> except (TypeError, ValueError):
> return 0.0
> if p != p:
> return 0.0
> if p < 0.0 or p > 1.0:
> return 0.0
> t = int(true_state)
> return 1.0 - (p - t) ** 2
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if not REQUIRED_SUB_COLS.issubset(submission.columns):
> return 0.0
> if not REQUIRED_ANS_COLS.issubset(answers.columns):
> return 0.0
> sub = submission[
> ["stream_id", "pred_payload", "pred_boundaries", "pred_lock_conf"]
> ].copy()
> if sub["stream_id"].duplicated().any():
> return 0.0
> if answers["stream_id"].duplicated().any():
> return 0.0
> if len(sub) != len(answers):
> return 0.0
> if set(sub["stream_id"]) != set(answers["stream_id"]):
> return 0.0
> if sub.isna().any().any():
> return 0.0
> merged = answers.merge(sub, on="stream_id", how="left")
> if merged.isna().any().any():
> return 0.0
> scores = []
> for _, row in merged.iterrows():
> length = int(row["length"])
> pa = _payload_accuracy(row["pred_payload"], row["true_payload"], length)
> bf = _boundary_macro_f1(row["pred_boundaries"], row["true_boundaries"], length)
> ls = _lock_score(row["pred_lock_conf"], row["true_lock_state"])
> stream_score = W_PAYLOAD * pa + W_BOUNDARY * bf + W_LOCK * ls
> scores.append(max(0.0, min(1.0, stream_score)))
> if not scores:
> return 0.0
> final = sum(scores) / len(scores)
> return float(max(0.0, min(1.0, final)))
> except Exception:
> return 0.0
> ```
> ## What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.
> * **Hand-crafted rule programs that don't actually learn from data.** Solutions that hard-code a regex cascade, decision tree, or symbolic search program over `l_tokens` and `r_tokens` to recover the regime tables, lock triggers, or boundary positions — without training a model on the supervised pairs in `public/train.csv` — are not valid. The goal is to advance learned multi-output sequence reasoning, not to re-implement a brute-force enumerator. Predictions must come from a trained model that consumes the actual stream tokens.
> * **Recovering or re-running the generator.** Reverse-engineering the generation procedure, recovering the random seed, running an equivalent generator to obtain ground-truth payloads or lock states, or otherwise reconstructing the test labels from anything other than the provided `public/` files is prohibited. Solvers must work only from `public/train.csv` and `public/test.csv`.
> * **Brute-force regime-table enumeration on the test set.** Searching the 8! permutations of regime indices on test sequences to find the assignment that maximises self-consistency, without using a learned model, is not a valid solution. Inducing regime structure must be done implicitly through training, not via combinatorial search at inference time on the unlabeled test set.
> * **Hosted or closed-source API models** at any stage of training or inference — OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, and similar — and any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
> * **Test-set leakage during model selection.** Using `test.csv` token statistics, `stream_id`s, or any other test-set property to choose models, engineer features, or tune hyper-parameters is prohibited. All model selection must be done by cross-validation on `public/train.csv` only.
> * **Brute-forcing the test set or leaderboard probing.** Large numbers of submissions crafted to binary-search the private answers, or any strategy whose effectiveness depends on repeated scoring of probe submissions, is prohibited.
> * **Grader or platform exploitation.** Hard-coded `stream_id → output` dictionaries, filesystem probes for the private answers file, attempts to read or import `private/answers.csv`, or any channel other than `public/train.csv` and `public/test.csv` is prohibited.
> * **Ensembles mixing allowed and prohibited components.** An ensemble is allowed only if every component is itself trained — or used zero-shot — within the rules above. One prohibited component contaminates the whole ensemble.

Inspiration note: Useful as a rule-inference benchmark pattern where solvers must learn the hidden grammar or simulator from generated examples.

## Ironhold Rulebook Interpreter accepted best one till date
- Challenge URL: https://drive.google.com/drive/folders/1KfhOfwVZjKqqEiA1sNi-GEd5z7p3DUG9
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: From Scratch (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Ironhold Rulebook Interpreter_accepted_best_one_till_date from shared Google Drive folder

Full challenge description from Drive:

> # Challenge Form Fill
> **Status:** ⭐ **Done & accepted** — author-marked reference challenge (this folder is the canonical package).
> ## Difficulty
> Hard
> ## Challenge Title
> Ironhold Tri-Board Tactical Sequence Resolution
> ## Tags
> text, reasoning, fine-tuning
> ## Problem Description
> ### Overview
> Ironhold is a fictional tri-board tactical game played on a 5 × 5 × 3 stacked board (three independent layers of a 5 × 5 grid). Six fictional piece types — Sovereign, Warder, Scout, Shadewalker, Phaser, and Striker — interact through a novel rule system that does not appear in any pre-training corpus; the rules can only be inferred from the 4,125 training examples. Each example gives you a starting position (8–12 pieces spread across the three layers, the current turn number, and the side to move), a forced 4-ply move sequence (two White moves and two Black moves, in order), and a *tracked piece* — the piece White moves on Ply 1. Your task is to simulate the 4 plies through the hidden rule system and predict the **final fate of the tracked piece** as one of four labels: `FATE_L1`, `FATE_L2`, `FATE_L3` (still on the board, on the given layer) or `FATE_CAPTURED` (captured during plies 1–4).
> This is a fine-tuning challenge: the final prediction for every test row must come from a fine-tuned open-weights language model (e.g., Phi-3-mini, Llama-3.2-3B, Qwen2.5-3B, or any larger open-weights model that fits the GPU tier and time limit). See **What Not To Use** at the bottom of this form for the full list of prohibited approaches.
> ### Evaluation
> Submissions are scored using **macro-averaged F1** across the four label classes. Higher is better; minimum 0.0, maximum 1.0. Any malformed submission (wrong columns, duplicated `question_id`s, missing / unseen IDs, or labels outside the four-class set) scores 0.0.
> ```python
> def evaluate(y_true, y_pred):
> classes = ["FATE_L1", "FATE_L2", "FATE_L3", "FATE_CAPTURED"]
> f1s = []
> for c in classes:
> tp = sum(1 for t, p in zip(y_true, y_pred) if t == c and p == c)
> fp = sum(1 for t, p in zip(y_true, y_pred) if t != c and p == c)
> fn = sum(1 for t, p in zip(y_true, y_pred) if t == c and p != c)
> if tp == 0 and fp == 0 and fn == 0:
> continue
> prec = tp / (tp + fp) if (tp + fp) else 0.0
> rec = tp / (tp + fn) if (tp + fn) else 0.0
> f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
> f1s.append(f1)
> return sum(f1s) / len(f1s) if f1s else 0.0
> ```
> Training labels contain ≈ 10 % uniform label noise; test labels are clean, so the theoretical maximum on the test set is 1.0.
> ### Dataset
> The `public/` directory contains three CSV files.
> | File | Rows | Description |
> |------|------|-------------|
> | `train.csv` | 4,125 | `question_id`, `situation`, `label`. Labels contain ≈ 10 % noise. |
> | `test.csv` | 1,375 | `question_id`, `situation`. No labels. |
> | `sample_submission.csv` | 1,375 | Placeholder submission with a default label. |
> | Column | Type | Description |
> |--------|------|-------------|
> | `question_id` | int | Unique identifier, matches between `test.csv` and the submission. |
> | `situation` | str | Single text block containing the starting position across the 3 layers, the 4-ply move sequence, and the description of the tracked piece. |
> | `label` | str | One of `FATE_L1`, `FATE_L2`, `FATE_L3`, `FATE_CAPTURED`. |
> **Coordinate notation.** Every square is written `L<layer>:<file><rank>` (e.g. `L2:e3`). The board has three stacked layers (`L1`, `L2`, `L3`), and each layer is an independent 5 × 5 grid with files `a`–`e` and ranks `1`–`5`. The layer prefix is part of the square's identity, not a decoration: **`L2:e3` and `L3:e3` are two distinct squares** on different layers, and a piece on one of them does not collide with or block a piece on the other. Two pieces share a square only when the full `L<layer>:<file><rank>` string matches.
> **Situation format (verbatim example):**
> ```
> Starting position (turn 6, WHITE to move):
> L1: W-Warder@a3, B-Scout@c2
> L2: W-Sovereign@c1, W-Striker@e3, B-Phaser@b4
> L3: W-Scout@d2, B-Shadewalker@a1, B-Sovereign@d4, B-Warder@c3
> Move sequence to resolve (play all 4 plies in order):
> Ply 1. WHITE: Scout L3:d2 -> L3:e3
> Ply 2. BLACK: Shadewalker L3:a1 -> L2:b2
> Ply 3. WHITE: Striker L2:e3 -> L2:e5
> Ply 4. BLACK: Phaser L2:b4 -> L2:b3
> Tracked piece: the piece WHITE moves on Ply 1 (a Scout starting at L3:d2).
> Report its FINAL status after all 4 plies are resolved: its layer if still
> on the board, or CAPTURED.
> ```
> In this example, Ply 1 sends the tracked Scout to `L3:e3` (layer 3) while the White Striker remains on `L2:e3` (layer 2); those are different squares on different layers, so the Scout's move is not blocked and is not a capture.
> ### Submission
> Submit a CSV file with the following format:
> | Column | Type | Description |
> |--------|------|-------------|
> | `question_id` | int | Identifier from `test.csv`. |
> | `label` | str | One of `FATE_L1`, `FATE_L2`, `FATE_L3`, `FATE_CAPTURED`. |
> **Requirements:**
> - Must contain exactly 1,375 rows (one per test sample) plus a header row.
> - `question_id` values must be unique and must exactly match the set in `test.csv`.
> - Every `label` must be one of the four allowed values.
> - Any violation causes the grader to return 0.0.
> ## GPU Tier
> A10G — single-GPU fine-tuning of an open-weights language model (e.g., QLoRA / LoRA on Phi-3-mini, Llama-3.2-3B, Qwen2.5-3B, or any other open-weights checkpoint that fits the 24 GB memory budget and the platform time limit).
> ## Grading Configuration
> - **Grade direction**: Maximize (higher is better)
> - **Theoretical minimum**: 0.0
> - **Theoretical maximum**: 1.0
> ## Grading Script
> ```python
> import pandas as pd
> CLASSES = ["FATE_L1", "FATE_L2", "FATE_L3", "FATE_CAPTURED"]
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if not {"question_id", "label"}.issubset(submission.columns):
> return 0.0
> if not {"question_id", "label"}.issubset(answers.columns):
> return 0.0
> if submission["question_id"].duplicated().any():
> return 0.0
> if len(submission) != len(answers):
> return 0.0
> if set(submission["question_id"]) != set(answers["question_id"]):
> return 0.0
> merged = answers.merge(
> submission, on="question_id", how="left", suffixes=("_true", "_pred")
> )
> if merged["label_pred"].isna().any():
> return 0.0
> allowed = set(CLASSES)
> if not set(merged["label_pred"].astype(str).unique()).issubset(allowed):
> return 0.0
> y_true = merged["label_true"].astype(str).tolist()
> y_pred = merged["label_pred"].astype(str).tolist()
> f1s = []
> for cls in CLASSES:
> tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
> fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
> fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
> if tp == 0 and fp == 0 and fn == 0:
> continue
> prec = tp / (tp + fp) if (tp + fp) else 0.0
> rec = tp / (tp + fn) if (tp + fn) else 0.0
> f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
> f1s.append(f1)
> if not f1s:
> return 0.0
> macro_f1 = sum(f1s) / len(f1s)
> return float(max(0.0, min(1.0, macro_f1)))
> except Exception:
> return 0.0
> ```
> ## What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.
> * **Hand-coded rule-based or symbolic simulators.** Manually inferring Ironhold's movement / freeze / ward / capture rules from the training examples and implementing them as a deterministic Python / regex / finite-state simulator whose output is used — directly, as a feature, as a teacher, or as an ensemble component — to produce test-row labels. This bypasses the fine-tuning requirement.
> * **Tabular or non-LLM classifiers as the prediction head.** XGBoost, LightGBM, CatBoost, random forests, logistic regression, SVMs, k-NN, MLPs, TabPFN, or any other classifier over hand-engineered features that is not a fine-tuned open-weights LLM.
> * **Zero-shot or few-shot prompting with no parameter update.** In-context examples on an off-the-shelf pretrained LLM do not satisfy the fine-tuning requirement; the model's parameters (base or LoRA / QLoRA adapter) must be updated on `train.csv`.
> * **Closed-source or hosted-API models** at any stage of training or inference (OpenAI, Anthropic, Google, Mistral-API, xAI, Cohere, etc.), and any distillation from such teachers.
> * **External Ironhold data.** The game is fictional; the only valid rule source is `train.csv`. No scraping, no synthetic games from an external model, no hand-written rulebook paraphrased into extra training rows.
> * **Ensembles mixing allowed and prohibited components.** An ensemble is allowed only if every component is itself a fine-tuned open-weights LLM trained on `train.csv`.
> * **Grader / platform exploitation** (hard-coded answer dictionaries, filesystem probes for the private answers file, etc.).

Inspiration note: Useful as a rule-inference benchmark pattern where solvers must learn the hidden grammar or simulator from generated examples.

## Private Token Cloze Modeling For Low-Resource Dialect Text
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7177x3etckxf80xmn4kzpq7d89q7zf
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Train a language model from scratch on a low-resource dialect corpus written with private token IDs, then answer four-option cloze questions from held-out documents.
> The public corpus is not ordinary web text. Before release, each whitespace-delimited source token was consistently recoded into a private fixed-length token ID. Sequence order is preserved within each line, but the original script, source token strings, and source token lengths are not exposed. This keeps the task focused on learning distributional structure from the supplied corpus rather than relying on pretrained tokenizers, web lookup, or phrase matching.
> Every test item asks you to choose the correct option letter A, B, C, or D. The distractors are in-vocabulary tokens matched to the correct answer by training frequency, and all public tokens have the same fixed-length surface form, so simple frequency, length, or option-position rules should stay close to random guessing.
> Dataset
> The public data contains three files.
> corpus.txt
> Training corpus for from-scratch language modeling.
> Field	Type	Description
> line	string	One recoded text line. Private token IDs are separated by spaces. This is the only text corpus allowed for training.
> test.jsonl
> Four-option cloze questions, one JSON object per line.
> Field	Type	Description
> item_id	string	Unique question identifier.
> kind	string	Question type: two_sided_blank, window_blank, or next_word.
> input_text	string	Recoded private-token context containing [BLANK] for fill-in questions or [NEXT] for next-word questions.
> option_a	string	Candidate answer for label A.
> option_b	string	Candidate answer for label B.
> option_c	string	Candidate answer for label C.
> option_d	string	Candidate answer for label D.
> Question types:
> two_sided_blank: one interior token is replaced by [BLANK]; context appears on both sides.
> window_blank: a local context window is shown around [BLANK].
> next_word: the line is truncated at [NEXT]; choose the next token.
> sample_submission.csv
> Example submission file.
> Column	Type	Description
> item_id	string	Must match every item_id in test.jsonl exactly once.
> answer	string	Predicted option letter: A, B, C, or D.
> Submission Format
> Submit a CSV with exactly these columns:
> item_id,answer
> POC_001122aabbcc,B
> POC_ffeeddccbbaa,A
> POC_abcdef123456,D
> Requirements:
> The file must contain exactly the columns item_id,answer.
> There must be exactly one row for every test item_id.
> Missing IDs, extra IDs, duplicate IDs, null values, extra columns, and invalid answer labels are rejected.
> answer is case-insensitive after whitespace stripping, but must be one of A, B, C, or D.
> Evaluation
> Submissions are scored with a bounded categorical metric in [0, 1], where higher is better.
> For every item:
> Correct_i = 1 if predicted answer letter equals the private answer letter, else 0
> The grader computes these accuracy terms:
> Metric	Definition
> OverallAccuracy	Mean of Correct_i over all test items.
> RareTokenAccuracy	Mean of Correct_i over hidden items whose answer token is rare in the training corpus.
> LongContextAccuracy	Mean of Correct_i over hidden items requiring longer two-sided context.
> NextWordAccuracy	Mean of Correct_i over next_word items.
> OrthographyStressAccuracy	Mean of Correct_i over hidden items whose original tokens had difficult orthographic patterns before private recoding.
> WorstTrackAccuracy	Minimum of RareTokenAccuracy, LongContextAccuracy, NextWordAccuracy, and OrthographyStressAccuracy.
> The final score is:
> Score =
> 0.35 * OverallAccuracy
> + 0.20 * RareTokenAccuracy
> + 0.15 * LongContextAccuracy
> + 0.15 * NextWordAccuracy
> + 0.10 * OrthographyStressAccuracy
> + 0.05 * WorstTrackAccuracy
> The weights sum to 1.00. Hidden tracks can overlap by design; each displayed term is included exactly once in the final formula.
> Random guessing is expected to score near 0.25. Strong solutions should train a compact model from random initialization on corpus.txt, then score each option in context.
> Allowed And Prohibited Methods
> Allowed:
> Training any model architecture from random initialization on corpus.txt.
> Fitting a tokenizer only on corpus.txt, or using a deterministic byte-level, character-level, or whitespace tokenizer.
> Self-supervised objectives derived only from corpus.txt, such as next-token prediction, masked-token prediction, span infilling, or contrastive option scoring.
> Rule-based preprocessing and postprocessing derived only from the public files.
> Prohibited:
> Pretrained language models, pretrained embeddings, externally fit tokenizers, or hosted LLM APIs.
> Any external corpus, dictionary, web text, source-text lookup, translation system, or phrase-matching system.
> Attempting to recover the original public source documents or map the private token IDs back to the source script.
> Hardcoded answer tables, item-ID lookup systems, row-order shortcuts, or any signal from private answer files.
> Submissions with missing IDs, duplicate IDs, extra IDs, extra columns, invalid labels, or null values.

Inspiration note: Useful as a from-scratch benchmark pattern where solvers must learn task-specific structure directly from the provided data rather than relying on retrieval or pretrained shortcuts.

## Diatoms in the Wild: Open-World Census
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7enwvz8fh65vfjc7zqrjvz6d89esy0
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, large-scale, feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Diatoms are single-celled photosynthetic microalgae whose chloroplasts power much of the primary production in rivers and lakes, and whose silica shells are read under the microscope to assess water quality. A working analyst never sees a clean, closed list of species: slides come from new sites, specimens lie at every orientation in a litter of debris, and a fraction of what appears belongs to taxa the analyst was never trained on.
> This is a real light-microscopy corpus (acid-cleaned freshwater diatom frustules; no synthetic images). Your task is an open-world census: for every specimen in the test set, predict its species, or output novel_taxon if you judge it to belong to a genus that is not present in the training data. The test set is drawn from source slides that never appear in training, so models that lean on slide-specific staining, focus, or background cues will not transfer.
> You are scored not on raw accuracy but on a taxonomy-aware, class-balanced metric: naming the exact species is best, but getting the genus or the broad morphology right earns partial credit, and every species — common or rare — and the novel class all count equally. Trivial constant guesses score near the floor; the skill is in the long tail and in telling genuinely unfamiliar specimens apart from familiar ones.
> What makes this unusual is that these demands are coupled into one task and one score. Three choices set this apart from a standard fine-grained image classifier and shape what a good solution looks like. The label set is intentionally incomplete, so unfamiliar taxa must be flagged rather than forced into a known class. Training and test specimens share no source slide, so an in-distribution validation split will flatter you and mistune your thresholds. And credit follows the species → genus → morphology hierarchy, so a careful near-miss is worth far more than a confident wrong guess.
> Evaluation
> Let each test specimen have a true label t (a species name, or novel_taxon) and your predicted label p. The per-specimen credit is a taxonomy similarity s(p, t):
> 1.00 — exact match (p == t), including correctly predicting novel_taxon.
> 0.60 — p and t are different species of the same genus.
> 0.35 — p and t are different genera of the same morphology type.
> 0.10 — p and t are real species of different morphology types.
> 0.00 — exactly one of p, t is novel_taxon (a missed or false novelty call), or p is a non-empty but unrecognised label string.
> The final score is the macro average of s over true classes: the mean credit is computed within each true label, and then averaged across the classes present in the test set (the known species plus novel_taxon). Macro averaging is why a constant or most-frequent guess cannot farm points on the abundant species. The score lies in [0, 1]; higher is better; a perfect submission scores 1.0.
> The exact metric (this is the grader, verbatim in spirit):
> Python
> SAME, GENUS_SIM, TYPE_SIM, ELSE_SIM = 1.0, 0.60, 0.35, 0.10
> # TAXONOMY[label] = (genus, type_id) for every known species; "novel_taxon" is special.
> def s(p, t):
> if t == "novel_taxon" or p == "novel_taxon":
> return SAME if p == t else 0.0
> if p not in TAXONOMY:            # blank / unknown string
> return 0.0
> if p == t:
> return SAME
> gp, yp = TAXONOMY[p]
> gt, yt = TAXONOMY[t]
> if gp == gt:  return GENUS_SIM
> if yp == yt:  return TYPE_SIM
> return ELSE_SIM
> def evaluate(y_true, y_pred):           # y_true, y_pred aligned by id
> import pandas as pd
> df = pd.DataFrame({"t": y_true, "p": y_pred})
> df["c"] = [s(p, t) for p, t in zip(df.p, df.t)]
> return float(df.groupby("t")["c"].mean().mean())   # class-balanced macro
> Dataset
> After preparation you receive a public/ folder:
> public/train/ — 43,528 grayscale PNG cutouts, one labelled specimen each, named <id>.png.
> public/train.csv — supervision and metadata for the training images:
> id (string) — matches public/train/<id>.png.
> label (string) — the species (one of 80 known species).
> genus (string) — genus of the species.
> type_id (integer) — broad morphology class from a fixed taxonomic key whose numbering is non-consecutive: training species fall into classes 1, 2, 4, 5, 6, and 7. There is no class 3 in this dataset — the gap is expected, not a typo.
> annotator (string) — expert who labelled it (Annotator 1 … Annotator 4).
> slide_id (integer) — source slide; provided for training so you can build slide-robust models. Test slide ids are deliberately withheld.
> public/test/ — 19,772 grayscale PNG cutouts named <id>.png, with no labels.
> public/test.csv — one column, id, listing the 19,772 ids you must predict.
> public/sample_submission.csv — a correctly formatted file whose prediction column is filled with randomly chosen valid labels. It exists only to demonstrate the exact required format; it is not a baseline and its score is not meaningful.
> The 80 known species are exactly the distinct values of train.csv.label. The test set contains those same species plus specimens of six entirely held-out genera, which you should label novel_taxon. Known and novel specimens come only from slides absent from training.
> Submission format
> A CSV with exactly two columns, id and prediction, and exactly 19,772 data rows — one for every id in public/test.csv.
> id — a test id; the set of ids must equal the test set exactly (no missing, extra, or duplicate ids). Order does not matter (scoring merges on id).
> prediction — either one of the 80 known species names (exactly as written in train.csv.label) or the literal string novel_taxon. Matching is case-sensitive and exact: the abstain label must be written novel_taxon in lower case exactly as shown (variants such as Novel_Taxon, NOVEL_TAXON, or novel taxon are not recognised and score 0), and species names must be copied verbatim. Every row must be filled; no blanks, no NaN.
> Example (the ids below are real test ids):
> Code snippet
> id,prediction
> DIA000005,Navicula lanceolata
> DIA000009,novel_taxon
> DIA000014,Achnanthidium minutissimum
> DIA000016,Nitzschia palea
> DIA000017,Achnanthidium minutissimum
> Requirements, stated as independent rules:
> Exactly two columns, id and prediction — no extra, missing, or renamed columns; a submission whose columns are not exactly these two is rejected.
> Exactly 19,772 rows plus a header, and the id set equals public/test.csv's id set exactly; any missing, extra, or duplicate id causes rejection.
> Every row must carry a non-empty prediction; a blank or NaN prediction anywhere causes the whole submission to be rejected.
> A non-empty prediction that is not a known species name and not novel_taxon is accepted but earns 0 credit for that specimen.
> A perfect submission scores 1.0.
> What not to use
> This challenge measures learning from the provided training images only.
> No pretrained weights and no external data — no ImageNet/CLIP/foundation-model weights, and no images, datasets, or annotations beyond the files provided in this challenge.
> Do not attempt to obtain labels for the test specimens from any outside source.
> No network access at train or inference time and no runtime downloads.
> Do not read, infer, or reconstruct the answer key, and do not attempt to recover the preparation logic, the seed, or slide_id for test specimens.
> Standard augmentation, self-supervision, and open-set methods on the provided training set are encouraged.

Inspiration note: Useful as a from-scratch benchmark pattern where solvers must learn task-specific structure directly from the provided data rather than relying on retrieval or pretrained shortcuts.

## Sahidic Coptic Anomaly Localization: Language Modeling from Scratch
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73qdtwdvrsb7qy6ez4zevp9d89ptpz
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Coptic is the final stage of the ancient Egyptian language, written in an alphabet derived from Greek (plus a handful of Demotic-derived letters) and recorded across a rich monastic literature of sermons, letters, sayings, saints' lives, martyrdoms and homilies. It is an extinct, low-resource language with heavily prefixing morphology — article, tense, pronoun and conjugation morphemes attach as separate orthographic tokens around a content stem — and telling a well-fitting word from a subtly wrong one in a given context demands real command of Coptic vocabulary and usage.
> This challenge gives you a corpus of Sahidic Coptic literary text (~10,000 sentences, ~0.19M word tokens, in Coptic Unicode script) and asks you to train a language model from random initialization. At test time you are shown single sentences from held-out works the model has never seen; in each sentence exactly one content word has been replaced in place by a plausible impostor, and you must output the 0-based token index of that corrupted (fake) word. Modern pretrained models do not help — Coptic is essentially absent from mainstream pretraining data, and its tokenization fragments under modern English/byte tokenizers. The only path is training from scratch on the provided corpus.
> Task
> Anomaly localization, not cloze: there is no marked blank and no option list. You receive the whole corrupted sentence, space-tokenized, and must identify which token is the fake one by its index.
> Dataset
> corpus.txt — the training corpus: one sentence per line (~10,000 lines, ~0.19M word tokens, ~0.7M characters), drawn from non-biblical Coptic literary works. This is the only permitted training data.
> test.jsonl — 1,700 anomaly items, one JSON object per line, with fields:
> item_id (string) — unique identifier, e.g. COP_a1b2c3d4e5f6.
> sentence (string) — a sentence from a held-out work, space-tokenized, in which exactly one interior content word has been replaced by an impostor. The fake word is never the first or last token, so context is available on both sides.
> sample_submission.csv — a format example (a fixed baseline that predicts index 1 for every item; it scores far below a real model).
> In each sentence, exactly one content word (a noun, verb, adjective or adverb) is fake. The impostor was drawn from the training vocabulary to share the original word's grammatical ending (so it is morphologically plausible in the slot), to be matched to the original on corpus frequency (bracketing it above and below) and on local collocation with the words on either side (its training-corpus bigram counts with the neighbours bracket the original's), and to be absent from the rest of the sentence — so ending, frequency, length and local-bigram cues do not reveal which token is fake. Only modelling Coptic vocabulary and longer-range context does.
> Evaluation
> Submissions are scored by accuracy — the fraction of items whose predicted index matches the fake token's true index exactly:
> score = correct_predictions / 1700
> Score range [0, 1], higher is better. Random guessing over token positions scores ~0.06, and frequency / rarity / local-bigram heuristics stay near this floor because the impostor is matched to the word it replaced on ending, frequency, neighbour collocation, length and presence.
> Submission
> Submit a CSV at ./working/submission.csv with exactly two columns:
> item_id,answer
> COP_a1b2c3d4e5f6,7
> COP_b2c3d4e5f6a1,3
> Requirements (strict — the grader rejects a violating submission rather than repairing it):
> Exactly the two columns item_id, answer; no extra columns; no null/duplicate item_ids.
> One row for every test item_id — missing a required id (or a duplicate/null id) causes rejection; rows for ids outside the graded set are ignored.
> answer is a non-negative integer — the 0-based index of the predicted fake token into the space-split sentence. Null, non-integer, or negative values are rejected. An index that is out of range simply counts as wrong.
> Allowed and Prohibited Methods
> This is a from-scratch language-modeling challenge. Train a language model from random initialization on corpus.txt and use it to score each token position's contextual fit, then flag the worst-fitting position.
> Allowed:
> Training any language-model architecture (transformer, RNN, state-space, n-gram, etc.) from random initialization on corpus.txt.
> Any tokenizer fit on corpus.txt or defined by a deterministic rule: BPE, WordPiece, SentencePiece, byte-level, or character-level.
> Hybrid solutions combining a from-scratch model with deterministic rule-based pre/post-processing, and self-supervised objectives derived from the corpus (next-token, masked-LM, span infilling, per-position surprisal / pseudo-log-likelihood scoring).
> Prohibited (grounds for rejection on review, regardless of score):
> Pretrained models, embeddings, or tokenizers of any kind (including any multilingual or Coptic checkpoint). All weights must be randomly initialized at the start of training on corpus.txt; the tokenizer must be fit on the corpus or be a deterministic rule.
> Any external data — other Coptic corpora, dictionaries, lexicons, or word lists — at training or inference time, and matching the held-out sentences against any external edition of the source works to recover the original words and locate the fake one by difference.
> Frequency-only / rarity-only / local-bigram / surface heuristics that answer without a learned model; the impostor is matched to the word it replaced on ending, frequency, neighbour collocation, length and presence, so these stay near the ~0.06 floor.
> Hosted LLM APIs at training or inference; hand-labeling test items; hardcoded {item_id → answer} tables; or any signal derived from the private answer file.

Inspiration note: Useful as a from-scratch pattern where the dataset itself defines the modeling signal and solvers must learn the structure without retrieval or pretrained shortcuts.

## Recovering Masked Notes in a Corpus of Monophonic Modal Melodies
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ag931e7h3at8bjz6s23bah189svj5
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given a symbolic corpus of monophonic modal melodies -- single-line melodies drawn from a traditional modal music (the Persian/Iranian classical modal tradition). Each piece is an ordered sequence of notes. There are no chords and no simultaneous voices: at every step there is exactly one note. Each note is represented by its MIDI-semitone pitch (an integer, e.g. 60 for middle C), or by the token R for a rest. Durations, rhythm, lyrics, ornaments, and microtonal tuning have all been stripped away -- only the ordered pitch sequence remains.
> This music is organised around modes: each mode fixes a scale, a small set of characteristic melodic intervals, and typical cadential motion. The note-to-note grammar (which pitches tend to follow which, how a line ascends and descends, where it comes to rest) is a convention of the tradition that must be learned from the melodies themselves; there is no external table you may consult.
> In a held-out set of pieces, contiguous runs of consecutive notes have been masked out. Your task is to recover the true pitch of each masked note.
> Concretely, you must:
> Train a model from scratch on the provided training melodies, learning this tradition's melodic grammar -- its pitch-transition structure and mode-specific tendencies.
> For each query, predict the integer MIDI-semitone pitch of the masked note.
> You do not need to identify the mode of a piece, transcribe rhythm, or recover anything other than the raw pitch that was masked.
> Data
> train_stream.csv -- the training melodies, in note order. This is the only data you may train on. Columns:
> piece_id -- opaque id of the piece.
> position -- 0-based index of the note within its piece (in melodic order).
> pitch -- the note as an integer MIDI semitone, or R for a rest.
> test_stream.csv -- the held-out melodies (pieces that never appear in train_stream.csv), same columns and same note order. In this file every queried note has its pitch replaced by XX. All other notes are shown. The full ordered stream is provided so you can use the surrounding melodic context of each masked note -- the preceding and following notes of the same piece (with their own holes where they too are queried). Masks come in contiguous runs, so the interior of a masked run has no immediately adjacent unmasked note; recovering it requires modelling the melodic line across the gap, not copying a neighbour.
> test.csv -- the query items. Columns:
> item_id -- opaque unique id for the query.
> piece_id -- the piece the masked note belongs to.
> position -- the 0-based index of the masked note within that piece (its row in test_stream.csv).
> sample_submission.csv -- a valid submission with pitch = 60 for every item.
> Task
> For each item_id in test.csv, predict the integer MIDI-semitone pitch of the masked note at (piece_id, position) in the test stream.
> Evaluation
> Note accuracy -- the fraction of query items whose predicted integer pitch exactly matches the true masked note:
> accuracy = mean( predicted_pitch == true_pitch )   over all queried notes
> A prediction counts only on an exact integer MIDI-semitone match. Higher is better; the score is in [0, 1].
> Submission format
> A CSV with exactly two columns:
> item_id -- every item_id from test.csv, each exactly once.
> pitch -- your predicted note, an integer MIDI semitone.
> Example:
> item_id,pitch
> MEL_ade4e7d4c26e,55
> MEL_0b3d824bc723,62
> Requirements (violations are rejected as invalid submissions):
> Exactly the columns item_id,pitch, in that order.
> No missing, duplicate, or extra item_id; every required item_id present exactly once.
> pitch must be an integer MIDI semitone with no nulls.
> Allowed
> Training any model from scratch (random initialization) on train_stream.csv.
> Using the ordered test_stream.csv for melodic context at inference time (the preceding/following notes of the same piece).
> Any standard modelling approach fit on the provided melodies: n-gram / Markov models over the pitch sequence, sequence models (RNN/transformer/state-space)
> Prohibited
> No pretrained weights, symbolic-music embeddings, note-language-model checkpoints, or externally-fit tokenizers of any kind. The model must be trained from random initialization on the provided melodies only.
> No external symbolic-music data, MIDI or score corpora, scale/mode dictionaries, or online lookup of this or any related tradition's melodies or note layouts.
> Do not attempt to identify the source corpus and retrieve any external copy of it or its annotations.
> No use of any answer/label file; the masked notes must be predicted from the model.

Inspiration note: Useful because it rewards learning a hidden structure or model directly from the provided data rather than using pretrained shortcuts.

## Metal-Organic Framework CO2 Capture GNN Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74mb25jxhew77hkyn8acfd3d89s1y6
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Metal-Organic Frameworks (MOFs) are 3D crystalline materials built from metal nodes connected by organic linker molecules — inherently graph-structured data. With over 100,000 synthesized structures, MOFs represent one of the largest design spaces in materials chemistry and a leading platform for Direct Air Capture (DAC) of CO₂.
> This is a 3D graph learning challenge. You receive pre-built molecular graph descriptors (graph_nodes and graph_edges as JSON) — the linker's atomic structure encoded as node features and edge lists — plus supplementary structural context. From these you must:
> Load molecular graphs from JSON descriptors (atoms = nodes with features, bonds = edges with types)
> Encode 3D geometry through conformer generation (rebuild molecule from graph → generate 3D coords) and equivariant message-passing, or through scalar structural descriptors
> Design a message-passing architecture from scratch — no pretrained weights
> Solve an inverse screening problem — rank candidate MOFs by DAC fitness
> The Challenge
> Part 1 — Graph-Level Property Prediction (60% of score):
> Build a GNN that predicts four CO₂ capture targets from the linker molecular graph augmented with global crystal features:
> CO₂ uptake at 0.15 bar (mmol/g) — Direct Air Capture (DAC) at atmospheric CO₂ partial pressure
> CO₂ uptake at 1.0 bar (mmol/g) — post-combustion flue gas capture
> CO₂/N₂ selectivity — separation efficiency, range [1, 1000], evaluated in log10 space
> Heat of adsorption (kJ/mol) — regeneration energy, range [15, 60]
> Your GNN must learn the selectivity-heat trade-off: strong CO₂ binding improves selectivity but increases regeneration cost. This is the central structure-property relationship your message-passing architecture must disentangle.
> Part 2 — Inverse Screening (40% of score):
> A computational screening tool is only useful if it correctly identifies the best materials. A pool of 500 MOFs in test.csv tests exactly this: predict their properties, rank by DAC fitness, scored via NDCG@100:
> DAC_Fitness = co2_uptake_015bar × 1.0 + co2_uptake_1bar × 0.3
> + log10(co2_n2_selectivity) × 2.0 - heat_of_adsorption × 0.05
> Your ranking determines which MOFs get synthesized — prediction accuracy matters only insofar as it produces the correct ordering.
> Why MOFs for Carbon Capture?
> Direct Air Capture (DAC) is recognized by the IPCC as a critical technology for climate change mitigation. MOFs offer several advantages over traditional liquid amine scrubbing:
> Tunable pore geometry: Pore size can be engineered at the Angstrom level to selectively capture CO₂
> Open metal sites: Unsaturated metal centers act as strong CO₂ binding sites, enhancing selectivity
> Functional group chemistry: Amine, fluorine, and heterocycle groups can be incorporated into linkers to enhance CO₂ affinity
> Lower regeneration energy: Many MOFs require less energy to release captured CO₂ than amine scrubbing (~20-40 kJ/mol vs. 80-120 kJ/mol for aqueous amines)
> The Fundamental Trade-Off
> MOF design involves a classic materials optimization problem: high selectivity requires strong CO₂ binding, but strong binding increases regeneration energy. Your GNN must capture this trade-off — predicting both how well a MOF captures CO₂ AND how easily it releases it. The best predictions will correctly rank MOFs across all four targets simultaneously. This requires your architecture to learn representations that disentangle binding strength from structural capacity.
> Domain Background
> MOFs as Graphs
> A MOF is a crystalline material built from metal nodes connected by organic linkers. For this challenge, the linker's molecular graph is provided as pre-built JSON descriptors in two columns:
> **graph_nodes** (JSON): array of atom objects, each with z (atomic number), hyb (hybridization), deg (degree), aro (aromatic), chg (formal charge), ring (in ring), nh (implicit hydrogens)
> **graph_edges** (JSON): array of bond objects, each with src (source atom index), dst (destination atom index), typ (bond type: SINGLE, DOUBLE, TRIPLE, AROMATIC)
> Parse these JSON strings to construct your molecular graph. You may work in 2D graph space (molecular topology + global features) or generate 3D conformers for equivariant message passing. Both are valid.
> Equivariance
> This is the core architectural challenge. A rotation-equivariant function satisfies f(R·x) = R·f(x). For scalar property prediction, we need invariance: f(R·x) = f(x) — the prediction must not change when the MOF is rotated.
> Your options:
> Equivariant models need fewer examples to generalize because the symmetry is built in rather than learned.
> Dataset
> The dataset contains ~110,000 MOF data points (plus a 500-MOF held-out screening pool) with structural features, chemical properties, and CO₂ capture performance metrics. You receive approximately 83,200 training rows and 25,100 test rows (all MOF_TE_*; a 500-MOF subset forms the screening pool).
> Features Provided
> Identifier:
> mof_id (str) — Unique identifier
> Categorical Features:
> metal_type (str) — Metal node: Zn, Cu, Zr, Al, Fe, Cr, Mg, Co, Ni
> graph_nodes (str) — JSON array of atom descriptors for the organic linker (key for graph construction)
> graph_edges (str) — JSON array of bond descriptors for the organic linker
> functional_group (str) — Primary functional group category
> Structural Features:
> pore_volume_cm3g, surface_area_m2g, pore_diameter_angstrom
> void_fraction, density_gcm3, linker_length_angstrom
> Chemical Features:
> num_open_metal_sites (int), has_amine (0/1), has_fluorine (0/1), has_nitrogen_heterocycle (0/1)
> Prediction Targets (NOT in test.csv)
> co2_uptake_015bar (float) — CO₂ uptake at 0.15 bar (mmol/g) (real data)
> co2_uptake_1bar (float) — CO₂ uptake at 1.0 bar (mmol/g) (real data)
> co2_n2_selectivity (float) — CO₂/N₂ selectivity, range [1, 1000] (derived heuristic)
> heat_of_adsorption (float) — Isosteric heat of adsorption (kJ/mol), range [15, 60] (derived heuristic)
> Train/Test Split
> The dataset is split by molecular scaffold (ring-based core structure): all MOFs sharing the same core ring framework go entirely to train OR test — never both. This forces your model to generalize to chemically novel linker cores unseen during training (true out-of-distribution evaluation). The exact train/test ratio depends on scaffold size distribution but targets approximately 70/30. The split is deterministic.
> Graph Construction from Tabular Data
> The dataset is provided as CSV tables. Converting this into graph-structured input for your GNN is part of the challenge. The primary graph-building pathway:
> **Parse graph_nodes and graph_edges** JSON to obtain atom types, bond connectivity, and bond types
> Build node features: atom type embedding, chirality, formal charge, hybridization, aromaticity, ring membership
> Build edge features: bond type, conjugation, ring membership
> Attach global context: metal type, structural parameters, chemical flags as graph-level features or connected via a virtual super-node
> Structural features are synthetic descriptors of the crystal environment. The primary predictive signal is in the molecular graph.
> Evaluation — Composite MOF Performance Score
> Submissions are evaluated using a weighted composite score with two components:
> composite = 0.60 × forward_score + 0.40 × screening_score
> Forward Prediction (60% of composite)
> Balances prediction accuracy across all four targets and correct ranking of MOFs.
> The four sub-weights below sum to 1.0 within the forward_score (they are
> fractions of forward_score, not fractions of composite):
> forward_score = 0.417 × uptake_score + 0.250 × selectivity_score
> + 0.167 × heat_score  + 0.167 × ranking_score
> Equivalently, when expressed as fractions of the final composite:
> 0.25 × uptake + 0.15 × selectivity + 0.10 × heat + 0.10 × ranking.
> Component A: Uptake Score (0.417 of forward_score, 0.25 of composite)
> Combined accuracy across both CO₂ uptake targets:
> mae_015     = mean(|y_true_015 - y_pred_015|)
> mae_1       = mean(|y_true_1 - y_pred_1|)
> score_015   = max(0, 1 - mae_015 / ref_015)
> score_1     = max(0, 1 - mae_1 / ref_1)
> uptake_score = (score_015 + score_1) / 2
> Reference values: ref_015 ≈ 2.0 mmol/g, ref_1 ≈ 5.0 mmol/g.
> Component B: Selectivity Score (0.250 of forward_score, 0.15 of composite)
> CO₂/N₂ selectivity spans 3 orders of magnitude — errors are evaluated in log10 space (base-10 logarithm, matching np.log10 in the grader):
> log_mae     = mean(|log10(y_true_sel) - log10(y_pred_sel)|)
> selectivity_score = max(0, 1 - log_mae / ref_log_sel)
> Reference value: ref_log_sel ≈ 0.5 (half an order of magnitude error).
> Component C: Heat Score (0.167 of forward_score, 0.10 of composite)
> Heat of adsorption scored in linear space:
> mae_heat    = mean(|y_true_heat - y_pred_heat|)
> heat_score  = max(0, 1 - mae_heat / ref_heat)
> Reference value: ref_heat ≈ 10 kJ/mol.
> Component D: Ranking Score (0.167 of forward_score, 0.10 of composite)
> Average of per-target Spearman rank correlations. Rewards correct MOF ranking even if absolute values are off:
> ranking_score = mean(spearman_r_015, spearman_r_1, spearman_r_sel, spearman_r_heat)
> Spearman correlations range [-1, 1], clipped to [0, 1].
> Inverse Screening (40% of composite)
> Evaluates your model's ability to correctly rank a held-out pool of 500 MOFs by DAC fitness. Uses NDCG@100 (Normalized Discounted Cumulative Gain):
> For each MOF in screening pool:
> DAC_Fitness = uptake_015 × 1.0 + uptake_1 × 0.3
> + log10(selectivity) × 2.0 - heat × 0.05
> NDCG@100 = DCG_pred / DCG_ideal
> where DCG    = Σ(top-100 by predicted fitness) true_fitness_i / log2(i+1)
> IDCG   = Σ(top-100 by true fitness)      true_fitness_i / log2(i+1)
> NDCG@100 is in [0, 1]. A score of 1.0 means your model ranks the top 100 MOFs perfectly. A score near 0 means your ranking is effectively random. This metric rewards correct relative ordering — a model with systematic bias but perfect ranking can achieve NDCG@100 ≈ 1.0.
> Final Score
> Two equivalent forms — both weight sets sum to 1.0:
> Form 1 — grouped (forward_score sub-weights sum to 1.0):
> forward_score = 0.417 × uptake + 0.250 × selectivity
> + 0.167 × heat   + 0.167 × ranking     (sum = 1.00)
> composite     = 0.60 × forward_score + 0.40 × screening_score   (sum = 1.00)
> Form 2 — fully expanded (all 5 weights sum to 1.0):
> composite = 0.25 × uptake + 0.15 × selectivity + 0.10 × heat
> + 0.10 × ranking + 0.40 × screening              (sum = 1.00)
> composite = clamp(composite, 0.0, 1.0)
> All component scores are in [0, 1]. Form 2 is what the platform computes.
> Score Interpretation
> 0.80+ — World-class: near-perfect prediction AND perfect screening. Your GNN correctly identifies optimal MOFs for DAC. Demonstrates sophisticated equivariant design and multi-task learning.
> 0.65–0.80 — Excellent: accurate predictions and strong screening. GNN effectively learns structure-property relationships and relative ordering. Solid message-passing and readout.
> 0.50–0.65 — Good: solid on most targets with reasonable screening. Architecture is functioning. May have weaknesses on selectivity, heat, or ranking discrimination.
> 0.35–0.50 — Developing: basic GNN signal captured. Screening performance suggests the model captures some chemical trends but struggles with fine-grained ranking.
> 0.15–0.35 — Basic: some signal above random. Graph construction may be suboptimal or message passing too shallow. Screening near-random.
> 0.00–0.15 — Insufficient: near-random predictions across all components. Check graph construction (are graph_nodes/graph_edges JSON parsed correctly?), message-passing implementation, and training convergence.
> Score range: [0, 1]. Higher is better.
> Submission Format
> Submit a CSV file with your model's predictions for all four targets:
> Submission CSV must contain exactly five columns:
> mof_id (str) — Row identifier from test.csv
> co2_uptake_015bar (float) — Predicted CO₂ uptake at 0.15 bar (mmol/g)
> co2_uptake_1bar (float) — Predicted CO₂ uptake at 1.0 bar (mmol/g)
> co2_n2_selectivity (float) — Predicted CO₂/N₂ selectivity
> heat_of_adsorption (float) — Predicted heat of adsorption (kJ/mol)
> Example:
> mof_id,co2_uptake_015bar,co2_uptake_1bar,co2_n2_selectivity,heat_of_adsorption
> MOF_TE_04200,2.145,8.302,45.67,28.3
> MOF_TE_04201,1.893,7.891,32.10,24.7
> MOF_TE_04202,3.012,11.234,78.90,35.2
> Requirements:
> Exactly one row per mof_id from test.csv. The test.csv file contains approximately 25,100 rows (all MOF_TE_* prefix) — a subset of 500 forms the screening pool evaluated via NDCG@100. Submissions with missing, extra, or duplicate mof_ids score 0.0.
> All float values must be finite (no NaN, no Inf)
> Selective submission (submitting only a subset of mof_ids) is detected and rejected with score 0.0
> Rules
> Allowed
> Models:
> Custom GNN architectures of your own design and implementation
> Any message-passing paradigm: MPNN, GCN, GAT, GIN, GatedGCN, PNA
> Any equivariant GNN: SchNet, DimeNet, EGNN, Equiformer, PaiNN — implemented by you
> Any readout/pooling, multi-task head, or loss function
> Hybrid architectures: GNN encoder + MLP decoder, multiple GNN branches
> Training:
> Any optimizer (Adam, AdamW, SGD, LAMB, Ranger, etc.) and scheduler (cosine, plateau, one-cycle, warmup)
> Any loss function (MSE, MAE, Huber, log-cosh, quantile loss)
> Multi-task loss weighting strategies (uncertainty weighting, GradNorm, DWA, hand-tuned)
> Hyperparameter tuning (manual or automated — Optuna, Ray Tune, grid search)
> Cross-validation (k-fold, stratified, group)
> Data:
> Only the provided challenge data (train.csv, test.csv)
> Any cheminformatics processing using RDKit, Open Babel, or similar open-source toolkits
> Graph construction from graph_nodes/graph_edges JSON descriptors
> 3D conformer generation by rebuilding molecules from graphs (RDKit ETKDG or MMFF94)
> Feature engineering from the provided features (interaction terms, log transforms, metal property lookup from periodic table)
> Standard augmentations: node dropout (DropNode), edge dropout (DropEdge), random rotation of 3D conformers
> Ensembling:
> Ensemble of up to 5 independently trained models (different seeds, architectures, or hyperparameters)
> Cross-validation ensembles, checkpoint averaging, SWA (Stochastic Weight Averaging)
> Not Allowed
> Pretrained models:
> No pretrained GNN weights (no pretrained SchNet, DimeNet, EGNN, Equiformer, etc.)
> No molecular foundation models (no MolFormer, ChemBERTa, GROVER, Uni-Mol, MolCLR)
> No pretrained molecular fingerprints or atom embeddings from external corpora
> No transfer learning from other datasets (QM9, MD17, OC20, PCQM4Mv2)
> This is a FROM SCRATCH challenge — all weights must be randomly initialized and trained solely on the provided training data
> External resources:
> No external MOF databases or CO₂ adsorption datasets beyond the provided training data
> No API-based models (GPT-4, Claude, Gemini, or any LLM API) during inference
> No external retrieval or web search during inference
> Data integrity:
> No manual labeling of test data
> No training on test set data (data leakage)
> No synthetic data generation from external distributions
> No database lookup of recovered SMILES. Rebuilding RDKit molecules from the provided graph descriptors trivially recovers canonical SMILES (via Chem.MolToSmiles). That is expected and allowed for 3D conformer generation. What is prohibited: canonicalizing those SMILES and searching public MOF databases to retrieve ground-truth CO₂ uptake targets.
> No test-time adaptation or test-time training

Inspiration note: Useful because it rewards learning a hidden structure or model directly from the provided data rather than using pretrained shortcuts.

## Predicting Mutational Effects on Protein Folding Stability for Unseen Folds
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cbwhrjn04m54fjx4q62hf5989teft
- DOMAIN exactly as displayed: From Scratch
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering, large-scale, medical
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This is a from-scratch modeling challenge: you build and train a sequence model from the provided data alone - no pretrained protein language models, no predicted structures, no homology databases (see "What Not To Use"). The question is how much of a mutation's stability effect can be learned from the training measurements themselves, with honest sequence modeling, when the test folds are new.
> Whether a protein folds into a stable shape is set by its folding free energy. A single amino-acid substitution can nudge that stability up or down, and knowing by how much is central to protein engineering, enzyme design, and understanding how mutations cause disease. The quantity of interest is the change in folding free energy caused by a mutation, written ddG and measured in kcal/mol: a positive value means the mutation makes the protein more stable, a negative value means it destabilizes it, and most random substitutions are destabilizing.
> You are given small protein domains as their amino-acid sequences, together with single-point mutations and the experimentally measured ddG for each mutation. Your task is to predict ddG for mutations in new domains from sequence alone.
> What makes this hard is deliberate and real. The test domains are structurally novel: they belong to fold groups that do not appear anywhere in the training set, so a model cannot lean on a memorized family and must generalize to unfamiliar structure. You are given only the sequence, never the three-dimensional structure, yet the effect of a mutation depends heavily on whether the residue is buried in the core or exposed on the surface, which the sequence alone does not reveal. And the measurements carry genuine experimental noise. A strong model still leaves a large fraction of the variance unexplained; closing even part of that gap is the signal this challenge measures.
> What you predict
> For every row in the test set, predict a single value:
> ddg - the change in folding free energy caused by the mutation, in kcal/mol (positive = stabilizing, negative = destabilizing).
> Data
> train.csv - one row per training mutation: id, wt_sequence, position, wt_aa, mut_aa, ddg.
> test.csv - the same columns without ddg (you predict it).
> sample_submission.csv - the required output format: every test id with a placeholder ddg. It shows the format only and is not intended to score.
> Notes on the columns:
> id - an opaque 20-character hexadecimal identifier; it carries no information and must not be a feature.
> wt_sequence - the wild-type amino-acid sequence of the protein domain (one-letter codes), the unmutated background on which the mutation is applied.
> position - the 1-based index into wt_sequence of the mutated residue.
> wt_aa - the wild-type amino acid at that position (equals wt_sequence at position).
> mut_aa - the amino acid the residue is changed to.
> ddg - the prediction target. Where a mutation was measured more than once, the value is the median across replicate measurements.
> The training and test domains are disjoint by fold: every test domain belongs to a structural group that does not occur in the training set. Many mutations share the same wt_sequence because they were measured on the same domain.
> Submission format
> A CSV with columns id, ddg - one row per test id, matching test.csv. Example (ids and values are illustrative only):
> id,ddg
> 3f9a1c7b2e8d4a6c5f01,-0.42
> a07d2e91c4b8f33a1106,0.15
> 72fb6a05c83c8239cc1a,-1.87
> Over the N test mutations, let y[i] be the true ddg, p[i] your prediction, and mean_y the mean ddg of the test set (the MSE-optimal constant). Define:
> SSE = sum over i of ( p[i] - y[i] )^2
> SST = sum over i of ( mean_y - y[i] )^2
> R   = 1 - SSE / SST
> R is the standard coefficient of determination against the constant baseline. The variance-matching factor V compares the spread of your predictions to the spread of the true values, using the population standard deviation (dividing by N) over the N test mutations:
> V = min( 1 , std(p) / std(y) )
> final score = clip( R * V , 0.001 , 1.0 )
> What this means in practice:
> Predicting a constant (including the mean) gives R <= 0 and V = 0, so the score collapses to the 0.001 floor. You only gain from mutation-specific predictions that are genuinely closer than the best constant.
> A near-constant submission is scaled down by V; inflating spread artificially raises SSE and does not help, because V is capped at 1.
> A perfect copy scores 1.0. Because the test folds are unseen, the structure is withheld, and the measurements are noisy, even a strong model lands well below 1.0 - that is expected.
> A submission that is malformed - missing a required column, containing duplicate ids, not matching the set of test ids, or containing any non-numeric or non-finite prediction - is rejected, not scored.
> What Not To Use
> Do not use pretrained protein language models or their embeddings (for example ESM, ESM-2, ESM-3, ProtT5, ProtBERT, Ankh, CARP, or any model pretrained on external protein sequences). This challenge is about learning from the provided training measurements, not transferring from an external pretrained model.
> Do not use predicted or experimental three-dimensional structures, structure predictors (for example AlphaFold, ESMFold, RoseTTAFold), or structure databases (for example the PDB). The task is sequence-only by design.
> Do not use multiple-sequence alignments, homology search, or evolutionary/conservation databases (for example BLAST against UniProt, Pfam, or profile databases). Predict from the given single sequence.
> Do not look the mutation up in any external stability resource (for example the source mega-scale stability dataset, ProThermDB, FireProtDB, or any published ddG dataset) and copy its measured value. Retrieving a measured ddg is out of scope; this challenge is about predicting it.
> Do not use the id, the row order, or the file position as a feature; ids are opaque. Do not pool across the test set or try to reconstruct the fold split; predict each mutation independently from its own row.
> Intended approach: train a sequence-to-stability model on the provided training mutations from scratch - hand-built local sequence features with a gradient-boosted or linear model, or a neural network (convolutional, recurrent, or attention based) trained only on this training set - and validate it on a fold-disjoint slice of the training domains so your local score reflects the unseen-fold test setting.

Inspiration note: Useful because it rewards learning a hidden structure or model directly from the provided data rather than using pretrained shortcuts.
