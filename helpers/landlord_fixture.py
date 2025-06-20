import pytest
from playwright.sync_api import Page
from pom.landlord_page import LandlordPage
import os
from dotenv import load_dotenv

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