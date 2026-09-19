# Validation Record

Run the following after controller or skill changes:

```powershell
py .\eris_automation\Audit\tests\test_flow.py
.\validate-portable.ps1
py .\eris_automation\Tools\quick_validate_skill.py .\.codex\skills\eris-challenge-automation
py .\eris_automation\Tools\quick_validate_skill.py .\.codex\skills\eris-challenge-factory
py .\eris_automation\Tools\quick_validate_skill.py .\.codex\skills\eris-submission-pool
py .\eris_automation\Tools\quick_validate_skill.py .\.codex\skills\eris-solver-rules
```

Required properties:

- exact positive batch count;
- one active batch at a time;
- immutable task IDs;
- revisions do not increase the count;
- `Ready` preserves nonterminal work and all evidence;
- local status never claims a live check;
- registry binding requires an existing record;
- traversal-style IDs are rejected;
- skill metadata and resource links validate.
