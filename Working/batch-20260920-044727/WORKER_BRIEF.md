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
