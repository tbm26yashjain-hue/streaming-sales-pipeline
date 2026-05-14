import os

WAREHOUSE_PATH = "warehouse/sales.duckdb"

if os.path.exists(WAREHOUSE_PATH):

    os.remove(WAREHOUSE_PATH)

    print(
        "Warehouse reset successfully."
    )

else:

    print(
        "Warehouse file not found."
    )
    