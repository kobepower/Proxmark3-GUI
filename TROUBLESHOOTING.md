# 🔧 CyberNinjaRFID - Troubleshooting Guide

## ❌ Common Issues & Solutions

### 1. "PM3 Python module not available"

**Problem**: SWIG Python bindings not compiled

**Solutions**:

#### Option A: Use Subprocess Fallback (Automatic)
The GUI automatically falls back to subprocess mode if SWIG bindings aren't available.
This should work out of the box!

#### Option B: Compile SWIG Bindings
```bash
cd ../proxmark3
make clean
make client PLATFORM=PM3GENERIC PYTHON3=python3
```

---

### 2. "No devices found" / COM5 not showing up

**Problem**: Device scanner not finding your PM3

**Solutions**:

#### Solution 1: Click "Scan Devices" Again
Sometimes ports aren't detected on first scan. Click the button 2-3 times.

#### Solution 2: Check USB Connection
- Unplug PM3
- Wait 5 seconds
- Plug back in
- Click "Scan Devices"

#### Solution 3: Manual Port Entry
The GUI now shows ALL serial ports. If COM5 isn't there:
1. Open Device Manager (Windows)
2. Find "Ports (COM & LPT)"
3. Look for your PM3 device
4. Note the COM port number
5. Select it manually from dropdown

#### Solution 4: Driver Issues (Windows)
- Install Zadig drivers
- Or use ProxSpace drivers
- Reboot after installation

---

### 3. "PM3 client executable not found"

**Problem**: `proxmark3.exe` not in expected location

**Solutions**:

#### Solution 1: Standard ProxSpace Setup
If using ProxSpace, the GUI auto-detects:
- `C:/ProxSpace/pm3/proxmark3/client/proxmark3.exe`
- `D:/ProxSpace/pm3/proxmark3/client/proxmark3.exe`

#### Solution 2: Custom Location
Edit `config.json`:
```json
{
  "paths": {
    "pm3_client": "C:/Your/Custom/Path/proxmark3.exe"
  }
}
```

#### Solution 3: Compile PM3 First
```bash
cd ../proxmark3
make clean
make client PLATFORM=PM3GENERIC
```

The executable will be at: `proxmark3/client/proxmark3.exe`

---

### 4. "Connection failed" / "Timeout"

**Problem**: Can't connect to PM3 on selected port

**Solutions**:

#### Solution 1: Check Port is Correct
- COM3, COM5, etc. must match Device Manager
- On Linux: `/dev/ttyACM0` or `/dev/ttyUSB0`

#### Solution 2: Close Other Programs
- Close Proxmark3 official client
- Close any terminal using PM3
- Only ONE program can use COM port at a time

#### Solution 3: Unplug/Replug PM3
Sometimes PM3 gets "stuck":
1. Disconnect from GUI (if connected)
2. Unplug USB cable
3. Wait 5 seconds
4. Plug back in
5. Try connecting again

#### Solution 4: Check Permissions (Linux)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# OR give permissions to specific port
sudo chmod 666 /dev/ttyACM0

# Then logout and login again
```

---

### 5. "PyQt5 not installed"

**Problem**: Missing GUI framework

**Solution**:
```bash
pip install PyQt5
```

Or on Linux:
```bash
sudo apt install python3-pyqt5
```

---

### 6. "pyserial not installed"

**Problem**: Missing serial communication library

**Solution**:
```bash
pip install pyserial
```

---

### 7. GUI doesn't start / crashes immediately

**Problem**: Missing dependencies or Python version

**Solutions**:

#### Solution 1: Check Python Version
```bash
python3 --version
```
Must be 3.7 or higher!

#### Solution 2: Run Setup Checker
```bash
python3 check_setup.py
```
This will tell you what's missing.

#### Solution 3: Install All Dependencies
```bash
pip install -r requirements.txt
```

---

### 8. Commands not working / "Command failed"

**Problem**: PM3 firmware incompatibility

**Solutions**:

#### Solution 1: Update Iceman Firmware
```bash
cd ../proxmark3
git pull
make clean
make all
pm3-flash-all
```

#### Solution 2: Check Command Syntax
The GUI auto-translates old commands, but if it fails:
- Check Proxmark3 docs
- Try command in official PM3 client first
- Report bug if command should work

#### Solution 3: Clear Command Cache
Delete the cache file:
```bash
rm logs/pm3_commands_cache.json
```
Then reconnect to PM3.

---

### 9. Slow performance / lag

**Problem**: GUI responding slowly

**Solutions**:

#### Solution 1: Clear Output
Click "🗑️ Clear Output" button to remove old text.

#### Solution 2: Reduce Output Lines
Edit `config.json`:
```json
{
  "ui": {
    "max_output_lines": 500
  }
}
```

#### Solution 3: Disable Command Discovery
If you don't need auto-discovery:
Edit `CyberNinjaRFID.py` and comment out discovery code.

---

### 10. Firmware version not detected

**Problem**: "unknown firmware"

**Solution**:
This is usually harmless. The GUI will still work, just without some optimizations.

To fix:
1. Ensure PM3 firmware is up to date
2. Run `hw version` manually
3. Check if output contains version number

---

## 🆘 Still Having Issues?

### Debug Mode

Enable verbose logging:

1. Edit `config.json`:
```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

2. Check logs:
```bash
cat logs/cyberninja_rfid.log
```

### Report a Bug

If none of these solutions work:

1. **Gather Info**:
   - Python version: `python3 --version`
   - OS: Windows/Linux/macOS version
   - PM3 firmware version
   - Error message from GUI
   - Contents of `logs/cyberninja_rfid.log`

2. **Test Basic PM3**:
   ```bash
   # Does the official client work?
   ../proxmark3/client/proxmark3.exe -p COM5
   ```

3. **Create Issue** with all the above info

---

## 💡 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| No PM3 module | ✅ Automatic fallback to subprocess |
| No devices found | 🔄 Click "Scan" again, check USB |
| Can't find proxmark3.exe | 📝 Edit `config.json` with correct path |
| Connection timeout | 🔌 Close other programs, replug PM3 |
| PyQt5 missing | 📦 `pip install PyQt5` |
| Permission denied | 🔓 `sudo chmod 666 /dev/ttyACM0` |
| Slow GUI | 🗑️ Clear output, reduce max lines |

---

## 🔍 Testing Your Setup

Run this checklist:

```bash
# 1. Check Python
python3 --version
# Should be 3.7+

# 2. Check dependencies
python3 check_setup.py
# Should show all ✅

# 3. Test PM3 client directly
../proxmark3/client/proxmark3.exe -p COM5
# Should connect (if not, GUI won't work either)

# 4. Launch GUI
./run_cyberninja_rfid.sh
# Should open window

# 5. Scan devices
# Click "🔍 Scan Devices"
# Should see your COM port

# 6. Connect
# Select COM port, click "🔌 Connect"
# Should see 🟢 Connected
```

If ANY step fails, that's where the problem is!

---

## 📞 Support Checklist

Before asking for help, please try:

- [ ] Run `python3 check_setup.py`
- [ ] Test PM3 with official client
- [ ] Check `logs/cyberninja_rfid.log`
- [ ] Try solutions in this guide
- [ ] Gather system info (Python version, OS, etc.)

---

**🔥 Most issues are solved by:**
1. Installing dependencies: `pip install -r requirements.txt`
2. Rescanning devices: Click "🔍 Scan" again
3. Closing other PM3 programs
4. Checking the correct COM port

**Good luck! 🥷**
