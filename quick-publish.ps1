# QUICK PUBLISH - Production release to Marketplace
# Use this when ready to release to all users

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('major', 'minor', 'patch')]
    [string]$BumpType = 'patch',
    
    [Parameter(Mandatory=$false)]
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"

Write-Host "`n=== VS CODE VIETNAM - MARKETPLACE PUBLISH ===`n" -ForegroundColor Cyan

Set-Location "c:\Users\Admin\Desktop\VS CODE VN\vscode-language-pack-vi"

# 1. Check vsce
Write-Host "[1/7] Checking vsce..." -ForegroundColor Yellow
$vsceCheck = Get-Command vsce -ErrorAction SilentlyContinue
if ($null -eq $vsceCheck) {
    Write-Host "X vsce not found. Installing..." -ForegroundColor Red
    npm install -g @vscode/vsce
}
Write-Host "OK vsce ready" -ForegroundColor Green

# 2. Read current version
Write-Host "`n[2/7] Reading current version..." -ForegroundColor Yellow
$pkgPath = "package.json"
$pkgContent = Get-Content $pkgPath -Raw
$pkg = $pkgContent | ConvertFrom-Json
$currentVersion = $pkg.version
Write-Host "OK Current version: $currentVersion" -ForegroundColor Green

# 3. Bump version
Write-Host "`n[3/7] Bumping version ($BumpType)..." -ForegroundColor Yellow
$versionParts = $currentVersion -split '\.'
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]
$patch = [int]$versionParts[2]

switch ($BumpType) {
    'major' {
        $major++
        $minor = 0
        $patch = 0
    }
    'minor' {
        $minor++
        $patch = 0
    }
    'patch' {
        $patch++
    }
}

$newVersion = "$major.$minor.$patch"
Write-Host "OK New version: $newVersion" -ForegroundColor Green

# 4. Update package.json (preserve formatting)
Write-Host "`n[4/7] Updating package.json..." -ForegroundColor Yellow
$pkgContent = $pkgContent -replace '"version":\s*"[\d\.]+"', ('"version": "{0}"' -f $newVersion)
$pkgContent | Set-Content $pkgPath -Encoding UTF8 -NoNewline
Write-Host "OK package.json updated" -ForegroundColor Green

# 5. Build VSIX
Write-Host "`n[5/7] Building VSIX..." -ForegroundColor Yellow
$vsixFile = "vscode-language-pack-vi-$newVersion.vsix"
if (Test-Path $vsixFile) {
    Remove-Item $vsixFile -Force
}
vsce package --out $vsixFile | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "X Failed to build VSIX" -ForegroundColor Red
    exit 1
}
$vsixSize = (Get-Item $vsixFile).Length / 1KB
Write-Host "OK VSIX built: $vsixFile ($([math]::Round($vsixSize, 2)) KB)" -ForegroundColor Green

# 6. Publish to Marketplace
Write-Host "`n[6/7] Publishing to Marketplace..." -ForegroundColor Yellow
Write-Host "Publisher: HoangNghia-HoangGia" -ForegroundColor Cyan
Write-Host "Version: $newVersion" -ForegroundColor Cyan

vsce publish --packagePath $vsixFile
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nX Failed to publish" -ForegroundColor Red
    Write-Host "`nCommon issues:" -ForegroundColor Yellow
    Write-Host "1. Not logged in: vsce login HoangNghia-HoangGia" -ForegroundColor White
    Write-Host "2. Publisher does not exist: Create at https://marketplace.visualstudio.com/manage" -ForegroundColor White
    Write-Host "3. Invalid PAT: Check token has Marketplace > Manage scope" -ForegroundColor White
    exit 1
}

Write-Host "`nOK Successfully published v$newVersion to Marketplace!" -ForegroundColor Green

# 7. Git commit and tag
Write-Host "`n[7/7] Git commit and tag..." -ForegroundColor Yellow

if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "Release v$newVersion"
}

git add package.json
git commit -m $Message
git tag "v$newVersion"
git push origin main
git push origin "v$newVersion"

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Git committed and tagged" -ForegroundColor Green
} else {
    Write-Host "WARNING: Git operations may have failed (check manually)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "RELEASE COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Version: v$newVersion" -ForegroundColor White
Write-Host "Marketplace: https://marketplace.visualstudio.com/items?itemName=HoangNghia-HoangGia.vscode-language-pack-vi" -ForegroundColor Cyan
Write-Host "`nUsers can install via:" -ForegroundColor Yellow
Write-Host "  1. Search 'Vietnamese Language Pack' in VS Code Extensions" -ForegroundColor White
Write-Host "  2. code --install-extension HoangNghia-HoangGia.vscode-language-pack-vi" -ForegroundColor White
Write-Host "`nExisting users will receive auto-update notification!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
