from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.cache.redis_client import redis_client


async def clear_redis_cache() -> None:
    if redis_client.client:
        await redis_client.clear_cache()


def start_scheduler() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_redis_cache, "cron", hour=14, minute=11)
    scheduler.start()
