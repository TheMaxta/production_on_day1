"""
ASGI adapter for FastAPI → Lambda.
Endpoints still raise 501 in main.py (stub).
"""
from mangum import Mangum
from .main import app  # your FastAPI app with 501 endpoints

# Entry point for Lambda
handler = Mangum(app)
