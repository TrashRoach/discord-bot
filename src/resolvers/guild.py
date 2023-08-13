from discord import Guild as DiscordGuild
from discord import Member as DiscordMember
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.guild import Guild as GuildModel
from src.resolvers.base import Base as BaseResolver
from src.resolvers.member import Member as MemberResolver
from src.resolvers.user import User as UserResolver


class Guild(BaseResolver):
    model = GuildModel

    @classmethod
    async def create(cls, session: AsyncSession, guild: DiscordGuild) -> GuildModel:
        guild_owner, _ = await UserResolver.get_or_create(session, guild.owner)
        guild_obj = cls.model(id=guild.id, name=guild.name, owner_id=guild_owner.id)
        session.add(guild_obj)

        for member in guild.members:  # type: DiscordMember
            _ = await UserResolver.get_or_create(session, member)
            _ = await MemberResolver.create(session, member, guild)

        await session.refresh(guild_obj)
        return await cls.get(session, guild.id)

    @classmethod
    async def update(cls, session: AsyncSession, guild: DiscordGuild, db_guild: model = None) -> GuildModel:
        raise NotImplementedError
