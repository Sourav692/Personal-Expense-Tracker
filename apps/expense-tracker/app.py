"""
Personal Expense Tracker - Databricks App
Main application file for the expense tracker app.
"""

import os
import sys
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add utils to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.db_connection import DatabaseConnection, get_connection_string, load_lakebase_config

app = Flask(__name__)

# Initialize database connection manager
try:
    config = load_lakebase_config()
    conn_str = get_connection_string(config)
    db = DatabaseConnection(conn_str, pool_size=5, max_overflow=10)
    db.create_pool()
    print("✓ Database connection pool initialized")
except Exception as e:
    print(f"⚠️  Database connection error: {str(e)}")
    db = None

def load_config():
    """Load configuration from JSON files."""
    config = {}
    try:
        config['lakebase'] = load_lakebase_config()
    except Exception as e:
        print(f"Warning: Could not load lakebase config: {str(e)}")
    
    APP_CONFIG = PROJECT_ROOT / "configuration" / "app-config.json"
    if APP_CONFIG.exists():
        with open(APP_CONFIG, 'r') as f:
            config['app'] = json.load(f)
    return config

@app.route('/')
def index():
    """Main dashboard page."""
    if not db:
        return "Database connection not available. Please run 02-connection-configuration.ipynb first.", 500
    
    try:
        with db.get_cursor() as cursor:
            # Get recent expenses
            cursor.execute("""
                SELECT e.*, c.category_name 
                FROM expenses e
                LEFT JOIN categories c ON e.category_id = c.category_id
                ORDER BY e.expense_date DESC, e.created_at DESC
                LIMIT 20
            """)
            expenses = cursor.fetchall()
            
            # Get summary statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_expenses,
                    SUM(amount) as total_amount,
                    AVG(amount) as avg_amount
                FROM expenses
                WHERE expense_date >= CURRENT_DATE - INTERVAL '30 days'
            """)
            stats = cursor.fetchone()
        
        return render_template('index.html', expenses=expenses, stats=stats)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """API endpoint to get expenses."""
    if not db:
        return jsonify({"error": "Database connection not available"}), 500
    
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT e.*, c.category_name 
                FROM expenses e
                LEFT JOIN categories c ON e.category_id = c.category_id
                ORDER BY e.expense_date DESC
            """)
            expenses = cursor.fetchall()
        
        return jsonify([dict(exp) for exp in expenses])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    """API endpoint to create a new expense."""
    if not db:
        return jsonify({"error": "Database connection not available"}), 500
    
    try:
        data = request.json
        with db.get_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO expenses (user_id, category_id, amount, description, expense_date, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING expense_id
            """, (
                data.get('user_id', 'user001'),
                data.get('category_id'),
                data.get('amount'),
                data.get('description'),
                data.get('expense_date'),
                data.get('payment_method', 'credit_card')
            ))
            
            expense_id = cursor.fetchone()[0]
        
        return jsonify({"expense_id": expense_id, "status": "created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """API endpoint to get categories."""
    if not db:
        return jsonify({"error": "Database connection not available"}), 500
    
    try:
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM categories WHERE is_active = true ORDER BY category_name")
            categories = cursor.fetchall()
        
        return jsonify([dict(cat) for cat in categories])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_db(error):
    """Cleanup database connections on app shutdown."""
    if db:
        db.close_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

