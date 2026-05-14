def validate_missing_values(df):

    critical_columns = [
        "order_id",
        "product_id",
        "qty",
        "unit_price"
    ]

    missing_summary = (
        df[critical_columns]
        .isnull()
        .sum()
    )

    return missing_summary