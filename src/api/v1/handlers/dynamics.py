from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.schemas.trading_result import (
    TradeResultDynamicFilter,
    TradeResultResponse,
    TradeResultDB,
)
from src.api.v1.services.trade_services import get_dynamics
from src.cache.decorator import redis_cache

dynamic_router = APIRouter(prefix="/dynamics")


@dynamic_router.get("/")
@redis_cache(type_adapter=TypeAdapter(TradeResultResponse))
async def dynamics(
    request: Request,
    background_tasks: BackgroundTasks,
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

    if (
        filters.start_date
        and filters.end_date
        and filters.start_date >= filters.end_date
    ):
        raise HTTPException(
            status_code=400, detail="start_date must be less than end_date"
        )

    result: list[TradeResultDB] = await get_dynamics(
        session=session,
        filters=filters,
    )
    return TradeResultResponse(payload=result)