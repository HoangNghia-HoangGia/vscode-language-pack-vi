# =============================================================================
# VIETNAMESE LANGUAGE PACK - AUTO UPDATE SETUP (V2.0)
# Focus: Register Scheduled Task only (Separation of Concerns)
# =============================================================================

param(
    [string]$GitHubRepo = "HoangNghia-HoangGia/vscode-language-pack-vi"
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SETUP: VSCode Vietnamese Auto-Update Task (V2.0)" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Admin privilege check
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Script can chay voi quyen Administrator. Hay mo PowerShell Run as Administrator."
    exit 1
}

# Validate repo placeholder
if ($GitHubRepo -match "DUNG-CAN-THAY-THE-BANG-REPO-THAT") {
    Write-Host "Ban chua thay the bien GitHubRepo bang repo that." -ForegroundColor Red
    exit 1
}

$CoreScript = "vietnamese-langpack-auto-update.ps1"
$ScriptPath = Join-Path $PSScriptRoot $CoreScript
if (-not (Test-Path $ScriptPath)) {
    Write-Host "Khong tim thay core script: $CoreScript" -ForegroundColor Red
    exit 1
}

# Task definition
$TaskName = "VSCode_Vietnamese_AutoUpdate"
$ActionArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`" -GitHubRepo `"$GitHubRepo`" -Silent"

Write-Host "Dang cau hinh Scheduled Task..." -ForegroundColor White

try {
    # Remove old task if exists (idempotent behavior)
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue | Out-Null
    Write-Host "Da lam sach task cu (neu ton tai)" -ForegroundColor Gray

    $Action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $ActionArgs
    $Trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 09:00am
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Auto-update for VS Code Vietnamese Language Pack" | Out-Null

    Write-Host "Task da tao thanh cong" -ForegroundColor Green
    Write-Host "   Ten Task: $TaskName" -ForegroundColor White
    Write-Host "   Lich chay: Chu Nhat 09:00 AM (Weekly)" -ForegroundColor White
    Write-Host "   Core Script: $ScriptPath" -ForegroundColor White
    Write-Host "   Log: %APPDATA%\VSCodeVietnameseLangPack\update-history.log" -ForegroundColor White
} catch {
    Write-Host "Loi khi tao task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "HUONG DAN TIEP THEO:" -ForegroundColor Cyan
Write-Host "   1. Co the chay thu cong: powershell -File $CoreScript" -ForegroundColor White
Write-Host "   2. Them SHA256 trong tham so -ExpectedSha256." -ForegroundColor White
Write-Host ""
Write-Host "HE THONG SAN SANG!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Read-Host "Nhan Enter de ket thuc setup"