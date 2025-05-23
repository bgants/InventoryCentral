from aws_lambda_powertools import Logger
import boto3

# Powertools logger
logger = Logger()

# DynamoDB client or resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("InventoryTable")