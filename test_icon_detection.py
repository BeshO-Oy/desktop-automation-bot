"""
Test script for icon detection.
Use this to test icon detection before running the full automation.
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from botcity.core import DesktopBot
    BOTCITY_AVAILABLE = True
except ImportError:
    # Use compatible wrapper if BotCity is not available
    from src.botcity_compat import DesktopBot
    BOTCITY_AVAILABLE = False
    print("Note: Using BotCity compatibility layer (BotCity not installed)")

from src.icon_grounding import IconGrounding
from src import config

def test_icon_detection():
    """Test icon detection functionality."""
    print("=" * 60)
    print("Icon Detection Test")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Capture a screenshot of your desktop")
    print("2. Attempt to find the Notepad icon")
    print("3. Save an annotated screenshot showing the detection")
    print("\nMake sure:")
    print("- Notepad shortcut exists on desktop")
    print("- Desktop is visible (minimize other windows)")
    print("- Screen resolution is 1920x1080")
    print("\n" + "=" * 60)
    
    # Auto-start after 2 seconds (or press Enter to start immediately)
    import time
    print("\nStarting in 2 seconds... (press Ctrl+C to cancel)")
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        return
    
    try:
        # Initialize bot
        bot = DesktopBot()
        bot.headless = False
        
        # Initialize icon grounding
        icon_grounding = IconGrounding(bot)
        
        # Capture screenshot
        print("\n[1/3] Capturing desktop screenshot...")
        screenshot = icon_grounding.capture_desktop_screenshot()
        print(f"✓ Screenshot captured: {screenshot.shape}")
        
        # Find icon
        print("\n[2/3] Searching for Notepad icon...")
        icon_position = icon_grounding.find_notepad_icon(
            retry_attempts=3,
            retry_delay=1.0
        )
        
        if icon_position:
            x, y = icon_position
            print(f"✓ Icon found at: ({x}, {y})")
            
            # Save annotated screenshot
            print("\n[3/3] Saving annotated screenshot...")
            output_path = config.SCREENSHOT_DIR / "test_icon_detection.png"
            icon_grounding.save_annotated_screenshot(
                icon_position,
                str(output_path),
                label="Test - Icon Detected"
            )
            print(f"✓ Screenshot saved to: {output_path}")
            print("\n" + "=" * 60)
            print("SUCCESS: Icon detection working correctly!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("FAILED: Could not detect icon")
            print("=" * 60)
            print("\nTroubleshooting:")
            print("- Ensure Notepad shortcut exists on desktop")
            print("- Make sure desktop is visible")
            print("- Try moving the icon to a different position")
            print("- Check screen resolution")
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_icon_detection()
