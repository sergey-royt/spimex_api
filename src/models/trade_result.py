from datetime import date, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from src.schemas.trading_result import TradeResultDB


class Base(DeclarativeBase):
    pass


class TradeResult(Base):
    __tablename__ = "trade_report_entities"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String(length=11))
    exchange_product_name: Mapped[str] = mapped_column(String(length=200))
    delivery_basis_name: Mapped[str] = mapped_column(String(length=50))
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[date]
    oil_id: Mapped[str] = mapped_column(String(length=4))
    delivery_basis_id: Mapped[str] = mapped_column(String(length=3))
    delivery_type_id: Mapped[str] = mapped_column(String(length=1))
    created_on: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now()
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def to_pydantic_schema(self) -> TradeResultDB:
        return TradeResultDB(**self.__dict__)
