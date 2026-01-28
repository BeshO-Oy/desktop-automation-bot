"""Configuration settings for the desktop automation project."""
import os
from pathlib import Path

# Desktop paths
DESKTOP_PATH = Path.home() / "Desktop"
PROJECT_DIR = DESKTOP_PATH / "tjm-project"

# API Configuration
API_BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_ENDPOINT = f"{API_BASE_URL}/posts"
MAX_POSTS = 10

# Icon Detection Configuration
ICON_SEARCH_REGION = None  # None means full screen
ICON_CONFIDENCE = 0.7  # Minimum confidence for icon detection
ICON_RETRY_ATTEMPTS = 3
ICON_RETRY_DELAY = 1.0  # seconds

# Notepad Configuration
NOTEPAD_WINDOW_TITLE = "Notepad"
NOTEPAD_LAUNCH_TIMEOUT = 5.0  # seconds
NOTEPAD_CLOSE_DELAY = 0.5  # seconds

# Screenshot Configuration
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

# Icon Template Configuration
ICON_TEMPLATE_DIR = Path("resources") / "icons"
ICON_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
NOTEPAD_ICON_TEMPLATE = ICON_TEMPLATE_DIR / "notepad_icon.png"

# File Format
FILE_FORMAT = "Title: {title}\n\n{body}"

# Create project directory if it doesn't exist
PROJECT_DIR.mkdir(parents=True, exist_ok=True)
