def test_user_balance_calculation(db_connection):
    """Verify total balance across all users"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(account_balance) as total FROM users")
    result = cursor.fetchone()
    
    # Total should be 50000 + 75000 + 100000 = 225000
    assert result['total'] == 225000.00