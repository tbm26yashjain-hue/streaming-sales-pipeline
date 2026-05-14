SELECT
    DATE(order_timestamp) AS order_date,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_clean
GROUP BY 1
ORDER BY 1;
