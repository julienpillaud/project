import uuid

from app.repository.interface import AbstractRoleRepository
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate
from app.services import BaseService


class RoleService(BaseService[AbstractRoleRepository]):
    def get_roles(self) -> list[RoleDetail]:
        return self.repository.get_all()

    def get_role(self, role_id: uuid.UUID) -> RoleDetail | None:
        return self.repository.get(entity_id=role_id)

    def get_role_by_code(self, code: str) -> RoleDetail | None:
        return self.repository.get_by_code(code=code)

    def create_role(self, role_create: RoleCreate) -> RoleDetail:
        return self.repository.create(entity_create=role_create)

    def update_role(self, role_id: uuid.UUID, role_update: RoleUpdate) -> RoleDetail:
        return self.repository.update(entity_id=role_id, entity_update=role_update)

    def delete_role(self, role_id: uuid.UUID) -> None:
        self.repository.delete(entity_id=role_id)
