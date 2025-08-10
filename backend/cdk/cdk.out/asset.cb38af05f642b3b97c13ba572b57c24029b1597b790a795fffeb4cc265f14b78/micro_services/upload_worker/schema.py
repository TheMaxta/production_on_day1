from pydantic import BaseModel

class UploadJob(BaseModel):
    """
    Job payload consumed from SQS (stub).
    """
    image_id: str
    s3_key: str
    content_type: str  # jpeg|png|webp
    # Optional: inline data for local tests later
