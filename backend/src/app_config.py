from dataclasses import dataclass, field
import os

@dataclass(frozen=True)
class AppConfig:
    region: str        = field(default_factory=lambda: os.getenv("AWS_REGION", "us-west-2"))
    bucket: str        = field(default_factory=lambda: os.getenv("APP_BUCKET", ""))
    table: str         = field(default_factory=lambda: os.getenv("APP_TABLE", ""))
    upload_q: str      = field(default_factory=lambda: os.getenv("UPLOAD_QUEUE_URL", ""))
    analyze_q: str     = field(default_factory=lambda: os.getenv("ANALYZE_QUEUE_URL", ""))

    provider: str      = field(default_factory=lambda: os.getenv("COMPLETIONS_PROVIDER", "openai"))
    small_model: str   = field(default_factory=lambda: os.getenv("SMALL_MODEL", "gpt-4o-mini"))
    vlm_model: str     = field(default_factory=lambda: os.getenv("VLM_MODEL", "gpt-4o"))
    thinking_model: str= field(default_factory=lambda: os.getenv("THINKING_MODEL", "o3-mini"))

    anthropic_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

    openai_key: str    = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))          # optional for local
    openai_secret_name:str = field(default_factory=lambda: os.getenv("OPENAI_SECRET_NAME", ""))   # used in Lambda

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
