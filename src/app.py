import logging
from contextlib import asynccontextmanager

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from settings.config import config
from src.api.query import Query
from src.db.engine import sessionmanager

schema = strawberry.Schema(
    query=Query,
    config=StrawberryConfig(auto_camel_case=True),
)

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)


def create_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(lifespan=lifespan)

    gql_router = GraphQLRouter(schema)
    app.include_router(gql_router, prefix="/graphql")

    return app
