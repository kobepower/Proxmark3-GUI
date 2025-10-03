# 🚀 How to Run CyberNinjaRFID

## ⚠️ IMPORTANT: Run on Windows (Not WSL)

The GUI **MUST** be run on Windows where ProxSpace is installed, **NOT** from WSL (Windows Subsystem for Linux).

## Quick Start (3 Steps)

### 1️⃣ Open Windows Command Prompt or PowerShell
```
Win + R → cmd → Enter
```

### 2️⃣ Navigate to GUI folder
```cmd
cd D:\Claude-Terminal\ProxSpace\pm3\GUI
```
*(Or wherever your ProxSpace is installed)*

### 3️⃣ Run the launcher
```cmd
RUN_GUI.bat
```

That's it! The GUI will launch automatically.

---

## 🔧 Manual Method

If the batch file doesn't work:

```cmd
cd D:\Claude-Terminal\ProxSpace\pm3\GUI
python CyberNinjaRFID.py
```

---

## 📋 Requirements

- **Windows OS** (ProxSpace environment)
- **Python 3.7+**
- **PyQt5** (`pip install PyQt5`)
- **pyserial** (`pip install pyserial`)
- **ProxSpace** with PM3 installed

---

## ❌ Common Issues

### Issue: "PM3 Python module not available"
✅ **Solution**: This is normal! The GUI will use subprocess fallback method through ProxSpace bash.

### Issue: "No devices found"
✅ **Solution**:
1. Make sure Proxmark3 is plugged in
2. Check Device Manager for COM port
3. PM3 will show in device list even if not connected

### Issue: "Commands return 0 chars"
✅ **Solution**:
1. Ensure ProxSpace is installed correctly
2. GUI uses ProxSpace bash.exe to run PM3
3. Path should be detected automatically

### Issue: GUI shows green instead of cyan blue
✅ **Solution**: Update config.json colors to use #00d4ff

---

## 🎨 CyberNinja Theme

The GUI features a **cyberpunk aesthetic** with:
- **Cyan blue** accents (#00d4ff)
- **Dark background** (#0a0e27)
- **Glowing borders** and effects
- **Emojis** throughout the interface

---

## 📡 Connecting to Proxmark3

1. Launch the GUI
2. Select your COM port from dropdown (e.g., COM5)
3. Click **🔌 Connect**
4. Wait for connection confirmation
5. Start sending commands!

---

## 🐛 Troubleshooting

If you encounter issues:

1. **Check logs**: `logs/cyberninja_rfid.log`
2. **Verify ProxSpace**: Run `runme64.bat` manually first
3. **Test PM3**: Try `./proxmark3.exe COM5` in ProxSpace bash
4. **Update paths**: Check `pm3_proxspace.py` for correct paths

---

## 💡 Tips

- The GUI auto-detects ProxSpace installation
- Commands are executed through ProxSpace bash (correct method!)
- SWIG bindings are optional - subprocess fallback works great
- Future-proof design adapts to firmware updates automatically

---

**Enjoy your CyberNinja RFID hacking experience! 🔧💻🔐**
