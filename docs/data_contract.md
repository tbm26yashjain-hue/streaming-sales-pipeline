# Data Contract

## Overview

This pipeline processes daily sales CSV files shared by the e-commerce operations team. Since multiple teams use the same data for reporting, the goal of this contract is to ensure everyone works from a single trusted version of revenue and sales metrics.

---

# File Expectations

## File Naming

Each file is expected in the following format:

sales_YYYY-MM-DD.csv

Example:
sales_2025-03-01.csv

---

# Expected Columns

| Column | Description |
|---|---|
| order_id | Unique order ID |
| order_timestamp | Time when the order was placed |
| customer_id | Customer identifier |
| product_id | Product identifier |
| product_name | Product name |
| category | Product category |
| qty | Quantity purchased |
| unit_price | Price per unit |
| discount_pct | Discount applied |
| region | Region where the order was placed |

---

# What the Pipeline Checks

## Duplicate Orders

An order_id should appear only once.

If duplicate rows are found, the pipeline keeps only one copy to avoid inflated revenue numbers.

---

## Schema Validation

All incoming files are expected to follow the same structure and column order.

If a file contains unexpected columns or missing fields, it is flagged and excluded from the trusted reporting layer.

---

## Missing Values

Some fields are critical for reporting:
- order_id
- order_timestamp
- product_id
- qty
- unit_price

If any of these are missing, those rows are isolated from KPI calculations.

---

## Late Arriving Files

The pipeline scans folders recursively, including nested folders, so late-arriving files can still be picked up automatically.

---

## Revenue Logic

Revenue is recalculated during ingestion using:

qty * unit_price * (1 - discount_pct)

This avoids inconsistencies across teams calculating revenue differently.

---

# Warehouse Layer

Cleaned and validated data is stored in DuckDB:

warehouse/sales.duckdb

Main trusted table:
sales_clean

---

# Dashboard Dependency

The dashboard reads only from trusted warehouse tables and not directly from raw CSV files.

This ensures all metrics shown to leadership are based on validated and cleaned data.