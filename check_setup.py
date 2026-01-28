"""
Setup checker - verifies if everything is ready to run the bot.
Run this to see what still needs to be done.
"""
import sys
from pathlib import Path

print("=" * 60)
print("Desktop Automation Bot - Setup Checker")
print("=" * 60)
print()

# Check 1: Python version
print("[1/6] Checking Python version...")
python_version = sys.version_info
print(f"   Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version.major == 3 and python_version.minor >= 8:
    print("   [OK] Python version is compatible")
else:
    print("   [ERROR] Python 3.8+ required")
print()

# Check 2: Required packages
print("[2/6] Checking required packages...")
packages = {
    'cv2': 'opencv-python',
    'numpy': 'numpy',
    'PIL': 'pillow',
    'requests': 'requests',
    'pyautogui': 'pyautogui',
    'pygetwindow': 'pygetwindow'
}

missing_packages = []
for module, package in packages.items():
    try:
        __import__(module)
        print(f"   [OK] {package} installed")
    except ImportError:
        print(f"   [MISSING] {package} NOT installed")
        missing_packages.append(package)

if missing_packages:
    print(f"\n   Missing packages: {', '.join(missing_packages)}")
    print("   Install with: python -m pip install " + " ".join(missing_packages))
else:
    print("   [OK] All required packages installed")
print()

# Check 3: BotCity (optional)
print("[3/6] Checking BotCity framework (optional)...")
try:
    from botcity.core import DesktopBot
    print("   [OK] BotCity framework installed")
    using_botcity = True
except ImportError:
    print("   [WARN] BotCity not installed (will use pyautogui fallback)")
    using_botcity = False
print()

# Check 4: Notepad shortcut
print("[4/6] Checking for Notepad shortcut on desktop...")
desktop_path = Path.home() / "Desktop"
notepad_shortcuts = list(desktop_path.glob("Notepad*"))
if notepad_shortcuts:
    print(f"   [OK] Found: {notepad_shortcuts[0].name}")
else:
    print("   [MISSING] Notepad shortcut not found on desktop")
    print("   Create it: Right-click desktop -> New -> Shortcut -> notepad.exe")
print()

# Check 5: Project directory
print("[5/6] Checking project directories...")
project_dir = desktop_path / "tjm-project"
screenshot_dir = Path("screenshots")

if project_dir.exists():
    print(f"   [OK] Project directory exists: {project_dir}")
else:
    print(f"   [INFO] Project directory will be created: {project_dir}")

if screenshot_dir.exists():
    print(f"   [OK] Screenshot directory exists: {screenshot_dir}")
else:
    print(f"   [INFO] Screenshot directory will be created: {screenshot_dir}")
print()

# Check 6: Internet connectivity (for API)
print("[6/6] Checking internet connectivity (for API)...")
try:
    import requests
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)
    if response.status_code == 200:
        print("   [OK] Can reach JSONPlaceholder API")
    else:
        print("   [ERROR] API returned error status")
except ImportError:
    print("   [WARN] Cannot check (requests not installed)")
except Exception as e:
    print(f"   [ERROR] Cannot reach API: {e}")
print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)

all_ready = True
if missing_packages:
    print("❌ Missing packages - install them first")
    all_ready = False
if not notepad_shortcuts:
    print("❌ Notepad shortcut missing - create it on desktop")
    all_ready = False

if all_ready:
    print("[SUCCESS] Everything looks good! You can run the bot:")
    print()
    print("   python -m src.main")
    print()
    print("Or test icon detection first:")
    print("   python test_icon_detection.py")
else:
    print("[WARNING] Some setup steps are incomplete. See NEXT_STEPS.md for details.")
print("=" * 60)
