from app.repository.interface import AbstractRoleRepository
from app.roles.schemas import RoleDetail


class RoleService:
    def __init__(self, repository: AbstractRoleRepository):
        self.repository = repository

    def get_roles(self) -> list[RoleDetail]:
        return self.repository.get_all()

    def get_role_by_code(self, code: str) -> RoleDetail | None:
        return self.repository.get_by_code(code=code)
