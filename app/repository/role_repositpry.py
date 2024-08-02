from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repository.interface import AbstractRoleRepository
from app.roles.models import Role
from app.roles.schemas import RoleDetail


class SQLAlchemyRoleRepository(AbstractRoleRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[RoleDetail]:
        stmt = select(Role)
        entities = self.session.scalars(stmt)
        return [RoleDetail.model_validate(entity) for entity in entities]

    def get_by_code(self, code: str) -> RoleDetail | None:
        stmt = select(RoleDetail).where(Role.code == code)
        entities = self.session.scalars(stmt).first()
        return RoleDetail.model_validate(entities) if entities else None


class InMemoryRoleRepository(AbstractRoleRepository):
    def __init__(self, data: list[RoleDetail]) -> None:
        self.data = data

    def get_all(self) -> list[RoleDetail]:
        return [RoleDetail.model_validate(entity) for entity in self.data]

    def get_by_code(self, code: str) -> RoleDetail | None:
        return next((item for item in self.data if item.code == code), None)
