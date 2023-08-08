from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Base model class"""

    pass


#  alembic imports
from src.models import guild, user  # noqa: E402
