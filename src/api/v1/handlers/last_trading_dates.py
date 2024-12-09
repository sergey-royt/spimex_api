from datetime import date
from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, Request, BackgroundTasks

from src.api.v1.services.trade_services import get_last_trading_dates
from src.schemas.trading_date import TradingDatesResponse
from src.schemas.trading_date import TradingDateFilter
from src.cache.decorators import redis_cache
from src.utils.custom_types import AsyncSessionDep


dates_router = APIRouter(prefix="/last_trading_dates")


@dates_router.get("/")
@redis_cache(data_model=TradingDatesResponse)
async def last_trading_dates(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSessionDep,
    filters: Annotated[TradingDateFilter, Depends()],
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
