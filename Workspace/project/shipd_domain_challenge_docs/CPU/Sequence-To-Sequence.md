# CPU Sequence To Sequence Challenge Examples

Scrape timestamp: 2026-07-19T00:00:00+05:30

Confirmed CPU examples in this document: 11

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Vector Stroke Gap Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75m1xf3d9h0wz5hk0w4a7bws8a9hw2
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: image, multimodal
- Best/top context found: Added from user-provided Shipd CPU-only challenge URL on 2026-07-14; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Recover the missing part of a hand-drawn vector stroke. Each row gives a sketch on a 32 by 32 grid with one contiguous stroke fragment removed. Your output is the ordered list of grid cells that best reconstructs the hidden fragment. This is a structured sequence-reconstruction task.
> Dataset
> train.csv: 3328 completed rows with the public inputs and answer_json.
> test.csv: 1792 rows with the same public inputs, without answer_json.
> sample_submission.csv: Valid baseline submission with id and answer_json.
> Columns:
> id (string): Unique row id.
> prompt (string): Task instruction.
> sketch_json (JSON object): Visible stroke context and gap metadata.
> point_count_hint (integer): Original sketch point-count hint.
> missing_count_hint (integer): Required hidden-fragment length hint.
> answer_json (JSON object, train only): {"hidden_cells":["c07_13",...]}.
> Submission Format
> Submit a CSV with exactly id and answer_json.
> id,answer_json
> qsg_example_1,"{""hidden_cells"":[""c07_13"",""c08_13""]}"
> qsg_example_2,"{""hidden_cells"":[""c12_04"",""c13_05"",""c14_05""]}"
> Evaluation
> Let P be submitted cells and T be true cells.
> set_f1 = 2*|set(P) intersect set(T)|/(|set(P)|+|set(T)|), with 1.0 if both are empty.
> ordered_lcs = LCS(P,T)/max(1,len(T)).
> length_score = exp(-abs(len(P)-len(T))/max(2,len(T)/2)).
> endpoint_score is the average of exp(-ManhattanDistance/3) for first and last submitted cells versus first and last true cells.
> row_score = 0.42*set_f1 + 0.34*ordered_lcs + 0.12*length_score + 0.12*endpoint_score. Final score is the mean row score. Range: 0 to 1; higher is better.
> What Not To Use
> Hardcoded mappings from ids to answers
> Manual lookup of held-out source drawings
> Any hidden answer metadata outside the released public files
> GPU Usage not allowed

Inspiration note: Useful because it turns visual structure completion into a compact ordered-output sequence task with explicit set, LCS, length, and endpoint scoring that can run on CPU.

