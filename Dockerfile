# Use the latest alpine image
FROM alpine:latest
# Install SQLite, Python, and pip
RUN apk --no-cache add sqlite python3 py3-pip
# Install Python libraries (pandas)
RUN pip install pandas
# Create a directory to store the database
WORKDIR /db
# Copy your SQLite database file into the container
COPY data/initial-db.sqlite /db/db.sqlite
# Copy the CSV and the Python script into the container
COPY data/database.csv /db/database.csv
COPY convert_csv.py /db/populate_db.py
# Run the Python script to populate the SQLite database
RUN python3 /db/populate_db.py
# Expose the port if needed
#EXPOSE 1433
# Command to run when the container starts
CMD ["sqlite3", "/db/db.sqlite"]
