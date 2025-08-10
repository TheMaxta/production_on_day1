from pydantic import BaseModel

class AnalyzeJob(BaseModel):
    """
    Job payload consumed from SQS (stub).
    """
    image_id: str
    extra: str | None = None
