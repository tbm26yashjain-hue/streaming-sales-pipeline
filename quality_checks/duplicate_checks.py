import pandas as pd

def remove_duplicate_orders(df):
    """
    Removes duplicate order IDs.
    """

    return df.drop_duplicates(
        subset=["order_id"]
    )