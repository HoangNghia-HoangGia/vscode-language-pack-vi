# DEV AUTO-UPDATE - Fast local development cycle
# Use this for rapid development and testing

Write-Host "`n=== VS CODE VIETNAM - DEV AUTO UPDATE ===`n" -ForegroundColor Cyan

# 1. Close VS Code
Write-Host "[1/6] Closing VS Code..." -ForegroundColor Yellow
taskkill /IM code.exe /F 2>$null
taskkill /IM Code.exe /F 2>$null
Start-Sleep -Seconds 2
Write-Host "OK VS Code closed" -ForegroundColor Green

# 2. Auto bump version
Write-Host "`n[2/6] Bumping version..." -ForegroundColor Yellow
$pkgPath = "package.json"
$pkgContent = Get-Content $pkgPath -Raw
$pkg = $pkgContent | ConvertFrom-Json
$ver = $pkg.version.Split('.')
$ver[2] = [int]$ver[2] + 1
$new = "$($ver[0]).$($ver[1]).$($ver[2])"

# Update version in original JSON format (preserve formatting)
$pkgContent = $pkgContent -replace '"version":\s*"[\d\.]+"', ('"version": "{0}"' -f $new)
$pkgContent | Set-Content $pkgPath -Encoding UTF8 -NoNewline
Write-Host "OK New version: $new" -ForegroundColor Green

# 3. Build VSIX
Write-Host "`n[3/6] Building VSIX..." -ForegroundColor Yellow
$vsix = "vscode-language-pack-vi-$new.vsix"
if (Test-Path $vsix) { Remove-Item $vsix -Force }
vsce package --out $vsix | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "X Failed to build VSIX" -ForegroundColor Red
    exit 1
}
$size = (Get-Item $vsix).Length / 1KB
Write-Host "OK VSIX built: $vsix ($([math]::Round($size, 2)) KB)" -ForegroundColor Green

# 4. Uninstall old version
Write-Host "`n[4/6] Removing old extension..." -ForegroundColor Yellow
code --uninstall-extension HoangNghia-HoangGia.vscode-language-pack-vi --force 2>$null | Out-Null
Get-ChildItem "$env:USERPROFILE\.vscode\extensions" -Filter "hoangnghia-hoanggia*" -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Write-Host "OK Old version removed" -ForegroundColor Green

# 5. Install new version
Write-Host "`n[5/6] Installing new version..." -ForegroundColor Yellow
code --install-extension $vsix --force | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "X Failed to install extension" -ForegroundColor Red
    exit 1
}
Write-Host "OK New version installed" -ForegroundColor Green

# 6. Force Vietnamese language
Write-Host "`n[6/6] Setting locale to Vietnamese..." -ForegroundColor Yellow
$localeDir = "$env:APPDATA\Code\User"
if (-not (Test-Path $localeDir)) {
    New-Item -ItemType Directory -Path $localeDir -Force | Out-Null
}
$locale = Join-Path $localeDir "locale.json"
@{ "locale"="vi" } | ConvertTo-Json | Set-Content $locale -Encoding UTF8
Write-Host "OK locale.json updated" -ForegroundColor Green

# Done
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DONE! Opening VS Code with Vietnamese UI..." -ForegroundColor Green
Write-Host "Version: $new" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Start-Sleep -Seconds 1
Start-Process "code" -ArgumentList "."

Write-Host "TIP: Use this script every time you edit translations/" -ForegroundColor Yellow
Write-Host "     No Marketplace needed for local testing!" -ForegroundColor Yellow
