import os
import pandas as pd
import duckdb

# =====================================================
# START PIPELINE
# =====================================================

print("Pipeline Started")

# =====================================================
# CONNECT TO DUCKDB
# =====================================================

conn = duckdb.connect(
    "warehouse/sales.duckdb"
)

# =====================================================
# EXPECTED SCHEMA
# =====================================================

EXPECTED_COLUMNS = [
    'order_id',
    'order_timestamp',
    'customer_id',
    'product_id',
    'product_name',
    'category',
    'qty',
    'unit_price',
    'discount_pct',
    'region'
]

# =====================================================
# FIND ALL CSV FILES
# =====================================================

csv_files = []

for root, dirs, files in os.walk("data/raw"):

    for file in files:

        if file.endswith(".csv"):

            full_path = os.path.join(
                root,
                file
            )

            csv_files.append(full_path)

print(f"CSV files found: {len(csv_files)}")

# =====================================================
# READ FILES
# =====================================================

all_dfs = []

schema_issues = []

for file in csv_files:

    print(f"Reading: {file}")

    try:

        df = pd.read_csv(file)

        # =================================================
        # SCHEMA VALIDATION
        # =================================================

        current_columns = list(df.columns)

        if current_columns != EXPECTED_COLUMNS:

            print(f"Schema mismatch detected: {file}")

            schema_issues.append(file)

            continue

        # =================================================
        # ADD SOURCE FILE
        # =================================================

        df['source_file'] = file

        all_dfs.append(df)

    except Exception as e:

        print(f"Error reading {file}")

        print(e)

# =====================================================
# CHECK IF FILES WERE READ
# =====================================================

if len(all_dfs) == 0:

    print("No valid files found")

    exit()

# =====================================================
# COMBINE DATAFRAMES
# =====================================================

final_df = pd.concat(
    all_dfs,
    ignore_index=True
)

print(
    f"Total rows before cleaning: {len(final_df)}"
)

# =====================================================
# REMOVE DUPLICATES INSIDE BATCH
# =====================================================

duplicate_count = final_df.duplicated(
    subset=['order_id']
).sum()

print(
    f"Duplicate orders detected in batch: {duplicate_count}"
)

final_df = final_df.drop_duplicates(
    subset=['order_id']
)

# =====================================================
# REVENUE CALCULATION
# =====================================================

final_df['revenue'] = (
    final_df['qty']
    * final_df['unit_price']
    * (1 - final_df['discount_pct'])
)

print("Revenue column created")

# =====================================================
# HANDLE MISSING VALUES
# =====================================================

missing_values = (
    final_df.isnull()
    .sum()
    .sum()
)

print(
    f"Missing values detected: {missing_values}"
)

# =====================================================
# ISOLATE INVALID RECORDS
# =====================================================

critical_columns = [
    'order_id',
    'order_timestamp',
    'product_id',
    'qty',
    'unit_price'
]

invalid_records = final_df[
    final_df[critical_columns]
    .isnull()
    .any(axis=1)
]

valid_df = final_df.drop(
    invalid_records.index
)

print(
    f"Invalid records isolated: {len(invalid_records)}"
)

print(
    f"Valid records remaining: {len(valid_df)}"
)

# =====================================================
# IDEMPOTENT RE-RUN LOGIC
# =====================================================

existing_table = conn.execute("""

SELECT COUNT(*)
FROM information_schema.tables
WHERE table_name = 'sales_clean'

""").fetchone()[0]

if existing_table > 0:

    print(
        "Existing sales_clean table detected"
    )

    existing_orders = conn.execute("""

    SELECT DISTINCT order_id
    FROM sales_clean

    """).fetchdf()

    existing_ids = set(
        existing_orders['order_id']
    )

    before_filter = len(valid_df)

    valid_df = valid_df[
        ~valid_df['order_id']
        .isin(existing_ids)
    ]

    after_filter = len(valid_df)

    skipped_rows = (
        before_filter - after_filter
    )

    print(
        f"Existing records skipped: {skipped_rows}"
    )

else:

    print(
        "No existing warehouse table found"
    )

# =====================================================
# CREATE OR APPEND TABLE
# =====================================================

if existing_table == 0:

    conn.execute("""

    CREATE TABLE sales_clean AS
    SELECT * FROM valid_df

    """)

    print(
        "sales_clean table created"
    )

else:

    conn.register(
        "new_sales_data",
        valid_df
    )

    conn.execute("""

    INSERT INTO sales_clean
    SELECT * FROM new_sales_data

    """)

    print(
        "New records appended"
    )

# =====================================================
# FINAL VALIDATION
# =====================================================

final_row_count = conn.execute("""

SELECT COUNT(*)
FROM sales_clean

""").fetchone()[0]

print(
    f"Final warehouse row count: {final_row_count}"
)

# =====================================================
# SHOW TABLES
# =====================================================

tables = conn.execute(
    "SHOW TABLES"
).fetchall()

print("Tables in warehouse:")

print(tables)

# =====================================================
# SCHEMA ISSUE REPORT
# =====================================================

if len(schema_issues) > 0:

    print("Files with schema issues:")

    for issue in schema_issues:

        print(issue)

else:

    print("No schema issues detected")

# =====================================================
# PIPELINE COMPLETE
# =====================================================

print(
    "Trusted analytics table ready for dashboard."
)

print(
    "Pipeline completed successfully."
)