# Personal Expense Tracker

A comprehensive expense tracking system built with Databricks, demonstrating the integration of **Lakebase (OLTP)**, **Lakehouse (OLAP)**, **Workflows**, and **Apps**.

## 🎯 Project Overview

This 1-day learning project showcases core Databricks features through a practical personal expense tracker application. It demonstrates the complete data lifecycle from transactional database to analytics and visualization.

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Lakebase       │      │  Unity Catalog  │      │  Databricks     │
│  (PostgreSQL)   │─────▶│  Lakehouse      │─────▶│  App            │
│  OLTP Database  │ Sync │  Delta Tables   │ Query│  Streamlit UI   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │                         │
        │                         │
        ▼                         ▼
┌─────────────────────────────────────────────────┐
│         Databricks Workflows                    │
│  - Scheduled sync pipeline                      │
│  - Data validation                              │
│  - Automated reporting                          │
└─────────────────────────────────────────────────┘
```

## ✨ Features

### 🗄️ Lakebase (OLTP)
- PostgreSQL database for transactional data
- Normalized schema (categories, expenses, budgets)
- ACID compliance for data integrity
- Real-time transaction processing

### 🏠 Lakehouse (OLAP)
- Unity Catalog Delta tables
- Optimized for analytics queries
- Time-travel capabilities
- Incremental data sync

### 🔄 Workflows
- Automated daily sync pipeline
- Data validation checks
- Error handling and notifications
- Task dependencies

### 📱 Databricks App
- Interactive Streamlit dashboard
- Real-time expense visualization
- Budget tracking and alerts
- Category-based analytics

## 📂 Project Structure

```
expense-tracker/
├── notebooks/
│   ├── 01-setup-lakebase.ipynb         # Create PostgreSQL instance
│   ├── 02-create-schema.ipynb          # Define database schema
│   ├── 03-sync-pipeline.ipynb          # OLTP to OLAP sync
│   ├── 04-workflow-automation.ipynb    # Job automation
│   └── 05-validate-results.ipynb       # Data validation
├── apps/
│   └── expense-tracker/
│       ├── app.py                      # Streamlit application
│       ├── requirements.txt            # Python dependencies
│       └── config.py                   # App configuration
├── configuration/
│   ├── lakebase-config.json           # Lakebase settings
│   ├── workflow-config.json           # Workflow definition
│   └── app-config.json                # App settings
├── data/
│   ├── sample-categories.csv          # Sample categories
│   └── sample-expenses.csv            # Sample expenses (50 records)
├── documentation/
│   ├── setup-guide.md                 # Setup instructions
│   └── validation-guide.md            # Validation procedures
└── README.md                          # This file
```

## 🚀 Quick Start

### Prerequisites
- Databricks workspace with Unity Catalog
- Access to create databases (for Lakebase)
- SQL Warehouse
- Cluster for notebook execution

### Setup (30 minutes)

1. **Clone or upload this project to your Databricks workspace**

2. **Run notebooks in sequence:**
   ```
   01-setup-lakebase.ipynb      → Create database
   02-create-schema.ipynb       → Define schema & load data
   03-sync-pipeline.ipynb       → Sync to Lakehouse
   04-workflow-automation.ipynb → Setup automation
   05-validate-results.ipynb    → Validate data
   ```

3. **Deploy the Databricks App:**
   - Upload `apps/expense-tracker/` files
   - Configure connection settings
   - Deploy to Databricks Apps

4. **Schedule the workflow:**
   - Create job in Workflows UI
   - Add sync and validation tasks
   - Set daily schedule

📖 **Detailed instructions:** See [Setup Guide](documentation/setup-guide.md)

## 📊 Data Model

### Tables

#### `categories`
- `category_id` (PK): Unique identifier
- `category_name`: Category name
- `category_type`: Essential, Lifestyle, Investment
- `description`: Category description

#### `expenses`
- `expense_id` (PK): Unique identifier
- `category_id` (FK): References categories
- `amount`: Expense amount
- `expense_date`: Date of expense
- `payment_method`: Credit Card, Cash, etc.
- `vendor`: Merchant name
- `description`: Expense details

#### `budgets`
- `budget_id` (PK): Unique identifier
- `category_id` (FK): References categories
- `month_year`: Budget month
- `budget_amount`: Allocated amount
- `spent_amount`: Current spending

### Analytics Views

#### `monthly_spending_by_category`
Aggregated spending by month and category with statistics.

#### `budget_vs_actual`
Budget performance with variance analysis and status indicators.

## 🎓 Learning Outcomes

### Lakebase Concepts
- Creating and managing PostgreSQL instances
- OLTP database design
- Connection management
- SSL/TLS configuration

### Lakehouse Concepts
- Unity Catalog schema design
- Delta Lake tables
- Incremental data sync
- Analytics views

### Workflow Concepts
- Job creation and scheduling
- Task dependencies
- Error handling
- Email notifications

### App Concepts
- Streamlit integration
- Real-time data visualization
- Interactive dashboards
- User experience design

## 🔧 Configuration

### Environment Variables
Create `.env` file (don't commit):
```env
DATABRICKS_HOST=your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-token
DATABRICKS_WAREHOUSE_ID=your-warehouse-id
CATALOG_NAME=main
SCHEMA_NAME=expense_tracker
```

### Customization
- **Categories:** Edit `data/sample-categories.csv`
- **Budgets:** Adjust amounts in notebook 02
- **Sync Schedule:** Modify cron expression in workflow config
- **App Theme:** Update colors in `apps/expense-tracker/config.py`

## 📈 Sample Data

The project includes sample data:
- **10 categories** across Essential, Lifestyle, and Investment types
- **50 expense transactions** spanning 3 months
- **Realistic spending patterns** across all categories

Replace with your own data by:
1. Importing CSV files
2. Connecting to external sources
3. Manual entry via SQL

## ✅ Validation

Run validation checks to ensure data quality:
```sql
-- Check table counts
SELECT COUNT(*) FROM main.expense_tracker.expenses;

