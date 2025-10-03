#!/usr/bin/env python3
"""
Test bash execution directly to see error messages
"""

import subprocess
from pathlib import Path

# Find bash
bash_path = Path("D:/ProxSpace/msys2/usr/bin/bash.exe")
if not bash_path.exists():
    bash_path = Path("C:/ProxSpace/msys2/usr/bin/bash.exe")

print(f"🔍 Testing bash at: {bash_path}")
print(f"   Exists: {bash_path.exists()}")
print()

# Find PM3
pm3_exe = Path("D:/ProxSpace/pm3/proxmark3/client/proxmark3.exe")
if not pm3_exe.exists():
    pm3_exe = Path("C:/ProxSpace/pm3/proxmark3/client/proxmark3.exe")

print(f"🔍 PM3 executable: {pm3_exe}")
print(f"   Exists: {pm3_exe.exists()}")
print()

# Convert to Unix path
drive = str(pm3_exe)[0].lower()
path_without_drive = str(pm3_exe)[2:].replace('\\', '/')
unix_path = f'/{drive}{path_without_drive}'

print(f"🔄 Converted to Unix path: {unix_path}")
print()

# Test commands
test_commands = [
    f'{unix_path} COM5 -c "hw version"',
    f'"{unix_path}" COM5 -c "hw version"',
    str(pm3_exe).replace('\\', '/') + ' COM5 -c "hw version"',
]

for i, cmd in enumerate(test_commands, 1):
    print("=" * 70)
    print(f"TEST {i}: {cmd}")
    print("=" * 70)

    try:
        result = subprocess.run(
            [str(bash_path), "-c", cmd],
            capture_output=True,
            text=True,
            timeout=10
        )

        print(f"Return code: {result.returncode}")
        print(f"Stdout length: {len(result.stdout)}")
        print(f"Stderr length: {len(result.stderr)}")

        if result.stdout:
            print(f"\nSTDOUT:\n{result.stdout[:500]}")

        if result.stderr:
            print(f"\nSTDERR:\n{result.stderr[:500]}")

        if result.returncode == 0:
            print("\n✅ SUCCESS!")
            break
        else:
            print(f"\n❌ FAILED with code {result.returncode}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    print()

print("\n" + "=" * 70)
print("Done!")
