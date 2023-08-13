from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Base model class"""

    __allow_unmapped__ = True


#  alembic imports
from src.models import guild, member, user  # noqa: E402
