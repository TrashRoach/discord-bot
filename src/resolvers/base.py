from abc import abstractmethod
from typing import Any, Optional, Protocol, Sequence, TypeVar, Union

from sqlalchemy import Row, RowMapping, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.guild import Guild as GuildModel
from src.models.member import Member as MemberModel
from src.models.user import User as UserModel

_RowData = Union[Row, RowMapping, Any]
_R = TypeVar('_R', bound=_RowData)


class DiscordEntity(Protocol):
    id: int = None


class Base:
    model: Union[GuildModel, MemberModel, UserModel] = None

    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, data: dict) -> model:
        pass

    @classmethod
    @abstractmethod
    async def update(cls, session: AsyncSession, data: dict) -> model:
        pass

    @classmethod
    async def get(cls, session: AsyncSession, obj_id: int) -> Optional[_R]:
        stmt = select(cls.model).filter(cls.model.id == obj_id)
        result = (await session.scalars(stmt)).unique().one_or_none()
        return result

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[_R]:
        stmt = select(cls.model)
        result = (await session.scalars(stmt)).unique().all()
        return result

    @classmethod
    async def get_or_create(cls, session: AsyncSession, data: dict) -> (model, bool):
        created = False
        if not (db_obj := await cls.get(session, data['id'])):
            db_obj = await cls.create(session, data)
            created = True
        return db_obj, created

    @classmethod
    async def update_or_create(cls, session: AsyncSession, data: dict) -> model:
        if await cls.get(session, data['id']):
            db_obj = await cls.update(session, data)
        else:
            db_obj = await cls.create(session, data)
        return db_obj

    @classmethod
    async def delete(cls, session: AsyncSession, obj_id: int) -> None:
        stmt = delete(cls.model).where(cls.model.id == obj_id)
        await session.execute(stmt)
