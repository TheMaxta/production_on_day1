from .schema import UploadJob
from app_config import AppConfig
from shared_infra.s3 import S3Client
from shared_infra.dynamo import DynamoRepository

class UploadImageWorker:
    """Processes upload jobs and persists minimal metadata."""
    def __init__(self, cfg: AppConfig | None = None):
        self.cfg = cfg or AppConfig()
        self.s3 = S3Client(bucket=self.cfg.bucket)
        self.repo = DynamoRepository(table_name=self.cfg.table)

    def handle_job(self, job: UploadJob) -> None:
        head = self.s3.head(job.s3_key)
        meta = {"content_type": job.content_type, "size": head.get("ContentLength")}
        url = self.s3.presign_get(job.s3_key)
        self.repo.put_image_record(job.image_id, job.s3_key, {**meta, "url": url})
