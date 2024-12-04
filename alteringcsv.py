import pandas as pd

# Read the CSV file
df = pd.read_csv(r"C:\Users\nobit\Downloads\query_result_2024-12-03T11_19_37.971692Z.csv")


#get column names
column_names = df.columns.tolist()
# Print column names
print("Column names:", column_names)


'''
# Rename columns
# Example: Rename 'old_name' to 'new_name'
df.rename(columns={'old_name': 'new_name'}, inplace=True)

# Drop columns
# Example: Drop columns 'unwanted_column1', 'unwanted_column2'
df.drop(columns=['unwanted_column1', 'unwanted_column2'], inplace=True)

# Save the modified DataFrame to a new CSV file
output_file = input("Enter the new CSV file name (with .csv extension): ")
df.to_csv(output_file, index=False)
'''