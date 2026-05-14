import requests
import pandas as pd

def fetch_sales_data_from_api(api_url):

    """
    Example API connector for future integrations.
    Currently unused in pipeline.
    """

    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(
            "API request failed"
        )

    data = response.json()

    return pd.DataFrame(data)