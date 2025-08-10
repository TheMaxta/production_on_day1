#!/usr/bin/env python3
import aws_cdk as cdk
from stacks import GenAiStack

app = cdk.App()
GenAiStack(app, "GenAiStack")
app.synth()
