from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.utils import doc_and_comment
from src.models import Base
from src.models.annotations import bigint_pk
from src.models.guild import Guild
from src.models.user import User


class Member(Base):
    """Discord guild member"""

    __tablename__ = 'members'
    __table_args__ = (
        {
            'comment': __doc__,
        },
    )

    guild_id: Mapped[bigint_pk] = mapped_column(
        ForeignKey('guilds.id', ondelete='CASCADE'),
        init=False,
        repr=False,
        **doc_and_comment(Guild.id.__doc__),
    )
    user_id: Mapped[bigint_pk] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        init=False,
        repr=False,
        **doc_and_comment(User.id.__doc__),
    )
    display_name: Mapped[Optional[str]] = mapped_column(
        **doc_and_comment('Discord guild member\'s name'),
    )
    guild: Mapped['Guild'] = relationship(
        back_populates='members',
        lazy='joined',
        innerjoin=True,
        init=False,
    )
    user: Mapped['User'] = relationship(
        back_populates='known_as',
        lazy='joined',
        innerjoin=True,
        init=False,
    )

    active: Mapped[bool] = mapped_column(
        default=True,
        repr=False,
        **doc_and_comment('Currently in guild'),
    )

    def to_dict(self):
        return {
            'guild_id': self.guild_id,
            'user_id': self.user_id,
            'display_name': self.display_name,
            'guild': self.guild,
            'user': self.user,
            'active': self.active,
        }
