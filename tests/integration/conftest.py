"""
Integration Test Fixtures

Provides fixtures specific to integration testing:
- db_connection: SQLite database connection
- flask_server: Flask API server (runs in background thread)
"""

import sqlite3
import os
import threading
import time

import pytest

from .api_server import app
from .setup_test_db import create_test_database

@pytest.fixture
def db_connection():
    """
    Provides a SQLite database connection for integration tests. 
    
    Automatically creates connection before test and closes after. 
    Uses row_factory for dict-like access to columns.
    """    
    # Path to test database
    db_path = os.path.join('tests', 'test_data.db')

    # Create fresh database (handles schema + data)
    create_test_database(db_path)
        
    # Create connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Provide connection to test
    yield conn

    # Cleanup: Close connection after test
    conn.close()
        
@pytest.fixture
def flask_server():
    """
    Starts Flask API server in a background thread for integration testing. 
    
    The server runs on http://localhost:5001 during the test,
    then automatically shuts down after the test completes.
    """
    
    # Configure Flask for testing
    app.config['Testing'] = True
    
    # Start server in a background thread
    server_thread = threading.Thread(
        target=lambda: app.run(port=5001, debug=False, use_reloader=False)
    )
    server_thread.daemon = True # Thread dies when main program exits
    server_thread.start()
    
    # Wait for server to start (give it 2 seconds)
    time.sleep(2)
    
    # Provide server URL to test
    yield "http://localhost:5001"
    
    # Cleanup: Server automatically stops when thread ends (daemon=True)
    
    