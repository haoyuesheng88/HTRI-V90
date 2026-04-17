$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceRoot = Join-Path $repoRoot "skills"
$targetRoot = Join-Path $env:USERPROFILE ".codex\skills"

if (-not (Test-Path $sourceRoot)) {
    throw "Source skills folder not found: $sourceRoot"
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

Get-ChildItem $sourceRoot -Directory | ForEach-Object {
    $targetPath = Join-Path $targetRoot $_.Name
    Copy-Item $_.FullName $targetPath -Recurse -Force
    Write-Host "Installed skill:" $_.Name "->" $targetPath
}

Write-Host "Done. Restart Codex if it is already running."
