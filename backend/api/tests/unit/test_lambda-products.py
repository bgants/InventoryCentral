import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from runtime.lambda_function import handler  # pylint: disable=import-error


def mock_api_gateway_post_event():
    # Simulate API Gateway event
    return {
        "httpMethod": "POST",
        "path": "/products",
        "headers": {"Content-Type": "application/json"},
        "queryStringParameters": {},
        "body": json.dumps(
            {
                "product_id": "XYZ456",
                "location_id": "Jimmy's House",
                "product_name": "Dizlesnazer Connectors",
                "quantity": 13,
                "last_updated": "2025-05-25",
            }
        ),
        "isBase64Encoded": False,
    }


def mock_api_gateway_get_event():
    return {
        "httpMethod": "GET",
        "path": "/products/XYZ456",
        "resource": "/products/{product_id}",
        "pathParameters": {"product_id": "XYZ456"},
        "queryStringParameters": None,
        "headers": {"Accept": "application/json"},
        "multiValueHeaders": {"Accept": ["application/json"]},
        "requestContext": {
            "resourcePath": "/products/{product_id}",
            "httpMethod": "GET",
        },
        "body": None,
        "isBase64Encoded": False,
    }


def mock_lambda_context():
    return SimpleNamespace(
        function_name="test_function",
        memory_limit_in_mb=128,
        invoked_function_arn="arn:aws:lambda:us-east-1:123456789012:function:test_function",
        aws_request_id="test-invoke-request",
    )


# Test for POST /products
@patch("resources.get_table")
def test_create_product(mock_get_table):
    # Create a mock table instance
    mock_table_instance = MagicMock()
    mock_get_table.return_value = mock_table_instance

    # Mock the put_item to do nothing (or return a fake response if needed)
    mock_table_instance.put_item.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200}
    }

    # Call the handler
    response = handler(mock_api_gateway_post_event(), mock_lambda_context())

    # Assertions
    assert int(response["statusCode"]) == 200

    response = handler(mock_api_gateway_post_event(), mock_lambda_context())

    assert int(response["statusCode"]) == 200
    body = json.loads(response["body"])
    assert body["statusCode"] == 200
    assert body["body"]["message"] == "Product created successfully!"
    assert body["body"]["product_id"] == "XYZ456"
    assert body["body"]["location_id"] == "Jimmy's House"


# Test for GET /products/{product_id}
@patch("resources.get_table")
def test_get_product(mock_get_table):
    mock_table = MagicMock()
    mock_table.query.return_value = {
        "Items": [
            {
                "product_id": "XYZ456",
                "location_id": "Jimmy's House",
                "product_name": "Dizlesnazer ANALOG Connectors",
                "quantity": 13,
                "last_updated": "2025-05-25",
            }
        ]
    }
    mock_get_table.return_value = mock_table

    # Call the Lambda handler with a mock event
    response = handler(mock_api_gateway_get_event(), mock_lambda_context())

    # Assert response contains the expected mock data
    assert response["statusCode"] == 200
    assert "XYZ456" in str(response["body"])
