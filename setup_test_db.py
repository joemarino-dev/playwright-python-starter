import sqlite3
import os

# Path to test database
db_path = os.path.join('tests', 'test_data.db')

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
                  FOREIGN KEY (user_id) REFERENCES users(id)
              )
              ''')

# Insert test data
users_data = [
    (1, 'John Smith', 'john.smith@example.com', 50000.00),
    (2, 'Jane Doe', 'jane.doe@example.com', 75000.00),
    (3, 'Bob Johnson', 'bob.johnson@example.com', 100000.00)
]

cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users_data)

transactions_data = [
    (1, 1, 1000.00, 'deposit', 'completed'),
    (2, 1, 500.00, 'withdrawal', 'completed'),
    (3, 2, 2000.00, 'deposit', 'completed'),
    (4, 2, 1500.00, 'deposit', 'pending'),
    (5, 3, 5000.00, 'withdrawal', 'completed')
]

cursor.executemany('INSERT INTO transactions VALUES (?, ?, ?, ?, ?)', transactions_data)

# Commit and close
conn.commit()
conn.close()

print(f"Test database created successfully at: {db_path}")
print("Tables created: users, transactions")
print(f"Users inserted: {len(users_data)}")
print(f"Transactions inserted: {len(transactions_data)}")