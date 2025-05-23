#!/usr/bin/env python3
import os

import aws_cdk as cdk

from oidc.oidc_stack import OidcStack

import os
from stacks.backend_stack import BackendStack
import aws_cdk as cdk

account = os.getenv("AWS_ACCOUNT_ID")
primary_region = os.getenv("AWS_PRIMARY_REGION")
secondary_region = os.getenv("AWS_SECONDARY_REGION")
domain_name = os.getenv("AWS_DOMAIN_NAME")
primary_environment = cdk.Environment(account=account, region=primary_region)
secondary_environment = cdk.Environment(account=account, region=secondary_region)

app = cdk.App()
OidcStack(
    app,
    "OidcStack",
    env=primary_environment,
    domain_name=domain_name,
    secondary_region=secondary_region,
    gitlab_project_path="dev4754101/inventorycentral",
)

app.synth()
