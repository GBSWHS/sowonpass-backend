from fastapi import APIRouter, Depends

from sowonpass_backend.authentication import get_current_user
from sowonpass_backend.db.dao.user_dao import UserDAO
from sowonpass_backend.db.dao.verification_history_dao import VerificationHistoryDAO
from sowonpass_backend.db.dao.verification_process_dao import VerificationProcessDAO
from sowonpass_backend.db.enum.verify_status import VerifyStatus
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.web.api.verification_history.schema import (
    VerificationHistoryInputDTO,
)
from sowonpass_backend.web.api.verify.exceptions import VerifyError
from sowonpass_backend.web.api.verify.schema import (
    VerifyOTPInputDTO,
    VerifyWithoutOTPInputDTO,
)
from sowonpass_backend.web.api.verify.utils import check_process_and_user, verify_totp

router = APIRouter()


@router.post("")
async def post_process_verify(
    verify_dto: VerifyOTPInputDTO,
    current_user: UserModel = Depends(get_current_user),
    verification_process_dao: VerificationProcessDAO = Depends(),
    history_dao: VerificationHistoryDAO = Depends(),
    user_dao: UserDAO = Depends(),
) -> None:
    process = await check_process_and_user(
        process_id=verify_dto.process_id,
        user_id=verify_dto.user_id,
        current_user=current_user,
        verification_process_dao=verification_process_dao,
    )

    status = VerifyStatus.VERIFIED.value
    message = ""

    try:
        user_totp_secret = await user_dao.read_user_totp_secret(verify_dto.user_id)
        await verify_totp(user_totp_secret, verify_dto.otp)
    except VerifyError as err:
        status = VerifyStatus.FAILED.value
        message = str(err)

    new_history = VerificationHistoryInputDTO(
        user_id=verify_dto.user_id,
        assignee_id=current_user.id,
        process_id=verify_dto.process_id,
        process_group_id=process.process_group_id,
        status=status,
        message=message,
    )
    await history_dao.create_history(new_history)


@router.post("/bypass")
async def post_process_bypass(
    verify_dto: VerifyWithoutOTPInputDTO,
    current_user: UserModel = Depends(get_current_user),
    verification_process_dao: VerificationProcessDAO = Depends(),
    history_dao: VerificationHistoryDAO = Depends(),
) -> None:
    process = await check_process_and_user(
        process_id=verify_dto.process_id,
        user_id=verify_dto.user_id,
        current_user=current_user,
        verification_process_dao=verification_process_dao,
    )

    new_history = VerificationHistoryInputDTO(
        user_id=verify_dto.user_id,
        assignee_id=current_user.id,
        process_id=verify_dto.process_id,
        process_group_id=process.process_group_id,
        status=VerifyStatus.BYPASSED.value,
        message="",
    )
    await history_dao.create_history(new_history)
