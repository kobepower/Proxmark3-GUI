#!/usr/bin/env python3
"""
🔄 PM3 Compatibility Layer
Ensures CyberNinjaRFID works with current and future Iceman firmware versions
"""

import re
import json
import logging
from typing import Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger('CyberNinjaRFID')

class PM3CompatibilityLayer:
    """
    Compatibility layer to handle different PM3 firmware versions
    """

    def __init__(self):
        self.firmware_version = None
        self.version_major = 0
        self.version_minor = 0
        self.version_patch = 0
        self.is_iceman = False
        self.capabilities = {}

    def detect_firmware_version(self, hw_version_output: str) -> bool:
        """
        Parse firmware version from 'hw version' output
        Returns True if version detected successfully
        """
        try:
            # Look for version patterns like "4.18341", "v4.18341-rrg-iceman", etc.
            patterns = [
                r'(?:version|fw:|firmware:)\s*v?(\d+)\.(\d+)(?:\.(\d+))?',
                r'PM3\s+(?:ICEMAN|RRG).*?(\d+)\.(\d+)(?:\.(\d+))?',
                r'Iceman.*?(\d+)\.(\d+)(?:\.(\d+))?',
            ]

            for pattern in patterns:
                match = re.search(pattern, hw_version_output, re.IGNORECASE)
                if match:
                    self.version_major = int(match.group(1))
                    self.version_minor = int(match.group(2))
                    self.version_patch = int(match.group(3)) if match.group(3) else 0
                    self.firmware_version = f"{self.version_major}.{self.version_minor}.{self.version_patch}"

                    # Check if it's Iceman fork
                    if 'iceman' in hw_version_output.lower() or 'rrg' in hw_version_output.lower():
                        self.is_iceman = True

                    logger.info(f"✅ Detected firmware: {self.firmware_version} (Iceman: {self.is_iceman})")
                    return True

            # If no version found, assume latest/unknown
            logger.warning("⚠️ Could not detect firmware version, assuming latest")
            self.firmware_version = "unknown"
            return False

        except Exception as e:
            logger.error(f"Error detecting firmware version: {e}")
            return False

    def detect_capabilities(self, hw_status_output: str, hw_version_output: str) -> Dict[str, bool]:
        """
        Detect device capabilities based on firmware version and hw status
        """
        self.capabilities = {
            'hf': True,  # High frequency support
            'lf': True,  # Low frequency support
            'flash': False,  # External flash
            'smartcard': False,  # Smartcard support
            'bluetooth': False,  # Bluetooth connectivity
            'standalone': False,  # Standalone mode
            'fpc': False,  # FPC connector
        }

        try:
            # Check for specific hardware features
            if 'flash' in hw_status_output.lower() or 'spi' in hw_status_output.lower():
                self.capabilities['flash'] = True

            if 'smartcard' in hw_status_output.lower() or 'sim' in hw_status_output.lower():
                self.capabilities['smartcard'] = True

            if 'bluetooth' in hw_status_output.lower() or 'bt' in hw_status_output.lower():
                self.capabilities['bluetooth'] = True

            if 'rdv4' in hw_version_output.lower():
                self.capabilities['flash'] = True
                self.capabilities['smartcard'] = True
                self.capabilities['fpc'] = True

            logger.info(f"📊 Detected capabilities: {self.capabilities}")

        except Exception as e:
            logger.error(f"Error detecting capabilities: {e}")

        return self.capabilities

    def get_compatible_commands(self) -> Dict[str, list]:
        """
        Returns command sets compatible with current firmware version
        """
        # Base commands that work across all versions
        base_commands = {
            'hw': [
                'hw version',
                'hw status',
                'hw tune',
                'hw help',
            ],
            'hf': [
                'hf search',
                'hf 14a reader',
                'hf 14a info',
                'hf list',
            ],
            'lf': [
                'lf search',
                'lf em 410x reader',
                'lf t55xx detect',
                'lf list',
            ],
        }

        # Enhanced commands for newer firmware (v4.0+)
        if self.version_major >= 4:
            base_commands['hf'].extend([
                'hf mf autopwn',
                'hf 14a raw',
                'hf mfu info',
            ])
            base_commands['lf'].extend([
                'lf em 410x clone',
                'lf t55xx read',
            ])

        # RDV4-specific commands
        if self.capabilities.get('flash'):
            base_commands['hw'].extend([
                'mem info',
                'mem load',
                'mem dump',
            ])

        # Smartcard commands
        if self.capabilities.get('smartcard'):
            base_commands['smartcard'] = [
                'smart reader',
                'smart info',
                'smart raw',
            ]

        # Bluetooth commands
        if self.capabilities.get('bluetooth'):
            base_commands['bluetooth'] = [
                'bt status',
                'bt connect',
            ]

        return base_commands

    def normalize_command(self, command: str) -> str:
        """
        Normalize command to work across firmware versions
        Handles command syntax changes between versions
        """
        command = command.strip()

        # Command translations for different versions
        translations = {
            # Old syntax -> New syntax mappings
            'hf 14a read': 'hf 14a reader',
            'hf mf nested': 'hf mf autopwn',  # Simplified for newer versions
            'lf em4x read': 'lf em 410x reader',
        }

        # Check if we need to translate
        for old_cmd, new_cmd in translations.items():
            if command.startswith(old_cmd):
                logger.info(f"🔄 Translating command: '{old_cmd}' -> '{new_cmd}'")
                return command.replace(old_cmd, new_cmd, 1)

        return command

    def check_command_compatibility(self, command: str) -> Tuple[bool, str]:
        """
        Check if command is compatible with current firmware
        Returns (is_compatible, message)
        """
        command = command.strip().lower()

        # Always allow basic commands
        basic_prefixes = ['hw', 'help', 'quit', 'exit', 'prefs', 'data']
        if any(command.startswith(prefix) for prefix in basic_prefixes):
            return True, "✅ Command supported"

        # Check HF commands
        if command.startswith('hf'):
            if not self.capabilities.get('hf', True):
                return False, "❌ HF not supported on this device"

        # Check LF commands
        if command.startswith('lf'):
            if not self.capabilities.get('lf', True):
                return False, "❌ LF not supported on this device"

        # Check smartcard commands
        if command.startswith('smart'):
            if not self.capabilities.get('smartcard'):
                return False, "❌ Smartcard reader not available on this device"

        # Check memory/flash commands
        if command.startswith('mem') or command.startswith('flash'):
            if not self.capabilities.get('flash'):
                return False, "⚠️ External flash not available on this device"

        # Check bluetooth commands
        if command.startswith('bt') or command.startswith('bluetooth'):
            if not self.capabilities.get('bluetooth'):
                return False, "❌ Bluetooth not available on this device"

        return True, "✅ Command should work"

    def get_version_info(self) -> Dict[str, any]:
        """Get current version information"""
        return {
            'version': self.firmware_version,
            'major': self.version_major,
            'minor': self.version_minor,
            'patch': self.version_patch,
            'is_iceman': self.is_iceman,
            'capabilities': self.capabilities,
        }

    def save_capabilities(self, filepath: Path):
        """Save detected capabilities to file"""
        try:
            data = {
                'firmware_version': self.firmware_version,
                'is_iceman': self.is_iceman,
                'capabilities': self.capabilities,
                'detected_at': str(Path.ctime(filepath)) if filepath.exists() else 'never',
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"💾 Saved capabilities to {filepath}")
        except Exception as e:
            logger.error(f"Error saving capabilities: {e}")

    def load_capabilities(self, filepath: Path) -> bool:
        """Load previously detected capabilities"""
        try:
            if not filepath.exists():
                return False

            with open(filepath, 'r') as f:
                data = json.load(f)

            self.firmware_version = data.get('firmware_version', 'unknown')
            self.is_iceman = data.get('is_iceman', False)
            self.capabilities = data.get('capabilities', {})

            # Parse version numbers
            if self.firmware_version != 'unknown':
                parts = self.firmware_version.split('.')
                self.version_major = int(parts[0]) if len(parts) > 0 else 0
                self.version_minor = int(parts[1]) if len(parts) > 1 else 0
                self.version_patch = int(parts[2]) if len(parts) > 2 else 0

            logger.info(f"📂 Loaded capabilities from {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error loading capabilities: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Test the compatibility layer
    compat = PM3CompatibilityLayer()

    # Simulate hw version output
    test_output = """
    Proxmark3 RFID instrument
    bootrom: /-suspect 2024-09-27 12:53:53
    os: /-suspect 2024-09-27 12:53:53
    compiled with GCC 12.2.0

    #db# Prox/RFID mark3 RFID instrument
    #db# FW Version: Iceman/master/v4.18341-212-g03b41f29a-suspect
    #db# Client: RRG/Iceman
    """

    compat.detect_firmware_version(test_output)
    print(f"Detected version: {compat.get_version_info()}")

    # Test command compatibility
    test_commands = [
        'hw version',
        'hf search',
        'smart reader',
        'bt status',
    ]

    for cmd in test_commands:
        compatible, msg = compat.check_command_compatibility(cmd)
        print(f"{cmd}: {msg}")
