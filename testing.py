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
