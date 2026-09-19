param(
    [string]$Destination = ''
)

$bundleRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($Destination)) {
    $Destination = Join-Path (Split-Path -Parent $bundleRoot) 'challenge_factory_handoff.zip'
}

$destinationPath = [System.IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationPath) {
    Remove-Item -LiteralPath $destinationPath -Force
}

$bundleItems = Get-ChildItem -LiteralPath $bundleRoot -Force | Select-Object -ExpandProperty FullName
Compress-Archive -LiteralPath $bundleItems -DestinationPath $destinationPath -CompressionLevel Optimal
Write-Output $destinationPath
