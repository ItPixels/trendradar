"""API key authentication for programmatic access."""
from fastapi import Request, HTTPException
from typing import Optional
import hashlib

async def verify_api_key(request: Request) -> Optional[str]:
    """Verify API key from X-API-Key header."""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return None

    # Hash the key for lookup
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    # TODO: Look up key_hash in api_keys table
    # api_key_record = await db.execute(
    #     select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.is_active == True)
    # )

    return key_hash
