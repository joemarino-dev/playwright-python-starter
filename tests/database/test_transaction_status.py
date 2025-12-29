def test_transaction_status(db_connection):
    """Verify transaction statuses"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM transactions
        WHERE status = 'completed'
    """)
    result = cursor.fetchone()
    
    assert result['count'] == 4 # 4 completed transactions