## Predicting ISPC SPMD Execution Masks

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72hp58zcksr3dr55zh55nk4d8amc7z
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Predicting ISPC SPMD Execution Masks
> Overview
> Each item is a small kernel written in ISPC, the Intel SPMD Program Compiler language. ISPC runs a "gang" of
> program instances (here, 4 lanes, with lane ids programIndex 0 to 3) in lock-step on SIMD hardware. When the
> control flow diverges, ISPC keeps an execution MASK that says which lanes are currently active; a statement
> under an "off" lane has no effect for that lane. Your task is code understanding: for every marked statement in
> the kernel (each line ending in a // sK comment), predict the 4-lane execution mask at that statement.
> The mask at a statement is not a local property. It is determined by the whole path of enclosing conditions and
> by any earlier return, following ISPC's masking and maximal-reconvergence rules. Conditions on programIndex
> (for example if (programIndex < 2)) are fully determined by the lane id, so their effect on the mask can be
> computed exactly from the code. Conditions on the per-lane input value x (for example if (x > 3), where
> x = in[programIndex]) depend on data that is NOT given to you, so the masks along those branches are only
> partially predictable. A model that reads tokens locally, or guesses from statement position, cannot recover
> the mask; it must track the nested control flow the way ISPC's execution model does.
> Background And Intuitive Context
> ISPC, the Intel SPMD Program Compiler, was created by Matt Pharr and William R. Mark at Intel and open-sourced
> around 2011 to 2012 (Pharr and Mark, "ispc: A SPMD Compiler for High-Performance CPU Programming", InPar 2012).
> Pharr is also a co-author of Physically Based Rendering, the graphics text whose authors received a Scientific
> and Technical Academy Award. Despite that pedigree, ISPC is a genuinely rare language. It lives in a narrow
> high-performance niche, and its community footprint is tiny next to mainstream parallel frameworks: there is
> very little Stack Overflow or forum discussion of it, and one of the few widely visible bodies of ISPC material
> online is Stanford's CS149 Parallel Computing course, which has used ISPC in its first assignment for years, in
> part because the language's SPMD execution model is subtle enough to make the assignment genuinely hard. There
> is a running joke that much of what you can find about ISPC online was written by students working through that
> very assignment.
> That rarity is the point of this challenge, not a footnote. ISPC's defining feature is how it runs a gang of
> lanes in lock-step and resolves divergent control flow with an execution mask plus maximal reconvergence: a
> hardware-level, SIMD-lane notion of control flow rather than ordinary sequential execution. The quantity you
> predict, which lanes are live at each statement, is a property of the SIMD hardware's divergence behavior, not
> a scalar program value. Two things make it genuinely hard to shortcut. First, almost no ISPC appears in
> training corpora, so a general pretrained model has essentially no prior knowledge of these lane-masking
> semantics to transfer; it must infer the rules from the provided examples. Second, the prediction is made under
> partial observability: the per-lane input values behind the data conditions are withheld, so the live-lane set
> must be inferred, not computed. Winning therefore requires learning a rare hardware-execution semantics from
> data alone. Because the kernels are tiny and the gang has four lanes, this needs no GPU: a small sequence model
> over the code, or a program that reconstructs the masking rules and applies them, trains in minutes on a CPU.
> Data
> Files provided:
> train.csv is the training table, one row per kernel, with an id column, a code column, and a masks column. code
> is the full text of the ISPC kernel (multiple lines). masks is a space-separated sequence of 4-character
> execution masks, one per marked statement in source order; character j of a mask is 1 if lane j is active at
> that statement and 0 otherwise (for example "1100" means lanes 0 and 1 are active).
> test.csv has an id column and the code column only. For each id predict the masks sequence.
> sample_submission.csv shows the exact required output with a trivial constant baseline you should replace.
> The marked statements are the lines that end in a // sK comment, numbered s0, s1, ... in the order they appear
> in the code; your masks sequence must have one 4-character mask per marked statement, in that order. An example
> training row (code abbreviated):
> id,code,masks
> k_000042,"export void kernel(...) { ... out[programIndex] += 5;   // s0 ... }",1111 1100 0100 ...
> Submission Format
> Submit a CSV named submission.csv with exactly two columns: id (every id in test.csv, one row each, no
> duplicates) and masks. Each masks cell is a space-separated sequence of 4-character strings over {0, 1}, of
> exactly the same length as that kernel's number of marked statements. Example:
> id,masks
> k_000042,1111 1100 0100 0000 1010 ...
> A submission is rejected (it does not score) if it does not have exactly the columns id and masks, is missing
> any id, has an extra or duplicate id, has a masks sequence of the wrong length, or contains a mask that is not
> a 4-character 0/1 string.
> Evaluation Metric
> Submissions are scored by token-level macro-averaged F1 over the mask classes (each distinct 4-bit mask is a
> class), pooled over every marked statement of every test kernel and averaged over the mask classes present in
> the ground truth:
> macro-F1
> =
> 1
> ∣
> 𝑀
> ∣
> ∑
> 𝑚
> ∈
> 𝑀
> 2
> T
> P
> 𝑚
> 2
> T
> P
> 𝑚
> +
> F
> P
> 𝑚
> +
> F
> N
> 𝑚
> macro-F1=
> ∣M∣
> 1
> ​
> ∑
> m∈M
> ​
> 2TP
> m
> ​
> +FP
> m
> ​
> +FN
> m
> ​
> 2TP
> m
> ​
> The score is in [0, 1], higher is better; 1.0 is not achievable because the data-dependent branches make some
> masks only partially predictable.
> Runnable reference scorer (exactly how submissions are graded):
> import numpy as np, pandas as pd
> W = 4
> def _parse(cell, n):
> toks = str(cell).split()
> if len(toks) != n: raise ValueError("length")
> out = []
> for t in toks:
> if len(t) != W or any(c not in "01" for c in t): raise ValueError("bad mask")
> out.append(int(t, 2))
> return np.asarray(out, dtype=np.int64)
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> if not isinstance(submission, pd.DataFrame): raise ValueError("df")
> cols = [str(c) for c in submission.columns]
> if len(cols) != 2 or sorted(cols) != ["id", "masks"]: raise ValueError("cols")
> s = submission.copy(); s.columns = cols; a = answers.copy()
> a["id"] = a["id"].astype(str).str.strip(); s["id"] = s["id"].astype(str).str.strip()
> if s["id"].duplicated().any() or len(s) != len(a) or set(s["id"]) != set(a["id"]): raise ValueError("ids")
> am = dict(zip(a["id"], a["masks"])); yt = []; yp = []
> for _, r in s.iterrows():
> n = len(str(am[r["id"]]).split()); g = _parse(am[r["id"]], n); p = _parse(r["masks"], n)
> yt.append(g); yp.append(p)
> yt = np.concatenate(yt); yp = np.concatenate(yp); f1 = []
> for c in np.unique(yt):
> tp = int(((yp==c)&(yt==c)).sum()); fp = int(((yp==c)&(yt!=c)).sum()); fn = int(((yp!=c)&(yt==c)).sum())
> f1.append(2*tp/(2*tp+fp+fn) if (2*tp+fp+fn)>0 else 0.0)
> return float(np.mean(f1)) if f1 else 0.0
> Baselines
> Predicting the single most common mask for every statement scores about 0.03 macro-F1. A model that reads the
> nested control flow and applies ISPC's masking rules, resolving programIndex conditions exactly and using the
> base rate for the hidden data conditions, reaches about 0.39, the ceiling set by the unknown per-lane inputs. A
> perfect 1.0 is not achievable.
> Rules
> Pretrained models are ALLOWED but of little use. ISPC is an uncommon language with almost no presence in
> training corpora, and the specific masking behavior here must be learned from the provided kernels; there is no
> external knowledge to transfer.
> Allowed:
> Any model or algorithm: a sequence model over the code, a small parser plus a learned or reconstructed mask
> simulator, gradient-boosted or linear models over code features, or a program that infers ISPC's masking
> rules from the training labels and applies them. Reconstructing the execution semantics from the training
> data is a legitimate and expected approach.
> Using the unlabeled test kernels at inference time.
> Prohibited:
> Using any data or labels other than the files provided in this competition. No external datasets.
> Trying to obtain the hidden per-lane input values, the random seed, or the test masks from any external
> source. The data-generation script is provided for transparency, but its private seed and the hidden
> per-lane data-branch outcomes are NOT included, so re-running it cannot reproduce the test masks.
> Hand-labeling or manually editing test predictions; predictions must come from a reproducible method run on
> the provided code.
> Exploiting id values, row order, or file structure instead of the code, or any other form of test-label
> leakage.
> Submissions and their code are reviewed for compliance with these rules.
> Compute Budget
> CPU only, no GPU. The graded solution must run within about one hour on a single CPU. The kernels are tiny and
> the gang has only 4 lanes, so a small sequence model or a reconstructed mask simulator trains and predicts
> comfortably within this budget. Grading is a plain CSV comparison and needs no GPU.

Inspiration note: Useful because it turns compiler/SIMD execution behavior into a CPU-friendly sequence prediction task, with structured mask outputs and domain-specific traces rather than generic text labels.

## Swadesh Phoneme Cipher Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79xxxxw4xxzaedqm5wdw7vqs8ahnr7
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, generative
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Swadesh Phoneme Cipher Decoding
> Overview
> Somewhere in this dataset is a single 'target' language whose pronunciations have been enciphered. Every distinct sound in that language - every IPA segment - has been consistently replaced by an opaque token under one fixed substitution (the same sound always becomes the same token, and two different sounds never share a token). You are given the meaning of each enciphered word, but not its language's identity and not its true pronunciation.
> You are also given complete, true-IPA wordlists for every other language in the database, each labelled with its genetic family and subfamily. The target belongs to the Uralic family. Some of the other languages are its relatives, and because the words in this list are core, slowly-changing basic vocabulary, related languages tend to share cognate forms. The regular sound correspondences between the target and its relatives are your way in: line the enciphered words up against their cognates, work out which token stands for which sound, and decode the whole lexicon.
> Concretely: suppose the enciphered word for 'water' is 'x10 x4 x1 x5', and across the support languages the word for 'water' shows up as 'v e s i', 'v e t e', and 'v e z i'. Reading the systematic correspondences across many such words lets you infer x10 -> v, x4 -> e, x1 -> s, x5 -> i, and therefore decode 'x10 x4 x1 x5' as 'v e s i'. The substitution is global, so once you have pinned a token down it decodes that token everywhere - including in words that have no obvious cognate anywhere in the support data.
> Evaluation
> Each word is scored by the segment-level normalised edit similarity between your decoded pronunciation and the true pronunciation:
> similarity = 1 - levenshtein(predicted_segments, true_segments) / max(len(predicted_segments), len(true_segments))
> where the two sequences are compared as whitespace-separated IPA segments (so 'v e s i' is four tokens). The final score is the mean of this similarity over every word in the evaluation set and lies in [0, 1]; higher is better. A word for which you submit no prediction, or which you leave enciphered, contributes a similarity near 0. Perfectly recovering the cipher yields a score of 1.
> Dataset
> Three files are provided.
> train.csv
> The crib material: true-IPA wordlists for every language in the database except the hidden target. One row per (language, word).
> Column	Type	Description
> language	string	Language code identifying which language the form belongs to (for example 'fin', 'krl').
> family	string	Genetic family of the language - one of roughly 21 families present in the data, such as Uralic, Indo-European, Turkic, Nakh-Daghestanian, Mongolic-Khitan, Tungusic, Dravidian, or Eskimo-Aleut.
> subfamily	string	Genetic subfamily or branch - one of roughly 48 values (for example the Uralic subfamily 'Finnic').
> concept	string	Concept identifier of the form 'N_gloss', where N is an integer index and gloss is a short English label (for example '1_eye', '2_ear', '3_nose'). The same concept ids appear in test.csv, which is what lets you align words across languages by meaning.
> ipa	string	The word's pronunciation, written as IPA segments separated by single spaces (for example 's i l m æ'). Individual segment tokens may be more than one character (for example 'aː').
> test.csv
> The enciphered target lexicon you must decode. One row per target word.
> Column	Type	Description
> id	string	Unique row identifier (for example 't00042'). Use it to match your predictions to rows.
> concept	string	Concept identifier in the same 'N_gloss' form as in train.csv (for example '1_eye'). This is the meaning of the enciphered word and your key for aligning it to the support languages.
> cipher	string	The enciphered pronunciation, written as opaque tokens separated by single spaces (for example 'x0 x5 x0 x2'). Each token is the letter 'x' followed by an integer, and each token maps to exactly one true IPA segment under a single fixed substitution that is shared by every row in the file.
> sample_submission.csv
> An example submission in the exact format required for grading. It has the same 'id' column as test.csv and a placeholder 'ipa' column; replace the placeholder values with your decoded pronunciations.
> The 'concept' ids are consistent between test.csv and train.csv; that shared vocabulary list is what makes cross-lingual alignment possible. A single concept may appear in more than one row (genuine synonyms); each row is scored independently. Some target sounds are rare, or occur only in words with no cognate in any relative, and will be harder to resolve than others.
> Submission
> Submit a single CSV file with exactly two columns, in this order:
> Column	Type	Description
> id	string	The row identifier, copied verbatim from the 'id' column of test.csv (for example 't00042').
> ipa	string	Your decoded pronunciation for that row: IPA segments separated by single spaces, in the same format as the 'ipa' column of train.csv (for example 'v e s i').
> The first line of the file is the header 'id,ipa'. Each following line is one data row, one per row in test.csv, with each 'id' used exactly once. There are no blank lines anywhere in the file: the header line is immediately followed by the first data row, and each data row is immediately followed by the next. Any 'id' from test.csv that is missing from your submission is scored as incorrect.
> A correctly formatted submission file for three test rows looks exactly like this:
> id,ipa
> t00042,s i l m
> t00043,n i n a
> t00044,v e s i
> Method Requirements
> This is an unsupervised decipherment problem: there are no target-language labels to train on. You are expected to recover the phoneme substitution from the data itself by modelling the systematic sound correspondences between the enciphered target and its relatives - for example through statistical alignment of cognates, iterative or EM-style refinement of a token-to-segment mapping, optimisation under the global one-to-one constraint, phonetic-feature or pretrained phoneme representations, or a small sequence model trained from scratch. Because the substitution is a single consistent bijection over the target's sound inventory, strong solutions exploit that global consistency rather than decoding each word in isolation. Solutions must be derived solely from the provided files; approaches that look the target up in outside resources, reconstruct it from a language model's memory, or hard-code the answers are not permitted (see What Not To Use).

Inspiration note: Useful because it turns comparative linguistics-style cipher recovery into a CPU-friendly sequence decoding task, with constrained symbol outputs and small-data feature engineering rather than large model inference.

## Deadzone: Action-State Recovery from Blind Controller Streams

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx773wm8ayxa26y2t7acaqg11d8ambcz
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Each record in this challenge is a pair of parallel strings over a 254-symbol alphabet. Your job is to emit a third string, over a different 8-symbol alphabet, aligned one-to-one with the scored positions of the input.
> That is the whole contract: two input strings in, one output string out. The actor_codes string and the foe_codes string describe two agents acting in the same episode; the states string you produce says which of eight behaviour classes the actor was in at each scored position.
> This is a transduction problem, not a forecasting one. Nothing is extrapolated beyond the end of the string, and no value is predicted before it is observed. The entire input pair is handed to you at once and the output is a labelling of it, so both left and right context are fair game — the strong reference model below is bidirectional. There is no timestamp, no sampling rate, no clock, and no numeric measurement anywhere in the data: every field you receive is either a symbol string or a categorical code. The task is closest in shape to sequence tagging or transliteration, where an input string is rewritten into an aligned output string over a different alphabet.
> What makes the rewriting hard is that it is not a symbol-to-symbol mapping. The alphabet was emitted by a hidden automaton, and the same input symbol licenses completely different output symbols depending on which state that automaton is in — a state you are never shown. The identical code yields atk from one state, air from another, and nothing at all from a third. So the mapping cannot be tabulated; the automaton has to be inferred from the parallel corpus in train.csv and then decoded, carrying the inferred state along the string.
> The second difficulty is that the two input strings are coupled. Roughly 28% of the output symbols hit, evd, rsp) are states the actor did not choose at all: they are forced by what the other agent did, and whether that agent's action took effect depends on a hidden relationship between them that appears in neither string. No amount of modelling actor_codes alone will explain them. They are recoverable only by reading both strings jointly and inferring the interaction that must have produced the pair.
> The symbols are opaque and salted. c000 does not tell you what it denotes, and nothing here reveals the mapping; which symbols mean "attack", which mean "block", and which mean "nothing at all" is itself something to learn from the training split. On top of that, 22% of the positions in every string are blanked to [X], so the evidence is lossy as well as opaque. Blanking removes evidence only — the output symbols are the source system's own recorded states, exactly as observed, never perturbed.
> Provenance. The strings are real recordings: two people operating hand controllers through matches of a competitive video game, and the output symbols are the game engine's own internal action states for one of the two characters. Everything the engine displayed on screen — positions, velocities, damage, collisions — is withheld, which is precisely why the automaton's state must be inferred rather than looked up.
> The intended first-order approach is to learn the association between short spans of surrounding symbols and the actor's class, then improve on it by decoding the pair as a sequence: propagating the inferred hidden state along the string, using the unscored prefix to initialise it, and reading the foe's symbols to explain the states the actor did not choose. A classifier that looks only at the symbol at the current position is measured below and scores poorly.
> Evaluation
> Pool the scored positions of every test record together and let C be the 8x8 confusion matrix over those positions, where C[i][j] counts the scored positions whose true class is i and whose predicted class is j.
> Define:
> N = total number of scored positions = the sum of all entries of C
> c = the sum of C[i][i] over i — the number of correct positions
> t_i = the sum of C[i][j] over j — how often class i is the truth
> p_j = the sum of C[i][j] over i — how often class j is predicted
> Term 1 — multiclass correlation. The classification term is the Matthews correlation coefficient generalised to 8 classes:
> MCC = (c × N − S_tp) / ( sqrt(N² − S_pp) × sqrt(N² − S_tt) )
> where
> S_tp = the sum over i of t_i × p_i
> S_pp = the sum over j of p_j × p_j
> S_tt = the sum over i of t_i × t_i
> If the denominator is 0, then MCC = 0. MCC is 1 for a perfect prediction, 0 for any constant prediction, and negative for anticorrelated predictions. It is chance-corrected, so predicting the majority class everywhere earns nothing.
> Term 2 — boundary agreement. This term asks where the output string changes symbol. For one record with true classes y_1 ... y_n and predicted classes d_1 ... d_n, define at each position k from 2 to n:
> true boundary B_k = 1 if y_k ≠ y_(k−1), else 0
> predicted boundary D_k = 1 if d_k ≠ d_(k−1), else 0
> Pooled over every scored position of every record:
> TP = the sum of B_k × D_k
> FP = the sum of (1 − B_k) × D_k
> FN = the sum of B_k × (1 − D_k)
> BoundaryF1 = 2 × TP / (2 × TP + FP + FN), and BoundaryF1 = 0 when TP = 0
> Final score.
> Score = 100 × clip(0.70 × MCC + 0.30 × BoundaryF1, 0, 1)
> clip(x, 0, 1) returns 0 below 0, 1 above 1, and x otherwise. The minimum score is 0 and the maximum is 100, awarded only for reproducing every scored position of every record exactly. Higher is better.
> The output string changes symbol at 4.8% of positions, so neither trivial boundary strategy pays: never predicting a change gives BoundaryF1 = 0, and predicting a change everywhere gives BoundaryF1 = 0.091.
> Measured reference scores
> All figures were produced by the published grader on the published test.csv, against the held-out key:
> | Approach | Score |
> |---|---|
> | Perfect reconstruction | 100.00 |
> | sample_submission.csv — the constant symbol gnd | 0.00 |
> | Uniform random symbol per position | 2.71 |
> | Constant most-frequent training symbol | 0.00 |
> | Per-symbol lookup: each code to its most common class in train | 19.31 |
> | Gradient-boosted trees over a span of surrounding symbols from both strings | 43.34 |
> | Bidirectional recurrent sequence model over both strings | 58.95 |
> Both constant baselines score exactly 0 because MCC is chance-corrected and a constant string has no boundaries.
> Dataset
> The public/ directory contains three files.
> train.csv* — 8,826 rows, one row per record:
> seq_id — integer, opaque identifier of the record; encodes nothing
> arena — string, salted code for the setting the episode took place in
> actor_kind — string, salted code for the actor's archetype
> foe_kind — string, salted code for the foe's archetype
> context_len — integer, always 60; the length of the unscored prefix, given as context only
> n_scored — integer, the number of scored positions in this record; varies from 160 to 260
> actor_codes — string, space-separated symbols for the actor, of length context_len + n_scored; each symbol is either c000 through c253 or the blanked marker [X]
> foe_codes — string, space-separated symbols for the foe, same length and alphabet
> states — string, space-separated ground-truth classes for the actor, of length n_scored
> test.csv* — 3,174 rows, identical to train.csv but without the states column.
> sample_submission.csv* — 3,174 rows, a valid but deliberately worthless submission in the exact required format.
> Both input strings span all context_len + n_scored positions, but only the last n_scored are scored. The 60-symbol prefix exists purely to let you warm up your estimate of the hidden state before scoring begins.
> The eight output classes are:
> rsp — the actor has been knocked out: dead, respawning, or re-entering
> gnd — grounded movement: standing, walking, dashing, running, turning, crouching, landing
> air — airborne movement with no attack: rising, falling
> atk — attacking: any ground attack, aerial attack, or special move, including its recovery lag
> shd — blocking: raising, holding, or dropping a shield
> grb — grappling: grabbing, holding, throwing, or being grabbed and thrown
> hit — being struck, knocked back, or tumbling
> evd — evasive and recovery states: rolls, dodges, teching, knockdown, get-up, and hanging on a ledge
> Classes are not balanced; their frequencies are those of real play, from 28.3% for atk down to 3.6% for grb.
> Submission
> Submit a CSV with a header row and exactly 3,174 data rows — one per seq_id in test.csv.
> seq_id — integer — the record identifier, copied from test.csv. Every id must appear exactly once.
> states — string — space-separated class symbols for the actor, in order. Must contain exactly n_scored symbols, each one of rsp, gnd, air, atk, shd, grb, hit, evd.
> Example, using real ids from test.csv — record 0 has n_scored = 184 and record 3 has n_scored = 183, so their strings are 184 and 183 symbols long respectively; both are truncated here with an ellipsis:
> seq_id,states
> 0,air air air air air gnd gnd atk atk ...
> 3,atk atk atk hit hit hit evd evd gnd ...
> Validity rules:
> Row order does not matter, and extra columns are ignored.
> Duplicate, missing, or unrecognised seq_id values are rejected, as is a wrong row count.
> A row whose states value is empty, non-string, or does not contain exactly n_scored recognised class symbols is scored as maximally wrong for that record: every position is counted incorrect, and its boundaries are counted as both missed and falsely raised. An unparseable row is therefore never cheaper than a wrong one — there is no benefit to abstaining.
> What Not to Use
> A constant or majority-class string. MCC is chance-corrected, so every constant submission scores exactly 0, not the 28% you might expect from the frequency of atk.
> A per-position classifier on the current symbol alone. This is the obvious shortcut and it is measured above at 19.31. It cannot work, because the symbol-to-class mapping is one-to-many by construction: the identical symbol yields atk, air, hit or nothing depending on hidden state you must carry along the string yourself.
> Any approach that ignores foe_codes. Roughly 28% of output symbols are hit, evd or rsp — states the actor did not choose. They are forced by the foe, and no amount of modelling the actor's own string will explain them.
> Prior knowledge of any particular device, layout, or archetype. The alphabet is salted and the archetype codes are anonymised. c000 is not something you already know. The mapping exists only in the training split.
> Blanket smoothing as a substitute for state tracking. Blurring the output raises apparent accuracy but destroys BoundaryF1, which is 30% of the score and rewards placing each transition at the correct position.
> What is expected instead: infer the hidden automaton from the training split, then decode each test record as a sequence — propagating the hidden state along the string, using the unscored prefix to initialise it, and reading both strings jointly to explain the symbols the actor did not choose.

