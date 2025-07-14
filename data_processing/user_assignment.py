import os
import json

# Path to the unprocessed data
unprocessed_path = 'data/raw/Germany'

# Define the parameters
parameters = ['ch4', 'co2', 'nh3', 'humidity', 'temperature', 'wind_ns', 'wind_ew']

# Create a dictionary to store file-parameter mapping
file_parameter_mapping = {}

# Iterate over each file in the directory
for filename in os.listdir(unprocessed_path):
    if filename.endswith('.csv'):
        print(f"Assign a parameter to the file: {filename}")
        for i, param in enumerate(parameters, 1):
            print(f"{i}. {param}")
        
        choice = int(input("Enter the number corresponding to the parameter: "))
        if 1 <= choice <= len(parameters):
            file_parameter_mapping[filename] = parameters[choice - 1]
        else:
            print("Invalid choice. Skipping this file.")

# Save the mapping to a JSON file
with open('file_parameter_mapping.json', 'w') as f:
    json.dump(file_parameter_mapping, f, indent=4)

print("File-parameter mapping saved to file_parameter_mapping.json")
