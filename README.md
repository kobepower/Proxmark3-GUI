# 🔥 CyberNinjaRFID - The Future-Proof Proxmark3 GUI 💀

> **A cyberpunk-themed, eternally-compatible GUI for Proxmark3 Iceman firmware**

[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-GPL-red.svg)](LICENSE)

---

## 🎯 Why CyberNinjaRFID is Different

### ❌ **Why Other GUIs Failed:**
- Hard-coded command buttons
- Broke on firmware updates
- Required constant maintenance
- Abandoned after 6-12 months

### ✅ **Why CyberNinjaRFID Will Last:**
- **Dynamic command discovery** - Auto-detects new commands
- **CLI passthrough** - Uses real PM3 binary, not reimplementation
- **Compatibility layer** - Works with old AND new firmware
- **User-editable profiles** - No coding required for customization
- **Future-proof architecture** - Adapts to Iceman updates automatically

**Result: A GUI that survives firmware changes! 🚀**

---

## ✨ Features

### 🎨 **Visual Design**
- Cyberpunk dark theme (inspired by CyberNinja Trader)
- Neon green accents on deep space blue
- 50+ emojis for visual feedback
- Professional, modern interface

### 🔌 **Smart Connectivity**
- Auto-detection of PM3 devices
- One-click connect/disconnect
- Visual status indicators 🟢⚪🔴
- Connection error handling

### 🧠 **Intelligence**
- **Dynamic command parsing** from PM3 help
- **Auto-discovery** of new commands
- **Smart suggestions** as you type
- **Compatibility checking** per firmware version

### 💻 **Interface**
- **5 Organized Tabs**:
  1. 💻 Command Console (manual + quick commands)
  2. 📊 Device Info (hardware/firmware details)
  3. 📡 HF Tools (high-frequency operations)
  4. 📻 LF Tools (low-frequency operations)
  5. 🔧 Scripts (Lua/Python management)

- **Command Profiles** (customizable via JSON)
- **Real-time output** with syntax highlighting
- **Command history** (↑/↓ navigation)
- **Raw console** (fallback for any command)

---

## 📁 Project Structure

```
pm3/GUI/
├── 🚀 CyberNinjaRFID.py              # Main GUI (700+ lines)
├── 🧠 pm3_command_parser.py          # Dynamic command discovery
├── 🔄 pm3_compatibility.py           # Version compatibility layer
├── 📋 command_profiles.json          # User-editable command presets
├── ⚙️  config.json                    # GUI configuration
├── 📦 requirements.txt                # Python dependencies
│
├── 🪟 run_cyberninja_rfid.bat        # Windows launcher
├── 🐧 run_cyberninja_rfid.sh         # Linux/macOS launcher
├── 🔍 check_setup.py                 # Setup verification tool
│
├── 📚 README.md                       # This file
├── 📖 README_CyberNinjaRFID.md       # User documentation
├── 🚀 QUICKSTART.md                   # Quick start guide
├── ✨ FEATURES.md                     # Feature details
├── 🔮 FUTURE_PROOF_DESIGN.md         # Architecture explanation
├── 📋 PROJECT_SUMMARY.md             # Project overview
│
└── 📂 logs/                           # Auto-generated logs
    ├── cyberninja_rfid.log           # Application log
    ├── pm3_capabilities.json         # Detected capabilities
    └── pm3_commands_cache.json       # Command cache
```

**Total:** ~1,175 lines of Python code across 3 modules

---

## 🚀 Quick Start

### 1️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2️⃣ **Launch the GUI**

**Windows:**
```bash
run_cyberninja_rfid.bat
```

**Linux/macOS:**
```bash
./run_cyberninja_rfid.sh
```

### 3️⃣ **Connect & Hack**

1. Click **"🔍 Scan Devices"**
2. Select your PM3 device
3. Click **"🔌 Connect"**
4. Start hacking! 🔥

---

## 🔮 Future-Proof Architecture

### **How It Adapts to Firmware Updates:**

```
1. User updates Iceman firmware
         ↓
2. User connects PM3 to GUI
         ↓
3. GUI detects new firmware version ✅
         ↓
4. GUI discovers new commands ✅
         ↓
5. GUI updates command cache ✅
         ↓
6. New commands appear in UI ✅

NO CODE CHANGES NEEDED! 🎉
```

### **Key Technologies:**

1. **PM3 Command Parser** (`pm3_command_parser.py`)
   - Parses `help` output
   - Discovers commands dynamically
   - Caches for performance
   - Auto-suggestions

2. **Compatibility Layer** (`pm3_compatibility.py`)
   - Detects firmware version
   - Normalizes command syntax
   - Checks device capabilities (HF/LF/Flash/BT)
   - Translates old → new commands

3. **Command Profiles** (`command_profiles.json`)
   - User-editable JSON
   - No coding required
   - Shareable configs
   - Custom workflows

