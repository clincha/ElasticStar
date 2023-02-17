output "elasticsearch_endpoint" {
  value = ec_deployment.production.elasticsearch[0].https_endpoint
}

output "kibana_endpoint" {
  value = ec_deployment.production.kibana[0].https_endpoint
}