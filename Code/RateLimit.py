import os
import time
import boto3
from datetime import datetime

dynamodb = boto3.client("dynamodb")
sns = boto3.client("sns")

TABLE = os.environ["TABLE_NAME"]
RATE_LIMIT = int(os.environ["RATE_LIMIT"])
WINDOW = int(os.environ["WINDOW_SECONDS"])
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    path = event["requestContext"]["http"]["path"].rstrip("/")

    client_id = (
        event.get("headers", {}).get("x-client-id")
        or event.get("queryStringParameters", {}).get("client_id")
    )

    if not client_id:
        return response(400, "Client ID required")

    if path == "/limit":
        return handle_limit(client_id)

    if path == "/dashboard":
        return handle_dashboard(client_id)

    return response(404, "Not Found")


def handle_limit(client_id):
    now = int(time.time())
    window_id = now // WINDOW
    expires_at = (window_id + 1) * WINDOW
    pk = f"{client_id}#{window_id}"

    res = dynamodb.update_item(
        TableName=TABLE,
        Key={"pk": {"S": pk}},
        UpdateExpression="ADD #c :inc SET expires_at = :exp",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={
            ":inc": {"N": "1"},
            ":exp": {"N": str(expires_at)}
        },
        ReturnValues="UPDATED_NEW"
    )

    count = int(res["Attributes"]["count"]["N"])

    if count == RATE_LIMIT + 1:
        send_sns_alert(client_id, count)

    status = 429 if count > RATE_LIMIT else 200

    return response(status, {
        "client_id": client_id,
        "count": count,
        "limit": RATE_LIMIT,
        "window_expires": expires_at
    })

def handle_dashboard(client_id):
    handle_limit(client_id)
    now = int(time.time())
    window_id = now // WINDOW
    pk = f"{client_id}#{window_id}"

    try:
        res = dynamodb.get_item(
            TableName=TABLE,
            Key={"pk": {"S": pk}}
        )
        count = int(res["Item"]["count"]["N"])
    except:
        count = 0

    remaining = max(0, RATE_LIMIT - count)
    color = "#e74c3c" if count > RATE_LIMIT else "#2ecc71"
    status_text = "LIMIT EXCEEDED" if count > RATE_LIMIT else "ALLOWED"

    html = f"""
    <html>
    <head>
        <title>Rate Limit Dashboard</title>
        <style>
            body {{
                display:flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh
                font-family: Arial;
                background: #f4f6f8;
                margin: 0;
            }}
            .card {{
                background: white;
                padding: 25px;
                width: 420px;
                border-radius: 10px;
                box-shadow: 0 6px 15px rgba(0,0,0,0.1);
            }}
            .status {{
                background: {color};
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Rate Limit Dashboard</h2>
            <div class="status">{status_text}</div>
            <p><b>Client:</b> {client_id}</p>
            <p><b>Used:</b> {count}</p>
            <p><b>Remaining:</b> {remaining}</p>
            <p><b>Window resets at: </b><br>
               {datetime.utcfromtimestamp((window_id + 1) * WINDOW)}
            </p>
        </div>
    </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }

def send_sns_alert(client_id, count):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Rate Limit Exceeded",
        Message=f"{client_id} exceeded rate limit with {count} requests"
    )

def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": body if isinstance(body, str) else str(body)
    }
