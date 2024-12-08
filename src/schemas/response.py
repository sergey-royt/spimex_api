from typing import Annotated

from pydantic import BaseModel, Field
from starlette.status import HTTP_200_OK


class BaseResponse(BaseModel):
    status: Annotated[int, Field(default=HTTP_200_OK)]
    error: Annotated[bool, Field(default=False)]
