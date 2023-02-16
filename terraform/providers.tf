terraform {
  required_providers {
    ec = {
      source  = "elastic/ec"
      version = "0.5.1"
    }
    github = {
      source  = "integrations/github"
      version = "5.17.0"
    }
  }
}


provider "ec" {
  apikey = var.elastic_api_key
}

provider "github" {
  token = var.github_api_key
}