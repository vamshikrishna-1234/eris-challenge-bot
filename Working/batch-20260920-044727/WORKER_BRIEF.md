# Worker brief — batch-20260920-044727 (Claude Code remote session)

Each `eris-slot-worker` owns exactly one slot. Repo root: /home/user/eris-challenge-bot
(branch claude/wonderful-bohr-b7u814). Goal stage for every slot: `challenge_checks_passed`
(all dataset + challenge checks green, Run Agents visibly available, NOT clicked).

Slots and immutable pairs (never remap, never edit another slot):
- task-001: problem jx7fc5d8gbp3hd9zt4pye0ywgd8efc5e / dataset jd71ktmw09xmcbpd8k2rwqc4v18efhft
- task-002: problem jx76g5p2hkwy4bt7etrft14cb18eeh26 / dataset jd7bk5e37hvhjg6q7vrm1z4jnx8efe0a
- task-003: problem jx7d7hc2kwrxdxn9r0eg4pjq4h8eebx9 / dataset jd7bgzt14yjrdhr55hvybg8kjn8ef7y5
Full URLs: Working/batch-20260920-044727/pairs.json

## Read first (canonical policy is unchanged)
1. .claude/skills/eris-challenge-automation/SKILL.md, then .codex/skills/eris-challenge-automation/SKILL.md
   and references/{commands,lifecycle,linked-drafts,resilience}.md, then
   .claude/skills/eris-challenge-automation/references/claude-runtime.md
