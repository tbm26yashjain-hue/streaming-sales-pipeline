SELECT
    product_name,
    category,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    AVG(revenue) AS avg_order_value
FROM sales_clean
GROUP BY 1,2
ORDER BY total_revenue DESC;