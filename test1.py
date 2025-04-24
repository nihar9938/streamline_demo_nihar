import os
import pandas as pd

# Set folder path
folder_path = "path/to/excel/folder"

# Get all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith((".xls", ".xlsx"))]

# Create an empty list to store DataFrames
df_list = []

# Define the columns you need
columns_to_keep = ["Column1", "Column2"]  # Replace with actual column names

# Loop through the files and read only the required columns
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path, usecols=columns_to_keep)
    df_list.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(df_list, ignore_index=True)

# Save to a new Excel file
merged_df.to_excel(os.path.join(folder_path, "merged_output.xlsx"), index=False)

print("Merging complete! Saved as 'merged_output.xlsx'")
