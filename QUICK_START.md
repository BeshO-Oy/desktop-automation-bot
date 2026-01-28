# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install uv (if needed)
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### 2. Setup Project
```powershell
cd desktop-automation-botcity
uv venv
.\.venv\Scripts\Activate.ps1
uv sync
```

### 3. Create Notepad Shortcut
- Right-click desktop → New → Shortcut
- Enter: `notepad.exe`
- Name: "Notepad"

### 4. Test Icon Detection (Optional)
```powershell
python test_icon_detection.py
```

### 5. Run the Bot
```powershell
.\run.ps1
```

## ✅ What to Expect

1. Bot captures desktop screenshot
2. Finds Notepad icon (regardless of position)
3. Launches Notepad
4. Fetches 10 blog posts from API
5. For each post:
   - Types content in Notepad
   - Saves as `post_{id}.txt` in `Desktop/tjm-project/`
   - Closes Notepad
   - Repeats for next post

## 📁 Output Files

- **Text files**: `Desktop/tjm-project/post_1.txt` through `post_10.txt`
- **Screenshots**: `screenshots/icon_detected_post_1.png` (first 3 posts)

## 🔧 Troubleshooting

**Icon not found?**
- Ensure Notepad shortcut is on desktop
- Make desktop visible (minimize windows)
- Try moving icon to different position

**Notepad not launching?**
- Verify shortcut points to `notepad.exe`
- Check icon is not blocked by other windows

**Files not saving?**
- Check `Desktop/tjm-project/` exists and is writable
- Verify Notepad has save permissions

## 📚 More Information

- Full documentation: `README.md`
- Setup details: `SETUP.md`
- Configuration: `src/config.py`
