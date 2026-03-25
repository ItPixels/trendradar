"""Supabase auth integration."""
import httpx
from typing import Optional
from app.config import settings

class SupabaseAuth:
    """Verify Supabase JWT tokens."""

    def __init__(self):
        self.supabase_url = settings.supabase_url
        self.service_key = settings.supabase_service_key

    async def get_user_from_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return user data."""
        if not self.supabase_url or not self.service_key:
            return None

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.supabase_url}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": self.service_key,
                },
            )
            if resp.status_code == 200:
                return resp.json()
            return None


supabase_auth = SupabaseAuth()
