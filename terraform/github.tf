resource "github_actions_secret" "secret_elastic_username" {
  repository      = "ElasticStar"
  secret_name     = "ELASTIC_USERNAME"
  plaintext_value = ec_deployment.development.elasticsearch_username
}

resource "github_actions_secret" "secret_elastic_password" {
  repository      = "ElasticStar"
  secret_name     = "ELASTIC_PASSWORD"
  plaintext_value = ec_deployment.development.elasticsearch_password
}

resource "github_actions_secret" "secret_elastic_cloud_id" {
  repository      = "ElasticStar"
  secret_name     = "ELASTIC_CLOUD_ID"
  plaintext_value = ec_deployment.development.elasticsearch[0].cloud_id
}