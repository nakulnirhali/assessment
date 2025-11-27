import redis.asyncio as redis
from app.core.config import settings

_redis = None

def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis

async def get_cached(key: str):
    r = get_redis()
    val = await r.get(key)
    return val

async def set_cached(key: str, value: str, ttl: int = None):
    r = get_redis()
    if ttl:
        await r.set(key, value, ex=ttl)
    else:
        await r.set(key, value)
