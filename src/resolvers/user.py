from discord import Member as DiscordMember
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User as UserModel
from src.resolvers.base import Base as BaseResolver


class User(BaseResolver):
    model = UserModel

    @classmethod
    async def create(cls, session: AsyncSession, user: DiscordMember) -> UserModel:
        user_obj = cls.model(
            id=user.id,
            name=user.name,
            global_name=user.global_name,
            avatar_url=user.avatar.url if user.avatar else None,
            bot=user.bot,
        )

        session.add(user_obj)
        return user_obj
