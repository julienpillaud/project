from sqlalchemy import String
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.repository.sqlalchemy_repo import AbstractSQLAlchemyRepository, Base
from app.users.schemas import UserDetail


class User(Base):
    email: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(128))


class UserSQLRepository(AbstractSQLAlchemyRepository[User, UserDetail]):
    """Implement an SQLAlchemy repository with a User model."""

    def __init__(self, session: Session) -> None:
        self.entity = UserDetail
        self.session = session
        self.model = User
