# Project Eris Solver Rule Checklist

Source: Project Eris Solver Guidebook Google Doc, last checked 2026-07-10.

This is a distilled operational checklist, not a verbatim copy of the guidebook. If the source guidebook changes, update this file and `update-log.md`.

## Order Of Authority

- Read the specific challenge instructions first.
- Real challenge-specific restrictions override this general checklist.
- User/local rules can be stricter than the guidebook.
- When rules conflict, follow the stricter rule unless a reviewer explicitly confirms otherwise.
- If unsure whether a challenge note is real or leftover boilerplate, ask a reviewer before submission.

## Environment And Libraries

- Submitted scripts run in the Kaggle Docker image.
- Use only libraries already available in that image.
- Do not `pip install`, `conda install`, `apt install`, clone repos, vendor package code, or depend on helper plugins unless reviewers explicitly approve.
- If a missing package is truly necessary, ask reviewers first.
- General-purpose pretrained/backbone weights may be allowed by the guidebook when loaded directly in the submitted script through installed tooling such as timm or Hugging Face.
- Do not use self-hosted, challenge-specific, private, gated, or previously fine-tuned weights.
- For tasks where the user or challenge says offline/no downloads, obey that stricter rule and use only local/runtime-available weights or train from scratch.

## Data Rules

- Use only the provided challenge data, plus allowed general-purpose pretrained weights when permitted.
- Do not bring external datasets, mirrors, annotations, source files, lookup tables, or extra training data.
- Do not generate synthetic data and train on it.
- Label-preserving augmentation of provided training samples is allowed.
- Do not reverse-engineer source filenames, hashed ids, row order, generator seeds, hidden labels, or private answers.
- Do not key predictions by id, filename hash, row position, or memorized answer tables.

## Training Must Happen In The Submission

- Real ML training or fine-tuning must happen inside the submitted script.
- An inference-only trick is not enough.
- Do not train locally, upload your own fine-tuned weights somewhere, then load them in the submission.
- Hyperparameter search or ensembling inside the single submitted script is allowed if it fits runtime.
- Avoid hardcoding parameters discovered offline when the script could learn or tune them from train/OOF.

## Test Set Usage

- Use the test set only for genuine per-sample or per-batch inference.
- Test-time augmentation is allowed when it is fixed in advance and inference-only.
- Do not use pseudo-labeling, self-training, test-time adaptation, test-distribution calibration, or reweighting from aggregate test predictions/statistics.
- Do not fit scalers, PCA, clustering, thresholds, blend weights, or normalization constants on test or train+test.
- Batch-level behavior that mirrors production inference can be acceptable, but avoid anything needing whole-test visibility.

## Runtime And Submission

- Expected max runtime is about 1 hour; anything beyond roughly 1.5 hours can be rejected.
- Build a time guard around 50-55 minutes so training stops and the script proceeds to inference and writing outputs.
- The environment is an Nvidia A10G unless a challenge states otherwise.
- Every submission must be one independent end-to-end script.
- Preprocessing, feature engineering, training, ensembling, inference, and submission writing must happen from scratch in that script.
- Do not rely on cached embeddings, precomputed artifacts, or outputs from a previous run.
- Validate `submission.csv` row count, columns, ids, dtypes, and finite ranges before spending a real submission credit.

## General Not Allowed

- Pure rule-based or algorithmic solutions without real ML training.
- External datasets for any model.
- Internally sharing private solutions or approaches with another solver on the same challenge.
- Test-set adaptation or whole-test transduction.
- Synthetic training data.
- Any approach the challenge explicitly forbids.

## Grey Areas

- Regex, TF-IDF, n-grams, Markov chains, frequency methods, and similar techniques can be risky.
- The practical test: remove the ML model. If the solution still basically works, it is probably not compliant.
- Use grey-area tools for cleaning or auxiliary signal only, not as the core solver.
- Reviewer judgment controls grey-area acceptability.

## Computer Vision Rules

- A real CV model must be central: CNN, ViT, detector, segmenter, or another trained image/video model.
- Do not solve CV by tabular models directly on raw pixels.
- Hand-engineered image features such as color histograms, lesion ratios, or edge counts are acceptable only as auxiliary signal beside a genuine CV model.
- A tabular model on pretrained embeddings is grey area; it may still be rejected if it is not robust/generalizable.
- For image/video tasks, do not bypass the visual data with metadata-only, filename, row-order, or shortcut features.

## NLP And Synthetic-Structure Reminder

- Regex/templates can be used lightly for parsing or cleaning, but not as the core solution.
- If a synthetic pattern is visible, train a model to learn it rather than hardcoding the pattern.
- Avoid brittle templates that exploit generator structure outside the model.

## RAG And Retrieval Reminder

- Use a genuinely trained ranking/retrieval model when the task is RAG or retrieval.
- Avoid lookup-only or heuristic-only retrieval systems.

## Fine-Tuning And From-Scratch Reminder

- Fine-tuning challenges must actually fine-tune in the submitted script.
- From-scratch challenges must respect any ban on pretrained weights.
- Challenge-specific model-size or runtime caps override general defaults.

## Audit Template

Use this short checklist before finalizing any Eris solution:

- Challenge prohibitions read and reflected in the approach.
- Only Kaggle Docker installed libraries used.
- No package installs or repo clones.
- No external data or synthetic training data.
- No private/self-hosted/challenge-specific weights.
- Training/fine-tuning happens inside the script.
- Test set used only for inference/TTA.
- No test-stat fitting or transductive calibration.
- Runtime guard added around 50-55 minutes.
- Single end-to-end script writes a valid submission.
- Domain-specific core model is real ML, not rules.
- Grey-area features are auxiliary and justified.
- Submission schema checked before writing.
