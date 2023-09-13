from abc import abstractmethod
from typing import Any, Optional, Sequence, TypeVar, Union

from sqlalchemy import Row, RowMapping, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import UNSET

from src.models.guild import Guild as GuildModel
from src.models.member import Member as MemberModel
from src.models.user import User as UserModel

_RowData = Union[Row, RowMapping, Any]
_R = TypeVar('_R', bound=_RowData)


class Base:
    model: Union[GuildModel, MemberModel, UserModel] = None

    @classmethod
    @abstractmethod
    def _resolve_filter(cls, field: str):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, data: dict) -> model:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update(cls, session: AsyncSession, data: dict) -> model:
        raise NotImplementedError

    @classmethod
    async def get_by_id(cls, session: AsyncSession, obj_id: int) -> Optional[_R]:
        stmt = select(cls.model).where(cls.model.id == obj_id)
        result = (await session.scalars(stmt)).unique().one_or_none()
        return result

    @classmethod
    async def get(cls, session: AsyncSession, filters: dict = None) -> Sequence[_R]:
        stmt = select(cls.model)

        if filters is None:
            filters = {}
        for filter_name, value in filters.items():
            if value == UNSET:
                continue
            stmt = stmt.where(cls._resolve_filter(filter_name)(value))  # noqa
        result = (await session.scalars(stmt)).unique().all()
        return result

    # region TODO: revisit and refactor
    @classmethod
    async def get_or_create(cls, session: AsyncSession, data: dict) -> (model, bool):
        created = False
        if not (db_obj := await cls.get_by_id(session, data['id'])):
            db_obj = await cls.create(session, data)
            created = True
        return db_obj, created

    @classmethod
    async def update_or_create(cls, session: AsyncSession, data: dict) -> model:
        if await cls.get_by_id(session, data['id']):
            db_obj = await cls.update(session, data)
        else:
            db_obj = await cls.create(session, data)
        return db_obj

    # endregion

    @classmethod
    async def delete(cls, session: AsyncSession, obj_id: int) -> None:
        stmt = delete(cls.model).where(cls.model.id == obj_id)
        await session.execute(stmt)
