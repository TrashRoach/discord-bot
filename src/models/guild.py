from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.utils import doc_and_comment
from src.models import Base
from src.models.annotations import bigint_pk

if TYPE_CHECKING:
    from src.models.member import Member
    from src.models.user import User


class Guild(Base):
    """Discord guild"""

    __tablename__ = 'guilds'
    __table_args__ = (
        {
            'comment': __doc__,
        },
    )

    id: Mapped[bigint_pk] = mapped_column(
        **doc_and_comment('The guild\'s unique ID'),
    )
    name: Mapped[str] = mapped_column(
        **doc_and_comment('The guild\'s name'),
    )
    owner_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id', ondelete='CASCADE'),
        repr=False,
    )
    owner: Mapped['User'] = relationship(
        back_populates='owner_of',
        lazy='subquery',
        init=False,
    )
    members: Mapped[List['Member']] = relationship(
        back_populates='guild',
        cascade='all, delete-orphan',
        default_factory=list,
        lazy='subquery',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'owner': self.owner,
            'members': self.members,  # type: List['Member']
        }
