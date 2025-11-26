# =============================================================================
# VIETNAMESE LANGUAGE PACK - AUTO UPDATE SETUP (V2.0)
# Focus: Register Scheduled Task only (Separation of Concerns)
# =============================================================================

param(
    [string]$GitHubRepo = "HoangNghia-HoangGia/vscode-language-pack-vi"
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🇻🇳 SETUP: VSCode Vietnamese Auto-Update Task (V2.0)" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Admin privilege check
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Script cần chạy với quyền Administrator. Hãy mở PowerShell 'Run as Administrator'."
    exit 1
}

# Validate repo placeholder
if ($GitHubRepo -match "DUNG-CAN-THAY-THE-BANG-REPO-THAT") {
    Write-Host "⛔ Bạn chưa thay thế biến GitHubRepo bằng repo thật. Ví dụ: nguyenvana/vscode-vi" -ForegroundColor Red
    exit 1
}

$CoreScript = "vietnamese-langpack-auto-update.ps1"
$ScriptPath = Join-Path $PSScriptRoot $CoreScript
if (-not (Test-Path $ScriptPath)) {
    Write-Host "⛔ Không tìm thấy core script: $CoreScript" -ForegroundColor Red
    exit 1
}

# Task definition
$TaskName = "VSCode_Vietnamese_AutoUpdate"
$ActionArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`" -GitHubRepo `"$GitHubRepo`" -Silent"

Write-Host "🔧 Đang cấu hình Scheduled Task..." -ForegroundColor White

try {
    # Remove old task if exists (idempotent behavior)
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue | Out-Null
    Write-Host "• Đã làm sạch task cũ (nếu tồn tại)" -ForegroundColor Gray

    $Action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $ActionArgs
    $Trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 09:00am
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType InteractiveToken

    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Auto-update for VS Code Vietnamese Language Pack" | Out-Null

    Write-Host "✅ Task đã tạo thành công" -ForegroundColor Green
    Write-Host "   • Tên Task: $TaskName" -ForegroundColor White
    Write-Host "   • Lịch chạy: Chủ Nhật 09:00 AM (Weekly)" -ForegroundColor White
    Write-Host "   • Core Script: $ScriptPath" -ForegroundColor White
    Write-Host "   • Log: %APPDATA%\VSCodeVietnameseLangPack\update-history.log" -ForegroundColor White
} catch {
    Write-Host "❌ Lỗi khi tạo task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📌 HƯỚNG DẪN TIẾP THEO:" -ForegroundColor Cyan
Write-Host "   1. Có thể chạy thủ công: powershell -File $CoreScript -GitHubRepo $GitHubRepo" -ForegroundColor White
Write-Host "   2. Thêm SHA256 trong tham số -ExpectedSha256 để bật kiểm tra toàn vẹn." -ForegroundColor White
Write-Host "   3. Tạo file checksums.txt trong release để công bố mã hash." -ForegroundColor White
Write-Host ""
Write-Host "🚀 HỆ THỐNG SẴN SÀNG!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Read-Host "Nhấn Enter để kết thúc setup"