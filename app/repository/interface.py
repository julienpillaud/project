import uuid
from typing import Any, Protocol, TypeVar

from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail

T = TypeVar("T")


class AbstractRepository(Protocol[T]):
    def get_all(self) -> list[T]: ...

    def get(self, entity_id: uuid.UUID) -> T | None: ...

    def create(self, entity_create: dict[str, Any]) -> T: ...

    def update(self, entity_id: uuid.UUID, entity_update: dict[str, Any]) -> T: ...

    def delete(self, entity_id: uuid.UUID) -> None: ...


class AbstractUserRepository(AbstractRepository[UserDetail], Protocol):
    def get_by_upn(self, upn: str) -> UserDetail | None: ...

    def add_site_to_user(
        self, user_id: uuid.UUID, site_id: uuid.UUID
    ) -> UserDetail: ...

    def delete_site_from_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> None: ...


class AbstractRoleRepository(AbstractRepository[RoleDetail], Protocol):
    def get_by_code(self, code: str) -> RoleDetail | None: ...


class AbstractSiteRepository(AbstractRepository[SiteDetail], Protocol):
    def get_by_code(self, code: str) -> SiteDetail | None: ...


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
