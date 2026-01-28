# Setup Instructions

## Prerequisites

1. **Windows 10/11** with 1920x1080 resolution (or configure in `src/config.py`)
2. **Python 3.8+** installed
3. **uv** package manager installed
4. **Notepad shortcut** on desktop (create before running)

## Step-by-Step Setup

### 1. Install uv (if not installed)

```powershell
# Using PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Or using pip
pip install uv
```

### 2. Clone/Navigate to Project

```powershell
cd C:\Users\Bishoy\desktop-automation-botcity
```

### 3. Create Virtual Environment and Install Dependencies

```powershell
# Create virtual environment
uv venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
uv sync
```

### 4. Create Notepad Shortcut on Desktop

1. Right-click on desktop
2. Select "New" → "Shortcut"
3. Enter: `notepad.exe`
4. Name it "Notepad"
5. Click "Finish"

### 5. Verify Setup

```powershell
# Test imports
python -c "import botcity; import cv2; import numpy; print('All dependencies installed!')"
```

### 6. Run the Bot

```powershell
# Using the run script
.\run.ps1

# Or directly
python -m src.main
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'botcity'"

**Solution:**
```powershell
uv sync
.\.venv\Scripts\Activate.ps1
```

### Issue: "Icon not found"

**Solutions:**
- Ensure Notepad shortcut exists on desktop
- Make sure desktop is visible (minimize other windows)
- Check screen resolution matches 1920x1080
- Try moving the icon to a different position

### Issue: "Notepad not launching"

**Solutions:**
- Verify the shortcut points to `notepad.exe`
- Check that Notepad is installed (usually in Windows by default)
- Ensure no other windows are blocking the icon

### Issue: "Permission denied" when saving files

**Solutions:**
- Check that `Desktop/tjm-project/` directory is writable
- Run PowerShell as Administrator if needed
- Check Windows file permissions

## Configuration

Edit `src/config.py` to customize:
- Screen resolution settings
- Retry attempts and delays
- Number of posts to process
- Output directory

## Next Steps

1. Test with icon in different positions
2. Verify files are saved correctly
3. Check screenshots in `screenshots/` directory
4. Review logs for any errors
