# Process Outline

 This document provides an overview of the process to create a Elastic Cloud deployment with Elasticsearch and Kibana instances in the Google Cloud Platform (GCP), using Terraform. Additionally, we describe the `starling_to_elastic.py` script, which retrieves transaction data for different account types using the Starling API and indexes the transaction data into Elasticsearch.

![ElasticStar.svg](/images/ElasticStar.svg)

## Terraform

The Terraform code sets up an Elastic Cloud deployment with Elasticsearch and Kibana instances using a memory-optimized deployment template in the Google Cloud Platform (GCP) region `europe-west2`.

1. It retrieves the latest Elastic Cloud stack version using the `ec_stack` data source, filtered by the `latest` version_regex and the specified region.
2. It creates an Elastic Cloud deployment resource named `clincha-production`.
   - The deployment uses the region and version obtained from the `ec_stack` data source.
   - It uses the `gcp-memory-optimized-v2` deployment template for the Elastic Cloud deployment.
3. It configures a Kibana instance within the deployment with the following settings:
   - The size is set to 1 GB of memory.
   - The number of zones (availability zones) for the Kibana instance is set to 1.
4. It configures an Elasticsearch instance within the deployment with the following settings:
   - The instance is assigned the ID `hot_content`.
   - The size is set to 1 GB of memory.
   - The number of zones (availability zones) for the Elasticsearch instance is set to 1.
   - Autoscaling is enabled with a maximum size of 120 GB of memory.

In summary, this Terraform code creates a memory-optimized Elastic Cloud deployment with Kibana and Elasticsearch instances in the GCP `europe-west2` region, with autoscaling enabled for the Elasticsearch instance.

## Script

The [starling_to_elastic.py](/starling_to_elastic.py) is where the majority of the application code lives. Other content describes the project, runs the script in GitHub Actions and ensures the environment is set up correctly. The script performs the following actions:

1. Loads environment variables (access tokens and Elastic search credentials) using the `dotenv` library.
2. Defines a list of account types: PERSONAL, BUSINESS, and JOINT.
3. Iterates through the account types and checks if the corresponding access token is available in the environment variables. If not, it skips to the next account type.
4. For each available account type, it prints the account type and initializes the Starling object with the appropriate access token.
5. Retrieves the main account ID and transaction feed for the current account type using the Starling API.
6. Initializes an Elasticsearch client with the provided cloud ID, username, and password from environment variables.
7. Constructs the Elasticsearch index name based on the account type.
8. Tries to create the Elasticsearch index. If the index already exists, it proceeds without raising an error.
9. Prints a message indicating that transactions are being added to Elastic.
10. Initializes a progress bar using the `tqdm` library to show the progress of adding transactions.
11. Uses the `streaming_bulk` function from the `elasticsearch.helpers` library to index the transaction data into Elasticsearch.
12. Updates the progress bar as transactions are indexed.
13. Closes the progress bar after all transactions have been indexed.

In summary, the script retrieves transaction data for various account types using the Starling API and indexes the transaction data into Elasticsearch.

![script-output.png](/images/script-output.png)