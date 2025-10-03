#!/usr/bin/env python3
"""
🔍 CyberNinjaRFID Setup Checker
Verifies all dependencies and requirements
"""

import sys
import os
from pathlib import Path

print("="*60)
print("🔍 CyberNinjaRFID Setup Checker")
print("="*60)
print()

# Check Python version
print("📌 Python Version Check:")
print(f"   Version: {sys.version}")
if sys.version_info < (3, 7):
    print("   ❌ ERROR: Python 3.7+ required!")
    sys.exit(1)
else:
    print("   ✅ Python version OK")
print()

# Check dependencies
print("📦 Dependency Check:")

dependencies_ok = True

# Check PyQt5
try:
    import PyQt5
    from PyQt5.QtCore import PYQT_VERSION_STR
    print(f"   ✅ PyQt5 installed (version {PYQT_VERSION_STR})")
except ImportError:
    print("   ❌ PyQt5 NOT installed")
    print("      Install with: pip install PyQt5")
    dependencies_ok = False

# Check pyserial
try:
    import serial
    print(f"   ✅ pyserial installed (version {serial.VERSION})")
except ImportError:
    print("   ❌ pyserial NOT installed")
    print("      Install with: pip install pyserial")
    dependencies_ok = False

print()

# Check PM3 module (optional)
print("🔌 PM3 Module Check (optional):")
try:
    pm3_path = Path(__file__).parent.parent / "proxmark3" / "client" / "pyscripts"
    if pm3_path.exists():
        sys.path.insert(0, str(pm3_path))
        import pm3
        print(f"   ✅ PM3 module found at {pm3_path}")
    else:
        print(f"   ⚠️  PM3 pyscripts directory not found")
        print(f"      Expected at: {pm3_path}")
        print("      GUI will work but PM3 connection will fail")
except ImportError as e:
    print(f"   ⚠️  PM3 module not importable: {e}")
    print("      Make sure Proxmark3 client is compiled with Python support")

print()

# Check configuration files
print("📄 Configuration Files:")
config_files = [
    "CyberNinjaRFID.py",
    "requirements.txt",
    "config.json",
    "README_CyberNinjaRFID.md"
]

for file in config_files:
    filepath = Path(__file__).parent / file
    if filepath.exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} NOT FOUND")

print()

# Summary
print("="*60)
if dependencies_ok:
    print("✅ All dependencies installed!")
    print("🚀 Ready to run: python3 CyberNinjaRFID.py")
else:
    print("❌ Missing dependencies!")
    print("📦 Install with: pip install -r requirements.txt")
print("="*60)
