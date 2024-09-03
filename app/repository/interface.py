import uuid
from typing import Any, Protocol, TypeVar

from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail

T = TypeVar("T")


class AbstractRepository(Protocol[T]):
    def get_all(self) -> list[T]: ...

    def create(self, entity_create: dict[str, Any]) -> T: ...


class AbstractUserRepository(AbstractRepository[UserDetail], Protocol):
    def get(self, entity_id: uuid.UUID) -> UserDetail | None: ...

    def get_by_upn(self, upn: str) -> UserDetail | None: ...

    def delete(self, entity_id: uuid.UUID) -> None: ...


class AbstractRoleRepository(AbstractRepository[RoleDetail], Protocol):
    def get_by_code(self, code: str) -> RoleDetail | None: ...

    def update(self, code: str, entity_update: dict[str, Any]) -> RoleDetail: ...

    def delete(self, code: str) -> None: ...


class AbstractSiteRepository(AbstractRepository[SiteDetail], Protocol):
    def get_by_code(self, code: str) -> SiteDetail | None: ...

    def update(self, code: str, entity_update: dict[str, Any]) -> SiteDetail: ...

    def delete(self, code: str) -> None: ...


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
