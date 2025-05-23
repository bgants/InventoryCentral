from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/products")
def get_products():
    return {"statusCode": 200, "body": "Get all products!"}


@app.get("/products/<product_id>")
def get_product(product_id: int):
    logger.info(f"Get product ID: {product_id}")
    return {"statusCode": 200, "body": "Get product!"}


@app.post("/products")
def create_product():
    product: dict = app.current_event.json_body
    logger.info(f"Create product: {product}")
    return {"statusCode": 200, "body": "Create product!"}


@app.put("/products/<product_id>")
def update_product(product_id: int):
    product: dict = app.current_event.json_body
    logger.info(f"Update product: {product} with ID: {product_id}")
    return {"statusCode": 200, "body": "Update product!"}


@app.delete("/products/<product_id>")
def delete_product(product_id: int):
    logger.info(f"Delete product ID: {product_id}")
    return {"statusCode": 200, "body": "Delete product!"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(f" Event: {event}")
    return app.resolve(event, context)
