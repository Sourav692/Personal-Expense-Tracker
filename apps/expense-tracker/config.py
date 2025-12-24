"""
Configuration file for the Expense Tracker App
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Databricks configuration
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")
DATABRICKS_WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID", "")

# Unity Catalog configuration
CATALOG_NAME = os.getenv("CATALOG_NAME", "main")
SCHEMA_NAME = os.getenv("SCHEMA_NAME", "expense_tracker")

# App configuration
APP_TITLE = "Personal Expense Tracker"
APP_ICON = "💰"
REFRESH_INTERVAL = 300  # seconds

# Data configuration
TABLES = {
    "categories": f"{CATALOG_NAME}.{SCHEMA_NAME}.categories",
    "expenses": f"{CATALOG_NAME}.{SCHEMA_NAME}.expenses",
    "budgets": f"{CATALOG_NAME}.{SCHEMA_NAME}.budgets",
    "monthly_spending": f"{CATALOG_NAME}.{SCHEMA_NAME}.monthly_spending_by_category",
    "budget_vs_actual": f"{CATALOG_NAME}.{SCHEMA_NAME}.budget_vs_actual"
}

# Chart colors
COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4",
    "success": "#95E1D3",
    "warning": "#FFE66D",
    "danger": "#FF6B6B",
    "info": "#4ECDC4"
}

# Budget thresholds
BUDGET_WARNING_THRESHOLD = 0.9  # 90%
BUDGET_DANGER_THRESHOLD = 1.0   # 100%

# Query cache TTL (seconds)
CACHE_TTL = 300  # 5 minutes

