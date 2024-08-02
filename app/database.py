import uuid

from sqlalchemy import UUID, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
