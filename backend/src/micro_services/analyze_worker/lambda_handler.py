"""
SQS event → AnalyzeImageWorker (stub).
"""
import json
from .worker import AnalyzeImageWorker
from .schema import AnalyzeJob

_worker = AnalyzeImageWorker()

def handler(event, _ctx):
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        job = AnalyzeJob(**body)
        _worker.handle_job(job)
    return {"ok": True}
