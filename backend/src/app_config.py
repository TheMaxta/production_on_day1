from dataclasses import dataclass, field
import os

@dataclass(frozen=True)
class AppConfig:
    """Process-level configuration sourced from environment variables."""
    region: str        = field(default_factory=lambda: os.getenv("AWS_REGION", "us-west-2"))
    bucket: str        = field(default_factory=lambda: os.getenv("APP_BUCKET", ""))
    table: str         = field(default_factory=lambda: os.getenv("APP_TABLE", ""))
    upload_q: str      = field(default_factory=lambda: os.getenv("UPLOAD_QUEUE_URL", ""))
    analyze_q: str     = field(default_factory=lambda: os.getenv("ANALYZE_QUEUE_URL", ""))
    openai_model: str  = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    openai_key: str    = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    def validate(self) -> "AppConfig":
        missing = [k for k, v in {
            "APP_BUCKET": self.bucket,
            "APP_TABLE": self.table,
            "UPLOAD_QUEUE_URL": self.upload_q,
            "ANALYZE_QUEUE_URL": self.analyze_q,
        }.items() if not v]
        if missing:
            raise RuntimeError(f"Missing required env: {', '.join(missing)}")
        return self
