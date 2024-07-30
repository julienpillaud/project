from typing import Any, Protocol, Type, TypeVar

from pydantic import BaseModel

EntityType = TypeVar("EntityType", bound=BaseModel)


class AbstractRepository(Protocol[EntityType]):
    entity: Type[EntityType]

    def get_all(self) -> list[EntityType]: ...

    def get(self, entity_id: int) -> EntityType | None: ...

    def create(self, entity_create: dict[str, Any]) -> EntityType: ...

    def update(
        self, entity_id: int, entity_update: dict[str, Any]
    ) -> EntityType | None: ...

    def delete(self, entity_id: int) -> None: ...
