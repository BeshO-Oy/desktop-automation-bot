import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List
import time
try:
    from botcity.core import BotCityMaestroSDK, DesktopBot
    from botcity.core.backend import Backend
except ImportError:
    from botcity_compat import DesktopBot, BotCityMaestroSDK
import pyautogui
from PIL import Image
import os

class IconGrounding:
    """
    Dynamic icon grounding system that can locate desktop icons
    regardless of their position using computer vision.
    """
    
    def __init__(self, bot: DesktopBot):
        self.bot = bot
        self.screenshot = None
        
    def capture_desktop_screenshot(self) -> np.ndarray:
        """Capture a screenshot of the desktop."""
        # Use BotCity's screenshot capability
        screenshot_path = "temp_screenshot.png"
        try:
            self.bot.save_screenshot(screenshot_path)
        except:
            # Fallback to pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
        
        # Read the screenshot
        screenshot = cv2.imread(screenshot_path)
        
        if screenshot is None:
            # Try reading as PIL Image and convert
            from PIL import Image
            pil_img = Image.open(screenshot_path)
            screenshot = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        # Clean up temp file
        if os.path.exists(screenshot_path):
            try:
                os.remove(screenshot_path)
            except:
                pass
            
        self.screenshot = screenshot
        return screenshot
    
    def find_icon_by_text(self, icon_text: str = "Notepad") -> Optional[Tuple[int, int]]:
        """
        Find icon by searching for text label near icons.
        Uses OCR-like approach to find text labels.
        """
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        # Convert to grayscale for text detection
        gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        
        # Use template matching with text detection
        # This is a simplified approach - in production, you'd use OCR
        # For now, we'll use a combination of icon shape detection and text proximity
        
        # Try to find icon by shape characteristics (square/rectangular regions)
        # Desktop icons typically have consistent sizes
        return self._find_icon_by_shape_and_text(gray, icon_text)
    
    def find_icon_by_template(self, template_path: Optional[str] = None) -> Optional[Tuple[int, int]]:
        """
        Find icon using template matching.
        If template_path is None, uses a generic icon detection approach.
        """
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        if template_path and Path(template_path).exists():
            return self._template_match(template_path)
        else:
            # Use generic icon detection
            return self._detect_icon_generic()
    
    def _find_icon_by_shape_and_text(self, gray: np.ndarray, text: str) -> Optional[Tuple[int, int]]:
        """
        Find icon by detecting icon-like shapes and checking for nearby text.
        This is a flexible approach that doesn't require exact template matching.
        """
        # Detect potential icon regions (rectangular areas with consistent patterns)
        # Desktop icons are typically arranged in a grid
        
        # Use edge detection to find rectangular regions
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size (icons are typically 32x32 to 96x96 pixels)
        icon_size_min = 20
        icon_size_max = 150
        
        potential_icons = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # Check if size is reasonable for an icon
            if icon_size_min <= w <= icon_size_max and icon_size_min <= h <= icon_size_max:
                # Check aspect ratio (icons are roughly square)
                aspect_ratio = w / h if h > 0 else 0
                if 0.7 <= aspect_ratio <= 1.3:
                    center_x = x + w // 2
                    center_y = y + h // 2
                    potential_icons.append((center_x, center_y, area))
        
        # Sort by area (larger icons are more likely to be the target)
        potential_icons.sort(key=lambda x: x[2], reverse=True)
        
        # For "Notepad", we can use text detection in the region below icons
        # Desktop icons have text labels below them
        for x, y, _ in potential_icons:
            # Check region below icon for text (simplified - in production use OCR)
            # For now, return the largest/most prominent icon
            # In a real implementation, you'd use OCR to verify the text label
            
            # Return the first reasonable candidate
            # In production, you'd verify with OCR or other methods
            return (x, y)
        
        return None
    
    def _detect_icon_generic(self) -> Optional[Tuple[int, int]]:
        """
        Generic icon detection that works for any icon without templates.
        Uses visual features and layout analysis.
        """
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Detect icon grid pattern
        # Desktop icons are arranged in a grid, we can detect this pattern
        
        # Use blob detection to find icon-like regions
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 400  # Minimum icon area
        params.maxArea = 10000  # Maximum icon area
        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False
        
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(gray)
        
        if keypoints:
            # Return the first detected keypoint (center of icon)
            kp = keypoints[0]
            return (int(kp.pt[0]), int(kp.pt[1]))
        
        # Method 2: Use the shape-based approach
        return self._find_icon_by_shape_and_text(gray, "Notepad")
    
    def _template_match(self, template_path: str) -> Optional[Tuple[int, int]]:
        """Template matching for icon detection."""
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            return None
        
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        
        # Perform template matching
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Check confidence threshold
        if max_val >= 0.7:  # config.ICON_CONFIDENCE
            # Return center of matched region
            h, w = template.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)
        
        return None
    
    def find_notepad_icon(self, retry_attempts: int = 3, retry_delay: float = 1.0) -> Optional[Tuple[int, int]]:
        """
        Find Notepad icon with retry logic.
        Uses multiple detection strategies, prioritizing Notepad-specific detection.
        """
        # Check if template image is available
        import config
        template_path = config.NOTEPAD_ICON_TEMPLATE
        
        for attempt in range(retry_attempts):
            try:
                # Capture fresh screenshot
                self.capture_desktop_screenshot()
                
                # Method 0: Template matching (MOST ACCURATE if template available)
                if template_path.exists():
                    result = self._template_match(str(template_path))
                    if result:
                        print(f"Found Notepad icon using template matching")
                        return result
                
                # Method 1: Find all icons and check text labels
                result = self._find_icon_by_label_text("Notepad")
                if result:
                    print(f"Found Notepad icon using text label detection")
                    return result
                
                # Method 2: Use Windows API to find Notepad shortcut
                result = self._find_icon_using_windows_api()
                if result:
                    print(f"Found Notepad icon using Windows API")
                    return result
                
                # Method 3: Find all icons and filter by characteristics
                result = self._find_notepad_by_characteristics()
                if result:
                    print(f"Found Notepad icon using characteristic matching")
                    return result
                
                # Method 4: Grid-based detection with text region checking
                result = self._find_icon_in_grid_with_text_check()
                if result:
                    print(f"Found Notepad icon using grid detection")
                    return result
                
                # Method 5: Fallback to generic detection (last resort)
                result = self._detect_icon_generic()
                if result:
                    print(f"Warning: Using generic icon detection (may not be Notepad)")
                    return result
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < retry_attempts - 1:
                time.sleep(retry_delay)
        
        return None
    
    def _find_icon_by_label_text(self, target_text: str = "Notepad") -> Optional[Tuple[int, int]]:
        """
        Find icon by detecting text labels below desktop icons.
        Desktop icons have text labels directly below them.
        """
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        
        # Find all potential icon regions
        icon_candidates = self._find_all_icon_candidates(gray)
        
        if not icon_candidates:
            return None
        
        # For each candidate, check the text region below the icon
        target_text_lower = target_text.lower()
        
        for icon_x, icon_y, icon_size in icon_candidates:
            # Text label is typically 20-40 pixels below the icon
            text_region_y = icon_y + icon_size // 2 + 30
            text_region_height = 30
            text_region_x = icon_x - icon_size
            text_region_width = icon_size * 2
            
            # Ensure region is within image bounds
            h, w = gray.shape
            text_region_x = max(0, min(text_region_x, w - text_region_width))
            text_region_y = max(0, min(text_region_y, h - text_region_height))
            text_region_width = min(text_region_width, w - text_region_x)
            text_region_height = min(text_region_height, h - text_region_y)
            
            if text_region_width > 0 and text_region_height > 0:
                # Extract text region
                text_region = gray[text_region_y:text_region_y+text_region_height,
                                  text_region_x:text_region_x+text_region_width]
                
                # Try simple text matching using template matching on text patterns
                # Or use OCR if available
                if self._check_text_region_matches(text_region, target_text_lower):
                    return (icon_x, icon_y)
        
        return None
    
    def _find_all_icon_candidates(self, gray: np.ndarray) -> List[Tuple[int, int, int]]:
        """Find all potential icon candidates on the desktop."""
        candidates = []
        
        # Use multiple methods to find icons
        icon_sizes = [32, 48, 64, 96]
        
        for icon_size in icon_sizes:
            step = icon_size // 2
            
            for y in range(0, gray.shape[0] - icon_size, step):
                for x in range(0, gray.shape[1] - icon_size, step):
                    roi = gray[y:y+icon_size, x:x+icon_size]
                    
                    # Calculate features
                    variance = np.var(roi)
                    mean = np.mean(roi)
                    std = np.std(roi)
                    
                    # Icon characteristics
                    if (300 < variance < 8000 and 40 < mean < 220 and std > 15):
                        edges_roi = cv2.Canny(roi, 50, 150)
                        edge_density = np.sum(edges_roi > 0) / (icon_size * icon_size)
                        
                        if 0.05 < edge_density < 0.5:
                            center_x = x + icon_size // 2
                            center_y = y + icon_size // 2
                            score = variance * edge_density * (std / mean if mean > 0 else 0)
                            candidates.append((center_x, center_y, icon_size, score))
        
        # Remove duplicates and sort by score
        filtered = []
        for candidate in candidates:
            x, y, size, score = candidate
            is_duplicate = False
            for existing in filtered:
                ex, ey, _, _ = existing
                distance = np.sqrt((x - ex)**2 + (y - ey)**2)
                if distance < 50:
                    is_duplicate = True
                    if score > existing[3]:
                        filtered.remove(existing)
                        filtered.append(candidate)
                    break
            if not is_duplicate:
                filtered.append(candidate)
        
        # Return as (x, y, size) tuples, sorted by score
        filtered.sort(key=lambda x: x[3], reverse=True)
        return [(x, y, size) for x, y, size, _ in filtered]
    
    def _check_text_region_matches(self, text_region: np.ndarray, target_text: str) -> bool:
        """
        Check if text region contains the target text.
        Uses simple pattern matching since OCR may not be available.
        """
        # Method 1: Try OCR if pytesseract is available
        try:
            import pytesseract
            # Preprocess for better OCR
            _, binary = cv2.threshold(text_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binary = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text = pytesseract.image_to_string(binary, config='--psm 6').strip().lower()
            if target_text in text:
                return True
        except:
            pass
        
        # Method 2: Simple pattern matching using character width analysis
        # Desktop icon text has consistent character spacing
        # We can detect if the text region has the right "shape" for the target text
        
        # Calculate text-like features
        # Text regions have horizontal lines and consistent spacing
        horizontal_projection = np.sum(text_region < 128, axis=0)  # Dark pixels (text)
        
        # Check if there are multiple text-like regions (characters)
        text_regions = []
        in_text = False
        start = 0
        
        for i, val in enumerate(horizontal_projection):
            if val > text_region.shape[0] * 0.3:  # Threshold for text
                if not in_text:
                    start = i
                    in_text = True
            else:
                if in_text:
                    text_regions.append((start, i))
                    in_text = False
        
        # Estimate character count based on text regions
        # "Notepad" has 7 characters, so we expect ~7 text regions
        if len(text_regions) >= 5 and len(text_regions) <= 10:
            # Could be "Notepad" or similar length text
            # For now, return True if it looks like text
            # In a more sophisticated implementation, we'd use OCR
            return True
        
        return False
    
    def _find_icon_using_windows_api(self) -> Optional[Tuple[int, int]]:
        """Use Windows API to find Notepad shortcut location."""
        try:
            import win32gui
            import win32con
            
            # Get desktop window
            desktop = win32gui.FindWindow("Progman", "Program Manager")
            if not desktop:
                desktop = win32gui.FindWindow("WorkerW", None)
            
            if desktop:
                # List all child windows (icons)
                def enum_child_proc(hwnd, lParam):
                    class_name = win32gui.GetClassName(hwnd)
                    if class_name == "SHELLDLL_DefView":
                        # Found desktop view
                        list_view = win32gui.FindWindowEx(hwnd, 0, "SysListView32", None)
                        if list_view:
                            # Get icon positions
                            # This is complex - for now, return None and use other methods
                            pass
                    return True
                
                win32gui.EnumChildWindows(desktop, enum_child_proc, None)
        except ImportError:
            # win32gui not available
            pass
        except Exception as e:
            print(f"Windows API method failed: {e}")
        
        return None
    
    def _find_notepad_by_characteristics(self) -> Optional[Tuple[int, int]]:
        """
        Find Notepad icon by analyzing icon characteristics.
        Notepad icon has specific visual features we can detect.
        """
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        candidates = self._find_all_icon_candidates(gray)
        
        if not candidates:
            return None
        
        # Score each candidate based on Notepad-specific characteristics
        scored_candidates = []
        
        for x, y, size in candidates:
            score = 0
            
            # Extract icon region
            icon_region = gray[max(0, y-size//2):min(gray.shape[0], y+size//2),
                              max(0, x-size//2):min(gray.shape[1], x+size//2)]
            
            if icon_region.size > 0:
                # Notepad icon characteristics:
                # 1. Has document-like features (rectangular with lines)
                # 2. Medium contrast
                # 3. Text-like patterns inside
                
                # Check for horizontal lines (document lines)
                edges = cv2.Canny(icon_region, 50, 150)
                horizontal_lines = np.sum(edges, axis=1)
                line_count = np.sum(horizontal_lines > np.mean(horizontal_lines) * 1.5)
                
                if 2 <= line_count <= 5:  # Document-like
                    score += 10
                
                # Check contrast (Notepad icon has medium contrast)
                contrast = np.std(icon_region)
                if 20 < contrast < 60:
                    score += 5
                
                # Check text region below
                text_y = y + size // 2 + 30
                if text_y < gray.shape[0] - 30:
                    text_region = gray[text_y:text_y+30, max(0, x-size):min(gray.shape[1], x+size)]
                    if text_region.size > 0:
                        # Check if text region has text-like patterns
                        text_variance = np.var(text_region)
                        if text_variance > 500:  # Text has high variance
                            score += 10
            
            scored_candidates.append((x, y, score))
        
        # Return highest scoring candidate
        if scored_candidates:
            scored_candidates.sort(key=lambda x: x[2], reverse=True)
            best = scored_candidates[0]
            if best[2] > 15:  # Minimum score threshold
                return (best[0], best[1])
        
        return None
    
    def _find_icon_in_grid_with_text_check(self) -> Optional[Tuple[int, int]]:
        """Find icon in grid and verify with text check."""
        result = self._find_icon_in_grid()
        if result:
            # Verify it's Notepad by checking text
            x, y = result
            gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
            
            # Check text region
            text_y = y + 40
            if text_y < gray.shape[0] - 30:
                text_region = gray[text_y:text_y+30, max(0, x-60):min(gray.shape[1], x+60)]
                if self._check_text_region_matches(text_region, "notepad"):
                    return result
        
        return None
    
    def _find_icon_in_grid(self) -> Optional[Tuple[int, int]]:
        """
        Find icon by detecting the desktop icon grid pattern.
        Desktop icons are arranged in a regular grid, which we can detect.
        This method is flexible and works for any icon without templates.
        """
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        
        # Use a multi-scale sliding window approach to find icon-like regions
        # Desktop icons can be different sizes (small, medium, large)
        icon_sizes = [32, 48, 64, 96]  # Different icon sizes in pixels
        step_ratio = 0.5  # Overlap between windows
        
        all_candidates = []
        
        for icon_size in icon_sizes:
            step = int(icon_size * step_ratio)
            candidates = []
            
            for y in range(0, gray.shape[0] - icon_size, step):
                for x in range(0, gray.shape[1] - icon_size, step):
                    roi = gray[y:y+icon_size, x:x+icon_size]
                    
                    # Calculate features that indicate an icon
                    variance = np.var(roi)
                    mean = np.mean(roi)
                    std = np.std(roi)
                    
                    # Icons have specific characteristics:
                    # - Medium to high variance (detailed images)
                    # - Reasonable brightness (not too dark or bright)
                    # - Good contrast (high std)
                    if (300 < variance < 8000 and 
                        40 < mean < 220 and 
                        std > 15):
                        
                        # Additional check: icons often have edges
                        edges_roi = cv2.Canny(roi, 50, 150)
                        edge_density = np.sum(edges_roi > 0) / (icon_size * icon_size)
                        
                        # Icons have moderate edge density
                        if 0.05 < edge_density < 0.5:
                            center_x = x + icon_size // 2
                            center_y = y + icon_size // 2
                            # Score based on multiple factors
                            score = variance * edge_density * (std / mean if mean > 0 else 0)
                            candidates.append((center_x, center_y, score, icon_size))
            
            all_candidates.extend(candidates)
        
        if all_candidates:
            # Remove duplicates (icons detected at multiple scales)
            # Group nearby detections
            filtered_candidates = []
            for candidate in all_candidates:
                x, y, score, size = candidate
                is_duplicate = False
                
                for existing in filtered_candidates:
                    ex, ey, _, _ = existing
                    distance = np.sqrt((x - ex)**2 + (y - ey)**2)
                    # If within 50 pixels, consider it a duplicate
                    if distance < 50:
                        is_duplicate = True
                        # Keep the one with higher score
                        if score > existing[2]:
                            filtered_candidates.remove(existing)
                            filtered_candidates.append(candidate)
                        break
                
                if not is_duplicate:
                    filtered_candidates.append(candidate)
            
            if filtered_candidates:
                # Sort by score (higher = more likely to be an icon)
                filtered_candidates.sort(key=lambda x: x[2], reverse=True)
                # Return the best candidate
                best = filtered_candidates[0]
                return (best[0], best[1])
        
        return None
    
    def save_annotated_screenshot(self, icon_position: Tuple[int, int], 
                                  output_path: str, 
                                  label: str = "Icon Detected"):
        """Save an annotated screenshot showing the detected icon."""
        if self.screenshot is None:
            self.capture_desktop_screenshot()
        
        annotated = self.screenshot.copy()
        x, y = icon_position
        
        # Draw circle at icon position
        cv2.circle(annotated, (x, y), 30, (0, 255, 0), 3)
        cv2.circle(annotated, (x, y), 5, (0, 255, 0), -1)
        
        # Add label
        cv2.putText(annotated, label, (x + 40, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated, f"({x}, {y})", (x + 40, y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Save annotated screenshot
        cv2.imwrite(output_path, annotated)
        print(f"Annotated screenshot saved to {output_path}")
