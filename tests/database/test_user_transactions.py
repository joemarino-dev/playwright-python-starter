def test_user_transactions(db_connection):
    """Verify transactions for a specific user"""
    cursor = db_connection.cursor()
    cursor.execute("""
                   SELECT t.*, u.name
                   FROM transactions t
                   JOIN users u ON t.user_id = u.id
                   WHERE u.id = 1
                   """)
    transactions = cursor.fetchall()
    
    assert len(transactions) == 2 # User 1 has 2 transactions
    assert transactions[0]['name'] == 'John Smith'