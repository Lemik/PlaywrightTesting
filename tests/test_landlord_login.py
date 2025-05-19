import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError, Page
from pom.landlord_page import LandlordPage

# Load environment variables
load_dotenv(override=True)

@pytest.fixture
def landlord_page(page: Page, base_url: str):
    """Fixture to provide a LandlordPage instance"""
    return LandlordPage(page, base_url)

@pytest.fixture
def landlord_credentials():
    """Fixture to provide landlord credentials"""
    email = os.getenv('LANDLORD_USER_EMAIL')
    password = os.getenv('LANDLORD_USER_PASSWORD')
    
    if not email or not password:
        pytest.fail("LANDLORD_USER_EMAIL and LANDLORD_USER_PASSWORD must be set in .env file")
    
    return {"email": email, "password": password}

def test_successful_login(landlord_page: LandlordPage, landlord_credentials: dict):
    """Test successful login with valid credentials"""
    landlord_page.navigate_to_login()
    landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
    expect(landlord_page.page).to_have_url(f"{landlord_page.base_url}/welcome")