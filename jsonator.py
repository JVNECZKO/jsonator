import zipfile
import json
import os
import pandas as pd

# Define the path to the ZIP file
zip_file_path = '' # zip file
extracted_dir_path = '' # where to extract
output_csv_path = '.csv' # output csv file

# Create a directory to extract the files
os.makedirs(extracted_dir_path, exist_ok=True)

# Step 1: Extract the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir_path)

# Step 2: Identify all JSON files in the extracted content
json_files = [os.path.join(root, file)
              for root, _, files in os.walk(extracted_dir_path)
              for file in files if file.endswith('.json')]

# Step 3 and 4: Parse JSON files and extract 'entityWrapper' from 'data' key
data = []
for json_file in json_files:
    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            content = json.load(file)
            if 'data' in content and 'entityWrapper' in content['data']:
                entity_wrapper_data = content['data']['entityWrapper']
                flattened_data = pd.json_normalize(entity_wrapper_data)
                data.append(flattened_data)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {json_file}")

# Step 5: Combine extracted data into a single CSV file
if data:
    combined_df = pd.concat(data, ignore_index=True)
    
    # Reorder columns and improve readability
    columns_order = sorted(combined_df.columns)
    combined_df = combined_df[columns_order]
    
    combined_df.to_csv(output_csv_path, index=False)
    print(f"Data combined and saved to {output_csv_path}")
else:
    print("No JSON files containing 'entityWrapper' found in 'data' key.")
