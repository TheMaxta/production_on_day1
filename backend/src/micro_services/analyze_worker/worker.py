from app_config import AppConfig
from shared_infra.dynamo import DynamoRepository
from shared_infra.s3 import S3Client
from shared_tools.prompt_warehouse.registry import PromptRegistry
from shared_tools.completions import build_completions
import base64

class AnalyzeImageWorker:
    """Loads image record, renders prompt, calls provider, saves analysis."""
    def __init__(self, cfg: AppConfig | None = None):
        self.cfg = (cfg or AppConfig()).validate()
        self.repo = DynamoRepository(table_name=self.cfg.table)
        self.s3 = S3Client(bucket=self.cfg.bucket)
        self.prompts = PromptRegistry()
        self.completions = build_completions(self.cfg)

    def handle_job(self, image_id: str) -> None:
        item = self.repo.get_record(image_id)
        if not item: return

        key = item["s3_key"]
        meta = item.get("meta") or {}

        # Determine content type
        content_type = meta.get("content_type")
        if not content_type:
            head = self.s3.head(key)
            content_type = head.get("ContentType", "application/octet-stream")

        # Load bytes and build data URL
        raw = self.s3.get_bytes(key)
        b64 = base64.b64encode(raw).decode("ascii")
        data_url = f"data:{content_type};base64,{b64}"

        p = self.prompts.render(
            "image_describe_v1",
            tone="neutral",
            audience="a general user",
            style="concise",
        )

        text = self.completions.vlm(p.system, p.user, image_url=data_url)

        self.repo.set_analysis(
            image_id,
            {"provider": self.cfg.provider, "model": self.cfg.vlm_model, "text": text},
        )