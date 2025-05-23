from aws_cdk import (
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
)

from constructs import Construct


class Database(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        lambda_function: iam.IGrantable,
    ) -> None:
        super().__init__(scope, construct_id)
        # Create a DynamoDB table
        self.inventory_table = dynamodb.Table(
            self,
            "InventoryTable",
            table_name="InventoryTable",
            partition_key=dynamodb.Attribute(
                name="product_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="location_id", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Add a GSI for querying by location_id
        self.inventory_table.add_global_secondary_index(
            index_name="ByLocation",
            partition_key=dynamodb.Attribute(
                name="location_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="product_id", type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL,  # or KEYS_ONLY, INCLUDE
        )

        # Give permission to lambda to use table
        self.inventory_table.grant_read_write_data(lambda_function)
