import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

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

    def get_assets(self):
        """
        Fetch a list of assets from the Artemis API.

        Returns:
            pd.DataFrame: DataFrame containing the list of assets.
        """
        url = f"{self.base_url}/asset"
        params = {"APIKey": self.api_key}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()["assets"])

    def get_asset_metrics(self, asset_id):
        """
        Fetch available metric names for a specific asset from the Artemis API.

        Args:
            asset_id (str): The ID of the asset.

        Returns:
            pd.DataFrame: DataFrame containing the available metrics for the asset.
        """
        url = f"{self.base_url}/asset/{asset_id}/metric"
        params = {"APIKey": self.api_key}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json())

    def get_data(self, asset_id, start_date, metric, end_date=None):
        """
        Fetch data for a specific metric of an asset from the Artemis API.

        Args:
            asset_id (str): The ID of the asset.
            start_date (str): The start date for the data in 'yyyy-mm-dd' format.
            metric (str): The metric to fetch data for (e.g., 'mc' for market cap).
            end_date (str, optional): The end date for the data in 'yyyy-mm-dd' format. Defaults to the current date.

        Returns:
            pd.DataFrame: DataFrame containing the data for the specified metric and asset.
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        url = f"{self.base_url}/data/{metric}"
        params = {
            "artemisIds": asset_id,
            "startDate": start_date,
            "endDate": end_date,
            "APIKey": self.api_key,
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        json_data = response.json()["data"]["artemis_ids"][asset_id][metric]
        data = pd.DataFrame(json_data)
        data.rename(columns={"val": metric}, inplace=True)
        return data

    def plot_data(self, data, title):
        y_columns = [col for col in data.columns if col != "date"]
        fig = px.line(data, x="date", y=y_columns, title=title)
        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.5
            )
        )
        return fig

    def plot_weekly_data(self, data, title):
        y_columns = [col for col in data.columns if col != "date"]

        # Calculate 7D Performance
        first_value = data[y_columns[0]].iloc[0]
        last_value = data[y_columns[0]].iloc[-1]
        performance = ((last_value - first_value) / first_value) * 100

        # Determine performance box color
        performance_color = (
            "rgba(0, 255, 0, 0.2)" if performance >= 0 else "rgba(255, 0, 0, 0.2)"
        )
        # Create the line plot
        fig = px.bar(data, x="date", y=y_columns, title=title)

        # Update layout
        fig.update_layout(
            title={
                "text": title,
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": dict(family="Arial", size=20, color="black"),
            },
            plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickformat="%d-%b"),
            yaxis=dict(showgrid=False, tickprefix=""),
            showlegend=False,
        )

        # Add annotations with dashed boxes
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.01,
            y=1.1,
            text=f"7D Performance:\n{performance:.2f}%",
            showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
            bgcolor=performance_color,
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
        )

        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.99,
            y=1.1,
            text=f"Current Value:\n{last_value:.2f}",
            showarrow=False,
            font=dict(family="Arial", size=12, color="black"),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
        )

        return fig