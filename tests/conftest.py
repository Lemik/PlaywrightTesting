import pytest
from playwright.sync_api import sync_playwright

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
    return "http://localhost:3000"  # Change this to your application's URL 

@pytest.fixture(scope="function")
def slow_mo():
    """Slows down Playwright operations for debugging"""
    return 100  # milliseconds