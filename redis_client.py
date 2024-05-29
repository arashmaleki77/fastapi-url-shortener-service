import aioredis
from core.settings import settings


async def get_from_cache(key: str):
    redis = await aioredis.create_redis_pool(f"redis://{settings.REDIS_HOST}:{str(settings.REDIS_PORT)}")
    value = await redis.get(key)
    redis.close()
    await redis.wait_closed()
    return value


async def set_to_cache(key: str, value: str, expire: int):
    redis = await aioredis.create_redis_pool(f"redis://{settings.REDIS_HOST}:{str(settings.REDIS_PORT)}")
    await redis.set(key, value, expire=expire)
    redis.close()
    await redis.wait_closed()
