# Vision-Based Desktop Automation with Dynamic Icon Grounding

A Python application using BotCity framework that uses computer vision to dynamically locate and interact with desktop icons on Windows. The system can find the Notepad icon regardless of its position on the desktop, enabling robust automation even when icon positions change.

## Features

- **Dynamic Icon Detection**: Locates desktop icons without hardcoded positions using computer vision
- **Flexible Grounding System**: Works for any icon or button without requiring exact templates
- **Robust Error Handling**: Retry logic, timeout handling, and graceful degradation
- **API Integration**: Fetches blog posts from JSONPlaceholder API
- **Automated Workflow**: Automates Notepad to save posts as text files

## Requirements

- Windows 10/11
- Screen resolution: 1920x1080 (configurable)
- Python 3.8+
- uv package manager
- Notepad shortcut icon on desktop (create before running)

## Installation

### Option 1: Using uv (Recommended)

#### 1. Install uv (if not already installed)

```powershell
# Using PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Or download from: https://github.com/astral-sh/uv
```

#### 2. Install Dependencies

```powershell
cd desktop-automation-botcity
uv venv
.\.venv\Scripts\Activate.ps1
uv sync
```

### Option 2: Using pip (Alternative)

If you don't have `uv` installed, you can use standard Python tools:

```powershell
cd desktop-automation-botcity

# Run the setup script
.\setup_with_pip.ps1

# Or manually:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Usage

### Basic Usage

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the bot
python -m src.main
```

### Using the Run Script

```powershell
.\run.ps1
```

## Project Structure

```
desktop-automation-botcity/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main bot entry point
│   ├── config.py            # Configuration settings
│   ├── icon_grounding.py    # Icon detection system
│   ├── notepad_automation.py # Notepad automation
│   └── api_client.py         # API client for posts
├── screenshots/              # Annotated screenshots (auto-created)
├── pyproject.toml           # Project dependencies
├── README.md                # This file
└── run.ps1                  # Run script
```

## How It Works

### Icon Grounding System

The icon grounding system uses multiple detection strategies:

1. **Visual Feature Detection**: Detects icon-like regions using computer vision
2. **Grid Pattern Detection**: Leverages the regular grid layout of desktop icons
3. **Shape Analysis**: Identifies rectangular/square regions typical of icons
4. **Blob Detection**: Uses OpenCV blob detection to find icon-sized regions

The system is designed to be flexible and work without requiring exact template images, making it robust to:
- Different icon positions
- Various Windows themes (light/dark)
- Different icon sizes
- Custom desktop backgrounds

### Automation Workflow

1. **Capture Screenshot**: Takes a screenshot of the desktop
2. **Locate Icon**: Uses computer vision to find the Notepad icon
3. **Launch Notepad**: Double-clicks the icon to launch Notepad
4. **Fetch Posts**: Retrieves blog posts from JSONPlaceholder API
5. **Process Posts**: For each post:
   - Types the post content in Notepad
   - Saves the file as `post_{id}.txt` in `Desktop/tjm-project/`
   - Closes Notepad
   - Repeats for the next post

## Configuration

Edit `src/config.py` to customize:

- `MAX_POSTS`: Number of posts to process (default: 10)
- `ICON_RETRY_ATTEMPTS`: Number of retry attempts for icon detection (default: 3)
- `ICON_RETRY_DELAY`: Delay between retries in seconds (default: 1.0)
- `PROJECT_DIR`: Directory to save files (default: `Desktop/tjm-project`)

## Error Handling

The bot includes comprehensive error handling:

- **Icon Not Found**: Retries up to 3 times with 1-second delays
- **Notepad Launch Failure**: Validates window title and uses timeout
- **API Unavailable**: Gracefully degrades and continues with empty post list
- **File Conflicts**: Handles existing files in target directory
- **Multiple Icons**: Selects the most prominent icon candidate

## Screenshots

The bot automatically saves annotated screenshots showing detected icons:
- `screenshots/icon_detected_post_1.png`
- `screenshots/icon_detected_post_2.png`
- `screenshots/icon_detected_post_3.png`

These screenshots show:
- Green circle marking the detected icon position
- Coordinates of the icon
- Label indicating which post was being processed

## Testing

### Manual Testing

1. Create a Notepad shortcut on your desktop
2. Move the icon to different positions (top-left, center, bottom-right)
3. Run the bot and verify it correctly locates and clicks the icon
4. Check that files are saved in `Desktop/tjm-project/`

### Test Scenarios

- **Icon in top-left area**: Bot should detect and click
- **Icon in bottom-right area**: Bot should detect and click
- **Icon in center**: Bot should detect and click
- **Icon partially obscured**: Bot should still attempt detection
- **Multiple similar icons**: Bot should select the most prominent one

## Troubleshooting

### Icon Not Found

- Ensure Notepad shortcut exists on desktop
- Check that desktop is visible (not covered by windows)
- Verify screen resolution is 1920x1080
- Try increasing `ICON_RETRY_ATTEMPTS` in config

### Notepad Not Launching

- Verify the icon is actually a Notepad shortcut
- Check that Notepad is installed
- Ensure no other windows are blocking the icon

### Files Not Saving

- Check that `Desktop/tjm-project/` directory exists and is writable
- Verify Notepad has permission to save files
- Check for file name conflicts

## Discussion Topics

### Icon Detection Approach

**Why this method?**
- **Flexibility**: Works without requiring exact template images
- **Robustness**: Multiple detection strategies provide fallbacks
- **Scalability**: Can be extended to detect any desktop icon
- **Performance**: Fast enough for real-time automation

**Alternatives considered:**
- Template matching: Requires exact images, less flexible
- OCR-based: More accurate but slower and requires text labels
- Windows API: Faster but less portable and requires specific Windows versions

### Failure Cases

The detection may fail when:
- Icon is completely obscured by windows
- Desktop background is extremely busy/noisy
- Icon size is significantly different from expected
- Multiple identical icons exist (may select wrong one)

**Improvements:**
- Use OCR to verify icon labels
- Implement machine learning-based detection
- Add support for different icon sizes
- Use Windows API as fallback

### Performance

- **Icon Detection**: ~0.5-2 seconds per detection
- **Optimization Strategies**:
  - Cache screenshots when possible
  - Use multi-threading for parallel detection
  - Implement region-of-interest (ROI) search
  - Use GPU acceleration for image processing

### Robustness

**Handles:**
- ✅ Different Windows themes (light/dark) - uses grayscale processing
- ✅ Different icon view sizes - adaptive size detection
- ✅ Custom backgrounds - multiple detection strategies
- ✅ Multiple similar icons - selects most prominent
- ✅ Icons with similar names - can be extended with OCR

### Scaling

**To detect any arbitrary desktop icon:**
- Add icon name/label parameter
- Implement OCR for label verification
- Use icon hash/fingerprint matching

**To work on different resolutions:**
- Scale detection parameters based on resolution
- Use relative coordinates instead of absolute
- Implement resolution detection and adaptation

## License

This project is created for a take-home assignment.

## Author

Created using BotCity framework for desktop automation.
