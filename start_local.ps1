# AegisSurge: Unified Local Runner for Google Cloud Hackathon
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   AegisSurge: Autonomous Cyclone Impact & Resilience Forecaster" -ForegroundColor Cyan
Write-Host "   Track 05: Google Cloud Build with AI - Code for Communities" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$ROOT_DIR = $PSScriptRoot
Set-Location $ROOT_DIR

# 1. Verify Virtual Environment
$VENV_PYTHON = Join-Path $ROOT_DIR ".venv\Scripts\python.exe"
if (-not (Test-Path $VENV_PYTHON)) {
    Write-Host "[1/4] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & (Join-Path $ROOT_DIR ".venv\Scripts\pip.exe") install -r requirements.txt
} else {
    Write-Host "[1/4] Python virtual environment active." -ForegroundColor Green
}

# 2. Seed Baseline Datasets
Write-Host "[2/4] Verifying Cyclone Fani GeoJSON datasets..." -ForegroundColor Yellow
& $VENV_PYTHON (Join-Path $ROOT_DIR "data\seed_fani.py")

# 3. Start FastAPI Backend in background job
Write-Host "[3/4] Launching FastAPI Simulation Engine on http://127.0.0.1:8000..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    param($dir, $py)
    Set-Location $dir
    & $py -m uvicorn api.main:app --host 127.0.0.1 --port 8000
} -ArgumentList $ROOT_DIR, $VENV_PYTHON

Start-Sleep -Seconds 2

# 4. Start Next.js Frontend
Write-Host "[4/4] Launching Next.js WebGL Console on http://localhost:3000..." -ForegroundColor Green
Write-Host ""
Write-Host ">>> Ready! Opening http://localhost:3000 in your browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"

Set-Location (Join-Path $ROOT_DIR "frontend")
try {
    npm run dev
} finally {
    Write-Host "Stopping background FastAPI simulation server..." -ForegroundColor Yellow
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Write-Host "AegisSurge stopped cleanly." -ForegroundColor Gray
}
