# Self-Contained Eris Challenge Bot Workspace

This folder is the complete command center for reusable Project Eris challenge work. All persistent rules, skills, registries, evidence, controller state, working files, and challenge outputs must remain beneath this folder.

- For `Ready`, `Status`, `Status & Fix`, `Create X Task(s)`, supplied Shipd challenge/dataset link pairs, or close equivalents, load and follow `.codex/skills/eris-challenge-automation/SKILL.md`. In Claude Code, enter through `.claude/skills/eris-challenge-automation/SKILL.md`, which loads that canonical copy and applies only the documented runtime translation.
- Before each workflow, run `validate-portable.ps1`. If it fails, repair the local bundle; never fall back to an older external workspace.
- Read `Config/workspace.json` before resolving rules, registry, output, or controller paths.
- Use `eris_automation/run.ps1` for the durable local ledger.
- Use the bundled `.codex/skills/eris-challenge-factory/`, `.codex/skills/eris-submission-pool/`, and `.codex/skills/eris-solver-rules/` copies. Do not read matching skills from the user profile when the bundled copies exist.
- A bare `Status` is read-only: inspect authenticated Shipd pages freshly and never present local JSON as live status.
- `Status & Fix` authorizes substantive in-scope repairs, not check suppression, grader weakening, or evaluator tampering.
- `Create X Task(s)` means exactly X successful challenge-ready slots. Default success is all checks green with Run Agents available; launch only when the current invocation explicitly requests it. Revisions and rejected dataset candidates do not count.
- For exact linked drafts, use the bundled Linked Draft Finisher role. Replace all placeholder/default values without asking why they exist, bind both URLs, and use verified package facts.
- Choose CPU, A10G, or H100 from measured dependency, memory, and runtime evidence; never accept the page default blindly.
- Apply the existing Eris factory gates before build handoff and the Eris submission workflow only to verified packages bound to exact platform drafts.
- Resolve every yellow and red finding genuinely. An explicit current request to finish supplied exact pairs through Run Agents authorizes the in-scope platform workflow without repetitive confirmations. Never bypass tool-enforced confirmation, authentication, CAPTCHA, or permission controls.
- Keep the batch, registry, package, and live platform states distinct and timestamp live observations.
- Rate limits, reconnects, and browser authentication failures are retryable runtime conditions. Checkpoint and resume; never report the affected candidate as rejected. Do not claim the batch is complete while the controller reports `remaining_to_goal > 0`.
- Multi-task batches use one worker per immutable slot. In Codex, use a persistent user-visible worker task and bind its thread ID. In Claude Code, use the bundled project subagent and bind a stable `claude:<batch-id>:<task-id>` worker label when no durable worker ID is exposed. Follow the runtime-specific browser mapping and keep separate exact dataset/challenge tabs.
- Never ask permission for placeholder replacement, ordinary field/script changes, uploads, rebuilds, validation, Mark as Ready, Prepare, or checks on the supplied drafts. Centralize browser-mandated always-confirm actions such as cloud deletion through one grouped supervisor question.
- Stop a submission workflow immediately after Run Agents is confirmed.

## Self-contained boundary

- Resolve every configured path relative to this bot root.
- Store new source downloads, pilots, packages, audit outputs, and challenge artifacts under `Workspace/output/` or `Working/`.
- Do not depend on junctions, symlinks, or files under the former `create_challenge_synthetic` roots on `C:`, `D:`, or `E:`.
- Internet sources, authenticated Shipd, Codex or Claude Code, browser control, Python, Node.js where required, and installed runtime libraries are execution services, not workspace-file dependencies. They may be used normally, but all durable results must be saved inside this folder.
