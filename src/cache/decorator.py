from functools import wraps

from fastapi import Request, BackgroundTasks
from pydantic import TypeAdapter

from .redis_client import redis_client


def request_to_key(request: Request):
    return f"{request.method}:{request.url}"


def redis_cache(type_adapter: TypeAdapter):
    """
    Decorator for endpoints which allows to use redis cache

    Generate key from request using it

    Look for value in cache if it exists
    encode it according given TypeAdapter.

    If not, call endpoint and save result in cache using
    background tasks
    """

    def actual_decorator(func):
        @wraps(func)
        async def wrapper(
            request: Request,
            background_tasks: BackgroundTasks,
            *args,
            **kwargs,
        ):
            key = request_to_key(request)
            cache = await redis_client.get_cache(key=key)
            if cache:
                return type_adapter.validate_json(cache)
            result = await func(request, background_tasks, *args, **kwargs)
            redis_client.set_in_background(
                background_tasks,
                key=key,
                value=type_adapter.dump_json(result).decode("utf-8"),
            )
            return result

        return wrapper

    return actual_decorator
