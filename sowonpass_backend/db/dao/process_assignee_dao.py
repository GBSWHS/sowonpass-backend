from fastapi import Depends
from sqlalchemy import and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.process_assignee import process_assignee


class ProcessAssigneeDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def read_process_assignees(self, process_id: int) -> list[int]:
        stmt = select(process_assignee).where(
            process_assignee.c.verification_process == process_id,
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_process_assignee(self, process_id: int, user_id: int) -> None:
        stmt = insert(process_assignee).values(
            verification_process=process_id,
            user=user_id,
        )
        await self.session.execute(stmt)

    async def delete_process_assignee(self, process_id: int, user_id: int) -> None:
        stmt = delete(process_assignee).where(
            and_(
                process_assignee.c.verification_process == process_id,
                process_assignee.c.user == user_id,
            ),
        )
        await self.session.execute(stmt)
