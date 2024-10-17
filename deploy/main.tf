module "my-ecr" {
  source                  = "./modules/ecr"
  repository_name         = "django-app"
}

module "my-lightsail" {
  source                  = "./modules/lightsail"
  repository_uri          = module.my-ecr.repository_uri
}