import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel

from app.entities import BaseEntity
from app.repository.interface import AbstractRepository

TypeDetail = TypeVar("TypeDetail", bound=BaseEntity)
TypeCreate = TypeVar("TypeCreate", bound=BaseModel)
TypeUpdate = TypeVar("TypeUpdate", bound=BaseModel)


class InMemoryRepositoryBase(
    AbstractRepository[TypeDetail, TypeCreate, TypeUpdate],
    Generic[TypeDetail, TypeCreate, TypeUpdate],
):
    model: type[TypeDetail]

    def __init__(self, data: list[TypeDetail]) -> None:
        self.data = data

    def get_all(self) -> list[TypeDetail]:
        return [self.model.model_validate(entity) for entity in self.data]

    def get(self, entity_id: uuid.UUID) -> TypeDetail | None:
        return next((entity for entity in self.data if entity.id == entity_id), None)

    def create(self, entity_create: TypeCreate) -> TypeDetail:
        data = self.model(id=uuid.uuid4(), **entity_create.model_dump())
        self.data.append(data)
        return data

    def update(self, entity_id: uuid.UUID, entity_update: TypeUpdate) -> TypeDetail:
        entity = self.get(entity_id=entity_id)
        if not entity:
            raise ValueError("Entity not found")

        for key, value in entity_update.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)

        return entity

    def delete(self, entity_id: uuid.UUID) -> None:
        self.data = [item for item in self.data if item.id != entity_id]
