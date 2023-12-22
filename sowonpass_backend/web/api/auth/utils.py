from typing import Any

from jose import jwt
from jose.exceptions import JWTError

from sowonpass_backend.settings import settings


async def verify_jwt(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            token,
            settings.auth_secret,
            algorithms=[settings.auth_algorithm],
        )
    except JWTError:
        return None


async def verify_refresh_jwt(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            token,
            settings.auth_refresh_secret,
            algorithms=[settings.auth_algorithm],
        )
    except JWTError:
        return None