4. **CLI Passthrough**
   - Direct PM3 binary communication
   - Real output, not simulated
   - Full feature support

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [📖 README_CyberNinjaRFID.md](README_CyberNinjaRFID.md) | Complete user manual |
| [🚀 QUICKSTART.md](QUICKSTART.md) | 3-step setup guide |
| [✨ FEATURES.md](FEATURES.md) | Detailed feature list |
| [🔮 FUTURE_PROOF_DESIGN.md](FUTURE_PROOF_DESIGN.md) | Architecture deep-dive |
| [📋 PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview |

---

## 🛠️ Requirements

- **Python 3.7+**
- **PyQt5** (GUI framework)
- **pyserial** (serial communication)
- **Proxmark3 Iceman** (firmware)

**Install all:**
```bash
pip install -r requirements.txt
```

**Verify setup:**
```bash
python3 check_setup.py
```

---

## 🎮 Usage Examples

### **Basic Operations**

```bash
# Connect to PM3
1. Scan devices
2. Select port (e.g., COM3 or /dev/ttyACM0)
3. Connect

# Search for tags
- HF: Click "🔎 HF Search"
- LF: Click "🔍 LF Search"

# Read a card
- HF: Click "💳 HF 14a Reader"
- LF: Click "🎫 LF EM Reader"
```

### **Advanced Features**

```bash
# Custom command profiles
1. Edit command_profiles.json
2. Add: {"My Scan": "hf search --extended"}
3. Reload GUI
4. New button appears!

# Command suggestions
1. Type "hf" in console
2. See suggestions appear
3. Press Tab to autocomplete
```

---

## 🔧 Customization

### **Add Custom Commands**

Edit `command_profiles.json`:

```json
{
  "🆕 My Category": {
    "Custom Scan": "hf search --extended",
    "Quick Clone": "lf em 410x clone --id {UID}"
  }
}
```

### **Change Theme Colors**

Edit `config.json`:

```json
{
  "colors": {
    "background": "#0a0e27",
    "foreground": "#00ff88",
    "accent": "#00ffff"
  }
}
```

### **Configure Behavior**

Edit `config.json`:

```json
{
  "ui": {
    "max_output_lines": 1000,
    "font_size": 10,
    "auto_scroll": true
  }
}
```

---

## 🏆 Key Advantages

### **Vs. Original PM3 GUI:**
- ✅ Modern cyberpunk theme
- ✅ Auto device detection
- ✅ Dynamic command discovery
- ✅ Future-proof architecture
- ✅ User customization without coding

### **Vs. Other Third-Party GUIs:**
- ✅ Doesn't break on firmware updates
- ✅ No hard-coded commands
- ✅ Actively maintained design
- ✅ Community-editable profiles
- ✅ Built to last years, not months

---

## 🐛 Troubleshooting

### **"PM3 module not available"**
- Ensure Proxmark3 client is compiled with Python/SWIG support
- Check: `../proxmark3/client/pyscripts/pm3.py` exists

### **"No devices found"**
- Verify USB connection
- Install PM3 drivers
- On Linux: `sudo usermod -a -G dialout $USER`

### **"PyQt5 not installed"**
```bash
pip install PyQt5
```

### **"Permission denied" (Linux)**
```bash
sudo chmod 666 /dev/ttyACM0
```

---

## 🤝 Contributing

Want to help? Here's how:

1. **Add Command Profiles**: Edit `command_profiles.json`
2. **Report Bugs**: Open an issue
3. **Suggest Features**: Open a discussion
4. **Submit PRs**: Fork → Code → PR
5. **Share Configs**: Share your `command_profiles.json`

---

## 📊 Statistics

- **3 Python modules** (1,175 lines total)
- **5 UI tabs** (Console, Device, HF, LF, Scripts)
- **15+ quick commands** (expandable via profiles)
- **50+ emojis** (because why not? 😎)
- **3 platforms** (Windows, Linux, macOS)
- **∞ firmware compatibility** (future-proof!)

---

## 🔥 What Makes This Special

### **The Problem:**
Every PM3 GUI before this died within 6-12 months because:
- Hard-coded commands broke on updates
- Developers couldn't keep up with Iceman changes
- GUIs became obsolete and abandoned

### **Our Solution:**
CyberNinjaRFID **adapts automatically** because:
- Commands are discovered, not hard-coded
- Direct PM3 communication (no reimplementation)
- Compatibility layer handles version differences
- Users customize without code changes

### **The Result:**
**A GUI that will work for YEARS! 🚀**

---

## 📜 License

This project follows the **Proxmark3 Iceman** license.

---

## 🙏 Credits

- **Proxmark3 Team** - For the incredible hardware
- **Iceman** - For the amazing firmware fork
- **CyberNinja** - For the theme inspiration
- **Community** - For feedback and support

---

## 🎯 Quick Links

- 📚 [Full Documentation](README_CyberNinjaRFID.md)
- 🚀 [Quick Start Guide](QUICKSTART.md)
- 🔮 [Architecture Details](FUTURE_PROOF_DESIGN.md)
- ✨ [Feature List](FEATURES.md)
- 📋 [Project Summary](PROJECT_SUMMARY.md)

---

## 💪 Mission Statement

**"Build a GUI that outlives firmware changes."**

While other GUIs die in 6 months, CyberNinjaRFID adapts automatically to:
- ✅ New commands
- ✅ Syntax changes
- ✅ Feature additions
- ✅ Hardware capabilities

**This is the LAST PM3 GUI you'll ever need! 🔥**

---

<div align="center">

## 🔥 Hack The Planet! 💀

**Stay Cyber. Stay Ninja. 🥷**

Made with 💚 for the RFID hacking community

</div>

---

## 🚀 Get Started Now!

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the GUI
./run_cyberninja_rfid.sh  # or .bat on Windows

# 3. Connect and hack!
# Click "Scan" → Select device → Connect → Done! 🎉
```

**Welcome to the future of PM3 GUIs! 🔥💀**
