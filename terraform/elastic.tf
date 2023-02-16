data "ec_stack" "latest" {
  version_regex = "latest"
  region        = "gcp-europe-west2"
}

resource "ec_deployment" "development" {
  name = "clincha-development"

  region                 = data.ec_stack.latest.region
  version                = data.ec_stack.latest.version
  deployment_template_id = "gcp-memory-optimized-v2"

  kibana {
    topology {
      size          = "2g"
      size_resource = "memory"
      zone_count    = 1
    }
  }

  elasticsearch {
    topology {
      id            = "hot_content"
      size          = "4g"
      size_resource = "memory"
      zone_count    = 1

      autoscaling {
        max_size          = "120g"
        max_size_resource = "memory"
      }
    }

    topology {
      id            = "ml"
      size          = "0"
      size_resource = "memory"
    }
    topology {
      id            = "master"
      size          = "0"
      size_resource = "memory"
    }
    topology {
      id            = "frozen"
      size          = "0"
      size_resource = "memory"
    }
    topology {
      id            = "cold"
      size          = "0"
      size_resource = "memory"
    }
    topology {
      id            = "warm"
      size          = "0"
      size_resource = "memory"
    }
    topology {
      id            = "coordinating"
      size          = "0"
      size_resource = "memory"
    }
  }
}