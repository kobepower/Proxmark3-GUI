#!/usr/bin/env python3
"""
🔧 PM3 Subprocess Wrapper
Fallback communication method using subprocess when SWIG module unavailable
"""

import subprocess
import logging
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger('CyberNinjaRFID')

class PM3Subprocess:
    """
    Wrapper for Proxmark3 client using subprocess
    Fallback when SWIG Python bindings aren't available
    """

    def __init__(self, port: str):
        self.port = port
        self.pm3_client = self._find_pm3_client()
        self.is_connected = False
        self.grabbed_output = ""

        if not self.pm3_client:
            raise Exception("❌ PM3 client executable not found!")

    def _find_pm3_client(self) -> Optional[Path]:
        """Find the PM3 client executable and ProxSpace shell"""
        # For ProxSpace, we need to find pm3 wrapper script, not proxmark3.exe
        gui_folder = Path(__file__).parent

        # ProxSpace uses 'pm3' bash script that sets up the environment
        possible_pm3_scripts = [
            # ProxSpace pm3 script (this is what we need!)
            gui_folder.parent.parent / "pm3",
            Path("C:/ProxSpace/pm3/pm3"),
            Path("D:/ProxSpace/pm3/pm3"),
            Path("C:/Claude-Terminal/ProxSpace/pm3/pm3"),
            Path("D:/Claude-Terminal/ProxSpace/pm3/pm3"),
        ]

        for path in possible_pm3_scripts:
            if path.exists():
                logger.info(f"📂 Found PM3 wrapper script at: {path}")
                return path

        # Fallback to direct executable (for non-ProxSpace setups)
        possible_paths = [
            gui_folder.parent / "proxmark3" / "client" / "proxmark3.exe",
            gui_folder.parent / "proxmark3" / "client" / "proxmark3",
            Path("C:/ProxSpace/pm3/proxmark3/client/proxmark3.exe"),
            Path("D:/ProxSpace/pm3/proxmark3/client/proxmark3.exe"),
            Path("/usr/local/bin/proxmark3"),
            Path("/usr/bin/proxmark3"),
        ]

        for path in possible_paths:
            logger.debug(f"Checking: {path}")
            if path.exists():
                logger.info(f"📂 Found PM3 client at: {path}")
                return path

        # Log all attempted paths
        logger.warning("⚠️ PM3 client not found in any of these locations:")
        for path in possible_pm3_scripts[:3]:
            logger.warning(f"   ❌ {path}")

        return None

    def console(self, command: str, capture=True, quiet=True):
        """
        Execute a command on PM3 via subprocess
        """
        try:
            # Check if using ProxSpace pm3 wrapper or direct executable
            if self.pm3_client.name == "pm3":
                # ProxSpace wrapper - needs bash
                # The pm3 script is a bash script that sets up environment
                bash_path = self.pm3_client.parent.parent / "msys2" / "usr" / "bin" / "bash.exe"

                if not bash_path.exists():
                    # Try common ProxSpace locations
                    for base in [Path("C:/ProxSpace"), Path("D:/ProxSpace"), Path("C:/Claude-Terminal/ProxSpace"), Path("D:/Claude-Terminal/ProxSpace")]:
                        test_bash = base / "msys2" / "usr" / "bin" / "bash.exe"
                        if test_bash.exists():
                            bash_path = test_bash
                            break

                logger.info(f"🔄 Using ProxSpace environment via bash")
                # Run: bash -c "cd /path/to/pm3 && ./pm3 -p PORT -c 'command'"
                pm3_dir = self.pm3_client.parent
                cmd_args = [
                    str(bash_path),
                    "-c",
                    f'cd "{pm3_dir}" && ./proxmark3/client/proxmark3 -p {self.port} -c "{command}"'
                ]
            else:
                # Direct executable
                cmd_args = [
                    str(self.pm3_client),
                    "-p", self.port,
                    "-c", command
                ]

            logger.info(f"📤 Running: {' '.join(cmd_args)}")

            # Execute command directly
            process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=60)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                logger.warning("⚠️ Command timed out!")

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

            if full_output:
                # Show first 200 chars of output
                preview = full_output[:200].replace('\n', ' ')
                logger.info(f"📥 Output preview: {preview}...")

            return process.returncode == 0

        except subprocess.TimeoutExpired:
            error_msg = f"❌ Command timeout: {command}"
            logger.error(error_msg)
            self.grabbed_output = error_msg
            return False
        except Exception as e:
            error_msg = f"❌ Command failed: {str(e)}"
            logger.error(error_msg)
            self.grabbed_output = error_msg
            return False

    def test_connection(self) -> bool:
        """Test if PM3 is responsive"""
        try:
            success = self.console("hw version", capture=True, quiet=True)
            if success and "Proxmark3" in self.grabbed_output:
                self.is_connected = True
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")

        self.is_connected = False
        return False


# Factory function to create PM3 connection
def create_pm3_connection(port: str):
    """
    Create PM3 connection using best available method
    """
    # Try SWIG bindings first
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "proxmark3" / "client" / "pyscripts"))
        import pm3

        logger.info("✅ Using PM3 SWIG Python bindings")
        return pm3.pm3(port)
    except ImportError as e:
        logger.warning(f"⚠️ SWIG bindings not available: {e}")
        logger.info("🔄 Falling back to subprocess method...")
        return PM3Subprocess(port)


if __name__ == "__main__":
    # Test the subprocess wrapper
    import sys

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "COM3"  # Default for testing

    print(f"\n🧪 Testing PM3 Subprocess Wrapper on {port}...\n")

    try:
        pm3_dev = PM3Subprocess(port)

        print("📡 Testing connection...")
        if pm3_dev.test_connection():
            print("✅ Connection successful!")
            print(f"\n📋 Output:\n{pm3_dev.grabbed_output}\n")
        else:
            print("❌ Connection failed!")
            print(f"\n📋 Output:\n{pm3_dev.grabbed_output}\n")

    except Exception as e:
        print(f"❌ Error: {e}")
