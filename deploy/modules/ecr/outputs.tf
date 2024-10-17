# Output the repository URL to use when pushing the Docker image
output "repository_url" {
  value = aws_ecr_repository.django_app_repo.repository_url
}
