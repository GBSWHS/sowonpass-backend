from fastapi import Depends
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.process_user import process_user
from sowonpass_backend.db.models.verification_process import VerificationProcessModel


class VerificationProcessDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_process(
        self,
        name: str,
        description: str,
    ) -> None:
        stmt = insert(VerificationProcessModel).values(
            name=name,
            description=description,
        )
        await self.session.execute(stmt)

    async def read_process(self, process_id: int) -> VerificationProcessModel | None:
        stmt = select(VerificationProcessModel).where(
            VerificationProcessModel.id == process_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_process(self, process_id: int) -> None:
        stmt = delete(VerificationProcessModel).where(
            VerificationProcessModel.id == process_id,
        )
        await self.session.execute(stmt)

    async def add_user_to_process(self, user_id: int, process_id: int) -> None:
        stmt = insert(process_user).values(
            verification_process=process_id,
            user=user_id,
        )
        await self.session.execute(stmt)
