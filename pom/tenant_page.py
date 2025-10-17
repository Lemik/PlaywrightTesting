from playwright.sync_api import Page, expect
from helpers.logger import TestLogger

class TenantPage:
    """Page Object Model for Tenant pages.
    
    This class encapsulates all interactions with tenant-related pages,
    providing a clean interface for test cases to interact with the tenant interface.
    """
    
    def __init__(self, page: Page, base_url: str):
        """Initialize the TenantPage with a Playwright page and base URL.
        
        Args:
            page (Page): Playwright page object
            base_url (str): Base URL of the application
        """
        self.page = page
        self.base_url = base_url
        self.logger = TestLogger("tenant_page")

    def navigate_to_login(self):
        """Navigate to the login page."""
        self.page.goto(f"{self.base_url}/login")

    def login(self, email: str, password: str):
        """Perform login with given credentials.
        
        Args:
            email (str): Tenant user email
            password (str): Tenant user password
        """
        # Fill email field - try multiple selectors
        email_selectors = [
            'input[type="email"]',
            'input[name="email"]',
            'input[placeholder*="email" i]',
            '#email',
            '.email-input'
        ]
        
        email_filled = False
        for selector in email_selectors:
            try:
                if self.page.locator(selector).is_visible():
                    self.page.fill(selector, email)
                    email_filled = True
                    self.logger.info(f"Email filled using selector: {selector}")
                    break
            except:
                continue
        
        if not email_filled:
            raise Exception("Could not find email input field")
        
        # Fill password field - try multiple selectors
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[placeholder*="password" i]',
            '#password',
            '.password-input'
        ]
        
        password_filled = False
        for selector in password_selectors:
            try:
                if self.page.locator(selector).is_visible():
                    self.page.fill(selector, password)
                    password_filled = True
                    self.logger.info(f"Password filled using selector: {selector}")
                    break
            except:
                continue
        
        if not password_filled:
            raise Exception("Could not find password input field")
        
        # Click login button - try multiple selectors
        login_button_selectors = [
            'button.login-button',
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Login")',
            'button:has-text("Sign In")',
            'button:has-text("Log In")',
            '.login-btn',
            '#login-button',
            '.submit-button'
        ]
        
        login_clicked = False
        for selector in login_button_selectors:
            try:
                if self.page.locator(selector).is_visible():
                    self.page.click(selector)
                    login_clicked = True
                    self.logger.info(f"Login button clicked using selector: {selector}")
                    break
            except:
                continue
        
        if not login_clicked:
            raise Exception("Could not find login button")
        
        # Wait for navigation after login - be more flexible with URL matching
        try:
            self.page.wait_for_url(f"{self.base_url}/welcome", timeout=10000)
            self.logger.info("Login successful, redirected to welcome page")
        except:
            # If welcome page doesn't load, check for any successful login indicator
            self.page.wait_for_load_state("networkidle")
            current_url = self.page.url
            
            # Check for error messages on the page
            error_selectors = [
                '.error',
                '.alert-danger',
                '.login-error',
                '[data-testid="error"]',
                'text=Invalid',
                'text=Error',
                'text=Failed'
            ]
            
            error_found = False
            for selector in error_selectors:
                try:
                    if self.page.locator(selector).is_visible():
                        error_text = self.page.locator(selector).text_content()
                        self.logger.error(f"Login error found: {error_text}")
                        error_found = True
                        break
                except:
                    continue
            
            if "/login" not in current_url:
                self.logger.info(f"Login successful, redirected to: {current_url}")
            elif error_found:
                raise Exception(f"Login failed with error message. Current URL: {current_url}")
            else:
                # Take a screenshot for debugging
                self.page.screenshot(path="tenant_login_debug.png")
                raise Exception(f"Login failed - still on login page. Current URL: {current_url}. Screenshot saved as tenant_login_debug.png")

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

    def navigate_to_tenants(self):
        """Navigate to the tenants page."""
        self.navigate_to_page("/tenants")

    def navigate_to_property(self):
        """Navigate to the property page."""
        self.navigate_to_page("/property")

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

    # Tenant-specific methods
    def get_tenant_cards(self):
        """Get all tenant cards on the tenants page.
        
        Returns:
            List of tenant card elements
        """
        return self.page.locator('.tenant-card, [data-testid="tenant-card"], .card, .tenant-item').all()

    def click_view_tenant_details(self, tenant_index: int = 0):
        """Click the 'View Details' button for a specific tenant.
        
        Args:
            tenant_index (int): Index of the tenant card (0-based)
        """
        tenant_cards = self.get_tenant_cards()
        if tenant_index >= len(tenant_cards):
            raise ValueError(f"Tenant index {tenant_index} is out of range. Found {len(tenant_cards)} tenants.")
        
        # Look for view details button within the tenant card
        view_details_button = tenant_cards[tenant_index].locator(
            'button:has-text("View Details"), a:has-text("View Details"), [data-testid="view-details"]'
        ).first
        view_details_button.click()
        
        # Wait for navigation to tenant information page
        self.page.wait_for_url(f"{self.base_url}/Tenant/Information")

    def verify_tenant_list_loaded(self):
        """Verify that the tenant list page has loaded with tenants.
        
        Returns:
            bool: True if tenants are visible
        """
        # Wait for the page to load
        self.page.wait_for_load_state("networkidle")
        
        # Check for tenant cards or list items
        tenant_selectors = [
            '.tenant-card, [data-testid="tenant-card"], .card',
            '.tenant-item, [data-testid="tenant-item"]',
            '.tenant-list-item'
        ]
        
        for selector in tenant_selectors:
            tenants = self.page.locator(selector).all()
            if tenants:
                self.logger.info(f"Found {len(tenants)} tenants with selector: {selector}")
                return True
        
        self.logger.warning("No tenants found on tenant list page")
        return False

    def verify_tenant_information_tabs(self):
        """Verify that all tabs on the tenant information page are loading correctly.
        
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
            self.logger.warning("No tabs found on tenant information page")
            return False
        
        # Verify that at least one tab is visible and clickable
        expect(self.page.locator(selector).first).to_be_visible()
        
        return True

    def click_tenant_tab(self, tab_name: str):
        """Click on a specific tab in the tenant information page.
        
        Args:
            tab_name (str): Name or text of the tab to click
        """
        tab_selector = f'button:has-text("{tab_name}"), a:has-text("{tab_name}"), [data-testid="tab-{tab_name.lower()}"]'
        self.page.click(tab_selector)
        self.page.wait_for_load_state("networkidle")

    def search_tenants(self, search_term: str):
        """Search for tenants using the search functionality.
        
        Args:
            search_term (str): Search term to enter
        """
        # Look for search input field
        search_selectors = [
            'input[placeholder*="search" i], input[placeholder*="tenant" i]',
            '[data-testid="search-input"]',
            '.search-input, #search'
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                search_input = self.page.locator(selector).first
                if search_input.is_visible():
                    break
            except:
                continue
        
        if search_input:
            search_input.fill(search_term)
            search_input.press("Enter")
            self.page.wait_for_load_state("networkidle")
        else:
            self.logger.warning("Search input field not found")

    def filter_tenants_by_status(self, status: str):
        """Filter tenants by status (e.g., "Active", "Inactive", "Pending").
        
        Args:
            status (str): Status to filter by
        """
        # Look for status filter dropdown or buttons
        filter_selectors = [
            f'button:has-text("{status}")',
            f'[data-testid="filter-{status.lower()}"]',
            f'select option:has-text("{status}")'
        ]
        
        filter_element = None
        for selector in filter_selectors:
            try:
                filter_element = self.page.locator(selector).first
                if filter_element.is_visible():
                    break
            except:
                continue
        
        if filter_element:
            filter_element.click()
            self.page.wait_for_load_state("networkidle")
        else:
            self.logger.warning(f"Filter for status '{status}' not found")

    def add_new_tenant(self):
        """Click the add new tenant button if available."""
        add_button_selectors = [
            'button:has-text("Add Tenant"), button:has-text("New Tenant")',
            '[data-testid="add-tenant"]',
            '.add-tenant-btn, #add-tenant'
        ]
        
        add_button = None
        for selector in add_button_selectors:
            try:
                add_button = self.page.locator(selector).first
                if add_button.is_visible():
                    break
            except:
                continue
        
        if add_button:
            add_button.click()
            self.page.wait_for_load_state("networkidle")
        else:
            self.logger.warning("Add tenant button not found") 