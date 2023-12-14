from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, String

from sowonpass_backend.db.base import Base

if TYPE_CHECKING:
    from sowonpass_backend.db.models.verification_process import (
        VerificationProcessModel,
    )


class ProcessGroupModel(Base):
    """Verification Process Group Model."""

    __tablename__ = "process_group"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    description: Mapped[str] = mapped_column(String(length=100), nullable=False)

    processes: Mapped[List["VerificationProcessModel"]] = relationship()

    time_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    time_updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )
