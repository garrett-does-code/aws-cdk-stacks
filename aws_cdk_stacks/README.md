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