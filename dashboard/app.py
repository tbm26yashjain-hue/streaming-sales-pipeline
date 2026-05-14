import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import os
import glob

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Revenue Intelligence Platform",
    layout="wide"
)

# =====================================================
# CUSTOM STYLING
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

h1, h2, h3 {
    color: #111827;
}

[data-testid="metric-container"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("Revenue Intelligence Platform")

st.caption(
    "Trusted executive reporting layer for e-commerce sales analytics"
)

# =====================================================
# CREATE WAREHOUSE FOLDER
# =====================================================

if not os.path.exists("warehouse"):

    os.makedirs("warehouse")

# =====================================================
# CONNECT TO DUCKDB
# =====================================================

conn = duckdb.connect(
    "warehouse/sales.duckdb"
)

# =====================================================
# CHECK IF sales_clean EXISTS
# =====================================================

table_exists = conn.execute("""

SELECT COUNT(*)

FROM information_schema.tables

WHERE table_name = 'sales_clean'

""").fetchone()[0]

# =====================================================
# CREATE TABLE IF MISSING
# =====================================================

if table_exists == 0:

    csv_files = glob.glob(
        "data/raw/*.csv"
    )

    all_dfs = []

    for file in csv_files:

        temp_df = pd.read_csv(file)

        all_dfs.append(temp_df)

    df_combined = pd.concat(
        all_dfs,
        ignore_index=True
    )

    # Revenue Calculation

    df_combined['revenue'] = (
        df_combined['qty']
        * df_combined['unit_price']
        * (
            1 - df_combined['discount_pct']
        )
    )

    # Remove duplicates

    df_combined = df_combined.drop_duplicates(
        subset=['order_id']
    )

    conn.register(
        "temp_sales",
        df_combined
    )

    conn.execute("""

    CREATE TABLE sales_clean AS

    SELECT * FROM temp_sales

    """)

# =====================================================
# LOAD DATA
# =====================================================

df = conn.execute("""

SELECT *
FROM sales_clean

""").fetchdf()

# =====================================================
# DATE PROCESSING
# =====================================================

df['order_timestamp'] = pd.to_datetime(
    df['order_timestamp']
)

df['order_date'] = df[
    'order_timestamp'
].dt.date

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df['region'].unique(),
    default=df['region'].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df['category'].unique(),
    default=df['category'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [
        df['order_date'].min(),
        df['order_date'].max()
    ]
)

# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df[
    (df['region'].isin(regions))
    &
    (df['category'].isin(categories))
]

if len(date_range) == 2:

    filtered_df = filtered_df[
        (
            filtered_df['order_date']
            >= date_range[0]
        )
        &
        (
            filtered_df['order_date']
            <= date_range[1]
        )
    ]

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = filtered_df[
    'revenue'
].sum()

total_orders = filtered_df[
    'order_id'
].nunique()

avg_order_value = (
    total_revenue / total_orders
)

top_region = (
    filtered_df.groupby('region')['revenue']
    .sum()
    .idxmax()
)

top_product = (
    filtered_df.groupby('product_name')['revenue']
    .sum()
    .idxmax()
)

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

with col2:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col3:

    st.metric(
        "Average Order Value",
        f"${avg_order_value:,.2f}"
    )

with col4:

    st.metric(
        "Top Region",
        top_region
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "Revenue Trends",
    "Product Intelligence",
    "Data Quality"
])

# =====================================================
# TAB 1 — REVENUE
# =====================================================

with tab1:

    st.subheader(
        "Daily Revenue Trend"
    )

    revenue_daily = (
        filtered_df
        .groupby('order_date')['revenue']
        .sum()
        .reset_index()
    )

    revenue_daily[
        '7_day_avg'
    ] = revenue_daily[
        'revenue'
    ].rolling(7).mean()

    fig = px.line(
        revenue_daily,
        x='order_date',
        y=['revenue', '7_day_avg'],
        labels={
            'value': 'Revenue',
            'order_date': 'Date'
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Regional Revenue Distribution"
    )

    regional = (
        filtered_df
        .groupby('region')['revenue']
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        regional,
        values='revenue',
        names='region',
        hole=0.5
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# TAB 2 — PRODUCTS
# =====================================================

with tab2:

    st.subheader(
        "Top Product Performance"
    )

    product_perf = (
        filtered_df
        .groupby('product_name')['revenue']
        .sum()
        .reset_index()
        .sort_values(
            by='revenue',
            ascending=False
        )
    )

    fig3 = px.bar(
        product_perf.head(10),
        x='product_name',
        y='revenue'
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(
        product_perf,
        use_container_width=True
    )

# =====================================================
# TAB 3 — DATA QUALITY
# =====================================================

with tab3:

    st.subheader(
        "Data Quality Monitoring"
    )

    duplicate_orders = (
        filtered_df.duplicated(
            subset=['order_id']
        ).sum()
    )

    missing_values = (
        filtered_df.isnull()
        .sum()
        .sum()
    )

    dq1, dq2 = st.columns(2)

    with dq1:

        st.metric(
            "Duplicate Orders",
            duplicate_orders
        )

    with dq2:

        st.metric(
            "Missing Values",
            missing_values
        )

    st.subheader(
        "Revenue Anomaly Detection"
    )

    avg_revenue = revenue_daily[
        'revenue'
    ].mean()

    threshold = avg_revenue * 0.75

    anomalies = revenue_daily[
        revenue_daily['revenue']
        < threshold
    ]

    st.dataframe(
        anomalies,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Built using Python, DuckDB, SQL models, and Streamlit"
)