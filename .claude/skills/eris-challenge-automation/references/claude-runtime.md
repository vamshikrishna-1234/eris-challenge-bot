# Claude Code Runtime Mapping

Use this file only to translate runtime mechanics. The canonical bundled Eris
skills remain authoritative for challenge quality and lifecycle policy.

## Browser

- Use the project `playwright` MCP server configured in `.mcp.json` for Shipd.
- Run the browser headed so the user can see the work. Preserve its persistent
  profile so Shipd authentication survives normal restarts.
- For each active slot, open the exact dataset and challenge URLs in distinct
  tabs and verify IDs before writing. Never navigate from memory or a nearby
  draft.
- Browser availability is not implied by local files. If Playwright is missing,
  continue safe local package work and record the precise platform blocker.
  Never report live completion.
- Authentication, CAPTCHA, or account authorization may require one user
  action. Checkpoint first, request only that precise action, and resume the
  pending slot afterward.

## Workers and persistence

- Use one `eris-slot-worker` project subagent per immutable batch slot when
  parallelism is useful and capacity permits. Give it exactly one slot, its
  fixed URL pair, the batch/task IDs, and the target completion stage.
- Claude subagents are visible in the current Claude session but are not
  persistent Codex sidebar tasks. The JSON controller ledger, registry, and
  package state are the durable checkpoint across Claude sessions.
- Bind a stable label such as `claude:<batch-id>:<task-id>` in the controller's
  worker-thread field when a Claude tool does not expose a durable worker ID.
  Record the agent name/title separately in the normal audit notes.
- Workers may scout replacements inside their slot. They must not swap Shipd
  URL pairs, count rejected candidates as successes, or edit another slot.
- Avoid concurrent writes to the same Shipd draft or local package. Browser
  tabs can share one MCP browser profile; ownership is therefore slot-based,
  not tab-process-based.

## Permissions and autonomy

- The exact linked drafts supplied by the user authorize ordinary placeholder
  replacement, title/description/tag/script edits, verified uploads/imports,
  rebuilds, validations, Mark as Ready, Prepare, and checks, as stated by the
  canonical skills. Do not ask repetitive workflow questions.
- Use Claude Code's `auto` permission mode for routine autonomous operation.
  Do not enable `bypassPermissions` or add broad committed allowlists. Claude,
  MCP, operating-system, or website safety prompts still take precedence.
- Destructive cloud deletion, authentication, CAPTCHA, credential entry, or a
  change outside the exact supplied drafts may still require action-time user
  involvement. Group unavoidable prompts after checkpointing rather than
  generating one per worker.

## Completion

- Default target: `challenge_checks_passed` — every dataset/challenge check is
  green and Run Agents is visibly available, but not clicked.
- Explicit `through Run Agents` target: `agent_runs_started` — click exactly
  once, verify queued/running/nonzero-round state, record it, and stop.
- Never say the batch is complete while the controller reports any remaining
  slots or while a live state is unverified.
