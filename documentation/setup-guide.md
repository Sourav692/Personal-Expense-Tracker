# Personal Expense Tracker - Setup Guide

This guide walks you through setting up the Personal Expense Tracker application using Databricks Lakebase, Lakehouse, Workflows, and Apps.

## Prerequisites

- Databricks workspace with appropriate permissions
- Databricks CLI or SDK configured with authentication
- Python 3.10+ environment
- Access to create Lakebase instances, Unity Catalog, and Workflows

## Project Structure

```
expense-tracker/
├── notebooks/              # Databricks notebooks for setup and processing
├── apps/                   # Databricks Apps application
├── configuration/         # Configuration files
├── data/                  # Sample data files
└── documentation/         # Setup and validation guides
```

## Setup Steps

### 1. Lakebase Instance Creation (MODULE 1.1)

**Notebook:** `notebooks/01-setup-lakebase.ipynb`

This notebook creates a PostgreSQL instance using Databricks Lakebase.

**Steps:**
1. Open the notebook in your Databricks workspace
2. Ensure you have the necessary permissions to create Lakebase instances
3. Run all cells sequentially
4. The notebook will:
   - Check for existing instances
   - Create a new PostgreSQL instance (if needed)
   - Wait for the instance to be ready
   - Retrieve connection details
   - Save configuration to `configuration/lakebase-config.json`

**Configuration:**
- Instance Size: SMALL (for development)
- Storage: 20 GB
- PostgreSQL Version: 15
- SSL: Enabled
- Region: us-east-1 (configurable)

**Output:**
- Instance ID and connection details saved to `configuration/lakebase-config.json`

### 2. Database Schema Creation (MODULE 1.2)

**Notebook:** `notebooks/02-create-schema.ipynb`

Creates the database schema with tables for expenses and categories.

### 3. Data Sync Pipeline (MODULE 1.3)

**Notebook:** `notebooks/03-sync-pipeline.ipynb`

Sets up the pipeline to sync data from Lakebase (OLTP) to Lakehouse (OLAP).

### 4. Workflow Automation (MODULE 1.4)

**Notebook:** `notebooks/04-workflow-automation.ipynb`

Creates and configures Databricks Workflows for automated data processing.

### 5. Validation (MODULE 1.5)

**Notebook:** `notebooks/05-validate-results.ipynb`

Validates the setup and data integrity.

## Configuration Files

### lakebase-config.json
Contains Lakebase instance configuration and connection details.

### workflow-config.json
Contains workflow definitions and scheduling information.

### app-config.json
Contains application configuration for the Databricks App.

## Environment Variables

Create a `.env` file in the project root (optional):

```env
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-token
```

Or configure using Databricks CLI:
```bash
databricks configure --token
```

## Troubleshooting

### Instance Creation Fails
- Verify you have permissions to create Lakebase instances
- Check if the region is available in your workspace
- Ensure you're not exceeding instance quotas

### Connection Issues
- Verify SSL settings match your network configuration
- Check firewall rules if connecting from outside Databricks
- Ensure credentials are correctly retrieved

### Configuration Not Saved
- Verify write permissions to the configuration directory
- Check that the project path is correctly set in the notebook

## Next Steps

After completing MODULE 1.1:
1. Review the connection details in `configuration/lakebase-config.json`
2. Proceed to `02-create-schema.ipynb` to set up database tables
3. Test the connection using the optional test cell in the notebook

## Security Best Practices

- Never commit credentials to version control
- Use Databricks Secrets for production deployments
- Rotate database passwords regularly
- Enable SSL for all connections
- Use least-privilege access principles

## Support

For issues or questions:
1. Check the Databricks documentation
2. Review error messages in notebook outputs
3. Verify configuration files are correctly formatted

