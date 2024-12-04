
import redis.asyncio as redis

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"

settings = Settings()

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_cache_value(key: str):
    return await redis_client.get(key)

async def set_cache_value(key: str, value: str, expire: int = None):
    await redis_client.set(key, value, ex=expire)

async def delete_cache_key(key: str):
    await redis_client.delete(key)