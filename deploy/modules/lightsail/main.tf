resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "13.3"
  instance_class       = "db.t3.micro"
  name                 = "mozio_db"
  username             = "postgres"
  password             = "postgres"
  parameter_group_name = "default.postgres13"
  skip_final_snapshot  = true
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
  container_service_name = aws_lightsail_container_service.django_service.name

  public_endpoint {
    container_name = "django-app"
    port           = 8000 
  }

  container {
    image          = var.repository_url
    container_name = "django-app"
    environment    = {
      DB_NAME     = "mozio_db"
      DB_USER     =  "postgres"
      DB_PASSWORD =  "postgres"
      DB_HOST     =  aws_db_instance.postgres.endpoint
      DB_PORT     = "5432"
    }
  }
}
