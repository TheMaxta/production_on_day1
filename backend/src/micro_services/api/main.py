from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app_config import AppConfig
from shared_infra.s3 import S3Client
from shared_infra.dynamo import DynamoRepository
from shared_infra.sqs import SQSQueues
from .schema import PresignReq, PresignResp, EnqueueUploadReq, AnalyzeReq
import uuid

ALLOWED = {"image/jpeg", "image/png", "image/webp"}

class ApiService:
    """
    Thin HTTP façade over shared_infra + microservice queues. STUB ONLY.
    """

    def __init__(self, cfg: AppConfig | None = None):
        self.cfg = cfg or AppConfig()
        self.s3 = S3Client(bucket=self.cfg.bucket)
        self.sqs = SQSQueues(upload_url=self.cfg.upload_q, analyze_url=self.cfg.analyze_q)
        self.repo = DynamoRepository(table_name=self.cfg.table)

    def presign_upload(self, req: PresignReq) -> PresignResp:
        """
        Return {image_id, s3_key, url} for browser PUT.
        """
        if req.content_type not in ALLOWED:
            raise HTTPException(status_code=400, detail="unsupported content_type")
        image_id = str(uuid.uuid4())
        s3_key = f"uploads/{image_id}"
        url = self.s3.presign_put(s3_key, req.content_type)
        return PresignResp(image_id=image_id, s3_key=s3_key, url=url)

    def enqueue_upload(self, req: EnqueueUploadReq) -> None:
        """Send UploadJob to SQS."""
        self.sqs.send_upload_job(req.model_dump())

    def enqueue_analyze(self, req: AnalyzeReq) -> None:
        """Send AnalyzeJob to SQS."""
        raise NotImplementedError

    def get_image(self, image_id: str) -> dict:
        """Lookup image record by id."""
        return self.repo.get_record(image_id) or {}


# FastAPI surface (kept for Swagger in frontend)
app = FastAPI(title="GenAI AWS API", version="0.0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
svc = ApiService()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/uploads/presign", response_model=PresignResp, tags=["uploads"])
def presign(req: PresignReq):
    return svc.presign_upload(req)

@app.post("/uploads/notify", tags=["uploads"])
def notify(req: EnqueueUploadReq):
    svc.enqueue_upload(req)
    return {"enqueued": True}

@app.post("/analyze", tags=["analyze"])
def analyze(req: AnalyzeReq):
    svc.sqs.send_analyze_job({"image_id": req.image_id})
    return {"enqueued": True}

@app.get("/images/{image_id}", tags=["images"])
def get_image(image_id: str):
    item = svc.get_image(image_id)
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item
