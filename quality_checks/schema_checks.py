EXPECTED_COLUMNS = [
    "order_id",
    "order_timestamp",
    "customer_id",
    "product_id",
    "product_name",
    "category",
    "qty",
    "unit_price",
    "discount_pct",
    "region"
]

def validate_schema(df):

    incoming_columns = list(df.columns)

    return incoming_columns == EXPECTED_COLUMNS