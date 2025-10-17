import os
import pytest
from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv
from helpers import ScreenshotHelper, TestLogger, PageLoadHelper, ReportsHelper

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1000,
            "height": 600,
        },
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="session")
def base_url():
    return os.getenv('URL')

@pytest.fixture(scope="function")
def slow_mo():
    """Slows down Playwright operations for debugging"""
    return 100  # milliseconds

@pytest.fixture(scope="session")
def reports_helper():
    """Fixture to provide a ReportsHelper instance"""
    return ReportsHelper()

@pytest.fixture
def test_logger(request, reports_helper):
    """Fixture to provide a TestLogger instance"""
    return TestLogger(request.node.name)

@pytest.fixture
def screenshot_helper(page: Page, request, reports_helper):
    """Fixture to provide a ScreenshotHelper instance"""
    return ScreenshotHelper(page, request.node.name)

@pytest.fixture
def page_load_helper(page: Page, request):
    """Fixture to provide a PageLoadHelper instance"""
    return PageLoadHelper(page, request.node.name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failures"""
    outcome = yield
    rep = outcome.get_result()
    
    # Only capture screenshots on failures, not on skips or passes
    if rep.when == "call" and rep.failed:
        # Get the page fixture if it exists
        if hasattr(item, 'funcargs') and 'page' in item.funcargs:
            page = item.funcargs['page']
            test_name = item.name
            
            try:
                # Create screenshot helper
                from helpers.screenshot import ScreenshotHelper
                screenshot_helper = ScreenshotHelper(page, test_name)
                
                # Take screenshot on failure
                screenshot_path = screenshot_helper.take_error_screenshot(
                    page_path="test_failure", 
                    error_message=rep.longreprtext[:50] if rep.longreprtext else "test_failed",
                    full_page=True
                )
                print(f"\n📸 Screenshot captured on failure: {screenshot_path}")
                
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")