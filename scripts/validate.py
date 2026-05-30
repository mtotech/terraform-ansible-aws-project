#!/usr/bin/env python3

import boto3
import requests
import sys

REGION = "ap-south-1"
BUCKET_NAME = "myapp-prod-bucket-12345"

def validate():

    errors = []

    ec2 = boto3.client("ec2", region_name=REGION)
    response = ec2.describe_instances()

    running = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == "running":
                running.append(instance)

    if len(running) < 2:
        errors.append("Expected at least 2 running EC2 instances")

    try:
        s3 = boto3.client("s3", region_name=REGION)
        s3.head_bucket(Bucket=BUCKET_NAME)
    except Exception as e:
        errors.append(f"S3 Error: {e}")

    try:
        rds = boto3.client("rds", region_name=REGION)
        dbs = rds.describe_db_instances()

        if len(dbs["DBInstances"]) == 0:
            errors.append("No RDS instance found")

    except Exception as e:
        errors.append(f"RDS Error: {e}")

    health_ok = False

    for instance in running:

        public_ip = instance.get("PublicIpAddress")

        if not public_ip:
            continue

        try:
            response = requests.get(
                f"http://{public_ip}:5000/health",
                timeout=5
            )

            if response.text.strip() == "Healthy":
                health_ok = True
                break

        except Exception:
            pass

    if not health_ok:
        errors.append("Flask Health Check Failed")

    if errors:

        print("\nVALIDATION FAILED\n")

        for err in errors:
            print(err)

        sys.exit(1)

    print("\nVALIDATION PASSED\n")

if __name__ == "__main__":
    validate()
