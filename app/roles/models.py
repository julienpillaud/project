from sqlalchemy import String
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.repository.sqlalchemy_repo import AbstractSQLAlchemyRepository, Base
from app.roles.schemas import RoleDetail


class Role(Base):
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)


class RoleSQLRepository(AbstractSQLAlchemyRepository[Role, RoleDetail]):
    """Implement an SQLAlchemy repository with a Role model."""

    def __init__(self, session: Session) -> None:
        self.entity = RoleDetail
        self.session = session
        self.model = Role
