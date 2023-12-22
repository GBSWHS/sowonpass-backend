from pydantic import BaseModel


class VerifyOTPInputDTO(BaseModel):
    process_id: int
    user_id: int
    otp: str


class VerifyWithoutOTPInputDTO(BaseModel):
    process_id: int
    user_id: int
    otp: str
