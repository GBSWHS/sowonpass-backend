from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from sowonpass_backend.db.base import Base


class ProcessAssigneeModel(Base):
    """Assignee of a verification process."""

    __tablename__ = "process_assignee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    process_id: Mapped[int] = mapped_column(
        ForeignKey("verification_process.id"),
        nullable=False,
    )
