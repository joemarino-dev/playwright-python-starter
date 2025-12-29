from playwright.sync_api import Page, expect

def test_has_heading(page: Page):
    page.goto("https://example.com")
    heading = page.get_by_role("heading", name="Example Domain")
    expect(heading).to_have_text("Example Domain") 
