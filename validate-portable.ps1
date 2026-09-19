$ErrorActionPreference = 'Stop'

$root = [System.IO.Path]::GetFullPath($PSScriptRoot)
$configPath = Join-Path $root 'Config\workspace.json'
$failures = [System.Collections.Generic.List[string]]::new()
$checks = [ordered]@{}

function Resolve-InternalPath {
    param([Parameter(Mandatory = $true)][string]$Value)

    # Windows PowerShell 5.1 runs on .NET Framework, which does not expose
    # Path.IsPathFullyQualified. IsPathRooted is sufficient here because every
    # rooted value is forbidden by this portable, bot-root-relative config.
    if ([System.IO.Path]::IsPathRooted($Value)) {
        $failures.Add("Absolute configuration path: $Value")
        return $null
    }
    $resolved = [System.IO.Path]::GetFullPath((Join-Path $root $Value))
    $prefix = $root.TrimEnd('\') + '\'
    if (-not $resolved.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $failures.Add("Configuration path escapes bot root: $Value")
        return $null
    }
    return $resolved
}

if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    throw "Missing configuration: $configPath"
}

$config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json
$pathFields = @(
    'shared_project_root',
    'challenge_registry',
    'rules',
    'challenge_output_root',
    'working_root',
    'controller',
    'bundled_skill',
    'factory_skill',
    'submission_skill',
    'solver_rules_skill',
    'claude_skill',
    'claude_runtime_reference',
    'claude_mcp_config'
)

$resolved = @{}
foreach ($field in $pathFields) {
    $value = $config.$field
    if ([string]::IsNullOrWhiteSpace($value)) {
        $failures.Add("Missing configuration field: $field")
        continue
    }
    $resolved[$field] = Resolve-InternalPath $value
}

foreach ($field in @('shared_project_root', 'challenge_registry', 'rules', 'challenge_output_root', 'working_root')) {
    $ok = $resolved[$field] -and (Test-Path -LiteralPath $resolved[$field] -PathType Container)
    $checks[$field] = [bool]$ok
    if (-not $ok) { $failures.Add("Missing directory for $field") }
}

foreach ($field in @('controller', 'bundled_skill', 'factory_skill', 'submission_skill', 'solver_rules_skill', 'claude_skill', 'claude_runtime_reference', 'claude_mcp_config')) {
    $ok = $resolved[$field] -and (Test-Path -LiteralPath $resolved[$field] -PathType Leaf)
    $checks[$field] = [bool]$ok
    if (-not $ok) { $failures.Add("Missing file for $field") }
}

$requiredFiles = @(
    'AGENTS.md',
    'CLAUDE.md',
    'CLAUDE_SETUP.md',
    'README.md',
    'PORTABILITY.md',
    'BUNDLE_MANIFEST.json',
    'RESILIENT_5_TASK_PROMPT.md',
    'run.ps1',
    'run-claude.ps1',
    '.mcp.json',
    'eris_automation\Tools\flow.py',
    '.codex\skills\eris-challenge-automation\references\linked-drafts.md',
    '.codex\skills\eris-challenge-automation\references\resilience.md',
    '.codex\skills\eris-challenge-automation\references\visible-workers.md',
    '.claude\skills\eris-challenge-automation\SKILL.md',
    '.claude\skills\eris-challenge-automation\references\claude-runtime.md',
    '.claude\skills\eris-challenge-factory\SKILL.md',
    '.claude\skills\eris-submission-pool\SKILL.md',
    '.claude\skills\eris-solver-rules\SKILL.md',
    '.claude\agents\eris-slot-worker.md',
    '.claude\agents\eris-supervisor.md',
    'Workspace\project\rules\LATEST.md',
    'Workspace\project\rules\prev_reviews.txt',
    'Workspace\project\.cursor\rules\challenge-creation.mdc',
    'Workspace\project\challenge_registry\_schema.json',
    'Workspace\project\sprint_3\problems_with_acceptances.txt'
)
foreach ($relative in $requiredFiles) {
    $ok = Test-Path -LiteralPath (Join-Path $root $relative) -PathType Leaf
    $checks["file:$relative"] = [bool]$ok
    if (-not $ok) { $failures.Add("Missing required file: $relative") }
}

$reparsePoints = @(Get-ChildItem -LiteralPath $root -Force -Recurse -Attributes ReparsePoint -ErrorAction SilentlyContinue)
$checks['no_reparse_points'] = ($reparsePoints.Count -eq 0)
foreach ($item in $reparsePoints) {
    $failures.Add("Reparse point is not portable: $($item.FullName)")
}

