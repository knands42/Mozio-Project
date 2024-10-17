# Create an ECR repository
resource "aws_ecr_repository" "django_app_repo" {
  name = var.repository_name
}
