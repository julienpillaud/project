from functools import lru_cache

from pydantic_settings import BaseSettings

from app.entities import DatabaseType


class Settings(BaseSettings):
    DATABASE_TYPE: DatabaseType
    SQLALCHEMY_DATABASE_URI: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=".env")  # type: ignore
