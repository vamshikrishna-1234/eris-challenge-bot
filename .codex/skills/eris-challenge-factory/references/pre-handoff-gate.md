# Pre-Handoff Proceed Gate

Use this gate after the bounded pilot and before creating a full challenge-building task.

## Required Registry Object

Add a `readiness` object to the challenge registry JSON:

```json
{
  "readiness": {
    "verdict": "Proceed",
    "native_targets_verified": true,
    "official_access_verified": true,
    "redistribution_verified": true,
    "source_package_verified": true,
    "post_filter_scale_passed": true,
    "split_stability_passed": true,
    "semantic_duplicate_audit_passed": true,
    "lookup_attack_passed": true,
    "capability_matched_baseline_passed": true,
    "null_metric_audit_passed": true,
    "import_route_verified": true,
    "reviewer_premortem_completed": true,
    "unresolved_gates": []
  }
}
```

Keep measured counts, methods, scores, runtimes, URLs, bytes, and representative source rows in the sibling `evidence` object. Boolean claims without that evidence do not count.

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\validate_handoff_readiness.ps1 -StatusFile <registry-json>
```

## Failure-Informed Stop Rules

- **Missing native answer:** Reject when the desired target is absent and would require manual, heuristic, parser-generated, or LLM-created truth.
- **Unmeasured post-filter scale:** Pilot. Candidate totals and projected yield are not usable-row counts.
- **Too few independent groups:** Reject or expand the official source before handoff. Do not rely on many crops/windows from a few physical sources.
- **Public answer reversibility:** Hold or reject when exact source matching recovers hidden answers. Require a private/unpublished holdout or a measured transformation that defeats a strong modality-specific retrieval attack without destroying the task.
- **Canonical-task reskin:** Reject when the source benchmark and proposed challenge have substantially the same input, target, and solver, even if the output is wrapped in JSON or renamed.
- **Platform semantic duplicate risk:** Pilot until the core target differs materially from known platform clusters. Rewording is not mitigation.
- **Toy-baseline gap:** Pilot when only priors or weak models have been tested. Run the strongest obvious domain algorithm before `Proceed`.
- **Metric-null shortcut:** Redesign when no-op, copied-input, empty, or one-head-only submissions retain substantial score relative to the intended baseline.
- **Single-group hidden test:** Reject or rebuild the split. A described worst-group metric is invalid when the test contains one group.
- **Unavailable authenticated source:** Hold. Do not open a build task that requires credentials not configured on the builder machine.
- **Unverified import route:** Pilot. Confirm the exact official URLs/files fit platform and raw-size limits before handoff.

## Reviewer Premortem

Answer these before `Proceed`:

1. What is the closest source benchmark and why is this a different learning problem?
2. What is the closest local or platform semantic cluster and why will originality survive?
3. What native artifact supplies every scored field?
4. How many usable rows and independent hidden groups remain after every filter?
5. Why is every input modality necessary? Report ablations.
6. How does a no-op, copied input, empty output, and one-head-only output score?
7. What capable solver is most likely to break the task, and what measured score did it obtain?
8. Can the public source recover hidden answers by exact, fuzzy, geometric, temporal, or signal retrieval?
9. Can the exact raw package be imported now, within the size and license rules?
10. What single result would still force rejection?

Any answer that says "the build task will find out" means the verdict is `Pilot`, not `Proceed`.
