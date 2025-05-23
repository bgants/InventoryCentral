from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    aws_route53_targets as targets,
)

from constructs import Construct
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer


class API(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        # Create a Hosted Zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=domain_name
        )

        # Creat a Certificate
        # This means that ACM will create DNS records in the specified
        # hosted zone to prove ownership of the domain
        certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # Define the AWS LambdaPowertools Layer once so we can reuse it
        power_tools_layer = LambdaPowertoolsLayer(self, "LambdaPowertoolsLayer")

        # Define the Lambda function with the API Gateway Resolver
        self.lambda_function = _lambda.Function(
            self,
            "LambdaGatewayResolver",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset(
                "backend/api/runtime",
            ),
            layers=[power_tools_layer],
            environment={
                "DOMAIN_NAME": domain_name,
                "POWERTOOLS_SERVICE_NAME": "BACK_END_API",
                "POWER_TOOLS_LOG_LEVEL": "INFO",
            },
        )

        # Create an API Gateway
        self.rest_api = apigateway.LambdaRestApi(
            self,
            "RestAPI",
            rest_api_name="RestApi",
            description="Backend RestAPI",
            handler=self.lambda_function,
            proxy=False,
        )

        products = self.rest_api.root.add_resource("products")
        products.add_method("POST")  # POST /products

        product_id = products.add_resource("{product_id}")
        product_id.add_method("GET")  # GET /products/{product_id}

        location_id = product_id.add_resource("{location_id}")
        location_id.add_method("PUT")  # PUT /products/{product_id}/{location_id}
        location_id.add_method("DELETE")  # DELETE /products/{product_id}/{location_id}

        self.apigateway_domain_name = apigateway.DomainName(
            self,
            "RestAPIDomain",
            domain_name=domain_name,
            certificate=certificate,
            endpoint_type=apigateway.EndpointType.REGIONAL,
        )

        # Add base path mapping to the API
        apigateway.BasePathMapping(
            self,
            "RestAPIGatewayPathMapping",
            domain_name=self.apigateway_domain_name,
            rest_api=self.rest_api,
        )

        # Add ARecord to the Hosted Zone
        route53.ARecord(
            self,
            "RestAPIAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayDomain(self.apigateway_domain_name)
            ),
        )
