import asyncio

import redis
from core.config import settings

redis_client = redis.StrictRedis.from_url(str(settings.radis_uri), decode_responses=True)


async def acquire_lock(lock_key: str, timeout: int) -> bool:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: redis_client.set(lock_key, "locked", ex=timeout, nx=True))
    return result


async def release_lock(lock_key: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, redis_client.delete, lock_key)
