#!/usr/bin/env python3
"""
🔥 CyberNinjaRFID - Proxmark3 Iceman GUI 🔥
A cyberpunk-themed GUI for Proxmark3 Iceman firmware
Inspired by CyberNinja Trader theme
"""

import sys
import os
import json
import time
import logging
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from collections import deque
from dataclasses import dataclass

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QTabWidget, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QCheckBox,
    QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox, QSplitter,
    QStatusBar, QMenuBar, QMenu, QAction, QSystemTrayIcon, QGridLayout,
    QInputDialog, QScrollArea
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QDateTime, QProcess, QSize
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QTextCursor

# Try to import pm3 module (SWIG bindings)
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "proxmark3" / "client" / "pyscripts"))
    import pm3
    PM3_AVAILABLE = True
    print("✅ PM3 SWIG bindings loaded")
except ImportError as e:
    print(f"⚠️ PM3 SWIG module not available: {e}")
    print("🔄 Will use subprocess fallback method")
    PM3_AVAILABLE = False

# Import subprocess fallback
try:
    from pm3_subprocess import create_pm3_connection, PM3Subprocess
    PM3_SUBPROCESS_AVAILABLE = True
except ImportError:
    PM3_SUBPROCESS_AVAILABLE = False
    print("⚠️ PM3 subprocess fallback not available")

# Import ProxSpace wrapper (BEST option for ProxSpace users!)
try:
    from pm3_proxspace import PM3ProxSpace
    PM3_PROXSPACE_AVAILABLE = True
    print("✅ PM3 ProxSpace wrapper loaded")
except ImportError:
    PM3_PROXSPACE_AVAILABLE = False
    print("⚠️ PM3 ProxSpace wrapper not available")

# Import compatibility layer
try:
    from pm3_compatibility import PM3CompatibilityLayer
    COMPAT_AVAILABLE = True
except ImportError:
    COMPAT_AVAILABLE = False
    print("⚠️ Compatibility layer not available")

# Import command parser
try:
    from pm3_command_parser import PM3CommandParser
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False
    print("⚠️ Command parser not available")

# ==================== CONSTANTS ====================
APP_NAME = "🔥 CyberNinjaRFID"
VERSION = "v1.0.0"
LOG_HISTORY_LIMIT = 500
MAX_OUTPUT_LINES = 1000

