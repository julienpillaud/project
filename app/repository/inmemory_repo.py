# import uuid
# from typing import Any, Generic, TypeVar
#
# EntityType = TypeVar("EntityType")
#
#
# class AbstractInMemoryRepository(Generic[EntityType]):
#     fake_data: list[EntityType]
#     key: str
#
#     def get_by_id(self, entity_id: uuid.UUID) -> EntityType | None:
#         return next(
#             (
#                 entity
#                 for entity in self.fake_data
#                 if getattr(entity, self.key) == entity_id
#             ),
#             None,
#         )
#
#     def update(
#         self, entity_id: uuid.UUID, entity_update: dict[str, Any]
#     ) -> EntityType | None:
#         entity = self.get_by_id(entity_id=entity_id)
#         if not entity:
#             return None
#
#         for key, value in entity_update.items():
#             if hasattr(entity, key):
#                 setattr(entity, key, value)
#
#         return entity
#
#     def delete(self, entity_id: uuid.UUID) -> None:
#         if entity := self.get_by_id(entity_id=entity_id):
#             self.fake_data.remove(entity)
#         else:
#             return None
