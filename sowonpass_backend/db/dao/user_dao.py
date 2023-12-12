from fastapi import Depends
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.user import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(self, name: str, phone_number: str, role: int) -> None:
        stmt = insert(UserModel).values(
            name=name,
            phone_number=phone_number,
            role=role,
        )
        await self.session.execute(stmt)

    async def read_user(self, user_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(stmt)
