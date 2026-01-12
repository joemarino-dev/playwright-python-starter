"""
End-to-End Integration Test: Banking Transfer Flow

Tests the complete flow: 
- UI interaction (Playwright browser automation)
- API validation (Flask endpoint)
- Database verification (SQLite)
- Property-based validation (conservation of money)
"""
    
import pytest

def test_transfer_e2e(page, db_connection, flask_server):
    """
    Integration test: Transfer money between accounts
    
    Validates: 
    - UI form submission works
    - API processes transfer correctly
    - Database balance updates
    - Total money for all accounts is conserved
    """
    
    # Get initial balances from database
    cursor = db_connection.cursor()
    
    cursor.execute("SELECT id, name, account_balance FROM users WHERE id =1")
    john_before = cursor.fetchone()
    
    cursor.execute("SELECT id, name, account_balance FROM users WHERE id =2")
    jane_before = cursor.fetchone()
    
    # Calculate total money in the system before transfer
    cursor.execute("SELECT SUM(account_balance) as total FROM users")
    total_before = cursor.fetchone()['total']
    
    # Navigate to transfer page
    page.goto(flask_server)
    
    # Fill out transfer form
    transfer_amount = 200
    page.select_option('[data-testid="from-account-select"]', '1') # John Smith
    page.select_option('[data-testid="to-account-select"]', '2') # Jane Doe
    page.fill('[data-testid="amount-input"]', str(transfer_amount)) # Amount to be transferred
    
    # Submit the form
    page.click('[data-testid="transfer-submit-button"]')
    
    # Wait for result to appear
    page.wait_for_selector('[data-testid="transfer-result"]', state='visible')
    
    # Verify success message appears in UI
    result_element = page.locator('[data-testid="transfer-result"]')
    result_text = result_element.text_content()
    
    assert 'success' in result_text.lower()
    assert '200' in result_text
    
    # Query databases to verify balances changed
    cursor.execute("SELECT id, name, account_balance FROM users WHERE id = 1")
    john_after = cursor.fetchone()
    
    cursor.execute("SELECT id, name, account_balance FROM users WHERE id = 2")
    jane_after = cursor.fetchone()
    
    # Verify John's balance decreased by $200
    expected_john = john_before['account_balance'] - transfer_amount
    assert john_after['account_balance'] == pytest.approx(expected_john, abs=0.01)
    
    # Verify Jane's balance increased by $200
    expected_jane = jane_before['account_balance'] + transfer_amount
    assert jane_after['account_balance'] == pytest.approx(expected_jane, abs=0.01)
    
    # Property-based validation - total money in system is unchanged
    cursor.execute("SELECT SUM(account_balance) as total FROM users")
    total_after = cursor.fetchone()['total']
    
    assert total_after == pytest.approx(total_before, abs=0.01)