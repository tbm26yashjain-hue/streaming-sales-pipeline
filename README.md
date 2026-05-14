# Revenue Intelligence Platform

Trusted executive reporting platform built using Python, DuckDB, SQL transformations, Streamlit, and modular data quality validation.

---

## Live Dashboard

https://streaming-sales-pipeline-dpcvh8tegeqy5ucipundey.streamlit.app/
---

## GitHub Repository

https://github.com/tbm26yashjain-hue/streaming-sales-pipeline

---

## Problem Statement

Business teams were reporting conflicting revenue numbers from the same sales files because:
- duplicate records existed
- malformed files entered reporting
- revenue logic differed across teams
- no centralized validation layer existed

The objective was to build:
- a trusted reporting layer
- automated data quality validation
- centralized KPI calculations
- and an executive-ready dashboard.

---

## Architecture Diagram

![Architecture](docs/architecture.png)

---

## Dashboard Preview

![Dashboard](docs/screenshots/dashboard.png)

---

## Key Features

### Data Ingestion
- Recursive CSV ingestion
- Late-arriving file support
- Idempotent reruns
- Revenue standardization

### Data Quality Validation
- Schema validation
- Duplicate checks
- Missing value checks
- Freshness validation
- Revenue anomaly monitoring

### Warehouse Layer
- DuckDB analytical warehouse
- Trusted reporting tables
- SQL / DBT-style transformations

### Executive Dashboard
- Revenue KPIs
- Revenue trends
- Regional contribution
- Product intelligence
- Data quality monitoring

---

## Tech Stack

| Layer | Technology |
|---|---|
| Ingestion | Python |
| Validation | Pandas |
| Warehouse | DuckDB |
| Transformations | SQL / DBT-style models |
| Dashboard | Streamlit |
| Visualization | Plotly |

---

## Data Quality Checks

| Check | Purpose |
|---|---|
| Schema Validation | Prevent malformed records |
| Duplicate Detection | Prevent revenue inflation |
| Missing Value Checks | Protect KPI accuracy |
| Freshness Validation | Detect delayed ingestion |
| Revenue Monitoring | Detect volatility anomalies |

---

## Business Outcome

The platform successfully created:
- one trusted revenue source
- centralized KPI logic
- visibility into data quality risks
- explainable revenue reporting

---

## Documentation

| Document | Purpose |
|---|---|
| `docs/data_contract.md` | Input expectations |
| `docs/business_logic.md` | KPI definitions |
| `docs/pipeline_flow.md` | Pipeline walkthrough |
| `docs/cfo_investigation_note.md` | Revenue discrepancy investigation |
| `DECISIONS.md` | Technical trade-offs & AI disclosure |

---

## Future Improvements

- Airflow orchestration
- Cloud warehouse migration
- Automated alerting
- Row-level lineage
- Advanced forecasting
- CI/CD deployment

---

## Author

Yash Jain
MBA Candidate · Analytics & Strategy