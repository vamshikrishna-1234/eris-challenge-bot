param(
    [Parameter(Mandatory = $true)]
    [string]$StatusFile
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $StatusFile -PathType Leaf)) {
    throw "Registry status file not found: $StatusFile"
}

$record = Get-Content -LiteralPath $StatusFile -Raw | ConvertFrom-Json
$errors = [System.Collections.Generic.List[string]]::new()

if ($null -eq $record.readiness) {
    $errors.Add("Missing readiness object.")
} else {
    if ($record.readiness.verdict -ne "Proceed") {
        $errors.Add("Readiness verdict must be Proceed; found '$($record.readiness.verdict)'.")
    }

    $requiredTrue = @(
        "native_targets_verified",
        "official_access_verified",
        "redistribution_verified",
        "source_package_verified",
        "post_filter_scale_passed",
        "split_stability_passed",
        "semantic_duplicate_audit_passed",
        "lookup_attack_passed",
        "capability_matched_baseline_passed",
        "null_metric_audit_passed",
        "import_route_verified",
        "reviewer_premortem_completed"
    )

    foreach ($field in $requiredTrue) {
        $property = $record.readiness.PSObject.Properties[$field]
        if ($null -eq $property -or $property.Value -ne $true) {
            $errors.Add("readiness.$field must be true.")
        }
    }

    $unresolved = @($record.readiness.unresolved_gates)
    if ($unresolved.Count -gt 0) {
        $errors.Add("Unresolved gates remain: $($unresolved -join '; ')")
    }
}

if ($null -eq $record.evidence) {
    $errors.Add("Missing measured evidence object.")
}

if ($errors.Count -gt 0) {
    Write-Error ("NOT BUILD READY`n- " + ($errors -join "`n- "))
    exit 1
}

Write-Output "BUILD READY: $($record.title)"
exit 0
