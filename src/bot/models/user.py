from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bot.models.annotations import bigint_pk
from src.db.base import Base
from src.db.utils import doc_and_comment


class User(Base):
    """Discord user"""

    __tablename__ = 'users'
    __table_args__ = {
        'comment': __doc__,
    }

    id: Mapped[bigint_pk] = mapped_column(**doc_and_comment('Unique Discord ID'))
    name: Mapped[str] = mapped_column(**doc_and_comment('User name'))
    avatar_url: Mapped[Optional[str]] = mapped_column(default=None, **doc_and_comment('User avatar url'))
    is_bot: Mapped[bool] = mapped_column(default=False, **doc_and_comment('Is bot'))
    owner_of: Mapped[List['Guild']] = relationship(back_populates='owner', default_factory=list)
