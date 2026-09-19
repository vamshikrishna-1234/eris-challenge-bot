# CPU Fine-Tuning Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 23

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.
## Vocal Imitation Sound Category Recognition

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74q4gk8yyjjsf2d5vvnxpdz58ax7aj
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio, Dataset source is visible after the challenge closes.
- Best/top context: Beat urwashi's score of 0.699!

### Full Challenge Description

> Overview
> When people cannot name a sound, they imitate it: they growl like a cat, sputter like a motorbike, or go "wee-ooo" like a siren. These vocal imitations are how humans query sounds when words fail, the basis of "search by voice" for audio. They are also acoustically bizarre: a single human vocal tract stretches to approximate engines, bells, and animals, so the imitation of a motorcycle shares almost nothing spectrally with a real motorcycle.
> Your task: given a short recording of a person vocally imitating a real-world sound, predict the ontology category of the sound they were imitating (e.g. Animal > Domestic animals, pets > Cat). This is a fine-tuning problem. The sensible path on CPU is to turn each clip into a log-mel spectrogram and fine-tune a pretrained model, but the real difficulty is generalization:
> The test imitators are different people from the training imitators. The train/test split is imitator-disjoint: no participant appears in both. A model that latches onto one person's quirks will not transfer.
> Some mistakes are worse than others. Confusing an imitated cat growl for an imitated dog bark (both Animal > Domestic animals, pets) is far less wrong than calling it an aircraft. Scoring reflects this via the ontology (below).
> Evaluation
> Submissions are scored with a hierarchy-aware, class-balanced metric.
> For each test clip, let pred and true be ontology paths (lists of levels d1 > d2 > d3). Per-clip similarity is Wu-Palmer style:
> def sim(pred_path, true_path):
> shared = 0
> for a, b in zip(pred_path, true_path):
> if a == b:
> shared += 1
> else:
> break
> if not pred_path or not true_path:
> return 0.0
> return 2.0 * shared / (len(pred_path) + len(true_path))
> So an exact match scores 1.0; sharing d1+d2 but not d3 scores 0.667; sharing only d1 scores 0.333; an unrelated branch (or a label not in the ontology) scores 0.0.
> The final score macro-averages over the true classes: compute the mean per-clip similarity within each true class, then average those class means. This means rare categories count as much as common ones.
> Be aware that the hierarchy gives constant baselines a non-trivial floor: because a wrong guess still earns partial credit for a shared d1/d2 branch, a single-label constant prediction does not score near zero. On this dataset a constant majority-class prediction scores about 0.20, the best constant (a well-chosen class in the largest branch) about 0.25, and random labels about 0.18. Exact match is still worth far more than branch-only credit, so beating these floors requires a real model, but do not mistake a score in the low 0.2s for a working solution.
> def score(rows):                       # rows: (true_label, sim) pairs
> from collections import defaultdict
> per_class = defaultdict(list)
> for true_label, s in rows:
> per_class[true_label].append(s)
> class_means = [sum(v) / len(v) for v in per_class.values()]
> return sum(class_means) / len(class_means)
> Range is [0, 1]; higher is better.
> Dataset
> prepare.py produces the following. The set of target classes is derived deterministically from the data (well-populated depth-3 ontology categories); it is listed in ontology.csv and typically contains about 15 to 20 classes.
> public/
> train/                 # training .wav imitations (variable length, mono)
> test/                  # test .wav imitations, imitators disjoint from train
> train.csv              # filename, label, imitator_id
> test.csv               # filename        (no labels, no imitator_id)
> sample_submission.csv  # filename, label (all set to one placeholder class)
> ontology.csv           # label, category_d1, category_d2, category_d3, label_id
> train.csv: filename (in train/) maps to label (the full ontology string, e.g. Sounds of things > Vehicle > Motor vehicle (road)) plus imitator_id, an anonymized id of the person who produced the imitation. Use imitator_id to build an imitator-disjoint validation split. The test set's imitators are disjoint from training, so test.csv deliberately omits this column.
> ontology.csv: the complete set of valid labels and their d1/d2/d3 ancestors. Predicted labels must be one of these exact strings to earn credit; anything else scores 0.0.
> Audio is single-channel WAV. Clips vary in length (roughly 1 to 10 s) and were recorded on consumer microphones, so expect background noise and clipping.
> Submission
> Submit a CSV named submission.csv. Columns:
> filename (string): a filename from test/, must match test.csv exactly.
> label (string): predicted label, an exact string from ontology.csv.
> Requirements
> Exactly one row per test clip (same count and filenames as test.csv).
> Include the header row.
> label must be one of the strings in ontology.csv["label"].
> Notes
> This is CPU-only with a ~1.5 h budget. The intended approach is log-mel spectrograms plus fine-tuning a small pretrained CNN (e.g. torchvision resnet18/mobilenet_v3_small treating the spectrogram as an image), not training a large network from scratch.
> Watch for leakage: build any validation split by held-out imitator_id, not random clips. A random-clip split lets one person's imitation style appear in both train and validation, inflating your local score in a way that will not survive the imitator-disjoint test set.
> Classes are imbalanced and the metric is macro plus hierarchy-aware. A constant prediction already floors around 0.20-0.25 from branch-only partial credit, so treat that band as "no model," not as progress; covering rare classes and landing exact-match (not just the right branch) are what push the score above it.
> Allowed
> CPU-only computation within the ~1.5 h budget.
> Standard Kaggle Docker libraries (e.g. numpy, pandas, scikit-learn, librosa, soundfile, torch, torchvision, torchaudio).
> Pretrained models and fine-tuning them: ImageNet CNNs applied to spectrogram images, or pretrained audio encoders, including downloading their published weights at runtime.
> Any input representation you derive from the audio (log-mel, MFCC, CQT, raw waveform, learned features).
> Data augmentation (SpecAugment, time shift/stretch, additive noise, mixup, and so on).
> Ensembling, cross-validation, and test-time augmentation.
> Using the imitator_id column in train.csv to build an imitator-disjoint validation split.
> Not allowed
> Recovering test labels from any external source. Predictions must be produced by a model trained on the provided train/ data. Matching, fingerprinting, or otherwise re-identifying test/ clips against any external audio collection to look up their categories is prohibited.
> Manually listening to and hand-labeling test clips.
> Hardcoding predictions, or otherwise not producing them from a trained model.
> Using external/pretrained data that overlaps the test imitations.
> Training on the test clips or tuning on the test set in any way (no labels are provided for test/).

Inspiration note: Useful for active/budgeted evidence-acquisition challenge designs with reconstruction outputs.

