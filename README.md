
# AWS CDK Stacks

This is an AWS CDK project with various workflow examples.

I like to use [Poetry](https://python-poetry.org/) for dependency management.

To run this repo, install Poetry and python version 3.11.

At the parent level directory, add a `.env` file with the following:

```
CDK_DEFAULT_ACCOUNT=<your_account>
CDK_DEFAULT_REGION=<your_region_here>
```

To initialize the virtual environment run:

```
$ poetry install
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Or you can run the unit tests.

```
poetry run pytest tests/
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
