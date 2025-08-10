from .schema import AnalyzeJob

class AnalyzeImageWorker:
    """
    SQS worker that runs vision analysis. STUB ONLY.

    Minimal logic (later):
    - Read record from Dynamo using image_id (from SQS payload)
    - Render prompt via PromptWarehouse
    - Call CompletionsClient (env-provided model)
    - Save analysis back to Dynamo
    """

    def __init__(self) -> None:
        # Inject DynamoRepository, PromptWarehouse, CompletionsClient in step 5.
        pass

    def handle_job(self, job: AnalyzeJob) -> None:
        """Process one analyze job."""
        raise NotImplementedError
