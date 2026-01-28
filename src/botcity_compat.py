"""
BotCity-compatible wrapper using pyautogui and opencv.
This allows the code to work even if BotCity packages aren't available.
"""
import pyautogui
import cv2
import numpy as np
from pathlib import Path
import time
from typing import Optional, Tuple
import os

class BotCityMaestroSDK:
    """Compatible BotCity Maestro SDK stub."""
    @staticmethod
    def from_sys_args():
        return None

class DesktopBot:
    """BotCity DesktopBot compatible wrapper using pyautogui."""
    
    def __init__(self):
        self.headless = False
        self.delay_between_actions = 200  # milliseconds
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def save_screenshot(self, path: str):
        """Save a screenshot of the screen."""
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
    
    def move_to(self, x: int, y: int):
        """Move mouse to coordinates."""
        pyautogui.moveTo(x, y, duration=0.2)
    
    def click(self, button='left'):
        """Click at current mouse position."""
        pyautogui.click(button=button)
    
    def double_click(self):
        """Double click at current mouse position."""
        pyautogui.doubleClick()
    
    def type_text(self, text: str, delay: float = 0.05):
        """Type text."""
        pyautogui.write(text, interval=delay)
    
    def control_a(self):
        """Press Ctrl+A."""
        pyautogui.hotkey('ctrl', 'a')

    def control_n(self):
        """Press Ctrl+A."""
        pyautogui.hotkey('ctrl', 'n')    
    
    def control_s(self):
        """Press Ctrl+S."""
        pyautogui.hotkey('ctrl', 's')
    
    def alt_f4(self):
        """Press Alt+F4."""
        pyautogui.hotkey('alt', 'f4')

    def yes(self):
        """Press Enter."""
        pyautogui.hotkey('alt', 'y')
    
    def enter(self):
        """Press Enter."""
        pyautogui.press('enter')
    
    def wait(self, milliseconds: int):
        """Wait for specified milliseconds."""
        time.sleep(milliseconds / 1000.0)
    
    def execute(self):
        """Execute the bot's action method."""
        if hasattr(self, 'action'):
            self.action()
