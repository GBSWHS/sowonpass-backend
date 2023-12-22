from fastapi import Depends
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.user import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(self, name: str, phone_number: str, role: int) -> int:
        stmt = insert(UserModel).values(
            name=name,
            phone_number=phone_number,
            role=role,
        )
        result = await self.session.execute(stmt)
        return result.lastrowid

    async def read_user_by_info(self, name: str, phone_number: str) -> UserModel | None:
        stmt = select(UserModel).where(
            and_(
                UserModel.name == name,
                UserModel.phone_number == phone_number,
            ),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def read_user(self, user_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def read_all_users(self) -> list[UserModel]:
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def read_user_totp_secret(self, user_id: int) -> str | None:
        stmt = select(UserModel.totp_secret).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user_totp_secret(self, user_id: int, totp_secret: str) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(totp_secret=totp_secret)
        )
        await self.session.execute(stmt)

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(stmt)
