@echo off
REM Batch file to activate virtual environment (works without PowerShell execution policy)

cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo ERROR: Virtual environment not found
    echo Please run: python -m venv .venv
    pause
)
