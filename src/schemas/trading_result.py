from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from src.schemas.filter import BaseFilter
from src.schemas.response import BaseResponse


class TradeResultDB(BaseModel):
    id: int
    exchange_product_id: str = Field(max_length=11)
    exchange_product_name: str = Field(max_length=200)
    delivery_basis_name: str = Field(max_length=50)
    volume: int
    total: int
    count: int
    date: date
    oil_id: str = Field(max_length=4)
    delivery_basis_id: str = Field(max_length=3)
    delivery_type_id: str = Field(max_length=2)
    created_on: datetime
    updated_on: datetime


@dataclass
class BaseTradeResultFilter(BaseFilter):
    oil_id: Optional[str] = Query(None)
    delivery_type_id: Optional[str] = Query(None)
    delivery_basis_id: Optional[str] = Query(None)


@dataclass
class TradeResultDynamicFilter(BaseTradeResultFilter):
    start_date: Optional[date] = Query(None)
    end_date: Optional[date] = Query(None)


class TradeResultResponse(BaseResponse):
    payload: list[TradeResultDB]