Inspiration note: Useful because it frames sequence-to-sequence as hidden action/state reconstruction from blind controller streams, a CPU-friendly temporal decoding task with structured outputs.

## Ornament Sequence Recovery from Lossy Performance Views

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f62hwc1hjnkypeksqy8wpvx8ama7n
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Traditional bowed-string performances contain rapid ornaments, simultaneous notes, resonating strings, and timing that does not follow a perfectly regular pulse. Each row in this challenge represents one real performance excerpt as an ordered sequence of 20–32 latent note events. You must reconstruct the complete event sequence from two complementary symbolic views and a compact acoustic feature array.
> The pitch view reveals relative pitch and simultaneous-note multiplicity at some positions. The timing view independently reveals inter-onset-gap and duration bins. Withheld positions are explicit question-mark tokens, and neither view is sufficient alone. The accompanying acoustic row supplies spectral and energy evidence for every ordered event. The intended first-order approach is to align the two visible views, use acoustic cues and neighboring events to recover withheld components, and decode a consistent sequence.
> Each target event has the form P±dd_Gd_Dd_Md:
> P±dd is relative pitch in semitones, clipped to -24 through +24.
> Gd is the inter-onset-gap bin from G0 through G5.
> Dd is the duration bin from D0 through D5.
> Md is simultaneous-note multiplicity from M1 through M4.
> Evaluation Metric
> Let the predicted token sequence be \hat y=(\hat y_1,\ldots,\hat y_n) and the target be y=(y_1,\ldots,y_m).
> Let d_{\mathrm{lev}}(\hat y,y) be token-level Levenshtein distance. The exact edit term is   E=\max\left(0,1-\frac{d_{\mathrm{lev}}(\hat y,y)}{\max(n,m,1)}\right).
> For valid events a=(p_a,g_a,d_a,m_a) and b=(p_b,g_b,d_b,m_b), pair similarity is   s(a,b)=0.50e^{-|p_a-p_b|/2}+0.20e^{-|g_a-g_b|/1.25}+0.20e^{-|d_a-d_b|/1.25}+0.10\mathbf{1}[m_a=m_b].   Invalid events have pair similarity zero.
> Let W be the maximum sum of s over every order-preserving one-to-one matching between predicted and target events. Define P_A=W/n, R_A=W/m, and   A=\frac{2P_AR_A}{P_A+R_A},   with A=0 when either sequence is empty or the denominator is zero.
> Form the multisets of adjacent token bigrams. If their multiset overlap count is c, define P_B=c/\max(n-1,1), R_B=c/\max(m-1,1), and   B=\frac{2P_BR_B}{P_B+R_B},   with B=0 when either sequence has no bigram or the denominator is zero.
> The final score is   100\times\operatorname{clip}(0.40E+0.40A+0.20B,0,1).
> Minimum 0 means no usable sequence agreement. Maximum 100 means every event and transition is reconstructed exactly.
> Measured public-data-only references: sample submission 0.000000; constant sequence 16.116568; mode-filled view fusion 47.295947; capable CPU gradient-boosted sequence decoder with transition decoding 54.994396; perfect 100.000000.
> Dataset
> train.csv - 1,714 labeled examples.
> sample_id - int64 - Content-free submission identifier.
> pitch_view - string - Ordered P±dd:Md tokens and P?:M? withheld tokens.
> timing_view - string - Ordered Gd:Dd tokens and G?:D? withheld tokens.
> capture_profile - string - Balanced nuisance profile A or B; it is not a target.
> target_sequence - string - Complete ordered training target.
> test.csv - 1,130 query examples with the same query columns and no target column.
> train_features.npz - acoustic, float16, shape (1714, 32, 18).
> test_features.npz - acoustic, float16, shape (1130, 32, 18).
> sample_submission.csv - Correct submission header and all required test IDs.
> CSV rows and feature arrays are positionally aligned: the first data row maps to acoustic[0], the second maps to acoustic[1], and so on. The number of populated event rows equals the number of tokens in either symbolic view; remaining rows are zero padding. Acoustic channels 0–11 are rotated chroma-band energies. Channels 12–17 are local pre-onset, center, post-onset, energy-change, variation, and mean-energy observations.
> Submission
> sample_id - int64 - Must match one test ID exactly.
> target_sequence - string - A variable-length, space-separated sequence of valid P±dd_Gd_Dd_Md event tokens.
> Submit exactly 1,130 data rows plus the required header. The exact column order is sample_id,target_sequence. Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and extra rows are rejected. Row order may differ because scoring aligns by ID. Missing, non-finite, empty, or malformed prediction values are scored as invalid events and never provide an abstention advantage.
> Example using real test IDs:
> sample_id,target_sequence
> 1231,P+00_G0_D2_M1 P+02_G3_D1_M1
> 1510,P-05_G0_D3_M2 P+00_G4_D2_M1
> 2194,P+00_G0_D1_M1 P+07_G5_D2_M2
> What Not to Use
> A constant or majority event sequence fails because tune, length, pitch contour, timing, and polyphony vary naturally.
> A pitch-view-only method cannot recover timing and duration components hidden independently in the timing view.
> A timing-view-only method cannot recover relative pitch or simultaneous-note multiplicity.
> Treating positions independently leaves performance on the table because ornament transitions and local timing form ordered motifs.
> capture_profile is deliberately balanced and non-informative; using it as a target shortcut does not generalize.
> External source matching is not expected and is undermined by tune-disjoint splitting, cropped windows, relative pitch, chroma rotation, feature normalization, and stripped source metadata.
> Successful systems should fuse both symbolic views with the acoustic event rows and model dependencies across the output sequence.

