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



import os
import pandas as pd

# Set folder path
folder_path = "path/to/excel/folder"

# Columns you want to keep
columns_to_keep = ["Column1", "Column2", "Column3"]  # Replace with your actual column names

# Get all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith((".xls", ".xlsx"))]

# List to collect DataFrames
df_list = []

# Loop and read selected columns
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path, usecols=columns_to_keep)
    df_list.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(df_list, ignore_index=True)

# Remove duplicates
merged_df = merged_df.drop_duplicates()

# Save to new Excel file
output_file = os.path.join(folder_path, "merged_cleaned_output.xlsx")
merged_df.to_excel(output_file, index=False)

print("Merge complete! Duplicates removed. File saved as 'merged_cleaned_output.xlsx'")



import os
import pandas as pd

# Set folder path
folder_path = "path/to/excel/folder"

# Columns you want to keep
columns_to_keep = ["ID", "Name", "Department"]  # Replace with your actual column names

# Column to use for deduplication
dedup_column = "ID"

# Get all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith((".xls", ".xlsx"))]

# List to collect DataFrames
df_list = []

# Loop and read selected columns
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path, usecols=columns_to_keep)
    df_list.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(df_list, ignore_index=True)

# Remove duplicates based on one column (keep first occurrence)
merged_df = merged_df.drop_duplicates(subset=[dedup_column])

# Save to new Excel file
output_file = os.path.join(folder_path, "merged_unique_by_id.xlsx")
merged_df.to_excel(output_file, index=False)

print("Merge complete! Duplicates removed based on 'ID'. File saved as 'merged_unique_by_id.xlsx'")



import os
import pandas as pd

# Set the folder path where your Excel files are stored
folder_path = "path/to/your/folder"

# Column to remove duplicates on
dedup_column = "ID"

# List all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xls', '.xlsx'))]

# List to collect data from each file
df_list = []

# Loop through files and read them
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    df_list.append(df)

# Merge all files into one DataFrame
merged_df = pd.concat(df_list, ignore_index=True)

# Remove duplicates based on the 'ID' column
merged_df = merged_df.drop_duplicates(subset='ID')

# Save the merged, de-duplicated DataFrame to a new Excel file
output_file = os.path.join(folder_path, "merged_unique_by_id.xlsx")
merged_df.to_excel(output_file, index=False)

print(f"Merged Excel saved as: {output_file}")




import os
import pandas as pd

# Set folder path
folder_path = "path/to/excel/folder"

# Get all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith((".xls", ".xlsx"))]

# Create an empty list to store DataFrames
df_list = []

# Loop through the files and read them
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    df_list.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(df_list, ignore_index=True)

# Save to a new Excel file
merged_df.to_excel(os.path.join(folder_path, "merged_output.xlsx"), index=False)

print("Merging complete! Saved as 'merged_output.xlsx'")


import pandas as pd

# File paths
file1 = "path/to/main_file.xlsx"  # The file to be updated
file2 = "path/to/source_file.xlsx"  # The file with additional data

# Read both files
df_main = pd.read_excel(file1)  # Main file
df_source = pd.read_excel(file2)  # File containing additional data

# Merge based on common column (e.g., 'ID')
merged_df = df_main.merge(df_source[['ID', 'New_Column']], on='ID', how='left')

# Save the updated DataFrame
merged_df.to_excel("path/to/updated_file.xlsx", index=False)

print("Merge complete! Saved as 'updated_file.xlsx'")


import pandas as pd

# Load the Excel file
file_path = "path/to/your_file.xlsx"
df = pd.read_excel(file_path)

# Specify the two columns
col1 = "ColumnA"  # Replace with actual column name
col2 = "ColumnB"  # Replace with actual column name

# Filter rows where either ColumnA or ColumnB is NOT null
filtered_df = df[df[col1].notna() | df[col2].notna()]

# Save to new Excel file
filtered_df.to_excel("filtered_either_notnull.xlsx", index=False)

print("Filtered file saved as 'filtered_either_notnull.xlsx'")
