param (
    [string]$SourcePath = "$PSScriptRoot\..",
    [string]$TargetFolderName = "null-void"
)

# Find Google Drive
$gdriveMatch = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -like "G:*" -or $_.Name -like "*Drive*" }
if (-not $gdriveMatch) {
    Write-Host "ERROR: Google Drive not found." -ForegroundColor Red
    exit 1
}

$gdriveRoot = $gdriveMatch.Root
$diskFolder = Get-ChildItem -LiteralPath $gdriveRoot | Where-Object { $_.Name -like "*disk*" -or $_.Name -like "My Drive" }

if (-not $diskFolder) {
    Write-Host "ERROR: Could not find 'Môj disk' folder." -ForegroundColor Red
    exit 1
}

$DestinationPath = Join-Path -Path $diskFolder.FullName -ChildPath $TargetFolderName

Write-Host "--- Google Drive Sync ---" -ForegroundColor Cyan
Write-Host "Source: $SourcePath"
Write-Host "Destination: $DestinationPath"

if (-not (Test-Path -LiteralPath $DestinationPath)) {
    New-Item -ItemType Directory -Force -Path $DestinationPath | Out-Null
}

# Simplified Robocopy for GDrive compatibility
# /S - Copy subdirectories
# /E - Copy subdirectories, including empty ones
# /PURGE - Delete dest files/dirs that no longer exist in source
# /COPY:DT - Copy Data and Timestamps (avoid Security/ACLs which GDrive rejects)
# /XD - Exclude directories
# /R:0 - No retries (for testing)
# /W:0 - No wait
Write-Host "Running robocopy..."
robocopy $SourcePath $DestinationPath /S /E /PURGE /COPY:DT /XD .git .vscode .gemini /R:1 /W:1 /NP /TEE

$exitCode = $LASTEXITCODE
if ($exitCode -lt 8) {
    Write-Host "Files copied. Duplicating .md to .txt..." -ForegroundColor Green
    
    # Workaround for NotebookLM: Copy .md files as .txt
    Get-ChildItem -LiteralPath $DestinationPath -Filter *.md -Recurse | ForEach-Object {
        $txtPath = $_.FullName -replace '\.md$', '.txt'
        Copy-Item -LiteralPath $_.FullName -Destination $txtPath -Force
    }
    Write-Host "Sync complete!" -ForegroundColor Green
} else {
    Write-Host "Sync failed with Robocopy exit code $exitCode" -ForegroundColor Red
    Write-Host "Trying fallback simple copy..." -ForegroundColor Yellow
    
    # Fallback to pure PowerShell copy if robocopy fails
    Copy-Item -Path "$SourcePath\*" -Destination $DestinationPath -Recurse -Force -Exclude ".git",".vscode",".gemini"
    Write-Host "Fallback sync complete!" -ForegroundColor Green
}
