@echo off
REM AI Employee System Startup Script for Windows
REM Starts all watchers with process monitoring

echo ==========================================
echo AI Employee System - Starting
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check if required directories exist
if not exist "AI_Employee_Vault" (
    echo [ERROR] AI_Employee_Vault directory not found
    exit /b 1
)

if not exist "watchers" (
    echo [ERROR] watchers directory not found
    exit /b 1
)

echo [OK] Prerequisites checked
echo.

REM Start process manager
echo Starting AI Employee Process Manager...
echo This will start and monitor:
echo   - Gmail Watcher
echo   - LinkedIn Watcher
echo.
echo Press Ctrl+C to stop all processes
echo.

python process_manager.py
