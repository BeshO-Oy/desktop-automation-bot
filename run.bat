@echo off
REM Run script for Desktop Automation BotCity
REM Windows Batch file version

echo ========================================
echo Desktop Automation Bot - Starting
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    uv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check and install dependencies
echo Checking dependencies...
python -c "import botcity" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    uv sync
)

REM Run the bot
echo.
echo Starting bot...
echo.

python -m src.main

echo.
echo Bot execution completed.
pause
