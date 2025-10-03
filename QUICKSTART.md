# 🚀 CyberNinjaRFID - Quick Start Guide

## ⚡ 3-Step Setup

### Step 1: Install Dependencies 📦

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
pip3 install -r requirements.txt
```

### Step 2: Launch the GUI 🔥

**Windows:**
- Double-click `run_cyberninja_rfid.bat`

**Linux/macOS:**
```bash
chmod +x run_cyberninja_rfid.sh
./run_cyberninja_rfid.sh
```

### Step 3: Connect to PM3 🔌

1. **Scan**: Click "🔍 Scan Devices" button
2. **Select**: Choose your PM3 from dropdown
3. **Connect**: Click "🔌 Connect" button
4. **Status**: Look for 🟢 "Connected" status

## 🎯 First Commands

### Test Connection
```
hw version
hw status
```

### Scan for Tags
**HF (High Frequency):**
```
hf search
```

**LF (Low Frequency):**
```
lf search
```

### Read a Card
**HF Card:**
```
hf 14a reader
hf 14a info
```

**LF Card:**
```
lf em 410x reader
```

## 💡 Pro Tips

1. **Quick Commands**: Use the preset buttons for instant execution
2. **Tabs**: Switch tabs for specialized tools (HF/LF/Scripts)
3. **History**: Press ↑ to recall previous commands
4. **Clear**: Use "🗑️ Clear Output" when console gets full
5. **Logs**: Check `logs/cyberninja_rfid.log` for debug info

## 🔧 Troubleshooting

### Can't find PM3?
- Check USB connection
- Install drivers (Windows)
- Add user to dialout group (Linux): `sudo usermod -a -G dialout $USER`

### PyQt5 error?
```bash
pip install PyQt5
```

### Permission denied (Linux)?
```bash
sudo chmod 666 /dev/ttyACM0
```

## 🎮 Example Session

```
1. Launch CyberNinjaRFID
2. Scan for devices → Found: /dev/ttyACM0
3. Connect → 🟢 Connected
4. Click "🔍 HF Search" → Found: MIFARE Classic 1K
5. Click "💳 HF 14a Reader" → Read tag data
6. Success! 🎉
```

## 📚 Learn More

- **Full Documentation**: See `README_CyberNinjaRFID.md`
- **Features List**: See `FEATURES.md`
- **PM3 Commands**: [Proxmark3 Command Guide](https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/commands.md)

---

**🔥 Hack The Planet! 💀**
