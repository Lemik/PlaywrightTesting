import datetime
from playwright.sync_api import expect
import time

def test_homepage_title(page, base_url):
    """Test that the homepage loads and has the correct title"""
    page.goto(base_url)
    expect(page).to_have_title("LLHUB")


def test_navigation(page, base_url):
    """Test basic navigation functionality"""
    page.goto(base_url)
    page.click("text=About Us")
    expect(page).to_have_url(f"{base_url}/about")
    expect(page).to_have_title("LLHUB")

def test_form_submission(page, base_url):
    """Test form submission functionality"""
    page.goto(f"{base_url}/ContactUs")
    
    # Fill out a form
    page.fill("#formName", "John Doe")
    page.fill("#formEmail", "john@example.com")
    page.fill("#formMessage", f"This is a test run for LLhub {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Submit the form
    page.click("button[type='submit']")

    # Print browser console logs after submission
    def log_console(msg):
        print(f"BROWSER LOG: {msg.type}: {msg.text}")
    page.on("console", log_console)

    # Wait for the submit button to become enabled again (max 10s)
    start = time.time()
    while True:
        if not page.locator("button[type='submit']").is_disabled():
            break
        if time.time() - start > 10:
            raise TimeoutError("Submit button did not become enabled within 10 seconds")
        time.sleep(0.1)

    # Debug: Print page content to see what's rendered
    print("Page content after submission:", page.content())
    
    # Assert success message - wait for toast with success class
    expect(page.locator(".Toastify__toast")).to_be_visible(timeout=10000)