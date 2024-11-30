from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.schemas.trading_result import (
    BaseTradeResultFilter,
    TradeResultResponse,
    TradeResultDB,
)
from src.api.v1.services.trade_services import get_trading_results


trade_router = APIRouter(prefix="/trading_results")


@trade_router.get("/")
async def trading_results(
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
    """

    result: list[TradeResultDB] = await get_trading_results(session, filters)
    return TradeResultResponse(payload=result)
