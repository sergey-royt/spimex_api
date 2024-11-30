from dataclasses import dataclass
from typing import Optional

from fastapi import Query


@dataclass
class BaseFilter:
    page: Optional[int] = Query(default=None)
    per_page: int = Query(ge=1, le=100, default=100)

    @property
    def offset(self) -> int:
        return self.page * self.per_page if self.page else 0

    @property
    def limit(self) -> Optional[int]:
        return self.per_page if self.page is not None else None
