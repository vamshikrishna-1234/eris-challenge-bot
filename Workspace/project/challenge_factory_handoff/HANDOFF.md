# Project Eris Cross-Computer Handoff

## Recommended Setup

Use one reusable skill on each computer, not one skill per challenge task.

The skill has three main modes:

1. Scout ideas and datasets in the main idea task.
2. Create one dedicated Codex task for each approved idea.
3. Build or audit the challenge inside that dedicated task.

Every task reads the same synchronized rules and examples. Every challenge has its own output folder and ownership/status JSON.

## Transfer To The Other Computer

1. Copy `challenge_factory_handoff.zip` to the other computer and extract it.
2. Synchronize or clone the main `create_challenge_synthetic` project, including rules, previous reviews, idea inventories, and accepted examples.
3. Synchronize the challenge output root, or at minimum make its directory/index available for duplicate audits.
4. Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 `
  -ProjectRoot "D:\create_challenge_synthetic" `
  -OutputRoot "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3"
```

Use paths that actually exist on that computer. The installer copies the skill to `%USERPROFILE%\.codex\skills\eris-challenge-factory` and writes `%USERPROFILE%\.codex\eris-challenge-factory.json`.

5. Restart Codex so it discovers the installed skill.
6. Start an idea task with `templates\IDEA_TASK_START.md`, or paste `templates\BUILD_TASK_START.md` into a dedicated challenge task.

Verify an installation with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

## Parallel Work Rule

Only one computer/task owns a challenge folder at a time. Before starting, create a claim under `<project-root>\challenge_registry`. Sync that claim immediately. The second computer may work on a different challenge or perform a read-only review.

The main idea task may continue discovering and opening challenge tasks while existing challenge tasks build independently.

## Updating The Workflow

Update the single portable skill, validate it, rebuild the ZIP, and reinstall it on both computers. Do not patch separate copies inside old challenge tasks.
