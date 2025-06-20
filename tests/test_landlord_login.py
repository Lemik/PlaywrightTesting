import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError, Page
from pom.landlord_page import LandlordPage
from helpers.landlord_fixture import landlord_page, landlord_credentials

def test_successful_login(landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
    """Test successful login with valid credentials"""
    test_logger.info("Starting login test")
    landlord_page.navigate_to_login()
    landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
    
    # Verify login success with comprehensive page load check
    page_load_helper.verify_page_loaded(
        expected_url=f"{landlord_page.base_url}/welcome",
        required_selector="h1"
    )
    test_logger.info("Login test completed successfully")

@pytest.mark.parametrize("page_path", [
    "/welcome",
    "/property",
    "/tenants",
    "/expense",
    "/income/history",
    "/cashflow",
#    "/tasks",
#    "/user/profile",
#    "/userFiles",
#    "/about",
#    "/news"
])
def test_landlord_pages_load(landlord_page: LandlordPage, landlord_credentials: dict, 
                           page_load_helper,screenshot_helper, test_logger, page_path: str):
    """Test that landlord pages load correctly after login"""
    test_logger.info(f"Testing page: {page_path}")
    
    # First login as landlord
    landlord_page.navigate_to_login()
    landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
    
    # Test the specific page
    try:
        landlord_page.navigate_to_page(page_path)
        # Verify page load with comprehensive checks
        page_load_helper.verify_page_loaded(
            expected_url=f"{landlord_page.base_url}{page_path}",
            required_selector="h1"
        )
        test_logger.info(f"Successfully loaded page: {page_path}")
    except Exception as e:
        test_logger.error(f"Failed to load page {page_path}: {str(e)}")
        # Take screenshot on failure using the helper
        screenshot_path = screenshot_helper.take_error_screenshot(page_path, str(e))
        pytest.fail(f"Failed to load page {page_path}: {str(e)}\nScreenshot saved to: {screenshot_path}")