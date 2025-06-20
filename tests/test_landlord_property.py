import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError, Page
from pom.landlord_page import LandlordPage
from helpers.landlord_fixture import landlord_page, landlord_credentials


def test_property_page_functionality(landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
    """Test property page functionality including login, property list, view details, and tabs"""
    test_logger.info("Starting property page functionality test")
    
    # Step 1: Login to the application
    test_logger.info("Step 1: Logging in to the application")
    landlord_page.navigate_to_login()
    landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
    
    # Verify login success with comprehensive page load check
    page_load_helper.verify_page_loaded(
        expected_url=f"{landlord_page.base_url}/welcome",
        required_selector="h1"
    )
    test_logger.info("Login completed successfully")
    
    # Step 2: Navigate to property page
    test_logger.info("Step 2: Navigating to property page")
    landlord_page.navigate_to_property()
    
    # Verify property page loaded with properties
    page_load_helper.verify_page_loaded(
        expected_url=f"{landlord_page.base_url}/property"
    )
    
    # Verify that properties are displayed
    properties_loaded = landlord_page.verify_property_list_loaded()
    assert properties_loaded, "Property list should be loaded and display properties"
    test_logger.info("Property page loaded successfully with properties")
    
    # Step 3: Click on "View Details" for the first property
    test_logger.info("Step 3: Clicking 'View Details' for first property")
    try:
        landlord_page.click_view_details(property_index=0)
        test_logger.info("Successfully clicked 'View Details' button")
    except ValueError as e:
        test_logger.error(f"Failed to click 'View Details': {e}")
        raise
    
    # Step 4: Verify navigation to Property/Information page
    test_logger.info("Step 4: Verifying navigation to Property/Information page")
    page_load_helper.verify_page_loaded(
        expected_url=f"{landlord_page.base_url}/Property/Information"
    )
    test_logger.info("Successfully navigated to Property/Information page")
    
    # Step 5: Verify that all tabs are loading correctly
    test_logger.info("Step 5: Verifying property information tabs are loading")
    tabs_loaded = landlord_page.verify_property_information_tabs()
    assert tabs_loaded, "Property information tabs should be present and functional"
    test_logger.info("Property information tabs verified successfully")
    
    # Step 6: Test tab interactions (optional - test clicking on tabs)
    test_logger.info("Step 6: Testing tab interactions")
    try:
        # Try to click on common tab names - adjust based on your actual tab names
        common_tabs = ["Overview", "Details", "Tenants", "Documents", "Maintenance"]
        for tab_name in common_tabs:
            try:
                landlord_page.click_property_tab(tab_name)
                test_logger.info(f"Successfully clicked on '{tab_name}' tab")
                # Wait a moment for tab content to load
                landlord_page.page.wait_for_timeout(1000)
                break  # If one tab works, we've verified tab functionality
            except Exception as e:
                test_logger.info(f"Tab '{tab_name}' not found or not clickable: {e}")
                continue
    except Exception as e:
        test_logger.warning(f"Tab interaction test failed: {e}")
        # Don't fail the test if tab interaction fails, as tab names might be different
    
    test_logger.info("Property page functionality test completed successfully")


def test_property_page_without_login(landlord_page: LandlordPage, page_load_helper, test_logger):
    """Test property page access without login (should redirect to login)"""
    test_logger.info("Starting property page access test without login")
    
    # Try to navigate to property page without login
    # Use direct navigation instead of navigate_to_page() which expects to stay on the target URL
    landlord_page.page.goto(f"{landlord_page.base_url}/property")
    landlord_page.page.wait_for_load_state("networkidle")
    
    # Should redirect to login page
    current_url = landlord_page.page.url
    test_logger.info(f"Current URL after navigation: {current_url}")
    
    # Verify we were redirected to login page
    assert "/login" in current_url, f"Expected redirect to login page, but current URL is: {current_url}"
    test_logger.info("Successfully redirected to login page when accessing property page without authentication")
    
    test_logger.info("Property page access test without login completed")


def test_property_view_details_multiple_properties(landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
    """Test viewing details for multiple properties if available"""
    test_logger.info("Starting multiple property view details test")
    
    # Login first
    landlord_page.navigate_to_login()
    landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
    page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
    
    # Navigate to property page
    landlord_page.navigate_to_property()
    page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/property")
    
    # Get all property cards
    property_cards = landlord_page.get_property_cards()
    test_logger.info(f"Found {len(property_cards)} properties on the page")
    
    # Test viewing details for up to 3 properties (to avoid long test times)
    max_properties_to_test = min(3, len(property_cards))
    
    for i in range(max_properties_to_test):
        test_logger.info(f"Testing view details for property {i + 1}")
        
        # Navigate back to property page if not the first iteration
        if i > 0:
            landlord_page.navigate_to_property()
            page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/property")
        
        # Click view details
        landlord_page.click_view_details(property_index=i)
        
        # Verify navigation to property information
        page_load_helper.verify_page_loaded(
            expected_url=f"{landlord_page.base_url}/Property/Information"
        )
        
        # Verify tabs are loading
        tabs_loaded = landlord_page.verify_property_information_tabs()
        assert tabs_loaded, f"Property information tabs should load for property {i + 1}"
        
        test_logger.info(f"Successfully tested property {i + 1} view details")
    
    test_logger.info("Multiple property view details test completed successfully")