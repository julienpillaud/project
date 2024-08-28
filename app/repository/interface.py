import uuid
from typing import Any, Generic, Protocol, TypeAlias, TypeVar

from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail

T = TypeVar("T")
PrimaryKey: TypeAlias = int | uuid.UUID | str  # noqa: UP040


class AbstractRepository(Protocol, Generic[T]):
    def get_all(self) -> list[T]: ...

    def create(self, entity_create: dict[str, Any]) -> T: ...

    def delete(self, entity_id: PrimaryKey) -> None: ...


class AbstractUserRepository(AbstractRepository[UserDetail], Protocol):
    def get(self, entity_id: uuid.UUID) -> UserDetail | None: ...

    def get_by_upn(self, upn: str) -> UserDetail | None: ...


class AbstractRoleRepository(AbstractRepository[RoleDetail], Protocol):
    def get_by_code(self, code: str) -> RoleDetail | None: ...

    def update(self, code: str, entity_update: dict[str, Any]) -> RoleDetail: ...


class AbstractSiteRepository(AbstractRepository[SiteDetail], Protocol):
    def get_by_code(self, code: str) -> SiteDetail | None: ...

    def update(self, code: str, entity_update: dict[str, Any]) -> SiteDetail: ...


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
