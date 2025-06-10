#!/usr/bin/env python3
"""
Deploy cfn-admin-user.yaml, wait for completion, and print the access-key outputs.

Usage: python create_cfn_admin_user.py  [--stack-name MyStack]  [--region us-east-1]
"""

import argparse
import pathlib
import sys
import time

import boto3
from botocore.exceptions import ClientError, WaiterError


def deploy(stack_name: str, template_path: pathlib.Path, region: str) -> None:
    cfn = boto3.client("cloudformation", region_name=region)

    try:
        template_body = template_path.read_text()
    except FileNotFoundError:
        sys.exit(f"Template not found: {template_path}")

    try:
        print(f"Creating stack {stack_name}…")
        cfn.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=["CAPABILITY_NAMED_IAM"],
        )
    except ClientError as e:
        if "AlreadyExistsException" in str(e):
            print(f"Stack {stack_name} exists – updating instead.")
            try:
                cfn.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Capabilities=["CAPABILITY_NAMED_IAM"],
                )
            except ClientError as ue:
                if "No updates" in str(ue):
                    print("No changes to apply.")
                    return
                raise
        else:
            raise

    waiter = cfn.get_waiter("stack_create_complete")
    try:
        print("Waiting for stack to reach CREATE_COMPLETE …")
        waiter.wait(StackName=stack_name)
    except WaiterError as w_err:
        sys.exit(f"Stack failed: {w_err}")

    outputs = cfn.describe_stacks(StackName=stack_name)["Stacks"][0].get("Outputs", [])
    for o in outputs:
        print(f"{o['OutputKey']}: {o['OutputValue']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stack-name",
        default="cfn-admin-user",
        help="CloudFormation stack name (default: cfn-admin-user)",
    )
    parser.add_argument(
        "--template",
        default="cfn-admin-user.yaml",
        help="Path to CloudFormation template (default: cfn-admin-user.yaml)",
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region for deployment (default: us-east-1)",
    )
    args = parser.parse_args()

    deploy(args.stack_name, pathlib.Path(args.template), args.region)


if __name__ == "__main__":
    main()
