output "elasticsearch_endpoint" {
  value = ec_deployment.development.elasticsearch[0].https_endpoint
}

output "kibana_endpoint" {
  value = ec_deployment.development.kibana[0].https_endpoint
}