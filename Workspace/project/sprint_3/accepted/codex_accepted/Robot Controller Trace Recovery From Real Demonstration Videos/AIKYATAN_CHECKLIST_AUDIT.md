# Aikyatan Checklist Audit

Checklist audited: `D:\create_challenge_synthetic_output_folder\sprint_3\checklist_aikyatan.txt`

Challenge audited: `Robot Controller Trace Recovery From Real Demonstration Videos`

## Verdict

SHIP under the current Project Eris challenge rules, with notes. The Aikyatan checklist is an older robust-audit guide and conflicts with current workspace rules in a few places, especially "no markdown tables" and required `rubrics.md`/`solution.ipynb`/`config.yaml` artifacts. No blocker was found under the active challenge-creation rules.

## Fingerprints

- Fixture raw hash: `020744da45aa49f31ce0e74bab736bcc55c1c173b546739f4fe32d35b767fba3`
- Deterministic prepared public hash, run 1: `27d658b21b84585069f1f5afbe7c5d14c38a868695228b3e1b6301e771c0d73e`
- Deterministic prepared public hash, run 2: `27d658b21b84585069f1f5afbe7c5d14c38a868695228b3e1b6301e771c0d73e`
- Deterministic prepared private hash, run 1: `73c968662bac87182e705276004fdf697f92155182a66c919e067075636b9396`
- Deterministic prepared private hash, run 2: `73c968662bac87182e705276004fdf697f92155182a66c919e067075636b9396`

Evidence command:

```powershell
python - <<'PY'
from prepare import prepare
prepare("<fixture raw>", "<public 1>", "<private 1>")
prepare("<fixture raw>", "<public 2>", "<private 2>")
PY
```

Observed output:

```json
{
  "prepare_string_args_ok": true,
  "deterministic_public": true,
  "deterministic_private": true
}
```

## Score Ladder

- Perfect submission: `1.0`
- Full real prepared sample submission: `0.20715530341513477`
- Full real duration-only transfer: `0.3019376000888273`
- Full real state-exact transfer: `0.32234033341502044`
- Full real train-optimized constant-head template: `0.5050602585426203`
- Fixture shotgun template: `0.000007863486601483839`
- Fixture generic broad template: `0.0021283187383558627`
- Fixture first train-copy template: `0.06413671949438014`
- Fixture best single train-template oracle: `0.14949184315990044`
- Empty-list submission: `0.0`
- Bad-column submission: `0.0`
- Duplicate-ID submission: `0.0`
- One row with invalid schema among otherwise perfect rows: `0.9583333333333334`
- Reference solution notebook: not applicable; this challenge bundle does not include a solver notebook under current Eris challenge-builder requirements.

Evidence commands:

```powershell
python _sanity_smoke.py
python _grade_redteam.py
```

Observed outputs:

```json
{
  "perfect": 1.0,
  "sample": 0.019304625355701818,
  "malformed": 0.9583333333333334
}
```

```json
{
  "bad_columns": 0.0,
  "best_single_train_template_oracle": 0.14949184315990044,
  "duplicate_id": 0.0,
  "empty_lists": 0.0,
  "first_train_copy": 0.06413671949438014,
  "generic_broad": 0.0021283187383558627,
  "one_row_invalid_schema": 0.9583333333333334,
  "sample": 0.019304625355701818,
  "shotgun_template": 0.000007863486601483839,
  "train_optimized_constant_heads": 0.06905582100070778
}
```

## Findings

- [PASS] [Gate A: Static Review] Current required challenge artifacts exist and paste files match canonical scripts. Evidence: `challenge_audit.py` reported all mandatory files present and `PASTE_THIS_GRADE.txt`/`PASTE_THIS_PREPARE.txt` match. Proposed fix: none.

- [PASS-WITH-NOTES] [Gate A: Static Review] The Aikyatan guide lists old artifact names such as `dataset_description.md`, `problem_description.md`, `config.yaml`, `solution.ipynb`, and `rubrics.md`. Current Project Eris rules use `DATASET_FORM_FILL.md`, `CHALLENGE_FORM_FILL.md`, paste files, and no rubrics. Evidence: `challenge_audit.py` reported `failures=0 warnings=10` for the current required artifact set. Proposed fix: do not add stale artifact formats unless the platform explicitly asks for them.

- [PASS] [Gate B: Determinism] `prepare.py` is deterministic on a fresh fixture and accepts string arguments. Evidence: two subprocess prepares produced identical public/private tree hashes, and `prepare_string_args_ok` was `true`. Proposed fix: none.

- [PASS-WITH-NOTES] [Gate C: Leakage Audit] Public leak checks pass on prepared fixture outputs. Evidence: `_analyze.py` returned `public_leak_issues: []`, `sample_non_degenerate_and_weak: true`, `duration_shortcut_not_saturated: true`, and `state_exact_shortcut_not_saturated: true`. Proposed fix: none for current public-output checks.

