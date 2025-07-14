import pandas as pd
import os

# Define the expected columns
expected_columns = ['datetime', 'value']  # Adjust these as per your actual data structure

# Path to the unprocessed data
unprocessed_path = 'data/germany_farm_unprocessed_data_files'

# Iterate over each file in the directory
for filename in os.listdir(unprocessed_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(unprocessed_path, filename)
        df = pd.read_csv(file_path)
        
        # Check if the columns match the expected structure
        if list(df.columns) != expected_columns:
            print(f"File {filename} does not match the expected structure.")
            # Here you can add code to standardize the file structure
            # For example, renaming columns or adding missing columns
            df.columns = expected_columns  # This is a simple example
            df.to_csv(file_path, index=False)
            print(f"File {filename} has been standardized.")
        else:
            print(f"File {filename} matches the expected structure.")
