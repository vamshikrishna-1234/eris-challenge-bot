param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [Parameter(Mandatory = $true)]
    [string]$OutputRoot
)

$project = [System.IO.Path]::GetFullPath($ProjectRoot)
$output = [System.IO.Path]::GetFullPath($OutputRoot)

$checks = [ordered]@{
    project_root = Test-Path -LiteralPath $project -PathType Container
    output_root = Test-Path -LiteralPath $output -PathType Container
    latest_rules = Test-Path -LiteralPath (Join-Path $project 'rules\LATEST.md') -PathType Leaf
    checkpoints = Test-Path -LiteralPath (Join-Path $project 'rules\checkpoints')
    previous_reviews = Test-Path -LiteralPath (Join-Path $project 'rules\prev_reviews.txt') -PathType Leaf
    cursor_rule = Test-Path -LiteralPath (Join-Path $project '.cursor\rules\challenge-creation.mdc') -PathType Leaf
    accepted_examples = (Test-Path -LiteralPath (Join-Path $project 'sprint_3\accepted') -PathType Container) -or
        (Test-Path -LiteralPath (Join-Path $output 'accepted') -PathType Container)
}

$critical = @('project_root', 'output_root', 'latest_rules', 'checkpoints', 'previous_reviews')
$missing = @($critical | Where-Object { -not $checks[$_] })

[ordered]@{
    project_root = $project
    output_root = $output
    checks = $checks
    critical_missing = $missing
    ready = ($missing.Count -eq 0)
} | ConvertTo-Json -Depth 4

if ($missing.Count -gt 0) {
    exit 1
}
