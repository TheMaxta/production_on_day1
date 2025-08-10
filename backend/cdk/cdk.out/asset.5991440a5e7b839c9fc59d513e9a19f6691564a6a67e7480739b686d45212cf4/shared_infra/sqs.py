from typing import Dict, Any

class SQSQueues:
    """SQS send/receive façade (stub)."""

    def send_upload_job(self, payload: Dict[str, Any]) -> None:
        """Enqueue an upload job."""
        raise NotImplementedError

    def send_analyze_job(self, payload: Dict[str, Any]) -> None:
        """Enqueue an analyze job."""
        raise NotImplementedError
