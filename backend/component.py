from aws_cdk import (
    CfnOutput,
    Stack,
)

from constructs import Construct
from backend.api.infrastructure import API
from backend.database.infrastructure import Database


class Backend(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = API(
            self,
            "API",
            domain_name=domain_name,
        )

        database = Database(
            self,
            "Database",
            lambda_function=api.lambda_function,
        )

        # Output the API Gateway URL
        CfnOutput(
            self,
            "APIGatewayURL",
            value=f"https://{api.apigateway_domain_name.domain_name}",
        )
        CfnOutput(self, "DynamoDBTableName", value=database.inventory_table.table_name)
