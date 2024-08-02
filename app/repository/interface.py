import uuid
from typing import Any, Protocol

from app.roles.schemas import RoleDetail
from app.users.schemas import UserDetail


class AbstractUserRepository(Protocol):
    def get_all(self) -> list[UserDetail]: ...

    def get(self, entity_id: uuid.UUID) -> UserDetail | None: ...

    def create(self, entity_create: dict[str, Any]) -> UserDetail: ...


class AbstractRoleRepository(Protocol):
    def get_all(self) -> list[RoleDetail]: ...

    def get_by_code(self, code: str) -> RoleDetail | None: ...
