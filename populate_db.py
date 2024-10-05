import pandas as pd
import sqlite3

# Paths
csv_file_path = 'data/database.csv'
db_file_path = 'data/db.sqlite'

try:
    # Load the CSV file
    df = pd.read_csv(csv_file_path, on_bad_lines='skip')
    print(f"CSV loaded successfully. DataFrame shape: {df.shape}")

    # Remove columns that are entirely NaN
    df.dropna(axis=1, how='all', inplace=True)

    # Alternatively, remove columns where all values are NaN or empty strings
    # df.replace('', pd.NA, inplace=True)
    # df.dropna(axis=1, how='all', inplace=True)

    print(f"DataFrame shape after dropping empty columns: {df.shape}")

    # Connect to the SQLite database (overwrite existing file)
    conn = sqlite3.connect(db_file_path)

    # Save DataFrame to SQLite database
    df.to_sql('csv_data', conn, if_exists='replace', index=False)
    print("Data successfully saved to SQLite database.")

except Exception as e:
    print(f"Error occurred during CSV loading or SQLite conversion: {e}")

finally:
    # Close the SQLite connection
    conn.close()