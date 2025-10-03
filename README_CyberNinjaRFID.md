# 🔥 CyberNinjaRFID - Proxmark3 Iceman GUI 🔥

A cyberpunk-themed, modern GUI for **Proxmark3 Iceman Firmware** with enhanced connectivity and sleek design.

**Hack The Planet! 💀**

---

## ✨ Features

🎨 **CyberNinja Dark Theme**
- Slick cyberpunk aesthetic with neon green accents
- Easy on the eyes for long hacking sessions
- Emoji-rich UI for visual feedback

🔌 **Enhanced Device Connectivity**
- Auto-detection of Proxmark3 devices on serial ports
- One-click connect/disconnect
- Real-time connection status

💻 **Command Console**
- Interactive command execution
- Command history
- Real-time output display
- Quick command buttons for common tasks

📊 **Multiple Tool Tabs**
- **Device Info**: Hardware/firmware information
- **HF Tools**: High-frequency RFID operations
- **LF Tools**: Low-frequency RFID operations
- **Scripts**: Lua script management

🚀 **Quick Actions**
- Pre-configured buttons for common commands
- HF/LF search and tuning
- MIFARE operations
- EM410x operations
- And much more!

---

## 📋 Requirements

- **Python 3.7+**
- **Proxmark3 Iceman Firmware** (installed and compiled)
- **PyQt5** (GUI framework)
- **pyserial** (serial communication)

---

## 🚀 Installation

### Windows

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the GUI**:
   ```bash
   run_cyberninja_rfid.bat
   ```
   Or simply double-click `run_cyberninja_rfid.bat`

### Linux/macOS

1. **Install Python3** (usually pre-installed):
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip

   # macOS (with Homebrew)
   brew install python3
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the GUI**:
   ```bash
   chmod +x run_cyberninja_rfid.sh
   ./run_cyberninja_rfid.sh
   ```
   Or:
   ```bash
   python3 CyberNinjaRFID.py
   ```

---

## 🔧 Usage

### 1. **Launch the GUI**
   - Windows: Run `run_cyberninja_rfid.bat`
   - Linux/macOS: Run `./run_cyberninja_rfid.sh`

### 2. **Connect to Proxmark3**
   - Click **"🔍 Scan Devices"** to auto-detect your PM3
   - Select your device from the dropdown
   - Click **"🔌 Connect"**
   - Status will show 🟢 when connected

### 3. **Execute Commands**
   - **Manual**: Type commands in the command input box and press Enter
   - **Quick Commands**: Click the pre-configured buttons for instant execution
   - **HF/LF Tools**: Use dedicated tabs for specific operations

### 4. **View Output**
   - All command outputs appear in the console
   - Auto-scrolls to latest output
   - Use **"🗑️ Clear Output"** to clean the console

---

## 📚 Common Commands

### Device Management
- `hw version` - Show firmware version
- `hw status` - Display hardware status
- `hw tune` - Tune antenna (HF/LF)

### High Frequency (HF)
- `hf search` - Auto-detect HF tags
- `hf 14a reader` - Read ISO14443A card
- `hf mf autopwn` - MIFARE autopwn attack
- `hf list` - List HF communications

### Low Frequency (LF)
- `lf search` - Auto-detect LF tags
- `lf em 410x reader` - Read EM410x card
- `lf t55xx detect` - Detect T55xx card
- `lf list` - List LF communications

---

## 🎯 Quick Start Guide

1. **First Time Setup**:
   ```bash
   # Install requirements
   pip install -r requirements.txt

   # Run the GUI
   python3 CyberNinjaRFID.py
   ```

2. **Connect Your PM3**:
   - Plug in your Proxmark3 device via USB
   - Click "🔍 Scan Devices"
   - Select your device (e.g., `/dev/ttyACM0` or `COM3`)
   - Click "🔌 Connect"

3. **Start Hacking**! 🔥
   - Place a tag near the antenna
   - Click "🔍 LF Search" or "🔎 HF Search"
   - Watch the magic happen! ✨

---

## 🛠️ Troubleshooting

### ❌ "PM3 module not available"
- Make sure you've compiled the Proxmark3 client with Python support
- The PM3 Python module should be in: `../proxmark3/client/pyscripts/`
- Run the compile with SWIG support enabled

### ❌ "No devices found"
- Check USB connection
- Ensure Proxmark3 drivers are installed
- On Linux: Check permissions (`sudo usermod -a -G dialout $USER`)
- On Windows: Install ProxSpace drivers

### ❌ "Connection failed"
- Verify the correct port is selected
- Close any other programs using the PM3 (like the official client)
- Try unplugging and replugging the device

### ❌ "Import Error: PyQt5"
- Install PyQt5: `pip install PyQt5`
- On Linux: `sudo apt install python3-pyqt5`

---

## 🎨 Theme Customization

The GUI uses a **CyberNinja dark theme** with:
- Background: `#0a0e27` (Deep space blue)
- Accent: `#00ff88` (Neon green)
- Borders: `#00ff88` (Neon green)
- Hover: Inverted colors for emphasis

To customize the theme, edit the `apply_cyber_theme()` method in `CyberNinjaRFID.py`.

---

## 📝 Features Roadmap

- [ ] 🔐 **Saved Sessions**: Save/load command sessions
- [ ] 📊 **Visual Tag Info**: Graphical display of tag data
- [ ] 🔄 **Auto-Update**: Check for GUI updates
- [ ] 🎭 **Multiple Themes**: Light/Dark/Custom themes
- [ ] 📡 **Wireless Support**: Bluetooth PM3 connectivity
- [ ] 🤖 **AI Assistant**: Smart command suggestions

---

## 🤝 Contributing

Want to add features or fix bugs? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

This project follows the **Proxmark3 Iceman** license.

---

## 🙏 Credits

- **Proxmark3 Team** - For the amazing hardware and firmware
- **Iceman** - For the incredible Iceman fork
- **CyberNinja** - For the theme inspiration

---

## 🔥 Hack Responsibly! 💀

This tool is for **educational and authorized security research only**.

Always obtain proper authorization before testing RFID systems.

**Stay Cyber. Stay Ninja. 🥷**

---

## 📞 Support

- **Issues**: Report bugs in the Issues section
- **Documentation**: [Proxmark3 Docs](https://github.com/RfidResearchGroup/proxmark3)
- **Community**: Join the Proxmark3 Discord/Forum

---

**🔥 Happy Hacking! 💀**
