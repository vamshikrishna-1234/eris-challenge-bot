$ErrorActionPreference = 'Stop'

$root = [System.IO.Path]::GetFullPath($PSScriptRoot)
Set-Location -LiteralPath $root

& (Join-Path $root 'validate-portable.ps1') | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw 'Portable-bundle validation failed. Repair the reported issue before starting Claude Code.'
}

$claudeCommand = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claudeCommand) {
    throw 'Claude Code is not installed or is not on PATH. See CLAUDE_SETUP.md.'
}

& $claudeCommand.Source --permission-mode auto @args