Inspiration note: Useful because it casts sequence-to-sequence as recovery of hidden symbolic ornament sequences from lossy performance observations, a compact CPU-friendly temporal reconstruction pattern.

## Opaque Security Clip Action Ledger Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73e84bnm1f8mfpsrhpecgcvn8aj7dw
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> For each 8-second surveillance clip, predict a JSON list of the actions that happen in the clip. Each predicted action record must say:
> when the action starts and ends within the 32-frame clip,
> who or what performs the action,
> what action is being performed,
> what object, place, or context the action involves,
> and how this action record connects to other action records in the same clip.
> The output is called an activity ledger. In plain language, a ledger is just an ordered set of action segments plus links between related segments. For example, if a person opens a vehicle door and then enters the vehicle, the desired output should contain two time-span records and a link showing that the records are adjacent or belong to a documented action pair.
> The videos are real fixed-camera surveillance-style recordings from a licensed activity-recognition collection. The scenes show ordinary outdoor security-camera views with pedestrians, vehicles, doors, packages, carried objects, phones, bicycles, documents, and scene structures. The labels come from human-created activity annotations that mark action names, frame spans, actor identifiers, and actor types. During preparation, the original files are cropped, resized, metadata-stripped, re-encoded, and assigned opaque IDs so participants see only neutral short clips and relative paths.
> This is not a whole-video classification task. A submission must recover the structured per-clip action ledger: multiple possible records, their frame ranges, their state fields, and their typed links.
> Task
> Given one 32-frame MP4, output one canonical graph_json object. The JSON has two top-level lists:
> nodes: action records. Each record has a frame span and a state tuple.
> edges: links between records. Each link says whether two records overlap, occur next to one another, or form a documented activity pair.
> The training set provides videos and their full graph_json ledgers. The test set provides only videos. Learn from the training videos and ledgers, then predict ledgers for held-out recording sessions. The test video is the only test-time signal.
> The task is CPU-only. A practical solution can use 32-frame MobileNetV3/ResNet18 embeddings followed by a small GRU, temporal-convolution network, or transformer-lite decoder with constrained JSON generation. End-to-end large video transformers are unnecessary. The reference CPU pipeline plus inference and preparation is designed for at most 90 minutes on 10 CPU cores and 62 GB RAM.
> Public files
> Item	Description
> train.csv	labeled videos
> test.csv	unlabeled videos
> sample_submission.csv	schema example
> train/videos/	256px MP4 clips
> test/videos/	256px MP4 clips
> All public IDs are opaque and all video paths are relative. No source filename, timestamp, session name, annotation ID, or group label is provided.
> train.csv columns
> Column	Type	Description
> id	string	opaque item ID
> video	string	relative MP4 path
> graph_json	string	canonical target ledger
> graph_json is only a training label. It is a JSON object with nodes and edges. Each node has an integer id (0-based canonical order), inclusive start and end frame bins in [0,31], and a state object. A state contains agent, action, context, and a sorted unique roles list. Allowed values are listed in the schema section below.
> test.csv columns
> Column	Type	Description
> id	string	opaque item ID
> video	string	relative MP4 path
> Each test row has exactly 32 effective frames at 4 FPS. The video is the only test-time signal.
> Example test row: item_001edae916ee264964,test/videos/item_001edae916ee264964.mp4.
> Example submission (the first three rows of the provided template):
> id,graph_json
> item_001edae916ee264964,"{""edges"":[],""nodes"":[]}"
> item_0053f6e879a2f2083c,"{""edges"":[],""nodes"":[{""end"":25,""id"":0,""start"":7,""state"":{""action"":""enters"",""agent"":""person"",""context"":""scene_structure"",""roles"":[""person""]}}]}"
> item_00be7ca4bc0ed7ac86,"{""edges"":[],""nodes"":[]}"
> Ledger JSON schema
> Each node is one action segment. Node state.agent is in {hand, person, vehicle}. state.action is in {abandons, carries, closes, drops_off, embraces, enters, exits, interacts, loads, makes_u_turn, opens, picks_up, purchases, puts_down, reads, reverses, rides, sits, stands, starts, steals, stops, talks, texts, transfers, turns, unloads}. state.context is in {bicycle, document, facility_door, heavy_object, laptop, left, none, object, package, person, phone, right, scene_structure, trunk, vehicle, vehicle_door}. Every role is one of {bag, bicycle, other, person, receptacle, vehicle} and roles are sorted without duplicates.
> agent is the acting category, action is the activity verb, context is the object/location cue, and roles lists participating object categories.
> An edge has integer from < to node indices and one type from {documented_pair, temporal_next, temporal_overlap}. documented_pair means the two source activity labels are linked by the preparation-time activity-pair table and their spans overlap or are within 30 source frames. temporal_overlap means source spans overlap when no documented pair applies; temporal_next is the next canonical non-overlapping activity record when neither other type applies. Edges are unique and sorted by (from,to,type). Empty ledgers are valid when no annotated activity record intersects the clip. The canonical JSON form uses UTF-8 JSON, sorted keys, compact separators, and no NaN, Infinity, duplicate keys, or extra fields.
> The parser caps each ledger JSON at 20,000 characters, 32 nodes, and 256 edges. Node IDs must be consecutive; a (from,to) pair cannot repeat even with a different edge type. These caps are hard validation limits, not suggestions.
> Submission format
> Column	Type	Constraint
> id	string	exact test IDs
> graph_json	string	valid ledger JSON
> Submit one row per test ID, in any order. The grader aligns by opaque ID, but rejects missing/extra/repeated IDs or wrong/reordered columns. A malformed ledger cell is row-local and receives score zero; a structurally malformed file raises InvalidSubmissionError.
> What Not To Do
> Do not use filename, ID, row order, path depth, file size, modification time, MP4 encoding, archive order, perceptual hashes, reverse-video lookup, or any other side channel. Do not use external annotations or private answers to recover labels, hard-code per-ID ledgers, or use a constant ledger template. Do not solve this with regex, timestamp parsing, motion-only frame differencing, color/shape thresholds, a detector-only pipeline, object-box relation proposals, or a rule table copied from the annotation vocabulary. External task-specific pretrained weights, hosted/closed-source APIs, teacher labeling, transductive use of hidden test labels, and inference-only pre-baked answers are prohibited.
> Generic ImageNet-pretrained backbones, ordinary augmentations, optical flow as an auxiliary feature, classical CV features used inside a learned model, CPU multiprocessing, and learned temporal/structured decoders are allowed. The solution must learn from the provided videos and training ledgers and must remain CPU feasible.
> Enforcement
> Submissions are checked for exact columns and row set, duplicate IDs, finite bounded JSON, canonical node/edge ordering, duplicate keys, node/edge caps, and legal vocabulary. Structural failures raise InvalidSubmissionError; malformed row content contributes zero for that row. Rule-only, source-lookup, metadata-only, or hard-coded solutions can be rejected even if they produce numerically valid JSON.
> Enforcement on invalid approaches: any submission that relies on external media retrieval, external annotation lookup, ID/file-size side channels, or inference-only pre-baked answers is invalid and may be rejected.
> Evaluation
> For each test row, the grader first parses and validates the submitted JSON. If both the predicted and true ledgers are empty, the row score is 1.0. If exactly one is empty, the row score is 0.0. Otherwise, predicted nodes and true nodes are matched one-to-one by maximizing:
> 0.55 * span_credit + 0.45 * tuple_credit
> where span_credit = max(span_iou, boundary_credit). span_iou is the inclusive frame-span intersection-over-union. boundary_credit = max(0, 1 - (abs(pred_start - true_start) + abs(pred_end - true_end)) / 8). tuple_credit = 0.20 * agent_match + 0.35 * action_match + 0.25 * context_match + 0.20 * role_set_f1.
> After matching, the row components are:
> Component	Definition	Weight in core score
> Temporal span	matched span accuracy	0.28
> State F1	exact state-token F1	0.27
> Sequence edit	ordered state edit similarity	0.17
> Typed edge F1	typed link F1 after node mapping	0.20
> Completeness	node-count and edge-count accuracy	0.08
> Temporal span is the mean matched span_credit divided by max(pred_node_count, true_node_count). State F1 uses exact state-token matches; a matched node counts only when span credit is at least 0.25 and the full state token matches. Sequence edit is 1 - levenshtein_distance / max(sequence_length) over ordered state tokens. Typed edge F1 is computed over (from,to,type) edges after matched predicted node IDs are mapped to true node IDs. Completeness is 0.65 * node_count_credit + 0.35 * edge_count_credit, where count credit is 1 - abs(pred_count - true_count) / max(pred_count, true_count, 1).
> The core score is the weighted sum of the five table components. The joint score is the geometric mean:
> joint = (temporal * state_f1 * sequence_edit * typed_edge_f1) ** 0.25
> The final row score is:
> row_score = clip(0.65 * core + 0.35 * joint, 0, 1)
> The overall score uses all private rows:
> balanced_mean = 0.80 * mean(rows with at least one true node) + 0.20 * mean(rows with no true nodes)
> final_score = clip(0.88 * balanced_mean + 0.12 * worst_session_mean, 0, 1)
> worst_session_mean is the lowest mean row score among the five held-out recording-session groups. Each private session group has at least 30 rows. A perfect private ledger submission scores exactly 1.0. The declared theoretical minimum is 0.0 and maximum is 1.0. The sample submission is a weak train-prior schema baseline and is intentionally below 0.5 while above the platform validation floor.
> Dataset
> The participant-visible dataset contains 479 labeled training clips and 175 unlabeled test clips. Each clip is a 256x256 MP4 with 32 frames sampled at 4 FPS from one longer fixed-camera recording. The visible content is source-neutral surveillance footage: pedestrians, vehicles, doors, packages, carried objects, phones, bicycles, and scene structures in outdoor security-camera views.
> The ledgers are derived from human activity annotations, not from synthetic labels. The preparation script reads activity packets, converts source frame spans into 32-frame clip coordinates, maps activity names into the allowed agent/action/context vocabulary, and uses actor-type packets to populate the roles list. Edges are derived deterministically from source span overlap, source temporal order, and a documented action-pair table.
> A recording-session group is the strongest available hidden grouping that could leak nearby footage: usually one original continuous camera recording, or a same-time or adjacent-camera recording group when multiple cameras observe related activity. Train and test are split by these groups. No original session group, neighboring window, or directly related camera recording appears in both train and test.

