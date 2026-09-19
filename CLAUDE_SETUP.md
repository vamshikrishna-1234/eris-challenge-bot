# Use the Eris Challenge Bot with Claude Code

## One-time setup

1. Install Claude Code and Node.js 20 or newer.
2. Open PowerShell in this repository root.
3. Run `claude doctor` and sign in if requested.
4. Start the bot with `./run-claude.ps1`.
5. Approve this trusted repository and its project Playwright MCP server once.
6. When the visible Playwright browser opens Shipd, sign in once if the saved
   browser profile is not already authenticated.

The project `.mcp.json` starts Microsoft's Playwright MCP server. It gives
Claude a headed browser that the user can see; it is the Claude equivalent of
Codex in-app browser control.

## Commands to send

Use the same commands as Codex:

- `Ready`
- `Status`
- `Status & Fix`
- `Create 5 Tasks` followed by suggestions and five Shipd URL pairs
- `Finish 5 Linked Tasks` followed by five Shipd URL pairs

You may invoke the router explicitly, for example:

`/eris-challenge-automation Create 5 Tasks ...`

Copy `RESILIENT_5_TASK_PROMPT.md` when you want the complete five-task request.
Add `through Run Agents` only when Claude should click Run Agents; otherwise it
stops when every check is green and that button is visibly available.

## Exact first run

You do not need to paste `CLAUDE.md`; Claude Code discovers it automatically.

1. Send `Ready`.
2. If the controller is ready, paste the complete prompt under **First five-task
   prompt to paste** in `README.md`, replacing all bracketed values.
3. If `Ready` reports an unfinished batch, send `Status & Fix` instead. This
   resumes the saved slots rather than creating duplicates.

For end-to-end platform work, supply exactly five dataset/challenge URL pairs.
Candidate dataset suggestions are optional because the workers can search
official sources themselves. The Shipd pairs are not optional: they identify
the editable drafts that each worker must populate.

`Create 5 Tasks` creates five immutable controller slots and dispatches one
`eris-slot-worker` subagent for each. Workers may run in waves when the Claude
concurrency limit is below five. They are separate subagent contexts within the
main Claude Code session, not five permanent top-level chats.

The project Playwright MCP server opens a visible headed browser window and
separate dataset/challenge tabs for the linked drafts. It is not an embedded
Claude chat browser. After one-time MCP trust and Shipd authentication, the
workflow proceeds automatically until the requested stopping stage, subject to
authentication/CAPTCHA and safety-enforced confirmation boundaries.

## Important differences from Codex

- Claude Code uses project subagents rather than persistent Codex sidebar tasks.
  The local controller ledger preserves progress across sessions.
- Use Claude Code in this local folder. A normal claude.ai web chat does not
  automatically receive the repository, controller, local files, or Playwright
  browser tools.
- `run-claude.ps1` uses Claude's `auto` permission mode for routine autonomy.
  It deliberately does not use the unsafe `bypassPermissions` mode. A one-time
  repository/MCP trust prompt, a Shipd login/CAPTCHA, or a safety-mandated
  destructive-cloud confirmation can still require the user.
- Resume later from this directory with `claude --continue` or start the launcher
  again and send `Status & Fix`; the ledger remains authoritative.
