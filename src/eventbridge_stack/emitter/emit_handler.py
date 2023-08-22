import boto3
import json
import os

def lambda_handler(event, context):
    client = boto3.client("events")
    detail = {"message": "Hello World", "payload": "I come from your event bus!"}
    response = client.put_events(
        Entries=[
            {
                'Source': 'emitter',
                'DetailType': 'example_event',
                'Detail': json.dumps(detail),
                'EventBusName': os.getenv("bus_name")
            }
        ]
    )
    return response