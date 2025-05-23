from datetime import datetime
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from botocore.exceptions import ClientError
from resources import logger, table


def register_product_routes(app: APIGatewayRestResolver):
    @app.get("/products/<product_id>")
    def get_product(product_id: str):
        logger.info(f"Get product ID: {product_id}")
        try:
            response = table.query(
                KeyConditionExpression="product_id = :pid",
                ExpressionAttributeValues={":pid": product_id},
            )
            return {"statusCode": 200, "body": response.get("Items", [])}
        except ClientError as e:
            logger.error(f"Error getting product: {str(e)}")
            return {"statusCode": 500, "body": str(e)}

    @app.post("/products")
    def create_product():
        logger.info("Create product")
        try:
            body: dict = app.current_event.json_body
            product_id = body.get("product_id")
            location_id = body.get("location_id")

            items = {
                "product_id": product_id,
                "location_id": location_id,
                **{
                    k: v
                    for k, v in body.items()
                    if k not in ["product_id", "location_id"]
                },
            }

            table.put_item(Item=items)
            logger.info(f"Inserted: {product_id} at {location_id}")
            return {
                "statusCode": 200,
                "body": {
                    "message": "Product created successfully!",
                    "product_id": product_id,
                    "location_id": location_id,
                },
            }
        except ClientError as e:
            logger.error(f"Error creating product: {str(e)}")
            return {"statusCode": 500, "body": str(e)}

    @app.put("/products/<product_id>/<location_id>")
    def update_product(product_id: str, location_id: str):
        logger.info(f"Update product with ID: {product_id} at location: {location_id}")
        try:
            now = datetime.utcnow().isoformat()
            body: dict = app.current_event.json_body
            table.update_item(
                Key={"product_id": product_id, "location_id": location_id},
                UpdateExpression="set #product_name = :product_name, quantity = :quantity, last_updated = :last_updated",
                ExpressionAttributeNames={"#product_name": "product_name"},
                ExpressionAttributeValues={
                    ":product_name": body.get("product_name"),
                    ":quantity": body.get("quantity"),
                    ":last_updated": now,
                },
                ConditionExpression="attribute_exists(product_id) AND attribute_exists(location_id)",
            )
            logger.info(f"Updated: {product_id} at {location_id}")
            return {
                "statusCode": 200,
                "body": {
                    "message": "Product updated successfully!",
                    "product_id": product_id,
                    "location_id": location_id,
                },
            }
        except ClientError as e:
            logger.error(f"Error updating product: {str(e)}")

    @app.delete("/products/<product_id>/<location_id>")
    def delete_product(product_id: str, location_id: str):
        logger.info(f"Delete product with ID: {product_id} at location: {location_id}")
        try:
            table.delete_item(
                Key={"product_id": product_id, "location_id": location_id}
            )
            logger.info(f"Deleted: {product_id} at {location_id}")
            return {
                "statusCode": 200,
                "body": {
                    "message": "Product deleted successfully!",
                    "product_id": product_id,
                    "location_id": location_id,
                },
            }
        except ClientError as e:
            logger.error(f"Error deleting product: {str(e)}")
            return {"statusCode": 500, "body": str(e)}
