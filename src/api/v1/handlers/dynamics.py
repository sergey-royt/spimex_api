from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.schemas.trading_result import (
    TradeResultDynamicFilter,
    TradeResultResponse,
    TradeResultDB,
)
from src.api.v1.services.trade_services import get_dynamics


dynamic_router = APIRouter(prefix="/dynamics")


@dynamic_router.get("/")
async def dynamics(
    session: AsyncSession = Depends(get_async_session),
    filters: TradeResultDynamicFilter = Depends(TradeResultDynamicFilter),
) -> TradeResultResponse:
    """
    Return trade results for given period (descending order)
    If start_date not provided it set to the earliest trade date
    If end_date not provided it set to the current date
    Results can be filtered by: oil_id, delivery_basis_id, delivery_type_id
    Page and count of trades per page can be specified
    """

    result: list[TradeResultDB] = await get_dynamics(session, filters)
    return TradeResultResponse(payload=result)
