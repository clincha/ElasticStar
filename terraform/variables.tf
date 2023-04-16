variable "github_api_key" {
  type    = string
  default = ""
}

variable "elastic_api_key" {
  type    = string
  default = ""
}

variable "deployment_name" {
  type    = string
  default = "clincha-production"
}

variable "gcp_reign" {
  type    = string
  default = "gcp-europe-west2"
}

variable "terraform_organisation" {
  type    = string
  default = "clinch-home"
}

variable "terraform_workspace" {
  type = string
  default = "elasticstar-elastic-cloud-deployment"
}