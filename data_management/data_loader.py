"""Utility functions for loading processed data files."""

import os
import pandas as pd


def load_data(filename='merged_sensor_data.csv', country='Germany'):
    """Load a processed CSV file for the specified farm."""

    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'processed', country, filename)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    raise FileNotFoundError(f"Data file {data_path} not found.")
