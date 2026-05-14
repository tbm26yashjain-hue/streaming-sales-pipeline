SELECT
    product_id,
    product_name,
    category,
    CURRENT_DATE AS effective_start_date,
    NULL AS effective_end_date,
    TRUE AS is_current

FROM sales_clean

GROUP BY
    product_id,
    product_name,
    category;