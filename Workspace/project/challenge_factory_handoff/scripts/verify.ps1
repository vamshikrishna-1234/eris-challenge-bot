param(
    [string]$CodexHome = (Join-Path $env:USERPROFILE '.codex')
)

$skill = Join-Path $CodexHome 'skills\eris-challenge-factory\SKILL.md'
$configPath = Join-Path $CodexHome 'eris-challenge-factory.json'

$result = [ordered]@{
    skill_installed = Test-Path -LiteralPath $skill -PathType Leaf
    config_present = Test-Path -LiteralPath $configPath -PathType Leaf
    project_root_exists = $false
    output_root_exists = $false
}

if ($result.config_present) {
    $config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    $result.project_root_exists = -not [string]::IsNullOrWhiteSpace($config.project_root) -and
        (Test-Path -LiteralPath $config.project_root -PathType Container)
    $result.output_root_exists = -not [string]::IsNullOrWhiteSpace($config.output_root) -and
        (Test-Path -LiteralPath $config.output_root -PathType Container)
}

$result | ConvertTo-Json

if (-not $result.skill_installed -or -not $result.config_present) {
    exit 1
}
