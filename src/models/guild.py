from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.utils import doc_and_comment
from src.models import Base
from src.models.annotations import bigint_pk


class Guild(Base):
    """Discord guild"""

    __tablename__ = 'guilds'
    __table_args__ = {
        'comment': __doc__,
    }

    id: Mapped[bigint_pk] = mapped_column(**doc_and_comment('Unique Discord ID'))
    name: Mapped[str] = mapped_column(**doc_and_comment('Guild name'))
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped['User'] = relationship('User', back_populates='owner_of')