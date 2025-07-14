"""Calculate Temperature-Humidity Index (THI) from processed data."""

import pandas as pd
import os


def add_thi_column(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``df`` with an additional ``thi`` column."""
    if df.empty:
        return df.copy()

    result = df.copy()
    result["thi"] = (
        (1.8 * result["temperature"] + 32)
        - ((0.55 - 0.0055 * result["humidity"]) * (1.8 * result["temperature"] - 26))
    )
    return result

def calculate_thi():
    """Load Germany and Poland data and append a THI column.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        DataFrames for Germany and Poland, each with an added ``thi`` column.
    """

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    germany_file = os.path.join(
        base_dir, "data", "processed", "Germany", "hourly_merged_sensor_data.csv"
    )
    poland_file = os.path.join(
        base_dir, "data", "processed", "Poland", "hourly_merged_sensor_data.csv"
    )

    germany_data = pd.read_csv(germany_file)
    poland_data = pd.read_csv(poland_file)

    germany_data = add_thi_column(germany_data)
    poland_data = add_thi_column(poland_data)

    return germany_data, poland_data

# You can now test your API by sending a GET request to /api/calculate_thi/. This will return the THI data in JSON format.

