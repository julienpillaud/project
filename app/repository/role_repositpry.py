from typing import Any

from sqlalchemy import delete, select

from app.repository.interface import AbstractRoleRepository
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.roles.models import Role
from app.roles.schemas import RoleDetail


class SQLAlchemyRoleRepository(
    SQLAlchemyRepositoryBase[Role, RoleDetail], AbstractRoleRepository
):
    def get_by_code(self, code: str) -> RoleDetail | None:
        stmt = select(Role).where(Role.code == code)
        entity = self.session.scalars(stmt).first()
        return RoleDetail.model_validate(entity) if entity else None

    def update(self, code: str, entity_update: dict[str, Any]) -> RoleDetail:
        stmt = select(Role).where(Role.code == code)
        entity = self.session.scalars(stmt).one()
        for key, value in entity_update.items():
            setattr(entity, key, value)
        self.session.commit()
        return RoleDetail.model_validate(entity)

    def delete(self, code: str) -> None:
        stmt = delete(Role).where(Role.code == code)
        self.session.execute(stmt)
        self.session.commit()


class InMemoryRoleRepository(AbstractRoleRepository):
    def __init__(self, data: list[RoleDetail]) -> None:
        self.data = data

    def get_all(self) -> list[RoleDetail]:
        return [RoleDetail.model_validate(entity) for entity in self.data]

    def get_by_code(self, code: str) -> RoleDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)

    def create(self, entity_create: dict[str, Any]) -> RoleDetail:
        data = RoleDetail.model_validate(entity_create)
        self.data.append(data)
        return data

    def update(self, code: str, entity_update: dict[str, Any]) -> RoleDetail:
        entity = self.get_by_code(code=code)
        if not entity:
            raise ValueError

        for key, value in entity_update.items():
            setattr(entity, key, value)

        return entity

    def delete(self, code: str) -> None:
        self.data = [item for item in self.data if item.code != code]
