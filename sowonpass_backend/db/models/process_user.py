from sqlalchemy import Column, ForeignKey, Table

from sowonpass_backend.db.base import Base

process_user = Table(
    "process_user",
    Base.metadata,
    Column(
        "verification_process",
        ForeignKey("verification_process.id"),
        primary_key=True,
    ),
    Column("user", ForeignKey("user.id"), primary_key=True),
)
