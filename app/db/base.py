'''
import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
from app.models import *  # Import all your models

# Create a base class for your declarative models
Base = declarative_base()
# engine = create_async_engine(settings.postgres_database_uri, echo=settings.ECHO_SQL)


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        # Initialize the engine with the provided host and engine arguments
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        # Create a sessionmaker bound to the engine for creating sessions
        self._sessionmaker = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        
    async def close(self):
        # Close the engine and dispose of the sessionmaker
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        # Provide an asynchronous session context manager
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self._sessionmaker() as session:
            try:
                yield session  # Yield the session to the caller
            except Exception:
                await session.rollback()  # Roll back the transaction on error
                raise
            finally:
                await session.close()  # Close the session after use

# Instantiate the DatabaseSessionManager with the database URI and engine options
sessionmanager = DatabaseSessionManager(
    settings.postgres_database_uri,
    {"echo": settings.ECHO_SQL, "future": True},  # Use settings.ECHO_SQL
)


async def get_idb() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
        
    

async def get_db() -> AsyncSession:
    return await anext(get_idb())

async def get_session() -> AsyncIterator[AsyncSession]:
    postgres_database_uri = "postgresql+psycopg2://postgres:root@localhost:5432/metahouse"
    sessionmanager = DatabaseSessionManager(
        postgres_database_uri,
        {"echo": True , "future": True},  # Use settings.ECHO_SQL
    )
    async with sessionmanager.session() as session:
        yield session

'''
# base.py

import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

from app.core.config import settings
from app.models import *  # Import all your models
# from utils.logger import GetLogger

# logger = GetLogger(__name__)

Base = declarative_base()
engine = create_async_engine(settings.postgres_database_uri, echo=settings.ECHO_SQL)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
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

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e

sessionmanager = DatabaseSessionManager(
    settings.postgres_database_uri,
    {"echo": settings.ECHO_SQL, "future": True},
)

async def get_idb() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session

async def get_db() -> AsyncSession:
    return await anext(get_idb())