$coreFiles = @(
    'AGENTS.md',
    'CLAUDE.md',
    'CLAUDE_SETUP.md',
    'README.md',
    'RESILIENT_5_TASK_PROMPT.md',
    'PORTABILITY.md',
    'Config\workspace.json',
    'run.ps1',
    'run-claude.ps1',
    '.mcp.json',
    'eris_automation\run.ps1',
    '.codex\skills\eris-challenge-automation\SKILL.md',
    '.codex\skills\eris-challenge-automation\references\linked-drafts.md',
    '.codex\skills\eris-challenge-automation\references\resilience.md',
    '.codex\skills\eris-challenge-automation\references\visible-workers.md',
    '.codex\skills\eris-challenge-factory\SKILL.md',
    '.codex\skills\eris-submission-pool\SKILL.md',
    '.claude\skills\eris-challenge-automation\SKILL.md',
    '.claude\skills\eris-challenge-automation\references\claude-runtime.md',
    '.claude\skills\eris-challenge-factory\SKILL.md',
    '.claude\skills\eris-submission-pool\SKILL.md',
    '.claude\skills\eris-solver-rules\SKILL.md',
    '.claude\agents\eris-slot-worker.md',
    '.claude\agents\eris-supervisor.md'
)
$legacyRoots = @(
    'C:\Users\vamsh\Downloads\create_challenge_synthetic',
    'D:\create_challenge_synthetic',
    'E:\create_challenge_synthetic_output_folder'
)
foreach ($relative in $coreFiles) {
    $path = Join-Path $root $relative
    $text = Get-Content -Raw -LiteralPath $path
    foreach ($legacy in $legacyRoots) {
        if ($text.IndexOf($legacy, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $failures.Add("Legacy external path in core file ${relative}: $legacy")
        }
    }
}
$checks['no_legacy_core_paths'] = -not ($failures | Where-Object { $_ -like 'Legacy external path*' })

try {
    $status = & (Join-Path $root 'eris_automation\run.ps1') status --json | ConvertFrom-Json
    $checks['controller_status'] = ($null -ne $status)
}
catch {
    $checks['controller_status'] = $false
    $failures.Add("Controller status failed: $($_.Exception.Message)")
}

$checks['external_file_dependencies_empty'] = @($config.external_file_dependencies).Count -eq 0
if (-not $checks['external_file_dependencies_empty']) {
    $failures.Add('Config declares external file dependencies')
}

try {
    $probeScript = Join-Path $root '.codex\skills\eris-challenge-factory\scripts\workspace_probe.ps1'
    $probe = & $probeScript -ProjectRoot $resolved['shared_project_root'] -OutputRoot $resolved['challenge_output_root'] | ConvertFrom-Json
    $checks['factory_workspace_probe'] = [bool]$probe.ready
    if (-not $probe.ready) { $failures.Add('Factory workspace probe is not ready') }
}
catch {
    $checks['factory_workspace_probe'] = $false
    $failures.Add("Factory workspace probe failed: $($_.Exception.Message)")
}

try {
    $skillValidator = Join-Path $root 'eris_automation\Tools\quick_validate_skill.py'
    $skillFolders = @(
        '.codex\skills\eris-challenge-automation',
        '.codex\skills\eris-challenge-factory',
        '.codex\skills\eris-submission-pool',
        '.codex\skills\eris-solver-rules',
        '.claude\skills\eris-challenge-automation',
        '.claude\skills\eris-challenge-factory',
        '.claude\skills\eris-submission-pool',
        '.claude\skills\eris-solver-rules'
    )
    $allSkillsValid = $true
    foreach ($relative in $skillFolders) {
        & py $skillValidator (Join-Path $root $relative) | Out-Null
        if ($LASTEXITCODE -ne 0) { $allSkillsValid = $false }
    }
    $checks['bundled_skill_validation'] = $allSkillsValid
    if (-not $allSkillsValid) { $failures.Add('One or more bundled skills failed validation') }
}
catch {
    $checks['bundled_skill_validation'] = $false
    $failures.Add("Bundled skill validation failed: $($_.Exception.Message)")
}

try {
    $mcp = Get-Content -Raw -LiteralPath (Join-Path $root '.mcp.json') | ConvertFrom-Json
    $playwright = $mcp.mcpServers.playwright
    $mcpValid = $playwright.command -eq 'npx' -and @($playwright.args) -contains '@playwright/mcp@latest'
    $checks['claude_playwright_mcp_config'] = [bool]$mcpValid
    if (-not $mcpValid) { $failures.Add('Claude Playwright MCP configuration is invalid') }
}
catch {
    $checks['claude_playwright_mcp_config'] = $false
    $failures.Add("Claude MCP configuration failed: $($_.Exception.Message)")
}

$result = [ordered]@{
    schema_version = 1
    bot_root = $root
    checked_at = (Get-Date).ToString('o')
    portable = ($failures.Count -eq 0)
    checks = $checks
    failures = @($failures)
    runtime_requirements = @('Codex or Claude Code', 'Python', 'Node.js 20+ for Claude Playwright MCP', 'internet', 'browser-control capability', 'authenticated Shipd session')
}
$result | ConvertTo-Json -Depth 6

if ($failures.Count -gt 0) { exit 1 }
