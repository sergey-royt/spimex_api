from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class BaseFilter(BaseModel):
    page: Annotated[int, Query(ge=1, default=1)]
    per_page: Annotated[int, Query(ge=1, le=100, default=100)]

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page
