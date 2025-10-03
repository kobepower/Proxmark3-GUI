# 📂 CyberNinjaRFID - Complete File Guide

## 🎯 Quick Reference

| File | Type | Purpose | Lines |
|------|------|---------|-------|
| **CyberNinjaRFID.py** | Main | GUI Application | ~700 |
| **pm3_command_parser.py** | Core | Command Discovery | ~300 |
| **pm3_compatibility.py** | Core | Version Compatibility | ~250 |
| **command_profiles.json** | Config | User Presets | - |
| **config.json** | Config | GUI Settings | - |
| **requirements.txt** | Deps | Python Packages | - |

---

## 🔥 Core Application Files

### **CyberNinjaRFID.py**
- **Purpose**: Main GUI application
- **Size**: ~700 lines
- **Features**:
  - PyQt5 GUI with 5 tabs
  - Device auto-detection
  - Command execution
  - Real-time output display
  - CyberNinja dark theme
  - Integration with all modules

**Usage**: This is the main entry point
```bash
python3 CyberNinjaRFID.py
```

---

### **pm3_command_parser.py**
- **Purpose**: Dynamic command discovery system
- **Size**: ~300 lines
- **Features**:
  - Parses PM3 help output
  - Discovers commands automatically
  - Provides smart suggestions
  - Caches commands for speed
  - Searches by keyword

**Key Classes**:
- `PM3Command` - Command data structure
- `PM3CommandParser` - Main parser class

**Why It Matters**: Makes GUI future-proof!

---

### **pm3_compatibility.py**
- **Purpose**: Firmware compatibility layer
- **Size**: ~250 lines
- **Features**:
  - Detects firmware version
  - Normalizes command syntax
  - Checks device capabilities
  - Translates old→new commands
  - Hardware feature detection

**Key Classes**:
- `PM3CompatibilityLayer` - Main compatibility class

**Why It Matters**: Works with ANY Iceman version!

---

## ⚙️ Configuration Files

### **command_profiles.json**
- **Purpose**: User-editable command presets
- **Format**: JSON
- **Structure**:
  ```json
  {
    "Category Name": {
      "Button Label": "pm3 command"
    }
  }
  ```

**How to Use**:
1. Edit this file directly
2. Add your favorite commands
3. Reload GUI
4. New buttons appear!

**Example**:
```json
{
  "🔍 My Scans": {
    "Quick HF": "hf search",
    "Quick LF": "lf search"
  }
}
```

---

### **config.json**
- **Purpose**: GUI configuration
- **Format**: JSON
- **Settings**:
  - App info (name, version)
  - Connection (timeout, retries)
  - UI (colors, fonts, behavior)
  - Paths (PM3 client, scripts)
  - Logging (level, size)

**Customization**:
```json
{
  "colors": {
    "background": "#0a0e27",
    "foreground": "#00ff88"
  },
  "ui": {
    "font_size": 12,
    "max_output_lines": 2000
  }
}
```

---

## 📦 Dependencies

### **requirements.txt**
- **Purpose**: Python package requirements
- **Packages**:
  - `PyQt5` - GUI framework
  - `pyserial` - Serial communication

**Install**:
```bash
pip install -r requirements.txt
```

---

## 🚀 Launcher Scripts

### **run_cyberninja_rfid.bat** (Windows)
- **Purpose**: Easy Windows launcher
- **Features**:
  - Checks Python installation
  - Installs dependencies
  - Launches GUI
  - Shows errors

**Usage**: Double-click the file

---

### **run_cyberninja_rfid.sh** (Linux/macOS)
- **Purpose**: Easy Unix launcher
- **Features**:
  - Checks Python3 installation
  - Installs dependencies
  - Launches GUI
  - Shows errors

**Usage**:
```bash
chmod +x run_cyberninja_rfid.sh
./run_cyberninja_rfid.sh
```

---

## 🔍 Utility Scripts

### **check_setup.py**
- **Purpose**: Verify installation
- **Checks**:
  - ✅ Python version
  - ✅ PyQt5 installed
  - ✅ pyserial installed
  - ✅ PM3 module available
  - ✅ Config files present

**Usage**:
```bash
python3 check_setup.py
```

**Output**:
```
============================================================
🔍 CyberNinjaRFID Setup Checker
============================================================

📌 Python Version Check:
   ✅ Python version OK

📦 Dependency Check:
   ✅ PyQt5 installed
   ✅ pyserial installed

🔌 PM3 Module Check:
   ✅ PM3 module found

============================================================
✅ All dependencies installed!
🚀 Ready to run: python3 CyberNinjaRFID.py
============================================================
```

---

## 📚 Documentation Files

### **README.md** (Master)
- **Purpose**: Main project documentation
- **Covers**:
  - Why CyberNinjaRFID is different
  - Features overview
  - Quick start guide
  - Architecture explanation
  - Troubleshooting
  - Contributing guide

**Audience**: Everyone

---

### **README_CyberNinjaRFID.md**
- **Purpose**: User manual
- **Covers**:
  - Detailed features
  - Installation steps
  - Usage instructions
  - Common commands
  - Troubleshooting
  - Tips & tricks

**Audience**: End users

---

### **QUICKSTART.md**
- **Purpose**: Get up and running fast
- **Covers**:
  - 3-step installation
  - First connection
  - Basic commands
  - Quick tips

**Audience**: Beginners

---

### **FEATURES.md**
- **Purpose**: Complete feature list
- **Covers**:
  - Core features
  - Tab descriptions
  - Technical architecture
  - Comparison with old GUI
  - Future roadmap

