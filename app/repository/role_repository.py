import uuid

from sqlalchemy import select

from app.repository.interface import AbstractRoleRepository
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.roles.models import Role
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate


class SQLAlchemyRoleRepository(
    SQLAlchemyRepositoryBase[Role, RoleDetail], AbstractRoleRepository
):
    model = Role
    schema = RoleDetail

    def get_by_code(self, code: str) -> RoleDetail | None:
        stmt = select(Role).where(Role.code == code)
        entity = self.session.scalars(stmt).first()
        return RoleDetail.model_validate(entity) if entity else None


class InMemoryRoleRepository(AbstractRoleRepository):
    def __init__(self, data: list[RoleDetail]) -> None:
        self.data = data

    def get_all(self) -> list[RoleDetail]:
        return [RoleDetail.model_validate(entity) for entity in self.data]

    def get(self, entity_id: uuid.UUID) -> RoleDetail | None:
        return next((entity for entity in self.data if entity.id == entity_id), None)

    def get_by_code(self, code: str) -> RoleDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)

    def create(self, entity_create: RoleCreate) -> RoleDetail:
        data = RoleDetail(id=uuid.uuid4(), **entity_create.model_dump())
        self.data.append(data)
        return data

    def update(self, entity_id: uuid.UUID, entity_update: RoleUpdate) -> RoleDetail:
        entity = self.get(entity_id=entity_id)
        if not entity:
            raise ValueError

        for key, value in entity_update.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)

        return entity

    def delete(self, entity_id: uuid.UUID) -> None:
        self.data = [item for item in self.data if item.id != entity_id]
