import boto3, json
from botocore.client import BaseClient

class SQSQueues:
    """Minimal queue sender."""
    def __init__(self, upload_url: str, analyze_url: str, sqs: BaseClient | None = None):
        self.sqs = sqs or boto3.client("sqs")
        self.upload_url = upload_url
        self.analyze_url = analyze_url

    def send_upload_job(self, payload: dict) -> None:
        self.sqs.send_message(QueueUrl=self.upload_url, MessageBody=json.dumps(payload))

    def send_analyze_job(self, payload: dict) -> None:
        self.sqs.send_message(QueueUrl=self.analyze_url, MessageBody=json.dumps(payload))
