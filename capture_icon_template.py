"""
Helper script to capture Notepad icon for template matching.
This will help improve icon detection accuracy.
"""
import pyautogui
from pathlib import Path
import time

def capture_notepad_icon():
    """Interactive script to capture Notepad icon."""
    print("=" * 60)
    print("Notepad Icon Template Capture")
    print("=" * 60)
    print()
    print("This script will help you capture the Notepad icon for better detection.")
    print()
    print("Instructions:")
    print("1. Make sure your desktop is visible")
    print("2. Make sure the Notepad icon is visible on desktop")
    print("3. Position your mouse over the Notepad icon")
    print("4. Press Enter when ready to capture")
    print()
    print("=" * 60)
    
    input("Press Enter when your mouse is over the Notepad icon...")
    
    # Get mouse position
    x, y = pyautogui.position()
    print(f"\nMouse position: ({x}, {y})")
    
    # Capture region around icon
    # Desktop icons are typically 32-96 pixels
    icon_size = 64
    region_size = icon_size + 20  # Add padding
    
    left = max(0, x - region_size // 2)
    top = max(0, y - region_size // 2)
    width = region_size
    height = region_size
    
    print(f"\nCapturing region: ({left}, {top}) size: {width}x{height}")
    print("Capturing in 2 seconds...")
    time.sleep(2)
    
    # Capture screenshot
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    
    # Save to resources/icons directory
    icon_dir = Path("resources") / "icons"
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = icon_dir / "notepad_icon.png"
    screenshot.save(output_path)
    
    print(f"\n✓ Icon template saved to: {output_path}")
    print()
    print("The bot will now use this template for more accurate detection!")
    print("You can test it by running: python test_icon_detection.py")
    print()

if __name__ == "__main__":
    try:
        capture_notepad_icon()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
