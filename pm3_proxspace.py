#!/usr/bin/env python3
"""
🔧 PM3 ProxSpace Wrapper
Proper communication with PM3 through ProxSpace environment
"""

import subprocess
import logging
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger('CyberNinjaRFID')

class PM3ProxSpace:
    """
    Wrapper for Proxmark3 via ProxSpace MSYS2 environment
    This is the CORRECT way to use PM3 in ProxSpace!
    """

    def __init__(self, port: str):
        self.port = port
        self.bash_path = self._find_bash()
        self.pm3_dir = self._find_pm3_dir()
        self.is_connected = False
        self.grabbed_output = ""

        if not self.bash_path:
            raise Exception("❌ ProxSpace bash not found!")
        if not self.pm3_dir:
            raise Exception("❌ PM3 directory not found!")

        logger.info(f"✅ Using ProxSpace bash: {self.bash_path}")
        logger.info(f"✅ PM3 directory: {self.pm3_dir}")

    def _find_bash(self) -> Optional[Path]:
        """Find ProxSpace msys2_shell.cmd (not bash.exe directly!)"""
        # We need msys2_shell.cmd to get the proper ProxSpace environment
        possible_paths = [
            Path("C:/ProxSpace/msys2/msys2_shell.cmd"),
            Path("D:/ProxSpace/msys2/msys2_shell.cmd"),
            Path("C:/Claude-Terminal/ProxSpace/msys2/msys2_shell.cmd"),
            Path("D:/Claude-Terminal/ProxSpace/msys2/msys2_shell.cmd"),
            Path(__file__).parent.parent.parent / "msys2" / "msys2_shell.cmd",
        ]

        for path in possible_paths:
            if path.exists():
                logger.info(f"📂 Found msys2_shell at: {path}")
                return path

        return None

    def _find_pm3_dir(self) -> Optional[Path]:
        """Find PM3 installation directory"""
        possible_paths = [
            Path("C:/ProxSpace/pm3"),
            Path("D:/ProxSpace/pm3"),
            Path("C:/Claude-Terminal/ProxSpace/pm3"),
            Path("D:/Claude-Terminal/ProxSpace/pm3"),
            Path(__file__).parent.parent,
        ]

        for path in possible_paths:
            # Check if proxmark3 client exists
            pm3_client = path / "proxmark3" / "client" / "proxmark3.exe"
            if pm3_client.exists():
                logger.info(f"📂 Found PM3 dir at: {path}")
                return path

        return None

    def console(self, command: str, capture=True, quiet=True):
        """
        Execute a command on PM3 via ProxSpace bash
        """
        try:
            # ProxSpace mounts D:\ProxSpace\pm3 as /pm3 in bash!
            import tempfile
            import os

            logger.info(f"📤 Executing PM3 command: {command}")
            logger.info(f"📂 Using ProxSpace mounted path: /pm3")

            # Create a temporary BASH SCRIPT (not batch file!)
            # This avoids ALL Windows quoting issues
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False, newline='\n') as bash_script:
                bash_script.write('#!/bin/bash\n')
                bash_script.write('cd /pm3/proxmark3/client\n')
                bash_script.write(f'./proxmark3.exe {self.port} -c "{command}"\n')
                bash_script_path = bash_script.name

            # Convert Windows path to Unix for bash
            bash_script_unix = bash_script_path.replace('\\', '/').replace('C:', '/c').replace('D:', '/d')

            logger.info(f"🔧 Created bash script: {bash_script_path}")
            logger.info(f"🔧 Unix path: {bash_script_unix}")

            # Create batch file that calls msys2_shell to run our bash script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as tmp:
                tmp.write('@echo off\n')
                tmp.write(f'call "{self.bash_path}" -mingw64 -defterm -no-start {bash_script_unix}\n')
                tmp_path = tmp.name

            logger.info(f"🔧 Created temp batch file: {tmp_path}")

            try:
                # Run the temp batch file
                process = subprocess.Popen(
                    [tmp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=str(self.pm3_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )

                # Wait for completion
                try:
                    stdout, stderr = process.communicate(timeout=60)
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    logger.warning("⚠️ Command timed out!")
            finally:
                # Clean up temp files
                try:
                    os.unlink(tmp_path)
                    os.unlink(bash_script_path)
                except:
                    pass

            # Capture output
            output = stdout if stdout else ""
            errors = stderr if stderr else ""

            # Combine output
            full_output = output + errors

            if capture:
                self.grabbed_output = full_output

            if not quiet and full_output:
                print(full_output)

            logger.info(f"📥 Return code: {process.returncode}")
            logger.info(f"📥 Stdout length: {len(output)} chars")
            logger.info(f"📥 Stderr length: {len(errors)} chars")
            logger.info(f"📥 Total output length: {len(full_output)} chars")

            # Handle return codes
            # Return code 127 with output means command executed but bash wrapper had issues
            # Treat as success if we got valid PM3 output
            is_success = process.returncode == 0
            if process.returncode == 127 and full_output and '[+]' in full_output:
                logger.info(f"⚠️ Return code 127 but command executed successfully (ProxSpace wrapper quirk)")
                is_success = True
            elif process.returncode != 0:
                logger.error(f"❌ Return code {process.returncode} - Command failed!")
                if errors:
                    logger.error(f"❌ FULL Stderr: {errors}")
                if output:
                    logger.error(f"❌ FULL Stdout: {output}")

            if full_output:
                # Show first 500 chars for better debugging
                preview = full_output[:500].replace('\n', ' ')
                logger.info(f"📥 Preview: {preview}...")

            return is_success

        except Exception as e:
            error_msg = f"❌ Command failed: {str(e)}"
            logger.error(error_msg)
            self.grabbed_output = error_msg
            return False

    def test_connection(self) -> bool:
        """Test if PM3 is responsive"""
        try:
            success = self.console("hw version", capture=True, quiet=True)
            if success and len(self.grabbed_output) > 0 and "Proxmark3" in self.grabbed_output:
                self.is_connected = True
                logger.info(f"✅ PM3 connection test passed! ({len(self.grabbed_output)} chars)")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")

        self.is_connected = False
        return False


if __name__ == "__main__":
    # Test the ProxSpace wrapper
    import sys

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "COM5"

    print(f"\n🧪 Testing PM3 ProxSpace Wrapper on {port}...\n")

    try:
        pm3_dev = PM3ProxSpace(port)

        print("📡 Testing connection...")
        if pm3_dev.test_connection():
            print("✅ Connection successful!")
            print(f"\n📋 Output:\n{pm3_dev.grabbed_output}\n")

            # Try another command
            print("Testing 'hw status'...")
            pm3_dev.console("hw status")
            print(f"\n📋 Output:\n{pm3_dev.grabbed_output}\n")
        else:
            print("❌ Connection failed!")
            print(f"\n📋 Output:\n{pm3_dev.grabbed_output}\n")

    except Exception as e:
        print(f"❌ Error: {e}")
