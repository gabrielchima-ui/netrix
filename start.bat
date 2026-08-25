@echo off
title NETRIX Server
cd /d "%~dp0"

echo.
echo  ========================================
echo   NETRIX - Enterprise Network Planning
echo  ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo  [ERROR] Python is not installed or not on PATH.
    echo  Install Python 3 from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH".
    pause
    exit /b 1
)

if not exist "venv\" (
    echo  Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo  Installing dependencies (first run may take a minute)...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo  [ERROR] pip install failed.
    pause
    exit /b 1
)

echo.
echo  Starting server...
echo  Open your browser at:  http://127.0.0.1:5000
echo  Press Ctrl+C to stop.
echo.
python run.py
pause
