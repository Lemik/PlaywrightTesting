import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError

# Load environment variables
load_dotenv()

# Debug: Print all environment variables
print("All environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

# Debug: Print specific variables we're trying to access
print("\nSpecific variables we need:")
print(f"ADMIN_USER_EMAIL: {os.getenv('ADMIN_USER_EMAIL')}")
print(f"ADMIN_USER_PASSWORD: {os.getenv('ADMIN_USER_PASSWORD')}")

def test_successful_login(page, base_url):
    """Test successful login with valid credentials"""
    # Navigate to login page
    page.goto(f"{base_url}/login")
    
    # Get credentials from environment variables
    email = os.getenv('ADMIN_USER_EMAIL')
    password = os.getenv('ADMIN_USER_PASSWORD')
    
    if not email or not password:
        pytest.fail("ADMIN_USER_EMAIL and ADMIN_USER_PASSWORD must be set in .env file")
    
    
    # Fill in login 
    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    
    # Click login button
    page.wait_for_selector('button.login-button')
    page.click('button.login-button')
    
    # Wait for navigation after successful login
    page.wait_for_url(f"{base_url}/welcome")
    
    # Verify we're on the dashboard
    expect(page).to_have_url(f"{base_url}/welcome")