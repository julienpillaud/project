from app.repository.inmemory.base import InMemoryRepositoryBase
from app.repository.interface import AbstractRoleRepository
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate


class InMemoryRoleRepository(
    AbstractRoleRepository, InMemoryRepositoryBase[RoleDetail, RoleCreate, RoleUpdate]
):
    model = RoleDetail

    def get_by_code(self, code: str) -> RoleDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)
