# Personal Expense Tracker - Validation Guide

## Overview
This guide explains the validation checks performed by the expense tracker system and how to interpret the results.

## Validation Notebooks

### Notebook: 05-validate-results.ipynb

This notebook performs comprehensive validation of the expense tracker data pipeline.

## Validation Categories

### 1. Table Existence Checks

**Purpose:** Verify that all required tables exist and contain data.

**Tables Validated:**
- `main.expense_tracker.categories`
- `main.expense_tracker.expenses`
- `main.expense_tracker.budgets`
- `main.expense_tracker.monthly_spending_by_category` (view)
- `main.expense_tracker.budget_vs_actual` (view)

**Expected Results:**
```
✓ main.expense_tracker.categories: 10 rows
✓ main.expense_tracker.expenses: 150+ rows
✓ main.expense_tracker.budgets: 9 rows
```

**Failure Indicators:**
- ✗ Table: NOT FOUND
- 0 rows in any table

**Resolution:**
1. Re-run notebook `02-create-schema.ipynb` to create missing tables
2. Re-run notebook `03-sync-pipeline.ipynb` to sync data
3. Check Unity Catalog permissions

---

### 2. Data Quality Checks

**Purpose:** Ensure data integrity and completeness.

#### Check: Null Values in Critical Fields

**Query:**
```sql
SELECT 
    table_name,
    SUM(CASE WHEN primary_key IS NULL THEN 1 ELSE 0 END) as null_pk,
    SUM(CASE WHEN critical_field IS NULL THEN 1 ELSE 0 END) as null_field
FROM tables
```

**Expected Results:**
- All primary keys: 0 null values
- Category names: 0 null values
- Expense amounts: 0 null values
- Budget amounts: 0 null values

**Failure Indicators:**
- Any null values in primary keys
- Null values in required fields

**Resolution:**
1. Identify source of null values
2. Check data insertion logic in notebook 02
3. Update validation rules in source system
4. Re-insert affected records

---

### 3. Referential Integrity Checks

**Purpose:** Verify foreign key relationships are valid.

#### Check: Orphaned Expenses

**Query:**
```sql
SELECT COUNT(*) as orphaned_expenses
FROM expenses e
LEFT JOIN categories c ON e.category_id = c.category_id
WHERE c.category_id IS NULL
```

**Expected Result:** `0 orphaned_expenses`

**Failure Indicators:**
- Count > 0

**Resolution:**
1. Identify invalid category_id values in expenses
2. Check if categories were deleted
3. Update expenses with valid category_id
4. Add foreign key constraints

#### Check: Orphaned Budgets

**Query:**
```sql
SELECT COUNT(*) as orphaned_budgets
FROM budgets b
LEFT JOIN categories c ON b.category_id = c.category_id
WHERE c.category_id IS NULL
```

**Expected Result:** `0 orphaned_budgets`

**Failure Indicators:**
- Count > 0

**Resolution:**
1. Identify invalid category_id values in budgets
2. Update budgets with valid category_id
3. Add referential integrity constraints

---

### 4. Business Logic Validation

**Purpose:** Ensure data follows business rules.

#### Check: Invalid Amounts

**Query:**
```sql
SELECT 
    COUNT(*) as invalid_amount_count,
    MIN(amount) as min_amount
FROM expenses
WHERE amount <= 0
```

**Expected Results:**
- `invalid_amount_count: 0`
- `min_amount > 0`

**Failure Indicators:**
- Negative or zero amounts
- Unrealistic amounts (e.g., > $10,000)

**Resolution:**
1. Review data entry process
2. Add validation at input
3. Correct invalid records
4. Add CHECK constraints

#### Check: Future Dates

**Query:**
```sql
SELECT COUNT(*) as future_date_count
FROM expenses
WHERE expense_date > CURRENT_DATE
```

**Expected Result:** `0 future_date_count`

**Failure Indicators:**
- Count > 0

**Resolution:**
1. Correct future dates to actual dates
2. Add date validation at input
3. Set max date to CURRENT_DATE

---

### 5. Summary Statistics

**Purpose:** Provide overview of expense data for reasonableness checks.

#### Overall Expense Statistics

**Metrics:**
- Total expenses count
- Unique categories used
- Date range (earliest to latest)
- Total amount
- Average expense amount
- Min/Max amounts

**Expected Ranges:**
- Total expenses: > 0
- Unique categories: 1-10
- Date range: Last 90 days
- Average amount: $20 - $500
- Min amount: > $0
- Max amount: < $10,000 (depends on your spending)

**Interpretation:**
- **Low total expenses:** May indicate sync issues
- **Few categories:** Check if all categories are being used
- **Old date range:** Sync may not be running
- **Extreme averages:** Review for data quality issues

#### Spending by Category

**Metrics per category:**
- Expense count
- Total spent
- Average expense

**Expected Patterns:**
- Essential categories (Groceries, Utilities) have higher totals
- Lifestyle categories vary by personal habits
- Investment categories may have fewer but larger amounts

**Red Flags:**
- Zero spending in essential categories
- Extreme spending in any single category
- Suspicious patterns (all same amounts)

#### Budget Status

**Metrics:**
- Budget amount
- Actual spent
- Remaining
- Percent used
- Status (OK / WARNING / OVER BUDGET)

**Status Definitions:**
- 🟢 **OK**: < 90% of budget used
- 🟡 **WARNING**: 90-100% of budget used
- 🔴 **OVER BUDGET**: > 100% of budget used

