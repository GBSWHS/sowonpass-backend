import pyotp
from fastapi import APIRouter, Depends, HTTPException, status

from sowonpass_backend.authentication import auth_or_create, create_token
from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.settings import settings
from sowonpass_backend.web.api.auth.schema import TokenDTO
from sowonpass_backend.web.api.auth.utils import (
    get_sso_public_key,
    verify_jwt,
    verify_sso_jwt,
)

router = APIRouter()


@router.get("/callback", response_model=TokenDTO)
async def callback(id_token: str, user_dao: UserDAO = Depends()) -> dict[str, str]:
    public_key = await get_sso_public_key(settings.public_key_url)

    payload = await verify_sso_jwt(id_token, public_key, aud=settings.client_id)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await auth_or_create(
        name=payload["data"]["fullname"],
        phone_number=payload["data"]["phone"],
        user_type=payload["data"]["type"],
        user_dao=user_dao,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate or create user",
        )

    totp_secret = pyotp.random_base32()
    await user_dao.update_user_totp_secret(user_id=user.id, totp_secret=totp_secret)

    return {
        "access_token": create_token(user.id),
        "refresh_token": create_token(user.id, is_refresh=True),
        "totp_secret": totp_secret,
    }


@router.get("/refresh", response_model=TokenDTO)
async def refresh(refresh_token: str, user_dao: UserDAO = Depends()) -> dict[str, str]:
    payload = await verify_jwt(refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: str = payload["id"]
    if not user_id.isdigit():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await user_dao.read_user(int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    new_access_token = create_token(user.id)
    new_refresh_token = create_token(user.id, is_refresh=True)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "totp_secret": "",
    }
