from pydantic import BaseModel


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str
    totp_secret: str


class UserLoginInputDTO(BaseModel):
    name: str
    phone_number: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str
