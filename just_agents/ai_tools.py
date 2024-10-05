import requests
from typing import List, Dict, Any, Optional

URL_BASE = "http://127.0.0.1:8000"

def get_headers() -> Dict[str, Any]:
    """
    Retrieves the headers information from the API.

    Returns:
        dict: A dictionary containing the table name and columns information.

    The returned dictionary has the following structure:
    ```python
    {
        "table_name": str,  # Name of the table in the database (e.g., "csv_data").
        "columns": {
            "column_name": {
                "unique_values_count": int,  # Number of unique values in the column.
                "nullable": bool,            # Indicates if the column contains NULL values.
                "min": Optional[float],      # Minimum value or length in bytes (for text columns).
                "max": Optional[float],      # Maximum value or length in bytes (for text columns).
                "avg": Optional[float],      # Average value or length in bytes (for text columns).
                "literals": Optional[List[str]],  # List of all unique values if they are few.
                "examples": Optional[List[str]],  # Sample values from the column.
                "character_set": Optional[str]    # String of unique characters in text columns.
            },
            ...
        }
    }
    ```

    Notes:
    - **Numeric Columns**:
      - `min`, `max`, and `avg` represent the minimum, maximum, and average numerical values.
    - **Text Columns**:
      - `min`, `max`, and `avg` represent the lengths in bytes of the entries.
      - `character_set` contains all unique characters found in the column, concatenated into a single string.
    - **Literals vs. Examples**:
      - If the number of unique values is small and the total size is manageable (<= 500 bytes), `literals` contains all unique values.
      - If there are too many unique values, or the total size exceeds 500 bytes, `examples` contains a random sample of up to 10 values.
    - **Nullable**:
      - Indicates whether the column contains NULL values (`True`) or not (`False`).
    - The function waits for the API to complete computation if it's not yet available.

    Raises:
        Exception: If the API request fails or returns an error.

    Example:
        ```python
        headers = get_headers()
        print(headers["table_name"])
        for column_name, info in headers["columns"].items():
            print(f"Column: {column_name}, Unique Values: {info['unique_values_count']}")
        ```
    """
    url = URL_BASE + "/db/headers"
    print("TOOL HEADERS was used")
    try:
        response = requests.get(url)
        response.raise_for_status()
        headers_info = response.json()
        return headers_info
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve headers information: {e}")

def execute_query(query: str) -> List[Dict[str, Any]]:
    """
    Executes a SQL query against the database via the API.

    Args:
        query (str): The SQL query string to be executed.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the query results.
            Each dictionary corresponds to a row, with keys being column names.

    Raises:
        Exception: If the query execution fails or the API returns an error.

    Notes:
    - The query must be a valid SQL statement compatible with SQLite.
    - The API endpoint expects a JSON payload with the 'query' field containing the SQL query.
    - The function returns the result of the query as a list of dictionaries for ease of use.
    - If the query returns no data, an empty list is returned.
    - The function handles HTTP errors and raises an exception with relevant details.

    Example:
        ```python
        query = "SELECT * FROM csv_data WHERE age > 30 LIMIT 5"
        results = execute_query(query)
        for row in results:
            print(row)
        ```
    """
    url = URL_BASE + "/db/query"
    print(f"TOOL QUERY was used with {query}")
    payload = {"query": query}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to execute query: {e}")
