from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from sowonpass_backend.db.base import Base


class VerificationHistoryModel(Base):
    """Verification History Model."""

    __tablename__ = "verification_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    assignee: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    process: Mapped[int] = mapped_column(
        ForeignKey("verification_process.id"),
        nullable=False,
    )
    process_group: Mapped[int] = mapped_column(
        ForeignKey("process_group.id"),
        nullable=False,
    )
    status: Mapped[int] = mapped_column(nullable=False, default=0)
    message: Mapped[str] = mapped_column(String(length=100), nullable=False, default="")
    time_stamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
