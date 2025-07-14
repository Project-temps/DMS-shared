"""Merge individual sensor CSV files into a single dataset."""

import pandas as pd
import os
import json

def merge_sensor_data():
    # Define base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'raw/Germany')
    output_dir = os.path.join(base_dir, 'data', 'processed', 'germany')

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the file-parameter mapping
    with open(os.path.join(base_dir, 'file_parameter_mapping.json'), 'r') as f:
        file_parameter_mapping = json.load(f)

    # Initialize an empty dictionary to store dataframes
    dfs = {}

    # Read all files based on the mapping
    for filename, parameter in file_parameter_mapping.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Rename columns to standard format
            df.columns = ['datetime', parameter]
            # Convert datetime string to pandas datetime
            df['datetime'] = pd.to_datetime(df['datetime'])
            dfs[parameter] = df
        else:
            print(f"Warning: File not found - {filename}")

    # Merge all dataframes on datetime
    merged_df = None
    for key, df in dfs.items():
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='datetime', how='outer')

    # Sort by datetime
    if merged_df is not None:
        merged_df = merged_df.sort_values('datetime')
        
        # Handle missing values using ffill and bfill directly
        merged_df = merged_df.ffill().bfill()

        # Save to processed data directory
        output_path = os.path.join(output_dir, 'merged_sensor_data.csv')
        merged_df.to_csv(output_path, index=False)
        print(f"Merged data saved to: {output_path}")
        
        return merged_df
    else:
        print("Error: No data to merge")
        return None

if __name__ == "__main__":
    merge_sensor_data() 
