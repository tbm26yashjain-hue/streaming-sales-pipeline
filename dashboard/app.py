import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Revenue Intelligence Dashboard",
    layout="wide"
)

# =====================================================
# COLORS
# =====================================================

PRIMARY = "#2563EB"

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: white;
}

.main .block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
    border-right: 1px solid #E5E7EB;
}

.metric-card {
    background-color: #EFF6FF;
    border-left: 5px solid #2563EB;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
}

.metric-heading {
    font-size: 15px;
    color: #374151;
    margin-bottom: 8px;
    font-weight: 600;
}

.metric-main {
    font-size: 26px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
}

.metric-sub {
    font-size: 14px;
    color: #6B7280;
}

hr {
    margin-top: 1rem;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE
# =====================================================

conn = duckdb.connect(
    "warehouse/sales.duckdb"
)

df = conn.execute("""
SELECT * FROM sales_clean
""").fetchdf()

# =====================================================
# DATE PROCESSING
# =====================================================

df['date'] = pd.to_datetime(
    df['order_timestamp']
).dt.date

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Filters")

min_date = df['date'].min()
max_date = df['date'].max()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df['region'].unique()),
    default=sorted(df['region'].unique())
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df['category'].unique()),
    default=sorted(df['category'].unique())
)

apply_filters = st.sidebar.button(
    "Apply Filters"
)

# =====================================================
# SESSION STATE
# =====================================================

if "filtered_df" not in st.session_state:

    st.session_state.filtered_df = df.copy()

# =====================================================
# APPLY FILTERS
# =====================================================

if apply_filters:

    start_date = selected_dates[0]
    end_date = selected_dates[1]

    filtered_df = df[
        (df['region'].isin(selected_regions)) &
        (df['category'].isin(selected_categories)) &
        (df['date'] >= start_date) &
        (df['date'] <= end_date)
    ]

    st.session_state.filtered_df = filtered_df

df = st.session_state.filtered_df

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = df['revenue'].sum()

total_orders = df['order_id'].nunique()

avg_order = total_revenue / total_orders

top_region = (
    df.groupby('region')['revenue']
    .sum()
    .idxmax()
)

top_product = (
    df.groupby('product_name')['revenue']
    .sum()
    .idxmax()
)

# =====================================================
# DAILY REVENUE
# =====================================================

daily_rev = (
    df.groupby('date')['revenue']
    .sum()
    .reset_index()
    .sort_values('date')
)

daily_rev['7d_avg'] = (
    daily_rev['revenue']
    .rolling(7)
    .mean()
)

# =====================================================
# WEEK OVER WEEK
# =====================================================

weekly_revenue = (
    daily_rev['revenue']
    .tail(7)
    .sum()
)

previous_week_revenue = (
    daily_rev['revenue']
    .tail(14)
    .head(7)
    .sum()
)

wow_change = (
    (
        weekly_revenue
        - previous_week_revenue
    )
    / previous_week_revenue
) * 100

# =====================================================
# HIGHEST / LOWEST
# =====================================================

highest_day = daily_rev.loc[
    daily_rev['revenue'].idxmax()
]

lowest_day = daily_rev.loc[
    daily_rev['revenue'].idxmin()
]

highest_pct = (
    highest_day['revenue']
    / total_revenue
) * 100

lowest_pct = (
    lowest_day['revenue']
    / total_revenue
) * 100

# =====================================================
# TOP PRODUCT
# =====================================================

top_product_revenue = (
    df[df['product_name'] == top_product]['revenue']
    .sum()
)

top_product_pct = (
    top_product_revenue
    / total_revenue
) * 100

# =====================================================
# HEADER
# =====================================================

st.title("Revenue Intelligence Dashboard")

st.caption(
    "Trusted executive reporting platform"
)

st.markdown("---")

# =====================================================
# KPI ROWS
# =====================================================

k1, k2 = st.columns(2)

with k1:

    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

with k2:

    st.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

k3, k4 = st.columns(2)

with k3:

    st.metric(
        "📈 Avg Order",
        f"${avg_order:,.2f}"
    )

with k4:

    st.metric(
        "🌍 Top Region",
        top_region
    )

st.metric(
    "📦 Top Product",
    top_product
)

# =====================================================
# WEEK OVER WEEK
# =====================================================

if wow_change > 0:

    st.success(
        f"Revenue increased {wow_change:.1f}% week over week."
    )

else:

    st.warning(
        f"Revenue declined {abs(wow_change):.1f}% week over week."
    )

# =====================================================
# INSIGHT CARDS
# =====================================================

c1 = st.container()

