"""Notepad automation using BotCity."""
import time
from pathlib import Path
from typing import Optional
try:
    from botcity.core import DesktopBot
    from botcity.core.backend import Backend
except ImportError:
    from botcity_compat import DesktopBot
try:
    import pygetwindow as gw
except ImportError:
    gw = None

class NotepadAutomation:
    """Handles automation of Notepad application."""
    
    def __init__(self, bot: DesktopBot):
        self.bot = bot
        self.notepad_window = None
    
    def launch_notepad(self, icon_position: tuple) -> bool:
        """
        Launch Notepad by double-clicking the desktop icon.
        
        Args:
            icon_position: (x, y) coordinates of the Notepad icon
            
        Returns:
            True if Notepad launched successfully, False otherwise
        """
        try:
            x, y = icon_position
            
            # Move mouse to icon position
            self.bot.move_to(x, y)
            time.sleep(0.2)
            
            # Double-click to launch
            self.bot.double_click()
            time.sleep(1.0)  # Wait for Notepad to launch
            
            # Verify Notepad launched
            return self.verify_notepad_launched()
            
        except Exception as e:
            print(f"Error launching Notepad: {e}")
            return False
    
    def verify_notepad_launched(self, timeout: float = 5.0) -> bool:
        """
        Verify that Notepad window is open.
        
        Args:
            timeout: Maximum time to wait for window
            
        Returns:
            True if Notepad window found, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if gw:
                    windows = gw.getWindowsWithTitle("Notepad")
                    if windows:
                        self.notepad_window = windows[0]
                        # Activate the window
                        self.notepad_window.activate()
                        time.sleep(0.3)
                        return True
                else:
                    # Fallback: just wait and assume it launched
                    time.sleep(1.0)
                    return True
            except Exception as e:
                print(f"Error checking for Notepad window: {e}")
            
            time.sleep(0.2)
        
        return False
    
    def type_text(self, text: str, delay: float = 0.05):
        """
        Type text into Notepad.
        
        Args:
            text: Text to type
            delay: Delay between keystrokes
        """
        try:
            # Ensure Notepad is active
            if self.notepad_window:
                self.notepad_window.activate()
                time.sleep(0.2)
            
            # Type the text
            self.bot.type_text(text, delay=delay)
            time.sleep(0.2)
            
        except Exception as e:
            print(f"Error typing text: {e}")
    
    def save_file(self, filename: str, directory: Path):
        """
        Save the current Notepad file.
        
        Args:
            filename: Name of the file to save
            directory: Directory to save the file in
        """
        try:
            # Ensure Notepad is active
            if self.notepad_window:
                self.notepad_window.activate()
                time.sleep(0.2)
            
            # Press Ctrl+S to open Save dialog
            self.bot.control_a()  # Select all (to ensure we're in the text area)
            time.sleep(0.1)
            self.bot.control_s()  # Save
            time.sleep(0.5)
            
            # Type the directory path
            full_path = directory / filename
            self.bot.type_text(str(full_path), delay=0.05)
            time.sleep(0.3)
            
            # Press Enter to save
            self.bot.enter()
            time.sleep(0.5)
            
            # Handle "File already exists" dialog if it appears
            # Press Enter to confirm overwrite (or Alt+N for "No")
            # For now, we'll just wait a bit
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def close_notepad(self):
        """Close Notepad window."""
        try:
            if gw and self.notepad_window:
                try:
                    self.notepad_window.close()
                    time.sleep(0.5)
                except:
                    # Fallback: use Alt+F4
                    self.bot.alt_f4()
                    time.sleep(0.5)
            else:
                # Fallback: use Alt+F4
                self.bot.alt_f4()
                time.sleep(0.5)
        except Exception as e:
            print(f"Error closing Notepad: {e}")
