import uuid
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repository.interface import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class SQLAlchemyRepositoryBase(Generic[ModelType, SchemaType]):
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

    def create(self, entity_create: dict[str, Any]) -> SchemaType:
        entity = self.model(**entity_create)
        self.session.add(entity)
        self.session.commit()
        return self.schema.model_validate(entity)

    def update(self, entity_id: uuid.UUID, entity_update: dict[str, Any]) -> SchemaType:
        entity = self.session.get(self.model, entity_id)
        for key, value in entity_update.items():
            setattr(entity, key, value)
        self.session.commit()
        return self.schema.model_validate(entity)

    def delete(self, entity_id: uuid.UUID) -> None:
        entity = self.session.get(self.model, entity_id)
        self.session.delete(entity)
