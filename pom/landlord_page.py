from playwright.sync_api import Page, expect

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