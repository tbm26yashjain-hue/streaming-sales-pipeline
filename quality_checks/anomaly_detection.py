import duckdb

conn = duckdb.connect("warehouse/sales.duckdb")

query = """

SELECT
    DATE(order_timestamp) AS order_date,
    SUM(revenue) AS revenue

FROM sales_clean

GROUP BY 1
ORDER BY 1

"""

df = conn.execute(query).fetchdf()

average_revenue = df['revenue'].mean()

threshold = average_revenue * 0.75

anomalies = df[
    df['revenue'] < threshold
]

print(anomalies)