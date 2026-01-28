# Run script for Desktop Automation BotCity
# PowerShell script to run the bot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desktop Automation Bot - Starting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    uv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    # Try to activate normally
    & .\.venv\Scripts\Activate.ps1 2>$null
    if ($LASTEXITCODE -ne 0) {
        # If that fails, use alternative method
        $env:VIRTUAL_ENV = (Resolve-Path ".venv").Path
        $env:PATH = "$(Join-Path $env:VIRTUAL_ENV 'Scripts');$env:PATH"
    }
} catch {
    # Use alternative activation method
    $env:VIRTUAL_ENV = (Resolve-Path ".venv").Path
    $env:PATH = "$(Join-Path $env:VIRTUAL_ENV 'Scripts');$env:PATH"
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import botcity" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        uv sync
    }
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    uv sync
}

# Run the bot
Write-Host ""
Write-Host "Starting bot..." -ForegroundColor Green
Write-Host ""

python -m src.main

Write-Host ""
Write-Host "Bot execution completed." -ForegroundColor Cyan
