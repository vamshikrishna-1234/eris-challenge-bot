"""Python reimplementation of .codex/skills/eris-challenge-factory/scripts/validate_handoff_readiness.ps1
(PowerShell is unavailable in this container). Same checks: readiness object present, verdict Proceed,
twelve required booleans true, no unresolved gates, evidence object present."""
import json, sys
REQUIRED=["native_targets_verified","official_access_verified","redistribution_verified","source_package_verified",
 "post_filter_scale_passed","split_stability_passed","semantic_duplicate_audit_passed","lookup_attack_passed",
 "capability_matched_baseline_passed","null_metric_audit_passed","import_route_verified","reviewer_premortem_completed"]
rec=json.load(open(sys.argv[1],encoding='utf-8-sig')); errors=[]
r=rec.get('readiness')
if r is None: errors.append('Missing readiness object.')
else:
    if r.get('verdict')!='Proceed': errors.append(f"Readiness verdict must be Proceed; found '{r.get('verdict')}'.")
    for f in REQUIRED:
        if r.get(f) is not True: errors.append(f'readiness.{f} must be true.')
    if r.get('unresolved_gates'): errors.append('Unresolved gates remain: '+'; '.join(r['unresolved_gates']))
if rec.get('evidence') is None or rec.get('evidence')=={}: errors.append('Missing measured evidence object.')
if errors: print('NOT BUILD READY\n- '+'\n- '.join(errors)); sys.exit(1)
print('BUILD READY:',rec.get('title')); sys.exit(0)
