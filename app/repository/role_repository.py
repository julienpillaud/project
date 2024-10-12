from sqlalchemy import select

from app.repository.interface import AbstractRoleRepository
from app.repository.sql.models import Role
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate


class SQLAlchemyRoleRepository(
    AbstractRoleRepository,
    SQLAlchemyRepositoryBase[Role, RoleDetail, RoleCreate, RoleUpdate],
):
    model = Role
    schema = RoleDetail

    def get_by_code(self, code: str) -> RoleDetail | None:
        stmt = select(Role).where(Role.code == code)
        entity = self.session.scalars(stmt).first()
        return RoleDetail.model_validate(entity) if entity else None
