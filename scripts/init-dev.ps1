[CmdletBinding()]
param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$BackendPath = Join-Path $RepoRoot "backend"
$FrontendPath = Join-Path $RepoRoot "frontend"
$VenvPath = Join-Path $BackendPath ".venv"
$PythonPath = Join-Path $VenvPath "Scripts\python.exe"
$PipPath = Join-Path $VenvPath "Scripts\pip.exe"

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $Command $($Arguments -join ' ')"
    }
}

if (-not $SkipBackend) {
    if (-not (Test-Path $VenvPath)) {
        Invoke-CheckedCommand -Command "python" -Arguments @("-m", "venv", $VenvPath)
    }

    Invoke-CheckedCommand -Command $PythonPath -Arguments @("-m", "pip", "install", "--upgrade", "pip")
    Invoke-CheckedCommand -Command $PipPath -Arguments @("install", "-r", (Join-Path $BackendPath "requirements.txt"))

    $BackendEnvPath = Join-Path $BackendPath ".env"
    if (-not (Test-Path $BackendEnvPath)) {
        Copy-Item (Join-Path $BackendPath ".env.example") $BackendEnvPath
    }
}

if (-not $SkipFrontend) {
    Push-Location $FrontendPath
    try {
        Invoke-CheckedCommand -Command "npm" -Arguments @("install")

        $FrontendEnvPath = Join-Path $FrontendPath ".env"
        if (-not (Test-Path $FrontendEnvPath)) {
            Copy-Item (Join-Path $FrontendPath ".env.example") $FrontendEnvPath
        }
    }
    finally {
        Pop-Location
    }
}

Write-Host "Local dependencies are ready."
