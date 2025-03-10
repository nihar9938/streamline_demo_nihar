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

# File paths
main_file = "path/to/main_file.xlsx"
source_files = [
    "path/to/source_file1.xlsx",
    "path/to/source_file2.xlsx",
    "path/to/source_file3.xlsx"
]

# Read the main file
df_main = pd.read_excel(main_file)

# Loop through each source file and merge
for file in source_files:
    df_source = pd.read_excel(file)
    df_main = df_main.merge(df_source, on='ID', how='left')  # Merge on 'ID'

# Save the final merged file
df_main.to_excel("path/to/updated_file.xlsx", index=False)

print("Merge complete! Saved as 'updated_file.xlsx'")
