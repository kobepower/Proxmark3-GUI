#!/usr/bin/env python3
"""
Quick test to see if PM3 client works directly
"""

import subprocess
from pathlib import Path

pm3_path = Path("D:/Claude-Terminal/ProxSpace/pm3/proxmark3/client/proxmark3.exe")
port = "COM5"

print(f"Testing PM3 client directly...")
print(f"Path: {pm3_path}")
print(f"Port: {port}")
print(f"Exists: {pm3_path.exists()}")
print()

# Test 1: Just version
print("=" * 60)
print("TEST 1: Running with -c 'hw version'")
print("=" * 60)

cmd = [str(pm3_path), "-p", port, "-c", "hw version"]
print(f"Command: {' '.join(cmd)}")
print()

try:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )

    print(f"Return code: {result.returncode}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"Stderr length: {len(result.stderr)}")
    print()

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
        print()

    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        print()

except Exception as e:
    print(f"ERROR: {e}")

print()
print("=" * 60)
print("If you see output above, PM3 is working!")
print("If not, there's an issue with the PM3 client or port.")
print("=" * 60)
