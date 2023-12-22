from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy import Select, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from sowonpass_backend.db.dependencies import get_db_session
from sowonpass_backend.db.models.verification_history import VerificationHistoryModel

if TYPE_CHECKING:
    from sowonpass_backend.web.api.verification_history.schema import (
        VerificationHistoryInputDTO,
    )


def apply_joined_loads(
    stmt: Select[tuple[VerificationHistoryModel]],
) -> Select[tuple[VerificationHistoryModel]]:
    stmt = stmt.options(joinedload(VerificationHistoryModel.user))
    stmt = stmt.options(joinedload(VerificationHistoryModel.assignee))
    stmt = stmt.options(joinedload(VerificationHistoryModel.process))
    return stmt.options(joinedload(VerificationHistoryModel.process_group))


class VerificationHistoryDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_history(self, history_dto: "VerificationHistoryInputDTO") -> int:
        stmt = insert(VerificationHistoryModel).values(
            user=history_dto.user_id,
            assignee=history_dto.assignee_id,
            process=history_dto.process_id,
            process_group=history_dto.process_group_id,
            status=history_dto.status,
            message=history_dto.message,
        )
        result = await self.session.execute(stmt)
        return result.lastrowid

    async def read_process_histories(
        self,
        process_id: int,
    ) -> list[VerificationHistoryModel]:
        stmt = select(VerificationHistoryModel).where(
            VerificationHistoryModel.process == process_id,
        )
        stmt = apply_joined_loads(stmt)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def read_process_group_histories(
        self,
        process_group_id: int,
    ) -> list[VerificationHistoryModel]:
        stmt = select(VerificationHistoryModel).where(
            VerificationHistoryModel.process_group == process_group_id,
        )
        stmt = apply_joined_loads(stmt)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def read_user_histories(
        self,
        user_id: int,
    ) -> list[VerificationHistoryModel]:
        stmt = select(VerificationHistoryModel).where(
            VerificationHistoryModel.user == user_id,
        )
        stmt = apply_joined_loads(stmt)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def read_assignee_histories(
        self,
        assignee_id: int,
    ) -> list[VerificationHistoryModel]:
        stmt = select(VerificationHistoryModel).where(
            VerificationHistoryModel.assignee == assignee_id,
        )
        stmt = apply_joined_loads(stmt)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
