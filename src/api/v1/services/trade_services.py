from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.trade_result import TradeResult
from src.schemas.trading_result import (
    BaseTradeResultFilter,
    TradeResultDynamicFilter,
    TradeResultDB,
)
from src.schemas.trading_date import TradingDateFilter


async def get_last_trading_dates(
    session: AsyncSession, filters: TradingDateFilter
) -> Sequence[date]:
    """
    Return list of last trading dates
    """

    stmt = (
        select(TradeResult.date)
        .order_by(TradeResult.date.desc())
        .distinct()
        .limit(filters.count)
    )

    result = await session.execute(stmt)

    return result.scalars().all()


async def get_dynamics(
    session: AsyncSession,
    filters: TradeResultDynamicFilter,
) -> list[TradeResultDB]:
    """
    Returns list of trade results for given period
    using:
    - start_date and - end_date args
    If no start_date is provided, result starts from the earliest date
    If no end_date is provided, it will be set to today

    Result can be filtered by:
    - oil_id
    - delivery_type_id
    - delivery_basis_id

    Pagination is supported
    """

    query = (
        select(TradeResult)
        .order_by(TradeResult.date.desc())
        .limit(filters.limit)
        .offset(filters.offset)
    )

    if filters.start_date:
        query = query.filter(TradeResult.date >= filters.start_date)

    if filters.end_date:
        query = query.filter(TradeResult.date <= filters.end_date)

    if filters.oil_id:
        query = query.filter(TradeResult.oil_id == filters.oil_id)

    if filters.delivery_type_id:
        query = query.filter(
            TradeResult.delivery_type_id == filters.delivery_type_id
        )

    if filters.delivery_basis_id:
        query = query.filter(
            TradeResult.delivery_basis_id == filters.delivery_basis_id
        )

    result = await session.execute(query)
    trades = result.scalars().all()
    return [TradeResultDB.from_orm(trade) for trade in trades]


async def get_trading_results(
    session: AsyncSession,
    filters: BaseTradeResultFilter,
) -> list[TradeResultDB]:
    """
    Returns list of last trades
    Result can be filtered by:
    - oil_id
    - delivery_type_id
    - delivery_basis_id

    Pagination is supported
    """

    query = (
        select(TradeResult)
        .distinct(
            TradeResult.oil_id,
            TradeResult.delivery_basis_id,
            TradeResult.delivery_type_id,
        )
        .order_by(
            TradeResult.oil_id,
            TradeResult.delivery_basis_id,
            TradeResult.delivery_type_id,
            TradeResult.date.desc(),
        )
        .limit(filters.limit)
        .offset(filters.offset)
    )

    if filters.oil_id:
        query = query.filter(TradeResult.oil_id == filters.oil_id)

    if filters.delivery_type_id:
        query = query.filter(
            TradeResult.delivery_type_id == filters.delivery_type_id
        )

    if filters.delivery_basis_id:
        query = query.filter(
            TradeResult.delivery_basis_id == filters.delivery_basis_id
        )

    result = await session.execute(query)
    trades = result.scalars().all()
    return [TradeResultDB.from_orm(trade) for trade in trades]
