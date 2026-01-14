import sqlite3
import os

def create_test_database(db_path='tests/test_data.db'):
    """
    Creates a fresh test database with schema and sample data.
    Can be called from fixtures or run standalone.
    """
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
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

    # Commit and close
    conn.commit()
    conn.close()
    
    return db_path

    if __name__ == '__main__':
        print(f"Test database created successfully at: {db_path}")
        print("Tables created: users, transactions")
        print(f"Users inserted: {len(users_data)}")
        print(f"Transactions inserted: {len(transactions_data)}")
        print("\nInitial account balances:")
        print("  John Smith: $1000.00")
        print("  Jane Doe: $500.00")
        print("  Bob Johnson: $2000.00")
        print("  TOTAL SYSTEM: $3500.00")