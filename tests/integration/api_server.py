"""
Flask API Server for Banking Transfer Integration Test

This simple API provides a transfer endpoint that:
1. Validates transfer request
2. Updates account balances
3. Creates transaction records
4. Returns success/failure response

Used by Playwright integration tests to validate end-to-end transfer flow.
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database path
DB_PATH = os.path.join('tests', 'test_data.db')


def get_db_connection():
    """Create database connection with row factory for dict-like access"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """Serve the transfer form page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bank Transfer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            select, input {
                width: 100%;
                padding: 8px;
                font-size: 14px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .account-info {
                background-color: #f8f9fa;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Bank Transfer</h1>
        
        <div class="account-info" id="accounts-display">
            <h3>Available Accounts:</h3>
            <div id="accounts-list"></div>
        </div>

        <form id="transfer-form">
            <div class="form-group">
                <label for="from-account">From Account:</label>
                <select id="from-account" name="from_account" data-testid="from-account-select" required>
                    <option value="">Select account...</option>
                </select>
            </div>

            <div class="form-group">
                <label for="to-account">To Account:</label>
                <select id="to-account" name="to_account" data-testid="to-account-select" required>
                    <option value="">Select account...</option>
                </select>
            </div>

            <div class="form-group">
                <label for="amount">Amount ($):</label>
                <input type="number" id="amount" name="amount" data-testid="amount-input" step="0.01" min="0.01" required>
            </div>

            <button type="submit" data-testid="transfer-submit-button">Transfer Funds</button>
        </form>

        <div id="result" data-testid="transfer-result"></div>

        <script>
            // Load accounts on page load
            async function loadAccounts() {
                try {
                    const response = await fetch('/api/accounts');
                    const accounts = await response.json();
                    
                    const fromSelect = document.getElementById('from-account');
                    const toSelect = document.getElementById('to-account');
                    const accountsList = document.getElementById('accounts-list');
                    
                    // Clear existing options (keep placeholder)
                    fromSelect.innerHTML = '<option value="">Select account...</option>';
                    toSelect.innerHTML = '<option value="">Select account...</option>';
                    accountsList.innerHTML = '';
                    
                    // Populate dropdowns and display
                    accounts.forEach(account => {
                        // Add to dropdowns
                        const option1 = document.createElement('option');
                        option1.value = account.id;
                        option1.textContent = `${account.name} - $${account.account_balance.toFixed(2)}`;
                        fromSelect.appendChild(option1);
                        
                        const option2 = document.createElement('option');
                        option2.value = account.id;
                        option2.textContent = `${account.name} - $${account.account_balance.toFixed(2)}`;
                        toSelect.appendChild(option2);
                        
                        // Add to display list
                        const accountDiv = document.createElement('div');
                        accountDiv.textContent = `${account.name}: $${account.account_balance.toFixed(2)}`;
                        accountsList.appendChild(accountDiv);
                    });
                } catch (error) {
                    console.error('Error loading accounts:', error);
                }
            }

            // Handle form submission
            document.getElementById('transfer-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = {
                    from_account_id: parseInt(document.getElementById('from-account').value),
                    to_account_id: parseInt(document.getElementById('to-account').value),
                    amount: parseFloat(document.getElementById('amount').value)
                };
                
                const resultDiv = document.getElementById('result');
                
                try {
                    const response = await fetch('/api/transfer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const data = await response.json();
                    
                    resultDiv.style.display = 'block';
                    if (data.success) {
                        resultDiv.className = 'success';
                        resultDiv.textContent = data.message;
                        // Reload accounts to show updated balances
                        setTimeout(loadAccounts, 500);
                        // Clear form
                        document.getElementById('transfer-form').reset();
                    } else {
                        resultDiv.className = 'error';
                        resultDiv.textContent = data.message;
                    }
                } catch (error) {
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'error';
                    resultDiv.textContent = 'Error processing transfer: ' + error.message;
                }
            });

            // Load accounts when page loads
            loadAccounts();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts with current balances"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, email, account_balance FROM users ORDER BY id')
        accounts = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify(accounts)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/transfer', methods=['POST'])
def transfer():
    """
    Process a transfer between two accounts
    
    Expected JSON payload:
    {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 100.00
    }
    
    Returns:
    {
        "success": true/false,
        "message": "Transfer completed successfully" or error message,
        "transaction_id": 5 (if successful)
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        from_account_id = data.get('from_account_id')
        to_account_id = data.get('to_account_id')
        amount = data.get('amount')
        
        if not all([from_account_id, to_account_id, amount]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: from_account_id, to_account_id, amount'
            }), 400
        
        if from_account_id == to_account_id:
            return jsonify({
                'success': False,
                'message': 'Cannot transfer to the same account'
            }), 400
        
        if amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Transfer amount must be greater than zero'
            }), 400
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get source account
        cursor.execute('SELECT * FROM users WHERE id = ?', (from_account_id,))
        from_account = cursor.fetchone()
        
        if not from_account:
            conn.close()
            return jsonify({
                'success': False,
                'message': f'Source account {from_account_id} not found'
            }), 404
        
        # Get destination account
        cursor.execute('SELECT * FROM users WHERE id = ?', (to_account_id,))
        to_account = cursor.fetchone()
        
        if not to_account:
            conn.close()
            return jsonify({
                'success': False,
                'message': f'Destination account {to_account_id} not found'
            }), 404
        
        # Check sufficient funds
        if from_account['account_balance'] < amount:
            conn.close()
            return jsonify({
                'success': False,
                'message': f'Insufficient funds. Available: ${from_account["account_balance"]:.2f}'
            }), 400
        
        # Perform transfer (as a transaction)
        try:
            # Update source account (decrease balance)
            cursor.execute(
                'UPDATE users SET account_balance = account_balance - ? WHERE id = ?',
                (amount, from_account_id)
            )
            
            # Update destination account (increase balance)
            cursor.execute(
                'UPDATE users SET account_balance = account_balance + ? WHERE id = ?',
                (amount, to_account_id)
            )
            
            # Create transaction record
            cursor.execute('''
                INSERT INTO transactions 
                (user_id, amount, transaction_type, status, from_account_id, to_account_id)
                VALUES (?, ?, 'transfer', 'completed', ?, ?)
            ''', (from_account_id, amount, from_account_id, to_account_id))
            
            transaction_id = cursor.lastrowid
            
            # Commit the transaction
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'Transfer of ${amount:.2f} completed successfully',
                'transaction_id': transaction_id,
                'from_account': from_account['name'],
                'to_account': to_account['name']
            })
        
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({
                'success': False,
                'message': f'Transfer failed: {str(e)}'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing request: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Run server on port 5001
    print("Starting Flask server on http://localhost:5001")
    print("Database path:", DB_PATH)
    app.run(debug=True, port=5001)