import pandas as pd
import sqlite3

# Load the CSV file
csv_file_path = 'data/database.csv'

try:
    # Attempt to load the CSV file with safe load using error_bad_lines=False to skip problematic lines
    df = pd.read_csv(csv_file_path, on_bad_lines='skip')
    print(f"CSV loaded successfully. DataFrame shape: {df.shape}")

    # Connect to the SQLite database (overwrite existing file)
    conn = sqlite3.connect('data/initial-db.sqlite')

    # Save DataFrame to SQLite database
    df.to_sql('csv_data', conn, if_exists='replace', index=False)
    print("Data successfully saved to SQLite database.")

except Exception as e:
    print(f"Error occurred during CSV loading or SQLite conversion: {e}")

finally:
    # Close the SQLite connection
    conn.close()
