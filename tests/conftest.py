import pytest
import sqlite3
import os
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()
        
@pytest.fixture
def api_request_context():
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url="https://jsonplaceholder.typicode.com"
        )
        yield request_context
        
@pytest.fixture
def db_connection():
    # Path to test database
    db_path = os.path.join(os.path.dirname(__file__), 'test_data.db')
    
    # Create connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    
    yield conn
    
    # Cleanup
    conn.close()