-- Verify data freshness
SELECT MAX(expense_date) FROM main.expense_tracker.expenses;

-- Budget status
SELECT * FROM main.expense_tracker.budget_vs_actual;
```

📖 **Full validation guide:** [Validation Guide](documentation/validation-guide.md)

## 🐛 Troubleshooting

### Common Issues

**Lakebase not available:**
- Skip notebook 01
- Use Unity Catalog directly
- Run notebook 03 with sample data generation

**Sync pipeline fails:**
- Check Unity Catalog permissions
- Verify SQL Warehouse is running
- Review error logs

**App won't connect:**
- Verify warehouse ID
- Check authentication token
- Ensure network connectivity

## 🔐 Security

- Store credentials in Databricks Secrets
- Use SSL/TLS for all connections
- Implement least-privilege access
- Rotate tokens regularly
- Never commit `.env` files

## 📝 Notes

- **Demo Purpose:** This is a learning project, not production-ready
- **Lakebase:** New feature, may not be available in all regions
- **Sample Data:** For demonstration only
- **Costs:** Monitor cluster and warehouse usage

## 🗺️ Roadmap

Future enhancements:
- [ ] Mobile app integration
- [ ] Receipt scanning with OCR
- [ ] Multi-currency support
- [ ] Predictive budget recommendations
- [ ] Export to Excel/PDF
- [ ] Spending insights with ML

## 📚 Resources

- [Databricks Lakebase Docs](https://docs.databricks.com/lakebase/)
- [Unity Catalog Guide](https://docs.databricks.com/data-governance/unity-catalog/)
- [Workflows Documentation](https://docs.databricks.com/workflows/)
- [Databricks Apps](https://docs.databricks.com/apps/)
- [Delta Lake](https://delta.io/)

## 🤝 Contributing

This is a demo project for learning purposes. Feel free to:
- Customize for your needs
- Add new features
- Share improvements
- Report issues

## 📄 License

This project is provided as-is for educational purposes.

## 🎉 Acknowledgments

Built to demonstrate Databricks platform capabilities:
- Lakebase for OLTP workloads
- Unity Catalog for data governance
- Delta Lake for reliable data lakes
- Workflows for automation
- Apps for user interfaces

---

**Version:** 1.0.0
**Created:** December 2024
**Time to Complete:** 1 day
**Skill Level:** Intermediate
**Platform:** Databricks

**Happy Tracking! 💰📊**

