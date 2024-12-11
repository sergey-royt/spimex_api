from typing import Optional, Annotated

from fastapi import Query
from pydantic import BaseModel


class BaseFilter(BaseModel):
    page: Annotated[int, Query(ge=1, default=1)]
    per_page: Annotated[int, Query(ge=1, le=100, default=100)]

    @property
    def offset(self) -> int:
        return self.page * self.per_page if self.page else 0

    @property
    def limit(self) -> Optional[int]:
        return self.per_page if self.page is not None else None
