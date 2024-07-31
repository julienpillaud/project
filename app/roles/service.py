import uuid

from app.repository.interface import AbstractRepository
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate


class RoleService:
    @staticmethod
    def get_roles(repository: AbstractRepository[RoleDetail]) -> list[RoleDetail]:
        return repository.get_all()

    @staticmethod
    def get_role(
        repository: AbstractRepository[RoleDetail], role_id: uuid.UUID
    ) -> RoleDetail | None:
        return repository.get(entity_id=role_id)

    @staticmethod
    def create_role(
        repository: AbstractRepository[RoleDetail], role_create: RoleCreate
    ) -> RoleDetail:
        return repository.create(entity_create=role_create.model_dump())

    @staticmethod
    def update_role(
        repository: AbstractRepository[RoleDetail],
        role_id: uuid.UUID,
        role_update: RoleUpdate,
    ) -> RoleDetail | None:
        return repository.update(
            entity_id=role_id, entity_update=role_update.model_dump()
        )

    @staticmethod
    def delete_role(
        repository: AbstractRepository[RoleDetail], role_id: uuid.UUID
    ) -> None:
        return repository.delete(entity_id=role_id)
