"""Simple API key authentication for admin endpoints."""

import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin-secret-key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_admin(api_key: str = Security(api_key_header)) -> str:
    """Verify admin API key."""
    if not api_key or api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key"
        )
    return api_key
