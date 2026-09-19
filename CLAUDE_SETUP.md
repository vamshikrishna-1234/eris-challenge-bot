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
