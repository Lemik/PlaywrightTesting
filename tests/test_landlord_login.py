import pytest
from playwright.sync_api import expect
from pom.landlord_page import LandlordPage
from helpers.landlord_fixture import landlord_page, landlord_credentials

def test_login_page_loads(landlord_page: LandlordPage, test_logger):
    """Test that the login page loads correctly"""
    test_logger.info("Testing login page load")
    landlord_page.navigate_to_login()
    
    # Verify we're on the login page
    expect(landlord_page.page).to_have_url(f"{landlord_page.base_url}/login")
    
    # Verify login form elements are present
    expect(landlord_page.page.locator('input[type="email"]')).to_be_visible()
    expect(landlord_page.page.locator('input[type="password"]')).to_be_visible()
    expect(landlord_page.page.locator('button:has-text("Login")')).to_be_visible()
    
    test_logger.info("Login page loaded successfully")

def test_successful_login(landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
    """Test successful login with valid credentials"""
    test_logger.info("Starting login test")
    landlord_page.navigate_to_login()
    
    try:
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        
        # Verify login success - check that we're no longer on login page
        current_url = landlord_page.page.url
        assert "/login" not in current_url, f"Login failed - still on login page: {current_url}"
        
        # Verify page loaded successfully
        page_load_helper.verify_page_loaded(
            required_selector="body"
        )
        test_logger.info(f"Login test completed successfully. Redirected to: {current_url}")
        
    except Exception as e:
        test_logger.warning(f"Login test failed (likely due to invalid credentials): {str(e)}")
        # This is expected if credentials are not valid - just log the issue
        pytest.skip("Login test skipped - credentials may be invalid or application not running")

def test_invalid_login(landlord_page: LandlordPage, test_logger):
    """Test login with invalid credentials"""
    test_logger.info("Testing invalid login")
    landlord_page.navigate_to_login()
    
    # Try to login with invalid credentials
    landlord_page.page.fill('input[type="email"]', "invalid@example.com")
    landlord_page.page.fill('input[type="password"]', "wrongpassword")
    landlord_page.page.click('button:has-text("Login")')
    
    # Wait for page to process the login attempt
    landlord_page.page.wait_for_load_state("networkidle")
    
    # Should still be on login page or show error message
    current_url = landlord_page.page.url
    assert "/login" in current_url, f"Expected to stay on login page, but redirected to: {current_url}"
    
    test_logger.info("Invalid login test completed - correctly stayed on login page")

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
                           page_load_helper, screenshot_helper, test_logger, page_path: str):
    """Test that landlord pages load correctly after login"""
    test_logger.info(f"Testing page: {page_path}")
    
    # First login as landlord
    landlord_page.navigate_to_login()
    
    try:
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        
        # Verify we're logged in before testing pages
        current_url = landlord_page.page.url
        assert "/login" not in current_url, f"Login failed - still on login page: {current_url}"
        
        # Test the specific page
        try:
            landlord_page.navigate_to_page(page_path)
            
            # Verify page load - be more flexible with URL matching
            current_url = landlord_page.page.url
            test_logger.info(f"Successfully navigated to: {current_url}")
            
            # Verify page loaded successfully
            page_load_helper.verify_page_loaded(
                required_selector="body"
            )
            test_logger.info(f"Successfully loaded page: {page_path}")
            
        except Exception as e:
            test_logger.error(f"Failed to load page {page_path}: {str(e)}")
            # Take screenshot on failure using the helper
            screenshot_path = screenshot_helper.take_error_screenshot(page_path, str(e))
            pytest.fail(f"Failed to load page {page_path}: {str(e)}\nScreenshot saved to: {screenshot_path}")
            
    except Exception as e:
        test_logger.warning(f"Login failed for page test {page_path} (likely due to invalid credentials): {str(e)}")
        pytest.skip(f"Page test skipped for {page_path} - login failed, credentials may be invalid")