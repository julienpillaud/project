from typing import Any, Protocol, Type, TypeVar

from pydantic import BaseModel


class GenericBaseModel(BaseModel):
    id: int


EntityType = TypeVar("EntityType", bound=GenericBaseModel)


class AbstractRepository(Protocol[EntityType]):
    entity: Type[EntityType]

    def get_all(self) -> list[EntityType]: ...

    def get(self, entity_id: int) -> EntityType | None: ...

    def create(self, entity_create: dict[str, Any]) -> EntityType: ...

    def update(
        self, entity_id: int, entity_update: dict[str, Any]
    ) -> EntityType | None: ...

    def delete(self, entity_id: int) -> None: ...
