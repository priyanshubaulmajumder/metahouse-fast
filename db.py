import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection, async_sessionmaker
from sqlalchemy.orm import  sessionmaker
from app.core.config import settings
from app.services.service import get_hist_nav_data



class DatabaseSessionManager:
    '''
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
    '''
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
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
# Instantiate the DatabaseSessionManager with the database URI and engine options
sessionmanager = DatabaseSessionManager(
    settings.postgres_database_uri,
    {"echo": settings.ECHO_SQL , "future": True},  
)

async def get_idb() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
        
    

async def get_db() -> AsyncSession:
    return await anext(get_idb())

async def trial(wpc):
    import sqlalchemy
    from sqlalchemy.future import select
    from db import get_db
    from app.models.scheme import SchemeHistNavData
    from app.services.service import SchemeHistNavService

    db = await get_db()
    result = await SchemeHistNavService.get_hist_nav_data(db, wpc)
    return result

#wpc="MF00001580"


import asyncio
loop = asyncio.get_event_loop()
data = loop.run_until_complete(trial(wpc="MF00001580"))



#results = await trial()

