from fastapi import APIRouter, Depends

from sowonpass_backend.db.dao.process_group_dao import ProcessGroupDAO
from sowonpass_backend.web.api.process_group.schema import ProcessGroupModelInputDTO

router = APIRouter()


@router.put("")
async def put_process_group(
    new_group: ProcessGroupModelInputDTO,
    process_group_dao: ProcessGroupDAO = Depends(),
) -> None:
    await process_group_dao.create_process_group(
        name=new_group.name,
        description=new_group.description,
    )
