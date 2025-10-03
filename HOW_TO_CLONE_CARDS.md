# 🔥 How to Clone RFID Cards - CyberNinjaRFID Guide

## 🎯 Quick Start: 3-Step Clone Process

### Step 1: Identify the Card Type
1. Place the original card/fob on the Proxmark3 antenna
2. Click **🔍 LF Search** or **🔍 HF Search** (try LF first for most access cards)
3. Read the output to identify card type

### Step 2: Read the Card Data
Based on the type found:
- **EM410x** → Click **🎫 EM410x Reader**
- **HID Prox** → Click **🏢 HID Reader**
- **Indala** → Click **🎟️ Indala Reader**
- **MIFARE** → Click **💳 ISO14443-A Reader**

### Step 3: Clone to Blank Card
1. Place a blank T55xx card on the antenna
2. Click the appropriate clone button
3. Verify with **🔍 Search** again

---

## 📚 Detailed Cloning Guides

### 🎫 Cloning EM410x Cards (Most Common)

**What it is:** Most common 125kHz proximity cards used in buildings, gyms, parking garages.

**Steps:**
1. **Read Original:**
   - Place original on antenna
   - Click **🔍 LF Search**
   - Should see: `[+] EM410x ID found`

2. **Clone:**
   - Place blank T55xx on antenna
   - Click **🎫 EM410x Clone**
   - Wait for confirmation

3. **Verify:**
   - Click **🔍 LF Search** again
   - Should match original ID

**Commands used:**
```
lf search
lf em 410x reader
lf em 410x clone --to t55xx
```

---

### 🏢 Cloning HID Prox Cards

**What it is:** Common corporate access cards (gray/white cards with HID logo).

**Steps:**
1. **Read Original:**
   - Place original on antenna
   - Click **🏢 HID Reader**
   - Note the **Facility Code (FC)** and **Card Number (CN)**

2. **Clone:**
   - Place blank T55xx on antenna
   - Click **🏢 HID Clone**
   - Enter Facility Code when prompted
   - Enter Card Number when prompted

3. **Verify:**
   - Click **🏢 HID Reader**
   - Verify FC and CN match

**Commands used:**
```
lf hid reader
lf hid clone --fc <facility> --cn <cardnum>
lf hid reader
```

---

### 🎟️ Cloning Indala Cards (Multi-Method)

**What it is:** Less common 125kHz cards, requires multiple clone methods.

**Method 1 - Raw Clone (Try First):**
1. **Read:**
   - Click **🎟️ Indala Reader**
   - Copy the **RAW HEX** value shown

2. **Wipe Blank:**
   - Place blank T55xx on antenna
   - Click **🔓 T55xx Wipe**

3. **Clone:**
   - Click **📋 Indala (Raw)**
   - Paste RAW HEX value
   - Click OK

4. **Verify:**
   - Click **🔍 LF Search**

**If Method 1 fails, try Method 2 - FC/CN:**
1. Click **🔓 T55xx Wipe**
2. Click **🔢 Indala (FC/CN)**
3. Enter Facility Code and Card Number
4. Verify with **🔍 LF Search**

**If Method 2 fails, try Method 3 - HEDEN:**
1. Click **🔓 T55xx Wipe**
2. Click **🔤 Indala (HEDEN)**
3. Enter the printed ID from the card
4. Verify with **🔍 LF Search**

**Important:** After Indala clone, you may need to click **⚙️ T55xx Config Block** to finalize.

**Commands used:**
```
lf indala reader
lf t55xx wipe
lf indala clone -r <rawhex>
# OR
lf indala clone --fc <fc> --cn <cn>
# OR
lf indala clone --heden <printedID>
lf t55xx write --blk 1 --data 000880E0
```

---

### 💳 Cloning MIFARE Classic Cards (HF - 13.56MHz)

**What it is:** White cards used for public transit, hotels, some buildings.

**Steps:**
1. **Read:**
   - Place original on antenna
   - Click **🤖 MIFARE Autopwn**
   - Wait for keys to be found (can take 5-30 seconds)

2. **Dump Data:**
   - Click **📖 Dump Card**
   - Data saved to file

3. **Clone:**
   - Place blank MIFARE card on antenna
   - Use PM3 client to write dump to card
   - (Advanced users only - requires hex editing)

**Commands used:**
```
hf 14a reader
hf mf autopwn
hf mf dump
```

---

## 🛠️ Button Reference Guide

### 📡 LF Tab - Tag Scanning Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **🔍 LF Search** | Auto-detects LF card type | First step for any 125kHz card |
| **📊 LF Tune** | Shows antenna tuning graph | Check if antenna is working |
| **📈 LF Sniff** | Records RF traffic | Advanced: analyze card-reader communication |

### 📇 LF Tab - Tag Readers Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **🎫 EM410x Reader** | Reads EM410x card ID | After LF Search finds EM410x |
| **🏢 HID Reader** | Reads HID Prox FC/CN | After LF Search finds HID |
| **🎟️ Indala Reader** | Reads Indala card data | After LF Search finds Indala |
| **🔑 T55xx Detect** | Detects T55xx chip type | Check if blank card is T55xx |
| **📖 T55xx Read Blocks** | Reads all 8 blocks (0-7) | View complete T55xx memory |

### 🧾 LF Tab - Tag Writers Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **✍️ EM410x Write** | Writes custom EM410x ID | Manual programming |
| **✏️ T55xx Write** | Writes to specific block | Advanced T55xx programming |
| **🔓 T55xx Wipe** | Erases T55xx card | Before cloning, or to reuse blank |
| **⚙️ T55xx Config Block** | Sets block 1 config | After Indala clone |

### 📤 LF Tab - Clone Tools Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **🎫 EM410x Clone** | Clones last-read EM410x | Quick EM410x cloning |
| **🏢 HID Clone** | Clones HID with FC/CN | After reading HID card |
| **📋 Indala (Raw)** | Clones Indala via RAW hex | Indala Method 1 |
| **🔢 Indala (FC/CN)** | Clones Indala via FC/CN | Indala Method 2 |
| **🔤 Indala (HEDEN)** | Clones Indala via printed ID | Indala Method 3 |

### 💾 LF Tab - Dump & Restore Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **💾 T55xx Dump** | Saves T55xx to file | Backup before experimenting |
| **📥 T55xx Restore** | Restores T55xx from file | Restore backup |
| **🎭 LF Simulate** | Emulates card from file | Test without writing to card |

### 📝 LF Tab - Trace Analysis Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **📝 List EM** | Shows captured EM410x data | After sniffing EM traffic |
| **📝 List HID** | Shows captured HID data | After sniffing HID traffic |

---

### 📡 HF Tab - Tag Scanning Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **🔍 HF Search** | Auto-detects HF card type | First step for any 13.56MHz card |
| **📊 HF Tune** | Shows HF antenna tuning | Check if HF antenna working |
| **🎯 HF Sniff** | Records HF RF traffic | Advanced analysis |

### 📇 HF Tab - Tag Readers Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **💳 ISO14443-A Reader** | Reads ISO14443-A cards | Most 13.56MHz cards |
| **🎴 ISO14443-A Info** | Shows detailed card info | Get UID, ATQA, SAK |
| **🔎 iClass Reader** | Reads iClass cards | Corporate high-security cards |
| **💎 Legic Reader** | Reads Legic cards | European ski passes, transit |

### 🔐 HF Tab - MIFARE Tools Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **🤖 MIFARE Autopwn** | Auto-attacks MIFARE card | One-click MIFARE key recovery |
| **🗝️ Check Keys** | Tests known keys | Find valid authentication keys |
| **📖 Dump Card** | Dumps MIFARE to file | After autopwn succeeds |
| **🔓 Nested Attack** | Advanced key recovery | When autopwn fails |

### 📝 HF Tab - Trace Analysis Section

| Button | What It Does | When To Use |
|--------|--------------|-------------|
| **📝 HF List (ISO14443a)** | Shows captured ISO14443-A traffic | After sniffing HF communication |

---

## ⌨️ Command Input Boxes

Both HF and LF tabs have command input boxes at the top right.

**How to use:**
1. Type any Proxmark3 command
2. Press **Enter** or click **▶️ Execute**
3. View output in console below

**Examples:**
```
lf search
hf 14a reader
lf em 410x reader
hf mf autopwn
lf t55xx read --blk 0
```

---

## 💡 Pro Tips

### ✅ Always Verify
After every clone, run **Search** again to confirm it worked.

### ✅ Backup First
Before experimenting, click **💾 T55xx Dump** to save original data.

### ✅ Wipe Before Indala
Indala clones work best when you **🔓 T55xx Wipe** first.

### ✅ Read the Output
The colorized console shows:
- 🟢 **Green** = Success
- 🔴 **Red** = Error
- 🟡 **Yellow** = Warning
- 🔵 **Cyan** = Data/Info

### ✅ Try LF First
Most building access cards are LF (125kHz). Try **LF Search** before HF.

### ✅ Use Autopwn for MIFARE
Don't manually try keys - **🤖 MIFARE Autopwn** does it all automatically.

---

## 🚨 Troubleshooting

### "No tag found"
- Check card placement on antenna
- Try rotating card 90 degrees
- Ensure PM3 is connected (green status indicator)

### "Clone failed"
- Ensure blank card is T55xx type
- Try **🔓 T55xx Wipe** first
- For Indala: try all 3 clone methods

### "Autopwn failed"
- Card may have custom keys
- Try **🔓 Nested Attack** instead
- Some cards are encrypted and can't be cloned

### "Command returns 0 chars"
- PM3 may be disconnected
- Click **🔌 Connect** again
- Check logs at bottom of window

---

## 🎓 Learning Resources

### Beginner Path:
1. Start with **EM410x cards** (easiest)
2. Try **HID Prox** (medium)
3. Attempt **MIFARE** (advanced)

### Practice Cards:
- Buy variety pack of blank T55xx cards
- Get EM410x test cards
- Practice cloning before attempting real cards

### Advanced Topics:
- Custom key dictionaries for MIFARE
- Analyzing sniffed traffic
- Writing custom lua scripts

---

## ⚖️ Legal Disclaimer

**Important:** Only clone cards you own or have explicit permission to clone. Unauthorized cloning of access cards may be illegal in your jurisdiction. This tool is for:
- ✅ Security research
- ✅ Personal backups
- ✅ Educational purposes
- ✅ Authorized penetration testing

**Do NOT use for:**
- ❌ Unauthorized access
- ❌ Fraud
- ❌ Illegal entry

---

## 🎉 You're Ready!

Now you know how to use every button in CyberNinjaRFID. Start with simple EM410x clones and work your way up to advanced MIFARE attacks.

**Happy (legal) hacking! 🔥**

---

*CyberNinjaRFID v1.0.0 - Built for the Proxmark3 Community*
