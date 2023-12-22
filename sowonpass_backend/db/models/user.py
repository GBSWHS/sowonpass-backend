from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, String

from sowonpass_backend.db.base import Base
from sowonpass_backend.db.models.process_assignee import process_assignee
from sowonpass_backend.db.models.process_user import process_user

if TYPE_CHECKING:
    from sowonpass_backend.db.models.verification_process import (
        VerificationProcessModel,
    )


class UserModel(Base):
    """User model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(length=100), nullable=False)
    totp_secret: Mapped[str] = mapped_column(String(length=100), nullable=True)

    processes: Mapped[List["VerificationProcessModel"]] = relationship(
        secondary=process_user,
        back_populates="users",
        passive_deletes=True,
    )
    assigned_processes: Mapped[List["VerificationProcessModel"]] = relationship(
        secondary=process_assignee,
        back_populates="assignees",
        passive_deletes=True,
    )

    time_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    time_updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )
