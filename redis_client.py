from aioredis import create_redis_pool, Redis
from core.settings import settings


async def get_redis_client() -> Redis:
    redis = await create_redis_pool(f"redis://{settings.REDIS_HOST}:{str(settings.REDIS_PORT)}")
    yield redis
    redis.close()
    await redis.wait_closed()
