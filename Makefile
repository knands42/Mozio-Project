ENV = env
PYTHON = $(ENV)/bin/python
PIP = $(ENV)/bin/pip
DJANGO_MANAGE = $(PYTHON) manage.py

# Create virtual environment and install dependencies
install:
	sudo apt-get install binutils libproj-dev gdal-bin libgdal-dev
	python3 -m venv $(ENV)
	$(PIP) install -r requirements.txt

# Make postgres available
docker-up:
	docker compose up --build --force-recreate

# Apply database migrations
migrate:
	$(DJANGO_MANAGE) makemigrations
	$(DJANGO_MANAGE) migrate

# Load initial data (seed)
seed:
	$(DJANGO_MANAGE) loaddata tickets.json

# Run the Django development server
run:
	$(DJANGO_MANAGE) runserver

# Run unit tests
test:
	$(DJANGO_MANAGE) test

# Clean up the environment
clean:
	rm -rf $(ENV)

# Set up the application (install, migrate, seed)
setup: install docker-up migrate seed

# Run server and watch the logs
run_with_logs:
	$(DJANGO_MANAGE) runserver | tee server.log
