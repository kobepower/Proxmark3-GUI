@echo off
REM 🚀 CyberNinjaRFID Launcher
REM This batch file launches the GUI on Windows where ProxSpace is installed

echo.
echo ====================================
echo  🔧 CyberNinjaRFID Launcher
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.x
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  PyQt5 not found. Installing...
    pip install PyQt5 pyserial
)

echo.
echo 🚀 Launching CyberNinjaRFID GUI...
echo.

REM Launch the GUI
python "%~dp0CyberNinjaRFID.py"

if errorlevel 1 (
    echo.
    echo ❌ GUI crashed or exited with error
    pause
)
