"""
Main automation bot for desktop icon grounding and Notepad automation.
"""
import sys
import pyautogui
from pathlib import Path

# Add src to path before other imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from botcity.core import DesktopBot, BotCityMaestroSDK
    from botcity.core.backend import Backend
    BOTCITY_AVAILABLE = True
except ImportError:
    # Use compatible wrapper if BotCity is not available
    print("WARNING: BotCity framework not found. Using compatible wrapper with pyautogui.")
    from botcity_compat import DesktopBot, BotCityMaestroSDK
    BOTCITY_AVAILABLE = False

from icon_grounding import IconGrounding
from notepad_automation import NotepadAutomation
from api_client import APIClient
import config

class DesktopAutomationBot(DesktopBot):
    """Main bot class for desktop automation."""
    
    def action(self, execution=None):
        """Main bot action."""
        try:
            # Initialize components
            icon_grounding = IconGrounding(self)
            notepad_automation = NotepadAutomation(self)
            api_client = APIClient(config.API_BASE_URL)
            
            print("=" * 60)
            print("Desktop Automation Bot - Starting")
            print("=" * 60)
            
            # Fetch posts from API
            print("\n[1/5] Fetching blog posts from API...")
            posts = api_client.fetch_posts(limit=config.MAX_POSTS)
            
            if not posts:
                print("ERROR: No posts fetched from API. Exiting.")
                return
            
            print(f"✓ Successfully fetched {len(posts)} posts")
            
            # Process each post
            for idx, post in enumerate(posts, 1):
                print(f"\n{'=' * 60}")
                print(f"Processing Post {idx}/{len(posts)} (ID: {post['id']})")
                print(f"{'=' * 60}")
                
                # Step 1: Capture screenshot and find icon
                print("\n[2/5] Capturing desktop screenshot...")
                icon_grounding.capture_desktop_screenshot()
                print("✓ Screenshot captured")
                
                print("\n[3/5] Locating Notepad icon...")
                icon_position = icon_grounding.find_notepad_icon(
                    retry_attempts=config.ICON_RETRY_ATTEMPTS,
                    retry_delay=config.ICON_RETRY_DELAY
                )
                
                if not icon_position:
                    print("ERROR: Could not locate Notepad icon. Skipping post.")
                    continue
                
                x, y = icon_position
                print(f"✓ Icon found at coordinates: ({x}, {y})")
                
                # Save annotated screenshot for first 3 posts in different positions
                if idx <= 3:
                    screen_width, screen_height = pyautogui.size()
                    x, y = icon_position

                    if x < screen_width * 0.33 and y < screen_height * 0.33:
                        location = "top_left"
                    elif x > screen_width * 0.66 and y > screen_height * 0.66:
                        location = "bottom_right"
                    else:
                        location = "center"

                    screenshot_name = f"icon_detected_{location}.png"
                    screenshot_path = config.SCREENSHOT_DIR / screenshot_name
                    icon_grounding.save_annotated_screenshot(
                        icon_position,
                        str(screenshot_path),
                        label=f"Icon detected in {location.replace('_', ' ')}"
                    )

                
                # Step 2: Launch Notepad
                print("\n[4/5] Launching Notepad...")
                if not notepad_automation.launch_notepad(icon_position):
                    print("ERROR: Failed to launch Notepad. Skipping post.")
                    continue
                print("✓ Notepad launched successfully")
                
                # Step 3: Type post content
                print("\n[5/5] Typing post content...")
                post_content = config.FILE_FORMAT.format(
                    title=post['title'],
                    body=post['body']
                )
                
                # Clear any existing text
                self.control_a()
                self.wait(200)

                # Create new file
                self.control_n()
                self.wait(200)




                
                # Type the content
                notepad_automation.type_text(post_content, delay=0.03)
                print("✓ Content typed")
                
                # Step 4: Save file
                print("\nSaving file...")
                filename = f"post_{post['id']}.txt"
                notepad_automation.save_file(filename, config.PROJECT_DIR)
                print(f"✓ File saved: {filename}")

                self.wait(500)

                self.yes()

                self.wait(500)

                # Step 5: Close Notepad
                print("\nClosing Notepad...")
                notepad_automation.close_notepad()
                print("✓ Notepad closed")
                
                # Wait before next iteration
                self.wait(500)

                #deselect notepad icon
                self.move_to(100, 100)
                self.double_click()
            
            print("\n" + "=" * 60)
            print("Automation completed successfully!")
            print("=" * 60)
            print(f"\nFiles saved to: {config.PROJECT_DIR}")
            print(f"Screenshots saved to: {config.SCREENSHOT_DIR}")

            
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            raise

def main():
    """Main entry point."""
    try:
        # Initialize BotCity (Maestro is optional)
        try:
            maestro = BotCityMaestroSDK.from_sys_args()
        except:
            maestro = None
            print("Running without BotCity Maestro SDK (standalone mode)")
        
        bot = DesktopAutomationBot()
        
        # Set headless mode (set to False to see the bot in action)
        bot.headless = False
        
        # Set default delay
        bot.delay_between_actions = 200
        
        # Run the bot
        bot.execute()
    except KeyboardInterrupt:
        print("\nBot execution interrupted by user.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()