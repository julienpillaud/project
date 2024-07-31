import uuid
from typing import Any, Generic, Type, TypeVar

from sqlalchemy import UUID, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    declared_attr,
    mapped_column,
)

from app.repository.interface import AbstractRepository, EntityType


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


ModelType = TypeVar("ModelType", bound=Base)


class AbstractSQLAlchemyRepository(
    Generic[ModelType, EntityType], AbstractRepository[EntityType]
):
    model: Type[ModelType]
    session: Session

    def get_all(self) -> list[EntityType]:
        stmt = select(self.model)
        entities = self.session.scalars(stmt)
        return [self.entity.model_validate(entity) for entity in entities]

    def get(self, entity_id: uuid.UUID) -> EntityType | None:
        # Need to have Base(DeclarativeBase) to call self.model.id
        stmt = select(self.model).where(self.model.id == entity_id)
        model_obj = self.session.scalars(stmt).first()
        return self.entity.model_validate(model_obj) if model_obj else None

    def create(self, entity_create: dict[str, Any]) -> EntityType:
        model_obj = self.model(**entity_create)
        self.session.add(model_obj)
        self.session.commit()
        return self.entity.model_validate(model_obj)

    def update(
        self, entity_id: uuid.UUID, entity_update: dict[str, Any]
    ) -> EntityType | None:
        stmt = select(self.model).where(self.model.id == entity_id)
        model_obj = self.session.scalars(stmt).first()
        if not model_obj:
            return None

        for key, value in entity_update.items():
            if hasattr(model_obj, key):
                setattr(model_obj, key, value)
        self.session.commit()
        return self.entity.model_validate(model_obj)

    def delete(self, entity_id: uuid.UUID) -> None:
        stmt = select(self.model).where(self.model.id == entity_id)
        if model_obj := self.session.scalars(stmt).first():
            self.session.delete(model_obj)
        else:
            return None
