from typing import Union

from discord import Guild as DiscordGuild
from discord import Member as DiscordMember
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.guild import Guild as GuildModel
from src.models.member import Member as MemberModel
from src.resolvers.base import Base as BaseResolver


class Member(BaseResolver):
    model = MemberModel

    @classmethod
    async def create(
        cls, session: AsyncSession, member: DiscordMember, guild: Union[DiscordGuild, GuildModel]
    ) -> MemberModel:
        member_obj = cls.model(display_name=member.display_name)
        member_obj.user_id = member.id
        member_obj.guild_id = guild.id

        session.add(member_obj)
        return member_obj
