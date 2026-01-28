# Run script that works even with restricted execution policy
# Uses Python directly from venv without activating

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desktop Automation Bot - Starting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$venvPython = ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor White
    Write-Host "  $venvPython -m pip install -r requirements.txt" -ForegroundColor White
    exit 1
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    & $venvPython -c "import botcity" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        & $venvPython -m pip install --upgrade pip
        & $venvPython -m pip install -r requirements.txt
    }
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r requirements.txt
}

# Run the bot
Write-Host ""
Write-Host "Starting bot..." -ForegroundColor Green
Write-Host ""

& $venvPython -m src.main

Write-Host ""
Write-Host "Bot execution completed." -ForegroundColor Cyan
