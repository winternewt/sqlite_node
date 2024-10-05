# Simple SQLITE+REST Endpoint from CSV

This repository contains a simple FastAPI application that serves a SQLite database converted from a CSV file. The application exposes REST endpoints to interact with the database.

## Contents

- `main.py`: The FastAPI application code.
- `populate_db.py`: A script to populate the SQLite database from a CSV file.
- `ai_tools.py`: A module with helper functions to interact with the API.
- `sample_csv.py`: A module to generate a CSV database example.
- `testdata.py`: A module to generate a synthetic sqlite DB with testdata.
- `data/database.csv`: The CSV file used to populate the database.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Dockerfile to build the application image.
- `docker-compose.yml`: Docker Compose configuration.


## Preparing the docker environment
Install the latest Docker and Docker-Compose from their respective websites.
Optionally, if needed, you may use or refer to the provided script:
```commandline
install_docker_ubuntu.sh
```

## Quickstart
Place your database of choice as `data/database.csv`
Build the Docker image for the application and run the containers:
```bash
docker-compose build
docker-compose up
```

This will start two services:

- **`sqlite-node`**: The FastAPI application serving the SQLite database.
- **`sqlite-browser`**: A web-based SQLite Browser to view and manage the database.

### Notes
- The SQLite database is stored in the `./database` directory on your host machine. This directory is mounted as a volume in both containers, allowing them to share the database file.
- The use of volumes ensures that the database data persists between container restarts.
- The database is populated from the `data/database.csv` file when the `sqlite-node` container is built.


### Access the Application

- **FastAPI application**:
  The application is accessible at `http://localhost:38000`. You can access the API documentation at `http://localhost:38000/docs` SWAGGER.

- **SQLite Browser**:
  The SQLite Browser is accessible at `http://localhost:33000`. You can use it to interact with the SQLite database via a web interface.


## Stopping the Containers
To stop the containers, press `Ctrl+C` in the terminal where `docker-compose up` is running, or run:
```bash
docker-compose down 
```

## Rebuilding the Image
If you make changes to the application code or dependencies, rebuild the image:
```bash
docker-compose build
```

## Troubleshooting

- **Database Issues**:
  - If you encounter issues with the database not being created or populated, check the logs of the `sqlite-node` container:

    ```
    docker logs sqlite-node
    ```

  - Ensure that the `./database` directory has the correct permissions and is accessible.
  - Ensure that the `data/database.csv` file exists and contains the data you wish to import into the SQLite database.
  - Optionally, execute `python3 populate_db.py` locally to validate the conversion process

- **Port Conflicts**:
  - If the ports `38000` or `33000` are already in use, you can change them in the `docker-compose.yml` file under the `ports` section.
  
- **File Permissions**:
  - The `PUID` and `PGID` variables in the `sqlite-browser` service are set to `1000`, which is typically the default user ID and group ID on Unix systems. Adjust these if necessary to match your system.


## License
This project is licensed under the Apache 2.0 License.


