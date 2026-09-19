# Eris Solver Rule Update Log

Use this file to record new guidebook changes, reviewer warnings, platform behavior, or repeated failures that should influence future Project Eris solving.

## 2026-07-10 - Initial Guidebook Distillation

Source:
- Project Eris Solver Guidebook Google Doc.
- User request to save the rulebook as a reusable skill and keep it updated.

Issue:
- Eris solving needs a persistent compliance checklist across challenges.

Required behavior:
- Use only Kaggle Docker installed libraries unless reviewer-approved.
- Keep real ML training/fine-tuning inside the submitted script.
- Do not use external data, synthetic training data, private fine-tuned weights, reverse lookup, or answer tables.
- Use test only for per-sample/per-batch inference or fixed TTA.
- Keep CV solutions centered on a trained image/video model, with handcrafted features only as auxiliary signal.
- Add a runtime guard around 50-55 minutes.

Preventive check:
- Before coding or submitting, read `guidebook-checklist.md` plus the challenge statement and audit strictest-rule compliance.

## 2026-07-10 - Kaggle PyTorch CUDA Kernel-Image Failure

Source:
- Coffee Leaf Spray Allocation v1 Kaggle run.

Issue:
- Kaggle accepted a GPU-enabled private kernel but PyTorch failed on the first CUDA convolution with `CUDA error: no kernel image is available for execution on the device`.

Required behavior:
- Add a small CUDA probe before training if using PyTorch on Kaggle.
- If the probe fails, either switch to a TensorFlow/TPU-compatible route or fall back to a time-bounded CPU profile that still writes `submission.csv` and `oof_report.json`.
- Do not silently write a weak constant fallback; report the device and fallback reason in `oof_report.json`.

Preventive check:
- Inspect Kaggle logs for CUDA probe output and verify the report records `device`, completed folds, fallback reason, and elapsed time.

## 2026-09-14 - Identical Scores from Retained Sample Checkpoints

Source:
- Serial Crystallography Lattice Indexing Shipd review and exported Run 3 trajectory.

Issue:
- Three displayed agent scores were all `0.1189`, which looked like ceiling saturation or copied solutions.
- The available trajectory showed a different failure: the agent validated the sample once at `0.11885677041408906`, developed a much stronger train-only solver, exhausted its step budget, and never wrote or validated the improved test submission.

Required behavior:
- Distinguish the retained checkpoint from the best code or local validation result in the trajectory.
- Audit every write to `working/submission.csv` and every `validate_submission` call before interpreting repeated scores.
- Treat missing trajectories as unauditable; identical rounded scores alone are not evidence of copying.
- Generate and checkpoint a complete test submission before extended tuning, then checkpoint meaningful improvements while time remains.

Preventive check:
- Record the last submission mutation, all validation scores, the terminal step/tool, and any private/grader/source-lookup actions. Compare trajectories only when at least two traces are actually available.
