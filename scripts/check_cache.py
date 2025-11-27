import asyncio
import redis.asyncio as redis
from app.core.config import settings

async def main():
    try:
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        info = await r.info()
        print("redis info: server:", info.get("redis_version"), "used_memory_human:", info.get("used_memory_human"))
        dbsize = await r.dbsize()
        print("DBSIZE (total keys):", dbsize)

        # list first 200 keys to avoid flooding
        keys = await r.keys("*")
        print("sample keys (count):", len(keys))
        for k in keys[:200]:
            try:
                t = await r.type(k)
                ttl = await r.ttl(k)
                v = None
                if t == "string":
                    v = await r.get(k)
                    if v and len(v) > 400:
                        v = v[:400] + "..."
                else:
                    v = f"<type {t}>"
                print(f"KEY: {k}  TYPE: {t} TTL: {ttl}  VAL: {v}")
            except Exception as e:
                print("error reading key", k, repr(e))
    except Exception as e:
        print("redis error:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
