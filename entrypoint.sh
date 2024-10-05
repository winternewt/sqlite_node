#!/bin/sh
set -e

# If the database does not exist, populate it
if [ ! -f /app/db/db.sqlite ]; then
    echo "Database not found. Populating the database..."
    python3 /app/populate_db.py
    cp /app/data/db.sqlite /app/db/db.sqlite
else
    echo "Database already exists. Skipping population."
fi
chmod 666 /app/db/db.sqlite
# Start the application
exec python3 /app/main.py "$@"
