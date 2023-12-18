from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.enum.user_enum import UserRole
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/swagger")


class BearAuthError(Exception):
    pass  # noqa: WPS420, WPS604


def create_token(user_id: int, is_refresh: bool = False) -> str:
    if is_refresh:
        hours = settings.auth_refresh_expire_hours
        data = f"{user_id}.refresh"
    else:
        hours = settings.auth_expire_hours
        data = str(user_id)

    expire = datetime.utcnow() + timedelta(hours=hours)
    payload = {
        "id": data,
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload,
        settings.auth_secret,
        algorithm=settings.auth_algorithm,
    )


def get_token_payload(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.auth_secret,
            algorithms=[settings.auth_algorithm],
        )
        payload_sub: str = payload["id"]

        if payload_sub is None:
            raise BearAuthError("Token could not be validated")
        return payload_sub
    except JWTError:
        raise BearAuthError("Token could not be validated")


async def auth_or_create(
    name: str,
    phone_number: str,
    user_type: int,
    user_dao: UserDAO,
) -> UserModel | None:
    user = await user_dao.read_user_by_info(name, phone_number)

    if user:
        return user

    if user_type == 2:
        user_id = await user_dao.create_user(name, phone_number, UserRole.ADMIN.value)
        user = await user_dao.read_user(user_id)
    else:
        user_id = await user_dao.create_user(name, phone_number, UserRole.USER.value)
        user = await user_dao.read_user(user_id)
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> UserModel:
    try:
        user_id = get_token_payload(token)
    except BearAuthError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_dao = UserDAO(db)
    user = await user_dao.read_user(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized, could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
