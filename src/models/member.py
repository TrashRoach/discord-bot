from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.utils import doc_and_comment
from src.models import Base
from src.models.annotations import bigint_pk
from src.models.guild import Guild as GuildModel
from src.models.user import User as UserModel


class Member(Base):
    """Discord guild member"""

    __tablename__ = 'members'
    __table_args__ = (
        {
            'comment': __doc__,
        },
    )

    guild_id: Mapped[bigint_pk] = mapped_column(
        ForeignKey('guilds.id', ondelete='CASCADE'), **doc_and_comment(GuildModel.id.__doc__), init=False, repr=False
    )
    user_id: Mapped[bigint_pk] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), **doc_and_comment(UserModel.id.__doc__), init=False, repr=False
    )
    display_name: Mapped[Optional[str]] = mapped_column(**doc_and_comment('Discord guild member\'s name'))
    guild: Mapped['GuildModel'] = relationship(back_populates='members', lazy='joined', init=False)
    user: Mapped['UserModel'] = relationship(back_populates='known_as', lazy='joined', init=False)

    active: Mapped[bool] = mapped_column(default=True, **doc_and_comment('Currently in guild'), repr=False)
