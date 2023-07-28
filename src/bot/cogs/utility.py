import random
from typing import Optional

from discord.ext import commands

from src.bot.cogs._base import BaseCog


class Utility(BaseCog):
    """Utility commands"""

    @commands.hybrid_group(name='random')
    async def _random(self, ctx):
        """Command group for random choices"""
        ...

    @_random.command()
    async def roll(self, ctx: commands.Context, start: Optional[int] = 1, end: Optional[int] = 100) -> None:
        """Roll a number in range provided (1-100 by default)"""

        if start > end:
            start, end = end, start
        number = str(random.randint(start, end))
        await ctx.send(number)

    @_random.command()
    # *args are not supported in hybrid (slash) commands for now
    async def choice(
        self,
        ctx: commands.Context,
        option_1: Optional[str] = None,
        option_2: Optional[str] = None,
        option_3: Optional[str] = None,
    ) -> None:
        """Choose one of the options provided (Yes, No and Maybe by default)"""

        default_choices = ('Yes', 'No', 'Maybe')
        args = {option_1, option_2, option_3}
        choices = [choice for choice in args if choice] or default_choices

        choice = random.choice(choices)
        await ctx.send(choice)

    @_random.command()
    async def coinflip(self, ctx: commands.Context) -> None:
        """Toss a coin"""

        cmd = self.bot.get_command('random choice')
        await cmd(ctx, option_1='Heads', option_2='Tails')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))
