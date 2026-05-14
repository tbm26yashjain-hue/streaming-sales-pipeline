# Revenue Intelligence Platform

## Overview

This project was built to solve a common reporting problem inside an e-commerce business: different teams calculating different revenue numbers from the same raw sales data.

The goal was to create a trusted analytics pipeline that ingests daily CSV files, validates data quality, loads cleaned data into a warehouse, and powers an executive dashboard with consistent KPIs.

---

# Problem Statement

Daily sales CSVs were being shared across teams with:
- duplicate records
- schema inconsistencies
- late-arriving files
- missing values

As a result, revenue reporting was inconsistent across finance, operations, and business teams.

This pipeline creates a single trusted reporting layer for leadership dashboards.

---

# Architecture

Raw CSV Files
↓
Python Ingestion Pipeline
↓
Data Quality Validation
↓
DuckDB Warehouse
↓
SQL / DBT-style Transformation Models
↓
Streamlit Executive Dashboard

---

# Tech Stack

| Layer | Technology |
|---|---|
| Ingestion | Python |
| Warehouse | DuckDB |
| Transformation | SQL / DBT-style models |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Data Processing | Pandas |

---

# Pipeline Features

## Ingestion

- Recursive CSV ingestion
- Late-arriving file detection
- Batch processing
- Idempotent re-runs

---

## Data Quality Checks

The pipeline validates:

- duplicate order IDs
- schema consistency
- missing critical fields
- revenue anomalies
- late-arriving files

---

## Revenue Logic

Revenue is calculated using:

```python
qty * unit_price * (1 - discount_pct)