2. .codex/skills/eris-challenge-factory/SKILL.md + references/{scout-workflow,pre-handoff-gate,build-workflow}.md
3. .codex/skills/eris-submission-pool/SKILL.md + references/workflow.md + assets/pool-state-template.json
4. Living policy: Workspace/project/rules/LATEST.md, rules/challenge_template_file_creation.txt,
   rules/dataset_template_creation.txt, rules/checkpoints/*, rules/prev_reviews.txt (large; skim for
   recurring rejection reasons), Workspace/project/.cursor/rules/challenge-creation.mdc,
   Workspace/project/sprint_3/problems_with_acceptances.txt, 2-3 accepted examples under
   Workspace/project/sprint_3/accepted/.
5. Duplicate/novelty map: Workspace/project/_all_challenge_titles.txt, challenge_registry/*.json
   (files carry a UTF-8 BOM: open with encoding="utf-8-sig"), Workspace/project/Shipd_Challenge_Archive_*.

## Runtime facts (translate tool mechanics only; never a quality/safety gate)
- No PowerShell here. Controller invocation:
  cd /home/user/eris-challenge-bot && export ERIS_PROJECT_ROOT=$PWD/Workspace/project ERIS_OUTPUT_ROOT=$PWD/Workspace/output ERIS_REGISTRY_ROOT=$PWD/Workspace/project/challenge_registry ERIS_RULES_ROOT=$PWD/Workspace/project/rules ERIS_AUTOMATION_HOME=$PWD/eris_automation && python3 eris_automation/Tools/flow.py <command ...>
  Bundled .ps1 helpers (workspace_probe, validate_handoff_readiness, new_challenge_status) cannot run:
  reimplement their checks in Python under your slot folder and record that you did.
- Internet: curl/python/pip go through a preconfigured proxy (CA already set in env). Use the
  WebSearch/WebFetch tools (load with ToolSearch) for research. Disk is a limited allowance: prefer
  sources whose required raw package is bounded (pilot on subsets, stream/partial download when
  possible, delete scratch). Do not pull multi-GB archives speculatively.
- Browser: the project Playwright MCP (mcp__playwright__*, load via ToolSearch) runs headless in this
  container. Its Shipd authentication is being verified by the supervisor. DO NOT open or edit Shipd
  until the supervisor sends you a message confirming an authenticated session. Everything through a
  complete, audited local package needs no Shipd access. If you reach the Shipd phase without that
  confirmation: write your checkpoint, run `record-transient <task> --kind browser_auth --message ...`,
  `set-state <task> --state retry_wait`, and return your report.
- If you do get browser access: open your two exact URLs in your own tabs, verify IDs before any
  write, never close or use another slot's tabs, and never automate login/CAPTCHA.
- Files: durable outputs under Working/batch-20260920-044727/<task-id>/ (scout notes, pilots,
  evidence, CHECKPOINT.md) and the challenge package under Workspace/output/<slug>/. Registry entry:
  Workspace/project/challenge_registry/<slug>.json (schema in _schema.json plus the `readiness` and
  `evidence` objects from pre-handoff-gate.md). Do not run git commit/push; the supervisor does.
- Ledger discipline: `set-state` on every transition (scouting -> pilot -> build_ready -> building ->
  ...), `replace-candidate --verdict rejected|hold --reason ... --evidence <path>` for every failed
  candidate (same slot, keep searching), `record-transient` for rate limits/reconnects/auth. After a
  measured Proceed: `bind <task-id> --registry-key <slug> --dataset-url <exact> --problem-url <exact>`.
- Checkpoint: update Working/batch-20260920-044727/<task-id>/CHECKPOINT.md before any long step and
  before returning: phase, candidate, last completed gate, next action, artifact paths.

## Work plan
Scout (dataset-first; real native labels; permissive redistribution; CPU-feasible; novel vs. the
duplicate map and Shipd archive) -> bounded pilot with measured gates (post-filter rows, independent
families, raw bytes, lookup attack, capability-matched baseline, metric-null audit, premortem) ->
Proceed only with a complete readiness object -> Build the full package (prepare.py, grade.py,
PASTE_THIS_*.txt, CHALLENGE_FORM_FILL.md, DATASET_FORM_FILL.md, SOURCE_VERIFICATION.md,
DATA_ACQUISITION.md, raw upload plan, baselines, red-team, smoke, grader robustness, final audit) ->
registry status ready_for_review -> SUBMISSION_POOL_STATE.json prepared (no website write yet) ->
Shipd phase only after supervisor confirmation.

Return: slot ID; every candidate with verdict and measured reason; package path; registry key;
whether the pair is bound; gates passed with numbers; current controller state; exact next action
or blocker.

## Batch-wide design rules learned from measured rejections (binding for every slot)

As of 2026-09-20T11:10Z this batch has measured and rejected 7 candidates across 3 slots.
Every one failed the same underlying test in a different disguise. Apply these before
spending budget on a build.

**Rule 1 — the universal-signal rule (the one that killed all 7).**
The predictable structure your task asks a solver to learn must be *universal*: physical,
signal-level, combinatorial, or generative, and taught just as well by the released training
split as by the full public source. It must NOT be the identity or per-group structure of an
identifiable public item. When the only signal that beats the standard domain method is a
property of identifiable public source groups, the learning signal and the leakage channel are
the same quantity, and hardening trades them one-for-one until the task is destroyed.
Disguises already seen and rejected: a photograph's public caption (slot 2 candidate 1); a
camera station's roster (slot 2 candidate 2); a census area's association structure (slot 2
candidate 3); a wind farm's published status log (slot 3 candidate 1); a public per-image EXIF
sidecar (slot 1 candidate 2).

**Rule 2 — measure the lookup attack at the shipped bundle size, not per row.**
Per-row lookup resistance does not survive bundling. A measured 0.0025 per-row recovery became
1.000 group recovery at bundle size 60. Report the bundle size alongside every lookup number,
and run a two-stage attack: de-anonymise the group first, then re-attack the rows.

**Rule 3 — report ceiling minus capability, not skill above zero.**
Measure the chance floor for the *restricted* choice, and also the achievable ceiling: the best
predictor that never sees the scored sample. Judge headroom as ceiling minus capability-matched
baseline. Skill-above-zero flattered one candidate by 0.29, and a constant prior flattered
another into looking acceptable when it was near chance.

**Rule 4 — order of work during scouting, before any package exists.**
semantic-duplicate audit -> instance-level retrieval attack at shipped bundle size ->
chance-floor-relative capability-matched baseline AND achievable ceiling -> null-metric audit ->
premortem -> registry `readiness` -> `validate_handoff_readiness.py` -> only then build.
Two slots burned most of their budget discovering a reversibility failure after the package was
complete. Do not repeat that.

**Consequence for candidate selection.** Prefer sources where the scored target is derived
privately across many rows by `prepare.py` (a structural quantity computed over the corpus), or
where knowing the origin record still does not reveal the answer. Accepted workspace challenges
on public corpora survive for exactly this reason.

**Rule 5 — validate any ordering/matching/assignment grader against a uniform-random
submission before you believe a single baseline number.** A pooled metric in slot 1 gave a
uniform-random submission 0.577 tau and 0.23 score, because per-row `max(0, .)` rectification
combined with occurrence-rank alignment inflated the floor. Scoring the solver's explicit
positions and skipping same-descriptor pairs corrected it to 0.0032. Every baseline measured
against an uninspected floor is unusable, in either direction.

**Rule 6 — a weak hand-built "capability-matched" baseline understates the true ceiling.**
In slot 1 a hand-tuned likelihood decoder scored 0.113, below the trivial prior, while the
principled version (learned pairwise model plus global search plus domain constraints) scored
0.225. Build the capability-matched baseline the way a strong solver would, then report it.
This matters most before accepting a candidate: an understated ceiling makes headroom look
larger than it is. Rejections already recorded on saturation grounds are conservative under
this rule and do not need revisiting.

**Rule 7 — one writer per slot, and write results incrementally.**
Ownership is slot-based, not process-based. Only one worker may write a slot's folder, registry
entry and controller task at a time; a predecessor is stood down in writing (see the slot's
`OWNERSHIP.md`) before a successor is dispatched, and a stood-down worker routes any correction
through the supervisor instead of editing shared files. If you ever must touch a file another
worker may hold, guard the write: assert the expected target strings are present and assert the
mtime is unchanged immediately before writing.

Related measurement-integrity rule: a pilot script whose only durable output is one `json.dump`
at the end loses every completed arm when a later arm times out. Write each arm's result as it
completes, and never cite an artifact without confirming the file exists. One slot-2 evidence
file cited a JSON that a timeout had prevented from ever being written; the numbers were genuine
but only the stdout survived, and the citation had to be corrected after the fact.

**Rule 8 — populate the pool checkpoint's exact IDs, and verify what you claim about your own
files.** Both slots that reached Proceed reported `SUBMISSION_POOL_STATE.json` as carrying both
exact Shipd IDs; in both cases the fields were null and the supervisor filled them from the
controller ledger. `references/workflow.md` requires the checkpoint to preserve the exact problem
and dataset IDs and URLs so a later run resumes from verified state rather than browser memory.
Before reporting an artifact as complete, read the file back and confirm the specific fields you
are claiming. The same discipline that caught a cited JSON which never existed applies to fields
inside a file that does.
