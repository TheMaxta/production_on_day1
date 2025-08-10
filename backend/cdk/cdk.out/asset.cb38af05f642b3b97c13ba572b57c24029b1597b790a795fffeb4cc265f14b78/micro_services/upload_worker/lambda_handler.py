"""
SQS event → UploadImageWorker (stub).
No business logic; will raise NotImplemented when worker runs.
"""
import json
from .worker import UploadImageWorker
from .schema import UploadJob

_worker = UploadImageWorker()

def handler(event, _ctx):
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        job = UploadJob(**body)
        # stub dispatch (will hit NotImplemented in handle_job)
        _worker.handle_job(job)
    return {"ok": True}
