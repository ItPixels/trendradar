"""Auth middleware for FastAPI."""
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.auth.supabase import supabase_auth

security = HTTPBearer(auto_error=False)

async def get_current_user(request: Request) -> Optional[dict]:
    """Extract and verify the current user from the request."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    user = await supabase_auth.get_user_from_token(token)

    return user

async def require_auth(request: Request) -> dict:
    """Require authenticated user — raises 401 if not authenticated."""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
