from typing import Optional, Annotated

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    DEBUG: bool
    HOST: Annotated[Optional[str], Field(default="")]


settings = Settings(_env_file=".env")  # type: ignore[call-arg]
