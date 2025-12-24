# Personal Expense Tracker - Quick Reference

## 📋 Project Summary

**Purpose:** Learn Databricks core features through a practical expense tracking system
**Time:** 1 day project
**Level:** Intermediate

## 🎯 What You'll Build

1. **Lakebase PostgreSQL Database** (OLTP)
   - Categories, Expenses, Budgets tables
   - Normalized schema with referential integrity
   
2. **Unity Catalog Lakehouse** (OLAP)
   - Delta tables for analytics
   - Pre-aggregated views
   
3. **Automated Workflow**
   - Daily sync pipeline
   - Data validation
   - Email alerts
   
4. **Streamlit Dashboard**
   - Expense visualization
   - Budget tracking
   - Spending insights

## 📊 Project Files

### Notebooks (5 total)
| # | Name | Purpose | Time |
|---|------|---------|------|
| 01 | setup-lakebase | Create PostgreSQL instance | 30 min* |
| 02 | create-schema | Define tables & load data | 15 min |
| 03 | sync-pipeline | Sync OLTP → OLAP | 20 min |
| 04 | workflow-automation | Setup scheduled jobs | 15 min |
| 05 | validate-results | Data quality checks | 10 min |

*Includes 15-30 min provisioning wait time

### App Files (3 total)
- `app.py` - Streamlit dashboard (280 lines)
- `config.py` - Configuration settings
- `requirements.txt` - Dependencies

### Configuration (3 files)
- `lakebase-config.json` - Database settings
- `workflow-config.json` - Job definition
- `app-config.json` - App settings

### Data (2 files)
- `sample-categories.csv` - 10 categories
- `sample-expenses.csv` - 50 sample expenses

### Documentation (2 guides)
- `setup-guide.md` - Step-by-step setup
- `validation-guide.md` - Data validation

## 🔄 Data Flow

```
1. Input Data
   └─▶ Lakebase PostgreSQL (OLTP)
       ├─ categories table
       ├─ expenses table  
       └─ budgets table

2. Sync Pipeline (Daily)
   └─▶ Unity Catalog (OLAP)
       ├─ categories (Delta)
       ├─ expenses (Delta)
       ├─ budgets (Delta)
       ├─ monthly_spending_by_category (View)
       └─ budget_vs_actual (View)

3. Visualization
   └─▶ Databricks App (Streamlit)
       ├─ Overview dashboard
       ├─ Expense details
       ├─ Budget monitoring
       └─ Analytics charts
```

## 🎨 Features Showcase

### Lakebase (OLTP)
✅ PostgreSQL instance creation
✅ ACID transactions
✅ Foreign key constraints
✅ SSL connections
✅ Backup configuration

### Lakehouse (OLAP)  
✅ Unity Catalog integration
✅ Delta Lake format
✅ Incremental sync
✅ Analytics views
✅ Time travel queries

### Workflows
✅ Multi-task jobs
✅ Task dependencies
✅ Cron scheduling
✅ Email notifications
✅ Error handling

### Apps
✅ Interactive dashboard
✅ Real-time data
✅ Multiple visualizations
✅ Budget alerts
✅ Export capabilities

## 📈 Sample Outputs

### Budget Status (from validation)
```
Category      | Budget | Actual | Remaining | Status
--------------|--------|--------|-----------|-------------
Groceries     | $600   | $545   | $55       | 🟢 OK
Dining Out    | $300   | $385   | -$85      | 🔴 OVER
Transportation| $400   | $320   | $80       | 🟢 OK
Shopping      | $300   | $425   | -$125     | 🔴 OVER
Entertainment | $200   | $195   | $5        | 🟡 WARNING
```

### Monthly Spending (from analytics)
```
Month   | Category       | Expenses | Total    | Avg
--------|----------------|----------|----------|-------
2024-12 | Shopping       | 8        | $1,250   | $156
2024-12 | Groceries      | 12       | $890     | $74
2024-12 | Dining Out     | 15       | $680     | $45
2024-12 | Transportation | 20       | $650     | $33
```

## ⚡ Quick Start Commands

```bash
# 1. Navigate to project
cd "Personal Expense Tracker"

# 2. Run notebooks in Databricks in order:
# 01-setup-lakebase.ipynb
# 02-create-schema.ipynb
# 03-sync-pipeline.ipynb
# 04-workflow-automation.ipynb
# 05-validate-results.ipynb

# 3. Deploy app (if running locally)
cd apps/expense-tracker
pip install -r requirements.txt
streamlit run app.py
```

## 🎓 Key Learnings

### Database Design
- Normalized vs denormalized schemas
- OLTP vs OLAP patterns
- Referential integrity

### Data Engineering
- ETL pipeline design
- Incremental data sync
- Data validation strategies

### Data Analytics
- Aggregation patterns
- View materialization
- Query optimization

### DevOps
- Workflow automation
- Monitoring and alerting
- CI/CD concepts

## 🔍 Testing Checklist

After setup, verify:
- [ ] All 5 notebooks run successfully
- [ ] 3 tables exist in Unity Catalog
- [ ] 2 views return data
- [ ] Workflow job created
- [ ] Validation passes (0 errors)
- [ ] App displays data

## 💡 Tips

1. **Start Simple:** Use sample data first, then add real data
2. **Check Permissions:** Ensure Unity Catalog access
3. **Monitor Costs:** Use small clusters for demo
4. **Save Outputs:** Keep notebook results for reference
5. **Customize:** Adjust budgets and categories to your needs

## 🆘 Quick Troubleshooting

| Issue | Quick Fix |
|-------|-----------|
| Lakebase unavailable | Skip notebook 01, use sample data |
| Sync fails | Check Unity Catalog permissions |
| Workflow won't run | Verify cluster is available |
| App won't connect | Update warehouse ID in config |
| No data showing | Re-run sync pipeline (notebook 03) |

## 📞 Support Resources

1. **Setup Issues:** See `setup-guide.md`
2. **Data Problems:** See `validation-guide.md`
3. **Errors:** Check notebook outputs
4. **General:** Databricks documentation

## 📦 Deliverables

After completion, you'll have:
- ✅ Working OLTP database (Lakebase)
- ✅ Analytics lakehouse (Unity Catalog)
- ✅ Automated sync pipeline (Workflows)
- ✅ Interactive dashboard (Apps)
- ✅ Complete documentation
- ✅ Validation framework
- ✅ Sample data for testing

## 🎯 Success Criteria

Project is complete when:
1. All notebooks execute without errors
2. Data syncs to Unity Catalog
3. Validation shows 0 failures
4. Workflow runs successfully
5. App displays expense data
6. Budget status calculates correctly

---

**Ready to start?** Open `01-setup-lakebase.ipynb` and follow the setup guide!

**Questions?** Check the documentation folder for detailed guides.

**Enjoy building! 🚀**

