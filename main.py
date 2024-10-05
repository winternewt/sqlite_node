import uvicorn
import argparse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import random
import asyncio

app = FastAPI(title="Simple SQLITE+REST endpoint from CSV.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = 'db/db.sqlite'
TABLE_NAME = 'csv_data'
MAX_SIZE = 1024

class ColumnInfo(BaseModel):
    unique_values_count: int
    nullable: bool
    min: Optional[float] = None
    max: Optional[float] = None
    avg: Optional[float] = None
    literals: Optional[List[str]] = None
    examples: Optional[List[str]] = None
    character_set: Optional[str] = None  # Changed to string

class HeadersResponse(BaseModel):
    table_name: str
    columns: Dict[str, ColumnInfo]

class SQLQuery(BaseModel):
    query: str = Field(..., example=f"SELECT * FROM {TABLE_NAME} LIMIT 10")

headers_info = None
headers_info_event = asyncio.Event()

@app.get("/", description="Default message", response_model=str)
async def default():
    return "Simple SQLITE+REST Endpoint v1.0"

@app.get("db/tables", description="Available database tables names", response_model=str)
async def default():
    return TABLE_NAME

@app.get("/db/headers", description="Database headers information", response_model=HeadersResponse)
async def get_headers():
    await headers_info_event.wait()
    if headers_info is None:
        raise HTTPException(status_code=500, detail="Failed to compute headers information")
    return headers_info

def compute_headers_info():
    global headers_info
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Get column names and types
        cursor.execute(f"PRAGMA table_info('{TABLE_NAME}')")
        columns_info = cursor.fetchall()

        result = {}

        for col in columns_info:
            header = col[1]
            col_type = col[2].upper()
            col_info = {}

            # Number of unique values
            cursor.execute(f"SELECT COUNT(DISTINCT [{header}]) FROM {TABLE_NAME}")
            unique_values_count = cursor.fetchone()[0]
            col_info['unique_values_count'] = unique_values_count

            # Check for NULLs
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE [{header}] IS NULL")
            null_count = cursor.fetchone()[0]
            col_info['nullable'] = null_count > 0

            if col_type in ('INTEGER', 'REAL', 'NUMERIC'):
                # Numeric column
                cursor.execute(f"""
                    SELECT MIN([{header}]), MAX([{header}]), AVG([{header}]) 
                    FROM {TABLE_NAME} WHERE [{header}] IS NOT NULL
                """)
                min_val, max_val, avg_val = cursor.fetchone()
                col_info['min'] = min_val
                col_info['max'] = max_val
                col_info['avg'] = avg_val
                col_info['character_set'] = None
            else:
                # Text column
                # Calculate min, max, avg length in bytes
                cursor.execute(f"""
                    SELECT MIN(LENGTH(CAST([{header}] AS BLOB))), 
                           MAX(LENGTH(CAST([{header}] AS BLOB))), 
                           AVG(LENGTH(CAST([{header}] AS BLOB)))
                    FROM {TABLE_NAME} WHERE [{header}] IS NOT NULL
                """)
                min_len, max_len, avg_len = cursor.fetchone()
                col_info['min'] = min_len
                col_info['max'] = max_len
                col_info['avg'] = avg_len

                # Get character_set as a single string
                cursor.execute(f"""
                    SELECT [{header}] FROM {TABLE_NAME} WHERE [{header}] IS NOT NULL
                """)
                all_values = [row[0] for row in cursor.fetchall()]
                concatenated_values = ''.join(all_values)
                unique_characters = ''.join(sorted(set(concatenated_values)))
                col_info['character_set'] = unique_characters

                cursor.execute(f"SELECT COUNT(DISTINCT [{header}]) FROM {TABLE_NAME} WHERE [{header}] IS NOT NULL")
                non_null_unique_values_count = cursor.fetchone()[0]

                if non_null_unique_values_count < 50:
                    cursor.execute(f"SELECT DISTINCT [{header}] FROM {TABLE_NAME} WHERE [{header}] IS NOT NULL")
                    unique_values = [row[0] for row in cursor.fetchall()]
                    values_str = repr(unique_values)
                    if len(values_str.encode('utf-8')) <= MAX_SIZE:
                        # Exact and complete list of values
                        col_info['literals'] = unique_values
                    else:
                        # Still too long, sample 10 random non-null values
                        samples = random.sample(unique_values, min(10, len(unique_values)))
                        col_info['examples'] = samples
                else:
                    # Too many unique values, sample 10 random non-null values
                    samples = random.sample(all_values, min(10, len(all_values)))
                    col_info['examples'] = samples

            # Create ColumnInfo object
            column_info = ColumnInfo(**col_info)
            result[header] = column_info

        conn.close()
        headers_info = HeadersResponse(
            table_name=TABLE_NAME,
            columns=result
        )
    except Exception as e:
        headers_info = None
        # Log the exception
        print(f"Error computing headers_info: {e}")
    finally:
        headers_info_event.set()

@app.post("/db/query", description="Execute SQL query", response_model=List[Dict[str, Any]])
def execute_query(query: SQLQuery):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query.query)
        rows = cursor.fetchall()
        # Get column names
        columns = [description[0] for description in cursor.description]
        conn.close()
        # Combine columns and rows into list of dicts
        result = [dict(zip(columns, row)) for row in rows]
        return result

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Start computation at startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(asyncio.to_thread(compute_headers_info))

# Parse command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI app with Uvicorn")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server")
    args = parser.parse_args()

    # Start the server with Uvicorn
    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)
