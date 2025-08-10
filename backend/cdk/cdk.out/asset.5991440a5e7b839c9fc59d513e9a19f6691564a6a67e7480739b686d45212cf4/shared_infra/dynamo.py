from typing import Any, Optional, Dict

class DynamoRepository:
    """Image-centric repository (stub) on a single-table design."""

    def put_image_record(self, image_id: str, s3_key: str, meta: Dict[str, Any]) -> None:
        """
        Create/replace image item:
        - pk: image_id
        - type: "image"
        - s3_key, meta, status="UPLOADED"
        """
        raise NotImplementedError

    def get_record(self, image_id: str) -> Optional[Dict[str, Any]]:
        """Fetch image record by id or None if missing."""
        raise NotImplementedError

    def set_analysis(self, image_id: str, analysis: Dict[str, Any]) -> None:
        """Attach analysis payload and set status='DONE'."""
        raise NotImplementedError
