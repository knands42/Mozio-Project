ENV = env
PYTHON = $(ENV)/bin/python
PIP = $(ENV)/bin/pip
DJANGO_MANAGE = $(PYTHON) manage.py

# Make postgres available
docker-up:
	docker compose up --build --force-recreate

# Apply database migrations
migrate:
	$(DJANGO_MANAGE) migrate

# Run the Django development server
run:
	$(DJANGO_MANAGE) runserver

# Run unit tests
test:
	$(DJANGO_MANAGE) test

# Clean up the environment
clean:
	rm -rf $(ENV)

# Build for production
build-local:
	docker build -t geobound .
	docker run -e DB_HOST=host.docker.internal -p 8000:8000 geobound

push-prod:
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.<region>.amazonaws.com
	docker tag django-app:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/django-app-repo:latest
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/my-django-app-repo:latest

# Set up the application (install, migrate, seed)
setup: docker-up migrate

# Run server and watch the logs
run_with_logs:
	$(DJANGO_MANAGE) runserver | tee server.log
