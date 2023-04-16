data "ec_stack" "latest" {
  version_regex = "latest"
  region        = var.gcp_reign
}

resource "ec_deployment" "production" {
  name = var.deployment_name

  region                 = data.ec_stack.latest.region
  version                = data.ec_stack.latest.version
  deployment_template_id = "gcp-memory-optimized-v2"

  kibana {
    topology {
      size          = "1g"
      size_resource = "memory"
      zone_count    = 1
    }
  }

  elasticsearch {
    topology {
      id            = "hot_content"
      size          = "1g"
      size_resource = "memory"
      zone_count    = 1
    }
  }
}