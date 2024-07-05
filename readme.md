
# ArtemisAPI Python Class

## Overview

The `ArtemisAPI` class provides a convenient interface for interacting with the Artemis API to fetch asset data, metrics, and developer activity information. It allows users to retrieve data in the form of pandas DataFrames and visualize it using Plotly.

## Features

- Fetch a list of supported assets.
- Fetch available metrics for a specific asset.
- Retrieve specific metric data for assets.
- List supported ecosystems.
- Fetch weekly commit data for ecosystems.
- Fetch weekly active developer data for ecosystems.
- Plot data using Plotly.

## Installation

### Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - pandas
  - requests
  - plotly

### Install Required Packages

You can install the required packages using `pip`:

```bash
pip install pandas requests plotly
```

## Usage

### Initialization

To use the `ArtemisAPI` class, you need to instantiate it with your API key:

```python
from artemis_api import ArtemisAPI

api_key = "your_api_key_here"
api = ArtemisAPI(api_key)
```

### Fetching Assets

To fetch a list of supported assets:

```python
assets = api.get_assets()
print(assets)
```

### Fetching Asset Metrics

To fetch available metrics for a specific asset:

```python
asset_id = "bitcoin"
metrics = api.get_asset_metrics(asset_id)
print(metrics)
```

### Fetching Metric Data for Assets

To fetch data for a specific metric of an asset:

```python
asset_id = "bitcoin"
start_date = "2023-01-01"
metric = "price"
data = api.get_data(asset_id, start_date, metric)
print(data)
```

### Listing Supported Ecosystems

To list supported ecosystems:

```python
ecosystems = api.list_ecosystems()
print(ecosystems)
```

### Fetching Weekly Commits for Ecosystems

To fetch weekly commits data for ecosystems:

```python
commits = api.query_weekly_commits_for_ecosystem()
print(commits)
```

To fetch weekly commits data for a specific ecosystem:

```python
ecosystem = "Uniswap"
commits = api.query_weekly_commits_for_ecosystem(ecosystem=ecosystem)
print(commits)
```

### Fetching Weekly Active Developers for Ecosystems

To fetch weekly active developer data for ecosystems:

```python
active_devs = api.query_active_devs_for_ecosystem()
print(active_devs)
```

To fetch weekly active developer data for a specific ecosystem:

```python
ecosystem = "Uniswap"
active_devs = api.query_active_devs_for_ecosystem(ecosystem=ecosystem)
print(active_devs)
```

### Plotting Data

To plot data using Plotly:

```python
data = api.get_data("bitcoin", "2023-01-01", "price")
fig = api.plot_data(data, "Bitcoin Price Data")
fig.show()
```

To plot weekly data with performance annotations:

```python
weekly_data = api.query_weekly_commits_for_ecosystem(ecosystem="Uniswap")
fig = api.plot_weekly_data(weekly_data, "Uniswap Weekly Commits")
fig.show()
```

## Error Handling

The class includes basic error handling for HTTP errors and other exceptions. Errors are logged using the `logging` module.

## Logging

Logging is configured to the INFO level by default. You can change the logging level as needed:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
