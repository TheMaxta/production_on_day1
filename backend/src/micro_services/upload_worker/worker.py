from .schema import UploadJob

class UploadImageWorker:
    """
    SQS worker that finalizes uploads. STUB ONLY.

    Intended minimal logic:
    1) Save image bytes to S3 (if inline path used)  [1 line later]
    2) Extract minimal metadata (shared tool)        [~1-3 lines later]
    3) Save presigned GET URL + metadata in Dynamo   [~1-3 lines later]
    """

    def __init__(self) -> None:
        # Inject S3Client + DynamoRepository in step 3/4.
        pass

    def handle_job(self, job: UploadJob) -> None:
        """Process one upload job."""
        raise NotImplementedError