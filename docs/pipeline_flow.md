# Revenue Intelligence Pipeline Flow

## Overview

This project simulates a modern analytics pipeline used for executive revenue reporting.

The pipeline ingests raw sales files, validates data quality, transforms records into trusted analytical tables, and powers a Streamlit dashboard for business users.

---

# End-to-End Pipeline Flow

Raw CSV Files
↓
Python Ingestion Pipeline
↓
Data Quality Validation
↓
DuckDB Warehouse
↓
SQL / DBT Transformations
↓
Executive Dashboard
↓
Business Reporting & Insights

---

# Step 1: Raw Data Ingestion

Daily sales CSV files are stored inside:

data/raw/

The ingestion layer:
- reads all incoming CSV files
- standardizes column formats
- validates schemas
- combines datasets into a unified dataframe

Handled by:

ingestion/ingest_sales_data.py

---

# Step 2: Data Cleaning

The pipeline performs cleaning operations including:
- duplicate removal
- missing value handling
- type conversion
- invalid row isolation
- revenue calculation

Additional metadata such as:
- source_file
- ingestion date

is also attached for traceability.

---

# Step 3: Data Quality Checks

The quality layer validates:
- schema consistency
- duplicate orders
- missing values
- freshness expectations
- business rule sanity checks

Files:
- quality_checks/duplicate_checks.py
- quality_checks/missing_value_checks.py
- quality_checks/schema_checks.py
- quality_checks/freshness_checks.py

Purpose:
- protect executive KPIs
- prevent reporting corruption
- improve trust in business metrics

---

# Step 4: Warehouse Storage

Cleaned data is loaded into DuckDB.

Warehouse location:

warehouse/sales.duckdb

Main analytical table:

sales_clean

DuckDB was selected because:
- lightweight
- fast local analytics
- SQL compatible
- easy dashboard integration

---

# Step 5: SQL / DBT Transformations

Transformation logic creates reporting-ready models.

Location:
- transformations/sql/
- transformations/dbt/

Examples:
- revenue_daily.sql
- dim_products.sql
- sales_clean.sql

Purpose:
- separate raw ingestion from business logic
- create reusable analytical models
- improve maintainability

---

# Step 6: Executive Dashboard

The Streamlit dashboard connects directly to DuckDB and displays:
- revenue KPIs
- revenue trends
- moving averages
- product contribution
- regional distribution
- data quality monitoring

Dashboard file:

dashboard/app.py

Purpose:
- provide executive visibility
- support fast business decision-making
- simplify reporting access

---

# Step 7: Monitoring & Investigation

The pipeline supports operational monitoring using:
- DQ risk scores
- duplicate tracking
- revenue volatility analysis
- missing value monitoring

This helps investigate:
- unexpected KPI shifts
- reporting discrepancies
- ingestion failures
- delayed source files

---

# Idempotent Reruns

The ingestion layer prevents duplicate loading using:
- order_id validation
- existing warehouse checks

This ensures rerunning the pipeline does not duplicate revenue.

---

# Key Technologies Used

| Component | Technology |
|---|---|
| Ingestion | Python |
| Validation | Pandas |
| Warehouse | DuckDB |
| Transformations | SQL / DBT |
| Dashboard | Streamlit |
| Visualization | Plotly |

---

# Final Outcome

The final system provides:
- trusted analytical reporting
- automated data validation
- clean executive dashboards
- transparent business metrics
- traceable revenue monitoring