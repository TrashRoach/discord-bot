from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.utils import doc_and_comment
from src.models import Base
from src.models.annotations import bigint_pk

if TYPE_CHECKING:
    from src.models.guild import Guild
    from src.models.member import Member


class User(Base):
    """Discord user"""

    __tablename__ = 'users'
    __table_args__ = (
        {
            'comment': __doc__,
        },
    )

    id: Mapped[bigint_pk] = mapped_column(
        **doc_and_comment('The user\'s unique ID'),
    )
    name: Mapped[str] = mapped_column(
        **doc_and_comment('The user\'s username'),
    )
    global_name: Mapped[Optional[str]] = mapped_column(
        **doc_and_comment('The user\'s global nickname'),
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        default=None,
        repr=False,
        **doc_and_comment('The user\'s avatar url'),
    )
    bot: Mapped[bool] = mapped_column(
        default=False,
        repr=False,
        **doc_and_comment('Specifies if the user is a bot account'),
    )
    owner_of: Mapped[List['Guild']] = relationship(
        back_populates='owner',
        default_factory=list,
        lazy='joined',
        repr=False,
    )
    known_as: Mapped[List['Member']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        default_factory=list,
        lazy='subquery',
        repr=False,
    )

    # TODO: isinstance(model_obj.to_dict()['attribute'], Base), what if List[Base]?
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'global_name': self.global_name,
            'avatar_url': self.avatar_url,
            'bot': self.bot,
            'owner_of': self.owner_of,  # type: List['Guild']
            'known_as': self.known_as,  # type: List['Member']
        }
