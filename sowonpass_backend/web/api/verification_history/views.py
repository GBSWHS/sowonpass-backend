from fastapi import APIRouter, Depends

from sowonpass_backend.authentication import get_current_user
from sowonpass_backend.db.dao.verification_history_dao import VerificationHistoryDAO
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.db.models.verification_history import VerificationHistoryModel
from sowonpass_backend.web.api.verification_history.schema import (
    VerificationHistoryModelDTO,
)

router = APIRouter()


@router.get("/{user_id}/history", response_model=list[VerificationHistoryModelDTO])
async def get_user_history(
    user_id: int,
    verification_history_dao: VerificationHistoryDAO = Depends(),
) -> list[VerificationHistoryModel]:
    return await verification_history_dao.read_user_histories(user_id)


@router.get("/history", response_model=list[VerificationHistoryModelDTO])
async def get_current_user_history(
    user: UserModel = Depends(get_current_user),
    verification_history_dao: VerificationHistoryDAO = Depends(),
) -> list[VerificationHistoryModel]:
    return await verification_history_dao.read_user_histories(user.id)


# TODO 특정 프로세스의 오늘 인증 기록을 조회하는 API
