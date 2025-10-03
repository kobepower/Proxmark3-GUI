@echo off
REM CyberNinjaRFID Launcher for Windows
REM Hack The Planet! 🔥💀

echo.
echo ================================================
echo    🔥 CyberNinjaRFID - Proxmark3 GUI 🔥
echo    Hack The Planet! 💀
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Install requirements if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt --quiet

REM Launch the GUI
echo 🚀 Launching CyberNinjaRFID...
python CyberNinjaRFID.py

pause
