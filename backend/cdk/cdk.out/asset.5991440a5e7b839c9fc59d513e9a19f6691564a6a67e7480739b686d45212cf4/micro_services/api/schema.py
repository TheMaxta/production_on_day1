from pydantic import BaseModel

class PresignReq(BaseModel):
    content_type: str  # image/jpeg | image/png | image/webp

class PresignResp(BaseModel):
    image_id: str
    s3_key: str
    url: str  # presigned PUT

class EnqueueUploadReq(BaseModel):
    image_id: str
    s3_key: str
    content_type: str

class AnalyzeReq(BaseModel):
    image_id: str
    extra: str | None = None
