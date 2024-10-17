# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1         # Ensures Python outputs everything to the console
ENV DJANGO_ENV=production     

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \ 
    binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 to allow connections
EXPOSE 8000

# Run the application with Gunicorn as the WSGI server
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:8000 mozio_project_django.wsgi:application --workers 4

