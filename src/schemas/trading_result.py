from typing_extensions import Self
from datetime import date
from typing import Optional, Annotated

from fastapi import Query, HTTPException
from pydantic import BaseModel, Field, model_validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.schemas.filter import BaseFilter
from src.schemas.response import BaseResponse


class TradeResultDB(BaseModel):
    exchange_product_id: Annotated[str, Field(max_length=11)]
    exchange_product_name: Annotated[str, Field(max_length=200)]
    delivery_basis_name: Annotated[str, Field(max_length=50)]
    volume: int
    total: int
    count: int
    date: date
    oil_id: Annotated[str, Field(max_length=4)]
    delivery_basis_id: Annotated[str, Field(max_length=3)]
    delivery_type_id: Annotated[str, Field(max_length=2)]


class BaseTradeResultFilter(BaseFilter):
    oil_id: Annotated[Optional[str], Query(None)]
    delivery_type_id: Annotated[Optional[str], Query(None)]
    delivery_basis_id: Annotated[Optional[str], Query(None)]


class TradeResultDynamicFilter(BaseTradeResultFilter):
    start_date: Annotated[Optional[date], Query(None)]
    end_date: Annotated[Optional[date], Query(None)]

    @model_validator(mode="before")
    @classmethod
    def validate_date(cls, data) -> Self:
        if (
            data.get("start_date")
            and data.get("end_date")
            and data.get("start_date") >= data.get("end_date")
        ):
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Start_date must be less than end_date",
            )
        return data


class TradeResultResponse(BaseResponse):
    payload: list[TradeResultDB]
