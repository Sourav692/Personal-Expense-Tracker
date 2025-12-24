# Personal Expense Tracker - Setup Guide

## Overview
This guide will walk you through setting up the Personal Expense Tracker using Databricks Lakebase (OLTP), Lakehouse (OLAP), Workflows, and Apps.

## Prerequisites
- Databricks workspace with Unity Catalog enabled
- Access to create Lakebase databases (if available)
- SQL Warehouse for query execution
- Permissions to create Jobs and Apps

## Project Structure
```
expense-tracker/
├── notebooks/              # Databricks notebooks
│   ├── 01-setup-lakebase.ipynb
│   ├── 02-create-schema.ipynb
│   ├── 03-sync-pipeline.ipynb
│   ├── 04-workflow-automation.ipynb
│   └── 05-validate-results.ipynb
├── apps/                   # Databricks App
│   └── expense-tracker/
│       ├── app.py
│       ├── requirements.txt
│       └── config.py
├── configuration/          # Configuration files
│   ├── lakebase-config.json
│   ├── workflow-config.json
│   └── app-config.json
├── data/                   # Sample data
│   ├── sample-categories.csv
│   └── sample-expenses.csv
└── documentation/          # Documentation
    ├── setup-guide.md
    └── validation-guide.md
```

## Setup Steps

### Step 1: Set Up Lakebase PostgreSQL (Optional)

**Note:** Lakebase is a new feature. If not available, skip to Step 2 and use Unity Catalog directly.

1. Open notebook `01-setup-lakebase.ipynb`
2. Configure the following variables:
   ```python
   INSTANCE_NAME = "expense-tracker-lakebase"
   DATABASE_NAME = "expense_tracker_db"
   INSTANCE_TYPE = "SMALL"
   REGION = "us-west-2"  # Match your workspace region
   ```
3. Run all cells to:
   - Create Lakebase PostgreSQL instance
   - Wait for provisioning (15-30 minutes)
   - Retrieve connection details
   - Save configuration

**Expected Output:**
```
✓ Lakebase PostgreSQL database created: expense_tracker_db
✓ Database ID: <database-id>
✓ State: ACTIVE
✓ Instance Type: SMALL
✓ SSL: Enabled
```

### Step 2: Create Database Schema

1. Open notebook `02-create-schema.ipynb`
2. Run all cells to:
   - Create tables (categories, expenses, budgets)
   - Add indexes for performance
   - Insert sample categories
   - Generate sample expense data

**Tables Created:**
- `categories`: Expense categories (Groceries, Dining, etc.)
- `expenses`: Individual expense transactions
- `budgets`: Monthly budget allocations

**Expected Output:**
```
✓ Tables created:
  - categories (10 categories)
  - expenses (sample data)
  - budgets (monthly budgets)
✓ Indexes created for performance
✓ Sample data inserted
```

### Step 3: Set Up Sync Pipeline (Lakebase → Lakehouse)

1. Open notebook `03-sync-pipeline.ipynb`
2. Configure Unity Catalog settings:
   ```python
   CATALOG_NAME = "main"  # Your catalog
   SCHEMA_NAME = "expense_tracker"
   ```
3. Run all cells to:
   - Create Unity Catalog schema
   - Read data from Lakebase (or create sample data)
   - Write to Delta tables in Unity Catalog
   - Create analytics views

**Views Created:**
- `monthly_spending_by_category`: Spending aggregated by month and category
- `budget_vs_actual`: Budget status with variance analysis

**Expected Output:**
```
✓ Schema main.expense_tracker created
✓ Synced 3 tables from Lakebase to Lakehouse
✓ Created analytics views
```

### Step 4: Set Up Workflow Automation

1. Open notebook `04-workflow-automation.ipynb`
2. Review the workflow configuration
3. **Option A - Create via UI** (Recommended for demo):
   - Go to **Workflows** in left sidebar
   - Click **Create Job**
   - Add Task 1: `sync_expenses`
     - Type: Notebook
     - Path: `/Workspace/Users/<your-email>/expense-tracker/notebooks/03-sync-pipeline`
     - Cluster: Select existing cluster
   - Add Task 2: `validate_results`
     - Type: Notebook
     - Path: `/Workspace/Users/<your-email>/expense-tracker/notebooks/05-validate-results`
     - Cluster: Select existing cluster
     - Depends on: `sync_expenses`
   - Add Schedule (optional):
     - Cron: `0 0 2 * * ?` (Daily at 2 AM)
     - Timezone: Your timezone
   - Save and run manually to test

4. **Option B - Create via SDK**:
   - Update `workflow-config.json` with your details
   - Run the notebook cells to create job programmatically

