$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot 'Tools\flow.py'
$workspaceRoot = Split-Path $PSScriptRoot -Parent
$configPath = Join-Path $workspaceRoot 'Config\workspace.json'

if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Missing controller: $scriptPath"
}
if (-not (Test-Path -LiteralPath $configPath)) {
    throw "Missing workspace configuration: $configPath"
}

$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json

function Resolve-PortablePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ConfiguredPath
    )

    if ([System.IO.Path]::IsPathRooted($ConfiguredPath)) {
        throw "Portable workspace paths must be relative to the bot root: $ConfiguredPath"
    }

    $resolved = [System.IO.Path]::GetFullPath((Join-Path $workspaceRoot $ConfiguredPath))
    $rootPrefix = $workspaceRoot.TrimEnd('\') + '\'
    if (-not $resolved.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Configured path escapes the bot root: $ConfiguredPath"
    }
    return $resolved
}

$projectRoot = Resolve-PortablePath $config.shared_project_root
$outputRoot = Resolve-PortablePath $config.challenge_output_root
$registryRoot = Resolve-PortablePath $config.challenge_registry
$rulesRoot = Resolve-PortablePath $config.rules

foreach ($required in @($projectRoot, $outputRoot, $registryRoot, $rulesRoot)) {
    if (-not (Test-Path -LiteralPath $required -PathType Container)) {
        throw "Required portable workspace directory is unavailable: $required"
    }
}

$previousProjectRoot = $env:ERIS_PROJECT_ROOT
$previousOutputRoot = $env:ERIS_OUTPUT_ROOT
$previousRegistryRoot = $env:ERIS_REGISTRY_ROOT
$previousRulesRoot = $env:ERIS_RULES_ROOT
$previousAutomationHome = $env:ERIS_AUTOMATION_HOME
$env:ERIS_PROJECT_ROOT = $projectRoot
$env:ERIS_OUTPUT_ROOT = $outputRoot
$env:ERIS_REGISTRY_ROOT = $registryRoot
$env:ERIS_RULES_ROOT = $rulesRoot
$env:ERIS_AUTOMATION_HOME = $PSScriptRoot

try {
    $python = Get-Command py -ErrorAction SilentlyContinue
    if ($null -ne $python) {
        & py $scriptPath @args
    } else {
        & python $scriptPath @args
    }
    $controllerExitCode = $LASTEXITCODE
}
finally {
    $env:ERIS_PROJECT_ROOT = $previousProjectRoot
    $env:ERIS_OUTPUT_ROOT = $previousOutputRoot
    $env:ERIS_REGISTRY_ROOT = $previousRegistryRoot
    $env:ERIS_RULES_ROOT = $previousRulesRoot
    $env:ERIS_AUTOMATION_HOME = $previousAutomationHome
}
exit $controllerExitCode
