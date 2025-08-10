from fastapi import FastAPI, HTTPException
from .schema import PresignReq, PresignResp, EnqueueUploadReq, AnalyzeReq

class ApiService:
    """
    Thin HTTP façade over shared_infra + microservice queues. STUB ONLY.
    """

    def __init__(self) -> None:
        # Wire real implementations in step 3.
        pass

    def presign_upload(self, req: PresignReq) -> PresignResp:
        """
        Return {image_id, s3_key, url} for browser PUT.
        """
        raise NotImplementedError

    def enqueue_upload(self, req: EnqueueUploadReq) -> None:
        """Send UploadJob to SQS."""
        raise NotImplementedError

    def enqueue_analyze(self, req: AnalyzeReq) -> None:
        """Send AnalyzeJob to SQS."""
        raise NotImplementedError

    def get_image(self, image_id: str) -> dict:
        """Lookup image record by id."""
        raise NotImplementedError


# FastAPI surface (kept for Swagger in frontend)
app = FastAPI(title="GenAI AWS API", version="0.0.1")
svc = ApiService()

@app.post("/uploads/presign", response_model=PresignResp, tags=["uploads"])
def presign(req: PresignReq):
    # Stubbed: expose API shape for Swagger UI
    raise HTTPException(status_code=501, detail="Not implemented (stub)")

@app.post("/uploads/notify", tags=["uploads"])
def notify(req: EnqueueUploadReq):
    raise HTTPException(status_code=501, detail="Not implemented (stub)")

@app.post("/analyze", tags=["analyze"])
def analyze(req: AnalyzeReq):
    raise HTTPException(status_code=501, detail="Not implemented (stub)")

@app.get("/images/{image_id}", tags=["images"])
def get_image(image_id: str):
    raise HTTPException(status_code=501, detail="Not implemented (stub)")