- [PASS-WITH-NOTES] [Gate C: Source-Reversibility] Full public/raw video retrieval against the official Zenodo archive passed after video hardening. Evidence: `_source_lookup_probe.py` on the full official ZIP and hardened prepared split returned top-1 recovery `0.0500` and top-5 recovery `0.1250`, below thresholds `0.10` and `0.25`. Proposed fix: keep the stronger video transform chain and rerun the probe after any prepare-video changes.

- [PASS] [Gate D: Hardcoding And Exploit Red Team] Cheap template and copy attacks do not saturate the metric. Evidence: full real `_analyze.py` scores `train_optimized_constant_heads=0.5050602585426203`, below the `0.6` agent ceiling, and fixture `_grade_redteam.py` scores `generic_broad=0.0021283187383558627`, `first_train_copy=0.06413671949438014`, and `best_single_train_template_oracle=0.14949184315990044`, all far below perfect. Proposed fix: none.

- [PASS] [Gate E: Grader Strictness] Structural malformed submissions score `0.0`; row-local malformed content zeros the affected row rather than crashing. Evidence: `_grade_redteam.py` returned `bad_columns=0.0`, `duplicate_id=0.0`, `empty_lists=0.0`, and `one_row_invalid_schema=0.9583333333333334`; `_sanity_smoke.py` returned malformed-row score between 0 and 1. Proposed fix: none.

- [PASS-WITH-NOTES] [Gate E: Exception Semantics] The Aikyatan guide expects `ValueError` for some invalid submissions. Current workspace rules require structural failures to return `0.0` safely through `grade()`, and row-local malformed JSON to score zero for that row. Evidence: `grade.py` follows this pattern and smoke/red-team tests pass. Proposed fix: keep current behavior unless the platform changes its grader contract.

- [N/A] [Gate F: Reference Solution Verification] No `solution.ipynb` is included in this challenge bundle, and current challenge-builder requirements do not require one. Evidence: challenge mandatory file audit passes without a solution notebook. Proposed fix: if a reference solution is later requested, add one and rerun Gate F.

- [PASS] [Gate G: Documentation-Reality Diff] The visible description includes CPU limit, task contract, exact submission path, exact column order, JSON schemas, malformed-submission behavior, and What Not To Use. Evidence: `CHALLENGE_FORM_FILL.md` contains `./working/submission.csv`, submission table, schema examples, CPU limits, and enforcement block; `challenge_audit.py` reports description/table checks pass. Proposed fix: none.

- [N/A] [Gate H: Rubric Audit] Rubrics are removed by current platform rules. Evidence: `rules/LATEST.md` says evaluation rubrics are removed, and `challenge_audit.py` passes "challenge form avoids rubric wording." Proposed fix: do not add `rubrics.md`.

- [PASS-WITH-NOTES] [Gate P: Platform-Survivability] Direct official URL import is preferred and under 1 GB; string-argument prepare works; sample clears platform floor on the full real prepared split. Evidence: source file is official `PandaHandover_Real_Val.zip`, size `296.2 MB`, full real sample score `0.20715530341513477`, string args accepted. Proposed fix: use the official direct URL import; if URL import fails, upload only the unmodified official ZIP.

- [PASS-WITH-NOTES] [Gate P: Local Upload Zip] No local upload zip is present in the challenge folder. Evidence: `challenge_audit.py` warns `no upload zip found in challenge folder`. This is acceptable because the raw source is a single official Zenodo URL and the challenge explicitly prefers URL import. Proposed fix: no zip needed unless URL import fails.

- [PASS] [Gate N: Novelty And Domain] Source verification names nearest neighbors and documents novelty score `7/10`. The task is real robotics/video structured prediction, not tabular/regression. Evidence: `SOURCE_VERIFICATION.md` novelty section; `CHALLENGE_FORM_FILL.md` explicitly rejects raw trajectory regression-only solutions. Proposed fix: none.

- [PASS-WITH-NOTES] [Gate R: Render/Formatting] Current active rules require markdown tables in `CHALLENGE_FORM_FILL.md`, while the Aikyatan guide says "No markdown tables." Evidence: `.cursor/rules/challenge-creation.mdc` requires markdown tables; `challenge_audit.py` passes table checks. Proposed fix: follow current active rules and keep tables.

## Gate Summary

- Gate A Static review: PASS-WITH-NOTES
- Gate B Determinism proofs: PASS
- Gate C Leakage audit: PASS-WITH-NOTES
- Gate D Hardcoding and exploit red team: PASS
- Gate E Grader strictness battery: PASS-WITH-NOTES
- Gate F Reference solution verification: N/A
- Gate G Documentation reality diff: PASS
- Gate H Rubric audit: N/A
- Gate P Platform-survivability: PASS-WITH-NOTES
- Gate N Novelty and domain classification: PASS
- Gate R Render-safety and formatting: PASS-WITH-NOTES due current-rule conflict

## Residual Risks

- Full official-source video retrieval probe now passes after video hardening, but source retrieval remains a residual nonzero risk because the upstream corpus is public.
- No reference solution notebook was audited because the current challenge bundle does not include or require one.
- The Aikyatan checklist is partly stale relative to current Project Eris rules, so literal compliance with every line would cause conflicts, especially around rubrics and markdown tables.
