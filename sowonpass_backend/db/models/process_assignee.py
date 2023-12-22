from sqlalchemy import Column, ForeignKey, Table

from sowonpass_backend.db.base import Base

process_assignee = Table(
    "process_assignee",
    Base.metadata,
    Column(
        "verification_process",
        ForeignKey("verification_process.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user",
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
