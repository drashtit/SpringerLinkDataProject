import pandas as pd
import os

# Path to the directory containing your CSV files
download_folder = "/Users/drashtithummar/PycharmProjects/SpringerLink/SplinkCsvData"
# Path for the output merged CSV file
output_file = "/Users/drashtithummar/PycharmProjects/SpringerLink/merged_csv_data.csv"

# List to hold data from each CSV file
dataframes = []

# Iterate through each file in the directory
for filename in os.listdir(download_folder):
    if filename.endswith('.csv'):  # Check if the file is a CSV
        filepath = os.path.join(download_folder, filename)
        # Read the CSV file and append it to the list
        df = pd.read_csv(filepath, index_col=None, header=0)
        dataframes.append(df)

# Concatenate all dataframes in the list into a single dataframe
merged_df = pd.concat(dataframes, axis=0, ignore_index=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv(output_file, index=False)

print("CSV files have been merged and saved to:", output_file)
