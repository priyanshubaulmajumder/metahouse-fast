import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.deps import get_db
from ..main import app
from tests.test_config import TEST_SETTINGS

# Create async engine for testing
engine = create_async_engine(
    TEST_SETTINGS["DATABASE_URL"],
    echo=False  # Set to True for SQL debugging
)

# Create async session factory
TestingSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    bind=engine
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_app():
    # Setup
    app.state.testing = True
    yield app
    # Cleanup
    app.state.testing = False

@pytest.fixture(scope="function")
async def db():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session for test
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

    # Cleanup - drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(test_app):
    """Create a test client using httpx.AsyncClient"""
    from httpx import AsyncClient
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac

# Override the dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db
