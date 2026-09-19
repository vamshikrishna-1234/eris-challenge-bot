param(
    [Parameter(Mandatory = $true)]
    [string]$RegistryRoot,

    [Parameter(Mandatory = $true)]
    [string]$Title,

    [Parameter(Mandatory = $true)]
    [string]$OwnerMachine,

    [string]$OwnerTask = '',
    [string]$OutputFolder = '',
    [string]$Dataset = '',
    [string]$License = '',
    [ValidateSet('idea', 'claimed', 'researching', 'building', 'blocked', 'ready_for_review', 'submitted', 'accepted', 'rejected', 'abandoned')]
    [string]$Status = 'claimed'
)

$registry = [System.IO.Path]::GetFullPath($RegistryRoot)
New-Item -ItemType Directory -Path $registry -Force | Out-Null

$slug = $Title.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
$slug = $slug.Trim('-')
if ([string]::IsNullOrWhiteSpace($slug)) {
    throw 'Title does not contain a usable ASCII slug.'
}

$path = Join-Path $registry ($slug + '.json')
if (Test-Path -LiteralPath $path) {
    throw "Challenge is already registered: $path"
}

$now = [DateTimeOffset]::Now.ToString('o')
[ordered]@{
    title = $Title
    slug = $slug
    status = $Status
    owner_machine = $OwnerMachine
    owner_task = $OwnerTask
    output_folder = $OutputFolder
    dataset = $Dataset
    license = $License
    created_at = $now
    updated_at = $now
    blocker = ''
    notes = @()
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $path -Encoding utf8

Write-Output $path
