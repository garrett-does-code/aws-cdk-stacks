# AWS Workflows

The `main_stack.py` owns a culmination of nested stacks. Each stack is a different common AWS workflow.

## EventBridge Stack

This stack uses Event Bus, EventBridge Rule, SQS Queue with Dead-Letter Queue, and two lambdas to simulate
a bus-driven workflow.

### Flow
1. The emitter lambda adds a message onto the event bus.
2. The EventBridge rule listens to a specific message pattern.
3. On pattern match, the message is enqueued on the SQS queue.
4. The SQS queue triggers the receiver lambda.

## API Stack

This stack uses API Gateway, DynamoDB, and Lambda to create a serverless API solution.
The end solution allows for the creation and retrieval of generic Items for a simple retail application.

The Lambda is a proxy that utilizes [FastAPI](https://fastapi.tiangolo.com/) to handle routing as well as
auto generate Swagger documentation.

### Flow
1. Create a DynamoDB table with pk `email` and sk `id`.
2. Create a reference to the lambda layer containing [FastAPI](https://fastapi.tiangolo.com/), 
[Mangum](https://mangum.io/), and [Pydantic](https://docs.pydantic.dev/latest/).
3. Create the lambda proxy.
4. Assign the lambda proxy as the handler for the Lambda Rest API.
