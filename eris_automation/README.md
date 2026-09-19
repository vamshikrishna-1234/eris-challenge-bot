# Eris Challenge Automation

This folder is the durable local controller for the reusable Project Eris workflow.

The natural-language interface is provided by the installed `eris-challenge-automation` Codex skill:

- `Ready`
- `Status`
- `Status & Fix`
- `Create X Task` / `Create X Tasks`

The controller intentionally does **not** automate authenticated Shipd clicks by itself. Codex performs live browser work through the existing Eris factory and submission skills, then records exact observations here. This prevents stale local files from being reported as live platform status.

## Local commands

```powershell
.\eris_automation\run.ps1 create 3 --authorization "Create 3 Task"
.\eris_automation\run.ps1 status
.\eris_automation\run.ps1 status --json
.\eris_automation\run.ps1 bind <task-id> --registry-key <registry-key> --codex-task-id <thread-id>
.\eris_automation\run.ps1 record-live <task-id> --platform-state challenge_checks_passed --problem-id <id> --dataset-id <id> --url <url> --note "All required checks green"
.\eris_automation\run.ps1 status-fix
.\eris_automation\run.ps1 ready
```

`status` is local-only and always prints `live_check_performed: false`. The Codex `Status` workflow first performs a fresh authenticated inspection and records it.

## Safety and counting

- `Ready` clears only the active pointer after every slot is terminal; it never deletes evidence or challenge packages.
- Only one batch can be active.
- `X` means exactly X immutable task slots.
- Revisions update `revision_count`; they never inflate the task count.
- Registry bindings must point to an existing `challenge_registry/<key>.json` file.
- Batch and task IDs reject path separators and traversal syntax.
- Yellow and red platform findings remain repair work; the controller contains no bypass mechanism.

## Validation

```powershell
py .\eris_automation\Audit\tests\test_flow.py
```

## Install on another Codex computer

1. Copy the `eris_automation` folder into that computer's synchronized Eris project root.
2. Copy `skill/eris-challenge-automation` from the portable ZIP to `<CODEX_HOME>/skills/eris-challenge-automation`.
3. Keep the existing `eris-challenge-factory`, `eris-submission-pool`, and computer-use capabilities installed.
4. Run the validation commands above, then say `Ready` or `Status` in Codex.

The state directory is intentionally project-local so multiple computers can synchronize it with the challenge registry. Follow the factory ownership protocol: one owner computer and one owner Codex task per challenge.
