def test_user_count(db_connection):
    """Verify correct number of users in database"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    result = cursor.fetchone()
    
    assert result['count'] == 3