with c1:

    a, b, c = st.columns(3)

    with a:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-heading">
        Highest Revenue Day
        </div>

        <div class="metric-main">
        ${highest_day['revenue']:,.0f}
        </div>

        <div class="metric-sub">
        ({highest_pct:.1f}% contribution)
        </div>

        <br>

        <div class="metric-sub">
        {highest_day['date']}
        </div>

        </div>
        """, unsafe_allow_html=True)

    with b:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-heading">
        Lowest Revenue Day
        </div>

        <div class="metric-main">
        ${lowest_day['revenue']:,.0f}
        </div>

        <div class="metric-sub">
        ({lowest_pct:.1f}% contribution)
        </div>

        <br>

        <div class="metric-sub">
        {lowest_day['date']}
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-heading">
        Top Product Contribution
        </div>

        <div class="metric-main">
        ${top_product_revenue:,.0f}
        </div>

        <div class="metric-sub">
        ({top_product_pct:.1f}% contribution)
        </div>

        <br>

        <div class="metric-sub">
        {top_product}
        </div>

        </div>
        """, unsafe_allow_html=True)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.info(
    f"{top_product} remained the strongest product driver while {top_region} generated the highest regional contribution."
)

st.markdown("---")

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "Executive Overview",
    "Product Intelligence",
    "Data Quality"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("Revenue Trend & Moving Average")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=daily_rev['date'],
            y=daily_rev['revenue'],
            name='Daily Revenue',
            marker_color='#BFDBFE',
            opacity=0.7
        )
    )

    fig.add_trace(
        go.Scatter(
            x=daily_rev['date'],
            y=daily_rev['revenue'],
            mode='lines',
            name='Revenue Trend',
            line=dict(
                color=PRIMARY,
                width=3
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=daily_rev['date'],
            y=daily_rev['7d_avg'],
            mode='lines',
            name='7 Day Moving Avg',
            line=dict(
                color='#DC2626',
                width=3,
                dash='dash'
            )
        )
    )

    fig.update_layout(
        template='simple_white',
        height=420,
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Revenue',
        legend=dict(
            orientation='h',
            y=1.08
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': False
        }
    )

    # =====================================================
    # REGIONAL PERFORMANCE
    # =====================================================

    st.subheader("Regional Revenue Contribution")

    region_df = (
        df.groupby('region')['revenue']
        .sum()
        .reset_index()
        .sort_values(
            by='revenue',
            ascending=True
        )
    )

    regional_bar = px.bar(
        region_df,
        x='revenue',
        y='region',
        orientation='h',
        color='revenue',
        color_continuous_scale='Blues'
    )

    regional_bar.update_layout(
        template='simple_white',
        height=350,
        xaxis_title='Revenue',
        yaxis_title='Region',
        coloraxis_showscale=False
    )

    st.plotly_chart(
        regional_bar,
        use_container_width=True,
        config={
            'displayModeBar': False
        }
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader("Top Products by Revenue")

    product_df = (
        df.groupby('product_name')['revenue']
        .sum()
        .reset_index()
        .sort_values(
            by='revenue',
            ascending=False
        )
        .head(10)
    )

    bar = px.bar(
        product_df,
        x='product_name',
        y='revenue',
        color='revenue',
        color_continuous_scale='Blues'
    )

    bar.update_layout(
        template='simple_white',
        height=420,
        xaxis_title='Product',
        yaxis_title='Revenue',
        coloraxis_showscale=False
    )

    st.plotly_chart(
        bar,
        use_container_width=True,
        config={
            'displayModeBar': False
        }
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader("Data Quality Monitoring")

    duplicate_orders = (
        df.duplicated(
            subset=['order_id']
        ).sum()
    )

    missing_values = (
        df.isnull()
        .sum()
        .sum()
    )

    dq_score = 100

    if duplicate_orders > 0:
        dq_score -= 20

    if missing_values > 0:
        dq_score -= 10

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Duplicate Orders",
        duplicate_orders
    )

    d2.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

    d3.metric(
        "DQ Risk Score",
        f"{dq_score}/100"
    )

    st.markdown("")

    st.subheader(
        "Daily Revenue Volatility"
    )

    daily_rev['previous_day_revenue'] = (
        daily_rev['revenue']
        .shift(1)
    )

    daily_rev['drop_pct'] = (
        (
            daily_rev['previous_day_revenue']
            - daily_rev['revenue']
        )
        / daily_rev['previous_day_revenue']
    ) * 100

    drop_days = daily_rev[
        daily_rev['drop_pct'] > 20
    ].copy()

    final_drop_df = drop_days[
        [
            'date',
            'revenue',
            'previous_day_revenue',
            'drop_pct'
        ]
    ]

    final_drop_df.columns = [
        'Date',
        'Revenue',
        'Previous Day Revenue',
        'Drop %'
    ]

    final_drop_df['Revenue'] = (
        final_drop_df['Revenue']
        .apply(lambda x: f"${x:,.0f}")
    )

    final_drop_df['Previous Day Revenue'] = (
        final_drop_df['Previous Day Revenue']
        .apply(lambda x: f"${x:,.0f}")
    )

    final_drop_df['Drop %'] = (
        final_drop_df['Drop %']
        .round(1)
        .astype(str) + "%"
    )

    st.dataframe(
        final_drop_df.head(5),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Built with Python, DuckDB, Streamlit, and Plotly"
)