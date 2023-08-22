'''This stack deploys an event bus, EventBridge Rule, SQS queue with dead-letter queue, and lambdas.'''
import os
from pathlib import Path
from aws_cdk import (
    NestedStack,
    aws_sqs as sqs,
    aws_events,
    aws_events_targets,
    aws_lambda,
    aws_lambda_event_sources,
    Duration,
    Tags
)
from constructs import Construct

class EventBridgeStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the event bus
        self.event_bus = aws_events.EventBus(
            self, "event-bus"
        )
        # Add some tags for tracking
        Tags.of(self.event_bus).add("application", construct_id)

        # Use the generated defaults
        bus_name = self.event_bus.event_bus_name

        # Get /src directory
        path = Path(os.path.dirname(__file__))
        src_dir = os.path.join(path.parent.resolve(), "src")

        # Create the emitter and receiver lambdas
        self.emitter_lambda = aws_lambda.Function(
            self, "emitter-lambda", 
            code=aws_lambda.Code.from_asset(
                os.path.join(src_dir, "eventbridge_stack", "emitter")
            ),
            handler="emit_handler.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            timeout=Duration.minutes(5),
            memory_size=512,
            environment={"bus_name": bus_name}
        )
        Tags.of(self.emitter_lambda).add("application", construct_id)

        self.receiver_lambda = aws_lambda.Function(
            self, "receiver-lambda", 
            code=aws_lambda.Code.from_asset(
                os.path.join(src_dir, "eventbridge_stack", "receiver")
            ),
            handler="receive_handler.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            timeout=Duration.minutes(5),
            memory_size=512
        )
        Tags.of(self.receiver_lambda).add("application", construct_id)

        # Create the SQS queues
        self.dlq = sqs.Queue(
            self, "event-dlq", retention_period=Duration.days(7)
        )
        Tags.of(self.dlq).add("application", construct_id)

        self.queue = sqs.Queue(
            self, "event-queue",
            dead_letter_queue=sqs.DeadLetterQueue(
                queue=self.dlq, max_receive_count=5
            ),
            visibility_timeout=self.receiver_lambda.timeout
        )
        Tags.of(self.queue).add("application", construct_id)

        # Add event and permissions to receiver lambda
        self.receiver_lambda.add_event_source(
            aws_lambda_event_sources.SqsEventSource(self.queue)
        )
        self.queue.grant_consume_messages(self.receiver_lambda)
        self.dlq.grant_send_messages(self.receiver_lambda)

        # Allow emitter lambda to send events to bus
        self.event_bus.grant_all_put_events(self.emitter_lambda)

        # Set up EventBridge Rule
        self.event_rule = aws_events.Rule(
            self, "event-rule", 
            event_bus=self.event_bus,
            event_pattern=aws_events.EventPattern(
                source=["emitter"],
                detail_type=["example_event"],
                detail={
                    "message": ["Hello World"]
                }
            ),
            targets=[aws_events_targets.SqsQueue(self.queue)]
        )
        Tags.of(self.event_rule).add("application", construct_id)

