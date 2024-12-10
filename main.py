import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import get_db, async_session
import uvicorn
import asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# Test endpoint to verify database access
@app.get("/test-db")
async def test_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "success", "result": result.scalar()}

# Startup event to check database connection
@app.on_event("startup")
async def startup_event():
    async with async_session() as session:
        try:
            redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            await asyncio.sleep(0)  # Allow event loop to process
            raise SystemExit("Failed to connect to the database.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True, log_level="debug")