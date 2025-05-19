from playwright.sync_api import Page, expect

class AdminPage:
    """Page Object Model for Admin pages.
    
    This class encapsulates all interactions with admin-related pages,
    providing a clean interface for test cases to interact with the admin interface.
    """
    
    def __init__(self, page: Page, base_url: str):
        """Initialize the AdminPage with a Playwright page and base URL.
        
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
            email (str): Admin user email
            password (str): Admin user password
        """
        self.page.fill('input[type="email"]', email)
        self.page.fill('input[type="password"]', password)
        self.page.click('button.login-button')
        self.page.wait_for_url(f"{self.base_url}/welcome")

    def navigate_to_page(self, path: str):
        """Navigate to a specific page and verify it loaded correctly.
        
        Args:
            path (str): Path to navigate to (e.g., '/status', '/stats')
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