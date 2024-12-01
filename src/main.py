import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.v1.handlers.last_trading_dates import dates_router
from src.api.v1.handlers.dynamics import dynamic_router
from src.api.v1.handlers.trading_results import trade_router
from src.cache.redis_client import redis_client
from src.tasks.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Application start")
    await redis_client.connect()
    start_scheduler()
    yield
    await redis_client.clear_cache()
    await redis_client.close()
    logging.info("Application stop")


def create_app() -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan)
    return fastapi_app


app = create_app()

app.include_router(dates_router)
app.include_router(dynamic_router)
app.include_router(trade_router)
