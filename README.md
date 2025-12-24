# Personal Expense Tracker

A comprehensive Personal Expense Tracker application built on Databricks platform, demonstrating the use of Lakebase (OLTP), Lakehouse (OLAP), Workflows, and Apps.

## Overview

This project is designed as a 1-day learning exercise covering all core Databricks features:

- **Lakebase**: PostgreSQL instance for transactional data (OLTP)
- **Lakehouse**: Delta tables for analytical workloads (OLAP)
- **Workflows**: Automated data synchronization pipelines
- **Apps**: Web application for expense management

## Project Structure

```
expense-tracker/
├── notebooks/              # Databricks notebooks
│   ├── 01-setup-lakebase.ipynb      # MODULE 1.1: Lakebase instance creation
│   ├── 02-create-schema.ipynb        # Database schema setup
│   ├── 03-sync-pipeline.ipynb       # Data sync pipeline
│   ├── 04-workflow-automation.ipynb  # Workflow configuration
│   └── 05-validate-results.ipynb    # Validation and testing
├── apps/
│   └── expense-tracker/
│       ├── app.py                    # Flask application
│       ├── requirements.txt          # Python dependencies
│       └── config.py                 # Configuration module
├── configuration/
│   ├── lakebase-config.json          # Lakebase instance config
│   ├── workflow-config.json         # Workflow definitions
│   └── app-config.json              # Application config
├── data/
│   ├── sample-expenses.csv          # Sample expense data
│   └── sample-categories.csv        # Sample category data
└── documentation/
    ├── setup-guide.md               # Setup instructions
    └── validation-guide.md          # Validation procedures
```

## Quick Start

### Prerequisites

- Databricks workspace with appropriate permissions
- Databricks SDK configured (via CLI or environment variables)
- Python 3.10+ environment

### Step 1: Setup Lakebase Instance (MODULE 1.1)

1. Open `notebooks/01-setup-lakebase.ipynb` in Databricks
2. Run all cells sequentially
3. The notebook will:
   - Create a PostgreSQL instance
   - Configure SSL and security settings
   - Retrieve connection details
   - Save configuration to `configuration/lakebase-config.json`

**Key Features:**
- ✅ Instance creation with Databricks SDK
- ✅ Proper naming convention (`personal-expense-tracker-db`)
- ✅ Region configuration (configurable)
- ✅ Storage size optimization (20GB for development)
- ✅ Database version selection (PostgreSQL 15)
- ✅ Connection details retrieval
- ✅ SSL connection support
- ✅ Comprehensive error handling

### Step 2: Create Database Schema

Run `notebooks/02-create-schema.ipynb` to create tables and relationships.

### Step 3: Setup Data Sync Pipeline

Run `notebooks/03-sync-pipeline.ipynb` to configure Lakebase → Lakehouse sync.

### Step 4: Configure Workflows

Run `notebooks/04-workflow-automation.ipynb` to automate data processing.

### Step 5: Validate Setup

Run `notebooks/05-validate-results.ipynb` to verify everything works.

## Configuration

### Lakebase Configuration

The `configuration/lakebase-config.json` file contains:
- Instance metadata (ID, name, region, status)
- Connection details (host, port, credentials)
- Instance settings (size, storage, version)

**Note:** Credentials are stored in the config file. For production, use Databricks Secrets.

### Workflow Configuration

The `configuration/workflow-config.json` file defines:
- Workflow name and schedule
- Task definitions
- Email notifications
- Timeout and concurrency settings

### App Configuration

The `configuration/app-config.json` file contains:
- Application metadata
- Runtime configuration
- Feature flags

## Usage

### Running the Application

1. Deploy the app from `apps/expense-tracker/`
2. Access the app URL provided by Databricks
3. Use the web interface to manage expenses

### API Endpoints

- `GET /api/expenses` - List all expenses
- `POST /api/expenses` - Create a new expense
- `GET /api/categories` - List all categories

## Documentation

- **[Setup Guide](documentation/setup-guide.md)** - Detailed setup instructions
- **[Validation Guide](documentation/validation-guide.md)** - Validation procedures and troubleshooting

## Features

### MODULE 1.1: Lakebase Instance Creation

- ✅ Small instance for development (cost-optimized)
- ✅ SSL-enabled connections
- ✅ Automatic status polling
- ✅ Connection string generation
- ✅ Configuration persistence
- ✅ Error handling and validation

## Security Notes

- **Development**: Credentials stored in config files
- **Production**: Use Databricks Secrets for credential management
- **SSL**: Enabled by default for all connections
- **Access Control**: Follow least-privilege principles

## Troubleshooting

See [Validation Guide](documentation/validation-guide.md) for common issues and solutions.

## Next Steps

After completing MODULE 1.1:
1. Review connection details in `configuration/lakebase-config.json`
2. Proceed to schema creation (`02-create-schema.ipynb`)
3. Test database connectivity
4. Continue with remaining modules

## License

This is a learning project for educational purposes.

