"""Process sensor data files and resample them to hourly intervals."""

import os
import pandas as pd

def process_hourly_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'processed')
    
    # Iterate through each subfolder in the data directory
    for farm_folder in os.listdir(data_dir):
        farm_path = os.path.join(data_dir, farm_folder)
        
        if os.path.isdir(farm_path):
            # Iterate through each CSV file in the farm folder
            for file_name in os.listdir(farm_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(farm_path, file_name)
                    
                    try:
                        # Read the CSV file
                        df = pd.read_csv(file_path)
                        
                        # Ensure 'datetime' column is in datetime format
                        df['datetime'] = pd.to_datetime(df['datetime'])
                        
                        # Set datetime as index
                        df.set_index('datetime', inplace=True)
                        
                        # Resample to hourly frequency, keeping NaN for missing data
                        hourly_data = df.resample('H').mean()  # This will keep NaN for missing hours
                        
                        # Reset index to have 'datetime' as a column again
                        hourly_data.reset_index(inplace=True)
                        
                        # Create a new file name
                        new_file_name = f'hourly_{file_name}'
                        new_file_path = os.path.join(farm_path, new_file_name)
                        
                        # Save the new hourly averaged data to a new CSV file
                        hourly_data.to_csv(new_file_path, index=False)
                        
                        print(f"Processed and saved: {new_file_path}")
                    
                    except Exception as e:
                        print(f"Error processing {file_name}: {str(e)}")

if __name__ == "__main__":
    process_hourly_data()
