from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=".env")  # type: ignore


def get_engine(settings: Annotated[Settings, Depends(get_settings)]) -> Engine:
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    with Session(engine) as session:
        yield session
