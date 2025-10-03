#!/bin/bash
# CyberNinjaRFID Launcher for Linux/macOS
# Hack The Planet! 🔥💀

echo ""
echo "================================================"
echo "   🔥 CyberNinjaRFID - Proxmark3 GUI 🔥"
echo "   Hack The Planet! 💀"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "Please install Python 3.7+ first"
    exit 1
fi

# Install requirements if needed
echo "📦 Checking dependencies..."
pip3 install -r requirements.txt --quiet

# Launch the GUI
echo "🚀 Launching CyberNinjaRFID..."
python3 CyberNinjaRFID.py
