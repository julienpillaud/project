import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import Uuid, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    declared_attr,
    mapped_column,
)

from app.repository.interface import AbstractRepository


class Base(DeclarativeBase):
    """Custom declarative base for SQLAlchemy

    # https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateType = TypeVar("CreateType", bound=BaseModel)
UpdateType = TypeVar("UpdateType", bound=BaseModel)


class SQLAlchemyRepositoryBase(
    AbstractRepository[SchemaType, CreateType, UpdateType],
    Generic[ModelType, SchemaType, CreateType, UpdateType],
):
    model: type[ModelType]
    schema: type[SchemaType]

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[SchemaType]:
        stmt = select(self.model)
        entities = self.session.scalars(stmt)
        return [self.schema.model_validate(entity) for entity in entities]

    def get(self, entity_id: uuid.UUID) -> SchemaType | None:
        entity = self.session.get(self.model, entity_id)
        return self.schema.model_validate(entity) if entity else None

    def create(self, entity_create: CreateType) -> SchemaType:
        entity = self.model(**entity_create.model_dump())
        self.session.add(entity)
        self.session.commit()
        return self.schema.model_validate(entity)

    def update(self, entity_id: uuid.UUID, entity_update: UpdateType) -> SchemaType:
        entity = self.session.get(self.model, entity_id)
        for key, value in entity_update.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)
        self.session.commit()
        return self.schema.model_validate(entity)

    def delete(self, entity_id: uuid.UUID) -> None:
        entity = self.session.get(self.model, entity_id)
        self.session.delete(entity)
