from playwright.sync_api import expect

def test_has_body(page):
    page.goto("https://example.com")
    
