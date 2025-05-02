from aws_cdk import (
    Stack,
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, domain_name: str, secondary_region: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)