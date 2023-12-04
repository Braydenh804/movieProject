import numpy as np
import pandas as pd

# Specify data types for columns, using 'object' for columns with mixed types
dtype_mapping = {'isAdult': 'object', 'startYear': 'object', 'endYear': 'object'}

# Read the TSV file with specified data types
file1 = pd.read_csv('title.basics.tsv', sep='\t', dtype=dtype_mapping)

# Replace '\\N' with NaN in the specified columns
file1[['isAdult', 'startYear', 'endYear']] = file1[['isAdult', 'startYear', 'endYear']].replace('\\N', np.nan)

# Drop the specified columns
columns_to_drop = ['originalTitle', 'isAdult', 'endYear', 'runtimeMinutes']
file1 = file1.drop(columns=columns_to_drop, errors='ignore')

# Filter rows based on the condition in the 'titleType' column
file1 = file1[file1['titleType'].isin(['movie', 'tvSeries'])]

# Replace '\\N' with NaN in the 'genres' column
file1['genres'] = file1['genres'].replace('\\N', np.nan)

# Filter rows based on whether 'genres' column has a non-null value
file1 = file1.dropna(subset=['genres'])

# Drop rows where 'startYear' has a null (NaN) value
file1 = file1.dropna(subset=['startYear'])

# Read the second TSV file with 3 columns
file2 = pd.read_csv('title.ratings.tsv', sep='\t')

# Merge the two dataframes based on the common identifier column
merged_data = pd.merge(file1, file2[['tconst', 'averageRating', 'numVotes']], left_on='tconst', right_on='tconst', how='left')

# Rename the columns
merged_data.rename(columns={'averageRating': 'averageRating', 'numVotes': 'numVotes'}, inplace=True)

# Replace '\\N' with NaN in the 'numVotes' column
merged_data['numVotes'] = merged_data['numVotes'].replace('\\N', np.nan)

# Convert the values in the 'numVotes' column to integers
merged_data['numVotes'] = merged_data['numVotes'].astype(float).fillna(0).astype(int)

# Fill missing values in the 'averageRating' column with 0
merged_data['averageRating'] = merged_data['averageRating'].fillna(0)

# Sort the DataFrame based on the specified criteria
sorted_data = merged_data.sort_values(by=['averageRating', 'numVotes', 'startYear'], ascending=[False, False, False])

# Save the merged dataframe back to a TSV file
sorted_data.to_csv('output_file.tsv', sep='\t', index=False)