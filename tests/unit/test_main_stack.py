import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_stacks.main_stack import MainStack

app = core.App()
stack = MainStack(app, "aws-cdk-stacks")

def test_eventbridge_queue():
    template = assertions.Template.from_stack(stack.eventbridge_stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })

def test_eventbridge_lambdas():
    template = assertions.Template.from_stack(stack.eventbridge_stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "MemorySize": 512,
        "Timeout": 300,
        "Runtime": "python3.11"
    })

def test_eventbridge_rule():
    template = assertions.Template.from_stack(stack.eventbridge_stack)

    template.has_resource_properties("AWS::Events::Rule", {
        "EventPattern": {
            "detail": {
                "message": [
                    "Hello World"
                ]
            },
            "detail-type": [
                "example_event"
            ],
            "source": [
                "emitter"
            ]
        }
    })