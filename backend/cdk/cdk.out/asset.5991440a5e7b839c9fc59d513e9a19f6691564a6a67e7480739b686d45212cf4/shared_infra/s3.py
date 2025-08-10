from typing import Optional

class S3Client:
    """Thin S3 CRUD facade (stub)."""

    def presign_put(self, key: str, content_type: str, expires: int = 900) -> str:
        """Return a presigned PUT URL for key/content_type."""
        raise NotImplementedError

    def presign_get(self, key: str, expires: int = 900) -> str:
        """Return a presigned GET URL for key."""
        raise NotImplementedError

    def put_bytes(self, key: str, data: bytes, content_type: Optional[str] = None) -> None:
        """Store raw bytes into S3 (optional path for tests/tools)."""
        raise NotImplementedError
