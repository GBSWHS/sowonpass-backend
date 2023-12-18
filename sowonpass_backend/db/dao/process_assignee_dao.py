from fastapi import Depends
from sqlalchemy import and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.process_assignee import process_assignee
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.db.models.verification_process import VerificationProcessModel


class ProcessAssigneeDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_process_assignee(self, process_id: int, user_id: int) -> None:
        stmt = insert(process_assignee).values(
            verification_process=process_id,
            user=user_id,
        )
        await self.session.execute(stmt)

    async def read_process_assignees(self, process_id: int) -> list[UserModel]:
        stmt = select(VerificationProcessModel).where(
            VerificationProcessModel.id == process_id,
        )
        result = await self.session.execute(stmt)
        process = result.scalars().first()
        if not process:
            return []
        return list(process.assignees)

    async def delete_process_assignee(self, process_id: int, user_id: int) -> None:
        stmt = delete(process_assignee).where(
            and_(
                process_assignee.c.verification_process == process_id,
                process_assignee.c.user == user_id,
            ),
        )
        await self.session.execute(stmt)
