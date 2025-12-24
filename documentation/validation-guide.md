# Personal Expense Tracker - Validation Guide

This guide helps you validate that your Personal Expense Tracker setup is working correctly.

## Validation Checklist

### 1. Lakebase Instance Validation

**Check:**
- [ ] Instance status is READY
- [ ] Connection details are available
- [ ] SSL connection works
- [ ] Can connect to PostgreSQL database

**Validation Steps:**
1. Run `notebooks/01-setup-lakebase.ipynb`
2. Verify instance status shows READY
3. Check connection details are populated in `configuration/lakebase-config.json`
4. Test connection using the optional test cell

**Expected Results:**
- Instance ID is present
- Host, port, and credentials are available
- Connection string is generated
- PostgreSQL version query succeeds

### 2. Database Schema Validation

**Check:**
- [ ] Tables are created successfully
- [ ] Primary keys and foreign keys are set up
- [ ] Indexes are created
- [ ] Constraints are enforced

**Validation Steps:**
1. Run `notebooks/02-create-schema.ipynb`
2. Query information_schema to verify tables
3. Check table structures match expected schema
4. Verify relationships between tables

**Expected Results:**
- `expenses` table exists with correct columns
- `categories` table exists with correct columns
- Foreign key relationship is established
- Indexes are created on key columns

### 3. Data Sync Validation

**Check:**
- [ ] Data syncs from Lakebase to Lakehouse
- [ ] Data integrity is maintained
- [ ] Incremental sync works correctly
- [ ] Error handling works

**Validation Steps:**
1. Insert test data into Lakebase
2. Run `notebooks/03-sync-pipeline.ipynb`
3. Verify data appears in Lakehouse tables
4. Check row counts match
5. Validate data types and values

**Expected Results:**
- All rows synced successfully
- No data loss or corruption
- Timestamps are correct
- Data types match source

### 4. Workflow Validation

**Check:**
- [ ] Workflow is created successfully
- [ ] Schedule is configured correctly
- [ ] Tasks run without errors
- [ ] Notifications work (if configured)

**Validation Steps:**
1. Run `notebooks/04-workflow-automation.ipynb`
2. Verify workflow appears in Databricks UI
3. Trigger a manual run
4. Check run history and logs
5. Verify scheduled runs execute

**Expected Results:**
- Workflow is visible in UI
- Manual run completes successfully
- Scheduled runs execute on time
- Logs show successful execution

### 5. Application Validation

**Check:**
- [ ] App deploys successfully
- [ ] App connects to database
- [ ] CRUD operations work
- [ ] UI displays correctly

**Validation Steps:**
1. Deploy the app from `apps/expense-tracker/`
2. Access the app URL
3. Test creating an expense
4. Test reading expenses
5. Test updating an expense
6. Test deleting an expense

**Expected Results:**
- App loads without errors
- Database operations succeed
- Data displays correctly
- No runtime errors

## Data Validation Queries

### Count Records
```sql
-- Lakebase (PostgreSQL)
SELECT COUNT(*) FROM expenses;
SELECT COUNT(*) FROM categories;

-- Lakehouse (Delta)
SELECT COUNT(*) FROM main.expense_tracker.expenses;
```

### Data Integrity Check
```sql
-- Check foreign key relationships
SELECT e.*, c.category_name
FROM expenses e
LEFT JOIN categories c ON e.category_id = c.category_id
WHERE c.category_id IS NULL;
```

### Date Range Validation
```sql
-- Check expense dates are valid
SELECT MIN(expense_date) as min_date, MAX(expense_date) as max_date
FROM expenses;
```

## Performance Validation

### Query Performance
- Measure query execution time
- Check for slow queries
- Verify indexes are being used

### Sync Performance
- Measure sync duration
- Check for bottlenecks
- Verify incremental sync efficiency

## Error Scenarios to Test

1. **Database Connection Failure**
   - Disconnect network
   - Verify error handling
   - Check retry logic

2. **Invalid Data**
   - Insert invalid data
   - Verify constraint enforcement
   - Check error messages

3. **Workflow Failure**
   - Cause a task failure
   - Verify error notifications
   - Check retry behavior

4. **Concurrent Access**
   - Multiple users accessing app
   - Verify data consistency
   - Check for race conditions

## Validation Script

Run the validation notebook `notebooks/05-validate-results.ipynb` for automated validation.

## Common Issues

### Issue: Instance Not Ready
**Solution:** Wait longer or check instance status in Databricks UI

### Issue: Connection Timeout
**Solution:** Check network connectivity and firewall rules

### Issue: Data Not Syncing
**Solution:** Verify workflow is running and check logs for errors

### Issue: App Not Loading
**Solution:** Check app logs and verify database connection

## Reporting Issues

When reporting issues, include:
1. Error messages
2. Relevant logs
3. Configuration files (sanitized)
4. Steps to reproduce
5. Expected vs actual behavior

