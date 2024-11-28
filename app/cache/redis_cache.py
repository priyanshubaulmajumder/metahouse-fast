import asyncio
import aioredis

from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"

settings = Settings()

redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_cache_value(key: str):
    return await redis.get(key)

async def set_cache_value(key: str, value: str, expire: int = None):
    await redis.set(key, value, ex=expire)

async def delete_cache_key(key: str):
    await redis.delete(key)