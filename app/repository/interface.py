import uuid
from typing import Any, Protocol

from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail


class AbstractUserRepository(Protocol):
    def get_all(self) -> list[UserDetail]: ...

    def get(self, entity_id: uuid.UUID) -> UserDetail | None: ...

    def get_by_upn(self, upn: str) -> UserDetail | None: ...

    def create(self, entity_create: dict[str, Any]) -> UserDetail: ...

    def delete(self, entity_id: uuid.UUID) -> None: ...


class AbstractRoleRepository(Protocol):
    def get_all(self) -> list[RoleDetail]: ...

    def get_by_code(self, code: str) -> RoleDetail | None: ...

    def create(self, entity_create: dict[str, Any]) -> RoleDetail: ...

    def update(self, code: str, entity_update: dict[str, Any]) -> RoleDetail: ...

    def delete(self, code: str) -> None: ...


class AbstractSiteRepository(Protocol):
    def get_all(self) -> list[SiteDetail]: ...

    def get_by_code(self, code: str) -> SiteDetail | None: ...

    def create(self, entity_create: dict[str, Any]) -> SiteDetail: ...

    def update(self, code: str, entity_update: dict[str, Any]) -> SiteDetail: ...

    def delete(self, code: str) -> None: ...


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
