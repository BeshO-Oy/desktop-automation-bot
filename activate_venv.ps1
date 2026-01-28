# Alternative activation script that bypasses execution policy
# This script activates the virtual environment by modifying PATH

$venvPath = Join-Path $PSScriptRoot ".venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"

if (Test-Path $pythonPath) {
    $env:VIRTUAL_ENV = $venvPath
    $env:PATH = "$(Join-Path $venvPath 'Scripts');$env:PATH"
    Write-Host "Virtual environment activated!" -ForegroundColor Green
    Write-Host "Python: $pythonPath" -ForegroundColor Cyan
} else {
    Write-Host "ERROR: Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
}
