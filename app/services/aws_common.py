import os

import boto3
from dotenv import load_dotenv

load_dotenv()


def get_boto3_client(service_name: str):
    return boto3.client(
        service_name,
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
    )
