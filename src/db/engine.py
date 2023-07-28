import contextlib
from typing import AsyncIterator, Optional

from dynaconf import settings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DSN_STR = 'postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}'.format(
    username=settings.POSTGRES.user,
    password=settings.POSTGRES.password,
    host=settings.POSTGRES.host,
    port=settings.POSTGRES.port,
    database=settings.POSTGRES.database,
)


class DatabaseSessionManager:
    def __init__(self):
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker] = None

    def init(self, host: str = DSN_STR):
        self._engine = create_async_engine(host, echo=True, future=True)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False, future=True)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()