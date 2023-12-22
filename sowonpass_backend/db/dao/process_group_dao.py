from fastapi import Depends
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.process_group import ProcessGroupModel


class ProcessGroupDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_process_group(
        self,
        name: str,
        description: str,
    ) -> int:
        stmt = insert(ProcessGroupModel).values(
            name=name,
            description=description,
        )
        result = await self.session.execute(stmt)
        return result.lastrowid

    async def read_process_group(self, group_id: int) -> ProcessGroupModel | None:
        stmt = select(ProcessGroupModel).where(
            ProcessGroupModel.id == group_id,
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def read_all_process_groups(self) -> list[ProcessGroupModel]:
        stmt = select(ProcessGroupModel)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_process_group(self, process_id: int) -> None:
        stmt = delete(ProcessGroupModel).where(
            ProcessGroupModel.id == process_id,
        )
        await self.session.execute(stmt)
