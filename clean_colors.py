import os
import shutil
import pandas as pd

# Load CSV file
colors_df = pd.read_csv('colours.csv')
valid_names = set(colors_df.iloc[:, 0].astype(str))

# Create the target directory if it doesn't exist
target_dir = 'outputs_cleaned'
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Directory containing the files to process
source_dir = 'outputs'

# Process each file in the directory
for filename in os.listdir(source_dir):
    if filename.endswith(".png"):  # Filter files with .png extension
        base_name = filename.split('.')[0]  # Remove the extension
        base_name=base_name.replace("sc_","")
        new_name = base_name.split('_', 1)[-1]  # Remove the part before '_'
        new_name = new_name.strip("_")
        if new_name in valid_names:  # Check if the new name is in the CSV
            # Construct full file paths
            new_name=new_name+".png"
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, new_name)
            # Move the file
            if not os.path.isfile(target_path):
              shutil.copy(source_path, target_path)
              print(f"Copied: {filename} to {target_dir}")
