# Pip Installation Troubleshooting

## Current Issue
Pip cannot find packages from PyPI. This could be due to:
1. Network/proxy issues
2. Python 3.14.2 compatibility (very new version)
3. Pip configuration problems

## Solutions

### Solution 1: Check Network Connectivity

```powershell
# Test PyPI connectivity
python -m pip install --dry-run requests

# Check pip configuration
python -m pip config list
```

### Solution 2: Use System Python (if available)

If you have another Python version installed:

```powershell
# Check available Python versions
py --list

# Use Python 3.11 or 3.12 (more compatible)
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Solution 3: Configure Proxy (if behind firewall)

```powershell
# Set proxy if needed
python -m pip config set global.proxy http://proxy.example.com:8080

# Or use environment variable
$env:HTTP_PROXY = "http://proxy.example.com:8080"
$env:HTTPS_PROXY = "http://proxy.example.com:8080"
```

### Solution 4: Use Alternative Index

```powershell
python -m pip install -i https://pypi.org/simple/ -r requirements.txt
```

### Solution 5: Install Packages One by One

```powershell
python -m pip install requests
python -m pip install numpy
python -m pip install pillow
python -m pip install opencv-python
python -m pip install pyautogui
python -m pip install pygetwindow
```

### Solution 6: Use Conda/Miniconda (Alternative)

If pip continues to fail, consider using Conda:

```powershell
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
# Then:
conda create -n desktop-automation python=3.11
conda activate desktop-automation
conda install -c conda-forge opencv numpy pillow requests
pip install pyautogui pygetwindow
```

## Verify Installation

After installing, verify:

```powershell
python -c "import requests; import cv2; import numpy; import pyautogui; print('All packages installed!')"
```

## Current Status

The code has been updated to work with or without BotCity:
- If BotCity is available: Uses BotCity framework
- If BotCity is not available: Uses pyautogui fallback (botcity_compat.py)

You can run the bot once the core packages (opencv, numpy, pillow, requests, pyautogui) are installed.
