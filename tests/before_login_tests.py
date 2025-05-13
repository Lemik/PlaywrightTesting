from playwright.sync_api import expect

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