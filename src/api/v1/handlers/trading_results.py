from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Request

from src.cache.decorators import redis_cache
from src.schemas.trading_result import (
    BaseTradeResultFilter,
    TradeResultResponse,
    TradeResultDB,
)
from src.api.v1.services.trade_services import get_trading_results
from src.utils.custom_types import AsyncSessionDep


trade_router = APIRouter(prefix="/trading_results")


@trade_router.get("/")
@redis_cache(data_model=TradeResultResponse)
async def trading_results(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSessionDep,
    filters: Annotated[BaseTradeResultFilter, Depends()],
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
