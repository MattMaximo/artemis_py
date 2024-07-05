# %%

import pandas as pd
import requests
from datetime import datetime
import logging

class ArtemisAPI:
    """
    A class to interact with the Artemis API to fetch asset data and metrics.

    Attributes:
        api_key (str): API key for authentication.
        base_url (str): Base URL for the API.
        headers (dict): Headers for the API requests.
    """

    def __init__(self, api_key):
        """
        Initialize the ArtemisAPI class with an API key.

        Args:
            api_key (str): API key for authentication.
        """
        self.api_key = api_key
        self.base_url = "https://api.artemisxyz.com"
        self.headers = {"Accept": "application/json"}
        logging.basicConfig(level=logging.INFO)

    def _get(self, endpoint, params=None):
        """
        Internal method to perform a GET request.

        Args:
            endpoint (str): The API endpoint.
            params (dict): Parameters for the request.

        Returns:
            dict: JSON response from the API.
        """
        params = params or {}
        params["APIKey"] = self.api_key
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")

    def get_assets(self):
        """
        Fetch a list of assets from the Artemis API.

        Returns:
            pd.DataFrame: DataFrame containing the list of assets.
        """
        data = self._get('/asset')
        if data:
            return pd.DataFrame(data.get("assets", []))

    def get_asset_metrics(self, asset_id):
        """
        Fetch available metric names for a specific asset from the Artemis API.

        Args:
            asset_id (str): The ID of the asset.

        Returns:
            pd.DataFrame: DataFrame containing the available metrics for the asset.
        """
        data = self._get(f'/asset/{asset_id}/metric')
        if data:
            return pd.DataFrame(data)

    def get_data(self, asset_ids, metrics, start_date, end_date=None):
        """
        Fetch data for specific metrics of assets from the Artemis API.

        Args:
            asset_ids (list): List of IDs of the assets.
            start_date (str): The start date for the data in 'yyyy-mm-dd' format.
            metrics (list): List of metrics to fetch data for (e.g., ['mc', 'price']).
            end_date (str, optional): The end date for the data in 'yyyy-mm-dd' format. Defaults to the current date.

        Returns:
            pd.DataFrame: DataFrame containing the data for the specified metrics and assets.
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Ensure asset_ids and metrics are lists
        if isinstance(asset_ids, str):
            asset_ids = [asset_ids]
        if isinstance(metrics, str):
            metrics = [metrics]
        
        all_data = []

        for asset_id in asset_ids:
            asset_data = None
            for metric in metrics:
                params = {
                    "artemisIds": asset_id,
                    "startDate": start_date,
                    "endDate": end_date,
                }
                data = self._get(f'/data/{metric}', params)
                if data:
                    json_data = data["data"]["artemis_ids"].get(asset_id, {}).get(metric, [])
                    df = pd.DataFrame(json_data)
                    if not df.empty:
                        df.rename(columns={"val": metric}, inplace=True)
                        df["date"] = pd.to_datetime(df["date"])
                        if asset_data is None:
                            asset_data = df
                        else:
                            asset_data = pd.merge(asset_data, df, on="date", how="outer")
            
            if asset_data is not None:
                asset_data["artemis_id"] = asset_id
                all_data.append(asset_data)
        
        if all_data:
            result_df = pd.concat(all_data, axis=0)
            result_df = result_df.reset_index(drop=True)
            return result_df
        else:
            return pd.DataFrame()

    def query_weekly_commits_for_ecosystem(self, ecosystem=None, include_forks=None, days_back=None):
        """
        Fetch weekly commits data for ecosystems.

        Args:
            ecosystem (str, optional): Name of the ecosystem. Defaults to None.
            include_forks (bool, optional): Include forks in the data. Defaults to None.
            days_back (int, optional): Days back from today to pull data for. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing the weekly commits data.
        """
        params = {
            "ecosystem": ecosystem,
            "includeForks": include_forks,
            "daysBack": days_back,
        }
        data = self._get('/weekly-commits', params)
        if data:
            return pd.DataFrame(data)

    def query_active_devs_for_ecosystem(self, ecosystem=None, include_forks=None, days_back=None):
        """
        Fetch weekly active developer data for ecosystems.

        Args:
            ecosystem (str, optional): Name of the ecosystem. Defaults to None.
            include_forks (bool, optional): Include forks in the data. Defaults to None.
            days_back (int, optional): Days back from today to pull data for. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing the weekly active developer data.
        """
        params = {
            "ecosystem": ecosystem,
            "includeForks": include_forks,
            "daysBack": days_back,
        }
        data = self._get('/weekly-active-devs', params)
        if data:
            return pd.DataFrame(data)




# Example usage
if __name__ == "__main__":
    api = ArtemisAPI(api_key="api_key_here")
    asset_ids = ["bitcoin", "ethereum"]
    metrics = ["price", "mc"]
    start_date = "2023-06-01"
    end_date = "2023-06-10"

    data = api.get_data(asset_ids, metrics, start_date, end_date)

# %%
