import logging
from asyncio import get_event_loop

import strawberry
from fastapi import Depends, FastAPI
from fastapi_lifespan_manager import LifespanManager
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from settings.config import config
from src.api.query import Query
from src.bot.main import bot
from src.db.engine import sessionmanager

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)

schema = strawberry.Schema(
    query=Query,
    config=StrawberryConfig(auto_camel_case=True),
)


def create_app(init_db=True, init_bot=False):
    manager = LifespanManager()

    if init_db:

        @manager.add
        async def init_db(app: FastAPI):
            sessionmanager.init(config.DB_CONFIG)
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    if init_bot:

        @manager.add
        async def init_bot(app: FastAPI):
            get_event_loop().create_task(bot.start_bot(config.DISCORD_BOT_TOKEN))
            yield
            if not bot.is_closed():
                await bot.close()

    app = FastAPI(lifespan=manager)

    async def get_context(session: AsyncSession = Depends(sessionmanager.session)):
        return {
            'session': session,
            'discord_bot': bot,
        }

    gql_router = GraphQLRouter(
        schema,
        context_getter=get_context,
    )
    app.include_router(gql_router, prefix='/graphql')

    return app
