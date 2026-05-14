SELECT DISTINCT
    order_id,
    order_timestamp,
    customer_id,
    product_id,
    product_name,
    category,
    qty,
    unit_price,
    discount_pct,
    region,
    qty * unit_price * (1 - discount_pct) AS revenue
FROM raw_sales
WHERE order_id IS NOT NULL;