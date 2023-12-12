from fastapi import APIRouter, Depends, HTTPException, status

from sowonpass_backend.db.dao.verification_process_dao import VerificationProcessDAO
from sowonpass_backend.db.models.verification_process import VerificationProcessModel
from sowonpass_backend.web.api.verification_process.schema import (
    VerificationProcessModelDTO,
    VerificationProcessModelInputDTO,
)

router = APIRouter()


@router.get("/{process_id}", response_model=VerificationProcessModelDTO)
async def get_process(
    process_id: int,
    verification_process_dao: VerificationProcessDAO = Depends(),
) -> VerificationProcessModel:
    process = await verification_process_dao.read_process(process_id=process_id)
    if not process:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return process


@router.put("")
async def add_process(
    new_process: VerificationProcessModelInputDTO,
    verification_process_dao: VerificationProcessDAO = Depends(),
) -> None:
    await verification_process_dao.create_process(
        name=new_process.name,
        description=new_process.description,
    )


@router.delete("/{process_id}")
async def delete_process(
    process_id: int,
    verification_process_dao: VerificationProcessDAO = Depends(),
) -> None:
    await verification_process_dao.delete_process(process_id=process_id)
