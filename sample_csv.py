import pandas as pd

# Paths
csv_file_path = 'data/database.csv'

# Create a sample dataframe to mimic a sample 'database.csv' file
data = {
    'id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'age': [25, 30, 35, 40, 22],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 'david@example.com', 'eva@example.com']
}

# Convert to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_csv(csv_file_path, index=False)
