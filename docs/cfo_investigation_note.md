# If the CFO Asks Why Monday’s Revenue Changed by 3%

If a reported revenue number changes unexpectedly, the first priority is to understand whether the issue is business-related or pipeline-related.

The goal would be to narrow down the root cause within 10 minutes using the warehouse tables and data quality checks already built into the pipeline.

---

# Step 1: Check Whether All Files Arrived

The first thing I would verify is whether all expected sales files were successfully ingested.

A delayed or missing file can immediately impact reported revenue.

I would compare:
- expected reporting dates
- ingested file logs
- row counts by day

---

# Step 2: Validate Duplicate Handling

Next, I would check whether duplicate transactions were introduced or removed during ingestion.

Since the pipeline removes duplicate order_ids, a change in duplicate counts could affect the final revenue number.

---

# Step 3: Review Schema Validation Logs

I would then verify whether any files were excluded because of schema mismatches or malformed columns.

If a file failed validation, its revenue would not appear in the dashboard until corrected.

---

# Step 4: Check Missing or Invalid Records

I would inspect whether there was a spike in rows with missing critical fields.

For example:
- missing product IDs
- missing quantities
- incomplete timestamps

Those records are intentionally excluded from KPI calculations to protect reporting accuracy.

---

# Step 5: Compare Business Drivers

Once the pipeline checks are cleared, I would compare business performance drivers across days.

Main areas to investigate:
- regional sales shifts
- product-level revenue movement
- order volume changes
- discount spikes

This helps determine whether the change is operational or genuinely business-driven.

---

# Final Validation

Before confirming the number to leadership, I would validate that:
- all files were ingested
- duplicate handling worked correctly
- schema checks passed
- revenue calculations matched warehouse totals

This process ensures the final reported revenue number is explainable, traceable, and trustworthy.