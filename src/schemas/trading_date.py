from datetime import date
from typing import Sequence, Annotated

from fastapi import Query
from pydantic import BaseModel

from src.schemas.response import BaseResponse


class TradingDateFilter(BaseModel):
    count: Annotated[int, Query(ge=1, default=10)]


class TradingDatesResponse(BaseResponse):
    payload: Sequence[date]
