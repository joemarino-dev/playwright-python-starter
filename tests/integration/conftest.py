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

@pytest.fixture
def db_connection():
    """
    Provides a SQLite database connection for integration tests. 
    
    Automatically creates connection before test and closes after. 
    Uses row_factory for dict-like access to columns.
    """    
    # Path to test database
    db_path = os.path.join('tests', 'test_data.db')

    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        
    # Create connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create schema
    cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    account_balance REAL NOT NULL
                )
                ''')

    cursor.execute('''
                CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    transaction_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    from_account_id INTEGER,
                    to_account_id INTEGER,
                    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (from_account_id) REFERENCES users(id),
                    FOREIGN KEY (to_account_id) REFERENCES users(id)
                )
                ''')

    # Insert test data
    users_data = [
        (1, 'John Smith', 'john.smith@example.com', 1000.00),
        (2, 'Jane Doe', 'jane.doe@example.com', 500.00),
        (3, 'Bob Johnson', 'bob.johnson@example.com', 2000.00)
    ]

    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users_data)

    transactions_data = [
        (1, 1, 500.00, 'deposit', 'completed', None, None),
        (2, 1, 200.00, 'withdrawal', 'completed', None, None),
        (3, 2, 500.00, 'deposit', 'completed', None, None),
        (4, 2, 1500.00, 'deposit', 'pending', None, None),
        (5, 3, 2000.00, 'deposit', 'completed', None, None)
    ]

    cursor.executemany('''
        INSERT INTO transactions (id, user_id, amount, transaction_type, status, from_account_id, to_account_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', transactions_data)

    # Commit changes
    conn.commit()

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
    
    