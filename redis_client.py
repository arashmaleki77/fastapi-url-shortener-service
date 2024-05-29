from core.settings import settings
from redis import Redis


cache = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
