# Use Python 3.11 Alpine image
FROM python:3.11-alpine

# Install SQLite
RUN apk --no-cache add sqlite

# Create a directory to store the database
RUN mkdir -p /app/data

# Set working directory to /app
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY *.py .

# Copy the CSV into the container
COPY data/database.csv /app/data/database.csv

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port for Uvicorn
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]