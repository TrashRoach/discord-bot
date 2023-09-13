import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


def setup_events(bot: commands.Bot):
    """
    God is dead.
    God remains dead.
    And we have killed him.
    """

    @bot.event
    async def on_ready():
        watching_activity = discord.Activity(type=discord.ActivityType.watching, name="You.")
        await bot.change_presence(activity=watching_activity, status=discord.Status.do_not_disturb)
        logger.info(f'{bot.user.name} - Ready!')

    @bot.event
    async def on_connect():
        logger.info(f'{bot.user.name} - Connected!')

    @bot.event
    async def on_disconnect():
        logger.debug(f'{bot.user.name} - Disconnected!')

    # region TODO: Update events __doc__

    # region members
    @bot.event
    async def on_member_join(member):
        """
        Called when a Member joins a Guild.
        :param member: (Member) – The member who joined.
        """
        ...

    @bot.event
    async def on_member_remove(member):
        """
        Called when a Member leaves a Guild.
        :param member: (Member) – The member who left.
        """
        ...

    @bot.event
    async def on_member_update(before, after):
        """
        Called when a Member updates their profile.
        This is called when one or more of the following things change:
            status
            activity
            nickname
            roles

        :param before: (Member) – The updated member’s old info.
        :param after: (Member) – The updated member’s updated info.
        """

    # endregion

    # region users
    @bot.event
    async def on_user_update(before, after):
        """
        Called when a User updates their profile.
        This is called when one or more of the following things change:
            avatar
            username
            discriminator

        :param before: (User) – The updated user’s old info.
        :param after: (User) – The updated user’s updated info.
        """
        ...

    # endregion

    # region guilds
    @bot.event
    async def on_guild_join(guild):
        """
        Called when a Guild is either created by the Client or when the Client joins a guild.

        :param guild: (Guild) – The guild that was joined.
        """
        ...

    @bot.event
    async def on_guild_remove(guild):
        """
        Called when a Guild is removed from the Client

        :param guild: (Guild) – The guild that got removed.
        """
        ...

    @bot.event
    async def on_guild_role_create(role):
        """
        Called when a Guild creates a new Role.
        This requires Intents.guilds to be enabled.

        :param role: (Role) – The role that was created.
        """
        ...

    @bot.event
    async def on_guild_role_delete(role):
        """
        Called when a Guild deletes a new Role.
        This requires Intents.guilds to be enabled.

        :param role: (Role) – The role that was deleted.
        """
        ...

    @bot.event
    async def on_guild_role_update(before, after):
        """
        Called when a Role is changed guild-wide.
        This requires Intents.guilds to be enabled.

        :param before: (Role) – The updated role’s old info.
        :param after: (Role) – The updated role’s updated info.
        """
        ...

    # endregion

    # endregion