**Audience**: Users exploring features

---

### **FUTURE_PROOF_DESIGN.md**
- **Purpose**: Architecture deep-dive
- **Covers**:
  - Why past GUIs failed
  - Our solution
  - How it stays compatible
  - Update workflow
  - Design principles

**Audience**: Developers, technical users

---

### **PROJECT_SUMMARY.md**
- **Purpose**: Project overview
- **Covers**:
  - What was built
  - Project structure
  - Features implemented
  - How to use
  - Testing status
  - Statistics

**Audience**: Project overview seekers

---

### **FILE_GUIDE.md** (This file)
- **Purpose**: Navigate all files
- **Covers**:
  - File descriptions
  - Purpose of each file
  - Usage instructions
  - Quick reference

**Audience**: You! 😎

---

## 📂 Auto-Generated Files

### **logs/cyberninja_rfid.log**
- **Purpose**: Application log file
- **Contains**: All app activity, errors, debug info
- **Auto-created**: On first run

---

### **logs/pm3_capabilities.json**
- **Purpose**: Detected PM3 capabilities
- **Contains**: Firmware version, features (HF/LF/Flash/BT)
- **Auto-created**: On PM3 connection

**Example**:
```json
{
  "firmware_version": "4.18341",
  "is_iceman": true,
  "capabilities": {
    "hf": true,
    "lf": true,
    "flash": true
  }
}
```

---

### **logs/pm3_commands_cache.json**
- **Purpose**: Cached PM3 commands
- **Contains**: All discovered commands
- **Auto-created**: After command discovery

**Why**: Speeds up startup

---

## 🗂️ Directory Structure

```
pm3/GUI/
│
├── 🔥 CORE APPLICATION
│   ├── CyberNinjaRFID.py          # Main GUI
│   ├── pm3_command_parser.py      # Command discovery
│   └── pm3_compatibility.py       # Compatibility layer
│
├── ⚙️ CONFIGURATION
│   ├── command_profiles.json      # User presets
│   └── config.json                # GUI settings
│
├── 📦 DEPENDENCIES
│   └── requirements.txt           # Python packages
│
├── 🚀 LAUNCHERS
│   ├── run_cyberninja_rfid.bat    # Windows
│   └── run_cyberninja_rfid.sh     # Linux/macOS
│
├── 🔍 UTILITIES
│   └── check_setup.py             # Setup checker
│
├── 📚 DOCUMENTATION
│   ├── README.md                  # Master doc
│   ├── README_CyberNinjaRFID.md   # User manual
│   ├── QUICKSTART.md              # Quick start
│   ├── FEATURES.md                # Feature list
│   ├── FUTURE_PROOF_DESIGN.md     # Architecture
│   ├── PROJECT_SUMMARY.md         # Overview
│   └── FILE_GUIDE.md              # This file
│
├── 📂 LOGS (auto-generated)
│   ├── cyberninja_rfid.log
│   ├── pm3_capabilities.json
│   └── pm3_commands_cache.json
│
└── 📁 LEGACY (old GUI)
    ├── V0.2.8-win64/
    └── GUIsettings.ini
```

---

## 🎯 File Usage Flowchart

```
User wants to run GUI
         ↓
   Run launcher script
   (bat/sh)
         ↓
   Checks dependencies
   (requirements.txt)
         ↓
   Launches main GUI
   (CyberNinjaRFID.py)
         ↓
   Loads configuration
   (config.json)
         ↓
   Connects to PM3
         ↓
   Detects capabilities
   (pm3_compatibility.py)
         ↓
   Discovers commands
   (pm3_command_parser.py)
         ↓
   Loads user presets
   (command_profiles.json)
         ↓
   Ready to hack! 🔥
```

---

## 📝 Quick Actions

### **Want to customize commands?**
→ Edit: `command_profiles.json`

### **Want to change theme?**
→ Edit: `config.json` (colors section)

### **Want to check if setup works?**
→ Run: `python3 check_setup.py`

### **Want to understand architecture?**
→ Read: `FUTURE_PROOF_DESIGN.md`

### **Want quick start guide?**
→ Read: `QUICKSTART.md`

### **Want all features?**
→ Read: `FEATURES.md`

### **Want to launch GUI?**
→ Run: `./run_cyberninja_rfid.sh` (or `.bat`)

---

## 🏆 File Importance Ranking

### 🔥 **Critical** (don't delete!)
1. `CyberNinjaRFID.py` - Main application
2. `pm3_command_parser.py` - Command discovery
3. `pm3_compatibility.py` - Compatibility layer
4. `requirements.txt` - Dependencies

### ⚙️ **Important** (needed for full features)
5. `command_profiles.json` - User presets
6. `config.json` - Configuration
7. `run_cyberninja_rfid.*` - Easy launchers

### 📚 **Documentation** (helpful but not required)
8. `README.md` - Main docs
9. `QUICKSTART.md` - Quick guide
10. `FEATURES.md` - Feature list
11. Others - Additional docs

### 🔧 **Utilities** (nice to have)
12. `check_setup.py` - Setup checker

---

## 🎉 Summary

**Total Files**: 15+ files
**Core Code**: 3 Python modules (~1,175 lines)
**Documentation**: 7 markdown files
**Configuration**: 2 JSON files
**Utilities**: 3 scripts

**Everything you need for a future-proof PM3 GUI! 🔥💀**

---

**📂 File navigation complete! Now go hack the planet! 🚀**
