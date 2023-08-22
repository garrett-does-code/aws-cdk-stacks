#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import aws_cdk as cdk

from aws_cdk_stacks.main_stack import MainStack

# load your .env file
load_dotenv()

# Setting deploy location. Learn more at https://docs.aws.amazon.com/cdk/latest/guide/environments.html
env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
app = cdk.App()
MainStack(app, "AwsCdkExamplesStack", env=env)

app.synth()
