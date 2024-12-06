from datetime import date
from typing import Sequence

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.api.v1.services.trade_services import get_last_trading_dates
from src.schemas.trading_date import TradingDatesResponse
from src.schemas.trading_date import TradingDateFilter
from src.cache.decorators import redis_cache


dates_router = APIRouter(prefix="/last_trading_dates")


@dates_router.get("/")
@redis_cache(type_adapter=TypeAdapter(TradingDatesResponse))
async def last_trading_dates(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    filters: TradingDateFilter = Depends(TradingDateFilter),
) -> TradingDatesResponse:
    """
    Return last trading dates (descending order)
    The count of dates can be specified
    By default it would be 10

    Using cash if possible
    """

    result: Sequence[date] = await get_last_trading_dates(
        session=session,
        filters=filters,
    )
    return TradingDatesResponse(payload=result)