Inspiration note: Useful because it frames sequence-to-sequence as action-ledger recovery from opaque security clips, combining temporal perception with structured event output while staying CPU-friendly.

## Multilingual Conditional Tool Contract Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74kqme45dwa9et96sj61yn0x8aknbt
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Production routing contracts often contain conditions that are invisible in a tool name: a request is accepted only when an argument is present, or only when an argument is absent. Each row contains six multilingual requests accepted by one unnamed tool and four rejected requests. Two rejected requests come from the same underlying behaviour but violate its hidden argument gate; two come from a nearby, distinct behaviour.
> Return the raw target and peer tool tokens together with the conditional interface:
> accepted requests + same-purpose gate violations + nearby negatives -> conditional tool contract
> Broad tool recognition is only one component. A solution must also infer the gate argument, decide whether that argument is required or forbidden, recover the accepted interface, and separate the peer behaviour from same-tool policy violations.
> Solutions must use CPU only, at most 10 CPU cores and 62 GB RAM, and finish within 90 minutes.
> Dataset
> train.csv: 900 labeled episodes from 30 latent tools.
> test.csv: 450 unlabeled episodes from 15 entirely unseen latent tools.
> sample_submission.csv: 450 schema-valid empty placeholder contracts.
> Columns:
> contract_id: opaque unique string identifier.
> positive_examples_json: JSON array of exactly six accepted examples. Each object has string locale and string request. No intent, argument label, source identifier, or literal-span annotation is provided.
> contrast_examples_json: JSON array of exactly four rejected examples in shuffled order. Two are same-purpose gate violations and two represent one nearby behaviour. Each object has string locale and string request; group membership is hidden.
> argument_registry_json: JSON array of 55 permitted argument objects. Each object has string name, string description, and categorical string type equal to string. The same broad registry is used for every episode, so registry membership does not reveal the target interface.
> induction_requirements: JSON object containing string rules named required_threshold, optional_threshold, routing_rule, and peer_rule.
> induced_contract: train-only JSON target string.
> Requests span Arabic, German, English, Spanish, French, Hindi, Indonesian, Japanese, Russian, Swahili, Turkish, and Simplified Chinese. Every episode uses ten distinct underlying semantic groups.
> Target Contract
> induced_contract must be one JSON object with exactly five keys:
> target_tool: raw lowercase underscore-delimited tool token for the six accepted examples, such as alarm_remove.
> routing_rule: object with exactly two string fields:
> argument: one name from the row registry;
> operator: exactly required or forbidden. required means accepted requests contain the argument and same-purpose negatives omit it; forbidden means the reverse.
> required_arguments: lexicographically sorted array of unique registry names expressed in at least three accepted examples.
> optional_arguments: lexicographically sorted array of unique registry names expressed in one or two accepted examples.
> peer_tool: raw lowercase underscore-delimited tool token for the distinct nearby behaviour in the contrast set.
> Required and optional arrays must be disjoint. The routing argument and all submitted interface arguments must come from the registry.
> Example:
> {"target_tool":"alarm_remove","routing_rule":{"argument":"date","operator":"required"},"required_arguments":["date"],"optional_arguments":["time"],"peer_tool":"alarm_query"}
> Evaluation
> target_tool and peer_tool use exact string accuracy. Required and optional arguments use exact set F1. Correct empty-set agreement scores 1 for that component; an incorrect empty/non-empty pairing scores 0. Routing score is the mean of exact gate-argument accuracy and exact operator accuracy.
> The component base is worth 90 percent:
> 10 percent target-tool accuracy;
> 30 percent routing-rule score;
> 20 percent required-argument set F1;
> 20 percent optional-argument set F1;
> 10 percent peer-tool accuracy.
> Let interface be the mean of required and optional set F1. The balance multiplier is:
> 0.5 + 0.5 * min(target_tool, routing, interface, peer_tool)
> The row score is:
> component_base * balance_multiplier + 0.10 * exact_complete_contract
> exact_complete_contract is 1 only when the parsed five-field object exactly matches the canonical contract. A perfect contract scores 1.0; tool-token recognition alone cannot compensate for a failed conditional policy.
> Raw tool values may contain only lowercase letters, digits, and underscores and may be at most 64 characters. A value that violates this content bound receives zero for that row; it does not abort or invalidate other submission rows. Structural failures such as malformed JSON, wrong keys, missing IDs, duplicate IDs, or unregistered argument names remain submission errors.
> The final score is the mean row score clipped to [0, 1]. If one identical non-empty contract is submitted for more than 20 percent of test rows, the final score is capped at 0.10.
> Submission Format
> Submit a CSV with exactly these columns in this order:
> contract_id,induced_contract
> Every test ID must appear exactly once. JSON must be CSV-escaped normally:
> contract_id,induced_contract
> ct_00dec2ba1717b9f829b7,"{""target_tool"":"""",""routing_rule"":{""argument"":"""",""operator"":""required""},""required_arguments"":[],""optional_arguments"":[],""peer_tool"":""""}"
> ct_010bb671af20a22dbbc8,"{""target_tool"":"""",""routing_rule"":{""argument"":"""",""operator"":""required""},""required_arguments"":[],""optional_arguments"":[],""peer_tool"":""""}"
> These placeholders are schema-valid but score zero.
> Requirements
> Use CPU only and finish within 90 minutes.
> Fit learned vocabularies, thresholds, and task-specific models on train.csv only.
> Aggregate all accepted and rejected examples at episode level.
> Produce strict JSON with exactly the documented keys and permitted registry names.
> Use a genuinely learned semantic method; deterministic logic may validate and render predictions.
> Prohibited Leakage
> Do not use private answers, unreleased labels, external label tables, hidden identifiers, internet services, or external-corpus record matching. Do not reconstruct released requests through search, translations, metadata, or a separately obtained copy of their source corpus. CUDA and GPU-only dependencies are prohibited.

Inspiration note: Useful because it frames sequence-to-sequence as multilingual contract induction: infer conditional tool-call schemas/constraints from examples, a practical structured-output benchmark for agents.

