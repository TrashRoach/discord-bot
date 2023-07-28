from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    pass


#  alembic imports
from src.models import guild, user  # noqa: E402
