from sqlalchemy.orm import DeclarativeBase

from sowonpass_backend.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
