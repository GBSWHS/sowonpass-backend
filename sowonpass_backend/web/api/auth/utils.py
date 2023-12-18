from typing import Any

import httpx
from jose import jwt
from jose.exceptions import JWTError

from sowonpass_backend.settings import settings


async def get_sso_public_key(url: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.RequestError:
            return ""


async def verify_sso_jwt(token: str, pub_key: str, aud: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, pub_key, algorithms=["ES256"], audience=aud)
    except JWTError:
        return None


async def verify_jwt(token: str) -> dict[str, str] | None:
    try:
        return jwt.decode(
            token,
            settings.auth_secret,
            algorithms=[settings.auth_algorithm],
        )
    except JWTError:
        return None
