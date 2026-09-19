# Portable Eris Challenge Bot

This is the reusable Project Eris challenge-creation bot. It contains the controller, skills, rules, templates, lightweight registry metadata, accepted examples, and duplicate-check references. Raw datasets, model weights, old challenge outputs, and historical working copies are intentionally not bundled; each new task downloads only the source data it needs into the ignored runtime folders.

## Start in Codex

1. Open this folder in Codex:

   `E:\Eris Challenge Bot`

2. Start a new chat in that folder.
3. Send one of these commands:

   - `Ready`
   - `Status`
   - `Status & Fix`
   - `Create 1 Task`
   - `Create 3 Tasks`
   - `Finish 5 Linked Tasks` followed by five labeled challenge/dataset URL pairs

That is all you need to provide. The workspace instructions route the command through the bundled Eris skill and durable controller.

## Start in Claude Code

1. Open PowerShell in this folder.
2. Run `./run-claude.ps1`.
3. Approve the trusted project and Playwright MCP server once, then sign in to
   Shipd in the visible browser if needed.
4. Send the same commands listed above, or invoke
   `/eris-challenge-automation` explicitly.

Claude-native adapters live under `.claude/`, while `.codex/skills/` remains
the single canonical policy copy. See `CLAUDE_SETUP.md` for the one-time setup
and the runtime differences.

## Command meanings

- **Ready:** safely closes a fully terminal batch and prepares the controller for new work. It never deletes packages or evidence.
- **Status:** performs a fresh, read-only Shipd check and reports both live and local state.
- **Status & Fix:** checks Shipd, repairs genuine yellow/red findings, and reruns the affected checks.
- **Create X Tasks:** pursues exactly X successful Eris challenge-ready slots. By default it stops with every check green and Run Agents available; include “through Run Agents” only when you want it clicked.
- **Finish X Linked Tasks:** takes exactly X Shipd challenge/dataset pairs, replaces all default placeholders, uploads and rebuilds the verified data, clears every dataset and challenge warning/failure genuinely, chooses measured CPU/GPU compute, marks the dataset ready, runs preparation, and stops with Run Agents available. Add “through Run Agents” only when you explicitly want it launched.

You can also include the URL pairs in the original `Create X Tasks` request. The bot will create each verified local package, bind the corresponding pair in the order supplied, and finish the platform workflow. You do not need to explain placeholder titles or confirm every step again.

Rate limits and reconnects are automatically checkpointed and retried. An expired authenticated Shipd session may require you to sign in again, because the bot cannot bypass authentication or CAPTCHA; this keeps the slot pending and resumable rather than rejecting it. The controller never calls a batch complete until all X tasks reach their configured goal stage.

For multi-task runs, Codex creates one visible worker task per slot. Claude Code uses one project subagent per slot and a headed Playwright MCP browser. In both runtimes, the durable controller—not chat memory—is the source of truth, and the exact dataset/challenge pair remains bound to its slot.

All ordinary Shipd draft work is pre-authorized by supplying the exact links. The bot will not ask about changing placeholder titles/descriptions, uploading verified files, rebuilding, validating, marking ready, preparing, or checking. The browser safety layer still requires action-time confirmation before cloud deletion; the supervisor groups those into one question. For a true zero-question run, leave the draft's Data Files empty instead of uploading disposable placeholder archives.

For the recommended resilient five-task request, paste the template in `RESILIENT_5_TASK_PROMPT.md` and replace its bracketed dataset suggestions and Shipd links.

## Portability

- Workspace paths in `Config/workspace.json` are relative to this folder.
- No external file or folder is required for the bot's code, policy, templates, lightweight registry, or controller. Source datasets are fetched from their verified official URLs as part of each new challenge.
- `Working`, `Workspace/output`, and live batch/task records are runtime-only and ignored by Git, keeping the repository small while preserving local resumability.
- Run `./validate-portable.ps1` after copying or moving the folder. It verifies the internal paths, bundled skills, living rules, registry, controller, and local ledger.
- The machine still needs Python, internet access, an authenticated Shipd session, and either Codex with browser control or Claude Code plus Node.js 20+ and the configured Playwright MCP server. Those are runtime services; they are not hidden file dependencies.

## Optional terminal access

```powershell
.\run.ps1 status --json
```

Normal use does not require terminal commands; use the four chat commands above.

## GitHub

The maintained private repository is `https://github.com/vamshikrishna-1234/eris-challenge-bot`.

Runtime datasets and generated challenge packages stay local because `.gitignore` excludes `Working`, `Workspace/output`, and live batch/task records. Commit and push only reusable bot improvements.
