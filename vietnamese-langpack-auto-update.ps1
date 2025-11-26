#!/usr/bin/env powershell

# =============================================================================
# VIETNAMESE LANGUAGE PACK - AUTO UPDATE SYSTEM (CORE ENGINE V2.0)
# Status: PRODUCTION READY | Security Checked
# =============================================================================

param(
    [string]$GitHubRepo = "HoangNghia-HoangGia/vscode-language-pack-vi",
    [string]$ExpectedSha256 = "",  # Optional expected hash published with release
    [switch]$ForceUpdate,
    [switch]$Silent
)

# =============================================================================
# CONFIGURATION
# =============================================================================

$ExtensionId = "vscode-language-pack-vi"
$AppDataDir = "$env:APPDATA\VSCodeVietnameseLangPack"
$TempDir = "$env:TEMP\VietnameseLangPack_Update"
$LogFile = Join-Path $AppDataDir "update-history.log"

if (-not (Test-Path $AppDataDir)) { New-Item -ItemType Directory -Path $AppDataDir -Force | Out-Null }

# =============================================================================
# LOGGING FUNCTION
# =============================================================================

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    if (-not $Silent) {
        $Color = switch ($Level) { "ERROR" {"Red"} "SUCCESS" {"Green"} "WARN" {"Yellow"} Default {"White"} }
        Write-Host $LogEntry -ForegroundColor $Color
    }
    try { Add-Content -Path $LogFile -Value $LogEntry -ErrorAction SilentlyContinue } catch {}
}

# =============================================================================
# SMART VS CODE DETECTION (PATH + COMMON LOCATIONS)
# =============================================================================

function Get-VSCodePath {
    if (Get-Command "code" -ErrorAction SilentlyContinue) { return "code" }
    $CommonPaths = @(
        "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd",
        "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd",
        "$env:ProgramFiles(x86)\Microsoft VS Code\bin\code.cmd"
    )
    foreach ($path in $CommonPaths) { if (Test-Path $path) { return $path } }
    return $null
}

# =============================================================================
# SECURITY: INTEGRITY CHECK (OPTIONAL SHA256)
# =============================================================================

function Verify-FileIntegrity {
    param([string]$FilePath, [string]$ExpectedHash)
    if (-not $ExpectedHash) {
        Write-Log "No hash provided – skipping integrity verification." "WARN"
        return $true
    }
    try {
        $FileHash = (Get-FileHash $FilePath -Algorithm SHA256).Hash
        if ($FileHash -eq $ExpectedHash) {
            Write-Log "Integrity check passed (SHA256 matches)." "SUCCESS"
            return $true
        } else {
            Write-Log "SHA256 mismatch. Expected: $ExpectedHash | Actual: $FileHash" "ERROR"
            return $false
        }
    } catch {
        Write-Log "Failed to compute file hash: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# =============================================================================
# MAIN UPDATE LOGIC
# =============================================================================

function Start-AutoUpdate {
    Write-Log "=== AUTO UPDATE STARTED ==="

    if ($GitHubRepo -match "DUNG-CAN-THAY-THE-BANG-REPO-THAT") {
        Write-Log "Placeholder GitHubRepo detected. Please provide a real repository." "ERROR"
        return $false
    }

    $CodeCommand = Get-VSCodePath
    if (-not $CodeCommand) {
        Write-Log "VS Code executable not found in PATH or standard locations." "ERROR"
        return $false
    }

    # Get current installed version
    $currentVer = "0.0.0"
    try {
        $extensions = & $CodeCommand --list-extensions --show-versions 2>$null
        $match = ($extensions | Select-String "$ExtensionId@(.+)" -AllMatches).Matches
        if ($match.Count -gt 0) {
            $currentVer = $match[0].Groups[1].Value
            Write-Log "Current installed version: $currentVer"
        } else {
            Write-Log "Extension not installed – fresh install will proceed." "WARN"
        }
    } catch {
        Write-Log "Failed to enumerate installed extensions: $($_.Exception.Message)" "ERROR"
        return $false
    }

    # Query latest release
    try {
        $apiUrl = "https://api.github.com/repos/$GitHubRepo/releases/latest"
        $response = Invoke-RestMethod -Uri $apiUrl -Method Get -ErrorAction Stop
        $latestVer = $response.tag_name -replace "^v", ""
        Write-Log "Latest available version: $latestVer"
    } catch {
        Write-Log "Failed to query GitHub latest release: $($_.Exception.Message)" "ERROR"
        return $false
    }

    # Version comparison
    try {
        if ([Version]$latestVer -le [Version]$currentVer -and -not $ForceUpdate) {
            Write-Log "Already up to date (installed: $currentVer | latest: $latestVer)." "SUCCESS"
            return $true
        }
    } catch {
        Write-Log "Version comparison failed: $($_.Exception.Message)" "ERROR"
        return $false
    }

    # Acquire VSIX asset
    $vsixAsset = $response.assets | Where-Object { $_.name -match "\.vsix$" } | Select-Object -First 1
    if (-not $vsixAsset) {
        Write-Log "No VSIX asset found in latest release." "ERROR"
        return $false
    }

    # Prepare temp directory
    if (-not (Test-Path $TempDir)) { New-Item -ItemType Directory -Path $TempDir -Force | Out-Null }
    $downloadPath = Join-Path $TempDir $vsixAsset.name
    Write-Log "Downloading VSIX: $($vsixAsset.name)"
    try {
        Invoke-WebRequest -Uri $vsixAsset.browser_download_url -OutFile $downloadPath -UseBasicParsing -ErrorAction Stop
        Write-Log "Download complete: $downloadPath" "SUCCESS"
    } catch {
        Write-Log "Failed to download VSIX: $($_.Exception.Message)" "ERROR"
        return $false
    }

    # Integrity verification (optional)
    if (-not (Verify-FileIntegrity -FilePath $downloadPath -ExpectedHash $ExpectedSha256)) {
        Write-Log "Aborting update due to failed integrity check." "ERROR"
        return $false
    }

    # Install extension
    Write-Log "Installing extension (force overwrite)..."
    $installOutput = & $CodeCommand --install-extension $downloadPath --force 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "Update successful. Installed version: $latestVer" "SUCCESS"
        return $true
    } else {
        Write-Log "Extension installation failed. Output: $installOutput" "ERROR"
        return $false
    }
}

# =============================================================================
# EXECUTION WRAPPER WITH CLEANUP
# =============================================================================

try {
    $result = Start-AutoUpdate
} catch {
    Write-Log "Critical failure: $($_.Exception.Message)" "ERROR"
    $result = $false
} finally {
    if (Test-Path $TempDir) { Remove-Item $TempDir -Recurse -Force -ErrorAction SilentlyContinue }
    Write-Log "Cleanup complete." "INFO"
    if (-not $Silent) { Write-Host "Process finished. Result: $result" }
}
