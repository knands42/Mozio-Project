# Mozio Project

This is a Django application for Mozio with geolocation capabilities, using PostgreSQL and PostGIS.

## Requirements

Ensure before execute the project to have the following dependencies installed:

- Python 3.8+
- Make
- Python-pip
- Python venv
- Docker (PostgreSQL with PostGIS extension)

> **Note**: For debian users you can install the dependencies by running the following command:
>
> ```bash
> sudo apt-get install python3 python3-pip python3-venv make binutils libproj-dev gdal-bin libgdal-dev docker.io docker-compose-v2 -y
> ```

### Dependencies

```bash
make docker-up
```

# Project Setup

1. Clone the repository

```bash
git clone https://github.com/your-repo/Mozio-Project.git
cd Mozio-Project
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

2. Set up the application
You can set up the app by running the following Makefile commands:

```bash
# Create a virtual environment, install dependencies, and set up the database
make setup
```

> This will:
>
> Create a virtual environment in the env directory.
> Install all necessary Python dependencies from requirements.txt.
> Apply database migrations.

3. Run the development server

Start the Django development server:

```bash
make run
Visit the app at http://127.0.0.1:8000.
```

4. Run Tests
To run the tests, use the following command:

```bash
make test
```

5. Clean Up
To clean up the project (remove the virtual environment), run:

```bash
make clean
```

## Additional Commands

`make migrate`: Apply database migrations </br>
`make seed`: Load initial data (seed the database). </br>
`make run_with_logs`: Run the server and output logs to server.log.
