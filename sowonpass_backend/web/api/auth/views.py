import pyotp
from fastapi import APIRouter, Depends, HTTPException, status

from sowonpass_backend.authentication import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)
from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.web.api.auth.schema import (
    RefreshTokenDTO,
    TokenDTO,
    UserLoginInputDTO,
)
from sowonpass_backend.web.api.auth.utils import verify_refresh_jwt

router = APIRouter()


@router.post("", response_model=TokenDTO)
async def user_login(
    data: UserLoginInputDTO,
    user_dao: UserDAO = Depends(),
) -> dict[str, str]:
    user = await authenticate_user(
        name=data.name,
        phone_number=data.phone_number,
        user_dao=user_dao,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 정보가 일치하지 않습니다.",
        )

    totp_secret = pyotp.random_base32()
    await user_dao.update_user_totp_secret(user_id=user.id, totp_secret=totp_secret)

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "totp_secret": totp_secret,
    }


@router.post("/refresh", response_model=TokenDTO)
async def refresh(
    data: RefreshTokenDTO,
    user_dao: UserDAO = Depends(),
) -> dict[str, str]:
    payload = await verify_refresh_jwt(data.refresh_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: int = payload["id"]
    user = await user_dao.read_user(int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    totp_secret = pyotp.random_base32()
    await user_dao.update_user_totp_secret(user_id=user.id, totp_secret=totp_secret)

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "totp_secret": totp_secret,
    }
