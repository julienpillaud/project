from collections.abc import Iterator
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.api.dependencies.repositories import BaseRepositoryDependency
from app.config import Settings, get_settings
from app.entities import ServiceName
from app.repository.sqlalchemy.role import SQLAlchemyRoleRepository
from app.repository.sqlalchemy.site import SQLAlchemySiteRepository
from app.repository.sqlalchemy.user import SQLAlchemyUserRepository

repositories_map: dict[ServiceName, type[Any]] = {
    "role": SQLAlchemyRoleRepository,
    "site": SQLAlchemySiteRepository,
    "user": SQLAlchemyUserRepository,
}


def get_engine(settings: Annotated[Settings, Depends(get_settings)]) -> Engine:
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    with Session(engine) as session:
        yield session


class SQLAlchemyRepositoryDependency(BaseRepositoryDependency):
    def __init__(self, service_name: ServiceName) -> None:
        super().__init__(service_name)
        self.repository = repositories_map[service_name]

    def __call__(self, session: Annotated[Session, Depends(get_session)]) -> Any:
        return self.repository(session=session)
