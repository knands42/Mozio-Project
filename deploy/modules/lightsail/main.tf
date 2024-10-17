provider "aws" {
  region = "us-east-1"  # Adjust to your preferred AWS region
}

# Create Lightsail PostgreSQL Database
resource "aws_lightsail_database" "postgres" {
  availability_zone = "us-east-1a"
  blueprint_id      = "postgresql_13_3"
  bundle_id         = "medium_1_0"  # Use a small bundle for development (adjust based on needs)
  database_name     = "mydb"
  master_database_name = "mydb"
  master_username      = "myuser"
  password             = "supersecretpassword"  # Replace with a secure password

  tags = {
    Name = "DjangoAppDatabase"
  }
}

output "db_endpoint" {
  value = aws_lightsail_database.postgres.endpoint
}

output "db_username" {
  value = aws_lightsail_database.postgres.master_username
}

output "db_password" {
  value = aws_lightsail_database.postgres.master_password
  sensitive = true
}


# Lightsail Container Service for Django App
resource "aws_lightsail_container_service" "django_service" {
  service_name = "django-app-service"
  power        = "nano" 
  scale        = 1      

  tags = {
    Name = "DjangoAppService"
  }
}

# Deployment configuration for Lightsail Container Service
resource "aws_lightsail_container_service_deployment_version" "django_deployment" {
  container_service_name = aws_lightsail_container_service.django_service.service_name

  public_endpoint {
    container_name = "django-app"
    port           = 8000 
  }

  container {
    image          = var.repository_url
    container_name = "django-app"
    environment    = {
      DB_NAME     = aws_lightsail_database.postgres.master_database_name
      DB_USER     = aws_lightsail_database.postgres.master_username
      DB_PASSWORD = aws_lightsail_database.postgres.master_password
      DB_HOST     = aws_lightsail_database.postgres.endpoint
      DB_PORT     = "5432"
    }
  }
}
