from discord.ext import commands

from src.bot.cogs._base import BaseCog
from src.db.engine import sessionmanager
from src.resolvers.guild import Guild as GuildResolver


class Test(BaseCog, command_attrs=dict(hidden=True)):
    """
    Do you think God stays in heaven
    because he too lives in fear of what he's created?
    """

    @commands.is_owner()
    @commands.hybrid_command()
    async def test(self, ctx: commands.Context):
        await ctx.message.delete()
        async with sessionmanager.session() as session:
            guild = await GuildResolver.update_or_create(session, GuildResolver.discord_object_as_dict(ctx.guild))
        self.logger.info(f'Created/Updated guild: {guild}')
        await ctx.send("This is a hybrid command!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Test(bot))
