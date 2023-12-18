from fastapi import APIRouter, Depends, HTTPException, status

from sowonpass_backend.db.dao.process_assignee_dao import ProcessAssigneeDAO
from sowonpass_backend.db.dao.process_user_dao import ProcessUserDAO
from sowonpass_backend.db.dao.verification_process_dao import VerificationProcessDAO
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.db.models.verification_process import VerificationProcessModel
from sowonpass_backend.web.api.user.schema import UserModelDTO
from sowonpass_backend.web.api.verification_process.schema import (
    VerificationProcessModelDTO,
    VerificationProcessModelInputDTO,
)

router = APIRouter()


@router.put("")
async def put_process(
    new_process: VerificationProcessModelInputDTO,
    verification_process_dao: VerificationProcessDAO = Depends(),
) -> None:
    await verification_process_dao.create_process(
        name=new_process.name,
        description=new_process.description,
    )


@router.get("/{process_id}", response_model=VerificationProcessModelDTO)
async def get_process(
    process_id: int,
    verification_process_dao: VerificationProcessDAO = Depends(),
) -> VerificationProcessModel:
    process = await verification_process_dao.read_process(process_id=process_id)
    if not process:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return process


@router.delete("/{process_id}")
async def delete_process(
    process_id: int,
    verification_process_dao: VerificationProcessDAO = Depends(),
) -> None:
    await verification_process_dao.delete_process(process_id=process_id)


@router.put("/{process_id}/user/{user_id}")
async def put_process_user(
    process_id: int,
    user_id: int,
    process_user_dao: ProcessUserDAO = Depends(),
) -> None:
    await process_user_dao.create_process_user(
        user_id=user_id,
        process_id=process_id,
    )


@router.get("/{process_id}/user", response_model=list[UserModelDTO])
async def get_process_users(
    process_id: int,
    process_user_dao: ProcessUserDAO = Depends(),
) -> list[UserModel]:
    return await process_user_dao.read_process_users(process_id=process_id)


@router.delete("/{process_id}/user/{user_id}")
async def delete_process_user(
    process_id: int,
    user_id: int,
    process_user_dao: ProcessUserDAO = Depends(),
) -> None:
    await process_user_dao.delete_process_user(
        user_id=user_id,
        process_id=process_id,
    )


@router.put("/{process_id}/assignee/{user_id}")
async def put_process_assignee(
    process_id: int,
    user_id: int,
    process_assignee_dao: ProcessAssigneeDAO = Depends(),
) -> None:
    await process_assignee_dao.create_process_assignee(
        user_id=user_id,
        process_id=process_id,
    )


@router.get("/{process_id}/assignee", response_model=list[UserModelDTO])
async def get_process_assignees(
    process_id: int,
    process_assignee_dao: ProcessAssigneeDAO = Depends(),
) -> list[UserModel]:
    return await process_assignee_dao.read_process_assignees(process_id=process_id)


@router.delete("/{process_id}/assignee/{user_id}")
async def delete_process_assignee(
    process_id: int,
    user_id: int,
    process_assignee_dao: ProcessAssigneeDAO = Depends(),
) -> None:
    await process_assignee_dao.delete_process_assignee(
        user_id=user_id,
        process_id=process_id,
    )
