import boto3

# DynamoDB client or resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("InventoryTable")

# Sample inventory items
items = [
    {
        "product_id": "P1001",
        "location_id": "WH1",
        "product_name": "Widget A",
        "quantity": 120,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P1001",
        "location_id": "STORE5",
        "product_name": "Widget A",
        "quantity": 35,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P2002",
        "location_id": "WH1",
        "product_name": "Gadget B",
        "quantity": 75,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P3003",
        "location_id": "STORE5",
        "product_name": "Thing C",
        "quantity": 60,
        "last_updated": "2025-05-08",
    },
]

# Insert items
for item in items:
    response = table.put_item(Item=item)
    print(f"Inserted: {item['product_id']} at {item['location_id']}")
