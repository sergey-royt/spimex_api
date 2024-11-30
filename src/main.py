from fastapi import FastAPI

from src.api.v1.handlers.last_trading_dates import dates_router
from src.api.v1.handlers.dynamics import dynamic_router
from src.api.v1.handlers.trading_results import trade_router


def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    return fastapi_app


app = create_app()

app.include_router(dates_router)
app.include_router(dynamic_router)
app.include_router(trade_router)
