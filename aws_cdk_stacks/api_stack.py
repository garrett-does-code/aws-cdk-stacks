'''This stack uses a lambda layer, lambda proxy, and API Gateway.'''
import os
from pathlib import Path
from aws_cdk import (
    NestedStack,
    aws_lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigw,
    Duration,
    Tags
)
from constructs import Construct

class ApiStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Dynamo Table
        self.table = dynamodb.Table(
            self,
            "ExampleItemsTable",
            table_name="ItemsTable",
            partition_key=dynamodb.Attribute(
                name="email",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        Tags.of(self.table).add("application", construct_id)

        # Get Lambda Layer
        # For Pydantic, we need to build on the same OS as our lambda.
        # I built the lambda layer on an Amazon Linux 2 EC2 instance
        self.layer = aws_lambda.LayerVersion.from_layer_version_arn(
            self, "FastApiMangumPydanticLayer",
            layer_version_arn=f"arn:aws:lambda:{self.region}:{self.account}:layer:fastapi-mangum-pydantic:3"
        )

        # Get /src directory
        path = Path(os.path.dirname(__file__))
        src_dir = os.path.join(path.parent.resolve(), "src")

        # Create Lambda Proxy
        self.lambda_proxy = aws_lambda.Function(
            self, "ExampleLambdaProxy", 
            code=aws_lambda.Code.from_asset(
                os.path.join(src_dir, "api_stack")
            ),
            handler="handler.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            timeout=Duration.minutes(5),
            memory_size=512,
            environment={"table": self.table.table_name},
            layers=[self.layer]
        )
        Tags.of(self.lambda_proxy).add("application", construct_id)

        # Allow lambda permissions to dynamo table
        self.table.grant_read_write_data(self.lambda_proxy)

        # Create API Gateway
        self.api = apigw.LambdaRestApi(
            self,
            "ExampleApi",
            handler=self.lambda_proxy,
            proxy=True
        )

        