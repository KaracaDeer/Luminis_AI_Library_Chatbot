@echo off
REM ========================================
REM Luminis.AI Library Assistant - Project Starter
REM ========================================
REM 
REM This script starts both the backend and frontend services for the
REM Luminis.AI Library Assistant project simultaneously.
REM 
REM What it does:
REM 1. Checks if Python, Node.js, and npm are installed
REM 2. Starts the FastAPI backend server on port 5000
REM 3. Starts the React frontend development server on port 5173
REM 4. Provides a unified development environment
REM 
REM Usage: Simply double-click this file or run it from command line
REM 
REM Prerequisites:
REM - Python 3.8+ installed and in PATH
REM - Node.js 16+ installed and in PATH
REM - npm installed and in PATH
REM - All dependencies installed (run setup.py first if needed)
REM 
REM Services:
REM - Backend API: http://localhost:5000
REM - Frontend App: http://localhost:5173
REM - API Documentation: http://localhost:5000/docs
REM 
REM To stop: Press Ctrl+C in the terminal window
REM ========================================

echo ========================================
echo    Luminis AI Library Assistant
echo ========================================
echo.
echo Starting services...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    pause
    exit /b 1
)

echo Python: OK
echo Node.js: OK
echo npm: OK
echo.

REM Start the project
echo Starting Luminis AI Library Assistant...
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:5173
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start the project using npm run dev
npm run dev

pause
