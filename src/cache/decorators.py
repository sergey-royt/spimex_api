from functools import wraps
from typing import Type
from collections.abc import Callable

from fastapi import Request, BackgroundTasks
from pydantic import BaseModel

from .redis_client import redis_client


def request_to_key(request: Request) -> str:
    return f"{request.method}:{request.url}"


def redis_cache(data_model: Type[BaseModel]) -> Callable:
    """
    Decorator for endpoints which allows to use redis cache

    Generate key from request using it

    Look for value in cache if it exists
    convert it to given data_model.

    If not, call endpoint and save result in cache using
    background tasks
    """

    def actual_decorator(func) -> Callable:
        @wraps(func)
        async def wrapper(
            request: Request,
            background_tasks: BackgroundTasks,
            *args,
            **kwargs,
        ) -> BaseModel:
            key = request_to_key(request)
            cache = await redis_client.get_cache(key=key)
            if cache:
                return data_model.model_validate_json(cache)
            result = await func(request, background_tasks, *args, **kwargs)
            redis_client.set_in_background(
                background_tasks,
                key=key,
                value=result.model_dump_json(),
            )
            return result

        return wrapper

    return actual_decorator
