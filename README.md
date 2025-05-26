
# InventoryCentral
This is a personal learning project developed to explore AWS CDK, GitHub Actions CI/CD, and AWS service integrations using Python.
While not production-critical, the project attemps to mirror real-world patterns and challenges to help build practical skills.

InventoryCentral is a cloud-native inventory tracking backend designed to explore AWS CDK usage with Python and GitHub Actions.
The project automates the provisioning, deployment, and teardown of infrastructure on AWS using infrastructure as code and a secure CI/CD pipeline.

## What It Does
* Provides an extensible backend service for tracking inventory data.
* Automates the deployment process via GitHub Actions using OpenID.
* Connect (OIDC) for secure, credential-free AWS access.
* Uses the AWS CDK (in Python) to define and deploy infrastructure, following best practices for modern cloud applications.

## Key Components
* AWS CDK (Python) - Used to define the infrastructure (API Gateway, Lambda, S3, Route53, etc.) as code.
* GitHub Actions + OIDC - Automates cdk synth, deploy, and destroy operations without AWS secrets, using federated identity.
* Route53- DNS Routing and domain management for backend endpoints.
* S3 - Asset and deployment artifact storage during CDK operations.
* SSM Parameter Store - Stores CDK bootstrap metadata and versioning used during deployments.
* IAM Roles & Policies - Fine-grained access control for all resources, including cross-role assumptions from GitHub.

## Deployment Workflow
Push to GitHub triggers build pipeline.
* Code formatting and linting
* cdk synth to generate CloudFormation templates

Manual GitHub trigger to deploy pipeline.
* cdk deploy to launch or update the infrastructure

Manual GitHub trigger to destroy pipline.
* cdk destroy to remove infrastructure

Assets and templates are uploaded to S3, and CDK roles are assumed via OIDC.


# Create virtual env
To manually create a virtualenv on MacOS and Linux, at the root of the project:

```
InventoryCentral$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
InventoryCentral$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
InventoryCentral$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
InventoryCentral$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Setting up the environment
Open up the env.sh file and modify, then source the file to set the environment.

```
InventoryCentral$ source ./env.sh
```

All CDK commands are available, this project uses a Makefile. See Makefile for details.

[![Build](https://github.com/bgants/InventoryCentral/actions/workflows/build.yml/badge.svg)](https://github.com/bgants/InventoryCentral/actions/workflows/build.yml)
