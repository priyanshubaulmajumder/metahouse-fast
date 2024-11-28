'''
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings
import psycopg2
import psycopg2_pool

Base = declarative_base()

def validate_database():
    # Use a synchronous engine for database existence check and creation
    sync_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.replace('asyncpg', 'psycopg2'))
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
        print("New database is created")
    else:
        print("Database already exists")
        
    # Create all tables if they do not exist
    Base.metadata.create_all(sync_engine)
    print("All tables are created")

# Import all your models here so that Base has them before calling create_all
from app.models import *



import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings
from app.models import *
#from utils.logger import GetLogger

#logger = GetLogger(__name__)

Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

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
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(
    settings.SQLALCHEMY_DATABASE_URI,
    {"echo": settings.echo_sql, "future": True},
)

async def validate_database():
    async with sessionmanager.connect() as connection:
        if not await connection.run_sync(database_exists, connection.url):
            await connection.run_sync(create_database, connection.url)
            logger.info("New database is created")
        else:
            logger.info("Database already exists")
        await connection.run_sync(Base.metadata.create_all)

# Import all your models here so that Base has them before calling create_all
from app.models import *


async def get_idb() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session

async def get_db() -> AsyncSession:
    return await anext(get_idb())

'''