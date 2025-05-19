import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError, Page
from pom.tenant_page import TenantPage

# Load environment variables
load_dotenv(override=True)

@pytest.fixture
def tenant_page(page: Page, base_url: str):
    """Fixture to provide a TenantPage instance"""
    return TenantPage(page, base_url)

@pytest.fixture
def tenant_credentials():
    """Fixture to provide tenant credentials"""
    email = os.getenv('TenantA_USER_EMAIL')
    password = os.getenv('TenantA_USER_PASSWORD')
    
    if not email or not password:
        pytest.fail("TenantA_USER_EMAIL and TenantA_USER_PASSWORD must be set in .env file")
    
    return {"email": email, "password": password}

def test_successful_login(tenant_page: TenantPage, tenant_credentials: dict):
    """Test successful login with valid credentials"""
    tenant_page.navigate_to_login()
    tenant_page.login(tenant_credentials["email"], tenant_credentials["password"])
    expect(tenant_page.page).to_have_url(f"{tenant_page.base_url}/welcome")