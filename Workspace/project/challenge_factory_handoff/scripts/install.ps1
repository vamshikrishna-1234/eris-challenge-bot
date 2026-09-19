param(
    [string]$ProjectRoot = '',
    [string]$OutputRoot = '',
    [string]$MachineName = $env:COMPUTERNAME,
    [string]$CodexHome = (Join-Path $env:USERPROFILE '.codex')
)

$bundleRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $bundleRoot 'skills\eris-challenge-factory'
$skillsRoot = Join-Path $CodexHome 'skills'
$destination = Join-Path $skillsRoot 'eris-challenge-factory'

if (-not (Test-Path -LiteralPath (Join-Path $sourceSkill 'SKILL.md') -PathType Leaf)) {
    throw "Skill source is missing: $sourceSkill"
}

New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
New-Item -ItemType Directory -Path $destination -Force | Out-Null
Get-ChildItem -LiteralPath $sourceSkill -Force | Copy-Item -Destination $destination -Recurse -Force

$config = [ordered]@{
    project_root = $ProjectRoot
    output_root = $OutputRoot
    machine_name = $MachineName
}
$configPath = Join-Path $CodexHome 'eris-challenge-factory.json'
$config | ConvertTo-Json | Set-Content -LiteralPath $configPath -Encoding utf8

Write-Output "Installed skill: $destination"
Write-Output "Wrote config: $configPath"
Write-Output 'Restart Codex before using the skill.'
