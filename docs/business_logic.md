# Business Logic Documentation

## Purpose

This document explains the core business logic used inside the Revenue Intelligence Pipeline and Dashboard.

The objective is to ensure:
- KPI consistency
- trusted executive reporting
- transparent metric calculations
- reliable downstream analytics

---

# Revenue Calculation

Revenue is calculated at transaction level using:

Revenue = qty × unit_price × (1 - discount_pct)

Example:

| qty | unit_price | discount_pct | revenue |
|---|---|---|---|
| 2 | 50 | 0.10 | 90 |

Formula:

2 × 50 × (1 - 0.10) = 90

---

# Daily Revenue

Daily revenue is calculated by aggregating all validated transaction revenue for a given date.

Used in:
- executive KPI reporting
- revenue trend charts
- moving averages
- volatility analysis

---

# Average Order Value (AOV)

AOV measures average revenue generated per order.

Formula:

Average Order Value = Total Revenue / Total Orders

Used to understand:
- customer purchasing behavior
- transaction efficiency
- pricing effectiveness

---

# Top Product Logic

Products are ranked using total revenue contribution.

Formula:

Product Contribution % =
(Product Revenue / Total Revenue) × 100

Used in:
- top product KPI card
- product intelligence reporting
- contribution analysis

---

# Regional Revenue Contribution

Regional contribution is calculated as:

Region Contribution % =
(Regional Revenue / Total Revenue) × 100

Used for:
- regional performance analysis
- identifying high-performing markets
- executive territory monitoring

---

# Revenue Trend Analysis

The dashboard tracks:
- daily revenue
- revenue volatility
- 7-day moving average

The moving average smooths short-term fluctuations and highlights broader trends.

---

# Revenue Drop Analysis

Revenue drops are identified when daily revenue declines significantly compared to the previous reporting day.

Formula:

Drop % =
((Previous Revenue - Current Revenue) / Previous Revenue) × 100

Purpose:
- identify unusual business dips
- monitor operational disruptions
- detect ingestion inconsistencies
- improve executive visibility

---

# Duplicate Handling Logic

Duplicate transactions are identified using:

order_id

Only unique order_ids are retained in reporting tables.

Purpose:
- prevent double counting
- support idempotent reruns
- maintain reporting accuracy

---

# Missing Value Handling

Rows with missing business-critical values are isolated from KPI reporting.

Critical fields include:
- order_id
- order_timestamp
- qty
- unit_price
- product_id

Purpose:
- protect executive metrics
- avoid distorted revenue calculations

---

# Data Quality Risk Score

The DQ Risk Score is a simplified health indicator derived from:
- duplicate volume
- missing value count
- schema consistency
- ingestion reliability

Purpose:
- quickly communicate reporting confidence
- surface operational risk to stakeholders

---

# Forecasting / Trend Smoothing

The dashboard uses a 7-day moving average instead of predictive forecasting.

Reason:
- simpler interpretation
- avoids misleading projections
- provides stable executive trend visibility

---

# Idempotency Logic

The ingestion layer prevents duplicate loading during reruns.

Before insertion:
- existing order_ids are checked
- already processed transactions are excluded

Purpose:
- ensure reruns remain safe
- avoid warehouse inflation
- maintain trusted reporting