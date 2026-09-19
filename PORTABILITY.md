# Portability Contract

The `Eris Challenge Bot` directory is the complete reusable bot workspace. It deliberately excludes historical raw datasets, model weights, generated challenge packages, pilot binaries, and old batch state.

## Included

- command router and durable controller;
- Eris automation, factory, submission-pool, and solver-rule skills;
- Claude Code project instructions, thin skill adapters, subagents, launcher, and
  the project Playwright MCP configuration;
- living rules, templates, and previous-review memory;
- lightweight challenge-registry metadata without bulky pilot payloads;
- accepted examples and Shipd challenge archives;
- empty ignored working and output roots for future challenge runs.

## Runtime services

The folder does not bundle executables, accounts, or remote services. Running the workflow still requires:

- Codex with browser control, or Claude Code with Node.js 20+ and Playwright MCP;
- Python available as `py` or `python`;
- internet access;
- the installed browser-control capability;
- an authenticated Shipd session.

These are runtime requirements, not external workspace-file dependencies.

## Invariant

No configuration entry may be absolute or escape the bot root. Do not create junctions or symlinks inside the bot. New downloads, evidence, source packages, prepared data, graders, and runtime state must be written beneath this directory, but runtime payloads remain excluded from Git by `.gitignore`.

Historical audit documents may quote former absolute locations as provenance. Those quoted paths are archival evidence, not active configuration or lookup instructions.

Run `./validate-portable.ps1` after moving or copying the folder and before starting an Eris workflow.

The Claude adapters intentionally reference only files inside this repository.
They do not duplicate raw data or the canonical policy. Claude Code may ask once
to trust the project MCP configuration; that security approval is runtime state,
not a missing workspace dependency.
