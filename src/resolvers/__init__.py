from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class Base:
    model = None

    @classmethod
    async def get(cls, session: AsyncSession, obj_id: int):
        stmt = select(cls.model).filter(cls.model.id == obj_id)
        result = (await session.scalars(stmt)).one_or_none()
        return result

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        stmt = insert(cls.model).values(**kwargs).returning(cls.model)
        result = (await session.scalars(stmt)).one()
        return result

    @classmethod
    async def update(cls, session: AsyncSession, obj_id: int, **kwargs):
        if kwargs:
            stmt = update(cls.model).where(cls.model.id == obj_id).values(**kwargs).returning(cls.model)
            result = (await session.scalars(stmt)).one()
            return result

    @classmethod
    async def delete(cls, session: AsyncSession, obj_id: int):
        stmt = delete(cls.model).where(cls.model.id == obj_id)
        await session.execute(stmt)
