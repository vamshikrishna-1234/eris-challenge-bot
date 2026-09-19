$ErrorActionPreference = 'Stop'
$validator = Join-Path $PSScriptRoot 'validate-portable.ps1'
$controller = Join-Path $PSScriptRoot 'eris_automation\run.ps1'

if (-not (Test-Path -LiteralPath $validator)) {
    throw "Missing portability validator: $validator"
}
if (-not (Test-Path -LiteralPath $controller)) {
    throw "Missing Eris controller: $controller"
}

& $validator | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw 'Portable workspace validation failed. Run .\validate-portable.ps1 for details.'
}

& $controller @args
exit $LASTEXITCODE
