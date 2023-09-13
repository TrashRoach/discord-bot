from discord import Member as DiscordMember
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User as UserModel
from src.resolvers.base import Base as BaseResolver


class User(BaseResolver):
    model = UserModel

    @classmethod
    def _resolve_filter(cls, field: str):
        filter_map = {
            'ids': cls.model.id.in_,
            'names': cls.model.name.in_,
            'global_names': cls.model.global_name.in_,
        }
        return filter_map[field]

    # region TODO: revisit and refactor
    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> UserModel:
        user_obj = cls.model(**data)

        session.add(user_obj)
        return user_obj

    @classmethod
    async def update(cls, session: AsyncSession, data: dict) -> UserModel:
        user_id = data.pop('id')
        if not user_id:
            raise ValueError(f'PK is not present in data')
        stmt = update(cls.model).where(cls.model.id == user_id).values(**data).returning(cls.model)
        user_obj = (await session.execute(stmt)).unique().one()
        return user_obj

    @staticmethod
    def from_discord(user: DiscordMember) -> dict:
        return {
            'id': user.id,
            'name': user.name,
            'global_name': user.global_name,
            'avatar_url': user.avatar.url if user.avatar else None,
            'bot': user.bot,
        }

    # endregion
