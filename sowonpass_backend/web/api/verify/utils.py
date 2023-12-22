import pyotp
from fastapi import HTTPException, status

from sowonpass_backend.db.dao.verification_process_dao import VerificationProcessDAO
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.db.models.verification_process import VerificationProcessModel
from sowonpass_backend.web.api.verify.exceptions import VerifyError


async def check_process_and_user(
    process_id: int,
    user_id: int,
    current_user: UserModel,
    verification_process_dao: VerificationProcessDAO,
) -> VerificationProcessModel:
    process = await verification_process_dao.read_process(process_id=process_id)

    if not process:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.id not in {assignee.id for assignee in process.assignees}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current user not an assignee",
        )

    if user_id not in {user.id for user in process.users}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Target user not in process",
        )

    return process


async def verify_totp(user_totp_secret: str | None, otp: str) -> None:
    if not user_totp_secret:
        raise VerifyError("User does not have TOTP secret")
    totp = pyotp.TOTP(user_totp_secret)
    if not totp.verify(otp):
        raise VerifyError("OTP is not valid")
