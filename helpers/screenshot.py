from playwright.sync_api import Page
import os
from datetime import datetime
import re
from .logger import TestLogger

class ScreenshotHelper:
    """Helper class for test screenshots"""
    
    def __init__(self, page: Page, test_name: str):
        """Initialize the ScreenshotHelper.
        
        Args:
            page (Page): Playwright page object
            test_name (str): Name of the test for screenshot naming
        """
        self.page = page
        self.test_name = self._sanitize_filename(test_name)
        self.screenshot_dir = "reports/screenshots"
        self.logger = TestLogger(f"screenshot_{test_name}")
        self._ensure_screenshot_dir()

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be safe for all operating systems.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove square brackets and their contents
        filename = re.sub(r'\[.*?\]', '', filename)
        # Replace multiple underscores with a single one
        filename = re.sub(r'_+', '_', filename)
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        return filename

    def _ensure_screenshot_dir(self):
        """Ensure the screenshot directory exists"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            self.logger.info(f"Created screenshot directory: {self.screenshot_dir}")

    def take_screenshot(self, name: str, full_page: bool = False):
        """Take a screenshot with a given name.
        
        Args:
            name (str): Name for the screenshot
            full_page (bool): Whether to take a full page screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self._sanitize_filename(name)
        filename = f"{self.test_name}_{safe_name}_{timestamp}.png"
        screenshot_path = os.path.join(self.screenshot_dir, filename)
        
        try:
            self.page.screenshot(path=screenshot_path, full_page=full_page)
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise

    def take_error_screenshot(self, page_path: str, error_message: str = None, full_page: bool = True):
        """Take a screenshot on test failure.
        
        Args:
            page_path (str): The path of the page that failed
            error_message (str, optional): Additional error message to include in filename
            full_page (bool): Whether to take a full page screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_path = self._sanitize_filename(page_path)
        
        if error_message:
            safe_error = self._sanitize_filename(error_message[:20])
            name = f"error_{safe_path}_{safe_error}"
        else:
            name = f"error_{safe_path}"
            
        return self.take_screenshot(name, full_page) 