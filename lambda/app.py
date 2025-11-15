import json
import os
import logging
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def _response(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

def lambda_handler(event, context):
    # HTTP API v2 puts method here:
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    logger.info(f"Event method={method} event={json.dumps(event)[:1000]}")

    if method == "GET":
        # Return all items (simple demo)
        resp = table.scan()
        return _response(200, resp.get("Items", []))

    if method == "POST":
        raw = event.get("body") or "{}"
        try:
            body = json.loads(raw) if isinstance(raw, str) else raw
        except json.JSONDecodeError:
            return _response(400, {"error": "Invalid JSON"})

        if "id" not in body:
            return _response(400, {"error": "Item must include 'id'"})

        table.put_item(Item=body)
        return _response(200, {"message": "Item added", "id": body["id"]})

    return _response(405, {"error": "Method not allowed"})

