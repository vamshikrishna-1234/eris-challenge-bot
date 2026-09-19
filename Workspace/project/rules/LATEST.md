# Rules — current expectations (read this)

**Primary reference:** `challenge_template_file_creation.txt` — it tracks the **live** platform challenge-creation form.

## Score bounds vs. sample-grade validation (BACKUP STEP — apply when a discrepancy arises)

The platform runs TWO independent pre-submission checks that can fight each other:

- **Grade Sample Validation** — runs `grade.py` on `sample_submission.csv`; FAILS if the sample scores at (or effectively at) the declared theoretical minimum. The sample must be a valid, NON-DEGENERATE baseline that scores comfortably above the minimum (accepted challenges' samples land ~0.12–0.17; aim for ≥ ~0.12).
- **Grade Script Score Bounds** — independently verifies the declared theoretical minimum/maximum equal what `grade.py` can ACTUALLY return. If the grader can output 0.0 (empty/invalid/id-mismatched submission) it expects the declared minimum to be 0; declaring any other minimum fails with e.g. "Expected minimum score to be 0, but got 0.0909…".

**Two ways to satisfy both (pick one and keep it consistent EVERYWHERE — description prose, formula, theoretical-min field, platform config, and the grader code):**

1. **Preferred — keep min = 0.0, lift the sample.** Declare min 0.0 / max 1.0, and make the sample submission score well above 0 using LABEL PRIORS only (median count, median/mean of continuous targets, a spread layout — never an all-empty submission). If an over-harsh partial-credit shaping (e.g. squaring every sub-score, `SCORE_POWER=2.0`) crushes an honest baseline below ~0.1, soften the power (e.g. 1.6): verify by a sweep that oracle=1.0, strong-solver<0.7, and sample≥~0.12 all hold together.
2. **Reliable backup — floor the grader at the declared minimum.** Add a `FLOOR_SCORE` constant and make EVERY return path (invalid/empty included) and the final clip return `np.clip(final, FLOOR_SCORE, 1.0)`, so the grader's real range is exactly `[FLOOR_SCORE, 1.0]`. Then declare that same `FLOOR_SCORE` (e.g. `1/11 = 0.09090909090909091`) as the theoretical minimum everywhere. This makes both checks pass because the declared bound now matches the grader's actual minimum. Trade-off: invalid submissions no longer score 0 — acceptable when the platform gate requires it, but prefer option 1 if reviewers want strict-zero on invalid.

**To find the right sample target empirically:** prepare an ALREADY-ACCEPTED challenge locally and grade its `sample_submission.csv` — that number is the passing floor to match.

## Rubrics (important)

**Evaluation rubrics are removed.** Do not add a “Rubrics” / “Evaluation rubrics” section to `CHALLENGE_FORM_FILL.md` or other challenge deliverables. The form no longer asks for them.

If other files in this `rules/` folder (e.g. `dataset and challenge.txt`, `intro and datasets.txt`) still mention “5+ rubrics” or rubric types, treat that as **outdated** — it is kept for historical context only.

## New / notable (challenge form)

- **“What not to use”** — list ML techniques or libraries solvers should avoid; misuse can lead to solution rejection.
- **Enforcement on invalid approaches** — rule-only solutions or approaches that do not match the challenge domain (e.g. a fine-tuning challenge solved with heuristics) may be rejected before payout. Intent is to reward genuine learning, not score-chasing shortcuts.

## Unchanged (still in effect)

- Difficulty, title (title case), full problem description, tags, grading config, theoretical min/max, custom `grade.py`, GPU tier (A10G default; H100 for LLM train/finetune).
- `prepare.py`: deterministic split into `public/` and `private/answers.csv` as documented elsewhere.

## Raw dataset upload for synthetic generated datasets

Current platform behavior for synthetic generated datasets: upload **two source files** in the dataset Data Files / Source Files area:

- `generate.py`
- `raw_upload.zip`

The uploaded `raw_upload.zip` should still be **flat internally**: archive members should be the raw corpus files directly, such as `scenes.csv`, `images/`, `videos/`, `LICENSE.txt`, or equivalent. Do not put `raw_data/`, the challenge repo folder, `public/`, `private/`, caches, or source code inside the zip.

After platform rebuild, the dataset file tree may be displayed as top-level `generate.py` plus an extracted `raw_upload/` directory. Therefore `DATASET_FORM_FILL.md` should describe this validator-visible layout, and `prepare.py` should handle `raw/raw_upload/scenes.csv` as well as local organizer layouts such as `raw/scenes.csv`.

For non-generated or legacy real-data uploads, the same flat-zip principle applies unless the dataset form and `prepare.py` explicitly document a different platform-visible directory layout.

## Dataset creation form (`DATASET_FORM_FILL.md`) — what belongs there

In the dataset form, describe **what the corpus is**: overview, platform-visible source-file structure, columns, license, source, and notes. For synthetic generated datasets, include `generate.py` and the extracted `raw_upload/` tree in the File Structure section because the validator checks these files directly after rebuild.

**Learning (reviewer-confirmed):** The dataset description must **never** reference `grade.py`, `prepare.py`, scoring mechanics, train/test split logic, or how the data will be consumed downstream. It is still a data-dictionary document; mentioning `generate.py` as corpus provenance and source-file structure is allowed for synthetic generated datasets.

## Source reversibility and public-corpus lookup leaks

If the upstream source is public or can be named from the dataset card, the prepared public split must not be reversible back to raw rows, source files, timestamps, annotation ids, original subjects/speakers, or hidden labels. This applies even when the license is valid and even when the raw source itself is allowed to be redistributed.

Common failure modes reviewers have repeatedly caught:

- Participant-facing prose names enough source/subset details to identify hidden test rows.
- Public CSVs expose original filenames, meeting ids, speaker ids, timestamps, segment ids, source hashes, raw row order, or split groups.
- Public text windows are verbatim source text and can be searched in public annotation files.
- Public audio/video/image clips are exact raw slices or crops and can be fingerprinted against public media.
- `prepare.py` or form prose describes held-out construction, exact preprocessing transforms, generator rules, noise rates, or other private evaluation design.
- Calibration/support examples in public test contain labeled versions of scored test targets.

Required preventive check: `_analyze.py` should include a source-lookup or reversibility stress test appropriate to the domain. Examples include exact transcript search against source annotations, filename/timestamp pattern scans, raw-id/source-id column scans, nearest-neighbor/retrieval baselines, public metadata-only baselines, and simple media fingerprint checks. If the source can still recover hidden rows, redact, re-encode, de-identify, aggregate, salt, or transform the public artifacts before submission while preserving the modeling signal.

## Prepared split size and source-family stability

**Learning (repeat mistake to avoid):** for grouped real-data challenges, especially image/map/audio/document tasks with hidden worst-group scoring, abstention, or strict high-score caps, a small prepared split is not stable enough for approval even when local checks pass. Do not ship splits like `63` train rows and `27` test rows, or hidden tests made from only around `9` source maps/files/subjects with a few variants each. Also do not treat a marginal repair such as `316` train rows and `136` test rows as review-ready for image/map challenges when the raw source can support a larger package.

Concrete rule: enforce explicit minimums in `prepare.py` for train rows, test rows, train source families, and test source families. For image/map grouped challenges, target roughly `1000+` train rows and several hundred test rows when feasible under the upload/runtime limits. Increase independent source records first, not just variants. Variants are useful for coverage, but they do not replace enough independent held-out source families.

## Challenge description formatting — tables and sections

**Learning (repeat mistake to avoid):** Reviewers flag "tables missing" if column definitions are written as bullet-point lists instead of proper markdown tables. Every challenge description **must** include tables for:

- File overview of `public/` contents (Item | Description)
- `train.csv` column definitions (Column | Type | Description)
- `test.csv` column definitions (Column | Type | Description)
- Submission format (Column | Type | Constraint)

Keep all table cells under ~30 characters. Use `|---|---|---|` separator style.

**Learning (repeat mistake to avoid):** Do **not** include a "What makes this challenging" section. Reviewers consider it unnecessary and have explicitly flagged it for removal. The difficulty should be self-evident from the task specification.

## Raw upload size budget — **stay well under the platform cap**

**Learning (repeat mistake to avoid):** the platform rejects raw-data uploads larger than **100 GB**, and an organiser disk also has to hold the materialised `raw_data/` to package it. So when `generate.py` pulls from a giant primary source (TCIA, NIH ChestX-ray, etc.), the script must shrink the corpus to a defensible-but-bounded slice **before** packaging — do not ship a `generate.py` whose default behaviour produces a 100+ GB folder.

Concrete rules every `generate.py` must satisfy:

- Have a **non-zero default** for `--max-patients` / `--max-samples` etc., chosen so the resulting `raw_data/` is at most ~tens of GB (target the upload to ≲50 GB; never plan for >90 GB).
- Resize images to a sensible long-edge cap (`--max-edge`, e.g. 1024 px for mammograms) before PNG/JPEG encoding. Native DICOM / 4 k+ images cost 30–60× more disk than the resized version and almost never improve agent task performance vs. the resized version.
- Stream-decode each per-series archive to its final image, then **delete the per-series ZIP** so peak working-disk = one series at a time.
- Document the resulting size budget in `DATASET_FORM_FILL.md` (`Notes:` section) — e.g. "default settings produce ~2.4k images, a few GB total". **Do not** advertise "163 GB if you fetch everything" as the headline number; that signal scares reviewers and may trigger "this challenge can't be uploaded" rejections.

### Minimal-but-novel sizing (the platform server stalls on multi-GB uploads)

**Learning (repeat mistake to avoid):** even within the 100 GB cap, the platform raw-upload server **stalls on multi-GB archives**. Default `generate.py` settings should target **≤ ~2 GB** for the upload, not the full upstream corpus. The novelty axes (paired-view reasoning, vendor-shift robustness, decoy linkage, etc.) almost always depend on **diversity** (number of patients / classes), not on **per-image resolution** or **total volume**. Trim aggressively along these axes and keep diversity:

- **Cap entities, not just images.** Patient-level / class-level caps (e.g. `--max-patients`, `--max-per-class`, `--max-images-per-patient`) preserve diversity while shrinking the dataset linearly.
- **Resize hard.** Medical CV tasks usually retain everything they need at long-edge **384–1024 px** (768 is a good default for X-ray / mammogram; 384 is fine for OCT B-scans). Native DICOM / 4 k+ images cost 30–60× more disk than the resized version.
- **Pick defaults that yield a sub-GB to ~2 GB upload.** Examples that worked in this repo: mammography 200 patients × 768 px ≈ ~0.3-0.8 GB; OCT 800 per class × 384 px ≈ ~0.1-0.25 GB; chest X-ray 800 patients × 8 images × 768 px ≈ ~1-2 GB.
- **Document the budget in `DATASET_FORM_FILL.md`** as the headline ("defaults yield ~5-6k images, ~1-2 GB"), not as a footnote.

If a challenge **needs** the full corpus to be valid (rare), say so explicitly in the dataset form and provide a downsampling fallback.
