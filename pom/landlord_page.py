from playwright.sync_api import Page, expect
from helpers.logger import TestLogger

class LandlordPage:
    """Page Object Model for Landlord pages.
    
    This class encapsulates all interactions with landlord-related pages,
    providing a clean interface for test cases to interact with the landlord interface.
    """
    
    def __init__(self, page: Page, base_url: str):
        """Initialize the LandlordPage with a Playwright page and base URL.
        
        Args:
            page (Page): Playwright page object
            base_url (str): Base URL of the application
        """
        self.page = page
        self.base_url = base_url
        self.logger = TestLogger("landlord_page")

    def navigate_to_login(self):
        """Navigate to the login page."""
        self.page.goto(f"{self.base_url}/login")

    def login(self, email: str, password: str):
        """Perform login with given credentials.
        
        Args:
            email (str): Landlord user email
            password (str): Landlord user password
        """
        self.page.fill('input[type="email"]', email)
        self.page.fill('input[type="password"]', password)
        self.page.click('button.login-button')
        self.page.wait_for_url(f"{self.base_url}/welcome")

    def navigate_to_page(self, path: str):
        """Navigate to a specific page and verify it loaded correctly.
        
        Args:
            path (str): Path to navigate to
        """
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("networkidle")
        expect(self.page).to_have_url(f"{self.base_url}{path}")
        self._verify_page_content()
    
    def navigate_to_page_and_redirect(self, path: str):
        """Navigate to a specific page and verify it loaded correctly.
        
        Args:
            path (str): Path to navigate to
        """
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("networkidle")
        self._verify_page_content()

    def _verify_page_content(self):
        """Verify that the page loaded without errors and has content."""
        expect(self.page.locator("text=Error")).not_to_be_visible()
        expect(self.page.locator("text=404")).not_to_be_visible()
        expect(self.page.locator("text=Not Found")).not_to_be_visible()
        expect(self.page.locator("body")).not_to_be_empty()

    # Navigation methods for specific pages
    def navigate_to_welcome(self):
        """Navigate to the welcome page."""
        self.navigate_to_page("/welcome")

    def navigate_to_property(self):
        """Navigate to the property page."""
        self.navigate_to_page("/property")

    def navigate_to_tenants(self):
        """Navigate to the tenants page."""
        self.navigate_to_page("/tenants")

    def navigate_to_expense(self):
        """Navigate to the expense page."""
        self.navigate_to_page("/expense")

    def navigate_to_income_history(self):
        """Navigate to the income/history page."""
        self.navigate_to_page("/income/history")

    def navigate_to_cashflow(self):
        """Navigate to the cashflow page."""
        self.navigate_to_page("/cashflow")

    def navigate_to_tasks(self):
        """Navigate to the tasks page."""
        self.navigate_to_page("/tasks")

    def navigate_to_user_profile(self):
        """Navigate to the user profile page."""
        self.navigate_to_page("/user/profile")

    def navigate_to_user_files(self):
        """Navigate to the user files page."""
        self.navigate_to_page("/user/files")

    def navigate_to_about(self):
        """Navigate to the about page."""
        self.navigate_to_page("/about")

    def navigate_to_news(self):
        """Navigate to the news page."""
        self.navigate_to_page("/news")

    def get_property_cards(self):
        """Get all property cards on the property page.
        
        Returns:
            List of property card elements
        """
        return self.page.locator('.property-card, [data-testid="property-card"], .card').all()

    def click_view_details(self, property_index: int = 0):
        """Click the 'View Details' button for a specific property.
        
        Args:
            property_index (int): Index of the property card (0-based)
        """
        property_cards = self.get_property_cards()
        if property_index >= len(property_cards):
            raise ValueError(f"Property index {property_index} is out of range. Found {len(property_cards)} properties.")
        
        # Look for view details button within the property card
        view_details_button = property_cards[property_index].locator(
            'button:has-text("View Details"), a:has-text("View Details"), [data-testid="view-details"]'
        ).first
        view_details_button.click()
        
        # Wait for navigation to property information page
        self.page.wait_for_url(f"{self.base_url}/Property/Information")

    def verify_property_information_tabs(self):
        """Verify that all tabs on the property information page are loading correctly.
        
        Returns:
            bool: True if all tabs are present and functional
        """
        # Wait for the page to load
        self.page.wait_for_load_state("networkidle")
        
        # Common tab selectors - adjust based on your actual implementation
        tab_selectors = [
            'button[role="tab"], .tab, [data-testid="tab"]',
            'a[role="tab"], .nav-link'
        ]
        
        tabs_found = False
        for selector in tab_selectors:
            tabs = self.page.locator(selector).all()
            if tabs:
                tabs_found = True
                self.logger.info(f"Found {len(tabs)} tabs with selector: {selector}")
                break
        
        if not tabs_found:
            self.logger.warning("No tabs found on property information page")
            return False
        
        # Verify that at least one tab is visible and clickable
        expect(self.page.locator(selector).first).to_be_visible()
        
        return True

    def click_property_tab(self, tab_name: str):
        """Click on a specific tab in the property information page.
        
        Args:
            tab_name (str): Name or text of the tab to click
        """
        tab_selector = f'button:has-text("{tab_name}"), a:has-text("{tab_name}"), [data-testid="tab-{tab_name.lower()}"]'
        self.page.click(tab_selector)
        self.page.wait_for_load_state("networkidle")

    def verify_property_list_loaded(self):
        """Verify that the property list page has loaded with properties.
        
        Returns:
            bool: True if properties are visible
        """
        # Wait for the page to load
        self.page.wait_for_load_state("networkidle")
        
        # Check for property cards or list items
        property_selectors = [
            '.property-card, [data-testid="property-card"], .card',
            '.property-item, [data-testid="property-item"]',
            '.property-list-item'
        ]
        
        for selector in property_selectors:
            properties = self.page.locator(selector).all()
            if properties:
                self.logger.info(f"Found {len(properties)} properties with selector: {selector}")
                return True
        
        self.logger.warning("No properties found on property list page")
        return False 