## Shuffled Prompt Template Assembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71he8tp8bgb599zd0kavcyk98bx069
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Shuffled Prompt Template Assembly
> Plain language objective: fine-tune a local model, or train a compact model from scratch, for structured prompt-fragment classification and graph decoding. For each PromptSource prompt-template row, use a shuffled packet of row-local Jinja and natural-language fragments to recover which fragments belong on the template input side, which belong on the target-response side, and the correct order within each side.
> PromptSource templates are human-written prompt programs. They combine natural-language instructions with Jinja placeholder syntax such as {{ question }} or {% if condition %}. A standard template has an input side that becomes the model prompt and a target side that becomes the expected model response.
> Each public row represents one prompt-template assembly instance. You receive:
> an opaque row ID;
> a shuffled candidates_json packet containing five to fifteen row-local fragments;
> exactly two authentic distractor fragments from another prompt in the same source family; and
> for training rows only, the correct assembly_json target.
> For every test row, predict a compact structured assembly: the ordered input-side fragment IDs and the ordered target-side fragment IDs. IDs omitted from both lists are treated as distractors.
> This is a supervised fine-tuning / train-from-scratch structured text challenge. It is not sequence generation, translation, prompt writing, dataset-task classification, ordinary text classification, semantic matching, or scalar regression. The scored object is the row-local prompt program structure: fragment roles plus boundary-aware ordering edges.
> The closest public analogues study prompt recovery or shuffled-text reconstruction. This challenge instead scores executable PromptSource/Jinja template assembly with row-local distractors, explicit input/target separation, grouped held-out source families, and a role-plus-edge metric. A solution must learn structural evidence from the released training rows, not recover a source file or memorize public PromptSource templates.
> Only offline local solutions are allowed. Strong solutions may fine-tune open-source models or build and train architectures from scratch within the platform runtime. Fine-tune the best local open-source model for this prompt-fragment classification and graph-decoding task: map shuffled candidate fragments to ordered input and target fragment ID lists. The intended solution trains only on the released public files, not by looking up the upstream source repository or shortcutting through IDs, row order, source UUIDs, filenames, private preparation artifacts, or source metadata.
> What Not To Use / What Not To Do, violation may cause rejection regardless of score:
> Do not download, index, fingerprint, search, or query PromptSource, its mirrors, source archives, source commits, public prompt repositories, or web search to recover hidden test assemblies.
> Do not use external datasets, prompt repositories, source copies, mirrors, source UUIDs, source paths, template names, file names, row order, hashes, packaging details, generator salts, split seeds, or platform artifacts as answer channels.
> Do not use hosted APIs, remote inference services, closed-source teacher APIs, runtime-downloaded model weights, challenge-specific pretrained checkpoints, external labels, or manual annotations of held-out rows.
> Do not inspect private answers, grader internals, prepare-script outputs outside public/, or filesystem side channels.
> Do not reduce the task to source lookup, fixed template matching, source-family identification, dataset-task classification, rule-only parsing, or prompt text regeneration.
> Do not fit, calibrate, cluster, pseudo-label, or adapt on the complete test distribution. Test data may be used only for per-row inference.
> Do not exploit malformed JSON, duplicate IDs, extra columns, overlong cells, impossible references, repeated fragment IDs, or other grader attacks.
> Enforcement on invalid approaches: solutions may be reviewed for actual use of the public training rows, source-lookup code, remote calls, hidden-answer access, metadata-only behavior, test-distribution adaptation, and rule-only shortcuts. The goal is to reward learned prompt-template structure recovery from row-local evidence, not source retrieval or format exploits.
> Task
> For each test row, read candidates_json and submit assembly_json.
> candidates_json is a shuffled JSON array. Each object has:
> fragment_id: a row-local ID such as p00, unique within that row;
> text: a natural-language and/or Jinja fragment.
> Every real packet has five to fifteen fragments. Exactly two fragments are distractors. The remaining fragments must be split into:
> input_order: fragment IDs in left-to-right order before the input/target delimiter;
> target_order: fragment IDs in left-to-right order after the input/target delimiter.
> Each list must be non-empty. The two lists may not overlap. Submit only fragment IDs; do not rewrite fragment text.
> Example candidate packet:
> [
> {"fragment_id":"p00","text":"Passage: {{ context }}"},
> {"fragment_id":"p01","text":"Question: {{ question }}"},
> {"fragment_id":"p02","text":"{{ answer_choices[label] }}"}
> ]
> Example assembly:
> {
> "input_order": ["p00", "p01"],
> "target_order": ["p02"]
> }
> The example above is a compact schema illustration. Real packets follow the same object format but contain five to fifteen fragments and exactly two distractors.
> Intended Approach
> A practical solution fine-tunes a compact local open-source model, or trains a small architecture from scratch, to classify fragment roles and decode a coherent prompt-template graph. The model should use the fragment text, Jinja syntax, natural-language instruction flow, placeholder dependencies, punctuation, answer-choice cues, and local coherence between candidate fragments.
> Suitable approaches include supervised fragment encoders, pairwise role and adjacency classifiers, compact Transformers, recurrent encoders, graph neural networks, contrastive/coherence models, constrained decoding, and small verifier models that check whether a proposed assembly forms a plausible PromptSource/Jinja prompt program. A strong system can score candidate assemblies with learned role probabilities and boundary-aware edge probabilities, then decode valid non-overlapping input and target lists.
> Good validation should be train-only and grouped by source family, because complete source families are held out from train to test. Calibration should come from public training folds. Open-source local libraries such as NumPy, pandas, scikit-learn, PyTorch, JAX, TensorFlow, and local transformer tooling are appropriate when run within the selected platform runtime. Internet-dependent inference, hidden source metadata, and source-row lookup are not allowed.
> Evaluation
> Each submitted assembly_json is parsed as a JSON object with exactly two keys: input_order and target_order. Both values must be non-empty lists of unique row-local fragment IDs. The lists must not overlap, and every referenced ID must exist in that row's candidate packet.
> For every candidate fragment, the submitted role is:
> input if its ID appears in input_order;
> target if its ID appears in target_order;
> omit otherwise.
> Let F1_input, F1_target, and F1_omit be ordinary set-based F1 scores for those three roles:
> F1 = 2 * |predicted intersection expected| / (|predicted| + |expected|)
> The role score is:
> Role = (F1_input + F1_target + F1_omit) / 3
> For ordering, each side becomes a set of directed boundary-aware edges. A list [a,b,c] produces START->a, a->b, b->c, and c->END, tagged with its side. Input and target edge sets are combined. Edge is the same set-based F1 formula applied to submitted versus expected edges.
> The row score is:
> row_score = 0.55 * Role
> + 0.45 * Edge
> Held-out rows belong to three private structural groups:
> control_flow   = original template contains Jinja control statements
> choice_mapping = answer-choice mapping without control statements
> direct_render  = all other templates
> The final score blends mean row quality with worst-group robustness:
> Final = 0.85 * mean(row_score)
> + 0.15 * worst private structural group
> The private group labels are used only by the grader. They are not random buckets and are not public columns. Higher is better. The theoretical minimum is 0.0, the theoretical maximum is 1.0, and a perfect valid submission scores exactly 1.0.
> The grader requires exactly the submission columns in the listed order, one row per test ID, unique IDs, and the exact test ID set. Wrong columns or column order, duplicate IDs, missing IDs, extra IDs, blank IDs, or an ID-set mismatch make the entire submission invalid. Row-local malformed JSON, wrong keys, empty lists, unknown IDs, repeated IDs, overlapping lists, nested lists, overlong cells, or impossible references make the affected row score zero without crashing the grader.
> Dataset
> The prepared data is under public/. Complete source families are assigned wholly to train or test. No source family used in test contributes a training row.
> File overview:
> Item	Description
> train.csv	Training inputs plus assembly_json labels
> test.csv	Test inputs only
> sample_submission.csv	Weak valid template with required columns
> train.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> candidates_json	JSON string	Shuffled candidate fragment packet
> assembly_json	JSON string	Train label with ordered input/target fragment IDs
> test.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> candidates_json	JSON string	Shuffled candidate fragment packet
> candidates_json schema:
> Field	Type	Description
> fragment_id	string	Row-local ID matching pNN; unique within packet
> text	string	Non-empty natural-language and/or Jinja fragment
> assembly_json schema:
> Key	Type	Description
> input_order	JSON list of strings	Ordered input-side fragment IDs
> target_order	JSON list of strings	Ordered target-side fragment IDs
> The candidate fragments are row-local. A fragment ID such as p02 has no meaning outside its own row. Candidate order is shuffled and is not the template order.
> Submission
> Submit a CSV with exactly these two columns in exactly this order:
> Column	Type	Constraint
> id	string	Same IDs as test
> assembly_json	JSON string	Object with input_order and target_order
> assembly_json must be a JSON object with exactly two keys: input_order and target_order. Both values must be non-empty lists of unique candidate fragment IDs from that row. The lists must not overlap. IDs omitted from both lists are treated as distractors.
> Example submission rows:
> id,assembly_json
> row_0123456789abcdef0123,"{""input_order"":[""p00"",""p01""],""target_order"":[""p02""]}"
> row_abcdef0123456789abcd,"{""input_order"":[""p03"",""p04""],""target_order"":[""p00""]}"
> Requirements are strict: start from sample_submission.csv or write the same header yourself, preserve exactly one row per test id, keep the columns in the table order, and do not add extra columns. Duplicate IDs, missing IDs, extra IDs, reordered columns, blank IDs, or an ID-set mismatch make the whole submission invalid. Malformed row-local assembly_json cells score zero for the affected row.
> Submissions
> 32

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Food Descriptor Program Fine-Tuning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79r142jdkf30gay7jmze8ncx8bsrrk
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> National dietary surveys record what people eat as free text — a short product
> description typed by a fieldworker or copied off a label. Before that text is usable it
> has to be annotated with a descriptor program: one symbol naming the product's base
> category, plus any number of typed descriptors that pin down how the product was sourced,
> processed, preserved, packaged and cooked. A trained coder does this by hand, following an
> in-house convention that says which descriptor families a given kind of product is obliged
> to carry and which value to choose inside each family. That convention was never
> published. It exists only implicitly, in the annotations themselves.
> This is a fine-tuning task. You are given a niche, expert-annotated corpus — 21,360
> labelled descriptions in train.csv — and your job is to adapt a pretrained language
> model to a specialised annotation convention it has never seen. 4,215 unlabelled
> descriptions in test.csv are held out for scoring. The annotations are real coder
> output and are never perturbed. Difficulty comes instead from what was removed from the
> inputs: roughly a third of the attribute clauses were deleted from every description
> before publication, so the text you fine-tune on is a lossy view of what the coder saw.
> Recovering a descriptor whose clause is gone means inferring it from the product's
> identity and from the clauses that survived.
> Every symbol is opaque. Base categories, descriptor families and descriptor values were
> put through a fixed permutation, so b0363 and g19.d0845 mean the same thing in every
> row but mean nothing outside this corpus and cannot be looked up anywhere. No pretrained
> checkpoint has ever seen this vocabulary, so the symbol inventory and the convention that
> governs it must both be acquired during fine-tuning, from the released training split
> alone. The product text, by contrast, is ordinary English, and the pretrained knowledge
> that transfers is knowledge of what a food actually is — that a courgette is a
> vegetable, that speculaas is a biscuit. That transfer is what lets you annotate a product
> the training split never mentions. Test descriptions are drawn from head nouns absent
> from training, so copying the nearest training row does not work.
> What makes this hard to fine-tune well: the label inventory is large and very long-tailed
> (1,445 base symbols over 21,360 examples), the number of descriptors per product is not
> stated anywhere in the input and varies from 0 to 20, and 22.8% of products correctly take
> no descriptors at all, so a model that over-produces is punished as hard as one that
> under-produces. Output is checked against a strict grammar, so the fine-tuned model has to
> be reliable in format, not merely approximately right. The released corpus is small and the
> descriptions are short, so a compact pretrained encoder fine-tunes in minutes on modest
> hardware; model capacity is not the binding constraint here, the withheld convention is.
> To be explicit about what this is not: nothing in a description lines up positionally with
> anything in its annotation, so there is no correspondence between the two to exploit. It
> is also not one label per row — the annotation is a structured program whose size is
> itself part of what has to be predicted. The intended first-order approach is to
> fine-tune a pretrained model on train.csv so that it produces the annotation string
> for a description directly: use the identity words in the description to select the base
> symbol, then use the surviving attribute clauses together with what the base symbol
> implies to decide which descriptor pairs apply, including deciding that none apply.
> Evaluation Metric
> Let 𝑁 be the number of scored rows. Each row contributes a true base symbol and a true
> multiset of descriptor pairs; your prediction contributes the same two things.
> Term A — base symbol agreement above chance. Pool a 𝐾 × 𝐾 count table 𝐶 over all
> rows, where 𝐶[𝑘][𝑙] counts rows whose true base symbol is 𝑘 and whose predicted base
> symbol is 𝑙, and 𝐾 covers every symbol appearing as either. Write 𝑆 = Σₖ Σₗ 𝐶[𝑘][𝑙],
> 𝑐 = Σₖ 𝐶[𝑘][𝑘], 𝑡ₖ = Σₗ 𝐶[𝑘][𝑙] and 𝑝ₖ = Σₗ 𝐶[𝑙][𝑘]. Then:
> 𝑅 = (𝑐 × 𝑆 − Σₖ 𝑝ₖ × 𝑡ₖ) ⁄ √( (𝑆² − Σₖ 𝑝ₖ²) × (𝑆² − Σₖ 𝑡ₖ²) )
> 𝐴 = max(0, 𝑅)
> Term F — descriptor agreement, pooled over every row at once. With 𝑃ᵢ the predicted
> pair multiset for row 𝑖 and 𝑇ᵢ the true one:
> TP = Σᵢ |𝑃ᵢ ∩ 𝑇ᵢ|
> Precision = TP ⁄ Σᵢ |𝑃ᵢ|
> Recall = TP ⁄ Σᵢ |𝑇ᵢ|
> 𝐹 = 2 × Precision × Recall ⁄ (Precision + Recall), and 𝐹 = 0 whenever TP = 0
> Final score.
> Score = 100 × clip(0.40 × 𝐴 + 0.60 × 𝐹, 0, 1)
> A score of 0 means no agreement beyond chance on either term. A score of 100 means every
> base symbol and every descriptor pair is exactly right. Because the two terms are pooled
> across the whole held-out split rather than averaged per row, answering only the easy rows
> does not lift them: a submission that produces no descriptors anywhere scores 𝐹 = 0, and
> a submission that repeats one base symbol everywhere scores 𝐴 = 0.
> Any row whose prediction is missing, empty, non-numeric where a symbol is required, or not
> well formed under the grammar below is scored as a base symbol that is always wrong and is
> additionally charged as many spurious descriptor pairs as the true annotation holds. An
> unparseable answer is therefore never cheaper than an honest wrong guess.
> Reference points measured on the shipped grader, using only the released public files:
> sample_submission.csv as shipped — 0.00
> distractor-only rule keyed on batch_code — 3.93
> always produce the three commonest descriptor pairs — 4.32
> nearest-neighbour copy from the training split — 29.34
> competent linear model over character and word features — 41.66
> stronger model adding pretrained sentence embeddings — 44.31
> exact reconstruction — 100.00
> Dataset
> train.csv — 21,360 rows.
> sample_id — integer — row identifier
> product_text — string — the published product description
> batch_code — string — survey round, one of R1, R2, R3, R4
> target_program — string — the descriptor program to be reproduced
> test.csv — 4,215 rows.
> sample_id — integer — row identifier
> product_text — string — the published product description
> batch_code — string — survey round, one of R1, R2, R3, R4
> sample_submission.csv — 4,215 rows, a valid but deliberately weak submission.
> sample_id — integer — row identifier
> prediction — string — a constant base symbol and no descriptors
> symbol_vocabulary.csv — 2,993 rows listing every admissible symbol.
> symbol — string — the symbol
> symbol_type — string — base for a base symbol, pair for a family-and-descriptor pair
> The vocabulary holds 1,445 base symbols and 1,548 descriptor pairs, the pairs spanning 27
> descriptor families and 1,401 descriptor values. Every symbol appearing in a held-out
> answer also appears somewhere in train.csv, so nothing scored is unlearnable from the
> released data.
> batch_code is a distractor. It is assigned from a hash, its four values are within
> 0.02 of uniform, and conditioning on it shifts the base-symbol distribution by at most
> 0.0055. Any rule built on it scores near zero.
> Submission
> Submit a CSV with a header row and exactly 4,215 data rows, one per held-out sample_id.
> sample_id — integer — must match a sample_id in test.csv; each exactly once
> prediction — string — the descriptor program as space-separated symbols
> Grammar:
> the first symbol is a base symbol matching b followed by four digits
> each remaining symbol is a pair matching g plus two digits, a dot, then d plus four digits
> a program holds at least 1 and at most 64 symbols, so zero descriptor pairs is a valid answer
> pair symbols are compared as a multiset, so the order you write them in does not matter; a
> pair repeated within a row counts as an extra prediction and costs precision
> Programs in train.csv hold up to 21 symbols, and no answer in the held-out split holds
> more than 12.
> Identifiers are checked strictly: duplicate, missing or unrecognised sample_id values and
> a wrong row count are all rejected outright. Columns are handled leniently, so a small
> formatting slip does not throw away a real attempt — surplus columns such as an index column
> written by to_csv are dropped, column order is free, row order is free, and surrounding
> whitespace on an identifier is trimmed. A required column that is absent, or repeated, is
> still rejected.
> Example, using real identifiers from test.csv:
> sample_id,prediction
> 12170,b1332
> 12692,b0864 g19.d0845 g23.d0251
> 19939,b0309 g08.d1184 g10.d0828 g15.d0025 g15.d1455 g19.d0812 g23.d0548 g23.d0581 g23.d0686
> What Not to Use
> A constant answer. Repeating one base symbol everywhere scores 𝐴 = 0 because Term A
> is corrected for chance, and the shipped sample submission measures 0.00.
> Producing no descriptors. Term F is pooled globally, so predicting nothing anywhere
> gives TP = 0 and 𝐹 = 0, even though 22.8% of held-out rows genuinely take no descriptors.
> Frequency shortcuts. Always producing the commonest descriptor pairs measures
> 4.32: precision collapses because the common pairs are wrong far more often than
> they are right.
> The distractor. A rule keyed on batch_code measures 3.93. It is balanced by
> construction and carries no signal about the answer.
> Nearest-neighbour copying. Reusing the closest training description measures
> 29.34, well under a trained model, because the split is partitioned by head noun and
> held-out products are ones the training split never names.
> An off-the-shelf pretrained model used as-is. No checkpoint has seen this symbol
> inventory, and the permutation behind it is not published, so there is no external table
> to join against and nothing useful to extract zero-shot. The convention has to be learned
> by fine-tuning on the released training split.
> What is expected instead is a pretrained model fine-tuned on train.csv until it has
> absorbed both the symbol inventory and the coding convention — placing an unfamiliar
> product into a base category from what the words mean, then deciding which descriptor
> families that category obliges you to fill and which value each one takes, including the
> decision to fill none.
> Submissions
> 32

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cardiac and Respiratory Audio Source Separation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a748sb6jdfze6hbspkk5f758bmvab
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each test row is a 4.0-second digital-stethoscope recording made while a controlled simulator plays a cardiac program and a respiratory program together. Reconstruct the sound contributed by each program, sample by sample, place heartbeat and breath evidence on the shared timeline, and mark intervals where overlap reduces certainty.
> These are simulator recordings, not patient recordings. The cardiac channel contains repeating cycle sounds centered on beat complexes. The respiratory channel contains airflow sounds that extend across breath intervals. The target is a synchronized acoustic account of both channels, not a diagnosis.
> Hidden supervision comes from three synchronized captures of the same controlled setup: cardiac-only, respiratory-only, and both programs together. Preparation joins two paired 2-second passages, applies deterministic timing and spectral response changes, and forms the public recording from the transformed source channels, retained recording context, and low-level noise. The transformed cardiac-only and respiratory-only channels are the hidden replay targets.
> This is a CPU-only Fine-Tuning audio reconstruction task. Solutions must use CPU computation only. Training rows expose both replay waveforms and their temporal evidence. Test rows contain the observed WAV, an opaque id, a coarse chest zone, and fixed recording-format fields.
> Task
> Return one synchronized record for every test row:
> Output	Required prediction
> Heart replay	The 4.0-second cardiac-source waveform
> Lung replay	The 4.0-second respiratory-source waveform
> Event ledger	Heartbeat center times and boundaries, breath intervals, event confidence, and overlap regions
> Uncertainty	Bounded uncertainty for both source replays and both event families
> Confidence	Finite row-level confidence in [0,1]
> Base64 is only the transport container. The prediction itself is an ordered pair of time-domain waveforms plus structured evidence on the same 4.0-second clock. Every waveform payload must decode to exactly 16,000 little-endian int16 mono samples at 4,000 Hz.
> Concordance Contract
> All five prediction fields describe the same acoustic episode and are checked against distinct hidden evidence. The heart and lung payloads are compared independently with their replay targets. Heartbeat and breath entries are matched to hidden source-derived events rather than inferred from the submitted payloads. Uncertainty is checked against hidden source and event ambiguity, while source consistency compares the sum of the two submitted replays with the sum of the two hidden replays.
> No output can substitute for another. The row score uses the minimum of heart replay quality, lung replay quality, and event-ledger quality as its completeness support. Full credit therefore requires two correctly ordered waveforms, aligned cardiac and respiratory evidence, calibrated uncertainty, and a physically coherent recombination for one shared timeline.
> Intended Approach
> Fine-tune a compact offline open-source audio encoder using only the supplied training rows. A practical system can share an encoder across a cardiac replay decoder, a respiratory replay decoder, and temporal evidence heads. Time-frequency masks, lightweight waveform decoders, residual-derived overlap estimates, and calibrated ensembles all fit the contract. Signal-processing features may support the learned model, but fixed filters alone are only a baseline.
> The official tier is CPU with 10 cores and 62 GB RAM. Solutions must finish within 1.5 hours. The public data is small enough for in-memory feature extraction, compact CPU fine-tuning, and efficient local inference.
> What Not To Do
> Do not use source lookup, raw file matching, recovered source IDs, filenames, row order, file size, modification time, or archive order.
> Do not use external annotations, private answers, hidden preparation metadata, or hardcoded id-to-answer maps.
> Do not use hosted APIs, closed remote inference, runtime internet calls, or private teacher labels.
> Do not submit scalar-only, label-only, or fixed-template outputs that ignore the waveform replay contract.
> Do not exploit malformed JSON, oversized payloads, invalid base64, duplicate IDs, missing IDs, or grader behavior.
> Enforcement on invalid approaches: submissions may be reviewed for source lookup, metadata reconstruction, private-file access, external calls, fixed answer maps, and approaches that avoid the required audio replay and event-ledger task.
> Evaluation
> The concordance score combines waveform fidelity, event precision/recall/F1, interval IoU, uncertainty agreement, and replay-sum consistency. Higher is better. Every component and the final score lie in [0,1]; a perfect valid submission scores exactly 1.0.
> Rows are aligned by id. Wrong columns or column order, duplicate IDs, or a missing, extra, or foreign ID raises InvalidSubmissionError. A malformed waveform or JSON payload gives that row a score of 0.0 without affecting other rows.
> 1. Heart and lung replay scores
> The same replay metric is applied separately to heart_pcm16_b64 and lung_pcm16_b64. Let P be the submitted float waveform after PCM16 decoding, T the hidden target, and clip(x)=min(1,max(0,x)).
> power        = mean(T^2) + 1e-12
> pred_energy  = mean(P^2) + 1e-12
> energy_ratio = min(pred_energy, power) / max(pred_energy, power)
> energy_gate  = sqrt(energy_ratio)
> NRMSE = sqrt(mean((P-T)^2) / power)
> time  = clip(1 - NRMSE / 1.10)
> corr  = clip(PearsonCorrelation(P, T))
> energy = clip(1 - abs(log(pred_energy / power)) / 2.2)
> For the spectral term, both waveforms are framed with a 512-sample Hann window and 128-sample hop. Each frame becomes log1p(abs(rFFT(frame))).
> spectral_MAE = mean(abs(predicted_log_spectrum - target_log_spectrum))
> spectral_scale = mean(abs(target_log_spectrum)) + 0.05
> spectral = clip(1 - spectral_MAE / (1.45 * spectral_scale))
> * (0.20 + 0.80 * energy_gate)
> replay_score = (0.30*time + 0.34*spectral + 0.22*corr + 0.14*energy)
> * (0.30 + 0.70*energy_gate)
> This produces heart_score and lung_score. An exact PCM16 payload receives exactly 1.0.
> 2. Heartbeat and breath event score
> Events are split into the heart and lung families. Within each family, candidate pairs are sorted by match quality from highest to lowest and accepted greedily while both events are unmatched. This creates deterministic one-to-one matches.
> Event family	Eligible submitted/reference pair	Matched-pair quality
> Heartbeat	Absolute center-time error is at most 0.12 seconds	0.68*time_quality + 0.32*boundary_quality
> Breath interval	Interval IoU is positive or midpoint error is at most 0.35 seconds	0.70*IoU + 0.30*midpoint_quality
> The quality terms are:
> time_quality = max(0, 1 - abs(pred_time-true_time) / 0.12)
> boundary_quality = max(0, 1 - (abs(pred_start-true_start)
> + abs(pred_end-true_end)) / 0.24)
> midpoint_quality = max(0, 1 - abs(pred_time-true_time) / 0.35)
> IoU = intersection_length / union_length
> For either event family, let M be the number of accepted matches, P the submitted count, and R the reference count.
> precision = M / P
> recall    = M / R
> F1        = 2 * precision * recall / (precision + recall)
> If P=R=0, F1 is 1.0. If one side is empty or M=0, F1 is 0.0. heart_timing and breath_timing are the mean matched-pair qualities. A timing score is 1.0 when both family lists are empty and 0.0 when a non-empty family has no match. For each matched event, confidence credit is max(0,1-abs(pred_confidence-true_confidence)); the family confidence score is the mean of those credits. It is 1.0 when both event lists are empty and 0.0 when no submitted event matches a non-empty reference. The count term is:
> count_score = max(0, 1 - abs(P_total-R_total) / max(1,R_total))
> Overlap regions are also matched one-to-one, in descending interval IoU, and only positive-IoU pairs are eligible. region_F1 uses the same M, P, R, precision, recall, and empty-set rules above. If both region lists are empty, region_score is 1.0. Otherwise, mean_matched_IoU is zero when no regions match.
> region_score = 0.60*region_F1 + 0.40*mean_matched_IoU
> event_core = 0.30*heart_F1 + 0.16*heart_timing + 0.10*heart_confidence
> + 0.24*breath_F1 + 0.12*breath_timing + 0.04*breath_confidence
> + 0.04*count_score
> events_score = 0.90*event_core + 0.10*region_score
> 3. Uncertainty score
> The four required uncertainty values are heart-source, lung-source, heartbeat-event, and breath-event uncertainty. Each receives:
> scalar_credit = clip(1 - abs(predicted-target) / 0.75)
> uncertainty_score = 0.85*mean(four scalar credits) + 0.15*region_score
> The region_score here is computed from uncertainty_json.regions with the same region matching defined above.
> 4. Row score
> The row-level components are:
> Component	Weight	Rewarded behavior
> Heart replay	0.25	Accurate temporal and spectral heart waveform
> Lung replay	0.25	Accurate temporal and spectral lung waveform
> Event ledger	0.22	Correct heartbeat, breath, confidence, and overlap evidence
> Source consistency	0.12	Submitted sources recombine consistently
> Uncertainty	0.10	Calibrated source and event uncertainty
> Source-family balance	0.06	Similar supported quality across both replay streams and the ledger
> consistency_score applies the replay metric from step 1 to clip(submitted_heart + submitted_lung, -1, 1) against the hidden sum of the target sources. The balance term is:
> balance_score = (1 - min(1,abs(heart_score-lung_score)))
> * min(heart_score,lung_score,events_score)
> The six row components are combined as follows:
> heart_score       = waveform replay score for heart_pcm16_b64
> lung_score        = waveform replay score for lung_pcm16_b64
> events_score      = matched heartbeat and breath ledger score
> uncertainty_score = bounded uncertainty agreement
> consistency_score = agreement of the two submitted sources
> balance_score     = source-family balance term
> core = 0.25 * heart_score
> + 0.25 * lung_score
> + 0.22 * events_score
> + 0.12 * consistency_score
> + 0.10 * uncertainty_score
> + 0.06 * balance_score
> required_support  = min(heart_score, lung_score, events_score)
> completeness_gate = 0.70 + 0.30 * sqrt(required_support)
> supported_core    = core * completeness_gate
> row_score         = supported_core * (1 - 0.05 * abs(confidence - supported_core))
> The completeness gate is task-aligned: an answer cannot retain full partial credit by reconstructing only one source or by omitting the event ledger. It preserves the relative quality of supported predictions and equals 1.0 when all three required heads are perfect.
> 5. Final score
> The grader first computes the mean of all row scores. It then checks four hidden grouping axes: heart activity family, lung activity family, auscultation zone, and row-local segment position. For each axis, it computes every subgroup mean and keeps the lowest subgroup mean. The four axis minima are then averaged.
> worst_group = mean(
> minimum heart-activity subgroup mean,
> minimum lung-activity subgroup mean,
> minimum auscultation-zone subgroup mean,
> minimum segment-position subgroup mean
> )
> Final = 0.82*mean(row_score) + 0.18*worst_group
> Every checked subgroup has at least 12 scored test rows. The theoretical minimum is 0.0; the theoretical maximum is 1.0.
> Dataset
> The public bundle contains short source-neutral WAV episodes prepared from controlled simulator captures. It omits original filenames, exact source IDs, pair IDs, source row order, sound-type labels, simulator settings, exact recording landmarks, raw timestamps, hidden split groups, and private answer metadata.
> The split keeps each complete underlying waveform family on one side: all row variants and every byte-identical cardiac, respiratory, or combined capture remain together. Test rows therefore use held-out paired recordings while every scored physiological activity family remains represented in training.
> Prepared split:
> Item	Value
> Train rows	291
> Test rows	144
> Audio format	4,000 Hz PCM16 mono
> Samples per row	16,000
> Duration per row	4.0 seconds
> File overview
> Item	Description
> train/audio/*.wav	Train mixed WAVs
> test/audio/*.wav	Test mixed WAVs
> train.csv	Inputs plus labels
> test.csv	Test inputs only
> metadata.json	Format constants
> sample_submission.csv	Valid template
> train.csv columns
> Column	Type	Description
> id	string	Opaque row id
> mixed_wav	path	Mixed WAV path
> auscultation_zone	string	upper_chest, mid_apex_chest, or lower_costal_chest
> recording_context	string	Always clinical_manikin_stethoscope
> sample_rate_hz	int	Always 4000
> sample_count	int	Always 16000
> duration_sec	float	Always 4.0
> heart_pcm16_b64	string	Train heart replay
> lung_pcm16_b64	string	Train lung replay
> events_json	JSON	Train event ledger
> uncertainty_json	JSON	Train uncertainty
> confidence_label	float	Label confidence
> test.csv columns
> Column	Type	Description
> id	string	Opaque row id
> mixed_wav	path	Mixed WAV path
> auscultation_zone	string	upper_chest, mid_apex_chest, or lower_costal_chest
> recording_context	string	Always clinical_manikin_stethoscope
> sample_rate_hz	int	Always 4000
> sample_count	int	Always 16000
> duration_sec	float	Always 4.0
> Label JSON format
> events_json is a JSON object with keys events and uncertain_regions. Each event object has:
> source: heart or lung
> type: heartbeat or breath_interval
> time: row-local seconds
> start: row-local seconds
> end: row-local seconds
> confidence: value in [0,1]
> Heart events use source=heart and type=heartbeat. Lung events use source=lung and type=breath_interval. Times must stay inside [0, 4.0], and every event must satisfy start <= time <= end.
> uncertain_regions is a JSON list of overlap intervals. Every item has source="both", finite start and end in [0,4.0] with start <= end, and reason="overlap". At most 20 regions are allowed.
> uncertainty_json is a JSON object with:
> source_uncertainty: {"heart": value, "lung": value}
> event_uncertainty: {"heartbeat": value, "breath": value}
> regions: optional list of uncertain regions
> All uncertainty values must be finite numbers in [0, 1].
> The regions list uses the same overlap-region object schema as events_json.uncertain_regions. The two lists should describe the same row-local uncertainty evidence.
> Submission
> Write ./working/submission.csv with exactly one row for every test id. Use the following columns in exactly this order:
> Column	Type	Constraint
> id	string	Same set as test
> heart_pcm16_b64	string	16000 int16 samples
> lung_pcm16_b64	string	16000 int16 samples
> events_json	JSON	Event ledger
> uncertainty_json	JSON	Bounded uncertainty
> confidence	float	In [0,1]
> Waveform payload rules:
> Decode with base64.b64decode.
> Interpret bytes as little-endian int16.
> Require exactly 16,000 mono samples.
> Sample rate is fixed at 4,000 Hz.
> Each base64 cell is limited to 52,000 characters, each JSON cell to 20,000 characters, events_json.events to 40 items, and each region list to 20 items. Missing, extra, duplicated, or reordered columns, or a missing, extra, or duplicated id, makes the whole submission structurally invalid. A malformed waveform, JSON object, or non-finite/out-of-range confidence instead scores 0.0 only for that row; every other valid row is still scored.
> The supplied sample_submission.csv is a valid weak template with full fixed-length payloads. Replace every prediction field with your own reconstructed source replays, event ledger, uncertainty object, and confidence.
> Illustrative rows are shown below. <42668-char-base64> denotes one complete payload and must be replaced by a real base64 string; ellipses are not valid submission content.
> id,heart_pcm16_b64,lung_pcm16_b64,events_json,uncertainty_json,confidence
> cpsr_076f308edeb0a60c5b,<42668-char-base64>,<42668-char-base64>,"{""events"":[],""uncertain_regions"":[]}","{""event_uncertainty"":{""breath"":0.6,""heartbeat"":0.6},""regions"":[],""source_uncertainty"":{""heart"":0.6,""lung"":0.6}}",0.30
> cpsr_081ee5cf3bf9841f76,<42668-char-base64>,<42668-char-base64>,"{""events"":[],""uncertain_regions"":[]}","{""event_uncertainty"":{""breath"":0.6,""heartbeat"":0.6},""regions"":[],""source_uncertainty"":{""heart"":0.6,""lung"":0.6}}",0.30
> Submissions
> 0

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Vendor-Disjoint Six-Way Vulnerability Assessment Card Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx777vqmb2byv4w51zrhf2s8518aj68x
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data
- Best/top context found: ↑ Higher is better

Full challenge description from page:

> Objective
> You are given six anonymized software-vulnerability reports and six shuffled security assessment cards. For each report, identify which card describes the same underlying vulnerability.
> For every report, submit six probabilities: the probability that its correct match is card_1, card_2, and so on through card_6. The six reports in a batch must collectively match the six cards one-to-one.
> The target is the hidden card assignment. The recommended modeling approach is described separately and is not part of the target definition.
> Overview
> This challenge uses transformed records derived from an official 2023 United States government vulnerability feed. Each original record describes a software or hardware security flaw and includes structured information about how the flaw can be exploited and what damage it can cause.
> A test batch presents the same six shuffled assessment cards beside six different vulnerability evidence briefs. Your task is to decide which card belongs to each brief. In simple terms, you are solving a six-way matching puzzle:
> Read a vulnerability evidence brief.
> Compare it with the six candidate assessment cards in that batch.
> Assign probabilities to the six possible card slots.
> Repeat this for all six briefs while respecting the fact that each card is used exactly once.
> The public evidence is deliberately transformed. A brief_text does not contain the original CVE identifier, vendor, product, version, URL, reference, or verbatim description. Instead, it summarizes mechanism cues, access conditions, likely effects, and a shuffled set of partly masked technical concepts.
> Each assessment card summarizes one candidate vulnerability using a coarse weakness family, platform type, attack route, attack complexity, required privilege, user interaction, authority scope, and confidentiality-integrity-availability impact profile.
> The correct answers form a permutation. Within every complete six-row batch, card slots 1 through 6 are each correct exactly once. This means that a locally plausible prediction can still be globally inconsistent if several briefs place too much probability on the same card.
> Why This Task Is Distinct
> This task is not ordinary CVSS classification, independent label prediction, or retrieval against a global corpus.
> It is a set-conditioned matching problem. The correct output for one row depends on the other briefs and cards in the same batch.
> It requires permutation-constrained reasoning. Six independently plausible local decisions can still be globally invalid if they reuse a card.
> It evaluates calibrated probabilities rather than only hard assignments.
> It penalizes violations of the one-to-one structure through a batch-level column-consistency factor.
> It uses vendor-disjoint source-group generalization, so source families represented in test are absent from training.
> It uses transformed evidence rather than searchable source descriptions, so direct source lookup does not directly reveal the private card slot.
> Required Outputs
> For every row in test.csv, output:
> pair_id — The opaque row identifier.
> p_card_1 through p_card_6 — Probabilities that the row’s brief matches card slot 1 through 6.
> Each row’s six probabilities must be finite, lie in [0, 1], have positive mass, and sum to 1.0 within an absolute tolerance of 1e-6.
> There are no sentinel classes, loc_none values, or missing-target codes. Every hidden true_card_slot is an integer from 1 through 6.
> Required Fine-Tuning Setting
> This is a Fine-Tuning challenge. Competitive solutions should adapt a pretrained language model to compare brief-card semantics and then reconcile scores across the six-by-six batch.
> The requirement concerns the intended solution setting, not the formal target. The formal target remains the hidden card-slot permutation.
> Dataset
> The prepared dataset is derived from an official public 2023 United States government vulnerability feed. Each source record originally contains a vulnerability description plus structured security metadata. The preparation pipeline converts that material into a matching task while removing direct source identifiers.
> Public records do not contain original vulnerability identifiers, vendor names, product names, versions, URLs, references, CPE strings, numeric CWE identifiers, publication dates, verbatim descriptions, CVSS vectors, or CVSS scores.
> The source-group key is the normalized primary vulnerable vendor extracted from structured platform criteria. That key is used only during preparation and is never published. All records from one vendor are assigned to only one split, so no vendor source group appears in both train and test.
> What brief_text Contains
> A brief_text has four pipe-separated fields:
> mechanism_cues — The kind of flaw suggested by the source description, such as memory-boundary violation, path resolution escape, authorization check failure, or resource exhaustion.
> access_cues — Conditions needed to reach or exploit the flaw, such as network reachability, prior authentication, local access, victim action, or a special timing condition.
> effect_cues — Likely consequences, such as code execution, service disruption, confidential-data exposure, data modification, or privilege elevation.
> abstract_evidence — Entity-stripped technical terms whose original order has been destroyed. Some terms are replaced by [MASK] to reduce exact-source reconstruction.
> Illustrative brief_text value:
> mechanism_cues=path resolution escape | access_cues=network-reachable; no-prior-authentication | effect_cues=confidential-data exposure; data modification | abstract_evidence=archive; extraction; traversal; destination; [MASK]; overwrite; validation
> This example means that the transformed source evidence suggests a remotely reachable path-handling flaw that may expose or overwrite data. It does not reveal the original vendor, product, version, identifier, or sentence wording.
> What an Assessment Card Contains
> Every card_1 through card_6 value is a semicolon-separated record with these fields:
> weakness_family — A coarse software-flaw family, such as memory-safety, authorization, path-handling, or resource-management.
> platform_part — application, operating-system, hardware, or mixed.
> attack_route — routed-network, adjacent-network, local-session, or physical-presence.
> attack_complexity — ordinary-conditions or special-conditions.
> required_privilege — none, ordinary-conditions, or special-conditions, corresponding to no, low, or high required privileges.
> user_action — none or required.
> authority_scope — same-authority or cross-authority.
> impact_profile — The confidentiality, integrity, and availability impact values.
> Illustrative assessment-card value:
> weakness_family=path-handling; platform_part=application; attack_route=routed-network; attack_complexity=ordinary-conditions; required_privilege=none; user_action=none; authority_scope=same-authority; impact_profile=C:HIGH/I:HIGH/A:NONE
> A model should compare the meaning of the brief with all six cards. For the illustrative pair above, the shared path-handling, network-access, no-privilege, no-user-action, and confidentiality and integrity cues would make this card a plausible match.
> How Rows Form a Batch
> All six rows with the same batch_id contain the same card_1 through card_6 values. Each row contains a different brief_text and a different brief_slot.
> In train.csv, target_card_slot gives the correct card number for that row. For example, a value of 4 means that the brief matches the text in card_4.
> In test.csv, target_card_slot is omitted. Participants must predict its value probabilistically through p_card_1 through p_card_6.
> The private target is always one of the integers 1 through 6. There are no sentinel classes, no loc_none value, and no missing-target code.
> Split Sizes
> Training batches: exactly 360.
> Training rows: exactly 2,160, with 6 rows per batch.
> Test batches: exactly 120.
> Test rows: exactly 720, with 6 rows per batch.
> Pairwise auxiliary training rows: exactly 12,960, with 6 candidate-card rows for every training brief.
> Private answer rows: exactly 720.
> Every batch contains six records from six distinct source vendors. No vendor source group appears in both train and test.
> Public File Schemas
> train.csv
> ColumnTypeDescriptionpair_idstringOpaque identifier for one brief row.batch_idstringOpaque identifier shared by the six rows in a batch.brief_slotintegerPublic row position from 1 through 6 within the batch.brief_textstringTransformed vulnerability evidence brief.card_1stringCandidate assessment card in slot 1.card_2stringCandidate assessment card in slot 2.card_3stringCandidate assessment card in slot 3.card_4stringCandidate assessment card in slot 4.card_5stringCandidate assessment card in slot 5.card_6stringCandidate assessment card in slot 6.target_card_slotintegerTrain-only correct card slot from 1 through 6.difficultycategorical stringTrain-only batch stratum: standard, medium, or hard.
> test.csv
> ColumnTypeDescriptionpair_idstringOpaque identifier for one brief row.batch_idstringOpaque identifier shared by the six rows in a batch.brief_slotintegerPublic row position from 1 through 6 within the batch.brief_textstringTransformed vulnerability evidence brief.card_1stringCandidate assessment card in slot 1.card_2stringCandidate assessment card in slot 2.card_3stringCandidate assessment card in slot 3.card_4stringCandidate assessment card in slot 4.card_5stringCandidate assessment card in slot 5.card_6stringCandidate assessment card in slot 6.
> test.csv omits target_card_slot and difficulty. It also omits all original source identifiers, source-group keys, vendor names, product names, version strings, URLs, CPE strings, numeric CWE identifiers, references, publication dates, raw descriptions, CVSS vectors, and CVSS scores.
> sample_submission.csv
> The exact columns, in order, are:
> pair_id,p_card_1,p_card_2,p_card_3,p_card_4,p_card_5,p_card_6
> The file contains exactly 720 rows and assigns probability 1/6 to every card. It is a valid submission and scores exactly 0.0 under the grader’s numerical tolerance.
> assessment_card_guide.json
> This public auxiliary file defines the meanings of the transformed brief fields and assessment-card fields.
> Its contents explain:
> The six-card matching objective.
> The absence of sentinel classes.
> The meaning of mechanism_cues, access_cues, effect_cues, and abstract_evidence.
> The meaning of weakness_family, platform_part, attack_route, attack_complexity, required_privilege, user_action, authority_scope, and impact_profile.
> It contains no row-level targets, original source identifiers, or private mappings.
> dataset_metadata.json
> This public metadata file contains:
> Preparation-pipeline version.
> Raw source archive filename.
> Raw source archive SHA-256.
> Eligible-record counts.
> Train and test pool counts.
> Train and test source-vendor counts.
> Fixed public row and batch counts.
> Difficulty-stratum counts.
> A description of the source-group split.
> A description of the public identifier scheme.
> A description of the text transformation.
> It contains no source-record mapping and no private target information.
> Auxiliary Training File
> pairwise_train.csv
> This file expands each training brief into six brief-card candidate pairs.
> ColumnTypeDescriptionpair_idstringIdentifier of the original training brief.batch_idstringBatch identifier.brief_slotintegerBrief position from 1 through 6.card_slotintegerCandidate card position from 1 through 6.brief_textstringTransformed vulnerability evidence brief.card_textstringOne candidate assessment card.is_matchintegerTrain-only binary pair label; 1 for the true card and 0 otherwise.difficultycategorical stringTrain-only batch difficulty stratum.
> The file is intended for cross-encoder fine-tuning. It does not change the required test submission format.
> For each training pair_id, the file contains exactly six rows: one positive candidate with is_match = 1 and five negative candidates with is_match = 0.
> Controlled Construction
> Locate the raw ZIP, GZ, or JSON feed deterministically.
> Parse only records from the 2023 identifier year.
> Exclude rejected, reserved, short-description, missing-CPE, and missing-CVSS-v3.1 records.
> Choose a primary CVSS v3.1 assessment deterministically, preferring primary NVD assessments.
> Extract vulnerable CPE records recursively and derive a stable primary vendor source-group key.
> Retain vendor groups with 2 through 300 eligible records.
> Split complete vendor groups into train and test using SHA-256-based deterministic ordering.
> Remove source identifiers and create salted opaque batch and row identifiers.
> Replace URLs, emails, vulnerability identifiers, versions, paths, quoted literals, numbers, vendor tokens, and product tokens.
> Convert descriptions into controlled mechanism, access, effect, and abstract-evidence fields. Abstract evidence is canonicalized, hash-reordered, and partly masked.
> Create assessment cards from coarse weakness, platform, access, scope, and impact fields.
> Greedily create difficult six-record candidate sets with distinct vendors and distinct card signatures.
> Shuffle briefs and cards independently and deterministically within each batch.
> Assign exact difficulty quotas by deterministic ambiguity ranking.
> Generate public files, private answers, metadata, and validation reports.
> Difficulty Strata
> Difficulty is assigned by a deterministic ambiguity score based on pairwise card similarity, weakness-family collisions, and evidence density.
> Training batches:
> standard: 90 batches, weight 1.0.
> medium: 180 batches, weight 1.25.
> hard: 90 batches, weight 1.5.
> Test batches:
> standard: 30 batches, weight 1.0.
> medium: 60 batches, weight 1.25.
> hard: 30 batches, weight 1.5.
> The test difficulty label is private. Harder batches receive greater evaluation weight.
> Leakage and Source-Independence Safeguards
> Vendor groups are strictly disjoint between train and test.
> Every six-record batch also contains six distinct vendors.
> Original vulnerability IDs are never published.
> Public IDs are salted SHA-256 tokens rather than sorted or sequential mappings.
> Vendor and product tokens extracted from CPE data are removed from evidence.
> URLs, emails, versions, numbers, paths, quoted literals, and explicit vulnerability identifiers are replaced.
> Original sentence order is destroyed.
> Evidence concepts are hash-reordered and partly masked.
> Public cards contain no source-record identifiers.
> The hidden target is the private within-batch card permutation, not a public source label.
> The preparation pipeline checks source-record reuse, source-group overlap, batch vendor uniqueness, card-signature uniqueness, target permutations, class coverage, difficulty quotas, duplicate IDs, and public output size.
> No original source-record mapping is written to any public file.
> No vendor source group appears in both train and test.
> Evaluation
> Higher is better. The final score is a Python float in the closed interval [0, 1].
> The score has two main parts:
> Row probability quality. For each brief, the grader checks how much probability was placed on the correct card. This uses a Brier loss, so confident wrong predictions are penalized more than cautious predictions.
> Batch assignment consistency. The grader checks whether the total probability assigned to each card slot agrees with the one-to-one matching structure. This discourages assigning several briefs to the same card.
> The row component is converted into a skill score where a uniform six-way guess is the zero baseline and a perfect prediction is one. Predictions worse than the uniform baseline are clipped to zero rather than producing a negative challenge score.
> The batch-consistency factor is applied as a soft penalty through a fourth root. It rewards predictions that respect the matching structure without allowing the structural penalty to overwhelm the row-level probability score.
> Finally, standard, medium, and hard batches receive difficulty weights of 1.0, 1.25, and 1.5.
> Let p[i,j] be the submitted probability that brief row i matches card slot j. Let y[i,j] be the one-hot hidden target. There are six possible card slots.
> The row Brier loss is:
> B_i = sum over j=1..6 of (p[i,j] - y[i,j])^2
> For a uniform prediction, every card receives probability 1/6.
> The correct card contributes:
> (1/6 - 1)^2 = 25/36
> The five incorrect cards contribute:
> 5 * (1/6 - 0)^2 = 5/36
> Therefore, the uniform-prediction Brier loss is:
> B_uniform = 25/36 + 5/36 = 30/36 = 5/6
> The normalized row skill is:
> s_i = clip(1 - B_i / (5/6), 0, 1)
> Here, clip(x, 0, 1) means:
> Return 0 when x is below 0.
> Return 1 when x is above 1.
> Otherwise, return x unchanged.
> This transformation gives:
> s_i = 1 for a perfect row prediction.
> s_i = 0 for a uniform row prediction.
> s_i = 0 for any prediction whose Brier loss is worse than uniform, because negative values are clipped to zero.
> The grading platform can evaluate a row subset of answers.csv for a public or private leaderboard partition. A grading call can therefore contain only part of an original six-row batch.
> Let I_b be the set of rows from original batch b that are present in the current grading call.
> Let:
> n_b = number of rows in I_b
> For each card slot j, define the hidden target column mass and submitted column mass as:
> t[b,j] = sum over i in I_b of y[i,j]
> q[b,j] = sum over i in I_b of p[i,j]
> Because a complete source batch is a one-to-one permutation, every observed subset also has distinct correct card slots. Therefore, each t[b,j] is either 0 or 1.
> The mean absolute column-mass deviation is:
> D_b = (1/6) * sum over j=1..6 of abs(q[b,j] - t[b,j])
> The largest possible deviation for the rows visible in the current grading partition is:
> M_b = 2 * (n_b - minimum over j of t[b,j]) / 6
> For a complete six-row batch, every target column has mass 1. Therefore:
> n_b = 6
> minimum over j of t[b,j] = 1
> M_b = 2 * (6 - 1) / 6 = 10/6 = 5/3
> For a partial leaderboard subset, the same formula measures consistency only over the observed rows. It does not assume that unobserved rows were included in the submission.
> The column-consistency factor is:
> C_b = clip(1 - D_b / M_b, 0, 1)
> C_b = 1 when the submitted column totals exactly match the hidden observed assignment totals. It approaches 0 as too much probability is placed in incorrect card columns.
> Let w_i be the hidden difficulty weight. All observed rows belonging to the same original batch have the same weight.
> The weighted row skill is:
> R_b = (sum over i in I_b of w_i * s_i) / (sum over i in I_b of w_i)
> The batch score is:
> S_b = R_b * C_b^(1/4)
> The fourth root makes column consistency a moderate structural penalty. For example:
> 0.5^(1/4) is approximately 0.841
> Therefore, a column-consistency value of 0.5 multiplies the row score by approximately 0.841, rather than cutting it in half.
> Let W_b be the batch difficulty weight. The final score is:
> Score = clip(
> (sum over batches b of W_b * S_b)
> /
> (sum over batches b of W_b),
> 0,
> 1
> )
> A uniform submission has B_i = 5/6 for every row. Every row skill is therefore zero, and the final score is exactly 0.0 after numerical thresholding.
> A perfect submission assigns probability 1 to every correct card and produces the correct observed column totals. It therefore has zero Brier loss, unit column consistency, and a final score of exactly 1.0.
> Submission
> Submit one CSV file named submission.csv with exactly seven columns in this exact order:
> pair_id,p_card_1,p_card_2,p_card_3,p_card_4,p_card_5,p_card_6
> A valid one-row uniform example is:
> pair_id,p_card_1,p_card_2,p_card_3,p_card_4,p_card_5,p_card_6
> PAIR_d4c664be9eef1404,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666
> The example contains exactly seven columns and six probability values.
> Submission Requirements
> Column names and order must match exactly.
> Every test pair_id must appear exactly once.
> Duplicate pair_id values are invalid.
> Missing test IDs are invalid.
> Extra IDs are invalid.
> Missing values are invalid.
> Probability values must be numeric and finite.
> Every probability must lie in [0, 1].
> Every row must have positive probability mass.
> Every row must sum to 1.0 within an absolute tolerance of 1e-6.
> Row order is not scored; the grader aligns rows by pair_id after exact ID-set validation.
> A hard one-hot assignment is valid, but calibrated probabilities are rewarded when the evidence is ambiguous.
> The submission must contain exactly 720 data rows when scored against the full test set.
> The platform may score a public or private subset internally. Participants must still submit predictions for the complete public test.csv.
> Modeling Guidance
> Fine-tune a pretrained cross-encoder on pairwise_train.csv to score brief-card compatibility.
> Reshape the six-by-six compatibility scores for each batch and apply Sinkhorn normalization or a differentiable matching layer.
> Decode validation assignments with the Hungarian algorithm while retaining calibrated row probabilities for submission.
> Use vendor-group-disjoint validation rather than random row splits.
> Optimize or monitor the official normalized Brier-plus-column-consistency metric.
> Calibrate probabilities with temperature scaling, vector scaling, or a held-out calibration method that preserves row normalization.
> Consider a set transformer, graph neural network over the bipartite brief-card graph, or an iterative assignment model to exploit cross-row constraints.
> Evaluate standard, medium, and hard validation subsets separately.
> Confirm that card-slot ordering is preserved when converting pairwise compatibility scores into submission probabilities.
> Verify both row sums and batch-level column behavior before writing the final submission.
> What Not to Use
> Do not query external vulnerability databases, search engines, mirrors, or advisory sites to reconstruct source records.
> Do not attempt to reverse opaque IDs or recover original vendor, product, version, or vulnerability identifiers.
> Do not join against CPE, CWE, CVSS, reference, or advisory data not provided in the public challenge files.
> Do not use original source descriptions recovered from external systems.
> Do not validate with random row splits that place the same vendor family on both sides.
> Do not treat rows as independent without checking the six-by-six permutation structure.
> Do not submit six unnormalized compatibility scores; the grader requires row probabilities that sum to 1.
> Do not assume the grading platform always supplies complete six-row batches internally; public and private scoring partitions may contain partial batches.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## IssueSplice: Counterfactual Complaint Ontology Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7agry93j8a5rcpyg9kvabhq58bz93q
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Easy
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> IssueSplice: Counterfactual Complaint Ontology Repair
> Task
> Fine-tune a language model to repair a complaint whose discriminative phrase
> has been replaced by <EVIDENCE_GAP>. Each example also supplies a complete
> contrast complaint and its four-level ontology path. The contrast is
> deliberately plausible but belongs to a sibling path. Produce three coupled
> outputs:
> recover the missing phrase;
> reconstruct the target complaint's product, sub-product, issue, and sub-issue path; and
> identify the first ontology level where that path diverges from the supplied decoy path.
> The target path must be inferred from the masked narrative, while the contrast
> establishes the local decision boundary that the output must reject.
> Structural Difference
> IssueSplice is neither ordinary complaint classification nor standalone text
> infilling. The model must undo a counterfactual pairing: restore variable-length
> evidence, select a coherent path in a four-level taxonomy, and name the first
> branch at which its reconstruction departs from a lexically similar decoy.
> Partial labels, full-path consistency, evidence recovery, and boundary
> localization are scored separately and jointly. Small changes to the repaired
> phrase or one internal ontology level can therefore produce materially
> different scores without collapsing the task into exact-string grading.
> Construction removes exact duplicate source narratives, caps recurring opening
> templates, keeps supported ontology paths, and assigns companies as indivisible
> split groups. Because masking can make two different source narratives identical,
> the final masked inputs are deduplicated globally a second time. A contrast
> complaint always comes from another company in the same public partition and
> never has the target's complete ontology path.
> Dataset
> Public Split
> The 1,529 test examples are 17.2% of all 8,890 prepared examples. All 95 retained
> ontology paths occur in both partitions, while no company or normalized masked
> narrative crosses the partition boundary.
> train.csv
> test.csv
> test.csv contains the same seven input columns through decoy_sub_issue and
> omits all six targets.
> Submission Format
> Submit exactly one row per example_id with exactly these seven columns:
> example_id,recovered_span,product,sub_product,issue,sub_issue,divergence_level
> IS_004614304A3FCF59,alleged rent collection,Debt collection,Rental debt,Attempts to collect debt not owed,Debt is not yours,issue
> IS_006F6A91C89AB271,credit card balance,Credit card,General-purpose credit card or charge card,Trouble using your card,Card payment fee or surcharge,issue
> Use standard CSV quoting when a value contains commas. Start from
> public/sample_submission.csv so every identifier is present once.
> Metric
> The Penalized Contrastive Repair Utility has native range
> -0.20 to 1.00 and is maximized:
> 0.15 * ordered-token LCS F1(recovered_span)
> + 0.15 * exact recovered-span accuracy
> + 0.20 * mean accuracy over the four path fields
> + 0.10 * complete-path accuracy
> + 0.10 * divergence-level accuracy
> + 0.30 * joint exact accuracy of span, path, and divergence
> - 0.10 * invalid path-field rate
> - 0.05 * invalid divergence-label rate
> - 0.05 * zero span-overlap rate
> Text comparison is case-insensitive and punctuation-insensitive. The ordered
> token score rewards useful partial recovery, but the joint term makes a fully
> consistent repair worth more than unrelated component guesses. Invalid values
> and spans with no token overlap incur explicit penalties. A perfect submission
> scores 1.00; a submission that is invalid on every target and has no span
> overlap scores -0.20.
> Report stochastic systems using at least five independent runs and the mean
> score, together with sample standard deviation, minimum, and maximum. Do not
> select the best run as the primary result.
> Not Allowed Methods
> Looking up complaint IDs, phrases, or records in the database, API,
> search engines, mirrors, or other external corpora.
> Matching test narratives against externally downloaded complaint records.
> Manually labeling test examples or using human-in-the-loop test annotation.
> Using identifiers, file order, answer-file access, grader internals, or other
> evaluation artifacts to derive targets.
> Training on any additional complaint export beyond the supplied public
> training file. General-purpose pretrained language models are allowed.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Proof State Tactic Completion Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70ad1mmw7e61bsd6ep38d8g58222hs
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background and Overview
> Automatic formal proof generation requires interactive reasoning models that understand formal mathematical states and accurately predict state transitions. In formal proof systems like Lean 4, a proof progresses step-by-step through tacticsâ€”commands that manipulate the current proof state by applying logical rules, invoking automation, or referencing existing mathematical theorems and definitions (premises).
> The Proof-State Tactic Completion challenge is a structured formal-language completion task. Given the current proof state (state_before) and a short window of up to two preceding tactics (history_json), participants must build and fine-tune a model to generate a structured prediction object containing:
> The exact next tactic executed (tactic).
> The set of fully qualified premises referenced by the tactic (premises).
> The resulting active goal remaining after the tactic execution (goal_after).
> This challenge is framed as proof-state-conditioned model fine-tuning within a strict CPU-only computational envelope. Models must be trained on the provided training split during the competition run and used for inference on the test split.
> Dataset Information
> The challenge dataset consists of structured CSV files prepared for fine-tuning and evaluation:
> train.csv: The primary public training set containing input proof states, tactic histories, and gold-standard target JSON strings.
> test.csv: The public evaluation set containing input proof states and tactic histories for which valid predictions must be generated.
> sample_submission.csv: A valid submission template matching the exact format and row IDs of test.csv, populated with baseline default predictions.
> Data Schema and Contract
> The public datasets and prediction targets conform to the following schema and JSON specifications:
> +------------------+-------------------+-----------------------------------------------------------------------+
> | Column Name      | Data Type         | Description                                                           |
> +------------------+-------------------+-----------------------------------------------------------------------+
> | id               | UTF-8 String      | Opaque string identifier for each tactic transition record            |
> |                  |                   | (e.g., lt_0000000_12345678).                                         |
> +------------------+-------------------+-----------------------------------------------------------------------+
> | history_json     | UTF-8 JSON Array  | Serialized JSON array containing up to 2 preceding tactic strings     |
> |                  |                   | applied earlier in the theorem proof.                                 |
> +------------------+-------------------+-----------------------------------------------------------------------+
> | state_before     | UTF-8 String      | The Lean proof state before tactic execution, detailing local        |
> |                  |                   | hypotheses and the active target goal (containing "âŠ¢ ...").           |
> +------------------+-------------------+-----------------------------------------------------------------------+
> | target_json      | UTF-8 JSON String | (Present in train.csv / answers) The ground-truth target object.      |
> +------------------+-------------------+-----------------------------------------------------------------------+
> | prediction       | UTF-8 JSON String | (Present in submission) The predicted target JSON object.             |
> +------------------+-------------------+-----------------------------------------------------------------------+
> Structured Prediction Payload Contract
> Each prediction cell in your submission must contain a valid, serialized JSON string matching the following exact keys and structural limits:
> JSON
> {
> "goal_after": "âŠ¢ ...",
> "premises": ["Namespace.theorem_name"],
> "tactic": "exact ..."
> }
> goal_after: UTF-8 string (max length 2,000 characters) representing the active goal remaining after executing the tactic.
> premises: JSON array of UTF-8 strings (max 64 items, each item max length 300 characters) representing fully qualified premise names referenced by the tactic.
> tactic: UTF-8 string (max length 1,000 characters) representing the predicted single tactic execution.
> Note: Malformed JSON, extra/missing keys, or strings/arrays exceeding character/item limits will result in a row score of 0.0.
> Evaluation Metric
> The competition evaluates predictions across all three components of the tactic transition payload. Each row is scored using a composite weighted metric:
> RowScore
> =
> 0.35
> Ã—
> ð‘‡
> exact
> +
> 0.20
> Ã—
> ð‘‡
> F1
> +
> 0.20
> Ã—
> ð‘ƒ
> F1
> +
> 0.20
> Ã—
> ðº
> F1
> +
> 0.05
> Ã—
> ð‘‰
> valid
> RowScore=0.35Ã—T
> exact
> â€‹
> +0.20Ã—T
> F1
> â€‹
> +0.20Ã—P
> F1
> â€‹
> +0.20Ã—G
> F1
> â€‹
> +0.05Ã—V
> valid
> â€‹
> Exact Tactic Match (
> ð‘‡
> exact
> T
> exact
> â€‹
> ):
> 1.0
> 1.0 if the whitespace-normalized predicted tactic string exactly equals the normalized gold tactic; otherwise
> 0.0
> 0.0.
> Tactic Token F1 (
> ð‘‡
> F1
> T
> F1
> â€‹
> ): Token-level F1 score comparing Unicode-tokenized predicted tactic text against gold tactic text. Tokens are extracted using the pattern [A-Za-z_][A-Za-z0-9_'.]*|\d+|[^\s].
> Premise Set F1 (
> ð‘ƒ
> F1
> P
> F1
> â€‹
> ): Set-level F1 score comparing the predicted list of fully qualified premise strings against the gold premise set.
> Goal Token F1 (
> ðº
> F1
> G
> F1
> â€‹
> ): Token-level F1 score comparing tokenized predicted goal_after against gold goal_after.
> Tactic Syntax Validity (
> ð‘‰
> valid
> V
> valid
> â€‹
> ):
> 1.0
> 1.0 if the predicted tactic has balanced string literals and matching parentheses (), brackets [], and braces {}; otherwise
> 0.0
> 0.0.
> The overall competition score is the arithmetic mean of all row scores across the test set, clamped strictly to
> [
> 0.0
> ,
> 1.0
> ]
> [0.0,1.0]. A malformed prediction JSON or failed parse yields a row score of
> 0.0
> 0.0.
> Submission Format
> Submissions must be a single UTF-8 encoded CSV file named submission.csv containing exactly two columns in the following explicit order: id,prediction.
> Submission Constraints
> The id column must contain the exact set of IDs present in test.csv with no duplicates or missing rows.
> The prediction column must contain a valid JSON string conforming to the payload contract.
> Example Submission Row
> Code snippet
> id,prediction
> lt_0000000_12345678,"{""goal_after"":""âŠ¢ True"",""premises"":[""Mathlib.Algebra.Group.Basic""],""tactic"":""exact True.intro""}"
> Resource Envelope & Fine-Tuning Rules
> Submissions are evaluated in a containerized CPU-only execution environment:
> Hardware Allocation: 10 CPU cores and 62 GB RAM. GPU acceleration and network access are strictly disabled.
> Time Limit: The complete training and inference pipeline must complete within 90 minutes of wall-clock time.
> Fine-Tuning Mandate: Solutions must perform measurable parameter optimization on train.csv during the timed execution run and use the optimized model parameters for test inference. Fine-tuning adapters, training task heads on frozen backbones, or end-to-end training of compact Transformer/sequence architectures are acceptable.
> Rules and What Not To Use
> To maintain fairness and the integrity of the fine-tuning task, participants must strictly adhere to the following constraints:
> No External Assets: No external datasets, web downloads, external APIs, or non-preinstalled model checkpoints.
> No Hardware Bypasses: No GPU dependencies or workflows that exceed the 90-minute CPU execution limit.
> No Search Bypasses: Do not call Lean interactive provers or external search tools as brute-force substitutes for model generation.
> No Pure Rule Predictors: Pure lookup tables, hard-coded tactic frequency rules, or memorization heuristics used as primary predictors are prohibited.
> No Test Adaptation: No test-time gradient updates, pseudo-labeling on test rows, or hard-coded test IDs.
> Isolation: Train and infer exclusively using the supplied public training and test files.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Fine-Tune a Parliamentary Rejoinder Encoder

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77bycrahpkd8xjqdsv77s4yd8bxq36
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Given a protected sketch of the recent debate context and ten candidate speech sketches, predict which candidate is the authentic next substantive contribution. Parliamentary debate unfolds as a sequence of floor contributions interrupted by procedural chair turns, so this task models continuation ranking rather than speaker-label classification. The supplied compact discourse-pair ranker was learned from early German Bundestag terms and must be fine-tuned for later parliamentary language and speaker dynamics.
> Raw speeches, dates, names, source identifiers, session identifiers, and vocabulary are not public. Each contribution is represented by a normalized 128-bin signed text sketch, and candidate metadata is reduced to coarse relationship, role, and length codes. Candidate display order is independently shuffled for every case.
> Fine-Tuning Objective
> Start from pretrained_pair_encoder.npz and update its supplied skip, encoder, and scoring-head parameters using the labeled train.npz cases. Use validation.npz for schedule, regularization, residual-weight, and decoding selection. Use the adapted checkpoint to predict the case-local candidate ID S0 through S9 that corresponds to the observed next substantive contribution in each test case.
> The supplied checkpoint combines a trainable 263-feature linear skip with a 263-32-1 tanh residual encoder. It was pretrained on 18,000 authentic adjacency-ranking cases from Wahlperioden 1 through 15. Fine-tuning data comes from later terms, so successful adaptation must transfer the older model to changed vocabulary sketches, parties, roles, and discourse conventions. The reference solution updates all five parameter arrays and adds the normalized adapted-minus-frozen score change to a stable cosine base; it does not treat the checkpoint as a frozen feature lookup.
> A substantive contribution is any attributed speech whose role is not exactly PrÃ¤sident, PrÃ¤sidentin, VizeprÃ¤sident, or VizeprÃ¤sidentin. Intervening chair turns are skipped when defining adjacency.
> Dataset
> The source contains 1,033,723 speeches from 4,611 Bundestag plenary sessions. Wahlperioden 1 through 15 supply only the bundled pretrained checkpoint. Wahlperioden 16 through 20 provide 3,000 labeled fine-tuning cases. A speech-disjoint Wahlperiode 21 pool is partitioned by protected case ID into 800 labeled validation cases and 1,800 hidden-label test cases before either stage constructs candidate slates. No source speech is reused across selected contexts or authentic targets, no source speech crosses a stage boundary, and validation and test share no exact candidate sketch.
> The public directory contains:
> pretrained_pair_encoder.npz
> train.npz
> validation.npz
> test.npz
> dataset_summary.json
> sample_submission.csv
> pretrained_pair_encoder.npz contains:
> w0: shape (263,), float32, pretrained linear-skip weights.
> w1: shape (263, 32), float32, pretrained encoder weights.
> b1: shape (32,), float32, pretrained encoder bias.
> w2: shape (32,), float32, pretrained ranking-head weights.
> b2: shape (1,), float32, pretrained ranking-head bias.
> format_version: shape (1,), Unicode, with value bundestag-pair-encoder-v2.
> pretraining_wahlperioden: the integer values 1 through 15.
> train.npz and validation.npz contain:
> case_ids: shape (n,), Unicode strings.
> context_sketches: shape (n, 128), int16.
> candidate_sketches: shape (n, 10, 128), int16.
> context_meta: shape (n, 4), int8.
> candidate_meta: shape (n, 10, 3), int8.
> target_index: shape (n,), int8, with values 0 through 9.
> test.npz contains the same case arrays except target_index. Candidate index i corresponds to submission value Si.
> For each context-candidate pair, the supplied encoder expects 263 inputs in this order: 128 elementwise context-candidate products, 128 absolute differences, three scaled candidate metadata values, and four repeated scaled context metadata values. Sketches are divided by 32767; metadata values are divided by 7.
> The sketches use signed sublinear term-frequency features over normalized unigrams and adjacent bigrams, training-derived inverse-document-frequency weights, a private signed Hadamard rotation, L2 normalization, and int16 quantization. A context sketch combines up to three preceding substantive contributions with greater weight on the most recent contribution. Sketch coordinates are stable across public splits but do not correspond to published vocabulary positions, and the dense rotation suppresses key-invariant sparsity fingerprints.
> The four context_meta columns are anchor_role_group, anchor_length_bucket, history_count, and chair_turns_skipped_capped. The three candidate_meta columns are party_relation, role_group, and length_bucket.
> Candidate decoys come only from the same stage-local authentic-target pool, exclude the target session, and are matched on party relation, role group, length bucket, token occupancy, repetition, and other key-independent text-shape statistics when the pool permits. Candidate sketches may recur as decoys only within their own stage. Validation and test pools are constructed independently and have no shared candidate sketch. Candidate IDs and order remain case-local and have no global meaning.
> Evaluation
> The score is top-1 accuracy over the 1,800 test cases:
> score = correct predictions / 1800
> Higher is better. The score range is [0, 1]. An exact oracle scores 1. The supplied sample uses an empty prediction for every case; empty predictions are valid abstentions and score 0 for those cases, so the complete sample scores exactly 0.
> Submission
> Write ./working/submission.csv with exactly these columns in this order:
> case_id,predicted_candidate_id
> Q0000000000000000,S3
> Include each test case_id exactly once. predicted_candidate_id must be an empty string or one of S0, S1, S2, S3, S4, S5, S6, S7, S8, or S9. Empty strings abstain. Wrong columns, missing or extra rows, duplicate IDs, unknown IDs, non-string values, and leading or trailing whitespace are rejected.
> Modeling Rules
> Fine-tune the supplied checkpoint using only the public challenge files. The adapted w0, w1, b1, w2, and b2 parameters must originate from pretrained_pair_encoder.npz and be updated from the labeled fine-tuning data; replacing the checkpoint with external pretrained weights is not allowed. External corpora, source-corpus lookup, reverse identification of protected cases, private-file access, solve-time internet, downloads, and package installation are prohibited. The checkpoint and all required NumPy arrays are bundled for offline CPU execution.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Container Material Region Layout

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx733a54v1ze8dhqtdqveaksqh8byw4q
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Fine-tune a model on the released industrial camera images and their structured layout labels. For each test image, submit a compact record describing visible flexible-material regions in the frame.
> The required record contains the total number of visible regions, a coarse count bin, which 10 by 12 grid cells are covered, how many regions fall into upper/middle/lower image zones, how many regions fall into coarse size bins, and up to eight cards for the largest visible regions. Each region card contains a normalized rectangle, center grid cell, vertical zone, size bin, and rank by visible area.
> The images contain mixed material texture, low-resolution overhead views, clutter, blur, and overlapping flexible regions. A useful solution has to adapt image features from the labeled training rows and make the count, grid, zone, and card fields agree with the same image.
> Dataset
> The provided files are:
> train.csv: 1,800 labeled industrial-frame examples.
> test.csv: 600 unlabeled industrial-frame examples.
> sample_submission.csv: valid low-information submission file with the required columns.
> images/: 2,400 transformed JPEG images referenced by train.csv and test.csv.
> Columns in train.csv:
> id (string): unique row id.
> image_path (string): relative path to the JPEG image under images/.
> width (integer): image width in pixels. All rows use 512.
> height (integer): image height in pixels. All rows use 340.
> layout_packet_json (JSON string): row context, including the output grid size, zone names, and maximum number of region cards.
> answer_format_json (JSON string): required output schema, allowed cell names, valid bins, and card fields.
> answer_json (JSON string): ground-truth flexible-region layout record for training rows.
> Columns in test.csv:
> id (string): unique row id.
> image_path (string): relative path to the JPEG image under images/.
> width (integer): image width in pixels.
> height (integer): image height in pixels.
> layout_packet_json (JSON string): same context structure as in train.csv.
> answer_format_json (JSON string): required output schema and allowed values.
> layout_packet_json has this structure:
> {
> "output_grid": [10, 12],
> "visible_region": "industrial overhead container view",
> "max_region_cards": 8,
> "zone_names": ["upper", "middle", "lower"]
> }
> The answer_json object has exactly these fields:
> {
> "region_count": 2,
> "region_count_bin": "few",
> "occupied_cells": ["r03_c04", "r03_c05", "r04_c04"],
> "zone_counts": {"upper": 0, "middle": 2, "lower": 0},
> "area_bin_counts": {"tiny": 0, "small": 1, "medium": 1, "large": 0},
> "region_cards": [
> {
> "region_rank": 1,
> "center_cell": "r03_c05",
> "zone": "middle",
> "area_bin": "medium",
> "bbox": [0.36, 0.30, 0.49, 0.47]
> }
> ]
> }
> Cell names use a 10-row by 12-column grid, r00_c00 through r09_c11, with r00_c00 at the top-left of the image. occupied_cells must be sorted lexicographically and contain no duplicates.
> Allowed region_count_bin values are none, few, several, and many. Allowed zone names are upper, middle, and lower. Allowed area_bin values are tiny, small, medium, and large. region_count, zone_counts, and area_bin_counts values must be integers from 0 through 12. Each bbox is [x0, y0, x1, y1] normalized to [0, 1].
> Evaluation
> The score is the mean row score over all evaluated rows. Each row score is clipped to [0, 1].
> The occupied-cell score is set F1:
> precision = |predicted_cells intersect true_cells| / |predicted_cells|
> recall    = |predicted_cells intersect true_cells| / |true_cells|
> cell_f1   = 1 if both sets are empty
> cell_f1   = 0 if exactly one set is empty
> cell_f1   = 0 if precision + recall = 0
> cell_f1   = 2 * precision * recall / (precision + recall) otherwise
> Region count is scored by normalized absolute error:
> count_score = max(0, 1 - |predicted_region_count - true_region_count| / 12)
> Zone and area-bin count dictionaries are scored by normalized absolute error:
> dict_total = sum(predicted_counts) + sum(true_counts)
> dict_error = sum over keys |predicted_count - true_count|
> dict_score = 1 if dict_total = 0
> dict_score = max(0, 1 - dict_error / dict_total) otherwise
> Region cards are matched greedily to unused true cards. The pair score for one predicted card and one true card is:
> pair_score = 0.45 * bbox_iou^2
> + 0.20 if center_cell matches
> + 0.15 if zone matches
> + 0.15 if area_bin matches
> + 0.05 if region_rank matches
> The best unused true card is selected for each predicted card. The final card score is:
> matched_precision = sum matched pair scores / number of predicted cards
> matched_recall    = sum matched pair scores / number of true cards
> card_score        = 1 if both card lists are empty
> card_score        = 0 if exactly one card list is empty
> card_score        = 2 * matched_precision * matched_recall / (matched_precision + matched_recall) otherwise
> The row score is:
> row_score = 0.24 * occupied_cell_f1^2
> + 0.12 * count_score
> + 0.06 * region_count_bin_match
> + 0.14 * zone_count_score
> + 0.12 * area_bin_count_score
> + 0.32 * card_score
> Malformed JSON, missing fields, extra fields, invalid cell names, duplicate cells, unsorted cells, invalid bins, invalid rectangles, invalid ranks, or invalid value types receive zero for that row. Submissions with the wrong columns, wrong column order, duplicate ids, missing ids, extra ids, or the wrong number of rows are rejected.
> Submission
> Submit a CSV file with exactly these two columns in this order:
> id (string): test row id.
> answer_json (JSON string): predicted flexible-material layout record.
> Example:
> id,answer_json
> flexmat_11111111111111,"{""region_count"":2,""region_count_bin"":""few"",""occupied_cells"":[""r03_c04"",""r03_c05"",""r04_c04""],""zone_counts"":{""upper"":0,""middle"":2,""lower"":0},""area_bin_counts"":{""tiny"":0,""small"":1,""medium"":1,""large"":0},""region_cards"":[{""region_rank"":1,""center_cell"":""r03_c05"",""zone"":""middle"",""area_bin"":""medium"",""bbox"":[0.36,0.30,0.49,0.47]}]}"
> flexmat_22222222222222,"{""region_count"":0,""region_count_bin"":""none"",""occupied_cells"":[],""zone_counts"":{""upper"":0,""middle"":0,""lower"":0},""area_bin_counts"":{""tiny"":0,""small"":0,""medium"":0,""large"":0},""region_cards"":[]}"
> What Not To Use
> Do not use GPU acceleration.
> Do not use external industrial-container, flexible-material, or overhead-camera image datasets.
> Do not use pretrained recycling, street-scene, or vision-language models.
> Do not use hosted vision APIs or manually maintained answer tables.
> Do not install packages at runtime, include additional model checkpoints, use non-public or gated assets, or load remote code such as torch.hub or trust_remote_code.
> Do not hard-code predictions for specific test ids.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Multilingual Span Gap Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx747xke6yzsyqq19yrvhmetgh88e7k2
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background & Overview
> The objective of this challenge is to train a sequence model that can perform trilingual structured gap restoration. Specifically, you must fine-tune a model to look at an original English source sentence (source_en) and perfectly reconstruct missing one-to-three-token spans (holes) in its corresponding French and German translations (fr_skeleton, de_skeleton). In addition to filling the gaps and restoring the complete texts, the model must also identify "protected tokens" shared across the languages.
> This challenge focuses strictly on structured gap restoration via fine-tuning on the provided subset of ~80,000 training and ~12,000 test examples. It is not a general machine-translation benchmark, nor is it a from-scratch task.
> Dataset
> The dataset is derived from official EU translations and is provided in CSV format. To prevent data leakage, the data is split based on the source document identity, ensuring that sentences from the same EU document family do not cross between the train and test sets.
> File Structure
> +-----------------------+----------------------------------------------------------------------------------+
> | File                  | Description                                                                      |
> +-----------------------+----------------------------------------------------------------------------------+
> | train.csv             | The training set (~80,000 rows). Contains all features and ground-truth targets. |
> | test.csv              | The test set (~12,000 rows). Contains only the inputs. Used for inference.       |
> | sample_submission.csv | A valid submission template with the correct IDs and default schema.             |
> +-----------------------+----------------------------------------------------------------------------------+
> Column Descriptions
> id (string): An opaque, unique identifier for the translation unit.
> source_en (string): The raw, unmasked English source sentence.
> fr_skeleton (string): The French translation with an independently chosen one-to-three-token span replaced by the placeholder <fr0>.
> de_skeleton (string): The German translation with an independently chosen one-to-three-token span replaced by the placeholder <de0>.
> hole_ids_json (string): A serialized JSON array listing the gap identifiers present in the row (e.g., ["fr0", "de0"]).
> target_json (string, train only): A serialized JSON object containing the ground-truth answers. It includes the exact gap text, full restored texts, and a list of protected tokens.
> prediction (string, submission only): Your model's serialized JSON string output, perfectly matching the schema of target_json.
> Execution Envelope & Rules
> Your run must fine-tune a real multilingual model on the supplied training data. Compact seq2seq models, adapters, and multilingual denoisers are suitable.
> Compute Limits: 10 CPU cores and 62 GB RAM.
> Time Limit: 90 minutes maximum for the complete solution (training + inference).
> Environment Constraints: No GPU or accelerator dependency. No internet access is permitted during execution. You may use only the supplied public files and packages already available in the execution image.
> Fine-Tuning Requirement: The submitted solution must perform measurable parameter optimization on the public training split during the timed run and use the resulting trained parameters for test inference. Freezing a compact backbone and fine-tuning adapters or task heads is acceptable.
> Reproducibility: Set all random seeds, cap worker/thread counts at 10, document any sampling, and write exactly one submission.csv. The row order may differ, but IDs, row count, and columns must exactly match the sample submission.
> Evaluation Metrics
> Each prediction is evaluated independently. The final score is the mean of all row scores, bounded to [0, 1]. The row score consists of multiple components based on Token F1, Exact Matches, completeness, and protected tokens.
> Protected Tokens
> Protected tokens are specific entitiesâ€”such as numbers or uppercase acronyms (length 2-16 characters)â€”that are shared by at least two language views (e.g., English and French, or French and German). Exact source spelling must be preserved. The model is evaluated on its ability to extract these shared tokens correctly.
> Token F1 Score (
> ð¹
> 1
> F1)
> For a predicted multiset of tokens
> ð‘ƒ
> P and a gold multiset
> ðº
> G:
> ð¹
> 1
> =
> 2
> Ã—
> âˆ£
> ð‘ƒ
> âˆ©
> ðº
> âˆ£
> âˆ£
> ð‘ƒ
> âˆ£
> +
> âˆ£
> ðº
> âˆ£
> F1=
> âˆ£Pâˆ£+âˆ£Gâˆ£
> 2Ã—âˆ£Pâˆ©Gâˆ£
> â€‹
> Gap Score (
> ð‘†
> ð‘”
> ð‘Ž
> ð‘
> S
> gap
> â€‹
> )
> Evaluated independently for French and German. It takes the union of predicted and gold hole IDs (
> ð‘
> N total IDs). For each hole ID, it checks for an exact match and computes the token F1.
> ð‘†
> ð‘”
> ð‘Ž
> ð‘
> =
> 1
> ð‘
> âˆ‘
> ð‘–
> (
> 0.65
> â‹…
> Exact
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> +
> 0.35
> â‹…
> ð¹
> 1
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> )
> S
> gap
> â€‹
> =
> N
> 1
> â€‹
> âˆ‘
> i
> â€‹
> (0.65â‹…Exact(P
> i
> â€‹
> ,G
> i
> â€‹
> )+0.35â‹…F1(P
> i
> â€‹
> ,G
> i
> â€‹
> ))
> Text Score (
> ð‘†
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> S
> text
> â€‹
> )
> Evaluated independently for the full restored French and German texts.
> ð‘†
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> =
> 0.55
> â‹…
> Exact
> (
> ð‘ƒ
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> ,
> ðº
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> )
> +
> 0.45
> â‹…
> ð¹
> 1
> (
> ð‘ƒ
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> ,
> ðº
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> )
> S
> text
> â€‹
> =0.55â‹…Exact(P
> text
> â€‹
> ,G
> text
> â€‹
> )+0.45â‹…F1(P
> text
> â€‹
> ,G
> text
> â€‹
> )
> Final Row Score
> The aggregated score combines the French (FR) and German (DE) metrics, the shared protected tokens, and a completeness bonus. (where
> Complete
> Complete is 1 if the predicted gap IDs exactly match the gold gap IDs for both languages, and 0 otherwise).
> RowÂ Score
> =
> 0.28
> â‹…
> ð‘†
> ð‘”
> ð‘Ž
> ð‘
> (
> FR
> )
> +
> 0.28
> â‹…
> ð‘†
> ð‘”
> ð‘Ž
> ð‘
> (
> DE
> )
> +
> 0.18
> â‹…
> ð‘†
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> (
> FR
> )
> +
> 0.18
> â‹…
> ð‘†
> ð‘¡
> ð‘’
> ð‘¥
> ð‘¡
> (
> DE
> )
> +
> 0.05
> â‹…
> ð¹
> 1
> ð‘
> ð‘Ÿ
> ð‘œ
> ð‘¡
> ð‘’
> ð‘
> ð‘¡
> ð‘’
> ð‘‘
> +
> 0.03
> â‹…
> Complete
> RowÂ Score=0.28â‹…S
> gap
> â€‹
> (FR)+0.28â‹…S
> gap
> â€‹
> (DE)+0.18â‹…S
> text
> â€‹
> (FR)+0.18â‹…S
> text
> â€‹
> (DE)+0.05â‹…F1
> protected
> â€‹
> +0.03â‹…Complete
> Sample Submission Format
> Submit a UTF-8 CSV with exactly two columns: id and prediction.
> The prediction column must contain a properly escaped, serialized JSON object adhering to the following structure:
> JSON
> {
> "de_gaps": [{"hole_id": "de0", "text": "einem neuen"}],
> "de_text": "Mit einem neuen Rahmenwerk...",
> "fr_gaps": [{"hole_id": "fr0", "text": "un nouveau"}],
> "fr_text": "Avec un nouveau cadre...",
> "protected_tokens": ["2014", "COM(2025)"]
> }
> Example CSV output:
> Code snippet
> id,prediction
> tm_0000001_a1b2c3d4,"{""de_gaps"": [{""hole_id"": ""de0"", ""text"": ""einem neuen""}], ""de_text"": ""Mit einem neuen Rahmenwerk..."", ""fr_gaps"": [{""hole_id"": ""fr0"", ""text"": ""un nouveau""}], ""fr_text"": ""Avec un nouveau cadre..."", ""protected_tokens"": [""2014"", ""COM(2025)""]}"
> What Not To Use
> External datasets, checkpoints not already permitted by the platform, APIs, or web downloads.
> GPU-only architectures or workflows likely to exceed 90 minutes on the stated CPU.
> Private/test labels, hidden answer paths, or platform implementation details.
> Test-time gradient updates, pseudo-label fitting on test rows, or hard-coded test IDs.
> A task-family substitution (such as classification when the problem asks for structured generation/detection).
> Phrase-table-only systems, pure lookup tables, hand-written rules as the complete predictor, answer memorization, or labels obtained from an external model/service.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Counterfactual Boundary Field Inversion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dn09khrk1aqzaj6f4r1z2598c2966
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Counterfactual Boundary Field Inversion is a hard CPU NLP challenge over Ukrainian text.
> Each test sample contains eight partially observed versions of the same passage.
> Your job is simple to state:
> Generate one hidden complete endpoint text: north_pole.
> Generate the opposite hidden complete endpoint text: south_pole.
> Predict whether each public view V01 through V08 is depth 3 or depth 4 from north_pole.
> The two endpoint texts are never present in the input.
> Each public view also contains exactly two literal <MASK> tokens, but the masked spans are not prediction targets. The <MASK> symbols only indicate that part of that particular observation has been withheld.
> The actual prediction target is the pair of complete hidden boundary texts and the position of every public observation between them.
> Behind each sample are seven independent local text factors. Each factor has two possible realizations. Together they define:
> 2^7 = 128
> possible complete text states.
> Only eight internal states are observed.
> All eight are deliberately chosen from the middle of this hidden state space, so every clean public state is exactly three or four factor changes away from north_pole.
> The benchmark also inserts one small recurring distractor variation into four public views. That variation is absent from both hidden endpoints and is not one of the seven scored factors.
> A strong system must therefore determine:
> Which recurring text differences define the hidden boundary pair.
> Which recurring difference is only a distractor.
> What text is hidden behind observations that omit two factor realizations.
> Which orientation of each factor belongs to each endpoint.
> Which public states are depth 3 and which are depth 4.
> This is an inverse latent-state problem over text, not a masked-span completion benchmark.
> Data Context
> The benchmark is constructed from naturally written Ukrainian prose that was professionally reviewed.
> The underlying writing includes essays, translation-derived writing, donated prose, informal writing, formal writing, and general-purpose text.
> The writers include both native and non-native Ukrainian speakers.
> Professional review provides naturally occurring local alternatives involving phenomena such as:
> Case.
> Gender.
> Number.
> Agreement.
> Verb morphology.
> Preposition choice.
> Lexical choice.
> Spelling.
> Punctuation.
> Collocation.
> Repetition.
> Phrase realization.
> Fluency.
> Style.
> The public benchmark does not expose ordinary source-to-correction pairs.
> Instead, several naturally occurring local alternatives are recomposed into a counterfactual state field.
> The resulting prediction problem asks whether a model can infer two missing boundary conditions from sparse and partially censored observations of that field.
> Plain-Language Example
> Imagine one passage contains seven independent places where two realizations are possible.
> For explanation only, call them:
> A
> B
> C
> D
> E
> F
> G
> One complete version might use:
> A1 B1 C1 D1 E1 F1 G1
> The opposite complete version might use:
> A0 B0 C0 D0 E0 F0 G0
> Those two complete texts are the hidden endpoints.
> A public view might correspond to:
> A1 B1 C1 D0 E0 F0 G1
> That clean state is three changes away from the all-1 endpoint.
> Another public view might correspond to:
> A0 B0 C1 D1 E1 F0 G0
> That state is four changes away.
> The participant never sees these factor labels or bit patterns.
> The participant sees only text.
> A visible view may additionally hide two complete local realizations:
> A1   C1 D0 E0   G1
> The correct output is not the content of those two masks.
> The model must infer the two complete all-1 and all-0 endpoint texts using evidence distributed across all eight observations.
> Hidden Counterfactual Field
> Each sample contains exactly seven binary text factors.
> Conceptually:
> f1
> f2
> f3
> f4
> f5
> f6
> f7
> Each factor can take one of two realizations.
> A complete state can therefore be represented conceptually by seven bits.
> There are:
> 128
> possible complete states.
> The two hidden boundaries are:
> 1111111
> and:
> 0000000
> The public files never contain these bit coordinates.
> They exist only to define the benchmark geometry.
> Hidden Boundary Pair
> The all-one state is north_pole.
> The all-zero state is south_pole.
> Both complete strings are withheld from test input.
> Under the official token-level comparison procedure, the two gold endpoints differ through exactly seven separated non-equal blocks.
> Those seven local endpoint divergences define the seven hidden factors.
> The factors are sample-local.
> There is no global factor label inventory.
> For example, a case change may behave like one factor in one sample and a lexical replacement may occupy the analogous position in another sample.
> The benchmark therefore cannot be solved as seven fixed global classifiers.
> Public State Probes
> Every sample releases eight views:
> V01
> V02
> V03
> V04
> V05
> V06
> V07
> V08
> These are best understood as state probes.
> Each probe samples one internal state of the hidden field.
> The clean state behind each probe is exactly depth:
> 3
> or:
> 4
> from north_pole.
> No public state is depth 0, 1, 2, 5, 6, or 7.
> Therefore no input view is a near-copy of either answer.
> Balanced Factor Incidence
> Across the eight clean public states, every hidden factor is balanced.
> For each factor:
> Four states use its north realization.
> Four states use its south realization.
> This removes frequency as an orientation signal.
> A realization is not guaranteed to be north because it is:
> More frequent.
> More grammatical-looking in isolation.
> Longer.
> Shorter.
> Earlier.
> Later.
> Attached to a particular view ID.
> Orientation must be learned from the linguistic evidence and the training examples.
> Partial Observation
> Every public view contains exactly two literal <MASK> tokens.
> Each <MASK> replaces one complete realization of one hidden factor.
> The two omitted factors differ within a view.
> Different views omit different factors.
> Across the complete eight-view bundle, both realizations of every scored factor remain visible somewhere.
> The masks therefore create partial observation, not a separate fill-in-the-blank target.
> Neither submitted endpoint may contain <MASK>.
> Balanced Confounder
> Every sample also contains one small recurring surface change that is not one of the seven endpoint-defining factors.
> This confounder appears in exactly four public views.
> It is absent from both hidden endpoints.
> It does not affect depth.
> Its four-view activation pattern is selected so that it does not duplicate the activation pattern of any one true factor.
> This means the participant observes eight recurring binary-looking variation patterns:
> Seven define the endpoint field.
> One is a balanced confounder.
> The model must identify which seven are structurally relevant.
> Prediction Targets
> For every test sample, submit exactly three predictions.
> north_pole
> Type:
> string
> The complete hidden all-north endpoint.
> It must not contain <MASK>.
> south_pole
> Type:
> string
> The complete hidden all-south endpoint.
> It must not contain <MASK>.
> view_depths
> Type:
> JSON object encoded inside one CSV cell.
> It must contain exactly:
> V01
> V02
> V03
> V04
> V05
> V06
> V07
> V08
> Every value must be integer:
> 3
> or:
> 4
> Example:
> {"V01":3,"V02":4,"V03":3,"V04":4,"V05":4,"V06":3,"V07":3,"V08":4}
> Depth is computed from the seven hidden endpoint factors only.
> The two <MASK> omissions do not alter depth.
> The balanced confounder does not alter depth.
> What <MASK> Does and Does Not Mean
> The literal <MASK> token is easy to misinterpret, so the distinction is explicit.
> <MASK> means:
> this observation does not reveal one factor realization at this location.
> It does not mean:
> predict this masked span as the benchmark answer.
> There is no masked-token accuracy metric.
> There is no masked-span exact-match target.
> There is no requirement to submit individual mask fillings.
> A participant could perfectly infer every locally missing span and still fail the challenge if it does not recover the two global endpoint texts and the depth geometry.
> Conversely, a system can recover the hidden endpoints without ever emitting a separate prediction for a mask.
> Why This Is a Counterfactual Boundary Problem
> The two targets are counterfactual combinations.
> The north endpoint combines all seven north-oriented realizations.
> The south endpoint combines all seven opposite realizations.
> Neither combination is observed.
> Each public state contains only a mixed subset of endpoint choices.
> The task therefore requires synthesizing two missing global boundary conditions from several internal observations.
> This is different from selecting, restoring, or correcting one observed string.
> Construction Pipeline
> Each benchmark sample is constructed through the following high-level procedure.
> Start from one naturally written Ukrainian passage with professional linguistic adjudication.
> Identify seven separated local divergence loci whose two realizations can coexist as independent choices.
> Treat those seven divergence loci as sample-local binary factors.
> Compose the factors into a 128-state counterfactual field.
> Define the two all-aligned states as the hidden boundary pair.
> Select eight internal states only from depth 3 and depth 4.
> Require every scored factor to occur four times in each orientation across the eight clean states.
> Remove two factor realizations from each selected state and replace them with <MASK>.
> Preserve visible evidence for both orientations of every scored factor somewhere in the full eight-view bundle.
> Introduce one small recurring balanced confounder into exactly four views.
> Ensure the confounder activation pattern does not duplicate any scored factor pattern.
> Randomize V01 through V08 locally.
> Keep protected writer groups entirely on one side of the official train/test split.
> The hidden coordinates, factor identities, confounder map, raw editorial alignment, and split construction keys are not public prediction features.
> Representative Structural Example
> The following example is schematic and demonstrates the geometry rather than real benchmark text.
> Assume the seven hidden factors control these local spans:
> Shared text:
> "Автор [A] документ [B] учора, [C] команда [D] результат [E] після [F] перевірки [G]."
> Suppose the north endpoint uses:
> A = "оновив"
> B = "уважно"
> C = "а"
> D = "підтвердила"
> E = "остаточно"
> F = "повторної"
> G = "."
> Suppose the south endpoint uses:
> A = "оновлював"
> B = "ретельно"
> C = "але"
> D = "підтверджувала"
> E = "частково"
> F = "першої"
> G = "!"
> The benchmark does not publish A through G.
> One hidden clean state could select:
> A north
> B north
> C south
> D south
> E north
> F south
> G north
> Its seven-bit representation would be:
> 1100101
> Its north-depth is:
> 3
> A public observation of that state might hide B and F.
> The participant would see a text containing two <MASK> tokens instead of those complete realizations.
> Another state exposes different loci.
> Across eight views, the evidence overlaps sufficiently to make the endpoint field inferable, but no single view exposes it completely.
> One additional recurring change may appear in four views even though it is absent from both endpoints.
> That extra change is the confounder.
> This example illustrates why local mask restoration is not equivalent to solving the benchmark.
> Research Distinction
> The benchmark is deliberately positioned away from three neighboring task families.
> Masked Language Modeling and Lacuna Restoration
> Masked language models predict hidden tokens or characters from surrounding context.
> Here, the <MASK> locations are observation censoring only.
> They have no direct evaluation target.
> The primary outputs are two complete counterfactual boundary texts that never occur among the eight observations.
> The model must also predict the radial depth of every public state.
> Instruction-Based Ukrainian Text Editing
> Instruction-following editing benchmarks map an input text and an editing instruction to an edited output, such as grammatical correction, simplification, coherence editing, or paraphrasing.
> This benchmark contains no edit instruction and no privileged input text.
> Eight unordered mixed states jointly define one sample.
> The targets are two unobserved global combinations of seven local choices.
> Revision-History Modeling
> Revision datasets can contain multiple versions of a document or aligned edits over time.
> The eight views here are not chronological versions.
> They form a balanced subset of a combinatorial field.
> No temporal order exists.
> V06 is not "later" than V05.
> The prediction target is not the next revision.
> It is the pair of missing boundary states plus the radial class of all observed probes.
> Closest-Work Contrast
> A nearby masked-language-modeling direction is DualEmbLM, which uses character-level and word-level representations for masked prediction and lacuna restoration in historical Slavic text.
> Counterfactual Boundary Field Inversion differs in the supervised object:
> DualEmbLM predicts missing local content.
> This benchmark never scores local mask filling.
> DualEmbLM operates on one masked context at a time.
> This benchmark requires joint reasoning over eight coupled state probes.
> DualEmbLM has no sample-local seven-factor combinatorial field.
> DualEmbLM has no simultaneous two-boundary generation target.
> DualEmbLM has no depth-3/depth-4 state geometry.
> DualEmbLM has no balanced recurrent confounder that must be excluded from the boundary field.
> A nearby Ukrainian editing direction is Spivavtor, which instruction-tunes models for Ukrainian correction, simplification, coherence, and paraphrasing.
> Counterfactual Boundary Field Inversion differs in both input and output geometry:
> There is no editing instruction.
> There is no single privileged source.
> There is no direct source-to-edited-target mapping.
> Two absent boundary texts must be generated simultaneously.
> The eight public states are coupled by a hidden binary incidence design.
> Two factor realizations are censored in every view.
> One recurrent variation is intentionally non-causal for the target field.
> Radial state depth is explicitly predicted and scored.
> The linguistic source material supplies natural alternatives, but the released benchmark objective is a newly constructed inverse state-identification problem.
> Novelty-Critical Properties
> The defining contribution is not any one component in isolation.
> The benchmark requires one model to solve all of the following within the same prediction unit:
> Infer a sample-local seven-factor binary text field.
> Recover two globally unobserved counterfactual boundary strings.
> Aggregate eight unordered internal observations.
> Reason when every observation hides two complete factor realizations.
> Distinguish seven causal endpoint factors from one balanced recurrent confounder.
> Predict the radial depth of every observation.
> Produce a boundary pair whose token-level divergence structure agrees with the hidden seven-factor field.
> Produce a boundary pair whose expanded state family explains the visible portions of the public probes.
> Changing one local string into another is not the benchmark objective.
> The scored object is the hidden field itself, represented through its two boundary conditions and its observed-state geometry.
> Why This Is Not Ordinary Grammatical Error Correction
> Ordinary grammatical error correction is approximately:
> one source text
> →
> one corrected text
> This challenge is:
> eight partially observed mixed states
> →
> two hidden counterfactual boundary texts + eight radial labels
> Neither endpoint must be interpreted as simply "the corrected version of V01."
> Every public state contains a mixture of opposite endpoint realizations.
> Why This Is Not Mask Filling
> There are sixteen visible <MASK> tokens per sample across eight views.
> The submission contains zero mask-fill columns.
> Mask completion is therefore only a possible intermediate modeling strategy.
> It is not the benchmark output.
> Why This Is Not Candidate Ranking
> Neither hidden endpoint appears in the candidate set because there is no candidate set.
> Both strings are generated.
> Why This Is Not State Classification Alone
> The model does predict eight depth labels, but those labels are only part of the task.
> The principal generative outputs are two complete texts.
> The hidden factors themselves do not have global class names.
> Challenge Type
> This is a Fine-Tuning challenge.
> Public pretrained language-model weights are allowed.
> Pretrained sequence-to-sequence models are explicitly permitted and are the intended model family.
> Eligible approaches include:
> Compact multilingual encoder-decoder transformers.
> Ukrainian-capable pretrained seq2seq models.
> Byte-level text-to-text models.
> Character-aware pretrained models.
> Pretrained encoders with learned generation heads.
> Adapter tuning.
> Low-rank adaptation.
> Multi-view neural encoders.
> Set encoders.
> Cross-view attention.
> Neural latent-factor models.
> Joint endpoint-generation and depth models.
> CPU-friendly neural ensembles.
> Training a foundation model from scratch is not required.
> Machine-Learning Requirement
> Predictions must be produced primarily by learned model parameters.
> Purely rule-based or nearest-neighbor systems are not eligible as the primary predictor.
> Disallowed primary approaches include:
> Handwritten grammar rules.
> Regular-expression rewrite engines.
> Fixed substitution dictionaries.
> Manually encoded morphological paradigms.
> TF-IDF prediction.
> Bag-of-words retrieval.
> Character n-gram nearest-neighbor retrieval.
> Exact-string nearest-neighbor prediction.
> Hard-coded endpoint-selection rules.
> Hard-coded depth patterns.
> Manual test annotation.
> Hard-coded test outputs.
> Deterministic infrastructure around a learned model is allowed.
> Examples include:
> Tokenization.
> JSON parsing.
> Beam search.
> Greedy decoding.
> Tensor masking.
> Deterministic normalization.
> Learned reranking.
> Compute
> The execution environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> Participants should choose pretrained models practical for CPU fine-tuning and inference.
> Useful strategies include:
> Compact pretrained backbones.
> Frozen or partially frozen encoders.
> Parameter-efficient fine-tuning.
> Cached tokenization.
> Cached view encodings.
> Shared encoders across all eight views.
> Small cross-view attention modules.
> Permutation-invariant aggregation.
> Greedy decoding.
> Small beam sizes.
> Distilled multilingual models.
> Byte-aware or character-aware representations.
> Remote inference APIs are not permitted.
> Released Dataset
> The public package contains:
> train.jsonl
> test.jsonl
> sample_submission.csv
> There is no official validation file.
> The labeled train.jsonl can be split locally for validation.
> The reference grader can score any locally held-out subset using the corresponding labels.
> train.jsonl
> Each line contains one JSON object.
> Every training object contains:
> sample_id
> views
> north_pole_target
> south_pole_target
> view_depths_target
> sample_id
> Type:
> string
> Unique row identifier used for submission alignment.
> Do not use sample_id as a predictive feature.
> views
> Type:
> list of eight objects
> Every object contains:
> view_id
> text
> The view IDs are:
> V01
> V02
> V03
> V04
> V05
> V06
> V07
> V08
> view_id
> Type:
> string
> Sample-local state-probe identifier.
> It has no meaning across samples.
> text
> Type:
> string
> One partially observed internal state.
> Every view contains exactly two literal <MASK> tokens.
> Some views additionally contain the sample's balanced confounder realization.
> north_pole_target
> Training only.
> Type:
> string
> The complete hidden north boundary.
> south_pole_target
> Training only.
> Type:
> string
> The complete hidden south boundary.
> view_depths_target
> Training only.
> Type:
> object
> Maps V01 through V08 to integer depth:
> 3
> or:
> 4
> test.jsonl
> Contains:
> sample_id
> views
> The target fields are omitted.
> The test data does not expose:
> Either boundary text.
> Hidden seven-bit coordinates.
> Which factors are censored in each view.
> Factor identities.
> Confounder location.
> Confounder activation pattern.
> Raw editorial identities.
> Protected source groups.
> Construction metadata.
> Split keys.
> Public Structural Guarantees
> Every released sample satisfies all of the following.
> Exactly seven scored binary factors exist.
> Exactly 128 clean combinations are defined.
> Exactly eight public state probes are released.
> Both boundary texts are hidden.
> Every clean public state has north-depth 3 or 4.
> Every scored factor appears in each orientation exactly four times across the eight clean states.
> The hidden boundaries differ through exactly seven token-level SequenceMatcher change blocks with autojunk=False.
> Every public view contains exactly two <MASK> tokens.
> Each <MASK> replaces one complete scored factor realization.
> Both realizations of every scored factor remain visible somewhere in the complete eight-view bundle.
> Exactly four public views contain one small recurring confounder.
> The confounder is absent from both boundaries.
> The confounder does not affect depth.
> View IDs do not encode geometry.
> Text Normalization
> The evaluator applies:
> Unicode NFC normalization.
> Replace every contiguous whitespace run with one ASCII space.
> Remove leading and trailing whitespace.
> The evaluator does not:
> Lowercase.
> Transliterate.
> Stem.
> Lemmatize.
> Remove punctuation.
> Normalize Ukrainian morphology.
> Submission Format
> The submission contains exactly four columns:
> sample_id
> north_pole
> south_pole
> view_depths
> There must be exactly one row for every test sample.
> Use sample_submission.csv exactly.
> Conceptual example:
> sample_id,north_pole,south_pole,view_depths
> CBFI_example,"predicted north boundary","predicted south boundary","{""V01"":3,""V02"":4,""V03"":3,""V04"":4,""V05"":4,""V06"":3,""V07"":3,""V08"":4}"
> The endpoint predictions must not contain <MASK>.
> Invalid Predictions
> A sample receives zero component credit when:
> north_pole is blank.
> south_pole is blank.
> view_depths cannot be parsed as JSON.
> view_depths is not an object.
> A required view ID is missing.
> An extra view ID is present.
> A depth is not an integer.
> A depth is not 3 or 4.
> The complete submission must contain:
> Every expected sample_id.
> No extra sample IDs.
> No duplicate sample IDs.
> Exactly the four published columns in the published order.
> Malformed overall submission structure receives the minimum score.
> Evaluation
> Submissions are evaluated with the Counterfactual Boundary Field Score.
> Scores range from:
> 0.01
> to:
> 100
> Higher is better.
> The metric measures four ideas:
> How accurately the two hidden boundary texts are generated.
> Whether their seven local divergences are recovered.
> Whether the depth-3/depth-4 geometry of the eight public probes is correct.
> Whether the predicted boundary pair can explain the visible portions of the eight public observations.
> These ideas are represented by eight published components:
> North Boundary Fidelity.
> South Boundary Fidelity.
> Boundary Exactness.
> Absolute Depth Accuracy.
> Relative Depth Geometry.
> Factor Cardinality.
> Boundary Divergence Recovery.
> Projection Consistency.
> There are no hidden metric components.
> A perfect submission receives exactly 100.
> Boundary Text Fidelity
> Boundary fidelity uses character-level longest-common-subsequence F1.
> For normalized strings X and Y, let:
> L
> be their Unicode-character longest common subsequence length.
> If both strings are empty:
> CharLCSF1 = 1
> If exactly one is empty:
> CharLCSF1 = 0
> Otherwise:
> CharLCSF1(X,Y) = 2 × L / (len(X) + len(Y))
> For every sample:
> N_sample = CharLCSF1(predicted north_pole, gold north_pole)
> S_sample = CharLCSF1(predicted south_pole, gold south_pole)
> Dataset-level:
> N = mean of N_sample
> S = mean of S_sample
> Boundary Exactness
> For each sample:
> north_exact = 1
> when normalized predicted north_pole exactly equals the normalized gold north boundary.
> Otherwise:
> north_exact = 0
> The south boundary is scored identically.
> Then:
> X_sample = (north_exact + south_exact) / 2
> Dataset-level:
> X = mean of X_sample
> Absolute Depth Accuracy
> Compare all eight submitted depths with the hidden gold depths.
> For one sample:
> D_sample = exact depth matches / 8
> Dataset-level:
> D = mean of D_sample
> Relative Depth Geometry
> For every unordered pair of public views, compare their submitted depth relationship with the gold relationship.
> The relation is:
> First view closer to north.
> Equal depth.
> First view farther from north.
> There are:
> 8 choose 2 = 28
> pairs.
> For one sample:
> R_sample = correct pair relations / 28
> Dataset-level:
> R = mean of R_sample
> Official Boundary Comparison
> The structural text metrics normalize both boundary strings and split them on ASCII spaces.
> The evaluator compares:
> south_pole
> to:
> north_pole
> using behavior equivalent to:
> difflib.SequenceMatcher
> with:
> autojunk=False
> Every non-equal opcode is one predicted boundary-divergence block.
> Gold boundary pairs always contain exactly seven such blocks.
> Factor Cardinality
> Let:
> K
> be the number of predicted non-equal boundary blocks.
> Then:
> A_sample = max(0, 1 - |K - 7| / 7)
> Dataset-level:
> A = mean of A_sample
> Boundary Divergence Recovery
> Each non-equal boundary block is represented by:
> (south token substring, north token substring)
> Predicted blocks form a multiset:
> P
> Gold blocks form a multiset:
> G
> Multiset overlap is the total shared occurrence count.
> Then:
> EditPrecision = overlap / |P|
> EditRecall = overlap / |G|
> BoundaryDivergenceF1 = 2 × EditPrecision × EditRecall / (EditPrecision + EditRecall)
> when the denominator is non-zero.
> If both multisets are empty:
> BoundaryDivergenceF1 = 1
> If only one is empty:
> BoundaryDivergenceF1 = 0
> Dataset-level:
> E = mean BoundaryDivergenceF1
> Projection Consistency
> Projection Consistency checks whether the predicted boundary pair can generate internal states compatible with the visible public probes.
> Let:
> K
> be the number of predicted boundary-divergence blocks.
> If:
> K <= 0
> or:
> K > 10
> Projection Consistency for that sample is zero.
> Otherwise:
> Enumerate every binary combination of the K predicted divergence blocks.
> Each combination creates one predicted complete internal state.
> Its predicted north-depth equals the number of blocks using the south realization.
> This produces at most:
> 2^10 = 1024
> predicted states.
> For each public view:
> Remove the two literal <MASK> tokens.
> Keep the remaining visible tokens.
> Consider only predicted states at the submitted depth for that view.
> Compute token-level LCS recall between the visible public tokens and each candidate state.
> Keep the best recall.
> Convert it to:
> ProjectionCandidate = min(1, VisibleRecall / 0.96)
> The 0.96 saturation point prevents the intentionally small balanced confounder from dominating this structural check.
> For one sample:
> C_sample = mean of the eight view scores
> Dataset-level:
> C = mean of C_sample
> Final Score
> Define boundary text similarity:
> BoundarySimilarity = sqrt(N × S)
> Combine text similarity with exact divergence recovery:
> BoundaryCore = sqrt(BoundarySimilarity × E)
> Define structural geometry:
> Geometry = (D × R × A × C)^(1/4)
> Define exactness:
> ExactnessFactor = 0.15 + 0.85 × X
> The final score is:
> 100 × BoundaryCore^1.60 × (0.20 + 0.80 × Geometry) × ExactnessFactor
> The result is clipped to:
> [0.01,100]
> For a perfect submission:
> N = 1
> S = 1
> X = 1
> D = 1
> R = 1
> A = 1
> E = 1
> C = 1
> Therefore:
> BoundaryCore = 1
> Geometry = 1
> ExactnessFactor = 1
> Final Score = 100
> Metric Interpretation
> The metric deliberately prevents broad textual similarity from dominating the leaderboard.
> A high-scoring system must:
> Generate both hidden boundaries accurately.
> Recover the correct seven local boundary divergences.
> Predict the depth of the public probes.
> Produce endpoints whose implied internal states explain the visible observations.
> A fluent but structurally unrelated endpoint pair cannot receive a high score.
> A copied public view cannot receive a high score.
> A system that only fills the <MASK> positions is not directly rewarded unless that intermediate reasoning helps it recover the hidden boundary field.
> Reproducing the Metric
> For every validation sample:
> Parse the two predicted boundary strings.
> Parse all eight submitted depths.
> Apply public normalization.
> Compute north and south character LCS F1.
> Compute exact equality for each boundary.
> Compute absolute depth accuracy.
> Compute all 28 relative-depth relationships.
> Tokenize the predicted south and north boundaries.
> Run SequenceMatcher with autojunk=False.
> Count non-equal blocks.
> Convert predicted and gold divergence blocks into token-payload multisets.
> Compute Boundary Divergence Recovery F1.
> Enumerate predicted internal states when K is between 1 and 10.
> Record their predicted north-depth.
> Remove <MASK> from each public view.
> Compare each view with candidate predicted states at its submitted depth.
> Compute Projection Consistency.
> Average all dataset-level components.
> Compute BoundaryCore.
> Compute Geometry.
> Compute ExactnessFactor.
> Apply the final formula.
> Clip to [0.01,100].
> The released grader.py is the reference implementation.
> Reference Implementation and Verifiability
> The challenge package includes a reference grader.py.
> It can be used with a locally held-out subset of train.jsonl to reproduce the full score.
> The published training targets also allow participants or reviewers to independently verify structural guarantees on released examples.
> For any training row, a reviewer can check that:
> Both endpoint strings are present as targets.
> Endpoint comparison yields seven non-equal token blocks.
> Every depth target is 3 or 4.
> Every public view contains exactly two <MASK> tokens.
> The view IDs are exactly V01 through V08.
> The complete hidden construction coordinates are intentionally not published because they would directly reveal the latent answer structure.
> The public guarantees are defined by the construction code and reflected in the released examples and grader behavior.
> Intended Modeling Approaches
> A useful neural system should process all eight views jointly.
> Possible architectures include:
> Shared pretrained seq2seq encoders.
> Set transformers.
> Cross-view attention.
> Pairwise difference encoders.
> Mask-aware latent representations.
> Learned binary-factor bottlenecks.
> Neural confounder suppression.
> Joint north/south generation.
> Depth classification heads.
> Ordinal depth prediction.
> Contrastive cross-view training.
> Copy-aware decoders.
> Byte-level generation.
> Practical CPU Baseline
> A practical eligible baseline can:
> Serialize V01 through V08 using explicit view markers.
> Fine-tune a compact multilingual seq2seq model to generate north_pole.
> Fine-tune the same backbone under another task prefix to generate south_pole.
> Attach a small neural depth classifier.
> Train generation and depth prediction jointly.
> Randomize public view order during training.
> Generate locally on CPU.
> Write predictions using sample_submission.csv.
> A stronger model can explicitly compare views and learn to distinguish endpoint-defining recurrence from balanced non-endpoint recurrence.
> Allowed Resources
> Participants may use:
> Released challenge files.
> Public pretrained model weights.
> Public pretrained tokenizers.
> Standard deep-learning frameworks.
> Standard numerical libraries.
> Public architecture implementations.
> Parameter-efficient fine-tuning libraries.
> CPU optimization libraries.
> Local validation splits derived from released training data.
> Neural auxiliary targets derived from released training labels.
> Disallowed Resources
> Participants may not use:
> Hidden evaluation targets.
> Private evaluator files.
> Manual annotation of test examples.
> Remote LLM APIs.
> Remote translation APIs.
> Remote grammar-correction services.
> Search engines during prediction.
> External answer retrieval.
> Benchmark-specific leaked outputs.
> Handwritten Ukrainian grammar systems as the primary predictor.
> Rule-based morphological generators as the primary predictor.
> Fixed replacement dictionaries.
> Regular-expression prediction systems.
> TF-IDF prediction.
> Bag-of-words nearest-neighbor prediction.
> Character n-gram nearest-neighbor prediction.
> Hard-coded endpoint strings.
> Hard-coded depth assignments.
> sample_id as a predictive feature.
> View order as a predictive feature.
> Filename order as a predictive feature.
> Leaderboard probing intended to reconstruct hidden targets.
> Validation and Leakage
> One complete eight-view bundle is the atomic prediction unit.
> Keep together:
> All eight views.
> Both boundary targets.
> All eight depth labels.
> Cached embeddings.
> Pairwise representations.
> Auxiliary latent labels.
> The official split keeps protected writer groups on one side.
> Exact normalized boundary pairs do not cross the train/test boundary.
> Exact normalized public views do not cross the boundary.
> The private partition favors harder valid examples with:
> Larger edited token mass.
> Lower boundary overlap.
> More lexical and morphological replacement.
> More multi-token divergence.
> Less punctuation-only structure.
> Harder combinations of seven divergence shapes.
> Coarse boundary-divergence signatures that dominate the private set are reduced from training when doing so does not collapse the released training set.
> Private construction metadata is not released.
> Expected Outcome
> A successful system should:
> Compare eight incomplete related text states.
> Infer seven endpoint-defining binary factors.
> Recover evidence hidden by partial observation.
> Reject one balanced recurrent confounder.
> Determine the linguistic orientation of each factor.
> Generate two complete boundary texts absent from the input.
> Recover depth-3 versus depth-4 geometry.
> Preserve the common textual backbone.
> Recover the exact seven-block boundary divergence structure.
> Generalize across held-out writers and difficult factor combinations.
> Train and infer within the CPU-only environment.
> The prediction objective is:
> recover two hidden counterfactual boundary texts and the latent seven-factor field that explains eight partially observed internal states.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Cross-Lingual Payload Drift Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b058ycvhkk1fnq13eb6ggd18c5jx3
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jesuisnadi's score of 76.430!

Full challenge description from page:

> Leaderboard
> (2)
> Your Submissions
> Overview
> Cross-Lingual Payload Drift Detection is a hard CPU fine-tuning challenge about repairing disagreement across several textual views of the same underlying command.
> Each sample contains:
> One English anchor request.
> Four mixed-language echoes.
> Several plausible payload disagreements spread across those echoes.
> One hidden minimal repair ledger.
> The four echoes are not independent questions.
> They are competing observations of one command.
> Most wording is already correct.
> A small number of payload fragments have drifted.
> The model must identify those local disagreements, determine what the shared command actually requires, and generate the ordered set of repairs needed to bring every echo back into agreement.
> A conceptual sample may look like:
> Anchor:
> set an alarm for 7 tomorrow morning
> Echo E01:
> kal subah 8 baje alarm laga do
> Echo E02:
> kal subah 7 baje alarm laga do
> Echo E03:
> parso subah 7 baje alarm laga do
> Echo E04:
> kal subah 7 baje alarm set karo
> The hidden repair ledger could conceptually require:
> Repair the time payload in E01.
> Repair the day payload in E03.
> Leave the other payloads untouched.
> The participant does not output a corrected paragraph.
> The participant outputs a compact patch sequence.
> A conceptual target may look like:
> <PATCH> E01 L018 <OLD> 8 baje </OLD> <NEW> 7 baje </NEW> </PATCH>
> <PATCH> E03 L041 <OLD> parso </OLD> <NEW> kal </NEW> </PATCH>
> The L### symbols are opaque repair lanes.
> Their meanings are stable across the released challenge, but their numeric IDs carry no semantic information.
> A model must therefore solve five coupled problems:
> Detect which echoes contain semantic drift.
> Localize the incorrect payload span.
> Infer the intended replacement from the anchor and the other echoes.
> Infer the correct opaque repair lane.
> Emit all repairs in the required ledger order.
> This is not ordinary translation.
> It is not grammatical error correction.
> It is not intent classification.
> It is not semantic-tree generation.
> It is a multi-view discrepancy-repair task where the target is the minimal patch program that reconciles several partially trustworthy observations.
> Why the Task Uses Multiple Views
> A single noisy utterance can be ambiguous.
> Four echoes provide redundancy.
> For any recoverable semantic payload, at least one public view retains useful evidence about the intended value.
> However, the model is not told which echo is trustworthy for which payload.
> Different echoes can be correct in different places.
> A useful model should combine evidence across the entire sample rather than choose one echo as globally authoritative.
> The English anchor supplies an additional semantic reference.
> It can help resolve disagreements when the mixed-language echoes disagree with one another.
> The challenge therefore resembles a small textual sensor-fusion problem:
> The anchor provides one view.
> Each echo provides another view.
> Each view can preserve or distort different payloads.
> The output records only the repairs needed to restore consistency.
> The Repair Ledger
> Every target is a sequence of one or more patch records.
> Each patch uses the form:
> <PATCH> E## L### <OLD> old text </OLD> <NEW> new text </NEW> </PATCH>
> For example:
> <PATCH> E02 L007 <OLD> 9 pm </OLD> <NEW> 8 pm </NEW> </PATCH>
> A patch contains four important pieces of information:
> Which echo must be changed.
> Which learned repair lane is affected.
> Which visible span is wrong.
> Which replacement span restores the shared command.
> The output contains only actual repairs.
> Correct text is not repeated.
> This makes the target sparse.
> A model must distinguish:
> Evidence that confirms the shared command.
> Evidence that contradicts the shared command.
> Text that is grammatical framing.
> Text that represents a mutable payload.
> Echo IDs
> Every sample contains exactly four echo IDs:
> E01
> E02
> E03
> E04
> Echo IDs are local to the sample.
> They identify the four public observations.
> They do not have a stable quality ranking.
> E01 is not systematically cleaner than E04.
> The model should not treat echo number as a reliability feature.
> The repair ledger is ordered first by echo ID:
> E01 before E02 before E03 before E04.
> Within one echo, repairs are ordered by the left-to-right position of the incorrect span.
> This gives every sample one deterministic target ordering.
> Repair Lanes
> Every patch also contains one opaque lane ID.
> Lane IDs use the form:
> L001
> L002
> L003
> ...
> A repair lane identifies the recurring semantic role of the payload being repaired.
> The public label is intentionally opaque.
> For example, the challenge does not expose labels such as:
> destination
> date
> duration
> recipient
> reminder text
> artist
> event name
> Instead, those recurring repair channels are represented by arbitrary L### symbols.
> The mapping is globally stable.
> If L018 is associated with the same kind of payload in two training examples, it remains L018.
> The numeric ordering is random.
> Participants should not assume:
> Similar lane numbers have similar meanings.
> Low lane numbers are common.
> High lane numbers are rare.
> Consecutive lanes belong to the same task family.
> Lane numbers encode source position.
> The lane system forces the model to learn how local textual disagreements map onto recurring repair behavior.
> Pretrained language knowledge can help understand the utterances.
> It cannot directly reveal the lane mapping.
> Minimality
> The gold ledger contains only necessary changes.
> Suppose E02 already contains the correct payload.
> The model should not emit a patch that replaces that payload with an identical string.
> Suppose two echoes disagree, but one matches the shared command supported by the anchor and the remaining views.
> Only the inconsistent echo should be patched.
> A prediction that edits already-correct text is over-repair.
> A prediction that misses an inconsistent payload is under-repair.
> Both are penalized.
> The challenge therefore rewards minimal semantic intervention.
> Payload Drift
> Drift occurs only inside short payload-bearing spans.
> Examples may involve:
> Times.
> Dates.
> Durations.
> Locations.
> Names.
> Recipients.
> Message content.
> Reminder content.
> Music references.
> Event descriptions.
> Numeric quantities.
> Navigation endpoints.
> Weather locations.
> Other short task-bearing phrases.
> Drift is designed to remain locally plausible.
> A wrong payload should still look like text that could naturally occur in that position.
> For example:
> One valid city can replace another city.
> One valid time can replace another time.
> One valid contact name can replace another name.
> One valid duration can replace another duration.
> The task is not to detect nonsense.
> The task is to detect semantic inconsistency across views.
> Code-Switched Echoes
> The echo text mixes English and Romanized Indic phrasing in Latin script.
> A single echo may contain:
> English task vocabulary inside Indic syntax.
> Indic function words around English names.
> Mixed date and time expressions.
> English named entities inside mostly non-English wording.
> Informal Romanization.
> Spelling variation.
> Lower-case text.
> Missing punctuation.
> Short imperative constructions.
> The amount of switching varies.
> The same semantic payload can surface differently across the anchor and echoes.
> For example, an anchor may use:
> tomorrow morning
> while an echo may use:
> kal subah
> The model therefore cannot solve the task by exact substring agreement alone.
> Public Input
> Each sample exposes five textual views:
> One English anchor.
> Four mixed-language echoes.
> The four echo IDs are always:
> E01
> E02
> E03
> E04
> Training samples additionally expose repair_target.
> Test samples omit repair_target.
> The exact field types, row counts, and full JSON examples are provided in the Dataset section.
> Training Target
> repair_target is one string containing the complete ordered repair ledger.
> A conceptual target is:
> <PATCH> E01 L018 <OLD> 8 baje </OLD> <NEW> 7 baje </NEW> </PATCH> <PATCH> E03 L041 <OLD> parso </OLD> <NEW> kal </NEW> </PATCH>
> Every patch has exactly this structural order:
> <PATCH>
> Echo ID.
> Lane ID.
> <OLD>
> Incorrect visible span.
> </OLD>
> <NEW>
> Correct replacement text.
> </NEW>
> </PATCH>
> Ordinary whitespace between structural items is not semantically meaningful.
> Whitespace inside payload spans is canonicalized during evaluation.
> Repair Count
> Every sample requires between one and four patches.
> The released build is deliberately concentrated around two- and three-patch cases rather than single-edit cases.
> Across the full challenge:
> Approximately 20% of samples contain one repair.
> Approximately 40% contain two repairs.
> Approximately 30% contain three repairs.
> Approximately 10% contain four repairs.
> The median repair count is 2.
> The mean repair count is approximately 2.3.
> The exact counts are fixed in the released files.
> Participants should not assume a constant repair count.
> The model must decide when to stop emitting patches.
> A complete prediction must contain every required patch exactly once.
> Duplicate repair keys are structurally redundant and are penalized.
> What Must Be Learned
> The task contains several layers of learnable structure.
> Cross-View Agreement
> The model must determine which payload value is supported by the sample as a whole.
> This can require:
> Comparing the anchor with all four echoes.
> Recognizing paraphrases.
> Recognizing cross-language equivalents.
> Ignoring grammatical wording differences.
> Distinguishing semantic payloads from surrounding syntax.
> Drift Localization
> The model must identify the wrong span in the affected echo.
> This requires exact enough generation to reproduce the visible incorrect text.
> Replacement Recovery
> The model must generate the intended replacement span.
> The replacement may be:
> Copied from another echo.
> Closely paraphrased by another echo.
> Supported by the English anchor.
> Recoverable only after combining several views.
> Lane Induction
> The model must infer which opaque L### lane corresponds to the repaired payload role.
> Sparse Sequencing
> The model must output only the edits that matter and serialize them in deterministic order.
> Challenge Type
> This is a Fine-Tuning challenge.
> Generic pretrained sequence-to-sequence models are allowed.
> The intended solution is a learned conditional generator that consumes the anchor and four echoes and emits the repair ledger.
> Suitable model families include:
> Compact T5-style encoder-decoder models.
> Small BART-style encoder-decoder models.
> Compact multilingual text-to-text models.
> Byte-level encoder-decoder models.
> Small pretrained models with task-specific structural tokens.
> Pointer-augmented encoder-decoder systems.
> Compact models with learned cross-view pooling.
> CPU-friendly ensembles of eligible learned models.
> The challenge does not require a large language model.
> The intended regime is compact fine-tuning under CPU constraints.
> Machine-Learning Requirement
> The primary predictive system must be learned from released challenge examples.
> The following are not eligible as the main solution:
> Hand-written keyword dispatch.
> Manually authored lane dictionaries.
> Rule-only repair systems.
> Regular-expression-only drift detection.
> TF-IDF retrieval.
> Nearest-neighbor target replay.
> Template matching as the main predictor.
> Manual language-specific translation tables.
> Hard-coded payload correction rules.
> Exact memorization of training ledgers followed by lookup.
> Deterministic structural post-processing is allowed.
> Examples include:
> Blocking malformed patch tags.
> Preventing duplicate patch keys.
> Canonicalizing whitespace.
> Enforcing legal echo IDs.
> Enforcing legal lane IDs discovered from training.
> Sorting already-predicted patches into canonical order.
> Those procedures may constrain syntax.
> They must not determine the semantic repairs themselves.
> Compute
> The execution environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> The challenge is designed for compact fine-tuning.
> Useful CPU strategies include:
> Small pretrained encoder-decoder checkpoints.
> Compact source formatting.
> Short target length caps.
> Dynamic padding.
> Length bucketing.
> Cached tokenization.
> Gradient accumulation.
> Frozen lower layers during early experiments.
> Parameter-efficient fine-tuning where useful.
> Small beam widths.
> Constrained decoding.
> Early stopping on a participant-created local validation split.
> One or a few compact models instead of very large ensembles.
> The public text is short enough that participants do not need long-context architectures.
> Dataset
> The prepared competition dataset contains 16,800 samples in total.
> The split is fixed as:
> 14,400 training samples
> 2,400 test samples
> No official validation file
> 4 mixed-language echoes per sample
> 60 opaque repair lanes
> 1 to 4 gold repairs per sample
> Across the complete prepared dataset there are:
> 16,800 English anchors
> 67,200 mixed-language echoes
> Approximately 38,600 gold patch records
> 60 distinct L### repair-lane symbols
> A median of 2 repairs per sample
> A mean of approximately 2.3 repairs per sample
> The repair-count distribution is approximately:
> 20% of samples require 1 repair.
> 40% require 2 repairs.
> 30% require 3 repairs.
> 10% require 4 repairs.
> Every repair lane required by the test set is represented in the training set.
> The numeric lane IDs are scrambled and have no semantic ordering.
> The public package contains exactly three files:
> train.jsonl
> test.jsonl
> sample_submission.csv
> The private evaluator uses hidden answer data that is not part of the public package.
> train.jsonl
> train.jsonl contains exactly 14,400 JSON objects, one object per line.
> Each object contains four fields:
> sample_id
> anchor
> echoes
> repair_target
> sample_id
> Type: string.
> Opaque identifier used only for submission alignment.
> Example:
> PPL_0A17C4D2
> The identifier must not be used as a predictive feature.
> anchor
> Type: string.
> An English realization of the command shared by the sample.
> Example:
> Add a new weekly reminder for Sunday Brunch at 9 : 30 am
> echoes
> Type: list of four objects.
> Each echo object contains:
> echo_id: string
> text: string
> The four IDs are always:
> E01
> E02
> E03
> E04
> Each text field contains one mixed-language Latin-script realization of the same command.
> Different echoes may contain different payload drifts.
> repair_target
> Type: string.
> The complete ordered gold repair ledger.
> It contains every patch required to reconcile the four public echoes with the command expressed by the sample.
> One training row is:
> {"sample_id":"PPL_0A17C4D2","anchor":"Add a new weekly reminder for Sunday Brunch at 9 : 30 am","echoes":[{"echo_id":"E01","text":"9 : 30 am ko Sunday Brunch ke liye ek naya weekly reminder add karen"},{"echo_id":"E02","text":"8 : 30 am ko Sunday Brunch ke liye ek naya weekly reminder add karen"},{"echo_id":"E03","text":"9 : 30 am ko Saturday Brunch ke liye ek naya weekly reminder add karen"},{"echo_id":"E04","text":"9 : 30 am ko Sunday Brunch ke liye ek naya monthly reminder add karen"}],"repair_target":"<PATCH> E02 L017 <OLD> 8 : 30 am </OLD> <NEW> 9 : 30 am </NEW> </PATCH> <PATCH> E03 L044 <OLD> Saturday Brunch </OLD> <NEW> Sunday Brunch </NEW> </PATCH> <PATCH> E04 L052 <OLD> monthly </OLD> <NEW> weekly </NEW> </PATCH>"}
> For this row:
> E01 requires no repair.
> E02 contains one time drift.
> E03 contains one reminder-description drift.
> E04 contains one recurrence drift.
> The target contains exactly three patches.
> The lane IDs are opaque public symbols rather than descriptive field names.
> test.jsonl
> test.jsonl contains exactly 2,400 JSON objects, one object per line.
> Each object contains three fields:
> sample_id
> anchor
> echoes
> The structure of sample_id, anchor, and echoes is identical to the training file.
> The only omitted field is:
> repair_target
> One test row has the following structure:
> {"sample_id":"PPL_7D42B19E","anchor":"Send Alex a message saying I will arrive at six","echoes":[{"echo_id":"E01","text":"Alex ko message bhejo ki main six baje pahunchunga"},{"echo_id":"E02","text":"Alex ko message bhejo ki main seven baje pahunchunga"},{"echo_id":"E03","text":"Alex ko bolo ki main six baje pahunchunga"},{"echo_id":"E04","text":"Sam ko message bhejo ki main six baje pahunchunga"}]}
> For a test row, participants must infer:
> Which echoes require repair.
> Which lane applies to each repair.
> The visible OLD span.
> The intended NEW span.
> The complete patch sequence.
> The public test file does not expose:
> Gold patch keys.
> Gold OLD spans.
> Gold NEW spans.
> Gold repair counts.
> Canonical repaired echoes.
> Lane meanings.
> Construction metadata.
> Source partition metadata.
> sample_submission.csv
> sample_submission.csv contains exactly 2,400 rows, one for every sample_id in test.jsonl.
> It contains exactly two columns:
> sample_id
> prediction
> sample_id is copied directly from the test set.
> prediction is initially blank.
> The file begins in this form:
> sample_id,prediction
> PPL_7D42B19E,
> PPL_18F0A6C3,
> PPL_A931D50B,
> Participants should preserve:
> The same 2,400 sample IDs.
> The same column order.
> One row per test sample.
> No duplicate rows.
> No additional columns.
> The completed prediction cell must contain the entire generated repair ledger for that sample.
> Lane Inventory
> The prepared training data contains 60 distinct repair lanes.
> They are serialized as:
> L001
> L002
> L003
> ...
> L060
> The IDs are globally stable across training and test.
> There is no separate lane dictionary.
> Participants infer lane behavior from examples in train.jsonl.
> Every lane appearing in hidden test answers has at least one training occurrence.
> Lane numbers do not encode:
> Frequency.
> Semantic category.
> Source position.
> Echo identity.
> Difficulty.
> Repair count.
> Length and Sparsity Characteristics
> The source side of each sample is compact:
> One anchor.
> Four echoes.
> Five total text views.
> The target side is sparse.
> Only incorrect payloads are written into repair_target.
> Most words visible in the source do not appear in the target.
> Typical target variation comes from:
> Number of required repairs.
> OLD-span length.
> NEW-span length.
> Number of distinct repair lanes.
> Whether several echoes drift on related payloads.
> Whether the replacement is copied from another echo or inferred from the anchor.
> The combination of short inputs and sparse targets is intended to keep fine-tuning feasible on CPU while preserving a difficult multi-view reasoning problem.
> Drift Constellations
> The challenge does not use a plain random split.
> A sample can contain several repair keys such as:
> E01 / L018
> E03 / L041
> E04 / L006
> The set and co-occurrence pattern of repaired lanes across echoes forms a drift constellation.
> The official evaluation partition is designed so that the exact repair constellation of a test sample does not appear as a training target.
> In addition, test examples contain at least one lane co-repair relationship that is not reproduced as the same local repair pairing in released training examples.
> Individual lanes remain learnable.
> The challenge therefore tests whether a model can recombine familiar repair behaviors in unfamiliar multi-view disagreement patterns.
> This is different from memorizing a complete ledger template.
> For local validation, participants should avoid a purely random row split when possible.
> A more realistic split groups examples by repair constellation or rare lane co-repair patterns.
> Submission Format
> The submission contains one row per test sample.
> The columns are exactly:
> sample_id
> prediction
> The prediction field contains the complete generated repair ledger.
> Example:
> sample_id,prediction
> PPL_example,"<PATCH> E01 L018 <OLD> 8 baje </OLD> <NEW> 7 baje </NEW> </PATCH> <PATCH> E03 L041 <OLD> parso </OLD> <NEW> kal </NEW> </PATCH>"
> The submission must contain:
> Every expected sample_id.
> No missing IDs.
> No extra IDs.
> No duplicate IDs.
> Exactly the two published columns in the published order.
> Use sample_submission.csv exactly.
> Patch Parsing
> The evaluator parses every prediction into a sequence of patch records.
> A patch is valid only when it contains:
> One legal echo ID.
> One syntactically valid lane ID.
> One non-empty OLD span.
> One non-empty NEW span.
> Properly nested structural tags.
> A prediction can contain several valid patches.
> If one patch is malformed, that patch is not credited as a valid repair record.
> Catastrophic submission-schema errors still receive the minimum overall score.
> Patch Key
> Every repair has a patch key:
> echo_id + lane_id
> For example:
> E03 / L041
> The gold ledger never contains the same patch key twice.
> A prediction that repeats the same key creates redundant repairs.
> For structural matching, only the first predicted occurrence of a duplicate key is used.
> Duplicate records still reduce sequence and replay quality.
> Canonical Span Text
> For OLD and NEW spans, the evaluator applies:
> HTML entity decoding.
> Unicode NFKC normalization.
> Ordinary whitespace normalization.
> Case is preserved for exact-span matching.
> A separate token-level component compares spans case-insensitively.
> This allows partial credit for near-correct lexical recovery.
> Evaluation
> Submissions are scored with the Parallax Ledger Score from 0.01 to 100.
> Higher is better.
> The score evaluates six published components:
> Patch Key F1.
> OLD Span F1.
> NEW Span F1.
> Ledger Order LCS.
> Replay Fidelity.
> Exact Ledger.
> There are no hidden metric components.
> A perfect prediction receives exactly 100.
> Patch Key F1
> For each sample, compare the set of predicted patch keys with the gold patch keys.
> Let:
> P = unique predicted (echo_id, lane_id) keys
> G = gold patch keys
> Then:
> KeyPrecision = |P ∩ G| / |P|
> KeyRecall = |P ∩ G| / |G|
> PatchKeyF1 = 2 × KeyPrecision × KeyRecall / (KeyPrecision + KeyRecall)
> If the prediction contains no valid patch keys while gold repairs exist:
> PatchKeyF1 = 0
> The dataset-level value:
> K
> is the arithmetic mean of sample-level PatchKeyF1.
> This component measures whether the model found the correct repair locations in latent lane space.
> OLD Span F1
> For every gold patch key that also appears in the prediction, compare the predicted OLD span with the gold OLD span.
> Tokenization uses:
> Unicode normalization.
> Whitespace splitting.
> Case-insensitive token comparison.
> Tokens are compared as multisets.
> For one matched patch key:
> OldPrecision = matched_old_tokens / predicted_old_tokens
> OldRecall = matched_old_tokens / gold_old_tokens
> OLDTokenF1 is their harmonic mean.
> Predicted keys that are not gold keys contribute zero.
> Missing gold keys also contribute zero.
> The sample-level OLD Span F1 is the arithmetic mean over the union of predicted and gold patch keys.
> The dataset-level value is:
> O
> OLD Span F1 rewards precise localization of the visible disagreement.
> NEW Span F1
> The NEW span is evaluated in the same way.
> For every patch key, compare the predicted replacement text with the gold replacement text using case-insensitive token multiset F1.
> The sample-level score averages over the union of predicted and gold keys.
> The dataset-level value is:
> N
> This component rewards recovery of the intended payload, even when exact casing or one token is imperfect.
> Ledger Order LCS
> The gold patch sequence is ordered by:
> Echo ID.
> Left-to-right repair position within that echo.
> Ignore OLD and NEW text.
> Convert each patch to its key:
> E01/L018
> E03/L041
> ...
> Let:
> S_pred = predicted patch-key sequence
> S_gold = gold patch-key sequence
> Compute their longest common subsequence.
> Then:
> LedgerLCS = LCS_length / max(1, number_of_gold_patches)
> The value is clipped to 1.
> The dataset-level value is:
> L
> This component rewards recovery of the correct sparse repair route even when some lexical details are imperfect.
> Replay Fidelity
> The patch ledger is also evaluated by what happens when it is executed.
> For every echo:
> Start from the original public echo text.
> Read predicted patches for that echo in ledger order.
> For each patch, search for the normalized OLD span in the current echo.
> Replace the first unmatched exact occurrence with the predicted NEW span.
> If the OLD span cannot be found, that patch does not modify the echo.
> Continue until all predicted patches for the echo have been attempted.
> Canonical Repaired Echoes
> The canonical comparison text is not produced by a hidden model, external translator, retrieval system, or undisclosed normalization rule.
> For every sample and every echo, the canonical repaired echo is defined mechanically:
> Begin with the exact public echo string.
> Take the gold patches for that echo from the hidden gold ledger.
> Apply those gold patches in their published ledger order.
> Use the resulting string as the canonical repaired echo.
> An echo with no gold patch is its own canonical repaired echo.
> This definition means participants can reproduce Replay Fidelity exactly on any local validation row for which they know the gold ledger.
> No additional semantic annotation is consulted during scoring.
> After replaying the participant prediction, compare the resulting echo with the canonical repaired echo using normalized token edit similarity.
> For one echo:
> ReplaySimilarity = 1 - token_edit_distance / max(1, gold_token_count, predicted_token_count)
> where:
> gold_token_count is the number of tokens in the canonical repaired echo.
> predicted_token_count is the number of tokens after predicted replay.
> token_edit_distance is ordinary Levenshtein edit distance over whitespace-normalized tokens.
> The value is clipped to:
> [0, 1]
> The sample-level Replay Fidelity is the arithmetic mean across E01 through E04.
> The dataset-level value is:
> R
> This component is important because a patch can contain plausible local pieces but still fail to repair the visible echo when executed.
> Exact Ledger
> Normalize ordinary whitespace in the full predicted ledger and gold ledger.
> For one sample:
> ExactLedger = 1
> when the normalized strings are identical.
> Otherwise:
> ExactLedger = 0
> The dataset-level value is:
> X
> Exact match is a completion bonus rather than the sole metric.
> Final Score
> Let:
> K = Patch Key F1
> O = OLD Span F1
> N = NEW Span F1
> L = Ledger Order LCS
> R = Replay Fidelity
> X = Exact Ledger
> First define the localization term:
> Localization = sqrt(K × O)
> Then define the repair core:
> Core = 0.34 × Localization + 0.31 × N + 0.20 × R + 0.15 × L
> Define the replay gate:
> ReplayGate = 0.72 + 0.28 × R
> Define the completion bonus:
> Completion = 0.86 + 0.14 × X
> The final score is:
> Parallax Ledger Score = 100 × Core^1.20 × ReplayGate × Completion
> The result is clipped to:
> [0.01, 100]
> A perfect submission has:
> K = 1
> O = 1
> N = 1
> L = 1
> R = 1
> X = 1
> Therefore:
> Localization = 1
> Core = 1
> ReplayGate = 1
> Completion = 1
> Final Score = 100
> The exponent of 1.20 makes the upper leaderboard region require broad competence.
> The localization term requires both the correct latent repair key and the correct visible OLD span.
> The NEW span term rewards actual correction content.
> Replay Fidelity checks whether the ledger works when executed.
> Ledger LCS rewards correct sparse ordering.
> Exact Ledger adds a small premium for complete end-to-end reconstruction.
> Reproducing the Metric Locally
> For every validation sample:
> Parse the predicted patch ledger.
> Parse the gold patch ledger.
> Extract unique (echo_id, lane_id) patch keys.
> Compute Patch Key F1.
> Match predicted and gold records by patch key.
> Compute OLD span token F1 over the union of keys.
> Compute NEW span token F1 over the union of keys.
> Convert each ledger to its ordered patch-key sequence.
> Compute longest common subsequence divided by the number of gold patches.
> Replay the predicted ledger against each public echo.
> Compare each replayed echo with its canonical repaired echo using token edit similarity.
> Average Replay Fidelity across the four echoes.
> Compare the complete normalized ledger string for Exact Ledger.
> Average K, O, N, L, R, and X across validation samples.
> Compute Localization = sqrt(K × O).
> Compute Core = 0.34 × Localization + 0.31 × N + 0.20 × R + 0.15 × L.
> Compute ReplayGate = 0.72 + 0.28 × R.
> Compute Completion = 0.86 + 0.14 × X.
> Compute 100 × Core^1.20 × ReplayGate × Completion.
> Clip to [0.01, 100].
> The provided grader.py implements this procedure directly.
> Intended Learned Approaches
> A useful model should treat the entire sample as one multi-view source sequence.
> A practical source serialization may resemble:
> <ANCHOR> set an alarm for 7 tomorrow morning
> <E01> kal subah 8 baje alarm laga do
> <E02> kal subah 7 baje alarm laga do
> <E03> parso subah 7 baje alarm laga do
> <E04> kal subah 7 baje alarm set karo
> The target is the patch ledger.
> Compact Encoder-Decoder Fine-Tuning
> A practical baseline can fine-tune a compact pretrained seq2seq checkpoint on:
> anchor + four echoes -> repair_target
> Useful choices include:
> Small text-to-text transformers.
> Compact multilingual encoder-decoders.
> Byte-level models.
> Small models with added patch-grammar tokens.
> Structural Tokens
> Participants may add target grammar symbols as tokenizer tokens:
> <PATCH>
> </PATCH>
> <OLD>
> </OLD>
> <NEW>
> </NEW>
> Echo IDs.
> Lane IDs.
> This can reduce unnecessary fragmentation of the output language.
> Cross-View Attention
> A strong model should compare all views rather than encode each echo independently without interaction.
> Useful learned designs include:
> One concatenated encoder source.
> Segment embeddings for anchor and echo identity.
> Per-view encoding followed by learned pooling.
> Pairwise anchor-echo interaction layers.
> Echo-to-echo attention.
> Compact cross-view reranking heads.
> Copy-Aware Decoding
> OLD spans are visible in public echoes.
> NEW spans are often supported by another view.
> Useful mechanisms include:
> Ordinary cross-attention copying.
> Pointer-style heads.
> Copy gates.
> Source alignment supervision derived from training targets.
> Span-copy auxiliary losses.
> Lane Auxiliary Tasks
> Participants may derive extra supervision from repair_target.
> Examples include:
> Lane presence.
> Echo repair count.
> Per-echo lane set.
> Total patch count.
> OLD span alignment.
> NEW span source-view alignment.
> Patch-key sequence.
> Whether a lane is repaired in more than one echo.
> Pairwise lane co-repair prediction.
> These labels are allowed because they are derived entirely from released challenge training targets.
> Constrained Decoding
> The patch grammar is regular enough to constrain.
> Useful constraints include:
> <OLD> cannot appear before a legal echo and lane.
> Every <PATCH> must close.
> Echo IDs must be E01 through E04.
> Lane IDs must come from the training inventory.
> <NEW> must follow </OLD>.
> End-of-sequence can be blocked while a patch is open.
> These restrictions improve serialization without hand-coding the semantic answer.
> Hard-Negative Learning
> The public echoes contain plausible but conflicting payloads.
> This creates natural hard negatives.
> A participant may derive training pairs such as:
> Correct lane versus incorrect lane.
> Correct echo versus unmodified echo.
> Gold replacement versus rival payload from another view.
> Required patch versus unnecessary patch.
> A compact model may benefit from an auxiliary ranking objective over these alternatives.
> Local Validation
> A random validation split can be misleading.
> A stronger local estimate groups by:
> Exact repair constellation.
> Lane co-repair pairs.
> Patch count.
> Echo repair pattern.
> Rare lane combinations.
> Keep all derived versions of one sample together.
> Do not split augmented copies, cached features, or auxiliary labels from one sample across local train and validation.
> What Makes the Challenge Hard
> Several sources of uncertainty interact.
> No Globally Trusted Echo
> Different views can be wrong in different places.
> A model cannot simply select E01 or E04 as the canonical sentence.
> Cross-Language Evidence
> The English anchor and mixed-language echoes can express the same payload with different surface forms.
> Plausible Drift
> Incorrect values are chosen to remain locally believable.
> Surface fluency is therefore a weak signal.
> Sparse Output
> Most source text is already correct.
> The model must learn when not to emit a repair.
> Opaque Lane Semantics
> The correct repair lane must be inferred from training examples.
> Multi-Patch Coupling
> Several disagreements can occur in one sample.
> A wrong global interpretation can cause multiple patch errors.
> Replay Requirement
> Plausible-looking patches still need to execute successfully against the public text.
> Constellation Holdout
> The evaluation split recombines familiar repair behaviors in disagreement patterns that are not repeated as full training targets.
> CPU Constraint
> Very large sequence models are impractical.
> Strong results require efficient use of compact pretrained models.
> Practical CPU Baseline
> A practical eligible baseline may:
> Read train.jsonl.
> Serialize anchor and echoes with explicit segment tokens.
> Discover lane IDs from training targets.
> Extend a compact pretrained tokenizer with patch grammar tokens.
> Fine-tune a small encoder-decoder on complete repair ledgers.
> Use a local constellation-aware validation split.
> Decode with a small beam.
> Apply grammar constraints.
> Evaluate with the official metric.
> Generate one repair ledger for every test sample.
> A stronger system may add:
> Copy-aware decoding.
> Patch-count auxiliary prediction.
> Per-echo repair detection.
> Lane-presence auxiliaries.
> Cross-view contrastive objectives.
> Hard-negative ranking among rival payloads.
> Two compact models with different tokenization schemes.
> Model-based reranking using replay validity.
> Allowed Resources
> Participants may use:
> Released challenge files.
> Generic pretrained sequence-to-sequence checkpoints.
> Generic pretrained tokenizers distributed with eligible checkpoints.
> Standard machine-learning libraries.
> Standard deep-learning frameworks.
> Public architecture implementations.
> Beam search.
> Grammar-constrained decoding.
> Tokenizer extension with released structural tokens.
> Auxiliary labels derived from released training targets.
> Participant-created local validation splits.
> CPU-friendly ensembles of eligible learned models.
> Disallowed Resources
> Participants may not use:
> A checkpoint trained specifically for this challenge.
> External examples containing challenge repair ledgers.
> External mappings from lane IDs to descriptive meanings.
> Search engines at inference time.
> External retrieval at inference time.
> Hand-written keyword-to-lane rules.
> Manual lane dictionaries.
> Rule-only repair systems.
> TF-IDF retrieval as the primary predictor.
> Nearest-neighbor ledger replay as the primary predictor.
> Manual annotation of test samples.
> Hidden evaluator files.
> Hard-coded test repairs.
> Submission-feedback reconstruction of hidden answers.
> sample_id as a predictive feature.
> Row order as a predictive feature.
> Filename order as a predictive feature.
> Leakage Rules
> The atomic modeling unit is one complete parallax sample:
> One anchor.
> Four echoes.
> One repair ledger.
> All derivatives of one sample should remain together in local validation.
> This includes:
> Tokenized copies.
> Span alignments.
> Copy labels.
> Lane-presence labels.
> Patch-count labels.
> Hard-negative variants.
> Cached embeddings.
> Augmented source serializations.
> Do not use packaging artifacts as features.
> Limitations
> The benchmark focuses on short assistant-style requests.
> It does not measure:
> Open-domain conversation.
> Long-form translation.
> Document revision.
> Factual web retrieval.
> General spelling correction.
> Speech recognition.
> Acoustic code-switching.
> Long-context memory.
> Arbitrary software patching.
> Mixed-language Romanization is variable.
> Some payloads are easier to align than others.
> Some replacement strings may have several plausible surface realizations, but each released training row uses one deterministic target repair.
> The metric provides partial lexical credit, but it does not automatically treat all paraphrases as equivalent.
> Expected Outcome
> A successful system should:
> Fuse evidence from one anchor and four partially trustworthy echoes.
> Detect semantically inconsistent payloads.
> Avoid unnecessary edits.
> Recover correct replacement text.
> Induce the hidden repair-lane vocabulary.
> Serialize a minimal patch program.
> Generalize to unfamiliar multi-repair constellations.
> Produce patches that successfully replay against the public echoes.
> Train and infer efficiently on 10 CPU cores and 62.5 GiB RAM.
> The prediction objective is:
> reconstruct the minimal parallax patch ledger that reconciles every test sample.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Discourse Compression Program Synthesis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72w0rctdqpzh7wvrth6hgqgx8c3bht
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat zip_zip_zap_zap's score of 80.970!

Full challenge description from page:

> Leaderboard
> (13)
> Your Submissions
> Overview
> Discourse Compression Program Synthesis is a hard pretrained sequence-to-sequence challenge about compiling explicit multi-turn language into executable conversational compression programs.
> Each sample contains one four-stage discourse chain.
> The chain does not contain ordinary free-form conversation turns.
> Instead, every stage exposes an expanded request in which important referents and relations are stated explicitly.
> The first three stages also contain a reply.
> Later stages may be compressed because information is already available earlier in the chain.
> The prediction is not the compressed text itself.
> The model must emit a compact program that transforms the expanded requests at stages S2, S3, and S4 into their hidden compact conversational forms.
> Every program must jointly determine:
> Which source-token spans should be deleted.
> Which source-token spans should be replaced.
> Where new short phrases should be inserted.
> Which local phrase-vault entry supplies inserted or replacement text.
> Which earlier discourse cell licenses a compression decision.
> The exact program order for three successive stages.
> The official evaluator executes the submitted program.
> This means the task is simultaneously:
> Sequence generation.
> Span localization.
> Local-symbol grounding.
> Discourse dependency prediction.
> Program synthesis.
> Executable text transformation.
> A prediction can therefore fail in several different ways.
> It can select the correct phrase but edit the wrong source span.
> It can identify the correct edit but point to the wrong earlier discourse cell.
> It can predict individually plausible edits that do not form a valid executable program.
> It can produce a syntactically correct program whose execution yields the wrong compact turn.
> The challenge is designed around these coupled failure modes.
> What Is Being Predicted
> Every sample contains four stages:
> S1
> S2
> S3
> S4
> The participant predicts programs only for:
> T2
> T3
> T4
> T2 transforms the expanded request at S2.
> T3 transforms the expanded request at S3.
> T4 transforms the expanded request at S4.
> A complete prediction has the form:
> T2{...}|T3{...}|T4{...}
> Each block contains one or more edit operations or the special operation:
> NOP
> The allowed edit operations are:
> D
> I
> R
> D means delete a source span.
> I means insert one phrase-vault entry before a source-token position.
> R means replace a source span with one phrase-vault entry.
> Every non-NOP operation also contains an antecedent cell.
> The antecedent describes where the discourse chain makes that compression possible.
> Why This Is Not Ordinary Text Generation
> The target is an executable transformation program rather than a sentence.
> The model cannot receive full credit by producing text that merely sounds conversational.
> It has to recover the hidden transformation geometry.
> Consider an expanded request with the following token sequence:
> what other films did x02 direct ?
> The zero-based token positions are:
> 0 what
> 1 other
> 2 films
> 3 did
> 4 x02
> 5 direct
> 6 ?
> Suppose the hidden compact turn uses:
> he
> instead of:
> x02
> and suppose the phrase vault contains:
> V07 = he
> A replacement operation can be:
> R:4:5:V07:C02
> This means:
> R: perform a replacement.
> 4: source span begins at token 4.
> 5: source span ends before token 5.
> V07: insert the phrase stored in V07.
> C02: the compression is licensed by discourse cell C02.
> Executing the operation transforms:
> what other films did x02 direct ?
> into:
> what other films did he direct ?
> The model is therefore learning a latent conversational compression process rather than generating unconstrained surface text.
> Four-Stage Chains
> Each public sample contains a chain with four stage objects.
> S1 contains:
> One expanded request.
> One reply.
> S2 contains:
> One expanded request.
> One reply.
> S3 contains:
> One expanded request.
> One reply.
> S4 contains:
> One expanded request.
> Replies are included because later compression can depend on material introduced either by an earlier request or by an earlier reply.
> The entire four-stage chain is visible when predicting T2, T3, and T4.
> The benchmark evaluates retrospective discourse compilation rather than an online causal assistant.
> Local Variables
> Public chains contain local symbols such as:
> x01
> x02
> x03
> These symbols are sample-local discourse variables.
> They have no global meaning.
> x01 in one sample has no relationship to x01 in another sample.
> The model should treat them as locally bound semantic objects whose behavior must be inferred from the chain in which they occur.
> This design matters because success should come from understanding discourse structure rather than memorizing globally recurring names or topics.
> A model may need to learn patterns such as:
> A locally repeated variable can later be replaced by a pronoun.
> A relation already established in an earlier stage can be omitted later.
> A compact follow-up can inherit a predicate from previous discourse.
> A replacement can be licensed by an earlier request or an earlier reply.
> The local symbols deliberately break global lexical identity.
> Phrase Vault
> Every sample contains exactly twelve local phrase-vault entries:
> V01
> V02
> V03
> V04
> V05
> V06
> V07
> V08
> V09
> V10
> V11
> V12
> Each vault entry contains a short text phrase.
> A vault may contain phrases such as:
> he
> it
> they
> that
> there
> what about
> how about
> that person
> Only some vault entries are needed by the hidden program.
> The remaining entries are distractors.
> The vault is local to one sample.
> V03 in one sample is unrelated to V03 in another sample.
> The model must therefore select vault entries from their text and their compatibility with the current discourse state.
> Discourse Cells
> Antecedent pointers use local discourse-cell IDs.
> The available cells grow as the chain progresses.
> For T2, the available prior cells are:
> C01 = S1 expanded request
> C02 = S1 reply
> For T3, the available prior cells are:
> C01 = S1 expanded request
> C02 = S1 reply
> C03 = S2 expanded request
> C04 = S2 reply
> For T4, the available prior cells are:
> C01 = S1 expanded request
> C02 = S1 reply
> C03 = S2 expanded request
> C04 = S2 reply
> C05 = S3 expanded request
> C06 = S3 reply
> The special pointer:
> C00
> means that the operation does not have one explicit earlier discourse cell as its canonical license.
> C00 is valid at every target stage.
> Pointers to future cells are invalid.
> For example:
> T2 cannot point to C03.
> T3 cannot point to C05.
> T4 can point to C01 through C06.
> Program Grammar
> A complete prediction must contain exactly three blocks in this order:
> T2{...}|T3{...}|T4{...}
> Blocks cannot be omitted or reordered.
> NOP
> NOP means that the expanded request is already the hidden compact form under the benchmark's canonical tokenization.
> Example:
> T3{NOP}
> NOP must appear alone inside its stage block.
> It cannot be combined with another operation.
> Delete
> Delete syntax is:
> D:start:end:antecedent
> Example:
> D:2:5:C03
> The source span is zero-based and half-open.
> D:2:5 deletes source tokens:
> 2
> 3
> 4
> Token 5 is not deleted.
> The operation does not use a vault entry.
> Insert
> Insert syntax is:
> I:position:vault_id:antecedent
> Example:
> I:2:V04:C00
> The vault phrase is inserted before source token position 2.
> Insertion at the end of a source is allowed by using a position equal to the source-token count.
> Replace
> Replace syntax is:
> R:start:end:vault_id:antecedent
> Example:
> R:4:6:V09:C02
> The source span from token 4 through token 5 is replaced by the phrase stored in V09.
> The end position is exclusive.
> Multiple Operations
> Multiple operations inside one stage are separated by semicolons.
> Example:
> T3{D:0:2:C03;I:0:V06:C03}
> Operations must be listed in nondecreasing source-position order.
> Source-consuming spans cannot overlap.
> A prediction that tries to edit an already consumed source span is invalid for that stage.
> Multiple insertions at the same source position are not valid.
> Canonical Tokenization
> Program positions operate on canonical tokens rather than raw character offsets.
> Before tokenization, text is:
> Unicode-normalized with NFKC.
> Whitespace-collapsed.
> Case-folded.
> The tokenizer then uses the following conceptual rule:
> A word token may contain letters, digits, underscores, and an internal straight or curly apostrophe.
> Every remaining non-whitespace punctuation symbol is a separate token.
> Conceptually, the tokenization pattern is:
> word-with-optional-apostrophe OR one punctuation symbol
> For example:
> where did x03's group go?
> becomes approximately:
> where
> did
> x03's
> group
> go
> ?
> The released public text is already normalized to this style, but participants should reproduce the official tokenization exactly when generating span positions.
> The provided grader.py contains the definitive implementation.
> Program Execution
> A stage program is executed against the stage's expanded request.
> Let the source token list be:
> s0 s1 s2 ... sn
> Operations are processed from left to right.
> For a deletion:
> Copy untouched tokens before the deleted span.
> Skip the deleted source tokens.
> For an insertion:
> Copy untouched tokens before the insertion position.
> Emit the selected vault phrase.
> Continue from the same source position.
> For a replacement:
> Copy untouched tokens before the replaced span.
> Emit the selected vault phrase.
> Skip the replaced source tokens.
> After all operations, the remaining source suffix is copied.
> NOP simply returns the source token sequence unchanged.
> The evaluator performs this execution itself.
> The submission therefore specifies an actual program, not merely metadata describing an intended edit.
> Conceptual Example
> Suppose one sample contains:
> S1 expanded request:
> who directed x01 ?
> S1 reply:
> x02 directed x01 .
> S2 expanded request:
> what other films did x02 direct ?
> S2 reply:
> x02 also directed several later films .
> S3 expanded request:
> when was x02 born ?
> S3 reply:
> x02 was born in 1937 .
> S4 expanded request:
> where did x02 study ?
> Suppose the phrase vault includes:
> V03 = they
> V07 = he
> V10 = there
> A possible target program is:
> T2{R:4:5:V07:C02}|T3{R:2:3:V07:C04}|T4{R:2:3:V07:C06}
> The program does three things jointly:
> Compresses the explicit variable x02.
> Chooses the local phrase he from the vault.
> Tracks which earlier discourse cell canonically licenses the compression at each stage.
> The exact examples in the dataset are more varied than this simplified illustration.
> Why the Task Is Structured
> A standard seq2seq problem usually asks a model to generate one target string from one source string.
> This benchmark adds several coupled structures.
> First, all three target stages share one phrase vault.
> Second, later stages can point to a larger set of discourse cells than earlier stages.
> Third, an edit must satisfy token-span geometry.
> Fourth, the emitted program must execute.
> Fifth, several different-looking programs can produce superficially similar text, but the benchmark also evaluates whether the predicted program recovers the canonical hidden structure.
> A useful model therefore has to reason at several levels at once:
> Which discourse information is already established.
> Whether a later request should be compressed.
> Which source material should disappear.
> Which short replacement best fits.
> Which previous cell explains the compression.
> How to serialize the result in a strict program language.
> Challenge Type
> This is a pretrained sequence-to-sequence Fine-Tuning challenge.
> Pretrained encoder-decoder models are allowed.
> The intended solution family is compact neural sequence transduction.
> Suitable model families include:
> T5-style encoder-decoder models.
> FLAN-T5-style compact encoder-decoder models.
> BART-style encoder-decoder models.
> Compact pretrained denoising seq2seq models.
> Neural pointer-generator hybrids initialized from eligible pretrained seq2seq checkpoints.
> Encoder-decoder models with auxiliary span heads.
> Encoder-decoder models with auxiliary antecedent classification heads.
> Multi-task neural systems that predict both program tokens and program components.
> Small neural ensembles that fit the execution environment.
> Participants may also train a seq2seq architecture from scratch, but pretrained encoder-decoder initialization is explicitly allowed and is the intended route.
> ML-Only Requirement
> Predictions must be produced by a learned machine-learning model.
> This is not a rule-programming competition.
> The following are not eligible as the primary predictive system:
> Hand-written pronoun replacement systems.
> Regex-only compression logic.
> Deterministic edit-template lookup.
> Manually authored antecedent rules.
> TF-IDF systems.
> BM25 systems.
> Character n-gram retrieval used as the main predictor.
> Nearest-neighbor target copying.
> Hard-coded program inventories selected without a learned model.
> Deterministic code is still allowed for ordinary plumbing such as:
> Parsing JSON.
> Tokenization.
> Serializing model outputs.
> Validating generated program syntax.
> Executing a predicted program locally.
> Constrained decoding around neural model scores.
> The semantic prediction itself must come from learned model parameters.
> Pretrained Model Limits
> The environment is CPU-only.
> The benchmark is intended for compact pretrained seq2seq models rather than large language models.
> Eligible pretrained models should be practical under the released environment.
> Participants should prefer models in approximately the small-to-base encoder-decoder range.
> Large decoder-only chat models are outside the intended solution class.
> Remote model APIs are not allowed.
> External model-generated labels are not allowed.
> External retrieval is not allowed.
> Compute
> The execution environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> The challenge is designed around short local chains and short structured targets.
> Useful CPU strategies include:
> Compact encoder-decoder checkpoints.
> Sequence-length truncation based on the released data distribution.
> Dynamic padding.
> Gradient accumulation.
> Freezing lower encoder layers for early experiments.
> Adapter or low-rank fine-tuning when supported efficiently.
> Cached tokenization.
> Constrained program-token decoding.
> Separate lightweight auxiliary heads for span positions and antecedent cells.
> Mixed objectives that teach program syntax before exact full-program generation.
> The target sequence is substantially shorter than ordinary open-ended generation.
> This makes structured seq2seq fine-tuning practical on CPU despite the reasoning difficulty of the task.
> Released Dataset
> The public package contains:
> public/train.jsonl
> public/test.jsonl
> public/sample_submission.csv
> There is no official validation file.
> There is no separate public schema file.
> All required structure is documented here.
> train.jsonl
> Each line contains one JSON object.
> sample_id
> Type: string.
> Unique row identifier used only for submission alignment.
> Do not use sample_id itself as a predictive feature.
> chain
> Type: list of four objects.
> The objects are ordered S1 through S4.
> Every stage object contains:
> stage
> expanded_request
> S1 through S3 additionally contain:
> reply
> S4 has no reply field.
> phrase_vault
> Type: list of twelve objects.
> Each object contains:
> id
> text
> The IDs are always V01 through V12.
> The order of the list carries no semantic meaning beyond the explicit ID.
> target_program
> Training only.
> Type: string.
> Contains the canonical three-stage program:
> T2{...}|T3{...}|T4{...}
> The participant may execute the training target program against the public chain and phrase vault to recover the corresponding compact token sequence.
> This is useful for local debugging and auxiliary supervision.
> test.jsonl
> Contains the same participant-visible input fields as train.jsonl except:
> target_program
> is omitted.
> The test data does not expose:
> The canonical edit operations.
> The compact executed target turns.
> The correct vault choices.
> The correct antecedent cells.
> Hidden grouping information.
> Construction metadata.
> Train/Test Split
> The official split keeps related discourse chains together.
> Samples derived from the same underlying discourse family do not cross the official partition boundary.
> This prevents a validation strategy from succeeding by seeing another transformed view of the same local discourse on the opposite side of the split.
> Local validation should also be performed at complete-sample level.
> Do not split individual operations from one program across training and validation.
> Submission Format
> The submission contains one row per test sample.
> The columns are exactly:
> sample_id
> prediction
> The prediction field contains one complete three-stage program.
> Example:
> DCP_example,T2{R:4:5:V07:C02}|T3{R:2:3:V07:C04}|T4{R:2:3:V07:C06}
> The submission must contain:
> Every expected sample_id.
> No extra sample IDs.
> No duplicate sample IDs.
> Exactly the two published columns in the published order.
> Use sample_submission.csv exactly.
> Syntactic Validity
> A prediction is syntactically parseable only when:
> It contains exactly three blocks.
> The block order is T2, T3, T4.
> Every block has matching braces.
> Every non-NOP operation has the required number of fields.
> Every numeric position parses as an integer.
> Every vault ID is one of V01 through V12.
> Every antecedent ID is valid for that stage.
> A completely unparseable prediction receives zero component credit for that sample before final score clipping.
> Execution Validity
> A syntactically parseable stage can still be non-executable.
> A stage is invalid when, for example:
> A source position is negative.
> A source position exceeds the source-token count.
> A deletion has end less than or equal to start.
> A replacement has end less than or equal to start.
> Operations move backward in source order.
> Source-consuming edit spans overlap.
> Multiple insertions target the same position.
> NOP is mixed with another operation.
> An invalid stage receives zero executed-surface credit.
> Its operations do not contribute valid predicted atoms.
> The Validity component also records the failure directly.
> Evaluation
> Submissions are evaluated using the Discourse Compression Program Synthesis Score from 0.01 to 100.
> Higher is better.
> The evaluator measures both what the program does and how the program is structured.
> The published dataset-level components are:
> Surface Reconstruction.
> Program Topology.
> Exact Atom F1.
> Antecedent Recovery.
> Execution Validity.
> There are no hidden metric weights.
> A perfect gold program receives exactly 100.
> Surface Reconstruction
> The evaluator executes both the submitted program and the hidden gold program for T2, T3, and T4.
> For each stage, let:
> P = predicted executed token sequence
> G = gold executed token sequence
> Two sequence similarities are calculated.
> Token Bag F1
> Treat P and G as token multisets.
> Let overlap be the multiset intersection count.
> Precision is:
> overlap / number of predicted tokens
> Recall is:
> overlap / number of gold tokens
> TokenBagF1 is their harmonic mean.
> Token Sequence F1
> Compute the longest common subsequence length between P and G.
> Let L be the LCS length.
> Then:
> TokenSequenceF1 = 2 × L / (|P| + |G|)
> Stage Surface
> The stage surface score is the harmonic mean of:
> TokenBagF1
> and
> TokenSequenceF1
> If the submitted stage is not executable, its stage surface score is zero.
> Surface Reconstruction is the arithmetic mean of the three stage-surface values, followed by an arithmetic mean across test samples.
> Call this dataset-level value:
> S
> Program Topology
> Program Topology evaluates the geometric shape of the edits without requiring the vault choice or antecedent pointer to already be correct.
> For a non-NOP operation, its topology skeleton is:
> stage
> operation type
> start position
> end position
> For an insertion, start and end are the same insertion position.
> For NOP, the stage-specific NOP marker is the topology skeleton.
> Two topology scores are calculated for each sample.
> Skeleton F1
> Compare the multiset of predicted topology skeletons with the gold topology skeletons using F1.
> Skeleton Sequence F1
> Compare the ordered predicted and gold skeleton sequences using longest-common-subsequence F1:
> 2 × LCS / (predicted skeleton count + gold skeleton count)
> Sample Topology
> The sample Program Topology is the harmonic mean of:
> Skeleton F1
> and
> Skeleton Sequence F1
> Program Topology is averaged across all test samples.
> Call this dataset-level value:
> T
> Exact Atom F1
> Program Topology ignores the selected phrase and antecedent.
> Exact Atom F1 evaluates the full operation.
> For delete, the canonical atom is:
> stage, D, start, end, antecedent
> For insert, the canonical atom is:
> stage, I, position, vault_id, antecedent
> For replace, the canonical atom is:
> stage, R, start, end, vault_id, antecedent
> NOP is a stage-specific atom.
> Predicted and gold atoms are compared as multisets using F1.
> This gives partial credit when some operations are correct and others are wrong.
> Exact Atom F1 is averaged across all test samples.
> Call this dataset-level value:
> A
> Antecedent Recovery
> Some gold operations use C00.
> Other gold operations point to a concrete earlier discourse cell.
> Antecedent Recovery evaluates only gold operations whose canonical antecedent is not C00.
> For every such gold operation:
> Find a predicted operation with the same topology skeleton.
> Check whether its antecedent cell is exactly correct.
> Give one point if the pointer matches.
> Give zero otherwise.
> The sample score is:
> correct concrete antecedent pointers / number of gold concrete antecedent pointers
> If a sample has no concrete gold antecedent pointers, its Antecedent Recovery value is 1.
> The dataset-level value is the arithmetic mean across samples.
> Call this value:
> P
> Execution Validity
> For every sample, independently validate the T2, T3, and T4 programs.
> A valid stage contributes one.
> An invalid stage contributes zero.
> For one sample:
> Validity = valid stage count / 3
> The dataset-level Execution Validity is the arithmetic mean across samples.
> Call this value:
> V
> Final Score
> First define the structure term:
> Structure = 0.55 × T + 0.45 × A
> Then combine executed text quality and program structure with a harmonic mean:
> Core = 0, if S + Structure = 0
> otherwise:
> Core = 2 × S × Structure / (S + Structure)
> Define the discourse-dependency term:
> Dependency = sqrt(P × V)
> The final score is:
> Discourse Compression Program Synthesis Score = 100 × Core^1.20 × (0.65 + 0.35 × Dependency)
> The result is clipped to:
> [0.01, 100]
> A perfect prediction has:
> S = 1
> T = 1
> A = 1
> P = 1
> V = 1
> Therefore:
> Structure = 1
> Core = 1
> Dependency = 1
> Final Score = 100
> Why the Metric Is Joint
> Surface-only evaluation would allow a model to receive high credit from an accidental or non-canonical transformation.
> Program-only evaluation would over-penalize a model whose alternate local edit still reconstructs most of the correct compact language.
> The combined score rewards both.
> Surface Reconstruction measures the behavior of the executed program.
> Program Topology measures whether the correct source geometry was found.
> Exact Atom F1 measures vault grounding and full canonical operations.
> Antecedent Recovery measures discourse dependency.
> Execution Validity prevents malformed programs from receiving structural credit.
> The Core exponent makes good joint reconstruction necessary for strong leaderboard scores.
> Reproducing the Metric Locally
> For every validation sample:
> Parse the gold target program.
> Parse the predicted program.
> Tokenize the S2, S3, and S4 expanded requests using the official canonical tokenizer.
> Validate each predicted stage against its source-token count.
> Execute every valid predicted stage using the local phrase vault.
> Execute the gold stages the same way.
> Compute Token Bag F1 for each stage.
> Compute token LCS F1 for each stage.
> Harmonic-mean the two values to obtain stage Surface Reconstruction.
> Average the three stage values.
> Convert predicted and gold programs into topology skeletons.
> Compute skeleton multiset F1.
> Compute skeleton LCS F1.
> Harmonic-mean the two topology scores.
> Convert valid predicted and gold programs into full atoms.
> Compute Exact Atom F1.
> Evaluate concrete antecedent pointers only on topology-matched operations.
> Compute the fraction of T2, T3, and T4 that executed validly.
> Average each component across validation samples.
> Compute Structure = 0.55 × T + 0.45 × A.
> Harmonic-mean S and Structure to obtain Core.
> Compute Dependency = sqrt(P × V).
> Apply the published final formula.
> Clip the result to [0.01, 100].
> The provided grader.py implements this procedure directly.
> Intended Modeling Approaches
> The task is naturally suited to compact pretrained encoder-decoder models.
> A strong system may serialize the input chain into one source sequence such as:
> S1 request ... S1 reply ... S2 request ... S2 reply ... S3 request ... S3 reply ... S4 request ... vault V01 ... V12 ...
> and train the decoder directly on the canonical program string.
> That simple formulation is eligible, but several stronger approaches are possible.
> Program-Aware Seq2Seq
> Use a pretrained seq2seq model and add special tokens for:
> T2
> T3
> T4
> D
> I
> R
> NOP
> C00 through C06
> V01 through V12
> The model can learn the grammar as a structured target language.
> Constrained Decoding
> At inference time, the decoder can be constrained so impossible next tokens are masked.
> Examples include:
> Force T2 before T3 before T4.
> Restrict antecedent cells by stage.
> Restrict vault IDs to V01 through V12.
> Prevent malformed braces.
> Prevent illegal operation field counts.
> Constrained decoding is allowed because the semantic scores still come from the learned model.
> Auxiliary Span Prediction
> A model can attach lightweight heads to encoder states and predict:
> Operation start positions.
> Operation end positions.
> Operation type.
> Whether a stage is NOP.
> The auxiliary predictions can be used only during training or can guide the decoder.
> Auxiliary Vault Selection
> The twelve phrase-vault entries form a small local candidate set.
> A model can encode each vault phrase and score it against the current stage representation.
> The resulting local selection loss can supplement sequence cross-entropy.
> Auxiliary Antecedent Selection
> Each target stage has only a small legal antecedent inventory.
> A neural pointer head can score earlier discourse cells.
> Useful representations include:
> Mean-pooled encoder states for each cell.
> Cell boundary states.
> Cross-attention scores from the target-stage representation.
> Learned local cell embeddings combined with contextual states.
> Multi-Task Training
> Useful learned objectives include:
> Full program sequence cross-entropy.
> Stage-level NOP classification.
> Edit-operation classification.
> Start-position prediction.
> End-position prediction.
> Vault-entry classification.
> Antecedent-cell classification.
> Program-validity auxiliary loss.
> Executed-token reconstruction as an auxiliary decoder target.
> All auxiliary supervision must be derived from released training examples.
> A Practical Neural Baseline
> A practical baseline can:
> Read train.jsonl.
> Serialize the four-stage chain and twelve vault phrases into a single input sequence.
> Add a small set of program symbols to the tokenizer.
> Fine-tune a compact pretrained encoder-decoder model.
> Train with teacher-forced cross-entropy on target_program.
> Use beam search at inference time.
> Reject malformed beams.
> Prefer the highest-scoring executable beam.
> Write the final program into the prediction column.
> A stronger baseline may jointly train auxiliary classifiers for:
> Stage edit count.
> Operation type.
> Span boundaries.
> Vault choice.
> Antecedent pointer.
> This is still compact enough for CPU experimentation because each sample contains only four short stages and twelve short vault entries.
> Why Pure Copying Is Weak
> The target is not present as a contiguous substring of the input.
> The decoder must generate:
> Operation letters.
> Numeric source positions.
> Local vault IDs.
> Local antecedent IDs.
> Stage delimiters.
> Copying the input text does not produce an executable program.
> Likewise, copying the most common program template is weak because:
> Edit spans vary.
> Vault assignments are local.
> Local variables reset per sample.
> Antecedent availability changes by stage.
> Some stages are NOP.
> Some stages use deletion or insertion rather than replacement.
> Why Global Memorization Is Weak
> The important identifiers are local.
> x01 is local.
> V01 is local.
> C01 is a positional discourse cell rather than a global entity.
> The same surface vault phrase can receive different vault IDs across samples.
> A model cannot learn that V07 always means he or that x02 always denotes a person.
> It has to perform local binding from each sample's input.
> Validation and Leakage
> Treat a full four-stage chain as one atomic example.
> Do not create local splits by separating T2, T3, and T4.
> Do not flatten operations from one sample and place them on opposite sides of a local split.
> All derivatives of one sample should remain together, including:
> Serialized source variants.
> Auxiliary span labels.
> Vault-selection labels.
> Antecedent labels.
> Executed compact targets.
> Program tokens.
> Augmented copies.
> The official split is constructed so related discourse families remain on one side.
> For a realistic local estimate, group strongly related chains instead of performing operation-level random splitting.
> Allowed Resources
> Participants may use:
> Released public challenge files.
> Eligible pretrained encoder-decoder checkpoints.
> Standard deep-learning frameworks.
> Standard tokenizer libraries.
> Public neural architecture source code.
> Tokenizers associated with eligible pretrained checkpoints.
> Additional special tokens learned during challenge fine-tuning.
> Neural auxiliary targets derived from released training programs.
> Constrained decoding over the published program grammar.
> Program execution for local training diagnostics.
> CPU-friendly neural ensembles.
> Disallowed Resources
> Participants may not use:
> Remote language-model APIs.
> Hidden test labels.
> Private evaluator files.
> Manual test annotation.
> External conversational labels used as additional supervision.
> External retrieval systems.
> Search engines at training or inference time.
> Teacher labels generated by an external large language model.
> Hard-coded test programs.
> sample_id as a predictive feature.
> JSON row order as a predictive feature.
> Filename order as a predictive feature.
> Submission-feedback reconstruction of hidden programs.
> Rule-based systems as the primary predictor.
> TF-IDF as the primary predictor.
> BM25 as the primary predictor.
> Nearest-neighbor target copying as the primary predictor.
> Limitations
> The public text is an abstracted discourse representation.
> Local variables intentionally remove some lexical identity.
> The benchmark therefore emphasizes:
> Referential structure.
> Elliptical compression.
> Span geometry.
> Local phrase binding.
> Discourse dependency.
> rather than encyclopedic knowledge.
> The hidden program is deterministic, but natural language can admit more than one plausible conversational compression.
> The benchmark evaluates recovery of the canonical released program, not every linguistically valid alternative.
> The Surface Reconstruction component provides graded credit when an alternate program still executes to a similar compact token sequence.
> Phrase-vault entries are deliberately short.
> The benchmark does not measure unrestricted open-vocabulary generation.
> It measures whether a model can compile a locally grounded discourse chain into a constrained executable transformation language.
> Expected Outcome
> A successful system should:
> Fine-tune efficiently on CPU.
> Understand a four-stage discourse chain.
> Track locally scoped variables.
> Distinguish explicit information from information that can be compressed.
> Locate edit spans precisely.
> Select the correct local phrase-vault entries.
> Recover antecedent dependencies.
> Generate syntactically valid programs.
> Produce programs that actually execute to the correct compact turns.
> Generalize to unseen local variable bindings and unseen discourse chains.
> The prediction objective is:
> compile each expanded discourse chain into the three-stage executable compression program for T2, T3, and T4.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Arabic Handwriting Hidden Form Ledger

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx737vt9m8mc9gw0bsafmy05x58byghx
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hitlocation's score of 0.806!

Full challenge description from page:

> Leaderboard
> (7)
> Your Submissions
> Arabic Handwriting Hidden Form Ledger
> Overview
> A handwritten form creates a small visual system: repeated words, page-level writing rhythm, stroke habits, spacing, and baseline drift appear across multiple crops from the same sheet.
> In this challenge, each case contains 24 cropped Arabic handwritten word images. Sixteen of the images come from one hidden original form: four different words, each written four times on that form. The remaining eight images are distractors from a different form: two complete four-image repeated-word groups. These distractors should be ignored.
> Your task is to fine-tune or train a model that reads the full 24-image set and returns a compact hidden-form ledger: the four four-image groups that came from the concealed source form. The challenge is deliberately not a plain OCR task. Reading the word text is useful but insufficient, because both forms contribute multiple complete repeated-word groups and the answer is the exact structured ledger.
> The prepared split is form-disjoint. Test cases are built from forms that are not used to build training cases. All samples are prepared from real scanned handwriting crops from the source dataset; no synthetic, generated, or artificially rendered handwriting is used to create the cases.
> Prediction Objective
> For each test case, identify the four repeated-word groups from the hidden original form.
> Each case has sample columns sample_0 through sample_23. Each sample column points to one handwritten word image.
> The target is a ledger string containing four groups. Each group contains four sample indices. Indices inside a group are joined with hyphens. Groups are joined with vertical bars.
> Example ledger:
> 0-4-7-13|2-5-8-11|1-6-12-16|3-9-14-21
> This example means:
> samples 0, 4, 7, and 13 are one repeated word from the hidden form;
> samples 2, 5, 8, and 11 are another repeated word from that same hidden form;
> samples 1, 6, 12, and 16 are the third repeated word from that same hidden form;
> samples 3, 9, 14, and 21 are the fourth repeated word from that same hidden form;
> the eight sample indices not listed are distractors from one different form.
> The order of groups is canonicalized by the grader, and indices inside each group are canonicalized too. A correct submission must identify the same four four-image groups.
> Dataset
> The prepared dataset lives in ./dataset/public/ and contains these files and folders:
> train/: labelled training cases and training sample images.
> test/: unlabelled test cases and test sample images.
> sample_submission.csv: submission format demonstration.
> metadata.json: split metadata.
> Inside train/, the images/ directory contains PNG files and cases.csv contains labelled case rows.
> Inside test/, the images/ directory contains PNG files and cases.csv contains unlabelled case rows.
> Input Schema
> Columns of train/cases.csv:
> id: unique case identifier.
> sample_0 through sample_23: relative paths to the 24 handwritten sample images in the case.
> ledger: target grouping ledger for the training case.
> Columns of test/cases.csv:
> id: unique case identifier.
> sample_0 through sample_23: relative paths to the 24 handwritten sample images in the case.
> Each image referenced by a sample column contains one cropped handwritten Arabic word sample. The distractors also contain complete repeated-word groups, so the task is to infer the hidden ledger rather than transcribe individual words.
> Target Schema
> The target field is named ledger.
> A valid ledger has exactly four groups. Each group has exactly four distinct integers from 0 to 23. Groups use | as the separator, and indices inside each group use - as the separator.
> Valid examples:
> 0-4-7-13|2-5-8-11|1-6-12-16|3-9-14-21
> 4-8-10-23|0-5-12-17|1-7-15-22|3-9-11-19
> Exactly sixteen unique indices must be listed. The eight omitted indices are predicted as distractors.
> Evaluation
> Submissions are scored with exact ledger accuracy after whitespace removal and canonicalization of group order.
> A row receives credit only when all four four-image hidden-form groups are exactly correct. Partial grouping, correct word recognition with wrong form membership, or listing a distractor inside a true group receives no credit for that row.
> The final score is the fraction of test cases with a fully correct ledger. Higher is better.
> Submission
> Write ./working/submission.csv with exactly one row per test case plus a header. The file has two columns:
> id: case identifier from sample_submission.csv.
> ledger: predicted hidden-form grouping ledger.
> The header line is id,ledger.
> A valid data row looks like this:
> test_case_000001,0-4-7-13|2-5-8-11|1-6-12-16|3-9-14-21
> Requirements enforced by the grader:
> exactly one row per test id, no duplicates and none missing;
> the file must contain id and ledger columns;
> each ledger should contain exactly four groups;
> each group should contain exactly four sample indices;
> valid sample indices are 0 through 23;
> whitespace is ignored;
> malformed or blank ledger values are accepted as submitted values but score as incorrect unless they canonicalize to the expected ledger.
> Expected Methods
> The challenge is intended for supervised fine-tuning or compact from-scratch training on case-level visual reasoning. Strong solutions should process the 24 samples together and produce the structured ledger directly or through learned intermediate case representations.
> Approaches that fit naturally include:
> fine-tuning an open multimodal model to map the full case to a ledger string;
> training a compact image encoder with a case-level structured decoder;
> learning sample embeddings jointly with a ledger-construction head;
> using a small assignment or decoding step after the model predicts which samples belong to the hidden form;
> training from scratch on the provided public training cases when the model remains CPU-friendly;
> tuning thresholds and decoding choices only on held-out splits made from the public training cases.
> What Not To Use
> No template matching. Do not compare test samples to train samples and copy group assignments from visually nearest examples.
> No nearest-neighbor retrieval as the primary prediction method. This includes raw pixels, perceptual hashes, handcrafted descriptors, or embedding lookup used to identify exact or near-exact samples.
> No manual reading, manual grouping, or manual labelling of test examples.
> No external OCR, writer-identification, handwriting-recognition, or closed visual-recognition services.
> No synthetic, generated, or artificially rendered handwriting samples may be used to create extra training data.
> No non-public data. Fit and tune only on the provided public training files.
> No hardcoded predictions. Do not embed test-id-to-output maps.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Torlak Nominal Inheritance Profiles

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7714w0kxv0642f9xcfr48zxd8c1ba6
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat data47's score of 0.831!

Full challenge description from page:

> Leaderboard
> (5)
> Your Submissions
> Torlak Nominal Inheritance Profiles
> Overview
> Dialect lexicography must distinguish two independent properties of a deverbal nominal: whether its attested form has a direct standard-language counterpart and whether its source verb is perfective. Treating those decisions separately can create inconsistent dictionary entries.
> Fine-tune a multilingual language model on authentic Timok Torlak transcript windows to recover each marked nominalisation's two-axis linguistic inheritance profile:
> local_imperfective: no straightforward standard BCMS form; imperfective or biaspectual base verb.
> local_perfective: no straightforward standard BCMS form; perfective base verb.
> standard_imperfective: corresponds to a standard BCMS form; imperfective or biaspectual base verb.
> standard_perfective: corresponds to a standard BCMS form; perfective base verb.
> The benchmark is intentionally compact so genuine full-parameter fine-tuning remains practical on CPU. The 440 training utterances still cover 129 normalized lemma groups, varied speakers and contexts, both nominalisation types, and all four profiles. The broader 166-row test set covers 44 entirely unseen lemma groups, giving wider hidden coverage and reducing the effect of any single test example. Effective fine-tuning must transfer orthographic, morphological, aspectual, and contextual cues to unseen lexemes rather than memorize training vocabulary.
> Dataset
> The source authors manually screened 2,979 extracted tokens and fully annotated 606 characteristic Timok Torlak deverbal nominalisations. No generated or augmented utterance is used.
> File descriptions
> train.csv: 440 labeled spoken-context examples from 129 lemma groups.
> test.csv: 166 examples from 44 held-out normalized lemmas.
> sample_submission.csv: a randomized valid example submission.
> Column descriptions
> id: an opaque row identifier.
> lexeme_group: an opaque grouping key for development folds; all forms of one normalized lemma share a key.
> nominal_class: nje_ce for the -nje/-će class or cija for the -cija class.
> left_context: semi-orthographic transcript before the nominalisation.
> token: the attested nominalisation form, including source prosody where present.
> right_context: transcript after the nominalisation.
> inheritance_profile: the joint standard-correspondence/aspect label; present only in training and submissions.
> Evaluation
> Each submitted profile combines two linguistic decisions. The evaluation balances recovery of both axes and rewards a fully consistent joint profile:
> score = 0.40 * correspondence_balance \
> + 0.40 * aspect_balance \
> + 0.20 * joint_profile_consistency
> correspondence_balance and aspect_balance give equal weight to both states on their respective axes. joint_profile_consistency requires both axes to be correct on the same token. The final score is bounded to [0, 1]; higher is better.
> For either binary axis, let F1_0 and F1_1 be the standard F1 scores for its two states, where F1 = 2 precision recall / (precision + recall) and a zero denominator gives 0. The component is:
> axis_balance = (F1_0 + F1_1) / 2
> Therefore, correspondence_balance applies this calculation to local versus standard correspondence, while aspect_balance applies it to imperfective versus perfective aspect. The joint component is:
> joint_profile_consistency = number_of_exact_profile_matches / number_of_test_rows
> The hidden set is normalized-lemma-disjoint. Orthographic, prosodic, inflectional, and contextual variants of a lemma cannot cross the train/test boundary.
> Submission
> Submit a CSV containing:
> id: every test identifier exactly once.
> inheritance_profile: one of the four published profiles.
> Example using real test IDs:
> id,inheritance_profile
> tnp_8b15eeb755384aa2,standard_imperfective
> tnp_34a193103e1684c5,local_imperfective
> Requirements
> Include exactly the columns id,inheritance_profile in that order.
> Include exactly 166 rows, one for every test ID, with no duplicate IDs.
> Use only the four exact profile strings above.
> Do not submit missing or empty values.
> What Not to Use
> Do not reverse-map opaque IDs or group hashes to recover hidden annotations.
> Do not search exact test contexts or use a precomputed label lookup from external copies.
> Do not manually label test rows.
> Do not generate synthetic or model-authored training examples.
> Start from general-purpose pretrained multilingual weights and fine-tune model parameters on the supplied training rows during the submitted run.
> The intended solution performs genuine parameter updates; inference-only prompting, fixed rules, and cached label lookup are not substitutes for fine-tuning.
> Do not load a precomputed external checkpoint that was already trained or tuned specifically on these labeled examples.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Recognising a Writer Behind an Assigned Persona

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c8yyqyrgmser6544n8nqw5h8bwcem
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat devaton's score of 0.672!

Full challenge description from page:

> Leaderboard
> (5)
> Your Submissions
> Recognising a Writer Behind an Assigned Persona
> What you are building
> These texts were written under instruction. Crowd writers were each given prompts and, for many of the texts, told to sound like someone else - to imitate a different gender, an older or younger person, or another writing style. Your job is to see past that: given short texts by anonymous people, decide which two came from the same hand even when one or both was deliberately written not to sound like its author. You work from the writing alone, never from what it is about.
> This is genuinely a training problem, not a lookup. A pretrained sentence encoder used as-is scores only about 0.36 MRR here, WORSE than a plain character n-gram baseline (about 0.43), because an off-the-shelf encoder matches topic - and here topic and even the stated persona are misleading. What survives an assigned persona is the deeper idiolect - punctuation rhythm, syntax, habitual phrasing - and you have to train a model to represent it.
> The deliverable is a trained matching model. You are expected to learn a text embedding under which two texts by the same author land close together and texts by different authors land apart - either by fine-tuning a pretrained (multilingual) text encoder on the same-author supervision with a contrastive / metric-learning objective, or by training such an embedding from scratch on the provided data. The score comes from the training you do.
> The texts are in Russian.
> Concretely, at test time each reference text comes with a candidate list of 40 texts. Of those 40, exactly one is the true match - a different text by the very same author as the reference - and the other 39 are decoys, texts by other authors (40 = 1 true match + 39 decoys). The reference text itself is never one of the 40 candidates. You assign a score to each of the 40 candidates, and you are graded on where the single true match lands in your ordering.
> Where the difficulty comes from
> You are tested on authors you never trained on. Authors are partitioned between train and test, so no author contributes texts to both. Memorising "these texts go together" earns nothing on the test set; you must learn, in general, what makes two texts share a hand and carry it to writers you have never seen. In the training data every text is tagged with its author's code - that is your supervision, and the thing to train on.
> Different subjects, sometimes a faked persona. Each author's texts were written to different prompts, and a writer was sometimes asked to imitate another gender, age, or style. So topic and stated identity are misleading; only the idiolect ties an author's texts together. A topic-matching model is actively led astray, which is why the raw encoder scores below a character baseline.
> The impostors are deliberate look-alikes. The 39 decoys are not random. For each reference they are the other-author texts whose surface similarity to the reference is closest to the true match's, measured on both whole words and character fragments, so every candidate sits in the same surface-similarity band as the answer. A ranker that leans on shared wording cannot tell the planted decoys from the match.
> Inputs
> Everything lives under dataset/public/.
> train.csv with text_id, author_id, text: the labelled pool. Texts sharing an author_id were written by the same person; this is the signal you train on.
> test.csv with text_id, text: the texts you are scored on, with the author label withheld.
> test_pairs.csv with query_id, candidate_id: for every reference, its 40 candidate texts (all ids refer to rows of test.csv).
> sample_submission.csv: a ready-to-edit submission covering every pair, filled with a chance-level score.
> How you are scored
> The metric is mean reciprocal rank (MRR). For one reference, sort its 40 candidates by your score, find the rank of the single correct text, and take one over that rank; the challenge score averages this across all references.
> MRR = mean over references of 1 / rank(correct text)
> Ties are resolved to the average reciprocal rank across the tied block, so a flat, all-equal submission lands exactly on chance. With 40 candidates chance is about 0.107 and a perfect ranking is 1.00.
> Output format
> Write ./working/submission.csv with three columns and nothing else:
> query_id,candidate_id,score txt_5b1c128f44cc,txt_0057ac0cb099,0.02 txt_5b1c128f44cc,txt_1245d2af2314,0.88
> Emit one row for each (query_id, candidate_id) in test_pairs.csv, no more and no fewer. Dropping, repeating, or inventing a pair is rejected.
> Any finite real number is a valid score; only the order within a reference matters.
> The safe route is to load sample_submission.csv, overwrite the score column, and save with index=False.
> Measured difficulty and shortcuts
> There are 9,569 training texts and 3,861 test texts over 972 held-out authors (2,380 authors are used for training). The test texts form the candidate pool; 1,944 of them serve as references (up to two per test author), each with 40 candidates, so test_pairs.csv has 1,944 x 40 = 77,760 rows. Measured on this split:
> Constant / chance: 0.107
> Candidate frequency: 0.076
> Length proximity to the query: 0.072
> Word n-gram overlap: 0.393
> Pretrained sentence encoder, cosine, no training: 0.360
> Character n-gram overlap (stylometric baseline): 0.434
> Fine-tuned encoder (contrastive, same-author pairs): 0.563
> Candidate length carries no signal: every candidate is drawn from a band around the true match's length, so ranking by length proximity to the query sits at chance (0.072). The telling numbers are the middle ones: an untrained semantic encoder (0.360) does no better than character overlap (0.434), and in fact worse, because it reaches for topic. Fine-tuning the same encoder for style lifts it to 0.563, and training an embedding from scratch is a valid alternative route. The climb past the ~0.43 surface floor is exactly what training for authorship buys.
> Runtime environment
> Runs are scored on CPU with no GPU, with 62 GB RAM and a 90-minute limit. Package installation is not allowed; the preinstalled stack (numpy, scipy, pandas, scikit-learn, pytorch, transformers, sentence-transformers) is available, and a compact multilingual text encoder may be downloaded and fine-tuned on CPU within the budget, or an embedding may be trained from scratch. The scorer grades only the submitted predictions and does not inspect your method, so this is guidance rather than an automated filter; but the candidates are surface-matched to the answer, and an untrained encoder scores below a character baseline, so a trained representation is what separates a strong solution. Your code must read from ./dataset/public/ and write ./working/submission.csv.
> Source and collection
> The texts come from a published Russian author-profiling corpus gathered on a crowdsourcing platform under a documented collection protocol. In that protocol the same writers were asked to produce texts under several deliberate personas - writing as their own age and as an older or younger person, in their own gender and pretending to be the opposite gender, and in their habitual style and while distorting it on behalf of someone else. That imitation-by-instruction design is what makes the underlying resource purpose-built for same-author matching under assigned personas, rather than a repurposing of scraped or single-persona text. For this challenge the corpus is heavily re-derived into an author-disjoint matching split that is not distributed anywhere in this form: demographic and imitation labels are dropped, author identity is replaced with opaque salted codes, texts are re-partitioned so test authors never appear in training, and only the raw text and its salted author code are kept. The original source is intentionally not named here, and the released split cannot be reconstructed from any public download.
> What not to use
> Do not try to identify the author from any outside archive. The texts are anonymous crowd writing and the author codes are opaque on purpose. Work from the text.
> Do not hardcode outputs or rank by candidate position, length, or global frequency; those sit at or below chance and sidestep the learning the task is about.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Safety Recall Compatibility Assignment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bqfamrwc7xbr351fdx9edgh8bwa0t
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.674

Full challenge description from page:

> Safety Recall Compatibility Assignment
> Overview
> Safety reviewers often receive a defect description before the corresponding operational consequence and service action have been attached to the correct case. This becomes difficult when several cases concern the same subsystem and use nearly identical terminology.
> Each packet in this challenge contains two defect narratives and four candidate consequence-and-service cards. Exactly two cards belong to the two defects, one card per defect; the other two are plausible decoys. Your task is to assign the correct card to each defect while respecting the one-to-one constraint.
> Strong solutions should adapt a text model to score defect-card compatibility and decode the best valid assignment. Keyword overlap alone is unreliable because all four cards are selected from closely related failure mechanisms.
> Modeling Objective
> This is a fine-tuning benchmark for compact pretrained text encoders. Use the labeled packets to adapt model parameters for scalar defect-card compatibility, then decode the highest-scoring one-to-one assignment. The required outputs are local candidate indices; the task does not require generating a text sequence.
> Assignment Semantics
> Candidate letters are local to each packet:
> defect_1_choice is the letter of the card compatible with defect_1_text.
> defect_2_choice is the letter of the card compatible with defect_2_text.
> Allowed letters are A, B, C, and D.
> The two predicted letters must be different.
> The two unused letters are the packet's decoy set.
> Evaluation
> The score is maximized and ranges from 0 to 1. Submissions with unknown letters or duplicate choices within a packet are rejected.
> For each packet:
> row_score = 0.55  *pair_accuracy + 0.15*  decoy_set_accuracy + 0.30 * exact_packet
> pair_accuracy is the fraction of the two defect assignments that are correct. decoy_set_accuracy is 1 when the two unused letters exactly match the hidden decoy set, regardless of order, and 0 otherwise. exact_packet is 1 only when both defect assignments are correct.
> The final score is the mean row_score over all test packets.
> Dataset
> Public files:
> | File | Rows | Description |
> |---|---:|---|
> | train.csv | 2000 | Labeled compatibility packets. |
> | test.csv | 1400 | Held-out packets without assignment labels. |
> | sample_submission.csv | 1400 | Valid submission template. |
> train.csv columns:
> | Column | Type | Meaning |
> |---|---|---|
> | packet_id | string | Anonymous packet identifier. |
> | defect_1_text, defect_2_text | string | Sanitized defect narratives. |
> | candidate_A_effect through candidate_D_effect | string | Candidate operational-consequence text. |
> | candidate_A_service through candidate_D_service | string | Candidate service-action text. |
> | defect_1_choice, defect_2_choice | string | Gold local candidate letters. |
> test.csv has the same feature columns but omits defect_1_choice and defect_2_choice.
> The held-out split uses later cases than the training split. It contains 5,600 unique underlying cases, and every defect narrative and candidate card appears in exactly one packet. Underlying cases are disjoint across train and test. Names, product identifiers, campaign numbers, dates, contact details, URLs, and source ordering are not included.
> Submission
> Submit exactly these columns, in this order:
> packet_id,defect_1_choice,defect_2_choice
> packet_0123456789abcdef1234,B,D
> packet_fedcba9876543210abcd,A,C
> Requirements:
> Include exactly one row for every test packet_id.
> Use only A, B, C, or D.
> Use two different letters in every row.
> Do not include extra columns.
> Save the file as ./working/submission.csv.
> Restrictions
> Use only the released public files and generally available modeling tools. Do not use external record lookup, source-row reconstruction, hidden files, private answers, row order, file order, hashes, or grader internals. Fine-tuning compact text encoders, public-train retrieval, compatibility modeling, constrained assignment, and ensembling are allowed.

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Paired Biography Generation from Entangled Records

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70xkfr4409eq4hg2qpavnwb98c92e9
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 17.589

Full challenge description from page:

> Overview
>
> Paired Biography Generation from Entangled Records is a hard CPU sequence-to-sequence challenge about separating mixed person records and turning them into two grounded biographical narratives.
>
> Each example originates from two historical English-language biographical records collected from a September 2015 snapshot of a large collaborative encyclopedia. The source material contains structured person attributes aligned with editor-written introductory prose. The challenge transforms those aligned records into a new paired prediction problem: the two people are placed inside one shared record bundle, their ordinary schema labels are concealed, and unrelated fragments are mixed into the same bundle.
>
> The practical setting resembles record fusion in archival, publishing, and knowledge-management systems. A downstream model may receive fragments from several profiles after schema migration, aggregation, or partial provenance loss. The model must determine which information belongs to which person before it can write a clean narrative.
>
> For every test example, the model receives:
>
> Two sample-local profile aliases.
> Two short anchor passages.
> One shared pool of interleaved attribute fragments.
> Opaque attribute codes.
> One schema dialect identifier.
> Relevant fragments for Profile P1.
> Relevant fragments for Profile P2.
> A small number of cross-profile bridge fragments.
> Plausible unclaimed fragments that belong to neither target profile.
>
> The model must emit one structured sequence containing:
>
> An ownership decision for every fragment.
> An ordered realization route for P1.
> An ordered realization route for P2.
> The recovered bridge set.
> A generated narrative for P1.
> A generated narrative for P2.
>
> This is not ordinary table-to-text generation.
>
> The input does not reveal a complete table for either profile. Before generation can succeed, the model must infer a latent partition of the shared fragment pool.
>
> A successful system must jointly solve:
>
> Latent record ownership.
> Opaque schema induction.
> Cross-profile relation detection.
> Distractor rejection.
> Content admission.
> Content ordering.
> Grounded sequence generation.
> Cross-profile contamination control.
>
> The challenge is designed for compact pretrained encoder-decoder models that can be fine-tuned on CPU.
>
> Core Prediction Problem
>
> Every sample contains two target profiles:
>
> P1
> P2
>
> Their original person names are replaced by sample-local aliases inside the released challenge material.
>
> The aliases identify the two narrative channels but do not reveal the underlying real-world identity.
>
> A sample may look conceptually like:
>
> P1 anchor:
>
> P1 was an English writer and educator associated with ...
>
> P2 anchor:
>
> P2 was a Scottish physician who later worked in ...
>
> The shared fragment pool may contain entries such as:
>
> F01 | K17 | 12 march 1871
>
> F02 | K41 | university of edinburgh
>
> F03 | K09 | novelist
>
> F04 | K23 | london
>
> F05 | K17 | 4 october 1842
>
> F06 | K55 | royal infirmary
>
> F07 | K09 | physician
>
> F08 | K31 | cambridge
>
> Some of these fragments belong to P1.
>
> Some belong to P2.
>
> Some are bridge fragments that connect both profiles through a shared institution, office, location, organization, predecessor-successor relation, or another relation supported by the source records.
>
> Some are unclaimed fragments.
>
> The input does not directly label those roles.
>
> The model must infer them.
>
> Why Ownership Is Latent
>
> The challenge deliberately removes the standard assumption that every structured value arrives inside the correct entity record.
>
> The fragment pool is shared.
>
> A fragment has:
>
> A local fragment ID.
> An opaque code.
> A textual value.
>
> It does not contain a public profile_id field.
>
> Therefore:
>
> F07 | K09 | physician
>
> does not tell the model whether it belongs to P1, P2, both through a bridge relation, or neither.
>
> Ownership must be inferred from the complete sample.
>
> Useful evidence can come from:
>
> The anchor passages.
> Other fragments already associated semantically with one profile.
> Learned behavior of the opaque code under the active dialect.
> Compatibility between attribute values.
> Repeated structural patterns learned from training examples.
> Cross-fragment coherence.
> The way relevant facts are realized in target narratives.
>
> The target is therefore not a shuffled pair of already separated tables.
>
> The separation itself is part of the prediction problem.
>
> Opaque Schema Dialects
>
> Every fragment contains a code such as:
>
> K03
> K11
> K24
> K37
> K52
>
> The code replaces the ordinary semantic label of the underlying attribute.
>
> Code semantics are not globally fixed.
>
> Every sample also contains one dialect identifier:
>
> D01
> D02
> D03
> D04
>
> A code can represent different semantic roles in different dialects.
>
> For example, conceptually:
>
> K17 under D01 may behave like a date-bearing attribute.
> K17 under D03 may behave like an institutional attribute.
>
> The exact mapping is not published.
>
> It must be learned from released training examples.
>
> This prevents the task from collapsing into direct reading of transparent field names.
>
> The dialect is public.
>
> The code meaning under that dialect is latent.
>
> Anchor Passages
>
> Each profile receives one short anchor passage.
>
> The anchors provide enough local evidence to make ownership learnable without external retrieval, but they are intentionally incomplete.
>
> An anchor may express:
>
> A broad profession.
> A geographic association.
> A role family.
> An institution.
> A period.
> A nationality-like descriptor.
> A short identifying phrase.
>
> Anchors do not contain the complete target narrative.
>
> They also do not enumerate every relevant fragment.
>
> The model must combine anchor evidence with the shared fragment pool.
>
> Fragment Roles
>
> Every fragment has exactly one gold role:
>
> P1
> P2
> BRIDGE
> VOID
> P1
>
> The fragment belongs to Profile P1 and is eligible for P1's narrative route.
>
> P2
>
> The fragment belongs to Profile P2 and is eligible for P2's narrative route.
>
> BRIDGE
>
> The fragment encodes information that jointly links the two profiles.
>
> A bridge can represent a shared or relational fact such as:
>
> A common institution.
> A common location.
> The same office lineage.
> A predecessor-successor relation.
> A shared organization.
> A shared team or ensemble.
> Another relation present in the released evidence.
>
> Bridge fragments are scored separately because they are neither ordinary P1 fragments nor ordinary P2 fragments.
>
> VOID
>
> The fragment is a plausible attribute capsule but does not belong to either target profile in the current sample.
>
> VOID fragments are not random noise.
>
> They are selected to resemble useful fragments in:
>
> Length.
> Surface form.
> Semantic type.
> Date shape.
> Name shape.
> Institutional form.
> Geographic form.
>
> A model therefore cannot solve the task by rejecting obviously malformed text.
>
> Narrative Admission
>
> Not every owned fragment must appear in the final narrative.
>
> For each profile, only a subset of its owned fragments forms the gold realization route.
>
> This distinction is important.
>
> The model must learn both:
>
> Which profile owns the fragment.
> Whether that fragment is admitted into the narrative.
>
> An owned fragment may remain unspoken because the reference narrative prioritizes other information.
>
> The challenge therefore separates record membership from narrative selection.
>
> Realization Routes
>
> Each profile has one ordered realization route.
>
> A route is a sequence of fragment IDs.
>
> For example:
>
> P1 route:
>
> F03 F11 F04 F16
>
> P2 route:
>
> F07 F02 F05 F14
>
> The route represents the ordered factual cadence of the target narrative.
>
> It is not simply the physical order of fragments in the input.
>
> The fragment pool is deliberately permuted.
>
> A model must infer:
>
> Which fragments are narratively admitted.
> Which profile each admitted fragment belongs to.
> The order in which those fragments should be realized.
>
> The route is scored directly.
>
> It is not inferred by the evaluator from the generated text.
>
> Generated Narratives
>
> The model must also generate two short narratives.
>
> The narratives use the aliases P1 and P2 rather than the original source names.
>
> The target text is grounded in the released anchors and admitted fragments.
>
> A correct narrative should:
>
> Preserve the correct profile channel.
> Realize important admitted values.
> Follow the learned factual cadence.
> Use grammatical English.
> Avoid importing values owned by the other profile.
> Avoid importing VOID values.
> Avoid unsupported external facts.
> Remain concise.
>
> The task does not require reproducing an entire encyclopedia article.
>
> Targets are compact profile narratives suitable for CPU-friendly sequence-to-sequence fine-tuning.
>
> Prediction Sequence
>
> Training examples contain one serialized target_sequence.
>
> Test examples omit it.
>
> The target sequence uses the following envelope:
>
> <OWN> ... </OWN> <R1> ... </R1> <R2> ... </R2> <BR> ... </BR> <T1> ... </T1> <T2> ... </T2>
>
> Ownership block
>
> The ownership block contains one assignment for every released fragment.
>
> Example:
>
> <OWN> F01=P1 F02=VOID F03=P2 F04=BRIDGE ... </OWN>
>
> Every test fragment must appear exactly once in the ownership block.
>
> Valid labels are:
>
> P1
> P2
> BRIDGE
> VOID
> P1 route
>
> Example:
>
> <R1> F07 F03 F12 F01 </R1>
>
> P2 route
>
> Example:
>
> <R2> F09 F05 F14 F11 </R2>
>
> Bridge block
>
> Example:
>
> <BR> F04 F16 </BR>
>
> The bridge block is an unordered inventory.
>
> P1 narrative
>
> Example:
>
> <T1> P1 was a ... </T1>
>
> P2 narrative
>
> Example:
>
> <T2> P2 was a ... </T2>
>
> The full prediction is one sequence.
>
> This makes the task compatible with ordinary encoder-decoder fine-tuning.
>
> Challenge Type
>
> This is a Fine-Tuning challenge.
>
> Pretrained sequence-to-sequence models are allowed.
>
> Eligible model families include compact pretrained:
>
> Encoder-decoder transformers.
> Text-to-text transformers.
> Denoising encoder-decoder models.
> Small multilingual encoder-decoder models when they can process English efficiently.
> Copy-aware sequence generators.
> Pointer-augmented encoder-decoder systems.
>
> Participants may also train sequence-to-sequence models from scratch, but pretrained encoder-decoder initialization is permitted.
>
> The intended solution is machine learning.
>
> ML-Only Requirement
>
> Final predictions must be produced by a learned predictive model trained or fine-tuned using the released training set.
>
> Allowed components can include:
>
> Neural sequence encoders.
> Neural sequence decoders.
> Learned fragment classifiers.
> Learned ownership heads.
> Learned route heads.
> Learned copy mechanisms.
> Learned rerankers.
> Learned auxiliary objectives.
> Constrained decoding applied to learned model scores.
>
> The following are not eligible as complete predictive systems:
>
> Hand-written rules.
> Deterministic templates as the primary predictor.
> TF-IDF-only systems.
> BM25-only systems.
> Nearest-neighbor-only lookup.
> Hard-coded mappings from fragment surface forms to outputs.
> Manually constructed external biography dictionaries.
>
> Deterministic post-processing is allowed for syntax repair, duplicate removal, or enforcing the published output grammar after a learned model has produced scores or tokens.
>
> Compute
>
> The execution environment provides:
>
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
>
> The task is designed around compact sequence-to-sequence models and bounded example lengths.
>
> Participants should prefer:
>
> Small pretrained encoder-decoder checkpoints.
> Short maximum input lengths.
> Short maximum output lengths.
> Gradient accumulation when needed.
> Frozen or partially frozen encoders when useful.
> Low-rank adaptation if supported by the chosen implementation.
> CPU-efficient tokenization.
> Cached preprocessing.
> Compact beam search.
> Mixed integer or exact decoding only for the small structural blocks.
>
> Large language models are not required.
>
> External API inference is not allowed.
>
> Released Dataset
>
> The public package contains:
>
> train.jsonl
> test.jsonl
> sample_submission.csv
>
> There is no official validation file.
>
> Participants should create local validation splits from train.jsonl.
>
> train.jsonl
>
> Each line contains one JSON object.
>
> sample_id
>
> Type: string.
>
> Unique identifier used only for alignment.
>
> Do not use the identifier itself as a predictive feature.
>
> dialect
>
> Type: string.
>
> One of:
>
> D01
> D02
> D03
> D04
>
> The dialect determines the latent semantics of opaque K-codes.
>
> anchors
>
> Type: object.
>
> Contains:
>
> P1
> P2
>
> Each value is a short text passage.
>
> Example:
>
> {"P1":"P1 was an English writer associated with ...","P2":"P2 was a Scottish physician who ... "}
>
> fragments
>
> Type: list of objects.
>
> Each fragment contains:
>
> fragment_id
> code
> value
>
> Example:
>
> {"fragment_id":"F07","code":"K09","value":"physician"}
>
> Fragment IDs are sample-local.
>
> F07 in one sample has no relation to F07 in another sample.
>
> target_sequence
>
> Training only.
>
> Type: string.
>
> Contains the complete serialized target:
>
> Ownership block.
> P1 route.
> P2 route.
> Bridge inventory.
> P1 narrative.
> P2 narrative.
> test.jsonl
>
> Contains the same public input fields as train.jsonl except:
>
> target_sequence is omitted.
>
> The public test records do not expose:
>
> Gold fragment ownership.
> Gold narrative admission.
> Gold realization routes.
> Gold bridge sets.
> Gold generated narratives.
> Original source article identifiers.
> Original source titles.
> Original source URLs.
> Original schema labels.
> Source partition identifiers.
> Construction donor identifiers.
> Preparation hashes.
> Dataset Scale
>
> The challenge release contains approximately:
>
> 16,000 training pairs.
> 2,400 test pairs.
>
> Each pair is intentionally compact.
>
> A typical sample contains:
>
> Two anchors.
> Roughly 16 to 24 mixed fragments.
> Two short output routes.
> Zero to a few bridge fragments.
> Two compact target narratives.
>
> The exact fragment count can vary across samples.
>
> Public Data Context
>
> The underlying language material comes from historical English-language biography pages and their aligned structured person records.
>
> The source snapshot was collected in September 2015 from a large collaborative encyclopedia.
>
> The challenge does not expose the original article identity.
>
> Instead, the public transformation:
>
> Replaces the original person names with sample-local aliases.
> Conceals ordinary schema labels behind opaque codes.
> Mixes two records into one fragment pool.
> Adds plausible unclaimed fragments.
> Introduces explicit bridge cases.
> Separates ownership from narrative admission.
> Requires two coordinated narrative outputs.
>
> The challenge labels are therefore not native annotations copied directly from the source corpus.
>
> They are derived targets specific to this prediction problem.
>
> Train/Test Separation
>
> The official split is designed to reduce direct memorization.
>
> The preparation process prevents the same source biography from appearing in both released train and hidden test examples.
>
> The split also avoids reusing exact paired profile combinations across partitions.
>
> Participants should therefore expect test examples with:
>
> New profile pairings.
> New local fragment permutations.
> New distractor mixtures.
> New ownership combinations.
> New route combinations.
>
> Exact sample-local aliases and fragment IDs never carry global semantics.
>
> Research Positioning
>
> Conventional structured-to-text benchmarks normally begin with a record whose rows already belong to the entity being verbalized.
>
> This challenge removes that assumption.
>
> The model is evaluated on an intermediate latent structure that must be recovered before generation:
>
> mixed fragments -> ownership -> narrative admission -> realization route -> paired text
>
> The key distinction is not merely that two tables are concatenated.
>
> There are no public tables for P1 and P2.
>
> Only the entangled fragment pool is public.
>
> The challenge additionally distinguishes:
>
> Record ownership from narrative admission.
> Entity-local facts from cross-profile bridge facts.
> Schema meaning from visible K-code identity.
> Surface fluency from cross-profile factual purity.
>
> A system can therefore produce fluent text and still score poorly if it:
>
> Assigns fragments to the wrong person.
> Selects the wrong owned fragments for narration.
> Misses bridge fragments.
> Realizes the right values in the wrong profile.
> Produces the right fragment set in the wrong factual cadence.
>
> The evaluation treats these failures separately.
>
> Submission Format
>
> The submission contains exactly two columns:
>
> sample_id
> prediction
>
> Use sample_submission.csv exactly.
>
> The prediction value must contain the complete serialized output envelope:
>
> <OWN> ... </OWN> <R1> ... </R1> <R2> ... </R2> <BR> ... </BR> <T1> ... </T1> <T2> ... </T2>
>
> Example:
>
> sample_id,prediction
>
> PBR_example,"<OWN> F01=P1 F02=P2 F03=VOID F04=BRIDGE </OWN> <R1> F01 </R1> <R2> F02 </R2> <BR> F04 </BR> <T1> P1 was a writer. </T1> <T2> P2 was a physician. </T2>"
>
> The exact set of expected fragment IDs is sample-dependent and is available in test.jsonl.
>
> Evaluation
>
> Submissions are evaluated with the Paired Entanglement Generation Score from 0.01 to 100.
>
> Higher is better.
>
> The metric combines six published components:
>
> Ownership Macro F1.
> Route Fidelity.
> Bridge F1.
> Grounded Value Coverage.
> Cross-Profile Purity.
> Narrative Similarity.
>
> A perfect submission receives exactly 100.
>
> There are no hidden metric components.
>
> Ownership Macro F1
>
> For every fragment in every test sample, compare the predicted ownership label with the gold label.
>
> The four labels are:
>
> P1
> P2
> BRIDGE
> VOID
>
> For each class c, compute:
>
> Precision_c = TP_c / (TP_c + FP_c)
>
> Recall_c = TP_c / (TP_c + FN_c)
>
> F1_c = 0 when both precision and recall cannot be defined from any correct prediction.
>
> Otherwise:
>
> F1_c = 2 Precision_c Recall_c / (Precision_c + Recall_c)
>
> Ownership Macro F1 is the arithmetic mean across the four class F1 values.
>
> This component prevents the large VOID class from dominating evaluation.
>
> Let:
>
> O = OwnershipMacroF1
>
> Route Fidelity
>
> Each profile has one gold ordered route.
>
> Route quality is measured using both set recovery and order recovery.
>
> For one profile:
>
> RouteSetF1 = 2 * |P ∩ G| / (|P| + |G|)
>
> where:
>
> P is the unique predicted route set.
> G is the gold route set.
>
> Order recovery is:
>
> RouteLCS = LCS(predicted_route, gold_route) / |gold_route|
>
> If the gold route is empty, the profile receives full order credit only when the predicted route is also empty.
>
> For one profile:
>
> ProfileRoute = sqrt(RouteSetF1 * RouteLCS)
>
> The sample route score is the mean of the P1 and P2 profile route scores.
>
> Route Fidelity is the arithmetic mean across test samples.
>
> Let:
>
> R = RouteFidelity
>
> Duplicates are ignored for set membership but remain present when computing LCS, so repeated fragment IDs do not provide an advantage.
>
> Bridge F1
>
> Ignore order in the <BR> block.
>
> For each sample, compare the unique predicted bridge set with the gold bridge set.
>
> BridgeF1 = 2 * |P ∩ G| / (|P| + |G|)
>
> If both sets are empty:
>
> BridgeF1 = 1
>
> Bridge F1 is averaged across test samples.
>
> Let:
>
> B = BridgeF1
>
> Grounded Value Coverage
>
> This component checks whether values attached to the gold realization routes actually land in the correct generated narrative.
>
> For each gold route fragment:
>
> Normalize its released fragment value.
> Normalize the generated narrative for the corresponding profile.
> Compute token coverage of the fragment value inside that narrative.
>
> For a fragment with normalized token multiset V and generated token multiset T:
>
> Coverage(fragment) = |V ∩ T| / |V|
>
> Multiset intersection is used.
>
> Values that normalize to zero tokens are ignored.
>
> The profile score is the arithmetic mean across its gold route fragments.
>
> The sample score is the mean of available P1 and P2 profile scores.
>
> Grounded Value Coverage is averaged across samples.
>
> Let:
>
> G = GroundedValueCoverage
>
> This component rewards faithful realization without requiring an exact surface string match.
>
> Cross-Profile Purity
>
> A narrative should not absorb values owned by the opposite profile or VOID fragments.
>
> For P1, construct a contamination inventory from:
>
> Gold P2-owned fragments.
> Gold VOID fragments.
>
> BRIDGE fragments are excluded from contamination because they can legitimately connect both profiles.
>
> Normalize the contamination values and the generated P1 narrative.
>
> Count contamination tokens that appear in the generated narrative.
>
> Let:
>
> LeakRate_P1 = leaked contamination tokens / total contamination tokens
>
> Then:
>
> Purity_P1 = 1 - LeakRate_P1
>
> Compute P2 symmetrically.
>
> The sample purity score is:
>
> (Purity_P1 + Purity_P2) / 2
>
> Cross-Profile Purity is the arithmetic mean across samples.
>
> Let:
>
> C = CrossProfilePurity
>
> The value is clipped to [0, 1].
>
> Narrative Similarity
>
> Generated text is also compared with the gold target narratives.
>
> Two complementary sequence measures are used.
>
> Token F1
>
> For each profile, normalize text into tokens.
>
> Compute multiset token precision and recall against the gold narrative.
>
> Then compute token F1.
>
> Sequence LCS
>
> For each profile:
>
> TextLCS = LCS(predicted_tokens, gold_tokens) / |gold_tokens|
>
> For one profile:
>
> NarrativeProfile = sqrt(TokenF1 * TextLCS)
>
> Average P1 and P2.
>
> Then average across samples.
>
> Let:
>
> N = NarrativeSimilarity
>
> This component rewards both lexical recovery and coherent token ordering.
>
> Final Score
>
> First define the structural core:
>
> Structural = (O R B)^(1/3)
>
> Then define the grounded generation core:
>
> Generation = (G C N)^(1/3)
>
> The final score is:
>
> Paired Entanglement Generation Score = 100 Structural^1.20 Generation^0.80
>
> The result is clipped to:
>
> [0.01, 100]
>
> A perfect prediction has:
>
> O = 1
>
> R = 1
>
> B = 1
>
> G = 1
>
> C = 1
>
> N = 1
>
> Therefore:
>
> Structural = 1
>
> Generation = 1
>
> and:
>
> Final Score = 100
>
> The structural exponent is deliberately stronger because ownership recovery and route reconstruction define the central latent problem.
>
> A fluent generator cannot receive a high score while ignoring the entangled record structure.
>
> Likewise, a model cannot reach a strong score by predicting only the structure and emitting weak or contaminated narratives.
>
> Invalid Predictions
>
> A sample receives zero component credit for every structure-dependent component when:
>
> Required envelope tags are missing.
> The ownership block cannot be parsed.
> An unknown ownership label is used.
> A fragment ID not present in the public sample is emitted.
> The same fragment receives multiple ownership assignments.
> Required fragment ownership assignments are omitted.
>
> Narrative components can still be parsed only when both <T1> and <T2> blocks are present.
>
> At the submission level, the file must contain:
>
> Every expected sample_id.
> No extra sample IDs.
> No duplicate sample IDs.
> Exactly the published columns in the published order.
>
> Any submission-level schema failure receives the minimum score.
>
> Reproducing the Metric Locally
>
> For every validation sample:
>
> Parse the six output blocks.
> Recover one predicted ownership label for every fragment.
> Accumulate class counts for P1, P2, BRIDGE, and VOID.
> Compute dataset-level Ownership Macro F1.
> Compare each predicted profile route with its gold route.
> Compute route set F1.
> Compute route LCS.
> Combine those two route terms with a geometric mean.
> Average P1 and P2 route scores.
> Compare predicted and gold bridge sets with set F1.
> For every gold route fragment, measure normalized token coverage inside the correct generated narrative.
> Build opposite-profile and VOID contamination inventories.
> Measure contamination token leakage into each generated narrative.
> Convert leakage into Cross-Profile Purity.
> Compute token F1 between each generated narrative and its gold narrative.
> Compute token LCS between each generated narrative and its gold narrative.
> Combine token F1 and text LCS geometrically.
> Average each published component across the test set.
> Compute Structural = (O R B)^(1/3).
> Compute Generation = (G C N)^(1/3).
> Compute 100 Structural^1.20 Generation^0.80.
> Clip the result to [0.01, 100].
>
> The official grader.py follows this procedure directly.
>
> Intended Modeling Approaches
>
> A strong system can treat the task as one sequence-to-sequence problem or use several learned heads.
>
> Single-Sequence Fine-Tuning
>
> The simplest intended approach is:
>
> Serialize dialect, anchors, and fragments.
> Fine-tune a compact pretrained encoder-decoder model.
> Generate the complete target envelope autoregressively.
> Apply lightweight deterministic syntax repair.
> Submit the resulting serialized sequence.
> Multi-Task Encoder-Decoder
>
> A stronger system may share one encoder and train learned heads for:
>
> Fragment ownership.
> Bridge detection.
> Narrative admission.
> Route ordering.
> Text generation.
>
> The predicted structural state can then condition the decoder.
>
> Ownership-Aware Generation
>
> Useful architectures may:
>
> Encode each fragment separately.
> Add dialect embeddings.
> Add fragment-ID embeddings.
> Predict P1/P2/BRIDGE/VOID ownership.
> Pool profile-specific fragment states.
> Decode P1 and P2 narratives from separate conditioned states.
> Use pointer or copy attention over owned fragments.
> Route-Aware Decoding
>
> The route can be learned with:
>
> Autoregressive fragment-ID generation.
> Pointer networks.
> Learned ranking followed by sequence decoding.
> Pairwise precedence heads.
> Neural permutation models.
> Beam search with no-repeat constraints.
> Auxiliary Learning
>
> Participants may derive additional labels from target_sequence.
>
> Useful auxiliary objectives include:
>
> Fragment ownership classification.
> BRIDGE versus non-BRIDGE classification.
> VOID rejection.
> Route membership.
> Pairwise route precedence.
> Value-copy probability.
> Profile contamination detection.
> Dialect-conditioned code prediction.
>
> All auxiliary supervision must come from released training data.
>
> Pretrained Model Policy
>
> Pretrained encoder-decoder checkpoints are allowed.
>
> Participants may use publicly available pretrained model weights that were released before the challenge.
>
> Allowed use includes:
>
> Fine-tuning.
> Partial freezing.
> Parameter-efficient fine-tuning.
> Continued pretraining on released challenge text.
> Distillation performed only from an eligible local model.
>
> External retrieval is still prohibited.
>
> The challenge is intended to test adaptation to its latent ownership system rather than memorization of public biographies.
>
> Because original person names are replaced by local aliases and source metadata is withheld, direct encyclopedic recall should not be necessary.
>
> Allowed Resources
>
> Participants may use:
>
> Released challenge files.
> Public pretrained encoder-decoder model weights.
> Public tokenizer files associated with eligible pretrained models.
> Standard NLP libraries.
> Standard machine-learning libraries.
> Standard deep-learning frameworks.
> Public architecture code.
> Auxiliary labels derived from released training targets.
> Deterministic constrained decoding after learned scoring.
> Ensemble averaging or reranking among eligible learned models.
> Disallowed Resources
>
> Participants may not use:
>
> Search engines during inference.
> External biography databases.
> External knowledge graphs.
> Current encyclopedia lookup.
> Reverse lookup of source identities.
> Manually reconstructed source articles.
> Hidden evaluator files.
> Hidden test labels.
> Private preparation metadata.
> Manual test annotation.
> Hard-coded test ownership maps.
> Hard-coded test routes.
> Hard-coded test narratives.
> sample_id as a predictive feature.
> JSON row order as a predictive feature.
> Submission-feedback reconstruction of hidden labels.
> Rule-only prediction systems.
> TF-IDF-only prediction systems.
> Nearest-neighbor-only prediction systems.
> Validation and Leakage
>
> The atomic unit is the complete paired sample.
>
> Do not split fragments from the same sample across training and validation.
>
> All derivatives of one sample should remain together, including:
>
> Anchor encodings.
> Fragment encodings.
> Ownership labels.
> Route labels.
> Bridge labels.
> Generated target text.
> Auxiliary targets.
>
> For stronger local validation, participants should also avoid placing the same source profile in both local training and validation when they can infer such clusters from released data.
>
> The official hidden split already prevents exact source-biography reuse across released train and test.
>
> Why the Task Is Difficult
>
> Several ambiguities occur at once.
>
> A model can understand the broad meaning of a fragment yet still fail because:
>
> It attaches the value to the wrong profile.
> It learns the wrong K-code meaning for the active dialect.
> It mistakes a bridge for ordinary ownership.
> It mistakes an owned but unspoken fact for a route item.
> It selects the right route members in the wrong order.
> It copies a correct value into the wrong narrative.
> It produces fluent text that ignores the latent structure.
>
> The fragment pool also contains same-shape collisions.
>
> One sample can contain:
>
> Several dates.
> Several occupations.
> Several institutions.
> Several locations.
> Several title-like strings.
>
> Surface type alone is therefore insufficient.
>
> Practical CPU Strategy
>
> A practical solution can use a compact pretrained text-to-text model.
>
> One possible pipeline is:
>
> Serialize each sample into a bounded input sequence.
> Fine-tune on the full target envelope.
> Add an auxiliary fragment-ownership loss.
> Add an auxiliary route-membership loss.
> Prefer copying for rare proper nouns and dates.
> Use constrained decoding for fragment IDs and ownership labels.
> Decode the narrative blocks with ordinary beam search.
> Validate with complete paired examples rather than fragment-level splits.
>
> A stronger model can use separate learned structure and narrative decoders while sharing the same compact encoder.
>
> Limitations
>
> The source language is historical English-language biographical prose.
>
> The challenge therefore inherits limitations of historical encyclopedia data, including:
>
> Uneven geographic coverage.
> Uneven occupational representation.
> Uneven representation of demographic groups.
> Editorial inconsistencies.
> Historical inaccuracies.
> Sparse or conflicting attributes.
> Older tokenization conventions.
> Uneven article quality.
>
> The source snapshot is from September 2015.
>
> The challenge should not be treated as a source of current biographical truth.
>
> The benchmark measures model behavior on released record fragments and generated targets.
>
> It does not measure:
>
> Current factual accuracy.
> Open-web research ability.
> Citation retrieval.
> Long-form biography writing.
> General-purpose entity resolution across arbitrary databases.
> Expected Outcome
>
> A successful system should learn to:
>
> Decode opaque schema behavior under multiple dialects.
> Partition an entangled record pool between two profiles.
> Detect genuine cross-profile bridges.
> Reject plausible unclaimed fragments.
> Distinguish ownership from narrative admission.
> Recover the ordered factual cadence of each profile.
> Generate two grounded narratives.
> Keep profile-specific values in the correct narrative channel.
> Adapt a compact pretrained seq2seq model within the CPU-only environment.
>
>  
>
> Submissions
> 2
> Top Score
> 17.589
> Created
> Aug 11, 2026
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

## Cross-Modal Audio-Motion Representation Adaptation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7admwkm56zvkdwj20bbfxz018c7esh
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> Train or fine-tune a dual-stream representation model that matches four measured group-motion responses to four anonymous acoustic candidates. For every case, predict the one-to-one response-to-sound assignment, whether each response leads or follows its matched sound pattern, and whether the participants moved coherently as a group.
>
> The data comes from controlled standstill experiments in which several people were tracked with optical body markers while silence or music excerpts were presented. Experimental archives can preserve motion recordings and acoustic summaries while losing the key that says which stimulus belongs to each response window. Recovering that key is necessary before researchers can compare conditions or study whether a group moved together.
>
> Each packet has motion responses R1 through R4 and shuffled acoustic candidates A through D. Candidate letters are local to one packet and carry no identity across cases. A correct solution must compare dense marker trajectories with acoustic dynamics and solve a four-way one-to-one assignment.
>
> The benchmark measures transfer to unseen participant groups. All packets from one complete group recording stay in one split, and five groups are held out for testing. The public tensors retain marker-level displacement, velocity, and acoustic timing at 256 steps. They are intentionally richer than summary statistics so that high-scoring solutions learn cross-modal representations rather than rely on a few global correlations.
>
> Dataset
>
> There are 4,500 labeled training packets and 900 hidden-label test packets. Fifteen complete recording groups supply training cases, and five different groups supply test cases. Every packet payload is unique.
>
> Files And CSV Columns
> | Path | Description |
> |---|---|
> | `train.csv` | Inputs plus the three target columns for 4,500 cases. |
> | `test.csv` | Inputs only for 900 cases. |
> | `sample_submission.csv` | Schema-valid baseline predictions for every test ID. |
> | `motion_packets/*.npz` | One compressed tensor packet per train or test case. |
>
>
> train.csv contains case_id, packet_path, response_contract, stimulus_key, response_lag_word, and consensus_state.
>
> test.csv contains only case_id, packet_path, and response_contract.
>
> | Column | Data type | Train | Test | Meaning |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque content-derived identifier. |
> | `packet_path` | string | yes | yes | Relative path to the case's compressed tensor packet. |
> | `response_contract` | string | yes | yes | Case-independent reminder of row, card, and timing-symbol order. |
> | `stimulus_key` | ordered token string | yes | no | Acoustic candidate assigned to each response row. |
> | `response_lag_word` | ordered token string | yes | no | Early, aligned, or late relation for each matched pair. |
> | `consensus_state` | categorical string | yes | no | Group-motion state: `coherent`, `split`, or `weak`. |
>
>
> response_contract is identical in meaning for every row. It states that R1 through R4 must be matched to A through D and defines the timing symbols. It contains no case-specific clue.
>
> Tensor Packets
>
> Load a packet with numpy.load(packet_path).
>
> | Array | Shape | Data type | Axis meaning |
> |---|---:|---|---|
> | `motion_responses` | `4 x 8 x 256 x 6` | float16 | Response row, padded marker, normalized time, then three displacement and three velocity channels. |
> | `marker_mask` | `4 x 8` | uint8 | One for a real participant marker and zero for padding. |
> | `acoustic_candidates` | `4 x 256 x 10` | float16 | Candidate A through D, normalized time, then ten acoustic descriptors. |
>
> Each motion response uses four to eight measured participant markers. Coordinates are centered per marker, robustly scaled within the selected window, and resampled to 256 points. The first three channels describe relative X, Y, and Z displacement. The next three describe X, Y, and Z velocity. Padding is always zero and must be interpreted through marker_mask.
>
> The acoustic descriptor order is:
>
> RMS level;
> spectral centroid;
> spectral bandwidth;
> 85 percent rolloff;
> spectral flatness;
> zero-crossing rate;
> low-frequency energy fraction;
> onset strength;
> onset indicator;
> pulse clarity.
>
> Descriptors are robustly centered and scaled within their source stimulus. A response and its correct candidate cover corresponding portions of the experiment, but their row positions are shuffled independently.
>
> Targets
>
> stimulus_key is a permutation of A, B, C, and D joined by >. Its four positions answer R1, R2, R3, and R4.
>
> Example: B>D>A>C means R1 matches B, R2 matches D, R3 matches A, and R4 matches C. All 24 permutations occur in both splits.
>
> response_lag_word contains four symbols joined by > in response-row order:
>
> | Symbol | Meaning |
> |---|---|
> | `E` | Motion evidence leads the matched acoustic onset pattern. |
> | `A` | The strongest association is temporally aligned. |
> | `L` | Motion evidence follows the matched acoustic onset pattern. |
>
>
> Example: L>A>E>A.
>
> consensus_state summarizes marker agreement:
>
> | Value | Meaning |
> |---|---|
> | `coherent` | Participant markers show a strong shared movement envelope. |
> | `split` | Movement is present, but marker amplitudes divide into inconsistent responses. |
> | `weak` | Motion strength or cross-marker agreement is too low for a confident group response. |
>
> | Split | `coherent` | `split` | `weak` |
> |---|---:|---:|---:|
> | Train | 2,047 | 1,482 | 971 |
> | Test | 491 | 261 | 148 |
> Submission Format
>
> Write ./working/submission.csv with exactly these columns in this order: case_id, stimulus_key, response_lag_word, consensus_state.
>
> | Column | Required serialization |
> |---|---|
> | `case_id` | Every test identifier exactly once, without whitespace padding. |
> | `stimulus_key` | Four unique letters from A through D joined by `>`; maximum 24 characters. |
> | `response_lag_word` | Four symbols from E, A, and L joined by `>`; maximum 24 characters. |
> | `consensus_state` | Exactly `coherent`, `split`, or `weak`. |
>
> | case_id | stimulus_key | response_lag_word | consensus_state |
> |---|---|---|---|
> | `mm_example` | `B>D>A>C` | `L>A>E>A` | `split` |
>
>
> The grader rejects extra or reordered user columns, duplicate column names, missing or additional rows, duplicate IDs, unknown IDs, and IDs with whitespace padding. Invalid target strings receive zero for their component.
>
> Evaluation
>
> The Cross-Modal Response Recovery Score is:
>
> Score = 0.55 * KeyScore + 0.30 * LagScore + 0.15 * ConsensusScore.
>
> Minimum score: 0.0
> Maximum score: 1.0
> Higher scores are better.
>
> KeyScore
>
> For one case, position_accuracy is the fraction of four response positions assigned the correct candidate. Then:
>
> key_case = 0.25 * position_accuracy + 0.75 * exact_key_match.
>
> Case scores are averaged inside each hidden recording group. KeyScore is the unweighted mean of those group averages, so a group with more derived windows cannot dominate evaluation.
>
> LagScore
>
> lag_accuracy is the fraction of four lag symbols that exactly match. Per case:
>
> lag_case = 0.35 * lag_accuracy + 0.65 * exact_lag_word_match.
>
> LagScore uses the same recording-group macro average.
>
> ConsensusScore
>
> For each consensus class present in the hidden answers, recall is:
>
> correct predictions for that class / hidden rows of that class.
>
> ConsensusScore is the mean of these class recalls. A consensus prediction counts as correct only when the submitted stimulus_key is also exactly correct for that case. This prevents collecting state credit while assigning responses to the wrong stimuli.
>
> Expected And Allowed Methods
>
> This benchmark evaluates target-domain adaptation of two learned encoders. One branch must summarize variable-size marker sets over time; the other must represent acoustic dynamics. Their pairwise scores feed a differentiable or discrete four-way assignment layer, while temporal and group-level heads predict lag and consensus.
>
> The prepared training set contains 18,000 dense motion responses and 18,000 acoustic candidates. Its padded motion tensors contain 221,184,000 float16 values before compression; marker_mask distinguishes measured markers from padding. Fine-tuning compact temporal, point-set, or cross-attention encoders in mini-batches is the intended workload. The assignment itself is tiny; the GPU-relevant work is learning representations from dense marker and acoustic tensors and transferring them to unseen groups.
>
> Hosted inference services are not allowed. Training and inference must run inside the competition environment.
>
> What Not To Use
> Do not infer labels from case IDs, row order, filenames, packet sizes, hashes, or padding counts.
> Do not identify participant groups or original stimuli through external lookup.
> Do not treat candidate letters as global identities; A through D are independently permuted in every case.
> Do not exploit repeated windows, malformed submissions, private files, hidden labels, or repeated leaderboard probing.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 10, 2026
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

## French Discourse Choice Drift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77202aq4bmevedkvpvqrq8398byak9
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat lock's score of 0.699!

Full challenge description from page:

> French Discourse Choice Drift Overview Restore one removed French discourse span in an authentic social-media post. Each context contains exactly one [CHOIX] placeholder. Reconstruct the phrase that occupied that span: enfin, finalement, au final, or à la fin. These expressions overlap in broad meaning but differ in discourse function, syntax, register, and temporal framing. Reliable restoration is useful for corpus repair, anonymized-text analysis, and evaluating whether French language models preserve pragmatic choices under temporal drift. This is a supervised masked-span restoration task in the Fine-Tuning lane. Your solution must adapt a language model on the public restoration examples and run on the selected NVIDIA A10G tier. A fixed phrase list, an unfitted pretrained model, or a CPU-only template system is not a valid solution. Fine-tuning requirement Tokenize the masked post and use the labeled public contexts to make gradient-based updates to a language model's encoder, decoder, or trainable adaptation layers. Full-model fine-tuning and trained parameter-efficient adapters are valid; zero-shot inference, a frozen encoder with only an untrained lookup, or hand-written phrase rules are not. The four phrase strings are the serialized restoration output. A compliant solver should learn this conditional restoration from the post context (for example, with a trainable language-model head or adapter and cross-entropy), rather than copy a fixed prior. Keep the test-time decision context-based. The test month and all labels are hidden, so no month-prior lookup or test-wide quota fitting can substitute for learned contextual restoration. Dataset File descriptions dataset/public/train.csv — 36,000 labeled contexts from February through November 2025. dataset/public/test.csv — 8,800 unlabeled contexts from December 2025 and January 2026. dataset/public/sample_submission.csv — Random valid marker choices for every test ID. Column descriptions id — Stable opaque identifier such as fd_866adab1c30d628c; present in every public file. context — Authentic French post with one original marker replaced by [CHOIX]; present in train.csv and test.csv. month — Training data only: source month in YYYY-MM form. It supports public temporal validation and is absent from test.csv so it cannot be mistaken for an evaluation target or used as a test-time shortcut. marker — Training restoration target only: the original span, one of enfin, finalement, au final, or à la fin; present only in train.csv. All four markers are balanced within every public training month. The private months preserve their natural marker mix; no private class quota is disclosed or enforced. Exact duplicate masked contexts and posts containing more than one target-marker occurrence are removed before splitting. Public training months end before the two private months. Evaluation risk and calibration The public training set has 36,000 rows with exactly 9,000 examples per marker (25% each) across ten months. The private set has 8,800 rows, 4,400 from each of the next two months, but its marker prior is the unbalanced natural source mix rather than a designed 25%/25%/25%/25% sample. No exact private class quota or target proportion is disclosed. For the frozen challenge artifact, every marker is present in each private month and occupies between 5% and 65% of that month's rows (220–2,860 of 4,400); across both months this implies 440–5,720 of 8,800 per marker. These are deliberately coarse support bounds, not quotas. Because the month term is macro F1, each marker receives equal weight within each month even when the natural prior is skewed; rare-marker support remains the main calibration risk. A model calibrated to the public 25% prior can still overpredict common expressions or underpredict rare ones. The weakest-marker and weakest-month terms expose that risk, while the score remains bounded in [0, 1]. The month field is withheld in test.csv, so temporal validation must use the public training month field rather than a test-time month shortcut. Evaluation The Temporal-Robust Discourse F1 rewards restoration quality while protecting the weakest expression and weakest private month. Compute F1 independently for each of the four restored expressions across the full private set. Compute macro F1 independently within December 2025 and January 2026. Combine the results: score = ( 0.60 * mean(marker_f1) 0.25 * min(marker_f1) 0.15 * min(month_macro_f1) ) The score ranges from 0 to 1 and is maximized. The weakest-marker term prevents a model from neglecting a pragmatically difficult choice. The weakest-month term reflects the practical need for corpus restoration to remain stable as online language changes. Submission Submit one prediction for every test row. id — Exact test identifier. marker — The restored span, exactly one of enfin, finalement, au final, or à la fin. Example: id,marker fd_866adab1c30d628c,au final fd_bcfa382a36fca984,enfin fd_fd59d0cd0df05c8c,enfin Requirements Columns must be exactly id,marker in that order. Include every test ID exactly once; extra, duplicate, or missing IDs are rejected. Missing predictions and values outside the four allowed restored spans are rejected. Train or fine-tune on public data only. Publicly released pretrained model weights are allowed, but the model must be genuinely fine-tuned on this task. Do not assume or force a hidden whole-test class quota; select each prediction from its linguistic context. &nbsp;
> $700 Pool
> 4 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Sentence-to-Turn Semantic Compiler Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a1kx3hjmj5y0nhx1pgm9qjh8c9h8g
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat xbongox's score of 93.926!

Full challenge description from page:

> Overview Sentence-to-Turn Semantic Compiler Induction is a hard CPU sequence-to-sequence challenge over human-authored English customer-service turns. The data contains customer turns that have been interpreted at two resolutions: Sentence resolution: each sentence is analyzed separately. Whole-turn resolution: the complete multi-sentence turn is analyzed as one unit. Those two views are related, but they are not always identical. When several sentences are interpreted together, a local meaning can survive, merge with another meaning, disappear as a separate unit, change its argument role, or become part of a new whole-turn meaning. The prediction task is simple to state: Study three worked sentence-to-turn transformations, infer the temporary transformation system used in that example, and apply it to a fourth customer turn. Every sample contains: Three worked support turns. One query turn. Public sentence-level semantic atoms for all four turns. Public whole-turn semantic atoms and derivations for the three supports. A fresh set of opaque semantic codes used only inside that sample. Public token coordinates for grounded arguments. A few public counterfactual probes such as removing one source atom or blocking whole-turn emergence. For the query turn, the model must generate: The source-to-target derivation. The whole-turn semantic atom inventory. Exact token spans for grounded target arguments. A small consistency checksum. The target atoms that would disappear under each public counterfactual probe. A compact target can look like: X01 KEEP Y01 X02+X04 FUSE Y02 X03 DROP VOID ROOT RISE Y03 Y01 V06 Y02 V11 Y03 V02 Y04 R07 T09:T11 SRC=4 USED=3 DROP=1 ROOT=1 OUT=4 P01=Y02 P02=Y03 The five transformation operators are: KEEP: one sentence-level atom survives as one whole-turn atom. FUSE: several sentence-level atoms combine into one whole-turn atom. DROP: a sentence-level atom does not survive as a separate whole-turn atom. RISE: a whole-turn atom appears only when the complete turn is interpreted together. REBIND: a grounded argument survives but changes its whole-turn semantic role. The visible semantic codes are deliberately sample-local. For example, U04 in one sample has no relationship to U04 in another sample. The same is true for the target codes. A model therefore cannot solve the task by learning one global label dictionary. The three support turns act as worked examples for the current sample. They reveal enough of the temporary code system and transformation behavior to make the query learnable, but the query recombines those behaviors in a new way. Real-world context The underlying language comes from human customer-service interactions containing requests, clarifications, corrections, confirmations, troubleshooting statements, account questions, transaction details, and other service-oriented language. The challenge uses paired sentence-level and whole-turn semantic observations of that language to create a new transformation problem. Original human-readable ontology names and source identifiers are not part of the public prediction task. A practical analogy is a semantic-processing pipeline that has two stages: A local analyzer produces sentence-level units. A turn-level compiler reconciles those units into one final interpretation. Participants are given examples of how that compiler behaves and must infer its behavior for a new turn. At a glance A successful model must jointly learn: How to use worked support examples. What the temporary semantic codes mean inside the current sample. Which source atoms survive. Which atoms merge. Which atoms disappear. Which whole-turn meanings emerge. How argument roles move across resolution. Where grounded arguments occur in the fused text. How the inferred derivation behaves after controlled evidence removal. This is a Fine-Tuning challenge. Compact pretrained encoder-decoder models are allowed, subject to the published parameter and CPU limits. The Central Idea Most structured language benchmarks assume one fixed target ontology. A model sees many examples and gradually learns that a particular output label has one stable global meaning. This challenge removes that assumption. Every episode invents a new visible semantic dialect. The model must first determine how that local dialect behaves from the support turns. Only then can it solve the query. The transferable skill is therefore not: "map this sentence to label V12." The transferable skill is: "read a few examples of how local semantic units are compiled into whole-turn units, infer the transformation rules and temporary symbols, then apply that compiler to a new composition." This creates an explicit meta-learning problem inside every training and test example. Why Sentence Resolution and Turn Resolution Are Different Consider a customer turn containing three sentences: S01: i paid the invoice yesterday S02: the balance still shows as unpaid S03: can you check whether the payment went through At sentence resolution, the three sentences can support several local semantic atoms. At whole-turn resolution, those atoms can behave differently. For example: The payment statement may survive. The unpaid-balance report may remain independent. The final question may absorb information from both earlier sentences. Two locally separate argument traces may become one whole-turn argument structure. The query is not asking the model to repeat the sentence-level analysis. It is asking the model to infer the resolution transition. Episode Structure Each episode contains four turns: Support A. Support B. Support C. Query Q. All four turns use the same temporary source and target ciphers. The three supports reveal worked examples of the hidden compiler. The query hides the target side. The temporary ciphers are regenerated independently for every episode. This means: U08 in one episode is unrelated to U08 in another episode. V08 in one episode is unrelated to V08 in another episode. K08 in one episode is unrelated to K08 in another episode. R08 in one episode is unrelated to R08 in another episode. The numerical suffix is merely a local symbol ID. No global source-to-target dictionary exists. Why Three Supports Are Provided One support example is often too weak. Two supports can still leave several transformations underdetermined. Three supports provide enough local evidence for meaningful induction while keeping the episode compact. The supports are deliberately chosen so that they reveal different parts of the temporary compiler. A support set can jointly demonstrate: One source PULSE surviving unchanged in structure. Two source PULSE atoms fusing. One source atom being dropped. One target atom emerging from whole-turn context. One argument role changing its attachment. One grounded target span shifting under whole-turn interpretation. The query then recombines those phenomena. The query is not selected to be an exact copy of any support derivation. Fine-Grained Source View The fine-grained view is built from sentence-level semantic atoms. Every source atom has: atom_id kind glyph home trace Example: {"atom_id":"X03","kind":"PULSE","glyph":"U09","home":"S02","trace":"-"} or: {"atom_id":"X05","kind":"TRACE","glyph":"K04","home":"S03","trace":"T03:T05"} Source atom IDs are local to one turn. The source alphabet uses: U-codes for PULSE atoms. K-codes for TRACE atoms. Whole-Turn Target View The target view describes the complete turn after whole-turn semantic compilation. Target atoms use: V-codes for PULSE atoms. R-codes for TRACE atoms. The target view is hidden for the query. The model must predict it. Whole-turn atoms receive canonical IDs: Y01 Y02 Y03 ... These IDs are assigned using the public canonical ordering rule described later. PULSE Atoms A PULSE represents a semantic commitment that is not tied to one exact argument span. A PULSE can encode behavior such as: A request. A statement of state. A correction. A confirmation. A question. A refusal. A problem report. Another service-relevant semantic commitment. The human-readable semantic names are intentionally not released. The challenge is designed so participants learn the temporary symbol behavior from the supports. TRACE Atoms A TRACE represents an argument grounded in a contiguous token span. A TRACE can correspond to material such as: A date. A number. A monetary amount. A location. A product name. A service object. A transaction reference. Another value-bearing phrase. TRACE atoms contain token coordinates. The coordinates refer to the public whitespace token tape. Token Tape Every fused turn includes a deterministic token tape. For example: T01 i T02 paid T03 the T04 invoice T05 yesterday T06 but T07 it T08 still T09 shows T10 unpaid The challenge output always uses this tape. Participants may use any tokenizer internally. The public T-coordinates remain the evaluation coordinates. Temporary Semantic Ciphers Each episode independently remaps all visible semantic symbols. The four alphabets are: Source PULSE: U01, U02, ... Target PULSE: V01, V02, ... Source TRACE: K01, K02, ... Target TRACE: R01, R02, ... The remapping is performed after the official train/test partition is established. The same hidden semantic concept can therefore appear under different visible symbols in different episodes. Likewise, the same visible symbol can denote unrelated concepts in different episodes. This is a deliberate anti-memorization mechanism. The Compiler View The hidden transformation is expressed through five public operator families: KEEP FUSE DROP RISE REBIND The names describe structural behavior. They do not reveal the hidden semantic label. KEEP Syntax: X01 KEEP Y01 One source atom survives as one target atom. The visible source and target glyphs can still differ. KEEP describes lineage, not cipher equality. FUSE Syntax: X02+X04 FUSE Y02 Two or more source atoms contribute to one target atom. FUSE is not simple duplicate removal. The parents can: Carry the same source glyph. Carry different source glyphs. Come from different sentences. Include both PULSE and TRACE evidence when the target structure warrants it. The supports teach what kinds of fusion occur under the current episode-local compiler. DROP Syntax: X03 DROP VOID A source semantic atom does not survive as an independent whole-turn atom. DROP can occur when: A sentence-level interpretation is absorbed by another whole-turn unit. Local wording becomes subordinate after context is considered. A sentence-level distinction is not retained at turn resolution. RISE Syntax: ROOT RISE Y03 A whole-turn atom appears even though no single source atom is declared its direct parent. ROOT represents complete-turn evidence. RISE captures semantic structure that materializes only after multiple sentences are interpreted jointly. REBIND Syntax: X05 REBIND Y04 REBIND is used for grounded TRACE behavior. A source argument survives semantically but changes its whole-turn attachment or role. The target R-glyph and token span must be predicted. REBIND is intentionally distinct from KEEP because the argument's semantic function after compilation differs from its local sentence reading. Why REBIND Matters Without REBIND, argument handling would collapse into ordinary span copying. The challenge includes cases where: A value appears locally under one sentence-level role. Whole-turn interpretation changes which semantic commitment it belongs to. The same surface span remains relevant but receives a different target cipher. This forces the model to reason about the relation between arguments and whole-turn semantics rather than merely copying token boundaries. Derivation Tape Every support turn contains a public derivation tape. The derivation tape is the exact sequence of compiler operations needed to transform the source view into the target view. Example: X01 KEEP Y01 X02+X04 FUSE Y02 X03 DROP VOID ROOT RISE Y03 X05 REBIND Y04 The query derivation tape is hidden. Participants must predict it. The derivation tape serves two purposes: It teaches the temporary compiler behavior. It makes the query prediction auditable. A model can recover the correct target inventory for the wrong lineage and still lose derivation credit. Target Register The target register lists the predicted whole-turn PULSE atoms. Example: &nbsp; Y01 V06 Y02 V11 Y03 V02 &nbsp; TRACE atoms are listed separately in the GROUND block. This avoids duplicating grounded atoms in two places. Grounding Register The grounding register lists whole-turn TRACE atoms. Example: &nbsp; Y04 R07 T09:T11 Y05 R02 T14:T14 &nbsp; Each entry contains: Canonical target atom ID. Target TRACE glyph. Inclusive fused-turn token span. If there are no target TRACE atoms: NONE Conservation Signature Every target also contains a small semantic conservation signature. Example: &nbsp; SRC=5 USED=4 DROP=1 ROOT=1 OUT=4 &nbsp; The fields mean: SRC: number of source atoms. USED: number of source atoms assigned to KEEP, FUSE, or REBIND. DROP: number of source atoms assigned to DROP. ROOT: number of RISE-produced target atoms. OUT: total number of target atoms. The conservation signature is deterministic. It does not introduce new hidden information. It functions as a checksum over the predicted compiler execution. The model must generate it because the task is framed as structured compilation rather than isolated label emission. Why Include a Conservation Signature A structured output can be locally plausible while globally inconsistent. For example, a model could: Forget one source atom. Reuse one source atom twice. Produce a target atom with no parent. Emit one extra target atom. The conservation signature makes global structure explicit. It also creates an additional learned consistency signal during training. The evaluator recomputes the signature from the predicted derivation. Participants do not gain anything by hard-coding the counts. Counterfactual Execution Probes Every query contains a small set of intervention instructions. The intervention is public. Its hidden fallout is part of the target. The probes do not alter the natural-language query text. They alter the available semantic evidence after the model has inferred the query compiler. This is intentional. The benchmark is asking: "if this is truly the transformation law you inferred, what would that law produce when one piece of its source evidence is removed?" A typical query contains three probes. Possible probe forms are: REMOVE Xnn CUT Snn BLOCK ROOT The probes are evaluated independently from one another. Each begins from the original unmodified query source view. REMOVE Example: P01 REMOVE X03 The probe removes source atom X03. Any target atom whose derivation requires X03 becomes unavailable. For KEEP and REBIND: Removing the sole parent removes the target. For FUSE: The parent set is conjunctive. Every listed source parent is required. Removing any required FUSE parent invalidates the fused target. For DROP: There is no target atom to remove. RISE atoms are not affected by ordinary source removal because their parent is ROOT. CUT Example: P02 CUT S02 CUT removes every source atom whose home is S02. The compiler is then evaluated under the same strict-support rule. If a target atom depends on any removed required parent, that target atom enters the fallout set. CUT therefore tests whether the model understands how several local sentence atoms jointly support the whole-turn frame. BLOCK ROOT Example: P03 BLOCK ROOT BLOCK ROOT disables whole-turn emergence. Every target atom produced by: ROOT RISE Yxx enters the fallout set. Parented KEEP, FUSE, and REBIND targets remain unaffected. Probe Fallout The hidden answer to each probe is the set of canonical target Y IDs that become underivable. Example: &nbsp; P01=Y02 P02=Y02,Y04 P03=Y03 &nbsp; NONE is used when an intervention causes no target atom to fail. The probe block is ordered by public probe ID. Y IDs inside one fallout set are ordered numerically. Why Counterfactual Probes Are Part of the Prediction Without interventions, a model can sometimes obtain a plausible target register while relying on a weak or accidental internal lineage. The probe ledger makes that shortcut visible. Two predictions can contain the same macro atoms yet imply different causal support structures. For example: Prediction A: X01+X02 FUSE Y01 Prediction B: X01 KEEP Y01 X02 DROP VOID Both may contain target Y01. But under: REMOVE X02 their consequences differ. Under the benchmark's conjunctive FUSE semantics: Prediction A loses Y01. Prediction B preserves Y01. The hidden probe answer therefore tests the derivation law itself. This adds a second execution surface to the benchmark: Compile the observed query. Execute interventions against the inferred compiler. The model is rewarded for learning a transformation that remains coherent beyond one static output. Counterfactual Probes Are Not Extra Human Annotation Probe answers are deterministic consequences of the hidden derivation tape. No additional semantic labeling is required. This matters for reproducibility. Given a gold derivation and the published intervention semantics, any participant can regenerate the probe targets locally for training or validation examples. The counterfactual layer therefore strengthens the task without introducing subjective hidden judgments. Canonical Target Ordering Target Y IDs are assigned deterministically. For each predicted target atom: Determine its earliest supporting fused-turn token position. For FUSE, use the earliest position contributed by any parent. For KEEP, use the earliest position of the source atom's home sentence or TRACE. For REBIND, use the predicted target TRACE start coordinate. RISE atoms with a grounded TRACE use that TRACE position. Ungrounded RISE PULSE atoms follow all grounded or parented atoms. Remaining ties are broken by target glyph and then operator order. After sorting, assign: Y01 Y02 Y03 ... This avoids arbitrary target identifiers. Query Output Envelope The submission target is one structured sequence: ... ... ... ... ... Example: X01 KEEP Y01 X02+X04 FUSE Y02 X03 DROP VOID ROOT RISE Y03 X05 REBIND Y04 Y01 V06 Y02 V11 Y03 V02 Y04 R07 T09:T11 SRC=5 USED=4 DROP=1 ROOT=1 OUT=4 The entire output is one sequence. This makes the benchmark compatible with ordinary encoder-decoder fine-tuning while retaining explicit structure. What Makes the Query Non-Trivial The query is selected so that no single support provides the answer pattern. For example: Support A may demonstrate: U03 -> V08 through KEEP. U11 -> V04 through KEEP. Support B may demonstrate: Two U03 atoms FUSE into one V08 atom. Support C may demonstrate: A K05 TRACE is REBINDed into R09. The query can then contain: Two U03 atoms. One U11 atom. One K05 TRACE. One additional local atom that is dropped. Solving the query requires combining evidence across all three supports. Support Coverage The support selection process aims to make the query learnable without making it trivial. For every query: Most temporary source glyphs are witnessed in at least one support. Most temporary target glyphs are witnessed in at least one support. At least one operator behavior relevant to the query is demonstrated. The full query derivation is not copied verbatim from one support. Harder examples may include one underdetermined symbol whose interpretation must be inferred compositionally from language. Episode-Local Meta-Learning The benchmark deliberately separates two kinds of learning. Across-Episode Learning Across the training set, the model learns: How to read the public representation. What KEEP/FUSE/DROP/RISE/REBIND mean structurally. How sentence meaning differs from whole-turn meaning. How to use worked support derivations. How to produce valid compiler outputs. Within-Episode Learning Inside one foldbook, the model must learn: What the temporary U/K glyphs mean. What the temporary V/R glyphs mean. Which source and target glyphs correspond. Which merges are licensed. Which TRACE roles rebind. Which whole-turn meanings can rise from ROOT. The challenge score depends on both. A model strong only at one level should plateau. What Common Shortcuts Miss Several apparently natural shortcuts do not solve the full task. Global code memorization fails because U/V/K/R meanings are re-randomized for every sample. Nearest-example copying fails because the query combines support behaviors in a new composition. One-to-one code translation fails because FUSE, DROP, RISE, and REBIND are non-bijective transformations. Predicting only the final target atoms is incomplete because the evaluator also scores source-to-target lineage and operator identity. Predicting only lineage is incomplete because target codes, grounded spans, conservation, and intervention fallout are also evaluated. Static graph guessing is incomplete because public probes test whether the submitted derivation behaves correctly when evidence is removed. The public source atoms are already a semantic analysis of the query. The hidden object is the transformation between sentence-scale and whole-turn semantics, not a fresh parse from raw text alone. Why Existing Program-Induction Benchmarks Cannot Directly Express This Task The challenge shares the broad idea of learning from worked examples with episodic reasoning benchmarks. That resemblance is intentional but incomplete. The important distinction is representational. Several widely known benchmark families would require fundamental changes to their input language, target language, or evaluator before they could encode one complete episode of this task. Abstraction and Reasoning Corpus ARC episodes provide several input-output grid transformations followed by a held-out grid. That captures episodic transformation induction. However, an ARC task does not natively contain: Two aligned linguistic annotation resolutions. A source semantic graph whose nodes have temporary meanings. A separate temporary target semantic alphabet. Explicit source-to-target lineage. Many-to-one semantic parentage. A distinguished ROOT parent for whole-input emergence. Argument-role rebinding. Token-coordinate grounding. Counterfactual interventions over latent source atoms. A conservation checksum over semantic flow. To express one compiler episode as ARC, the benchmark would need more than a new set of grid puzzles. It would need: A graph-valued input representation. Local symbol bindings. A derivation language. Grounded text coordinates. Intervention semantics. A structured evaluator aware of lineage and operator identity. That would materially change the benchmark interface rather than instantiate an ordinary ARC task. SCAN SCAN maps commands into action sequences under a globally shared symbolic interpretation. Its compositional splits test systematic generalization. This compiler challenge differs because the visible semantic vocabulary is not globally shared. Every episode rebinds its U/V/K/R symbols. SCAN also lacks: Source and target semantic graphs. Explicit cross-resolution parentage. Many-to-one FUSE ancestry. Source deletion through DROP. ROOT-originated RISE nodes. REBIND of grounded arguments. Counterfactual source interventions. A SCAN-like system would need an episode-local ontology and graph derivation semantics before it could represent the target. COGS COGS evaluates compositional generalization from text to a fixed logical representation. Its target formalism is globally meaningful. The challenge here instead makes the visible source and target semantics temporary. The learner has to infer those semantics from support transformations. COGS also evaluates the final logical form rather than a transformation witness connecting two semantic resolutions. To represent this task, COGS would need: Paired source and target ontologies per episode. Non-bijective lineage. Operator-labeled derivations. Grounded target spans. Query interventions. Those are not ordinary COGS split changes. They alter the supervised object. CFQ CFQ tests compositional generalization from natural-language questions to SPARQL queries. Its relation and entity schema is fixed globally. The target is one executable query. Cross-Resolution Semantic Compiler Induction instead predicts: A temporary ontology binding. A semantic lineage proof. Non-bijective transformations. Whole-turn-only emergence. Argument rebinding. Counterfactual fallout. Representing this with CFQ would require replacing the fixed SPARQL target language with an episode-specific typed derivation language. TOP and Task-Oriented Semantic Parsing Hierarchical task-oriented parsers such as TOP produce structured semantic trees over utterances. The ontology is ordinarily fixed. A parse tree describes the semantic analysis of the utterance itself. This challenge instead predicts the mapping between two analyses of the same language at different resolutions. The source semantic atoms are already public. The hidden object is how those atoms compile into another representation. TOP would therefore need a second semantic plane plus explicit cross-plane ancestry before it could express the task. SMCalFlow-Style Meaning Representation Program-oriented dialogue representations can capture rich semantic programs. They still assume a stable executable vocabulary. The current challenge resets its visible semantic vocabulary per episode and evaluates the derivation relating two annotation resolutions. A meaning representation alone is not enough. It would need explicit: Source atoms. Target atoms. Compiler operators. Parentage. Grounding transfers. Counterfactual intervention behavior. The Fundamental Difference The closest broad family is episodic induction. The central supervised object, however, is not merely an input-output mapping. It is a locally bound semantic compiler with an auditable derivation and intervention behavior. A complete episode therefore has four coupled layers: Natural-language evidence. Fine-grained source semantics. Whole-turn target semantics. The compiler witness connecting them. The counterfactual probes add a fifth layer: Behavior of that compiler under controlled semantic evidence removal. Removing any one of these layers produces a materially easier and qualitatively different task. What Must Be Learned Versus What Is Fixed Several pieces of the benchmark are global and therefore learnable across episodes: The meaning of KEEP. The meaning of FUSE. The meaning of DROP. The meaning of RISE. The meaning of REBIND. Probe intervention semantics. Output grammar. Canonical target ordering. Conservation arithmetic. Several pieces are intentionally local and must be inferred anew: Meaning of U glyphs. Meaning of V glyphs. Meaning of K glyphs. Meaning of R glyphs. Which local source and target glyphs correspond. Which combinations fuse in the current episode. Which argument roles rebind. Which whole-turn meanings rise. This division is deliberate. The benchmark is not trying to hide syntax. It hides the episode-specific semantic binding while publishing the transformation machinery. That makes the task inspectable without reducing it to a fixed-ontology parser. Research Positioning The benchmark deliberately combines ideas that normally live in separate evaluation families. From episodic induction it takes: Worked support examples. A held-out query. Within-episode rule inference. From semantic parsing it takes: Language-grounded structured representations. Argument spans. Compositional outputs. From program synthesis it takes: Explicit operators. Derivation witnesses. Executable structural constraints. From causal or intervention-style evaluation it takes: Controlled removal of evidence. Predictions about downstream structural fallout. However, the benchmark does not reduce to any one of those ingredients. The defining object is the cross-resolution compiler episode: A natural-language turn already has a public fine-grained semantic analysis. A hidden whole-turn analysis uses a different temporary symbol language. Support examples reveal how the two resolutions relate. Query compilation requires non-bijective operator behavior. The participant must expose the lineage connecting source and target. The same inferred lineage is then tested under intervention. The novelty claim therefore does not rest on opaque renaming alone. Opaque ciphers remove a shortcut. The substantive task is the combination of: Dual semantic resolutions. Episodic compiler induction. Explicit non-bijective lineage. Grounded argument rebinding. Whole-turn emergence. Counterfactual execution tests. The benchmark can be ablated along each axis. Those ablations are meaningfully different tasks. Ablation A: Fixed Global Ciphers Keeping U/V/K/R meanings fixed across episodes turns much of the task into ordinary supervised structured prediction. Ablation B: No Derivation Witness Scoring only the target register removes lineage induction. A system can reach the right macro inventory for the wrong reason. Ablation C: KEEP Only Removing FUSE, DROP, RISE, and REBIND reduces the task toward local label translation. Ablation D: No Grounding Removing TRACE coordinates eliminates the requirement to carry semantic arguments across resolution. Ablation E: No Counterfactual Probes Removing probes makes the derivation a static explanation rather than an executable law. The full challenge retains all five axes. Challenge Type This is a Fine-Tuning challenge. General-purpose pretrained sequence-to-sequence models are allowed. The intended solution family is compact learned encoder-decoder modeling under CPU constraints. Eligible models include: Small text-to-text transformers. Compact denoising encoder-decoder transformers. Pointer-augmented encoder-decoders. Copy-aware structured generators. Shared encoders with learned lineage heads. Graph-conditioned sequence decoders. Small neural rerankers over a bounded candidate beam. Participants may also train suitable neural models from scratch. ML-Only Requirement The primary prediction mechanism must be learned. Allowed learned components include: Sentence encoders. Turn encoders. Episode-local glyph embeddings. Support-query attention. Pairwise source-target compatibility heads. Operator classifiers. Coalescence heads. DROP heads. RISE heads. REBIND heads. TRACE boundary predictors. Autoregressive decoders. Learned candidate rerankers. Deterministic processing is allowed for: JSON parsing. Token-coordinate conversion. Structural validation. Canonical ordering. Masking impossible node references. Deduplicating impossible repeated IDs. Constrained decoding from neural scores. The following are not eligible as complete predictive systems: Handwritten semantic rules. Fixed source-to-target dictionaries. Regex decision trees. TF-IDF-only prediction. BM25-only prediction. Nearest-neighbor-only retrieval. Exact phrase lookup. Hard-coded operator templates. Manual test-specific mappings. Pretrained Model Limit Each pretrained model may contain at most 120 million parameters. The checkpoint must be general-purpose. Participants may: Fine-tune all model parameters. Freeze part of the encoder. Use low-rank adaptation. Use lightweight adapters. Continue training on released challenge text. Add compact learned structural heads. External task-specific semantic supervision is prohibited. External API inference is prohibited. Compute The execution environment provides: 10 CPU cores. 62.5 GiB RAM. No GPU. The task is designed around compact bounded episodes. Useful CPU strategies include: Pre-tokenizing episodes. Caching support representations. Freezing lower encoder layers. Short maximum sequence lengths. Gradient accumulation. Small beam widths. Pointer decoding for X/Y IDs. Candidate masks for valid V/R glyphs. Quantized inference where supported. One compact model or a very small ensemble. Large language models are not required. Released Dataset The challenge release is built from human-authored English customer-service turns with aligned sentence-level and whole-turn semantic observations. The public package contains: train.jsonl test.jsonl sample_submission.csv There is no official validation file. No public ontology file is required. Every episode contains all local symbol information needed for prediction. train.jsonl Each line contains one complete episode. sample_id Type: string. Unique submission key. The identifier is opaque. Do not use it as a predictive feature. support_a Type: object. Contains: sentences fused_text tokens micro_atoms macro_atoms derivation conservation support_b Uses the same structure. support_c Uses the same structure. query Contains: sentences fused_text tokens micro_atoms probes The query omits its whole-turn target representation. probes Type: list of strings. Example: ["P01 REMOVE X03","P02 CUT S02","P03 BLOCK ROOT"] Probe instructions are part of the public query. The hidden fallout sets are predicted in the PROBES block. target_sequence Training only. Contains: DERIVE block. REGISTER block. GROUND block. CONSERVE block. PROBES block. Sentence Objects Every sentence object contains: sid text Example: {"sid":"S02","text":"the balance still shows as unpaid"} Sentence order is original and public. The challenge does not involve sentence-order reconstruction. Micro Atom Objects Every micro atom contains: atom_id kind glyph home trace Example PULSE: {"atom_id":"X02","kind":"PULSE","glyph":"U04","home":"S01","trace":"-"} Example TRACE: {"atom_id":"X05","kind":"TRACE","glyph":"K09","home":"S03","trace":"T03:T05"} TRACE coordinates are local to the sentence view. Support Macro Atom Objects Support macro atoms contain: atom_id kind glyph home trace Their home is always: M00 Macro TRACE coordinates refer to the fused support-turn token tape. test.jsonl The test representation contains the same public fields except: target_sequence is omitted. The hidden evaluator retains the canonical query compiler result. The public package does not expose: Original human-readable semantic labels. Original source-domain names. Original conversation IDs. Original utterance IDs. Source split identifiers. Construction pairing keys. Original annotation filenames. Preparation hashes. Data Provenance The linguistic material consists of human-authored English customer-service interactions. The underlying material contains aligned semantic observations at sentence scale and complete-turn scale. The benchmark does not expose the original ontology names because those names are not part of the prediction problem. Instead, the challenge derives a new episodic transformation task by: Pairing aligned sentence-level and whole-turn observations. Converting them into source and target semantic atoms. Generating explicit compiler lineage. Constructing support/query episodes. Re-randomizing all visible semantic ciphers per episode. Canonicalizing target atom order. Adding conservation signatures. The language is therefore grounded in observed human conversations, while the compiler representation is challenge-specific. Why the Public Ontology Is Hidden Publishing ordinary human-readable semantic names would materially change the task. A model could rely on descriptive label wording rather than infer the episode-local compiler. The hidden source ontology is therefore treated as construction metadata rather than participant input. The released U/V/K/R alphabets preserve all structure needed to learn the benchmark while preventing semantic-name shortcuts. Official Split Construction The official split occurs before episode construction. Complete source conversations are assigned to one partition. All sentence-level and whole-turn derivatives of one source conversation remain on the same side. Only after this grouping are episodes generated. Temporary semantic ciphers are created after the split. This prevents: Conversation overlap. Alternate-resolution leakage. Cross-partition temporary-cipher reuse. Source-ID memorization. Support Selection Supports are selected from the same official partition as the query. They are chosen to provide partial local coverage. A support candidate is useful when it demonstrates at least one query-relevant property such as: A source glyph. A target glyph. An operator family. A TRACE role. A coalescence pattern. A RISE behavior. The support set is rejected when one support already reveals the complete query derivation pattern. This prevents direct demonstration copying. Query Difficulty Filtering Very easy queries are excluded from the hidden evaluation. A hidden query should normally contain: At least two source atoms. At least two target atoms or one non-trivial exceptional event. More than one sentence when available. At least one compiler behavior beyond a trivial one-to-one identity. The harder subset favors: FUSE. DROP. RISE. REBIND. Repeated source glyphs. Multiple TRACE candidates. Similar argument spans. Multi-sentence requests. Corrections. Ellipsis. Shared arguments. Several semantically related local atoms. Submission Format The submission contains exactly two columns: sample_id prediction Use sample_submission.csv exactly. Example: sample_id,prediction STSCI_example,"X01 KEEP Y01 X02+X04 FUSE Y02 X03 DROP VOID ROOT RISE Y03 X05 REBIND Y04 Y01 V06 Y02 V11 Y03 V02 Y04 R07 T09:T11 SRC=5 USED=4 DROP=1 ROOT=1 OUT=4 P01=Y02 P02=Y02,Y04 P03=Y03" Structural Validation A sample prediction is valid only when: Every public X atom appears exactly once as a source in DERIVE. No X atom appears in more than one derivation group. ROOT is used only with RISE. VOID is used only with DROP. KEEP has exactly one X parent. FUSE has at least two X parents. REBIND has exactly one TRACE parent. Every non-VOID Y appears exactly once in REGISTER or GROUND. Every V glyph appears only in REGISTER. Every R glyph appears only in GROUND. Every T coordinate exists in the query fused token tape. Grounded intervals have start <= end. The CONSERVE counts agree with the structural prediction. Every public probe ID appears exactly once in PROBES. Probe fallout values contain only predicted non-VOID Y IDs or NONE. BLOCK ROOT probes refer to no X atom. REMOVE probes refer to an existing X atom. CUT probes refer to an existing sentence ID. Malformed samples receive zero component credit for that sample. Other rows remain evaluable. Evaluation Submissions are evaluated using the Sentence-to-Turn Compiler Score from 0.01 to 100. Higher is better. The metric evaluates seven published components: Lineage Edge F1. Operator Macro F1. Target Register F1. Grounding IoU. Conservation Accuracy. Counterfactual Fallout F1. Exact Compile. There are no hidden metric components. A perfect prediction receives exactly 100. Lineage Edge F1 Convert every derivation relation into elementary lineage edges. Examples: X01 KEEP Y01 creates: X01-Y01 X02+X04 FUSE Y02 creates: X02-Y02 X04-Y02 X03 DROP VOID creates: X03-VOID ROOT RISE Y03 creates: ROOT-Y03 X05 REBIND Y04 creates: X05-Y04 Let: P = predicted lineage edge set G = gold lineage edge set Then: Precision = |P ∩ G| / |P| Recall = |P ∩ G| / |G| LineageEdgeF1 is the harmonic mean. If both sets are empty: LineageEdgeF1 = 1 The dataset-level component is the arithmetic mean across test episodes. Let: L = LineageEdgeF1 Operator Macro F1 Every source derivation group receives one operator label: KEEP FUSE DROP RISE REBIND Normalize each operation by its sorted parent set and target reference. Compare predicted and gold operations as labeled structured items. Compute F1 independently for each operator family. Then average the five operator F1 values. This gives equal importance to rare structural behaviors such as RISE and REBIND. Let: O = OperatorMacroF1 Target Register F1 Represent every predicted target atom as: (kind, target_glyph, canonical_Y_position) TRACE coordinates are ignored for this component. Compare predicted and gold target atom multisets. Compute multiset precision and recall. Then compute F1. This rewards recovering the whole-turn semantic inventory even when one grounding boundary is imperfect. Let: R = TargetRegisterF1 Grounding IoU For every gold TRACE target atom: Match a predicted TRACE using canonical Y position and target R glyph. Compare inclusive token spans. Compute token Intersection over Union. For predicted span: T09:T11 and gold span: T10:T12 the overlap contains: T10 T11 The union contains: T09 T10 T11 T12 Therefore: IoU = 2 / 4 = 0.5 Unmatched gold TRACE atoms receive zero. Extra predicted TRACE atoms receive no positive credit. If a sample contains no gold TRACE atoms: Grounding credit is 1 when no TRACE is predicted. Otherwise grounding credit is 0. Average over samples. Let: G = GroundingIoU Conservation Accuracy The evaluator recomputes: SRC USED DROP ROOT OUT from the predicted derivation. For each field, award one point when the submitted CONSERVE value matches the recomputed value and the recomputed value also matches gold. The sample Conservation Accuracy is: correct conservation fields / 5 Average across test episodes. Let: C = ConservationAccuracy This component rewards globally coherent compiler execution. Counterfactual Fallout F1 For every public probe, compare the predicted fallout Y set with the gold fallout set. Let: P = predicted fallout set G = gold fallout set Then: ProbePrecision = |P ∩ G| / |P| ProbeRecall = |P ∩ G| / |G| ProbeF1 is their harmonic mean. If both fallout sets are empty: ProbeF1 = 1 If only one is empty: ProbeF1 = 0 The sample Counterfactual Fallout score is the arithmetic mean across its public probes. The dataset-level value is then averaged across test episodes. Let: F = CounterfactualFalloutF1 Derivation-Consistency Check The evaluator also recomputes the fallout implied by the submitted DERIVE block. A probe receives zero credit when the submitted fallout contradicts the participant's own derivation, even if the listed Y set accidentally overlaps the gold answer. For example: Submitted derivation: X01+X02 FUSE Y01 Public probe: P01 REMOVE X02 Under published strict-support semantics, Y01 must fail. If the submitted PROBES block says: P01=NONE that probe receives zero credit. This rule prevents the probe block from becoming an independent classification head disconnected from the predicted compiler. Why Fallout F1 Is Separate from Lineage F1 Lineage evaluates the observed query compilation. Fallout evaluates the consequences of that compilation under intervention. A model can recover many correct edges while still misunderstand whether a target requires: One parent. All FUSE parents. ROOT. A particular sentence's evidence. The probe score therefore measures a different property: causal execution of the inferred derivation. Exact Compile ExactCompile for one query is 1 only when all normalized output structures match: Complete lineage. Complete operator assignments. Complete target register. Exact target TRACE spans. Exact conservation signature. Exact normalized counterfactual fallout for every public probe. Otherwise: ExactCompile = 0 The dataset-level value is the fraction of exactly solved queries. Let: X = ExactCompile Final Score Define the compiler core as: CompilerCore = (L × O × R)^(1/3) Define the execution geometry as: ExecutionGeometry = (G × C × F)^(1/3) The final score is: Sentence-to-Turn Compiler Score = 100 × CompilerCore^1.35 × (0.45 + 0.40 × ExecutionGeometry + 0.15 × X) The result is clipped to: [0.01, 100] For a perfect prediction: L = 1 O = 1 R = 1 G = 1 C = 1 F = 1 X = 1 Therefore: CompilerCore = 1 ExecutionGeometry = 1 Final Score = 100 The compiler exponent makes correct transformation structure central. The execution geometry now includes grounding, global conservation, and counterfactual behavior. This means a static derivation that cannot survive intervention testing is not treated as a fully understood compiler. The exact term rewards fully solved episodes without reducing the benchmark to exact string match. Reproducing the Metric Locally For every validation episode: Parse DERIVE. Validate every source atom. Validate operator arity. Validate ROOT and VOID usage. Parse REGISTER. Parse GROUND. Parse CONSERVE. Canonicalize parent groups. Expand derivations into elementary lineage edges. Compute Lineage Edge F1. Group normalized derivations by operator family. Compute per-operator F1. Macro-average the five operator scores. Build target atom multisets. Compute Target Register F1. Match target TRACE atoms. Compute token-span IoU. Recompute the five conservation fields. Compare them with both prediction and gold. Compute Conservation Accuracy. Execute each public probe against the predicted derivation. Verify that the submitted PROBES block is self-consistent. Compare predicted and gold fallout sets with F1. Average probe scores to obtain Counterfactual Fallout F1. Compare the complete normalized compiler outputs, including probe fallout. Compute Exact Compile. Average all published components across the evaluation set. Compute CompilerCore. Compute ExecutionGeometry. Apply the published final formula. Clip to [0.01, 100]. The provided grader.py implements this procedure directly. Intended Modeling Approaches The task can be approached as direct text-to-structure generation or as a hybrid learned compiler. Direct Encoder-Decoder Fine-Tuning A simple baseline can serialize: Support A source view. Support A target view. Support A derivation. Support B source view. Support B target view. Support B derivation. Support C source view. Support C target view. Support C derivation. Query source view. The model generates the complete query target envelope. Episodic Glyph Binding A stronger model can explicitly build temporary representations for: U glyphs. V glyphs. K glyphs. R glyphs. Those representations can be computed from all support occurrences. The query atoms then attend to the temporary glyph representations. This makes the architecture reflect the episode-local nature of the task. Learned Lineage Matrix A model may score: Every X-to-Y candidate. Every X-to-VOID candidate. ROOT-to-Y candidates. The resulting matrix can feed: An operator classifier. A constrained decoder. A graph-aware reranker. Operator Heads Separate learned heads can predict: KEEP probability. FUSE membership. DROP probability. RISE probability. REBIND probability. These heads can provide auxiliary losses even when the final output is generated autoregressively. TRACE Boundary Heads TRACE targets can use dedicated start and end classifiers over fused-turn tokens. The resulting span scores can condition GROUND generation. Neural Constraint Reranking A compact beam of candidate compiler outputs can be reranked by a learned model using: Support consistency. Query language compatibility. Operator plausibility. Conservation coherence. Target register likelihood. Counterfactual probe agreement. Deterministic validity checks are allowed after learned scoring. Intervention-Aware Training Public probe instructions can also be used during training. A model may: Encode the unmodified query once. Predict the primary derivation. Apply learned or differentiable source-atom masks for each probe. Predict the target fallout set. Penalize disagreement between primary lineage and probe behavior. The final submission remains one serialized sequence. Participants are not required to build a differentiable symbolic executor. A standard seq2seq model can simply generate the PROBES block jointly with the rest of the output. Auxiliary Supervision Participants may derive additional labels from released training outputs. Useful auxiliary objectives include: Source atom usage. X-to-Y edge prediction. Pairwise source coalescence. Operator family. Target atom count. DROP count. RISE count. TRACE target glyph. TRACE start coordinate. TRACE end coordinate. Conservation fields. Temporary source-to-target glyph affinity. Probe fallout membership. Probe self-consistency. Intervention-sensitive target survival. All auxiliary supervision must come from released training episodes. Expected Baseline Behavior A direct encoder-decoder should learn: Output grammar. Common operator patterns. Some temporary cipher binding. Basic one-to-one transformations. It should struggle more on: Novel FUSE compositions. Rare RISE cases. REBIND cases. Similar temporary glyphs. Long multi-sentence query turns. Several plausible TRACE boundaries. A stronger structured model should improve by explicitly learning lineage and operator behavior. Partial-Solution Plateaus The challenge is designed so several shortcuts plateau. Global Cipher Memorization Fails because ciphers are re-randomized per episode. One-to-One Translation Fails on FUSE, DROP, RISE, and REBIND. Support Copying Fails because the query derivation is not copied verbatim from any support. Macro-Only Prediction Loses Lineage and Operator credit. Lineage-Only Prediction Loses Target Register and Grounding credit. Span Copying Fails when TRACE semantics rebind under whole-turn interpretation. Generic Seq2Seq Generation Can produce valid-looking output but loses heavily when the compiler structure is wrong. Static Graph Guessing A model can sometimes predict a plausible lineage graph without learning what that graph implies. Counterfactual probes expose this failure. The predicted graph must produce the correct fallout after REMOVE, CUT, and BLOCK ROOT interventions. Hardness Controls The hidden evaluation can be tuned without changing the public task. Difficulty is controlled through: Number of source atoms. Number of target atoms. Number of sentences. Fraction of non-KEEP operators. Frequency of repeated temporary glyphs. Number of TRACE atoms. Number of plausible TRACE boundaries. Support coverage. Degree of support/query lexical similarity. Number of query behaviors requiring evidence from multiple supports. Probe interventions that strike high-degree FUSE parents. Sentence CUT probes affecting several candidate target atoms. BLOCK ROOT probes in episodes containing both RISE and non-RISE targets. The intended hidden test emphasizes non-trivial compositions and intervention-sensitive lineages. CPU Feasibility The challenge remains practical on CPU because each episode is compact. The task does not require: Long document context. Retrieval over a large external corpus. Large-scale beam search. Huge output vocabularies. Most outputs consist of: A small number of X/Y identifiers. A small temporary cipher vocabulary. A small operator vocabulary. Short token coordinate strings. Participants can therefore devote model capacity to learning the transformation rather than generating long prose. Validation and Leakage The complete episode is the atomic unit. Do not split: Supports. Query. Temporary glyph mappings. Derivation tapes. Grounding labels. across local train and validation partitions. Doing so would leak the episode-specific compiler. For more realistic local validation: Keep complete source-conversation groups together. Regenerate local temporary ciphers after splitting. Avoid support/query reuse across folds. Allowed Resources Participants may use: Released challenge files. General-purpose pretrained seq2seq checkpoints within the parameter limit. Associated tokenizers. Standard neural-network libraries. Standard numerical libraries. Public model architecture code. Auxiliary labels derived from released targets. Learned constrained decoding. CPU quantization. Small neural ensembles. Disallowed Resources Participants may not use: Hidden evaluator files. Manual test annotation. External task-specific service annotations. External semantic parsers as the primary predictor. Fixed human-readable translations of U/V/K/R symbols. Hard-coded test derivations. Hard-coded target registers. sample_id as a predictive feature. Source-file ordering as a predictive feature. Submission-feedback reconstruction. Rule-only predictive systems. TF-IDF-only systems. BM25-only systems. Nearest-neighbor-only systems. Limitations The language is English customer-service interaction. The temporary compiler representation is a challenge-specific abstraction. The benchmark does not claim that KEEP, FUSE, DROP, RISE, and REBIND form a universal theory of semantics. They are operational categories describing how two aligned annotation resolutions relate inside this benchmark. Some language can support several reasonable semantic interpretations. The released benchmark nevertheless uses one deterministic target derived from the paired source annotations. The benchmark does not evaluate: Open-ended response generation. Web retrieval. Tool use. Persistent dialogue state. Long-form reasoning. Speech processing. Current factual knowledge. It evaluates learned cross-resolution transformation under a temporary episode-local semantic system. Expected Outcome A successful system should learn to: Read several worked source-to-target transformations. Infer a temporary local semantic dialect. Transfer that dialect to a new query. Recover source-to-target lineage. Detect semantic fusion. Detect semantic suppression. Detect whole-turn emergence. Detect argument rebinding. Recover the target semantic register. Predict exact whole-turn token grounding. Produce a globally consistent conservation signature. Predict which target meanings fail after controlled evidence removal. Keep counterfactual answers consistent with the submitted derivation. Execute all of the above efficiently with a compact CPU-friendly model. &nbsp;
> $700 Pool
> Closes in 2h 15m
> 12 / 12 continuing slots

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Stomatal Spatial Merge Barcodes

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74ztdvanaspq366jw7sp970x8e0znz
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.681!

Full challenge description from page:

> Background Understanding the spatial distribution of stomatal complexes on plant leaves is critical for analyzing transpiration, photosynthesis, and drought resilience. While traditional segmentation models identify isolated guard cells or pores, extracting higher-order biological patterns requires summarizing the spatial relationships between these structures. Persistent homology offers a mathematical framework to track how individual stomata connect into larger structural components at varying spatial thresholds, providing an abstract "barcode" of the tissue's geometric organization. Overview Given a high-resolution micrograph crop of a sorghum leaf, infer a spatial merge barcode summarizing the human-annotated stomatal complexes. The target is not a pixel mask or a bounding box. Instead, it is a variable-length multiset of [birth, death] intervals. Each stomatal complex enters the geometric graph at a size-dependent "birth" threshold, and merges with neighboring components based on spatial proximity, yielding a zero-dimensional persistence barcode. This summarizes the spatial distribution pattern of the leaf without inferring physical tissue connectivity or conductance. This is a CPU-only challenge with strict offline limits (at most 10 CPU cores, 62 GB RAM, and a 90-minute limit). You must fine-tune a pretrained image model using only the supplied public training crops and barcode pairs. Dataset Information (Public Files) The dataset comprises perturbed sorghum micrographs and their derived spatial barcodes. All files necessary for development and local evaluation are located in the public directory. Images are $384 \times 384$ RGB JPEGs. +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | images/ | Directory of 384x384 RGB leaf micrographs. | | train.csv | Labeled training queries with target barcode arrays. | | test.csv | Unlabeled evaluation panels. | | sample_submission.csv | Format-example rows for test IDs. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +------------+---------+---------------------------------------------------------------+ | Column | Type | Description | +------------+---------+---------------------------------------------------------------+ | id | String | Opaque unique example identifier. | | image | String | Relative path to the RGB micrograph crop. | | barcode | JSON | (train only) Array of [birth, death] float intervals. | +------------+---------+---------------------------------------------------------------+ Geometry and Target Definitions The target barcodes are derived mathematically from human-annotated complex-area polygons: Birth Generation: Let $A_i$ be a polygon's shoelace area (in native pixels). Vertex $i$ enters the graph at a birth value: $b_i = 0.1 \times (1 - \min(\sqrt{A_i} / 128, 1))$. Edge Formation: For every pair of complexes $(i, j)$ with shoelace centroids $p_i, p_j$, an edge enters at $\max\left(b_i, b_j, \frac{\Vert{}p_i - p_j\Vert{}}{1024\sqrt{2}}\right)$. Merge Logic: When components merge, the component with the earlier (lower) minimum vertex birth survives (ties broken by native annotation order). Interval Creation: A finite interval [birth, death] is recorded for the younger component when its lifetime (death - birth) exceeds $1e-10$. The final essential (infinite) component is discarded. Generalization & Leakage Controls Genotype Splitting: All images of a specific genotype and its three biological replicate groups are held out for testing. The remaining genotypes form the training data. Overlapping crops and image variants strictly remain within their respective split. Target Robustness: Boundary-truncated complexes and degenerate annotations are explicitly excluded from the targets. Perturbations: Images receive deterministic light corruption on normalized [0,1] intensities: gain 0.95–1.05, offset ±0.01, sinusoidal amplitude 0.002, Gaussian standard deviation 0.008–0.018, zero or one directional smoothing pass with weight 0.02–0.05, and 0–2 light or dark patches with half-sizes 1–4 pixels and intensity changes 0.02–0.05. Gamma is 0.98–1.02 after clipping. JPEG quality is 96 without chroma subsampling. Spatial geometry and targets are unchanged. Evaluation Metrics The evaluation metric is Persistence Wasserstein Recovery. It calculates the minimum total cost of matching the predicted barcode intervals to the ground-truth intervals using an augmented Hungarian assignment algorithm. 1. Cost Calculation Direct Matching: The cost of matching a predicted interval $(b_{\text{pred}}, d_{\text{pred}})$ to a gold interval $(b_{\text{gold}}, d_{\text{gold}})$ is computed using the $L_\infty$ distance: $$\text{Cost} = \max(\vert{}b_{\text{pred}} - b_{\text{gold}}\vert{}, \vert{}d_{\text{pred}} - d_{\text{gold}}\vert{})$$ Diagonal Matching (Unmatched Penalty): An unmatched predicted or gold interval is matched to the diagonal (effectively discarded) at a cost of: $$\text{Cost} = \frac{\text{death} - \text{birth}}{2}$$ 2. Wasserstein-1 ($W_1$) Distance The total loss for a row is the minimum sum of matching costs ($W_1(\text{pred}, \text{gold})$) over all possible assignments between predictions and ground truth. 3. Row Score Let $W_1(\text{empty}, \text{gold})$ be the cost of predicting an empty barcode (matching all gold intervals to the diagonal). The row score normalizes the prediction loss: $$\text{Score} = \max\left(0, 1 - \frac{W_1(\text{pred}, \text{gold})}{W_1(\text{empty}, \text{gold})}\right)$$ The final competition score is the arithmetic mean of all row scores. Scores range from $0.0$ to $1.0$ (higher is better). An exact or order-permuted prediction scores $1.0$. An empty barcode prediction [] scores $0.0$. Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,barcode. Include one row per test ID. id,barcode 1a2b3c4d5e6f7g8h9i0j,"[[0.03, 0.12], [0.02, 0.31]]" Parsing Bounds & Rejection: - barcode must be a JSON list of at most 64 [birth, death] pairs. - Values must be finite numerics satisfying $0 \le \text{birth} - The JSON cell is bounded at 8,192 characters. - A malformed barcode receives a score of 0.0 for that row. - Wrong/reordered columns, missing/extra IDs, or duplicate IDs invalidate the entire submission resulting in a final score of 0.0. Row and interval order are irrelevant. What Not To Use To ensure a fair and reproducible benchmarking environment: No External Data: Do not use raw image/annotation files, external datasets, or outside text corpora. Train and select using public training examples only. No Private Labels: Do not access or derive hidden complex centers, areas, or hidden identifiers. Hardware Execution Limits: The submitted solution must execute completely within the strict offline CPU constraints (at most 10 CPU cores, 62 GB RAM, 90 minutes). Pre-trained Weights: task-specific fine-tuning must occur within the evaluation runtime. &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

## Articulatory Coordination Loops

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fvd77v9nxdtmakfwz2bnr6s8e9ra9
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shubhangg's score of 0.236!

Full challenge description from page:

> Background During speech, the human vocal tract's articulators (lips, jaw, and tongue) move in highly coordinated, coupled trajectories. Inferring these hidden physical movements directly from the acoustic speech signal is a complex inverse problem. Rather than predicting absolute anatomical point coordinates or phoneme labels, this task focuses on the coupled geometry of these movements. Models must predict how pairs of articulator distances trace closed loops (excursion direction and shape) over a short time window. Overview Predict the coupled geometry of lip, jaw, and tongue movements from a short speech recording. Your target is a six-coordinate signed-area signature describing how pairs of articulator-distance trajectories move around one another. You must fine-tune a pretrained acoustic or general representation model using the provided training examples. This is an offline, CPU-only challenge. Inference and structured decoding must execute within an isolated session using at most 10 host CPU cores, 62 GB of RAM, and a strict 90-minute runtime budget. Pretrained weights may be acquired beforehand. All data originates from elicited recordings of a single speaker utilizing a repeated carrier sentence across various vowel and consonant families; it evaluates narrow coordination geometry, not new-speaker generalization or clinical diagnostics. Dataset Information (Public Files) All assets necessary for training and evaluation are provided in the public directory. The input audio files are cropped, mildly distorted 16 kHz recordings. +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | audio/ | Directory containing 1.2-second 16 kHz mono PCM16 WAV files. | | train.csv | 1,158 training examples with 6-coordinate target signatures. | | test.csv | 418 evaluation queries requiring a signature prediction. | | signature_schema.json | Metadata detailing the fixed coordinate pair order. | | sample_submission.csv | Format-example rows demonstrating the required JSON output. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +-----------+--------+-----------------------------------------------------------------+ | Column | Type | Description | +-----------+--------+-----------------------------------------------------------------+ | id | String | Opaque unique identifier for the specific audio crop. | | audio | String | Relative path to the audio file (audio/.wav). | | signature | JSON | (Train only) Array of six finite real numbers in [-1, 1]. | +-----------+--------+-----------------------------------------------------------------+ Audio Perturbations Every audio file contains exactly 19,200 samples (1.2 seconds). To test robustness, the audio has been subjected to deterministic perturbations: Gaussian noise at $0.008$ times the clean clip RMS. Sinusoidal interference at $0.006$ times RMS and 50/100/150 Hz. Random gain scaling between $0.85$ and $1.15$. Mild $\tanh$ amplitude distortion. Monotone temporal warp of at most $0.003$ of the clip span. Target Definition (The Geometric Signature) The target signature represents the signed area of closed polygons formed by pairs of articulator distances. 1. Distances Four Euclidean distances are calculated relative to the upper-lip: 0: Lower lip 1: Jaw 2: Tongue tip 3: Tongue dorsum 2. Coordinate Pairs The signature consists of six elements corresponding to the following pairs: [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]. 3. Mathematical Construction For each distance pair $(i, j)$, 120 consecutive points (spanning 1.19 seconds) are plotted in a 2D plane where distance $i$ is the horizontal axis ($x$) and distance $j$ is the vertical axis ($y$). The 120-point polygon is mathematically closed with a straight chord from the last point to the first. Let $C$ be the sum over the closed consecutive points of the cross product: $$C = \sum (x_k y_{k+1} - y_k x_{k+1})$$ Let the total variations $TV_x$ and $TV_y$ be the sums of the absolute coordinate differences over the closed polygon (including the closing chord): $$TV_x = \sum \vert{}x_{k+1} - x_k\vert{}$$ $$TV_y = \sum \vert{}y_{k+1} - y_k\vert{}$$ The final target coordinate for that pair is normalized as: $$\text{Target} = \frac{2C}{TV_x TV_y}$$ This yields a value in the range $[-1, 1]$. Positive values denote a positive signed area. Evaluation Metrics Submissions are evaluated using Lin's Concordance Correlation Coefficient (CCC). For each of the six coordinates, the CCC is computed across all test examples to measure both correlation and absolute magnitude agreement between the prediction ($p$) and the reference ($r$): $$\text{CCC} = \frac{2 \cdot \text{cov}(p, r)}{\text{var}(p) + \text{var}(r) + (\text{mean}(p) - \text{mean}(r))^2}$$ (Note: Population moments are used for variance and covariance.) The final score is the arithmetic average of the six coefficients, clamped to the range $[0, 1]$. Higher is better. Perfect answers score $1.0$. A positively correlated prediction with a poorly scaled magnitude loses credit. A constant prior against a nonconstant reference scores $0.0$. Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,signature. Include exactly one row per test ID. The signature column must contain a JSON array of exactly six finite real numbers in the range $[-1, 1]$. Standard CSV quoting is required around the JSON array. id,signature 1a2b3c4d5e6f7g8h9i0j1k2l,"[0.08, -0.02, 0.11, 0.03, -0.01, 0.05]" Parsing Bounds & Rejection - Missing, extra, duplicate, or unknown IDs, or wrong columns invalidate the whole submission and score 0.0. - A malformed JSON array, an array with a length other than 6, or arrays containing booleans, non-finite values, or values outside $[-1, 1]$ will invalidate the entire file and result in a global score of 0.0. What Not To Use To ensure a rigorous evaluation of coordination geometry learning: No Source Lookup: You must not attempt to reconstruct source IDs, perform hidden test label lookups, or access the native, uncorrupted recordings from the original corpus. No External Kinematic Supervision: Public training data is the only permitted source of task-specific supervision. Do not use private electromagnetic articulography (EMA) recordings or external phonetic-to-articulatory datasets. Offline Execution: The solution must execute completely offline with no internet access, API calls, or manual annotations during inference. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it frames adaptation, unlearning, or domain-specialized behavior as measurable supervised outputs.

