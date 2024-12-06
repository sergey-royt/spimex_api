from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import TypeAdapter

from src.cache.decorators import redis_cache
from src.database.db import get_async_session
from src.schemas.trading_result import (
    BaseTradeResultFilter,
    TradeResultResponse,
    TradeResultDB,
)
from src.api.v1.services.trade_services import get_trading_results


trade_router = APIRouter(prefix="/trading_results")


@trade_router.get("/")
@redis_cache(type_adapter=TypeAdapter(TradeResultResponse))
async def trading_results(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    filters: BaseTradeResultFilter = Depends(BaseTradeResultFilter),
) -> TradeResultResponse:
    """
    Return last trade results (descending order)
    For specified filters
    - oil_id
    - delivery-type_id
    - delivery_basis_id

    Page and count of trades per page can be specified
    Using cash if possible
    """

    result: list[TradeResultDB] = await get_trading_results(session, filters)
    return TradeResultResponse(payload=result)
