from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.database.db import get_async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
