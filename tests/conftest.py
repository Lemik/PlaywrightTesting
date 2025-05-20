import os
import pytest
from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv
from helpers import ScreenshotHelper, TestLogger, PageLoadHelper, ReportsHelper

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