from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    DEBUG: bool


settings = Settings(_env_file=".env")  # type: ignore[call-arg]