**Expected Output:**
```
✓ Workflow configuration created
✓ Job management functions defined
✓ Monitoring utilities ready
```

### Step 5: Validate Results

1. Open notebook `05-validate-results.ipynb`
2. Run all cells to:
   - Check table existence and row counts
   - Perform data quality checks
   - Verify referential integrity
   - Validate business logic
   - Generate summary statistics

**Expected Output:**
```
✓ Data quality checks performed
✓ Referential integrity verified
✓ Business logic validated
✓ Summary statistics generated
```

### Step 6: Deploy Databricks App

1. Navigate to the `apps/expense-tracker/` directory
2. Update `config.py` with your settings:
   ```python
   DATABRICKS_HOST = "your-workspace.cloud.databricks.com"
   DATABRICKS_TOKEN = "your-token"
   DATABRICKS_WAREHOUSE_ID = "your-warehouse-id"
   ```
3. Create `.env` file (don't commit to git):
   ```
   DATABRICKS_HOST=your-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=your-token
   DATABRICKS_WAREHOUSE_ID=your-warehouse-id
   CATALOG_NAME=main
   SCHEMA_NAME=expense_tracker
   ```

4. **Deploy to Databricks Apps**:
   - In Databricks workspace, go to **Apps**
   - Click **Create App**
   - Select **Upload Files**
   - Upload `app.py`, `requirements.txt`, `config.py`
   - Configure app settings
   - Deploy

5. **Or run locally for testing**:
   ```bash
   cd apps/expense-tracker/
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Configuration Files

### lakebase-config.json
Contains Lakebase PostgreSQL instance configuration:
- Instance name and type
- Connection details
- Table definitions

### workflow-config.json
Contains Databricks Workflow configuration:
- Job schedule (cron expression)
- Task definitions and dependencies
- Email notifications
- Retry policies

### app-config.json
Contains Databricks App configuration:
- Data source connections
- UI theme and settings
- Alert thresholds
- Chart colors

## Data Files

### sample-categories.csv
Contains 10 expense categories:
- Essential: Groceries, Transportation, Utilities, Healthcare
- Lifestyle: Dining Out, Entertainment, Shopping, Travel
- Investment: Education, Savings

### sample-expenses.csv
Contains 50 sample expense transactions with:
- Date, amount, category
- Payment method
- Vendor
- Tags

## Troubleshooting

### Issue: Lakebase instance creation fails
**Solution:** 
- Verify you have permissions to create databases
- Check that your workspace has Lakebase enabled
- Ensure region is correctly configured
- Contact Databricks support if needed

### Issue: Sync pipeline fails
**Solution:**
- Verify Unity Catalog permissions
- Check catalog and schema names
- Ensure SQL Warehouse is running
- Review error messages in notebook output

### Issue: Workflow doesn't run
**Solution:**
- Verify cluster is available
- Check notebook paths are correct
- Review job run logs in Workflows UI
- Ensure dependencies are satisfied

### Issue: App won't deploy
**Solution:**
- Check all required files are uploaded
- Verify requirements.txt has correct versions
- Review app logs for errors
- Ensure warehouse ID is correct

## Next Steps

1. **Customize Categories**: Add your own expense categories in notebook 02
2. **Import Real Data**: Replace sample data with actual expense data
3. **Adjust Budgets**: Set realistic monthly budgets for your spending
4. **Schedule Workflow**: Enable automatic daily sync
5. **Customize App**: Modify visualizations and add features
6. **Set Up Alerts**: Configure budget warnings via email

## Security Best Practices

1. **Never commit sensitive data**:
   - Use Databricks Secrets for credentials
   - Add `.env` to `.gitignore`
   - Use environment variables

2. **Limit permissions**:
   - Grant minimum required access
   - Use service principals for production
   - Enable audit logging

3. **Secure connections**:
   - Always use SSL/TLS
   - Rotate credentials regularly
   - Use private endpoints when available

## Support

For issues or questions:
1. Check the validation guide for common problems
2. Review Databricks documentation
3. Contact your workspace administrator
4. File issues in your project repository

## Additional Resources

- [Databricks Lakebase Documentation](https://docs.databricks.com/lakebase/)
- [Unity Catalog Guide](https://docs.databricks.com/data-governance/unity-catalog/)
- [Workflows Documentation](https://docs.databricks.com/workflows/)
- [Databricks Apps Guide](https://docs.databricks.com/apps/)
- [Delta Lake Documentation](https://docs.delta.io/)

---

**Setup Time:** Approximately 2-3 hours (excluding Lakebase provisioning)
**Skill Level:** Intermediate
**Prerequisites:** Basic SQL, Python, and Databricks knowledge

