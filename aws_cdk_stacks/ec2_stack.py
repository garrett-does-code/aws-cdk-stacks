import os
from pathlib import Path
from aws_cdk import (
    NestedStack,
    aws_iam as iam,
    aws_ec2 as ec2,
    Duration,
    Tags
)
from constructs import Construct

# WIP
class EC2Stack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "MyExampleVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16")
        )

        self.instance_profile_role = iam.Role(
            self,
            "EC2InstanceProfileRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        self.instance_profile_role.add_to_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["lambda:PublishLayerVersion"]
        ))

        self.lambda_layer_ec2 = ec2.Instance(
            self,
            "LambdaLayerEC2",
            instance_type=ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.T2,
                instance_size=ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            role=self.instance_profile_role
        )