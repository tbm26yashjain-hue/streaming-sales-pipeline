import pandas as pd
import os

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

folder = "data/raw"

for file in os.listdir(folder):

    if file.endswith(".csv"):

        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        current_columns = list(df.columns)

        if current_columns != EXPECTED_COLUMNS:

            print(f"Schema mismatch detected: {file}")

        else:

            print(f"Schema valid: {file}")