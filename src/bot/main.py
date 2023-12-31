import asyncio
import logging

import discord
from discord.ext import commands

from settings.config import config
from src.bot import cogs
from src.bot.events import setup_events

logger = logging.getLogger('bot')


class DiscordBot(commands.Bot):
    """Discord Bot configuration"""

    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix=self.get_command_prefix(), intents=intents)
        setup_events(self)

    async def setup_hook(self) -> None:
        results = await asyncio.gather(
            *(self.load_extension(ext) for ext in cogs.ALL_EXTENSIONS),
            return_exceptions=True,
        )
        failures = {}
        for ext, result in zip(cogs.ALL_EXTENSIONS, results):
            if isinstance(result, Exception):
                # TODO: send as Discord message too
                failures[ext] = result.__cause__ or result
        if failures:
            logger.critical(
                f'{len(failures)}/{len(results)} extensions failed to load.\n{failures}',
                # extra={'fields': failures},
            )

    async def start_bot(self, token: str) -> None:
        async with self:
            await self.start(token)

        await self.change_presence(status=discord.Status.invisible)

    @staticmethod
    def get_command_prefix():
        prefix = config.DISCORD_BOT_PREFIX
        if prefix:
            return commands.when_mentioned_or(prefix)
        return commands.when_mentioned


bot = DiscordBot()


# TODO: remove maybe?
# async def main():
#     from src.db.engine import sessionmanager
#
#     logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
#     sessionmanager.init()
#     await bot.start_bot(config.DISCORD_BOT_TOKEN)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
