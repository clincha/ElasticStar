# Forking instructions

If you would like to use this code to make your own dashboard you may find this guide helpful. If anything is confusing feel free to raise an issue and ask me a question.

## Terraform setup

### Creating a Terraform account

To create a Terraform Cloud account, set up a workspace, and retrieve the Terraform Cloud API key for that workspace, follow these steps:

1. **Create a Terraform Cloud account**:
    - Visit the Terraform Cloud sign-up page: [https://app.terraform.io/signup/account](https://app.terraform.io/signup/account)
    - Enter your email address, password, and any other required information.
    - Click "Create account" and follow the instructions to verify your email address.

2. **Log in to Terraform Cloud**:
    - Visit the Terraform Cloud login page: [https://app.terraform.io/session](https://app.terraform.io/session)
    - Enter your email address and password, then click "Log in."

3. **Create an organization**:
    - If you don't have an organization already, click "Create new organization."
    - Enter a name and email address for the organization, then click "Create organization."

4. **Set up a workspace**:
    - Click "Create a new workspace" within your organization's dashboard.
    - Choose "Version control workflow" or "CLI-driven workflow" depending on your preferred workflow.
    - For "Version control workflow," connect your version control provider (e.g., GitHub, GitLab) and select the repository containing your Terraform configuration.
    - For "CLI-driven workflow," provide a name for your workspace and click "Create workspace."
    - Configure any additional settings, such as variables or run triggers, as needed.

5. **Retrieve the Terraform Cloud API key**:
    - Click on your user avatar in the top right corner of the Terraform Cloud UI, then select "User settings."
    - Navigate to the "Tokens" tab.
    - Click "Create an API token."
    - Enter a token description and click "Create API token."
    - Copy the generated API token and store it securely. This token will not be shown again.

### Adding the Terraform API key to GitHub

Now you have a Terraform Cloud account, a workspace, and an API key for that workspace. You can now securely store the API key in GitHub Secrets to use it with GitHub Actions. Follow these steps to add the API key to your GitHub repository's secrets:

1. Navigate to your GitHub repository, and click on the "Settings" tab.
2. On the left sidebar, click "Secrets."
3. Click the "New repository secret" button.
4. Enter the name for the secret as `TERRAFORM_CLOUD_API_KEY`, and paste the API key you retrieved from Terraform Cloud in the "Value" field.
5. Click "Add secret" to save the API key as a secret in your GitHub repository.

Now the Terraform Cloud API key is securely stored in GitHub Secrets and can be used in your GitHub Actions workflows.

### Changing the Terraform variables

Override the values in [terraform.tfvars](/terraform/terraform.tfvars) with the values you prefer.

Due to a [limitation with the Terraform Cloud provider block](https://developer.hashicorp.com/terraform/cli/cloud/settings#the-cloud-block) you'll need to change the values in the [providers.tf](/terraform/providers.tf) Terraform file. Override the values with the vales you have in your Terraform account

```hcl
terraform {
  cloud {
    organization = "clinch-home" # <------- Change to your organisation name

    workspaces {
      name = "elasticstar-elastic-cloud-deployment" # <------- Change to your workspace name
    }
  }
}
```

## GitHub setup

To run the Terraform successfully you will need a  GitHub API token with permissions to create and edit repository secrets. These instructions will take you through using that token to populate a repository secret named `SECRETS_GITHUB_API_KEY` in your forked repository.

1. **Create a GitHub API token**:
   - Go to your GitHub account settings: [https://github.com/settings/profile](https://github.com/settings/profile)
   - Click on "Developer settings" in the left sidebar.
   - Click on "Personal access tokens" in the left sidebar.
   - Click the "Generate new token" button.
   - Enter a descriptive note for the token, such as "API token for managing repository secrets."
   - Under the "Select scopes" section, check the box for `repo` to grant full control of private repositories. This scope includes the `public_repo` scope, which grants access to public repositories.
   - Scroll down and click the "Generate token" button.
   - Copy the generated token and save it in a secure place, as you won't be able to see it again.

2. **Populate the `SECRETS_GITHUB_API_KEY` secret in your forked repository**:
   - Go to the main page of your forked repository on GitHub.
   - Click on the "Settings" tab.
   - In the left sidebar, click "Secrets."
   - Click the "New repository secret" button.
   - Enter the name of the secret as `SECRETS_GITHUB_API_KEY`.
   - Paste the GitHub API token you generated in step 1 into the "Value" field.
   - Click "Add secret" to save the API token as a secret in your forked repository.

Now you have a GitHub API token with the necessary permissions to create and edit repository secrets, and you've used that token to populate the `SECRETS_GITHUB_API_KEY` secret in your forked repository. This secret can be used in the GitHub Actions workflows.

## Elastic Cloud setup

This section guide you through creating an Elastic Cloud account and generating an API token. Then, you'll be instructed to use that token to populate a repository secret named `ELASTIC_API_KEY` in your forked repository.

1. **Create an Elastic Cloud account**:
   - Visit the Elastic Cloud registration page: [https://cloud.elastic.co/register](https://cloud.elastic.co/register)
   - Enter your email address, password, and any other required information.
   - Click "Create account" and follow the instructions to verify your email address.

2. **Generate an Elastic Cloud API token**:
   - Log in to your Elastic Cloud account: [https://cloud.elastic.co/login](https://cloud.elastic.co/login)
   - Click on your user avatar in the top right corner of the Elastic Cloud UI, then select "API Keys."
   - Click the "Generate API Key" button.
   - Enter a name for the API key, such as "GitHub Repository Secret."
   - Choose the desired role for the API key, such as "Editor" to grant read and write access to all deployments.
   - Click "Generate API Key."
   - Copy the generated API key and save it securely, as it will not be shown again.

3. **Populate the `ELASTIC_API_KEY` secret in your forked repository**:
   - Go to the main page of your forked repository on GitHub.
   - Click on the "Settings" tab.
   - In the left sidebar, click "Secrets."
   - Click the "New repository secret" button.
   - Enter the name of the secret as `ELASTIC_API_KEY`.
   - Paste the Elastic Cloud API token you generated in step 2 into the "Value" field.
   - Click "Add secret" to save the API token as a secret in your forked repository.

Now you have an Elastic Cloud account, an API token with the necessary permissions, and the `ELASTIC_API_KEY` secret in your forked repository. This secret can be used in the GitHub Actions workflows.

## Starling setup

This section will walk you through the process of creating a Starling developer account, generating personal access tokens for personal, joint, and business accounts, and then adding these tokens to your GitHub repository secrets.

1. **Create a Starling developer account**:
   - Visit the Starling Developer Portal: [https://developer.starlingbank.com/](https://developer.starlingbank.com/)
   - Click "Join now" or "Sign in" if you already have a Starling account.
   - Enter your email address, password, and any other required information.
   - Complete the registration process and sign in to your Starling developer account.

2. **Create personal access tokens**:
   - Log in to the Developer Portal.
   - Go to the [Personal Access page](https://developer.starlingbank.com/personal).
   - Link your Starling Bank account to your Starling Developer account.
   - Create a token, selecting the scopes you require. Note that you won't be able to make payments from your account with a personal access token.
   - Use the personal access token to make API requests against your own Starling Bank account.

   Keep your personal access token secure, and never give it to a third party or embed it in publicly available code. Anyone who has it can access to your bank account, so treat it as you would your username and password.

   You can only link a Developer Portal account to one Starling Bank account. If you want to link more than one Starling Bank account (for example, a personal account and a business account) you need a separate Developer Portal account for each Starling Bank account you want to link.

3. **Add personal access tokens to GitHub repository secrets**:
   - Go to the main page of your GitHub repository.
   - Click on the "Settings" tab.
   - In the left sidebar, click "Secrets."
   - For each personal access token (Personal, Joint, and Business), follow these steps:
     - Click the "New repository secret" button.
     - Enter the name of the secret in the format `upper(account_name)_ACCESS_TOKEN` (e.g., `PERSONAL_ACCESS_TOKEN`, `JOINT_ACCESS_TOKEN`, `BUSINESS_ACCESS_TOKEN`).
     - Paste the corresponding personal access token into the "Value" field.
     - Click "Add secret" to save the token as a secret in your repository.

Now you have a Starling developer account, personal access tokens for personal, joint, and business accounts, and these tokens securely stored in your GitHub repository secrets with the appropriate naming format. These secrets can be used in GitHub Actions workflows or other automated processes that require access to the Starling API for different account types.

## Final steps!

Now just push the code to your master branch. This should kick off a GitHub Actions workflow which will create a deployment in Elastic Cloud and populate it with your bank data. The URL for the Kibana instance (where you will visualise the data) will be available in the Terraform Cloud portal or in the Elastic Cloud deployment.

If you got this far, please leave a comment somewhere or let me know you managed to get it working. Any feedback would be appreciated.