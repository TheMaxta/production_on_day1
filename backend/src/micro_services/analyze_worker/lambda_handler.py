"""
SQS event → AnalyzeImageWorker.
"""
import json
from .worker import AnalyzeImageWorker
from .schema import AnalyzeJob

_worker = AnalyzeImageWorker()

def handler(event, _ctx):
    processed = 0
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        job = AnalyzeJob(**body)
        if getattr(job, "image_id", None):
            _worker.handle_job(job.image_id)
            processed += 1
    return {"processed": processed}
