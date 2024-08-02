import uuid
from typing import Any, Protocol

from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.roles.schemas import RoleDetail
from app.users.schemas import UserDetail


class AbstractUserRepository(Protocol):
    def get_all(self) -> list[UserDetail]: ...

    def get(self, entity_id: uuid.UUID) -> UserDetail | None: ...

    def create(self, entity_create: dict[str, Any]) -> UserDetail: ...


class AbstractRoleRepository(Protocol):
    def get_all(self) -> list[RoleDetail]: ...

    def get_by_code(self, code: str) -> RoleDetail | None: ...


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
