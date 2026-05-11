import os

from app.services.aws_common import get_boto3_client

ses_client = get_boto3_client("ses")
SENDER = os.getenv("SES_SENDER_EMAIL")


def verify_email(email: str):
    ses_client.verify_email_identity(EmailAddress=email)


def send_todo_created_email(recipient_email: str, todo_title: str, todo_id: int):
    try:
        verify_email(SENDER)
        verify_email(recipient_email)
        ses_client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [recipient_email]},
            Message={
                "Subject": {
                    "Data": f"New TODO Created: {todo_title}",
                    "Charset": "UTF-8",
                },
                "Body": {
                    "Html": {
                        "Data": (
                            "<h2>Your TODO has been created!</h2>"
                            f"<p><b>Title:</b> {todo_title}</p>"
                            f"<p><b>ID:</b> {todo_id}</p>"
                            "<p>Manage this task from your LocalStack-backed TODO app.</p>"
                        ),
                        "Charset": "UTF-8",
                    }
                },
            },
        )
        return True
    except Exception:
        return False
