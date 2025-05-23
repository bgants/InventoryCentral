import os
import aws_cdk as cdk
from backend.component import Backend

account = os.getenv("AWS_ACCOUNT_ID")
primary_region = os.getenv("AWS_PRIMARY_REGION")
secondary_region = os.getenv("AWS_SECONDARY_REGION")
domain_name = os.getenv("AWS_DOMAIN_NAME") or "example.com"
primary_environment = cdk.Environment(account=account, region=primary_region)
# secondary_environment = cdk.Environment(account=account, region=secondary_region)

app = cdk.App()

Backend(
    app,
    "Backend",
    domain_name=domain_name,
    env=primary_environment,
)

app.synth()
