from typing import Any

from app.repository.interface import AbstractRepository, EntityType


class AbstractInMemoryRepository(AbstractRepository[EntityType]):
    fake_data: list[EntityType]
    id_counter: int = 1
    key: str

    def get_by_id(self, entity_id: int) -> EntityType | None:
        return next(
            (
                entity
                for entity in self.fake_data
                if getattr(entity, self.key) == entity_id
            ),
            None,
        )

    def get_all(self) -> list[EntityType]:
        return [self.entity.model_validate(entity) for entity in self.fake_data]

    def get(self, entity_id: int) -> EntityType | None:
        return self.get_by_id(entity_id=entity_id)

    def create(self, entity_create: dict[str, Any]) -> EntityType:
        entity_create["id"] = self.id_counter
        data = self.entity.model_validate(entity_create)
        self.fake_data.append(data)
        self.id_counter += 1
        return data

    def update(
        self, entity_id: int, entity_update: dict[str, Any]
    ) -> EntityType | None:
        entity = self.get_by_id(entity_id=entity_id)
        if not entity:
            return None

        for key, value in entity_update.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        return entity

    def delete(self, entity_id: int) -> None:
        if entity := self.get_by_id(entity_id=entity_id):
            self.fake_data.remove(entity)
        else:
            return None
