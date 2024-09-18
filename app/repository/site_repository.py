import uuid
from typing import Any

from sqlalchemy import select

from app.repository.interface import AbstractSiteRepository
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.sites.models import Site
from app.sites.schemas import SiteDetail


class SQLAlchemySiteRepository(
    SQLAlchemyRepositoryBase[Site, SiteDetail], AbstractSiteRepository
):
    model = Site
    schema = SiteDetail

    def get_by_code(self, code: str) -> SiteDetail | None:
        stmt = select(Site).where(Site.code == code)
        entity = self.session.scalars(stmt).first()
        return SiteDetail.model_validate(entity) if entity else None


class InMemorySiteRepository(AbstractSiteRepository):
    def __init__(self, data: list[SiteDetail]) -> None:
        self.data = data

    def get_all(self) -> list[SiteDetail]:
        return [SiteDetail.model_validate(entity) for entity in self.data]

    def get(self, entity_id: uuid.UUID) -> SiteDetail | None:
        return next((entity for entity in self.data if entity.id == entity_id), None)

    def get_by_code(self, code: str) -> SiteDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)

    def create(self, entity_create: dict[str, Any]) -> SiteDetail:
        entity_create["id"] = uuid.uuid4()
        data = SiteDetail.model_validate(entity_create)
        self.data.append(data)
        return data

    def update(self, entity_id: uuid.UUID, entity_update: dict[str, Any]) -> SiteDetail:
        entity = self.get(entity_id=entity_id)
        if not entity:
            raise ValueError

        for key, value in entity_update.items():
            setattr(entity, key, value)

        return entity

    def delete(self, entity_id: uuid.UUID) -> None:
        self.data = [item for item in self.data if item.id != entity_id]
