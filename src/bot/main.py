import asyncio
import logging

import discord
from discord.ext import commands
from dynaconf import settings

logger = logging.getLogger(__name__)


class TestBot(commands.Bot):
    """Test Bot configuration"""

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # noqa
        intents.presences = True  # noqa
        intents.message_content = True  # noqa

        super().__init__(command_prefix=self.get_command_prefix(), intents=intents)
        self.setup_events()

    def setup_events(self):
        @self.event
        async def on_ready():
            await self.tree.sync()
            for guild in self.guilds:
                logger.debug(guild.name)
            logger.info(f'{self.user.name} - Ready!')

        @self.event
        async def on_connect():
            logger.info(f'{self.user.name} - Connected!')

        @self.event
        async def on_disconnect():
            logger.debug(f'{self.user.name} - Disconnected!')

        @self.hybrid_command()
        async def test(ctx):
            await ctx.send("This is a hybrid command!")

    async def start_bot(self, token: str) -> None:
        async with self:
            await self.start(token)

        await self.change_presence(status=discord.Status.invisible)

    @staticmethod
    def get_command_prefix():
        return commands.when_mentioned_or(settings.DISCORD.prefix)


async def main():
    logging.basicConfig(format=settings.LOG_FORMAT, level=settings.LOG_LEVEL)
    bot = TestBot()
    await bot.start_bot(settings.DISCORD.token)


if __name__ == '__main__':
    asyncio.run(main())
