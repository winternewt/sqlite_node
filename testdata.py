import pandas as pd
import random
import hashlib
import sqlite3

# Paths
db_file_path = 'data/db.sqlite'

try:
    # Column with 51 unique text entries (random words)
    unique_text_entries = [f"text_entry_{i}" for i in range(1, 52)]

    # Column with less than 10 unique short words (repeated words)
    short_words = ['apple', 'banana', 'cherry', 'date', 'fig', 'grape', 'kiwi']
    repeated_words = [random.choice(short_words) for _ in range(51)]

    # Column with float values
    float_values = [round(random.uniform(0.1, 100.0), 2) for _ in range(51)]

    # Column with less than 20 unique hash entries
    hash_base = ['hash_entry_' + str(i) for i in range(1, 16)]
    hash_entries = [hashlib.md5(entry.encode()).hexdigest() for entry in hash_base]
    limited_hash_entries = [random.choice(hash_entries) for _ in range(51)]

    # Combine all into a DataFrame
    data = {
        'unique_text_column': unique_text_entries,
        'repeated_short_words': repeated_words,
        'float_column': float_values,
        'limited_hash_column': limited_hash_entries
    }

    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Connect to the SQLite database (overwrite existing file)
    conn = sqlite3.connect(db_file_path)

    # Save DataFrame to SQLite database
    df.to_sql('csv_data', conn, if_exists='replace', index=False)
    print("Data successfully saved to SQLite database.")

except Exception as e:
    print(f"Error occurred during CSV creation or SQLite conversion: {e}")

finally:
    # Close the SQLite connection
    conn.close()