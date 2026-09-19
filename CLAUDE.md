# Eris Challenge Bot — Claude Code

@AGENTS.md

This repository is dual-runtime: the canonical workflow lives in the bundled
`.codex/skills/` files, while `.claude/skills/` provides Claude Code adapters.
Follow the canonical quality, evidence, and lifecycle rules unchanged.

## Claude runtime mapping

- Treat references to a Codex worker task as one Claude project subagent for one
  immutable batch slot. Use the `eris-slot-worker` project agent when useful.
- Treat references to the Codex in-app browser as the project Playwright MCP
  browser. Keep it headed/visible, use the persistent authenticated profile,
  and open the exact dataset and challenge URLs in separate tabs.
- Claude subagents are session workers, not permanent Codex sidebar tasks. The
  controller ledger is the durable source of truth across restarts.
- Read `.claude/skills/eris-challenge-automation/references/claude-runtime.md`
  before any live Shipd work or multi-task batch. Its runtime translations
  override only Codex-specific tool wording, never a quality or safety gate.
- Never claim a Shipd edit, check, Mark as Ready state, or Run Agents launch
  from local files alone. Verify the live page through the browser tool.
- By default, stop after every check is green and Run Agents is visibly
  available. Click Run Agents only if the current invocation explicitly says
  `through Run Agents`.

## Commands

Route `Ready`, `Status`, `Status & Fix`, `Create X Task(s)`, `Finish X Linked
Tasks`, and supplied Shipd URL pairs through `/eris-challenge-automation`.
Natural-language equivalents are valid.

Before acting, run `./validate-portable.ps1`. Keep all downloads and generated
artifacts under `Working/` or `Workspace/output/`.
