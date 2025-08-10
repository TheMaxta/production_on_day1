from app_config import AppConfig
from shared_infra.dynamo import DynamoRepository
from shared_tools.prompt_warehouse.registry import PromptRegistry
from shared_tools.completions import build_completions

class AnalyzeImageWorker:
    """Loads image record, renders prompt, calls provider, saves analysis."""
    def __init__(self, cfg: AppConfig | None = None):
        self.cfg = (cfg or AppConfig()).validate()
        self.repo = DynamoRepository(table_name=self.cfg.table)
        self.prompts = PromptRegistry()
        self.completions = build_completions(self.cfg)

    def handle_job(self, image_id: str) -> None:
        item = self.repo.get_record(image_id)
        if not item: return
        url = item.get("meta", {}).get("url")
        if not url: return
        p = self.prompts.render(
            "image_describe_v1",
            tone="neutral",
            audience="a general user",
            style="concise",
        )
        text = self.completions.vlm(p.system, p.user, image_url=url)
        self.repo.set_analysis(image_id, {"provider": self.cfg.provider, "model": self.cfg.vlm_model, "text": text})
