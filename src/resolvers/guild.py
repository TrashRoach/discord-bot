from discord import Guild as DiscordGuild
from discord import Member as DiscordMember
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.guild import Guild as GuildModel
from src.resolvers.base import Base as BaseResolver
from src.resolvers.member import Member as MemberResolver
from src.resolvers.user import User as UserResolver


class Guild(BaseResolver):
    model = GuildModel

    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> GuildModel:
        owner_data = data.pop('owner')
        if not owner_data:
            raise ValueError('NO OWNER?')  # TODO: unfuck error messages
        guild_owner, _ = await UserResolver.get_or_create(session, owner_data)

        members = data.pop('members')
        if len(members) < 1:
            raise ValueError('NO GUILD MEMBERS?')  # TODO: unfuck error messages

        guild_obj = cls.model(**data)
        session.add(guild_obj)

        for member in members:  # type: dict
            _ = await UserResolver.get_or_create(session, member)
            _ = await MemberResolver.create(session, member)

        await session.refresh(guild_obj)
        return await cls.get(session, data['id'])

    @classmethod
    async def update(cls, session: AsyncSession, data: dict) -> GuildModel:
        owner_data = data.pop('owner')
        if not owner_data:
            raise ValueError('NO OWNER?')  # TODO: unfuck error messages
        guild_owner, _ = await UserResolver.get_or_create(session, owner_data)

        members = data.pop('members')
        if len(members) < 1:
            raise ValueError('NO GUILD MEMBERS?')  # TODO: unfuck error messages

        guild_id = data.pop('id')
        if not guild_id:
            raise ValueError(f'PK is not present in data')
        stmt = update(cls.model).where(cls.model.id == guild_id).values(**data).returning(cls.model)
        guild_obj = (await session.execute(stmt)).unique().one()[0]

        old_member_ids = set(member.user_id for member in guild_obj.members)
        current_member_ids = set()
        for current_member in members:  # type: dict
            # _ = await UserResolver.update_or_create(session, current_member['user'])  # TODO
            member = await MemberResolver.update_or_create(session, current_member)
            current_member_ids.add(member.user_id)

        ex_member_ids = old_member_ids - current_member_ids
        for ex_member_id in ex_member_ids:
            ex_member_data = {
                'user': {'id': ex_member_id},
                'guild_id': guild_id,
                'active': False,
            }  # TODO: Mother of God WTF
            _ = await MemberResolver.update(session, ex_member_data)
        # TODO: ex_member_ids.active = False

        return await cls.get(session, guild_id)

    @staticmethod
    def discord_object_as_dict(guild: DiscordGuild) -> dict:
        return {
            'id': guild.id,
            'name': guild.name,
            'owner_id': guild.owner_id,
            'owner': UserResolver.discord_object_as_dict(guild.owner),
            'members': [MemberResolver.discord_object_as_dict(member) for member in guild.members],
        }
