from playwright.sync_api import Page, expect, TimeoutError
from .logger import TestLogger

class PageLoadHelper:
    """Helper class for page load verification strategies"""
    
    def __init__(self, page: Page, test_name: str):
        """Initialize the PageLoadHelper.
        
        Args:
            page (Page): Playwright page object
            test_name (str): Name of the test for logging
        """
        self.page = page
        self.logger = TestLogger(f"page_load_{test_name}")

    def wait_for_network_idle(self, timeout: int = 30000):
        """Wait for network to be idle.
        
        Args:
            timeout (int): Maximum time to wait in milliseconds
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.logger.info("Network is idle")
        except TimeoutError:
            self.logger.warning("Network did not become idle within timeout")

    def wait_for_dom_content_loaded(self, timeout: int = 30000):
        """Wait for DOM content to be loaded.
        
        Args:
            timeout (int): Maximum time to wait in milliseconds
        """
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            self.logger.info("DOM content is loaded")
        except TimeoutError:
            self.logger.warning("DOM content did not load within timeout")

    def wait_for_load(self, timeout: int = 30000):
        """Wait for page load event.
        
        Args:
            timeout (int): Maximum time to wait in milliseconds
        """
        try:
            self.page.wait_for_load_state("load", timeout=timeout)
            self.logger.info("Page load event fired")
        except TimeoutError:
            self.logger.warning("Page load event did not fire within timeout")

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for a specific element to be present.
        
        Args:
            selector (str): CSS selector to wait for
            timeout (int): Maximum time to wait in milliseconds
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.logger.info(f"Selector '{selector}' is present")
        except TimeoutError:
            self.logger.warning(f"Selector '{selector}' did not appear within timeout")

    def wait_for_navigation(self, timeout: int = 30000):
        """Wait for navigation to complete.
        
        Args:
            timeout (int): Maximum time to wait in milliseconds
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            self.logger.info("Navigation completed")
        except TimeoutError:
            self.logger.warning("Navigation did not complete within timeout")

    def verify_page_loaded(self, expected_url: str = None, expected_title: str = None, 
                          required_selector: str = None, timeout: int = 30000):
        """Comprehensive page load verification.
        
        Args:
            expected_url (str, optional): Expected URL to verify
            expected_title (str, optional): Expected page title
            required_selector (str, optional): Required element selector
            timeout (int): Maximum time to wait in milliseconds
        """
        try:
            # Wait for network and DOM
            self.wait_for_network_idle(timeout)
            self.wait_for_dom_content_loaded(timeout)

            # Verify URL if provided
            if expected_url:
                expect(self.page).to_have_url(expected_url)
                self.logger.info(f"URL verified: {expected_url}")

            # Verify title if provided
            if expected_title:
                expect(self.page).to_have_title(expected_title)
                self.logger.info(f"Title verified: {expected_title}")

            # Verify required element if provided
            if required_selector:
                self.wait_for_selector(required_selector, timeout)
                self.logger.info(f"Required element verified: {required_selector}")

            # Check for common error indicators
            error_selectors = ["text=Error", "text=404", "text=Not Found", "text=Server Error"]
            for selector in error_selectors:
                expect(self.page.locator(selector)).not_to_be_visible()

            self.logger.info("Page load verification completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Page load verification failed: {str(e)}")
            raise 