**Expected Results:**
- Mix of OK, WARNING, and OVER statuses is normal
- Consistent OVER BUDGET suggests unrealistic budgets
- All OK might indicate budgets are too high

**Actions:**
- **OVER BUDGET**: Review expenses, adjust future spending
- **WARNING**: Monitor closely, reduce discretionary spending
- **OK**: Budget is working well

---

## Validation Report Format

The validation notebook generates a comprehensive report:

```
================================================================================
VALIDATION REPORT
================================================================================
Generated: 2024-12-24 10:30:00
Schema: main.expense_tracker

Table Counts:
  categories: 10
  expenses: 234
  budgets: 9

Validation Status:
  ✓ categories: 10 rows
  ✓ expenses: 234 rows
  ✓ budgets: 9 rows

✓ All validation checks PASSED
================================================================================
```

## Interpreting Results

### All Checks Pass ✓
**Meaning:** Data pipeline is healthy and working correctly.

**Actions:**
- Continue normal operations
- Review spending insights
- Update budgets as needed

### Some Checks Fail ✗
**Meaning:** Data quality issues detected.

**Priority Actions:**
1. **High Priority** (Fix immediately):
   - Null primary keys
   - Orphaned records
   - Negative amounts

2. **Medium Priority** (Fix within 1 day):
   - Future dates
   - Missing expected data
   - Sync delays

3. **Low Priority** (Monitor):
   - Budget warnings
   - Unusual spending patterns
   - Date range gaps

## Automated Validation

### Workflow Integration

The validation notebook is integrated into the workflow:
```
Task 1: sync_expenses (03-sync-pipeline.ipynb)
    ↓
Task 2: validate_results (05-validate-results.ipynb)
```

**Email Notifications:**
- Sent on validation failures
- Includes error summary
- Links to job run logs

### Continuous Monitoring

**Recommended Schedule:**
- **Daily validation**: Run at 2 AM after sync
- **Weekly review**: Check trends and patterns
- **Monthly audit**: Deep dive into spending

## Common Issues and Solutions

### Issue: Tables Have 0 Rows

**Symptoms:**
- All tables empty
- "NOT FOUND" errors

**Causes:**
- Sync hasn't run yet
- Sync failed
- Permissions issues

**Solutions:**
1. Run sync pipeline manually
2. Check workflow logs
3. Verify Unity Catalog permissions
4. Re-run schema creation

### Issue: Data is Stale

**Symptoms:**
- Latest expense date is old
- New expenses not appearing

**Causes:**
- Workflow not scheduled
- Sync failing silently
- Lakebase connectivity issues

**Solutions:**
1. Check workflow schedule
2. Review job run history
3. Test Lakebase connection
4. Run sync manually

### Issue: Budget Shows Wrong Status

**Symptoms:**
- OVER BUDGET when shouldn't be
- Incorrect percentages

**Causes:**
- Budget amounts not updated
- Expenses in wrong category
- Date range mismatch

**Solutions:**
1. Verify budget amounts
2. Check expense categorization
3. Review date filters in view
4. Re-calculate budget view

### Issue: Duplicate Expenses

**Symptoms:**
- Same expense appears multiple times
- Inflated totals

**Causes:**
- Sync running multiple times
- No deduplication logic
- Primary key issues

**Solutions:**
1. Add DISTINCT to queries
2. Implement idempotent sync
3. Use MERGE instead of INSERT
4. Clean up duplicates manually

## Data Quality Metrics

### Key Performance Indicators (KPIs)

**Data Completeness:**
- Target: 100% of expected tables exist
- Measure: Count of existing tables / expected tables

**Data Freshness:**
- Target: Data < 24 hours old
- Measure: Current time - MAX(expense_date)

**Data Accuracy:**
- Target: 0 validation errors
- Measure: Sum of all failed checks

**Referential Integrity:**
- Target: 0 orphaned records
- Measure: Count of foreign key violations

### Monitoring Dashboard

Create a monitoring dashboard with:
1. **Data Quality Score** (0-100)
2. **Last Sync Time**
3. **Error Count** (last 7 days)
4. **Data Volume** (rows per table)

## Best Practices

### Regular Validation

1. **Run validation after every sync**
2. **Review validation reports weekly**
3. **Address failures immediately**
4. **Track trends over time**

### Alerting

Set up alerts for:
- Validation failures
- Data staleness (> 24 hours)
- Budget thresholds (> 90%)
- Unusual spending patterns

### Documentation

Document:
- Expected data ranges
- Validation failure procedures
- Contact information
- Escalation paths

## Appendix: Validation Queries

### Complete Validation SQL

```sql
-- Run all validations at once
WITH table_counts AS (
  SELECT 'categories' as table_name, COUNT(*) as row_count FROM categories
  UNION ALL
  SELECT 'expenses', COUNT(*) FROM expenses
  UNION ALL
  SELECT 'budgets', COUNT(*) FROM budgets
),
null_checks AS (
  SELECT 
    COUNT(*) as null_count,
    'expenses' as table_name
  FROM expenses
  WHERE expense_id IS NULL OR amount IS NULL
),
integrity_checks AS (
  SELECT COUNT(*) as orphaned_count FROM expenses e
  LEFT JOIN categories c ON e.category_id = c.category_id
  WHERE c.category_id IS NULL
)
SELECT * FROM table_counts
UNION ALL
SELECT table_name, null_count FROM null_checks
UNION ALL
SELECT 'orphaned_expenses', orphaned_count FROM integrity_checks;
```

---

**Last Updated:** December 24, 2024
**Version:** 1.0
**Maintained by:** Expense Tracker Team

