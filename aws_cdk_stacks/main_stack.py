from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from .eventbridge_stack import EventBridgeStack

class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # This main stack deploys nested stacks
        self.eventbridge_stack = EventBridgeStack(self, "EventBridgeExampleStack")
