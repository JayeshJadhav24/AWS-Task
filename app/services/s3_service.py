import os
import uuid

from fastapi import UploadFile

from app.services.aws_common import get_boto3_client

s3_client = get_boto3_client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")


def create_bucket_if_not_exists():
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except Exception:
        create_kwargs = {"Bucket": BUCKET_NAME}
        if os.getenv("AWS_DEFAULT_REGION") != "us-east-1":
            create_kwargs["CreateBucketConfiguration"] = {
                "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
            }
        s3_client.create_bucket(**create_kwargs)


def upload_file(file: UploadFile) -> str:
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "bin"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    s3_client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        unique_filename,
        ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
    )

    return f"{ENDPOINT_URL}/{BUCKET_NAME}/{unique_filename}"


def delete_file(file_url: str):
    filename = file_url.rstrip("/").split("/")[-1]
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
