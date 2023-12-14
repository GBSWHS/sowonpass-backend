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
    gender: Mapped[str] = mapped_column(String(length=1), nullable=True)
    classroom_number: Mapped[int] = mapped_column(nullable=True)
    student_number: Mapped[int] = mapped_column(nullable=True)
    room_number: Mapped[int] = mapped_column(nullable=True)

    processes: Mapped[List["VerificationProcessModel"]] = relationship(
        secondary=process_user,
        back_populates="users",
    )
    assigned_processes: Mapped[List["VerificationProcessModel"]] = relationship(
        secondary=process_assignee,
        back_populates="assignees",
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
