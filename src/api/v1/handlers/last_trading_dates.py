from fastapi import APIRouter, Request


router = APIRouter(prefix="/last_trading_dates")


@router.get("/")
async def get_last_trading_dates(request: Request):
    return {"response": "ok"}
