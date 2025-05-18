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
BackendStack(
    app,
    "BackendStack",
    env=primary_environment,
    domain_name=domain_name,
    secondary_region=secondary_region,
)
app.synth()
