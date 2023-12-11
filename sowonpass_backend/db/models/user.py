from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, String

from sowonpass_backend.db.base import Base


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

    time_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    time_updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )
