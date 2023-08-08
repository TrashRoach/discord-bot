from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.utils import doc_and_comment
from src.models import Base
from src.models.annotations import bigint_pk


class User(Base):
    """Discord user"""

    __tablename__ = 'users'
    __table_args__ = {
        'comment': __doc__,
    }

    id: Mapped[bigint_pk] = mapped_column(**doc_and_comment('The user\'s unique ID.'))
    name: Mapped[str] = mapped_column(**doc_and_comment('The user\'s username.'))
    global_name: Mapped[Optional[str]] = mapped_column(**doc_and_comment('The user\'s global nickname.'))
    avatar_url: Mapped[Optional[str]] = mapped_column(default=None, **doc_and_comment('User avatar url'))
    bot: Mapped[bool] = mapped_column(default=False, **doc_and_comment('Specifies if the user is a bot account.'))
    owner_of: Mapped[List['Guild']] = relationship(back_populates='owner', default_factory=list)