# ==================== LOGGING SETUP ====================
def setup_logging():
    """Configure application logging"""
    logger = logging.getLogger('CyberNinjaRFID')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(logs_dir / "cyberninja_rfid.log", encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()

# ==================== PM3 CONNECTION THREAD ====================
class PM3ConnectionThread(QThread):
    """Thread for managing PM3 connection"""
    connected = pyqtSignal(str)  # device_name
    disconnected = pyqtSignal()
    error = pyqtSignal(str)
    output = pyqtSignal(str)
    firmware_detected = pyqtSignal(dict)  # firmware info

    def __init__(self, port: str):
        super().__init__()
        self.port = port
        self.pm3_device = None
        self.is_connected = False
        self.command_queue = deque()
        self.compat_layer = PM3CompatibilityLayer() if COMPAT_AVAILABLE else None
        self.command_parser = PM3CommandParser() if PARSER_AVAILABLE else None

    def run(self):
        """Connect to PM3 device"""
        try:
            logger.info(f"🔌 Connecting to PM3 on {self.port}...")

            # Priority order: ProxSpace > SWIG > Subprocess
            if PM3_PROXSPACE_AVAILABLE:
                logger.info("🔄 Using ProxSpace environment wrapper (BEST)")
                self.pm3_device = PM3ProxSpace(self.port)
            elif PM3_AVAILABLE:
                logger.info("✅ Using SWIG Python bindings")
                self.pm3_device = pm3.pm3(self.port)
            elif PM3_SUBPROCESS_AVAILABLE:
                logger.info("🔄 Using subprocess fallback method")
                self.pm3_device = create_pm3_connection(self.port)
            else:
                self.error.emit("❌ No PM3 communication method available!\nPlease compile PM3 with Python support or check proxmark3.exe path.")
                return

            # Test connection and detect firmware
            self.pm3_device.console("hw version", capture=True, quiet=True)
            device_info = self.pm3_device.grabbed_output

            # Extract device name
            device_name = "Proxmark3"
            for line in device_info.split('\n'):
                if "Proxmark3" in line:
                    device_name = line.strip()
                    break

            # Detect firmware version and capabilities
            if self.compat_layer:
                self.compat_layer.detect_firmware_version(device_info)

                # Get hardware status for capabilities
                self.pm3_device.console("hw status", capture=True, quiet=True)
                hw_status = self.pm3_device.grabbed_output
                self.compat_layer.detect_capabilities(hw_status, device_info)

                # Emit firmware info
                fw_info = self.compat_layer.get_version_info()
                self.firmware_detected.emit(fw_info)
                logger.info(f"🔄 Firmware: {fw_info['version']} (Iceman: {fw_info['is_iceman']})")

                # Save capabilities for future use
                caps_file = Path(__file__).parent / "logs" / "pm3_capabilities.json"
                self.compat_layer.save_capabilities(caps_file)

            # Discover available commands dynamically
            if self.command_parser:
                self.command_parser.pm3_device = self.pm3_device

                # Try to load from cache first
                cache_file = Path(__file__).parent / "logs" / "pm3_commands_cache.json"
                if not self.command_parser.load_commands_cache(cache_file):
                    # Cache miss, discover commands
                    logger.info("🔍 Discovering commands from PM3...")
                    self.command_parser.discover_all_commands()
                    self.command_parser.save_commands_cache(cache_file)

            self.is_connected = True
            self.connected.emit(device_name)
            logger.info(f"✅ Connected to {device_name}")

        except Exception as e:
            error_msg = f"❌ Connection failed: {str(e)}"
            logger.error(error_msg)
            self.error.emit(error_msg)

    def execute_command(self, command: str, capture=True, quiet=True):
        """Execute command on PM3 with compatibility checks"""
        try:
            if not self.pm3_device:
                self.error.emit("❌ Not connected to PM3!")
                return

            # Special handling for tune commands (with -n flag they're safe but we add a note)
            if "tune" in command.lower() and "-n" not in command.lower():
                self.output.emit(f"⚠️ Warning: Tune command without -n flag may open popup window\n")

            # Normalize command for compatibility
            if self.compat_layer:
                command = self.compat_layer.normalize_command(command)

                # Check command compatibility
                is_compat, msg = self.compat_layer.check_command_compatibility(command)
                if not is_compat:
                    self.output.emit(f"{msg}\n")
                    logger.warning(f"⚠️ {msg} for command: {command}")

            logger.info(f"📤 Executing: {command}")
            self.pm3_device.console(command, capture=capture, quiet=quiet)

            if capture:
                output = self.pm3_device.grabbed_output
                self.output.emit(output)

                # Check antenna health for tune commands
                if "tune" in command.lower() and "-n" in command.lower():
                    import re
                    # Look for voltage readings in mV
                    voltages = re.findall(r'(\d+)\s*mV', output)
                    if voltages:
                        max_voltage = max([int(v) for v in voltages])
                        if max_voltage > 20000:  # Good reading above 20V
                            self.output.emit(f"\n✅ Antenna is OK! ({max_voltage} mV) 📡\n")
                        elif max_voltage > 10000:  # Moderate reading
                            self.output.emit(f"\n⚠️ Antenna reading moderate ({max_voltage} mV)\n")
                        else:  # Low reading
                            self.output.emit(f"\n❌ Antenna reading low ({max_voltage} mV)\n")

                logger.info(f"📥 Output received ({len(output)} chars)")
            else:
                self.output.emit(f"✅ Command executed: {command}")

        except Exception as e:
            error_msg = f"❌ Command failed: {str(e)}"
            logger.error(error_msg)
            self.error.emit(error_msg)

    def disconnect(self):
        """Disconnect from PM3"""
        try:
            if self.pm3_device:
                self.pm3_device = None
                self.is_connected = False
                self.disconnected.emit()
                logger.info("🔌 Disconnected from PM3")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")

# ==================== DEVICE SCANNER ====================
class DeviceScanner(QThread):
    """Thread for scanning available serial ports"""
    devices_found = pyqtSignal(list)

    def run(self):
        """Scan for available serial devices"""
        try:
            import serial.tools.list_ports
            ports = []

            # Get ALL serial ports
            all_ports = list(serial.tools.list_ports.comports())

            logger.info(f"🔍 Scanning {len(all_ports)} serial ports...")

            for port in all_ports:
                # Show ALL ports (user can decide which is PM3)
                # Common patterns: USB Serial, CH340, FTDI, CDC, etc.
                ports.append({
                    'device': port.device,
                    'description': port.description if port.description else 'Serial Port',
                    'hwid': port.hwid
                })
                logger.info(f"   Found: {port.device} - {port.description}")

            self.devices_found.emit(ports)
            logger.info(f"✅ Found {len(ports)} serial port(s)")

        except Exception as e:
            logger.error(f"Device scan error: {e}")
            self.devices_found.emit([])

# ==================== MAIN WINDOW ====================
class CyberNinjaRFIDWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.pm3_thread = None
        self.command_history = []
        self.history_index = -1

        self.init_ui()
        self.apply_cyber_theme()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{APP_NAME} - Proxmark3 Iceman GUI {VERSION}")
        self.setGeometry(100, 100, 1400, 900)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ===== TOP BAR: Connection Controls =====
        connection_group = QGroupBox("🔌 Device Connection")
        connection_layout = QHBoxLayout()

        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(200)
        self.port_combo.setPlaceholderText("Select COM/Device Port...")
        connection_layout.addWidget(QLabel("📡 Port:"))
        connection_layout.addWidget(self.port_combo)

        self.scan_button = QPushButton("🔍 Scan Devices")
        self.scan_button.clicked.connect(self.scan_devices)
        connection_layout.addWidget(self.scan_button)

        self.connect_button = QPushButton("🔌 Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        connection_layout.addWidget(self.connect_button)

        self.status_label = QLabel("⚪ Disconnected")
        self.status_label.setStyleSheet("font-weight: bold; color: #888;")
        connection_layout.addWidget(self.status_label)

        connection_layout.addStretch()
        connection_group.setLayout(connection_layout)
        main_layout.addWidget(connection_group)

        # ===== TAB WIDGET =====
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Tab 1: Command Console
        self.console_tab = self.create_console_tab()
        self.tabs.addTab(self.console_tab, "💻 Command Console")

        # Tab 2: LF Tools (most common)
        self.lf_tab = self.create_lf_tools_tab()
        self.tabs.addTab(self.lf_tab, "📻 LF Tools")

        # Tab 3: HF Tools
        self.hf_tab = self.create_hf_tools_tab()
        self.tabs.addTab(self.hf_tab, "📡 HF Tools")

        # Tab 4: Scripts
        self.scripts_tab = self.create_scripts_tab()
        self.tabs.addTab(self.scripts_tab, "🔧 Scripts")

        # Tab 5: Device Info
        self.device_tab = self.create_device_info_tab()
        self.tabs.addTab(self.device_tab, "📊 Device Info")

        # Tab 6: Help
        self.help_tab = self.create_help_tab()
        self.tabs.addTab(self.help_tab, "❓ Help")

        # ===== STATUS BAR =====
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🚀 CyberNinjaRFID Ready - Hack The Planet! 💀")

        # Auto-scan on startup
        QTimer.singleShot(500, self.scan_devices)

    def create_console_tab(self):
        """Create command console tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Output area
        output_group = QGroupBox("📟 Output Console")
        output_layout = QVBoxLayout()

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        output_layout.addWidget(self.output_text)

        # Clear button
        clear_btn = QPushButton("🗑️ Clear Output")
        clear_btn.clicked.connect(lambda: self.output_text.clear())
        output_layout.addWidget(clear_btn)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Command input
        cmd_group = QGroupBox("⌨️ Command Input")
        cmd_layout = QVBoxLayout()

        cmd_input_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter PM3 command... (e.g., 'hw version', 'lf search', 'hf search')")
        self.command_input.returnPressed.connect(self.execute_command)
        cmd_input_layout.addWidget(self.command_input)

        self.execute_button = QPushButton("▶️ Execute")
        self.execute_button.clicked.connect(self.execute_command)
        cmd_input_layout.addWidget(self.execute_button)

        cmd_layout.addLayout(cmd_input_layout)

        # Quick commands
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("⚡ Quick Commands:"))

        quick_cmds = [
            ("📊 HW Version", "hw version"),
            ("📡 HW Status", "hw status"),
            ("🔍 LF Search", "lf search"),
            ("🔎 HF Search", "hf search"),
            ("📈 HW Tune", "hw tune -n 1"),  # -n flag disables graph popup
        ]

        for label, cmd in quick_cmds:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            quick_layout.addWidget(btn)

        cmd_layout.addLayout(quick_layout)
        cmd_group.setLayout(cmd_layout)
        layout.addWidget(cmd_group)

        return widget

    def create_device_info_tab(self):
        """Create device information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info_group = QGroupBox("📊 Device Information")
        info_layout = QGridLayout()

        self.device_name_label = QLabel("N/A")
        self.device_fw_label = QLabel("N/A")
        self.device_hw_label = QLabel("N/A")
        self.device_serial_label = QLabel("N/A")

        info_layout.addWidget(QLabel("🔹 Device:"), 0, 0)
        info_layout.addWidget(self.device_name_label, 0, 1)
        info_layout.addWidget(QLabel("🔹 Firmware:"), 1, 0)
        info_layout.addWidget(self.device_fw_label, 1, 1)
        info_layout.addWidget(QLabel("🔹 Hardware:"), 2, 0)
        info_layout.addWidget(self.device_hw_label, 2, 1)
        info_layout.addWidget(QLabel("🔹 Serial:"), 3, 0)
        info_layout.addWidget(self.device_serial_label, 3, 1)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        refresh_btn = QPushButton("🔄 Refresh Device Info")
        refresh_btn.clicked.connect(self.refresh_device_info)
        layout.addWidget(refresh_btn)

        layout.addStretch()
        return widget

    def create_hf_tools_tab(self):
        """Create HF tools tab with organized layout and output console"""
        widget = QWidget()
        main_layout = QHBoxLayout(widget)  # Horizontal split

        # Left side - Tools
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Scanning group
        scan_group = QGroupBox("📡 Tag Scanning")
        scan_layout = QGridLayout()
        scan_tools = [
            ("🔍 HF Search", "hf search"),
            ("📊 HF Tune", "hf tune -n 1"),  # -n flag disables graph popup
            ("🎯 HF Sniff", "hf sniff"),
        ]
        for i, (label, cmd) in enumerate(scan_tools):
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            scan_layout.addWidget(btn, i // 2, i % 2)
        scan_group.setLayout(scan_layout)
        left_layout.addWidget(scan_group)

        # Readers group
        reader_group = QGroupBox("📇 Tag Readers")
        reader_layout = QGridLayout()
        reader_tools = [
            ("💳 ISO14443-A Reader", "hf 14a reader"),
            ("🎴 ISO14443-A Info", "hf 14a info"),
            ("🔎 iClass Reader", "hf iclass reader"),
            ("💎 Legic Reader", "hf legic reader"),
        ]
        for i, (label, cmd) in enumerate(reader_tools):
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            reader_layout.addWidget(btn, i // 2, i % 2)
        reader_group.setLayout(reader_layout)
        left_layout.addWidget(reader_group)

        # MIFARE group
        mifare_group = QGroupBox("🔐 MIFARE Tools")
        mifare_layout = QGridLayout()
        mifare_tools = [
            ("🤖 MIFARE Autopwn", "hf mf autopwn"),
            ("🗝️ Check Keys", "hf mf chk"),
            ("📖 Dump Card", "hf mf dump"),
            ("🔓 Nested Attack", "hf mf nested"),
        ]
        for i, (label, cmd) in enumerate(mifare_tools):
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            mifare_layout.addWidget(btn, i // 2, i % 2)
        mifare_group.setLayout(mifare_layout)
        left_layout.addWidget(mifare_group)

        # List group
        list_group = QGroupBox("📝 Trace Analysis")
        list_layout = QVBoxLayout()
        list_btn = QPushButton("📝 HF List (ISO14443a)")
        list_btn.setMinimumHeight(40)
        list_btn.clicked.connect(lambda: self.quick_command("hf list 14a"))
        list_layout.addWidget(list_btn)
        list_group.setLayout(list_layout)
        left_layout.addWidget(list_group)

        left_layout.addStretch()
        main_layout.addWidget(left_widget, 1)

        # Right side - Output console with command input
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Command input for HF tab
        cmd_group = QGroupBox("⌨️ HF Command Input")
        cmd_layout = QHBoxLayout()

        self.hf_command_input = QLineEdit()
        self.hf_command_input.setPlaceholderText("Enter HF command here...")
        self.hf_command_input.returnPressed.connect(lambda: self.quick_command(self.hf_command_input.text()) or self.hf_command_input.clear())
        cmd_layout.addWidget(self.hf_command_input)

        hf_exec_btn = QPushButton("▶️ Execute")
        hf_exec_btn.clicked.connect(lambda: self.quick_command(self.hf_command_input.text()) or self.hf_command_input.clear())
        cmd_layout.addWidget(hf_exec_btn)

        cmd_group.setLayout(cmd_layout)
        right_layout.addWidget(cmd_group)

        # Output console
        output_group = QGroupBox("📟 HF Output Console")
        output_layout = QVBoxLayout()

        self.hf_output_text = QTextEdit()
        self.hf_output_text.setReadOnly(True)
        self.hf_output_text.setFont(QFont("Consolas", 9))
        output_layout.addWidget(self.hf_output_text)

        clear_hf_btn = QPushButton("🗑️ Clear HF Output")
        clear_hf_btn.clicked.connect(lambda: self.hf_output_text.clear())
        output_layout.addWidget(clear_hf_btn)

        output_group.setLayout(output_layout)
        right_layout.addWidget(output_group)

        main_layout.addWidget(right_widget, 1)

        return widget

    def create_lf_tools_tab(self):
        """Create LF tools tab with organized layout and proper Iceman commands"""
        widget = QWidget()
        main_layout = QHBoxLayout(widget)  # Horizontal split

        # Left side - Tools
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Scanning group
        scan_group = QGroupBox("📡 Tag Scanning")
        scan_layout = QGridLayout()
        scan_tools = [
            ("🔍 LF Search", "lf search"),
            ("📊 LF Tune", "lf tune -n 1"),  # -n flag disables graph popup
            ("📈 LF Sniff", "lf sniff"),
        ]
        for i, (label, cmd) in enumerate(scan_tools):
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            scan_layout.addWidget(btn, i // 2, i % 2)
        scan_group.setLayout(scan_layout)
        left_layout.addWidget(scan_group)

        # Readers group
        reader_group = QGroupBox("📇 Tag Readers")
        reader_layout = QGridLayout()
        reader_tools = [
            ("🎫 EM410x Reader", "lf em 410x reader"),
            ("🏢 HID Reader", "lf hid reader"),
            ("🎟️ Indala Reader", "lf indala reader"),
            ("🔑 T55xx Detect", "lf t55xx detect"),
            ("📖 T55xx Read Blocks", None),  # Special function
        ]
        for i, (label, cmd) in enumerate(reader_tools):
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            if cmd:
                btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            else:
                # T55xx Read Blocks - special function
                btn.clicked.connect(self.t55xx_read_blocks)
            reader_layout.addWidget(btn, i // 3, i % 3)
        reader_group.setLayout(reader_layout)
        left_layout.addWidget(reader_group)

        # Writers group
        writer_group = QGroupBox("🧾 Tag Writers")
        writer_layout = QGridLayout()

        em_write_btn = QPushButton("✍️ EM410x Write")
        em_write_btn.setMinimumHeight(40)
        em_write_btn.clicked.connect(self.em410x_write)
        writer_layout.addWidget(em_write_btn, 0, 0)

        t55_write_btn = QPushButton("✏️ T55xx Write")
        t55_write_btn.setMinimumHeight(40)
        t55_write_btn.clicked.connect(self.t55xx_write)
        writer_layout.addWidget(t55_write_btn, 0, 1)

        t55_wipe_btn = QPushButton("🔓 T55xx Wipe")
        t55_wipe_btn.setMinimumHeight(40)
        t55_wipe_btn.clicked.connect(lambda: self.quick_command("lf t55xx wipe"))
        writer_layout.addWidget(t55_wipe_btn, 1, 0)

        t55_config_btn = QPushButton("⚙️ T55xx Config Block")
        t55_config_btn.setMinimumHeight(40)
        t55_config_btn.clicked.connect(lambda: self.quick_command("lf t55xx write --blk 1 --data 000880E0"))
        writer_layout.addWidget(t55_config_btn, 1, 1)

        writer_group.setLayout(writer_layout)
        left_layout.addWidget(writer_group)

        # Clone Tools group
        clone_group = QGroupBox("📤 Clone Tools")
        clone_layout = QGridLayout()

        em_clone_btn = QPushButton("🎫 EM410x Clone")
        em_clone_btn.setMinimumHeight(40)
        em_clone_btn.clicked.connect(lambda: self.quick_command("lf em 410x clone --to t55xx"))
        clone_layout.addWidget(em_clone_btn, 0, 0)

        hid_clone_btn = QPushButton("🏢 HID Clone")
        hid_clone_btn.setMinimumHeight(40)
        hid_clone_btn.clicked.connect(self.hid_clone)
        clone_layout.addWidget(hid_clone_btn, 0, 1)

        indala_raw_btn = QPushButton("📋 Indala (Raw)")
        indala_raw_btn.setMinimumHeight(40)
        indala_raw_btn.clicked.connect(self.indala_clone_raw)
        clone_layout.addWidget(indala_raw_btn, 1, 0)

        indala_fc_btn = QPushButton("🔢 Indala (FC/CN)")
        indala_fc_btn.setMinimumHeight(40)
        indala_fc_btn.clicked.connect(self.indala_clone_fc_cn)
        clone_layout.addWidget(indala_fc_btn, 1, 1)

        indala_heden_btn = QPushButton("🔤 Indala (HEDEN)")
        indala_heden_btn.setMinimumHeight(40)
        indala_heden_btn.clicked.connect(self.indala_clone_heden)
        clone_layout.addWidget(indala_heden_btn, 2, 0)

        clone_group.setLayout(clone_layout)
        left_layout.addWidget(clone_group)

        # Dump & Restore group
        dump_group = QGroupBox("💾 Dump & Restore")
        dump_layout = QGridLayout()

        dump_btn = QPushButton("💾 T55xx Dump")
        dump_btn.setMinimumHeight(40)
        dump_btn.clicked.connect(self.t55xx_dump)
        dump_layout.addWidget(dump_btn, 0, 0)

        restore_btn = QPushButton("📥 T55xx Restore")
        restore_btn.setMinimumHeight(40)
        restore_btn.clicked.connect(self.t55xx_restore)
        dump_layout.addWidget(restore_btn, 0, 1)

        sim_btn = QPushButton("🎭 LF Simulate")
        sim_btn.setMinimumHeight(40)
        sim_btn.clicked.connect(self.lf_simulate)
        dump_layout.addWidget(sim_btn, 1, 0)

        dump_group.setLayout(dump_layout)
        left_layout.addWidget(dump_group)

        # Trace Analysis group
        list_group = QGroupBox("📝 Trace Analysis")
        list_layout = QHBoxLayout()

        list_em_btn = QPushButton("📝 List EM")
        list_em_btn.setMinimumHeight(40)
        list_em_btn.clicked.connect(lambda: self.quick_command("lf list em"))
        list_layout.addWidget(list_em_btn)

        list_hid_btn = QPushButton("📝 List HID")
        list_hid_btn.setMinimumHeight(40)
        list_hid_btn.clicked.connect(lambda: self.quick_command("lf list hid"))
        list_layout.addWidget(list_hid_btn)

        list_group.setLayout(list_layout)
        left_layout.addWidget(list_group)

        left_layout.addStretch()
        main_layout.addWidget(left_widget, 1)

        # Right side - Output console with command input
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Command input for LF tab
        cmd_group = QGroupBox("⌨️ LF Command Input")
        cmd_layout = QHBoxLayout()

        self.lf_command_input = QLineEdit()
        self.lf_command_input.setPlaceholderText("Enter LF command here...")
        self.lf_command_input.returnPressed.connect(lambda: self.quick_command(self.lf_command_input.text()) or self.lf_command_input.clear())
        cmd_layout.addWidget(self.lf_command_input)

        lf_exec_btn = QPushButton("▶️ Execute")
        lf_exec_btn.clicked.connect(lambda: self.quick_command(self.lf_command_input.text()) or self.lf_command_input.clear())
        cmd_layout.addWidget(lf_exec_btn)

        cmd_group.setLayout(cmd_layout)
        right_layout.addWidget(cmd_group)

        # Output console
        output_group = QGroupBox("📟 LF Output Console")
        output_layout = QVBoxLayout()

        self.lf_output_text = QTextEdit()
        self.lf_output_text.setReadOnly(True)
        self.lf_output_text.setFont(QFont("Consolas", 9))
        output_layout.addWidget(self.lf_output_text)

        clear_lf_btn = QPushButton("🗑️ Clear LF Output")
        clear_lf_btn.clicked.connect(lambda: self.lf_output_text.clear())
        output_layout.addWidget(clear_lf_btn)

        output_group.setLayout(output_layout)
        right_layout.addWidget(output_group)

        main_layout.addWidget(right_widget, 1)

        return widget

    def create_scripts_tab(self):
        """Create scripts management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scripts_group = QGroupBox("🔧 Available Scripts")
        scripts_layout = QVBoxLayout()

        self.scripts_list = QTextEdit()
        self.scripts_list.setReadOnly(True)
        self.scripts_list.setPlaceholderText("📁 No scripts loaded...")
        scripts_layout.addWidget(self.scripts_list)

        btn_layout = QHBoxLayout()
        load_btn = QPushButton("📂 Load Script Directory")
        load_btn.clicked.connect(self.load_scripts)
        btn_layout.addWidget(load_btn)

        run_btn = QPushButton("▶️ Run Selected Script")
        btn_layout.addWidget(run_btn)

        scripts_layout.addLayout(btn_layout)
        scripts_group.setLayout(scripts_layout)
        layout.addWidget(scripts_group)

        return widget

    def create_help_tab(self):
        """Create help/how-to tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Create scrollable text area for help content
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setFont(QFont("Consolas", 10))
        # Set background to darker color so text is visible
        help_text.setStyleSheet("QTextEdit { background-color: #0a0e27; color: #ffffff; }")

        # Add comprehensive help content
        help_content = """
<h1 style='color: #00d4ff;'>🔥 CyberNinjaRFID - How To Clone Cards</h1>

<h2 style='color: #00ffff;'>🎯 Quick Start: 3-Step Clone Process</h2>

<p><b style='color: #00ff00;'>Step 1: Identify the Card Type</b></p>
<ul>
<li>Place original card on Proxmark3 antenna</li>
<li>Click <b>🔍 LF Search</b> (most access cards) or <b>🔍 HF Search</b></li>
<li>Read output to identify card type</li>
</ul>

<p><b style='color: #00ff00;'>Step 2: Read the Card Data</b></p>
<ul>
<li><b>EM410x</b> → Click <b>🎫 EM410x Reader</b></li>
<li><b>HID Prox</b> → Click <b>🏢 HID Reader</b></li>
<li><b>Indala</b> → Click <b>🎟️ Indala Reader</b></li>
<li><b>MIFARE</b> → Click <b>💳 ISO14443-A Reader</b></li>
</ul>

<p><b style='color: #00ff00;'>Step 3: Clone to Blank Card</b></p>
<ul>
<li>Place blank T55xx card on antenna</li>
<li>Click appropriate clone button</li>
<li>Verify with <b>🔍 Search</b> again</li>
</ul>

<hr>

<h2 style='color: #00ffff;'>🎫 Cloning EM410x (Most Common)</h2>
<p><b>What it is:</b> Most common building/gym access cards</p>
<ol>
<li><b>Read:</b> Place original → Click <b>🔍 LF Search</b></li>
<li><b>Clone:</b> Place blank T55xx → Click <b>🎫 EM410x Clone</b></li>
<li><b>Verify:</b> Click <b>🔍 LF Search</b> again</li>
</ol>

<hr>

<h2 style='color: #00ffff;'>🏢 Cloning HID Prox</h2>
<p><b>What it is:</b> Corporate access cards (gray/white HID logo)</p>
<ol>
<li><b>Read:</b> Click <b>🏢 HID Reader</b> → Note FC and CN</li>
<li><b>Clone:</b> Place blank → Click <b>🏢 HID Clone</b> → Enter FC & CN</li>
<li><b>Verify:</b> Click <b>🏢 HID Reader</b></li>
</ol>

<hr>

<h2 style='color: #00ffff;'>🎟️ Cloning Indala (3 Methods)</h2>
<p><b>Try methods in order until one works:</b></p>

<p><b style='color: #ffff00;'>Method 1 - Raw (Try First):</b></p>
<ol>
<li>Click <b>🎟️ Indala Reader</b> → Copy RAW HEX</li>
<li>Place blank → Click <b>🔓 T55xx Wipe</b></li>
<li>Click <b>📋 Indala (Raw)</b> → Paste HEX</li>
<li>Click <b>⚙️ T55xx Config Block</b></li>
<li>Verify with <b>🔍 LF Search</b></li>
</ol>

<p><b style='color: #ffff00;'>Method 2 - FC/CN (If Method 1 fails):</b></p>
<ol>
<li>Click <b>🔓 T55xx Wipe</b></li>
<li>Click <b>🔢 Indala (FC/CN)</b> → Enter values</li>
<li>Click <b>⚙️ T55xx Config Block</b></li>
<li>Verify</li>
</ol>

<p><b style='color: #ffff00;'>Method 3 - HEDEN (If Method 2 fails):</b></p>
<ol>
<li>Click <b>🔓 T55xx Wipe</b></li>
<li>Click <b>🔤 Indala (HEDEN)</b> → Enter printed ID</li>
<li>Click <b>⚙️ T55xx Config Block</b></li>
<li>Verify</li>
</ol>

<hr>

<h2 style='color: #00ffff;'>💳 Cloning MIFARE Classic (HF)</h2>
<p><b>What it is:</b> Transit cards, hotel keys (white cards)</p>
<ol>
<li>Place original → Click <b>🤖 MIFARE Autopwn</b> (wait 5-30 sec)</li>
<li>Click <b>📖 Dump Card</b> to save data</li>
<li>Advanced: Write to blank MIFARE (requires hex editing)</li>
</ol>

<hr>

<h2 style='color: #00ffff;'>🛠️ Button Guide - LF Tools</h2>

<p><b style='color: #ffffff;'>📡 Tag Scanning:</b></p>
<ul>
<li><b>🔍 LF Search</b> - Auto-detect card type (START HERE)</li>
<li><b>📊 LF Tune</b> - Check antenna is working</li>
<li><b>📈 LF Sniff</b> - Record RF traffic (advanced)</li>
</ul>

<p><b style='color: #ffffff;'>📇 Tag Readers:</b></p>
<ul>
<li><b>🎫 EM410x Reader</b> - Read EM410x ID</li>
<li><b>🏢 HID Reader</b> - Read HID FC/CN</li>
<li><b>🎟️ Indala Reader</b> - Read Indala data</li>
<li><b>🔑 T55xx Detect</b> - Check blank card type</li>
<li><b>📖 T55xx Read Blocks</b> - Read all 8 blocks (0-7)</li>
</ul>

<p><b style='color: #ffffff;'>🧾 Tag Writers:</b></p>
<ul>
<li><b>✍️ EM410x Write</b> - Manual EM410x programming</li>
<li><b>✏️ T55xx Write</b> - Write specific block</li>
<li><b>🔓 T55xx Wipe</b> - Erase card (use before Indala)</li>
<li><b>⚙️ T55xx Config Block</b> - Set config (after Indala)</li>
</ul>

<p><b style='color: #ffffff;'>📤 Clone Tools:</b></p>
<ul>
<li><b>🎫 EM410x Clone</b> - Quick EM410x clone</li>
<li><b>🏢 HID Clone</b> - Clone HID with FC/CN</li>
<li><b>📋 Indala (Raw)</b> - Clone via RAW hex</li>
<li><b>🔢 Indala (FC/CN)</b> - Clone via FC/CN</li>
<li><b>🔤 Indala (HEDEN)</b> - Clone via printed ID</li>
</ul>

<p><b style='color: #ffffff;'>💾 Dump & Restore:</b></p>
<ul>
<li><b>💾 T55xx Dump</b> - Save card to file (backup!)</li>
<li><b>📥 T55xx Restore</b> - Restore from backup</li>
<li><b>🎭 LF Simulate</b> - Test without writing</li>
</ul>

<p><b style='color: #ffffff;'>📝 Trace Analysis:</b></p>
<ul>
<li><b>📝 List EM</b> - Show captured EM traffic</li>
<li><b>📝 List HID</b> - Show captured HID traffic</li>
</ul>

<hr>

<h2 style='color: #00ffff;'>🛠️ Button Guide - HF Tools</h2>

<p><b style='color: #ffffff;'>📡 Tag Scanning:</b></p>
<ul>
<li><b>🔍 HF Search</b> - Auto-detect HF card type</li>
<li><b>📊 HF Tune</b> - Check HF antenna</li>
<li><b>🎯 HF Sniff</b> - Record HF traffic</li>
</ul>

<p><b style='color: #ffffff;'>📇 Tag Readers:</b></p>
<ul>
<li><b>💳 ISO14443-A Reader</b> - Read most 13.56MHz cards</li>
<li><b>🎴 ISO14443-A Info</b> - Detailed card info (UID, ATQA, SAK)</li>
<li><b>🔎 iClass Reader</b> - Corporate high-security</li>
<li><b>💎 Legic Reader</b> - European ski passes/transit</li>
</ul>

<p><b style='color: #ffffff;'>🔐 MIFARE Tools:</b></p>
<ul>
<li><b>🤖 MIFARE Autopwn</b> - One-click key recovery (USE THIS)</li>
<li><b>🗝️ Check Keys</b> - Test known keys</li>
<li><b>📖 Dump Card</b> - Save MIFARE data</li>
<li><b>🔓 Nested Attack</b> - Advanced key recovery</li>
</ul>

<hr>

<h2 style='color: #00ffff;'>💡 Pro Tips</h2>
<ul>
<li><b style='color: #00ff00;'>✅ Always Verify</b> - Run Search after every clone</li>
<li><b style='color: #00ff00;'>✅ Backup First</b> - Use T55xx Dump before experimenting</li>
<li><b style='color: #00ff00;'>✅ Wipe Before Indala</b> - Always wipe blank first for Indala</li>
<li><b style='color: #00ff00;'>✅ Read Console Colors:</b>
  <ul>
  <li><span style='color: #00ff00;'>🟢 Green = Success</span></li>
  <li><span style='color: #ff0000;'>🔴 Red = Error</span></li>
  <li><span style='color: #ffff00;'>🟡 Yellow = Warning</span></li>
  <li><span style='color: #00ffff;'>🔵 Cyan = Data/Info</span></li>
  </ul>
</li>
<li><b style='color: #00ff00;'>✅ Try LF First</b> - Most building cards are 125kHz</li>
<li><b style='color: #00ff00;'>✅ Use Autopwn</b> - Don't manually try MIFARE keys</li>
</ul>

<hr>

<h2 style='color: #00ffff;'>🚨 Troubleshooting</h2>
<p><b style='color: #ff0000;'>"No tag found"</b></p>
<ul>
<li>Check card placement on antenna</li>
<li>Try rotating card 90 degrees</li>
<li>Ensure PM3 connected (green status)</li>
</ul>

<p><b style='color: #ff0000;'>"Clone failed"</b></p>
<ul>
<li>Verify blank is T55xx type</li>
<li>Try T55xx Wipe first</li>
<li>For Indala: try all 3 methods</li>
</ul>

<p><b style='color: #ff0000;'>"Autopwn failed"</b></p>
<ul>
<li>Card may have custom keys</li>
<li>Try Nested Attack instead</li>
<li>Some cards are encrypted (can't clone)</li>
</ul>

<hr>

<h2 style='color: #00ffff;'>⚖️ Legal Disclaimer</h2>
<p><b style='color: #ffff00;'>⚠️ IMPORTANT:</b> Only clone cards you own or have permission to clone.</p>
<p><b style='color: #00ff00;'>✅ Legal uses:</b> Security research, personal backups, education, authorized pentesting</p>
<p><b style='color: #ff0000;'>❌ Illegal uses:</b> Unauthorized access, fraud, illegal entry</p>

<hr>

<h2 style='color: #00ffff;'>🎉 You're Ready!</h2>
<p>Start with simple <b>EM410x</b> clones, then try <b>HID</b>, then advanced <b>MIFARE</b>.</p>
<p><b style='color: #00ff00;'>Happy (legal) hacking! 🔥</b></p>

<p style='color: #888; font-size: 9px;'><i>CyberNinjaRFID v1.0.0 - Built with ❤️ for the Proxmark3 Community</i></p>
"""

        help_text.setHtml(help_content)
        layout.addWidget(help_text)

        # Add quick reference buttons at bottom
        btn_layout = QHBoxLayout()

        em_guide_btn = QPushButton("📖 EM410x Guide")
        em_guide_btn.clicked.connect(lambda: help_text.verticalScrollBar().setValue(
            help_text.document().findBlockByLineNumber(20).position()))
        btn_layout.addWidget(em_guide_btn)

        hid_guide_btn = QPushButton("📖 HID Guide")
        hid_guide_btn.clicked.connect(lambda: help_text.verticalScrollBar().setValue(
            help_text.document().findBlockByLineNumber(35).position()))
        btn_layout.addWidget(hid_guide_btn)

        indala_guide_btn = QPushButton("📖 Indala Guide")
        indala_guide_btn.clicked.connect(lambda: help_text.verticalScrollBar().setValue(
            help_text.document().findBlockByLineNumber(50).position()))
        btn_layout.addWidget(indala_guide_btn)

        top_btn = QPushButton("⬆️ Back to Top")
        top_btn.clicked.connect(lambda: help_text.verticalScrollBar().setValue(0))
        btn_layout.addWidget(top_btn)

        layout.addLayout(btn_layout)

        return widget

    def apply_cyber_theme(self):
        """Apply CyberNinja dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e27;
                color: #00d4ff;
            }
            QWidget {
                background-color: #0a0e27;
                color: #00d4ff;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QGroupBox {
                border: 2px solid #00d4ff;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #00d4ff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #1a1f3a;
                color: #00d4ff;
                border: 2px solid #00d4ff;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00d4ff;
                color: #0a0e27;
                border: 2px solid #00ffff;
            }
            QPushButton:pressed {
                background-color: #0088cc;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1a1f3a;
                color: #00d4ff;
                border: 2px solid #00d4ff;
                border-radius: 3px;
                padding: 5px;
                selection-background-color: #00d4ff;
                selection-color: #0a0e27;
            }
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #00d4ff;
                width: 12px;
                height: 12px;
            }
            QTabWidget::pane {
                border: 2px solid #00d4ff;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #1a1f3a;
                color: #00d4ff;
                border: 2px solid #00d4ff;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #00d4ff;
                color: #0a0e27;
            }
            QTabBar::tab:hover {
                background-color: #2a3f5a;
            }
            QLabel {
                color: #00d4ff;
            }
            QStatusBar {
                background-color: #1a1f3a;
                color: #00d4ff;
                border-top: 2px solid #00d4ff;
            }
            QMenuBar {
                background-color: #1a1f3a;
                color: #00d4ff;
            }
            QMenuBar::item:selected {
                background-color: #00d4ff;
                color: #0a0e27;
            }
        """)

    def scan_devices(self):
        """Scan for available devices"""
        self.status_bar.showMessage("🔍 Scanning for devices...")
        self.scanner = DeviceScanner()
        self.scanner.devices_found.connect(self.on_devices_found)
        self.scanner.start()

    def on_devices_found(self, devices: List[Dict]):
        """Handle device scan results"""
        self.port_combo.clear()

        if not devices:
            self.port_combo.addItem("❌ No devices found")
            self.status_bar.showMessage("❌ No devices found")
        else:
            for dev in devices:
                display = f"{dev['device']} - {dev['description']}"
                self.port_combo.addItem(display, dev['device'])
            self.status_bar.showMessage(f"✅ Found {len(devices)} device(s)")

    def toggle_connection(self):
        """Toggle PM3 connection"""
        if self.pm3_thread and self.pm3_thread.is_connected:
            self.disconnect_pm3()
        else:
            self.connect_pm3()

    def connect_pm3(self):
        """Connect to PM3 device"""
        port_data = self.port_combo.currentData()
        if not port_data:
            # Try to extract from text
            port_text = self.port_combo.currentText()
            if " - " in port_text:
                port_data = port_text.split(" - ")[0]
            else:
                QMessageBox.warning(self, "⚠️ No Device", "Please select a device first!")
                return

        self.log_output(f"🔌 Connecting to {port_data}...")

        self.pm3_thread = PM3ConnectionThread(port_data)
        self.pm3_thread.connected.connect(self.on_connected)
        self.pm3_thread.disconnected.connect(self.on_disconnected)
        self.pm3_thread.error.connect(self.on_connection_error)
        self.pm3_thread.output.connect(self.log_output)
        self.pm3_thread.start()

    def disconnect_pm3(self):
        """Disconnect from PM3"""
        if self.pm3_thread:
            self.pm3_thread.disconnect()
            self.pm3_thread = None

    def on_connected(self, device_name: str):
        """Handle successful connection"""
        self.status_label.setText(f"🟢 Connected: {device_name}")
        self.status_label.setStyleSheet("font-weight: bold; color: #00d4ff;")
        self.connect_button.setText("🔌 Disconnect")
        self.status_bar.showMessage(f"✅ Connected to {device_name}")
        self.log_output(f"✅ Successfully connected to {device_name}\n")

        # Auto-refresh device info
        QTimer.singleShot(500, self.refresh_device_info)

    def on_disconnected(self):
        """Handle disconnection"""
        self.status_label.setText("⚪ Disconnected")
        self.status_label.setStyleSheet("font-weight: bold; color: #888;")
        self.connect_button.setText("🔌 Connect")
        self.status_bar.showMessage("🔌 Disconnected")
        self.log_output("🔌 Disconnected from PM3\n")

    def on_connection_error(self, error: str):
        """Handle connection error"""
        self.log_output(f"{error}\n")
        QMessageBox.critical(self, "Connection Error", error)

    def execute_command(self):
        """Execute PM3 command"""
        command = self.command_input.text().strip()
        if not command:
            return

        if not self.pm3_thread or not self.pm3_thread.is_connected:
            QMessageBox.warning(self, "⚠️ Not Connected", "Please connect to PM3 first!")
            return

        # Disable command input during execution to prevent double-execution
        self.command_input.setEnabled(False)
        self.status_bar.showMessage(f"⏳ Executing: {command}")

        self.log_output(f"\n💻 > {command}\n")

        # Use QTimer to execute command asynchronously to keep GUI responsive
        QTimer.singleShot(10, lambda: self._do_execute_command(command))

    def _do_execute_command(self, command: str):
        """Internal command execution with cleanup"""
        try:
            self.pm3_thread.execute_command(command)

            # Add to history
            self.command_history.append(command)
            self.command_input.clear()
        finally:
            # Re-enable command input after execution
            QTimer.singleShot(500, lambda: self.command_input.setEnabled(True))
            QTimer.singleShot(500, lambda: self.status_bar.showMessage("✅ Ready"))

    def quick_command(self, command: str):
        """Execute a quick command"""
        self.command_input.setText(command)
        self.execute_command()

    def em410x_write(self):
        """EM410x Write with HEX ID input"""
        hex_id, ok = QInputDialog.getText(
            self,
            "EM410x Write",
            "Enter EM410x HEX ID (10 digits):",
            QLineEdit.Normal,
            ""
        )
        if ok and hex_id:
            command = f"lf em 410x write {hex_id}"
            self.quick_command(command)

    def t55xx_write(self):
        """T55xx Write with block and data input"""
        block, ok = QInputDialog.getText(
            self,
            "T55xx Write",
            "Enter block number (0-7):",
            QLineEdit.Normal,
            "0"
        )
        if not ok or not block:
            return

        data, ok = QInputDialog.getText(
            self,
            "T55xx Write",
            "Enter HEX data (8 digits):",
            QLineEdit.Normal,
            ""
        )
        if ok and data:
            command = f"lf t55xx write --blk {block} --data {data}"
            self.quick_command(command)

    def indala_clone_raw(self):
        """Indala Clone by Raw HEX"""
        raw, ok = QInputDialog.getText(
            self,
            "Indala Clone (Raw)",
            "Enter RAW HEX (from 'lf search'):",
            QLineEdit.Normal,
            ""
        )
        if ok and raw:
            command = f"lf indala clone -r {raw}"
            self.quick_command(command)

    def indala_clone_fc_cn(self):
        """Indala Clone by Facility Code + Card Number"""
        fc, ok = QInputDialog.getText(
            self,
            "Indala Clone",
            "Enter Facility Code:",
            QLineEdit.Normal,
            ""
        )
        if not ok or not fc:
            return

        cn, ok = QInputDialog.getText(
            self,
            "Indala Clone",
            "Enter Card Number:",
            QLineEdit.Normal,
            ""
        )
        if ok and cn:
            command = f"lf indala clone --fc {fc} --cn {cn}"
            self.quick_command(command)

    def indala_clone_heden(self):
        """Indala Clone by HEDEN HEX ID"""
        heden_id, ok = QInputDialog.getText(
            self,
            "Indala Clone (HEDEN)",
            "Enter HEDEN HEX ID:",
            QLineEdit.Normal,
            ""
        )
        if ok and heden_id:
            command = f"lf indala clone --heden {heden_id}"
            self.quick_command(command)

    def hid_clone(self):
        """HID Clone by Facility Code + Card Number"""
        fc, ok = QInputDialog.getText(
            self,
            "HID Clone",
            "Enter Facility Code:",
            QLineEdit.Normal,
            ""
        )
        if not ok or not fc:
            return

        cn, ok = QInputDialog.getText(
            self,
            "HID Clone",
            "Enter Card Number:",
            QLineEdit.Normal,
            ""
        )
        if ok and cn:
            command = f"lf hid clone --fc {fc} --cn {cn}"
            self.quick_command(command)

    def t55xx_read_blocks(self):
        """Read all T55xx blocks (0-7)"""
        self.log_output("\n[*] 📖 T55xx Block Dump Starting...\n")

        for block in range(8):
            command = f"lf t55xx read --blk {block}"
            self.command_input.setText(command)
            self.execute_command()
            # Add a small delay to prevent overwhelming the PM3
            import time
            time.sleep(0.5)

        self.log_output("\n[*] ✅ T55xx Block Dump Complete!\n")

    def t55xx_dump(self):
        """Dump T55xx to file"""
        filename, ok = QInputDialog.getText(
            self,
            "T55xx Dump",
            "Enter filename (e.g., mytag.bin):",
            QLineEdit.Normal,
            "dump.bin"
        )
        if ok and filename:
            command = f"lf t55xx dump {filename}"
            self.quick_command(command)

    def t55xx_restore(self):
        """Restore T55xx from file"""
        filename, ok = QInputDialog.getText(
            self,
            "T55xx Restore",
            "Enter filename to restore:",
            QLineEdit.Normal,
            "dump.bin"
        )
        if ok and filename:
            command = f"lf t55xx restore {filename}"
            self.quick_command(command)

    def lf_simulate(self):
        """LF Simulate from file"""
        filename, ok = QInputDialog.getText(
            self,
            "LF Simulate",
            "Enter filename to simulate:",
            QLineEdit.Normal,
            "dump.bin"
        )
        if ok and filename:
            command = f"lf sim {filename}"
            self.quick_command(command)

    def log_output(self, text: str):
        """Log output to console with Linux-style colorization"""
        # Skip empty text to reduce processing
        if not text or not text.strip():
            return

        # Colorize the output based on content
        colored_html = self.colorize_output(text)

        # Batch update to reduce redraws (better performance)
        self.output_text.setUpdatesEnabled(False)
        self.output_text.append(colored_html)

        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output_text.setTextCursor(cursor)

        # Limit output size
        if self.output_text.document().lineCount() > MAX_OUTPUT_LINES:
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, 100)
            cursor.removeSelectedText()

        self.output_text.setUpdatesEnabled(True)

        # Also update HF/LF consoles if they exist (async to prevent lag)
        if hasattr(self, 'hf_output_text'):
            QTimer.singleShot(0, lambda: self.hf_output_text.append(colored_html))
        if hasattr(self, 'lf_output_text'):
            QTimer.singleShot(0, lambda: self.lf_output_text.append(colored_html))

    def colorize_output(self, text: str) -> str:
        """Colorize text output Linux terminal style"""
        lines = text.split('\n')
        colored_lines = []

        for line in lines:
            # Success patterns (green)
            if any(word in line for word in ['✅', '[+]', 'success', 'Success', 'SUCCESS', 'OK', 'Connected', 'found']):
                colored_lines.append(f'<span style="color: #00ff00;">{line}</span>')
            # Error patterns (red)
            elif any(word in line for word in ['❌', '[-]', 'error', 'Error', 'ERROR', 'failed', 'Failed', 'FAILED']):
                colored_lines.append(f'<span style="color: #ff0000;">{line}</span>')
            # Warning patterns (yellow)
            elif any(word in line for word in ['⚠️', '[!]', 'warning', 'Warning', 'WARNING', 'timeout']):
                colored_lines.append(f'<span style="color: #ffff00;">{line}</span>')
            # Info/Data patterns (green)
            elif any(word in line for word in ['[=]', 'UID', 'ID', 'Type', 'Block', 'Data', 'Version', 'Proxmark']):
                colored_lines.append(f'<span style="color: #00ff00;">{line}</span>')
            # Command execution (magenta)
            elif line.startswith('pm3') or line.startswith('[usb'):
                colored_lines.append(f'<span style="color: #ff00ff;">{line}</span>')
            # Default (green for readability)
            else:
                colored_lines.append(f'<span style="color: #00ff00;">{line}</span>')

        return '<br>'.join(colored_lines)

    def refresh_device_info(self):
        """Refresh device information"""
        if not self.pm3_thread or not self.pm3_thread.is_connected:
            return

        self.status_bar.showMessage("🔄 Refreshing device info...")

        # Execute hw version and parse output
        self.pm3_thread.execute_command("hw version", capture=True)

        # Give it time to execute, then update labels
        QTimer.singleShot(1000, self.update_device_labels)

    def update_device_labels(self):
        """Update device info labels from PM3 output"""
        if not self.pm3_thread or not hasattr(self.pm3_thread, 'pm3_device'):
            self.device_fw_label.setText("❌ Not connected")
            self.device_hw_label.setText("❌ Not connected")
            self.device_serial_label.setText("❌ Not connected")
            return

        try:
            # Get the output from the command
            output = self.pm3_thread.pm3_device.grabbed_output

            if not output or len(output) < 10:
                self.device_fw_label.setText("⏳ Loading...")
                self.device_hw_label.setText("⏳ Loading...")
                self.device_serial_label.setText("⏳ Loading...")
                return

            # Parse firmware version - look for Iceman/master line in ARM section
            fw_found = False
            for line in output.split('\n'):
                if "Iceman/master" in line and ("Bootrom" in line or "OS........." in line):
                    # Extract just the version part
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if "Iceman/master" in part:
                            # Get version and date/time
                            version_info = ' '.join(parts[i:i+3]) if i+2 < len(parts) else part
                            self.device_fw_label.setText(version_info)
                            fw_found = True
                            break
                    if fw_found:
                        break
            if not fw_found:
                self.device_fw_label.setText("Iceman Firmware v4.x")

            # Parse hardware model - look for "Firmware.................. PM3 GENERIC"
            hw_found = False
            for line in output.split('\n'):
                if "Firmware" in line and "PM3" in line and "." in line:
                    # Extract PM3 model after dots
                    if "PM3 GENERIC" in line:
                        self.device_hw_label.setText("PM3 GENERIC")
                        hw_found = True
                    elif "PM3 EASY" in line:
                        self.device_hw_label.setText("PM3 EASY")
                        hw_found = True
                    elif "PM3 RDV" in line:
                        self.device_hw_label.setText("PM3 RDV4")
                        hw_found = True
                    break
            if not hw_found:
                self.device_hw_label.setText("PM3 GENERIC")

            # Parse serial/port - look for "Using UART port COM5"
            port_found = False
            for line in output.split('\n'):
                if "Using UART port" in line:
                    # Extract just "Using UART port COM5"
                    self.device_serial_label.setText(line.strip().replace("[+] ", ""))
                    port_found = True
                    break
            if not port_found and hasattr(self, 'port'):
                self.device_serial_label.setText(f"Connected on {self.port}")

            self.status_bar.showMessage("✅ Device info updated")

        except Exception as e:
            logger.error(f"Failed to update device labels: {e}")
            self.device_fw_label.setText("⚠️ Failed to read")
            self.device_hw_label.setText("⚠️ Failed to read")
            self.device_serial_label.setText("⚠️ Failed to read")

    def load_scripts(self):
        """Load scripts from directory"""
        scripts_dir = Path(__file__).parent.parent / "proxmark3" / "client" / "luascripts"
        if scripts_dir.exists():
            scripts = list(scripts_dir.glob("*.lua"))
            script_list = "\n".join([f"📜 {s.name}" for s in scripts])
            self.scripts_list.setText(script_list or "📁 No scripts found")
            self.status_bar.showMessage(f"✅ Loaded {len(scripts)} scripts")
        else:
            self.scripts_list.setText("❌ Scripts directory not found")

# ==================== MAIN ====================
def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    # Set app icon if available
    # app.setWindowIcon(QIcon("icon.png"))

    window = CyberNinjaRFIDWindow()
    window.show()

    logger.info(f"🚀 {APP_NAME} {VERSION} started")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
