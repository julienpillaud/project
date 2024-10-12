from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import Settings
from app.repository.sqlalchemy.role import SQLAlchemyRoleRepository
from app.repository.sqlalchemy.site import SQLAlchemySiteRepository
from app.repository.sqlalchemy.user import SQLAlchemyUserRepository
from app.roles.service import RoleService
from app.sites.service import SiteService
from app.users.service import UserService


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=".env")  # type: ignore


def get_engine(settings: Annotated[Settings, Depends(get_settings)]) -> Engine:
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_role_service(session: Annotated[Session, Depends(get_session)]) -> RoleService:
    repository = SQLAlchemyRoleRepository(session=session)
    return RoleService(repository=repository)


def get_site_service(session: Annotated[Session, Depends(get_session)]) -> SiteService:
    repository = SQLAlchemySiteRepository(session=session)
    return SiteService(repository=repository)


def get_user_service(session: Annotated[Session, Depends(get_session)]) -> UserService:
    repository = SQLAlchemyUserRepository(session=session)
    return UserService(repository=repository)
