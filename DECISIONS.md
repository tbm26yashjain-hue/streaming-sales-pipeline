# Technical Decisions & AI Usage Disclosure

## Project Overview

This project was built as an end-to-end analytics engineering pipeline for trusted revenue reporting using:
- Python
- DuckDB
- SQL / DBT-style transformations
- Streamlit
- Plotly

The goal was to create a centralized and explainable reporting layer for executive stakeholders.

---

# AI Usage Disclosure

AI-assisted tools were used during development for:
- debugging environment and deployment issues
- improving dashboard UI structure
- brainstorming modular pipeline organization
- refining documentation and presentation wording
- accelerating repetitive boilerplate generation

Primary assistance included:
- ChatGPT
- Claude.ai

All architectural decisions, debugging iterations, implementation validation, and final integration were reviewed, modified, and understood before submission.

Non-trivial logic such as:
- idempotent ingestion
- duplicate prevention
- DuckDB warehouse integration
- data quality checks
- and dashboard calculations

can be fully explained independently.

---

# Key Technical Decisions

## Why DuckDB?

DuckDB was selected because:
- lightweight setup
- no infrastructure overhead
- fast analytical performance
- easy local deployment
- ideal for medium-scale CSV analytics

Trade-off:
DuckDB is not intended for large multi-user production workloads, but the architecture is designed for future migration to Snowflake or BigQuery.

---

## Why Python for Ingestion?

Python provided:
- flexible file handling
- easy recursive ingestion
- strong Pandas integration
- fast iteration for data quality logic

The ingestion layer handles:
- recursive CSV loading
- duplicate prevention
- schema validation
- missing value checks
- revenue standardization

---

## Why Modular Quality Checks?

Data quality checks were separated into:
- schema validation
- duplicate checks
- missing value checks
- freshness checks

This improves:
- maintainability
- debugging
- scalability
- testability

and prevents one failure from cascading through the entire pipeline.

---

## Why Idempotent Reruns?

Revenue pipelines must avoid duplicate inflation.

The ingestion logic validates:
- existing order_ids
before insertion.

This ensures rerunning the same files does not duplicate records or inflate revenue metrics.

---

## Why Streamlit?

Streamlit was selected because:
- rapid dashboard development
- lightweight deployment
- simple DuckDB integration
- strong executive dashboard capabilities

The dashboard prioritizes:
- KPI visibility
- trend monitoring
- regional analysis
- product intelligence
- data quality visibility

instead of operational complexity.

---

## Why Moving Average Instead of Advanced Forecasting?

The dataset only covered one month of data.

Using ARIMA or Prophet with limited history would create misleading confidence.

A 7-day moving average was selected instead because it:
- smooths volatility
- remains interpretable
- avoids overfitting
- is more honest for short historical windows

---

# Future Improvements

With additional time, the next priorities would be:
- Airflow orchestration
- automated alerting
- cloud warehouse migration
- CI/CD deployment
- lineage tracking
- production monitoring
- advanced forecasting
- role-based dashboard access
