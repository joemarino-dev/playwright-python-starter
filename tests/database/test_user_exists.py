def test_user_exists_in_database(db_connection):
    """Verify user data exists and is correct"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = 1")
    user = cursor.fetchone()
    
    assert user is not None
    assert user['name'] == 'John Smith'
    assert user['email'] == 'john.smith@example.com'
    assert user['account_balance'] == 50000.00