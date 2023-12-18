from fastapi import Depends
from sqlalchemy import and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.process_user import process_user
from sowonpass_backend.db.models.user import UserModel
from sowonpass_backend.db.models.verification_process import VerificationProcessModel


class ProcessUserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_process_user(self, process_id: int, user_id: int) -> None:
        stmt = insert(process_user).values(
            verification_process=process_id,
            user=user_id,
        )
        await self.session.execute(stmt)

    async def read_process_users(self, process_id: int) -> list[UserModel]:
        stmt = select(VerificationProcessModel).where(
            VerificationProcessModel.id == process_id,
        )
        result = await self.session.execute(stmt)
        process = result.scalars().first()
        if not process:
            return []
        return list(process.users)

    async def delete_process_user(self, process_id: int, user_id: int) -> None:
        stmt = delete(process_user).where(
            and_(
                process_user.c.verification_process == process_id,
                process_user.c.user == user_id,
            ),
        )
        await self.session.execute(stmt)
