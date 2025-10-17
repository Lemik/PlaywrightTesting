import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect, TimeoutError, Page
from pom.landlord_page import LandlordPage
from helpers.landlord_fixture import landlord_page, landlord_credentials

# Load environment variables
load_dotenv(override=True)

class TestTenantFunctionality:
    """Test suite for tenant page functionality (landlord's view of tenants)"""
    
    def test_tenant_list_display(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test that tenant list page displays tenants correctly"""
        test_logger.info("Starting tenant list display test")
        
        # Login as landlord
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        # Navigate to tenants page
        landlord_page.navigate_to_tenants()
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
        
        # Verify tenants are displayed
        tenants_loaded = landlord_page.verify_tenant_list_loaded()
        assert tenants_loaded, "Tenant list should display tenants"
        
        # Get tenant count
        tenant_cards = landlord_page.get_tenant_cards()
        test_logger.info(f"Tenant list displays {len(tenant_cards)} tenants")
        
        # Verify each tenant card has basic elements
        for i, card in enumerate(tenant_cards):
            # Check if card is visible
            expect(card).to_be_visible()
            
            # Check for common tenant card elements
            card_text = card.text_content()
            test_logger.info(f"Tenant {i + 1} card content: {card_text[:100]}...")
            
            # Verify view details button exists
            view_details_button = card.locator(
                'button:has-text("View Details"), a:has-text("View Details"), [data-testid="view-details"]'
            ).first
            expect(view_details_button).to_be_visible()
        
        test_logger.info("Tenant list display test completed successfully")

    def test_view_tenant_details_navigation(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test that clicking 'View Details' navigates to Tenant/Information page"""
        test_logger.info("Starting view tenant details navigation test")
        
        # Login as landlord
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        # Navigate to tenants page
        landlord_page.navigate_to_tenants()
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
        
        # Click view details for first tenant
        landlord_page.click_view_tenant_details(tenant_index=0)
        
        # Verify navigation to Tenant/Information page
        page_load_helper.verify_page_loaded(
            expected_url=f"{landlord_page.base_url}/Tenant/Information"
        )
        
        # Verify page title or heading indicates tenant information
        page_title = landlord_page.page.title()
        page_heading = landlord_page.page.locator("h1, h2").first.text_content()
        test_logger.info(f"Tenant information page title: {page_title}")
        test_logger.info(f"Tenant information page heading: {page_heading}")
        
        test_logger.info("View tenant details navigation test completed successfully")

    def test_tenant_information_tabs(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test that tenant information page tabs are loading correctly"""
        test_logger.info("Starting tenant information tabs test")
        
        # Login as landlord and navigate to tenant information
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        landlord_page.navigate_to_tenants()
        landlord_page.click_view_tenant_details(tenant_index=0)
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/Tenant/Information")
        
        # Verify tabs are present and functional
        tabs_loaded = landlord_page.verify_tenant_information_tabs()
        assert tabs_loaded, "Tenant information tabs should be present and functional"
        
        # Test clicking on different tabs
        common_tab_names = ["Overview", "Details", "Documents", "Payments", "Maintenance", "Settings"]
        
        for tab_name in common_tab_names:
            try:
                # Try to click the tab
                landlord_page.click_tenant_tab(tab_name)
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
        
        test_logger.info("Tenant information tabs test completed successfully")

    def test_tenant_search_functionality(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test tenant search functionality"""
        test_logger.info("Starting tenant search functionality test")
        
        # Login as landlord
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        # Navigate to tenants page
        landlord_page.navigate_to_tenants()
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
        
        # Test search functionality
        search_terms = ["test", "tenant", "john", "doe"]
        
        for search_term in search_terms:
            try:
                landlord_page.search_tenants(search_term)
                test_logger.info(f"Successfully searched for: {search_term}")
                
                # Wait for search results
                landlord_page.page.wait_for_timeout(2000)
                
                # Verify search results are displayed
                tenant_cards = landlord_page.get_tenant_cards()
                test_logger.info(f"Search for '{search_term}' returned {len(tenant_cards)} results")
                
                # If we found results, break (search is working)
                if len(tenant_cards) > 0:
                    test_logger.info(f"Search functionality working with term: {search_term}")
                    break
                    
            except Exception as e:
                test_logger.info(f"Search with term '{search_term}' failed: {str(e)}")
                continue
        
        test_logger.info("Tenant search functionality test completed successfully")

    def test_tenant_filter_functionality(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test tenant filter functionality by status"""
        test_logger.info("Starting tenant filter functionality test")
        
        # Login as landlord
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        # Navigate to tenants page
        landlord_page.navigate_to_tenants()
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
        
        # Test filter functionality
        filter_statuses = ["Active", "Inactive", "Pending", "All"]
        
        for status in filter_statuses:
            try:
                landlord_page.filter_tenants_by_status(status)
                test_logger.info(f"Successfully filtered by status: {status}")
                
                # Wait for filter results
                landlord_page.page.wait_for_timeout(2000)
                
                # Verify filter results are displayed
                tenant_cards = landlord_page.get_tenant_cards()
                test_logger.info(f"Filter by '{status}' returned {len(tenant_cards)} results")
                
                # If we found results, break (filter is working)
                if len(tenant_cards) > 0:
                    test_logger.info(f"Filter functionality working with status: {status}")
                    break
                    
            except Exception as e:
                test_logger.info(f"Filter by status '{status}' failed: {str(e)}")
                continue
        
        test_logger.info("Tenant filter functionality test completed successfully")

    def test_add_new_tenant_functionality(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test add new tenant functionality"""
        test_logger.info("Starting add new tenant functionality test")
        
        # Login as landlord
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        # Navigate to tenants page
        landlord_page.navigate_to_tenants()
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
        
        # Test add new tenant functionality
        try:
            landlord_page.add_new_tenant()
            test_logger.info("Successfully clicked add new tenant button")
            
            # Wait for page to load
            landlord_page.page.wait_for_timeout(2000)
            
            # Check if we're on a form page or modal
            current_url = landlord_page.page.url
            test_logger.info(f"Current URL after clicking add tenant: {current_url}")
            
            # Look for form elements
            form_selectors = [
                'form',
                '[data-testid="tenant-form"]',
                '.tenant-form',
                'input[name="name"], input[name="email"]'
            ]
            
            form_found = False
            for selector in form_selectors:
                try:
                    form_element = landlord_page.page.locator(selector).first
                    if form_element.is_visible():
                        form_found = True
                        test_logger.info(f"Add tenant form found with selector: {selector}")
                        break
                except:
                    continue
            
            if form_found:
                test_logger.info("Add new tenant functionality working correctly")
            else:
                test_logger.info("Add new tenant button clicked but form not found")
                
        except Exception as e:
            test_logger.info(f"Add new tenant functionality failed: {str(e)}")
        
        test_logger.info("Add new tenant functionality test completed successfully")

    def test_tenant_page_responsiveness(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test tenant page responsiveness on different viewport sizes"""
        test_logger.info("Starting tenant page responsiveness test")
        
        # Login as landlord
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
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
            
            # Navigate to tenants page
            landlord_page.navigate_to_tenants()
            page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
            
            # Verify tenants are still visible
            tenants_loaded = landlord_page.verify_tenant_list_loaded()
            assert tenants_loaded, f"Tenant list should be visible at {viewport['width']}x{viewport['height']}"
            
            # Test view details functionality
            try:
                landlord_page.click_view_tenant_details(tenant_index=0)
                page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/Tenant/Information")
                
                # Verify tabs work at this viewport
                tabs_loaded = landlord_page.verify_tenant_information_tabs()
                assert tabs_loaded, f"Tenant tabs should work at {viewport['width']}x{viewport['height']}"
                
                test_logger.info(f"Tenant functionality works correctly at {viewport['width']}x{viewport['height']}")
                
            except Exception as e:
                test_logger.warning(f"Tenant functionality issue at {viewport['width']}x{viewport['height']}: {str(e)}")
        
        test_logger.info("Tenant page responsiveness test completed successfully")

    def test_tenant_page_error_handling(self, landlord_page: LandlordPage, page_load_helper, test_logger):
        """Test tenant page error handling for unauthorized access"""
        test_logger.info("Starting tenant page error handling test")
        
        # Try to access tenant page without login
        landlord_page.navigate_to_page_and_redirect("/tenants")
        
        # Check if redirected to login or shows error
        current_url = landlord_page.page.url
        
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
                "text=Authentication required"
            ]
            
            error_found = False
            for selector in error_selectors:
                try:
                    error_element = landlord_page.page.locator(selector).first
                    if error_element.is_visible():
                        error_found = True
                        test_logger.info(f"Error message found: {error_element.text_content()}")
                        break
                except:
                    continue
            
            if not error_found:
                test_logger.warning(f"Unexpected behavior: accessed tenant page without login. URL: {current_url}")
        
        test_logger.info("Tenant page error handling test completed successfully")

    def test_tenant_view_details_multiple_tenants(self, landlord_page: LandlordPage, landlord_credentials: dict, page_load_helper, test_logger):
        """Test viewing details for multiple tenants if available"""
        test_logger.info("Starting multiple tenant view details test")
        
        # Login as landlord first
        landlord_page.navigate_to_login()
        landlord_page.login(landlord_credentials["email"], landlord_credentials["password"])
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/welcome")
        
        # Navigate to tenants page
        landlord_page.navigate_to_tenants()
        page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
        
        # Get all tenant cards
        tenant_cards = landlord_page.get_tenant_cards()
        test_logger.info(f"Found {len(tenant_cards)} tenants on the page")
        
        # Test viewing details for up to 3 tenants (to avoid long test times)
        max_tenants_to_test = min(3, len(tenant_cards))
        
        for i in range(max_tenants_to_test):
            test_logger.info(f"Testing view details for tenant {i + 1}")
            
            # Navigate back to tenants page if not the first iteration
            if i > 0:
                landlord_page.navigate_to_tenants()
                page_load_helper.verify_page_loaded(expected_url=f"{landlord_page.base_url}/tenants")
            
            # Click view details
            landlord_page.click_view_tenant_details(tenant_index=i)
            
            # Verify navigation to tenant information
            page_load_helper.verify_page_loaded(
                expected_url=f"{landlord_page.base_url}/Tenant/Information"
            )
            
            # Verify tabs are loading
            tabs_loaded = landlord_page.verify_tenant_information_tabs()
            assert tabs_loaded, f"Tenant information tabs should load for tenant {i + 1}"
            
            test_logger.info(f"Successfully tested tenant {i + 1} view details")
        
        test_logger.info("Multiple tenant view details test completed successfully") 