from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, String

from sowonpass_backend.db.base import Base
from sowonpass_backend.db.models.process_assignee import process_assignee
from sowonpass_backend.db.models.process_user import process_user
from sowonpass_backend.db.models.user import UserModel


class VerificationProcessModel(Base):
    """Verification Process Model."""

    __tablename__ = "verification_process"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    description: Mapped[str] = mapped_column(String(length=100), nullable=False)
    process_group_id: Mapped[int] = mapped_column(
        ForeignKey("process_group.id"),
        nullable=True,
    )

    users: Mapped[List["UserModel"]] = relationship(
        secondary=process_user,
        back_populates="processes",
    )
    assignees: Mapped[List["UserModel"]] = relationship(
        secondary=process_assignee,
        back_populates="assigned_processes",
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