## Audit Record Sequence Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx799dfpt4e0zxc0ebhx9sj82d8asywz
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ? Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (4)
> Your Submissions
> Audit Record Sequence Restoration
> Overview
> Operational collectors can recover the contents of a damaged audit fragment while losing the fragment's exact record order. Restoring that order matters: downstream incident reconstruction depends on which state transition preceded another, not merely which records were present.
> Each row provides five unordered recovered records. Direct message headers and neighboring boundary records are withheld because repeated boundary templates can identify a memorized protocol chain. The remaining evidence contains coarse one-second timing, protocol layer, and decoded field fragments from real captured records. Recover the original order of the five candidate IDs.
> Rows come from non-overlapping source blocks. Every private row contains at least one directed decoded-evidence transition family absent from training, while every represented event retains at least ten training examples. This makes generalization to unseen protocol transitions load-bearing instead of rewarding recombinations of familiar local chains. Solvers must combine coarse timing with relationships among decoded security, identity, transaction, capability, and radio-control evidence.
> Dataset
> File descriptions
> train.csv -- 912 recovered audit fragments with context and the correct five-candidate order.
> test.csv -- 312 recovered audit fragments with context but no restoration.
> sample_submission.csv -- A valid template containing independently shuffled candidate orders.
> Column descriptions
> id (string) -- Unique 12-character hexadecimal row identifier. IDs do not encode capture order.
> context (string) -- Five unordered recovered records named c0 through c4. Candidate records include a coarse time offset and decoded field evidence, but not their direct message header or neighboring boundary records.
> restoration (JSON string; train only) -- Object with exactly one key, order, whose value is the five candidate IDs in original chronological order.
> Evaluation
> Submissions are scored with Sequence Proof Score. It rewards correct global precedence and exact local transitions:
> pair_accuracy = correct_ordered_candidate_pairs / 10
> pair_skill = max(0, 2 * pair_accuracy - 1)  # random ordering has zero expected skill
> adjacency_score = correct_directed_adjacent_links / 4
> exact_score = 1 if the complete five-record order is correct else 0
> score = 0.30  *mean_pair_skill + 0.25*  mean_adjacency_score + 0.45 * mean_exact_score
> Higher is better. Scores range from 0 to 1. The ten pairwise comparisons measure global ordering, the four directed adjacency links emphasize locally coherent reconstruction, and exact recovery rewards an operationally usable complete chain. Pair skill removes the 0.5 chance baseline of raw pair accuracy.
> Submission
> Submit one JSON restoration for every row in test.csv.
> id (string) -- Exact identifier from test.csv.
> restoration (JSON string) -- Object containing exactly order, a permutation of c0 through c4.
> Example:
> id,restoration
> 0255e70e45d6,"{""order""":[""c2"",""c0"",""c4"",""c1"",""c3""]}"
> 8b8dec771519,"{""order""":[""c1"",""c4"",""c3"",""c0"",""c2""]}"
> Requirements
> The file must contain exactly 312 rows plus the header.
> Every test id must appear exactly once.
> Columns must be named exactly id,restoration; extra columns are rejected.
> Every restoration must parse as JSON with exactly the order key.
> order must contain each of c0 through c4 exactly once.
> Missing values, malformed JSON, duplicate candidates, unknown candidates, and incomplete orders are rejected.
> File format: .csv only.
> What Not To Use
> Do not reverse-match decoded fragments against outside packet-trace copies to recover their original timestamps or row order; that retrieves the answer instead of reconstructing the sequence from supplied evidence.
> Do not decode row IDs or infer ordering from public/test file position. IDs and row order are independently hashed and shuffled.
> Do not use a hand-written message-signature dictionary or fixed protocol state table as the primary predictor. Direct message headers are intentionally withheld; the benchmark measures learned ordering from decoded evidence across held-out candidate-family combinations.

Inspiration note: Useful because it is a compact sequence-order reconstruction task with structured permutation output and a metric that rewards both local transition correctness and full-order recovery.

## Article Lead Paragraph Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73mhynnwp23cmh9d6gdyexxn83tt1j
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ? Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (3)
> Your Submissions
> Article Lead Paragraph Generation
> Overview
> Summarisation models have a well-known crutch: the source text. Given enough body content, a model can identify salient sentences, compress them, and produce something that scores well on ROUGE without ever understanding what the article is actually about. This challenge removes that crutch entirely.
> You are given an article title and a structural skeleton: the heading of each section paired only with its opening sentence. There is no body text. There are no paragraphs to compress. The skeleton tells you what an article covers, not what it says. From this outline alone, your model must generate a 1 to 3 sentence lead paragraph that matches the style and informational density of a reference encyclopaedic introduction.
> This is not summarisation. It is structural inference. A skilled encyclopaedic editor reading only a list of section headings and opening claims must reason about what kind of entity the article describes, which facets matter most, and how to introduce the subject to someone who knows nothing about it. The skeleton is a signal about article architecture, not a source of text to paraphrase.
> The difficulty is compounded by the breadth of the task. The 120,000 training articles span geography, biography, natural history, military history, sport, culture, science, law, architecture, and dozens of other domains. A model that learns to write encyclopaedic introductions for one category of article must generalise that skill across fundamentally different types of entities: a lake in Tajikistan, a class of Iranian patrol boats, a species of wren, a Scottish actor, a 1918 cargo ship. Each requires a different type of opening claim. Each has a different encyclopaedic convention for what the lead sentence must establish.
> Dataset
> The dataset contains 120,000 labelled Wikipedia articles for training and 30,000 for testing. Each article is represented only by its title and skeleton. The full article body is never provided.
> train.csv (120,000 articles)
> Column           Type    Description
> ????????????????????????????????????????????????????????????????????????????????
> article_id       str     Unique article identifier
> title            str     Article title
> skeleton         str     Section headings, each followed by the opening sentence
> of that section. Sections separated by blank lines.
> lead_paragraph   str     Reference lead paragraph (generation target)
> test.csv (30,000 articles)
> Column           Type    Description
> ????????????????????????????????????????????????????????????????????????????????
> article_id       str     Unique article identifier
> title            str     Article title
> skeleton         str     Section headings each followed by opening sentence
> The lead_paragraph column is withheld in the test set.
> Skeleton format
> Each skeleton entry looks like this:
> Early life
> Born in 1942 in rural Mississippi, she was the youngest of five children.
> Career
> She joined the company in 1968 as a junior analyst and rose to lead the division by 1979.
> Legacy
> Her work influenced a generation of researchers across three continents.
> The skeleton tells you the article's structure and the opening claim of each section. It does not contain enough text to paraphrase into a lead directly. The model must reason from the outline to produce an introduction that would appear before any of these sections in the finished article.
> Scale and diversity
> The training set spans a wide range of encyclopaedic article types. Articles about geographic locations, biological species, historical vessels, military equipment, biographical subjects, cultural events, and institutional entities each follow different lead conventions. A well-trained model must learn what kind of entity is being described from structural cues alone and apply the appropriate encyclopaedic opening pattern.
> Evaluation
> Submissions are scored on a composite of three signals, each targeting a distinct property of a well-formed encyclopaedic lead:
> score = 0.50 * ROUGE-L + 0.30 * title_presence + 0.20 * heading_coverage
> ROUGE-L (50%) measures longest common subsequence overlap with the reference lead paragraph. It rewards lexical fidelity to the reference phrasing and penalises outputs that are fluent but thematically divergent from the reference.
> Title presence (30%) is 1.0 if the article title appears in the generated lead as a discrete phrase (case-insensitive), and 0.0 otherwise. The match respects word boundaries, so the title must appear as a whole phrase rather than as a fragment inside a longer word: a title of "Cat" is credited by "The cat is a small mammal" but not by "This is a category page". Any punctuation in the title is matched literally. A trailing disambiguation parenthetical is removed from the title before matching, so the lead only needs to name the subject itself and not the disambiguator: "HMS Myrmidon (1867)" is matched on "HMS Myrmidon" and "Mercury (element)" on "Mercury", while a leading or internal parenthetical that is part of the actual name, such as "(Almost) Straight Outta Compton", is kept in full. Encyclopaedic convention requires the subject to be named explicitly in the opening sentence, and this component enforces that convention as a measurable signal rather than leaving it implicit in ROUGE. A generated lead that never names the subject fails this component entirely regardless of how fluent or accurate it is.
> Heading coverage (20%) measures what fraction of the skeleton section headings have at least one content word reflected in the generated lead. Each heading is reduced to its content words (short words and common stopwords are ignored), and a heading counts as covered when at least one of those content words appears as a whole-word token in the generated lead. A lead that addresses only one facet of a multi-section article is incomplete by encyclopaedic standards. This component rewards topical breadth and penalises generated leads that focus narrowly on a single section of the skeleton while ignoring the others.
> All three components are averaged across all 30,000 test articles. Higher is better. Score range: 0.0 to 1.0.
> Note on the achievable ceiling: submitting the exact reference lead_paragraph for every test article does not score 1.0. In practice it scores approximately 0.75 (ROUGE-L 1.0, title presence ?0.76, heading coverage ?0.12). This is expected and not a grading defect. Roughly a quarter of reference leads open with a fuller or different form of the subject's name than the literal article title (for example "Jim Dowd" is introduced as "James Thomas Dowd", and "Rob Grant" as "Robert Grant"), so the literal title string is genuinely absent from a meaningful fraction of ground-truth leads. Likewise, well-written encyclopaedic leads rarely restate a section heading verbatim, so heading coverage on real reference text is naturally low; the component is designed to catch leads that ignore the article's breadth entirely, not to reward leads that resemble the skeleton. Treat a score in the 0.70s as very strong, not as an indication of a bug in your pipeline.
> Submission Format
> Column           Type    Description
> ????????????????????????????????????????????????????????????????????????????????
> article_id       str     Must match an article_id from test.csv
> generated_lead   str     Your generated 1 to 3 sentence lead paragraph
> The article_id values in test.csv are opaque identifiers. The example rows below use placeholder ids purely to illustrate the format; use the actual ids from test.csv in your submission.
> Example rows:
> article_id,generated_lead
> 3f9a1c04e8b7449da2c6f0518e7b3a91,"Cumberland Terrace is a Grade I listed building on the east side of Regent's Park in London, designed by John Nash and completed in 1826 as part of his grand plan for the park commissioned by the Prince Regent."
> b7d2e6690a1f4c3e8f95a02d1c74be83,"Drumkul, also spelt Dirumkul, is an artificial freshwater lake in southern Gorno-Badakhshan Autonomous Province in eastern Tajikistan, identified by BirdLife International as an Important Bird Area."
> c081547af2664b9db3ee7c9a15d0f6a2,"The fawn-breasted wren (Cantorchilus guarayanus) is a species of bird in the family Troglodytidae, found in Bolivia, Brazil, and Paraguay."
> Requirements
> Must contain exactly 30,000 rows, one per test article
> Must include the header row
> Every generated_lead must be a non-empty string
> Leads longer than 150 words will be truncated to 150 words before scoring
> What To Use
> Any pretrained sequence-to-sequence or causal language model available on HuggingFace that fits the CPU compute budget above ? T5-small, T5-base, BART-base, DistilBART, and GPT-2 small are all well suited. (Multi-billion-parameter models such as Mistral and LLaMA are not viable on CPU within the 90-minute limit.)
> QLoRA or LoRA fine-tuning on the provided training set
> Standard tokenization and preprocessing libraries (HuggingFace Transformers, tokenizers)
> ROUGE evaluation libraries for offline validation (rouge-score, evaluate)
> The provided title and skeleton as the only input context at inference time
> What Not To Use
> External retrieval of the source article at inference time, including web search, live Wikipedia queries, or any API or network call to fetch the article, its body, or its lead paragraph. The provided title and skeleton are the only permitted inference input.
> Wikipedia dumps, snapshots, or the underlying structured-wikipedia dataset used to look up or reconstruct the reference lead for a given title. The lead must be generated from the skeleton, not retrieved.
> Any attempt to reverse or de-anonymise an article_id back to its original Wikipedia page.
> The withheld test lead_paragraph values, or any other source of ground-truth labels for the test split.
> Hand-written or manually looked-up leads for individual test articles, and external labelled datasets whose contents overlap the test references. Sourcing the target text by any of these routes is data leakage and invalidates the submission.
> Compute Budget
> Your solution runs on CPU only ? there is no GPU at inference time. The target hardware is:
> 10 CPU cores, 62.5 GB RAM, no GPU
> 90-minute wall-clock limit to generate the full 30,000-row submission, including model loading, tokenization, generation, and writing the output file.

Inspiration note: Useful because it turns lead generation into structure-only reasoning, with a clear output shape and a clever metric that blends overlap, explicit subject naming, and topical breadth.

## Few-Shot Hyper-Relation Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bqfp4he8qqvmyr655pe8atn89qvj3
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (1)
> Your Submissions
> SchemaShift
> Overview
> SchemaShift is a few-shot, episode-based information-extraction challenge.
> For each query sentence, participants must predict every directed hyper-relation defined by a small labeled support set. Each prediction must identify the relation head, relation tail, anonymous relation label, and every qualifier attached to that relation.
> Candidate entity spans are provided for every sentence. All predicted head, tail, and qualifier spans must exactly match one of those candidates.
> Each episode defines a temporary extraction schema using anonymous labels such as R0, R1, R2, Q0, and Q1. These labels are remapped independently in every episode.
> For example, R1 may represent an award relation in one episode and a family relation in another. Q0 may represent a date, location, role, quantity, country, time period, or another contextual value.
> Participants must infer from the current episode’s support examples what each relation and qualifier label means, which entities serve as relation heads and tails, the direction of each relation, which qualifier types are valid, and which relation each qualifier modifies.
> The support annotations are the only authoritative definition of the active schema. Label numbers, label order, support order, query order, and episode identifiers carry no semantic meaning.
> A system must therefore interpret every anonymous label independently in every episode. Assigning permanent global meanings to labels such as R0, R1, or Q0 is not permitted.
> The underlying records describe factual relations involving people, organizations, locations, creative works, awards, memberships, family relationships, roles, dates, time periods, quantities, ordinal values, and related contextual information.
> SchemaShift models temporary or customer-defined schemas, newly introduced ontology terms, changing extraction objectives, and few-shot deployment without training a separate model for every ontology.
> The challenge is designed for CPU-only execution. Suitable systems include compact pretrained encoders, embedding models, classical classifiers, retrieval systems, prototype methods, structured predictors, and hybrid learned-deterministic pipelines.
> Central Evaluation Principle
> The objective is not to recover one universal relation vocabulary.
> The objective is to infer an ontology that applies only within the current episode and then use it consistently across that episode’s queries.
> Successful systems must combine schema interpretation, semantic matching, argument-role prediction, relation-direction prediction, qualifier interpretation, qualifier attachment, exact span selection, abstention, and complete graph construction.
> Surface Variation
> Some episodes include surface-level transformations intended to reduce sentence memorization while preserving the extraction problem.
> Possible transformations include replacing entity names with synthetic alternatives of similar type, replacing numerical values while preserving token positions, replacing selected non-entity words with token-preserving alternatives, or adding short prefixes and suffixes while shifting affected spans.
> Participants may use only the released competition files and permitted pretrained models.
> Searching for source sentences, source annotations, or external copies of the underlying records is prohibited.
> Hyper-Relations
> A core relation contains a head entity span, a tail entity span, and an anonymous relation label.
> A hyper-relation may additionally contain one or more qualifiers. Each qualifier contains a value span and an anonymous qualifier label.
> Qualifiers are evaluated together with their parent relation.
> A qualifier receives no credit when its span and label are correct but it is attached to the wrong relation.
> A complete prediction must therefore recover both the factual relation edge and the relation-specific context attached to that edge.
> Required Capabilities
> A strong system should jointly perform few-shot schema induction, support-query semantic comparison, relation detection, head and tail assignment, direction prediction, qualifier interpretation, qualifier labeling, qualifier attachment, exact token-span prediction, and structured output generation.
> The complete support set should be considered before solving the queries in an episode.
> Candidate entity spans are supplied. Participants do not need to perform unrestricted named-entity recognition and may not submit spans outside the provided candidate set.
> Machine-Learning Requirement
> SchemaShift is an ML-oriented challenge.
> A valid system must include at least one trained or pretrained machine-learning component that meaningfully contributes to prediction.
> The learned component may support semantic similarity, schema interpretation, relation detection, label selection, role assignment, direction prediction, qualifier attachment, or confidence estimation.
> Eligible components include pretrained language or embedding models, token, span, or sentence encoders, compact sequence-to-sequence models, classifiers trained on learned representations, metric-learning systems, meta-learning systems, graph-prediction models, and other learned architectures.
> Hybrid systems are allowed and encouraged.
> Deterministic components may handle candidate generation, lexical features, retrieval, thresholding, constrained decoding, span alignment, validation, deduplication, and output canonicalization.
> Keyword features, regular expressions, patterns, and schema heuristics may be used within a hybrid system. A system based only on fixed rules does not satisfy the machine-learning requirement.
> Nearest-neighbor and retrieval methods are allowed when retrieval is restricted to the current episode’s support set, the released public training data, and locally computed representations.
> Anonymous labels must still be interpreted independently in every episode.
> Task
> For each episode, participants receive a set of anonymous relation labels, a set of anonymous qualifier labels, a labeled support set, and an unlabeled query set.
> Each support example contains tokenized text, candidate entity spans, and labeled hyper-relations.
> Each query contains tokenized text and candidate entity spans but no relation annotations.
> For every query, participants must predict all hyper-relations supported by the episode-local schema.
> Each predicted relation must contain a head span, a tail span, an anonymous relation label, and a qualifiers list. Every qualifier must contain an anonymous qualifier label and a value span.
> A query may contain no relations, one relation, or several relations. A relation may have no qualifiers, one qualifier, or multiple qualifiers.
> When no relation is predicted, return an empty list:
> []
> Dataset Size
> The released challenge contains 3,000 public training episodes and 1,000 public test episodes.
> Each episode contains 5 to 8 relation labels, 3 to 6 qualifier labels, 8 to 14 support examples, and 3 to 5 query examples.
> Counts vary by episode.
> Dataset Files
> public/train.jsonl
> This is a JSON Lines file containing one complete training episode per line.
> Each episode contains the fields episode_id, relation_labels, qualifier_labels, support, queries, and answers.
> The answers field contains the ground-truth relations for the training queries.
> public/test.jsonl
> This is a JSON Lines file with the same structure as train.jsonl, except that answers is omitted.
> Participants must generate predictions for every query in this file.
> public/sample_submission.csv
> This is the submission template.
> It contains one row per test query and exactly three columns in the following order:
> episode_id,query_id,relations
> The sample submission uses an empty JSON list for every prediction.
> Episode Fields
> episode_id
> Type: string
> A unique identifier for the episode.
> It carries no semantic information and must not be used as a prediction feature.
> relation_labels
> Type: list of strings
> All anonymous relation labels available in the episode.
> Predictions may use only labels from this list.
> qualifier_labels
> Type: list of strings
> All anonymous qualifier labels available in the episode.
> Predictions may use only labels from this list.
> support
> Type: list of support objects
> The labeled demonstrations that define the episode-local schema.
> queries
> Type: list of query objects
> The unlabeled examples that must be solved using the support set.
> answers
> Type: list of answer objects
> This field is present only in train.jsonl.
> It contains one ground-truth answer object for every training query.
> Queries and answers are matched by query_id:
> query.query_id == answer.query_id
> List position does not carry semantic meaning and should not be used to associate a query with its answer.
> Token-Span Requirements
> All spans use inclusive-start, exclusive-end indexing.
> Every submitted head, tail, and qualifier span must exactly match an entity span supplied for the corresponding query.
> Participants must calculate spans against the original tokens list.
> Models may use a different tokenizer internally, but all submitted spans must be aligned back to the dataset tokenization.
> Submission Format
> Submit one CSV file based on public/sample_submission.csv.
> The file must contain exactly three columns in the following order:
> episode_id,query_id,relations
> Each test query must appear exactly once. The submission therefore contains one row per query rather than one row per episode.
> The episode_id and query_id values must be copied exactly from public/test.jsonl.
> The relations column has the logical data type “JSON array serialized as CSV text.” Its value must be a valid JSON list containing zero or more relation objects.
> A query with no predicted relations must use:
> []
> Predictions must use valid JSON syntax. Strings must use double quotes, and spans must be two-element JSON lists containing integers.
> Submission Requirements
> Each expected query must have exactly one valid row.
> Every relations value must decode to a JSON list and may contain no more than 200 relation objects.
> Head, tail, and qualifier spans must each contain two integers satisfying:
> 0 <= start < end
> Every submitted span must exactly match an entity span supplied for the query.
> Relation labels must come from the current episode’s relation_labels list. Qualifier labels must come from its qualifier_labels list.
> Duplicate core relations and duplicate qualifiers are not permitted.
> Evaluation
> SchemaShift uses a maximization score ranging from 0.0 to 1.0.
> Higher scores are better.
> The final score is:
> Score = 0.25 × Core Relation Micro F1
> 0.25 × Attached Qualifier Micro F1
> 0.20 × Exact Query Graph Accuracy
> 0.20 × Episode-Balanced Graph F1
> 0.10 × Local-Label-Balanced F1
> Compute Environment
> The official environment provides 10 CPU cores, 64 GB RAM, and no GPU, TPU, or other accelerator.
> The complete prediction pipeline must run in this environment. This includes model loading, preprocessing, support analysis, inference, qualifier attachment, decoding, validation, and submission generation.
> CPU-Friendly Baseline Strategy
> Because candidate entity spans are supplied, a practical baseline can formulate the task as structured candidate ranking.
> Candidate ranking is generally more efficient than unrestricted graph generation.

Inspiration note: Useful because it turns few-shot extraction into a structured graph-generation task with episode-local schemas, exact span constraints, and JSON-serialized outputs that still fit a CPU-only setup.

## Ciphered Dialogue Thread Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a0h9fdae37bjp5nbke426vn8ap7vv
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (18)
> Your Submissions
> Ciphered Dialogue Thread Reconstruction
> Overview
> Two short conversations have been mixed together. You receive twelve anonymous speech turns in shuffled order, noisy local clues about rough dialogue position and possible next turns, and a small voice profile for every possible speaker. Your job is to separate the two conversations, put the turns in the correct order inside each conversation, and label the speaker of every turn.
> This is an NLP sequence-to-structure task. A prediction is an unordered pair of labeled dialogue paths, not a class label or a free-form continuation. Solving it requires three coupled abilities:
> separate the twelve turns into the two hidden conversations;
> recover the exact order within each conversation; and
> match each turn to a row-local speaker from short examples.
> The underlying passages come from real, structured dramatic texts. Whole source plays are disjoint between train and test. Searchable names and content phrases are removed by a row-local lexical cipher, and every row mixes two separated passages. The public clues are deliberately partial: they do not reveal which conversation a turn belongs to and they do not give the exact order.
> What you must predict
> Each row contains twelve turn aliases (U1 through U12) and between four and seven cast aliases (K1, K2, ...). Submit exactly two strands separated by ||.
> Each strand must contain exactly six items. An item has the form:
> TURN@CAST
> A complete prediction has this shape:
> U7@K2 U1@K2 U9@K4 U3@K1 U12@K4 U5@K1 || U2@K3 U8@K5 U4@K3 U11@K2 U6@K5 U10@K2
> The order of the two strands does not matter. The order inside each strand does matter. Every public turn alias must appear exactly once, and every cast alias must come from that row.
> Understanding the ciphered text
> Speech text is space-tokenized.
> | Token form | Meaning |
> |---|---|
> | `the`, `if`, `why`, `shall` | Visible grammatical or discourse word. |
> | `W037` | Row-local alias for a content word. The same source word receives the same alias within one row only. |
> | `D03` | Row-local alias for a number. |
> | `?`, `,`, `;` | Visible punctuation token. |
> W037 in one row has no relationship to W037 in another row. The cipher preserves repetition, grammatical shape, punctuation, question/answer cues, and lexical overlap between cast examples and query turns while preventing source-title or phrase lookup. Each cast profile now contains three support speeches, giving speaker-attribution models a real but still noisy row-local signal.
> Dataset files
> ### `train.csv`
> Column	Type	Description
> id	string	Unique row identifier with no semantic meaning.
> turn_cards	JSON list	Twelve shuffled objects containing a turn alias, ciphered text, noisy beat_hint, and noisy next_candidates.
> cast_cards	JSON list	Four to seven cast profiles, each with a cast alias and three ciphered example speeches.
> thread_count	integer	Always 2.
> turns_per_thread	integer	Always 6.
> target_exchange	string	Training-only answer: two six-item TURN@CAST strands separated by `||`.
> ### `test.csv`
> `test.csv` has the same five public columns as `train.csv` and omits `target_exchange`.
> sample_submission.csv
> | Column | Type | Description |
> |---|---|---|
> | `id` | string | Test row ID. |
> | `predicted_exchange` | string | Your two-strand labeled dialogue reconstruction. The supplied blank dummy scores `0`. |
> JSON structures
> Turn card
> {"turn":"U4","text":"why should i W019 the W006 ?","beat_hint":"middle","next_candidates":["U2","U7","U11"]}
> Field	Type	Description
> turn	string	Row-local alias matching U[1-9][0-9]*.
> text	string	Space-tokenized ciphered speech.
> beat_hint	string	Noisy rough-position clue: early, middle, late, or uncertain. It is sometimes wrong and is not tied to a conversation label.
> next_candidates	list[string]	Three weakly ranked candidate turn aliases that might follow this turn in a hidden conversation. The list contains decoys, can omit the true next turn, and is meaningless for final turns.
> ### Cast card
> {"cast":"K2","examples":["i W014 it well .","what shall we W003 now ?","nay , i W021 no W008 ."]}
> | Field | Type | Description |
> |---|---|---|
> | `cast` | string | Row-local speaker alias matching `K[1-9][0-9]*`. |
> | `examples` | list[string] | Exactly three ciphered speeches by that speaker, outside the two query passages. |
> Evaluation
> The grader treats the two predicted strands as unordered. It checks partition, order, speaker labels, and labeled links separately so useful partial solutions receive credit without giving a large score to arbitrary valid output.
> For two sets P and T:
> F1(P,T) = 2 * |P intersection T| / (|P| + |T|)
> When one set is empty and the other is not, F1 is 0.
> Partition
> Create the 30 unordered pairs of turns that occur in the same true strand. PartitionRaw is F1 between predicted and true same-strand pairs. A random balanced two-way partition has a substantial chance floor, so it is removed:
> Partition = max(0, (PartitionRaw - 5/11) / (1 - 5/11))
> Within-thread order
> There are 30 ordered precedence pairs inside the two true strands. WithinRaw is the fraction placed in the same predicted strand and in the correct direction. Its balanced-random floor is removed:
> WithinOrder = max(0, (WithinRaw - 5/22) / (1 - 5/22))
> Adjacent links
> AdjacentF1 is F1 over the ten directed adjacent-turn pairs (previous_turn, next_turn) in the two strands.
> Speaker labels
> For each true cast alias, compare the set of turns assigned to that cast. SpeakerMacroF1 is the unweighted mean of these cast-specific F1 values. Predicting the most frequent cast therefore cannot dominate the component.
> Labeled links
> LabeledLinkF1 is F1 over the ten tuples:
> (previous_turn, previous_cast, next_turn, next_cast)
> This component rewards adjacency only when both endpoint speakers are also correct.
> Exact reconstruction
> ExactExchange is 1 only when both labeled strands are exactly correct, allowing the two strands to be swapped; otherwise it is 0.
> Row and final score
> row_score =
> 0.10 * Partition
> + 0.10 * WithinOrder
> + 0.25 * AdjacentF1
> + 0.30 * SpeakerMacroF1
> + 0.20 * LabeledLinkF1
> + 0.05 * ExactExchange
> final_score =
> 0.85 * mean(row_score over all test rows)
> + 0.15 * mean(the lowest-scoring 20% of test rows)
> The score is finite and bounded in [0, 1]. The sample scores 0; an oracle scores 1. There is no hidden family label in the metric.
> Invalid prediction behavior
> A row receives 0 if its prediction has malformed items, an unknown alias, a repeated or missing turn, anything other than two strands, or anything other than six items per strand.
> The entire submission is rejected for wrong column names or order, a wrong row count, missing IDs, duplicate IDs, unknown IDs, or extra columns. Rows are aligned by id, never by file order.
> Submission format
> The submission must contain exactly these columns in this order:
> | Column | Type | Description |
> |---|---|---|
> | `id` | string | Test ID copied exactly from `test.csv`. |
> | `predicted_exchange` | string | Two valid six-item strands separated by `||`. |
> CSV example:
> id,predicted_exchange
> 0a12bc34de56f789,U7@K2 U1@K2 U9@K4 U3@K1 U12@K4 U5@K1 || U2@K3 U8@K5 U4@K3 U11@K2 U6@K5 U10@K2
> What not to use
> Do not infer meaning from id, row order, U numbering, K numbering, JSON serialization order, or the order of cast cards. All are independently reassigned or shuffled.
> Do not treat beat_hint or next_candidates as ground truth. They are noisy scaffolding: they can be wrong, include cross-conversation decoys, omit true links, and never directly identify the hidden thread. The first candidate is only a weak suggestion, not a guaranteed successor.
> Do not treat W or D aliases as global vocabulary. Their meanings reset in every row.
> Do not search for the original play or line. A public row mixes two separated passages, removes titles and character names, and ciphers content words.
> Do not output JSON, prose, probabilities, more than two strands, or separators other than ||.
> Do not collapse all turns onto one speaker. Speaker scoring is macro-averaged, and labeled links require both endpoint speakers.
> Do not optimize only pairwise order. The metric removes the random pairwise floor and gives most weight to adjacency, speaker matching, and their joint correctness.
> Benchmark boundary
> Sentence-ordering benchmarks recover one sequence from shuffled sentences but do not jointly infer row-local speakers or separate two source conversations. Conversation-disentanglement benchmarks normally retain chronological message order and known speaker identities while predicting thread membership or reply links. Literary speaker-attribution benchmarks predict who spoke a quotation without reconstructing two ordered threads.
> This challenge changes multiple axes at once: the public turns are shuffled, two ordered paths must be recovered from weak structural hints, speaker labels are anonymous and learned from row-local demonstrations, searchable content is ciphered, and evaluation includes exact labeled adjacency. It is therefore a constrained dialogue path transduction problem rather than a renamed instance of any one neighboring task.

Inspiration note: Useful because it turns dialogue disentanglement into a compact two-path reconstruction problem with speaker labeling, ordering, and structured strand output all at once.

