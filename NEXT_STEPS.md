# Next Steps - Getting Your Project Running

## Step-by-Step Guide

### Step 1: Fix Pip Installation Issue

You need to resolve the pip package installation problem first. Try these in order:

#### Option A: Try Different Python Version (Recommended)

Python 3.14.2 is very new and may have compatibility issues. Try using Python 3.11 or 3.12:

```powershell
# Check what Python versions you have
py --list

# If you have Python 3.11 or 3.12, use it:
cd C:\Users\Bishoy\desktop-automation-botcity

# Remove old venv
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# Create new venv with Python 3.11 (or 3.12)
py -3.11 -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Try installing packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### Option B: Check Network/Proxy Settings

```powershell
# Test if you can reach PyPI
python -m pip install --dry-run requests

# If behind proxy, configure it:
# python -m pip config set global.proxy http://your-proxy:port
```

#### Option C: Install Packages One by One

```powershell
cd C:\Users\Bishoy\desktop-automation-botcity
.\.venv\Scripts\Activate.ps1

python -m pip install requests
python -m pip install numpy
python -m pip install pillow
python -m pip install opencv-python
python -m pip install pyautogui
python -m pip install pygetwindow
```

### Step 2: Verify Installation

Once packages are installed, verify everything works:

```powershell
# Test imports
python -c "import cv2; import numpy; import requests; import pyautogui; print('✓ All packages installed successfully!')"
```

If this works, you're ready to proceed!

### Step 3: Create Notepad Shortcut on Desktop

Before running the bot, create a Notepad shortcut:

1. Right-click on your desktop
2. Select **New** → **Shortcut**
3. In the location field, type: `notepad.exe`
4. Click **Next**
5. Name it: **Notepad**
6. Click **Finish**

**Important:** Make sure this shortcut is visible on your desktop before running the bot.

### Step 4: Test Icon Detection (Optional but Recommended)

Test if the icon detection works:

```powershell
cd C:\Users\Bishoy\desktop-automation-botcity
.\.venv\Scripts\Activate.ps1

python test_icon_detection.py
```

This will:
- Capture a screenshot
- Try to find the Notepad icon
- Save an annotated screenshot showing where it detected the icon

If this works, the main bot should work too!

### Step 5: Run the Full Automation

Once everything is set up:

```powershell
cd C:\Users\Bishoy\desktop-automation-botcity
.\.venv\Scripts\Activate.ps1

# Run the bot
python -m src.main
```

Or use the run script:
```powershell
.\run_direct.ps1
```

### Step 6: What to Expect

The bot will:

1. ✅ Capture desktop screenshot
2. ✅ Find Notepad icon (regardless of position)
3. ✅ Launch Notepad by double-clicking the icon
4. ✅ Fetch 10 blog posts from JSONPlaceholder API
5. ✅ For each post:
   - Type the post content in Notepad
   - Save as `post_{id}.txt` in `Desktop/tjm-project/`
   - Close Notepad
   - Repeat for next post

### Step 7: Check Results

After the bot completes:

1. **Check files**: Look in `Desktop/tjm-project/` for `post_1.txt` through `post_10.txt`
2. **Check screenshots**: Look in `screenshots/` folder for annotated screenshots
3. **Review console output**: Check for any errors or warnings

## Troubleshooting

### If Icon Not Found

- Ensure Notepad shortcut exists on desktop
- Make sure desktop is visible (minimize other windows)
- Try moving the icon to a different position
- Check screen resolution is 1920x1080 (or update in `src/config.py`)

### If Notepad Doesn't Launch

- Verify shortcut points to `notepad.exe`
- Check that Notepad is installed (usually comes with Windows)
- Ensure no other windows are blocking the icon

### If Files Don't Save

- Check `Desktop/tjm-project/` directory exists and is writable
- Verify Notepad has permission to save files
- Check for file name conflicts

## Quick Reference Commands

```powershell
# Navigate to project
cd C:\Users\Bishoy\desktop-automation-botcity

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (if not done)
python -m pip install -r requirements.txt

# Test icon detection
python test_icon_detection.py

# Run the bot
python -m src.main
```

## Need Help?

- Check `README.md` for full documentation
- See `PIP_TROUBLESHOOTING.md` for pip issues
- Review `INSTALLATION_STATUS.md` for current status
- Check `GROUNDING_APPROACH.md` for technical details

## Success Indicators

You'll know everything is working when:

✅ Packages install without errors
✅ `test_icon_detection.py` finds the icon
✅ Bot runs and processes all 10 posts
✅ Files appear in `Desktop/tjm-project/`
✅ Screenshots are saved in `screenshots/`

Good luck! 🚀
