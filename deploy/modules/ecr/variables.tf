# Define the variable for the repository name
variable "repository_name" {
  type        = string
  description = "The name of the ECR repository"
  default     = "django-app"
}
