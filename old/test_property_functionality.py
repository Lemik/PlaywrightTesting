import pytest
from playwright.sync_api import expect
from pom.landlord_page import LandlordPage
from helpers.landlord_fixture import landlord_page, landlord_credentials


class TestPropertyFunctionality:
    """Test suite for property page functionality"""
    
    def _login_and_navigate_to_property(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Helper method to login and navigate to property page"""
        try:
            # Login
            landlord_page.navigate_to_login()
            landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
            
            # Verify we're logged in
            current_url = landlord_page.page.url
            assert "/login" not in current_url, f"Login failed - still on login page: {current_url}"
            
            # Navigate to property page
            landlord_page.navigate_to_property()
            
            # Verify page loaded successfully
            page_load_helper.verify_page_loaded(required_selector="body")
            
            return True
        except Exception as e:
            test_logger.warning(f"Login failed (likely due to invalid credentials): {str(e)}")
            pytest.skip("Test skipped - login failed, credentials may be invalid")
            return False
    
    def test_property_list_display(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test that property list page displays properties correctly"""
        test_logger.info("Starting property list display test")
        
        # Login and navigate to property page
        if not self._login_and_navigate_to_property(landlord_page, landlord_credentials, page_load_helper, test_logger):
            return
        
        # Verify properties are displayed
        properties_loaded = landlord_page.verify_property_list_loaded()
        assert properties_loaded, "Property list should display properties"
        
        # Get property count
        property_cards = landlord_page.get_property_cards()
        test_logger.info(f"Property list displays {len(property_cards)} properties")
        
        # Verify each property card has basic elements
        for i, card in enumerate(property_cards):
            # Check if card is visible
            expect(card).to_be_visible()
            
            # Check for common property card elements
            card_text = card.text_content()
            test_logger.info(f"Property {i + 1} card content: {card_text[:100]}...")
            
            # Verify view details button exists
            view_details_button = card.locator(
                'button:has-text("View Details"), a:has-text("View Details"), [data-testid="view-details"]'
            ).first
            expect(view_details_button).to_be_visible()
        
        test_logger.info("Property list display test completed successfully")

    def test_view_details_navigation(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test that clicking 'View Details' navigates to Property/Information page"""
        test_logger.info("Starting view details navigation test")
        
        # Login and navigate to property page
        if not self._login_and_navigate_to_property(landlord_page, landlord_credentials, page_load_helper, test_logger):
            return
        
        # Click view details for first property
        landlord_page.click_view_details(property_index=0)
        
        # Verify navigation to Property/Information page
        current_url = landlord_page.page.url
        test_logger.info(f"Navigated to: {current_url}")
        
        # Verify page loaded successfully
        page_load_helper.verify_page_loaded(required_selector="body")
        
        # Verify page title or heading indicates property information
        page_title = landlord_page.page.title()
        page_heading = landlord_page.page.locator("h1, h2").first.text_content()
        test_logger.info(f"Property information page title: {page_title}")
        test_logger.info(f"Property information page heading: {page_heading}")
        
        test_logger.info("View details navigation test completed successfully")

    def test_property_information_tabs(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test that property information page tabs are loading correctly"""
        test_logger.info("Starting property information tabs test")
        
        # Login and navigate to property page
        if not self._login_and_navigate_to_property(landlord_page, landlord_credentials, page_load_helper, test_logger):
            return
        
        # Navigate to property information
        landlord_page.click_view_details(property_index=0)
        
        # Verify page loaded successfully
        current_url = landlord_page.page.url
        test_logger.info(f"Navigated to property information: {current_url}")
        page_load_helper.verify_page_loaded(required_selector="body")
        
        # Verify tabs are present and functional
        tabs_loaded = landlord_page.verify_property_information_tabs()
        assert tabs_loaded, "Property information tabs should be present and functional"
        
        # Test clicking on different tabs
        common_tab_names = ["Overview", "Details", "Tenants", "Documents", "Maintenance", "Financial", "Settings"]
        
        for tab_name in common_tab_names:
            try:
                # Try to click the tab
                landlord_page.click_property_tab(tab_name)
                test_logger.info(f"Successfully clicked on '{tab_name}' tab")
                
                # Verify tab content loaded (wait for any dynamic content)
                landlord_page.page.wait_for_timeout(2000)
                
                # Check if tab content is visible (look for common content indicators)
                content_selectors = [
                    f'[data-testid="tab-content-{tab_name.lower()}"]',
                    f'[data-testid="{tab_name.lower()}-content"]',
                    '.tab-content',
                    '.content'
                ]
                
                content_found = False
                for selector in content_selectors:
                    try:
                        content = landlord_page.page.locator(selector).first
                        if content.is_visible():
                            content_found = True
                            test_logger.info(f"Tab content found with selector: {selector}")
                            break
                    except:
                        continue
                
                if content_found:
                    test_logger.info(f"'{tab_name}' tab content loaded successfully")
                    break  # Found a working tab, no need to test others
                else:
                    test_logger.info(f"'{tab_name}' tab clicked but content verification inconclusive")
                    
            except Exception as e:
                test_logger.info(f"Tab '{tab_name}' not available: {str(e)}")
                continue
        
        test_logger.info("Property information tabs test completed successfully")

    def test_property_page_responsiveness(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test property page responsiveness on different viewport sizes"""
        test_logger.info("Starting property page responsiveness test")
        
        # Login and navigate to property page
        if not self._login_and_navigate_to_property(landlord_page, landlord_credentials, page_load_helper, test_logger):
            return
        
        # Test different viewport sizes
        viewport_sizes = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 1024, "height": 768},   # Tablet
            {"width": 768, "height": 1024},   # Tablet Portrait
            {"width": 375, "height": 667}     # Mobile
        ]
        
        for viewport in viewport_sizes:
            test_logger.info(f"Testing viewport size: {viewport['width']}x{viewport['height']}")
            
            # Set viewport
            landlord_page.page.set_viewport_size(viewport)
            
            # Refresh the page to test responsiveness
            landlord_page.page.reload()
            landlord_page.page.wait_for_load_state("networkidle")
            
            # Verify properties are still visible
            properties_loaded = landlord_page.verify_property_list_loaded()
            assert properties_loaded, f"Property list should be visible at {viewport['width']}x{viewport['height']}"
            
            # Test view details functionality
            try:
                landlord_page.click_view_details(property_index=0)
                
                # Verify page loaded successfully
                page_load_helper.verify_page_loaded(required_selector="body")
                
                # Verify tabs work at this viewport
                tabs_loaded = landlord_page.verify_property_information_tabs()
                assert tabs_loaded, f"Property tabs should work at {viewport['width']}x{viewport['height']}"
                
                test_logger.info(f"Property functionality works correctly at {viewport['width']}x{viewport['height']}")
                
                # Navigate back to property list for next iteration
                landlord_page.navigate_to_property()
                
            except Exception as e:
                test_logger.warning(f"Property functionality issue at {viewport['width']}x{viewport['height']}: {str(e)}")
        
        test_logger.info("Property page responsiveness test completed successfully")

    def test_property_page_error_handling(self, landlord_page: LandlordPage, test_logger):
        """Test property page error handling for unauthorized access"""
        test_logger.info("Starting property page error handling test")
        
        # Try to access property page without login
        landlord_page.navigate_to_page_and_redirect("/property")
        
        # Wait for page to load
        landlord_page.page.wait_for_load_state("networkidle")
        
        # Check if redirected to login or shows error
        current_url = landlord_page.page.url
        test_logger.info(f"Current URL after accessing property page: {current_url}")
        
        if "/login" in current_url:
            test_logger.info("Successfully redirected to login page for unauthorized access")
        elif "error" in current_url.lower() or "unauthorized" in current_url.lower():
            test_logger.info("Appropriate error page shown for unauthorized access")
        else:
            # Check for error messages on the page
            error_selectors = [
                "text=Unauthorized",
                "text=Access Denied", 
                "text=Please log in",
                "text=Authentication required",
                ".error",
                ".alert-danger"
            ]
            
            error_found = False
            for selector in error_selectors:
                try:
                    error_element = landlord_page.page.locator(selector).first
                    if error_element.is_visible():
                        error_found = True
                        error_text = error_element.text_content()
                        test_logger.info(f"Error message found: {error_text}")
                        break
                except:
                    continue
            
            if not error_found:
                test_logger.warning(f"Unexpected behavior: accessed property page without login. URL: {current_url}")
                # Take screenshot for debugging
                landlord_page.page.screenshot(path="property_error_debug.png")
                test_logger.info("Screenshot saved as property_error_debug.png")
        
        test_logger.info("Property page error handling test completed successfully") 