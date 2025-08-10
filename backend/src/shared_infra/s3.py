import boto3
from botocore.client import BaseClient

class S3Client:
    """Minimal S3 operations."""
    def __init__(self, bucket: str, s3: BaseClient | None = None):
        self.bucket = bucket
        self._s3 = s3 or boto3.client("s3")

    def presign_put(self, key: str, content_type: str, expires: int = 900) -> str:
        return self._s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=expires,
            HttpMethod="PUT",
        )

    def presign_get(self, key: str, expires: int = 900) -> str:
        return self._s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires,
        )

    def get_bytes(self, key: str) -> bytes:
        r = self._s3.get_object(Bucket=self.bucket, Key=key)
        return r["Body"].read()

    def head(self, key: str) -> dict:
        return self._s3.head_object(Bucket=self.bucket, Key=key)