import asyncio
import redis.asyncio as redis
from app.core.config import settings

async def main():
    try:
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        pong = await r.ping()
        print("Redis ping:", pong)
    except Exception as e:
        print("Redis error:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
