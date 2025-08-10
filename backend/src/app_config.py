from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AppConfig:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    bucket_name: str = os.getenv("APP_BUCKET", "REPLACE_ME")
    table_name: str = os.getenv("APP_TABLE", "REPLACE_ME")
    upload_queue_url: str = os.getenv("UPLOAD_QUEUE_URL", "REPLACE_ME")
    analyze_queue_url: str = os.getenv("ANALYZE_QUEUE_URL", "REPLACE_ME")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "REPLACE_ME")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
