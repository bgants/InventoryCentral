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
        "product_id": "P1003",
        "location_id": "STORE5",
        "product_name": "Widget C",
        "quantity": 45,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P2002",
        "location_id": "Happy Store",
        "product_name": "Gadget B",
        "quantity": 75,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P3003",
        "location_id": "STORE15",
        "product_name": "Thing C",
        "quantity": 50,
        "last_updated": "2025-05-08",
    },    {
        "product_id": "P1001",
        "location_id": "WH3",
        "product_name": "Widget A",
        "quantity": 125,
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
        "location_id": "WH2",
        "product_name": "Gadget B",
        "quantity": 55,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P3003",
        "location_id": "STORE6",
        "product_name": "Thing C",
        "quantity": 10,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "P1005",
        "location_id": "WH1",
        "product_name": "Symteric-Atomic Wrench",
        "quantity": 10,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "Q1001",
        "location_id": "STORE5",
        "product_name": "Zoter Synthizer Washer A",
        "quantity": 435,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "Q4002",
        "location_id": "WH3",
        "product_name": "Dizmoid Gizmo Shifter Ring B",
        "quantity": 25,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "Z3003",
        "location_id": "STORE1",
        "product_name": "Atomizer Wire Wrap Kit",
        "quantity": 600,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "R1001",
        "location_id": "WH3",
        "product_name": "Wide O-Ring Insert A",
        "quantity": 20,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "F1001",
        "location_id": "STORE3",
        "product_name": "Fly Tie Tape Green",
        "quantity": 15,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "G2002",
        "location_id": "WH1",
        "product_name": "Grunion Guts Removal Kit",
        "quantity": 15,
        "last_updated": "2025-05-08",
    },
    {
        "product_id": "X3003",
        "location_id": "STORE1",
        "product_name": "Traction Gear Cleaning and Lube Set",
        "quantity": 60,
        "last_updated": "2025-05-08",
    },
]

# Insert items
for item in items:
    response = table.put_item(Item=item)
    print(f"Inserted: {item['product_id']} at {item['location_id']}")
