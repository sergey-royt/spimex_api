import hashlib
from typing import Optional

from loguru import logger
from fastapi import BackgroundTasks
import redis.asyncio as redis
from redis.exceptions import ConnectionError

from src.config import settings


class RedisClient:
    """
    Key-value cache client
    Keys are hashed for storing
    """

    def __init__(self, url: str):
        self.url = url
        self.client: Optional[redis.Redis[str]] = None

    async def connect(self) -> None:
        try:
            logger.info("Connecting to Redis")
            self.client = await redis.from_url(self.url)
            await self.client.ping()
        except ConnectionError as e:
            self.client = None
            logger.error(f"Error while connecting to Redis: {e}")

    async def close(self) -> None:
        if self.client:
            await self.client.close()

    async def get_cache(self, key: str) -> Optional[str]:
        """
        Hash key and search for value using it
        Return value or None if not found
        """

        if self.client:
            key = self._hash_key(key)
            logger.info(f"Searching for key: {key}")
            value = await self.client.get(key)
            return value
        else:
            self.log_not_connected()
            return None

    async def set_cache(self, key: str, value: str) -> None:
        """
        Hash key and set value
        """

        if self.client:
            db_key = self._hash_key(key)
            try:
                await self.client.set(db_key, value)
            finally:
                logger.info(f"Value for key: {db_key} is set")
        else:
            self.log_not_connected()

    def set_in_background(
        self, background_tasks: BackgroundTasks, key: str, value: str
    ) -> None:
        """
        add set_cache task to given background_tasks
        """

        background_tasks.add_task(self.set_cache, key, value)

    async def clear_cache(self) -> None:
        if self.client:
            try:
                await self.client.flushall()
            finally:
                logger.info("Cache cleared")
        return None

    @staticmethod
    def _hash_key(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    @staticmethod
    def log_not_connected() -> None:
        logger.warning("Can't using cache. Not connected to Redis")


redis_client = RedisClient(url=settings.REDIS_URL)


def get_redis_client() -> RedisClient:
    return redis_client
