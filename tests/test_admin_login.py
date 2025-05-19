import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError, Page
from pom.admin_page import AdminPage

# Load environment variables
load_dotenv(override=True)

@pytest.fixture
def admin_page(page: Page, base_url: str):
    """Fixture to provide an AdminPage instance"""
    return AdminPage(page, base_url)

@pytest.fixture
def admin_credentials():
    """Fixture to provide admin credentials"""
    email = os.getenv('ADMIN_USER_EMAIL')
    password = os.getenv('ADMIN_USER_PASSWORD')
    
    if not email or not password:
        pytest.fail("ADMIN_USER_EMAIL and ADMIN_USER_PASSWORD must be set in .env file")
    
    return {"email": email, "password": password}

def test_successful_login(admin_page: AdminPage, admin_credentials: dict):
    """Test successful login with valid credentials"""
    admin_page.navigate_to_login()
    admin_page.login(admin_credentials["email"], admin_credentials["password"])
    expect(admin_page.page).to_have_url(f"{admin_page.base_url}/welcome")

@pytest.mark.parametrize("page_path", [
    #  "/welcome",
    "/status",
    "/stats",
    #  "/admin/dashboard",
    #  "/admin/users",
    #  "/admin/settings",
    #  "/admin/reports"
])
def test_admin_pages_load(admin_page: AdminPage, admin_credentials: dict, page_path: str):
    """Test that admin pages load correctly after login"""
    # First login as admin
    admin_page.navigate_to_login()
    admin_page.login(admin_credentials["email"], admin_credentials["password"])
    
    # Test the specific page
    try:
        admin_page.navigate_to_page(page_path)
    except Exception as e:
        # Take screenshot on failure
        admin_page.page.screenshot(path=f"error-{page_path.replace('/', '-')}.png")
        pytest.fail(f"Failed to load page {page_path}: {str(e)}")