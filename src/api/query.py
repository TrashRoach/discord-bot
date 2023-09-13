from typing import Optional

import strawberry
from strawberry.types import Info

from src.api.connection import Connection, to_connection
from src.api.definitions.guild import GuildNode
from src.api.definitions.member import MemberNode
from src.api.definitions.user import UserNode
from src.api.filters import GuildFilter, MemberFilter, UserFilter
from src.bot.main import DiscordBot
from src.resolvers.guild import Guild as GuildResolver
from src.resolvers.member import Member as MemberResolver
from src.resolvers.user import User as UserResolver


# region TODO: remove after testing
async def test_send_discord_message(bot: DiscordBot):
    if bot.is_ready():
        owner_id = bot.owner_id or (await bot.application_info()).owner.id
        user = bot.get_user(owner_id)
        await user.send('test :)')


# endregion


@strawberry.type
class Query:
    @strawberry.field
    async def users(
        self,
        info: Info,
        filters: Optional[UserFilter] = None,
    ) -> Connection[UserNode]:
        # region TODO: remove after testing
        info.context['background_tasks'].add_task(test_send_discord_message, info.context['discord_bot'])
        # endregion

        if filters:
            filters = strawberry.asdict(filters)
        async with info.context['session'] as session:
            users = await UserResolver.get(session, strawberry.asdict(filters))
            return to_connection(node_type=UserNode, relationship_field=users)

    @strawberry.field
    async def guilds(
        self,
        info: Info,
        filters: Optional[GuildFilter] = None,
    ) -> Connection[GuildNode]:
        if filters:
            filters = strawberry.asdict(filters)
        async with info.context['session'] as session:
            guilds = await GuildResolver.get(session, strawberry.asdict(filters))
            return to_connection(node_type=GuildNode, relationship_field=guilds)

    @strawberry.field
    async def members(
        self,
        info: Info,
        filters: Optional[MemberFilter] = None,
    ) -> Connection[MemberNode]:
        if filters:
            filters = strawberry.asdict(filters)
        async with info.context['session'] as session:
            members = await MemberResolver.get(session, filters)
            return to_connection(node_type=MemberNode, relationship_field=members)
