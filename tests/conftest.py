import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    """Fixture for UI testing with Playwright browser automation"""
    with sync_playwright() as p:
        is_ci = os.getenv('CI') == 'true'
        browser = p.chromium.launch(headless=is_ci)
        page = browser.new_page()
        yield page
        browser.close()
        
@pytest.fixture
def api_request_context():
    """Fixture for API testing with Playwright request context"""
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url="https://jsonplaceholder.typicode.com"
        )
        yield request_context
        request_context.dispose()