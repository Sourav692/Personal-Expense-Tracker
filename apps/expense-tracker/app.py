"""
Personal Expense Tracker - Databricks App
A Streamlit-based dashboard for visualizing expense data
"""

import streamlit as st
import pandas as pd
from databricks import sql
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Title and description
st.title("💰 Personal Expense Tracker")
st.markdown("Track your expenses, monitor budgets, and gain insights into your spending habits")

# Sidebar configuration
st.sidebar.header("Configuration")
CATALOG_NAME = st.sidebar.text_input("Catalog Name", "main")
SCHEMA_NAME = st.sidebar.text_input("Schema Name", "expense_tracker")

# Helper functions
@st.cache_data(ttl=300)
def get_data(query):
    """Execute SQL query and return DataFrame"""
    try:
        # Note: In actual Databricks App, use databricks-sql-connector
        # For demo, we'll show sample data structure
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return pd.DataFrame()

def load_expenses():
    """Load expense data"""
    query = f"""
    SELECT 
        e.expense_id,
        e.expense_date,
        c.category_name,
        c.category_type,
        e.amount,
        e.payment_method,
        e.vendor,
        e.description
    FROM {CATALOG_NAME}.{SCHEMA_NAME}.expenses e
    JOIN {CATALOG_NAME}.{SCHEMA_NAME}.categories c ON e.category_id = c.category_id
    ORDER BY e.expense_date DESC
    """
    return get_data(query)

def load_budget_status():
    """Load budget vs actual data"""
    query = f"""
    SELECT * FROM {CATALOG_NAME}.{SCHEMA_NAME}.budget_vs_actual
    ORDER BY percent_used DESC
    """
    return get_data(query)

def load_monthly_spending():
    """Load monthly spending by category"""
    query = f"""
    SELECT * FROM {CATALOG_NAME}.{SCHEMA_NAME}.monthly_spending_by_category
    ORDER BY month DESC, total_amount DESC
    """
    return get_data(query)

# Main dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💳 Expenses", "📈 Budget", "📉 Analytics"])

with tab1:
    st.header("Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Expenses", "$12,458.32", "-5.2%")
    with col2:
        st.metric("This Month", "$3,245.67", "+12.3%")
    with col3:
        st.metric("Budget Used", "78%", "+8%")
    with col4:
        st.metric("Categories", "9", "0")
    
    st.divider()
    
    # Spending trend chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Spending Trend")
        # Sample data for demo
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        amounts = [100 + i * 2 + (i % 7) * 20 for i in range(30)]
        trend_df = pd.DataFrame({'Date': dates, 'Amount': amounts})
        
        fig = px.line(trend_df, x='Date', y='Amount', 
                     title='Daily Spending (Last 30 Days)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Category Distribution")
        # Sample pie chart
        categories = ['Groceries', 'Dining', 'Transport', 'Shopping', 'Entertainment']
        values = [2500, 1800, 1200, 3000, 1500]
        
        fig = px.pie(values=values, names=categories, 
                    title='Spending by Category')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Recent Expenses")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input("Date Range", 
                                   value=(datetime.now() - timedelta(days=30), datetime.now()))
    with col2:
        category_filter = st.multiselect("Categories", 
                                        ["All", "Groceries", "Dining", "Transport"])
    with col3:
        min_amount = st.number_input("Min Amount", min_value=0.0, value=0.0)
    
    st.divider()
    
    # Sample expense data
    sample_expenses = pd.DataFrame({
        'Date': pd.date_range(end=datetime.now(), periods=10, freq='D'),
        'Category': ['Groceries', 'Dining', 'Transport', 'Shopping', 'Entertainment',
                    'Groceries', 'Healthcare', 'Utilities', 'Dining', 'Travel'],
        'Amount': [125.50, 45.99, 35.00, 230.45, 85.00, 
                  95.25, 150.00, 89.99, 62.50, 450.00],
        'Payment': ['Credit Card', 'Cash', 'Debit Card', 'Credit Card', 'Credit Card',
                   'Debit Card', 'Credit Card', 'Auto-pay', 'Cash', 'Credit Card'],
        'Vendor': ['Whole Foods', 'Chipotle', 'Uber', 'Amazon', 'Netflix',
                  'Trader Joes', 'CVS Pharmacy', 'PG&E', 'Starbucks', 'United Airlines']
    })
    
    st.dataframe(sample_expenses, use_container_width=True, hide_index=True)
    
    # Add expense button
    if st.button("➕ Add New Expense"):
        st.info("Feature: Open dialog to add new expense (to be implemented)")

with tab3:
    st.header("Budget Overview")
    
    # Sample budget data
    budget_df = pd.DataFrame({
        'Category': ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 
                    'Entertainment', 'Healthcare', 'Shopping', 'Travel', 'Education'],
        'Budget': [600, 300, 400, 200, 200, 150, 300, 500, 200],
        'Actual': [545, 385, 320, 189, 195, 75, 425, 0, 150],
        'Remaining': [55, -85, 80, 11, 5, 75, -125, 500, 50]
    })
    
    budget_df['Percent'] = (budget_df['Actual'] / budget_df['Budget'] * 100).round(1)
    budget_df['Status'] = budget_df['Percent'].apply(
        lambda x: '🔴 OVER' if x > 100 else '🟡 WARNING' if x > 90 else '🟢 OK'
    )
    
    st.dataframe(budget_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Budget progress bars
    st.subheader("Budget Progress")
    for _, row in budget_df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(min(row['Percent'] / 100, 1.0), 
                       text=f"{row['Category']}: ${row['Actual']:.0f} / ${row['Budget']:.0f}")
        with col2:
            st.metric("", f"{row['Percent']:.0f}%", delta=f"${row['Remaining']:.0f}")

with tab4:
    st.header("Analytics & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Comparison")
        # Sample monthly comparison
        months = ['Sep', 'Oct', 'Nov', 'Dec']
        amounts = [3200, 3500, 2980, 3245]
        
        fig = go.Figure(data=[
            go.Bar(x=months, y=amounts, marker_color='lightblue')
        ])
        fig.update_layout(title='Monthly Spending Comparison', 
                         yaxis_title='Amount ($)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Vendors")
        vendors = ['Amazon', 'Whole Foods', 'Starbucks', 'Shell', 'Target']
        spending = [1250, 890, 245, 380, 650]
        
        fig = go.Figure(data=[
            go.Bar(y=vendors, x=spending, orientation='h', marker_color='lightgreen')
        ])
        fig.update_layout(title='Top 5 Vendors by Spending',
                         xaxis_title='Amount ($)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Insights
    st.subheader("💡 Insights")
    st.info("📈 Your spending increased by 12.3% this month compared to last month")
    st.warning("⚠️ You're over budget in 2 categories: Dining Out and Shopping")
    st.success("✅ Great job! You're well under budget for Healthcare this month")

# Footer
st.divider()
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Databricks & Streamlit | Data updated every 5 minutes</p>
</div>
""", unsafe_allow_html=True)

