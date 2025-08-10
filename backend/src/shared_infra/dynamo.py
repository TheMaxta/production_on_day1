import boto3
from typing import Any, Optional, Dict
from boto3.resources.base import ServiceResource

class DynamoRepository:
    """Minimal image record repository."""
    def __init__(self, table_name: str, dynamodb: ServiceResource | None = None):
        self.table = (dynamodb or boto3.resource("dynamodb")).Table(table_name)

    def put_image_record(self, image_id: str, s3_key: str, meta: Dict[str, Any]) -> None:
        self.table.put_item(Item={
            "pk": image_id,
            "type": "image",
            "s3_key": s3_key,
            "meta": meta,
            "status": "UPLOADED",
        })

    def get_record(self, image_id: str) -> Optional[Dict[str, Any]]:
        r = self.table.get_item(Key={"pk": image_id})
        return r.get("Item")
